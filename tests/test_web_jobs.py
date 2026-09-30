#!/usr/bin/env python3
"""Offline checks for the web job layer and its progress events. No network, no model.

`src/llossless/web/jobs.py` and `src/llossless/web/events.py` are what stand
between a browser and a merge that takes between 23 and 4,559 seconds. Three
of the things they promise are the kind that look true from the outside while
being false:

**that a job which dies reaches `failed`**, rather than sitting at `running`
until the process restarts -- a progress bar turning forever is
indistinguishable, to the person watching it, from a merge that is still going;

**that the event stream replays exactly the tail a browser missed**, because
the whole reconnect design rests on it and an off-by-one in either direction is
invisible on a run that never dropped its connection;

**that the documents are deleted.** They are confidential files on somebody
else's server, and a retention sweep that quietly forgot to run looks exactly
like one that ran and found nothing to do.

Every merge here runs against `tests/fake_endpoint.py`, the same loopback
double `tests/test_cli.py` uses, and the scripted replies are imported from
that module rather than copied: two fixtures for one endpoint is how the second
one stops matching the prompts. The scheduling checks use a stub runner instead,
because the pool's concurrency is a property of the pool and testing it through
a real merge would make a thread-scheduling assertion depend on how fast a fake
HTTP server answers.

Every detector below has a must-fire case beside its must-not-fire one. The
ones that matter most are the pairs: the thread count is asserted against a
console that really does start a thread, the retention window is asserted a
second before it passes as well as a second after, and the concurrency limit is
asserted against a pool of two that really is observed running two.

Run with `python3 tests/test_web_jobs.py`, or collect with pytest.
"""

from __future__ import annotations

import contextlib
import io
import json
import os
import stat
import sys
import tempfile
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

# Installed before anything else runs. Every merge below reaches a real
# loopback socket, so this is the module's claim that the only socket it opens
# is the one it bound itself; `tests/test_socket_guard.py` asserts every test
# module states it in exactly this shape.
socket_guard.install()

from llossless import cli, config, merge  # noqa: E402
from llossless.console import Console  # noqa: E402
from llossless.web import catalogue, credentials, diagnose, events, jobs  # noqa: E402
from llossless.web.events import EventLog, WebConsole  # noqa: E402

from fake_endpoint import FakeEndpoint  # noqa: E402

# The scripted endpoint and the two sources, imported rather than restated.
# `Script` picks its reply by which prompt arrived, so the same script answers
# both a job-layer run and a `cli.one_merge` run without either depending on
# the other's call order -- which is what makes the equivalence check below
# possible at all.
from test_cli import CLEAN, MERGED, SOURCE_A, SOURCE_B, Script  # noqa: E402

failures: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


# --------------------------------------------------------------------------
# scaffolding
# --------------------------------------------------------------------------

# Long enough that a loaded machine running the whole suite does not fail a
# check about state transitions, short enough that a genuine hang is reported
# as one rather than as a suite that never returns.
PATIENCE = 60.0


def wait_for(predicate, *, timeout: float = PATIENCE) -> bool:
    """Poll until `predicate` holds. False on timeout, never an exception.

    Returned rather than asserted so the caller can put the failure in its own
    words: "the job never started" and "the job never finished" are different
    diagnoses and a shared assertion would give them one message.
    """
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(0.01)
    return predicate()


def a_request(**overrides) -> jobs.MergeRequest:
    """Two sources and a base. The model is named so no local file decides it.

    `config.from_env` merges `models.local.json` under the environment, and a
    developer's own file is untracked -- so without both model variables a run
    here would carry whatever model that machine happens to prefer into the
    provenance block of a test that never called one.
    """
    settings = {"LLOSSLESS_MODEL": "test-model", "LLOSSLESS_MERGE_MODEL": "test-model"}
    settings.update(overrides)
    return jobs.MergeRequest(
        documents={"notes-a.md": SOURCE_A, "notes-b.md": SOURCE_B},
        base="notes-a.md",
        overrides=settings,
    )


@contextlib.contextmanager
def live_store(script=None, **kwargs):
    """A started `JobStore` wired to a scripted endpoint. Yields (store, endpoint).

    `--structured prompt` for the reason `tests/test_cli.py` pins it: the
    capability probe is the client's business and is tested there, and leaving
    it on would put a negotiation this module does not own inside every
    assertion it makes.

    `script` defaults to `CLEAN`, which is what every caller but one gets. The
    one is the status scan, which submits a document with a line of its own
    and needs a merge that carries it.
    """
    with FakeEndpoint(script or Script(**CLEAN)) as base_url, \
            tempfile.TemporaryDirectory() as raw:
        environ = {"LLOSSLESS_BASE_URL": base_url, "LLOSSLESS_STRUCTURED": "prompt"}
        store = jobs.JobStore(Path(raw) / "work", environ=environ, **kwargs)
        try:
            yield store.start(), base_url
        finally:
            store.close()


@contextlib.contextmanager
def stub_store(runner, **kwargs):
    """A started `JobStore` with no endpoint behind it, for the scheduling checks."""
    with tempfile.TemporaryDirectory() as raw:
        store = jobs.JobStore(Path(raw) / "work", environ={}, runner=runner, **kwargs)
        try:
            yield store.start()
        finally:
            store.close()


class Clock:
    """A clock that only moves when a test moves it.

    Retention is a question about elapsed time, and the two honest ways to ask
    it are to wait an hour or to state the time. `JobStore` takes the clock as
    an argument so that this one can be handed in; a sweep tested by sleeping
    would either be slow or be testing a window short enough to be untypical.
    """

    def __init__(self, now: float = 1_000_000.0) -> None:
        self.now = now

    def __call__(self) -> float:
        return self.now

    def advance(self, seconds: float) -> None:
        self.now += seconds


class Gate:
    """A runner that blocks until released, and records how many ran at once.

    `peak` is what the concurrency checks read. It is a high-water mark rather
    than a sample, so a pool that briefly overlapped and then serialised is
    still caught -- a limit that holds most of the time is not a limit.
    """

    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.release = threading.Event()
        self.entered = 0
        self.active = 0
        self.peak = 0

    def __call__(self, job, workspace) -> None:
        with self.lock:
            self.entered += 1
            self.active += 1
            self.peak = max(self.peak, self.active)
        self.release.wait(timeout=PATIENCE)
        with self.lock:
            self.active -= 1


def quiet_runner(job, workspace) -> None:
    """A job that succeeds and leaves a file behind, without calling a model.

    The file matters: retention is measured by whether the directory is gone,
    and an empty directory disappearing proves less than one with something in
    it disappearing.
    """
    jobs.write_private(workspace.directory / jobs.MERGED_MD, "merged text\n")
    job.exit_code = 0


def exploding_runner(job, workspace) -> None:
    raise RuntimeError("the endpoint went away")


def exiting_runner(job, workspace) -> None:
    """Dies by `SystemExit`, which is not an `Exception` and not caught by one."""
    raise SystemExit(3)


class FakeTerminal:
    """A stream that claims to be a terminal, so `Console` really does animate.

    Only used by the must-fire half of the thread check. `Console.__init__`
    asks `is_tty(self.stream)` and `waiting()` starts its ticker only when the
    answer was yes, so without a stream that says yes there is no way to show
    that the thread assertion is capable of failing.
    """

    encoding = "utf-8"

    def __init__(self) -> None:
        self.written: list[str] = []

    def isatty(self) -> bool:
        return True

    def write(self, text: str) -> None:
        self.written.append(text)

    def flush(self) -> None:
        pass


# --------------------------------------------------------------------------
# a job, end to end
# --------------------------------------------------------------------------


def test_a_job_runs_end_to_end_and_reaches_done() -> None:
    """The must-not-fire half of every failure check below.

    `exit_code == 0` is asserted rather than merely `state == done`: a job that
    crashed before reaching the model would also leave a state, and this is
    what says the merge actually happened.
    """
    with live_store() as (store, _):
        job = store.submit(a_request())
        check(job.state == jobs.QUEUED, f"a submitted job starts queued, not {job.state}")
        finished = wait_for(lambda: job.terminal)
        check(finished, f"the job never finished; it is {job.state}")
        check(job.state == jobs.DONE, f"the job must reach done; it is {job.state} "
                                      f"with error {job.error!r}")
        check(job.error is None, f"a job that succeeded carries no error; got {job.error!r}")
        check(job.exit_code == 0, f"the scripted merge is clean and must exit 0; "
                                  f"got {job.exit_code}")
        check(job.started_at is not None and job.finished_at is not None,
              "a finished job must carry both timestamps")
        check(job.run is not None and job.report is not None,
              "a finished job must carry both the Run and the report dict")


def test_a_finished_job_leaves_three_readable_artefacts_and_no_others() -> None:
    """The three files the web server will serve, owner-readable only, and the two a restart reads.

    `sources.json` and `events.jsonl` are written from the moment a job
    is accepted, so a restarted server can resume a queued run and say what an
    interrupted one did. They are named here so that a sixth file appearing in
    a job directory is a failure rather than a surprise.

    The permission bits are checked because the work directory holds the
    operator's documents and everything quoted out of them, and a self-hosted
    box is frequently a shared one. `write_private` opens with the mode rather
    than writing and then chmod-ing, so there is no window in which the file
    exists at whatever the process umask allows.
    """
    with live_store() as (store, _):
        job = store.submit(a_request())
        if not wait_for(lambda: job.terminal):
            check(False, "the job never finished")
            return
        present = sorted(path.name for path in job.directory.iterdir())
        check(present == sorted([jobs.REPORT_JSON, jobs.MERGED_MD, jobs.REPORT_HTML,
                                 jobs.SOURCES_JSON, jobs.EVENTS_JSONL]),
              f"a finished job must leave exactly the three named artefacts and "
              f"the two restart files; got {present}")
        for name in present:
            mode = stat.S_IMODE((job.directory / name).stat().st_mode)
            check(mode == jobs.FILE_MODE,
                  f"{name} is mode {mode:o}, not {jobs.FILE_MODE:o}; an uploaded "
                  f"document's merge must not be world-readable")
        check(stat.S_IMODE(job.directory.stat().st_mode) == jobs.DIR_MODE,
              "the job directory must be owner-only")
        on_disk = json.loads((job.directory / jobs.REPORT_JSON).read_text(encoding="utf-8"))
        # Through a round trip, not against the dict itself. `report.as_dict`
        # emits tuples for several fields -- `rationale_names` is one -- and
        # JSON has only one sequence type, so a straight comparison would fail
        # on `() != []` and say nothing about whether the right payload was
        # written. What is being asserted is that the file is the serialisation
        # of the payload the job holds, which is what the server will serve from memory.
        check(on_disk == json.loads(json.dumps(job.report)),
              "report.json on disk must be the same payload the job holds")
        check(on_disk.get("merged_written_to") == jobs.MERGED_MD,
              f"the report must name the merged file as a bare name, not a path; "
              f"got {on_disk.get('merged_written_to')!r}")


def test_the_job_layer_and_cli_one_merge_agree_on_the_report() -> None:
    """The anti-drift guard for `run_merge` writing the sequence out.

    `jobs.run_merge` does not wrap `cli.one_merge` -- it cannot, because it
    needs the `Run` back on a `FATAL` fault and needs the client's
    `notify` channel routed to the event log. The cost of not wrapping is that
    the two can drift, and this is what makes drift a failure rather than a
    discovery: one merge through each, against the same endpoint and the same
    settings, and the reports must agree.

    Three keys are dropped before the comparison and each is dropped for a
    reason rather than for convenience: `generated_at` is a wall clock,
    `duration_seconds` is a stopwatch, and `merged_written_to` is deliberately
    different -- the CLI writes wherever `-o` pointed and the web path writes a
    bare name into a directory it owns. A fourth, `latency_ms`, is each ledger
    row's own stopwatch, taken off after asserting both sides carry it:
    against a local fake two calls can take the same milliseconds, so leaving
    it in would pass by chance and fail by chance. The split of that time
    goes with it, and so do the run's own time accounting blocks.
    """
    volatile = ("generated_at", "duration_seconds", "answering_seconds",
                "excluded", "discarded_calls", "unruled")
    stopwatches = ("latency_ms", "attempts", "answer_ms", "failed_ms",
                   "waited_ms", "ttfb_ms")
    with live_store() as (store, base_url):
        job = store.submit(a_request())
        if not wait_for(lambda: job.terminal) or job.report is None:
            check(False, f"the job never produced a report; it is {job.state}")
            return

        documents = {"notes-a.md": SOURCE_A, "notes-b.md": SOURCE_B}
        prepared, loaded, _ = cli.prepare_merge(dict(documents))
        with tempfile.TemporaryDirectory() as raw:
            workspace = jobs.Workspace(
                directory=Path(raw), cache_dir=Path(raw),
                environ={"LLOSSLESS_BASE_URL": base_url,
                         "LLOSSLESS_STRUCTURED": "prompt"})
            settings = jobs.web_settings(a_request(), workspace)
            paths = dict(zip(merge.source_names(len(documents)), documents))
            _, expected = cli.one_merge(settings, paths, prepared, loaded,
                                        "source_a.md", Console())

        mine, theirs = dict(job.report), dict(expected)
        # Another field only the web side ever carries, popped the same way
        # and for the same reason `merged_written_to` is: `cli_equivalent` is
        # `web/cli_render.render`'s block, and `cli.one_merge` has no request
        # to render one from -- there is no page behind it asking "how would I
        # have typed this". Asserted present and shaped rather than merely
        # absent from the comparison, so a future change that stops setting it
        # is caught here instead of by a browser finding an empty block.
        mine_cli_equivalent = mine.pop("cli_equivalent", None)
        check(isinstance(mine_cli_equivalent, dict)
              and isinstance(mine_cli_equivalent.get("command"), str)
              and mine_cli_equivalent["command"].startswith("llossless merge "),
              f"a finished web run must carry a rendered CLI-equivalent "
              f"command; got {mine_cli_equivalent!r}")
        check("cli_equivalent" not in theirs,
              "cli.one_merge has no request to render a CLI equivalent from")
        # One field the two paths differ on by design, and it is taken out of
        # the job's side only after asserting it is there: the web layer
        # chose a route for each role from a row somebody picked and records
        # how each was billed; the command line was handed an endpoint and
        # chose nothing, so it records nothing. Anything else in `endpoint`
        # still has to agree.
        endpoint = dict(mine["provenance"].get("endpoint") or {})
        billed = endpoint.pop("billed", None)
        check(billed == {role: "selfhosted" for role in cli.ROLES},
              f"a web run on a typed model at a loopback endpoint must record "
              f"every role as billed locally; got {billed!r}")
        check("billed" not in (theirs["provenance"].get("endpoint") or {}),
              "the command line recorded a route it never chose")
        mine["provenance"] = dict(mine["provenance"], endpoint=endpoint)
        for payload in (mine, theirs):
            payload.pop("merged_written_to", None)
            payload["provenance"] = {key: value
                                     for key, value in payload["provenance"].items()
                                     if key not in volatile}
            rows = payload["provenance"].get("ledger") or []
            check(rows and all(isinstance(row.get("latency_ms"), int) for row in rows),
                  f"both runs are live, so every ledger row carries its call's "
                  f"time: {[row.get('latency_ms') for row in rows]}")
            payload["provenance"]["ledger"] = [
                {k: v for k, v in row.items() if k not in stopwatches} for row in rows]
        differing = sorted(key for key in set(mine) | set(theirs)
                           if mine.get(key) != theirs.get(key))
        check(not differing,
              f"the job layer and cli.one_merge disagree on {', '.join(differing)}; "
              f"one of the two orchestrations has drifted from the other")


# --------------------------------------------------------------------------
# failure
# --------------------------------------------------------------------------


def test_a_merge_that_raises_reaches_failed_and_records_why() -> None:
    """Must fire. The companion to the end-to-end check above.

    The state is the assertion that matters: a worker that lost its exception
    would leave the job at `running`, which a browser polls forever without
    ever being told anything went wrong.
    """
    with stub_store(exploding_runner) as store:
        job = store.submit(a_request())
        check(wait_for(lambda: job.terminal), f"the job never left {job.state}")
        check(job.state == jobs.FAILED, f"a runner that raised must fail the job; "
                                        f"it is {job.state}")
        check(job.error is not None and "RuntimeError" in job.error
              and "the endpoint went away" in job.error,
              f"the job must record the class and the message; got {job.error!r}")
        check(job.finished_at is not None,
              "a failed job must still carry a finishing timestamp")
        terminal = [event for event in job.events.since(0)
                    if event.kind == "state" and event.fields.get("terminal")]
        check(len(terminal) == 1 and terminal[0].fields.get("state") == jobs.FAILED,
              "a failed job must emit exactly one terminal state event saying so")


