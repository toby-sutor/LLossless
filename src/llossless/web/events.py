"""Progress as structured events, for a browser watching a run it cannot hold open.

A merge takes between 23 and 4,559 seconds, measured over `paper/records/*.json`.
Nothing about that is compatible with a request/response cycle, so the web UI
submits work and then watches it, and this module is the watching half: a
`Console` subclass that records what the engine says instead of printing it, an
append-only log to record it into, and the encoding a Server-Sent Events
endpoint will write frames with.

**The events come from the console, and that is the point rather than a
convenience.** `cli.step` (`cli.py:653`) is the single place every unit of work
reports its outcome, and it reports to `run.steps` and to the console from the
same four branches, precisely so that a `-v` transcript and the step list in the
finished report cannot disagree about what happened. Building the progress
stream on the console inherits that property: the browser is watching the same
branches the report is written from. A second progress mechanism -- a callback
threaded through the pipeline, a tail of a log file, a poller comparing
`len(run.steps)` -- would be a second account of the run, and the interesting
failure is the one where the two accounts differ and the report is the one
nobody was reading.

**Nothing here formats.** `Console`'s eight public methods receive a message, an
optional `seconds=` and an optional `level=` *before* any glyph, colour or
indent is applied, so an override sees structured arguments and can store them
as such. That is why all eight are overridden rather than `_write` alone:
intercepting `_write` would hand this module a painted string to parse back
apart, and a parser for a format the same repository owns is a format that
breaks the day someone widens a column.

**Ids are per-job, stable, and never reused.** A browser that loses its
connection forty minutes into a run reconnects with `Last-Event-ID` and expects
everything it missed. That works only if the id it holds still identifies the
same position in the same sequence, so the counter here is monotonic for the
life of the log -- it is not an index into the list, and `forget()` below
clears the stored events without rewinding it. Ids are scoped to one job
because `Last-Event-ID` is scoped to the URL the browser reconnects to, and
each job has its own stream; a process-global counter would be a number whose
meaning depended on what some other user submitted in between.

**A frame's `data:` is one line.** SSE delimits fields by newline, so a message
carrying one would end the frame early and the rest of it would arrive as a
field the browser does not recognise. `json.dumps` with the default
`ensure_ascii=True` escapes every newline and every non-ASCII character, so the
payload is a single ASCII line by construction rather than by a sanitising pass
that has to be remembered. It is asserted rather than assumed --
`tests/test_web_jobs.py` puts a newline in a message and checks the frame.
"""

from __future__ import annotations

import io
import json
import os
import threading
import time
from pathlib import Path

from ..console import Console
from . import diagnose

# Every kind an event can have, and where each one comes from. A registry
# rather than a free string: W4 renders these into a page and W8 translates
# them, and a kind invented at a call site is a kind with no renderer and no
# translation, discovered by a reader who sees a blank row.
#
# The first eight are `Console`'s eight public methods, named after the method
# rather than after what the method prints, so that a reader who has the
# console open can follow the mapping without a table. The ninth is this
# module's own: a job's lifecycle is not something the engine has an opinion
# about, and folding it into `step` would put "the queue started this" in the
# same kind as "the merge call started".
KINDS = frozenset({
    "step",      # Console.step     -- a unit of work is starting
    "done",      # Console.done     -- it finished, with `seconds`
    "failed",    # Console.failed   -- it did not
    "skipped",   # Console.skipped  -- it was not attempted
    "detail",    # Console.detail   -- what a second -v would have added
    "warn",      # Console.warn     -- said whatever the verbosity
    "notice",    # Console.notice   -- something slow starting, e.g. a cold endpoint
    "banner",    # Console.banner   -- what this run is, before it starts
    "state",     # this module      -- queued/running/done/failed/forgotten
})

# What the WebConsole is constructed with, and why each number is that number.
# Both are arguments with defaults rather than constants inlined below, because
# a caller that wants a quieter stream should get it by turning the same knob
# the CLI turns, not by a second mechanism.
#
# `VERBOSITY = 2` is the CLI's `-vv`. `step`, `done` and `banner` are gated at
# level 1 and `detail` at level 2 (`console.py:157-183`), so anything lower
# silently drops whole classes of event and the browser would show a run that
# looked like it was doing less than it was. The CLI defaults to 0 because a
# terminal has to stay readable and the operator is watching one stream; a
# browser has a scrollable pane, one stream per job, and a forty-minute wait to
# fill, so the reason for the quiet default does not carry over.
VERBOSITY = 2

