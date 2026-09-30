"""What a fixture's own probes imply, derived once and read by everything.

Two questions, one derivation:

* **Is the fixture consistent with itself?** `expected.json` declares an
  `expected_exit_code`, and it also declares, probe by probe, the verdict it
  expects and the verdicts it will also accept. Those are two statements about
  the same run, and nothing checked that they agreed. Two fixtures disagreed
  with themselves for months: `conflict_surfaced` declared exit 1 from eleven
  all-`SUPPORTED` probes with nothing planted, which no correct run can produce,
  and `numeric_drift` declared exit 1 in both modes while sanctioning a reading
  that exits 0. `tests/test_fixtures.py` fails the suite on the disagreement now.

* **Did the fixture measure this arm?** When the strict and lenient codes
  differ, an arm landing on the lenient one has not passed and has not failed:
  it answered on a reading the fixture itself sanctions and the strict
  expectation was never wired to see. `tests/run_detect.py` records that as
  `unmeasured`, a third outcome beside matched and missed.

* **Did the run finish at all?** An exit 2 (an errored or unusable run: a
  429, a 5xx, a timeout, a worker that never loaded) or a run that wrote no
  report took no reading of the model. It is `errored`, a fourth outcome,
  excluded from the detection and exit-code denominators and named; the
  benchmark's rule is that a failure outside the model's control is
  not scored, and retried.

The derivation goes through `llossless.verify.FINDINGS` rather than repeating
the label-to-finding mapping, because a fixture's answer key must be checked
against the implementation and not against a second copy of the spec. The old
check derived the exit code from `expected_conflicts` instead, and
`expected_conflicts` is read by no file in `src/llossless`, so
it certified both broken fixtures as consistent. A derivation that runs through
a mechanism that was never built cannot fail.

`report.exit_code` also returns 1 for a structural finding or an over-budget run
and 2 for an errored or unusable one. Neither is declarable in a fixture, so
neither is derivable here; this covers the findings path, which is the path
`expected_exit_code` describes.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from llossless.verify import FINDINGS  # noqa: E402

# The four outcomes of grading one fixture against one arm. `UNMEASURED` is not
# a softer `MISSED`: it says the instrument did not take a reading, and a study
# that reports it as either a pass or a blank has claimed a measurement it does
# not have. `ERRORED` is the run that never finished: an exit 2 or no report.
# It says nothing about the model, so it is neither a miss nor a reading.
MATCHED = "matched"
UNMEASURED = "unmeasured"
MISSED = "missed"
ERRORED = "errored"
OUTCOMES = (MATCHED, UNMEASURED, MISSED, ERRORED)
# The exit status `report.exit_code` gives an errored or unusable run. No
# fixture may declare it (`implied_exit_codes` gives 0 or 1 only).
INCONCLUSIVE_EXIT = 2


def sanctioned_findings(probe: dict) -> set[str]:
    """Every finding this probe's fixture is prepared to accept.

    `expected_verdict` plus `also_acceptable`, each mapped through the
    implementation's own label-to-finding table in the probe's direction.
    """
    direction = probe.get("direction")
    labels = [probe.get("expected_verdict")] + list(probe.get("also_acceptable") or [])
    return {FINDINGS[(label, direction)] for label in labels
            if (label, direction) in FINDINGS}


def implied_exit_codes(expected: dict) -> dict[str, int]:
    """The exit codes the probes imply, strict and lenient.

    Strict is the declared reading: 1 if any probe's `expected_verdict` files a
    finding. Lenient is the most forgiving reading the fixture itself sanctions:
    0 exactly when every probe has some accepted verdict that files nothing.

    Lenient is therefore never stricter than strict, and the two differ only
    where an `also_acceptable` entry crosses the finding boundary. That is the
    whole of what `expected_exit_code.lenient` means, and it is the signal
    `run_detect` reads to call a fixture unmeasured on an arm.
    """
    probes = expected.get("probes") or []
    strict = 1 if any(
        FINDINGS.get((p.get("expected_verdict"), p.get("direction")), "none") != "none"
        for p in probes) else 0
    lenient = 0 if all("none" in sanctioned_findings(p) for p in probes) else 1
    return {"strict": strict, "lenient": lenient}


def outcome(declared: dict, exit_code: int, invented: int, probe_verdicts: list, *,
            reported: bool) -> str:
    """Grade one arm on one fixture: matched, unmeasured, missed, or errored.

    `errored` comes first and is not a grade of the model: the run exited 2,
    or wrote no report (`reported` false). Its findings, if a partial report
    has any, are not read.

    `unmeasured` is deliberately narrow. All four conditions must hold:

    1. the fixture admits two codes - `strict != lenient`, so there is a
       sanctioned alternative reading at all;
    2. the arm landed on the lenient one;
    3. it invented nothing, so the code it produced is attributable to the
       sanctioned reading rather than to an unrelated finding that happens to
       move the exit status the same way;
    4. no planted probe was plainly missed. A probe answered on an accepted
       label is `acceptable_no_finding`; a probe the arm never produced a
       verdict for is `missed`, and a fixture cannot excuse that.

    Condition 3 is the one that matters most. On the 2026-08-30 arms the only
    fixture-level "match" that condition 3 rejects was produced by a
    hallucination: an invented finding pushed the exit code onto the expected
    value, and the study scored it as a detection.
    """
    if exit_code == INCONCLUSIVE_EXIT or not reported:
        return ERRORED
    strict, lenient = declared["strict"], declared["lenient"]
    if exit_code == strict:
        return MATCHED
    if (lenient != strict and exit_code == lenient and not invented
            and not any(p.get("verdict") == MISSED for p in probe_verdicts)):
        return UNMEASURED
    return MISSED
