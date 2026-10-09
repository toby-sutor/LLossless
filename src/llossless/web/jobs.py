"""Submitted work, run in the background, observed separately. The job layer.

A merge takes between 23 and 4,559 seconds, measured over the graded run records in `paper/records/`.
No HTTP request holds one of those open, so the web UI cannot be a form that
posts two documents and waits for a report. It submits, gets an id back, and
watches the run through `events.py`. This module is what sits between those two
halves: a `Job` record, a `JobStore` that runs jobs on a small pool of threads,
and the retention that deletes the operator's documents when the window passes.

Four decisions here are worth a paragraph each.

**The merge sequence is written out, not wrapped.** `cli.prepare_merge`
(`cli.py:1151`) is the seam: its docstring says in as many words that it exists
for "the day a web server needed to run a merge starting from two strings
already in memory rather than from two paths on disk", and it ends by saying
that resolving settings, the client and the policy is the caller's, downstream
of it. So `run_merge` below calls the seam and then does exactly what `main`
does after it, in the same order, out of the same modules. `cli.one_merge`
(`cli.py:1258`) is the same nine lines and was considered instead; it is a
`run_sweep` helper, it does not take the `notify` channel (so a mid-run tier
move would go to a stderr nobody has open), and -- the one that decided it --
it owns the `Run`, so a `FATAL` fault on the last verify pass would take a
completed merge down with it. `cli.main` fixed exactly that defect for the
command line (`cli.py:1796`) and this path needs the same property, for more
money: the merged document is the product, and losing it to a transport blip
forty minutes in is not a failure a web deployment may have. The cost of not
wrapping is drift, and that is answered by a test rather than by a comment --
`tests/test_web_jobs.py` runs one merge through `cli.one_merge` and one through
this module against the same endpoint and requires the two reports to agree.

**Default one concurrent run.** The engine is synchronous, a hosted endpoint is
rate-sensitive, and `Settings.min_interval` paces one client rather than a
pool. More workers is a number the operator sets knowing their endpoint, never
a default this module picks for them. It is a pool rather than a single thread
so that raising it is a constructor argument and not a rewrite.

**Retention deletes the operator's documents, by default.** These are
confidential documents sitting on someone else's server; the project's stated
posture is local-first with no telemetry ever, and a queue that keeps every
uploaded file until the process restarts is the opposite of that. So the
window is a constructor argument, its default is two days, and `None` -- keep
forever -- has to be asked for. Two days is longer than the hour this shipped
with, and the trade is named where the constant is: an operator who wants the
shorter posture back sets `--retention` or `LLOSSLESS_RETENTION` and gets it,
and the page says which window it is on before anybody uploads anything.
What is deleted is everything derived from the
document as well as the document: `merged.md` is the text, `report.json` and
`report.html` quote it as evidence, and a failed step's detail can carry a
fragment of it, so the event log goes too (`events.EventLog.forget`). What
survives is a tombstone with no content in it: an id, a state, three
timestamps and an exit code, so that a browser which comes back to a
bookmarked job is told the run was forgotten rather than being shown a 404 it
cannot tell from a typo.

**A web form may not set a credential or an address.** `config.resolve` reads
the environment, and the picker needs to reach some of it -- choosing a model
is the point of having a catalogue. `REQUEST_SETTABLE` below is the allowlist,
and it is an allowlist rather than a denylist because the failure it prevents
is a variable added to `config.from_env` next year that nobody remembers to
deny. `LLOSSLESS_BASE_URL` is the one worth naming: a request that could set
it would point the server -- holding the operator's key, from the operator's
0600 file -- at a host of the submitter's choosing, and the first call would
hand the key over.

**A job belongs to whoever submitted it, and it runs on their credentials.**
`Job.owner` is an account id and `Workspace.keys` is the mapping
`config.keys_for_this_run` swaps in for the worker thread that runs it. That
seam is why this is a field and a `with` rather than a rewrite: the rule
it preserves is that no key value sits on anything `repr` or `asdict` reaches,
so the mapping is read out of the account's own file at the moment the run
starts, held as a local for the length of it, and never becomes a field on the
`Job`, the `Settings` or the provenance block. Two users running at
`workers=2` each see their own and neither sees the other's, because a
`ContextVar` is read by the thread that set it and by no other.

**A user's *addresses*, by contrast, do go into the environment a job resolves
against**, and the asymmetry is deliberate rather than an inconsistency. An
address is not a secret -- it is reported to the page and printed in the run's
own banner event -- and `endpoint_plan` below already looks for one there. A
key is, and the environment is the thing that gets copied, merged, logged
about and dumped.

**And an address is still derived rather than submitted.** `endpoint_plan`
below is what closes the gap that left: the picker set a model name and
nothing decided where that name was sent, so a hosted model's name went to
whatever endpoint the server happened to be started with and the run failed
two steps in. The plan reads each role's model, asks the catalogue which
provider serves it, and writes that provider's stored address and key variable
together. A model the catalogue does not know goes to whichever of the
operator's endpoints the request *named* -- a provider name looked up in an
allowlist, never an address -- or to the server's own default when it named
none. `REQUEST_SETTABLE` is untouched by any of it, and the plan is applied
after the request's overrides so that no ordering exists in which a submitted
value reaches an address or a key variable.
"""

from __future__ import annotations

import dataclasses
import json
import os
import queue
import re
import shutil
import sys
import threading
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path

import contextlib

try:  # POSIX; elsewhere the work directory is not locked (`_claim_work_dir`).
    import fcntl
except ImportError:  # pragma: no cover - not a platform this suite runs on
    fcntl = None

from .. import cli, config, merge
from .. import window as window_module
from ..client import Client
from ..html_report import render as render_html
from ..provenance import Provenance
from ..report import InventoryDisagrees, Run, as_dict, exit_code
from . import accounts as user_accounts
from . import catalogue, cli_render, commands, credentials, diagnose, discover
from .events import EventLog, WebConsole

# The six states. `cancelled` was considered early and rejected while nothing
# could stop a running merge, and a queued job's cancel read as a failure
# with a reason. A running merge became stoppable later, and a run somebody
# stopped on purpose is not a run that failed: the page words it differently
# and says what was billed. See `JobStore.cancel`.
#
# `interrupted` is a run that was `running` when the server stopped --
# a crash, a kill, a power cut -- found so by the next start. It is neither
# `failed` (nothing in the run went wrong) nor re-queued: re-running it
# silently would make and bill again every call it had already made, so it
# stops here and its owner decides, with Retry.
QUEUED = "queued"
RUNNING = "running"
DONE = "done"
FAILED = "failed"
CANCELLED = "cancelled"
INTERRUPTED = "interrupted"
STATES = (QUEUED, RUNNING, DONE, FAILED, CANCELLED, INTERRUPTED)
TERMINAL = frozenset({DONE, FAILED, CANCELLED, INTERRUPTED})
# What Retry is offered on: a run that did not finish for a reason other
# than its owner stopping it. A cancelled run was stopped on purpose, and a
# done one has its answer.
RETRYABLE = frozenset({FAILED, INTERRUPTED})

# One concurrent merge. See the module docstring.
DEFAULT_WORKERS = 1

# Two days from the moment a job finished. `None` means keep, and is the opt-in.
#
# **This was an hour until an earlier change, and the hour was chosen for a smaller
# scenario.** The reasoning then: long enough that an operator who started a
# merge and went to lunch still has their report, short enough that a forgotten
# browser tab does not leave a confidential document on a server overnight.
# That is still the right shape of argument and it is still the cost being
# paid; what changed is which scenario the window is sized for. An hour lost a
# real operator a finished report, and the scenario it failed is the ordinary
# one: **a run that finished at the end of one working day is still there the
# next morning.**
#
# Two days rather than one, because the window is measured from the moment the
# run finished and not from the end of a day. A 24-hour window expires at the
# same hour it started, so a run that finished at ten on Monday morning is
# already gone when the operator opens their laptop on Tuesday -- which is the
# same failure, one day later. 48 hours is the smallest window that covers a
# run finishing at *any* hour of one working day and being read at any hour of
# the next.
#
# It deliberately does not cover a weekend: Friday evening to Monday morning is
# more than sixty hours, and stretching the default that far would be sizing
# every deployment's privacy posture for the longest gap anybody might have.
# An operator who wants that says so, with `--retention` or `LLOSSLESS_RETENTION`,
# and an operator who wants the old hour back says that the same way.
DEFAULT_RETENTION_SECONDS = 172800.0

# Where an operator who has an environment but not a command line sets the
# window. A deployment under systemd or in a container edits a unit file or a
# compose file, not the argv of a process it does not spell out, and a default
# that can only be changed by a flag is a default those deployments are stuck
# with. Same units and the same two spellings as the flag -- seconds, and `0`
# or less for keep-forever -- because an operator moving the setting from one
# place to the other must not have to learn a second vocabulary.
RETENTION_ENV = "LLOSSLESS_RETENTION"

# How long before the window passes a reader should be *told* it is about to.
# A quarter of the window, capped at four hours.
#
# Derived from the window rather than fixed, because this server is run at
# `--retention 600` in a test and at two days by default, and a fixed "three
# hours" is either the whole of the first window or invisible in the second. A
# quarter is the last stretch at any scale. The cap is what keeps a long window
# from carrying a warning banner for most of its life -- at the two-day default
# a quarter would be twelve hours, and a warning that is up for half a working
# week is furniture rather than a warning. Four hours is the top of the range
# the operator asked for ("2-4 hours before deletion"), so the default lands on
# it exactly.
RETENTION_WARN_FRACTION = 0.25
RETENTION_WARN_MAX_SECONDS = 4 * 3600.0

# How often the reaper wakes. Retention is a promise about a document's
# lifetime, so it cannot be driven by request traffic: a server nobody touches
# again after the last upload is exactly the one holding a document nobody is
# coming back for. `sweep()` is also callable directly, which is how the
# suite tests the window without waiting for one.
DEFAULT_SWEEP_SECONDS = 60.0


class _FromEnvironment:
    """"Nobody has said", which is not the same answer as "keep forever".

    `retention_seconds` already spends `None` on the opt-out, so a caller that
    did not choose cannot be spelled with it, and a second meaning for `None`
    would make "keep these documents until the server stops" and "I did not
    pass the flag" the same value. One object, compared with `is`.
    """

    def __repr__(self) -> str:  # pragma: no cover - diagnostics only
        return "FROM_ENVIRONMENT"


FROM_ENVIRONMENT = _FromEnvironment()


def retention_from(environ=None) -> float | None:
    """What `LLOSSLESS_RETENTION` asks for, or the default when it says nothing.

    Seconds, and `0` or less means keep forever -- the flag's two spellings,
    unchanged, so that moving the setting into a unit file is a move and not a
    translation.

    **A value that is not a number is refused rather than ignored.** Ignoring
    it would fall back to the default, which is *longer* than almost anything
    an operator types here, so a typo in a unit file would quietly keep
    confidential documents on the server for longer than the person who wrote
    the file believes. That is the one direction this setting must not fail in.
    The caller turns the refusal into a line on stderr and a non-zero exit;
    see `server.serve`.
    """
    source = os.environ if environ is None else environ
    raw = (source.get(RETENTION_ENV) or "").strip()
    if not raw:
        return DEFAULT_RETENTION_SECONDS
    try:
        seconds = float(raw)
    except ValueError:
        raise ValueError(
            f"{RETENTION_ENV} must be a number of seconds; got {raw!r}. Use 0 "
            f"to keep runs until they are deleted.") from None
    return None if seconds <= 0 else seconds


def retention_warning_seconds(window: float | None) -> float | None:
    """How long before the window passes a reader is warned, or None when none is.

    `None` in -- retention off -- is `None` out, because there is nothing to
    warn about. See `RETENTION_WARN_FRACTION` for why this is a fraction of
    the window rather than a number of hours.
    """
    if window is None or window <= 0:
        return None
    return min(window * RETENTION_WARN_FRACTION, RETENTION_WARN_MAX_SECONDS)

# What a submitted request is allowed to put into the environment
# `config.resolve` reads. Everything else is refused by name.
#
# Two models because the picker offers a merge model and a verification model
# separately -- `config.from_env` reads `LLOSSLESS_MERGE_MODEL` for the first
# and `LLOSSLESS_MODEL` for the rest -- and the four below because they are
# the run's own parameters rather than anybody's credentials: how freely the
# merge may reword, how thoroughly the result is checked, what happens to the
# title, and the declared-loss ceiling the exit code is read against.
#
# `LLOSSLESS_VERIFY_DEPTH` is the one on this list that can make a run check
# *less*, and it is here anyway. The submitter is the person who reads the
# result: they are the one entitled to trade the invention check for three
# model calls instead of six, and a setting the server holds for them would
# make that decision for every run on the box. What stops it being a quiet
# downgrade is that nothing about it is quiet -- the depth is in the run's
# banner, in its provenance block, in two skipped steps naming what was not
# asked, and in a sentence on the verdict itself.
#
# `LLOSSLESS_WINDOW` is `--window`: the context window the submitter states
# for a model the catalogue does not know, sent to an endpoint that cannot
# report one. A vendor has no `/api/ps`, so without it every check
# refuses after the merge has run. It is a number, bounded below by
# `STATED_WINDOW_MIN` and above by `STATED_WINDOW_MAX`, and it names no
# address, key or path. It is never a guess: the run records it as stated, in
# the banner and the Provenance block, and the guard is only as true as the
# figure -- which is the CLI's arrangement, offered to the person who typed
# the model id. `endpoint_plan` refuses a vendor-bound unknown model without
# one, and `route_plan` refuses one beside a command route, whose own file
# states the window.
#
# Deliberately absent, each for its own reason rather than by oversight:
#
#   LLOSSLESS_BASE_URL*      an address. See the module docstring.
#   LLOSSLESS_API_KEY_ENV*   names the variable a key is read from, so
#                             setting it aims the server's own environment.
#   LLOSSLESS_CA_BUNDLE      a path, read from disk, chosen by a submitter.
#   LLOSSLESS_CACHE_DIR      a path the server writes to. Forced below anyway.
#   LLOSSLESS_THINKING       a quality decision, not a preference: suppressing
#                             reasoning on a model that reasons changes what is
#                             being measured, and the operator owns that.
#   LLOSSLESS_STRUCTURED     pins the request tier for the whole client and
#                             persists a probe result; an operator's call.
REQUEST_SETTABLE = frozenset({
    "LLOSSLESS_MODEL",
    "LLOSSLESS_MERGE_MODEL",
    "LLOSSLESS_FIDELITY",
    "LLOSSLESS_VERIFY_DEPTH",
    "LLOSSLESS_TITLE_POLICY",
    "LLOSSLESS_LOSS_BUDGET",
    "LLOSSLESS_WINDOW",
})