def test_a_worker_killed_by_a_system_exit_still_records_the_job_as_failed() -> None:
    """Must fire, and for the shape `except Exception` would have missed.

    `SystemExit` is not an `Exception`. A worker that took one from somewhere
    deep in a library would die between `running` and any record of why, and
    the job would read as in-progress for the life of the process -- which is
    the exact failure mode this file's docstring opens with.
    """
    with stub_store(exiting_runner) as store:
        job = store.submit(a_request())
        check(wait_for(lambda: job.terminal),
              f"a job whose worker exited must not stay at {job.state}")
        check(job.state == jobs.FAILED, f"the job must be failed; it is {job.state}")
        check(job.error is not None and "SystemExit" in job.error,
              f"the job must name what killed it; got {job.error!r}")


def test_a_refused_request_never_becomes_a_job() -> None:
    """Refusals happen before an id exists, so nothing is left half-submitted."""
    with stub_store(quiet_runner) as store:
        def refused(request, what: str) -> None:
            try:
                store.submit(request)
                check(False, f"{what} must be refused")
            except jobs.JobRefused:
                pass

        refused(jobs.MergeRequest(documents={"only.md": SOURCE_A}),
                "a single document")
        refused(jobs.MergeRequest(documents={"a.md": SOURCE_A, "b.md": "   \n"}),
                "a document with no text in it")
        refused(jobs.MergeRequest(documents={"a.md": SOURCE_A, "b.md": SOURCE_B},
                                  base="nowhere.md"),
                "a base that is not one of the documents")
        check(store.jobs() == [], "a refused request must leave nothing in the index")

        # Must not fire: the same store accepts the request that is well formed.
        job = store.submit(jobs.MergeRequest(
            documents={"a.md": SOURCE_A, "b.md": SOURCE_B}, base="b.md"))
        check(len(store.jobs()) == 1, "a well-formed request must be accepted")
        check(wait_for(lambda: job.terminal), "the accepted job never finished")


def test_the_base_label_is_translated_by_position_not_by_name() -> None:
    """`prepare_merge` renames by position, so the base has to be found the same way.

    The document keys here are in an order the alphabet disagrees with, which
    is what makes this more than a tautology: a lookup that sorted the labels,
    or one that matched on the label's own text against the canonical names,
    would pick `source_a.md` and be wrong.
    """
    request = jobs.MergeRequest(documents={"zulu.md": SOURCE_A, "alpha.md": SOURCE_B},
                                base="alpha.md")
    check(jobs.canonical_base(request) == "source_b.md",
          f"the second document submitted is source_b.md whatever it is called; "
          f"got {jobs.canonical_base(request)!r}")
    check(jobs.canonical_base(jobs.MergeRequest(
        documents={"a.md": SOURCE_A, "b.md": SOURCE_B})) is None,
        "no base given is None, not a guess")


# --------------------------------------------------------------------------
# events and replay
# --------------------------------------------------------------------------


def test_events_arrive_in_order_with_ids_that_never_repeat() -> None:
    with live_store() as (store, _):
        job = store.submit(a_request())
        if not wait_for(lambda: job.terminal):
            check(False, "the job never finished")
            return
        log = job.events.since(0)
        check(len(log) > 10, f"a complete merge emits more than ten events; got {len(log)}")
        check([event.id for event in log] == list(range(1, len(log) + 1)),
              "event ids must be 1..n with no gap and no repeat")
        check(all(a.at <= b.at for a, b in zip(log, log[1:])),
              "events must be ordered by the time they happened")
        check(log[0].kind == "state" and log[0].fields.get("state") == jobs.QUEUED,
              "the first event is the job being queued")
        check(log[-1].kind == "state" and log[-1].fields.get("terminal") is True,
              "the last event is terminal, so a stream knows when to stop")
        kinds = {event.kind for event in log}
        check(kinds <= events.KINDS, f"every event kind must be registered; "
                                     f"{sorted(kinds - events.KINDS)} is not")
        names = [event.message for event in log if event.kind == "step"]
        check("merge" in names and "verify (reverse)" in names,
              f"the stream must carry the pipeline's own step names; got {names}")
        check(job.events.closed, "a finished job's log must be closed")


def test_replay_from_a_mid_stream_id_returns_exactly_the_missing_tail() -> None:
    """The property a reconnecting browser depends on, tested as a property.

    Not "events exist after an id" -- an implementation using `>=` would pass
    that and hand the page a duplicate of the last event it already rendered,
    and one using the list index rather than the id would pass it and skip an
    event after any `forget`. The assertion is set equality against the tail,
    at every id the log ever issued.
    """
    log = EventLog()
    made = [log.emit("step", f"unit {index}") for index in range(8)]
    ids = [event.id for event in made]

    check(ids == list(range(1, 9)), f"ids must start at 1 and increment; got {ids}")
    check([event.id for event in log.since(0)] == ids,
          "since(0) is the whole log, which is what a first connection asks for")
    for cut in range(len(ids) + 1):
        after = ids[cut - 1] if cut else 0
        tail = [event.id for event in log.since(after)]
        check(tail == ids[cut:],
              f"replay after id {after} must return exactly {ids[cut:]}; got {tail}")
    check(log.since(ids[-1]) == (), "a reader that is current must be sent nothing")
    check(log.since(ids[-1] + 500) == (),
          "an id past the end returns nothing rather than raising")


def test_forgetting_a_log_keeps_its_ids_moving_forward() -> None:
    """Must fire against the obvious wrong implementation.

    Retention empties the log. If the id counter were an index into the list,
    or were reset with it, the tombstone would be issued an id a browser has
    already seen -- and that browser, asking for everything after the id it
    holds, would be told there was nothing and would wait for a run that had
    been deleted.
    """
    log = EventLog()
    for index in range(5):
        log.emit("step", f"unit {index}")
    last = log.since(0)[-1].id

    tombstone = log.forget("forgotten: the retention window has passed")
    check(tombstone.id == last + 1,
          f"the tombstone must take the next id, not reuse {tombstone.id}")
    tail = log.since(last)
    check([event.id for event in tail] == [last + 1],
          f"a browser holding id {last} must be handed the tombstone and nothing "
          f"else; got {[event.id for event in tail]}")
    check(len(log.since(0)) == 1,
          "forgetting leaves the tombstone and no stored event beside it")
    check(tail[0].fields.get("state") == "forgotten" and tail[0].fields.get("terminal"),
          "the tombstone must say the run is over and why")


def test_a_waiter_is_woken_by_an_event_and_by_the_log_closing() -> None:
    """`wait` is what keeps the event stream from polling. Both wake-ups are checked.

    Without the second, an endpoint looping on `wait` over a job that finished
    between two iterations would block for the whole keep-alive interval on
    every tick, for as long as the browser stayed connected.
    """
    log = EventLog()
    threading.Timer(0.05, lambda: log.emit("step", "late")).start()
    started = time.monotonic()
    woken = log.wait(0, timeout=PATIENCE)
    check(len(woken) == 1 and woken[0].message == "late",
          f"wait must return the event that woke it; got {woken}")
    check(time.monotonic() - started < PATIENCE / 2,
          "wait must be woken by the emit rather than by its own timeout")
    log.close()
    check(log.wait(woken[0].id, timeout=PATIENCE) == (),
          "wait on a closed log must return at once rather than block")


# --------------------------------------------------------------------------
# the console
# --------------------------------------------------------------------------

# `Console`'s eight public methods, listed so the check below can be about
# whether each one is overridden rather than about whether somebody remembered
# to add it here. `waiting` is excluded by name and on purpose: it is a context
# manager, it is deliberately not overridden, and inheriting it is what makes
# the thread check meaningful.
CONSOLE_METHODS = ("step", "done", "failed", "skipped", "detail", "warn",
                   "notice", "banner")


def test_every_public_console_method_is_overridden_and_emits_its_own_kind() -> None:
    public = {name for name, value in vars(Console).items()
              if not name.startswith("_") and callable(value)}
    missing = public - set(CONSOLE_METHODS) - {"waiting"}
    check(not missing,
          f"Console has grown {sorted(missing)}; WebConsole must override it or "
          f"the text goes to a stream nobody reads")
    not_overridden = [name for name in CONSOLE_METHODS if name not in vars(WebConsole)]
    check(not not_overridden,
          f"WebConsole does not override {not_overridden}")

    for name in CONSOLE_METHODS:
        console = WebConsole()
        if name == "banner":
            console.banner("merge", "a-model", "http://127.0.0.1:1/v1",
                           window="8192", fidelity="high",
                           depth=config.DEFAULT_VERIFY_DEPTH)
        else:
            getattr(console, name)("a message")
        emitted = console.log.since(0)
        check(len(emitted) == 1 and emitted[0].kind == name,
              f"Console.{name} must emit exactly one event of kind {name!r}; "
              f"got {[event.kind for event in emitted]}")
        if name == "banner":
            # Every argument, kept apart and none of them dropped on the way
            # out. `WebConsole.banner` takes six and emits them as fields
            # because the page has six places to put them; a field the method
            # accepts and never emits is a field the page renders as nothing
            # and nobody can tell from a server that was never told.
            sent = emitted[0].as_dict().get("fields") or {}
            missing = sorted({"command", "model", "endpoint", "window",
                              "fidelity", "depth"} - set(sent))
            check(not missing,
                  f"the banner event dropped {missing}; the method was given "
                  f"all six and the browser gets {sorted(sent)}")


def test_the_chosen_verbosity_actually_emits_the_gated_kinds() -> None:
    """`detail` is gated at level 2 and would be dropped at anything lower.

    The must-fire half is a console built at the CLI's own default: at
    verbosity 0 the same three calls produce nothing, which is what the browser
    would have shown if the number had been left alone.
    """
    console = WebConsole()
    console.step("a step")
    console.done("a step", seconds=1.5)
    console.detail("a detail")
    kinds = [event.kind for event in console.log.since(0)]
    check(kinds == ["step", "done", "detail"],
          f"at verbosity {events.VERBOSITY} all three must be emitted; got {kinds}")
    timed = [event for event in console.log.since(0) if event.kind == "done"]
    check(timed and timed[0].seconds == 1.5,
          "a done event must carry the seconds the console was told, unformatted")

    quiet = WebConsole()
    quiet.verbosity = 0
    quiet.step("a step")
    quiet.detail("a detail")
    check(len(quiet.log) == 0,
          "the level gates must be real: at verbosity 0 nothing is emitted, which "
          "is why the default here is not the CLI's")


def test_the_web_console_starts_no_threads() -> None:
    """A spinner thread inside a web worker is a bug, and `enabled=False` is why not.

    The must-fire half is the whole check. A console built the way the CLI
    builds one for a terminal really does start a ticker inside `waiting()`, so
    this shows the thread count is capable of moving -- without it, the
    assertion above would pass on a `waiting()` that had been deleted.
    """
    console = WebConsole()
    check(console.animate is False,
          "a web console must not animate; a ticker writes to a stream nobody reads")
    before = threading.active_count()
    with console.waiting("something slow") as elapsed:
        check(threading.active_count() == before,
              f"WebConsole.waiting started a thread: {threading.active_count()} "
              f"threads, was {before}")
        check(elapsed() >= 0, "waiting must still yield an elapsed-time closure")
    check(threading.active_count() == before,
          "the thread count must be unchanged after the block too")

    animated = Console(FakeTerminal(), verbosity=1, enabled=True)
    check(animated.animate is True, "the must-fire console must actually animate")
    before = threading.active_count()
    with animated.waiting("something slow"):
        started = threading.active_count()
    check(started > before,
          "the must-fire console did not start a thread, so the check above "
          "cannot fail and proves nothing")


def test_no_console_method_prints_instead_of_emitting() -> None:
    """The detector for a `Console` method that grew an override-shaped hole.

    Anything an unoverridden method prints lands in the buffer `WebConsole`
    hands the base class. After a complete merge it has to be empty; the
    must-fire case calls the base implementation directly to show the buffer
    catches text when there is text to catch.
    """
    with live_store() as (store, _):
        job = store.submit(a_request())
        if not wait_for(lambda: job.terminal):
            check(False, "the job never finished")
            return
    console = WebConsole()
    console.step("routed to the log")
    check(console.written == "",
          f"a WebConsole must print nothing; it wrote {console.written!r}")
    Console.warn(console, "not routed anywhere")
    check("not routed anywhere" in console.written,
          "the buffer did not catch a base-class write, so the assertion above "
          "would pass over a method nobody overrode")


# --------------------------------------------------------------------------
# SSE
# --------------------------------------------------------------------------


def test_an_sse_frame_carries_the_id_the_kind_and_one_line_of_data() -> None:
    log = EventLog()
    event = log.emit("done", "merge", seconds=2.5)
    rendered = events.frame(event)
    check(rendered.endswith("\n\n"),
          "a frame must end with the blank line that dispatches it")
    lines = rendered.rstrip("\n").split("\n")
    check(lines[0] == f"id: {event.id}",
          f"the id must come first, so a truncated frame never commits one; got {lines[0]!r}")
    check(lines[1] == "event: done", f"the kind is the event name; got {lines[1]!r}")
    check(len(lines) == 3 and lines[2].startswith("data: "),
          f"a frame is three lines and a blank; got {lines}")
    payload = json.loads(lines[2][len("data: "):])
    check(payload["message"] == "merge" and payload["seconds"] == 2.5,
          f"the payload must carry the structured fields; got {payload}")

    with_retry = events.frame(event, retry_ms=events.DEFAULT_RETRY_MS)
    check(with_retry.startswith(f"retry: {events.DEFAULT_RETRY_MS}\n"),
          "a stated reconnect delay rides ahead of the id")


def test_a_newline_in_a_message_cannot_break_out_of_the_frame() -> None:
    """Must fire against the naive encoding: `data: {message}` with the text in it.

    SSE delimits fields by newline, so a message carrying one would end the
    frame early and the remainder would arrive as a field the browser drops.
    A step detail is `f"{type(exc).__name__}: {exc}"` and an exception message
    is the model's to shape, so this is not a hypothetical input.
    """
    log = EventLog()
    event = log.emit(
        "failed", "merge: SchemaFailure: line one\nline two\r\nline three")
    rendered = events.frame(event)
    lines = rendered.rstrip("\n").split("\n")
    check(len(lines) == 3,
          f"a message with newlines in it must still render three lines; got {lines}")
    payload = json.loads(lines[2][len("data: "):])
    check(payload["message"].count("\n") == 2,
          "the newlines must survive inside the JSON rather than being stripped")


def test_last_event_id_is_read_leniently_and_never_refuses() -> None:
    """0 means "send everything", and anything unreadable means 0.

    Refusing a malformed header would turn a browser quirk into a page that
    never loads; the cost of being wrong this way is a few hundred events the
    page already has.
    """
    for value, expected in ((None, 0), ("", 0), ("  12 ", 12), ("0", 0),
                            ("-4", 0), ("nonsense", 0), ("3.5", 0)):
        got = events.parse_last_event_id(value)
        check(got == expected,
              f"Last-Event-ID {value!r} must read as {expected}; got {got}")


def test_frames_replay_the_tail_a_browser_asks_for() -> None:
    """The two halves joined: a header in, the frames it was missing out."""
    log = EventLog()
    for index in range(6):
        log.emit("step", f"unit {index}")
    resumed = events.frames(log.since(events.parse_last_event_id("4")))
    check(resumed.count("\n\n") == 2,
          f"resuming from id 4 of 6 must send two frames; got {resumed!r}")
    check("id: 5" in resumed and "id: 6" in resumed and "id: 4" not in resumed,
          f"the tail must be exactly 5 and 6; got {resumed!r}")


# --------------------------------------------------------------------------
# retention
# --------------------------------------------------------------------------


