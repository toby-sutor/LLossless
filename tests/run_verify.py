#!/usr/bin/env python3
"""Run the verify pass over every fixture probe and grade it against expected.json.

This is the entailment measurement. It is the verify pass *alone*: the claims fed to the
model are the fixtures' hand-written probe texts, not decompose output. That is
deliberate. Chaining the two passes would fold extraction quality into the
accuracy number, and a claim decompose never extracted would be scored here as a
verify failure. `run_decompose.py` measures extraction; this measures entailment,
and the end-to-end number is `run_merge.py`'s problem.

Graded, per probe:

  strict         the returned verdict equals expected_verdict
  lenient        the returned verdict is in {expected_verdict} u also_acceptable
  grounded       an evidenced verdict quoted a span actually present in the file
                 it named. Split three ways: grounded, transcription error (the
                 span is in no target file), attribution error (the span is real
                 but in a different file). The third is counted separately
                 because it is a different mistake with a different fix.
  evidence       every expected_evidence_contains span is in the returned evidence

A batch whose call could not be parsed *errors* every probe in it. Errored
probes leave the accuracy denominator entirely and the run exits 2 -- "did not
measure" rather than "measured badly", the same rule run_decompose.py follows.
A replay of a call named in `UNRECORDABLE` leaves its probes UNMEASURED, out of
every denominator, and a run whose only shortfall is that exits 3.

Usage:
    python3 tests/run_verify.py --offline
    python3 tests/run_verify.py --record tests/responses
    python3 tests/run_verify.py --dry-run
    python3 tests/run_verify.py --fixture paraphrase --fixture hallucination

`--min-interval` is the local card's thermal gap, not a project default: add
`--min-interval 30` when recording against 127.0.0.1 and omit it against a
hosted endpoint. Serial either way -- concurrency would shrink Ollama's context
window and change what the prompt-budget figures mean.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from llossless import config, prompts  # noqa: E402
from llossless.cassette import (  # noqa: E402
    ConflictingCassettes, MissingCassette,
)
from llossless.client import (  # noqa: E402
    CallBudgetExceeded,
    Client,
    DryRun,
)
from llossless.config import ConfigError  # noqa: E402
from llossless.decompose import Claim, normalise  # noqa: E402
from llossless.merge import MergePolicy  # noqa: E402
from llossless.parsing import VERDICTS  # noqa: E402
from llossless.provenance import Provenance  # noqa: E402
from llossless.verify import (  # noqa: E402
    ATTRIBUTION_ERROR,
    DEFAULT_BATCH,
    DIRECTIONS,
    FINDINGS,
    GROUNDED,
    NOT_GRADED,
    PROMPTS,
    TRANSCRIPTION_ERROR,
    Verdict,
    verify_claims,
)

# Beside this file: which corpora are stale by the operator's ruling.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import stale_corpus  # noqa: E402

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
DOCUMENTS = ("source_a.md", "source_b.md", "merged.md")

# How many times the whole fixture set is run. Three is the smallest number that
# can distinguish "the model says X" from "the model said X once": with two runs
# a disagreement has no majority and nothing to report but the disagreement.
DEFAULT_SAMPLES = 3

# A probe whose runs disagreed so completely that no verdict holds a majority.
# Not a verdict the model can return; it is what the measurement says when the
# model would not say one thing.
NO_MAJORITY = "NO-MAJORITY"

# The same contract `run_merge.py` carries. One bad call errors
# one fixture; the sweep goes on and exits 2 at the end. What ends the run is a
# fault that will be true of every later call too.
CONSECUTIVE_ERROR_LIMIT = 3

# Faults that end the sweep rather than one fixture. The list is `run_merge.py`'s
# minus MergeError, which this harness cannot raise, **plus DryRun**, which it
# can and `run_merge.py` cannot.
#
# DryRun is the one that does not transfer, and it is the reason this contract was
# not the copy-and-paste it was described as. `client.complete` raises it from
# inside the call to signal that --dry-run was asked for (`client.py:208`), so a
# catch-by-exclusion that did not name it would swallow the signal, record
# twelve fixtures as errored, and print a sweep report for a run that made no
# request. It is a statement about the whole run in the most literal sense: the
# run was never going to happen.
#
# Everything else -- transport faults, HTTP statuses, tier refusals, a body that
# will not parse -- errors the fixture. Caught structurally rather than by class
# so that naming TransportError here cannot import `transport` into a replay run.
FATAL_TO_THE_RUN = (ConflictingCassettes, DryRun, MissingCassette, CallBudgetExceeded, ConfigError)

# Requests the committed corpus holds no answer for, by full
# cassette key, and why. A replay that misses on one of these reports the probes
# of that call UNMEASURED with the reason -- never as a pass, never as a miss to
# fix by re-recording -- and every other miss stays fatal. Keyed by the key and
# not by fixture, so an edit that moves the request (a fixture, a prompt, the
# model) misses like any other change would.
#
# `attribution_invented`'s reverse call, its three sample keys: on
# Qwen/Qwen3.8-27B-FP8 it ran away in 7 of 8 attempts and the platform cut it.
RUNAWAY_27B = "a runaway on the 27B; not recordable: it ran away in 7 of 8 attempts and the platform cut it"
UNRECORDABLE: dict[str, str] = {
    "ac49a28a10a24b8caba1b8b5ee2b71b33eba6e56aa569534ca370ca83bfdf20d": RUNAWAY_27B,
    "0c7864835aa8e316b8d417b8dcafa2a82614e5a5d722aec7244e55360c0755ab": RUNAWAY_27B,
    "971961c0ce084b07af6e8138b2591812f500bcdb9b519dc6b0835bb0990a1256": RUNAWAY_27B,
}

# The exit code for a run whose only shortfall is an unmeasured probe:
# `run_all.UNMEASURED_EXIT`, the suite's "could have been checked and was not".
# An errored or failed run still exits 2 or 1; this never masks either.
UNMEASURED_EXIT = 3

# How many unmeasured probes the summary names one by one before it counts them.
NAMED_UNMEASURED = 6

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


@dataclass
class ProbeResult:
    """One probe, the verdict it got, and how that graded."""

    fixture: str
    probe_id: str
    direction: str
    document: str
    expected: str
    acceptable: list[str]
    expected_finding: str
    wants_evidence: list[str] | None
    wants_source: list[str] | None
    verdict: Verdict | None = None
    error: str | None = None
    # Why this probe has no reading, when its call is in `UNRECORDABLE`. Not an
    # error: nothing failed this run, the corpus has nothing to replay.
    unmeasured: str | None = None

    @property
    def observed(self) -> str:
        if self.unmeasured:
            return "UNMEASURED"
        return self.verdict.verdict if self.verdict else "ERROR"

    @property
    def strict_ok(self) -> bool:
        return self.verdict is not None and self.verdict.verdict == self.expected

    @property
    def lenient_ok(self) -> bool:
        return self.verdict is not None and self.verdict.verdict in (
            [self.expected] + self.acceptable
        )

    @property
    def finding_ok(self) -> bool:
        """The finding must be re-derived from the label that came back.

        Under lenient scoring numeric_drift's soft probe may legitimately return
        SUPPORTED, and the honest finding is then `none`, not the declared
        `contradicted`. SCHEMA.md says so explicitly; this is where it is checked
        rather than assumed.
        """
        if self.verdict is None:
            return False
        return self.verdict.finding == FINDINGS[(self.verdict.verdict, self.direction)]

    @property
    def evidence_ok(self) -> bool | None:
        """None when the probe declares no required substrings.

        Every declared span must be there. On a CONTRADICTED probe the spans
        are chosen so that only the contradicting value satisfies them, so this
        is the check that separates a model that read the conflicting value
        from one that quoted the claim back.

        An empty list is the absence of an expectation, not one of its own —
        the same as omitting the field, and written as `[]` with a
        `notes_evidence` beside it when a probe means "deliberately unasserted"
        rather than "nothing to say". It used to mean "the evidence must come
        back empty", which was redundant and double-counting: a MISSING verdict
        that quotes a span is already rejected by the parser, so the assertion
        could only ever fire on a probe that returned some other label, where
        the label is what is wrong and is already being scored.
        """
        if not self.wants_evidence or self.verdict is None:
            return None
        found = normalise(self.verdict.evidence)
        # A MISSING answer owes no span — the parser rejects one that quotes a
        # span anyway — so there is nothing here to grade. Not a pass: the label
        # is already being scored by strict and lenient, and counting it a
        # second time as an evidence failure would report one mistake twice.
        # Mirrors grounding, which is NOT_GRADED for the same reason.
        if self.verdict.verdict == "MISSING":
            return None
        return all(normalise(span) in found for span in self.wants_evidence)

    @property
    def source_ok(self) -> bool | None:
        """Did the model name a file the fact actually comes from?

        None when the probe declares no expectation. Distinct from grounding:
        grounding asks whether the span is in the file the model named, this
        asks whether that file is one of the right ones. A model can be grounded
        in source_b.md for a fact that source_a.md is the only home of, if it
        quoted something that happens to appear in both.

        Any one of the named files passes. Where a fact is stated in both
        sources there is no single correct answer to give, and demanding one
        would grade a coin toss. An empty list is again no expectation at all,
        for the reason given on evidence_ok.
        """
        if not self.wants_source or self.verdict is None:
            return None
        named = self.verdict.evidence_source
        if self.verdict.verdict == "MISSING":
            return None  # owes no filename either; see evidence_ok
        return named in self.wants_source

    @property
    def grounding(self) -> str:
        """One of verify's four grounding outcomes. NOT_GRADED for MISSING."""
        return self.verdict.grounding if self.verdict else NOT_GRADED


