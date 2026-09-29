"""One call to a model, from either the network or a cassette, parsed or failed.

Everything above this file — decompose, verify, merge — asks the same question:
"here is a prompt and a schema, give me an object". Everything below it is
either a socket, a directory of recordings, or a parser. This module is the
join, and it is where the run's honesty is enforced:

- A response that cannot be parsed twice is an error, not a finding. It never
  becomes a MISSING verdict, because "the model failed to answer" and "the
  claim is absent from the merge" are different facts about the world and the
  report has to distinguish them.
- A live call is counted before it is made, so --max-calls cannot be exceeded
  by one.
- Replay never imports the transport module. That is not a stylistic
  preference; it is how "this runs offline" is checked rather than asserted.
"""

from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from . import config, parsing, structured
from .console import Console
from .cassette import (ChainedStore, Store, canonical, guard_sources,
                       key_for, secure_dir, secure_write)
from .config import Settings
from .prompts import Prompt
from .usage import (Searches as SearchTally, Tokens as TokenTally,
                    Turns as TurnTally, answered_by, normalise, served_model)

SCHEMA_ATTEMPTS = 5  # PART C: one normal, then up to four with the validation error quoted

# Total tries at one tier when the endpoint answers 200 with a blank body. It
# is a re-ask of the identical request, not a repair: there is no fault to
# quote back, and the schema attempts above never see it because the emptiness
# is caught by the ladder's shape check. Paced like any other live call, so a
# genuinely mute endpoint costs three intervals per unit and then errors it.
EMPTY_RESPONSE_ATTEMPTS = 3

# Total tries at a response that came back in a repetition loop -- one claim
# restated past `parsing.CLAIM_REPEAT_LIMIT` at one place. One normal attempt,
# one re-ask with the repeat quoted, then the unit of work errors.
#
# Fewer than `SCHEMA_ATTEMPTS` on purpose, and the reason is the cost of the
# generation rather than the odds of the repair. Every other fault in this
# ladder is cheap to have made and cheap to ask again about; a loop is the most
# expensive answer a model can give. The two measured cases were the slowest
# call in their sweep by a factor of 20, and a 34,461-character generation that
# burned 904 seconds on a metered endpoint (`DECISIONS.md` entries 404, 427).
# Five attempts at that is five runaway generations for one document.
#
# It is re-asked once rather than not at all because the re-ask is not the same
# request: `parse_error` appends the repeat, named and counted, and a model told
# what it did has something to act on. What is not on offer is accepting the
# answer. A run that quietly deduplicated 449 claims would report a coverage
# denominator nobody could check, which is the failure this project exists to
# catch.
LOOPING_RESPONSE_ATTEMPTS = 2
TEMPERATURE = 0.0
SEED = 0

# What the wire says about a field the request profile left out entirely.
# Distinct from `None`, which on `Usage.wire_temperature` already means "this
# run made no live call, so there is no wire to read" -- and the two must not
# collapse, because the report's fallback for the second is to print the module
# constant. A run that sent no `temperature` and a run that sent `0.0` would
# then read identically, and the first would be claiming a decoding condition
# it did not set. A string rather than another sentinel object because it is
# printed and serialised: `"temperature": "not sent"` in a JSON provenance
# block is unambiguous to a reader and cannot be mistaken for a number.
NOT_SENT = "not sent"


class DryRun(Exception):
    """Raised instead of calling. The call has been planned and counted.

    An exception rather than a sentinel return value because there is no honest
    object to return: the model was not asked, so there is no answer, and
    anything this function could hand back would be something it made up.
    """


class CallBudgetExceeded(RuntimeError):
    """--max-calls would be exceeded. Stops the run before the next call."""


class ConcurrentCall(RuntimeError):
    """Two threads were inside `Client.complete` on one client at once.

    A `Client` is single-threaded and always has been. This class is here
    because that was a property nothing asserted, and because the way it fails
    is silent: the shared state a second caller overwrites is not the answer,
    it is the *bookkeeping about* the answer, so both calls return usable
    payloads and the run finishes looking exactly like a correct one.

    What overlaps. `_fetch` writes `self._pending_call` before the request goes
    out and `_record_usage` reads it after the response comes back, so the slot
    is held for the whole call -- 16 to 127 seconds on the runs this was
    measured against. Two overlapping calls therefore do not race on a window,
    they collide by construction: the second caller's identity is what the
    first caller's ledger row is written from. Measured on this class's
    must-fire probe, a `decompose` and a `verify` call issued 0.25 s apart
    filed two rows both reading `role: verify` with one `request_sha256` between
    them, and the `decompose` call vanished from the ledger entirely while
    `usage.calls_by_role` -- incremented at the call site rather than from the
    slot -- still counted it. A ledger that disagrees with the run it is the
    record of cannot be reconciled against a bill, which is the only thing it
    is for.

    The slot is the sharpest case and not the only one. `last_key`,
    `last_tier`, `last_gap`, `last_cached`, `last_reasoned` and
    `last_thinking` are one-slot journal fields a runner reads after each call
    (`tests/run_merge.py` writes seven of them per unit); `usage.calls`,
    `usage.tokens`, `usage.searches` and `usage.turns` are read-modify-write
    counters; `self.tier` is the ladder's latch; `_last_call_ended` is what
    `--min-interval` paces against; `_dump_seq` names failure dumps. None of
    them is protected and none of them needs to be while this holds.

    Raised rather than serialised behind a lock, deliberately. A lock would
    make an overlapping call correct and slow, which is the opposite of what
    anyone reaching for one wants, and it would hide the fact that the caller's
    pipeline is asking for something this client does not offer.
    `internal/docs/parallelism.md` has the dependency graph, the measured win
    and the list of what a parallel `Client` would have to fix first.
    """


class PinnedTierViolated(RuntimeError):
    """A call resolved to a tier other than the pinned one. Fatal, per call.

    Pinning exists so that "how strongly was the output constrained" is a
    constant of the run rather than something each call negotiates. If one call
    answers on a different rung, the run is two measurements wearing one label,
    and the report's single `mode` field - written once, at the end - cannot
    show it. So the check is here, on every row, rather than on the header.

    It is fatal rather than a warning because the alternative is a number that
    is quietly an average over two tiers. A run that cannot be what it says it
    is should stop, the same way the thinking contract stops it.
    """


class SchemaFailure(RuntimeError):
    """Two attempts, still unusable. The unit of work errors; the run continues."""

    def __init__(self, role: str, detail: str, dump: Path | None,
                 *, why: str | None = None,
                 payload: dict | None = None,
                 defects: tuple[str, ...] = (),
                 truncations: tuple[parsing.Truncation, ...] = ()) -> None:
        # `why` replaces the sentence, not the class. A failure that stopped at
        # the first attempt on purpose cannot be announced as "after 2
        # attempts", and callers above -- `cli.step`, the report, the exit code
        # -- treat it as exactly the same outcome, because it is one: this unit
        # of work has no usable answer.
        super().__init__(
            (why or f"{role}: model did not return a usable response after "
                    f"{SCHEMA_ATTEMPTS} attempts: {detail}")
            + (f"\n  raw response written to {dump}" if dump else "")
        )
        self.role = role
        self.detail = detail
        self.dump = dump
        # The last attempt's object, and only where that attempt cleared the
        # schema walk and failed the semantic check alone: there is nothing to
        # hand on from a response that was not JSON, and a schema fault is a
        # fault in the shape the caller would have to read. The class still
        # means what it says -- this unit of work has no usable answer -- and
        # nothing here changes an exit code. It is carried so a caller that can
        # tell one bad record from a bad response has the evidence to do it
        # (`verify.salvage`, `DECISIONS.md` entry 194), on the same principle as
        # Brief AQ v2 item 1: what the run already paid for is not thrown away.
        self.payload = payload
        self.defects = defects
        self.truncations = truncations


@dataclass
class Usage:
    """What the run spent and what it got away with. All of this reaches the report."""

    calls: int = 0
    cache_hits: int = 0
    replayed: int = 0
    repairs: int = 0  # attempt-2 successes
    # Endpoint loads this run had to ask for. Counted apart from `calls`
    # deliberately: a warm-up asks the endpoint for nothing but the model's
    # presence, is not keyed into a cassette and is not charged to --max-calls,
    # so folding it into the call count would put a request in the figure the
    # report calls "live calls" that no prompt and no cassette corresponds to.
    warmups: int = 0
    errors: int = 0  # units of work that failed both attempts
    # Of `errors`, the calls a caller went on to grade in part. Counted rather
    # than subtracted from `errors`, because both readings are true and needed:
    # the endpoint was asked twice and gave nothing acceptable either time, and
    # the run still has verdicts out of it. Written by the caller that did the
    # salvaging, not here -- `complete` raises the same failure whether or not
    # anyone can use what is attached to it. Pass C, `DECISIONS.md` entry 194.
    salvaged: int = 0
    # The legacy pair, kept because a dozen callers subtract one reading from
    # another to attribute spend to a unit of work. They mirror
    # `tokens.input` and `tokens.output` and are written in the same place, at
    # `Client._record_usage`; `test_client` asserts they agree, so the mirror
    # cannot drift into being a second answer.
    prompt_tokens: int = 0
    completion_tokens: int = 0
    # The full picture, normalised across vendors, with unmeasured calls
    # counted rather than folded into zero. See usage.Tokens and DECISIONS 138.
    tokens: TokenTally = field(default_factory=TokenTally)
    # Whether the model went and looked anything up, read off the response
    # rather than asked for (537). Three states -- searched, not-searched,
    # unmeasured -- and the third is why this is a tally and not a count: an
    # endpoint that never reports is not an endpoint that reported zero. This
    # says nothing about *this* process, which opens no socket for any
    # purpose; a model's own retrieval happens on the serving side, which is
    # exactly why a counter it wrote down is the only honest way to know.
    searches: SearchTally = field(default_factory=SearchTally)
    # The same question through the instrument that can see this backend (548).
    # `searches` reads `server_tool_use`, which counts Anthropic's server-side
    # web tools and is structurally blind to a CLI's local `WebFetch` -- a call
    # that demonstrably fetched reported zero. A tool call costs a turn, so
    # `num_turns` sees it. Two tallies rather than one, because they are two
    # measurements and a run can have one and not the other.
    turns: TurnTally = field(default_factory=TurnTally)
    seconds: float = 0.0
    planned_calls: int = 0
    planned_input_tokens: int = 0
    prompts: dict[str, str] = field(default_factory=dict)  # path -> sha256
    # Roles whose answers carried a reasoning block after the call asked for
    # thinking off. Not a count: the report names the roles, because "verify
    # reasoned anyway" and "merge reasoned anyway" are different runs. Empty on
    # every run where the endpoint did as it was told, which is every run in
    # the recorded corpus.
    thinking_ignored: set[str] = field(default_factory=set)
    # One row per response body this run charged, in the order they were
    # charged. Written at `Client._record_usage` beside the totals above --
    # entry 138's single write point -- so a run cannot carry a ledger that
    # disagrees with its own totals. Entry 168.
    ledger: list[dict] = field(default_factory=list)
    # Live calls this run made and did not charge to the ledger (681): a blank
    # answer re-asked, a call the platform failed, a cancel. Kept apart because
    # `ledger` is compared verbatim against a replay, which never meets them.
    # Written at `Client._discard` only; `provenance` reads both lists.
    discarded: list[dict] = field(default_factory=list)
    # Which mechanism guarded each role's calls against overrunning the
    # context window, and there are three:
    #
    #   "preflight"          `served_window` measured one against the endpoint.
    #   "stated: <figure>"   the operator declared one and no probe confirmed
    #                        it. The guard ran, against their number.
    #   "post-hoc: <reason>" the endpoint could not say, nothing preflighted,
    #                        and the run fell back to a per-draw truncation
    #                        check instead (Brief AL item 2).
    #
    # Three strings and not two, because a run guarded against a number an
    # operator typed and a run guarded against a number a server confirmed are
    # different claims, and the Provenance block has to be able to print the
    # difference. A role absent from this dict never asked -- a replay or dry
    # run, which sends nothing and needs no guard of any kind.
    window_mechanism: dict[str, str] = field(default_factory=dict)
    # Per role, whether the last live call's own wire body carried thinking
    # on or off -- read from the request that was actually sent, not from
    # `Settings.thinking`. Absent for a role with no live call: a replayed or
    # cached answer sent nothing, so there is no wire to read.
    wire_thinking: dict[str, bool] = field(default_factory=dict)
    # Live calls per role. `calls` is the run's total and cannot answer the one
    # question a per-role endpoint setup has to ask: did *this* box answer for
    # *this* role? Entry 423. Counted beside `calls` at the single place a live
    # call is charged, so the two cannot disagree; a role absent here made no
    # live call, which a replay, a cache hit and a dry run all look like and
    # which the artefacts a role leaves cannot tell apart.
    calls_by_role: dict[str, int] = field(default_factory=dict)
    # The last live call's own `temperature`, read from its request body --
    # not from `TEMPERATURE`. `None` when this run made no live call, which
    # `Provenance` treats the same way it treats a replay: report the constant,
    # because there is no wire to report instead. `NOT_SENT` when a live call
    # was made and carried no such field, which is a third state and not the
    # second one.
    wire_temperature: float | str | None = None
    # The same for `seed`, and added for the same reason one call later than
    # `temperature` was: a request profile can drop the field (Anthropic's
    # surface has no `seed`), and a provenance block printing the constant over
    # a run that sent nothing would be reporting a decoding condition nobody
    # set. `None` means no live call; `NOT_SENT` means a live call that omitted
    # it.
    wire_seed: int | str | None = None