def test_the_default_retention_deletes() -> None:
    """The posture, asserted as a fact about the default rather than as a comment."""
    check(jobs.DEFAULT_RETENTION_SECONDS is not None,
          "the default retention window must delete; None is the opt-out and "
          "has to be asked for")
    clock = Clock()
    with stub_store(quiet_runner, clock=clock) as store:
        check(store.retention_seconds == jobs.DEFAULT_RETENTION_SECONDS,
              "a store built with no retention argument must take the deleting default")
        job = store.submit(a_request())
        if not wait_for(lambda: job.terminal):
            check(False, "the job never finished")
            return
        clock.advance(jobs.DEFAULT_RETENTION_SECONDS + 1)
        store.sweep()
        check(job.forgotten, "a job past the default window must be forgotten")


def test_the_default_window_covers_a_run_finished_at_the_end_of_one_day() -> None:
    """The scenario the default is sized for, as an arithmetic claim about it.

    The default was raised from an hour, and an hour is a defensible number for a
    different scenario -- the one the constant used to name, an operator who
    started a merge and went to lunch. What it failed is the ordinary one: a
    run finished at the end of a working day, opened the next morning. The
    operator lost a finished report to exactly that.

    The check is the *worst* case inside that sentence rather than a
    comfortable one. A run does not have to finish at six in the evening to be
    read the next morning: it can finish at half past nine in the morning, sit
    in a tab through a day of meetings, and be wanted at ten the following day.
    That is 24 hours and a half, which is why a 24-hour window is not the
    answer here -- it expires at the hour it started.

    Deliberately not asserted against the number itself. A check that said
    `== 172800` would pass whatever the window was sized for and would have to
    be edited by whoever changed it, which is the shape of check that gets
    edited rather than read.
    """
    worst_case = 24.5 * 3600
    check(jobs.DEFAULT_RETENTION_SECONDS is not None
          and jobs.DEFAULT_RETENTION_SECONDS >= worst_case,
          f"the default window is {jobs.DEFAULT_RETENTION_SECONDS}s, which does "
          f"not cover a run finished at the start of one working day and read "
          f"the next morning ({worst_case}s)")
    # And still a deletion. The other half of the trade: a longer window is
    # still a window, and `None` is still the thing that has to be asked for.
    check(jobs.DEFAULT_RETENTION_SECONDS is not None,
          "the default window must still delete")
    # The weekend is deliberately outside it. If this ever stops holding, the
    # default has been stretched to cover Friday evening to Monday morning,
    # which is a different posture and needs its own decision rather than a
    # quiet edit to a constant.
    check(jobs.DEFAULT_RETENTION_SECONDS < 60 * 3600,
          f"the default window is {jobs.DEFAULT_RETENTION_SECONDS}s, which "
          f"covers a whole weekend; that is a posture change, not a size")


def test_a_run_finished_yesterday_evening_is_there_this_morning() -> None:
    """The same claim, driven through the reaper instead of read off a constant.

    A store on the real default, a finished run, and a clock moved to the next
    morning. Then past the window, so the must-not-fire half is beside the
    must-fire half on one job rather than in two tests that could both be
    passing for the wrong reason.
    """
    clock = Clock()
    with stub_store(quiet_runner, clock=clock) as store:
        check(store.retention_seconds == jobs.DEFAULT_RETENTION_SECONDS,
              "a store built with no retention argument must take the default")
        job = store.submit(a_request())
        if not wait_for(lambda: job.terminal):
            check(False, "the job never finished")
            return
        # Finished at half past nine; opened at ten the following day.
        clock.advance(24.5 * 3600)
        check(store.sweep() == [],
              "a run finished at the start of one working day must still be "
              "there the next morning")
        check(not job.forgotten and job.directory.is_dir(),
              "the documents of a run read the next morning must still exist")
        clock.advance(jobs.DEFAULT_RETENTION_SECONDS)
        check([one.id for one in store.sweep()] == [job.id],
              "a run well past the window must still be forgotten; a default "
              "that never deletes is not a retention window")


def test_the_hour_this_replaced_loses_the_run_by_morning() -> None:
    """The must-fire half, and it is a measurement rather than a restatement.

    Not the comparison above with a different number substituted: a store on
    the old sixty-minute window, a finished run, the same clock moved to the
    same next morning, and the real `sweep`. What comes out is the operator's
    report reproduced -- the report is gone before they come back to it -- and
    it is what makes the check above discriminating rather than decorative.
    """
    clock = Clock()
    with stub_store(quiet_runner, retention_seconds=3600.0, clock=clock) as store:
        job = store.submit(a_request())
        if not wait_for(lambda: job.terminal):
            check(False, "the job never finished")
            return
        clock.advance(24.5 * 3600)
        check([one.id for one in store.sweep()] == [job.id],
              "an hour-long window must lose a run by the next morning; if it "
              "does not, the scenario check above is passing on a window that "
              "was never at risk")


def test_the_variable_sets_the_window_and_a_bad_one_is_refused() -> None:
    """`LLOSSLESS_RETENTION`, in its own right, including the refusal.

    The refusal is the half worth stating. An unreadable value that fell back
    to the default would keep documents for *longer* than the operator asked,
    silently, and the one number this setting must never guess in the
    permissive direction is this one.
    """
    check(jobs.retention_from({}) == jobs.DEFAULT_RETENTION_SECONDS,
          "an unset variable must leave the default alone")
    check(jobs.retention_from({jobs.RETENTION_ENV: "  "})
          == jobs.DEFAULT_RETENTION_SECONDS,
          "a blank variable is an unset one")
    check(jobs.retention_from({jobs.RETENTION_ENV: "900"}) == 900.0,
          "the variable must set the window")
    check(jobs.retention_from({jobs.RETENTION_ENV: "0"}) is None,
          "`0` must mean keep forever, the same as `--retention 0`")
    check(jobs.retention_from({jobs.RETENTION_ENV: "-5"}) is None,
          "anything at or below zero must mean keep forever")
    refused = False
    try:
        jobs.retention_from({jobs.RETENTION_ENV: "48h"})
    except ValueError as bad:
        refused = jobs.RETENTION_ENV in str(bad)
    check(refused,
          "a value that is not a number must be refused by name, not ignored")


def test_the_old_variable_names_do_not_reach_a_job() -> None:
    """The server's `CLAIMCHECK_*` variables are not read as `LLOSSLESS_*`.

    The code used to fold them into a job's environment and the store's copy; the
    operator's fresh-start ruling removed that. The old names are unrelated
    variables now: no new name is filled from one, and `retention_from`
    ignores the old spelling. Must fire: `LLOSSLESS_RETENTION` is read.
    """
    base = {"CLAIMCHECK_BASE_URL": "http://127.0.0.1:9/v1",
            "CLAIMCHECK_MODEL": "server-model",
            "CLAIMCHECK_TITLE_POLICY": "keep-base",
            "CLAIMCHECK_RETENTION": "900"}
    with contextlib.redirect_stderr(io.StringIO()) as err, \
            tempfile.TemporaryDirectory() as raw:
        environ = jobs.resolved_environ(a_request(), base)
        stored = jobs.JobStore(Path(raw), environ=base).environ
        ignored = jobs.retention_from({"CLAIMCHECK_RETENTION": "900"})
        fired = jobs.retention_from({"LLOSSLESS_RETENTION": "900"})
    for name, copy in (("a job's environment", environ), ("the store's copy", stored)):
        check(copy.get("LLOSSLESS_TITLE_POLICY") != "keep-base"
              and copy.get("LLOSSLESS_BASE_URL") != "http://127.0.0.1:9/v1",
              f"{name} must not fill a new name from an old one")
    check(environ.get("LLOSSLESS_MODEL") == "test-model",
          f"the request's model is the job's: {environ.get('LLOSSLESS_MODEL')}")
    check(fired == 900.0, f"must fire: LLOSSLESS_RETENTION is read: {fired}")
    check(ignored == jobs.DEFAULT_RETENTION_SECONDS,
          f"CLAIMCHECK_RETENTION must not be read: {ignored}")
    check("CLAIMCHECK" not in err.getvalue(),
          f"the old names must not be mentioned: {err.getvalue()!r}")


def test_the_warning_threshold_scales_with_the_window() -> None:
    """A quarter of the window, capped at four hours, and off when retention is.

    Derived rather than fixed because this server runs at ten minutes in a
    check and at two days by default, and a fixed three hours is either the
    whole of the first window or invisible in the second.
    """
    check(jobs.retention_warning_seconds(None) is None,
          "there is nothing to warn about when nothing is deleted")
    check(jobs.retention_warning_seconds(600) == 150.0,
          f"a ten-minute window must warn a quarter of the way out; got "
          f"{jobs.retention_warning_seconds(600)}")
    check(jobs.retention_warning_seconds(jobs.DEFAULT_RETENTION_SECONDS)
          == 4 * 3600.0,
          f"the default window must warn four hours out -- the top of the "
          f"range asked for -- not twelve; got "
          f"{jobs.retention_warning_seconds(jobs.DEFAULT_RETENTION_SECONDS)}")
    for window in (60.0, 600.0, 7200.0, 86400.0, jobs.DEFAULT_RETENTION_SECONDS):
        warn = jobs.retention_warning_seconds(window)
        check(warn is not None and 0 < warn <= window,
              f"a {window}s window must warn inside itself; got {warn}")


def test_the_remaining_seconds_are_the_servers_own_arithmetic() -> None:
    """What the page counts down from, and the three states with nothing to count.

    A number of seconds and never a timestamp: the browser subtracts elapsed
    time on its own machine from this, so no comparison between two clocks
    exists anywhere on the path.
    """
    gate = Gate()
    clock = Clock()
    with stub_store(gate, retention_seconds=100.0, clock=clock) as store:
        job = store.submit(a_request())
        check(wait_for(lambda: job.state == jobs.RUNNING), "the job never started")
        check(store.forgets_in(job) is None,
              "a running job has no window yet; it is measured from the finish")
        gate.release.set()
        if not wait_for(lambda: job.terminal):
            check(False, "the job never finished")
            return
        check(store.forgets_in(job) == 100.0,
              f"a job that has just finished has the whole window left; got "
              f"{store.forgets_in(job)}")
        clock.advance(60)
        check(store.forgets_in(job) == 40.0,
              f"the count must fall with the clock; got {store.forgets_in(job)}")
        clock.advance(1000)
        check(store.forgets_in(job) == 0.0,
              f"a job past its window counts zero, never a negative; got "
              f"{store.forgets_in(job)}")
        store.sweep()
        check(job.forgotten and store.forgets_in(job) is None,
              "a forgotten job has nothing left to count down to")
    clock = Clock()
    with stub_store(quiet_runner, retention_seconds=None, clock=clock) as store:
        job = store.submit(a_request())
        if not wait_for(lambda: job.terminal):
            check(False, "the job never finished")
            return
        check(store.forgets_in(job) is None,
              "retention off means there is no countdown, not a large one")


def test_retention_forgets_a_job_a_second_after_the_window_and_not_a_second_before() -> None:
    """Must-not-fire and must-fire, on the same job, one second apart.

    A sweep that forgot everything it looked at would pass a check that only
    looked after the window; a sweep that forgot nothing would pass a check
    that only looked before it.
    """
    clock = Clock()
    with stub_store(quiet_runner, retention_seconds=60.0, clock=clock) as store:
        job = store.submit(a_request())
        if not wait_for(lambda: job.terminal):
            check(False, "the job never finished")
            return
        directory = job.directory
        check(directory.is_dir() and any(directory.iterdir()),
              "the job must have left something on disk for retention to delete")

        clock.advance(59)
        check(store.sweep() == [], "a job inside the window must not be forgotten")
        check(not job.forgotten and directory.is_dir(),
              "the documents must still be there a second before the window passes")
        check(job.request.documents != {},
              "the submitted documents must still be there inside the window")

        clock.advance(2)
        forgotten = store.sweep()
        check([one.id for one in forgotten] == [job.id],
              f"the job must be forgotten a second after the window; got {forgotten}")
        check(not directory.exists(),
              "the work directory and everything in it must be gone")
        check(job.request.documents == {},
              "the submitted documents must be gone from memory too")
        check(job.request.base is None,
              "the base label is a filename the operator chose and must go too")
        check(job.run is None and job.report is None,
              "the merged text and the report quote the documents and must go too")
        check(len(job.events) == 1 and job.events.since(0)[0].fields.get("state")
              == "forgotten",
              "the event log must be replaced by a tombstone")
        check(job.state == jobs.DONE and job.exit_code == 0 and job.forgotten_at is not None,
              "the tombstone keeps the outcome, which carries no document text")
        check(store.get(job.id) is job,
              "a forgotten job stays findable, so a bookmarked id is answered "
              "rather than looking like a typo")


def test_retention_never_touches_a_job_that_has_not_finished() -> None:
    """A window measured from submission would delete a document mid-merge."""
    gate = Gate()
    clock = Clock()
    with stub_store(gate, retention_seconds=1.0, clock=clock) as store:
        job = store.submit(a_request())
        check(wait_for(lambda: job.state == jobs.RUNNING), "the job never started")
        clock.advance(10_000)
        check(store.sweep() == [], "a running job must never be forgotten")
        check(job.request.documents != {},
              "a running merge is reading those documents")
        gate.release.set()
        check(wait_for(lambda: job.terminal), "the job never finished")


def test_retention_none_keeps_everything() -> None:
    """The opt-out, and the must-not-fire half of every check above."""
    clock = Clock()
    with stub_store(quiet_runner, retention_seconds=None, clock=clock) as store:
        job = store.submit(a_request())
        if not wait_for(lambda: job.terminal):
            check(False, "the job never finished")
            return
        clock.advance(10_000_000)
        check(store.sweep() == [], "retention_seconds=None must forget nothing")
        check(not job.forgotten and job.directory.is_dir(),
              "an operator who asked to keep the documents must still have them")


def test_delete_removes_the_job_from_the_index_entirely() -> None:
    """Stronger than retention: the operator asked for it to be gone."""
    with stub_store(quiet_runner) as store:
        job = store.submit(a_request())
        if not wait_for(lambda: job.terminal):
            check(False, "the job never finished")
            return
        directory = job.directory
        check(store.delete(job.id) is True, "deleting a job that exists returns True")
        check(store.get(job.id) is None, "a deleted job must not be findable")
        check(store.jobs() == [], "a deleted job must be out of the listing")
        check(not directory.exists(), "a deleted job's directory must be gone")
        check(store.delete(job.id) is False,
              "deleting a job twice must say it was not there the second time")


def test_cancel_takes_a_queued_job_and_flags_a_running_one() -> None:
    """A queued job is cancelled outright; a running one is flagged.

    The running half is the one that changed. The flag is set and the state
    stays `running`, because the merge really is until its client looks at the
    flag: this runner never does, so it finishes and the job is `done` -- a
    cancel that arrives after the last call has nothing left to stop, and the
    report is whole. The two live checks below are where the flag stops a
    real merge.
    """
    gate = Gate()
    with stub_store(gate) as store:
        running = store.submit(a_request())
        queued = store.submit(a_request())
        check(wait_for(lambda: running.state == jobs.RUNNING), "the first job never started")

        check(store.cancel(queued.id) is True, "a queued job must be cancellable")
        check(queued.state == jobs.CANCELLED and queued.error == jobs.CANCELLED_QUEUED,
              f"a queued job cancelled lands in cancelled with a reason; it is "
              f"{queued.state} / {queued.error!r}")
        check(store.cancel(running.id) is True, "a running job's cancel must be taken")
        check(running.state == jobs.RUNNING and running.stop.is_set()
              and running.status()["cancel_requested"] is True,
              f"a running job's cancel sets the flag and leaves it running; it is "
              f"{running.state}, flag {running.stop.is_set()}")

        gate.release.set()
        check(wait_for(lambda: running.terminal), "the running job never finished")
        check(running.state == jobs.DONE,
              f"a runner that finished despite the flag is done; it is {running.state}")
        check(store.cancel(running.id) is False, "a finished job cannot be cancelled")
        check(gate.entered == 1,
              f"the cancelled job must never have run; the runner was entered "
              f"{gate.entered} times")