# `ENABLED = False` is what stops a spinner thread existing. `Console.__init__`
# computes `self.animate = enabled and verbosity > 0 and is_tty(self.stream)`
# (`console.py:151`), and `waiting()` only starts its ticker thread when
# `animate` is true (`console.py:279`) -- so with `enabled` false the context
# manager yields an elapsed-time closure and starts nothing. That matters more
# here than on a terminal: `waiting()` wraps every model call, a worker pool
# would spawn one ticker per concurrent job, and each of those would be writing
# carriage returns to a stream no operator is looking at. `enabled` also turns
# off colour, which is what an escape sequence in a JSON payload would be.
#
# `waiting()` is deliberately *not* overridden. Inheriting it is the check: if
# the construction above is ever changed so that `animate` becomes true, the
# base implementation starts a thread and `tests/test_web_jobs.py` fails on the
# thread count. An override would make that failure unreachable by replacing
# the code path the mistake would live in.
ENABLED = False


class Event:
    """One thing that happened, as the console was told it.

    Not a dataclass, and not frozen by convention alone: the log below hands
    the same object to every reader, across threads, for the life of a job, and
    the whole replay guarantee rests on an event never changing after it is
    appended. `__slots__` and no setters is the cheapest way to mean that.

    `fields` is the escape hatch for the one method whose arguments are not a
    message -- `banner` takes five -- and for the lifecycle events this module
    emits itself. It is never used to carry a second copy of `message`.
    """

    __slots__ = ("id", "kind", "message", "at", "seconds", "level", "fields")

    def __init__(self, id: int, kind: str, message: str, *, at: float,
                 seconds: float | None = None, level: int = 1,
                 fields: dict | None = None) -> None:
        if kind not in KINDS:
            # Refused at construction rather than rendered as an unknown kind.
            # A frame whose `event:` field names something the page has no
            # handler for is dropped by the browser in silence, which is the
            # one failure shape a progress stream must not have.
            raise ValueError(f"unknown event kind {kind!r}; the kinds are "
                             f"{', '.join(sorted(KINDS))}")
        self.id = id
        self.kind = kind
        self.message = message
        self.at = at
        self.seconds = seconds
        self.level = level
        self.fields = dict(fields or {})

    def as_dict(self) -> dict:
        """The wire form. JSON-serialisable, and with no key whose value is absent.

        `seconds` is omitted rather than sent as null when the console was not
        told one: a step that is starting has no duration, and `"seconds":
        null` invites a renderer to print `0.0s` beside it.
        """
        payload = {"id": self.id, "kind": self.kind, "message": self.message,
                   "at": self.at, "level": self.level}
        if self.seconds is not None:
            payload["seconds"] = self.seconds
        if self.fields:
            payload["fields"] = self.fields
        return payload

    @classmethod
    def from_dict(cls, payload: dict) -> Event:
        """The inverse of `as_dict`, for a log read back off disk (660).

        Raises `ValueError`, `KeyError` or `TypeError` on anything that is not
        an event this module wrote; `EventLog.restore` decides what that means.
        """
        if not isinstance(payload, dict):
            raise TypeError("an event is a JSON object")
        seconds = payload.get("seconds")
        return cls(int(payload["id"]), str(payload["kind"]), str(payload["message"]),
                   at=float(payload["at"]),
                   seconds=None if seconds is None else float(seconds),
                   level=int(payload["level"]),
                   fields=dict(payload.get("fields") or {}))

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"Event({self.id}, {self.kind!r}, {self.message!r})"