@dataclass(frozen=True)
class Completion:
    """What `Client.complete` returns: the payload, and what it cost to get one.

    A dataclass rather than the bare payload so `truncations` has somewhere to
    live that is not a reserved key inside the payload itself -- the model's
    JSON and the parser's own report about that JSON stay two different
    objects. Empty `truncations` on the common case, a response that needed no
    capping. `DECISIONS.md` entry 190.
    """

    payload: dict
    truncations: tuple[parsing.Truncation, ...] = ()


def recorded_envelope(raw: str) -> dict | None:
    """The response envelope inside a recording, for its usage block only.

    Tolerant on purpose. A cassette that does not parse is a real problem and
    it is not this function's problem -- the parser downstream reports it with
    the context to act on, and a token count is not worth raising a second,
    worse-placed error about. An unparseable recording simply counts as one
    call whose usage is unknown, which is exactly what it is.
    """
    try:
        envelope = json.loads(raw)
    except (TypeError, ValueError):
        return None
    return envelope if isinstance(envelope, dict) else None


def to_stderr(message: str) -> None:
    """Where the library says something. stdout belongs to the report."""
    print(f"llossless: {message}", file=sys.stderr, flush=True)


def _replay_store(directory: Path | None) -> Store | ChainedStore | None:
    """The directory named by `--replay`/`--offline`, plus its `local/` overlay.

    A `local/` subdirectory is never created by this function and never
    written to by a live run -- only `--record` writes cassettes, and it
    writes wherever it is pointed, not here. This only changes what a replay
    can *find*: a directory recorded against one endpoint, extended by a
    cassette recorded honestly against another, read as one corpus. See
    `ChainedStore`.
    """
    if directory is None:
        return None
    primary = Store(directory)
    overlay_dir = directory / "local"
    overlay = Store(overlay_dir) if overlay_dir.is_dir() else None
    return ChainedStore(primary, overlay) if overlay is not None else primary