class SlowScript:
    """`Script`, answering each call after `delay` seconds, recording when.

    `inside` is set while a call is being answered, so a test can cancel with a
    call known to be in flight rather than guessing at a sleep.
    """

    def __init__(self, delay: float) -> None:
        self.script = Script(**CLEAN)
        self.delay = delay
        self.arrived: list[float] = []
        self.inside = threading.Event()

    def __call__(self, body: dict, n: int):
        self.arrived.append(time.monotonic())
        self.inside.set()
        time.sleep(self.delay)
        self.inside.clear()
        return self.script(body, n)


def test_cancel_stops_an_http_merge_before_its_next_call() -> None:
    """Against a slow loopback endpoint: cancel during a call.

    Asserted: no call arrives after the cancel (the one in flight is abandoned,
    and no retry follows it), the job ends `cancelled` quickly rather than when
    the endpoint answers, the report of what ran exists and is not clean, and
    `error` counts the calls. Must-fire: the same run with the flag never read
    goes on calling.
    """
    slow = SlowScript(delay=2.0)
    with live_store(slow) as (store, _):
        job = store.submit(a_request())
        check(wait_for(slow.inside.is_set), "the merge never reached the endpoint")
        arrived = len(slow.arrived)
        asked = time.monotonic()
        check(store.cancel(job.id) is True, "a running merge's cancel must be taken")
        check(wait_for(lambda: job.terminal, timeout=10), f"the job never ended; {job.state}")
        took = time.monotonic() - asked
        check(job.state == jobs.CANCELLED,
              f"a cancelled merge lands in cancelled; it is {job.state} ({job.error!r})")
        check(took < slow.delay,
              f"the cancel waited for the endpoint: {took:.2f}s against a {slow.delay}s call")
        time.sleep(slow.delay + 1.5)
        check(len(slow.arrived) == arrived,
              f"{len(slow.arrived) - arrived} call(s) arrived after the cancel")
        check(job.error and "cancelled" in job.error and f"{arrived} model call(s)" in job.error
              and "billed" in job.error,
              f"the error must count the calls and say they are billed: {job.error!r}")
        check(job.report is not None and job.exit_code not in (None, 0),
              f"a cancelled run keeps its report and does not exit clean; exit "
              f"{job.exit_code}")
        steps = (job.report or {}).get("steps") or []
        check(any("Cancelled" in str(step) for step in steps),
              f"the report does not say which unit the cancel stopped: {steps!r}")
        check((job.directory / jobs.REPORT_JSON).is_file(),
              "a cancelled run writes the report of what ran")
        check(job.status()["state"] == jobs.CANCELLED and job.status()["cancel_requested"],
              f"the status poll must read cancelled: {job.status()}")
        check(job.status()["calls_made"] == arrived,
              f"the status poll counts {job.status()['calls_made']} calls, the endpoint {arrived}")
        # Nothing half-written reads as complete, and the headline does not
        # blame the model for a cancel.
        from llossless import report as report_module
        page = (job.directory / jobs.REPORT_HTML).read_text(encoding="utf-8")
        check("Cancelled." in page and "could not be made to answer" not in page,
              "the cancelled run's report does not open by saying it was cancelled")
        check(report_module.verdict_line(job.run).startswith("**Cancelled.**"),
              f"verdict_line: {report_module.verdict_line(job.run)[:80]!r}")
        real_prefix = report_module.CANCELLED_PREFIX
        report_module.CANCELLED_PREFIX = "Nothing matches this:"
        try:
            check(not report_module.verdict_line(job.run).startswith("**Cancelled.**"),
                  "seeded: the cancelled headline does not depend on the step's record")
        finally:
            report_module.CANCELLED_PREFIX = real_prefix

    # Must-fire: a client that never reads the flag keeps calling.
    from llossless import client as client_module
    real = client_module.Client._stop_if_cancelled
    client_module.Client._stop_if_cancelled = lambda self: None
    real_abandon = client_module.Client._abandonable
    client_module.Client._abandonable = lambda self, call: call(time.sleep)
    try:
        slow = SlowScript(delay=0.3)
        with live_store(slow) as (store, _):
            job = store.submit(a_request())
            check(wait_for(slow.inside.is_set), "the seeded merge never reached the endpoint")
            arrived = len(slow.arrived)
            store.cancel(job.id)
            wait_for(lambda: job.terminal)
            check(len(slow.arrived) > arrived,
                  "seeded: a client that ignores the flag made no further call, so "
                  "the no-further-call check above measures nothing")
    finally:
        client_module.Client._stop_if_cancelled = real
        client_module.Client._abandonable = real_abandon


def slow_program(directory: Path, seconds: float, *, ignore_term: bool = False) -> Path:
    """A fake `claude` that records its pid and a child's, then sleeps."""
    program = directory / "claude"
    trap = "trap '' TERM\n" if ignore_term else ""
    program.write_text(
        "#!/bin/sh\n" + trap
        + f"echo $$ >> {directory / 'pids.txt'}\n"
        + f"sleep {seconds} &\n"
        + f"echo $! >> {directory / 'children.txt'}\n"
        + "cat >/dev/null\nwait\necho '{}'\n", encoding="utf-8")
    program.chmod(0o755)
    return program


def alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    # A zombie still answers kill(0); it has exited all the same.
    try:
        state = Path(f"/proc/{pid}/stat").read_text().split(") ")[-1][:1]
    except OSError:
        return False
    return state != "Z"


def test_cancel_stops_a_command_backend_program() -> None:
    """Against a fake slow `claude`: the program and its child are gone.

    Asserted: the job ends `cancelled` within the SIGTERM path's reach, the
    program and the child it started are no longer running, and no second
    program was started.
    """
    with tempfile.TemporaryDirectory() as raw:
        home = Path(raw)
        program = slow_program(home, 60)
        environ = {"LLOSSLESS_COMMAND": f"{program} --print",
                   "LLOSSLESS_PROFILE": "subscription", "LLOSSLESS_WINDOW": "200000",
                   "LLOSSLESS_THINKING": "merge,verify,decompose"}
        store = jobs.JobStore(home / "work", environ=environ).start()
        try:
            job = store.submit(a_request(LLOSSLESS_MODEL="haiku",
                                         LLOSSLESS_MERGE_MODEL="haiku"))
            check(wait_for(lambda: (home / "children.txt").is_file()
                           and (home / "children.txt").read_text().strip() != ""),
                  f"the program never started; the job is {job.state} ({job.error!r})")
            pids = [int(x) for x in (home / "pids.txt").read_text().split()]
            children = [int(x) for x in (home / "children.txt").read_text().split()]
            check(all(alive(pid) for pid in pids + children),
                  "the program was not running when the cancel was asked for")
            check(store.cancel(job.id) is True, "the command run's cancel must be taken")
            check(wait_for(lambda: job.terminal, timeout=15), f"the job never ended; {job.state}")
            check(job.state == jobs.CANCELLED,
                  f"a cancelled command run lands in cancelled; it is {job.state} ({job.error!r})")
            check(wait_for(lambda: not any(alive(pid) for pid in pids + children), timeout=5),
                  f"the program or its child is still running after the cancel: "
                  f"{[pid for pid in pids + children if alive(pid)]}")
            time.sleep(1.0)
            check(len((home / "pids.txt").read_text().split()) == 1,
                  "a second program was started after the cancel")
        finally:
            store.close()


def test_a_program_that_ignores_sigterm_is_killed_after_the_grace() -> None:
    """`backend.run_cancellable`: SIGTERM first, SIGKILL after the grace.

    Must-fire: the same program sent SIGTERM alone is still running half a
    second later, which is what shows the SIGKILL is the step that ended it.
    """
    from llossless import backend, transport
    with tempfile.TemporaryDirectory() as raw:
        home = Path(raw)
        program = slow_program(home, 60, ignore_term=True)
        cancel = threading.Event()
        timer = threading.Timer(0.5, cancel.set)
        timer.start()
        started = time.monotonic()
        try:
            backend.run_cancellable([str(program)], input="x", timeout=30,
                                    cancel=cancel, grace=0.5)
            check(False, "a cancelled program must raise Cancelled")
        except transport.Cancelled:
            pass
        took = time.monotonic() - started
        pids = [int(x) for x in (home / "pids.txt").read_text().split()]
        children = [int(x) for x in (home / "children.txt").read_text().split()]
        check(not any(alive(pid) for pid in pids + children),
              "a program that ignores SIGTERM is still running after the grace")
        check(0.9 < took < 10, f"SIGKILL came after {took:.2f}s, not after the 0.5s grace")

        import signal
        import subprocess
        (home / "pids.txt").unlink()
        (home / "children.txt").unlink()
        process = subprocess.Popen([str(program)], stdin=subprocess.PIPE,
                                   start_new_session=True)
        check(wait_for(lambda: (home / "children.txt").is_file()), "the seeded program never started")
        os.killpg(process.pid, signal.SIGTERM)
        time.sleep(0.5)
        check(alive(process.pid),
              "seeded: the program died of SIGTERM, so the check above never needed a SIGKILL")
        os.killpg(process.pid, signal.SIGKILL)
        process.wait()


# --------------------------------------------------------------------------
# the pool
# --------------------------------------------------------------------------


def test_one_worker_runs_one_job_at_a_time() -> None:
    """The default, and the reason it is the default: the engine is synchronous.

    The second job is checked to be still queued rather than merely not
    running, so a pool that had started it and immediately blocked somewhere
    else would not pass by accident.
    """
    gate = Gate()
    with stub_store(gate, workers=1) as store:
        first = store.submit(a_request())
        second = store.submit(a_request())
        check(wait_for(lambda: gate.entered >= 1), "no job ever started")
        # Long enough that a second worker, if there were one, would have run.
        time.sleep(0.2)
        check(gate.peak == 1, f"two jobs ran at once with the pool at 1; peak {gate.peak}")
        check(second.state == jobs.QUEUED,
              f"the second job must still be queued; it is {second.state}")
        gate.release.set()
        check(wait_for(lambda: first.terminal and second.terminal),
              "the queued job never ran after the first finished")
        check(gate.entered == 2, f"both jobs must eventually run; {gate.entered} did")


def test_the_overlap_detector_can_see_two_jobs_at_once() -> None:
    """Must fire. Without it the check above passes on a pool that runs nothing.

    Same runner, same assertion, a pool of two -- and `peak` has to reach 2. If
    it cannot, then `peak == 1` above is a fact about the stub rather than
    about the limit.
    """
    gate = Gate()
    with stub_store(gate, workers=2) as store:
        store.submit(a_request())
        store.submit(a_request())
        check(wait_for(lambda: gate.peak >= 2),
              f"a pool of two never ran two jobs at once; peak {gate.peak}, "
              f"entered {gate.entered}")
        gate.release.set()


def test_a_store_needs_at_least_one_worker() -> None:
    with tempfile.TemporaryDirectory() as raw:
        try:
            jobs.JobStore(Path(raw), workers=0)
            check(False, "a pool of zero workers must be refused")
        except ValueError:
            pass


# --------------------------------------------------------------------------
# what a web form may and may not decide
# --------------------------------------------------------------------------


def test_a_request_may_choose_a_model_and_may_not_choose_an_address_or_a_key() -> None:
    """The allowlist, both ways.

    `LLOSSLESS_BASE_URL` is the one that matters: a request that could set it
    would aim this server -- holding the operator's key, out of the operator's
    own file -- at a host the submitter picked, and the first call would hand
    the key over.
    """
    allowed = jobs.MergeRequest(documents={"a.md": SOURCE_A, "b.md": SOURCE_B},
                                overrides={"LLOSSLESS_MODEL": "a-model",
                                           "LLOSSLESS_FIDELITY": "mid"})
    check(allowed.overrides["LLOSSLESS_FIDELITY"] == "mid",
          "a request must be able to choose the settings the picker offers")

    for variable in ("LLOSSLESS_BASE_URL", "LLOSSLESS_BASE_URL_MERGE",
                     "LLOSSLESS_API_KEY_ENV", "LLOSSLESS_CA_BUNDLE",
                     "LLOSSLESS_CACHE_DIR", "LLOSSLESS_THINKING",
                     "PATH", "LLOSSLESS_MODEL_BUT_NOT_REALLY"):
        try:
            jobs.MergeRequest(documents={"a.md": SOURCE_A, "b.md": SOURCE_B},
                              overrides={variable: "anything"})
            check(False, f"a request setting {variable} must be refused")
        except jobs.JobRefused as refusal:
            check(variable in str(refusal),
                  f"the refusal must name {variable}; it said {refusal}")

    check(not (jobs.REQUEST_SETTABLE & {"LLOSSLESS_BASE_URL", "LLOSSLESS_API_KEY_ENV"}),
          "the allowlist must never carry an address or a key variable")


def test_the_allowlist_carries_no_address_and_no_key_variable_by_name() -> None:
    """Every address and every key variable this build knows, refused by name.

    The check above tests two spellings. This tests the set, and it derives the
    set rather than listing it: every `LLOSSLESS_BASE_URL_<ROLE>`, every
    `LLOSSLESS_API_KEY_ENV_<ROLE>`, every `LLOSSLESS_PROVIDER_URL_<PROVIDER>`
    and every variable a provider's key is actually read from. A role or a
    provider added next year is covered without anybody remembering to add a
    line here, which is the failure mode a hand-written list has.

    Must not fire: the four settings the picker genuinely offers are on the
    allowlist, asserted in the same breath, so this cannot be satisfied by
    emptying it.
    """
    forbidden = {"LLOSSLESS_BASE_URL", "LLOSSLESS_API_KEY_ENV"}
    for role in config.ROLES:
        forbidden.add(f"LLOSSLESS_BASE_URL_{role.upper()}")
        forbidden.add(f"LLOSSLESS_API_KEY_ENV_{role.upper()}")
    for provider, variable in credentials.PROVIDERS.items():
        forbidden.add(credentials.url_env(provider))
        forbidden.add(credentials.models_env(provider))
        forbidden.add(variable)
    overlap = sorted(jobs.REQUEST_SETTABLE & forbidden)
    check(not overlap,
          f"the allowlist carries {overlap}; a request that could set one of "
          f"those would choose where this server sends its key, or which "
          f"variable the key is read from")
    check({"LLOSSLESS_FIDELITY", "LLOSSLESS_VERIFY_DEPTH",
           "LLOSSLESS_TITLE_POLICY",
           "LLOSSLESS_LOSS_BUDGET", "LLOSSLESS_MODEL"} <= jobs.REQUEST_SETTABLE,
          "the settings the picker offers are no longer on the allowlist, so "
          "the check above is refusing everything")
    # And the derived names really are the shape being guarded against: a
    # typo here would make the set above a set of strings nothing could match.
    check(credentials.url_env("self-hosted") == "LLOSSLESS_PROVIDER_URL_SELF_HOSTED",
          f"url_env no longer produces the variable the job layer reads: "
          f"{credentials.url_env('self-hosted')!r}")


def test_a_request_never_reaches_an_address_or_a_key_variable() -> None:
    """The allowlist from the other end: what actually lands in the environment.

    `resolved_environ` is where a request's overrides and the server's own
    endpoint plan meet, and the plan writes exactly the variables the allowlist
    refuses. The ordering is what makes that safe, so it is asserted on the
    result rather than read off the source: a request that tries to set an
    address is refused, and a request that does not still comes out with the
    address the *server* configured for the model's provider.
    """
    entry = next(model for model in catalogue.models() if model.get("provider"))
    provider, wire = entry["provider"], entry["api_model"]
    base = {"LLOSSLESS_BASE_URL": "http://127.0.0.1:1/v1",
            credentials.url_env(provider): "http://127.0.0.1:2/v1"}

    request = jobs.MergeRequest(documents={"a.md": SOURCE_A, "b.md": SOURCE_B},
                                overrides={"LLOSSLESS_MODEL": wire,
                                           "LLOSSLESS_MERGE_MODEL": wire})
    environ = jobs.resolved_environ(request, base)
    for role in config.ROLES:
        check(environ[f"LLOSSLESS_BASE_URL_{role.upper()}"] == "http://127.0.0.1:2/v1",
              f"{role} was not aimed at the endpoint stored for {provider}")
        check(environ[f"LLOSSLESS_API_KEY_ENV_{role.upper()}"]
              == credentials.PROVIDERS[provider],
              f"{role}'s key variable did not come from the same provider as "
              f"its address")

    # Must fire: a request that tries to write one of those variables itself
    # is refused before the plan runs, so the plan is not a way in for one.
    for variable in (f"LLOSSLESS_BASE_URL_{config.ROLES[0].upper()}",
                     f"LLOSSLESS_API_KEY_ENV_{config.ROLES[0].upper()}",
                     credentials.url_env(provider)):
        try:
            jobs.MergeRequest(documents={"a.md": SOURCE_A, "b.md": SOURCE_B},
                              overrides={variable: "http://127.0.0.1:9/v1"})
            check(False, f"a request setting {variable} was accepted")
        except jobs.JobRefused as refusal:
            check(variable in str(refusal),
                  f"the refusal must name {variable}; it said {refusal}")

    # And a model whose provider has no endpoint is refused rather than sent
    # to whichever endpoint happened to be configured for something else.
    try:
        jobs.resolved_environ(request, {"LLOSSLESS_BASE_URL": "http://127.0.0.1:1/v1"})
        check(False, f"{wire} was routed somewhere with no endpoint stored for "
                     f"{provider}")
    except jobs.JobRefused as refusal:
        check(provider in str(refusal),
              f"the refusal does not name the provider: {refusal}")


