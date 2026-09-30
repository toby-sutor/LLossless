#!/usr/bin/env python3
"""Merge each fixture's two sources with the model, then check the merge end to end.

This is the end-to-end measurement and the project's first full pipeline: merge ->
decompose -> verify, both directions, over text nobody wrote by hand. It reads
`source_a.md` and `source_b.md` only. **A fixture's own `merged.md` is never
opened**, by anything, at any point in a run.

That is what makes the grading rule below necessary rather than merely
convenient.

**Every declared expectation on a forward probe is ignored.**
`expected_verdict`, `also_acceptable` and `expected_evidence_contains` all
describe the hand-written merge, and this harness is not looking at it. Each
`source_to_merged` probe is graded against one rule -- the verdict must be
SUPPORTED -- plus the *computed* grounding check verify already performs against
the document the model produced. So `dropped_claim` passes here and fails under
`run_verify`, on purpose: that asks whether the verify pass noticed the planted omission,
and this asks whether the merge model committed it.

Enforcing `expected_evidence_contains` would be worse than useless: 58 of the 121
forward probes declare one, and every declared span is a span of the
hand-written merge. A generated merge is free to write `30s` for `30 seconds`,
which is a notation change and silent by design (README.md, "Non-goals"), and
`contradiction/a-connect-timeout` declares `60` because the hand-written merge
silently took B's value -- so a merge that correctly surfaces both is SUPPORTED
quoting `30 seconds`, and would fail the assertion for being right.
`expected_evidence_source` needs no exclusion: no forward probe carries one.

Graded, per unit of (fixture, condition, sample):

  forward coverage   every source_to_merged probe must come back SUPPORTED
                     [headline]
  example leakage    raw substring scan of the generated text for merge.md's
                     worked example, run before decompose [headline]
  must_not_extract   GLOBAL.json plus the fixture's transferable assertions,
                     over the claims decomposed from the merge. Any-run rather
                     than modal [headline]
  reverse            claims from the merge verified against the two sources; a
                     MISSING claim was invented [advisory]
  grounding          as verify.py computes it [reported]

The reverse figure is advisory and `must_not_extract` is headline although both
ride the same decompose call, so the split needs defending rather than
asserting. They depend on different properties of that call. The reverse figure
is a rate whose denominator is the claim count, and the decompose runner measured claim
segmentation as the one unstable thing in the reference configuration
(`disjoint_sources/merged.md` at 18, 17, 18). `must_not_extract` is a pattern
search over claim texts: splitting one claim into two does not make a forbidden
sentence appear.

Usage:
    python3 tests/run_merge.py --dry-run
    python3 tests/run_merge.py --record tests/responses/m4
    python3 tests/run_merge.py --offline
    python3 tests/run_merge.py --fixture contradiction --condition off --samples 1

`--min-interval` is the local card's thermal gap, not a project default: add
`--min-interval 15` when recording against 127.0.0.1 and omit it against a
hosted endpoint. Serial either way -- concurrency would shrink Ollama's context
window and change what the prompt-budget figures mean.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
# Explicit rather than relying on `tests/` being sys.path[0] because this file
# was run as a script. It is also imported, and `journal` has to resolve either
# way.
sys.path.insert(0, str(ROOT / "tests"))

from llossless import config, merge, prompts  # noqa: E402
from llossless.cassette import (  # noqa: E402
    ConflictingCassettes, MissingCassette,
)
from llossless.client import (  # noqa: E402
    SEED,
    TEMPERATURE,
    CallBudgetExceeded,
    Client,
)
from llossless.config import ConfigError  # noqa: E402
from llossless.decompose import Claim, decompose_text  # noqa: E402
from llossless.provenance import Provenance  # noqa: E402
from llossless.verify import (  # noqa: E402
    ATTRIBUTION_ERROR,
    DEFAULT_BATCH,
    GROUNDED,
    MERGED_TO_SOURCES,
    NOT_GRADED,
    SOURCE_TO_MERGED,
    TRANSCRIPTION_ERROR,
    Verdict,
    verify_claims,
)

import journal  # noqa: E402  - tests/ is on the path
import stale_corpus  # noqa: E402  - which corpora are stale by ruling

# `run_all.UNMEASURED_EXIT`: everything measured passed and something was not
# measured -- here, the verify steps of a corpus stale by ruling.
UNMEASURED_EXIT = 3

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
GLOBAL_FILE = FIXTURES_DIR / "GLOBAL.json"

# This harness's corpus, one revision per directory. A fresh directory has no recorded
# sources, so `guard_sources` passes without `--mixed-sources` and the `run_verify` corpus
# next door is left alone. `Store._load_index` globs `*.json` non-recursively,
# so neither corpus can see the other, and `provenance.RECORDED_OUTPUT` already
# excludes the whole subtree from the dirty check.
CASSETTES = config.OFFLINE_CASSETTES / "m7"

# The generated document, under the name the forward prompt shows the model.
# Not `merged_generated.md`: keeping the name means this harness's forward prompt differs
# from `run_verify`'s in the document text alone, which is what makes the two
# comparable. The fixture's own file of this name is never read, so there is
# nothing for it to collide with -- see `unit_documents`.
# Every fixture is a pair, so this reads the two canonical names. From
# `merge.source_names` rather than written out: the merge pass names its own
# documents and this is a reader of that naming, not a second opinion on it.
SOURCES = merge.source_names(2)

MERGED = "merged.md"

# The one verdict a correct merge can produce on a fact taken from its own
# sources. See the module docstring for why nothing else is consulted.
FORWARD_EXPECTED = "SUPPORTED"

# thinking off / thinking on, the two conditions this harness compares.
CONDITIONS = ("off", "on")
THINKS = {"off": False, "on": True}

# Which model a step's call is billed to, for the journal. Both verify steps
# fall through to the verify role.
ROLES = {"merge": "merge", "decompose": "decompose"}

DEFAULT_SAMPLES = 3

# The steps of one unit, in the order they run, and the values the journal's
# `step` field takes. Recorded per unit because a failed *merge* takes all of
# that unit's forward probes out of the denominator at once, and a reader has to
# be able to tell that from a failed verify batch.
#
# Forward runs before decompose deliberately. The forward measurement is the
# headline and it makes no decompose call -- its claims are the fixtures'
# hand-written probe texts -- so putting it second means a decompose failure
# leaves the headline measured rather than erasing it.
STEPS = ("merge", "verify_forward", "decompose", "verify_reverse")

# How many units may error back to back before the sweep gives up. Three,
# because the thing this number has to separate is "one call went wrong" from
# "the endpoint is gone", and one is not evidence of the second.
#
# The first version had the limit effectively at one: `step` caught SchemaFailure and
# nothing else, so a single TransportError propagated out of `run_unit`, past
# the loop, into main's blanket handler, and exited 2 with no `sweep.json`
# written and every completed unit discarded. That happened three times in one
# sweep -- twice a transport fault, once a TierUnsupported -- and each time the
# cost was hours of GPU already spent, recoverable only because the cassettes
# were on disk and the journal could be resumed from.
#
# The other direction is a real cost too, which is why this is not simply
# "never abort". A dead endpoint with 15 s pacing and a 300 s timeout burns
# about five minutes per unit answering nothing, and 72 units of that is six
# hours. Three consecutive failures is roughly fifteen minutes of proof.
CONSECUTIVE_ERROR_LIMIT = 3

# A guard rather than the fix. The real defect is that
# `completion_tokens` is not the generation: ollama bills the reasoning trace
# to `prompt_tokens` and returns the text in a field of its own, so the figure
# compared against `max_tokens` understates a thinking-on call by 1.9x to 15.0x
# over this harness's corpus. Rebuilding token accounting to read the reasoning field
# is on the backlog and out of scope here. What is affordable now is a tripwire
# low enough that the understatement cannot hide a real overrun: at half the
# ceiling on the metric that exists, a 1.9x call is already over.
#
# It is live-only by construction. A replayed call reports zero completion
# tokens, so `--offline` never trips it -- which is why this is a guard on
# recording runs and not a check the corpora can demonstrate.
BUDGET_TRIPWIRE = 0.5

# Faults that end the sweep rather than one unit.
#
# The list is short and each entry earns its place by being a statement about
# the whole run rather than about one call. A replay miss means the corpus does
# not contain what this code asks for, and every later unit would miss for the
# same reason; continuing would report a subset of the suite as if it were the
# suite. --max-calls is a limit the operator set deliberately. A config error
# was true before the first call. MergeError means the mapping handed to the
# merge pass is not two sources, which is a fault in this harness rather than
# in an endpoint.
#
# Everything else -- transport faults, HTTP statuses, tier refusals, a body
# that will not parse -- errors the unit and the sweep goes on. Caught
# structurally rather than by class on purpose: naming TransportError here
# would import `transport` into a replay run, and "replay never opens a socket"
# is checked by watching the import graph (acceptance_replay_never_loads_the_
# transport_module), not asserted.
FATAL_TO_THE_RUN = (
    ConflictingCassettes, MissingCassette, CallBudgetExceeded, ConfigError, merge.MergeError,
)

# Two byte-identical merges under a flag that is supposed to change decoding is
# first a suspicion that the flag never reached the endpoint, and only then a
# finding about the model. What separates the two is evidence that the model
# actually thought.
#
# Not `completion_tokens`. That was the original discriminator and it was wrong
# for this endpoint: ollama returns qwen3's reasoning in a `reasoning` field
# beside `content` and bills only `content`, so the 2026-08-08 smoke pass saw
# 714 tokens off against 726 on for a call whose reasoning ran to 2901
# characters. A ratio test on those numbers would have called a working flag a
# harness fault. `client.reasoned` reads the response instead of the bill.
#
# Latency is the second signal and the weaker one -- it needs both calls to have
# been live, and it moves with load -- so it corroborates rather than decides.
# The same smoke pass measured 31.7 s off against 61.8 s on for the same merge;
# 1.25 is a floor well under that, chosen so a busy endpoint does not trip it.
# A fault is called only when *neither* signal is present, because a false
# harness fault blocks a four-hour run over nothing.
THINKING_LATENCY_RATIO = 1.25

GREEN, RED, YELLOW, DIM, BOLD, RESET = (
    "\033[32m",
    "\033[31m",
    "\033[33m",
    "\033[2m",
    "\033[1m",
    "\033[0m",
)


def colour(text: str, code: str, enabled: bool) -> str:
    return f"{code}{text}{RESET}" if enabled else text


# --------------------------------------------------------------------------
# fixtures
# --------------------------------------------------------------------------


def fixture_names() -> list[str]:
    """The fixture directories. GLOBAL.json is not one of them.

    `test_fixtures.py` validates one more unit than this returns, because
    GLOBAL.json holds cross-fixture assertions and has no sources, no merge and
    no probes. It contributes nothing to the sweep and nothing to the forward
    denominator. Said here because the two counts have been read as a
    discrepancy before. The number itself is not written down: `list_structure`
    made it fourteen and every figure derived from it moved with it.
    """
    return sorted(p.name for p in FIXTURES_DIR.iterdir() if p.is_dir())


def load_expected(fixture: str) -> dict:
    return json.loads((FIXTURES_DIR / fixture / "expected.json").read_text(encoding="utf-8"))


def load_sources(fixture: str) -> dict[str, str]:
    """The two source documents, and nothing else on disk."""
    return {
        name: (FIXTURES_DIR / fixture / name).read_text(encoding="utf-8")
        for name in SOURCES
    }


def unit_documents(fixture: str, merged: str) -> dict[str, str]:
    """The three documents a unit works over: two from disk, one from the model.

    The single place a `documents` mapping is built, so that "the fixture's own
    merged.md is never validated against" is a property of one function rather
    than a habit spread over the runner. `verify.locate` searches only the
    mapping it is handed, and this mapping's `merged.md` is the generated text,
    so a span quoted from the hand-written merge and absent from this one comes
    back a transcription error -- which is the correct reading of it.
    """
    return {**load_sources(fixture), MERGED: merged}


def forward_probes(expected: dict) -> list[dict]:
    return [p for p in expected["probes"] if p["direction"] == SOURCE_TO_MERGED]


def probe_claims(probes: list[dict]) -> list[Claim]:
    """Hand-written probes as claims, with the probe id as the join key.

    The same construction as `run_verify.probe_claims`, and repeated rather than
    imported for the reason the two runners repeat their report code:
    `run_verify` is a published measurement of its own and must not change shape
    because this harness wanted a helper. span and anchored carry no meaning here.
    """
    return [
        Claim(
            id=probe["probe_id"],
            source=probe["document"],
            text=probe["text"],
            line=probe["line"],
            span=probe["text"],
            anchored=True,
        )
        for probe in probes
    ]


def global_assertions() -> list[dict]:
    return json.loads(GLOBAL_FILE.read_text(encoding="utf-8"))["must_not_extract"]


def transferable(expected: dict, sources: dict[str, str]) -> list[dict]:
    """The fixture's `merged.md` assertions that describe *any* correct merge.

    A `must_not_extract` entry scoped to `merged.md` describes the hand-written
    merge, and most do not survive the move. `dropped_claim` forbids a JSON Lines
    claim because its merge omits the log format -- but a correct generated merge
    is *required* to carry that fact, so applying the assertion would punish the
    behaviour this harness is measuring.

    The rule is derived rather than a maintained exclusion list: **a `merged.md`
    `absent` assertion transfers iff its pattern matches neither source.** If the
    pattern matches a source, a correct merge must carry the text and the
    assertion contradicts the merge rules; if it matches neither, the text is
    absent from everything the model was shown and a claim of it is invention
    either way.

    `basis: not_a_claim` never transfers: it asserts that text present in one
    particular document must not become a claim, which is a statement about that
    document's prose and not about a merge of it.
    """
    out = []
    for assertion in expected.get("must_not_extract", []):
        if assertion.get("document") != MERGED or assertion.get("basis") != "absent":
            continue
        pattern = re.compile(assertion["pattern"])
        if any(pattern.search(text) for text in sources.values()):
            continue
        out.append(assertion)
    return out


def violations(claims: list[Claim], assertions: list[dict]) -> list[str]:
    """Which assertions the merge's claims matched. Empty is the only pass."""
    found = []
    for assertion in assertions:
        pattern = re.compile(assertion["pattern"])
        if any(pattern.search(claim.text) for claim in claims):
            found.append(assertion["assertion_id"])
    return found