class Client:
    def __init__(self, settings: Settings, *, notify=to_stderr, console=None) -> None:
        """`console` is the operator's running commentary; `notify` is a warning.

        Two channels rather than one because they answer to different people. A
        tier that moved mid-run is a fact about the measurement and is printed
        whatever the verbosity; "waiting for the endpoint" is a fact about the
        wait and is printed only if someone asked for it. The default console is
        silent at every level, so a library caller who passes neither gets the
        behaviour this class had before it grew the argument.
        """
        self.settings = settings
        self.usage = Usage()
        self.notify = notify
        # One notice per model, not one per call. A 13-fixture sweep against a
        # model that always reasons would otherwise print the same sentence a
        # few hundred times and bury everything else on the stream.
        self._reasoning_noticed: set[str] = set()
        self.console = Console() if console is None else console
        self.capabilities = structured.Capabilities(settings.cache_dir / "capabilities.json")
        self.tier: str | None = settings.structured if settings.pinned else None
        self.tier_source = "pinned" if settings.pinned else "probed"
        self._endpoint_identity: str | None = None

        self._replay = _replay_store(settings.replay_dir)
        self._record = Store(settings.record_dir) if settings.record_dir else None
        self._cache = Store(settings.cache_dir / "responses") if settings.use_cache else None

        # The revision this run is made under, stamped once at init and never
        # re-read per call (I7): a sweep is one process, and re-reading per
        # call would let a corpus straddle an edit while reporting each half
        # honestly, which is the outcome the guard below exists to prevent
        # rather than to document. Read regardless of whether this run
        # records -- it used to be read only then, which left every
        # `--no-cache` benchmark run's provenance stamped from `git_commit()`
        # alone (HEAD, never `-dirty`) rather than from this. `Provenance`
        # reads it off this client rather than calling `git_commit()` itself,
        # so a report and the guard above describe the same tree.
        # Imported here, not at module scope: provenance builds report headers
        # out of a Client, so the dependency only runs one way at import time.
        from .provenance import source_state

        self._source = source_state()
        if self._record is not None:
            # --mixed-sources waives this entirely, which is what it always
            # bought once the endpoint half of the guard was removed
            # (DECISIONS 405): the claim that an edit provably cannot reach
            # the model.
            guard_sources(
                self._record,
                None if settings.allow_mixed_sources else self._source,
            )

        # Whether to send `reasoning_effort` on thinking-off calls. Constant for
        # the life of the client, and deliberately so: it used to be cleared on
        # the first rejection, which turned one refused field into a whole corpus
        # recorded under the wrong condition. A rejection now raises
        # `structured.ThinkingNotHonoured` and the run stops. The attribute stays
        # because `build_body` takes it, and because a caller that genuinely
        # wants a thinking-on run gets that by asking for it, not by having the
        # endpoint decide.
        self._reasoning_effort = True
        self._last_call_ended = 0.0
        # Set by `_fetch` before any path answers; read by
        # `_record_usage`. Here so the attribute exists on a Client that
        # never reaches `_fetch`.
        self._pending_call: dict | None = None

        # The field order the replayed recording that answered the last
        # `_fetch` was read under when it was made, or None when the answer
        # came from the wire or the cache. `_reading_order` turns it into the
        # order this run reads the answer under; `_orders_read` keeps every
        # such order a replay used, for `resolved_field_order` (DECISIONS 583).
        self._recorded_order: str | None = None
        self._orders_read: set[str] = set()

        # Served context window per model, filled by `served_window` on first
        # use. Keyed by model and not by role because two roles pointed at one
        # model share a runner and therefore share its allocation.
        # (model, endpoint) -> Window. Both halves matter; see `served_window`.
        self._windows: dict[tuple[str, str], object] = {}

        # What the last call actually did, for a runner's journal. Where the
        # raw output is filed, at which tier, and how long the endpoint was
        # left alone before the request went out. None where the question does
        # not apply: a replayed or cached answer had no gap because it made no
        # call. A journal that recomputed the key from the outside would be a
        # second implementation of key_for, which is the one thing that must
        # not have two.
        self.last_key: str | None = None
        self.last_tier: str | None = None
        self.last_gap: float | None = None

        # Whether the last answer came out of the cache rather than the wire.
        # A cache hit costs no time and no tokens, so a timing figure that
        # averages one in is not a latency at all; a journal that cannot tell
        # them apart reports a fast endpoint whenever a document repeats.
        self.last_cached = False

        # Whether the last answer carried a reasoning block. Recorded because
        # `completion_tokens` is the wrong instrument for the question, though
        # not for the reason this comment used to give. It claimed usage counted
        # only `content`; measured on qwen3.8:27b, one question answered both
        # ways billed 50 completion tokens with thinking off and 168 with it on,
        # so the reasoning is charged -- it simply arrives in a `reasoning` field
        # beside `content` rather than inside it. A token count is still only
        # evidence about length, and a long thinking-off answer and a short
        # thinking-on one are not distinguishable by one. This reads the
        # response instead, and it survives replay because the whole body is
        # what a cassette stores.
        self.last_reasoned = False

        # Whether the last call was allowed to think. Recorded rather than
        # re-derived because the rule below has two inputs -- `settings.thinks`
        # and a per-call override -- and a runner that recomputed it from the
        # settings alone would report the default over an arm that ran with
        # something else. It is part of the cassette key, so it is also the
        # value a replay of that call would have to match.
        self.last_thinking: bool | None = None

        # Which repeat of an otherwise identical call this is. Part of the
        # cassette key and nothing else: it never reaches the request body, so
        # the endpoint cannot tell samples apart and is not meant to. A runner
        # that measures stability turns this dial between passes; everything
        # else leaves it at 0 and behaves exactly as it did before it existed.
        self.sample = self.settings.sample

        # A dump filename disambiguator. Not `usage.errors`: that counts
        # draws that exhaust every attempt, so a draw that repairs itself on
        # attempt 2 would leave attempt 1's response filed under no counter
        # at all and a second draw's attempt 1 would collide with the first's
        # on both timestamp and role. This counts dumps, one per attempt that
        # failed to parse, whatever the draw's eventual outcome.
        self._dump_seq = 0
        # Made on first use and never in a constructor: a run that dumps
        # nothing must not leave a directory behind to prove it ran.
        self._scratch: Path | None = None

        # Who is inside `complete` right now, by thread name, and the lock that
        # makes reading and writing that one decision rather than two. See
        # `ConcurrentCall` for what a second caller would overwrite. The lock
        # guards the *name*, not the call: it is held for two attribute
        # accesses and never across a request, so nothing here can serialise a
        # model call or add measurable time to one.
        self._caller_lock = threading.Lock()
        self._caller: str | None = None

    # -- public -----------------------------------------------------------

    def thinking_for(self, role: str, override: bool | None) -> bool:
        """The one place the rule lives: an override if there is one, else the role's setting.

        A method rather than an expression inside `complete` because two other
        readers need the same answer and must not each grow their own copy of
        it: `_fetch` puts the value in the cassette key, and a runner writing a
        per-role record of what an arm ran with has to name the same value the
        request carried.
        """
        return self.settings.thinks(role) if override is None else override

    def complete(
        self,
        *,
        role: str,
        prompt: Prompt,
        messages: list[dict],
        schema: dict,
        schema_name: str,
        semantic=None,
        max_tokens: int | None = None,
        thinking: bool | None = None,
        refuse_at_ceiling: bool = False,
    ) -> Completion:
        """Ask for one object. Raises SchemaFailure, DryRun, or a fatal error.

        `thinking` overrides `settings.thinks(role)` for this call only. It
        exists because the merge pass is run both ways in one process
        deliberately: `_pace()` and `_last_call_ended` are per-Client, so two
        conditions as two Clients would halve the effective interval between
        live calls, which is the one thing standing between a multi-hour sweep
        and a GPU that powers the machine off. One client, one pacer, one usage
        counter, one source revision. The flag is already in the cassette key,
        so the two conditions record separately without any further help.

        **One unit of work at a time on one client, and a second caller is
        refused rather than queued.** The paragraph above has said since M5
        that a client is one pacer and one usage counter; nothing asserted it,
        and what the assertion buys is that the way it fails stops being
        silent. See `ConcurrentCall` for the measurement: two overlapping calls
        file two ledger rows for one of them. The whole unit is held, not each
        attempt, because the repair loop's counters (`usage.repairs`,
        `usage.errors`) are per unit and a second unit interleaving between
        attempt 1 and attempt 2 would charge its outcome to this one.

        Two clients on two threads are untouched and remain the supported way
        to run work in parallel -- that is what `web.jobs.JobStore` does at
        `workers > 1`, and each of its jobs builds its own client, in
        `web.jobs._run_merge`.
        """
        caller = threading.current_thread().name
        with self._caller_lock:
            if self._caller is not None:
                raise ConcurrentCall(
                    f"{caller!r} asked this client for a {role!r} call while "
                    f"{self._caller!r} was still inside one. A Client is "
                    f"single-threaded: the ledger row for a call is written "
                    f"from a one-slot field held for the whole request, so "
                    f"two overlapping calls file one of them twice and lose "
                    f"the other. Give each thread its own Client, or run the "
                    f"calls in sequence. internal/docs/parallelism.md has the "
                    f"dependency graph and what a parallel Client would have "
                    f"to fix first."
                )
            self._caller = caller
        try:
            return self._complete(
                role=role, prompt=prompt, messages=messages, schema=schema,
                schema_name=schema_name, semantic=semantic,
                max_tokens=max_tokens, thinking=thinking,
                refuse_at_ceiling=refuse_at_ceiling,
            )
        finally:
            # Released on every path, including `DryRun` and `SchemaFailure`.
            # `cli.step` catches both and runs the next unit, so a guard left
            # held by a failed step would turn one bad unit into every later
            # one -- which is the failure mode `step` exists to prevent.
            with self._caller_lock:
                self._caller = None

    def _complete(
        self,
        *,
        role: str,
        prompt: Prompt,
        messages: list[dict],
        schema: dict,
        schema_name: str,
        semantic=None,
        max_tokens: int | None = None,
        thinking: bool | None = None,
        refuse_at_ceiling: bool = False,
    ) -> Completion:
        """`complete`'s body, with the single-caller claim already made.

        Split out so the guard is a `try/finally` around one call rather than
        around ninety lines. Nothing in `src/` calls this directly -- a caller
        that did would be asking for the mechanics without the claim, and the
        claim is the point. The one caller that does is
        `test_the_defect_the_guard_prevents_is_still_there_underneath`, which
        takes the claim off on purpose to show what it is standing in front of.
        """
        model = self.settings.model_for(role)
        thinking = self.thinking_for(role, thinking)
        self.usage.prompts[str(prompt.path)] = prompt.sha256

        if self.settings.dry_run:
            self.usage.planned_calls += 1
            self.usage.planned_input_tokens += _estimate_tokens(messages)
            raise DryRun(f"{role}: 1 call planned against {model}")

        attempt_messages = list(messages)
        last: parsing.ParseError | None = None
        raw = ""
        tier = self.resolved_tier()
        order_failed = False
        loop_failed = False
        final: tuple[dict, list[str], list[parsing.Truncation]] | None = None

        for attempt in range(1, SCHEMA_ATTEMPTS + 1):
            # Reset per attempt, not once above: a first attempt that parsed
            # and a second that did not must not report the first attempt's
            # object as the last word. Same hazard `_dump_discard` closed for
            # `dump` (entry 184 item 2).
            final = None
            raw, tier = self._fetch(
                role=role,
                model=model,
                prompt_sha256=prompt.sha256,
                messages=attempt_messages,
                schema=schema,
                schema_name=schema_name,
                max_tokens=max_tokens,
                thinking=thinking,
                attempt=attempt,
            )
            # The row `_fetch` just filed for this answer, on every path (681):
            # what became of it is written onto it below, as `outcome`.
            filed = self.usage.ledger[-1]
            order = self._reading_order()
            try:
                content = structured.read_content(tier, json.loads(raw))
                payload, defects, truncations = parsing.parse(
                    content, schema, semantic, field_order=order)
                if defects:
                    # `parse` runs the semantic check only on a payload the
                    # schema walk already passed, so this list belongs to one
                    # stage or the other and never both. Only the semantic one
                    # can be re-derived downstream from the payload alone, so
                    # the stage is settled here, with `parse`'s own rule about
                    # which faults `--field-order any` forgives.
                    if semantic is not None and not parsing.forgiven(
                            parsing.validate(payload, schema), order):
                        final = (payload, defects, list(truncations))
                    raise parsing.parse_error(schema, defects)
            except (parsing.ParseError, structured.TierUnsupported, json.JSONDecodeError) as exc:
                last = exc if isinstance(exc, parsing.ParseError) else parsing.ParseError(str(exc))
                dump = self._dump_attempt(role, attempt, raw)
                if refuse_at_ceiling:
                    # DECISIONS 668, extended at 680 (the cosmetic fix at the
                    # old `client.py:643`). An answer that stopped on its
                    # ceiling and does not parse is a prefix, and the same
                    # request at the same ceiling stops at the same place, so
                    # it is refused here, on the first attempt, as the length
                    # refusal it is (`window.Truncated`), rather than repaired
                    # `SCHEMA_ATTEMPTS` times at the full ceiling or handed
                    # to salvage as a partial answer. Opt-in: the verify role
                    # asks for it; decompose and merge keep their repair path.
                    #
                    # No longer gated on `max_tokens is not None`: a frontier
                    # profile sends no ceiling of its own (B1), so a response
                    # the endpoint cut on *its* own limit used to fall through
                    # to the ordinary schema ladder and be asked again
                    # `SCHEMA_ATTEMPTS` times at a request that cannot answer
                    # differently -- five requests where the 27B, which does
                    # send a ceiling, pays one. `ceiling_cut` reads
                    # `finish_reason` first and needs no ceiling for that
                    # signature; the cell is excluded from scoring either way
                    # (678), so this is spend saved, not a figure changed.
                    cut = ceiling_cut(raw, self.usage.ledger[-1] if self.usage.ledger else {},
                                      max_tokens)
                    if cut is not None:
                        from . import window as window_module
                        filed["outcome"] = OUTCOME_CEILING
                        self.usage.errors += 1
                        ceiling_said = (
                            f"its {max_tokens}-token output ceiling ({cut})"
                            if max_tokens is not None else
                            f"the endpoint's own length limit ({cut}), though "
                            f"this tool sent no ceiling of its own"
                        )
                        raise window_module.Truncated(
                            f"{role}: {model} stopped on {ceiling_said} and what "
                            f"came back does not parse: {last}. That is a "
                            f"runaway cut short, not an answer, and it was not "
                            f"asked again: the same request at the same ceiling "
                            f"stops at the same place. Nothing from it was "
                            f"graded.") from exc
                if last.order_only:
                    # Everything the contract asks for, present and valid, in
                    # the wrong sequence. The repair loop exists for a model
                    # that got something wrong and can be told what; this model
                    # got nothing wrong. Key order is a property of its
                    # serializer, the request is unchanged at temperature 0, and
                    # the second attempt returns the same order for the same
                    # money -- measured 2026-08-28, deepseek-r1:70b, two
                    # identical answers at 104.7 s and 105.0 s, after which a
                    # usable merge was thrown away. Stop on the first one.
                    filed["outcome"] = OUTCOME_FAILED
                    order_failed = True
                    break
                if last.looping and attempt >= LOOPING_RESPONSE_ATTEMPTS:
                    # The model is repeating itself and has already been told
                    # so once. Stop here rather than at SCHEMA_ATTEMPTS: the
                    # remaining attempts are the most expensive generations in
                    # the ladder and the evidence that they help is nil.
                    filed["outcome"] = OUTCOME_FAILED
                    loop_failed = True
                    break
                filed["outcome"] = (OUTCOME_REPAIR if attempt < SCHEMA_ATTEMPTS
                                    else OUTCOME_FAILED)
                if attempt < SCHEMA_ATTEMPTS:
                    # Quote the specific fault and the schema. Nothing else: not
                    # a reworded prompt, not a higher temperature. If the model
                    # cannot fix a named error at temperature 0, nudging it into
                    # randomness is not a fix, it is a different answer.
                    attempt_messages = attempt_messages + [
                        {"role": "user", "content": last.feedback}
                    ]
                    self.console.detail(
                        f"{role}: the answer did not fit the schema, "
                        f"asking again ({attempt + 1} of "
                        f"{LOOPING_RESPONSE_ATTEMPTS if last.looping else SCHEMA_ATTEMPTS})")
                continue
            filed["outcome"] = OUTCOME_ANSWER
            if attempt > 1:
                self.usage.repairs += 1
            return Completion(payload, tuple(truncations))

        self.usage.errors += 1
        assert last is not None
        raise SchemaFailure(
            role, str(last), dump,
            why=(
                f"{role}: {model} gave every field this response needs, valid, "
                f"and in the wrong order -- {last}. It was not asked again. "
                f"Field order is a property of how a model serializes JSON, so "
                f"a second attempt spends another full generation and returns "
                f"the same order; and the {tier} tier did not constrain it "
                f"either, because declaring an order in a schema does not make "
                f"an endpoint enforce one. Re-run with --field-order any to "
                f"accept a complete, valid answer whose keys arrived in another "
                f"order, or use a model that emits them in the order the schema "
                f"declares."
            ) if order_failed else (
                f"{role}: {model} answered in a repetition loop and did it "
                f"again when it was told -- {last}. It was asked "
                f"{LOOPING_RESPONSE_ATTEMPTS} times and not a third, because a "
                f"looping generation is the most expensive answer this tool "
                f"asks for and nothing about a longer prompt makes a model stop "
                f"repeating itself. Nothing was deduplicated: a claim list that "
                f"is mostly one claim is not a document with many facts, and "
                f"discarding the repeats would put a number in the coverage "
                f"table that nobody could check. Re-run against a model that "
                f"terminates, or shorten the document."
            ) if loop_failed else None,
            payload=final[0] if final else None,
            defects=tuple(str(d) for d in final[1]) if final else (),
            truncations=tuple(final[2]) if final else (),
        )

    def resolved_tier(self) -> str:
        """What the report should say the run ran at.

        `last_tier` covers the run that answered entirely from cache and so
        never resolved anything: the tier its answers were filed at is what
        happened, and reporting `auto` there would be less true, not more.
        """
        return self.tier or self.last_tier or self.settings.structured

    def _reading_order(self) -> str:
        """The field order the answer `_fetch` just returned is read under.

        The run's own setting, except for a replayed answer, which is read
        under `config.replay_field_order`: never more strictly than the
        recording run read it. A live answer and a cache hit are read under the
        setting and nothing else, so a live run behaves as it always has.
        """
        if self._recorded_order is None:
            return self.settings.field_order
        order = config.replay_field_order(self._recorded_order,
                                          self.settings.field_order)
        self._orders_read.add(order)
        return order

    def resolved_field_order(self) -> str:
        """What the report should say responses were read under.

        The setting, unless a replayed answer was read more permissively
        because its recording was: a replay of an `any` corpus with no flag
        reads every answer under `any`, and a report that said `schema` would
        describe a run that did not happen -- and would differ from the report
        of the run it reproduces. The most permissive order any answer was
        read under, because that is the weakest contract this run applied.
        """
        return max((self.settings.field_order, *self._orders_read),
                   key=config.FIELD_ORDERS.index)

    @property
    def sends_nothing(self) -> bool:
        """Replay or dry run: no request leaves this process.

        `served_window` returns None for three unrelated reasons and a caller
        that treats them alike is wrong twice. Replay and dry run send nothing
        and need no guard; an endpoint that cannot answer `/api/ps` is a live
        call about to go out unguarded, which is the one worth refusing.
        """
        return self._replay is not None or self.settings.dry_run

    def served_window(self, role: str):
        """The context window this endpoint has allocated for `role`'s model.

        Asked once per client and per role, then remembered: it is a property of
        a running server, and a sweep that re-asked per call would put an extra
        request in front of every merge to learn something that cannot change
        without the server restarting.

        `None` means the question does not arise, and there are exactly two ways
        for that to happen. A replay run sends nothing, so no window constrains
        it -- and asking anyway would open a socket on the one path that is
        supposed to prove it never does. A dry run has the same property for the
        same reason. Every other answer is a `window.Window` carrying where the
        number came from, because a caller that refuses a run has to be able to
        say whether it refused on a measurement or on a report.

        `window.WindowUnknown` is not caught here. An endpoint that will not say
        what it is serving is a fact about the run, and the alternative -- a
        default -- is precisely the hard-coded number task 41 exists to remove.

        **A stated window is answered first, and it is not that default.**
        `Settings.window` is `None` unless an operator named a figure, and a
        figure an operator named is not a number this file chose; the refusal
        above is unchanged for everyone who named none. It is answered before
        `/api/ps` is asked because the endpoints it exists for -- a hosted
        vendor -- do not have that route, and it skips `window.measured`
        outright: confirming a declared figure costs a calibration generation
        plus a probe at 97% of it, per model per run, and on a metered 200k
        window that is an expensive preflight for a number nobody disputed.
        What that buys is recorded rather than assumed: the mechanism reads
        `stated`, never `preflight`, so a reader can tell a run guarded against
        an operator's number from one guarded against the server's.

        `window.WindowUnmeasurable` *is* caught here, and is a different fact:
        the endpoint does not expose `/api/ps` at all, which no load request or
        retry changes. Brief AL item 1. Returning `None` in that case is not a
        default either -- no window value is invented and none is declared --
        it is the same "nothing constrains this" answer replay and dry run
        already return, for a third reason. `Client.usage.window_mechanism`
        records which of the two happened, because a caller has to be able to
        tell a run that asked and got nothing back apart from a run that never
        asked.

        **What the endpoint reports is a starting point, not the answer.**
        `/api/ps` gives what the runner allocated, and nothing in the response
        says how the runner divides it, so it is an upper bound on what one
        request gets. `needed <= reported` therefore establishes nothing when it
        holds: a guard that passed on it would put a passing check in front of
        the failure it was built to catch, since a prompt that overruns the
        window is trimmed and answered rather than refused. So the report is
        confirmed by probe -- a prompt of that size sent and the endpoint's own
        `prompt_tokens` read back -- before it is used, and only a measured
        window reaches `window.guard`. On this project's pod both models
        confirmed their report on 2026-08-17, at 40,960 and 65,536;
        `DECISIONS.md` entry 18 has the measurement, and the wrong one that
        preceded it.
        """
        from . import window

        if self._replay is not None or self.settings.dry_run:
            return None
        model = self.settings.model_for(role)
        # Per-role since entry 421: two endpoints serve two windows, and the
        # run-wide figure is the fallback rather than the answer.
        stated_window = self.settings.window_for(role)
        if stated_window is not None:
            # Named by `settings.window_declared_by` rather than fixed here
            # (605): a shell operator's `--window` / `LLOSSLESS_WINDOW` is the
            # default, and `web.jobs.web_settings` replaces it with the page's
            # own field when the request is what stated the figure -- one
            # attribution, read off the object that carries it, not guessed
            # from which process is running.
            served = window.stated(stated_window, model,
                                   declared_by=self.settings.window_declared_by)
            # Assigned, not `setdefault`. The reason used to be that one
            # stated figure covered the whole run, so no earlier answer for
            # this role could exist to disagree with; entry 421 made the
            # figure per-role and that reason went away. The assignment
            # stands on a better one: this is the figure the operator
            # declared for *this* role, so it is the answer, and a stale
            # entry left from an earlier call is exactly what must not win.
            # And `window.mechanism` rather than a string composed here --
            # how the call was guarded is derived from the window that
            # guarded it, so the two cannot come apart.
            self.usage.window_mechanism[role] = window.mechanism(served)
            return served
        # Keyed by model *and* endpoint since entry 421. A model id is not a
        # deployment: the same `qwen3:8b` served by a rented 24 GB card and by
        # the operator's own box are two windows, and keying on the id alone
        # would hand the second role the first one's measurement. The probe
        # costs a large generation, so this cache is worth keeping -- it just
        # has to be keyed on what actually determines the answer.
        served_by = (model, self.settings.base_url_for(role))
        if served_by not in self._windows:
            # One probe per model per endpoint per client, for the reason
            # above. It costs one large generation and the run it protects
            # costs hundreds.
            try:
                upper = self._reported(model, role=role)
            except window.WindowUnmeasurable as exc:
                self.usage.window_mechanism[role] = f"post-hoc: {exc}"
                return None
            self._warn_if_not_on_the_gpu(upper)
            self._windows[served_by] = window.measured(
                self.settings, model, at_most=upper.tokens, role=role)
        self.usage.window_mechanism.setdefault(
            role, window.mechanism(self._windows[served_by]))
        return self._windows[served_by]

    def _warn_if_not_on_the_gpu(self, served) -> None:
        """Say so, once per model, when the runner did not put it on the GPU.

        Not an error and not a refusal: a CPU load answers, and an operator who
        meant it -- no GPU on the box, a small model, a smoke test -- is not
        doing anything wrong. It is said because the failure it precedes is
        unreadable. A 27B model on the CPU takes longer than any proxy's read
        timeout, and what reaches the terminal is `HTTP 524` and a Cloudflare
        body about a slow origin, which points at the network. The cause is two
        layers down in a container that lost its GPU and started anyway, and
        nothing in the run says so. This is the one place the tool has the
        figures, and it has them before the first long call rather than after
        it.
        """
        if not served.placement or served.placement == "GPU":
            return
        where = (
            f"is loaded on the CPU on {self.settings.endpoint_name}, not on a GPU"
            if served.placement == "CPU" else
            f"is only {served.placement} on {self.settings.endpoint_name}; the rest of it "
            f"is on the CPU"
        )
        self.console.warn(
            f"{served.model} {where}. Generation will be many times slower and "
            f"long calls may time out before they finish. If that is not "
            f"deliberate, the server has no usable GPU -- check that before "
            f"waiting for this run."
        )

    def _reported(self, model: str, *, role: str | None = None):
        """`/api/ps` for `model`, loading it first if that is all that is wrong.

        A cold endpoint is not the operator's mistake and should not end their
        run. The remedy `window.reported` has always described in its docstring
        is performed here: one load, one re-probe, and then the original error
        if it still is not there. No loop and no backoff -- a model that did not
        appear after a load that reported success is not going to appear on the
        third ask, and a retry ladder would turn a clear failure into a long one.

        Only on `loadable`. The other four causes of `WindowUnknown` are
        properties of the endpoint's answer rather than of what it has resident,
        and sending a load request at any of them would be answering a question
        nobody asked.

        The announcement is unconditional rather than behind `-v`, because tens
        of seconds of silence is the thing being fixed and an operator who did
        not think to ask for verbosity is exactly the operator it happens to.
        """
        from . import window

        try:
            return window.reported(self.settings, model, role=role)
        except window.WindowUnknown as unknown:
            if not getattr(unknown, "loadable", False):
                raise
            self.console.notice(
                f"{model} is not loaded on {self.settings.endpoint_name}; loading it now, "
                f"which takes a moment for a large model"
            )
            with self.console.waiting(f"loading {model}"):
                loaded = window.warm(self.settings, model, role=role)
            if not loaded:
                raise
            # One re-probe. If it raises, it raises: `reported`'s message is
            # already the right one and wrapping it would bury the endpoint's
            # own account of itself under this method's guess about it.
            window_ = window.reported(self.settings, model, role=role)
            # Counted here and not above, so the number means "a model was
            # loaded" rather than "a load request was accepted". An endpoint
            # that returns 200 and still has nothing resident loaded nothing,
            # and the record should not claim otherwise.
            self.usage.warmups += 1
            return window_

    # -- fetching ---------------------------------------------------------

    def _fetch(
        self,
        *,
        role: str,
        model: str,
        prompt_sha256: str,
        messages: list[dict],
        schema: dict,
        schema_name: str,
        max_tokens: int | None,
        thinking: bool,
        attempt: int,
    ) -> tuple[str, str]:
        """Return (raw response body, tier used). Cassette, cache, or network."""
        # Lazy, for the reason every other import of it here is: a replay run
        # must be able to reach this path without loading the module that can
        # open a socket. Only the constant is wanted.
        from . import window as window_module

        def key(tier: str) -> str:
            return key_for(
                role=role,
                model=model,
                tier=tier,
                prompt_sha256=prompt_sha256,
                messages=messages,
                schema=schema,
                temperature=TEMPERATURE,
                seed=SEED,
                max_tokens=max_tokens,
                thinking=thinking,
                sample=self.sample,
                # Part of what was asked, because a profile decides which
                # fields reach the model at all -- a body with no `seed` is a
                # different request from one with `seed: 0`. It is omitted
                # from the hash at its default, so the 790 recordings made
                # before profiles existed keep their names; `key_for` says why
                # that is sound rather than convenient.
                profile=self.settings.profile,
                # And which *mechanism* answered, on the same terms. A
                # subprocess and an endpoint given the same request are two
                # different things, and the profile does not separate them --
                # nothing stops a command backend running under the default
                # profile. Empty on the HTTP path, so every existing recording
                # keeps its name.
                #
                # `command_for`, not `command`: the effort level is per
                # role since 562, so two roles answered by the same
                # program are asked for different amounts of reasoning
                # and did not send the same request. A key that read the
                # route would let a `low` decompose answer a `high` one.
                command=self.settings.command_for(role),
            )

        self.last_gap = None  # only a live call has one
        self.last_cached = False
        self.last_thinking = thinking
        self._recorded_order = None  # only a replayed answer has one

        # The identity of this request, fixed here so that all three paths file
        # the same row for it whichever one answers.
        #
        # `request_sha256` is over the bytes actually sent. `prompt_sha256` is
        # the unrendered template file and is constant across draws by
        # construction, so it cannot tell two draws apart and cannot settle
        # entry 167 -- `request_sha256` is the field that can. Both are here
        # because they answer different questions: which prompt version ran,
        # and what was sent under it.
        self._pending_call = {
            "role": role,
            "model": model,
            "prompt_sha256": prompt_sha256,
            "request_sha256": hashlib.sha256(canonical({
                "messages": messages,
                "schema": schema,
                "temperature": TEMPERATURE,
                "seed": SEED,
                "max_tokens": max_tokens,
                "thinking": thinking,
                # Same rule as the cassette key below it and for the same
                # reason: the profile changes which of the fields above
                # actually go on the wire, so two runs that differ by it did
                # not send the same request. Absent at the default, so every
                # ledger row this project has already published is unmoved.
                **({"profile": self.settings.profile}
                   if self.settings.profile != structured.DEFAULT_PROFILE else {}),
            })).hexdigest(),
            # Carried onto every ledger row so `window.assert_untruncated` can
            # read a call's own ceiling back off the ledger rather than being
            # passed it separately -- the same "the run already reports this
            # exactly" figure Brief AL item 2 asks the check to use. `None` for
            # a role with no ceiling, which the check already treats as
            # nothing to test.
            "max_tokens": max_tokens,
            # The same idea for the other end of the call, and the pair the
            # prompt-side check compares: what this run believed it was
            # sending, beside what the endpoint says it received
            # (`window.assert_prompt_not_trimmed`). Computed the way the
            # preflight computes it -- `chars // CHARS_PER_TOKEN` -- because
            # the check's whole basis is that the two are the same estimator,
            # so their ratio is a property of the endpoint rather than of two
            # different ways of counting.
            "estimated_prompt_tokens": sum(
                len(m.get("content") or "") for m in messages
            ) // window_module.CHARS_PER_TOKEN,
        }

        def note(tier: str, raw: str) -> None:
            self.last_key, self.last_tier = key(tier), tier
            self.last_reasoned = reasoned(raw)
            if not thinking and self.last_reasoned:
                self._reasoned_anyway(role=role, model=model)

        if self._replay is not None:
            tier = self._replay_tier(role, key)
            cassette = self._replay.require(key(tier), role)
            self.usage.replayed += 1
            self._record_usage(recorded_envelope(cassette.raw),
                               tier=tier, source="replay")
            self.console.detail(f"{role}: replayed from {self._replay.directory}")
            note(tier, cassette.raw)
            # How the recording run read this answer, which is the one
            # condition of the recording the key cannot carry: it changes how
            # the answer is read, not what was asked (DECISIONS 583).
            self._recorded_order = cassette.field_order
            return cassette.raw, tier

        # No seeding of `self.tier` from the capability record. It used to
        # happen here, and it is what made the record a latch: a verdict
        # written by some earlier process, possibly from a transient, chose the
        # rung for this one and was never tested again. The ladder re-derives
        # it from the top instead, every process, and the record is written
        # rather than read. See structured.Capabilities.

        def keep(raw: str, tier: str, latency: int) -> None:
            for store, force in ((self._cache, True), (self._record, self.settings.force_record)):
                if store is not None:
                    store.write(
                        key=key(tier), role=role, model=model, tier=tier, messages=messages,
                        schema=schema, temperature=TEMPERATURE, raw=raw, http_status=200,
                        endpoint=self.settings.endpoint_id_for(role), latency_ms=latency, attempt=attempt,
                        source=self._source, force=force,
                        # The order this run reads the answer under, which is
                        # what a replay needs to reproduce it. A cache hit
                        # written through is read under this run's setting too.
                        field_order=self.settings.field_order,
                    )

        if self._cache is not None:
            # Which tier to look under, when the ladder has not run yet in this
            # process? Whichever one the answer is actually filed at. This is
            # the same reasoning `_replay_tier` uses, and it is what replaced
            # seeding the tier from the capability file: an entry on disk is a
            # fact about one recorded response, and the recording proves the
            # tier because it could not have been written at any other.
            for cache_tier in (self.tier,) if self.tier else structured.TIERS:
                cached = self._cache.get(key(cache_tier))
                if cached is None:
                    continue
                if cached.endpoint_id and cached.endpoint_id != self.settings.endpoint_id_for(role):
                    # Advisory only, since DECISIONS 405: the endpoint is not
                    # in the key on purpose — it answers "what did this model
                    # say to this prompt", and that question has one answer
                    # regardless of which box asked it. A skip used to treat
                    # the endpoint as a second, unkeyed axis of the cache; that
                    # cost an ephemeral pod's restart its whole cache for a
                    # difference the key already says does not change the
                    # answer. `-vv` still gets to know which box actually
                    # filled the entry being served.
                    self.console.detail(
                        f"{role}: cache entry recorded against {cached.endpoint_id}, "
                        f"serving it to {self.settings.endpoint_id_for(role)} -- the key is "
                        f"content, not the machine"
                    )
                self.usage.cache_hits += 1
                self._record_usage(recorded_envelope(cached.raw),
                                   tier=cache_tier, source="cache")
                self.last_cached = True
                self.console.detail(f"{role}: answered from the cache, no call made")
                # Still write it through to --record. A recording run resumed
                # after a failure would otherwise produce a cassette set with
                # holes exactly where the first attempt succeeded.
                note(cache_tier, cached.raw)
                keep(cached.raw, cache_tier, cached.latency_ms)
                # Deliberately not `self.tier = cache_tier`. A cached answer
                # says what one request got, not what the endpoint can do now,
                # so the first live call of this process still starts the
                # ladder at the top. That is entry 1's rule applied to the one
                # place it could sneak back in.
                if self.tier_source == "probed":
                    self.tier_source = "cached"
                return cached.raw, cache_tier

        # The only line in this method that can take minutes, so it is the
        # only one the operator needs to be told about while it is happening
        # rather than after. `waiting` animates on a terminal and does nothing
        # anywhere else, so a piped run and a test harness see one step line.
        self.console.step(f"{role}: asking {model}")
        with self.console.waiting(f"{role}: waiting for the endpoint"):
            raw, tier, latency = self._live(
                role=role,
                model=model,
                messages=messages,
                schema=schema,
                schema_name=schema_name,
                max_tokens=max_tokens,
                thinking=thinking,
            )
        # The id the model's own CLI resolved the alias to, where it said: a
        # run log is read long after the alias has moved to a newer model.
        said = answered_by(recorded_envelope(raw))
        resolved = f" ({said['output']})" if said and said["output"] else ""
        self.console.done(f"{role}: {model}{resolved} answered at the {tier} tier",
                          seconds=latency / 1000)

        note(tier, raw)
        keep(raw, tier, latency)
        return raw, tier

    def _reasoned_anyway(self, *, role: str, model: str) -> None:
        """This answer carries reasoning and the call asked for none.

        Severity by mode, for the reason `structured.ThinkingIgnored` gives:
        under --record the artefact would carry a false label and there is no
        way to write it honestly, so the run stops before anything is written
        -- which is why `note` runs ahead of `keep` at every site. Everywhere
        else the run continues and says so, once per model here and in the
        provenance block for good.

        Checked on every path, not just the live one. A cached or replayed
        answer that was reasoned is just as reasoned when it is reused, and a
        recording run that writes a cache hit through to its cassette
        directory would otherwise put the same false label on disk by the
        longer route.
        """
        self.usage.thinking_ignored.add(role)
        if self._record is not None:
            raise structured.ThinkingIgnored(
                f"{model} reasons regardless of the thinking setting: this call "
                f"asked for {role} with thinking off and the answer came back "
                f"with a reasoning block in it. This run is recording, so "
                f"continuing would write that answer to a cassette keyed "
                f"`thinking=False` and every later reader would believe it. "
                f"Record the arm as what it is -- `--thinking {role}` -- or "
                f"record a model that can answer without thinking."
            )
        if model not in self._reasoning_noticed:
            self._reasoning_noticed.add(model)
            self.notify(
                f"{model} reasons regardless of the thinking setting; "
                f"continuing, and the report records it"
            )

    def _replay_tier(self, role: str, key) -> str:
        """Which tier was this call recorded at?

        A pinned tier answers directly. Otherwise the recording itself is the
        answer: whichever tier's key is on disk is the tier the live run
        resolved, which is what makes a replayed run reproduce it exactly.
        """
        if self.settings.pinned:
            return self.settings.structured
        if self.tier is not None and self._replay.has(key(self.tier)):
            return self.tier
        for tier in structured.TIERS:
            if self._replay.has(key(tier)):
                self.tier = tier
                self.tier_source = "replayed"
                return tier
        return self.tier or structured.TIERS[0]

    def _live(
        self,
        *,
        role: str,
        model: str,
        messages: list[dict],
        schema: dict,
        schema_name: str,
        max_tokens: int | None,
        thinking: bool,
    ) -> tuple[str, str, int]:
        """Make a real request, walking down the tier ladder if one is refused."""
        from . import transport  # imported here so replay never loads it
        from . import backend    # and the same for the second way to answer

        candidates = list(
            (self.settings.structured,)
            if self.settings.pinned
            else structured.tiers_from(self.tier or structured.TIERS[0])
        )
        # Per-role since entry 421. `role` has always been in scope here; what
        # changed is that the endpoint is now asked for by it, so a frontier
        # merge and a local decompose can be one run.
        # Empty for a command backend, which has no URL to build and nothing
        # to build one from. Kept as one name rather than branching twice:
        # everything between here and the call reads the same either way.
        #
        # `command_for` carries this role's effort level on the argv
        # (562). It is the one place the flag is appended, so what is
        # executed and what `provenance` prints are read off one function.
        command = self.settings.command_for(role)
        url = ("" if command
               else f"{self.settings.base_url_for(role)}/chat/completions")
        last: Exception | None = None
        tried: list[str] = []
        empties, empty_tier = 0, None

        while candidates:
            tier = candidates.pop(0)
            if tier not in tried:
                tried.append(tier)
            self._stop_if_cancelled()
            if self.usage.calls >= self.settings.max_calls:
                raise CallBudgetExceeded(
                    f"--max-calls {self.settings.max_calls} reached; stopping before "
                    f"the next call. Raise the limit or narrow the run."
                )
            try:
                body = structured.build_body(
                    tier=tier,
                    model=model,
                    messages=messages,
                    schema=schema,
                    schema_name=schema_name,
                    temperature=TEMPERATURE,
                    seed=SEED,
                    max_tokens=max_tokens,
                    thinking=thinking,
                    reasoning_effort=self._reasoning_effort,
                    profile=self.settings.profile,
                )
            except structured.TierUnsupported as exc:
                # The profile says this rung cannot carry this request -- today
                # that is `tools` beside `reasoning_effort`, an HTTP 400 on both
                # OpenAI 5.6 SKUs. Treated exactly as a refusal from the
                # endpoint would be, except that nothing was sent and nothing
                # was billed: the ladder steps down, and a pinned tier still
                # raises, because a run pinned to a rung its profile cannot
                # produce is a run that cannot be what it says it is.
                if self.settings.pinned:
                    raise
                last = exc
                continue
            # A cancel ends the pause early rather than after it (639). What
            # the pause really took is this call's own wait (681); a stand-in
            # pacer that reports nothing waited nothing this run can measure.
            paced = self._pace(**({} if self.cancel is None
                                  else {"sleep": self.cancel.wait})) or 0.0
            # Again after the pause: `--min-interval` can sleep for minutes,
            # and a cancel that arrived during it must not be followed by a
            # call (639).
            self._stop_if_cancelled()
            if self._last_call_ended:
                # Achieved, not requested. A sweep planned at 15 s a call can
                # drift, and a report claiming the interval it asked for rather
                # than the one it got is the kind of number nobody can check.
                self.last_gap = time.monotonic() - self._last_call_ended
            self.usage.calls += 1
            self.usage.calls_by_role[role] = self.usage.calls_by_role.get(role, 0) + 1
            started = time.monotonic()
            response = None
            envelope = None
            try:
                # The seam. Two ways to answer one request, and the branch
                # is here rather than behind a common object because the two
                # take different arguments for real reasons: there is no API
                # key to send a subprocess, no CA bundle to verify it against,
                # and nothing to stream. A wrapper hiding that would have to
                # accept and discard four arguments, which reads as though
                # they applied.
                response = (
                    backend.post_json(
                        command,
                        body,
                        timeout=self.settings.call_timeout,
                        host=self.settings.endpoint_name,
                        model=model,
                        # Declared by whoever configured the command, not
                        # detected from what it writes (537). A route that
                        # answers with a result envelope gets its token counts
                        # and its `server_tool_use` counter read; one that does
                        # not stays `unmeasured` on both, which is what it was.
                        envelope=self.settings.command_envelope,
                        cancel=self.cancel,
                    ) if command else
                    self._abandonable(lambda sleep, key=self.settings.api_key(role):
                                      transport.post_json(
                        url,
                        body,
                        # Read here, on the calling thread, and bound into the
                        # call: the key source is a ContextVar (468), and a
                        # thread started without this context would read the
                        # process environment -- the operator's key -- instead
                        # of the submitter's. `test_web_accounts` caught that.
                        api_key=key,
                        timeout=self.settings.call_timeout,
                        ca_bundle=self.settings.ca_bundle,
                        host=self.settings.endpoint_name,
                        model=model,
                        stream=self.settings.stream,
                        sleep=sleep,
                    ))
                )
                envelope = json.loads(response.body)
                structured.read_content(tier, envelope)  # shape check before committing
            except transport.Cancelled as exc:
                # Not a fault and not a tier question: the run was cancelled
                # during this call (639). The call was counted above when it
                # was sent, which is what it is -- made, and possibly billed.
                self.usage.seconds += time.monotonic() - started
                self._last_call_ended = time.monotonic()
                self._discard(DISCARD_CANCELLED, tier, exc, paced=paced,
                              started=started, response=response)
                raise transport.Cancelled(
                    f"cancelled during call {self.usage.calls}, which was "
                    f"abandoned without an answer; {self.usage.calls} call(s) "
                    f"were made in all, and the provider may still bill the "
                    f"last one ({exc})") from None
            except (structured.EmptyResponse, transport.EmptyBody) as exc:
                # A blank body says nothing about the tier, so it must not
                # descend one, and it must not reach the repair loop either:
                # there is no fault to quote back to a model that said nothing.
                # Ask the same question again, at the same rung -- unless the
                # envelope itself already says a retry cannot help (below).
                self.usage.seconds += time.monotonic() - started
                self._last_call_ended = time.monotonic()
                # Written before anything below decides to retry or raise, so
                # no path out of this except block can skip it. `envelope` is
                # the parsed body for an `EmptyResponse` (the content field was
                # blank, everything around it -- usage, any reasoning field --
                # arrived); it is `None` for an `EmptyBody`, because there
                # `response` itself was never assigned -- the body really was
                # zero bytes and there is nothing more to keep than that.
                self._dump_discard(
                    role, tier, kind=type(exc).__name__,
                    envelope=envelope, raw_body=response.body if response else None,
                    detail=str(exc),
                )
                # And a row for the report, from the same place and for the
                # same reason (681): a blank is excluded from the cell's time
                # and cost (678), and excluded is not the same as unrecorded.
                self._discard(blank_kind(envelope), tier, exc, paced=paced,
                              started=started, response=response, envelope=envelope)
                # The generation was not blank. `finish_reason: "length"` with
                # a reasoning block and no content means the model spent its
                # whole ceiling reasoning and never reached the answer -- a
                # different fault from an endpoint that answered 200 and said
                # nothing, and one a same-tier retry cannot fix: the same
                # prompt against the same ceiling reasons into the same wall a
                # second time. Measured against `claude-sonnet-5` before this
                # distinction existed: three attempts, 13,824 completion
                # tokens each, `content: null` every time, ~$0.85-1.00 across
                # six attempts for zero data, reported as "the generation is
                # blank" -- which sent an hour of investigation toward the
                # wrong endpoint.
                truncated = (
                    structured.length_truncation_reason(envelope)
                    if envelope is not None else None
                )
                if truncated is not None:
                    ceiling = body.get(structured.profile_for(self.settings.profile).budget_field)
                    raise structured.EmptyResponse(
                        f"{self.settings.endpoint_name} exhausted its output ceiling "
                        f"on {model} at tier {tier} before any content was emitted: "
                        f"{truncated}. The ceiling sent was "
                        f"{ceiling if ceiling is not None else 'unset (endpoint default)'}. "
                        f"Retrying at the same ceiling would not help, so this was "
                        f"not attempted a second time; raise the ceiling (or, on a "
                        f"profile with no project-imposed one, this is the "
                        f"endpoint's own default) instead."
                    ) from exc
                empties = empties + 1 if tier == empty_tier else 1
                empty_tier = tier
                if empties < EMPTY_RESPONSE_ATTEMPTS:
                    candidates.insert(0, tier)
                    continue
                raise structured.EmptyResponse(
                    f"{self.settings.endpoint_name} answered {empties} times with an empty "
                    f"body at tier {tier} for model {model}. The endpoint is "
                    f"reachable and returning 200; it is the generation that is "
                    f"blank."
                    # One hint, and only where it was measured. gpt-oss:120b
                    # asked for thinking off answers nothing at all: 763
                    # completion tokens billed, zero characters returned. A
                    # model that always reasons has no answer left to give once
                    # the reasoning is suppressed, and the operator cannot see
                    # that from a blank body.
                    + (f" This call asked {model} to answer {role} with thinking"
                       f" off. Some models cannot: they reason or they say"
                       f" nothing. Try --thinking {role} to let it think."
                       if not thinking else "")
                ) from exc
            except Exception as exc:  # noqa: BLE001 - re-raised below unless it means "wrong tier"
                self.usage.seconds += time.monotonic() - started
                self._last_call_ended = time.monotonic()
                # A call the platform lost, or a rung it refused: not the
                # model's answer, whatever happens next (681).
                self._discard(DISCARD_PLATFORM, tier, exc, paced=paced,
                              started=started, response=response, envelope=envelope)
                if self._reasoning_effort and structured.rejected_field(exc, "reasoning_effort"):
                    # Not a tier problem, and not survivable. `build_body` sends
                    # this field only when the caller asked for thinking off, so
                    # a rejection means the one lever that turns thinking off is
                    # gone. Retrying without it -- which is what this branch used
                    # to do, once, for the life of the client -- buys a run whose
                    # cassettes say `thinking=False` over answers the model
                    # reasoned its way to. Abort instead: an arm that cannot be
                    # what it claims to be is worth less than no arm.
                    raise structured.ThinkingNotHonoured(
                        f"{self.settings.endpoint_name} rejected `reasoning_effort` for model "
                        f"{model}, and that field is the only thing that turns thinking "
                        f"off on the OpenAI-compatible path. This call asked for thinking "
                        f"off, so continuing would record a thinking-on answer under a "
                        f"`thinking=False` cassette key. Find a value this endpoint "
                        f"accepts for this model, or run the role with thinking on and "
                        f"say so. Endpoint said: {exc}"
                    ) from exc
                if not structured.should_fall_back(exc) or self.settings.pinned:
                    raise
                last = exc
                continue

            self.usage.seconds += time.monotonic() - started
            self._last_call_ended = time.monotonic()
            # Read off `body`, the dict actually serialised onto the wire for
            # this call -- not rebuilt, not the module constants it was built
            # from. Brief AL item 3: DECISIONS 178 already ruled out rebuilding
            # a body to check one, because a rebuild proves the rebuild, and
            # `body` here is the original, never a second construction of it.
            self._record_usage(envelope, tier=tier, source="live",
                               latency_ms=response.latency_ms,
                               timing=call_timing(response, paced), wire={
                # Presence, not just value. A profile can omit either field
                # (Anthropic's sonnet-5 deprecates `temperature` and has no
                # `seed`), and "absent" is a different fact from any value the
                # key could have carried.
                "temperature": body["temperature"] if "temperature" in body else NOT_SENT,
                "seed": body["seed"] if "seed" in body else NOT_SENT,
                "thinking": "reasoning_effort" not in body,
            })

            self._settle(model, tier, tried, last)
            return response.body, tier, response.latency_ms

        # `candidates` is empty by now — it is the queue, and the loop drained
        # it — so the message has to name the tiers that were actually tried.
        raise RuntimeError(
            f"{self.settings.endpoint_name} accepted none of the structured-output modes "
            f"({', '.join(tried)}) for model {model}: {last}"
        ) from last

    def _record_usage(self, envelope: dict | None, *,
                      tier: str, source: str, wire: dict | None = None,
                      latency_ms: int | None = None,
                      timing: dict | None = None) -> None:
        """Charge one response's tokens to the run, and file its ledger row.

        `wire` carries what the live path's own request body said -- at
        minimum `temperature` and `thinking` -- read from `body` at the call
        site rather than from `TEMPERATURE`/`SEED`/`Settings.thinking`. Only
        the live path has one: a replay or cache hit sent nothing this run, so
        there is no wire to read and the row simply carries no such keys,
        which callers already treat the same way they treat a vendor that
        reported no usage -- absent, not zero.

        The only place that does either. Called from all three paths that
        produce a response body -- the live call, the cache hit and the replay
        -- because a replayed run that reported no tokens would make the
        recorded corpus, where every published figure comes from, the one place
        the cost figure cannot be read. The counts are in the recording already:
        every cassette stores the provider's envelope verbatim, and the usage
        block is part of it.

        The ledger is written here rather than anywhere else for the same
        reason the totals are. Two write points would let a run carry a
        per-call record that does not add up to its own per-run figure, and the
        whole use of a ledger is that it can be added up and checked against a
        bill.

        Entry 138's rule holds per call as it holds per run: a response whose
        vendor reported no usage has no token keys in its row. Not zero -- the
        row is still there, because a call that happened is a line on the bill
        whether or not its size was reported, and a spend reconciliation that
        dropped it would be reconciling against a shorter run than the one that
        took place.
        """
        counts = self.usage.tokens.add(envelope)
        # The same envelope, the same single write point, and the same
        # unknown-is-not-zero rule. Here rather than anywhere else for
        # entry 138's reason: two write points would let a run carry a
        # search count that disagrees with its own call count.
        self.usage.searches.add(envelope)
        # And the turn count beside it, at the same single write point and
        # under the same unknown-is-not-zero rule (548). Its floor is read off
        # the argv this call executed: under the isolation one retrieval is
        # two turns, not three, and the older floor would read it as none (610).
        role = (self._pending_call or {}).get("role")
        executed = (self.settings.command_for(role) if role in config.ROLES
                    else config.command_with_isolation(self.settings.command))
        # Filed by role as well (665): `sourced` is judged on the merge's
        # calls, which is where every citation it reports was written.
        self.usage.turns.add(envelope, web_only=config.only_web_tools(executed),
                             role=role if role in config.ROLES else None)
        row = dict(self._pending_call or {}, tier=tier, source=source)
        # The model ids that really answered, beside the `model` the route
        # named. On every path, not the live one only: it is read off the
        # envelope, which a cassette keeps verbatim, so a replay files the same
        # row its live run did and the replay comparison needs no exemption.
        # Absent, never empty, where the envelope named none -- every HTTP call
        # and every recording made before a command envelope carried it.
        answered = answered_by(envelope)
        if answered is not None:
            row["answered_by"] = answered
        # The HTTP path's own version of the same fact (B7, 680): a vendor
        # endpoint's bare `model` field, kept under its own key rather than
        # folded into `answered_by` above -- see `usage.served_model` for why
        # the two must not merge. Mutually exclusive by construction: a
        # command backend's synthesised envelope never carries a top-level
        # `model`, and an HTTP envelope never carries `answered_by`.
        served = served_model(envelope)
        if served is not None:
            row["served_model"] = served
        # The call's wall time, on the live row only (575): the one per-call
        # figure a `--no-cache` run left nowhere, since the cassette that also
        # records it is not written. A replay or a cache hit made no request
        # and has no time of its own, so the key is absent there, not zero --
        # and the replay acceptance test exempts it by name, beside `source`,
        # as how a call ran rather than what it asked.
        if latency_ms is not None:
            row["latency_ms"] = latency_ms
        # How that time was spent (681), on the live row only and for the
        # same reason: `attempts`, `answer_ms`, `failed_ms`, `waited_ms`,
        # `ttfb_ms` and a command route's own `cli_duration*_ms`. See
        # `call_timing`. Each is exempt by name from the replay comparison.
        if timing:
            row.update(timing)
        if wire is not None:
            # Kept off the row on purpose. `ledger` is compared verbatim
            # between a live run and its replay (the replay determinism
            # acceptance test), and a replay makes no request and so has no
            # wire of its own -- a key only the live path could ever carry
            # would make every replay disagree with the run it reproduces on
            # a field that run never claimed to answer. `latency_ms` above is
            # the one such key, exempted by name, because a call's time has no
            # per-run home to go to instead; these do. `Usage.wire_temperature`
            # and `.wire_thinking` are per-run/per-role instead, read only by
            # `Provenance`'s top-level `decoding` block, which already falls
            # back to the constant/setting for a run with no live call --
            # exactly what a replay is.
            if "temperature" in wire:
                self.usage.wire_temperature = wire["temperature"]
            if "seed" in wire:
                self.usage.wire_seed = wire["seed"]
            role = row.get("role")
            if role and "thinking" in wire:
                self.usage.wire_thinking[role] = wire["thinking"]
        # Asserted per row, not once at the start. `resolved_tier()` reports
        # what the run settled on and reaches the report header exactly once;
        # a single call that answered on another rung would not disturb it.
        if self.settings.pinned and tier != self.settings.structured:
            raise PinnedTierViolated(
                f"--structured {self.settings.structured} pins the tier, and this "
                f"{source} call resolved to {tier!r} instead. A run whose calls "
                f"are not all on one rung is two measurements under one label: "
                f"the report's mode field can only name one of them."
            )
        if counts is not None:
            if "input" in counts:
                self.usage.prompt_tokens += counts["input"]
                row["prompt_tokens"] = counts["input"]
            if "output" in counts:
                self.usage.completion_tokens += counts["output"]
                row["completion_tokens"] = counts["output"]
            # Cached input, per row, because that is where it has to be to be
            # *costed* (488): cache reads bill at a tenth to a fifth of the
            # input rate, and a run that read 7,449 of 21,405 input tokens from
            # cache is over-charged by 8% without this. The run-wide totals
            # already carry the same figure, but a run can put three roles on
            # three models at three rates, so the split has to be per call.
            #
            # Written only when the vendor reported it, like the two above. An
            # absent key is a vendor that said nothing about caching, and
            # writing zero would claim it said there was none.
            if "cached" in counts:
                row["cached_tokens"] = counts["cached"]
            # A total above input plus output is output the vendor billed and
            # did not count as output (624). Google's compatibility endpoint
            # reports `completion_tokens` without the thinking tokens and
            # `total_tokens` with them -- 7 in, 5 out, 253 total on a
            # three-word answer from gemini-3.8-flash -- and its pricing page
            # bills output "including thinking tokens". Kept only when the
            # total exceeds the sum, so no endpoint whose total adds up (every
            # recording in the corpus) gains a key.
            if ("total" in counts and "input" in counts and "output" in counts
                    and counts["total"] > counts["input"] + counts["output"]):
                row["total_tokens"] = counts["total"]
        self.usage.ledger.append(row)

    def _endpoint(self) -> str:
        """Which server this is. Resolved once, lazily, on a live path only.

        Never at construction: a replay run builds a Client too, and it must
        not so much as resolve a name.
        """
        if self._endpoint_identity is None:
            self._endpoint_identity = structured.endpoint_identity(
                self.settings.host, self.settings.port
            )
        return self._endpoint_identity

    def _settle(
        self, model: str, tier: str, tried: list[str], refusal: Exception | None
    ) -> None:
        """A call came back at `tier`. Say so if that is news, and write it down.

        Two different kinds of news, and the difference matters to whoever is
        reading. A demotion inside one process means the run is not the run it
        started as: earlier calls were answered at a stronger rung, later ones
        will not be, and because `tier` is part of the cassette key the corpus
        now has two halves. That is the failure M4 spent a sweep discovering
        from a journal afterwards, so it is said at the moment it happens.

        A resolution that merely differs from the last recorded one is
        ordinary: it is what re-deriving the answer every process is for, and
        the record is there to make the change visible rather than to prevent
        it.
        """
        if self.tier is not None and self.tier != tier:
            if structured.TIERS.index(tier) > structured.TIERS.index(self.tier):
                self.notify(
                    f"structured output demoted mid-run, {self.tier} -> {tier}, after "
                    f"{self.usage.calls} calls to {self.settings.endpoint_name}. Everything "
                    f"recorded from here files under a different cassette key. "
                    f"Cause: {refusal}"
                )
            else:
                self.notify(f"structured output moved {self.tier} -> {tier} mid-run")
        self.tier = tier

        if self.settings.pinned:
            why = f"pinned with --structured {tier}, and the endpoint accepted it"
        elif len(tried) > 1:
            why = f"{tried[0]} refused, descended to {tier}: {refusal}"
        else:
            why = f"accepted at {tier}, the first rung tried"

        previous = self.capabilities.record(self._endpoint(), model, tier, why)
        if previous is not None and previous.tier != tier:
            self.notify(
                f"{self.settings.endpoint_name} last resolved to {previous.describe()}; "
                f"today it resolved to {tier}. The record is updated. It is a "
                f"record only -- the ladder re-derives this every run."
            )

    # The web server's cancel (639): a `threading.Event`, set on the instance
    # by `web.jobs._run_merge` after construction. With one, `_live` makes no
    # call after it is set, abandons the call in flight, and has a command
    # backend stop its program. `None` here, which is every command-line run,
    # changes nothing. A class attribute, down here, rather than an
    # `__init__` argument, so every line a document cites above stays put.
    cancel = None

    def _stop_if_cancelled(self) -> None:
        """Raise `Cancelled` if the run was cancelled, before the next call (639)."""
        if self.cancel is not None and self.cancel.is_set():
            from .transport import Cancelled
            raise Cancelled(
                f"cancelled before call {self.usage.calls + 1}; "
                f"{self.usage.calls} call(s) had been made")

    # How often a waiting caller looks at the cancel flag while a call is in
    # flight (639).
    CANCEL_POLL_SECONDS = 0.1

    def _abandonable(self, call):
        """`call(sleep)` in a thread this client can walk away from (639).

        Without a cancel flag it is `call(time.sleep)` on this thread, exactly
        as before. With one, the request runs on a daemon thread and this one
        waits for either the answer or the flag. On the flag it raises
        `Cancelled` and the thread is abandoned: an HTTP request already sent
        cannot be taken back, and waiting for it would keep a cancelled run
        alive for as long as the model takes. `sleep` is how the abandoned
        thread is kept from making another request: the transport's retry
        backoff sleeps through it, and it raises instead of sleeping once the
        flag is set, so a retry never follows a cancel.
        """
        import contextvars

        from .transport import Cancelled
        cancel = self.cancel
        if cancel is None:
            return call(time.sleep)

        def sleep(seconds: float) -> None:
            if cancel.wait(seconds):
                raise Cancelled("stopped before a retry")

        box: dict = {}
        done = threading.Event()

        def work() -> None:
            try:
                box["value"] = call(sleep)
            except BaseException as exc:  # noqa: BLE001 - handed to the waiting thread
                box["error"] = exc
            finally:
                done.set()

        # In a copy of this thread's context as well, so anything the call
        # reads from a ContextVar is what this thread would have read.
        context = contextvars.copy_context()
        threading.Thread(target=lambda: context.run(work), name="llossless-call",
                         daemon=True).start()
        while not done.wait(self.CANCEL_POLL_SECONDS):
            if cancel.is_set():
                raise Cancelled("the request was abandoned in flight")
        if "error" in box:
            raise box["error"]
        return box["value"]

    def _pace(self, sleep=time.sleep) -> float:
        """Wait out --min-interval since the last live call finished.

        A local GPU under sustained load is a thermal problem, not a rate-limit
        one, and the failure mode is the machine powering off mid-run rather
        than a 429 that could be retried. Sleeping between calls is the whole
        mitigation. Cache hits and replays never come through here, so a warm
        run pays nothing for it.

        Returns the seconds it actually waited, measured rather than asked
        for: the next call's own `waited_ms` carries it (681), because a pause
        is not the model's time and a cell's speed must not include it.
        """
        if self.settings.min_interval <= 0 or not self._last_call_ended:
            return 0.0
        remaining = self.settings.min_interval - (time.monotonic() - self._last_call_ended)
        if remaining <= 0:
            return 0.0
        self.console.detail(f"pausing {remaining:.1f}s for --min-interval")
        began = time.monotonic()
        sleep(remaining)
        return time.monotonic() - began

    # -- failures ---------------------------------------------------------

    def _dump_root(self) -> Path:
        """Where `failures/` and `discards/` go. Not the cache when it is off.

        These two directories hold response bodies, and a response body is the
        merge -- the documents' content, rearranged. They were justified on the
        grounds that they land in "the same gitignored `.claimcheck-cache/`",
        which was true of a checkout and stopped being true the day the package
        became installable: an installed user has no git, so nothing there is
        gitignored, and `--no-cache` was switching off the cassettes while these
        kept writing.

        With the cache off they go to a directory made for this process, under
        the system temporary directory, and the path is printed once on stderr.
        Debugging survives -- the files are still there and still named -- and
        nothing outlives the machine's own cleanup. DECISIONS 311.
        """
        if self.settings.use_cache:
            return self.settings.cache_dir
        if self._scratch is None:
            self._scratch = Path(tempfile.mkdtemp(prefix="llossless-run-"))
            print(f"llossless: cache off; response dumps for this run go to "
                  f"{self._scratch}", file=sys.stderr)
        return self._scratch

    def _dump_attempt(self, role: str, attempt: int, raw: str) -> Path | None:
        """Keep the body that beat the parser, on every attempt that failed, not just the last.

        A draw that fails attempt 1 and repairs on attempt 2 used to leave
        attempt 1's response nowhere: only the response that ended the loop
        was ever written, so an audit trail could not show what a repair
        actually changed, or that an earlier attempt happened at all.
        """
        if not raw:
            return None
        directory = self._dump_root() / "failures"
        secure_dir(directory)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        self._dump_seq += 1
        path = directory / f"{stamp}-{role}-{self._dump_seq:04d}-attempt{attempt}.txt"
        secure_write(path, raw)
        return path

    def _dump_discard(self, role: str, tier: str, *, kind: str, envelope: dict | None,
                       raw_body: str | None, detail: str) -> Path:
        """Keep what a discarded call actually returned. Every discard path calls this.

        An `EmptyResponse` and an `EmptyBody` were both billed calls that
        produced nothing usable, and before this existed neither left anything
        on disk: a 200 with 763 completion tokens billed and zero characters
        of content was indistinguishable, after the fact, from a call that was
        never made at all. `envelope` carries `usage` and any `reasoning` or
        `reasoning_content` field whenever there was a body to parse; nothing
        here is redacted beyond what `_dump_attempt` already isn't, and both
        write wherever `_dump_root` says -- the cache in a checkout that has one
        gitignored, a per-run temporary directory when the cache is off.
        """
        directory = self._dump_root() / "discards"
        secure_dir(directory)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        self._dump_seq += 1
        path = directory / f"{stamp}-{role}-{self._dump_seq:04d}-{kind}.json"
        secure_write(path, json.dumps({
            "role": role,
            "tier": tier,
            "kind": kind,
            "detail": detail,
            "envelope": envelope,
            "raw_body": raw_body if envelope is None else None,
        }, indent=2))
        return path

    def _discard(self, kind: str, tier: str, exc: BaseException, *, paced: float,
                 started: float, response=None, envelope: dict | None = None) -> None:
        """File a live call that produced no ledger row under `Usage.discarded` (681).

        A blank re-asked, a call the platform lost, a rung refused, a cancel:
        each was counted in `usage.calls` when it went out, and none reaches
        the ledger, which only charges a body the model answered with. This is
        the row for the report, with the identity a ledger row carries, the
        tokens the vendor reported for it (a blank can be billed: 763
        completion tokens for zero characters, measured), and its time split
        the way a ledger row's is. `kind` is one of `DISCARD_KINDS`, and
        `counted_as` says whether 678 excludes it or it waits for a ruling.

        Not in `ledger`, and not in `usage.tokens`: the totals and the ledger
        keep the meaning every published figure was read under, and a replay,
        which never meets a blank, stays comparable with the run it
        reproduces.
        """
        row = dict(self._pending_call or {}, tier=tier, source="live", kind=kind,
                   counted_as=DISCARD_KINDS[kind], error=type(exc).__name__)
        finish = finish_reason(envelope)
        if finish is not None:
            row["finish_reason"] = finish
        served = served_model(envelope)
        if served is not None:
            row["served_model"] = served
        counts = normalise(envelope)
        for name, key in (("input", "prompt_tokens"), ("output", "completion_tokens"),
                          ("cached", "cached_tokens")):
            if counts is not None and name in counts:
                row[key] = counts[name]
        if (counts is not None and {"total", "input", "output"} <= set(counts)
                and counts["total"] > counts["input"] + counts["output"]):
            row["total_tokens"] = counts["total"]
        # `latency_ms` on every discarded row, with a ledger row's meaning:
        # the whole request, its retries and backoff included, pacing not.
        # Off the response where one arrived, else the client's own stopwatch
        # over the same span.
        row["latency_ms"] = (response.latency_ms if response is not None
                             else int((time.monotonic() - started) * 1000))
        if response is not None:
            row.update(call_timing(response, paced))
        elif getattr(exc, "attempts", None) is not None:
            # Stamped by the transport on the way out (`transport._stamp`).
            row.update(attempts=exc.attempts, failed_ms=exc.failed_ms,
                       waited_ms=int(paced * 1000) + exc.waited_ms)
            if exc.answer_ms is not None:
                row["answer_ms"] = exc.answer_ms
        else:
            # Nothing split it: a command backend's failure, a cancel. All of
            # it is failed time; attempts unknown, so not written.
            row.update(failed_ms=row["latency_ms"], waited_ms=int(paced * 1000))
        self.usage.discarded.append(row)