def test_a_submitted_depth_survives_as_far_as_the_settings_the_run_uses() -> None:
    """The variable is on the allowlist; this is whether it lands anywhere.

    Being allowlisted and being *read* are two facts, and the web path has
    already been wrong about the second one: once the setting resolved
    correctly and the pipeline was called without it, so a coverage run checked
    for invention, reported that it had, and looked exactly like a working
    `full` run. The allowlist would have passed that day.

    Both depths, because the default is the trap: a setting that never arrives
    resolves to `full`, and a check that only ever submits `full` is a check
    that cannot tell an arriving setting from an ignored one.
    """
    for depth in config.VERIFY_DEPTHS:
        request = jobs.MergeRequest(
            documents={"a.md": SOURCE_A, "b.md": SOURCE_B},
            overrides={"LLOSSLESS_VERIFY_DEPTH": depth})
        environ = jobs.resolved_environ(request, {})
        check(environ.get("LLOSSLESS_VERIFY_DEPTH") == depth,
              f"the depth {depth!r} did not reach the environment a run "
              f"resolves against: {environ.get('LLOSSLESS_VERIFY_DEPTH')!r}")
        settings = config.from_env(environ)
        check(settings.verify_depth == depth,
              f"{depth!r} resolved to Settings.verify_depth="
              f"{settings.verify_depth!r}")

    # Must fire, at the layer under the API's own 400: a depth this build does
    # not have is refused rather than resolving to the default. The API refuses
    # it earlier and with a better message (`bad_verify_depth`); this is the
    # floor under that, for anything reaching the job layer another way.
    try:
        config.from_env({"LLOSSLESS_VERIFY_DEPTH": "shallow"})
        check(False, "an unknown depth resolved instead of being refused, so a "
                     "typo would run at the default and report the default")
    except config.ConfigError as refusal:
        check("shallow" in str(refusal),
              f"the refusal must name what was asked for: {refusal}")


def test_a_request_may_name_an_endpoint_but_never_an_address() -> None:
    """A typed model goes where the request says, and a request cannot say a URL.

    `endpoint` is a provider name looked up in an allowlist. The must-fire half
    is a name that is not one; the must-not-fire half is a name that is, which
    has to route a model the catalogue has never heard of to that provider's
    stored endpoint.
    """
    provider = sorted(credentials.PROVIDERS)[0]
    base = {"LLOSSLESS_BASE_URL": "http://127.0.0.1:1/v1",
            credentials.url_env(provider): "http://127.0.0.1:3/v1"}
    # The window is stated because the first provider is a vendor, and a
    # model the catalogue does not know is refused there without one.
    named = jobs.MergeRequest(documents={"a.md": SOURCE_A, "b.md": SOURCE_B},
                              endpoint=provider,
                              overrides={"LLOSSLESS_MODEL": "qwen3:8b",
                                         "LLOSSLESS_MERGE_MODEL": "qwen3:8b",
                                         "LLOSSLESS_WINDOW": "40960"})
    environ = jobs.resolved_environ(named, base)
    check(environ["LLOSSLESS_BASE_URL_MERGE"] == "http://127.0.0.1:3/v1",
          "a request naming one of the operator's endpoints was not routed there")

    for attempt in ("http://evil.example/v1", "../anthropic", "ANTHROPIC"):
        try:
            jobs.MergeRequest(documents={"a.md": SOURCE_A, "b.md": SOURCE_B},
                              endpoint=attempt)
            check(False, f"endpoint={attempt!r} was accepted; it is looked up in "
                         f"an allowlist and is never an address")
        except credentials.UnknownProvider:
            pass

    # Must not fire: with no endpoint named, a model the catalogue does not
    # know still goes to the server's own endpoint, which is what a typed
    # model id has always done.
    plain = jobs.MergeRequest(documents={"a.md": SOURCE_A, "b.md": SOURCE_B},
                              overrides={"LLOSSLESS_MODEL": "qwen3:8b",
                                         "LLOSSLESS_MERGE_MODEL": "qwen3:8b"})
    left = jobs.resolved_environ(plain, base)
    check("LLOSSLESS_BASE_URL_MERGE" not in left,
          "a request that named no endpoint was aimed somewhere anyway")


def test_a_discovered_model_goes_to_the_endpoint_that_listed_it() -> None:
    """The defect a browser found and no file-level check saw. Must fire.

    A model discovered by probing an endpoint has no catalogue row, so nothing
    said which provider served it -- and it went to whichever endpoint the
    server was started with, which is the exact failure this milestone exists
    to remove, reintroduced one layer down. The endpoint that listed a model is
    the endpoint that serves it, and `provider_serving` is how the job layer
    asks.

    Must not fire, twice: a name nothing listed still reaches the server's own
    endpoint, because that is what a hand-typed model id has always done; and
    a catalogue model is still routed by its catalogue row rather than by a
    listing that happens to mention it.
    """
    provider = "self-hosted"
    base = {"LLOSSLESS_BASE_URL": "http://127.0.0.1:1/v1",
            credentials.url_env(provider): "http://127.0.0.1:4/v1",
            credentials.models_env(provider): "qwen3:8b\ngemma3:12b"}
    discovered = jobs.MergeRequest(
        documents={"a.md": SOURCE_A, "b.md": SOURCE_B},
        overrides={"LLOSSLESS_MODEL": "qwen3:8b",
                   "LLOSSLESS_MERGE_MODEL": "qwen3:8b"})
    environ = jobs.resolved_environ(discovered, base)
    for role in config.ROLES:
        check(environ.get(f"LLOSSLESS_BASE_URL_{role.upper()}")
              == "http://127.0.0.1:4/v1",
              f"a discovered model did not reach the endpoint that listed it "
              f"on the {role} role: {environ.get(f'LLOSSLESS_BASE_URL_{role.upper()}')!r}")

    unlisted = jobs.MergeRequest(
        documents={"a.md": SOURCE_A, "b.md": SOURCE_B},
        overrides={"LLOSSLESS_MODEL": "a-model-nobody-listed",
                   "LLOSSLESS_MERGE_MODEL": "a-model-nobody-listed"})
    left = jobs.resolved_environ(unlisted, base)
    check("LLOSSLESS_BASE_URL_MERGE" not in left,
          "a model nothing listed was routed anyway; a typed model id goes to "
          "this server's own endpoint")

    # A catalogue row wins over a listing that names the same model: its
    # provider is a fact about the model, not something an endpoint said.
    entry = next(model for model in catalogue.models()
                 if model.get("provider") and model["provider"] != provider)
    claimed = dict(base)
    claimed[credentials.models_env(provider)] = entry["api_model"]
    claimed[credentials.url_env(entry["provider"])] = "http://127.0.0.1:5/v1"
    routed = jobs.resolved_environ(
        jobs.MergeRequest(documents={"a.md": SOURCE_A, "b.md": SOURCE_B},
                          overrides={"LLOSSLESS_MODEL": entry["api_model"],
                                     "LLOSSLESS_MERGE_MODEL": entry["api_model"]}),
        claimed)
    check(routed["LLOSSLESS_BASE_URL_MERGE"] == "http://127.0.0.1:5/v1",
          f"a catalogue model was routed by a listing rather than by its own "
          f"row: {routed['LLOSSLESS_BASE_URL_MERGE']!r}")


def test_the_route_each_role_is_billed_under_is_recorded() -> None:
    """The provenance names how each role was paid for. Must fire, per shape.

    The page's button names the route before the click; `billed_by_role` is
    what names it after, in the report. It reads the plan's own three sources
    in `endpoint_plan`'s order, so each shape below is one the router already
    distinguishes: a catalogue row's provider, an endpoint's listing, a typed
    name at the address the plan gave it, and a command route's profile.

    The split case is the one this rests on: the merge metered and the checks
    local are two different answers, and a record with one word for the run
    would be true of one role only.
    """
    base = {"LLOSSLESS_BASE_URL": "http://127.0.0.1:1/v1",
            credentials.url_env("anthropic"): "https://api.anthropic.example/v1",
            credentials.url_env("self-hosted"): "http://127.0.0.1:4/v1",
            credentials.models_env("self-hosted"): "local-listed-8b"}
    documents = {"a.md": SOURCE_A, "b.md": SOURCE_B}

    def billed(request, environ=None):
        resolved = jobs.resolved_environ(request, dict(base) if environ is None
                                         else environ)
        return jobs.billed_by_role(request, config.resolve(None, environ=resolved),
                                   resolved)

    split = jobs.MergeRequest(documents=documents, overrides={
        "LLOSSLESS_MERGE_MODEL": "claude-opus-5-5",
        "LLOSSLESS_MODEL": "local-listed-8b"})
    check(billed(split) == {"merge": "metered", "decompose": "selfhosted",
                            "verify": "selfhosted"},
          f"a metered merge with checks on a listed local model must record "
          f"two routes; got {billed(split)!r}")

    typed = {"LLOSSLESS_MERGE_MODEL": "typed-x", "LLOSSLESS_MODEL": "typed-x"}
    check(set(billed(jobs.MergeRequest(documents=documents,
                                       overrides=typed)).values()) == {"selfhosted"},
          "a typed model at the loopback default must record local")
    # Stated, because a vendor-bound typed id is refused without one.
    named = jobs.MergeRequest(documents=documents,
                              overrides=dict(typed, LLOSSLESS_WINDOW="200000"),
                              endpoint="anthropic")
    check(set(billed(named).values()) == {"metered"},
          f"a typed model sent to a public endpoint must record metered; got "
          f"{billed(named)!r}")

    for profile, kind in (("subscription", "subscription"),
                          ("openai-compatible", "command")):
        command = dict(base, LLOSSLESS_COMMAND="/bin/true",
                       LLOSSLESS_PROFILE=profile, LLOSSLESS_WINDOW="200000",
                       LLOSSLESS_MODEL="haiku", LLOSSLESS_MERGE_MODEL="haiku",
                       LLOSSLESS_THINKING="merge,verify,decompose")
        answer = jobs.billed_by_role(jobs.MergeRequest(documents=documents),
                                     config.resolve(None, environ=command), command)
        check(answer == {role: kind for role in cli.ROLES},
              f"a command route with profile {profile} must record every role "
              f"as {kind}; got {answer!r}")

    check(set(jobs.ROUTE_KINDS) == {"metered", "subscription", "command",
                                    "selfhosted", "unknown"},
          f"the route vocabulary moved: {jobs.ROUTE_KINDS}")


def test_the_run_header_names_each_role_when_one_line_cannot() -> None:
    """The banner's Model and Endpoint were the check's, on every run.

    On a metered merge with local checks the header named the local model and
    the server's default address and nothing of the merge; on an all-metered
    run it named the default address, which answered nothing. `banner_roles`
    groups the roles by what the header shows about them, and a second group
    is what makes the single rows untrue.
    """
    base = {"LLOSSLESS_BASE_URL": "http://127.0.0.1:1/v1",
            credentials.url_env("anthropic"): "https://api.anthropic.example/v1",
            credentials.url_env("self-hosted"): "http://127.0.0.1:4/v1",
            credentials.models_env("self-hosted"): "local-listed-8b"}
    documents = {"a.md": SOURCE_A, "b.md": SOURCE_B}

    def header(merge, check_model):
        request = jobs.MergeRequest(documents=documents, overrides={
            "LLOSSLESS_MERGE_MODEL": merge, "LLOSSLESS_MODEL": check_model})
        resolved = jobs.resolved_environ(request, dict(base))
        settings = config.resolve(None, environ=resolved)
        billed = jobs.billed_by_role(request, settings, resolved)
        return settings, jobs.banner_roles(settings, billed)

    # Must fire: two routes. The route words are `billed`'s, one per group.
    settings, roles = header("claude-opus-5-5", "local-listed-8b")
    check(roles == [
        {"roles": ["merge"], "model": "claude-opus-5-5",
         "endpoint": "https://api.anthropic.example", "route": "metered"},
        {"roles": ["decompose", "verify"], "model": "local-listed-8b",
         "endpoint": "http://127.0.0.1:4", "route": "selfhosted"}],
          f"a metered merge with local checks is two groups: {roles!r}")

    # Must fire: one route, two models. The button names one route here, and
    # the header still has two models it cannot put in one row.
    _, roles = header("claude-opus-5-5", "claude-haiku-4-5-20251001")
    check([(g["roles"], g["model"], g["route"]) for g in roles or []] == [
        (["merge"], "claude-opus-5-5", "metered"),
        (["decompose", "verify"], "claude-haiku-4-5-20251001", "metered")],
          f"two metered models are two groups: {roles!r}")

    # Must not fire: one model, wherever it is, is one line -- and that
    # line's endpoint is the one every role used, not the default address.
    for model, address in (("local-listed-8b", "http://127.0.0.1:4"),
                           ("claude-opus-5-5", "https://api.anthropic.example")):
        settings, roles = header(model, model)
        check(roles is None, f"{model} for every role is one line: {roles!r}")
        check(settings.banner_endpoint_for("verify") == address,
              f"the header's Endpoint for {model} must be {address}, where "
              f"the calls go; got {settings.banner_endpoint_for('verify')!r}, "
              f"and the run-wide default is {settings.banner_endpoint!r}")

    # And a command route, which answers every role through one program.
    command = dict(base, LLOSSLESS_COMMAND="/bin/true", LLOSSLESS_WINDOW="200000",
                   LLOSSLESS_MODEL="haiku", LLOSSLESS_MERGE_MODEL="haiku",
                   LLOSSLESS_THINKING="merge,verify,decompose")
    settings = config.resolve(None, environ=command)
    billed = jobs.billed_by_role(jobs.MergeRequest(documents=documents),
                                 settings, command)
    check(jobs.banner_roles(settings, billed) is None,
          "a command route is one line")

    # The event carries the groups as sent, beside the seven fields it had.
    console = WebConsole()
    console.banner("merge", "local-listed-8b", "http://127.0.0.1:4",
                   roles=header("claude-opus-5-5", "local-listed-8b")[1])
    sent = console.log.since(0)[0].as_dict().get("fields") or {}
    check(len(sent.get("roles") or []) == 2,
          f"the banner event must carry the role groups: {sent}")


def test_the_no_such_model_failure_is_said_in_terms_of_the_endpoint() -> None:
    """The operator's own error message, translated. Must fire and must not.

    The engine's sentence is kept whole and a sentence is added: which model
    was asked for, which endpoint answered, and what to change. The endpoint's
    own name for itself is lifted out of the message rather than read off any
    settings, which is what makes it impossible for the translation to
    disclose more than the thing it is explaining.
    """
    raw = ("decompose document 2: WindowUnknown: localhost has no model named "
           "gpt-5.6-terra loaded; loaded: qwen3-8b:latest")
    said = diagnose.explain(raw)
    check(said != raw, "the failure was not translated at all")
    check(raw in said, "the engine's own message was rewritten rather than added to")
    check("localhost" in said.replace(raw, ""),
          "the translation does not name the endpoint that answered")
    check("gpt-5.6-terra" in said.replace(raw, ""),
          "the translation does not name the model that was asked for")
    check("qwen3-8b:latest" in said.replace(raw, ""),
          "the translation drops what the endpoint does serve")

    # The other tail `window.reported` can produce.
    empty = diagnose.explain("WindowUnknown: box-7 has no model named m "
                             "loaded and nothing else either")
    check("box-7" in empty and "no model at all" in empty,
          f"the empty-endpoint tail was not recognised: {empty!r}")

    # Must not fire: anything else is returned untouched, because a translator
    # that guessed would eventually explain a message as something it is not.
    for other in ("TransportError: cannot reach host: timed out",
                  "merge: MergeError: two documents needed",
                  "", "has no model named"):
        check(diagnose.explain(other) == other,
              f"an unrecognised message was rewritten: {other!r} -> "
              f"{diagnose.explain(other)!r}")