# The bounds on a stated window, in tokens. A request is checked against
# them; `--window` and `LLOSSLESS_WINDOW` on the server are not, because the
# operator who sets those can read the refusal in their own terminal.
#
# The floor: `prompts/merge.md` alone is 11,166 characters, about 3,700 tokens
# at the 3-characters-per-token prose figure, so a smaller window refuses every
# merge before a document is added. It also catches "200" typed for 200,000.
# The ceiling catches a figure with zeros to spare: fifty times the largest
# window the catalogue states (200,000).
STATED_WINDOW_MIN = 4_096
STATED_WINDOW_MAX = 10_000_000


def stated_window_refusal(raw) -> str | None:
    """Why `raw` is not a window a request may state, or None when it is.

    One rule for both callers: `api._overrides` answers a 400 `bad_window` with
    this sentence, and `MergeRequest` refuses the same value for any caller
    that builds a request without the API. Names the field a submitter sets.
    """
    text = str(raw).strip()
    if not text.isdigit() or not STATED_WINDOW_MIN <= int(text) <= STATED_WINDOW_MAX:
        return (f"window is the context window the model is served with, as a "
                f"whole number of tokens from {STATED_WINDOW_MIN:,} to "
                f"{STATED_WINDOW_MAX:,}; got {text!r}. The figure is on the "
                f"vendor's page for the model.")
    return None

# `LLOSSLESS_COMMAND` is deliberately not on the list above, and it is the one
# absence worth its own paragraph rather than a line in the block of reasons.
#
# It names a program this server runs, with the prompt on its stdin. A request
# that could set it would be a request that executes arbitrary code on this
# box, and no validation of the string turns that into something else -- the
# flag is safe on the command line because whoever types it already has a
# shell, and a form reachable over HTTP is not in that position.
#
# What replaces it is `web/commands.py`: the operator writes the routes into a
# file only they can write, a request names one by **id**, and the server
# supplies the command from its own file. Same shape as `endpoint_plan` one
# mechanism over -- choose among the operator's, never describe one.
#
# Asserted rather than left to this comment. The failure being prevented is a
# later edit adding it to the allowlist in the belief that it is a setting like
# the others above, and a comment does not fail a suite.
assert "LLOSSLESS_COMMAND" not in REQUEST_SETTABLE
assert "LLOSSLESS_COMMAND_LABEL" not in REQUEST_SETTABLE

# The one variable a request's `effort` becomes, written by `route_plan`
# after it has checked the route can carry a level. Not on `REQUEST_SETTABLE`:
# an override would reach an HTTP run too, where `effort_ignored` drops it.
EFFORT_MERGE_VARIABLE = "LLOSSLESS_EFFORT_MERGE"
assert EFFORT_MERGE_VARIABLE not in REQUEST_SETTABLE

# What a cancel says. The status poll's `error` for a cancelled job, and
# the event a running one gets when the cancel is asked for.
CANCELLED_QUEUED = "cancelled before it started; no model was called"
CANCEL_ASKED = ("cancel asked for: no further model call will be made, and a "
                "call in progress is abandoned")


def cancelled_error(job: Job, exc: BaseException) -> str:
    """The `error` of a running job that was cancelled: what ran and was billed.

    The calls are the run's own count, from the report `publish` wrote on the
    way out, so the number is the one the report carries. A call abandoned in
    flight is in it: it was sent, and the provider may bill it.
    """
    counts = ((job.report or {}).get("provenance") or {}).get("counts") or {}
    calls = counts.get("calls")
    made = (f"{calls} model call(s) were made before it stopped"
            if isinstance(calls, int) else "the number of model calls made is unknown")
    return (f"cancelled: {made}. Calls already made are billed and cannot be "
            f"undone. {type(exc).__name__}: {exc}")


# The three files a finished job leaves behind, named here so that retention
# and the download routes agree with the writer about what exists.
REPORT_JSON = "report.json"
MERGED_MD = "merged.md"
REPORT_HTML = "report.html"

# The two a job writes from the moment it is accepted, so that a restart
# can resume it: the documents as submitted, with their labels and the base,
# and the event log as it is emitted. Both in the job's own directory, so the
# `rmtree` retention already does deletes them with everything else.
SOURCES_JSON = "sources.json"
EVENTS_JSONL = "events.jsonl"

# The job index: one file in the work directory, naming every job this
# server holds, its owner, state, timestamps and settings -- never a document,
# a label or a key. See `JobStore._load`.
INDEX_JSON = "index.json"
INDEX_TEMP = ".index.json.tmp"
# Held with `flock` for as long as a store owns the work directory. The
# kernel drops it when the process dies, however it dies, so a crash never
# leaves it stale.
LOCK_FILE = ".lock"
INDEX_VERSION = 1
# What a job directory is called: its id, which is what `_load` may delete when
# no index entry names it. Nothing else in the work directory matches.
JOB_ID = re.compile(r"\A[0-9a-f]{32}\Z")

# Owner-only, on both the directory and the files inside it. The work directory
# holds the operator's documents and everything quoted out of them, and a
# self-hosted box is frequently a shared one. `os.open` with the mode rather
# than `write_text` then `chmod`: the second leaves a window, however short, in
# which the file exists at whatever the process umask allows.
DIR_MODE = 0o700
FILE_MODE = 0o600


class IndexUnreadable(RuntimeError):
    """The job index exists and cannot be read. The server refuses to start.

    Not "start with an empty list", and the choice is deliberate. The
    index is written to a temporary file, synced and renamed over the old one,
    so a crash leaves the old file or the new one and never a torn one: an
    index that does not parse is a disk fault or a hand edit, which somebody
    should look at. Starting empty would drop every retained run from its
    owner's list without a word, and would leave the job directories it named
    with no record of when their windows end -- kept forever, which breaks the
    retention promise, or deleted at once, which destroys the reports people
    came back for. Either is a decision about other people's documents, and it
    belongs to the operator, who makes it by moving the file aside.
    """

    def __init__(self, path: Path, reason: str) -> None:
        self.path = path
        self.reason = reason
        super().__init__(
            f"the job index {path} cannot be read ({reason}). Nothing was "
            f"started, and no run it names was deleted. To start with an empty "
            f"run list instead, move that file aside: the next start then "
            f"deletes every job directory in {path.parent} that no index names, "
            f"with the documents and reports in them.")


class WorkDirBusy(RuntimeError):
    """Another live server owns this work directory. Refused before anything is read.

    Two processes on one index would each believe the other's running jobs
    had been interrupted, run each other's queued jobs, and overwrite each
    other's index -- every one of those a run billed twice or a document kept
    past its window. One owner, enforced by a lock the kernel releases when
    that owner dies.
    """

    def __init__(self, path: Path) -> None:
        self.path = path
        super().__init__(
            f"another llossless server is already using the work directory "
            f"{path}. Stop that one first, or start this one with its own "
            f"--work-dir.")


class EffortRefused(ValueError):
    """A request's `effort` this server cannot carry. `400 bad_effort`.

    Its own class so the API can name the field: a level asked for with no
    command route, on a route whose program takes no `--effort`, or on a route
    whose command already states one, is a fact about the one field, and a
    generic refusal would leave the submitter to guess which part of the
    request it was about. Not a subclass of `JobRefused`, so no handler that
    catches that one can fold this into it.
    """


class JobRefused(ValueError):
    """The request was refused before any work started.

    A `ValueError` because it is always a fact about what the caller sent --
    too few documents, a base naming a document that is not there, an
    environment override that is not on the allowlist. The page renders these as a
    400 with the message shown to the operator, so the messages are written to
    be read by a person rather than by a log scraper.
    """


@dataclass(frozen=True)
class MergeRequest:
    """Two or more documents in memory, and what to do with them.

    `documents` is keyed however the caller likes -- an uploaded filename, a
    label typed into a form -- and **insertion order is the order the sources
    are given**, exactly as `prepare_merge` treats it and exactly as `main`
    treats `argv`. The keys are thrown away at the seam and replaced with
    `source_a.md`, `source_b.md` and so on, because every figure this project
    has published was measured with those names in the prompt; the caller's own
    key survives only in `run.paths`, which is what the report displays.

    `base` names one of those keys, not a canonical name and not an index: the
    operator picked a file in a form and should be told about their own choice
    in their own words if it is wrong. It is translated by position in
    `canonical_base` below.

    `overrides` is the part of the environment the form is allowed to set. See
    `REQUEST_SETTABLE`.
    """

    documents: dict[str, str]
    base: str | None = None
    overrides: dict[str, str] = field(default_factory=dict)
    # Which of the operator's configured endpoints a model the catalogue does
    # not know about should be sent to. A provider *name*, looked up in
    # `credentials.PROVIDERS`, and never an address: a request that could name
    # an address would be a request that aims this server, and the whole point
    # of the allowlist below is that it cannot. A catalogue model ignores this
    # -- its provider is a fact about the model, not a choice -- and `None`
    # means the endpoint this server was started with, which is what a
    # hand-typed model name has always gone to.
    endpoint: str | None = None
    # Which of the operator's command routes should answer this run, by **id**.
    # Never a command: see the paragraph on `REQUEST_SETTABLE` above, and
    # `web/commands.py` for the whole of the arrangement. `None` is the
    # ordinary case and means answer over HTTP, which is every run this tool
    # has ever made.
    #
    # A *sibling* of `endpoint` rather than a value it can take, because the
    # two are different questions with different answers: `endpoint` chooses
    # among addresses for a model the catalogue does not know, and this chooses
    # a different mechanism entirely. `resolved_environ` refuses a request that
    # names both.
    route: str | None = None
    # The merge role's effort level, chosen by the submitter on a command
    # route. One of `commands.EFFORT_CHOICES`, or `None` for the route's
    # own default. Not an override: `LLOSSLESS_EFFORT*` stays off
    # `REQUEST_SETTABLE`, and `route_plan` writes the one variable this maps to
    # only after it has checked the route can carry it.
    effort: str | None = None

    def __post_init__(self) -> None:
        # The allowlist is applied here, at construction, so that a refusal
        # reaches the caller before a job id exists and before anything is
        # written to disk. Not the document count, and not the base: those are
        # checked in `JobStore.submit`, because `retention` rebuilds this
        # object with `documents={}` when it forgets a job, and a constructor
        # that refused an emptied request would make forgetting impossible.
        refused = sorted(set(self.overrides) - REQUEST_SETTABLE)
        if refused:
            raise JobRefused(
                f"a submitted request may not set {', '.join(refused)}. "
                f"The settings a request may choose are "
                f"{', '.join(sorted(REQUEST_SETTABLE))}; everything else -- "
                f"the endpoint address, the variable an API key is read from, "
                f"the paths this server reads and writes -- belongs to whoever "
                f"runs the server, not to whoever submits to it.")
        if "LLOSSLESS_WINDOW" in self.overrides:
            refusal = stated_window_refusal(self.overrides["LLOSSLESS_WINDOW"])
            if refusal:
                raise JobRefused(refusal)
        if self.endpoint is not None:
            # Checked at construction for the same reason the allowlist is:
            # the refusal has to reach the caller before a job id exists.
            # `check_provider` looks the name up in an allowlist and never
            # builds anything out of it, which is what keeps a `{name}` off
            # the URL from becoming a path or an address.
            credentials.check_provider(self.endpoint)
        if self.route is not None:
            # The *shape* here and the lookup later, which is the split this
            # object forces: a `MergeRequest` has no store to look an id up in,
            # and giving it one would put the operator's command file behind
            # every object a request is parsed into. What a constructor can do
            # is refuse anything that is not an id at all, before a job exists.
            commands.check_route_id(self.route)
        if self.effort is not None:
            # The shape here, the route later, for `route`'s reason one
            # paragraph up: whether a route can carry a level needs the
            # operator's file, and this object has none.
            if self.effort not in commands.EFFORT_CHOICES:
                raise EffortRefused(
                    f"effort is the merge's effort level, one of "
                    f"{', '.join(commands.EFFORT_CHOICES)}; got {self.effort!r}.")
            if self.route is None:
                raise EffortRefused(
                    f"effort {self.effort!r} was sent without a command_route. "
                    f"An effort level is a flag on a subscription program's "
                    f"command line, so it applies only to a command route; an "
                    f"HTTP endpoint has no level to be asked for.")
        object.__setattr__(self, "overrides", dict(self.overrides))