def _estimate_tokens(messages: list[dict]) -> int:
    """chars/4. Crude, and only ever used to say "roughly this big" in a dry run."""
    return sum(len(str(message.get("content", ""))) for message in messages) // 4


# Where a reasoning block can turn up. Ollama puts qwen3's in a `reasoning`
# field beside `content`; other endpoints leave it inline in `content` behind
# <think> tags, which is why `parsing.strip_reasoning` exists. Both spellings
# are checked because the answer to "did this model think" must not depend on
# which of them the endpoint happened to pick.
REASONING_FIELDS = ("reasoning", "reasoning_content")



def ceiling_cut(raw: str, row: dict, max_tokens: int | None) -> str | None:
    """How a response shows it stopped on its `max_tokens` ceiling, or None.

    Either signature is enough: `finish_reason: "length"` in the envelope,
    or the ledger row's completion count at or past the ceiling, which is
    `window.assert_untruncated`'s test and the one a vendor that reports no
    finish reason still leaves.

    `max_tokens` is `None` when this tool sent no ceiling of its own -- every
    frontier profile but `openai-compatible` (B1) -- and `finish_reason` is
    still read and still enough on its own (680, the cosmetic fix at
    `client.py:643`): the endpoint applied *some* limit even though this tool
    did not ask for one, and a response that stopped there and does not parse
    is a cut prefix either way. Only the second signature, the completion
    count against a ceiling, needs one to compare against, so it is skipped
    rather than raising when there is none to check.
    """
    try:
        choice = (json.loads(raw).get("choices") or [{}])[0]
        finish = choice.get("finish_reason")
    except (ValueError, AttributeError, IndexError, TypeError):
        finish = None
    if finish == "length":
        return "finish_reason 'length'"
    if max_tokens is None:
        return None
    completion = row.get("completion_tokens")
    if completion is not None and completion >= max_tokens:
        return f"{completion} completion tokens"
    return None

