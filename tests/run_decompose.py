#!/usr/bin/env python3
"""Run the decompose pass over every fixture and grade it against expected.json.

This is the decompose measurement. It calls a model — live, or from recorded cassettes
— so it is a runner rather than a test. `tests/test_fixtures.py` remains the
offline structural check and `tests/test_client.py` the offline client suite;
the three should not be confused. Nothing here edits a fixture. If a fixture and
the model disagree, that is the result, and the result gets reported as it is.

Graded, per document:

  must_extract   every probe with must_extract must be matched by some claim
  line accuracy  a matched claim's line must sit within +/-2 of the probe's
  count band     the number of claims must fall inside claim_count_band
  anchored       claims whose span was located verbatim in the document

A document whose call could not be parsed is *errored*, not empty. Its probes
leave the coverage denominator entirely and the run exits 2 — "did not measure"
rather than "measured badly".

Usage:
    python3 tests/run_decompose.py --offline
    python3 tests/run_decompose.py --record tests/responses --model <id>
    python3 tests/run_decompose.py --dry-run
    python3 tests/run_decompose.py --fixture paraphrase --fixture hallucination
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
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
from llossless.decompose import ANCHOR_RADIUS, Claim, decompose_text  # noqa: E402
from llossless.provenance import Provenance  # noqa: E402

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"

# must_not_extract assertions that hold for every document of every fixture,
# for claims no document in the suite could legitimately produce. Read plainly
# rather than defensively: tests/test_fixtures.py validates this file offline on
# the same terms as a fixture's own assertions, and a measurement runner is not
# where a malformed one should first be discovered.
GLOBAL_FORBIDDEN = json.loads((FIXTURES_DIR / "GLOBAL.json").read_text())["must_not_extract"]

# See run_verify.DEFAULT_SAMPLES. Three is the smallest number that can tell
# "the model does this" apart from "the model did this once".
DEFAULT_SAMPLES = 3

# The same contract `run_merge.py` carries. One bad call errors
# one fixture; the sweep goes on and exits 2 at the end. What ends the run is a
# fault that will be true of every later call too.
CONSECUTIVE_ERROR_LIMIT = 3

# Faults that end the sweep rather than one fixture. DryRun is in the tuple and
# is the one that does not transfer from `run_merge.py`, which has no dry-run
# path through a call: `client.complete` raises it from inside the call
# (`client.py:208`), so a catch-by-exclusion that did not name it would swallow
# the signal and print a sweep report for a run that made no request.
#
# Everything else -- transport faults, HTTP statuses, tier refusals, a body that
# will not parse -- errors the document. Caught structurally rather than by
# class so that naming TransportError here cannot import `transport` into a
# replay run.
FATAL_TO_THE_RUN = (ConflictingCassettes, DryRun, MissingCassette, CallBudgetExceeded, ConfigError)
DOCUMENTS = ("source_a.md", "source_b.md", "merged.md")

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
class DocumentResult:
    """What decompose produced for one document, and how it graded."""

    fixture: str
    document: str
    claims: list[Claim]
    band: tuple[int, int]
    matched: dict[str, int] = field(default_factory=dict)  # probe_id -> claim index
    misplaced: dict[str, tuple[int, int]] = field(default_factory=dict)
    unmatched: list[str] = field(default_factory=list)
    error: str | None = None
    probe_count: int = 0
    # Every must-extract probe for this document, in fixture order, whether or
    # not it was found. matched and unmatched together carry the same names but
    # not the order, and comparing runs needs a stable spine to line them up on.
    probe_ids: list[str] = field(default_factory=list)
    # Every must_not_extract assertion for this document, and the ones a claim
    # actually tripped. Both are kept: the denominator is how many assertions
    # were checked, and without it "0 violations" cannot be told apart from
    # "nothing was asserted".
    forbidden_ids: list[str] = field(default_factory=list)
    forbidden: dict[str, str] = field(default_factory=dict)  # assertion_id -> claim text

    @property
    def count(self) -> int:
        return len(self.claims)

    @property
    def in_band(self) -> bool:
        return self.band[0] <= self.count <= self.band[1]

    @property
    def anchored(self) -> int:
        return sum(1 for claim in self.claims if claim.anchored)

    @property
    def ok(self) -> bool:
        if self.error:
            return False
        return not self.unmatched and not self.misplaced and self.in_band and not self.forbidden


def match_probe(claim: Claim, needles: list[str]) -> bool:
    """A claim matches a probe when it contains every substring, case-insensitively.

    Same rule the offline validator uses to anchor a probe to its document, so a
    probe that anchors there is matchable here.
    """
    haystack = claim.text.lower()
    return all(needle.lower() in haystack for needle in needles)


def grade_forbidden(result: DocumentResult, assertions: list[dict]) -> None:
    """Check this document's claims against its must_not_extract patterns.

    The mirror of must_extract, and it catches the opposite failure: not a
    decomposer that drops a fact, but one that produces a claim the document
    never made. tests/test_fixtures.py has already checked offline that each
    pattern is satisfiable — that it matches neither the document's own prose
    nor a must_extract probe on the same document — so a hit here is the model's
    output and nothing else.

    Both fields are searched, `text` and `span`, because the two can disagree
    and the interesting failures are the ones where they do. On
    `ordering_only/merged.md` this model has produced the correct claim text
    `512` alongside a span reading `51,2`, `513` and `510` in three successive
    corpora: the assertion is right, the receipt is wrong, and a check that read
    only `text` would call that clean.
    """
    for assertion in assertions:
        result.forbidden_ids.append(assertion["assertion_id"])
        if result.error:
            continue
        compiled = re.compile(assertion["pattern"])
        hit = next(
            (c for c in result.claims if compiled.search(c.text) or compiled.search(c.span)),
            None,
        )
        if hit is not None:
            matched = compiled.search(hit.text) or compiled.search(hit.span)
            field = "text" if compiled.search(hit.text) else "span"
            result.forbidden[assertion["assertion_id"]] = f"{field}: {matched.string}"


def grade(result: DocumentResult, probes: list[dict]) -> None:
    """Grade one document's claims against the probes that belong to it."""
    for probe in probes:
        if not probe.get("must_extract"):
            continue
        result.probe_count += 1
        result.probe_ids.append(probe["probe_id"])
        if result.error:
            continue
        needles = probe["match"]["all_of"]
        hit = next(
            (i for i, claim in enumerate(result.claims) if match_probe(claim, needles)),
            None,
        )
        if hit is None:
            result.unmatched.append(probe["probe_id"])
            continue
        result.matched[probe["probe_id"]] = hit
        actual, expected = result.claims[hit].line, probe["line"]
        if abs(actual - expected) > ANCHOR_RADIUS:
            result.misplaced[probe["probe_id"]] = (actual, expected)


