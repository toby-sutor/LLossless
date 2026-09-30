#!/usr/bin/env python3
"""The grading of the 2026-09-03 re-run, against the rules fixed before it ran.

The write-up for this benchmark fixed eight decision rules before the run
existed, and later reported the outcome. This program is the assertion
under that prose. Every number it states is read from a record here
and checked, because a sentence about a result is a claim with a truth value
and the suite has been green over wrong sentences before.

It grades and it does not interpret: no clause here decides what a number
means. The comparisons it draws are the ones fixed in advance --
which cells moved, which unmeasured cells resolved, and whether the arm that
was allowed to reach 13/13 did.

  tests/grade_rerun.py              print the grading
  tests/grade_rerun.py --self-test  prove the checks can fail

`paper` is NOT-PUBLISHED wholesale, so a published clone has no records to
grade. There the program says so and passes rather than reporting a result it
did not compute, the same way `test_fixtures.check_preregistered_block` does.
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

RECORDS = ROOT / "paper" / "records"
ARMS = ("A-27b", "B-70b", "C-120b")
ENDPOINT = "0d84ed4d2d30"

# What the write-up states, arm by arm, as it is stated there. A second place
# for the numbers to be wrong is the point: if the run is ever regraded, this
# tuple and the prose have to move together or the suite stops.
EXPECTED = {
    #        matched, unmeasured, missed, plants_detected, invented
    "A-27b": (12, 0, 1, 6, 2),
    "B-70b": (12, 1, 0, 5, 1),
    "C-120b": (11, 0, 2, 5, 3),
}


def load(name: str) -> dict:
    return json.loads((RECORDS / name).read_text(encoding="utf-8"))


def totals(record: dict) -> tuple:
    s = record["summary"]
    return (len(s["exit_code_matched"]), len(s["exit_code_unmeasured"]),
            len(s["exit_code_missed"]), s["plants_detected"], s["invented_total"])


def grade(quiet: bool = False) -> list[str]:
    """Every claim the write-up makes, checked. Returns the ones that failed."""
    bad: list[str] = []

    def check(ok: bool, claim: str) -> None:
        if not quiet:
            print(f"  [{'ok ' if ok else 'BAD'}] {claim}")
        if not ok:
            bad.append(claim)

    new = {a: load(f"detect-2026-09-03-{a}.json") for a in ARMS}
    old = {a: load(f"half1-{a}.json") for a in ARMS}
    base = {a["arm"]: a for a in load("regrade-detect.json")["arms"]}
    block = {r["fixture"] for r in old["A-27b"]["records"]}

    for arm in ARMS:
        graded = {r["fixture"] for r in new[arm]["records"]}
        check(graded == block,
              f"{arm} graded the pre-registered thirteen and nothing else")
        check(totals(new[arm]) == EXPECTED[arm],
              f"{arm} totals are matched/unmeasured/missed/plants/invented "
              f"{EXPECTED[arm]}, as section 10.6 states")

        tiers = {(r["harvest"]["structured_output"]["mode"],
                  r["harvest"]["structured_output"]["how"])
                 for r in new[arm]["records"]}
        check(tiers == {("json_schema", "pinned")},
              f"{arm} ran json_schema pinned on all 13, the recorded deviation")
        check({r["harvest"]["endpoint"]["id"] for r in new[arm]["records"]} == {ENDPOINT},
              f"{arm} ran against one endpoint, {ENDPOINT}, for all 13")

    # Rule 6. The 27B and the 70B reproduce across pods and the 120B does not,
    # so which arms moved decides whether movement is attributed to sampling.
    moved = {}
    for arm in ARMS:
        o = {r["fixture"]: r for r in old[arm]["records"]}
        n = {r["fixture"]: r for r in new[arm]["records"]}
        moved[arm] = sorted(f for f in n if o[f]["exit_code"] != n[f]["exit_code"])
        if not quiet:
            print(f"  ..  {arm} exit codes differ from 2026-08-30 on: "
                  f"{moved[arm] or 'nothing'}")
    check(moved["A-27b"] == [] and moved["B-70b"] == [],
          "rule 6: qwen3.8:27b and deepseek-r1:70b reproduced 2026-08-30 exactly")
    check(moved["C-120b"] == ["attribution_invented", "conflict_surfaced",
                              "disjoint_sources"],
          "rule 6: gpt-oss:120b moved on three cells and is the only arm that moved")

    # Rule 3. conflict_surfaced is the cell the repair exists for: it demanded
    # a failing exit with nothing planted, so only a hallucination could pass.
    for arm in ARMS:
        cell = {r["fixture"]: r for r in new[arm]["records"]}["conflict_surfaced"]
        check(cell["expected_exit_code"] == 0 and cell["exit_code"] == 0
              and not cell["invented_findings"],
              f"rule 3: {arm} matched conflict_surfaced's clean exit inventing nothing")

    # Rule 5, first clause. Two unmeasured cells on the 70B were to become
    # measurements, and the voided disqualification was to return or not.
    was = {u["fixture"] for u in base["B-70b"]["unmeasured_fixtures"]}
    now = set(new["B-70b"]["summary"]["exit_code_unmeasured"])
    check(was == {"conflict_surfaced", "numeric_drift"} and now == {"numeric_drift"},
          "rule 5: of the 70B's two unmeasured cells, conflict_surfaced resolved "
          "to a measurement and numeric_drift did not")
    check(base["B-70b"]["disqualified_as_run"] and not new["B-70b"]["summary"]["disqualified"],
          "rule 5: the 70B's voided disqualification did not return")

    # Rule 5, second clause. 13/13 was reachable for the 120B by one route only.
    c = new["C-120b"]["summary"]
    check(len(c["exit_code_matched"]) == 11
          and sorted(c["exit_code_missed"]) == ["attribution_invented", "disjoint_sources"],
          "rule 5: gpt-oss:120b did not reach 13/13; it matched 11 and missed two")
    check(len(c["disqualified"]) == 2,
          "rule 5: gpt-oss:120b is disqualified on both clauses of the rule")

    # Rule 7. Same weights, different machine, so the 2026-08-30 column above is
    # cross-day and every comparison drawn from it inherits that.
    old_ids = {r["harvest"]["endpoint"]["id"] for a in ARMS for r in old[a]["records"]}
    check(old_ids and ENDPOINT not in old_ids,
          f"rule 7: 2026-08-30 ran on {sorted(old_ids)}, not {ENDPOINT}, so every "
          "comparison to it is cross-day")
    return bad


def self_test() -> int:
    """A grading that cannot fail is a grading that reports nothing."""
    global EXPECTED
    keep = EXPECTED
    try:
        EXPECTED = dict(keep, **{"A-27b": (13, 0, 0, 6, 0)})
        if not grade(quiet=True):
            print("the grading stayed silent on a wrong arm total", file=sys.stderr)
            return 1
    finally:
        EXPECTED = keep
    if grade(quiet=True):
        print("the grading fails on the records as they stand", file=sys.stderr)
        return 1
    print("  self-test: the grading fails on a wrong total and passes on the records")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", dest="probe",
                        help="prove the checks can fail")
    args = parser.parse_args(argv)

    missing = [f"detect-2026-09-03-{a}.json" for a in ARMS
               if not (RECORDS / f"detect-2026-09-03-{a}.json").is_file()]
    if missing:
        print("no re-run records in this tree, so the grading is unchecked here: "
              + ", ".join(missing))
        return 0

    if args.probe:
        return self_test()
    if self_test() != 0:
        return 1
    bad = grade()
    if bad:
        print(f"{len(bad)} claim(s) section 10.6 makes are not what the records say",
              file=sys.stderr)
        return 1
    print("  the 2026-09-03 re-run grades as section 10.6 reports it, on every claim")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