@dataclass(frozen=True)
class Workspace:
    """Where one job may write, and the environment it resolves settings from.

    Passed to the runner rather than reached for, for the reason `cli.step`
    takes a console rather than importing one: this is the only object a runner
    needs from the store, and a runner that reached back into the store would
    be a second place the store's invariants could be broken from.
    """

    directory: Path
    # Shared by every job, and writable. `Client.__init__` opens
    # `settings.cache_dir / "capabilities.json"` unconditionally
    # (`client.py:364`), so a read-only cache directory is not a degraded mode,
    # it is a client that cannot be constructed. Shared rather than per-job
    # because what it holds is a fact about the endpoint -- which structured
    # tier it accepts -- and re-probing that once per upload would spend a call
    # per job to learn something that did not change.
    cache_dir: Path
    environ: dict[str, str]

    # Where this job's credentials come from: a zero-argument callable
    # returning the mapping `config.keys_for_this_run` is handed, or `None`
    # for "do not swap the source at all".
    #
    # **A callable rather than the mapping itself**, and that is the whole of
    # why this field is shaped oddly. `Workspace` is a frozen dataclass with a
    # generated `repr`, and a dict of API keys as a field is a dict of API keys
    # in a traceback, a debugger and every log line that formats a workspace.
    # A function's `repr` is its name. The values are read once, together with
    # the addresses in `environ`, and it hands back that one reading.
    #
    # `None` and `{}` are different answers and the difference is load-bearing:
    # `None` leaves `os.environ` in place, which is every CLI run and every
    # recorded cassette, and `{}` says this account has no credentials, which
    # is what stops a user with nothing configured from spending the
    # operator's key. A run `JobStore` starts with no mapping of its own gets
    # a `StandingKeys` in place of `None`: the same environment, read the
    # same way, for as long as the run's addresses stand.
    keys: object = None

    # The operator's command routes, or `None` for a server that has none.
    #
    # A store rather than the resolved command, and that is the same shaped
    # decision as `keys` above for a different value: the command string must
    # not become a field on anything the job layer keeps, because this is a
    # frozen dataclass with a generated `repr` and a command is a local path as
    # often as not. `commands.Commands` answers its own `repr` with a path and
    # a class name.
    #
    # `None` and an empty store are the same answer here -- no routes -- and
    # unlike `keys` there is no third state, because there is nothing to leave
    # unswapped: a request that names no route resolves over HTTP exactly as
    # every run before this one did.
    routes: object = None

    # The addresses this run's submitter may be shown in full: the ones they
    # stored themselves. `None` is no restriction, which is the operator and
    # a server with no accounts. Every other address a member's run uses is
    # the operator's, and the command-line panel and the report give it as
    # scheme, host and port (`accounts.reduced`).
    own_addresses: object = None


class StandingKeys:
    """This process's own keys, each handed to a run only while its address stands.

    The key source of a run that has no mapping of its own: the operator's,
    and every run on a server with no accounts. Their credentials are the
    process environment, read at send time, which is what lets a key the
    operator replaces reach a merge that is already running.

    Read like that with nothing else, it also let a key reach an address it
    was never saved with. A run resolves its addresses once, when it starts.
    If the operator then moved that provider's endpoint and saved a key for
    the new address, the run went on calling the old address and was handed
    the new key on its next call.

    So a provider's key is handed out only while the provider's address in
    the server's environment is still the one this run started with. The same
    address with a new key is a replaced key, and it is used. A different
    address means the key now in the environment belongs somewhere else, and
    the run gets none.

    Holds no key. It reads `os.environ` when asked, as an unswapped run does.
    `read` replaces that reading for a member's run, whose view of the
    operator's keys is `accounts.Directory.shared_keys` and not the process's
    whole environment.

    `credentials.NO_KEY_ENV` is never read: it is the name a role is pointed
    at when it must send no key, whatever a process happens to have exported.
    """

    def __init__(self, live: dict[str, str], started: dict[str, str],
                 read=None) -> None:
        self._live = live
        self._read = read
        self._started = {
            variable: (credentials.url_env(name),
                       started.get(credentials.url_env(name)))
            for name, variable in credentials.PROVIDERS.items()}

    def __repr__(self) -> str:
        """Neither a key nor an address."""
        return "StandingKeys()"

    def get(self, name: str, default=None):
        # The key first and the address second. `Credentials.apply` moves an
        # address before it writes the key stored with it, so a key read
        # here that belongs to a new address is always followed by a check
        # that sees the new address.
        if name == credentials.NO_KEY_ENV:
            return default
        value = os.environ.get(name) if self._read is None else self._read(name)
        stood = self._started.get(name)
        if stood is not None and self._live.get(stood[0]) != stood[1]:
            return default
        return default if not value else value


class MemberKeys:
    """A member's key source for one run: their own keys, and the operator's while they stand.

    A member's run was handed a plain mapping, read once when the run
    started. That is right for the member's own keys and wrong for the
    operator's: a shared key the operator deleted while the run was under
    way went on being sent on every later call, where the operator's own run
    stopped. So the variables that are the operator's (`shared`) are read
    through a `StandingKeys`: the key the operator's file and environment
    hold now, and only while that provider's address is the one this run
    started with.

    `addresses` is not a key. It is the set of addresses the member stored
    themselves, kept beside the keys because both come out of the one read
    of the member's file that `JobStore.resolved_for` makes.

    Any other name answers nothing: a member's run reads no variable of the
    server's environment but the operator's provider keys.
    """

    def __init__(self, own: dict[str, str], shared, standing: StandingKeys,
                 addresses=frozenset()) -> None:
        self._shared = frozenset(shared)
        self._own = {name: value for name, value in own.items()
                     if name not in self._shared}
        self._standing = standing
        self.addresses = frozenset(addresses)

    def __repr__(self) -> str:
        """Neither a key nor an address."""
        return "MemberKeys()"

    def get(self, name: str, default=None):
        if name in self._shared:
            return self._standing.get(name, default)
        value = self._own.get(name)
        return default if not value else value


# The exit code of a run with no verdict a reader can act on: `report.exit_code`'s
# own 2, which is what the command line returns for the same refusal.
INCONCLUSIVE = 2


class Inconclusive(Exception):
    """The run ended with no verdict, for a reason that is a sentence.

    Raised by `publish` when the report refuses to be written. The worker
    lands the job in `failed` with exit code 2 and this message as it is,
    with no exception name in front of it.
    """


class Job:
    """One submitted merge, its state, its result and its event log.

    Not a dataclass: the state and the three timestamps are written by a worker
    thread and read by HTTP threads, and the store's lock is what makes that
    safe. Keeping the mutation behind `JobStore` methods rather than behind
    attribute assignment anybody can reach is the difference between a rule and
    a convention.

    `run` and `report` are the same result twice -- the `Run` object for
    anything in-process that wants to ask it a question, and the dict
    `report.as_dict` produced for anything that wants to serve it. They are
    both here rather than one being derived on demand because `as_dict` walks
    the whole run and a status poll should not.
    """

    __slots__ = ("id", "request", "owner", "state", "created_at", "started_at",
                 "finished_at", "forgotten_at", "run", "report", "exit_code",
                 "error", "events", "directory", "document_count", "stop",
                 "retry_of", "cli_equivalent")

    def __init__(self, request: MergeRequest, *, now: float,
                 owner: str = "", job_id: str | None = None,
                 retry_of: str | None = None) -> None:
        # uuid4, not a counter and not a hash of the documents. A counter tells
        # a visitor how many documents this server has processed and lets them
        # guess the id of somebody else's; a content hash is an oracle for
        # whether a given document was ever submitted here. `job_id` is for a
        # job read back from the index after a restart, and nothing else.
        self.id = uuid.uuid4().hex if job_id is None else job_id
        # The run this one is a Retry of, by id, or None. A link, not a
        # dependency: the old run may be forgotten first.
        self.retry_of = retry_of
        self.request = request
        # Which account submitted this, as an opaque id and never a username.
        # `` on a server with no account store, which is the single-tenant
        # arrangement and means every job belongs to everybody -- `api.Api._owns`
        # compares against `` for a caller with no identity, so the two sides
        # agree by construction rather than by a special case.
        #
        # An id rather than a name because a name can be changed and a
        # directory cannot be renamed under a running job, and because nothing
        # in this package ever builds a path out of a username.
        self.owner = owner
        self.state = QUEUED
        self.created_at = now
        self.started_at: float | None = None
        self.finished_at: float | None = None
        self.forgotten_at: float | None = None
        self.run: Run | None = None
        self.report: dict | None = None
        self.exit_code: int | None = None
        self.error: str | None = None
        self.events = EventLog()
        self.directory: Path | None = None
        # Kept separately so the tombstone can still say how many documents
        # there were after the documents themselves are gone. A count is not
        # content; the labels are, which is why they are not kept -- a filename
        # is frequently the most sensitive line in a confidential document.
        self.document_count = len(request.documents)
        # Set by `JobStore.cancel`. The run's `Client` holds it and makes
        # no call once it is set; a command backend stops its program.
        self.stop = threading.Event()
        # The CLI-equivalent block (`cli_render.render`), set once `web_settings`
        # has resolved -- while the job is `running`, off the same `Settings`
        # object the pipeline is about to be handed, and never off the request
        # or the page's controls. `None` until then, and for a job that failed
        # before settings resolved: there is no settings object to render.
        self.cli_equivalent: dict | None = None

    @property
    def forgotten(self) -> bool:
        return self.forgotten_at is not None

    @property
    def terminal(self) -> bool:
        return self.state in TERMINAL

    @property
    def retryable(self) -> bool:
        """Can Retry start a new run from this one's documents?"""
        return (self.state in RETRYABLE and not self.forgotten
                and bool(self.request.documents))

    def status(self) -> dict:
        """The status poll's payload: state, timing, the outcome, and nothing quoted.

        The page serves this from a route anyone who has the id can reach, so what is
        in it is a decision rather than a dump. The report and the merged
        document are their own routes, because they are the operator's text and
        a status endpoint that included them would put a document in every
        polling response and in every proxy log along the way.

        **`error` is the one field that can carry a fragment of a document, and
        it is here deliberately.** It is `f"{type(exc).__name__}: {exc}"` from
        whatever raised, and an exception raised while parsing a model's answer
        about a document can quote it. The alternative is a failed job whose
        only account of itself is the word `failed`, which is the failure this
        whole layer exists to avoid -- so it stays, and this paragraph is the
        disclosure rather than a docstring claiming a guarantee that is not
        true. Everything else here is a state name, a timestamp, an integer or
        a count.
        """
        return {
            "id": self.id,
            "state": self.state,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "forgotten_at": self.forgotten_at,
            "exit_code": self.exit_code,
            "error": self.error,
            "documents": self.document_count,
            "events": len(self.events),
            # A cancel was asked for. True on a running job between the
            # request and the stop, and on every job that was cancelled.
            "cancel_requested": self.stop.is_set(),
            # How many model calls the run made, once its report exists: the
            # report's own count, so the page can say what a cancel left
            # billed. None before then, and for a run cancelled while queued.
            "calls_made": (((self.report or {}).get("provenance") or {})
                           .get("counts") or {}).get("calls"),
            # The run this one retried, and whether this one can be retried:
            # its documents are still held and it did not finish.
            "retry_of": self.retry_of,
            "retryable": self.retryable,
        }


# --------------------------------------------------------------------------
# turning a request into a run
# --------------------------------------------------------------------------


def canonical_base(request: MergeRequest) -> str | None:
    """Which canonical name the caller's `base` label picks out, or None.

    By position, because that is how `prepare_merge` renames: it zips
    `merge.source_names(len(documents))` onto `documents.values()`, so the nth
    key the caller inserted becomes the nth canonical name. `cli.canonical_base`
    (`cli.py:629`) answers the same question for the command line and cannot be
    reused here -- it resolves filesystem paths, and the web path's keys are
    labels that name no file.

    None in means None out, and that is not a missing value: it is the operator
    declining to say, which `merge` records as `DEFAULTED` and the report
    prints, because with no explicit base the document governing the merged
    structure is decided by what the files happened to be called.
    """
    if request.base is None:
        return None
    labels = list(request.documents)
    if request.base not in labels:
        raise JobRefused(
            f"the base document {request.base!r} is not one of the documents "
            f"submitted ({', '.join(repr(label) for label in labels)}). The "
            f"base is the document whose structure the merge follows, so it "
            f"has to be one of the documents being merged.")
    return merge.source_names(len(labels))[labels.index(request.base)]


def request_environ(workspace: Workspace, request: MergeRequest) -> dict[str, str]:
    """The server's environment with the request's allowlisted settings over it.

    A fresh dict rather than a mutation of the server's own: two jobs run
    concurrently at `workers=2` and would otherwise be choosing each other's
    model. `MergeRequest.__post_init__` has already refused anything not on the
    allowlist, and it is checked again here rather than trusted, because this
    function is also the one a future caller would reach for when building an
    environment by hand.
    """
    refused = sorted(set(request.overrides) - REQUEST_SETTABLE)
    if refused:
        raise JobRefused(f"a submitted request may not set {', '.join(refused)}")
    return resolved_environ(request, workspace.environ, routes=workspace.routes)