def test_the_translated_failure_leaks_neither_a_key_nor_a_path() -> None:
    """It is built from the message it explains and from a template, and nothing else.

    A translation that reached for the run's settings to name something the
    original did not would be able to disclose more than the failure it is
    explaining. Seeded with a key and a home-shaped path in the environment and
    in the message's own prefix: neither may appear in the part this module
    added, and the path that was already in the message must not be duplicated
    into it either.
    """
    secret = "sk-test-" + "z" * 24
    root = os.sep + os.path.join("home", "someone", "srv")
    with contextlib.ExitStack() as stack:
        stack.callback(os.environ.pop, "ANTHROPIC_API_KEY", None)
        os.environ["ANTHROPIC_API_KEY"] = secret
        raw = (f"decompose {root}/a.md: WindowUnknown: localhost has no model "
               f"named m1 loaded; loaded: m2")
        said = diagnose.explain(raw)
        added = said.replace(raw, "")
        check(secret not in added,
              "the translation carries a key out of the environment")
        check(root not in added,
              f"the translation repeats a filesystem path from the message it "
              f"is explaining: {added!r}")
        check("localhost" in added and "m1" in added,
              "the translation stopped naming the endpoint and the model, so "
              "the two checks above are vacuous")


def test_the_web_path_forces_no_cache_and_a_writable_cache_directory() -> None:
    """Both are requirements rather than preferences; see `web_settings`.

    The must-fire half is the unforced resolve directly above the forced one:
    in a checkout `use_cache` defaults to true, so this shows what would have
    been written into a cassette directory had the field been left alone.
    """
    with tempfile.TemporaryDirectory() as raw:
        cache = Path(raw) / "cache"
        cache.mkdir()
        workspace = jobs.Workspace(directory=Path(raw), cache_dir=cache,
                                   environ={"LLOSSLESS_BASE_URL": "http://127.0.0.1:1"})
        request = jobs.MergeRequest(documents={"a.md": SOURCE_A, "b.md": SOURCE_B})

        unforced = config.resolve(None, environ=dict(workspace.environ))
        check(unforced.use_cache is config.IN_CHECKOUT,
              "the unforced default must be whatever the checkout says, or this "
              "check is not measuring the thing being forced")

        settings = jobs.web_settings(request, workspace)
        check(settings.use_cache is False,
              "a server must never write an uploaded document into a response cache")
        check(settings.cache_dir == cache,
              f"the cache directory must be the one this process owns; "
              f"got {settings.cache_dir}")
        check(settings.record_dir is None and settings.replay_dir is None,
              "a server must never record or replay a cassette from user documents")
        check(settings.dry_run is False, "a web run is never a dry run")


def test_the_two_config_guards_stay_on_the_web_path() -> None:
    """`check_base_url` and `check_cleartext_key`, both reached through `web_settings`.

    Neither may be skipped because the values arrived through a web form.
    A `file://` base URL would have `urllib`'s `FileHandler` return a local
    file's bytes to be parsed as a model answer, and the suite's socket guard
    cannot see that one because it opens no socket at all.
    """
    with tempfile.TemporaryDirectory() as raw:
        workspace = jobs.Workspace(directory=Path(raw), cache_dir=Path(raw),
                                   environ={"LLOSSLESS_BASE_URL": "file:///etc/passwd"})
        request = jobs.MergeRequest(documents={"a.md": SOURCE_A, "b.md": SOURCE_B})
        try:
            jobs.web_settings(request, workspace)
            check(False, "a file:// base URL must be refused on the web path too")
        except config.ConfigError as refusal:
            check("http" in str(refusal), f"the refusal must say what is allowed; "
                                          f"it said {refusal}")

        # The cleartext-key guard needs the key to actually be in the
        # environment: `Settings` holds the name of the variable and never the
        # value, so `api_key()` reads it at send time. Restored afterwards
        # whatever happens -- a test that leaks a variable into the process
        # changes what every later test resolves.
        was = os.environ.get("LLOSSLESS_WEB_TEST_KEY")
        os.environ["LLOSSLESS_WEB_TEST_KEY"] = "a-token"
        try:
            remote = jobs.Workspace(
                directory=Path(raw), cache_dir=Path(raw),
                environ={"LLOSSLESS_BASE_URL": "http://endpoint.invalid:8000/v1",
                         "LLOSSLESS_API_KEY_ENV": "LLOSSLESS_WEB_TEST_KEY"})
            try:
                jobs.web_settings(request, remote)
                check(False, "a key in cleartext to a non-loopback host must be refused")
            except config.ConfigError as refusal:
                check("cleartext" in str(refusal),
                      f"the refusal must say why; it said {refusal}")

            # Must not fire: the same key to loopback is the documented local
            # default and has to keep working.
            local = jobs.Workspace(
                directory=Path(raw), cache_dir=Path(raw),
                environ={"LLOSSLESS_BASE_URL": "http://localhost:11434/v1",
                         "LLOSSLESS_API_KEY_ENV": "LLOSSLESS_WEB_TEST_KEY"})
            try:
                jobs.web_settings(request, local)
            except config.ConfigError as refusal:
                check(False, f"loopback with a key must be permitted; it said {refusal}")
        finally:
            if was is None:
                del os.environ["LLOSSLESS_WEB_TEST_KEY"]
            else:
                os.environ["LLOSSLESS_WEB_TEST_KEY"] = was


# The number the status scan looks for. It was `8443`, the port in the
# shared sources, and four digits are spelled by chance in a uuid4 hex id about
# once in 1,100 runs and in a float timestamp about as often again -- so the
# scan fired on generated values it was never about. This one is in a line the
# scan's own request adds, not in `SOURCE_A`, which `tests/test_cli.py` owns.
#
# **Long enough that nothing generated can spell it.** The id is exactly 32
# hex characters, so its longest digit run is 32; a float's `repr` carries at
# most 17 significant digits, so its longest run is 20 (`0.000` then 17); the
# integers are counts; no key or state name has a digit in it; and JSON puts a
# quote or a separator between any two values. A 40-digit run can only be in
# the payload if the payload carries it. Still a number, so it still catches
# what `8443` was there to catch: a value out of a document landing in a field
# that should hold a count, where it would be printed as bare digits.
STATUS_PROBE_NUMBER = "4096719235508172264913370658812047759013"
STATUS_PROBE_LINE = f"The relay licence number is {STATUS_PROBE_NUMBER}.\n"
STATUS_PROBES = ("relay", STATUS_PROBE_NUMBER, "notes-a.md", "notes-b.md")


def quoted_in_status(status: dict) -> list[str]:
    """Which probes out of the documents a status payload carries, `error` aside.

    `error` is excluded rather than asserted clean, because `Job.status` says in
    as many words that it is the one field which can carry a fragment of a
    document and why it is kept. Scanning it would make the check disagree with
    that disclosure; scanning everything else is what the disclosure claims.
    """
    payload = json.dumps({key: value for key, value in status.items()
                          if key != "error"})
    return [probe for probe in STATUS_PROBES if probe in payload]


def test_a_job_status_quotes_nothing_out_of_the_documents() -> None:
    """The web layer serves this from a route anyone holding the id can reach."""
    script = Script(**dict(CLEAN, merge=json.dumps({
        "merged_document": MERGED + STATUS_PROBE_LINE,
        "decisions": [], "dispositions": []})))
    with live_store(script) as (store, _):
        job = store.submit(jobs.MergeRequest(
            documents={"notes-a.md": SOURCE_A + STATUS_PROBE_LINE,
                       "notes-b.md": SOURCE_B},
            base="notes-a.md",
            overrides={"LLOSSLESS_MODEL": "test-model",
                       "LLOSSLESS_MERGE_MODEL": "test-model"}))
        if not wait_for(lambda: job.terminal):
            check(False, "the job never finished")
            return
        status = job.status()
        check(status["error"] is None, "a clean run carries no error")
        # The probe went through the whole run, not only into the request:
        # a merge that dropped the line would leave nothing to leak.
        check(job.report is not None and job.report.get("exit_code") == 0,
              f"the probe line must survive a clean run; exit "
              f"{(job.report or {}).get('exit_code')!r}")
        for secret in quoted_in_status(status):
            check(False, f"the status payload carries {secret!r} out of the "
                         f"operator's documents; everything but `error` must be "
                         f"a state, a timestamp, an integer or a count")
        check(status["state"] == jobs.DONE, "the status must still say what happened")


def test_the_status_scan_cannot_fire_on_a_generated_value() -> None:
    """The shape that used to collide, built on purpose, and the scan's must-fire.

    Rarer is not the claim. The id and the timestamps below are the worst a
    uuid4 and a float can do -- an id that is all digits and contains `8443`,
    the longest digit runs a float `repr` has in either notation, and `8443`
    inside a timestamp -- and the scan must stay silent on every one. The old
    probe is asserted to fire on the same payload, so the payload really is the
    one that used to collide.
    """
    worst = {
        "id": "84438443844384438443844384438443",  # 32 hex characters, all digits
        "state": jobs.DONE,
        "created_at": 1790208443.8443,           # `8443` in both halves
        "started_at": 0.00012345678901234567,    # the longest run: 0.000 + 17
        "finished_at": 1234567890123456.0,       # 16 digits before the point
        "forgotten_at": 1.2345678901234567e+300,
        "exit_code": 0,
        "error": None,
        "documents": 2,
        "events": 99,
    }
    check(len(worst["id"]) == 32 and set(worst["id"]) <= set("0123456789abcdef"),
          "the constructed id must have a uuid4 hex id's length and alphabet")
    payload = json.dumps({k: v for k, v in worst.items() if k != "error"})
    check("8443" in payload,
          "the constructed payload must be the one the old probe fired on")
    check(quoted_in_status(worst) == [],
          f"the scan fired on generated values: {quoted_in_status(worst)}")
    runs = [len(run) for run in
            "".join(c if c.isdigit() else " " for c in payload).split()]
    check(max(runs) < len(STATUS_PROBE_NUMBER),
          f"a generated digit run of {max(runs)} could spell a "
          f"{len(STATUS_PROBE_NUMBER)}-digit probe")

    # Must fire: the same payload quoting the documents, once per way it could.
    # A number in a count field is printed as bare digits, which is the case a
    # number probe is for and a word probe cannot see.
    for field, value, probe in (
            ("events", int(STATUS_PROBE_NUMBER), STATUS_PROBE_NUMBER),
            ("state", STATUS_PROBE_LINE.strip(), "relay"),
            ("id", "notes-b.md", "notes-b.md")):
        leaked = dict(worst, **{field: value})
        check(probe in quoted_in_status(leaked),
              f"the scan must fire on {field} carrying {probe!r}; it found "
              f"{quoted_in_status(leaked)}")
    check(quoted_in_status(dict(worst, error=STATUS_PROBE_LINE)) == [],
          "and not on `error`, which `Job.status` discloses can quote a document")


# --------------------------------------------------------------------------
# entry points
# --------------------------------------------------------------------------


def test_web_jobs_offline() -> None:
    """pytest entry point."""
    main()
    assert not failures, "\n".join(failures)


def openai_reasoning_endpoint(script):
    """A responder refusing what OpenAI's 5.6 reasoning SKUs refused when measured.

    Measured behaviour, not a reading of documentation: `max_tokens` refused
    for `max_completion_tokens`; `temperature: 0.0` refused unless it rides
    with `reasoning_effort: "none"`; `tools` beside `reasoning_effort` refused.
    Anything else is answered by `script`.
    """
    def refuse(message: str):
        return 400, json.dumps({"error": {"message": message,
                                          "type": "invalid_request_error"}})

    def responder(body: dict, n: int):
        if "max_tokens" in body:
            return refuse("Unsupported parameter: 'max_tokens' is not supported "
                          "with this model. Use 'max_completion_tokens' instead.")
        if ("temperature" in body and body["temperature"] != 1
                and body.get("reasoning_effort") != "none"):
            return refuse("Unsupported value: 'temperature' does not support 0.0 "
                          "with this model. Only the default (1) value is supported.")
        if "tools" in body and "reasoning_effort" in body:
            return refuse("Function tools with reasoning_effort are not supported")
        return script(body, n)
    return responder


def typed_for(provider: str | None, model: str, **overrides) -> jobs.MergeRequest:
    """A request carrying a typed model id, sent where the page's select says."""
    request = a_request(LLOSSLESS_MODEL=model, LLOSSLESS_MERGE_MODEL=model,
                        **overrides)
    return jobs.MergeRequest(documents=request.documents, base=request.base,
                             overrides=request.overrides, endpoint=provider)


def test_a_typed_id_gets_the_request_shape_its_provider_takes() -> None:
    """A typed OpenAI reasoning id sent to OpenAI must not go out as `openai-compatible`.

    `endpoint_plan` set a profile only from a catalogue row, so a model the
    catalogue does not know -- typed on the page, or listed by an endpoint --
    ran under the server's default body: `max_tokens`, and `temperature: 0.0`
    beside it. OpenAI's reasoning SKUs refuse the first on the first call.
    The shape now comes from the provider's own measured rows when they agree.

    Driven twice against a loopback endpoint that refuses what those SKUs
    refused: with the fix the run completes and no body carries `max_tokens`;
    with the lookup stubbed out the same run fails on exactly that refusal,
    which is what shows the endpoint can tell the two shapes apart.
    """
    openai_url = "https://api.openai.com/v1"
    # A stated window, because both providers are vendors and a model the
    # catalogue does not know is refused there without one.
    env = {"LLOSSLESS_PROVIDER_URL_OPENAI": openai_url,
           "LLOSSLESS_PROVIDER_URL_ANTHROPIC": "https://api.anthropic.com/v1",
           "LLOSSLESS_PROVIDER_MODELS_OPENAI": "gpt-5.6-listed",
           "LLOSSLESS_WINDOW": "200000"}
    for provider, model, want in (("openai", "gpt-5.6-luna", "openai-reasoning"),
                                  ("anthropic", "claude-typed-5", "anthropic"),
                                  (None, "gpt-5.6-listed", "openai-reasoning")):
        # Through `resolved_environ`, which puts the request's models over the
        # environment first; `endpoint_plan` alone would read this machine's
        # own model map instead of the typed id.
        plan = jobs.resolved_environ(typed_for(provider, model), dict(env))
        check(plan.get("LLOSSLESS_PROFILE") == want,
              f"{model} for {provider or 'the endpoint that listed it'} must "
              f"go out as {want}, got {plan.get('LLOSSLESS_PROFILE')!r}")
    # Must not fire: a typed id for the server's own endpoint names no
    # provider, so it keeps the server's shape; and an operator's own
    # LLOSSLESS_PROFILE is never overridden.
    plan = jobs.resolved_environ(typed_for(None, "some-local-model"), dict(env))
    check("LLOSSLESS_PROFILE" not in plan,
          f"a typed id for this server's own endpoint was given a profile: "
          f"{plan.get('LLOSSLESS_PROFILE')!r}")
    plan = jobs.resolved_environ(typed_for("openai", "gpt-5.6-luna"),
                                 dict(env, LLOSSLESS_PROFILE="openai-compatible"))
    check(plan.get("LLOSSLESS_PROFILE") == "openai-compatible",
          "a profile the operator set was overridden by the provider's")
    # And a row's stated shape outranks a provider's: a catalogue merge with
    # checks on a model an endpoint listed keeps the row's shape, as before.
    split = jobs.MergeRequest(
        documents={"a.md": SOURCE_A, "b.md": SOURCE_B},
        overrides={"LLOSSLESS_MERGE_MODEL": "claude-opus-5-5",
                   "LLOSSLESS_MODEL": "gpt-5.6-listed"})
    plan = jobs.resolved_environ(split, dict(env))
    check(plan.get("LLOSSLESS_PROFILE") == "anthropic",
          f"a split run must keep its catalogue row's shape, got "
          f"{plan.get('LLOSSLESS_PROFILE')!r}")

    def run(stub: bool):
        endpoint = FakeEndpoint(openai_reasoning_endpoint(Script(**CLEAN)),
                                ps_status=404)
        real = catalogue.provider_profile
        if stub:
            catalogue.provider_profile = lambda *_a, **_k: None
        try:
            with endpoint as url, tempfile.TemporaryDirectory() as raw:
                environ = {"LLOSSLESS_PROVIDER_URL_OPENAI": url,
                           "OPEN_AI_API_KEY": "sk-test-not-a-key",
                           "LLOSSLESS_STRUCTURED": "prompt",
                           # Stated, because a vendor exposes no /api/ps and a
                           # model the catalogue does not know carries no
                           # window: without it every decompose step refuses.
                           "LLOSSLESS_WINDOW": "200000"}
                with jobs.JobStore(Path(raw) / "work", environ=environ) as store:
                    job = store.submit(typed_for("openai", "gpt-5.6-luna",
                                                 LLOSSLESS_FIDELITY="high"))
                    wait_for(lambda: store.get(job.id).terminal)
                    done = store.get(job.id)
                    return done.state, str(done.error or ""), endpoint.requests
        finally:
            catalogue.provider_profile = real

    state, error, bodies = run(stub=False)
    check(state == jobs.DONE and not error,
          f"a typed OpenAI reasoning id must run against an endpoint that "
          f"refuses the default shape; ended {state}: {error[:200]}")
    check(len(bodies) >= 6 and not any("max_tokens" in b for b in bodies),
          f"{len(bodies)} call(s), and a body carried max_tokens")
    check(all(b.get("reasoning_effort") == "none" for b in bodies if "temperature" in b),
          "a temperature went out without reasoning_effort none")
    state, error, _ = run(stub=True)
    check(state == jobs.FAILED and "max_tokens" in error,
          f"with the provider's shape stubbed out the fake endpoint must refuse "
          f"the default body on max_tokens; it ended {state}: {error[:200]}")