@dataclass
class FixtureResult:
    fixture: str
    probes: list[ProbeResult] = field(default_factory=list)
    # Whether this fixture plants no defect and must therefore come back clean.
    # Read from the fixture's own `kind`, never from a list kept here: a list is
    # a second place to forget a fixture, and forgetting one does not fail
    # loudly — it drops that fixture out of the guard denominator, which is the
    # number least worth flattering.
    guard: bool = False

    @property
    def errored(self) -> bool:
        return any(p.error for p in self.probes)


@dataclass
class ProbeSamples:
    """One probe across every run of the sweep.

    ProbeResult grades a verdict. This grades a model on a probe, which is not
    the same thing, and the difference is why it exists. Temperature 0 and a
    fixed seed are supposed to make this deterministic and do not, so a figure
    taken from a single run is a screenshot of one sample rather than a
    measurement. The modal verdict is what the model says about this probe;
    `stable` is whether it says it every time. Right-by-majority and
    right-three-times-out-of-three are different results and are reported as
    different results.
    """

    runs: list[ProbeResult]

    def __post_init__(self) -> None:
        first = self.runs[0]
        assert all((r.fixture, r.probe_id) == (first.fixture, first.probe_id) for r in self.runs)

    # The declared side of the probe is identical in every run: it comes from
    # expected.json, which no run touches. Read it off the first.
    @property
    def fixture(self) -> str:
        return self.runs[0].fixture

    @property
    def probe_id(self) -> str:
        return self.runs[0].probe_id

    @property
    def direction(self) -> str:
        return self.runs[0].direction

    @property
    def expected(self) -> str:
        return self.runs[0].expected

    @property
    def acceptable(self) -> list[str]:
        return self.runs[0].acceptable

    @property
    def wants_evidence(self) -> list[str] | None:
        return self.runs[0].wants_evidence

    @property
    def wants_source(self) -> list[str] | None:
        return self.runs[0].wants_source

    # -- what the runs actually did -------------------------------------

    @property
    def observed(self) -> list[str]:
        return [r.observed for r in self.runs]

    @property
    def counts(self) -> Counter:
        return Counter(self.observed)

    @property
    def modal(self) -> str:
        """The verdict a strict majority of runs gave, or NO_MAJORITY.

        Majority, not plurality. With three runs and three labels a 1-1-1 split
        is reachable, and calling one of those three "the model's answer"
        because Counter happened to see it first would be inventing a result.
        """
        label, n = self.counts.most_common(1)[0]
        return label if n * 2 > len(self.runs) else NO_MAJORITY

    @property
    def stable(self) -> bool:
        return len(self.counts) == 1

    @property
    def errored(self) -> bool:
        return any(r.error for r in self.runs)

    @property
    def unmeasured(self) -> str | None:
        """The reason, when any run of this probe had no recording to replay."""
        return next((r.unmeasured for r in self.runs if r.unmeasured), None)

    @property
    def modal_runs(self) -> list[ProbeResult]:
        return [r for r in self.runs if r.observed == self.modal]

    @property
    def spread(self) -> str:
        """`SUPPORTED x2, MISSING x1` — what varied, for the flag line."""
        return ", ".join(f"{label} x{n}" for label, n in self.counts.most_common())

    # -- grading, always against the modal verdict ----------------------

    @property
    def strict_ok(self) -> bool:
        return self.modal == self.expected

    @property
    def lenient_ok(self) -> bool:
        return self.modal in [self.expected] + self.acceptable

    @property
    def finding_ok(self) -> bool:
        return bool(self.modal_runs) and all(r.finding_ok for r in self.modal_runs)

    @property
    def graded_runs(self) -> list[ProbeResult]:
        """Modal runs whose verdict owed a span. MISSING owes none."""
        return [r for r in self.modal_runs if r.grounding != NOT_GRADED]

    @property
    def grounding(self) -> str | None:
        """The worst grounding any modal run reached, or None if none was graded.

        Pessimistic on purpose. A model that fabricates a span in one run out of
        three is a model that fabricates spans; averaging that away would hide
        exactly the failure this check was built for. Worst means furthest from
        having quoted the document: a span that exists nowhere is a fabrication,
        a span in the wrong file is a real quote wrongly attributed, and the
        first is the deeper fault.

        None when the modal verdict was MISSING — nothing was quoted, so nothing
        was located — and also when there was no majority at all, because `max`
        over no runs would otherwise have to invent an answer.
        """
        order = (TRANSCRIPTION_ERROR, ATTRIBUTION_ERROR, GROUNDED)
        graded = self.graded_runs
        return min((r.grounding for r in graded), key=order.index) if graded else None

    @property
    def grounded(self) -> bool:
        """Located, in the file it named, in every modal run.

        False when nothing was graded. A MISSING probe is not grounded and is
        not ungrounded either; callers that care read `grounding`, and the
        summary counts only probes where `grounding` is not None.
        """
        return self.grounding == GROUNDED

    @property
    def grounding_stable(self) -> bool:
        return len({r.grounding for r in self.runs if r.verdict is not None}) <= 1

    @property
    def evidence_shown(self) -> tuple[str, str]:
        """The span and file a reader needs to audit this probe by hand.

        Taken from the first modal run, which is the one the reported verdict
        stands on. Empty when there is nothing to show.
        """
        for run in self.modal_runs:
            if run.verdict is not None and run.verdict.evidence:
                return run.verdict.evidence, run.verdict.evidence_source
        return "", ""

    @property
    def evidence_ok(self) -> bool | None:
        """None when the probe declares no required substring, or none was graded.

        A run that owed no span grades to None rather than to False, and folding
        that into `all()` would turn "not asked" into "failed". So the ungraded
        runs are dropped and a probe with nothing left is itself ungraded — the
        same rule ProbeResult applies one level down.
        """
        if not self.wants_evidence or not self.modal_runs:
            return None
        graded = [r.evidence_ok for r in self.modal_runs if r.evidence_ok is not None]
        return all(graded) if graded else None

    @property
    def source_ok(self) -> bool | None:
        """None when the probe declares no expected source file, or none was graded."""
        if not self.wants_source or not self.modal_runs:
            return None
        graded = [r.source_ok for r in self.modal_runs if r.source_ok is not None]
        return all(graded) if graded else None

    @property
    def rationale_conflicts(self) -> list[str]:
        """Labels this probe's rationales named while returning something else.

        Every run, not the modal ones, and it grades nothing. A model that
        reasons its way to CONTRADICTED and files MISSING has said something
        worth reading about the prompt, and it says it just as loudly in the run
        that lost the vote. See parsing.rationale_conflicts for why acting on it
        automatically would be the wrong move.
        """
        return sorted(
            {
                label
                for r in self.runs
                if r.verdict is not None
                for label in r.verdict.rationale_names
            }
        )