# --------------------------------------------------------------------------
# one unit of work
# --------------------------------------------------------------------------


@dataclass
class ForwardResult:
    probe_id: str
    document: str
    verdict: Verdict | None  # None means the batch errored: not measured

    @property
    def ok(self) -> bool:
        return self.verdict is not None and self.verdict.verdict == FORWARD_EXPECTED

    @property
    def observed(self) -> str:
        return self.verdict.verdict if self.verdict else "ERROR"

    @property
    def grounding(self) -> str:
        return self.verdict.grounding if self.verdict else NOT_GRADED


def _slower(on: "Unit", off: "Unit") -> bool:
    """Did the thinking-on merge take materially longer than the thinking-off one?

    False whenever the question cannot be asked -- a cached or replayed merge
    has no latency of its own, and a zero would read as "fast" rather than "not
    measured". The caller treats that as no evidence, not as evidence against.

    `journal.measurable` rather than a second hand-written test of
    the same flags, so that this and `latency_summary` cannot drift apart.
    """
    if not journal.measurable(on, off) or not off.merge_seconds:
        return False
    return on.merge_seconds >= off.merge_seconds * THINKING_LATENCY_RATIO


@dataclass
class Unit:
    """One (fixture, condition, sample): a merge and everything checked about it."""

    fixture: str
    condition: str
    sample: int
    merged: str = ""
    forward: list[ForwardResult] = field(default_factory=list)
    claims: int = 0
    leaks: list[str] = field(default_factory=list)
    violated: list[str] = field(default_factory=list)
    invented: list[str] = field(default_factory=list)
    reverse_claims: int = 0
    completion_tokens: int = 0  # the merge call alone
    merge_reasoned: bool = False  # did the merge call come back with a reasoning block
    merge_cached: bool = False  # served from .llossless-cache: no latency to read
    merge_replayed: bool = False  # served from a cassette: the other disk path, same
    merge_seconds: float = 0.0  # the merge call alone, pacing included
    seconds: float = 0.0  # every step of the unit, pacing and repairs included
    repairs: int = 0  # attempt-2 successes across the unit: a schema the model got wrong once
    # What each role was actually allowed to do, read back off the client after
    # the call rather than recomputed from the settings. Two inputs decide it --
    # `settings.thinks(role)` and the per-call override this harness uses to run
    # the merge both ways -- so a record derived from either one alone can name a
    # configuration the arm did not run with.
    thinking: dict[str, bool] = field(default_factory=dict)
    budget_tripped: bool = False  # merge spend crossed BUDGET_TRIPWIRE; see the guard
    failed_step: str | None = None
    error: str | None = None
    # Why the verify steps have no reading: the corpus holds them under a
    # prompt HEAD no longer sends, and the operator has held the re-record
    # back. Not an error: merge and decompose still ran and replayed.
    unmeasured: str | None = None

    @property
    def errored(self) -> bool:
        return self.failed_step is not None

    @property
    def measured(self) -> list[ForwardResult]:
        return [f for f in self.forward if f.verdict is not None]

    @property
    def supported(self) -> int:
        return sum(f.ok for f in self.measured)

    @property
    def rate(self) -> float | None:
        return self.supported / len(self.measured) if self.measured else None

    @property
    def clean(self) -> bool:
        """Everything headline, for this one unit."""
        return (
            not self.errored
            and bool(self.measured)
            and self.supported == len(self.measured)
            and not self.leaks
            and not self.violated
        )