def test_a_catalogue_model_carries_its_window_to_every_role() -> None:
    """A vendor endpoint has no `/api/ps`, so the window has to be stated.

    `config.DEFAULT_WINDOW` is `None`, meaning ask the endpoint, and asking is
    `GET /api/ps` -- ollama's route and nobody else's. Against OpenAI that is a
    404, `window.preflight` raises `WindowUnmeasurable`, and every decompose
    step refuses, while `merge` goes through because on a model-managed ceiling
    it never forms a budget to check.

    The operator hit exactly that: a run merged against `gpt-5.6-terra` in
    twenty seconds and then failed three times over. A half-finished run is a
    worse answer than a refusal, and the refusal was correct -- the catalogue
    had recorded `context_window` for every row all along and the web path was
    the one caller that knew it and did not pass it on.
    """
    env = {"LLOSSLESS_MODEL": "gpt-5.6-terra",
           "LLOSSLESS_MERGE_MODEL": "gpt-5.6-terra",
           "LLOSSLESS_PROVIDER_URL_OPENAI": "https://api.openai.com/v1"}
    plan = jobs.endpoint_plan(a_request(), env)
    for role in ("MERGE", "VERIFY", "DECOMPOSE"):
        check(plan.get(f"LLOSSLESS_WINDOW_{role}") == "200000",
              f"the catalogue records 200000 for this model and the {role} role "
              f"must be told it, got {plan.get(f'LLOSSLESS_WINDOW_{role}')!r}")

    # Must-not-fire: an operator who stated a window keeps it. A catalogue row
    # is a good default and not an override of somebody's explicit setting.
    stated = dict(env, LLOSSLESS_WINDOW="8192")
    kept = jobs.endpoint_plan(a_request(), stated)
    check(not any(k.startswith("LLOSSLESS_WINDOW_") for k in kept),
          f"a stated LLOSSLESS_WINDOW must not be overridden, got "
          f"{ {k: v for k, v in kept.items() if 'WINDOW' in k} }")

    # A model the catalogue has never seen carries no window, because nothing
    # in an endpoint's listing says how much context it serves. Guessing one is
    # the failure preflight exists to prevent.
    unknown = {"LLOSSLESS_MODEL": "some-model-nobody-catalogued",
               "LLOSSLESS_PROVIDER_MODELS_SELF_HOSTED": "some-model-nobody-catalogued",
               "LLOSSLESS_PROVIDER_URL_SELF_HOSTED": "http://127.0.0.1:11434/v1"}
    plan = jobs.endpoint_plan(a_request(), unknown)
    check(not any(k.startswith("LLOSSLESS_WINDOW_") for k in plan),
          f"a discovered model has no recorded window and must not be given "
          f"one, got { {k: v for k, v in plan.items() if 'WINDOW' in k} }")


def test_a_vendor_bound_unknown_model_is_refused_without_a_stated_window() -> None:
    """Where nothing can supply a window, the request must state one.

    A model the catalogue does not know, sent to a vendor, has no row window
    and no `/api/ps`; before this the merge ran and every check refused. Now
    `endpoint_plan` refuses at submit unless a window is stated -- by the
    request's `window`, or by the server for every role. Each case varies one
    thing against the refused one.
    """
    env = {"LLOSSLESS_PROVIDER_URL_OPENAI": "https://api.openai.com/v1",
           "LLOSSLESS_PROVIDER_URL_SELF_HOSTED": "http://127.0.0.1:4/v1"}

    def outcome(endpoint, model="gpt-typed-x", environ=None, **overrides):
        request = typed_for(endpoint, model, **overrides)
        try:
            jobs.resolved_environ(request, dict(env if environ is None else environ))
        except jobs.JobRefused as refusal:
            return str(refusal)
        return ""

    refused = outcome("openai")
    check("window field" in refused and "gpt-typed-x" in refused,
          f"a typed vendor id with no window must be refused, naming the "
          f"field and the model: {refused!r}")
    check(outcome("openai", LLOSSLESS_WINDOW="200000") == "",
          "a window stated in the request must satisfy it")
    check(outcome("openai", environ=dict(env, LLOSSLESS_WINDOW="200000")) == "",
          "a window the server states for every role must satisfy it")
    partial = dict(env, LLOSSLESS_WINDOW_MERGE="200000")
    check(outcome("openai", environ=partial) != "",
          "a window stated for the merge alone leaves the checks without one")
    check(outcome("self-hosted") == "",
          "a self-hosted endpoint may report its window and is not refused")
    check(outcome(None) == "",
          "nor is this server's own endpoint")
    check(outcome("openai", model="gpt-5.6-terra") == "",
          "a catalogue model carries its row's window and needs none")
    check(jobs.WINDOWLESS_PROVIDERS
          == frozenset(credentials.PROVIDERS) - {jobs.SELF_HOSTED_PROVIDER},
          f"the vendors are every provider but self-hosted: "
          f"{sorted(jobs.WINDOWLESS_PROVIDERS)}")
    for bad in ("100", "4095", "10000001", "2e5", "-5", ""):
        try:
            typed_for("openai", "gpt-typed-x", LLOSSLESS_WINDOW=bad)
            check(False, f"window {bad!r} was accepted by the job layer")
        except jobs.JobRefused:
            pass
    for good in (str(jobs.STATED_WINDOW_MIN), str(jobs.STATED_WINDOW_MAX)):
        check(outcome("openai", LLOSSLESS_WINDOW=good) == "",
              f"window {good} is inside the bounds and must be accepted")


# --------------------------------------------------------------------------
# the persisted queue
# --------------------------------------------------------------------------
#
# Every check below reads the shipped `JobStore` back from a directory, and
# every one has a must-fire seed: the shipped method patched to the defect the
# check exists for, and the same verdict function run against it. A crash is
# modelled as a copy of the work directory taken while a run is in flight --
# what reached disk at that instant is exactly what a SIGKILL leaves -- and
# `tests/test_web_server.py` kills a real server process for the same claim.


class Seeded:
    """Patch one attribute for the length of a `with`, and put it back."""

    def __init__(self, owner, name: str, value) -> None:
        self.owner, self.name, self.value = owner, name, value

    def __enter__(self):
        self.before = getattr(self.owner, self.name)
        setattr(self.owner, self.name, self.value)
        return self

    def __exit__(self, *exc_info) -> None:
        setattr(self.owner, self.name, self.before)


def crash_copy(work: Path, into: Path) -> Path:
    """The work directory as a SIGKILL would leave it: a copy, modes and all."""
    import shutil
    target = into / "after-crash"
    shutil.copytree(work, target)
    return target


class Selective:
    """A runner that finishes every job at once except the ones it is told to hold."""

    def __init__(self, hold: set[int]) -> None:
        self.hold = hold
        self.seen: list[str] = []
        self.release = threading.Event()
        self.lock = threading.Lock()

    def __call__(self, job, workspace) -> None:
        with self.lock:
            self.seen.append(job.id)
            number = len(self.seen)
        job.events.emit("done", f"step {number}", seconds=0.0)
        if number in self.hold:
            self.release.wait(timeout=PATIENCE)


def crash_verdict(seeded: bool = False) -> list[str]:
    """Queue three, crash while the second runs, restart. What went wrong, if anything."""
    problems: list[str] = []
    with tempfile.TemporaryDirectory() as raw:
        first = Selective(hold={2})
        store = jobs.JobStore(Path(raw) / "work", environ={}, runner=first).start()
        try:
            submitted = [store.submit(a_request()) for _ in range(3)]
            if not wait_for(lambda: submitted[0].state == jobs.DONE
                            and submitted[1].state == jobs.RUNNING):
                return ["the first run never finished or the second never started"]
            copy = crash_copy(store.work_dir, Path(raw))
        finally:
            first.release.set()
            store.close()
        second = Selective(hold=set())
        again = jobs.JobStore(copy, environ={}, runner=second)
        try:
            listed = [job.id for job in again.jobs()]
            if listed != [job.id for job in submitted]:
                problems.append(f"the order was not kept: {listed}")
            one, two, three = (again.get(job.id) for job in submitted)
            if one is None or one.state != jobs.DONE:
                problems.append("the finished run is not listed as done")
            if two is None or two.state != jobs.INTERRUPTED:
                problems.append(f"the running run is {getattr(two, 'state', None)}, "
                                f"not interrupted")
            elif not (two.error and "not complete" in two.error
                      and "1 step(s) had finished" in two.error
                      and "step 2" in two.error):
                problems.append(f"the interrupted run does not say what ran from "
                                f"its log on disk: {two.error!r}")
            if three is None or three.state != jobs.QUEUED:
                problems.append("the queued run was not queued after the restart")
            if again.restored["resumed"] != 1 or again.restored["interrupted"] != 1:
                problems.append(f"the reload summary is wrong: {again.restored}")
            again.start()
            if not wait_for(lambda: three is not None and three.state == jobs.DONE):
                problems.append("the queued run never ran after the restart")
            if second.seen != [submitted[2].id]:
                problems.append(f"the restarted server ran {second.seen}; only the "
                                f"queued run may run, and the interrupted one "
                                f"never by itself")
            replay = [event.fields.get("state") for event in two.events.since(0)
                      if event.kind == "state"] if two is not None else []
            if replay[-1:] != [jobs.INTERRUPTED]:
                problems.append(f"the interrupted run's log does not end on the "
                                f"interruption: {replay}")
        finally:
            again.close()
    return problems


def test_a_crash_mid_run_restarts_into_done_interrupted_and_resumed() -> None:
    """Three queued, a crash while the second runs: the restart settles each.

    Must not fire on the shipped store. Must fire on the seeded defect this
    exists for -- a store that puts a running job back on the queue, which is
    a silent re-run billing every call twice.
    """
    problems = crash_verdict()
    check(not problems, "after a crash: " + "; ".join(problems))

    shipped = jobs.JobStore._restore

    def requeue(self, record, now):
        if record["state"] == jobs.RUNNING:
            record = dict(record, state=jobs.QUEUED)
        return shipped(self, record, now)

    with Seeded(jobs.JobStore, "_restore", requeue):
        seeded = crash_verdict()
    check(any("interrupted" in problem for problem in seeded)
          and any("never by itself" in problem for problem in seeded),
          f"must fire: a store that re-queues a running job passed: {seeded}")


def restart_past_window(seed: bool = False) -> list[str]:
    """Finish a run, stop, restart after its window. Is everything of it gone?"""
    problems: list[str] = []
    with tempfile.TemporaryDirectory() as raw:
        clock = Clock()
        work = Path(raw) / "work"
        with jobs.JobStore(work, environ={}, runner=Selective(set()),
                           retention_seconds=600, clock=clock) as store:
            job = store.submit(a_request())
            kept = store.submit(a_request())
            if not wait_for(lambda: job.terminal and kept.terminal):
                return ["the runs never finished"]
        directory = work / job.id
        if not (directory / jobs.SOURCES_JSON).is_file():
            return ["the documents never reached disk, so nothing is being measured"]
        # One run finished well before the other, by the clock the window reads.
        clock.advance(601)
        index = json.loads((work / jobs.INDEX_JSON).read_text(encoding="utf-8"))
        for record in index["jobs"]:
            if record["id"] == kept.id:
                record["finished_at"] = clock.now - 10
        (work / jobs.INDEX_JSON).write_text(json.dumps(index), encoding="utf-8")
        context = (Seeded(jobs.JobStore, "sweep", lambda self, now=None: [])
                   if seed else contextlib.nullcontext())
        with context:
            again = jobs.JobStore(work, environ={}, runner=Selective(set()),
                                  retention_seconds=600, clock=clock)
        if directory.exists():
            problems.append("the run's directory outlived its window across a restart")
        stale = again.get(job.id)
        if stale is None or not stale.forgotten or stale.request.documents:
            problems.append("the expired run is not a tombstone after the restart")
        on_disk = json.loads((work / jobs.INDEX_JSON).read_text(encoding="utf-8"))
        entry = [r for r in on_disk["jobs"] if r["id"] == job.id]
        if not entry or entry[0]["settings"] is not None or entry[0]["forgotten_at"] is None:
            problems.append(f"the index still holds the expired run's settings: {entry}")
        if not (work / kept.id).is_dir() or again.get(kept.id).forgotten:
            problems.append("a run inside its window was deleted with the other")
        # And the tombstone itself goes one window later.
        clock.advance(601)
        again.sweep()
        if again.get(job.id) is not None or job.id in (work / jobs.INDEX_JSON).read_text():
            problems.append("the tombstone was never dropped from the index")
    return problems


def test_a_restart_past_the_window_deletes_and_leaves_only_a_tombstone() -> None:
    """Retention applies to the reloaded index as to the uploads."""
    problems = restart_past_window()
    check(not problems, "restart past the window: " + "; ".join(problems))
    seeded = restart_past_window(seed=True)
    check(any("outlived" in problem for problem in seeded),
          f"must fire: a restart that never swept passed: {seeded}")


class TwoAccounts:
    """The two methods `JobStore` asks a `Directory`, for two accounts with keys."""

    def __init__(self, keys: dict[str, dict[str, str]]) -> None:
        self.keys = keys

    def environ_for(self, owner: str) -> dict[str, str]:
        return {}

    def keys_for(self, owner: str, environ) -> dict[str, str]:
        return dict(self.keys.get(owner, {}))


