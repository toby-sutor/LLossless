#!/usr/bin/env python3
"""Re-score the 2026-09-03 detection arms once inventions count everywhere.

Disqualifier clause 2 read

    expected_exit_code == 0 and exit_code != 0 and invented_findings

so it could not fire on any fixture expecting exit 1 -- that is, on any of the
six fixtures in the block that plant a defect. It was reachable only on the
seven that plant none. `conflict_surfaced` was the instance, and it was
repaired; the class stayed open. An arm could report findings no probe
accounts for on a defect fixture, exit 1 for the wrong reason, and be scored as
matching. All three arms did exactly that on `attribution_swapped`: 1, 1 and 2
unaccounted findings, three `matched` outcomes.

**The first thing the generalised clause found was a broken fixture, not a
broken arm.** `attribution_swapped` declares its plant as "attribution swapped
between the two named sources". Swapped is symmetric, and merged.md carries
both halves:

    line 7  According to the Deployment Notes, the read timeout is 30 seconds.
    line 8  According to the Operator Guide,   the read timeout is 60 seconds.

Source B *is* the Deployment Notes and states 60; source A *is* the Operator
Guide and states 30. Both lines are false against the document they name. Only
line 7 was probed. Three of the four unaccounted findings are findings on line
8 -- correct readings of the unprobed half of the planted defect, recorded as
inventions because no probe claimed them. Disqualifying on that would have
rejected all three arms, including the one arm with nothing else against it,
for being right. The fixture is repaired the same way its own declaration
describes: the second probe is the first with the swap applied.

The fourth is a genuine false positive and stays one: `gpt-oss:120b` reported
"The read timeout is unresolved." as contradicted by source A's 30 seconds. The
merged document says the value is unresolved, and it is -- the sources disagree.

This program re-grades from stored evidence. No model is called; nothing here
asks anything of an endpoint. It needs the per-fixture reports the run wrote,
which the graded run records (withheld with the paper) do not carry, so it says so and passes rather than
reporting a result it did not compute -- the same refusal `grade_rerun.py` and
`test_fixtures.check_preregistered_block` make. What it writes instead is
self-contained: every finding it re-classified is in the output with the claim
text it was filed against, so the ruling can be audited from the record alone.

    tests/regrade_inventions.py                 report, and write the record
    tests/regrade_inventions.py --self-test     prove the clause can fire
    tests/regrade_inventions.py --reports-dir D read the reports from D
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

socket_guard.install()

import fixture_semantics  # noqa: E402
import run_detect  # noqa: E402

RECORDS = ROOT / "paper" / "records"
ARMS = ("A-27b", "B-70b", "C-120b")
OUT = RECORDS / "regrade-inventions.json"

# The date the clause changed. A pre-registered property amended after the
# block's results were known, so the paper's amendment log has to be able to
# say when, from the record rather than from prose.
AMENDED = "2026-09-03"

# Where the run left the per-fixture reports. They are in the repository now:
# they were the input to a *published* re-score and existed
# only on one machine, which made `regrade-inventions.json` unreproducible
# by anyone else -- the same defect as the dangling `report_ref` that led
# here, one level worse. This default is repo-relative so a clean checkout
# can run it; the mirror path it used to name is gone from this file.
DEFAULT_REPORTS = ROOT / "arms" / "2026-09-03"


def record_path(arm: str) -> Path:
    return RECORDS / f"detect-2026-09-03-{arm}.json"


def reports_for(root: Path, arm: str) -> Path:
    return root / arm / "detect-reports"


def regrade_arm(arm: str, reports: Path) -> dict:
    """Re-grade one arm's whole block against the fixtures as they are now.

    The exit code is the one the run recorded. Nothing here re-derives model
    behaviour; the only thing that changed is which probe accounts for which
    finding, and that is a property of the fixture.
    """
    blob = json.loads(record_path(arm).read_text(encoding="utf-8"))
    as_run = {r["fixture"]: r for r in blob["records"]}
    out = []
    for name in run_detect.block_names():
        old = as_run[name]
        expected = run_detect.load_expected(name)
        report = json.loads((reports / f"{name}.json").read_text(encoding="utf-8"))
        fresh = run_detect.grade(expected, report, old["exit_code"])
        fresh["fixture"] = name
        fresh["kind"] = expected["kind"]
        fresh["harvest"] = old.get("harvest")
        out.append(fresh)
    return {"as_run": blob, "records": out}


def claim_texts(reports: Path, fixture: str) -> dict[str, str]:
    report = json.loads((reports / f"{fixture}.json").read_text(encoding="utf-8"))
    return {c["id"]: c.get("text", "") for c in report.get("claims", [])}


def summarise(arm: str, as_run: dict, records: list[dict], reports: Path) -> dict:
    # An errored fixture (exit 2, no report) is no more measured than an
    # unmeasured one. No record this regrades has one.
    measured = [r for r in records
                if r["outcome"] not in (fixture_semantics.UNMEASURED, fixture_semantics.ERRORED)]
    unmeasured = [r for r in records
                  if r["outcome"] == fixture_semantics.UNMEASURED]
    # Every finding still unaccounted, with the claim it was filed against.
    # A count cannot be audited; this can.
    remaining = []
    for r in records:
        if not r["invented_findings"]:
            continue
        texts = claim_texts(reports, r["fixture"])
        for f in r["invented_findings"]:
            remaining.append({
                "fixture": r["fixture"], "claim_id": f.get("claim_id"),
                "claim_text": texts.get(f.get("claim_id") or "", ""),
                "finding": f.get("finding"), "evidence": f.get("evidence"),
                "rationale": f.get("rationale"),
            })
    return {
        "arm": arm,
        "label": arm,
        "passthrough": list(as_run["summary"]["passthrough"]),
        "fixtures": len(records),
        "exit_code_matched": sorted(r["fixture"] for r in records
                                    if r["outcome"] == fixture_semantics.MATCHED),
        "exit_code_unmeasured": sorted(r["fixture"] for r in unmeasured),
        "exit_code_missed": sorted(r["fixture"] for r in records
                                   if r["outcome"] == fixture_semantics.MISSED),
        "fixtures_measured": len(measured),
        "plants_total": sum(r["plants"] for r in records),
        "plants_unmeasured": sum(r["plants"] for r in unmeasured),
        "plants_detected": sum(len(r["detected"]) for r in measured),
        "invented_total": sum(len(r["invented_findings"]) for r in records),
        "disqualified": run_detect.disqualified(records),
        "disqualified_as_run": list(as_run["summary"]["disqualified"]),
        "unaccounted_findings": remaining,
    }


def _record(fixture: str, expected_exit: int, exit_code: int, invented: int,
            outcome: str = fixture_semantics.MATCHED) -> dict:
    return {"fixture": fixture, "expected_exit_code": expected_exit,
            "exit_code": exit_code, "outcome": outcome,
            "invented_findings": [{"claim_id": f"X-{i}"} for i in range(invented)]}


def self_test() -> int:
    """The clause must fire on a defect fixture and stay quiet without cause.

    The must-fire case is the one the old clause could not see: expected exit 1,
    exit 1, a finding no probe accounts for. Seeded against the shipped
    `run_detect.disqualified`, not against a copy of its expression.
    """
    fired = run_detect.disqualified([_record("seeded_defect", 1, 1, 2)])
    assert len(fired) == 1 and "2 invented finding(s) beside the seeded defect" in fired[0], fired
    # Must-not-fire: the same defect fixture with nothing unaccounted.
    assert run_detect.disqualified([_record("seeded_defect", 1, 1, 0)]) == []
    # The clean-fixture wording is unchanged, so old records stay comparable.
    clean = run_detect.disqualified([_record("guard", 0, 1, 1)])
    assert clean == ["guard: a clean fixture failed with 1 invented finding(s)"], clean
    # Unmeasured still disqualifies nothing, whatever it invented.
    assert run_detect.disqualified(
        [_record("nd", 1, 0, 3, fixture_semantics.UNMEASURED)]) == []
    # And clause 1 is untouched.
    assert run_detect.disqualified([_record("seeded_defect", 1, 0, 0)]) == [
        "seeded_defect: a seeded defect exited clean"]
    # The repaired fixture must probe both halves of its own swap, or the
    # generalised clause rejects three arms for a correct reading.
    swapped = run_detect.load_expected("attribution_swapped")
    plants = [p["probe_id"] for p in run_detect.planted(swapped)]
    assert sorted(plants) == ["m-guide-timeout-attribution",
                              "m-notes-timeout-attribution"], plants
    print("  self-test: the clause fires on a defect fixture and is quiet without "
          "cause; clean-fixture wording, clause 1 and the unmeasured skip all "
          "unchanged; attribution_swapped probes both halves")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--reports-dir", type=Path, default=DEFAULT_REPORTS)
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()

    if args.self_test:
        return self_test()
    self_test()

    if not all(record_path(a).is_file() for a in ARMS):
        print("  paper/records/ is NOT-PUBLISHED wholesale; no records to "
              "re-grade here")
        return 0
    missing = [a for a in ARMS if not reports_for(args.reports_dir, a).is_dir()]
    if missing:
        print(f"  no stored reports under {args.reports_dir} for "
              f"{', '.join(missing)}; the re-grade needs the per-fixture "
              f"reports and will not guess at them")
        print(f"  the ruling it reached is on record at "
              f"{args.out.relative_to(ROOT) if args.out.is_file() else args.out}")
        return 0

    # A list of arm objects each carrying its own `arm`, not a mapping keyed by
    # label: `build_numbers.collect` routes every `regrade-*.json` on its shape
    # and iterates `arms` expecting dicts. A mapping made it iterate the keys
    # and crash on the first `str.get` -- the one thing the comment above that
    # loop says the routing exists to prevent.
    arms = []
    for arm in ARMS:
        reports = reports_for(args.reports_dir, arm)
        graded = regrade_arm(arm, reports)
        arms.append(summarise(arm, graded["as_run"], graded["records"], reports))

    # Counts the paper states in prose. Derived here rather than written into
    # the sentence: a numeral in a result section has to come from a record.
    expected = {n: run_detect.load_expected(n) for n in run_detect.block_names()}
    swapped = [f for s in arms for f in s["unaccounted_findings"]
               if f["fixture"] == "attribution_swapped"]
    as_run_swapped = sum(
        len(r["invented_findings"])
        for s in arms
        for r in json.loads(record_path(s["arm"]).read_text(encoding="utf-8"))["records"]
        if r["fixture"] == "attribution_swapped")

    payload = {"brief": "BC item 1",
               "amended": AMENDED,
               "arm_count": len(arms),
               "defect_fixtures": sum(
                   1 for e in expected.values()
                   if fixture_semantics.implied_exit_codes(e)["strict"] == 1),
               "clean_fixtures": sum(
                   1 for e in expected.values()
                   if fixture_semantics.implied_exit_codes(e)["strict"] == 0),
               "swapped_unaccounted_as_run": as_run_swapped,
               "swapped_reclassified": as_run_swapped - len(swapped),
               "rule": "an invented finding disqualifies on every measured "
                       "fixture, whatever exit code the fixture expects",
               "fixture_repaired": "attribution_swapped: the second half of "
                                   "the declared swap was unprobed",
               "arms": arms}
    args.out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    for s in arms:
        arm = s["arm"]
        print(f"  {arm:7} matched {len(s['exit_code_matched'])}/"
              f"{s['fixtures_measured']} measured of {s['fixtures']}, "
              f"plants {s['plants_detected']}/{s['plants_total']}, "
              f"invented {s['invented_total']}, "
              f"disqualified {len(s['disqualified'])} "
              f"(as run {len(s['disqualified_as_run'])})")
        for line in s["disqualified"]:
            print(f"            - {line}")
    print(f"  written to {args.out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