class Spend(NamedTuple):
    """What the client had spent when a step began. Diffed, never read alone.

    A step is one to three calls and a repaired call is two HTTP requests, so
    every per-step figure is a difference of counters rather than anything a
    single response reports. `replayed` joins `completion_tokens` here because
    the cassette branch of `_fetch` sets no `last_*` flag -- it increments this
    counter (`client.py:324`) and returns -- and a journal that cannot see it
    calls every replay a live call.
    """

    completion_tokens: int
    replayed: int


def spent(client: Client) -> Spend:
    return Spend(client.usage.completion_tokens, client.usage.replayed)


def run_unit(
    fixture: str,
    condition: str,
    sample: int,
    client: Client,
    loaded: dict[str, prompts.Prompt],
    batch_size: int,
    journal_file=None,
) -> Unit:
    """Merge, verify the merge forward, decompose it, verify it back. One unit.

    A step that errors stops the unit there and leaves the steps after it
    unmeasured. That is the honest shape: without a merge there is nothing to
    verify, and reporting the forward probes of a unit whose merge failed as
    anything at all would be reporting on a document that does not exist.
    """
    unit = Unit(fixture=fixture, condition=condition, sample=sample)
    expected = load_expected(fixture)
    sources = load_sources(fixture)
    client.sample = sample
    unit_started, unit_repairs = time.monotonic(), client.usage.repairs

    def step(name: str, call):
        started, before = time.monotonic(), spent(client)
        try:
            value = call()
        except MissingCassette as exc:
            # A miss on a corpus that is stale by the operator's ruling
            # leaves this step unmeasured and the unit going; any other miss
            # still ends the run, as it always has.
            stale = stale_corpus.deferred_reason(exc.directory, exc.role)
            if stale is None:
                raise
            unit.unmeasured = stale
            unit.seconds = time.monotonic() - unit_started
            return None
        except FATAL_TO_THE_RUN:
            raise
        except Exception as exc:  # noqa: BLE001 - one bad call errors one unit, not the run
            # The contract already written down for a SchemaFailure, now applied
            # to every other way a call can fail: name the step, drop this
            # unit's remaining probes from the denominator, journal it, and let
            # the sweep continue to exit 2 at the end. The type is kept in the
            # message because "the endpoint answered nothing" and "the model
            # answered something unparseable" read alike once they are strings.
            unit.failed_step, unit.error = name, f"{type(exc).__name__}: {exc}"
            unit.thinking[ROLES.get(name, "verify")] = client.last_thinking
            journal_step(journal_file, unit, name, client, started, before, "error")
            unit.seconds = time.monotonic() - unit_started
            unit.repairs = client.usage.repairs - unit_repairs
            return None
        if name == "merge":
            unit.completion_tokens = client.usage.completion_tokens - before.completion_tokens
            unit.merge_reasoned = client.last_reasoned
            unit.merge_cached = client.last_cached
            unit.merge_replayed = client.usage.replayed > before.replayed
            unit.merge_seconds = time.monotonic() - started
            unit.budget_tripped = (
                unit.completion_tokens
                >= BUDGET_TRIPWIRE * merge.budget_tokens(sources, client.settings.fidelity)
            )
        unit.thinking[ROLES.get(name, "verify")] = client.last_thinking
        journal_step(journal_file, unit, name, client, started, before, "ok")
        unit.seconds = time.monotonic() - unit_started
        unit.repairs = client.usage.repairs - unit_repairs
        return value

    # One policy for the whole unit, off `Settings`, so the level that sizes the
    # budget above is the level the merger is given and the level both graders
    # are told about. Three reads of `settings.fidelity` in one unit of work is
    # three chances for a report to describe a run that did not happen.
    policy = merge.MergePolicy.from_settings(client.settings)

    result = step(
        "merge",
        lambda: merge.merge_documents(
            client, sources, loaded["merge"], thinking=THINKS[condition], policy=policy
        ),
    )
    if result is None:
        return unit
    merged = result.document
    unit.merged = merged
    unit.leaks = merge.example_content_leaks(merged)

    documents = unit_documents(fixture, merged)
    probes = forward_probes(expected)

    verdicts = step(
        "verify_forward",
        lambda: {
            v.claim_id: v
            for v in verify_claims(
                client,
                probe_claims(probes),
                documents,
                SOURCE_TO_MERGED,
                loaded[SOURCE_TO_MERGED],
                batch_size,
                policy,
            )
        },
    )
    unit.forward = [
        ForwardResult(
            probe_id=probe["probe_id"],
            document=probe["document"],
            verdict=(verdicts or {}).get(probe["probe_id"]),
        )
        for probe in probes
    ]
    if verdicts is None and not unit.unmeasured:
        return unit

    extracted = step(
        "decompose",
        lambda: decompose_text(client, merged, MERGED, loaded["decompose"]),
    )
    if extracted is None:
        return unit
    unit.claims = len(extracted)
    unit.violated = violations(
        extracted, transferable(expected, sources) + global_assertions()
    )
    if unit.unmeasured:
        # The reverse call reads the same stale corpus; asking would only
        # miss again. Merge and decompose have replayed, which is what this
        # unit can still prove.
        return unit

    reverse = step(
        "verify_reverse",
        lambda: verify_claims(
            client,
            extracted,
            documents,
            MERGED_TO_SOURCES,
            loaded[MERGED_TO_SOURCES],
            batch_size,
            policy,
        ),
    )
    if reverse is None:
        return unit
    unit.reverse_claims = len(reverse)
    unit.invented = [v.claim_id for v in reverse if v.verdict == "MISSING"]
    return unit