@dataclass
class DocumentSamples:
    """One document across every run of the sweep.

    Decompose is not stable either, and its instability shows up somewhere
    different from verify's: the verdict vocabulary is closed, but a claim count
    is not, so the same document decomposes into 18 claims one run and 21 the
    next without either being wrong. What must not move is whether a probe was
    extracted at all. That is what this grades, and the claim count is reported
    as the range it actually occupied rather than as whichever run went last.
    """

    runs: list[DocumentResult]

    @property
    def fixture(self) -> str:
        return self.runs[0].fixture

    @property
    def document(self) -> str:
        return self.runs[0].document

    @property
    def band(self) -> tuple[int, int]:
        return self.runs[0].band

    @property
    def probe_ids(self) -> list[str]:
        return self.runs[0].probe_ids

    @property
    def probe_count(self) -> int:
        return self.runs[0].probe_count

    @property
    def error(self) -> str | None:
        return next((r.error for r in self.runs if r.error), None)

    @property
    def counts(self) -> list[int]:
        return [r.count for r in self.runs]

    @property
    def count_range(self) -> str:
        lo, hi = min(self.counts), max(self.counts)
        return str(lo) if lo == hi else f"{lo}-{hi}"

    @property
    def count_stable(self) -> bool:
        return len(set(self.counts)) == 1

    @property
    def in_band(self) -> bool:
        """In band in a strict majority of runs."""
        hits = sum(1 for r in self.runs if r.in_band)
        return hits * 2 > len(self.runs)

    @property
    def band_stable(self) -> bool:
        return len({r.in_band for r in self.runs}) == 1

    @property
    def anchored(self) -> int:
        return sum(r.anchored for r in self.runs)

    @property
    def total_claims(self) -> int:
        return sum(r.count for r in self.runs)

    def extractions(self, probe_id: str) -> list[bool]:
        return [probe_id in r.matched for r in self.runs]

    def extracted(self, probe_id: str) -> bool:
        hits = sum(self.extractions(probe_id))
        return hits * 2 > len(self.runs)

    def placed(self, probe_id: str) -> bool:
        """Extracted, and the line was right in most of the runs that found it."""
        found = [r for r in self.runs if probe_id in r.matched]
        right = sum(1 for r in found if probe_id not in r.misplaced)
        return bool(found) and right * 2 > len(found)

    @property
    def unstable_probes(self) -> list[str]:
        return [p for p in self.probe_ids if len(set(self.extractions(p))) > 1]

    @property
    def forbidden_ids(self) -> list[str]:
        return self.runs[0].forbidden_ids

    def violations(self, assertion_id: str) -> list[bool]:
        return [assertion_id in r.forbidden for r in self.runs]

    @property
    def forbidden(self) -> dict[str, str]:
        """Assertions tripped in *any* run, with an example of the claim that did it.

        Deliberately not a majority vote, unlike everything else here. A claim
        the document never made is a defect the moment it appears once; a
        decomposer that invents it in one run of three is not two-thirds
        trustworthy. The majority rule exists to keep a noisy measurement from
        reporting noise as signal, and this is not a measurement of degree.
        """
        found: dict[str, str] = {}
        for run in self.runs:
            for assertion_id, claim in run.forbidden.items():
                found.setdefault(assertion_id, claim)
        return found

    @property
    def unmatched(self) -> list[str]:
        return [p for p in self.probe_ids if not self.extracted(p)]

    @property
    def misplaced(self) -> list[str]:
        return [p for p in self.probe_ids if self.extracted(p) and not self.placed(p)]

    @property
    def ok(self) -> bool:
        if self.error:
            return False
        # `forbidden` belongs here for the same reason it is in DocumentResult.ok.
        # Leaving it out printed every violation in full and then scored the
        # document clean anyway, which made must_not_extract an observation
        # rather than an assertion — the one thing it exists not to be.
        return (
            not self.unmatched
            and not self.misplaced
            and self.in_band
            and not self.forbidden
        )