def resolved_environ(request: MergeRequest, base: dict[str, str],
                     *, routes=None) -> dict[str, str]:
    """`base`, with the request's allowlisted settings and the backend plan over it.

    Split out from `request_environ` because `JobStore.submit` needs the same
    answer without a workspace: the refusal "this server cannot reach that
    model" has to be a 400 about the request rather than a job that is
    accepted, queued, started and then failed, and a second implementation of
    the merge order would be a second thing to keep in step with this one.

    The plan goes on **after** the request's own overrides, not before. The
    variables it writes -- an address and the name of a key variable, per role
    -- are exactly the ones `REQUEST_SETTABLE` refuses, and ordering it last
    means there is no sequence in which a submitted value reaches one of them.
    It is derived from the request's models, which is why it cannot simply be
    computed first.

    **A run answers over HTTP or through a command, never both**, so the two
    plans are an `if`/`else` rather than two updates that happen not to
    collide. A command backend addresses nothing, so planning an endpoint for
    it would write per-role addresses and key variables into the environment of
    a run that contacts none of them: the same fault, reintroduced one layer
    down, and would refuse the request outright whenever the route's model
    happens to share a name with a catalogue row whose provider has no endpoint
    configured. `Opus 5 - Subscription` on a server with no Anthropic key is
    exactly that case, and it is the case this milestone exists for.

    The route resolves **after** the request's own overrides for the reason the
    endpoint plan does, and for one more: the route decides the model, and a
    request that both picked a row in the table and named a route would
    otherwise run half on each.
    """
    refused = sorted(set(request.overrides) - REQUEST_SETTABLE)
    if refused:
        raise JobRefused(f"a submitted request may not set {', '.join(refused)}")
    environ = dict(base)
    environ.update(request.overrides)
    if request.route is not None:
        environ.update(route_plan(request, routes))
    else:
        environ.update(endpoint_plan(request, environ))
    # **`sourced` refuses here rather than at the first call.** The level
    # asks the model to go and look a fact up, and a backend that cannot be
    # granted a web tool would answer it from recall and label the answer
    # retrieved -- which a reader cannot tell apart from the real thing, since
    # the two runs cite the same source in near-identical words. `config` owns
    # the rule so the command line and this server refuse on the same
    # predicate; what is added here is the route's own id, because "this server
    # cannot retrieve" and "the row you picked cannot" are different repairs.
    #
    # After both plans, and that is the point: this is the one check that has
    # to read the backend the run will really use, and the route is what
    # decides that. Before a job id exists, for `resolved_environ`'s own
    # reason -- a refusal an operator meets after the work was accepted is a
    # refusal they meet in a log.
    refusal = config.retrieval_refusal(
        config.canonical_fidelity(environ.get("LLOSSLESS_FIDELITY", "")
                                  or config.DEFAULT_FIDELITY),
        environ.get("LLOSSLESS_COMMAND", ""))
    if refusal is not None:
        raise JobRefused(
            refusal + (f" This request named command_route {request.route!r}."
                       if request.route is not None else ""))
    return environ


def route_plan(request: MergeRequest, routes=None) -> dict[str, str]:
    """Which command answers this run. Resolved from an id, against the operator's file.

    **The request carries an id and this function supplies the command.** That
    is the whole of the arrangement and the reason `LLOSSLESS_COMMAND` is not
    on `REQUEST_SETTABLE`: a web form that accepts a command and a server that
    runs it is remote code execution, whatever the string is checked against.
    See `web/commands.py`.

    An unknown id is a refusal naming the field, never a fallback. A submitter
    who names a route this server does not have has said something about where
    their documents were going, and answering the request some other way is
    answering a question they did not ask -- with the money already spent by
    the time anybody notices.

    A server with no command routes refuses every id, including a
    well-formed one, and says so as a fact about this server rather than about
    the request. That is the empty default doing its job: out of the box there
    is no route, so there is nothing an id can resolve to.

    Refuses a request that names a route **and** a model. The route decides
    which model is recorded -- it is one row in the picker, not a model with a
    switch beside it -- so a request carrying both is a page and a request that
    disagree, and the one thing that must not happen is picking one of them
    silently. This is the check that fires when a browser shows a subscription
    selected and sends something else.
    """
    if routes is None:
        routes = commands.NoCommands()
    named = sorted(set(request.overrides)
                   & {"LLOSSLESS_MODEL", "LLOSSLESS_MERGE_MODEL",
                      "LLOSSLESS_WINDOW"})
    if named:
        raise JobRefused(
            f"this request names command_route {request.route!r} and also sets "
            f"{', '.join(named)}. A command route is a whole row in the picker "
            f"-- it decides which program answers, which model the run is "
            f"recorded under and the window it states -- so a request that "
            f"carries both is a page and a request that disagree about where "
            f"the documents are going. Choose the route or choose a model, not "
            f"one of each.")
    if request.endpoint is not None:
        raise JobRefused(
            f"this request names command_route {request.route!r} and also "
            f"names the {request.endpoint} endpoint. A command route contacts "
            f"no endpoint at all, so one of the two describes a run that is "
            f"not going to happen.")
    try:
        route = routes.get(request.route)
    except commands.UnknownRoute:
        # Deliberately **not** wrapped in a `JobRefused`. Both are refusals
        # before a job id exists, but they are different answers to a caller:
        # `api.submit` gives this one its own error code so a page can say
        # "this server has no such route" rather than repeating a generic
        # refusal, and wrapping it here is what made it indistinguishable.
        raise
    except commands.CommandsError as refusal:
        # The file itself is unusable -- a mode, a shape, a parse. That is a
        # fact about this server rather than about the request, and it is
        # reported as one: the routes are all unavailable, not merely this one.
        raise JobRefused(str(refusal)) from None
    plan = route.environ()
    if request.effort is not None:
        # The requester's merge level, as the variable `--effort merge=LEVEL`
        # reaches, so it goes onto the argv through `command_for` like
        # any level. Refused where the route cannot carry it rather than
        # dropped: `effort_ignored` would name it after the run, and a level
        # chosen on a slider that the run then ignored is the case to stop at
        # the door.
        if request.effort not in route.effort_levels:
            raise EffortRefused(
                f"command_route {request.route!r} takes no effort level from a "
                f"request: its program is not one whose --effort flag this "
                f"build has read, or its own command already names a level, "
                f"which wins. Send the request without effort.")
        plan[EFFORT_MERGE_VARIABLE] = request.effort
    return plan


def endpoint_plan(request: MergeRequest, environ: dict[str, str],
                  catalogue_path=None) -> dict[str, str]:
    """Which endpoint each role's model is served from. Derived, never submitted.

    This is the answer to a defect the picker shipped with: it set a model
    *name* and nothing else, the address came from the server's own
    environment, and nothing connected the two. Choosing a hosted model on a
    server pointed at a local endpoint produced a run that failed two steps in
    with "no model named ... loaded" -- a message about a model the operator
    had not typed, arriving after the documents were uploaded.

    The rule is one sentence: **a model is sent to the endpoint stored for its
    provider, and to nowhere else.** The provider of a catalogue model is a
    fact about the model rather than a choice, so it is read here and the
    request has no say in it. The provider of a model this catalogue has never
    heard of -- a name the operator typed, or one an endpoint listed for
    itself -- is `request.endpoint`, which names one of the operator's own
    configured endpoints by provider name and can name nothing else. A request
    that names none is the case that has always worked and still does: the
    endpoint this server was started with.

    **Nothing here reads an address out of the request**, and that is the
    invariant `REQUEST_SETTABLE` states from the other side. The addresses
    come from the server's own environment, under `credentials.url_env`, put
    there by the operator's `0600` file or by whatever started the server. A
    submitter chooses among the operator's endpoints; they never describe one.

    The key variable is written in the same statement as the address, out of
    the same provider name, so an environment cannot come out of this function
    holding an address from one provider and a key variable from another.

    Refuses rather than falling back when a catalogue model's provider has no
    endpoint. The fallback is the defect: it is what sent a hosted model's name
    to a local endpoint in the first place, and the operator is better served
    by being told the model is unreachable before they wait for it.
    """
    try:
        settings = config.resolve(None, environ=environ)
    except config.ConfigError:
        # Nothing to plan against, and this is not the place to say so. An
        # environment `resolve` refuses is refused again by `web_settings`
        # with the same message it always gave -- raising it here instead
        # would move a configuration error from a run that reports it to a
        # submit that answers 500, which is a worse answer to the same
        # question.
        return {}
    plan: dict[str, str] = {}
    profiles: set[str] = set()
    derived: set[str] = set()
    for role in cli.ROLES:
        try:
            model = settings.model_for(role)
        except config.ConfigError:
            # No model configured for this role. There is nothing to route,
            # and the engine already refuses a run with no model, at the point
            # where refusing is its job. Found by the suite's own fresh-tree
            # replay, which stands where an installed user stands: no
            # `models.local.json`, no `LLOSSLESS_MODEL`, and every submit
            # answering 500 instead of the 400 it used to.
            continue
        entry = catalogue.for_api_model(model, catalogue_path)
        # Three sources, in order of how much they know. A catalogue row knows
        # its provider as a fact. An endpoint that listed this model knows it
        # as something it said about itself. Only after both come up empty is
        # the model a name somebody typed, and only then does the request get
        # to say where it goes.
        provider = (entry["provider"] if entry else
                    credentials.provider_serving(model, environ)
                    or request.endpoint)
        if not provider:
            continue
        url = (environ.get(credentials.url_env(provider)) or "").strip()
        if not url:
            raise JobRefused(
                f"{model} is served by {provider}, and this server has no "
                f"endpoint configured for {provider}. A model is only ever "
                f"sent to the endpoint stored for its provider, so there is "
                f"nowhere for this request to go. Set the {provider} endpoint "
                f"on the credentials sheet, or choose a model whose provider "
                f"does have one.")
        suffix = role.upper()
        plan[f"LLOSSLESS_BASE_URL_{suffix}"] = url
        plan[f"LLOSSLESS_API_KEY_ENV_{suffix}"] = credentials.PROVIDERS[provider]
        # The served window, from the row that already records it.
        #
        # `config.DEFAULT_WINDOW` is `None`, meaning "ask the endpoint", and
        # asking means `GET /api/ps`, which is ollama's route and nobody
        # else's. A vendor endpoint answers 404, `window.preflight` raises
        # `WindowUnmeasurable`, and **every decompose step refuses** -- while
        # `merge` goes through, because on a model-managed ceiling it never
        # forms a budget to check. So a run against OpenAI merged in twenty
        # seconds and then failed three times over, which is how this was
        # found: a half-finished run is a worse answer than a refusal.
        #
        # Refusing was right. `preflight`'s own docstring says a stated window
        # satisfies it, and the catalogue has stated one all along -- every row
        # carries `context_window`, and the web path was the one caller that
        # knew it and did not pass it on.
        #
        # Not set for a model the catalogue has never seen: a discovered model
        # is a name an endpoint listed, and nothing in that listing says how
        # much context it serves. Guessing one is the failure `preflight`
        # exists to prevent, so those keep asking, which is correct where
        # `/api/ps` answers and a refusal naming `--window` where it does not.
        window = (entry or {}).get("context_window")
        if (window and not (environ.get(f"LLOSSLESS_WINDOW_{suffix}") or "").strip()
                and not (environ.get("LLOSSLESS_WINDOW") or "").strip()):
            plan[f"LLOSSLESS_WINDOW_{suffix}"] = str(window)
        # **And refused, before a job exists, where nothing can supply one.**
        # A model the catalogue does not know, sent to a vendor, has no
        # stated window and no `/api/ps` to measure one: the merge would run
        # and every check would refuse after it. The request's `window` field
        # is how the person who typed the id states it, as `--window` does on
        # the command line. The server's own endpoint and a self-hosted one
        # may be an ollama that reports its window, so they are not refused
        # here; one that does not still refuses at the first check.
        if not window and window_unreportable(provider, environ, role):
            raise JobRefused(
                f"{model} goes to {provider}, which does not report a context "
                f"window, and the catalogue states none for this model. A "
                f"window is measured or stated, never guessed, so without one "
                f"every check would refuse after the merge had run. State it "
                f"in the request's window field, as a whole number of tokens; "
                f"the figure is on {provider}'s page for the model.")
        if entry and entry.get("profile"):
            profiles.add(entry["profile"])
        elif not entry:
            # A model the catalogue does not know -- typed, or listed by an
            # endpoint -- gets the shape its provider's measured rows share.
            # It used to get none, so the run fell to the default
            # `openai-compatible` body, and an OpenAI reasoning model refuses
            # that body's `max_tokens` on the first call.
            shape = catalogue.provider_profile(provider, catalogue_path)
            if shape:
                derived.add(shape)
    # **A row's stated shape outranks a provider's**, and the provider's is
    # used only when every unknown model agrees on it. The profile is one per
    # run, so a split with a catalogue merge and a listed local check keeps the
    # row's shape exactly as it did before, rather than being refused as
    # two shapes; the derived one fills only the case where nothing was stated.
    if not profiles and len(derived) == 1:
        profiles = derived
    if len(profiles) > 1:
        raise JobRefused(
            f"these models need different request shapes "
            f"({', '.join(sorted(profiles))}), and a run sends one shape to "
            f"every role. Pick models that share a profile, or run them "
            f"separately.")
    # Only when the operator has not named one themselves. A profile in the
    # server's environment is a deliberate setting about how requests are
    # shaped, and a catalogue row is a good default rather than an override of
    # somebody's explicit choice.
    if profiles and not (environ.get("LLOSSLESS_PROFILE") or "").strip():
        plan["LLOSSLESS_PROFILE"] = profiles.pop()
    return plan


# How a run is paid for, per role, in the five words the page's submit button
# uses. `discover` owns the three an address can be classified as; a
# command route adds the two a program can be. The page's `ROUTE_KINDS` is
# asserted equal to this by `tests/test_web_static.py`, so the button before
# the click and the provenance after it cannot drift into two vocabularies.
ROUTE_SUBSCRIPTION = "subscription"
ROUTE_COMMAND = "command"
ROUTE_KINDS = (discover.KIND_METERED, ROUTE_SUBSCRIPTION, ROUTE_COMMAND,
               discover.KIND_SELFHOSTED, discover.KIND_UNKNOWN)

# The provider whose rows bill GPU minutes rather than tokens. The page's
# `SELF_HOSTED` is the same string, and `credentials.PROVIDERS` is where both
# come from.
SELF_HOSTED_PROVIDER = "self-hosted"
assert SELF_HOSTED_PROVIDER in credentials.PROVIDERS

# The providers whose endpoint cannot report a context window. Every one
# but `self-hosted` is a vendor API, and no vendor serves ollama's `/api/ps`,
# which is the only route `window.reported` can ask. Derived from the
# allowlist, so a vendor added there is in here without a second edit.
WINDOWLESS_PROVIDERS = frozenset(credentials.PROVIDERS) - {SELF_HOSTED_PROVIDER}