def latency_summary(path: Path) -> None:
    """Per-condition generation latency, over live calls only.

    Pacing is subtracted, because a mean that includes it measures the interval
    the operator chose rather than anything about the endpoint. Cached and
    replayed steps are dropped entirely rather than counted as fast: they made
    no request, and averaging a microsecond in with a minute would make the next
    sweep's estimate optimistic in exactly the places a document repeats.

    Read back from the journal rather than accumulated in memory so a resumed
    run reports over its whole history and not just the part it re-ran.

    The cached exclusion is `journal.steps`' default rather than a
    filter written here. It used to be written here, and in `_slower`, and a
    third time in `analyse_merges` -- so the next metric added to this harness
    had to remember on its own, which is how the second one got it wrong.
    """
    entries = journal.records(path)
    if not entries:
        return
    live: dict[str, list[float]] = {}
    cached = len(entries) - len(journal.steps(entries))
    for record in journal.steps(entries):
        if record["outcome"] != "ok" or not record["seconds"]:
            continue
        live.setdefault(record["condition"], []).append(
            record["seconds"] - (record["gap_seconds"] or 0.0)
        )
    print("\n  Generation latency, pacing removed, live calls only")
    if not live:
        # Not silence. A latency block that vanishes on an all-replay run is
        # indistinguishable from one that was never wired up, and the reader
        # who scrolls past it learns nothing either way. Say the denominator.
        print(f"    no live calls in {len(entries)} journalled step(s); nothing to time")
        return
    for condition in CONDITIONS:
        seconds = live.get(condition)
        if seconds:
            print(
                f"    thinking {condition:3} ....... {len(seconds):3d} call(s)  "
                f"mean {sum(seconds) / len(seconds):5.1f}s  "
                f"min {min(seconds):5.1f}s  max {max(seconds):5.1f}s"
            )
    if cached:
        print(f"    {cached} cached step(s) excluded; they made no request")


def de_identified(message: str | None, client: Client) -> str | None:
    """An error message with the endpoint's hostname in it, minus the hostname.

    `settings.host` is allowed into a report because a report is read once by
    the operator who ran it. A journal is committed: `tests/responses/m7/
    journal.jsonl` ships with the corpus, and the first error recorded against a
    hosted pod put that pod's address into the repository. The console keeps the
    address -- an operator debugging a dead endpoint needs to know which one --
    and the file gets the same id the cassettes carry.
    """
    host = client.settings.host
    if not message or not host:
        return message
    return message.replace(host, f"<endpoint {client.settings.endpoint_id}>")


def journal_step(journal_file, unit: Unit, step: str, client: Client, started, before, outcome) -> None:
    """One JSONL record per step: everything needed to account for that step.

    Token and timing figures are diffed off `client.usage` rather than read from
    a response, because a repaired call is two HTTP requests and a *step* is what
    a reader is trying to account for. For the same reason `cassette_key` and
    `tier` are the last call the step made, not all of them: a verify step over
    three batches is three keys, and the one recorded is the last. The whole set
    is recoverable from the corpus, which is keyed by content; this field is a
    thread back into it, not an index of it.

    `gap_seconds` is the achieved interval before that last live call, and is
    null for a replayed or cached answer because there was no call to space out.

    `cached` is why `seconds` cannot be averaged as it stands. A cache hit
    returns in microseconds and reports no tokens, so a mean that includes one
    describes the disk rather than the endpoint -- the 2026-08-08 smoke pass
    journalled a decompose at 0.0 s because the generated merge happened to
    match a document an earlier decompose run had already decomposed. `latency_summary` drops them.
    """
    if journal_file is None:
        return
    role = ROLES.get(step, "verify")
    journal_file.write(
        json.dumps(
            {
                "fixture": unit.fixture,
                "condition": unit.condition,
                "sample": unit.sample,
                "step": step,
                "outcome": outcome,
                "role": role,
                "model": client.settings.model_for(role),
                "tier": client.last_tier,
                "cassette_key": client.last_key,
                "temperature": TEMPERATURE,
                "seed": SEED,
                "max_tokens": (
                    merge.budget_tokens(load_sources(unit.fixture), client.settings.fidelity)
                    if step == "merge"
                    else None
                ),
                # Read off the client, which sets it from the same variable it
                # puts in the cassette key. The line this replaces re-derived it
                # from the step name and so wrote `false` for decompose and
                # verify on every run, including the runs where `--thinking
                # decompose` had been passed and the calls did think.
                "thinking": client.last_thinking,
                # Deliberately *not* in the cassette key
                # (`cassette.py:113-126`): the same request answered slowly and
                # answered quickly is the same request, so keying on it would
                # split a corpus every time an operator raised the deadline. But
                # excluding it from the key is not a reason to exclude it from
                # the record. One timeout message was split into two exactly
                # because a slow endpoint and an absent one are different
                # diagnoses, and neither can be told from a `seconds` figure by
                # a reader who does not know what the deadline was.
                # `call_timeout`, not the stated field: unstated is `None`
                # and the record has to carry the number the call really
                # ran under, which is the backend's default.
                "timeout": client.settings.call_timeout,
                "seconds": round(time.monotonic() - started, 2),
                "completion_tokens": client.usage.completion_tokens - before.completion_tokens,
                "gap_seconds": round(client.last_gap, 2) if client.last_gap else None,
                "cached": client.last_cached,
                # The cassette branch of `_fetch` does not set
                # `cached`, so a journal carrying only that field calls every
                # replay a live call. `journal.recorded` reads the union.
                "replayed": client.usage.replayed - before.replayed,
                "reasoned": client.last_reasoned,
                "error": de_identified(unit.error, client) if outcome == "error" else None,
            }
        )
        + "\n"
    )
    journal_file.flush()