def aggregate(sweeps: list[list[DocumentResult]]) -> list[DocumentSamples]:
    """Zip N runs of the fixture set into one record per document."""
    slots: dict[tuple[str, str], list[DocumentResult]] = {}
    for sweep in sweeps:
        for result in sweep:
            slots.setdefault((result.fixture, result.document), []).append(result)
    return [DocumentSamples(runs=runs) for runs in slots.values()]


def run_fixture(
    name: str, client: Client, prompt: prompts.Prompt, cache: dict[str, object]
) -> list[DocumentResult]:
    directory = FIXTURES_DIR / name
    expected = json.loads((directory / "expected.json").read_text())
    results: list[DocumentResult] = []

    for document in DOCUMENTS:
        text = (directory / document).read_text(encoding="utf-8")

        # contradiction and conflict_surfaced share byte-identical sources.
        # Calling twice with identical input in one run buys nothing, and with
        # --record it would write the same cassette twice. This is not the
        # tool's verdict cache; it does not survive the process.
        key = f"{document}:{hash(text)}"
        if key not in cache:
            try:
                cache[key] = decompose_text(client, text, document, prompt)
            except FATAL_TO_THE_RUN:
                raise
            except Exception as exc:  # noqa: BLE001 - one bad call errors one document
                # Once `except SchemaFailure`, which meant a model
                # that answered unparseably cost one document while an endpoint
                # that dropped a connection cost the whole sweep -- the more
                # recoverable fault treated as the less recoverable one. The
                # cached value stays the exception so the dedupe cache still
                # serves an errored document once rather than retrying it per
                # fixture, and the type is kept in the message because "the
                # endpoint answered nothing" and "the model answered something
                # unparseable" read alike once they are strings.
                cache[key] = exc

        outcome = cache[key]
        failed = isinstance(outcome, Exception)
        lo, hi = expected["claim_count_band"][document]
        result = DocumentResult(
            fixture=name,
            document=document,
            claims=[] if failed else outcome,
            band=(lo, hi),
            error=f"{type(outcome).__name__}: {outcome}" if failed else None,
        )
        grade(result, [p for p in expected["probes"] if p["document"] == document])
        grade_forbidden(
            result,
            [a for a in expected["must_not_extract"] if a["document"] == document]
            + GLOBAL_FORBIDDEN,
        )
        results.append(result)

    return results