def reasoned(raw: str) -> bool:
    """Did this response carry a reasoning block, in either place it can live?

    Best effort by design: an unparseable body is not a reasoning block, and a
    caller asking this question is describing a run, not deciding one. Nothing
    downstream of a verdict depends on the answer.
    """
    try:
        message = json.loads(raw)["choices"][0]["message"]
    except (ValueError, KeyError, IndexError, TypeError):
        return False
    if any(str(message.get(name) or "").strip() for name in REASONING_FIELDS):
        return True
    content = str(message.get("content") or "")
    # The same anchored rule the parser uses, and for the same reason: a
    # document that mentions <think> is not a model that reasoned, and marking
    # the role reasoned in provenance on that evidence would be a fact about
    # the corpus recorded as a fact about the run. Comparing against a stripped
    # copy would also fire on nothing but trailing whitespace.
    return parsing.LEADING_REASONING.match(content) is not None


# -- accounting (681) --------------------------------------------------------
#
# What a benchmark cell is charged with. 678: "Retries are not counted in
# speed or cost. A cell's cost and time are those of the attempt that
# produced its answer", and an empty response, a timeout or a platform
# failure is excluded. A schema repair is not one of those: it is the model
# failing the format it was asked for, so it stays in the model's cost and
# time. Written down here, once, so `provenance` sums what this file decided
# rather than deciding again.
#
# A ledger row's `outcome`, set in `Client._complete` on every path (live,
# cache, replay), so a replay files the same outcome its live run did:
OUTCOME_ANSWER = "answer"    # its payload was returned: the answering attempt
OUTCOME_REPAIR = "repair"    # did not parse, asked again with the fault quoted
OUTCOME_FAILED = "failed"    # did not parse, and the unit of work gave up
OUTCOME_CEILING = "ceiling"  # cut at an output ceiling and refused (668, 680)
# Charged to the model: the answer, and the model's own format failures.
MODEL_OUTCOMES = frozenset({OUTCOME_ANSWER, OUTCOME_REPAIR, OUTCOME_FAILED})
# Not ruled: a runaway cut at the ceiling is the model's generation, and 680
# says the cell is excluded from scoring either way. 678 names neither.
UNRULED_OUTCOMES = frozenset({OUTCOME_CEILING})