# --------------------------------------------------------------------------
# aggregation
# --------------------------------------------------------------------------


@dataclass
class Cell:
    """One (fixture, condition) across every sample."""

    fixture: str
    condition: str
    units: list[Unit] = field(default_factory=list)

    @property
    def errored(self) -> bool:
        return any(u.errored for u in self.units)

    @property
    def rates(self) -> list[float]:
        return [u.rate for u in self.units if u.rate is not None]

    @property
    def spread(self) -> str:
        measured = [u for u in self.units if u.measured]
        if not measured:
            return "not measured"
        return ", ".join(f"{u.supported}/{len(u.measured)}" for u in measured)

    @property
    def clean(self) -> bool:
        return bool(self.units) and all(u.clean for u in self.units)

    @property
    def disagreed(self) -> bool:
        """The samples do not agree on pass/fail. Neither passed nor failed."""
        return len({u.clean for u in self.units if not u.errored}) > 1

    @property
    def range(self) -> float:
        return max(self.rates) - min(self.rates) if self.rates else 0.0

    @property
    def mean(self) -> float | None:
        return sum(self.rates) / len(self.rates) if self.rates else None


@dataclass
class FixtureRun:
    fixture: str
    cells: dict[str, Cell]

    @property
    def units(self) -> list[Unit]:
        return [u for cell in self.cells.values() for u in cell.units]

    @property
    def errored(self) -> bool:
        return any(u.errored for u in self.units)

    @property
    def by_sample(self) -> dict[int, dict[str, Unit]]:
        pairs: dict[int, dict[str, Unit]] = {}
        for condition, cell in self.cells.items():
            for unit in cell.units:
                pairs.setdefault(unit.sample, {})[condition] = unit
        return pairs

    @property
    def identical(self) -> list[int]:
        """Samples where both conditions produced byte-identical merges.

        An explicit status, not a 0.0 delta. A zero would read as "measured, no
        difference"; `identical` says the comparison had no content to measure,
        which is a different and weaker statement.
        """
        return sorted(
            sample
            for sample, pair in self.by_sample.items()
            if set(pair) == set(CONDITIONS)
            and not any(u.errored for u in pair.values())
            and pair["off"].merged == pair["on"].merged
        )

    @property
    def suspect(self) -> list[int]:
        """Identical merges with no sign the thinking flag did anything.

        A harness fault, not a finding, and it blocks the run. Two signals, and
        it takes the absence of both: the thinking-on merge came back with no
        reasoning block, *and* it did not take materially longer than the
        thinking-off one. Either alone is evidence the model thought and the
        documents converged anyway, which is a real null result.

        `reasoned` survives replay, because a cassette stores the whole body.
        Latency does not, and neither does a cache hit, so those fall back to
        the reasoning signal alone rather than voting on no information.
        """
        pairs = self.by_sample
        return [
            sample
            for sample in self.identical
            if not pairs[sample]["on"].merge_reasoned
            and not _slower(pairs[sample]["on"], pairs[sample]["off"])
        ]

    @property
    def gap(self) -> float | None:
        """|off - on| in mean forward coverage. None when a condition is missing."""
        means = [self.cells[c].mean for c in CONDITIONS if c in self.cells]
        if len(means) != 2 or any(m is None for m in means):
            return None
        return abs(means[0] - means[1])

    @property
    def unresolved(self) -> bool:
        """Neither passed nor failed: the samples would not settle it.

        Two ways to land here. The samples disagree with each other on pass/fail,
        or the noise within a condition is larger than the difference between the
        conditions -- in which case any off-vs-on statement about this fixture is
        reading the noise.
        """
        if any(cell.disagreed for cell in self.cells.values()):
            return True
        gap = self.gap
        return gap is not None and max(c.range for c in self.cells.values()) > gap

    @property
    def status(self) -> str:
        if self.errored:
            return "ERROR"
        blind = [u for u in self.units if u.unmeasured]
        if blind:
            # What was measured decides FAIL; the verify half was not read
            # by ruling, so a fixture with nothing else wrong is UNMEASURED.
            seen = [u for u in self.units if not u.unmeasured]
            failing = (any(u.leaks or u.violated for u in blind)
                       or any(not u.clean for u in seen))
            return "FAIL" if failing else "UNMEASURED"
        if self.unresolved:
            return "unresolved"
        return "ok" if all(cell.clean for cell in self.cells.values()) else "FAIL"


def paired(runs: list[FixtureRun]) -> tuple[dict[str, int], int]:
    """Forward coverage per condition, over probes measured in *both*.

    An error in one condition and not the other gives the two conditions
    different denominators, and comparing 76 measured probes against 81 would
    attribute an error to the thinking flag. So the comparison is computed over
    the intersection, printed separately from the two per-condition figures and
    labelled as such.
    """
    supported = {c: 0 for c in CONDITIONS}
    total = 0
    for run in runs:
        if set(run.cells) != set(CONDITIONS):
            continue
        for pair in run.by_sample.values():
            if set(pair) != set(CONDITIONS):
                continue
            shared = set.intersection(
                *({f.probe_id for f in pair[c].measured} for c in CONDITIONS)
            )
            total += len(shared)
            for condition in CONDITIONS:
                supported[condition] += sum(
                    f.ok for f in pair[condition].measured if f.probe_id in shared
                )
    return supported, total


# --------------------------------------------------------------------------
# reporting
# --------------------------------------------------------------------------