class EventLog:
    """Append-only, thread-safe, and replayable from any id it ever issued.

    One of these per job. The worker thread appends; HTTP threads read. The
    lock is held only around the list itself, never across a caller's
    iteration, so a slow reader cannot stall a merge.

    `wait()` exists so that an SSE endpoint does not have to poll. Without it
    W4's stream loop would sleep on a timer, which either wastes the wakeups or
    adds latency to every line the operator is watching for; with it, the
    endpoint blocks until the worker appends something or the timeout expires,
    and the timeout is then only a keep-alive interval rather than a polling
    interval.
    """

    def __init__(self, path: Path | None = None, *, next_id: int = 1) -> None:
        self._events: list[Event] = []
        # Monotonic for the life of the log, and not derived from
        # `len(self._events)`. `forget()` empties the list; an id derived from
        # its length would then hand the tombstone the id of an event that has
        # already been delivered, and a browser holding that id would ask for
        # the tail after it and be told there was none. See `forget()`.
        #
        # An argument since 660, for the same reason: a job reloaded after a
        # restart carries on from the id its log had reached, so a browser that
        # held `Last-Event-ID: 57` across the restart is still answerable.
        self._next_id = max(1, int(next_id))
        self._condition = threading.Condition()
        self._closed = False
        # Where each event is appended as it is emitted, or None (660). The
        # file is what a server restarted after a crash reads to say what a
        # run had done before the stop -- the only account of it that reached
        # disk, since the report is written on the way out and a killed
        # process never gets there. It lives in the job's own directory, so
        # retention deletes it with the documents it may quote.
        self._path = path

    @property
    def next_id(self) -> int:
        """The id the next event will get. Persisted with a tombstone (660)."""
        with self._condition:
            return self._next_id

    @classmethod
    def restore(cls, path: Path) -> EventLog:
        """A log read back from the file `emit` appended to, still appending.

        A missing file is an empty log: a job can be killed before its first
        event reached disk. A torn *last* line is dropped, and only the last:
        the file is appended one whole line at a time, so a crash can cut the
        line being written and nothing before it. A bad line anywhere else is
        not a crash artefact, and the log is read up to it and no further
        rather than guessed across.
        """
        log = cls(path)
        try:
            raw = path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return log
        for line in raw.splitlines():
            if not line.strip():
                continue
            try:
                event = Event.from_dict(json.loads(line))
            except (ValueError, KeyError, TypeError):
                break
            if event.id < log._next_id:
                break
            log._events.append(event)
            log._next_id = event.id + 1
        return log

    def _persist(self, event: Event) -> None:
        """Append one event to the log's file, owner-only, synced. Never raises.

        `O_APPEND` so each line lands whole at the end, and synced because the
        crash this exists for is a machine going down, where an unsynced write
        is a write that did not happen. A failure to write is swallowed: the
        run is worth more than the transcript of it, and a log short of its
        last lines only makes a restarted server say *less* about what ran --
        the interrupted run's account says "what reached disk", never more.
        """
        if self._path is None:
            return
        line = json.dumps(event.as_dict(), sort_keys=True) + "\n"
        try:
            handle = os.open(self._path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
            try:
                os.write(handle, line.encode("utf-8"))
                os.fsync(handle)
            finally:
                os.close(handle)
        except OSError:
            pass

    def emit(self, kind: str, message: str, *, seconds: float | None = None,
             level: int = 1, **fields) -> Event:
        with self._condition:
            event = Event(self._next_id, kind, message, at=time.time(),
                          seconds=seconds, level=level, fields=fields)
            self._next_id += 1
            self._events.append(event)
            self._persist(event)
            self._condition.notify_all()
            return event

    def since(self, after_id: int = 0) -> tuple[Event, ...]:
        """Everything issued after `after_id`, oldest first. The replay query.

        `after_id=0` is the whole log, which is what a browser connecting for
        the first time sends by sending no `Last-Event-ID` at all. An id past
        the end returns empty rather than raising: a reader that is already
        current is the normal case on every reconnect, not an error.

        Linear rather than indexed, on purpose. The list is dense and ordered
        by id, so a bisect would be correct and faster, and the difference is
        unmeasurable against a log of a few hundred events -- while an index
        that got out of step with `forget()` would be a replay that silently
        skipped a range.
        """
        with self._condition:
            return tuple(event for event in self._events if event.id > after_id)

    def wait(self, after_id: int = 0, timeout: float | None = None) -> tuple[Event, ...]:
        """Block until there is something after `after_id`, or `timeout` passes.

        Returns the same tuple `since` would, possibly empty. The caller is
        expected to loop on `closed` rather than on this returning empty: an
        empty tuple means "nothing yet", and a job that has finished is
        recognised by the terminal `state` event or by `closed`, never by
        silence.
        """
        with self._condition:
            tail = tuple(event for event in self._events if event.id > after_id)
            if tail or self._closed:
                return tail
            self._condition.wait(timeout)
            return tuple(event for event in self._events if event.id > after_id)

    def close(self) -> None:
        """No further events. Wakes every waiter so no stream hangs on a done job."""
        with self._condition:
            self._closed = True
            self._condition.notify_all()

    @property
    def closed(self) -> bool:
        with self._condition:
            return self._closed

    def forget(self, message: str) -> Event:
        """Drop every stored event and leave one tombstone in their place.

        Called by retention. The step names this log carries are canonical
        (`merge`, `decompose source_a.md`) and carry nothing of the operator's
        text, but a failed step's detail is `f"{type(exc).__name__}: {exc}"`
        (`cli.py:679`) and an exception raised while parsing a model's answer
        about a document can quote that document. That is enough to make the
        log user data, and user data is deleted when the window passes rather
        than kept because most of it is probably harmless.

        The id counter is *not* rewound, and that is the whole reason this is a
        method rather than a caller assigning a fresh `EventLog`. A browser
        holding `Last-Event-ID: 57` must still be answerable: after this, id 58
        is the tombstone and `since(57)` returns it, so the page is told the
        run was forgotten instead of hanging on an empty tail forever.
        """
        with self._condition:
            # Detached first: the file is in the job's directory, which is
            # being deleted, and the tombstone is not user data to keep.
            self._path = None
            self._events.clear()
            event = Event(self._next_id, "state", message, at=time.time(),
                          fields={"state": "forgotten", "terminal": True})
            self._next_id += 1
            self._events.append(event)
            self._closed = True
            self._condition.notify_all()
            return event

    def __len__(self) -> int:
        with self._condition:
            return len(self._events)


class WebConsole(Console):
    """A `Console` that records instead of printing. All eight methods overridden.

    Constructed silent (`enabled=False`) and loud (`verbosity=2`) at once,
    which reads as a contradiction and is not: `enabled` decides whether
    anything is *painted and animated*, `verbosity` decides what is *said*.
    The web wants everything said and nothing painted. See `ENABLED` and
    `VERBOSITY` above for what each of those buys.

    The level gates are kept rather than dropped. An override could record
    unconditionally and let the browser filter, but then `verbosity` would mean
    something different here than it does on the command line while keeping the
    same name, and a caller lowering it would be surprised to find it changed
    nothing. Same knob, same meaning, different default.

    `stream` is a `StringIO` nobody reads, and it is a detector rather than a
    bin. `Console` may grow a ninth method; if it does and this class has not
    been extended to cover it, the inherited version calls `_write` and the
    text lands in that buffer instead of on the server's stderr, where it would
    be interleaved with every other job's output and attributed to none of
    them. `written` exposes the buffer so a test can assert it is empty after a
    complete run, which turns "all eight are overridden" from a claim in this
    docstring into something the suite checks.
    """

    def __init__(self, log: EventLog | None = None) -> None:
        self.log = EventLog() if log is None else log
        self._sink = io.StringIO()
        super().__init__(self._sink, verbosity=VERBOSITY, enabled=ENABLED)

    # -- the eight -------------------------------------------------------

    def step(self, message: str, *, level: int = 1) -> None:
        if self.verbosity < level:
            return
        self.log.emit("step", message, level=level)

    def done(self, message: str, *, seconds: float | None = None, level: int = 1) -> None:
        if self.verbosity < level:
            return
        self.log.emit("done", message, seconds=seconds, level=level)

    def failed(self, message: str, *, level: int = 1) -> None:
        """A step that errored, with the engine's message and what it means.

        `diagnose.explain` is applied here rather than at the page, and here
        rather than at every call site, because this is the one channel a step
        failure reaches on this path: `cli.step` calls `console.failed` from
        each of its three error branches and nothing else in the web package
        emits this kind. A translation applied in the browser would have to be
        a second copy of the engine's message shapes, in another language, in
        a file that cannot import the module that raised them.

        It appends rather than replaces. The engine's own sentence stays
        whole, so a reader comparing this log against a recorded run still has
        the string the engine produced.
        """
        if self.verbosity < level:
            return
        self.log.emit("failed", diagnose.explain(message), level=level)

    def skipped(self, message: str, *, level: int = 1) -> None:
        if self.verbosity < level:
            return
        self.log.emit("skipped", message, level=level)

    def detail(self, message: str, *, level: int = 2) -> None:
        if self.verbosity < level:
            return
        self.log.emit("detail", message, level=level)

    def warn(self, message: str) -> None:
        """Ungated, matching the base class, and the channel `client.notify` uses.

        `jobs.run_merge` passes this as the client's `notify` (`client.py:352`
        takes the two channels separately). On the command line `notify`
        defaults to `client.to_stderr`, which is right for a terminal and wrong
        for a server: "structured output moved prompt -> json_schema mid-run"
        is a fact about the measurement that is printed whatever the verbosity,
        and on a web deployment stderr is a file nobody has open.
        """
        self.log.emit("warn", message)

    def notice(self, message: str) -> None:
        self.log.emit("notice", message)

    def banner(self, command: str, model: str, endpoint: str, window: str | None = None,
               fidelity: str | None = None, depth: str | None = None,
               retrieval: str | None = None,
               roles: list[dict] | None = None,
               effort: str | None = None) -> None:
        """What this run is. The arguments are kept apart, not formatted into one.

        `Console.banner` renders these into a line and gates the fidelity on
        `-vv`; here they are seven fields, because the page has seven places to
        put them and reassembling a sentence into a table is the parsing this
        module's docstring refuses to do. The gate on the whole banner is kept
        (level 1); the ones on fidelity and depth are not, since they exist to
        keep a terminal line short.

        The depth is sent at every value and not only when it is off its
        default, which is where this differs from the terminal. A browser's
        banner is a line in a panel rather than a line competing for width with
        the run that follows it, and the question it answers -- was invention
        checked on this run -- is one the reader of a finished report should
        never have to infer from an *absent* field.

        `retrieval` joins on those terms and for a sharper version of the same
        reason (548). A run whose model was granted a web tool may put text
        from these documents into a query or a fetch, and at `sourced` that
        grant is made automatically rather than by hand -- so the one thing it
        must not be is invisible. Sent whatever it is, and the page renders the
        empty case as a sentence rather than as a missing row.

        `roles` is this console's alone, and `jobs.banner_roles` says when it is
        sent: when `model` and `endpoint` describe one role and not the run
        (576). The terminal names split roles on lines of their own, which
        `cli.main` prints, so `Console.banner` has no such argument.

        `effort` is the merge's effort level on a command run, read off the
        argv the merge will execute (613): the page's slider chose it, or the
        route's default did, and the header is where a person watching the run
        checks which. `None` for an HTTP run, which has no level. Like `roles`,
        this console's alone: the terminal prints the level in the Decoding
        row of the provenance block, which is where `--effort` has always been
        reported.
        """
        if self.verbosity < 1:
            return
        self.log.emit("banner", f"llossless {command}", command=command,
                      model=model, endpoint=endpoint, window=window,
                      fidelity=fidelity, depth=depth, retrieval=retrieval,
                      roles=roles, effort=effort)

    # -- the detector ----------------------------------------------------

    @property
    def written(self) -> str:
        """Anything an unoverridden `Console` method printed. Expected to be empty."""
        return self._sink.getvalue()


# --------------------------------------------------------------------------
# SSE
# --------------------------------------------------------------------------

# The browser's reconnect delay, in milliseconds, if W4 chooses to state one.
# Not sent by default: the EventSource default is 3 seconds, which is a
# reasonable answer for a run that lasts an hour, and a value invented here
# would be this module making a policy decision about a server it is not.
DEFAULT_RETRY_MS = 3000


def frame(event: Event, *, retry_ms: int | None = None) -> str:
    """One event as an SSE frame, terminated by the blank line that dispatches it.

    `id:` first so that a browser which drops the connection part-way through a
    frame has not yet updated its `Last-Event-ID` -- the id is only committed
    when the frame dispatches, and a frame only dispatches on the blank line.
    Put last, a truncated frame would leave the browser believing it had
    received an event it had not.

    `data:` is a JSON object rather than the bare message, so that a field
    added later (a step's `seconds`, a banner's model) reaches the page without
    changing the frame's shape or needing a second parser. It is one line: see
    the module docstring.
    """
    head = "" if retry_ms is None else f"retry: {int(retry_ms)}\n"
    payload = json.dumps(event.as_dict(), sort_keys=True)
    return f"{head}id: {event.id}\nevent: {event.kind}\ndata: {payload}\n\n"


def frames(events, *, retry_ms: int | None = None) -> str:
    """Several events, concatenated. `retry:` rides on the first frame only."""
    out = []
    for index, event in enumerate(events):
        out.append(frame(event, retry_ms=retry_ms if index == 0 else None))
    return "".join(out)


def parse_last_event_id(value: str | None) -> int:
    """The `Last-Event-ID` header as a number, or 0 for anything unreadable.

    0 means "send everything", which is what a first connection gets and what a
    browser sending a header this function cannot read should also get. The
    alternative -- refusing the request -- would turn a malformed header into a
    page that never loads, and the cost of being wrong in this direction is a
    few hundred events the page already has.

    Negative is clamped for the same reason `since` accepts an id past the end:
    the query is `id > after_id`, and a negative would still answer it
    correctly, but clamping keeps "0 is the whole log" the only spelling of
    that instruction.
    """
    if not value:
        return 0
    try:
        return max(0, int(str(value).strip()))
    except (TypeError, ValueError):
        return 0