def isolation_verdict() -> list[str]:
    """Two owners, a restart, and the API's own lookup. Who sees whose run?"""
    from llossless.web import api as web_api
    problems: list[str] = []

    class Who:
        def __init__(self, ident: str) -> None:
            self.id = ident
            self.operator = False

    alice, bob = Who("a" * 32), Who("b" * 32)
    with tempfile.TemporaryDirectory() as raw:
        work = Path(raw) / "work"
        with jobs.JobStore(work, environ={}, runner=Selective(set())) as store:
            hers = store.submit(a_request(), owner=alice.id)
            his = store.submit(a_request(), owner=bob.id)
            if not wait_for(lambda: hers.terminal and his.terminal):
                return ["the runs never finished"]
        again = jobs.JobStore(work, environ={}, runner=Selective(set()))
        facade = web_api.Api(again)
        for who, own, other in ((alice, hers, his), (bob, his, hers)):
            listed = [run["id"] for run in facade.runs(who)["runs"]]
            if listed != [own.id]:
                problems.append(f"{who.id[:1]} lists {listed} after the restart, "
                                f"not only their own run")
            try:
                facade.run(other.id, who)
                problems.append(f"{who.id[:1]} can read the other's reloaded run")
            except web_api.ApiError as refusal:
                if refusal.status != 404:
                    problems.append(f"a stranger's run answered {refusal.status}, "
                                    f"not the 404 an unknown id gets")
    return problems


def test_one_user_never_sees_another_s_reloaded_runs() -> None:
    """Per-user isolation holds across a restart.

    Two seeds on the shipped code: the owner not written to the index (so a
    run comes back belonging to nobody) and the ownership check answering yes.
    """
    problems = isolation_verdict()
    check(not problems, "isolation after a restart: " + "; ".join(problems))

    from llossless.web import api as web_api
    shipped = jobs.JobStore._record

    def ownerless(self, job):
        return dict(shipped(self, job), owner="")

    with Seeded(jobs.JobStore, "_record", ownerless):
        lost = isolation_verdict()
    check(any("not only their own" in problem for problem in lost),
          f"must fire: an index that drops the owner passed: {lost}")
    with Seeded(web_api.Api, "_owns", staticmethod(lambda job, who: True)):
        open_ = isolation_verdict()
    check(any("can read the other" in problem for problem in open_),
          f"must fire: an ownership check that says yes passed: {open_}")


def slow(script, delay: float):
    """A responder that answers `script`'s reply after `delay` seconds."""
    def responder(body: dict, n: int):
        time.sleep(delay)
        return script(body, n)
    return responder


def retry_verdict(seed: bool = False) -> list[str]:
    """Interrupt a real merge after its first step, restart, Retry. Is it a new run?"""
    problems: list[str] = []
    script = Script(**CLEAN)
    endpoint = FakeEndpoint(slow(script, 0.3))
    with endpoint as base_url, tempfile.TemporaryDirectory() as raw:
        environ = {"LLOSSLESS_BASE_URL": base_url, "LLOSSLESS_STRUCTURED": "prompt"}
        store = jobs.JobStore(Path(raw) / "work", environ=environ).start()
        try:
            old = store.submit(a_request())
            log = store.work_dir / old.id / jobs.EVENTS_JSONL
            if not wait_for(lambda: log.is_file() and '"kind": "done"' in log.read_text()):
                return ["the run never finished a step"]
            copy = crash_copy(store.work_dir, Path(raw))
        finally:
            store.close()
        again = jobs.JobStore(copy, environ=environ).start()
        try:
            interrupted = again.get(old.id)
            if interrupted is None or interrupted.state != jobs.INTERRUPTED:
                return [f"the run is {getattr(interrupted, 'state', None)} after "
                        f"the restart, not interrupted"]
            before = endpoint.calls
            context = (Seeded(jobs.JobStore, "retry", seeded_retry)
                       if seed else contextlib.nullcontext())
            with context:
                new = again.retry(old.id)
            if not wait_for(lambda: new.terminal):
                return ["the retry never finished"]
            if new.id == old.id or new is interrupted:
                problems.append("Retry re-used the interrupted job instead of "
                                "making a new one")
            if new.retry_of != old.id or new.status()["retry_of"] != old.id:
                problems.append("the new run does not link to the old one")
            if new.directory == interrupted.directory:
                problems.append("the new run writes into the old run's directory")
            old_steps = {e.id for e in interrupted.events.since(0)}
            if [e.id for e in new.events.since(0)][:1] != [1]:
                problems.append("the new run's log does not start from its own "
                                f"first event (old ids: {sorted(old_steps)[:3]}...)")
            calls = ((new.report or {}).get("provenance") or {}).get("counts", {}).get("calls")
            if not isinstance(calls, int) or endpoint.calls - before != calls:
                problems.append(f"the retry's report counts {calls} calls and the "
                                f"endpoint saw {endpoint.calls - before}")
            merges = [b for b in script.bodies[-(endpoint.calls - before):]
                      if Script.MARKERS["merge"] in b["messages"][0]["content"]] \
                if endpoint.calls - before else []
            if len(merges) != 1:
                problems.append(f"the retry did not make its own merge call "
                                f"({len(merges)} seen): the partial run's answers "
                                f"were re-used or skipped")
            if new.state != jobs.DONE:
                problems.append(f"the retry ended {new.state}: {new.error}")
            if interrupted.state != jobs.INTERRUPTED:
                problems.append("Retry changed the old run's state")
        finally:
            again.close()
    return problems


def seeded_retry(self, job_id):
    """The defect: Retry puts the interrupted job itself back on the queue."""
    job = self.get(job_id)
    with self._lock:
        job.state = jobs.QUEUED
        job.events = EventLog(job.directory / jobs.EVENTS_JSONL)
    self._queue.put(job.id)
    return job


def test_retry_is_a_new_run_and_reuses_none_of_the_partial_one() -> None:
    """Retry starts a new job from the same documents and settings."""
    problems = retry_verdict()
    check(not problems, "Retry: " + "; ".join(problems))
    seeded = retry_verdict(seed=True)
    check(any("re-used the interrupted job" in problem for problem in seeded),
          f"must fire: a Retry that re-queues the old job passed: {seeded}")


def test_retry_is_refused_for_a_run_that_finished_or_lost_its_documents() -> None:
    """Only failed and interrupted runs, and only while their documents are held."""
    with stub_store(Selective(set())) as store:
        done = store.submit(a_request())
        wait_for(lambda: done.terminal)
        try:
            store.retry(done.id)
            check(False, "a finished run was retried")
        except jobs.JobRefused:
            pass
        with store._lock:
            done.state = jobs.FAILED
        check(done.retryable, "must not fire: a failed run with its documents is retryable")
        store._forget(done, "forgotten: test")
        check(not done.retryable, "a forgotten run must not be retryable")
        try:
            store.retry(done.id)
            check(False, "a run whose documents are gone was retried")
        except jobs.JobRefused:
            pass


SECRET_ENV = "sk-envplanted-" + "q" * 20
SECRET_USER = "sk-userplanted-" + "w" * 20


def index_secrecy(seed=None) -> list[str]:
    """Run a job with a key in the environment and one on the account; grep the disk."""
    problems: list[str] = []
    seen_keys: list[dict] = []

    def runner(job, workspace):
        # The key really is in play for this run, or the grep proves nothing.
        seen_keys.append(workspace.keys() if callable(workspace.keys) else {})

    owner = "c" * 32
    with tempfile.TemporaryDirectory() as raw:
        work = Path(raw) / "work"
        environ = {"OPENAI_API_KEY": SECRET_ENV, "LLOSSLESS_API_KEY": SECRET_ENV}
        directory = TwoAccounts({owner: {"ANTHROPIC_API_KEY": SECRET_USER}})
        context = seed if seed is not None else contextlib.nullcontext()
        with context, jobs.JobStore(work, environ=environ, directory=directory,
                                    runner=runner) as store:
            job = store.submit(a_request(), owner=owner)
            wait_for(lambda: job.terminal)
        if not seen_keys or seen_keys[0].get("ANTHROPIC_API_KEY") != SECRET_USER:
            return ["the per-user key never reached the run, so the grep is vacuous"]
        index = work / jobs.INDEX_JSON
        mode = stat.S_IMODE(index.stat().st_mode)
        if mode != jobs.FILE_MODE:
            problems.append(f"the index is mode {mode:o}, not {jobs.FILE_MODE:o}")
        if stat.S_IMODE(work.stat().st_mode) != jobs.DIR_MODE:
            problems.append("the work directory is not owner-only")
        for path in sorted(work.rglob("*")):
            if not path.is_file():
                continue
            text = path.read_bytes()
            for secret in (SECRET_ENV, SECRET_USER):
                if secret.encode() in text:
                    problems.append(f"{path.relative_to(work)} holds a planted key")
            if path.parent != work / ".cache":
                file_mode = stat.S_IMODE(path.stat().st_mode)
                if file_mode != jobs.FILE_MODE:
                    problems.append(f"{path.relative_to(work)} is mode {file_mode:o}")
    return problems


def test_the_index_is_owner_only_and_holds_no_key() -> None:
    """0600, and no API key or per-user credential anywhere in the work directory.

    Two seeds on the shipped code: an index record that carries the store's
    environment, and an index written at 0644.
    """
    problems = index_secrecy()
    check(not problems, "index secrecy: " + "; ".join(problems))

    shipped = jobs.JobStore._record

    def leaky(self, job):
        return dict(shipped(self, job), environ=dict(self.environ),
                    keys=self.keys_for(job.owner))

    leaked = index_secrecy(Seeded(jobs.JobStore, "_record", leaky))
    check(any("planted key" in problem for problem in leaked),
          f"must fire: an index carrying the environment passed: {leaked}")
    loose = index_secrecy(Seeded(jobs, "FILE_MODE", 0o644))
    check(any("the index is mode 644" in problem for problem in loose),
          f"must fire: an index written 0644 passed: {loose}")


def corrupt_verdict(damage, seed: bool = False) -> list[str]:
    """Damage the index, restart. Refused loudly, with nothing deleted?"""
    problems: list[str] = []
    with tempfile.TemporaryDirectory() as raw:
        work = Path(raw) / "work"
        with jobs.JobStore(work, environ={}, runner=Selective(set())) as store:
            job = store.submit(a_request())
            wait_for(lambda: job.terminal)
        index = work / jobs.INDEX_JSON
        index.write_bytes(damage(index.read_bytes()))
        context = (Seeded(jobs, "parse_index", lambda raw, path: [])
                   if seed else contextlib.nullcontext())
        try:
            with context:
                jobs.JobStore(work, environ={}, runner=Selective(set()))
            problems.append("a damaged index was accepted")
        except jobs.IndexUnreadable as refusal:
            said = str(refusal)
            if str(index) not in said or "move that file aside" not in said:
                problems.append(f"the refusal does not name the file and the way "
                                f"out: {said!r}")
        if not (work / job.id / jobs.SOURCES_JSON).is_file():
            problems.append("the refusal deleted a run's documents")
        # The way out it names works: moved aside, the next start is empty and
        # removes the directory no index names.
        if not problems:
            index.rename(work / "index.json.broken")
            fresh = jobs.JobStore(work, environ={}, runner=Selective(set()))
            if fresh.jobs() or (work / job.id).exists():
                problems.append("after moving the index aside the start was not "
                                "empty, or left the unindexed directory")
            if fresh.restored["orphans_deleted"] != 1:
                problems.append(f"the orphan count is {fresh.restored}")
    return problems


def test_a_corrupt_or_partial_index_refuses_loudly_and_deletes_nothing() -> None:
    """Refuse, never start empty in silence and never mix."""
    truncations = {
        "truncated": lambda raw: raw[: len(raw) // 2],
        "garbage": lambda raw: b"\x00\xffnot json",
        "empty": lambda raw: b"",
        "unknown state": lambda raw: raw.replace(b'"done"', b'"finished"'),
        "missing field": lambda raw: raw.replace(b'"retry_of"', b'"retried_of"'),
        "planted variable": lambda raw: raw.replace(
            b'"overrides": {', b'"overrides": {"LLOSSLESS_BASE_URL": "http://x", '),
    }
    for name, damage in truncations.items():
        problems = corrupt_verdict(damage)
        check(not problems, f"index {name}: " + "; ".join(problems))
    seeded = corrupt_verdict(truncations["truncated"], seed=True)
    check(any("was accepted" in problem for problem in seeded),
          f"must fire: a parser that answers empty passed: {seeded}")


def queue_places(seed: bool = False) -> list[str]:
    """Three submitted, one running: are the positions the queue's own order?"""
    from llossless.web import api as web_api
    problems: list[str] = []
    gate = Gate()
    with stub_store(gate) as store:
        running, second, third = (store.submit(a_request()) for _ in range(3))
        if not wait_for(lambda: running.state == jobs.RUNNING):
            return ["the first run never started"]
        context = (Seeded(jobs.JobStore, "queue_position",
                          lambda self, job: (self._order.index(job.id) + 1,
                                             len(self._order)))
                   if seed else contextlib.nullcontext())
        with context:
            facade = web_api.Api(store)
            places = [(p["queue_position"], p["queue_length"])
                      for p in (facade.run(j.id) for j in (running, second, third))]
        if places != [(None, None), (1, 2), (2, 2)]:
            problems.append(f"positions {places}, expected no place for the running "
                            f"run and 1 of 2, 2 of 2")
        gate.release.set()
        wait_for(lambda: third.terminal)
        with context:
            after = facade.run(third.id)
        if (after["queue_position"], after["queue_length"]) != (None, None):
            problems.append("a finished run still reports a queue position")
    return problems


def test_a_queued_run_knows_its_place_and_nothing_more() -> None:
    """ "Queued, position 2 of 3": the running run has no place, the queue is ordered."""
    problems = queue_places()
    check(not problems, "queue position: " + "; ".join(problems))
    seeded = queue_places(seed=True)
    check(any("positions" in problem for problem in seeded),
          f"must fire: a position counted over every run passed: {seeded}")


def test_a_torn_last_event_line_is_dropped_and_ids_carry_on() -> None:
    """The log a crash leaves: every whole line kept, the cut one dropped."""
    with tempfile.TemporaryDirectory() as raw:
        path = Path(raw) / jobs.EVENTS_JSONL
        log = EventLog(path)
        for number in range(3):
            log.emit("step", f"step {number}")
        with open(path, "a", encoding="utf-8") as stream:
            stream.write('{"id": 4, "kind": "st')
        back = EventLog.restore(path)
        check([event.id for event in back.since(0)] == [1, 2, 3],
              f"the restored log is {[e.id for e in back.since(0)]}")
        check(back.emit("step", "next").id == 4,
              "a restored log must carry on from its last whole id")
        check(stat.S_IMODE(path.stat().st_mode) == jobs.FILE_MODE,
              "the event log is not owner-only")


def test_a_second_store_on_a_live_work_directory_is_refused() -> None:
    """One owner per work directory, released when the owner closes or dies.

    Must fire on the shipped store with its lock taken away: the second store
    then reads the first one's running job as interrupted.
    """
    def verdict() -> list[str]:
        problems: list[str] = []
        gate = Gate()
        with tempfile.TemporaryDirectory() as raw:
            work = Path(raw) / "work"
            first = jobs.JobStore(work, environ={}, runner=gate).start()
            try:
                job = first.submit(a_request())
                wait_for(lambda: job.state == jobs.RUNNING)
                try:
                    second = jobs.JobStore(work, environ={}, runner=Selective(set()))
                    problems.append("a second store opened a work directory in use")
                    if second.get(job.id) is not None and second.get(job.id).state == jobs.INTERRUPTED:
                        problems.append("the second store marked the live run interrupted")
                    second.close()
                except jobs.WorkDirBusy as refusal:
                    if str(work) not in str(refusal):
                        problems.append("the refusal does not name the directory")
                if job.state != jobs.RUNNING:
                    problems.append("the live run was disturbed")
            finally:
                gate.release.set()
                first.close()
            try:
                jobs.JobStore(work, environ={}, runner=Selective(set())).close()
            except jobs.WorkDirBusy:
                problems.append("a closed store kept the directory locked")
        return problems

    problems = verdict()
    check(not problems, "work directory lock: " + "; ".join(problems))
    with Seeded(jobs.JobStore, "_claim_work_dir", lambda self: None):
        seeded = verdict()
    check(any("in use" in problem for problem in seeded),
          f"must fire: a store with no lock passed: {seeded}")


def main() -> int:
    checks = 0
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and name != "test_web_jobs_offline" \
                and callable(function):
            function()
            checks += 1
    if failures:
        print(f"{len(failures)} failing:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"web jobs: {checks} checks pass over {len(jobs.STATES)} job states and "
          f"{len(events.KINDS)} event kinds")
    return 0


if __name__ == "__main__":
    sys.exit(main())