def report(run: FixtureRun, use_colour: bool) -> None:
    marks = {
        "ERROR": colour("ERROR", YELLOW, use_colour),
        "unresolved": colour("unresolved", YELLOW, use_colour),
        "ok": colour("ok", GREEN, use_colour),
        "FAIL": colour("FAIL", RED, use_colour),
        "UNMEASURED": colour("UNMEASURED (verify not replayed)", YELLOW, use_colour),
    }
    print(f"\n{colour(run.fixture, BOLD, use_colour)} .. {marks[run.status]}")

    for condition in CONDITIONS:
        cell = run.cells.get(condition)
        if cell is None:
            continue
        claims = ", ".join(str(u.claims) for u in cell.units if not u.errored)
        print(
            f"    thinking {condition:<3}  forward {cell.spread:<18}"
            f"claims {claims or '-'}"
        )
        for unit in cell.units:
            head = f"      sample {unit.sample}  "
            if unit.errored:
                print(
                    head
                    + colour("errored", YELLOW, use_colour)
                    + f" at {unit.failed_step}: {(unit.error or '')[:88]}"
                )
            for probe in unit.measured:
                if probe.ok:
                    continue
                print(
                    f"{head}{probe.probe_id:<26}"
                    f"{colour(probe.observed, RED, use_colour)} (from {probe.document})"
                )
            if unit.leaks:
                print(
                    head
                    + colour(
                        f"prompt example leaked: {', '.join(unit.leaks)}", RED, use_colour
                    )
                )
            if unit.violated:
                print(
                    head
                    + colour(f"must_not_extract: {', '.join(unit.violated)}", RED, use_colour)
                )
            if unit.invented:
                print(
                    colour(
                        f"{head}{len(unit.invented)} claim(s) in neither source (advisory)",
                        DIM,
                        use_colour,
                    )
                )

    if run.identical:
        note = f"identical merge in sample(s) {', '.join(str(s) for s in run.identical)}"
        if run.suspect:
            note += " -- and the token counts say the flag did nothing"
        print(colour(f"    off vs on: {note}", YELLOW if run.suspect else DIM, use_colour))


def summarise(runs: list[FixtureRun], samples: int, conditions, use_colour: bool,
              abandoned: int = 0) -> None:
    units = [u for run in runs for u in run.units]
    errored = [u for u in units if u.errored]

    def pct(part: int, whole: int) -> str:
        return f"{part}/{whole}" + (f" ({part / whole:.0%})" if whole else "")

    print(f"\n{colour('Merge over the fixture set', BOLD, use_colour)}")
    print(
        colour(
            f"  {samples} sample(s) per condition. Forward coverage is over "
            f"source_to_merged probes\n  graded against SUPPORTED alone: the declared "
            f"verdicts describe the hand-written\n  merge, which this run never reads.",
            DIM,
            use_colour,
        )
    )
    if errored:
        steps = ", ".join(sorted({u.failed_step or "?" for u in errored}))
        print(
            colour(
                f"  ERRORED ............... {len(errored)} unit(s) hit an error "
                f"(at {steps}); their\n                        remaining probes are not "
                f"measured",
                YELLOW,
                use_colour,
            )
        )

    # Above every figure, not after them, and red rather than yellow. An errored
    # unit narrows a denominator; an abandoned run means the suite described
    # below is not the suite that was asked for, and the two are not the same
    # size of statement. The line printed at the moment of abandonment has
    # scrolled past by the time anyone reads the report, and `abandoned_units`
    # in the JSON is not where a person looks. So it is repeated here, where the
    # coverage it qualifies is.
    if abandoned:
        print(
            colour(
                f"\n  ABANDONED: {abandoned} unit(s) were never attempted. Every figure "
                f"below is over\n  the units that ran, which are a subset of the suite. "
                f"Re-run with --journal to\n  resume; the run exits 2 either way.\n",
                RED,
                use_colour,
            )
        )

    # In the marker form `run_all` reads, above the figures it qualifies. When
    # no unit's verify steps replayed, the three figures they make are not
    # printed at all: a 0/0 under a figure's own label would read as one.
    blind = [u for u in units if u.unmeasured]
    for reason in dict.fromkeys(u.unmeasured for u in blind):
        print(colour(
            f"  UNMEASURED: forward coverage, evidence grounded and the reverse "
            f"pass, over {sum(u.unmeasured == reason for u in blind)} of "
            f"{len(units)} unit(s) -- {reason}", YELLOW, use_colour))
    verified = [u for u in units if not u.unmeasured]

    if verified:
        print(f"  {colour('Forward coverage', BOLD, use_colour)}")
    for condition in (conditions if verified else ()):
        cells = [run.cells[condition] for run in runs if condition in run.cells]
        measured = sum(len(u.measured) for cell in cells for u in cell.units)
        supported = sum(u.supported for cell in cells for u in cell.units)
        print(f"    thinking {condition:<8} .... {pct(supported, measured)}")

    if len(conditions) == 2 and verified:
        supported, total = paired(runs)
        print(
            "    paired ............ "
            + "   ".join(f"{c}: {pct(supported[c], total)}" for c in CONDITIONS)
        )
        print(colour("      (over probes measured in both conditions)", DIM, use_colour))

    leaked = [u for u in units if u.leaks]
    violated = [u for u in units if u.violated]
    print(
        f"  Prompt-example leaks .. {len(leaked)} unit(s)"
        + (colour("  FAIL", RED, use_colour) if leaked else "")
    )
    print(
        f"  must_not_extract ...... {len(violated)} unit(s) violating"
        + (colour("  FAIL", RED, use_colour) if violated else "")
        + colour("   (any-run, not modal)", DIM, use_colour)
    )

    graded = [f for u in units for f in u.measured if f.grounding != NOT_GRADED]
    grounded = [f for f in graded if f.grounding == GROUNDED]
    if verified:
        print(f"  Evidence grounded ..... {pct(len(grounded), len(graded))}")
        print(
            f"    transcription error   "
            f"{len([f for f in graded if f.grounding == TRANSCRIPTION_ERROR])}"
        )
        print(
            f"    attribution error     "
            f"{len([f for f in graded if f.grounding == ATTRIBUTION_ERROR])}"
        )

        reverse_claims = sum(u.reverse_claims for u in units)
        invented = sum(len(u.invented) for u in units)
        print(
            f"  Reverse (advisory) .... {invented} claim(s) in neither source, "
            f"of {reverse_claims} extracted"
        )

    if len(conditions) == 2:
        identical = [run for run in runs if run.identical]
        every = [run for run in runs if len(run.identical) == samples]
        if identical:
            print(
                f"  Identical merges ...... {len(identical)} fixture(s), "
                f"{len(every)} in every sample"
            )
        if every and len(every) == len(runs):
            print(
                colour(
                    "    No measurable difference between the conditions on this suite.\n"
                    "    That is not the same as no difference: twelve fixtures at\n"
                    "    temperature 0 can fail to detect one.",
                    DIM,
                    use_colour,
                )
            )

    suspect = [run for run in runs if run.suspect]
    if suspect:
        print(
            colour(
                f"\n  HARNESS FAULT: {len(suspect)} fixture(s) produced identical merges "
                f"with\n  comparable completion_tokens. The thinking flag probably never "
                f"reached the\n  endpoint, so this run measures nothing.",
                RED,
                use_colour,
            )
        )

    over = [u for run in runs for u in run.units if u.budget_tripped]
    if over:
        worst = max(over, key=lambda u: u.completion_tokens)
        print(
            colour(
                f"\n  BUDGET GUARD: {len(over)} merge call(s) spent at least "
                f"{BUDGET_TRIPWIRE:.0%} of their token ceiling on billed completion "
                f"alone,\n  worst {worst.fixture} [{worst.condition}] sample "
                f"{worst.sample} at {worst.completion_tokens} tokens. That figure "
                f"excludes the\n  reasoning trace, which this endpoint bills elsewhere, "
                f"so the true spend is higher by\n  an unknown factor. Raise max_tokens "
                f"and re-record: these merges may be budget-limited\n  rather than "
                f"quality-limited, and nothing downstream can tell the difference.",
                RED,
                use_colour,
            )
        )

    unresolved = [run for run in runs if run.status == "unresolved"]
    if unresolved:
        print(f"\n  {colour('Unresolved', BOLD, use_colour)} (the samples would not settle it)")
        for run in unresolved:
            print(f"    {run.fixture}")

    left_out = sum(r.status == "UNMEASURED" for r in runs)
    print(f"\n  Fixtures clean ........ {pct(sum(r.status == 'ok' for r in runs), len(runs))}"
          + (f"  ({left_out} unmeasured, not counted)" if left_out else ""))
    if errored:
        print(
            colour(
                "\n  Figures above are over measured probes only. This run is "
                "inconclusive and\n  exits 2 regardless of what they said.",
                DIM,
                use_colour,
            )
        )