def report(results: list[DocumentResult], use_colour: bool) -> None:
    fixture = results[0].fixture
    if any(result.error for result in results):
        mark = colour("ERROR", YELLOW, use_colour)
    elif all(result.ok for result in results):
        mark = colour("ok", GREEN, use_colour)
    else:
        mark = colour("FAIL", RED, use_colour)
    print(f"\n{colour(fixture, BOLD, use_colour)} .. {mark}")

    for result in results:
        if result.error:
            print(
                f"    {result.document:<13} {colour('errored', YELLOW, use_colour)}"
                f"  {result.probe_count} probes not measured"
            )
            print(f"      {colour(result.error.splitlines()[0], DIM, use_colour)}")
            continue

        band = f"{result.band[0]}-{result.band[1]}"
        band_note = colour(f"band {band}", GREEN if result.in_band else RED, use_colour)
        if not result.band_stable:
            band_note += colour("!", YELLOW, use_colour)
        anchored = f"{result.anchored}/{result.total_claims} anchored"
        hit = sum(1 for p in result.probe_ids if result.extracted(p))
        print(
            f"    {result.document:<13} {result.count_range:>7} claims  {band_note}"
            f"   {hit}/{result.probe_count} probes   "
            f"{colour(anchored, DIM, use_colour)}"
        )
        for probe_id in result.unmatched:
            print(f"      {colour('not extracted', RED, use_colour)}  {probe_id}")
        for probe_id in result.misplaced:
            lines = sorted({r.claims[r.matched[probe_id]].line for r in result.runs
                            if probe_id in r.matched})
            want = next(iter(r.misplaced[probe_id][1] for r in result.runs
                             if probe_id in r.misplaced))
            got = ", ".join(str(n) for n in lines)
            print(
                f"      {colour('wrong line', YELLOW, use_colour)}     {probe_id}"
                f"  got {got}, expected {want}"
            )
        for probe_id in result.unstable_probes:
            seen = ["yes" if x else "no" for x in result.extractions(probe_id)]
            print(
                f"      {colour('unstable', YELLOW, use_colour)}       {probe_id}"
                f"  extracted: {', '.join(seen)}"
            )
        for assertion_id, claim in result.forbidden.items():
            runs = sum(result.violations(assertion_id))
            print(
                f"      {colour('forbidden', RED, use_colour)}     {assertion_id}"
                f"  in {runs}/{len(result.runs)} run(s)"
            )
            print(f"        {colour(claim[:96], DIM, use_colour)}")


