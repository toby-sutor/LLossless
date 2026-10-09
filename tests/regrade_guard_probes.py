#!/usr/bin/env python3
"""Re-grade the 2026-09-03 re-run's guard fixtures against their own probes.

`paper/records/detect-2026-09-03-B-70b.json` shows
`conflict_surfaced` with `probes: []` and `plants: 0`. Both are correct readings
of `tests/run_detect.py` as it stood: `planted()` only ever kept a probe whose
`expected_finding` is not `"none"`, and every probe on a guard fixture declares
`"none"` by construction, so no guard fixture's per-claim answer key was ever
graded, on any arm, in the whole project. The control that remained -- clean
exit code, no invented finding -- cannot tell a correct reading from an arm that
got every claim wrong in directions that cancelled.

`tests/run_detect.py` now grades every probe, not only the planted ones
(`guard_probes()`). This program does not re-run anything: the full model
reports from the 2026-09-03 re-run survive outside the session scratchpad that
produced them (the session scratchpad can vanish mid-session, so the
copy loop is the only surviving copy), and the calls in them were already made.
Re-grading them against the repaired code costs nothing and asks a model
nothing.

The three published summary records are not rewritten -- they are what actually
ran, and there is already a precedent of re-scoring into a separate,
named file rather than editing history. This one carries the
`regrade.guard.<arm>.*` prefix.

Usage:
    tests/regrade_guard_probes.py --reports-dir <dir-with-A-27b,B-70b,C-120b>
    tests/regrade_guard_probes.py --self-test
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import run_detect  # noqa: E402
import socket_guard  # noqa: E402

socket_guard.install()

RECORDS = ROOT / "paper" / "records"
OUT = RECORDS / "regrade-guard-probes.json"
ARMS = ("A-27b", "B-70b", "C-120b")
AMENDED = "2026-09-03"


def regrade_arm(arm: str, reports_dir: Path) -> dict:
    source = RECORDS / f"detect-2026-09-03-{arm}.json"
    blob = json.loads(source.read_text(encoding="utf-8"))
    fixtures = []
    for record in blob["records"]:
        name = record["fixture"]
        expected = run_detect.load_expected(name)
        if not run_detect.guard_probes(expected):
            continue
        report_path = reports_dir / arm / "detect-reports" / f"{name}.json"
        report = json.loads(report_path.read_text(encoding="utf-8"))
        graded = run_detect.grade(expected, report, record["exit_code"])
        # The exit code and outcome were already correct -- this is not a
        # re-score of the fixture, it is a first score of a field the fixture
        # never had graded. Asserting the two agree is what makes this an
        # addition rather than a silent change of the published verdict.
        assert graded["outcome"] == record["outcome"], (
            f"{arm}/{name}: outcome moved from {record['outcome']!r} to "
            f"{graded['outcome']!r} -- this script must only add guard grading")
        fixtures.append({
            "fixture": name,
            "guard_probes_total": len(graded["guard_probes"]),
            "guard_confirmed": graded["guard_confirmed"],
            "guard_wrong": graded["guard_wrong"],
            "guard_unclaimed": graded["guard_unclaimed"],
            "detail": graded["guard_probes"],
        })
    return {
        "arm": arm,
        "guard_fixtures": len(fixtures),
        "guard_probes_total": sum(f["guard_probes_total"] for f in fixtures),
        "guard_confirmed_total": sum(len(f["guard_confirmed"]) for f in fixtures),
        "guard_wrong_total": sum(len(f["guard_wrong"]) for f in fixtures),
        "guard_unclaimed_total": sum(len(f["guard_unclaimed"]) for f in fixtures),
        "fixtures": fixtures,
    }


# The self-test's must-fire and must-not-fire seeds. A guard fixture's report
# is small enough to write inline rather than fixture a whole directory.
_PROBE = {"probe_id": "p", "direction": "source_to_merged", "document": "m.md",
          "line": 1, "text": "x", "expected_finding": "none",
          "anchor": {"all_of": ["the widget ships"]}, "expected_verdict": "SUPPORTED",
          "also_acceptable": []}


def _expected(probes):
    return {"kind": "guard", "probes": probes,
            "expected_exit_code": {"strict": 0, "lenient": 0}}


def _report(verdicts=(), findings=(), claims=None):
    return {"claims": claims or [{"id": "C-1", "text": "the widget ships"}],
            "verdicts": list(verdicts), "findings": list(findings)}


def self_test() -> int:
    bad = []

    def check(name, expected, report, want_verdict):
        graded = run_detect.grade(expected, report, 0)
        got = graded["guard_probes"][0]["verdict"]
        if got != want_verdict:
            bad.append(f"{name}: got {got!r}, want {want_verdict!r}")

    fwd = "source_to_merged"
    check("confirmed: the model's verdict matches the answer key",
          _expected([_PROBE]),
          _report(verdicts=[{"claim_id": "C-1", "verdict": "SUPPORTED",
                              "finding": "none", "direction": fwd}]),
          "confirmed")
    check("wrong_verdict: the model answered, and answered wrong",
          _expected([_PROBE]),
          _report(verdicts=[{"claim_id": "C-1", "verdict": "MISSING",
                              "finding": "dropped", "direction": fwd}]),
          "wrong_verdict")
    check("false_alarm: a finding fired on a claim the guard says is clean",
          _expected([_PROBE]),
          _report(findings=[{"claim_id": "C-1", "finding": "dropped",
                              "evidence": "the widget ships", "direction": fwd}]),
          "false_alarm")
    check("unclaimed: no verdict reaches this claim at all",
          _expected([_PROBE]), _report(), "unclaimed")
    check("also_acceptable softens a different label to confirmed",
          _expected([dict(_PROBE, also_acceptable=["ACCEPTABLE_NO_FINDING"])]),
          _report(verdicts=[{"claim_id": "C-1", "verdict": "ACCEPTABLE_NO_FINDING",
                              "finding": "none", "direction": fwd}]),
          "confirmed")
    check("a same-text verdict on the other direction is not this probe's answer "
          "-- the collision that hit three independent arms on attribution_swapped",
          _expected([_PROBE]),
          _report(verdicts=[{"claim_id": "C-2", "verdict": "CONTRADICTED",
                              "finding": "contradicted", "direction": "merged_to_sources",
                              "evidence": "the widget ships"}]),
          "unclaimed")
    check("a rationale reciting the right value for a different, losing claim "
          "is not this probe's answer either -- contradiction's b-connect-timeout, "
          "wrong on all three arms until this",
          _expected([_PROBE]),
          _report(
              claims=[{"id": "C-1", "text": "the widget ships"},
                      {"id": "C-2", "text": "the widget breaks"}],
              verdicts=[
                  {"claim_id": "C-2", "verdict": "CONTRADICTED", "finding": "contradicted",
                   "direction": fwd, "evidence": "the widget ships", "rationale": "not this one"},
                  {"claim_id": "C-1", "verdict": "SUPPORTED", "finding": "none",
                   "direction": fwd, "evidence": "the widget ships"},
              ]),
          "confirmed")

    # A finding already spoken for by the fixture's own planted probe must not
    # also be read as a false alarm on a guard probe whose claim disagrees with
    # it. `contradiction`'s losing claim's rationale cites the winning value
    # verbatim -- exactly this shape -- and was wrong on all three arms until
    # `accounted` was excluded from the guard search.
    planted_probe = {"probe_id": "defect", "direction": fwd, "document": "a.md",
                      "line": 1, "text": "y", "expected_finding": "contradicted",
                      "anchor": {"all_of": ["the losing claim"]},
                      "expected_verdict": "CONTRADICTED", "also_acceptable": []}
    guard_probe = dict(_PROBE, probe_id="winner", anchor={"all_of": ["the winning claim"]})
    graded = run_detect.grade(
        _expected([planted_probe, guard_probe]),
        _report(
            claims=[{"id": "L", "text": "the losing claim"},
                    {"id": "W", "text": "the winning claim"}],
            findings=[{"claim_id": "L", "finding": "contradicted", "direction": fwd,
                       "evidence": "the winning claim", "rationale": "the winning claim wins"}],
            verdicts=[{"claim_id": "L", "verdict": "CONTRADICTED", "finding": "contradicted",
                       "direction": fwd, "evidence": "the winning claim"},
                      {"claim_id": "W", "verdict": "SUPPORTED", "finding": "none",
                       "direction": fwd, "evidence": "the winning claim"}],
        ), 1)
    got = graded["guard_probes"][0]["verdict"]
    if got != "confirmed":
        bad.append(f"a finding already accounted to the planted probe was read as "
                   f"a false alarm on the guard probe instead: got {got!r}")

    # And the class this whole item is about: compensating errors that exit
    # clean and invent nothing must still be visible as `guard_wrong`, where
    # before this fix they were invisible because `probes` was always `[]`.
    two_probes = [_PROBE, dict(_PROBE, probe_id="q",
                                anchor={"all_of": ["the gadget ships"]})]
    expected = _expected(two_probes)
    report = _report(verdicts=[
        {"claim_id": "C-1", "verdict": "MISSING", "finding": "dropped", "direction": fwd},
    ])
    graded = run_detect.grade(expected, report, 0)
    if not graded["guard_wrong"]:
        bad.append("a wrong per-claim verdict did not surface in guard_wrong")
    if run_detect.planted(expected):
        bad.append("the seed accidentally planted a defect probe")

    for line in bad:
        print(f"SELF-TEST FAILED: {line}")
    if bad:
        return 1
    print(f"  self-test: 8 must-fire probe(s) reach the outcome they name, and a "
          f"guard fixture's wrong verdict surfaces in guard_wrong")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--reports-dir", type=Path,
                        help="directory holding <arm>/detect-reports/<fixture>.json")
    parser.add_argument("--self-test", action="store_true", dest="probe")
    args = parser.parse_args(argv)

    if args.probe:
        return self_test()
    if self_test() != 0:
        return 1
    if args.reports_dir is None:
        print("no --reports-dir given; nothing to re-grade", file=sys.stderr)
        return 2

    arms = [regrade_arm(arm, args.reports_dir) for arm in ARMS]
    for arm in arms:
        print(f"  {arm['arm']:<8}  guard probes {arm['guard_confirmed_total']:>2}"
              f"/{arm['guard_probes_total']:<2}  wrong {arm['guard_wrong_total']}"
              f"  unclaimed {arm['guard_unclaimed_total']}")
        if arm["guard_wrong_total"]:
            for f in arm["fixtures"]:
                if f["guard_wrong"]:
                    print(f"      WRONG: {f['fixture']}: {', '.join(f['guard_wrong'])}")

    OUT.write_text(json.dumps({
        "note": "Guard-fixture per-claim verdicts, graded for the first time "
                "(Brief BB item 1) from the 2026-09-03 re-run's own saved model "
                "reports. Nothing here changed the exit-code outcome any "
                "record already carries -- asserted in this script.",
        "amended": AMENDED, "arms": arms,
    }, indent=2) + "\n", encoding="utf-8")
    print(f"\n  -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