def dry_run_table(names: list[str], samples: int, conditions, batch: int,
                  fidelity: str, use_colour: bool) -> int:
    """The per-fixture plan: probes, call counts and the token budget, per unit.

    A table rather than a total, on purpose. `disjoint_sources`' claim band tops
    out at 70, three batches at 25, so its worst case is six calls where every
    other fixture takes four -- and the decompose corpus actually returned 17-18 claims
    for that document. The planned figure is the worst case, and the table is
    what makes the difference between plan and outcome visible now rather than at
    hour four.
    """
    print(
        f"\n{colour('Planned calls per sample per condition', BOLD, use_colour)}"
        f"  (batch {batch})"
    )
    print(
        f"  {'fixture':<22}{'fwd':>5}{'fwd calls':>11}{'merged band':>14}"
        f"{'rev calls':>11}{'calls/unit':>12}{'max_tokens':>12}"
    )
    total_probes = total_calls = 0
    for name in names:
        expected = load_expected(name)
        probes = len(forward_probes(expected))
        forward_calls = -(-probes // batch)
        band = expected["claim_count_band"][MERGED]
        reverse_calls = -(-band[1] // batch)
        per_unit = 1 + forward_calls + 1 + reverse_calls  # merge, fwd, decompose, rev
        total_probes += probes
        total_calls += per_unit
        print(
            f"  {name:<22}{probes:>5}{forward_calls:>11}{f'[{band[0]}, {band[1]}]':>14}"
            f"{reverse_calls:>11}{per_unit:>12}"
            f"{merge.budget_tokens(load_sources(name), fidelity):>12}"
        )
    print(f"  {'':<22}{total_probes:>5}{'':>11}{'':>14}{'':>11}{total_calls:>12}")

    planned = total_calls * samples * len(conditions)
    print(
        f"\n  {len(names)} fixtures (+1 GLOBAL), {total_probes} forward probes, "
        f"{total_calls} calls per sample per condition"
    )
    print(
        f"  {samples} sample(s) x {len(conditions)} condition(s) = {planned} calls, "
        f"worst case. No request was made."
    )
    return planned


# --------------------------------------------------------------------------
# JSON
# --------------------------------------------------------------------------


def digest(text: str) -> str:
    """Short sha256 of a generated merge, so two runs can be compared cheaply."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16] if text else ""


def write_json(
    path: Path,
    runs: list[FixtureRun],
    samples: int,
    provenance: Provenance,
    abandoned: int = 0,
) -> None:
    units = [u for run in runs for u in run.units]
    supported, total = paired(runs)
    path.write_text(
        json.dumps(
            {
                "provenance": provenance.as_dict(),
                "inconclusive": any(u.errored for u in units) or bool(abandoned),
                # Units the consecutive-failure abort never attempted. Zero on a
                # complete run. Distinct from an errored unit, which was tried
                # and failed: these were not tried, so the suite this file
                # describes is smaller than the suite that was asked for, and a
                # reader comparing coverage across runs has to know that.
                "abandoned_units": abandoned,
                "harness_fault": [r.fixture for r in runs if r.suspect],
                # The budget tripwire, per unit rather than per fixture: a
                # merge that crossed it may be budget-limited, and its coverage
                # figure means something weaker than the others'.
                "budget_tripped": [
                    f"{u.fixture}[{u.condition}]#{u.sample}"
                    for r in runs
                    for u in r.units
                    if u.budget_tripped
                ],
                "samples": samples,
                "grading": (
                    "every source_to_merged probe is graded against SUPPORTED alone; "
                    "expected_verdict, also_acceptable and expected_evidence_contains "
                    "describe the hand-written merge and are not consulted. No forward "
                    "probe declares an expected_evidence_source."
                ),
                "forward": {
                    "probes_declared": sum(len(u.forward) for u in units),
                    "probes_measured": sum(len(u.measured) for u in units),
                    "supported": sum(u.supported for u in units),
                    "paired_denominator": total,
                    "paired_supported": supported,
                },
                "headline": {
                    "example_leaks": [
                        f"{u.fixture}/{u.condition}/{u.sample}: {', '.join(u.leaks)}"
                        for u in units
                        if u.leaks
                    ],
                    "must_not_extract": [
                        f"{u.fixture}/{u.condition}/{u.sample}: {', '.join(u.violated)}"
                        for u in units
                        if u.violated
                    ],
                },
                "fixtures": [
                    {
                        "fixture": run.fixture,
                        "status": run.status,
                        "identical_samples": run.identical,
                        "units": [
                            {
                                "condition": u.condition,
                                "sample": u.sample,
                                "status": "error" if u.errored else "measured",
                                "failed_step": u.failed_step,
                                "error": u.error,
                                "forward_declared": len(u.forward),
                                "forward_measured": len(u.measured),
                                "forward_supported": u.supported,
                                "not_supported": [
                                    {"probe_id": f.probe_id, "verdict": f.observed}
                                    for f in u.measured
                                    if not f.ok
                                ],
                                "claims": u.claims,
                                "example_leaks": u.leaks,
                                "must_not_extract": u.violated,
                                "invented_claims": u.invented,
                                "reverse_claims": u.reverse_claims,
                                "merge_completion_tokens": u.completion_tokens,
                                "merged_sha256": digest(u.merged),
                                "thinking": u.thinking,
                                "schema_repairs": u.repairs,
                                "seconds": round(u.seconds, 2),
                            }
                            for u in run.units
                        ],
                    }
                    for run in runs
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


# --------------------------------------------------------------------------


def finished(path: Path | None) -> set[tuple[str, str, int]]:
    """Units a previous run already journalled to completion.

    Resumption is at unit granularity. A unit that errored or stopped partway is
    re-run, and its already-made calls come back from `.llossless-cache/` free
    -- still written through to `--record`, so a resumed sweep does not leave
    holes exactly where the first attempt succeeded.
    """
    if path is None or not path.exists():
        return set()
    done: set[tuple[str, str, int]] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if record.get("step") == STEPS[-1] and record.get("outcome") == "ok":
            done.add((record["fixture"], record["condition"], record["sample"]))
    return done


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--fixture", action="append", help="run one fixture; repeatable")
    parser.add_argument("--out", type=Path, help="write the full result here as JSON")
    parser.add_argument(
        "--journal",
        type=Path,
        help="append one JSONL record per step; read on restart to skip finished units",
    )
    parser.add_argument(
        "--merges",
        type=Path,
        help="write each generated merge here as .md (default: <record dir>/merges)",
    )
    parser.add_argument(
        "--condition",
        choices=(*CONDITIONS, "both"),
        default="both",
        help="thinking off, on, or both (default: both)",
    )
    parser.add_argument(
        "--batch",
        type=int,
        default=DEFAULT_BATCH,
        help=f"claims per verify call (default {DEFAULT_BATCH})",
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=DEFAULT_SAMPLES,
        help=f"repeats per condition (default {DEFAULT_SAMPLES})",
    )
    parser.add_argument("--no-colour", action="store_true")
    config.add_arguments(parser, offline_dir=CASSETTES)
    args = parser.parse_args(argv)

    use_colour = sys.stdout.isatty() and not args.no_colour
    conditions = CONDITIONS if args.condition == "both" else (args.condition,)

    names = args.fixture or fixture_names()
    missing = [name for name in names if not (FIXTURES_DIR / name).is_dir()]
    if missing:
        print(f"no such fixture: {', '.join(missing)}", file=sys.stderr)
        return 2
    if args.samples < 1:
        print("error: --samples must be at least 1", file=sys.stderr)
        return 2

    try:
        settings = config.resolve(args, offline_dir=CASSETTES)
        loaded = {
            "merge": prompts.load("merge"),
            "decompose": prompts.load("decompose"),
            SOURCE_TO_MERGED: prompts.load("verify"),
            MERGED_TO_SOURCES: prompts.load("verify_reverse"),
        }
    except (ConfigError, FileNotFoundError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    # Answered from the fixtures alone, before a Client exists. The plan is a
    # function of the corpus and the batch size and of nothing an endpoint would
    # say, so counting the calls by starting to make them would be building the
    # machinery in order to ask it a question it does not decide.
    if args.dry_run:
        dry_run_table(names, args.samples, conditions, args.batch,
                      settings.fidelity, use_colour)
        return 0

    client = Client(settings)
    started = time.monotonic()
    hashes = " ".join(f"{name[:6]}:{p.sha256[:8]}" for name, p in loaded.items())
    print(
        colour(
            f"merge  {settings.mode}  {settings.host} ({settings.where})  {hashes}",
            DIM,
            use_colour,
        )
    )

    merges_dir = args.merges or (
        settings.record_dir / "merges" if settings.record_dir else None
    )
    if merges_dir is not None:
        merges_dir.mkdir(parents=True, exist_ok=True)

    done = finished(args.journal)
    journal_file = args.journal.open("a", encoding="utf-8") if args.journal else None
    cells = {
        (name, condition): Cell(fixture=name, condition=condition)
        for name in names
        for condition in conditions
    }

    # sample outermost, conditions innermost: the two alternate every four to
    # six calls, the tightest interleave that keeps one fixture's pipeline
    # coherent. Thermal drift and endpoint load over a multi-hour run are then
    # spread across both conditions rather than correlating with one.
    #
    # Flattened into one list rather than three nested loops so that the
    # consecutive-failure abort is a plain `break`. A flag threaded back up
    # through three levels is the version of this that gets one level wrong.
    plan = [
        (sample, name, condition)
        for sample in range(args.samples)
        for name in names
        for condition in conditions
    ]
    consecutive = 0
    abandoned = 0

    try:
        for index, (sample, name, condition) in enumerate(plan):
            label = f"  sample {sample + 1}/{args.samples}  {name} [{condition}]"
            if (name, condition, sample) in done:
                print(
                    colour(f"{label}  already journalled, skipped", DIM, use_colour),
                    flush=True,
                )
                continue
            unit = run_unit(
                name, condition, sample, client, loaded, args.batch, journal_file
            )
            cells[(name, condition)].units.append(unit)
            if merges_dir is not None and unit.merged:
                (merges_dir / f"{name}-{condition}-{sample}.md").write_text(
                    unit.merged, encoding="utf-8"
                )
            print(
                colour(
                    f"{label}  {unit.supported}/{len(unit.measured)}"
                    + (f"  ERRORED at {unit.failed_step}" if unit.errored else "")
                    + ("  verify UNMEASURED" if unit.unmeasured else ""),
                    DIM,
                    use_colour,
                ),
                flush=True,
            )
            consecutive = consecutive + 1 if unit.errored else 0
            if consecutive >= CONSECUTIVE_ERROR_LIMIT:
                abandoned = len(plan) - index - 1
                print(
                    colour(
                        f"\n  ABANDONED: {consecutive} units errored back to back, the "
                        f"last at {unit.failed_step}.\n  {abandoned} unit(s) not attempted. "
                        f"Everything measured so far is reported below and\n  written to "
                        f"--out; the run exits 2. Re-run with --journal to resume.",
                        RED,
                        use_colour,
                    ),
                    flush=True,
                )
                break
    except MissingCassette as exc:
        print(f"\n{colour('replay miss', RED, use_colour)}: {exc}", file=sys.stderr)
        return 2
    except (CallBudgetExceeded, ConfigError) as exc:
        print(f"\n{colour('error', RED, use_colour)}: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # noqa: BLE001 - transport and endpoint faults are operational
        print(f"\n{colour('error', RED, use_colour)}: {exc}", file=sys.stderr)
        return 2
    finally:
        if journal_file is not None:
            journal_file.close()

    runs = [
        FixtureRun(fixture=name, cells={c: cells[(name, c)] for c in conditions})
        for name in names
    ]
    for run in runs:
        report(run, use_colour)
    summarise(runs, args.samples, conditions, use_colour, abandoned=abandoned)
    if args.journal:
        latency_summary(Path(args.journal))

    provenance = Provenance(
        settings=settings,
        client=client,
        roles=("merge", "decompose", "verify"),
        duration_seconds=time.monotonic() - started,
    )
    print()
    print(provenance.as_markdown())
    if merges_dir is not None:
        print(f"  merges -> {merges_dir}")
    if args.out:
        write_json(args.out, runs, args.samples, provenance, abandoned=abandoned)
        print(f"  -> {args.out}")

    tripped = any(u.budget_tripped for run in runs for u in run.units)
    if abandoned or tripped or any(run.errored for run in runs) or any(run.suspect for run in runs):
        return 2  # inconclusive supersedes the assertion result
    if any(run.status == "FAIL" for run in runs):
        return 1
    # Everything measured passed, and the verify half was not replayed:
    # a partial reading, which exit 0 would present as a whole one.
    return UNMEASURED_EXIT if any(run.status == "UNMEASURED" for run in runs) else 0


if __name__ == "__main__":
    sys.exit(main())