# A discarded call's `kind`, and how 678 counts it (`counted_as`).
EXCLUDED = "excluded"
UNRULED = "unruled"
DISCARD_BLANK = "blank"            # EmptyBody, or empty content with no named reason
DISCARD_PLATFORM = "platform"      # the transport or the command failed, or a rung was refused
DISCARD_CANCELLED = "cancelled"    # the run was cancelled with the call in flight (639)
DISCARD_BLANK_LENGTH = "blank_length"    # empty content, finish_reason "length"
DISCARD_BLANK_REFUSAL = "blank_refusal"  # empty content, finish_reason "content_filter"
DISCARD_KINDS = {
    DISCARD_BLANK: EXCLUDED,
    DISCARD_PLATFORM: EXCLUDED,
    DISCARD_CANCELLED: EXCLUDED,
    # Both are empty responses, which 678 excludes, and both are arguably the
    # model's own: a budget spent reasoning into the wall, a safety refusal.
    # Neither is guessed at; both wait for the operator's ruling.
    DISCARD_BLANK_LENGTH: UNRULED,
    DISCARD_BLANK_REFUSAL: UNRULED,
}


def finish_reason(envelope: dict | None) -> str | None:
    """`choices[0].finish_reason`, or None where the envelope has none."""
    try:
        finish = envelope["choices"][0].get("finish_reason")
    except (TypeError, KeyError, IndexError, AttributeError):
        return None
    return str(finish) if finish else None


