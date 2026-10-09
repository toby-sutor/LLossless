"""The block at the top of every report saying exactly what produced the number.

A quality figure in a README is worth nothing on its own. "94% coverage" is a
different claim depending on whether it came from an 8B model on a laptop or a
frontier model behind an API, on tier-1 constrained decoding or tier-3 prompting
and hope, from a live run or a replay of recordings made three months ago. This
header carries all of it, so any number the project publishes can be traced back
to the conditions that produced it.

It also carries the one disclosure the local-first design principle actually
owes the operator. "Local-first" cannot honestly mean "your documents never
leave the machine", because the tool supports hosted endpoints and people will
use them. It can mean "you are always told, in the report, when they did".
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

from .client import (EXCLUDED, MODEL_OUTCOMES, SEED, TEMPERATURE, UNRULED,
                     UNRULED_OUTCOMES, Client)
from .config import (DEFAULT_FIELD_ORDER, ROOT, Settings,
                     fidelity_name, granted_web_tools)
from . import config
from . import pricing
from . import window as window_module
from .structured import DEFAULT_PROFILE
from .usage import NOT_RETRIEVED, UNMEASURED

# Fields that differ between two runs of identical work. Excluded when reports
# are compared for equality; see the replay determinism acceptance test.
# `latency_ms` is not here: it lives on a live call's ledger row, not this
# top-level block, and the replay test exempts it there by name.
# `window` joins these for the same reason `structured_output.how` is exempt
# from the replay comparison: a replay sends nothing, so it preflights
# nothing, and recording that is a true statement about the run rather than
# drift between two runs of the same thing.
# `calls_by_role` joins on exactly the terms `window` did, for the same
# kind of reason: a replay makes no live call, so the map is
# empty, and that is a true statement about the run rather than drift between
# two runs of the same work. It is the one field here that a *vendor* smoke
# test reads, which is why it has to be recorded rather than inferred from the
# artefacts a role leaves -- those look identical whether the endpoint answered
# or a cassette did.
# The four accounting blocks joined the report on the same terms as
# `duration_seconds`: each carries seconds a stopwatch measured, and a replay
# made no call, so it has none of them to report. `answering_cost` is *not*
# here: it is priced off the ledger's tokens and outcomes, which a replay files
# exactly as its live run did, so the replay test compares it.
VOLATILE = ("generated_at", "duration_seconds", "run_mode", "counts", "window",
            "calls_by_role", "answering_seconds", "excluded", "unruled",
            "discarded_calls")

# What each route kind is called in the rendered block. The words the web
# page's submit button says before the click, said after it: `en.json`'s
# `route.*` strings, and `tests/test_contract_parity.py` holds the two equal.
# The kinds are the web layer's (`web/jobs.ROUTE_KINDS`); this module only
# renders a map it was handed, so a command-line run, which is handed none,
# prints nothing new.
ROUTE_WORDS = {
    "metered": "metered API",
    "subscription": "subscription",
    "command": "command on this server",
    "selfhosted": "local",
    "unknown": "route not identified",
}


def route_said(billed: dict) -> str:
    """`merge: metered API; decompose, verify: local`, roles named every time.

    Roles are named even when all three share one route, because the question
    this answers is asked about one role -- "did the checks go to the
    subscription?" -- and a bare "metered API" makes the reader infer that it
    covered the role they are asking about. A kind this build has no word for
    is printed as `route not identified`, never as its raw identifier and
    never as a guess.
    """
    grouped: dict[str, list[str]] = {}
    for role, kind in billed.items():
        word = ROUTE_WORDS.get(str(kind), ROUTE_WORDS["unknown"])
        grouped.setdefault(word, []).append(str(role))
    return "; ".join(f"{', '.join(roles)}: {word}" for word, roles in grouped.items())


def _cost_block(ledger: list[dict]) -> dict:
    """`pricing.estimate` as the report's five-state dict.

    `state` is carried rather than left to be inferred from `dollars` being
    null, because null has two causes here -- nothing priceable and nothing
    measured -- and a consumer that guessed would guess wrong half the time.
    `usd` is rounded to the cent it will be displayed at, and `usd_exact` is
    kept beside it so a reader reconciling against a vendor bill has the
    figure the arithmetic actually produced.
    """
    found = pricing.estimate(ledger)
    block: dict = {
        "state": found.state,
        "usd": None if found.dollars is None else round(found.dollars, 4),
        # The unrounded figure the arithmetic actually produced.
        # `usd` is what a reader looks at; this is
        # what a figure script sums across cells, so
        # rounding once per cell before adding does not
        # compound into the headline the way rounding `usd`
        # a second time would.
        "usd_exact": found.dollars,
        "priced_calls": found.priced_calls,
        "unpriced_calls": found.unpriced_calls,
        "unmeasured_calls": found.unmeasured_calls,
    }
    if found.unpriced_models:
        block["unpriced_models"] = list(found.unpriced_models)
    # The date the rates were read, so a stale table is visible rather than
    # implied. The rows *this run's own priced calls* actually billed against
    # (`found.priced_skus`), not, as before, every SKU the whole table
    # has ever priced: that read as the *oldest* date on record the moment any
    # other model's rate was read earlier, which named a rate this run never
    # touched. The oldest of the rows actually used is still the honest
    # figure to show, because it is the one that bounds how current *this*
    # run's own number is.
    read_on = sorted({pricing.PRICES[sku].read_on for sku in found.priced_skus
                      if sku in pricing.PRICES})
    if found.dollars is not None and read_on:
        block["rates_read_on"] = read_on[0]
    return block


def _seconds(rows: list[dict], field: str) -> float | None:
    """The sum of `field` over `rows`, in seconds, or None where no row has it."""
    values = [row[field] for row in rows if isinstance(row.get(field), int)]
    return round(sum(values) / 1000, 3) if values else None


def _by_role(rows: list[dict], field: str) -> dict:
    """`_seconds` per role, for the roles that have a figure; sorted."""
    found = {}
    for role in sorted({str(row.get("role")) for row in rows if row.get("role")}):
        seconds = _seconds([row for row in rows if row.get("role") == role], field)
        if seconds is not None:
            found[role] = seconds
    return found


def _accounting(ledger: list[dict], discarded: list[dict]) -> dict:
    """What a benchmark cell is charged with, and everything that is not.

    A cell's cost and time are those of the attempt that produced its
    answer, and a blank, a timeout or a platform failure is excluded. A schema
    repair is the model failing the format it was asked for, so it is charged
    to the model and stays in both answering figures. The split is decided in
    `client` (`MODEL_OUTCOMES`, `DISCARD_KINDS`) and only summed here.

    - `answering_seconds`: `answer_ms` over the ledger rows charged to the
      model, per role and in total. `None`, never zero, where no such row was
      timed -- a replay, a cache hit -- and `untimed_calls` says how many.
      `cli` carries a command route's own `duration_ms`/`duration_api_ms` over
      the same rows, where its envelope gave them; both include the CLI's own
      retries (`backend.cli_timing`).
    - `answering_cost`: `_cost_block` over the same rows, so the never-$0.00
      states hold for it exactly as for `cost`.
    - `excluded`: what is left out. `calls` counts the transport's own
      retries (attempts beyond the first, on every live call) and the
      discarded calls by kind; `seconds` is every live call's `waited_ms`
      and `failed_ms`, plus the answering attempt of every excluded discard;
      `cost` is `_cost_block` over the excluded discards, which is
      `unmeasured` for a call nothing reported tokens for. A transport
      retry has no row and no price: a 429 or a 5xx is not billed, and what a
      timed-out or cut attempt was billed is not reported to anyone.
    - `unruled`: what neither the rule nor the model's side of it covers, kept
      out of both totals until the operator rules: a ceiling cut (a ledger
      row) and a blank that named `length` or `content_filter` (discards).
      Present only when there is one.
    """
    charged = [row for row in ledger if row.get("outcome") not in UNRULED_OUTCOMES]
    held = ([row for row in ledger if row.get("outcome") in UNRULED_OUTCOMES]
            + [row for row in discarded if row.get("counted_as") == UNRULED])
    dropped = [row for row in discarded if row.get("counted_as") == EXCLUDED]
    live = [row for row in ledger if row.get("source") == "live"] + list(discarded)

    seconds = {"total": _seconds(charged, "answer_ms"),
               "by_role": _by_role(charged, "answer_ms")}
    untimed = sum(1 for row in charged if not isinstance(row.get("answer_ms"), int))
    if untimed:
        seconds["untimed_calls"] = untimed
    cli = {name: {"total": _seconds(charged, f"cli_{name}_ms"),
                  "by_role": _by_role(charged, f"cli_{name}_ms")}
           for name in ("duration", "duration_api")
           if _seconds(charged, f"cli_{name}_ms") is not None}
    if cli:
        seconds["cli"] = cli

    kinds: dict[str, int] = {}
    for row in dropped:
        kinds[str(row.get("kind"))] = kinds.get(str(row.get("kind")), 0) + 1
    waited = _seconds(live, "waited_ms") or 0.0
    failed = _seconds(live, "failed_ms") or 0.0
    discards = _seconds(dropped, "answer_ms") or 0.0
    excluded = {
        "calls": {"retries": sum(max(0, row["attempts"] - 1) for row in live
                                 if isinstance(row.get("attempts"), int)),
                  **dict(sorted(kinds.items()))},
        "seconds": {"waited": waited, "failed": failed, "discarded": discards,
                    "total": round(waited + failed + discards, 3)},
        "cost": _cost_block(dropped),
    }

    found = {"answering_seconds": seconds,
             "answering_cost": _cost_block(charged),
             "excluded": excluded}
    if held:
        held_kinds: dict[str, int] = {}
        for row in held:
            kind = str(row.get("kind") or row.get("outcome"))
            held_kinds[kind] = held_kinds.get(kind, 0) + 1
        found["unruled"] = {"calls": dict(sorted(held_kinds.items())),
                            "seconds": _seconds(held, "answer_ms"),
                            "cost": _cost_block(held)}
    return found


def _priced(row: dict) -> dict:
    """A discarded call's row as the report shows it: with its own price.

    `usd_exact` only where the row is both measured and priced, so a blank
    nothing reported tokens for carries no figure rather than `0.0`.
    """
    dollars = pricing.estimate([row]).dollars
    return dict(row, usd_exact=dollars) if dollars is not None else dict(row)


def _cost_sentence(block: dict) -> str:
    """The cost row, saying what it is and what it is not.

    Never a bare figure. An estimate presented as a number is read as a bill,
    and this one is arithmetic over a table of rates somebody typed off a
    pricing page on a stated date -- so the row says `estimate`, says when the
    rates were read, and says plainly when it is a floor rather than a total.

    The four non-priced states get a sentence each rather than a dash. A dash
    is a rendering failure to a reader; these are answers.
    """
    state = block.get("state")
    if state == "none":
        return "no call was made"
    if state == "unmeasured":
        return (f"unmeasured ({block['unmeasured_calls']} call(s) reported no "
                f"tokens, so no figure can be derived)")
    if state == "unpriced":
        named = ", ".join(block.get("unpriced_models") or []) or "this endpoint"
        return f"not priced here ({named})"

    figure = f"~${block['usd']:.2f} estimated"
    detail = [f"rates read {block['rates_read_on']}"] if block.get("rates_read_on") else []
    if state == "partial":
        left = []
        if block["unpriced_calls"]:
            named = ", ".join(block.get("unpriced_models") or [])
            left.append(f"{block['unpriced_calls']} call(s) on {named} not priced"
                        if named else f"{block['unpriced_calls']} call(s) not priced")
        if block["unmeasured_calls"]:
            left.append(f"{block['unmeasured_calls']} call(s) reported no tokens")
        detail.insert(0, "a floor, not a total: " + "; ".join(left))
    return f"{figure} ({'; '.join(detail)})" if detail else figure


def git_commit(root: Path = ROOT) -> str:
    """The commit this run was produced by, read straight from .git.

    Read rather than shelled out to: git may not be installed in the container,
    and a subprocess for one line of a text file is not worth the failure mode.
    """
    gitdir, common = _git_dirs(root)
    try:
        content = (gitdir / "HEAD").read_text(encoding="utf-8").strip()
    except OSError:
        return "unknown"
    if not content.startswith("ref:"):
        return content[:12]

    ref = content.split(maxsplit=1)[1]
    # The ref itself is looked up in the **common** directory, not the
    # worktree's own. A linked worktree has a private `HEAD` and shares
    # `refs/` and `packed-refs` with every other worktree on the repository,
    # so resolving the ref beside the HEAD that named it finds nothing.
    direct = common / ref
    if direct.exists():
        return direct.read_text(encoding="utf-8").strip()[:12]
    packed = common / "packed-refs"
    if packed.exists():
        for line in packed.read_text(encoding="utf-8").splitlines():
            if line.endswith(f" {ref}"):
                return line.split(maxsplit=1)[0][:12]
    return "unknown"


def _git_dirs(root: Path) -> tuple[Path, Path]:
    """Where this checkout's `HEAD` lives, and where its refs live.

    The same path twice for an ordinary clone, and that is the case worth
    stating first: `root/.git` is a directory, `HEAD` and `refs/` are both
    inside it, and nothing below changes what this function has always
    returned.

    **A linked worktree is the case this exists for.** `git worktree add`
    leaves a `.git` *file* holding `gitdir: <path>`, so reading
    `root/.git/HEAD` as a path raises and every run made from a worktree
    recorded its provenance as `unknown` -- the commit silently missing from
    exactly the checkouts a second line of work is done in. Found by running
    the paper's own build step from one, which wrote `unknown` over a real commit
    in its generated output, `paper/generated/numbers.json`.

    Shelling out to `git rev-parse` would be shorter and is refused for
    `git_commit`'s own reason: git may not be installed in the container, and
    a subprocess for one line of a text file is not worth the failure mode.
    """
    marker = root / ".git"
    if marker.is_dir():
        return marker, marker
    try:
        content = marker.read_text(encoding="utf-8").strip()
    except OSError:
        return marker, marker
    if not content.startswith("gitdir:"):
        return marker, marker
    # Relative to the file that names it, which is how git writes it when the
    # worktree and the repository share a parent.
    gitdir = Path(content.split(maxsplit=1)[1])
    if not gitdir.is_absolute():
        gitdir = (root / gitdir).resolve()
    # `commondir` is how the worktree names the repository it belongs to.
    # Absent for a plain `gitdir:` redirect (a submodule), where the one
    # directory holds both.
    pointer = gitdir / "commondir"
    if not pointer.is_file():
        return gitdir, gitdir
    try:
        shared = Path(pointer.read_text(encoding="utf-8").strip())
    except OSError:
        return gitdir, gitdir
    if not shared.is_absolute():
        shared = (gitdir / shared).resolve()
    return gitdir, shared


# The committed cassette directory. A sweep's own output must not count as a
# source change, for exactly the reason untracked files do not: the sweep writes
# it while it runs. Untracked output was already excluded, which quietly made the
# rule depend on whether a corpus happened to be new or a rewrite — `--force`
# over an existing corpus dirties the tree on its first call, and every cassette
# written afterwards is stamped `-dirty` for a change that is the recording
# itself. That is a false alarm about the source, which is the one thing the
# suffix is supposed to be about.
#
# Only this path needs naming. The exploratory corpora under `tests/eval/*/` are
# gitignored, so they are untracked and already excluded.
RECORDED_OUTPUT = "tests/responses"

# The paper's build stamp has the same shape of problem one directory over.
# The paper's generated numbers file is tracked and carries the commit the PDF was
# built from, so writing it is the build's own output: leave it in scope and
# the first `make paper` after a commit stamps a clean revision, the second
# stamps `-dirty` for nothing but the stamp the first one wrote. Passed in by
# the caller rather than added here, because a `verify` run has no paper and
# an amnesty nobody asked for is how the suffix stops meaning anything.
PAPER_OUTPUT = "paper/generated"


# Where an untracked file counts as source. `src/` and `prompts/` are
# what a report's commit-provenance field claims to describe, and an untracked
# file shadowing a tracked one there is not a smaller kind of edit -- an
# untracked `src/llossless/_prompts/` takes precedence over the tracked
# `prompts/` whenever a checkout looks like an install (`prompts.py`'s
# `PROMPT_CANDIDATES`), and it is invisible to `--untracked-files=no` below.
# Not the whole tree: a sweep's own untracked output elsewhere (a fresh
# corpus under `tests/eval/*/`, a cache directory) is not a source edit, and
# counting it would make the guard noise within a minute of being useful --
# the same reasoning that already excludes it everywhere else in this module.
UNTRACKED_SOURCE_PATHS = ("src", "prompts")


def is_dirty(root: Path = ROOT, exclude: tuple[str, ...] = ()) -> bool | None:
    """Are there uncommitted changes to tracked *source* files? None if git could not say.

    Two things are excluded, on one principle: a recording sweep's own output is
    not evidence that the code producing it changed.

    Untracked files are excluded for most of the tree, because a sweep writes
    them as it runs. Counting those would make every sweep dirty by its second
    call, which would turn the guard below into noise within a minute of being
    useful. `UNTRACKED_SOURCE_PATHS` is the one exception: an untracked file
    under `src/` or `prompts/` is checked too, because those two are exactly
    what a reader is relying on when they reproduce a number, and a file that
    is new rather than edited is not a smaller kind of change to either.

    `tests/responses/` is excluded whether tracked or not, because a re-record
    rewrites cassettes in place and a resumed or relaunched sweep would
    otherwise label its whole corpus `-dirty` on account of the corpus. What
    remains in scope is `src/`, `prompts/`, the fixtures and the runners — the
    things whose state a reader is actually relying on when they reproduce a
    number.

    Shelled out to, unlike `git_commit`, because reproducing "is the worktree
    different from the index" from the files in .git is a real implementation
    and not a line of parsing. When git is absent the answer is None, which
    callers treat as unknown rather than clean.
    """
    try:
        done = subprocess.run(
            # The pathspec is what excludes the corpus. `--untracked-files=no`
            # alone would not: it drops new cassettes and keeps rewritten ones.
            [
                "git", "status", "--porcelain", "--untracked-files=no",
                "--", ".", f":(exclude){RECORDED_OUTPUT}",
                *(f":(exclude){path}" for path in exclude),
            ],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        # A second, narrower call rather than one `--untracked-files=normal`
        # pass over the whole tree: that would also have to repeat every
        # exclusion above (the corpus, the caller's own), and an untracked
        # cassette or scratch file anywhere outside `src/`/`prompts/` must
        # stay invisible here exactly as it always has.
        untracked = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=normal",
             "--", *UNTRACKED_SOURCE_PATHS],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if done.returncode != 0 or untracked.returncode != 0:
        return None
    return bool(done.stdout.strip()) or bool(untracked.stdout.strip())


def source_state(root: Path = ROOT, exclude: tuple[str, ...] = ()) -> str:
    """One string naming the code that produced a recording.

    This is what a cassette carries and what a resumed sweep is checked
    against: `a1b2c3d4e5f6`, or `a1b2c3d4e5f6-dirty` when tracked files had
    uncommitted edits, or `-unknown` when git could not be asked.

    `exclude` adds pathspecs to the ones `is_dirty` already drops, for a caller
    whose own output is tracked. Named by the caller, never defaulted.

    A dirty tree does not silently poison a cassette — everything that changes
    a response is already in the cassette key, so an edited prompt produces a
    new key rather than a stale hit. What it poisons is the claim that a corpus
    was produced by one revision, which is the claim a reader relies on when
    they reproduce a number from the README.
    """
    dirty = is_dirty(root, exclude)
    suffix = {True: "-dirty", False: "", None: "-unknown"}[dirty]
    return f"{git_commit(root)}{suffix}"


@dataclass(frozen=True)
class Provenance:
    settings: Settings
    client: Client
    roles: tuple[str, ...]
    duration_seconds: float
    # Which document governed the merge, and whether anyone said so. Passed in
    # rather than read off `Settings`, because it is not a setting: it names one
    # of the documents this particular run was given, and a `verify` run made no
    # merge and so has no base at all. `merge.MergeResult` is where it is
    # resolved and this is where it is published; nothing recomputes it.
    base: str | None = None
    base_chosen: str | None = None
    # How each role was paid for, in `ROUTE_WORDS`' kinds, when the caller knew.
    # Only the web server does: it chose the route or the endpoint per
    # role from a row the operator picked, and the page's button named that
    # route before the click. `None` on the command line, where the operator
    # typed the endpoint and no such choice was made on their behalf.
    billed: dict | None = None
    # Taken once, here, rather than inside `as_dict`. `as_dict` used to
    # call `datetime.now` itself, and it is not the only reader: `rows` and
    # `notes` each call it too, `as_markdown` calls both of those, and the
    # report writer calls `as_dict` again on its own for the JSON export,
    # five live reads of the clock for one run's Markdown, HTML and JSON
    # reports between them, any two of which can disagree the moment a
    # second boundary falls between them (`isoformat(timespec="seconds")`
    # already throws away anything finer). A `default_factory` runs once, in
    # `__init__`, the moment this run's `Provenance` is built, so every
    # rendering after that reads the same field rather than the clock.
    generated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds"))

    @property
    def hosted(self) -> bool:
        """Did any document leave this machine. Across every endpoint, not one.

        Replay and dry run both send nothing, so neither can have leaked
        anything however remote the configured endpoint is. The warning has to
        be true when it appears or it stops being read.

        **Asked of `config.addresses`, not of `settings.is_local`.** `is_local`
        answers for the run-wide `base_url` alone, which was the whole story
        until a run could hold several endpoints at once. The web interface
        routes each role to its model's provider and leaves `base_url` at the
        server's own default, so a run whose every call went to a vendor
        reported `content_left_this_machine: false` and an endpoint id
        belonging to the local machine it never used.

        The operator found it in their first real vendor run: nine live calls
        to OpenAI, 264 seconds, and a provenance block saying the content
        stayed here. This block exists to answer exactly that question, so
        getting it backwards is worse than omitting it -- a reader who checks
        is a reader who was relying on it.
        """
        if self.settings.mode in ("replay", "dry-run"):
            return False
        # A command backend has no URL to classify, and silence here would be
        # read as "no". Everything this block relies on stops at the
        # process boundary: `config.check_base_url` has no address to inspect,
        # and the suite's network containment is per-process, so a
        # child that opens a socket opens it unobserved. The tool therefore
        # cannot establish that a document stayed on this machine, and the
        # honest answer to a question it cannot answer is the one that makes a
        # reader check rather than the one that makes them stop reading.
        #
        # This is the same question reached by a second route, and it is answered the same
        # way: getting it backwards is worse than omitting it.
        if self.settings.command:
            return True
        return any(not config.is_loopback(urlsplit(url).hostname or "")
                   for _, url in config.addresses(self.settings))

    def as_dict(self) -> dict:
        usage = self.client.usage
        # Read off `Settings.command_for` by role, the way `retrieval.permitted`
        # is read off the argv rather than off the table that produced it: what
        # is printed is what the run was really asked for, and a table this
        # build never reached cannot put a level in here.
        effort = {role: self.settings.effort_for(role)
                  for role in sorted(config.ROLES)
                  if self.settings.effort_for(role)}
        # Which of this run's roles answered through a model that takes one
        # level of effort rather than a scale -- a command
        # route never gets `--effort` for one (`config.auto_effort`), and an
        # HTTP route never had one to send in the first place (`structured.py`'s
        # `anthropic` profile has no graded field at all). Named here rather
        # than left as an absence in `effort` above, because silence there
        # reads as "the program's own default", which is a different claim
        # from "this model has no scale to default away from".
        #
        # `_effort_model`, not `_model`: a command backend's calls are gated
        # on `stated_model` -- the argv's own `--model`, what `auto_effort`
        # and every table in `config.py` are keyed by -- and `Settings.models`
        # is mostly inert there (`model_for`'s own docstring). `_model` is
        # still right for an HTTP role, which has no argv to read.
        single_level = sorted(role for role in self.roles
                              if config.is_single_level_model(self._effort_model(role)))
        # The client's own stamp, taken once at `Client.__init__`, not
        # `git_commit()` read fresh here: `git_commit()` is HEAD alone and can
        # never say `-dirty`, which is exactly the state every `--no-cache`
        # benchmark run is made in, since it never records. Falling back to
        # `git_commit()` only covers a `Provenance` built around something
        # that is not a real `Client` (a test double); every real run has the
        # attribute.
        commit_at_start = getattr(self.client, "_source", None) or git_commit()
        # Re-checked here, at report-write time, rather than trusted from
        # init: the one thing a single read at the start cannot catch is a
        # commit made *during* the run (a wrapper script, an operator in
        # another terminal), and a report claiming the tree never moved would
        # be wrong in the one direction that matters -- looking cleaner than
        # it was. When the two agree, `commit_at_start` is the whole story and
        # nothing more is said, so this changes no existing report.
        commit_at_end = source_state()
        commit_changed = commit_at_end != commit_at_start
        accounting = _accounting(usage.ledger, usage.discarded)
        return {
            "generated_at": self.generated_at,
            "claimcheck_commit": commit_at_start,
            # Present only when the tree moved between the two reads.
            # Two fields rather than one, because "it changed" and "what it
            # became" are different facts and a reader has to have both: the
            # commit a run *started* under is what every other field in this
            # block describes, and the commit it *ended* under is what the
            # next run will be compared against.
            **({"claimcheck_commit_end": commit_at_end,
                "claimcheck_commit_changed": True} if commit_changed else {}),
            "run_mode": self.settings.mode,
            "endpoint": {
                # The id, not the address. A run report is committed alongside
                # the cassettes it summarises, and the same reasoning applies:
                # what a reader needs is whether two runs used one machine and
                # whether content left this one, and neither question needs a
                # hostname. The operator's own address stays in the environment.
                "id": self.settings.endpoint_id,
                # "hosted" the moment any endpoint is, for the reason on
                # `hosted` above. Reporting the run-wide address's own
                # classification described a machine several of these calls
                # never touched.
                # `command` rather than `hosted` for a subprocess, because
                # the two are not the same disclosure: `hosted` names an
                # endpoint this tool addressed and can describe, and a command
                # backend is the case where it addressed nothing and can
                # describe nothing. `content_left_this_machine` is true beside
                # it either way -- see `hosted` -- and the pair reads as what
                # it is: something answered, and the tool cannot tell you from
                # where.
                "location": ("command" if self.settings.command
                             else "hosted" if self.hosted
                             else self.settings.where),
                "content_left_this_machine": self.hosted,
                # What a person calls the thing that answered, when anything
                # does. A command backend's id is the hashed command, which is
                # unreadable by design, and `location: command` says which
                # mechanism and not which route -- so a reader a week later
                # could tell that *a* program answered and not *which*. The
                # operator's own label closes that, verbatim and never
                # inferred: `commands.py` refuses a route without one, because
                # guessing that `claude` means Opus 5 is how a correct-looking
                # record describes the wrong bill.
                #
                # Absent for every HTTP run, which is every recorded figure in
                # this project. A key that is present and empty would add a
                # line to all of them saying nothing changed.
                # Written over three lines rather than inline so that the key
                # sits at the start of one. `test_web_static.py`'s guard reads
                # `as_dict`'s source for keys in exactly that position and
                # requires each to reach `renderProvenance`, and the inline
                # spelling one field up is why `by_role` has never been held to
                # it. A disclosure this milestone is about is not going in
                # under the one shape that check cannot see.
                **({
                    "route": self.settings.command_label,
                } if self.settings.command and self.settings.command_label
                    else {}),
                # Every distinct endpoint this run could reach, by id and role,
                # whenever there is more than one. A single id under a run that
                # used three endpoints is not a smaller truth, it is a
                # different one.
                # Dropped entirely for a command backend, which addresses
                # none of them. Listing endpoints a run configured and
                # never used describes a routing that did not happen, and the
                # reader most likely to check this block is the one asking
                # where their documents went.
                **({"by_role": {role or "default": self.settings.endpoint_id_for(role)
                                for role, _ in config.addresses(self.settings)}}
                   if not self.settings.command
                   and len(config.addresses(self.settings)) > 1 else {}),
                # How each role was paid for, per role, when the caller chose
                # the route. The id above says which box and `location`
                # says whether anything left this one; neither says whether the
                # checks went to a subscription or to a metered API, which is
                # the question the web page's split control made askable.
                # Absent on every command-line run and every recorded figure.
                **({
                    # In `models`' order, so the two read down together.
                    "billed": {role: self.billed[role] for role in self.roles
                               if role in self.billed},
                } if self.billed else {}),
            },
            # Printed on every report, including `verify` runs that made no
            # merge call. The level is a *verification* parameter as much as a
            # merge one — at `off` a rewording is a defect and at `high` it is
            # the requested behaviour — so the same coverage number means
            # different things at different levels, and a reader who cannot see
            # which one produced it cannot interpret it.
            # The title policy rides with it for the same reason one step down:
            # `choose-best` lets the merge take a heading neither the base nor
            # the reconciler's segment set predicts, so a coverage number is
            # read differently depending on which policy produced it.
            # The base rides with both, because it is their operand. Under
            # `keep-base` the base decides the merged title and under every
            # policy it decides the structure, so `title_policy: keep-base`
            # without it states a rule and withholds the document it applies to.
            # The canonical name, not the caller's path: it is the name the
            # prompt showed the model and the name every disposition record
            # points at.
            # The verification depth rides here too, and it is the one field in
            # this block that changes what a *clean* report means. At
            # `coverage` nothing ever read the merged document back, so exit 0
            # says the sources' content survived and says nothing at all about
            # invention. The two skipped steps record that inside the run
            # (`cli.pipeline`), but a reader holding two reports side by side
            # compares this block, and a depth visible only as an absence in a
            # step list is a depth nobody notices.
            "merge_policy": {
                "fidelity": self.settings.fidelity,
                "verify_depth": self.settings.verify_depth,
                "title_policy": self.settings.title_policy,
                "base": self.base,
                "base_chosen": self.base_chosen,
            },
            "models": {role: self._model(role) for role in self.roles},
            # What a role's own calls said actually answered, distinct from
            # the label above: `models` is the alias the route
            # asked for and stays that, whatever answered. This reads the
            # same per-call facts `model_said` already renders into the
            # Markdown table -- a command backend's `answered_by`
            # (`modelUsage`'s resolution) or an HTTP call's `served_model`
            # (`usage.served_model`) -- as data rather than only a sentence,
            # so a reader comparing runs does not have to parse one. Absent
            # for a role no live or replayed call ever named a model for,
            # which is every role on an endpoint that reports none (most of
            # this project's own corpus) and every replay of a recording made
            # before either mechanism existed.
            **({"models_answered": answered_map}
               if (answered_map := self._models_answered()) else {}),
            # `field_order` rides with the tier, not with the merge policy: it
            # says how strictly a response was read, which is what the tier
            # says. Always in the JSON, because a machine reading two runs has
            # to be able to tell which one relaxed the contract. Resolved, not
            # the setting: a replay reads an answer no more strictly than its
            # recording did, so a replay of an `any` corpus reports `any`
            # whatever it was passed.
            "structured_output": {
                "mode": self.client.resolved_tier(),
                "how": self.client.tier_source,
                "field_order": self.client.resolved_field_order(),
            },
            "prompts": dict(sorted(usage.prompts.items())),
            "decoding": {
                # Read from the last live call's own request
                # body when there was one -- `Usage.ledger`, written from
                # `body` at the point it was serialised, never rebuilt -- and
                # only the module constant when nothing this run actually sent
                # could be asked: a replay or a cache-only run. Reconstructing a
                # body to check one was ruled out; this instead
                # reports the one that was already kept.
                "temperature": self._wire_temperature(),
                "seed": self._wire_seed(),
                # Which request envelope went out, and only when it was not
                # the default one. Conditional for the reason `reasoned_anyway`
                # below is: every record in this corpus was produced before
                # profiles existed, all of them on the default, and an
                # unconditional key would rewrite their provenance to report
                # a choice nobody made. Present, it is load-bearing -- it says
                # which of the fields above actually reached the endpoint.
                **({"profile": self.settings.profile}
                   if self.settings.profile != DEFAULT_PROFILE else {}),
                # Which roles were allowed a reasoning block. It belongs with
                # temperature and seed: it changes the answer, so a number
                # produced with it on is not comparable to one produced without.
                # Per role, the last live call's wire body overrides the
                # configured set -- same reasoning as `temperature` above, and
                # for the same run this fixes: a run whose live thinking state
                # ever disagreed with `Settings.thinking` must say the wire's
                # answer, not the setting's.
                "thinking": self._wire_thinking_roles(),
                # What the endpoint did, when it differs from what was asked.
                # Present only then, like `model_loads` below and for the same
                # reason: every run in the recorded corpus was answered by a
                # model that did as it was told, and an unconditional key would
                # rewrite all of their provenance blocks to report the absence
                # of a thing that did not exist when they were measured.
                **({"reasoned_anyway": sorted(usage.thinking_ignored)}
                   if usage.thinking_ignored else {}),
                # How hard the command backend was asked to think, read back
                # off the argv the run will really execute -- the same
                # direction, and for the same reason, as `retrieval.permitted`
                # below. It belongs with `thinking` one field up: a level that
                # cuts reasoning tokens by an order of magnitude changes the
                # answer, so a figure produced at one is not comparable to one
                # produced at another.
                #
                # Present only when there is a level to name. Empty covers an
                # HTTP endpoint, a program `AUTO_EFFORT` has no row for, and a
                # command that names none -- "the program's own default" is a
                # different statement from any level, and an unconditional key
                # would write a claim about effort into the provenance of
                # every HTTP run in the recorded corpus.
                #
                # **A map, role -> level, and never one value**. The
                # merge is asked for more than the two roles that read its
                # work back, so a single figure here would be true of one call
                # of six and false of the rest -- and a reader comparing two
                # runs would be comparing a number neither of them ran at.
                # Roles that share a level still each get their own row: a
                # reader must not have to know which way round a shorthand
                # went. `sorted`, so the block is stable across runs.
                **({"effort": effort} if effort else {}),
                # The label, not a level: `config.SINGLE_LEVEL_LABEL`, once per
                # role named above, never a value this model was not asked
                # for and could not have honoured.
                **({"effort_single_level": {role: config.SINGLE_LEVEL_LABEL
                                            for role in single_level}}
                   if single_level else {}),
                # What was asked for and could not be delivered, kept beside
                # what was: an operator who names a level for an HTTP endpoint
                # or for a program whose flags this build has not read is not
                # refused, so the only way they learn is here.
                **({"effort_ignored": list(self.settings.effort_ignored)}
                   if self.settings.effort_ignored else {}),
                # Whose choice a level was, when it was a web request's:
                # role -> the level the requester picked on the page's slider.
                # `effort` above is what the argv carried, and `route_plan`
                # refuses a level the route cannot carry, so the two agree for
                # every role named here. Absent for every other run, whose
                # level is the operator's or this build's table.
                **({"effort_requested": dict(sorted(self.settings.effort_requested.items()))}
                   if self.settings.effort_requested else {}),
            },
            "counts": {
                "calls": usage.calls,
                "cache_hits": usage.cache_hits,
                "replayed": usage.replayed,
                "schema_repairs": usage.repairs,
                # A run that found its endpoint cold and loaded the model, and
                # a run that found it warm, are two different runs. The figure
                # is here rather than folded into `calls` because a warm-up
                # carries no prompt, is keyed into no cassette and is charged to
                # no budget -- see `Usage.warmups`.
                "model_loads": usage.warmups,
                "errors": usage.errors,
                "salvaged": usage.salvaged,
                # Omitted, not zeroed, when nothing reported a figure.
                #
                # These two are plain ints starting at zero and are only ever
                # incremented from a usage block that arrived, so a run against
                # an endpoint that reports none published `prompt_tokens: 0`
                # beside a `tokens_described` reading `unknown` -- two fields in
                # one block contradicting each other, and the one a machine
                # reads saying the wrong thing.
                #
                # `usage.py`'s rule in one line: "Unknown is not zero. A
                # token-free arm and an unmeasured arm support opposite
                # conclusions about cost." `Tokens.as_dict` already drops
                # absent fields for exactly this reason; `counts` now agrees
                # with it rather than contradicting it four lines below.
                #
                # The attributes themselves stay ints, because the bench
                # runners subtract one reading from another to attribute spend
                # to a unit of work and a `None` there would be a new failure
                # in place of an old lie.
                **({"prompt_tokens": usage.prompt_tokens}
                   if usage.tokens.get("input") is not None else {}),
                **({"completion_tokens": usage.completion_tokens}
                   if usage.tokens.get("output") is not None else {}),
            },
            # The full token picture, normalised across vendors, kept apart
            # from `counts` because it answers a different question and answers
            # it in a shape `counts` cannot hold. Every value there is an int; a
            # field absent here means no response reported it, and
            # `unmeasured_calls` says how many responses reported nothing at
            # all. An arm that spent nothing and an arm nobody measured are
            # different facts and the cost table needs to tell them apart.
            "tokens": usage.tokens.as_dict(),
            # The same figures as one sentence. In the dict rather than
            # composed in `rows`, so the Markdown table, the HTML table and the
            # JSON cannot disagree about whether a run was measured.
            "tokens_described": usage.tokens.describe(),
            # One row per response body charged, in order. Additive: the
            # totals above are unchanged and are still the figure to read for
            # a run. This is for the two questions a total cannot answer --
            # reconciling a vendor's bill against what the tool believed it
            # spent, and deciding whether two draws sent the same bytes. A row
            # with no `prompt_tokens` or `completion_tokens` key is a call the
            # vendor reported no usage for; the rule for that is one level down.
            "ledger": usage.ledger,
            # What the run cost, derived from the ledger above rather than
            # from the totals: a run can put three roles on three models at
            # three rates, and one total divided by one rate is a number with
            # no referent.
            #
            # **`dollars` is null for anything this table cannot price**, and a
            # reader is told which of the two reasons applied. `$0.00` is never
            # written for an unknown, because it reads as "measured, and free"
            # -- the inversion was already fixed once in `counts`,
            # and the one a cost display has exactly one way to make.
            "cost": _cost_block(usage.ledger),
            # What a benchmark cell is charged with, and what it is not.
            # `cost` above is unchanged -- every response body the ledger
            # charged, a ceiling cut included. These four are a separate reading of
            # the same run: see `_accounting`. `discarded_calls` is the live
            # calls that never reached the ledger (a blank re-asked, a call
            # the platform lost), each with the tokens its vendor reported
            # and its own price; kept out of `ledger` because the replay test
            # compares that list verbatim and a replay never meets them.
            "answering_seconds": accounting["answering_seconds"],
            "answering_cost": accounting["answering_cost"],
            "excluded": accounting["excluded"],
            **({"unruled": accounting["unruled"]} if "unruled" in accounting else {}),
            "discarded_calls": [_priced(row) for row in usage.discarded],
            # Which mechanism guarded which role against overrunning the
            # context window. A role absent here asked nothing of the kind --
            # replay and dry run, which send nothing. See `notes()` for the
            # reader-facing sentence this backs.
            "window": dict(sorted(usage.window_mechanism.items())),
            # Live calls per role. `calls` above is the run's total and cannot
            # say which endpoint answered for which role, which is the question
            # a per-role configuration exists to raise. A role absent here
            # made no live call: replay, cache hit or dry run.
            "calls_by_role": dict(sorted(usage.calls_by_role.items())),
            # What the model was *permitted* to reach for, and whether it did.
            # Two fields, because they are two facts and a reader
            # needs both: a run that retrieved nothing because it was granted
            # nothing and a run that was granted a tool and did not use it are
            # the same empty result and opposite conclusions about the
            # citations under it.
            #
            # `permitted` is `granted_web_tools` and never `retrieval_tools`,
            # and the difference is the whole honesty of the row. The second
            # answers "what *would* a sourced run get", which is the question
            # the route picker asks; this one reads the argv this run will
            # really execute, so a run at any level below sourced reports the
            # empty grant it actually had. Empty on every HTTP endpoint, which
            # is what an HTTP endpoint can honestly say here.
            #
            # **Neither is a claim about this process.** LLossless opens no
            # socket for any purpose; a tool call happened in the model's own.
            "retrieval": {
                "permitted": list(granted_web_tools(self.settings.command)),
                "tool_use": usage.turns.as_dict(),
                "described": usage.turns.describe(),
            },
            # Whether the command backend that answered this role ran
            # isolated: safe mode, and the exact `--tools` grant, off
            # `Settings.command_for(role)` -- the argv the call really
            # executed, never reconstructed from `command` or from `ISOLATED`
            # membership. `retrieval.permitted` above is empty at every
            # level but `sourced`, so a `high` report through the isolated
            # `claude` command said nothing about the isolation at all: an
            # operator reading it could not tell their own CLAUDE.md, skills,
            # plugins and MCP servers had been kept out of that run. This
            # block says so at every level, because safe mode is on
            # at every level and a reader deserves the same disclosure
            # regardless of which one produced the number in front of them.
            #
            # Per role, like `effort`, and for the same reason: the roles
            # share one route today, but a reader must not have to assume
            # that stays true, and a map that already answers per role cannot
            # be quietly true of one call and false of the rest tomorrow.
            #
            # `tools` is `None` for a role whose executed argv carries no
            # `--tools` at all -- unrestricted, the case for every program
            # outside `ISOLATED` unless the operator wrote one themselves --
            # and `[]` for `--tools ""`, an explicit grant of nothing. The two
            # are opposite facts and this is the one field in the report that
            # keeps them apart rather than collapsing both to empty.
            #
            # Present only for a command backend: an HTTP endpoint has no
            # argv for either flag to be on, and an always-present key would
            # write `safe_mode: false` into the provenance of every recorded
            # figure in this project, about a mechanism that did not exist
            # when they were measured.
            **({
                "isolation": {
                    role: {
                        "safe_mode": config.command_safe_mode(
                            self.settings.command_for(role)),
                        "tools": (list(tools) if (tools := config.stated_tools(
                            self.settings.command_for(role))) is not None
                            else None),
                        # Names only, never values: what the child's
                        # environment left out. `config.dropped_env_names`
                        # rather than `backend`'s copy of the same call, so
                        # this module never has a reason to import `backend`
                        # (and, through it, `transport`) merely because a
                        # command was configured -- a replay of a
                        # command-backend corpus must stay as import-free as
                        # every other replay. `for_report=True`: `LLOSSLESS_*`
                        # is still dropped from the child, but it is this
                        # tool's own configuration and not what this field
                        # means to disclose, and reporting it made the same
                        # setting's two spellings (`--answer-with` against
                        # `LLOSSLESS_COMMAND=`) print two different lists.
                        "env_dropped": config.dropped_env_names(for_report=True),
                        # The seconds one call on this route got: read
                        # off `Settings.call_timeout`, never `.timeout`, for
                        # the reason that property's own docstring gives --
                        # `COMMAND_TIMEOUT` (890s) the moment the operator
                        # stated nothing, and this is the one place a
                        # command backend's own default differs from the
                        # HTTP path's. Absent from the recorded corpus until
                        # now, and a reader comparing a stopped run against
                        # this figure could not previously tell a slow model
                        # from a route configured too tight to finish it.
                        "timeout": self.settings.call_timeout,
                    }
                    for role in self.roles
                },
            } if self.settings.command else {}),
            "duration_seconds": round(self.duration_seconds, 1),
        }

    def _wire_temperature(self):
        """The last live call's own temperature, or the constant if none ran.

        `TEMPERATURE` is what every call is built to send; this is what one
        actually did. They agree on every run in the recorded corpus, because
        nothing today varies `structured.build_body`'s `temperature` argument
        per call -- but a report that echoed the constant regardless would
        have said `0.0` about a smoke run too, which sent no
        `temperature` key at all. Read off `Usage.wire_temperature` rather
        than the ledger: the ledger row is shared with replay and cache, which
        send nothing, so a wire-only fact cannot live there without breaking
        the replay determinism acceptance test (the same "not the
        rebuild" rule applies here: `_record_usage` reads it once, off
        `body`, and keeps it off the row).
        """
        wire = self.client.usage.wire_temperature
        return wire if wire is not None else TEMPERATURE

    def _wire_seed(self):
        """The last live call's own seed, or the constant if none ran.

        The sibling of `_wire_temperature` and it exists for the sharper half
        of the same reason. `SEED` used to be printed unconditionally, which
        was true of every run this project has made -- and stops being true the
        moment a request profile drops the field, because Anthropic's surface
        has no `seed` at all. A block reporting `seed 0` over a request that
        carried none is not reporting a decoding condition, it is inventing
        one. `client.NOT_SENT` arrives here and is printed as itself.
        """
        wire = self.client.usage.wire_seed
        return wire if wire is not None else SEED

    def _wire_thinking_roles(self) -> list[str]:
        """Which roles thought, per the wire where a live call said so.

        Starts from `Settings.thinking` -- the configuration, and the only
        answer available for a role no live call ever reached, such as every
        role on a replay. Each role a live call *did* reach is then corrected
        to what that call's own body carried, which is `Usage.wire_thinking`:
        written in `Client._record_usage` from `body`, never from the setting
        that requested it.
        """
        roles = set(self.settings.thinking)
        for role, wire_on in self.client.usage.wire_thinking.items():
            if wire_on:
                roles.add(role)
            else:
                roles.discard(role)
        return sorted(roles)

    def _model(self, role: str) -> str:
        try:
            return self.settings.model_for(role)
        except Exception:  # noqa: BLE001 - an unconfigured role is reported, not fatal
            return "unset"

    def _effort_model(self, role: str) -> str:
        """The model name that actually governs whether this role's calls can
        carry a graded `--effort`.

        A command backend's calls are started against whatever `--model` its
        own argv names -- `config.stated_model`, the same reader
        `config.auto_effort` and `config.is_single_level_model` are keyed
        against -- and not against `Settings.models`, which such a backend
        mostly ignores. An HTTP role has no argv of its own, so `_model` (off
        `model_for`) is the one true answer there.
        """
        if self.settings.command:
            return config.stated_model(self.settings.command)
        return self._model(role)

    def _models_answered(self) -> dict:
        """`models_answered`'s value: every role that named an answering model.

        Aggregates across every ledger row of a role, the way `model_said`
        does for the Markdown table: every distinct id any row named, and the
        single author when every row that named one agrees, `None` when they
        disagree or none did. A role with no such row is left out entirely,
        never printed as an empty block.
        """
        found: dict[str, dict] = {}
        for role in self.roles:
            named = []
            for row in self.client.usage.ledger:
                if row.get("role") != role:
                    continue
                block = row.get("answered_by")
                if isinstance(block, dict) and block.get("models"):
                    named.append(block)
                    continue
                served = row.get("served_model")
                if isinstance(served, str) and served:
                    named.append({"models": [served], "output": served})
            if not named:
                continue
            models = list(dict.fromkeys(
                name for block in named for name in block.get("models") or []))
            outputs = {block["output"] for block in named if block.get("output")}
            found[role] = {"models": models,
                           "output": outputs.pop() if len(outputs) == 1 else None}
        return found

    def rows(self) -> list[tuple[str, str]]:
        """The provenance block as label/value pairs, before any renderer sees it.

        Split out of `as_markdown` so the HTML report shows the same rows rather
        than a second list assembled from the same dict. The values still carry
        Markdown inline markers - a renderer that cannot honour them escapes
        them, and a row that read differently in two outputs would be the one
        kind of drift a provenance block cannot afford.
        """
        data = self.as_dict()
        usage = data["counts"]
        rows = [
            ("Run mode", data["run_mode"]),
            ("Endpoint", f"{data['endpoint']['id']} ({data['endpoint']['location']})"
                         # The operator's own name for the route, where there
                         # is one. The id is a hash of the command by design,
                         # so without this the row says a program answered and
                         # withholds which -- and this row is what a reader
                         # comes back to a week later to find out whether the
                         # run went to the subscription or to the metered API.
                         + (f" -- {data['endpoint']['route']}"
                            if data["endpoint"].get("route") else "")),
            # Per role, and only where the caller recorded it: the row a
            # reader looks for when the question is which role was billed how.
            *((("Route", route_said(data["endpoint"]["billed"])),)
              if data["endpoint"].get("billed") else ()),
            # The published name, not the recorded one. `as_dict` keeps the
            # wire spelling because a report is read by machines too and 151
            # cassettes and every graded run record (`paper/records/`) say `off`; this row is
            # the half a person reads, so it says `verbatim`.
            ("Fidelity", fidelity_name(data["merge_policy"]["fidelity"])),
            # Unconditional, unlike `field_order` and `profile` below, which
            # are printed only when they are off their defaults. Those two say
            # how a response was read; this one says which questions were
            # asked, and a report that names the fidelity level and not the
            # depth describes half the run. A reader has to be able to tell a
            # clean `full` report from a clean `coverage` one without knowing
            # which flags the other run was given.
            ("Verification depth", data["merge_policy"]["verify_depth"]),
            ("Title policy", data["merge_policy"]["title_policy"]),
            ("Base document", _base(data["merge_policy"])),
            *(
                (f"Model ({role})", model_said(model, role, data["ledger"]))
                for role, model in data["models"].items()
            ),
            (
                "Structured output",
                f"{data['structured_output']['mode']} ({data['structured_output']['how']})"
                # Only when it is off the default. `schema` is the contract
                # every report was written under, so printing it would add a
                # line to every report that has ever been produced to say
                # nothing changed; `any` is the exception and has to be visible.
                + ("" if data["structured_output"]["field_order"] == DEFAULT_FIELD_ORDER
                   else f", field order {data['structured_output']['field_order']}"),
            ),
            (
                "Decoding",
                f"temperature {data['decoding']['temperature']}, "
                f"seed {data['decoding']['seed']}, thinking "
                + (", ".join(data["decoding"]["thinking"]) or "off")
                # Only off the default, the same rule as `field_order` on the
                # row above. The default profile is the body every report this
                # project has printed was produced by, so naming it would add a
                # phrase to all of them that says nothing changed; any other
                # profile changed which fields went out and has to be visible
                # beside the values it changed.
                + (f", profile {data['decoding']['profile']}"
                   if data["decoding"].get("profile") else "")
                # Requested and observed, side by side, whenever they differ.
                # Some models reason whatever the request says (deepseek-r1:70b
                # accepts the field that turns it off and reasons anyway), and
                # a provenance block that printed only the request would be
                # describing a run that did not happen.
                + (f" requested; {', '.join(data['decoding']['reasoned_anyway'])} "
                   f"reasoned anyway"
                   if data["decoding"].get("reasoned_anyway") else "")
                # The effort level, per role, and only where there is one.
                # An earlier change put it in the JSON and not in the rendered block, so the
                # reader most likely to need it -- the one holding a printed
                # report and asking why two runs disagree -- could not see it
                # at all. Spelled out per role rather than folded into "all
                # three at low", because the reader would then have to know
                # which way round the shorthand went.
                + (", effort " + ", ".join(
                    f"{role}={level}"
                    for role, level in data["decoding"]["effort"].items())
                   if data["decoding"].get("effort") else "")
                # A model with one level rather than a scale:
                # named beside `effort` and not folded into it, because the
                # label is not a level and a reader scanning for "effort
                # role=level" pairs must not mistake one for the other.
                + ((", " if data["decoding"].get("effort") else ", effort ")
                   + ", ".join(f"{role} {label}" for role, label in
                              data["decoding"]["effort_single_level"].items())
                   if data["decoding"].get("effort_single_level") else "")
                # Asked for and not deliverable, beside what was: the same
                # shape `reasoned_anyway` takes one clause up, and the only
                # place an operator learns their level went nowhere.
                + (f"; {', '.join(data['decoding']['effort_ignored'])} asked "
                   f"for a level this backend cannot carry"
                   if data["decoding"].get("effort_ignored") else "")
                # The requester's choice, beside the level it became.
                + ("; " + ", ".join(
                    f"{role}={level}"
                    for role, level in data["decoding"]["effort_requested"].items())
                   + " chosen by the requester"
                   if data["decoding"].get("effort_requested") else ""),
            ),
            # Only where a window was stated, and unconditional would be wrong
            # for the reason `Model loads` below is conditional: every figure
            # in the recorded corpus was produced by a run that measured its
            # window, and an always-present row would add a line to all of
            # their provenance blocks about a mechanism that did not exist when
            # they were measured. What it must never do is stay silent about a
            # stated one -- the preflight guard reads as a measurement
            # everywhere else in this report, and here it is not one.
            *([("Context window", _stated_window(data["window"]))]
              if _stated_window(data["window"]) else []),
            ("LLossless commit", data["claimcheck_commit"]),
            (
                "Calls",
                f"{usage['calls']} live, {usage['cache_hits']} cached, "
                f"{usage['replayed']} replayed",
            ),
            ("Tokens", data["tokens_described"]),
            ("Cost", _cost_sentence(data["cost"])),
            ("Schema repairs", str(usage["schema_repairs"])),
            # Only when it happened. Every recorded figure in this project was
            # produced by a run that found its endpoint warm, so an
            # unconditional row would rewrite the provenance block of every
            # replay in the corpus to say `0` about a mechanism that did not
            # exist when they were measured.
            *([("Model loads", str(usage["model_loads"]))]
              if usage.get("model_loads") else []),
            # Only where the run was granted something, and unconditional
            # would be wrong for `Model loads`' reason: every figure in the
            # recorded corpus was produced by a run that could reach nothing,
            # and an always-present row would add a line to all of their
            # provenance blocks about a mechanism that did not exist when they
            # were measured. Present, it is the disclosure the automatic grant
            # was made conditional on -- the operator's terms were that it be
            # obvious rather than hidden.
            #
            # Two facts on one row, in this order: what was permitted, then
            # what the turn counter saw. The permission is the load-bearing
            # half -- it is what separates a run that did not look from one
            # that could not -- and it is the half no counter carries.
            *([("Retrieval",
                f"{', '.join(data['retrieval']['permitted'])} permitted; "
                f"{data['retrieval']['described']}")]
              if data["retrieval"]["permitted"] else []),
            # Present for every command backend at every level, unlike the row
            # above: `Retrieval` is silent below `sourced` because nothing was
            # granted there, and that silence used to be the whole story a
            # `high` report told about the isolation. `_isolation_sentence`
            # groups roles that share one state, which is every role
            # today.
            *([("Isolation", _isolation_sentence(data["isolation"]))]
              if data.get("isolation") else []),
            ("Errors", str(usage["errors"])),
            ("Duration", f"{data['duration_seconds']}s"),
            ("Generated", data["generated_at"]),
        ]

        for path, digest in data["prompts"].items():
            rows.append(("Prompt", f"`{_relative(path)}` `{digest[:12]}`"))
        return rows

    def notes(self) -> list[str]:
        """The blockquotes under the table: what left the machine, and what failed.

        Same reasoning as `rows`. Both are conditions on the run rather than
        decoration, so both are said in every output the run produces.
        """
        data = self.as_dict()
        usage = data["counts"]
        notes = []
        if self.hosted and self.settings.command:
            # A different sentence, because the old one was false here. It
            # named `LLOSSLESS_BASE_URL` as the destination, and a command
            # backend contacts no URL at all -- so a reader following that
            # sentence would have gone and looked at an address this run
            # ignored. `hosted` is true for a command backend not because
            # something is known to have left, but because nothing here can
            # establish that it did not, and the note has to say which of
            # the two it is or it is worse than no note.
            named = data["endpoint"].get("route")
            notes.append(
                f"**Document content was handed to a program on this machine"
                + (f" (`{named}`)" if named else "")
                + f".** What that program did with it is outside anything this "
                f"tool can see: there is no address to classify, and the "
                f"network containment this suite runs under is per-process, so "
                f"a child that opened a socket opened it unobserved. Treat the "
                f"documents as having left unless you wrote the program."
            )
        elif self.hosted:
            notes.append(
                f"**Document content left this machine.** It was sent to the "
                f"endpoint in `LLOSSLESS_BASE_URL` (id `{data['endpoint']['id']}`), "
                f"which is not a local address. Run against a local endpoint if "
                f"that is not acceptable for the documents involved."
            )
        # The disclosure the automatic grant is conditional on. Same
        # class as the two notes above and stated in the same place: a granted
        # web tool means the model may put text from these documents into a
        # query or a fetch, which is a second way content leaves, and the
        # operator's terms for the grant being automatic were that it be
        # obvious rather than hidden.
        #
        # Two sentences kept apart, as everywhere else this is said: what the
        # model was permitted, and what this tool did. The second never
        # changes.
        permitted = data["retrieval"]["permitted"]
        if permitted:
            notes.append(
                f"**The model was permitted to reach the network** "
                f"({', '.join(permitted)}), so a query or a fetch it made may "
                f"have carried text from these documents to a third party. "
                f"{data['retrieval']['described'].capitalize()}, counted in "
                f"turns rather than in fetches. LLossless itself made no "
                f"network request of any kind and resolved none of the sources "
                f"the merge names."
            )
        # The interesting case, in the block that renders on every report
        # rather than only on one that declared an addition. A run at the level
        # that expects retrieval and retrieved nothing has produced citations
        # that are recollections, and it is indistinguishable from a run that
        # retrieved unless something says so out loud.
        #
        # `retrieval` rather than `state`: `state` reads the calls
        # that reported, and a run with one silent call is not a run shown to
        # have retrieved nothing.
        sourced = config.canonical_fidelity(self.settings.fidelity) == config.SOURCED
        achieved = data["retrieval"]["tool_use"]["retrieval"]
        if sourced and achieved == NOT_RETRIEVED:
            notes.append(
                f"**This run was made at fidelity {config.SOURCED}, which asks "
                f"the model to retrieve rather than recall, and it retrieved "
                f"nothing.** Every source the merge names is therefore a "
                f"recollection, exactly as it would be one level down."
            )
        # The third state, which was never said at all. An operator ran
        # `sourced` for hours through routes that reported no turn count, and
        # this block told them what was permitted and nothing about what was
        # achieved. `config.retrieval_refusal` now refuses a command that
        # cannot report; this is what a run says when a command that should
        # have reported did not.
        if sourced and achieved == UNMEASURED:
            notes.append(
                f"**This run was made at fidelity {config.SOURCED} and whether "
                f"the model retrieved anything is unmeasured**: "
                f"{data['retrieval']['described']}. That is not the same as "
                f"nothing retrieved, and it is not a sign that anything was. "
                f"Treat every source the merge names as unchecked."
            )
        # `errors` counts calls; the coverage table counts steps. They agreed
        # until Pass C, because a failed call failed its step with it. A
        # salvaged call is the case where they do not, so it is subtracted out
        # here and said separately -- a note claiming a unit produced nothing,
        # printed above a table crediting it with verdicts, is two true
        # sentences a reader can only read as a contradiction.
        lost = usage["errors"] - usage.get("salvaged", 0)
        if lost:
            notes.append(
                f"**{lost} unit(s) of work errored.** The model could not "
                f"be made to answer in a usable form. This run is inconclusive: "
                f"coverage below is computed over the units that did answer, and "
                f"the exit code is 2 regardless of what they said."
            )
        if usage.get("salvaged"):
            notes.append(
                f"**{usage['salvaged']} call(s) came back unusable and were graded "
                f"in part.** The model was asked again and did not fix it, so the "
                f"records that could not be read were dropped by name and the rest "
                f"of the answer was kept. They are listed under `Not graded`; the "
                f"claims they were about have no verdict and the exit code is 2."
            )
        # Every role names its mechanism, not only the ones that fell back.
        # A block that listed the exceptions and stayed silent about the rest
        # let a reader assume the rest were guarded, which for `decompose` and
        # `verify` was false for the whole life of the tool.
        preflighted = sorted(role for role, mechanism in data["window"].items()
                             if mechanism == "preflight")
        if preflighted:
            notes.append(
                f"**Preflight window guard ran for {', '.join(preflighted)}.** "
                f"The rendered prompt was measured against the served context "
                f"window before the call was sent."
            )
        # Said separately from the preflight note above, and never folded into
        # it. Both roles were guarded before the call went out, so both are
        # preflights in the mechanical sense -- and what they were guarded
        # *against* is the whole difference, because one figure was confirmed
        # by a probe against the endpoint and the other is a sentence somebody
        # typed. A note that reported them as one thing would be the report
        # blurring the two claims this mechanism exists to keep apart.
        declared = sorted(role for role, mechanism in data["window"].items()
                          if mechanism.startswith(STATED))
        if declared:
            figure = data["window"][declared[0]][len(STATED):]
            notes.append(
                f"**The context window was stated, not measured, for "
                f"{', '.join(declared)}.** {figure.capitalize()}. The rendered "
                f"prompt was checked against that figure before each call, so "
                f"a prompt too large for it was refused rather than sent -- but "
                f"nothing here confirmed the figure itself, and if the endpoint "
                f"serves less than was declared, an overrun is trimmed from the "
                f"front and answered exactly as it would be with no guard at "
                f"all. This is what a vendor endpoint with no /api/ps route can "
                f"be given; it is weaker than what a local endpoint is measured "
                f"against."
            )
        for role, mechanism in data["window"].items():
            if mechanism.startswith("post-hoc"):
                reason = mechanism.split(": ", 1)[1] if ": " in mechanism else mechanism
                notes.append(
                    f"**{role}'s context window is unmeasurable on this endpoint.** "
                    f"{reason} No preflight guard ran; each call was instead checked "
                    f"afterwards against its own completion-token ceiling. That "
                    f"is a weaker guarantee than a local endpoint gets: "
                    f"it catches a truncated answer, not an overrun prompt."
                )
        return notes

    def as_markdown(self) -> str:
        lines = ["## Provenance", "", "| | |", "|---|---|"]
        lines += [f"| {label} | {value} |" for label, value in self.rows()]
        for note in self.notes():
            lines += ["", f"> {note}"]
        return "\n".join(lines) + "\n"


# Imported rather than copied: the prefix a mechanism string starts with is
# written in `window.mechanism` and read here, and a second spelling of it
# would leave this block silently reporting nothing the first time the string
# moved -- a report that omits a caveat looks exactly like a run that did not
# need one.
STATED = window_module.STATED


def _stated_window(mechanisms: dict) -> str:
    """The Provenance row for a window the operator declared, or `""`.

    Empty for every other run, which is what keeps the row off the corpus's
    reports. Built from `Usage.window_mechanism` rather than from `Settings`
    so the row describes what the guard actually used: a replay carries no
    mechanism for any role, and a row read off the setting would announce a
    window over a run that was constrained by nothing.

    One row for all the roles that share the figure -- there is one stated
    window per run by construction -- and it names them, because a run where
    only `merge` reached the endpoint guarded only `merge`.
    """
    roles = sorted(role for role, mechanism in mechanisms.items()
                   if mechanism.startswith(STATED))
    if not roles:
        return ""
    figures = {mechanism[len(STATED):] for role, mechanism in mechanisms.items()
               if role in roles}
    # One figure is the only case the code can produce; several would mean two
    # settings in one run, and the row says so rather than picking the first.
    return f"{'; '.join(sorted(figures))} ({', '.join(roles)})"


def _isolation_sentence(isolation: dict) -> str:
    """The Isolation row: safe mode and the `--tools` grant, grouped by role.

    `_stated_window`'s shape: one clause per distinct state rather than one
    row per role, because the roles share one command by construction today
    and three identical clauses would read as three different answers. A
    role's `tools` is `None` when its executed argv carries no `--tools` at
    all -- unrestricted -- and `[]` for `--tools ""`; the two are worded apart
    because they are opposite facts, the reason `as_dict` keeps them apart too.
    """
    groups: dict[tuple[bool, tuple[str, ...] | None], list[str]] = {}
    for role in sorted(isolation):
        info = isolation[role]
        tools = info["tools"]
        key = (bool(info["safe_mode"]), None if tools is None else tuple(tools))
        groups.setdefault(key, []).append(role)
    clauses = []
    for (safe_mode, tools), roles in groups.items():
        state = "safe mode" if safe_mode else "not isolated"
        if tools is None:
            tool_state = ""
        elif tools:
            tool_state = f", tools {', '.join(tools)}"
        else:
            tool_state = ", no tools"
        clauses.append(f"{', '.join(roles)}: {state}{tool_state}")
    return "; ".join(clauses)


def _base(policy: dict) -> str:
    """The base row, including when there is no base.

    A `verify` run made no merge, so it has no base — and the row says that
    rather than being dropped, because a missing row reads as an omission and
    this one is a fact about the run. `defaulted` is spelled out for the same
    reason: it is the case where nobody chose.
    """
    if not policy["base"]:
        return "none — this run made no merge"
    # Backticks only when the name cannot close them. This row is the caller's
    # filename inside markup this module wrote, and both renderers mark up what
    # they are given: a name carrying a backtick or a `**` pair ended up as
    # `<code>` or `<strong>` structure in the HTML page, or closed a span early.
    # Quoting is a presentation choice and the name is the fact, so the
    # quoting is what gives way. The record itself is unaffected -- this
    # function builds a display row, and `base` is stored verbatim beside it.
    name = str(policy["base"])
    quoted = name if "`" in name or "**" in name else f"`{name}`"
    return f"{quoted} ({policy['base_chosen']})"


def _relative(path: str) -> str:
    try:
        return str(Path(path).relative_to(ROOT))
    except ValueError:
        return path


def model_said(alias: str, role: str, ledger: list[dict]) -> str:
    """`opus -> claude-opus-5-5`, from the role's own ledger rows.

    The alias alone when no row of the role names a model: every HTTP run and
    every replay of a recording made before command envelopes carried one,
    whose Model row must not move. Otherwise the id that wrote each answer,
    distinct and in call order, then every other id the CLI named -- it runs a
    small model for its own steps, and dropping that one would make the row
    tidier than the envelope. A call whose envelope named none, beside calls
    that did, is counted rather than folded into the others, and so is a call
    whose envelope could not say which id wrote the answer.
    """
    rows = [row for row in ledger if row.get("role") == role]
    named = [row["answered_by"] for row in rows if isinstance(row.get("answered_by"), dict)]
    if not named:
        return alias
    authors = list(dict.fromkeys(block["output"] for block in named if block.get("output")))
    others = [name for name in dict.fromkeys(
        name for block in named for name in block.get("models") or [])
        if name not in authors]
    said = f"{alias} -> {', '.join(authors) if authors else 'no single id'}"
    notes = []
    if others:
        notes.append(f"the answer's output tokens; also named {', '.join(others)}")
    undecided = sum(1 for block in named if not block.get("output"))
    if undecided and authors:
        notes.append(f"{undecided} of {len(rows)} call(s) named no single author")
    silent = len(rows) - len(named)
    if silent:
        notes.append(f"{silent} of {len(rows)} call(s) named no model")
    return said + (f" ({'; '.join(notes)})" if notes else "")