def window_unreportable(provider, environ: dict[str, str],
                        role: str | None = None) -> bool:
    """Does a model the catalogue does not know, sent to `provider`, lack a window?

    True when the provider's endpoint cannot report one and the environment
    states none for `role` -- or, with no role, for some role. The environment
    is the server's own with the request's settings over it, so a server-wide
    `LLOSSLESS_WINDOW` answers it as a request's `window` does.
    `endpoint_plan` refuses on this, and `api.endpoints` serves it per
    provider so the page asks for the field before it submits.
    """
    if provider not in WINDOWLESS_PROVIDERS:
        return False
    if (environ.get("LLOSSLESS_WINDOW") or "").strip():
        return False
    roles = cli.ROLES if role is None else (role,)
    return any(not (environ.get(f"LLOSSLESS_WINDOW_{r.upper()}") or "").strip()
               for r in roles)


def billed_by_role(request: MergeRequest, settings: config.Settings,
                   environ: dict[str, str], catalogue_path=None) -> dict[str, str]:
    """How each role of this run is paid for, as the page's button names it.

    **Recorded, not inferred afterwards.** The button names the route before
    the click; this names it after, in the run's own provenance, so the answer
    to "did the checks go to the subscription or to the metered API" is in the
    report that a week later is where the question is asked. It is
    computed from the same three sources `endpoint_plan` routes on, in the
    same order, so it describes the plan the calls were made under rather
    than a second opinion about it.

    A command route answers every role through one program -- `Settings.command`
    is run-wide, and per-role endpoints are dead configuration beside it
    -- so every role gets the route's kind. That is also why the page's Check
    column no longer offers a command row under an HTTP merge: there is no run
    this function could describe in which one role is on the subscription and
    another is not.

    Over HTTP, a model the catalogue or an endpoint's own listing places has a
    provider, and a provider is `metered` unless it is the self-hosted one --
    `routeKind`'s rule on the page, one row for one row. A model nothing places
    is a name somebody typed, and it goes wherever the plan pointed this role;
    that address is classified by `discover.kind_of`, which is what the page's
    `typedModelKind` reads for the same case.
    """
    if settings.command:
        kind = (ROUTE_SUBSCRIPTION if settings.profile == commands.DEFAULT_PROFILE
                else ROUTE_COMMAND)
        return {role: kind for role in cli.ROLES}
    billed: dict[str, str] = {}
    for role in cli.ROLES:
        try:
            model = settings.model_for(role)
        except config.ConfigError:
            # No model for this role, so no call and nothing billed. The
            # engine refuses such a run where refusing is its job.
            continue
        entry = catalogue.for_api_model(model, catalogue_path)
        provider = (entry["provider"] if entry
                    else credentials.provider_serving(model, environ))
        if provider:
            billed[role] = (discover.KIND_SELFHOSTED
                            if provider == SELF_HOSTED_PROVIDER
                            else discover.KIND_METERED)
        else:
            billed[role] = discover.kind_of(settings.base_url_for(role))
    return billed


def banner_roles(settings: config.Settings,
                 billed: dict[str, str]) -> list[dict] | None:
    """Each role's model, endpoint and route for the run header, or None.

    The header has one Model row and one Endpoint row, and they were the
    check's -- `model_for("verify")` and the run-wide address -- so on a
    metered merge with local checks it named the local model and the local
    box and said nothing of the merge. Roles are grouped by what the header
    shows about them, and when there is more than one group none of the
    single rows is true of every role, so each group gets its own.

    The route is `billed`'s word for the role, the one the button said before
    the click and the provenance records after it, so the header cannot name
    a route the run was not billed under. None whenever one line describes
    every role, which is every command run and every run with one model on
    one endpoint: the header is then what it always was.
    """
    groups: dict[tuple[str, str, str], list[str]] = {}
    for role in cli.ROLES:
        if role not in billed:
            continue  # no model for this role, so no call and nothing to name
        key = (settings.model_for(role), settings.banner_endpoint_for(role),
               billed[role])
        groups.setdefault(key, []).append(role)
    if len(groups) < 2:
        return None
    return [{"roles": roles, "model": model, "endpoint": endpoint, "route": route}
            for (model, endpoint, route), roles in groups.items()]


def web_settings(request: MergeRequest, workspace: Workspace) -> config.Settings:
    """Resolved settings for a web run, with the three a server may not inherit.

    `config.resolve` does the resolving and runs its two guards on the way
    through -- `check_base_url` (`config.py:2860`) refuses anything that is not
    http(s), because `urllib.request.build_opener` installs `FileHandler` and
    `FTPHandler` from its defaults and a `file://` base URL would have a local
    file's bytes parsed as a model answer; `check_cleartext_key`
    (`config.py:2938`) refuses putting a bearer token on the wire unencrypted
    to a host that is not this one. Neither is skipped because the values
    arrived through a web form rather than through a shell, and both are run
    again below after `replace`, so the object the `Client` is handed is the
    object that was checked rather than one derived from it.

    Three fields are then forced, and none of them is a preference:

    `use_cache=False`. `Settings.use_cache` defaults to `IN_CHECKOUT`
    (`config.py:1657`), which is true for anyone running the server out of a
    clone -- the ordinary self-hosting case. A response cache is keyed on the
    request, and the request contains the operator's document, so leaving the
    default on would write uploaded documents into a cassette directory on the
    server and serve a later upload's merge out of an earlier one's answer.

    `cache_dir` to a directory this process owns. Not for caching -- there is
    none, per the line above -- but because `Client.__init__` opens
    `settings.cache_dir / "capabilities.json"` whatever `use_cache` says
    (`client.py:364`), so the default (a `.llossless-cache` beside the
    checkout, or the working directory when installed) has to be replaced with
    somewhere the server is entitled to write. A read-only default is not a
    slower client, it is a `Client` that raises before the first call.

    `record_dir` and `replay_dir` to None, and `dry_run` to False. Today
    `config.from_env` sets none of them -- they arrive only through
    `apply_arguments`, and `resolve` is called here with `args=None` -- so all
    three are already what they are being set to. Set anyway, because the thing
    being asserted is not "they happen to be None": it is that a server must
    never write a user's uploaded document into a cassette, and that claim
    should not quietly become false the day one of them grows an environment
    variable.
    """
    settings = config.resolve(None, environ=request_environ(workspace, request))
    settings = dataclasses.replace(
        settings,
        use_cache=False,
        cache_dir=workspace.cache_dir,
        record_dir=None,
        replay_dir=None,
        dry_run=False,
        # The Provenance detail names whoever actually stated the figure.
        # `config.resolve`'s default assumes a shell operator's
        # `--window` / `LLOSSLESS_WINDOW`; a request that carried its own
        # `window` stated it through the page instead -- typed beside a
        # vendor id or beside a table row the catalogue does not know --
        # and only this call site can tell the two apart, since both
        # arrive here as the same `LLOSSLESS_WINDOW` override.
        **({"window_declared_by": 'the page\'s "Context window (tokens)" field'}
           if "LLOSSLESS_WINDOW" in request.overrides else {}),
        # Whose choice the merge's level was. `route_plan` has already
        # refused a level the route cannot carry, so what is recorded here is
        # what `command_for` puts on the argv.
        **({"effort_requested": {"merge": request.effort}}
           if request.effort is not None else {}),
    )
    config.check_base_url(settings)
    config.check_cleartext_key(settings)
    return settings


def write_private(path: Path, text: str) -> None:
    """Write `text` to `path`, owner-readable only, with no window in between."""
    handle = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, FILE_MODE)
    with open(handle, "w", encoding="utf-8") as stream:
        stream.write(text)


def publish(job: Job, run: Run, client: Client, settings: config.Settings,
            *, duration: float, workspace: Workspace,
            billed: dict[str, str] | None = None) -> None:
    """Stamp provenance, render the artefacts, attach the result to the job.

    Called on the way out of `run_merge` whether the pipeline returned or
    raised, which is the whole reason this is a function. `cli.main` learned
    the same lesson the same way (`cli.py:1796`): a fault on the pipeline's
    last call used to discard the report of everything that had already
    finished, including the merged document the call before it had spent forty
    minutes producing. Here the operator has no stdout to fall back on, so
    there is nothing else left if this does not run.

    `run.merged` may be None -- the merge step itself can error -- and then
    there is no `merged.md` to write. The JSON and the HTML are written
    regardless, because a report of a run that failed is the account of how it
    failed, and an absent file reads as a run that never happened.

    Order is load-bearing in two places. The merged document is written before
    the report is rendered, because `run.merged_written_to` is a field of the
    report and setting it afterwards would publish a report that said nothing
    was written next to the file that was. And what it is set to is the bare
    name rather than the path: the report is a file the operator downloads, the
    directory is an implementation detail of this server, and a report carrying
    `/srv/.../jobs/<id>/merged.md` tells its reader about a filesystem they
    cannot reach and should not be shown.
    """
    if run.merged is not None:
        write_private(workspace.directory / MERGED_MD, run.merged)
        run.merged_written_to = MERGED_MD

    run.provenance = Provenance(
        settings=settings,
        client=client,
        roles=cli.ROLES,
        duration_seconds=duration,
        base=run.base,
        base_chosen=run.base_chosen,
        billed=billed,
    )
    job.run = run
    job.report = as_dict(run)
    job.exit_code = exit_code(run)
    # Sharpened now that `run` exists: the base document, defaulted or not,
    # reads off what the merge actually followed (`run.base`) rather than off
    # the request's best guess before it ran. Carried in the report too, so it
    # survives a restart (`_restore` reads `report.json` back) and travels
    # through `redact.report` like the rest of the run's account of itself.
    job.cli_equivalent = cli_render.render(settings, job.request, run,
                                           shown=workspace.own_addresses)
    job.report["cli_equivalent"] = job.cli_equivalent

    # The page first, and nothing written until it exists. Rendering holds
    # the report's Inventory against its Coverage table and raises sooner
    # than print two counts for one quantity (`report.InventoryDisagrees`).
    # Written in the other order, `report.json` was already on disk with the
    # run's own exit code when the page refused, and the job then failed
    # under the exception's class name. The command line calls this an
    # inconclusive run and says why in a sentence (`cli.report_refused`), so
    # this does: exit code 2, no report in either form, and the merged
    # document kept where it was written.
    try:
        page = render_html(run)
    except InventoryDisagrees as exc:
        job.report = None
        job.exit_code = INCONCLUSIVE
        raise Inconclusive(report_refused(run, exc)) from None
    write_private(workspace.directory / REPORT_JSON,
                  json.dumps(job.report, indent=2) + "\n")
    write_private(workspace.directory / REPORT_HTML, page)


def report_refused(run: Run, exc: BaseException) -> str:
    """Why a run has no report, in the command line's own sentence.

    `cli.report_refused` words this for a terminal and prints as it goes, so
    the sentence is restated here; `tests/test_web_jobs.py` holds the two
    against each other.
    """
    what = ("the report was not written; the merged document was, and can "
            "still be downloaded" if run.merged is not None
            else "the report was not written")
    return (f"{what}. Its Inventory and its Coverage table counted the same "
            f"claims differently, and LLossless refuses to print two different "
            f"counts for one quantity, so this run is inconclusive. That is a "
            f"defect in LLossless and not in your documents: please report it, "
            f"with this detail. {exc}")


def run_merge(job: Job, workspace: Workspace) -> None:
    """One complete merge-and-verify, with its progress recorded as events.

    The default runner. `JobStore` takes this as an argument so that the suite
    can substitute a runner that does nothing but record when it started and
    stopped -- concurrency is a property of the pool, and testing it through a
    real merge would make a thread-scheduling assertion depend on how fast a
    fake endpoint answers.

    Everything that reports progress goes through one `WebConsole`, including
    the client's `notify` channel. On the command line those are two
    destinations for a reason `Client.__init__` (`client.py:352`) states: a
    warning is printed whatever the verbosity, progress is not. Here they are
    one log with two kinds in it, which keeps that distinction while putting
    both in front of the person who is watching.
    """
    console = WebConsole(job.events)
    request = job.request
    source = workspace.keys() if callable(workspace.keys) else workspace.keys
    # `None` leaves the source unswapped, which is `os.environ` and is
    # byte-identical to every CLI run, every cassette and every recorded
    # figure. That is the property `keys_for_this_run`'s unset case exists to
    # keep, and it is why this is a `nullcontext` rather than a swap to
    # `os.environ`: swapping in a copy would make the two able to disagree the
    # moment something else in the process exported a variable.
    swap = (contextlib.nullcontext() if source is None
            else config.keys_for_this_run(source))
    with swap:
        _run_merge(job, workspace, console, request)