def blank_kind(envelope: dict | None) -> str:
    """Which kind of blank this was: `blank_length`, `blank_refusal` or `blank`."""
    finish = finish_reason(envelope)
    if finish == "length":
        return DISCARD_BLANK_LENGTH
    if finish == "content_filter":
        return DISCARD_BLANK_REFUSAL
    return DISCARD_BLANK


def call_timing(response, paced: float) -> dict:
    """A live call's time, split the way the report charges it (681).

      `attempts`             transport attempts, retries included
      `answer_ms`            the attempt that returned this body, alone
      `failed_ms`            the attempts before it that failed, sleeps excluded
      `waited_ms`            `--min-interval` pacing before the call, plus the
                             transport's backoff sleeps between attempts
      `ttfb_ms`              the answering attempt's time to its first body line
      `cli_duration_ms`,     a command route's own figures off its result
      `cli_duration_api_ms`  envelope (`backend.cli_timing`: both include the
                             CLI's own retries)

    so `latency_ms` plus the pacing is `failed_ms + waited_ms + answer_ms`,
    to within a few milliseconds. A response that did not split its own time
    (a fake transport's, of several attempts) gets `attempts` and `waited_ms`
    only: unknown is not zero. One attempt with no split is its whole latency.
    """
    attempts = getattr(response, "attempts", None)
    answer = getattr(response, "answer_ms", None)
    timing: dict = {"attempts": attempts,
                    "waited_ms": int(paced * 1000) + (getattr(response, "waited_ms", 0) or 0)}
    if answer is None and attempts == 1:
        answer = response.latency_ms
    if answer is not None:
        timing["answer_ms"] = answer
        timing["failed_ms"] = getattr(response, "failed_ms", 0) or 0
    ttfb = getattr(response, "ttfb_ms", None)
    if ttfb is not None:
        timing["ttfb_ms"] = ttfb
    for name, value in (getattr(response, "cli_timing", None) or {}).items():
        timing[f"cli_{name}"] = value
    return timing