@dataclass
class FixtureSamples:
    fixture: str
    guard: bool
    probes: list[ProbeSamples]

    @property
    def errored(self) -> bool:
        return any(p.errored for p in self.probes)

    @property
    def unmeasured(self) -> list[ProbeSamples]:
        return [p for p in self.probes if p.unmeasured]

    @property
    def ok(self) -> bool:
        """Every measured probe passed. Unmeasured probes are neither side of this.

        A fixture with unmeasured probes is left out of "Fixtures clean" by the
        caller, so `ok` here never counts it as clean.
        """
        if self.errored:
            return False
        graded = [p for p in self.probes if not p.unmeasured]
        return all(p.lenient_ok and p.finding_ok for p in graded) and all(
            p.evidence_ok is not False and p.source_ok is not False for p in graded
        )

    @property
    def unstable(self) -> list[ProbeSamples]:
        return [p for p in self.probes if not p.stable]


def aggregate(sweeps: list[list[FixtureResult]]) -> list[FixtureSamples]:
    """Zip N runs of the fixture set into one record per probe.

    Fixture and probe order come from the first sweep, so the report reads the
    same however many samples were taken.
    """
    slots: dict[str, dict[str, list[ProbeResult]]] = {}
    guards: dict[str, bool] = {}
    for sweep in sweeps:
        for result in sweep:
            by_probe = slots.setdefault(result.fixture, {})
            guards.setdefault(result.fixture, result.guard)
            for probe in result.probes:
                by_probe.setdefault(probe.probe_id, []).append(probe)
    return [
        FixtureSamples(
            fixture=name,
            guard=guards[name],
            probes=[ProbeSamples(runs=runs) for runs in by_probe.values()],
        )
        for name, by_probe in slots.items()
    ]