def _run_merge(job: Job, workspace: Workspace, console, request) -> None:
    """The merge itself, inside whatever key source `run_merge` chose.

    Split out so that the `with` above wraps **everything** -- `web_settings`
    runs `config.check_cleartext_key`, which asks whether the key that would
    actually be sent goes on the wire unencrypted, and that question has a
    different answer for two users. A version of this that entered the context
    only around `cli.pipeline` would have run the guard against the wrong
    credential and then sent the right one.
    """

    # The seam. Canonical names, the fence scan and the arity guard, in the one
    # copy `main` also calls -- which is what stops this path and the command
    # line drifting while `tests/test_cli.py` stays green.
    # Resolved before the seam below rather than after it, because
    # `prepare_merge` now loads the prompts *this depth* will use and so has
    # to be told which depth that is. Nothing between here and the merge reads
    # a partially-resolved setting, and `web_settings`' two guards are
    # unchanged by the move: they refuse a bad base URL or a cleartext key
    # before any document is looked at, which is the stricter order of the
    # two, not the looser one.
    settings = web_settings(request, workspace)
    # The CLI-equivalent block, off the same `Settings` object the pipeline is
    # about to be handed and before any call -- so a run that fails on its
    # first request still leaves the operator an exact command to try by hand.
    # Recomputed in `publish` once `run` exists, which sharpens the one field
    # that needs it (the base document); everything else is already exact here.
    job.cli_equivalent = cli_render.render(settings, request,
                                           shown=workspace.own_addresses)
    # Beside the settings it describes and before any call, so a run that
    # fails on its first request still records how it would have been billed.
    # The environment is the one `web_settings` resolved from; the
    # listing it reads for a discovered model is in it.
    billed = billed_by_role(request, settings, request_environ(workspace, request))
    documents, loaded, unclosed_fences = cli.prepare_merge(
        request.documents, settings.verify_depth)
    for name, line, reason in unclosed_fences:
        # Reported, never repaired: everything after an unclosed fence is one
        # code block, which is what the document literally says. `main` prints
        # these before the run starts and so does this.
        console.warn(f"{name}: {reason}")

    policy = merge.MergePolicy.from_settings(settings)
    console.banner("merge", settings.model_for("verify"),
                   # `banner_endpoint`, not `base_url`: scheme, host and port,
                   # with no userinfo and no path. This event reaches a browser
                   # and is kept in the log for the job's lifetime, and a URL
                   # carries more than an address -- userinfo is a credential
                   # and a query can carry a pasted token.
                   #
                   # The verify role's own, beside the verify role's model.
                   # The run-wide one is the server's default address,
                   # and a catalogue model is routed per role: an all-metered
                   # run's header named the local box that answered nothing.
                   settings.banner_endpoint_for("verify"),
                   # The CLI has passed this since the banner existed and this
                   # call site never did, so the page's first line named
                   # the model and the endpoint and stopped -- while the window
                   # is one of the three things an operator reads it for. Same
                   # helper, so the two surfaces cannot word it differently.
                   window=window_module.banner_window(
                       settings, settings.model_for("verify")),
                   fidelity=policy.fidelity,
                   # The depth this run will actually use, read off the same
                   # `settings` object `pipeline` is handed below rather than
                   # off the request -- a request that named no depth resolves
                   # to the default here, and a banner reading the request
                   # would print nothing for exactly the runs whose reader
                   # most needs to see which questions were asked.
                   depth=settings.verify_depth,
                   # The grant this run carries, on the line the submitter
                   # watches while it runs. Read off `settings.command`,
                   # which is the argv after `config.resolve` has applied any
                   # automatic grant, so the banner says what the run really
                   # has rather than what the route was configured with.
                   retrieval=", ".join(
                       config.granted_web_tools(settings.command)) or None,
                   # Each role apart, when the model and endpoint above are one
                   # role's and not the run's. From `billed`, so the
                   # header's route words are the button's.
                   roles=banner_roles(settings, billed),
                   # The merge's effort level, off the argv the merge will run:
                   # the slider's choice, or the route's default.
                   effort=settings.effort_for("merge") or None)

    run = Run(command="merge")
    # The caller's own labels, which is what the report displays. The canonical
    # names went to the model; these come back to the operator.
    run.paths = dict(zip(merge.source_names(len(request.documents)),
                         request.documents))
    run.unclosed_fences = unclosed_fences

    client = Client(settings, notify=console.warn, console=console)
    # `job.stop` is the cancel: the client makes no call once it is set.
    client.cancel = job.stop
    # A reply the client cannot parse is kept on disk, whole, and a reply is
    # the documents' content rearranged. With the cache off, which it is
    # here, the client keeps those under the system temporary directory
    # (`Client._dump_root`), where deleting the run, retention and shutdown
    # all left them. In this run's own folder they go when the run goes.
    client._scratch = workspace.directory
    started = time.monotonic()
    fault: BaseException | None = None
    try:
        # `depth=` is not optional here, whatever the signature's default
        # says. The web path is the third call site and the two in `cli.py`
        # were wired first; leaving it off made the setting silently mean
        # nothing through the server, which is worse than not offering it --
        # an operator who set LLOSSLESS_VERIFY_DEPTH would have been told
        # `full` ran and believed the run checked for invention.
        cli.pipeline(client, run, documents, loaded,
                     canonical_base(request), policy,
                     depth=settings.verify_depth)
    except BaseException as exc:  # noqa: BLE001 - re-raised below, after publishing
        fault = exc
    publish(job, run, client, settings,
            duration=time.monotonic() - started, workspace=workspace,
            billed=billed)
    if fault is not None:
        raise fault


# --------------------------------------------------------------------------
# the store
# --------------------------------------------------------------------------


# Every field of an index record, and what each may hold. Required, all
# of them, on every record: a record missing one is not a record with a
# default, it is a file this build did not write.
_RECORD_FIELDS = {
    "id": (str,),
    "owner": (str,),
    "state": (str,),
    "created_at": (int, float),
    "started_at": (int, float, type(None)),
    "finished_at": (int, float, type(None)),
    "forgotten_at": (int, float, type(None)),
    "exit_code": (int, type(None)),
    "error": (str, type(None)),
    "document_count": (int,),
    "retry_of": (str, type(None)),
    "event_seq": (int,),
    "settings": (dict, type(None)),
}
_SETTINGS_FIELDS = {
    "overrides": (dict,),
    "endpoint": (str, type(None)),
    "route": (str, type(None)),
    "effort": (str, type(None)),
}


def parse_index(raw: bytes, path: Path) -> list[dict]:
    """The records of an index file, checked field by field, or `IndexUnreadable`.

    Strict, because the alternative to refusing is guessing about other
    people's documents: every field present, of its type, a known state, a
    unique id shaped like one, settings only on a record that is not a
    tombstone and only from the allowlist. Nothing is repaired.
    """
    def bad(reason: str):
        return IndexUnreadable(path, reason)

    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise bad(f"not JSON: {exc}") from None
    if not isinstance(payload, dict) or set(payload) != {"version", "jobs"}:
        raise bad("not an index: expected exactly the keys version and jobs")
    if payload["version"] != INDEX_VERSION:
        raise bad(f"version {payload['version']!r}, and this build reads "
                  f"version {INDEX_VERSION}")
    if not isinstance(payload["jobs"], list):
        raise bad("jobs is not a list")
    seen: set[str] = set()
    for number, record in enumerate(payload["jobs"], 1):
        where = f"record {number}"
        if not isinstance(record, dict) or set(record) != set(_RECORD_FIELDS):
            raise bad(f"{where} does not have exactly the fields "
                      f"{', '.join(sorted(_RECORD_FIELDS))}")
        for name, kinds in _RECORD_FIELDS.items():
            value = record[name]
            if not isinstance(value, kinds) or (isinstance(value, bool) and bool not in kinds):
                raise bad(f"{where}: {name} is {type(value).__name__}")
        if not JOB_ID.match(record["id"]) or record["id"] in seen:
            raise bad(f"{where}: id {record['id']!r} is not a job id, or is repeated")
        seen.add(record["id"])
        if record["retry_of"] is not None and not JOB_ID.match(record["retry_of"]):
            raise bad(f"{where}: retry_of is not a job id")
        if record["state"] not in STATES:
            raise bad(f"{where}: unknown state {record['state']!r}")
        settings = record["settings"]
        if (settings is None) != (record["forgotten_at"] is not None):
            raise bad(f"{where}: settings must be present exactly when the "
                      f"run is not forgotten")
        if settings is not None:
            if set(settings) != set(_SETTINGS_FIELDS):
                raise bad(f"{where}: settings do not have exactly the fields "
                          f"{', '.join(sorted(_SETTINGS_FIELDS))}")
            for name, kinds in _SETTINGS_FIELDS.items():
                if not isinstance(settings[name], kinds):
                    raise bad(f"{where}: settings.{name} is "
                              f"{type(settings[name]).__name__}")
            overrides = settings["overrides"]
            if (set(overrides) - REQUEST_SETTABLE
                    or not all(isinstance(v, str) for v in overrides.values())):
                raise bad(f"{where}: settings.overrides holds a variable a "
                          f"request may not set")
    return payload["jobs"]