def summarise(all_results: list[DocumentSamples], samples: int, use_colour: bool,
              abandoned: int = 0) -> None:
    measured = [r for r in all_results if not r.error]
    errored = [r for r in all_results if r.error]

    probes_hit = sum(1 for r in measured for p in r.probe_ids if r.extracted(p))
    probes_total = sum(r.probe_count for r in measured)
    unmeasured = sum(r.probe_count for r in errored)
    placed = sum(1 for r in measured for p in r.probe_ids if r.extracted(p) and r.placed(p))
    bands = sum(1 for r in measured if r.in_band)
    claims = sum(r.total_claims for r in measured)
    anchored = sum(r.anchored for r in measured)
    fixtures = {r.fixture for r in all_results}
    failing = {r.fixture for r in all_results if not r.ok}
    unstable = [(r, p) for r in measured for p in r.unstable_probes]
    drifting = [r for r in measured if not r.count_stable]
    asserted = sum(len(r.forbidden_ids) for r in measured)
    violated = [(r, a) for r in measured for a in r.forbidden]

    def pct(part: int, whole: int) -> str:
        return f"{part}/{whole}" + (f" ({part / whole:.0%})" if whole else "")

    print(f"\n{colour('Decompose over the fixture set', BOLD, use_colour)}")

    # Inside the report block and above every figure in it, including the
    # ERRORED line, and red rather than yellow. An errored document narrows a
    # denominator; an abandoned run means the suite described below is not the
    # suite that was asked for, and the two are not the same size of statement.
    # The line printed at the moment of abandonment has scrolled past by the
    # time anyone reads the report, and `abandoned_units` in the JSON is not
    # where a person looks. So it is repeated here, where the coverage it
    # qualifies is.
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

    if errored:
        # Printed first and never folded into a percentage. A coverage figure
        # that quietly counts an errored document as full coverage is the exact
        # dishonesty this tool exists to catch in other people's merges.
        print(
            colour(
                f"  ERRORED ............... {len(errored)} document(s), "
                f"{unmeasured} probe(s) not measured",
                YELLOW,
                use_colour,
            )
        )
    print(
        colour(
            f"  {samples} run(s) per document; probe figures are over the modal outcome.",
            DIM,
            use_colour,
        )
    )
    print(f"  Claims extracted ...... {claims} over {samples} run(s)")
    print(f"  Probes extracted ...... {pct(probes_hit, probes_total)}")
    print(f"  Line refs correct ..... {pct(placed, probes_hit)}  (within +/-{ANCHOR_RADIUS})")
    print(f"  Spans anchored ........ {pct(anchored, claims)}")
    print(f"  Count bands met ....... {pct(bands, len(measured))}")
    print(
        f"  Nothing invented ...... {pct(asserted - len(violated), asserted)}  "
        f"(must_not_extract, any run)"
    )
    print(f"  Fixtures clean ........ {pct(len(fixtures) - len(failing), len(fixtures))}")
    print(
        f"  Probe stability ....... "
        f"{pct(probes_total - len(unstable), probes_total)}  "
        f"(extracted or not, identically across {samples} run(s))"
    )
    print(
        f"  Claim counts stable ... {pct(len(measured) - len(drifting), len(measured))}  "
        f"(documents whose claim count never moved)"
    )

    if unstable:
        # A probe that is extracted in two runs out of three is not a 67% probe;
        # it is a probe this corpus cannot answer, and rolling it into a
        # coverage percentage is the exact flattening the sweep exists to stop.
        print(f"\n  {colour(f'Extracted in some runs and not others', BOLD, use_colour)}")
        for result, probe_id in unstable:
            seen = ", ".join("yes" if x else "no" for x in result.extractions(probe_id))
            print(f"    {result.fixture}/{result.document} {probe_id:<24} {seen}")
    if violated:
        print(f"\n  {colour('Claims the document never made', BOLD, use_colour)}")
        for result, assertion_id in violated:
            runs = sum(result.violations(assertion_id))
            print(
                f"    {result.fixture}/{result.document} {assertion_id:<24} "
                f"{runs}/{len(result.runs)} run(s)"
            )
            print(f"      {colour(result.forbidden[assertion_id][:96], DIM, use_colour)}")
    if errored:
        print(
            colour(
                "\n  Percentages above are over measured documents only. "
                "This run is inconclusive.",
                DIM,
                use_colour,
            )
        )