def probe_claims(probes: list[dict]) -> list[Claim]:
    """Turn hand-written probes into claims, with the probe id as the join key.

    span and anchored carry no meaning here -- they are decompose's way of
    earning belief in a line number, and these lines came from a human. Setting
    span to the probe text keeps the dataclass honest rather than blank.
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


# The level this corpus was recorded at, pinned rather than left to the default.
#
# `verify_claims` falls back to `MergePolicy()` when no policy is passed, and
# for as long as the default was `off` that fallback silently agreed with the
# 135 recorded `off` cassettes this sweep replays. The default moved to
# `high` and all 135 went to keys that were never recorded -- measured, not
# guessed: re-keying each of them with the high fragment substituted produced
# 135 misses and 0 hits.
#
# So the sweep says which level it is replaying instead of inheriting one. That
# is the more honest shape whatever the default is: the corpus is a recording
# made at a particular level, and a harness that reads the level from a constant
# somebody else is free to change was relying on a coincidence.
CORPUS_LEVEL = "off"


def run_fixture(
    name: str,
    client: Client,
    loaded: dict[str, prompts.Prompt],
    batch_size: int,
) -> FixtureResult:
    directory = FIXTURES_DIR / name
    expected = json.loads((directory / "expected.json").read_text(encoding="utf-8"))
    documents = {doc: (directory / doc).read_text(encoding="utf-8") for doc in DOCUMENTS}
    result = FixtureResult(fixture=name, guard=expected.get("kind") == "guard")

    for direction in DIRECTIONS:
        probes = [p for p in expected["probes"] if p["direction"] == direction]
        if not probes:
            continue

        claims = probe_claims(probes)
        prompt = loaded[direction]

        try:
            verdicts = {
                v.claim_id: v
                for v in verify_claims(
                    client, claims, documents, direction, prompt, batch_size,
                    policy=MergePolicy(fidelity=CORPUS_LEVEL),
                )
            }
            error = unmeasured = None
        except MissingCassette as exc:
            # Two misses are not faults: a call nobody could record, and
            # a corpus recorded under a prompt HEAD no longer sends, whose
            # re-record the operator has held back. Every other miss
            # still ends the run.
            stale = stale_corpus.deferred_reason(exc.directory, exc.role)
            if exc.key not in UNRECORDABLE and stale is None:
                raise
            verdicts, error = {}, None
            unmeasured = UNRECORDABLE.get(exc.key) or stale
        except FATAL_TO_THE_RUN:
            raise
        except Exception as exc:  # noqa: BLE001 - one bad call errors one fixture
            # Once `except SchemaFailure`, which meant a model that
            # answered unparseably cost one direction of one fixture while an
            # endpoint that dropped a connection cost the whole sweep -- the
            # more recoverable fault treated as the less recoverable one. The
            # type is kept in the message because "the endpoint answered
            # nothing" and "the model answered something unparseable" read alike
            # once they are strings.
            verdicts, error, unmeasured = {}, f"{type(exc).__name__}: {exc}", None

        for probe in probes:
            result.probes.append(
                ProbeResult(
                    fixture=name,
                    probe_id=probe["probe_id"],
                    direction=direction,
                    document=probe["document"],
                    expected=probe["expected_verdict"],
                    acceptable=list(probe.get("also_acceptable", [])),
                    expected_finding=probe["expected_finding"],
                    wants_evidence=probe.get("expected_evidence_contains"),
                    wants_source=probe.get("expected_evidence_source"),
                    verdict=verdicts.get(probe["probe_id"]),
                    error=error,
                    unmeasured=unmeasured,
                )
            )

    return result


def report(result: FixtureSamples, use_colour: bool) -> None:
    if result.errored:
        mark = colour("ERROR", YELLOW, use_colour)
    elif not result.ok:
        mark = colour("FAIL", RED, use_colour)
    elif result.unmeasured:
        # Not "ok": what was measured passed, and the rest was never read.
        rest = ("none measured" if len(result.unmeasured) == len(result.probes)
                else "the rest ok")
        mark = colour(f"UNMEASURED ({len(result.unmeasured)} probe(s)); "
                      f"{rest}", YELLOW, use_colour)
    else:
        mark = colour("ok", GREEN, use_colour)
    guard = colour(" [guard]", DIM, use_colour) if result.guard else ""
    unstable = (
        colour(f"  {len(result.unstable)} unstable", YELLOW, use_colour)
        if result.unstable
        else ""
    )
    print(f"\n{colour(result.fixture, BOLD, use_colour)}{guard} .. {mark}{unstable}")

    # One call carries a whole direction's probes, so the same
    # message would repeat on eight lines; it is printed once per distinct
    # message instead. Printed at all because the error contract keeps the
    # exception type in the text precisely so a reader can tell a dead endpoint
    # from an unparseable answer, and a report that stored it and never showed
    # it would leave that distinction in the JSON only.
    seen: list[str] = []
    for probe in result.probes:
        for run in probe.runs:
            if run.error and run.error not in seen:
                seen.append(run.error)
    for message in seen:
        print(f"    {colour('errored', YELLOW, use_colour)}  {message}")

    for probe in result.probes:
        if probe.errored:
            print(
                f"    {probe.probe_id:<22} {colour('errored', YELLOW, use_colour)}"
                f"  not measured"
            )
            continue
        if probe.unmeasured:
            print(
                f"    {probe.probe_id:<22} {colour('UNMEASURED', YELLOW, use_colour)}"
                f"  {probe.unmeasured}"
            )
            continue

        if probe.strict_ok:
            status = colour("ok     ", GREEN, use_colour)
        elif probe.lenient_ok:
            status = colour("lenient", YELLOW, use_colour)
        else:
            status = colour("WRONG  ", RED, use_colour)

        note = ""
        if not probe.strict_ok:
            note = f"  got {probe.modal}, expected {probe.expected}"
            if probe.lenient_ok:
                note += " (also acceptable)"
        if not probe.stable:
            note += colour(f"  [unstable: {probe.spread}]", YELLOW, use_colour)
        if probe.grounding == TRANSCRIPTION_ERROR:
            note += colour("  [evidence found in no target file]", RED, use_colour)
        elif probe.grounding == ATTRIBUTION_ERROR:
            note += colour("  [evidence real, wrong file named]", RED, use_colour)
        # False, not falsy: None means the probe asserted nothing about evidence
        # and there is nothing to report either way.
        if probe.evidence_ok is False:
            note += colour(f"  [evidence lacks {probe.wants_evidence!r}]", RED, use_colour)
        if probe.source_ok is False:
            note += colour(
                f"  [named the wrong source file, expected "
                f"{' or '.join(probe.wants_source)}]",
                RED,
                use_colour,
            )

        print(f"    {probe.probe_id:<22} {status}{note}")

        # A CONTRADICTED finding is the one a human is asked to act on, so the
        # span it rests on is printed rather than filed in the JSON. Before
        # evidence_source existed there was nothing to print: the pass reported
        # that something conflicted and not what said so.
        if probe.modal == "CONTRADICTED":
            span, source = probe.evidence_shown
            if span:
                print(colour(f"        {source}: {span!r}", DIM, use_colour))


def matrix(probes: list[ProbeSamples], use_colour: bool) -> None:
    """Expected against modal. Where the pass is wrong matters as much as how often."""
    counts: Counter = Counter((p.expected, p.modal) for p in probes
                              if not p.errored and not p.unmeasured)
    if not counts:
        return
    # NO_MAJORITY gets a column only when a probe actually landed there. A
    # permanently empty column would read as a category the model can return.
    columns = list(VERDICTS) + ([NO_MAJORITY] if any(o == NO_MAJORITY for _, o in counts) else [])
    width = max(len(v) for v in columns) + 2
    print(f"\n  {colour('expected \\ modal', DIM, use_colour)}")
    print("  " + " " * 14 + "".join(f"{v:>{width}}" for v in columns))
    for expected in VERDICTS:
        cells = []
        for observed in columns:
            n = counts[(expected, observed)]
            if not n:
                cells.append(colour(f"{'.':>{width}}", DIM, use_colour))
                continue
            text = f"{n:>{width}}"
            cells.append(colour(text, GREEN if expected == observed else RED, use_colour))
        print(f"  {expected:<14}" + "".join(cells))


def summarise(results: list[FixtureSamples], samples: int, use_colour: bool,
              abandoned: int = 0) -> None:
    probes = [p for r in results for p in r.probes]
    measured = [p for p in probes if not p.errored and not p.unmeasured]
    errored = [p for p in probes if p.errored]
    unmeasured = [p for p in probes if p.unmeasured and not p.errored]

    def pct(part: int, whole: int) -> str:
        return f"{part}/{whole}" + (f" ({part / whole:.0%})" if whole else "")

    # Every probe whose modal verdict owed a span: SUPPORTED and CONTRADICTED
    # both assert the reference text says something. CONTRADICTED was outside
    # this denominator until evidence_source landed, which meant the finding a
    # human is asked to act on was the one nothing checked.
    evidenced = [p for p in measured if p.grounding is not None]
    grounded = [p for p in evidenced if p.grounding == GROUNDED]
    attribution = [p for p in evidenced if p.grounding == ATTRIBUTION_ERROR]
    transcription = [p for p in evidenced if p.grounding == TRANSCRIPTION_ERROR]
    declared = [p for p in measured if p.evidence_ok is not None]
    sourced = [p for p in measured if p.source_ok is not None]
    unstable = [p for p in measured if not p.stable]

    print(f"\n{colour('Verify over the fixture probe set', BOLD, use_colour)}")

    # Inside the report block and above every figure in it, not after them, and
    # red rather than yellow. An errored probe narrows a denominator; an
    # abandoned run means the suite described below is not the suite that was
    # asked for, and the two are not the same size of statement. The line
    # printed at the moment of abandonment has scrolled past by the time anyone
    # reads the report, and `abandoned_units` in the JSON is not where a person
    # looks. So it is repeated here, where the coverage it qualifies is.
    if abandoned:
        print(
            colour(
                f"  ABANDONED: {abandoned} unit(s) were never attempted. Every figure "
                f"below is over\n  the units that ran, which are a subset of the suite. "
                f"Re-run to resume; the\n  run exits 2 either way.\n",
                RED,
                use_colour,
            )
        )
    print(
        colour(
            f"  {samples} run(s) per call; every figure below is over the modal verdict.",
            DIM,
            use_colour,
        )
    )
    if errored:
        print(
            colour(
                f"  ERRORED ............... {len(errored)} probe(s) not measured",
                YELLOW,
                use_colour,
            )
        )
    # Above the figures, like ERRORED, and in the marker form `run_all` reads:
    # each figure below is over fewer probes than the fixtures declare, and a
    # reader must see that before the percentages rather than after them.
    for reason in dict.fromkeys(p.unmeasured for p in unmeasured):
        these = [p for p in unmeasured if p.unmeasured == reason]
        # Named one by one while that is readable; a whole stale corpus
        # is every probe, and a line naming 160 of them is not.
        named = (", ".join(f"{p.fixture}/{p.probe_id}" for p in these)
                 if len(these) <= NAMED_UNMEASURED else
                 f"{len(these)} probe(s) across "
                 f"{len({p.fixture for p in these})} fixture(s)")
        print(colour(f"  UNMEASURED: {named} -- {reason}", YELLOW, use_colour))
    print(f"  Strict accuracy ....... {pct(sum(p.strict_ok for p in measured), len(measured))}")
    print(f"  Lenient accuracy ...... {pct(sum(p.lenient_ok for p in measured), len(measured))}")
    print(f"  Findings derived ...... {pct(sum(p.finding_ok for p in measured), len(measured))}")
    print(
        f"  Evidence grounded ..... {pct(len(grounded), len(evidenced))}  "
        f"(of SUPPORTED and CONTRADICTED)"
    )
    # Never folded into the line above. A transcription error means the model
    # wrote a quotation that does not exist; an attribution error means the
    # quotation is real and the claim about where it came from is not. One is a
    # fabrication and one is a bookkeeping fault, and a single "ungrounded"
    # figure would report a model with either as a model with both.
    print(
        f"    transcription error . {len(transcription)}  (span is in no target file)"
    )
    print(
        f"    attribution error ... {len(attribution)}  (span is real, wrong file named)"
    )
    print(
        f"  Evidence as declared .. "
        f"{pct(sum(bool(p.evidence_ok) for p in declared), len(declared))}"
    )
    if sourced:
        # Only disjoint_sources declares this, because it is the only fixture
        # whose two sources share no facts, so it is the only one where "which
        # file did this come from" has a single right answer to grade against.
        print(
            f"  Source file named ..... "
            f"{pct(sum(bool(p.source_ok) for p in sourced), len(sourced))}  "
            f"(of probes declaring one)"
        )

    print(
        f"  Verdict stability ..... "
        f"{pct(len(measured) - len(unstable), len(measured))}  "
        f"(identical across {samples} run(s))"
    )

    for direction in DIRECTIONS:
        subset = [p for p in measured if p.direction == direction]
        print(f"  {direction:<21} {pct(sum(p.strict_ok for p in subset), len(subset))} strict")

    # A fixture with an unmeasured probe is neither clean nor not: it leaves
    # both denominators, and the note says how many did.
    whole = [r for r in results if not r.unmeasured]
    partial = len(results) - len(whole)
    left_out = f"  ({partial} partly unmeasured, not counted)" if partial else ""
    guards = [r for r in whole if r.guard]
    clean = [r for r in guards if r.ok]
    print(f"  Guard fixtures clean .. {pct(len(clean), len(guards))}  (no over-flagging)")
    print(f"  Fixtures clean ........ {pct(sum(r.ok for r in whole), len(whole))}{left_out}")

    matrix(probes, use_colour)

    if unstable:
        # Listed individually, never rolled into the accuracy figure. A probe
        # that answers differently run to run has not been measured to within
        # one probe, and the headline number cannot say so on its own.
        print(f"\n  {colour(f'Unstable across {samples} runs', BOLD, use_colour)}")
        for probe in unstable:
            graded = "modal correct" if probe.strict_ok else colour("modal WRONG", RED, use_colour)
            print(f"    {probe.fixture}/{probe.probe_id:<24} {probe.spread}  ({graded})")

    conflicted = [p for p in measured if p.rationale_conflicts]
    if conflicted:
        # A diagnostic, not a deduction. Nothing above moved because of this,
        # and nothing should: the fix is to the prompt, by a human reading it.
        print(f"\n  {colour('Rationale named a label other than the verdict', BOLD, use_colour)}")
        for probe in conflicted:
            print(
                f"    {probe.fixture}/{probe.probe_id:<24} returned {probe.modal}, "
                f"rationale names {', '.join(probe.rationale_conflicts)}"
            )

    shaky = [p for p in measured if p.stable and not p.grounding_stable]
    if shaky:
        print(
            f"\n  {colour('Same verdict, evidence grounding varied', BOLD, use_colour)}"
        )
        for probe in shaky:
            print(f"    {probe.fixture}/{probe.probe_id}")

    if errored:
        print(
            colour(
                "\n  Percentages above are over measured probes only. "
                "This run is inconclusive.",
                DIM,
                use_colour,
            )
        )


def write_json(
    path: Path, results: list[FixtureSamples], samples: int, provenance: Provenance,
    abandoned: int = 0,
) -> None:
    probes = [p for r in results for p in r.probes]
    measured = [p for p in probes if not p.errored and not p.unmeasured]
    unstable = [p for p in measured if not p.stable]
    path.write_text(
        json.dumps(
            {
                "provenance": provenance.as_dict(),
                "inconclusive": any(p.errored for p in probes) or bool(abandoned),
                "abandoned_units": abandoned,
                "samples": samples,
                # No recording exists to replay, by name and why.
                "unmeasured": [
                    {"probe": f"{p.fixture}/{p.probe_id}", "reason": p.unmeasured}
                    for p in probes if p.unmeasured and not p.errored
                ],
                "accuracy": {
                    "probes_measured": len(measured),
                    "probes_not_measured": len(probes) - len(measured),
                    "strict": sum(p.strict_ok for p in measured),
                    "lenient": sum(p.lenient_ok for p in measured),
                    "stable": len(measured) - len(unstable),
                    "unstable": [f"{p.fixture}/{p.probe_id}" for p in unstable],
                    # Deliberately outside every count above: this one is read,
                    # not scored. See parsing.rationale_conflicts.
                    "rationale_conflicts": [
                        f"{p.fixture}/{p.probe_id}"
                        for p in measured
                        if p.rationale_conflicts
                    ],
                },
                "grounding": {
                    "evidenced": len([p for p in measured if p.grounding is not None]),
                    "grounded": len([p for p in measured if p.grounding == GROUNDED]),
                    # Listed by name, not counted. Both are faults a human has
                    # to read the span to understand, and a bare count sends
                    # nobody anywhere.
                    TRANSCRIPTION_ERROR: [
                        f"{p.fixture}/{p.probe_id}"
                        for p in measured
                        if p.grounding == TRANSCRIPTION_ERROR
                    ],
                    ATTRIBUTION_ERROR: [
                        f"{p.fixture}/{p.probe_id}"
                        for p in measured
                        if p.grounding == ATTRIBUTION_ERROR
                    ],
                },
                "probes": [
                    {
                        "fixture": p.fixture,
                        "probe_id": p.probe_id,
                        "direction": p.direction,
                        "document": p.runs[0].document,
                        "status": ("error" if p.errored else
                                   "unmeasured" if p.unmeasured else "measured"),
                        "error": next((r.error for r in p.runs if r.error), None),
                        "expected_verdict": p.expected,
                        "also_acceptable": p.acceptable,
                        "modal_verdict": p.modal,
                        "observed_verdicts": p.observed,
                        "stable": p.stable,
                        "strict_ok": p.strict_ok,
                        "lenient_ok": p.lenient_ok,
                        "expected_evidence_contains": p.wants_evidence,
                        "expected_evidence_source": p.wants_source,
                        "source_ok": p.source_ok,
                        "evidence_ok": p.evidence_ok,
                        "grounding": p.grounding,
                        "grounded": p.grounded,
                        "grounding_stable": p.grounding_stable,
                        # Every run, not just the modal ones. The point of
                        # recording three is that the two that lost are evidence.
                        "verdicts": [r.verdict.as_dict() if r.verdict else None for r in p.runs],
                    }
                    for p in probes
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--fixture", action="append", help="run one fixture; repeatable")
    parser.add_argument("--out", type=Path, help="write the full result here as JSON")
    parser.add_argument("--no-colour", action="store_true")
    parser.add_argument(
        "--batch",
        type=int,
        default=DEFAULT_BATCH,
        help=f"claims per call (default {DEFAULT_BATCH})",
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=DEFAULT_SAMPLES,
        help=(
            f"run the whole fixture set this many times and report the modal "
            f"verdict (default {DEFAULT_SAMPLES})"
        ),
    )
    config.add_arguments(parser)
    args = parser.parse_args(argv)

    use_colour = sys.stdout.isatty() and not args.no_colour

    names = args.fixture or sorted(p.name for p in FIXTURES_DIR.iterdir() if p.is_dir())
    missing = [name for name in names if not (FIXTURES_DIR / name).is_dir()]
    if missing:
        print(f"no such fixture: {', '.join(missing)}", file=sys.stderr)
        return 2

    try:
        settings = config.resolve(args)
        loaded = {d: prompts.load(PROMPTS[d][0]) for d in DIRECTIONS}
    except (ConfigError, FileNotFoundError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    client = Client(settings)
    started = time.monotonic()

    hashes = " ".join(f"{d[:6]}:{p.sha256[:8]}" for d, p in loaded.items())
    print(
        colour(
            f"verify  {settings.mode}  {settings.host} ({settings.where})  {hashes}",
            DIM,
            use_colour,
        )
    )

    if args.samples < 1:
        print("error: --samples must be at least 1", file=sys.stderr)
        return 2

    sweeps: list[list[FixtureResult]] = []
    abandoned = 0
    consecutive = 0
    planned_units = args.samples * len(names)
    attempted = 0
    try:
        # The whole set, N times over, rather than N calls back to back per
        # fixture. Both give the same cassettes; this one keeps a partial run
        # interpretable, because an interrupted sweep has covered every fixture
        # fewer times rather than some fixtures not at all.
        for sample in range(args.samples):
            client.sample = sample
            sweep = []
            for name in names:
                sweep.append(run_fixture(name, client, loaded, args.batch))
                attempted += 1
                consecutive = consecutive + 1 if sweep[-1].errored else 0
                if consecutive >= CONSECUTIVE_ERROR_LIMIT:
                    abandoned = planned_units - attempted
                    print(
                        colour(
                            f"\n  giving up: {consecutive} fixtures errored in a row, "
                            f"last {name}.\n  {abandoned} unit(s) not attempted. "
                            f"Re-run to resume; this run exits 2.",
                            RED,
                            use_colour,
                        ),
                        flush=True,
                    )
                    break
                if args.samples > 1:
                    # A recording sweep is paced at 30 s a call and runs for
                    # tens of minutes. Silence for that long is indistinguishable
                    # from a hang.
                    print(
                        colour(f"  sample {sample + 1}/{args.samples}  {name}", DIM, use_colour),
                        flush=True,
                    )
            sweeps.append(sweep)
            if abandoned:
                break
    except DryRun:
        planned = 0
        for name in names:
            expected = json.loads(
                (FIXTURES_DIR / name / "expected.json").read_text(encoding="utf-8")
            )
            for direction in DIRECTIONS:
                probes = [p for p in expected["probes"] if p["direction"] == direction]
                planned += -(-len(probes) // max(1, args.batch))  # ceil
        planned *= args.samples
        print(
            f"\ndry run: {planned} calls planned against "
            f"{settings.model_for('verify')} at {settings.host}, "
            f"roughly {client.usage.planned_input_tokens * planned:,} input tokens. "
            f"No request was made."
        )
        return 0
    except MissingCassette as exc:
        print(f"\n{colour('replay miss', RED, use_colour)}: {exc}", file=sys.stderr)
        return 2
    except (CallBudgetExceeded, ConfigError) as exc:
        print(f"\n{colour('error', RED, use_colour)}: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # noqa: BLE001 - transport and endpoint faults are operational
        print(f"\n{colour('error', RED, use_colour)}: {exc}", file=sys.stderr)
        return 2

    results = aggregate(sweeps)
    for result in results:
        report(result, use_colour)
    summarise(results, args.samples, use_colour, abandoned=abandoned)
    provenance = Provenance(
        settings=settings,
        client=client,
        roles=("verify",),
        duration_seconds=time.monotonic() - started,
    )
    print()
    print(provenance.as_markdown())

    if args.out:
        write_json(args.out, results, args.samples, provenance, abandoned=abandoned)
        print(f"  -> {args.out}")

    if abandoned or any(r.errored for r in results):
        return 2  # inconclusive supersedes the assertion result
    if not all(r.ok for r in results):
        return 1
    # Everything measured passed. Unmeasured probes make that a partial reading,
    # and an exit 0 would be read as a pass over the whole set.
    return UNMEASURED_EXIT if any(r.unmeasured for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