def read_sources(path: Path) -> tuple[dict[str, str], str | None]:
    """A job's documents and base label, as `submit` wrote them."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or set(payload) != {"documents", "base"}:
        raise ValueError("not a sources file")
    documents: dict[str, str] = {}
    for label, text in payload["documents"]:
        if not isinstance(label, str) or not isinstance(text, str):
            raise TypeError("a document is a label and a text")
        documents[label] = text
    base = payload["base"]
    if base is not None and not isinstance(base, str):
        raise TypeError("the base is a label or null")
    return documents, base


# How many finished steps an interrupted run's account names before it counts
# the rest. The account is a status line and a history row, not the log.
INTERRUPTED_STEPS_NAMED = 6


def interrupted_error(events) -> str:
    """What an interrupted run did before the stop, from the log that reached disk.

    Built from `done` and `failed` events only, whose messages are canonical
    step names (`merge`, `decompose source_a.md`) and carry nothing of the
    documents. It never reads as complete, because it was not: the report is
    written on the way out of a run, and a killed process never got there.
    """
    finished = [event.message for event in events if event.kind == "done"]
    failed = [event.message for event in events if event.kind == "failed"]
    if finished:
        named = ", ".join(finished[:INTERRUPTED_STEPS_NAMED])
        more = len(finished) - INTERRUPTED_STEPS_NAMED
        ran = (f"{len(finished)} step(s) had finished before the stop ({named}"
               f"{f', and {more} more' if more > 0 else ''})")
    else:
        ran = "no step had finished before the stop"
    errored = (f"; {len(failed)} step(s) had failed" if failed else "")
    return (f"interrupted: this server stopped while the run was in progress, "
            f"so the run is not complete and no merged document or report was "
            f"written. From the log that reached disk: {ran}{errored}. Model "
            f"calls made before the stop may have been billed; how many is not "
            f"known. It was not restarted, because a restart would make and "
            f"bill those calls again. Retry starts a new run from the same "
            f"documents and settings.")


class JobStore:
    """Submitted jobs, a worker pool that runs them, and the retention that ends them.

    **The index is on disk.** Until then it was in memory and died with
    the process, and that was argued as a decision: the alternative was "a
    database of who uploaded what and when". The operator's machine then
    crashed twice in a week and took the queue, the running merge and the
    run list with it, and the answer to "can I queue work and come back in
    a few hours" became no. So the index is written down -- `index.json`
    in the work directory, one record per job, rewritten atomically on
    every change of state -- and the objection is answered by what it
    holds and how long for, not by its absence: a state, timestamps, an
    owner id, the allowlisted settings and a count; never a document, a
    label or a key; and it forgets a job exactly when retention does.

    On start (`_load`): queued jobs resume in their order; a job that was
    running becomes `interrupted` and is never re-run by itself; finished jobs
    are listed again with their files; and the reaper runs once before anything
    is served, so a window that passed while the server was down has already
    been applied.

    `clock` and `runner` are injected for the suite. Retention is a question
    about elapsed time and a concurrency limit is a question about overlap, and
    neither is worth testing by sleeping.
    """

    def __init__(self, work_dir: Path | str, *, workers: int = DEFAULT_WORKERS,
                 retention_seconds: float | None = DEFAULT_RETENTION_SECONDS,
                 sweep_seconds: float = DEFAULT_SWEEP_SECONDS,
                 environ: dict[str, str] | None = None,
                 directory=None, routes=None,
                 runner=None, clock=time.time) -> None:
        if workers < 1:
            raise ValueError(f"a job store needs at least one worker; got {workers}")
        self.work_dir = Path(work_dir)
        self.workers = workers
        self.retention_seconds = retention_seconds
        self.sweep_seconds = sweep_seconds
        # Copied, not referenced. `os.environ` is process-global and mutable,
        # and a store that read it per job would let an unrelated part of the
        # server change what a queued job resolves to between submit and run.
        self.environ = dict(os.environ if environ is None else environ)
        self.runner = run_merge if runner is None else runner
        self.clock = clock
        # `accounts.Directory`, or None for a server with no account store.
        # It answers two questions and they are kept apart on purpose: which
        # *addresses* an account has, which go into the environment a job
        # resolves against, and which *keys* it has, which do not go into any
        # environment at all and are handed to the worker thread through
        # `config.keys_for_this_run`.
        self.directory = directory
        # `commands.Commands`, or a `NoCommands` holding none. **Never `None`
        # after this line**, so no call site below has to decide what a missing
        # store means -- the empty case is an object that answers "no routes"
        # to every question, which is the default a server has until an
        # operator writes a file and `server.serve` hands it one.
        self.routes = commands.NoCommands() if routes is None else routes

        self.work_dir.mkdir(parents=True, exist_ok=True)
        os.chmod(self.work_dir, DIR_MODE)
        self.cache_dir = self.work_dir / ".cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        os.chmod(self.cache_dir, DIR_MODE)
        self.index_path = self.work_dir / INDEX_JSON

        self._jobs: dict[str, Job] = {}
        self._order: list[str] = []
        self._lock = threading.Lock()
        # Held around a snapshot of the index *and* its write, so two writers
        # cannot land out of order and leave an older state on disk. Always
        # taken before `_lock`, never while holding it.
        self._persist_lock = threading.Lock()
        self._queue: queue.Queue = queue.Queue()
        self._threads: list[threading.Thread] = []
        self._stopping = threading.Event()
        self._started = False
        # What the start-up reload found, for `server.serve`'s banner.
        # The lock first, so nothing is read or rewritten under a live owner.
        self._lock_handle: int | None = None
        self._claim_work_dir()
        try:
            self.restored = self._load()
        except BaseException:
            self._release_work_dir()
            raise

    # -- lifecycle -------------------------------------------------------

    def start(self) -> JobStore:
        """Start the workers and the reaper. Idempotent, and returns self.

        The thread list and the stop flag are reset here rather than only in
        `close`, so that a store which was closed and started again -- a test
        harness, a server reloading its configuration -- gets a reaper that
        runs rather than one that sees a flag left set by the previous
        shutdown and exits on its first check.
        """
        if self._started:
            return self
        if self._lock_handle is None:
            self._claim_work_dir()
        self._started = True
        self._stopping.clear()
        self._threads = []
        for index in range(self.workers):
            thread = threading.Thread(target=self._work, name=f"llossless-job-{index}",
                                      daemon=True)
            thread.start()
            self._threads.append(thread)
        reaper = threading.Thread(target=self._reap, name="llossless-reaper",
                                  daemon=True)
        reaper.start()
        self._threads.append(reaper)
        return self

    def close(self, timeout: float | None = 10.0) -> None:
        """Stop taking work and wind the threads down.

        A running merge is not interrupted -- there is nothing to interrupt it
        with, the engine is a synchronous call -- so this waits for the worker
        to come back from whatever it is in the middle of, up to `timeout`, and
        then gives up rather than hanging the shutdown. The threads are daemons
        so a process that gives up still exits.
        """
        self._stopping.set()
        # One sentinel per worker, not one per thread. The reaper does not read
        # the queue, so a sentinel per thread would leave a spare `None` behind
        # -- and the next worker started against this store would take it as
        # its own shutdown signal and exit before running anything.
        for _ in range(self.workers):
            self._queue.put(None)
        for thread in self._threads:
            thread.join(timeout=timeout)
        self._threads = []
        self._started = False
        self._release_work_dir()

    def __enter__(self) -> JobStore:
        return self.start()

    def __exit__(self, *exc_info) -> None:
        self.close()

    # -- the index on disk --------------------------------------------------

    def _claim_work_dir(self) -> None:
        """Own the work directory, or refuse with `WorkDirBusy`.

        `flock` on a file in the directory, non-blocking. Not available off
        POSIX, where the directory is simply not locked: the store still
        works, and running two servers on one directory is then the
        operator's to avoid.
        """
        if fcntl is None:
            return
        handle = os.open(self.work_dir / LOCK_FILE, os.O_RDWR | os.O_CREAT, FILE_MODE)
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            os.close(handle)
            raise WorkDirBusy(self.work_dir) from None
        self._lock_handle = handle

    def _release_work_dir(self) -> None:
        """Give the work directory up. Closing the descriptor drops the lock."""
        handle, self._lock_handle = self._lock_handle, None
        if handle is not None:
            os.close(handle)

    def _record(self, job: Job) -> dict:
        """One job as the index stores it. Every field on every record.

        **No key can reach this**, by construction and then by check. The
        settings are the request's `overrides`, which `MergeRequest` refuses
        beyond `REQUEST_SETTABLE` -- models, fidelity, depth, title policy,
        loss budget, window -- and a provider *name*, a route *id* and an
        effort word. No field here is read from an environment, a credential
        file or an account. The allowlist is checked again on the way out
        rather than trusted, so an index cannot be the place a later edit
        writes something else down. A forgotten job keeps only its tombstone.
        """
        request = job.request
        refused = sorted(set(request.overrides) - REQUEST_SETTABLE)
        if refused:
            raise JobRefused(f"refusing to write {', '.join(refused)} to the job index")
        settings = None if job.forgotten else {
            "overrides": dict(sorted(request.overrides.items())),
            "endpoint": request.endpoint,
            "route": request.route,
            "effort": request.effort,
        }
        return {
            "id": job.id,
            "owner": job.owner,
            "state": job.state,
            "created_at": job.created_at,
            "started_at": job.started_at,
            "finished_at": job.finished_at,
            "forgotten_at": job.forgotten_at,
            "exit_code": job.exit_code,
            "error": job.error,
            "document_count": job.document_count,
            "retry_of": job.retry_of,
            "event_seq": job.events.next_id,
            "settings": settings,
        }

    def _save(self) -> None:
        """Rewrite the index: a temporary file, synced, renamed over the old one.

        The rename is what makes a crash harmless: the file on disk is the old
        index or the new one, never half of either. Owner-only from the moment
        it exists -- `os.open` with the mode, on a fresh name -- for the reason
        `write_private` gives. The directory is synced after the rename, since
        a rename that was not synced is a rename a power cut can undo.
        """
        with self._persist_lock:
            with self._lock:
                records = [self._record(self._jobs[job_id]) for job_id in self._order
                           if job_id in self._jobs]
            payload = json.dumps({"version": INDEX_VERSION, "jobs": records},
                                 indent=1, sort_keys=True) + "\n"
            temp = self.work_dir / INDEX_TEMP
            with contextlib.suppress(FileNotFoundError):
                temp.unlink()
            handle = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, FILE_MODE)
            try:
                os.write(handle, payload.encode("utf-8"))
                os.fsync(handle)
            finally:
                os.close(handle)
            os.replace(temp, self.index_path)
            directory = os.open(self.work_dir, os.O_RDONLY)
            try:
                os.fsync(directory)
            finally:
                os.close(directory)

    def _save_quietly(self) -> None:
        """`_save` from a worker or the reaper, where raising stops the thread.

        Said on stderr, which is the operator's terminal: the run goes on and
        is correct in memory, and the next change of state tries the write
        again.
        """
        try:
            self._save()
        except OSError as exc:
            print(f"llossless serve: could not write the job index "
                  f"{self.index_path}: {exc}", file=sys.stderr, flush=True)

    def _load(self) -> dict:
        """Read the index back, resume what was queued, and settle the rest.

        No index is a first start, or one after the operator moved it aside:
        an empty list. An index that cannot be read refuses; see
        `IndexUnreadable` for why that and not an empty list.

        After the jobs are back, any directory in the work directory named
        like a job and not held by one is deleted: documents nobody can reach,
        whose window no record carries. That is also what makes moving a
        broken index aside a complete recovery rather than a leak.
        """
        with contextlib.suppress(FileNotFoundError):
            (self.work_dir / INDEX_TEMP).unlink()
        summary = {"restored": 0, "resumed": 0, "interrupted": 0,
                   "orphans_deleted": 0, "reaped": 0}
        try:
            raw = self.index_path.read_bytes()
        except FileNotFoundError:
            records = []
        except OSError as exc:
            raise IndexUnreadable(self.index_path, str(exc)) from None
        else:
            records = parse_index(raw, self.index_path)
            os.chmod(self.index_path, FILE_MODE)
        now = self.clock()
        for record in records:
            job = self._restore(record, now)
            self._jobs[job.id] = job
            self._order.append(job.id)
            summary["restored"] += 1
            if job.state == INTERRUPTED:
                summary["interrupted"] += 1
        held = {job_id for job_id, job in self._jobs.items() if not job.forgotten}
        for path in sorted(self.work_dir.iterdir()):
            if path.is_dir() and JOB_ID.match(path.name) and path.name not in held:
                shutil.rmtree(path, ignore_errors=True)
                summary["orphans_deleted"] += 1
        for job_id in self._order:
            if self._jobs[job_id].state == QUEUED:
                self._queue.put(job_id)
                summary["resumed"] += 1
        if records or summary["orphans_deleted"]:
            self._save()
        summary["reaped"] = len(self.sweep(now))
        return summary

    def _restore(self, record: dict, now: float) -> Job:
        """One index record back as a `Job`, with its documents, log and report."""
        job_id = record["id"]
        directory = self.work_dir / job_id
        settings = record["settings"]
        forgotten = record["forgotten_at"] is not None
        documents: dict[str, str] = {}
        base = None
        problem = None
        if not forgotten:
            try:
                documents, base = read_sources(directory / SOURCES_JSON)
            except (OSError, ValueError, KeyError, TypeError) as exc:
                problem = (f"its documents could not be read back from disk "
                           f"({type(exc).__name__}), so it cannot run or be "
                           f"retried")
        request = MergeRequest(documents={}, base=None)
        if settings is not None:
            try:
                request = MergeRequest(
                    documents=documents, base=base,
                    overrides=settings["overrides"], endpoint=settings["endpoint"],
                    route=settings["route"], effort=settings["effort"])
            except (ValueError, commands.CommandsError,
                    credentials.CredentialsError) as exc:
                # A setting this build no longer accepts -- an allowlist that
                # shrank between versions. Refused as it would be on submit.
                problem = problem or (f"its settings are no longer accepted by "
                                      f"this server: {exc}")
                request = MergeRequest(documents=documents, base=base)
        job = Job(request, now=record["created_at"], owner=record["owner"],
                  job_id=job_id, retry_of=record["retry_of"])
        job.document_count = record["document_count"]
        job.state = record["state"]
        job.started_at = record["started_at"]
        job.finished_at = record["finished_at"]
        job.forgotten_at = record["forgotten_at"]
        job.exit_code = record["exit_code"]
        job.error = record["error"]
        if forgotten:
            job.events = EventLog(next_id=record["event_seq"])
            job.events.forget("forgotten: the retention window has passed")
            return job
        job.directory = directory
        job.events = EventLog.restore(directory / EVENTS_JSONL)
        if job.state == CANCELLED:
            job.stop.set()
        report = directory / REPORT_JSON
        if job.terminal and report.is_file():
            try:
                job.report = json.loads(report.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                job.report = None
        if job.state == RUNNING:
            # The server stopped under it. Never re-run: see `INTERRUPTED`.
            job.state = INTERRUPTED
            job.error = interrupted_error(job.events.since(0))
            job.finished_at = now
            job.events.emit("state", job.error, state=INTERRUPTED, terminal=True,
                            exit_code=None)
        elif job.state == QUEUED and problem is not None:
            job.state = FAILED
            job.error = f"not resumed after a restart: {problem}. No model was called."
            job.finished_at = now
            job.events.emit("state", job.error, state=FAILED, terminal=True,
                            exit_code=None)
        elif job.state == QUEUED:
            job.events.emit("notice", "this server restarted; the run is still "
                                      "queued and keeps its place")
        if job.terminal:
            job.events.close()
        return job

    def queue_position(self, job: Job) -> tuple[int, int] | None:
        """(position, length) of a queued job in the one queue, or None.

        The queue is every account's, because the workers are: position 2 of 3
        means one run -- anybody's -- starts before this one. That count is all
        it says about other people's work.
        """
        with self._lock:
            queued = [job_id for job_id in self._order
                      if self._jobs[job_id].state == QUEUED]
        if job.id not in queued:
            return None
        return queued.index(job.id) + 1, len(queued)

    def environ_for(self, owner: str) -> dict[str, str]:
        """The server's environment with this account's own addresses over it.

        Non-secret only. A key never reaches this mapping -- see the module
        docstring for the asymmetry and why it is not an inconsistency.
        """
        if not owner or self.directory is None:
            return self.environ
        return {**self.environ, **self.directory.environ_for(owner)}

    def keys_for(self, owner: str):
        """The mapping this account's runs read credentials from, or `None`."""
        if not owner or self.directory is None:
            return None
        return self.directory.keys_for(owner, self.environ)

    def resolved_for(self, owner: str) -> tuple[dict[str, str], object]:
        """One run's environment and its key source, taken from one state.

        The address a run sends to and the key it sends are one decision, so
        they are read once and together: one copy of this server's
        environment, and one read of the account's own file laid over it
        (`accounts.Directory.for_run`). `environ_for` and `keys_for` each
        answer half of this from a read of their own, which is right for a
        page that shows one half and wrong for a run: an endpoint deleted
        between the two reads left a run addressed to a member's endpoint and
        holding the operator's shared key.

        A copy for every run, including one with no owner, so that no
        address a settings request changes afterwards reaches a run that has
        started resolving.

        A run with no mapping of its own, the operator's or any run on a
        server with no accounts, reads this process's keys at send time, as
        it always has. `StandingKeys` is what ties those to the addresses
        taken here.
        """
        environ = dict(self.environ)
        keys = None
        addresses: dict[str, str] = {}
        if self.directory is not None:
            # With no owner as well: the directory also says which roles may
            # not read the key their variable names (`credentials.key_scope`),
            # and that holds for a run nobody owns.
            addresses, keys = self.directory.for_run(owner, environ)
            environ.update(addresses)
        if keys is None:
            keys = StandingKeys(self.environ, environ)
        else:
            # A member. Their own keys as read; the operator's through the
            # same rule the operator's own run reads them by, asked of the
            # directory against this server's environment as it then is.
            keys = MemberKeys(
                keys, getattr(keys, "shared", ()),
                StandingKeys(self.environ, environ,
                             read=lambda name: self.directory.shared_keys(
                                 self.environ).get(name)),
                addresses=(value for name, value in addresses.items()
                           if name.startswith(credentials.PROVIDER_URL_PREFIX)))
        return environ, keys

    def submit(self, request: MergeRequest, *, owner: str = "",
               retry_of: str | None = None) -> Job:
        """Queue a merge and hand back the job. Refuses a request it cannot run.

        The refusals happen here, before an id exists, because a caller that
        gets an id back has been told the work was accepted and will go looking
        for a report. `merge.source_names` is what checks the arity
        (`merge.py:257`), the same call `prepare_merge` makes, so the floor and
        the ceiling are not written down a second time; `canonical_base`
        checks the base names a document that is actually there.

        A document with no text is refused here rather than at the seam.
        `merge.check_sources` would refuse it too, but that happens inside the
        worker, forty minutes after the operator stopped watching.
        """
        empty = [label for label, text in request.documents.items() if not text.strip()]
        if empty:
            raise JobRefused(
                f"{', '.join(repr(label) for label in empty)} has no text in "
                f"it. Every document in a merge has to have something to merge.")
        try:
            merge.source_names(len(request.documents))
        except merge.MergeError as exc:
            raise JobRefused(str(exc)) from None
        canonical_base(request)
        # Where each role's model is going to be sent, computed here and
        # thrown away. `request_environ` computes it again when the worker
        # starts -- it is the same call, so the two cannot disagree -- and the
        # point of doing it twice is that "this server cannot reach that
        # model" is a 400 about the request rather than a job that is accepted,
        # queued, started and then fails. The operator finds out before they
        # wait, which is the whole complaint this work started from.
        # From `resolved_for`, which is what the worker reads: it carries which
        # roles may not read a key, and a refusal about a key in cleartext
        # has to be about the key the run would send.
        resolved_environ(request, self.resolved_for(owner)[0], routes=self.routes)

        job = Job(request, now=self.clock(), owner=owner, retry_of=retry_of)
        # On disk before the id is handed back: the documents, so a
        # restart can run a job that was still queued, and the log, so it can
        # say what a run that was killed had done. Owner-only, in the job's own
        # directory, which retention deletes whole.
        job.directory = self.work_dir / job.id
        job.directory.mkdir(parents=True, exist_ok=True)
        os.chmod(job.directory, DIR_MODE)
        write_private(job.directory / SOURCES_JSON, json.dumps(
            {"documents": [[label, text] for label, text in request.documents.items()],
             "base": request.base}, ensure_ascii=False) + "\n")
        job.events = EventLog(job.directory / EVENTS_JSONL)
        with self._lock:
            self._jobs[job.id] = job
            self._order.append(job.id)
        job.events.emit("state", "queued", state=QUEUED, terminal=False)
        self._save()
        self._queue.put(job.id)
        return job

    def retry(self, job_id: str) -> Job:
        """A new job from a failed or interrupted one's documents and settings.

        **A new job, never the old one re-queued.** New id, new directory, new
        log, and every call made again from the start: the web path runs with
        no response cache (`web_settings`), so nothing the old run was
        answered is reused -- and a partial run's answers are not something a
        new one should be built on anyway. The new job names the old one in
        `retry_of`; the old one is left as it was, with its own window.

        Refused, before an id exists, for a run that is not retryable: one
        that finished or was cancelled, or whose documents retention has
        already deleted. The caller checks ownership; this checks the run.
        """
        old = self.get(job_id)
        if old is None:
            raise JobRefused(f"there is no run with id {job_id}.")
        if old.state not in RETRYABLE:
            raise JobRefused(f"run {job_id} is {old.state}; only a failed or "
                             f"interrupted run can be retried.")
        if not old.retryable:
            raise JobRefused(f"run {job_id}'s documents have been deleted, so "
                             f"there is nothing to retry it from.")
        return self.submit(old.request, owner=old.owner, retry_of=old.id)

    def get(self, job_id: str) -> Job | None:
        with self._lock:
            return self._jobs.get(job_id)

    def jobs(self) -> list[Job]:
        """Every job, oldest first. Insertion order, not sorted by timestamp.

        `clock` is injectable and a test clock can stand still, so two jobs can
        share a `created_at` and a sort on it would order them arbitrarily.
        Submission order is what the caller saw happen.
        """
        with self._lock:
            return [self._jobs[job_id] for job_id in self._order if job_id in self._jobs]

    def cancel(self, job_id: str) -> bool:
        """Cancel a queued or running job. True if a cancel was made.

        **Queued:** it never starts, lands in `cancelled`, and no model was
        called.

        **Running:** `job.stop` is set and the job is left `running`
        until the worker comes back. The run's `Client` makes no call after
        the flag, abandons an HTTP call in flight (it cannot be taken back,
        and the provider may bill it), and a command backend's program is
        stopped, SIGTERM then SIGKILL. The pipeline records the unit it was in
        as errored, `publish` writes the report of what ran, and `_execute`
        lands the job in `cancelled` with the calls counted in `error`. Until
        then the state stays `running`, because the merge really is: marking
        it cancelled while a call is still being answered is the lie an
        earlier version refused to tell.

        False for a job that is gone or already finished.
        """
        with self._lock:
            job = self._jobs.get(job_id)
            if job is None or job.terminal:
                return False
            if job.state == RUNNING:
                job.stop.set()
                running = True
            else:
                job.stop.set()
                job.state = CANCELLED
                job.error = CANCELLED_QUEUED
                job.finished_at = self.clock()
                running = False
        if running:
            job.events.emit("notice", CANCEL_ASKED)
            return True
        job.events.emit("state", CANCELLED_QUEUED, state=CANCELLED, terminal=True)
        job.events.close()
        self._save_quietly()
        return True

    def cancel_owned(self, owner: str) -> int:
        """Cancel every queued or running job of one account. How many.

        For an account that is being removed. Its runs would otherwise go on:
        the queued ones start later, as a member with nothing of their own,
        which is a run on the operator's endpoints with the operator's key,
        and nobody left who can see or stop it.
        """
        if not owner:
            return 0
        with self._lock:
            mine = [job.id for job in self._jobs.values()
                    if job.owner == owner and not job.terminal]
        return sum(1 for job_id in mine if self.cancel(job_id))

    def delete(self, job_id: str) -> bool:
        """Forget the job and drop it from the index entirely. True if it was there.

        Stronger than retention, which leaves a tombstone: this is the operator
        asking for the job to be gone, and leaving a record that it existed
        would be answering a different question. A queued job is cancelled
        first, so deleting one cannot leave the worker holding a reference to
        a job nobody can look up.
        """
        self.cancel(job_id)
        with self._lock:
            job = self._jobs.pop(job_id, None)
            if job is None:
                return False
            self._order.remove(job_id)
        self._forget(job, "deleted")
        self._save_quietly()
        return True

    # -- retention -------------------------------------------------------

    def forgets_in(self, job: Job, now: float | None = None) -> float | None:
        """Seconds until this job may be forgotten, on this server's own clock.

        `None` when there is nothing to count down to: retention is off, the
        run has not finished, or it has already been forgotten. Never negative
        -- a job past its window that the reaper has not reached yet is `0.0`,
        which is a truthful "any moment now" and not a time in the past.

        **A remaining count rather than an expiry timestamp, because the
        caller is a browser.** A page that subtracted a server timestamp from
        `Date.now()` would be measuring the difference between two *clocks* as
        well as the difference between two moments, and a laptop half an hour
        out would either hide a run that is still there or keep offering
        downloads for one that is gone. Seconds remaining carry no skew: they
        are computed here, against the same clock `sweep` reads, and a page can
        count down from one with no opinion about what time it is.
        """
        if self.retention_seconds is None or job.forgotten or not job.terminal:
            return None
        now = self.clock() if now is None else now
        finished = job.finished_at if job.finished_at is not None else job.created_at
        return max(0.0, finished + self.retention_seconds - now)

    def sweep(self, now: float | None = None) -> list[Job]:
        """Forget every finished job past the window. Returns what it forgot.

        Only terminal jobs, and never a queued or running one: a window
        measured from submission would delete a document out from under the
        merge that is reading it. The clock starts when the job finished, so an
        operator whose merge took forty minutes still gets the whole window to
        collect the report.

        `retention_seconds=None` forgets nothing. It is the opt-out and it has
        to be asked for; see the module docstring for why the default is the
        other way round.
        """
        if self.retention_seconds is None:
            return []
        now = self.clock() if now is None else now
        forgotten = []
        purged = []
        for job in self.jobs():
            if job.forgotten:
                # A tombstone is kept one more window and then dropped from
                # the index and the list. On disk it is a record that a
                # run existed, and "every window retention promises" is the
                # life such a record may have.
                if now - job.forgotten_at >= self.retention_seconds:
                    purged.append(job.id)
                continue
            if not job.terminal:
                continue
            finished = job.finished_at if job.finished_at is not None else job.created_at
            if now - finished < self.retention_seconds:
                continue
            self._forget(job, "forgotten: the retention window has passed")
            forgotten.append(job)
        if purged:
            with self._lock:
                for job_id in purged:
                    self._jobs.pop(job_id, None)
                    self._order.remove(job_id)
        if forgotten or purged:
            self._save_quietly()
        return forgotten

    def _forget(self, job: Job, why: str) -> None:
        """Delete everything of the operator's, in memory and on disk.

        Four things, and the list is the point -- deleting the uploaded text
        and leaving the merged document would be deleting a copy:

          the request        the documents as submitted, and the label of the
                             base -- a filename is frequently the most
                             sensitive line in a confidential document, which
                             is also why `Job` never kept the other labels
          the run and report the merged text, and every claim and piece of
                             evidence quoted out of the sources
          the directory      `merged.md`, `report.json`, `report.html`
          the event log      a failed step's detail can quote a document

        `Job.error` is left alone, and it is the one thing here that can still
        carry a fragment: see `Job.status`. It survives because the tombstone's
        job is to say what became of the run, and "failed" with no reason is
        not an answer. If that trade is ever reversed, this is the line to
        change and `status` is the docstring to correct with it.

        `shutil.rmtree` with `ignore_errors=True`: a directory that is already
        gone is the outcome this is for, and raising here would stop the sweep
        before it reached the next job.
        """
        with self._lock:
            job.request = dataclasses.replace(job.request, documents={}, base=None)
            job.run = None
            job.report = None
            job.forgotten_at = self.clock()
        if job.directory is not None:
            shutil.rmtree(job.directory, ignore_errors=True)
        job.events.forget(why)

    # -- the workers -----------------------------------------------------

    def _work(self) -> None:
        while True:
            job_id = self._queue.get()
            try:
                if job_id is None:
                    return
                job = self.get(job_id)
                # Cancelled between submit and here, or deleted. Not an error:
                # the queue holds ids rather than jobs precisely so that the
                # index stays the one place a job's existence is decided.
                if job is None or job.state != QUEUED:
                    continue
                self._execute(job)
            finally:
                self._queue.task_done()

    def _execute(self, job: Job) -> None:
        with self._lock:
            job.state = RUNNING
            job.started_at = self.clock()
            job.directory = self.work_dir / job.id
        job.events.emit("state", "running", state=RUNNING, terminal=False)
        # Before the first call, so a crash from here on is found `running`
        # by the next start and reported `interrupted` -- never re-run.
        self._save_quietly()
        # The addresses and the keys, from one read. Taken now and not at
        # submit: the file is the operator's or the user's and may have been
        # edited since, and the run that spends a credential should spend the
        # one configured now, at the address configured now.
        #
        # A read that fails ends this job and nothing else. It used to be
        # made outside any handler, so a member's credentials file this
        # server could not use ended the worker thread: the job stayed
        # `running`, and with one worker every later run stayed queued.
        try:
            environ, keys = self.resolved_for(job.owner)
        except (credentials.CredentialsError, user_accounts.AccountError) as exc:
            # Said in full where the operator is. The submitter is told what
            # happened and not where on this server it happened: both
            # messages name a file by its path.
            print(f"llossless serve: run {job.id} was not started: {exc}",
                  file=sys.stderr, flush=True)
            self._finish(job, FAILED, error=(
                str(exc) if isinstance(exc, user_accounts.UnknownAccount) else
                "the endpoints and keys stored for your account could not be "
                "read on this server, so the run was not started. No model "
                "was called. The reason is on the server's own error stream; "
                "ask whoever runs it."))
            return
        workspace = Workspace(
            directory=job.directory, cache_dir=self.cache_dir,
            environ=environ,
            # A callable, which is what keeps the mapping off this frozen
            # dataclass (see `Workspace.keys`). It returns what was read
            # above and reads nothing again: a second read is a second state.
            keys=lambda: keys,
            # The store, not a resolved route. Read when the run resolves
            # its settings: the file is the operator's and may have been
            # edited between submit and start, and a run that executes a
            # program should execute the one configured now.
            routes=self.routes,
            own_addresses=getattr(keys, "addresses", None))
        try:
            job.directory.mkdir(parents=True, exist_ok=True)
            os.chmod(job.directory, DIR_MODE)
            self.runner(job, workspace)
        except Inconclusive as exc:
            # No verdict, and a sentence that says why. `publish` has set the
            # exit code; the message goes out as written.
            self._finish(job, FAILED, error=str(exc))
        except BaseException as exc:  # noqa: BLE001 - see below
            if job.stop.is_set() and not isinstance(exc, (KeyboardInterrupt, SystemExit)):
                # Cancelled, whatever the unit it was in raised on the
                # way out: the flag is what stopped it.
                self._finish(job, CANCELLED, error=cancelled_error(job, exc))
                return
            # Every exception, including the ones that are not `Exception`. A
            # job that dies must not be left reading `running` forever: that
            # state is what a browser polls on, and a worker killed by a
            # `SystemExit` from somewhere deep in a library would otherwise
            # leave a progress bar turning for the life of the process. The two
            # that mean the interpreter is going down are re-raised after the
            # record is made, so the record is written and the thread still
            # ends.
            # Translated for the same reason the event log's failures are,
            # and with the same call: this string is the whole of what a
            # failed job says about itself on a status poll, and "no model
            # named X loaded" is not an account anybody can act on.
            self._finish(job, FAILED,
                         error=diagnose.explain(f"{type(exc).__name__}: {exc}"))
            if isinstance(exc, (KeyboardInterrupt, SystemExit)):
                raise
        else:
            self._finish(job, DONE)

    def _finish(self, job: Job, state: str, *, error: str | None = None) -> None:
        with self._lock:
            job.state = state
            job.error = error
            job.finished_at = self.clock()
        message = error if error is not None else "done"
        job.events.emit("state", message, state=state, terminal=True,
                        exit_code=job.exit_code)
        job.events.close()
        self._save_quietly()

    def _reap(self) -> None:
        """The retention thread. Wakes on the interval, or early on shutdown.

        `Event.wait` rather than `time.sleep`: a `close()` during a sixty-second
        sleep would otherwise wait out the rest of it, and a server that takes
        a minute to shut down is a server somebody kills instead.
        """
        while not self._stopping.wait(self.sweep_seconds):
            try:
                self.sweep()
            except Exception:  # noqa: BLE001 - a reaper that dies stops deleting
                # Swallowed on purpose, and this is the one place in this
                # module where that is right: the reaper is the only thing
                # deleting the operator's documents, and a thread that died on
                # one unlucky job would silently stop deleting everything after
                # it. The next tick tries again.
                continue