def write_json(
    path: Path, all_results: list[DocumentSamples], samples: int, provenance: Provenance,
    abandoned: int = 0,
) -> None:
    measured = [r for r in all_results if not r.error]
    path.write_text(
        json.dumps(
            {
                "provenance": provenance.as_dict(),
                "inconclusive": any(r.error for r in all_results) or bool(abandoned),
                "abandoned_units": abandoned,
                "samples": samples,
                "coverage": {
                    "probes_extracted": sum(
                        1 for r in measured for p in r.probe_ids if r.extracted(p)
                    ),
                    "probes_measured": sum(r.probe_count for r in measured),
                    "probes_not_measured": sum(r.probe_count for r in all_results if r.error),
                    "probes_unstable": [
                        f"{r.fixture}/{r.document}/{p}" for r in measured for p in r.unstable_probes
                    ],
                    "assertions_checked": sum(len(r.forbidden_ids) for r in measured),
                    "assertions_violated": [
                        {
                            "fixture": r.fixture,
                            "document": r.document,
                            "assertion_id": a,
                            "runs": r.violations(a),
                            "claim": r.forbidden[a],
                        }
                        for r in measured
                        for a in r.forbidden
                    ],
                },
                "documents": [
                    {
                        "fixture": r.fixture,
                        "document": r.document,
                        "status": "error" if r.error else "measured",
                        "error": r.error,
                        "claim_count_band": list(r.band),
                        "claim_counts": r.counts,
                        "unmatched_probes": r.unmatched,
                        "misplaced_probes": r.misplaced,
                        "unstable_probes": {
                            p: r.extractions(p) for p in r.unstable_probes
                        },
                        # Every run's claims, not the last one's. A reader
                        # checking an unstable probe needs the run that missed it.
                        "runs": [[c.as_dict() for c in run.claims] for run in r.runs],
                    }
                    for r in all_results
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
    parser.add_argument(
        "--samples",
        type=int,
        default=DEFAULT_SAMPLES,
        help=(
            f"run the whole fixture set this many times and report the modal "
            f"outcome per probe (default {DEFAULT_SAMPLES})"
        ),
    )
    parser.add_argument("--out", type=Path, help="write the full result here as JSON")
    parser.add_argument("--no-colour", action="store_true")
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
        prompt = prompts.load("decompose")
    except (ConfigError, FileNotFoundError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    client = Client(settings)
    started = time.monotonic()

    print(
        colour(
            f"decompose  {settings.mode}  {settings.host} ({settings.where})  "
            f"prompt {prompt.sha256[:12]}",
            DIM,
            use_colour,
        )
    )

    if args.samples < 1:
        print("error: --samples must be at least 1", file=sys.stderr)
        return 2

    sweeps: list[list[DocumentResult]] = []
    abandoned = 0
    consecutive = 0
    planned_units = args.samples * len(names)
    attempted = 0
    try:
        for sample in range(args.samples):
            client.sample = sample
            # The in-process dedupe cache is per sweep, never across them.
            # Sharing it would serve sample 0's claims as sample 1's answer for
            # every duplicated document and manufacture the stability being
            # measured -- the same trap the cassette key's sample field closes.
            cache: dict[str, object] = {}
            sweep: list[list[DocumentResult]] = []
            for name in names:
                sweep.append(run_fixture(name, client, prompt, cache))
                attempted += 1
                consecutive = consecutive + 1 if all(r.error for r in sweep[-1]) else 0
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
                    print(
                        colour(f"  sample {sample + 1}/{args.samples}  {name}", DIM, use_colour),
                        flush=True,
                    )
            all_of_them: list[DocumentResult] = []
            for results in sweep:
                all_of_them.extend(results)
            sweeps.append(all_of_them)
            if abandoned:
                break
    except DryRun:
        # The first planned call short-circuits the run: every fixture renders
        # the same prompt against a different document, so counting the rest is
        # arithmetic, not another round of guesswork.
        planned = len(names) * len(DOCUMENTS) * args.samples
        per_call = client.usage.planned_input_tokens
        print(
            f"\ndry run: {planned} calls planned against "
            f"{settings.model_for('decompose')} at {settings.host}, "
            f"roughly {per_call * planned:,} input tokens. No request was made."
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

    all_results = aggregate(sweeps)
    for fixture in sorted({r.fixture for r in all_results}, key=lambda f: names.index(f)):
        report([r for r in all_results if r.fixture == fixture], use_colour)
    summarise(all_results, args.samples, use_colour, abandoned=abandoned)
    provenance = Provenance(
        settings=settings,
        client=client,
        roles=("decompose",),
        duration_seconds=time.monotonic() - started,
    )
    print()
    print(provenance.as_markdown())

    if args.out:
        write_json(args.out, all_results, args.samples, provenance, abandoned=abandoned)
        print(f"  -> {args.out}")

    if abandoned or any(result.error for result in all_results):
        return 2  # inconclusive supersedes the assertion result
    return 0 if all(result.ok for result in all_results) else 1


if __name__ == "__main__":
    sys.exit(main())
