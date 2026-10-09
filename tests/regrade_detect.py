#!/usr/bin/env python3
"""Re-score the recorded detection arms against the repaired fixtures.

Two fixtures disagreed with themselves, and the disagreement scored the arms.
`conflict_surfaced` declared exit 1 with nothing planted and
eleven all-`SUPPORTED` probes, so the only way to reach the expected code was to
invent a finding; `numeric_drift` declared exit 1 in both modes while sanctioning
a reading that exits 0, so an arm taking that reading was disqualified for
correct behaviour. Both are repaired. The runs are not affected -- no model
output changed, and nothing here asks a model anything -- so the honest
correction is to re-score what was recorded rather than to re-run it, exactly as
`tests/regrade_check2.py` did for check 2.

What comes out is not a corrected pass or a corrected failure. It is a third
state, `unmeasured`: this fixture could not take a reading on this arm. A blank
cell beside a pass reads as a pass, and folding an unmeasured fixture into
either column would claim a measurement the study does not have.

Two rules, both auditable from the records:

  1. **The fixture was broken when the arm ran.** The record says which exit
     code the arm was graded against. Where that differs from what the repaired
     fixture declares, the arm was measured against a fixture that no longer
     exists, and no verdict from it survives -- in either direction. This is
     what voids `conflict_surfaced` on all three arms, including the arm the
     study credited with matching it.
  2. **The arm took a sanctioned alternative reading.** Where the repaired
     fixture's strict and lenient codes differ and the arm landed on the lenient
     one with nothing invented, `fixture_semantics.outcome` calls it unmeasured.
     This is what voids `numeric_drift` on B-70b.

Rule 2 has a limit these records cannot pass, and the output says so per arm
rather than in a footnote. `fixture_semantics.outcome` also requires that no
planted probe was plainly missed, which needs the per-probe verdicts.
`run_detect.py` records those now; it did not on 2026-08-30, and `half1.sh` did
not pass `--reports-dir`, so the reports are gone too. Whether B-70b answered
`SUPPORTED` on the soft probe or never extracted the claim at all is not
recoverable from what survives. Either way the fixture as declared could not
measure it, which is what `unmeasured` says; but the record must not imply the
stronger reading, so every fixture re-scored without probe evidence is listed
under `unverifiable_conditions`.

The output is `paper/records/regrade-detect.json`, giving it the
`regrade.detect.<arm>.*` key prefix. A reader who sees
`regrade.detect.B-70b.matched` therefore knows it was not measured by the run
that produced `detect.B-70b.exit_code_matched`.

Usage:

    tests/regrade_detect.py                 write the record
    tests/regrade_detect.py --print         write nothing, print the table
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import fixture_semantics  # noqa: E402
import run_detect  # noqa: E402
import socket_guard  # noqa: E402

socket_guard.install()

# The date of the amendment, not the date of the run. Hard-coded so that
# re-running this file is idempotent: the record is a committed artefact and the
# paper cites this through a `\ccnum` key, so a wall-clock stamp would move a
# published figure every time somebody regenerated it.
AMENDED = "2026-09-03"

RECORDS = ROOT / "paper" / "records"
OUT = RECORDS / "regrade-detect.json"

BROKEN_AT_MEASUREMENT = (
    "the fixture declared exit {was} when this arm ran and declares {now} now; "
    "the arm was graded against a fixture that no longer exists"
)
SANCTIONED_READING = (
    "the fixture sanctions a reading that exits {lenient} as well as the strict "
    "{strict}, and this arm exited {got} having invented nothing"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rescore(record: dict, declared: dict) -> tuple[str, str]:
    """(outcome, why) for one recorded fixture result against the repaired fixture."""
    was, got = record["expected_exit_code"], record["exit_code"]
    if was != declared["strict"]:
        return fixture_semantics.UNMEASURED, BROKEN_AT_MEASUREMENT.format(
            was=was, now=declared["strict"])
    outcome = fixture_semantics.outcome(
        declared, got, len(record.get("invented_findings") or []),
        record.get("probes") or [], reported=record.get("report_written") is not False)
    if outcome == fixture_semantics.UNMEASURED:
        return outcome, SANCTIONED_READING.format(
            lenient=declared["lenient"], strict=declared["strict"], got=got)
    return outcome, ""


def as_run_inventions(record: dict) -> int:
    """How many findings the run recorded as unaccounted, before any withholding."""
    if "invented_findings_as_run" in record:
        return len(record["invented_findings_as_run"])
    return len(record.get("invented_findings") or [])


def regrade_arm(source: Path) -> dict:
    blob = json.loads(source.read_text(encoding="utf-8"))
    summary, records = blob["summary"], blob["records"]

    rescored, unverifiable = [], []
    for record in records:
        expected = run_detect.load_expected(record["fixture"])
        declared = expected["expected_exit_code"]
        outcome, why = rescore(record, declared)
        fresh = dict(record, outcome=outcome,
                     expected_exit_code=declared["strict"],
                     expected_exit_code_lenient=declared["lenient"],
                     regrade_why=why)
        # `invented_findings` means "no probe in the fixture accounts for this",
        # so it is a statement about the answer key the run was graded against.
        # Where the key has since gained a plant -- `attribution_swapped` was
        # repaired, from one probe to two -- the stored list
        # was computed against a fixture that no longer exists, and some of what
        # is on it is now accounted for. Re-accounting needs the per-fixture
        # report, which this program does not have: it re-grades from records.
        # So the invention clause is withheld here rather than applied to a
        # stale list, and the withholding is named in the output. Applying it
        # would have disqualified all three arms for correctly reading the half
        # of the swap the fixture had not yet probed.
        if len(run_detect.planted(expected)) != record.get("plants"):
            unverifiable.append(
                f"{record['fixture']}: the fixture's planted probes changed "
                f"from {record.get('plants')} to "
                f"{len(run_detect.planted(expected))} since this run, so "
                f"`invented_findings` cannot be re-accounted from the record")
            fresh["invented_findings"] = []
            fresh["invented_findings_as_run"] = list(
                record.get("invented_findings") or [])
        rescored.append(fresh)
        # Only rule 2 needs the probes. Rule 1 rests on the fixture's own
        # declared code, which the record carries, so it is verifiable from
        # what survives and does not belong on this list.
        if why.startswith("the fixture sanctions") and not record.get("probes"):
            unverifiable.append(record["fixture"])

    by = {name: [r for r in rescored if r["outcome"] == name]
          for name in fixture_semantics.OUTCOMES}
    unmeasured = by[fixture_semantics.UNMEASURED]
    # An errored fixture (exit 2, no report) is no more measured than an
    # unmeasured one. No record this regrades has one.
    measured = [r for r in rescored if r["outcome"] not in (fixture_semantics.UNMEASURED,
                                                            fixture_semantics.ERRORED)]
    return {
        "arm": summary["label"],
        "record": source.name,
        "sha256": sha256(source),
        "model": run_detect_model(summary),
        "fixtures": len(rescored),
        "fixtures_measured": len(measured),
        "matched": len(by[fixture_semantics.MATCHED]),
        "unmeasured": len(unmeasured),
        "missed": len(by[fixture_semantics.MISSED]),
        "matched_fixtures": sorted(r["fixture"] for r in by[fixture_semantics.MATCHED]),
        "unmeasured_fixtures": [{"fixture": r["fixture"], "why": r["regrade_why"]}
                                for r in sorted(unmeasured, key=lambda r: r["fixture"])],
        "missed_fixtures": sorted(r["fixture"] for r in by[fixture_semantics.MISSED]),
        "plants_total": sum(r["plants"] for r in rescored),
        "plants_unmeasured": sum(r["plants"] for r in unmeasured),
        "plants_detected": sum(len(r["detected"]) for r in measured),
        # The descriptive counts stay what the run recorded. Withholding the
        # disqualifier clause is a statement about what this program can
        # re-derive, not a claim that the findings were never filed.
        "invented_total": sum(as_run_inventions(r) for r in rescored),
        "invented_on_unmeasured": sum(as_run_inventions(r) for r in unmeasured),
        "disqualified": run_detect.disqualified(rescored),
        "disqualified_as_run": list(summary["disqualified"]),
        "unverifiable_conditions": sorted(unverifiable),
    }


def run_detect_model(summary: dict) -> str | None:
    through = summary.get("passthrough") or []
    return through[through.index("--model") + 1] if "--model" in through else None


# The re-score's own must-fire probes. Each is a recorded fixture result and the
# repaired fixture's codes, with the outcome the two must produce. A re-score
# that cannot be shown to call anything unmeasured is a re-score whose counts
# mean nothing, and the two states it must not confuse are the two the study
# already got wrong once.
PROBES = (
    ("graded against a fixture that has since been repaired",
     {"expected_exit_code": 1, "exit_code": 0, "invented_findings": []},
     {"strict": 0, "lenient": 0}, fixture_semantics.UNMEASURED),
    ("the same, for the arm that reached the old code by inventing a finding",
     {"expected_exit_code": 1, "exit_code": 1,
      "invented_findings": [{"claim_id": "M-007"}]},
     {"strict": 0, "lenient": 0}, fixture_semantics.UNMEASURED),
    ("a sanctioned alternative reading",
     {"expected_exit_code": 1, "exit_code": 0, "invented_findings": []},
     {"strict": 1, "lenient": 0}, fixture_semantics.UNMEASURED),
    ("the strict reading, on a fixture that admits two",
     {"expected_exit_code": 1, "exit_code": 1, "invented_findings": []},
     {"strict": 1, "lenient": 0}, fixture_semantics.MATCHED),
    ("a plain miss, which no repair excuses",
     {"expected_exit_code": 1, "exit_code": 0, "invented_findings": []},
     {"strict": 1, "lenient": 1}, fixture_semantics.MISSED),
    ("an invented finding on a fixture that expects a clean exit",
     {"expected_exit_code": 0, "exit_code": 1,
      "invented_findings": [{"claim_id": "A-002"}]},
     {"strict": 0, "lenient": 0}, fixture_semantics.MISSED),
    ("a probe the arm never answered, which the lenient code must not excuse",
     {"expected_exit_code": 1, "exit_code": 0, "invented_findings": [],
      "probes": [{"probe_id": "p", "verdict": fixture_semantics.MISSED}]},
     {"strict": 1, "lenient": 0}, fixture_semantics.MISSED),
)


def self_test() -> int:
    bad = []
    for why, record, declared, want in PROBES:
        got, _ = rescore(record, declared)
        if got != want:
            bad.append(f"{why}: got {got!r}, want {want!r}")
    # And the disqualifier must not fire on an unmeasured fixture, which is the
    # clause the whole re-score turns on.
    unmeasured = {"fixture": "f", "expected_exit_code": 1, "exit_code": 0,
                  "invented_findings": [], "outcome": fixture_semantics.UNMEASURED}
    if run_detect.disqualified([unmeasured]):
        bad.append("the disqualifier fired on an unmeasured fixture")
    if not run_detect.disqualified([dict(unmeasured, outcome=fixture_semantics.MISSED)]):
        bad.append("the disqualifier stayed quiet on a seeded defect that exited clean")
    for line in bad:
        print(f"SELF-TEST FAILED: {line}")
    if bad:
        return 1
    print(f"  self-test: {len(PROBES)} must-fire probe(s) produce the outcome they "
          f"must, and the disqualifier fires only on a measured fixture")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--print", action="store_true", dest="show",
                        help="print the table and write nothing")
    parser.add_argument("--self-test", action="store_true", dest="probe",
                        help="prove the re-score can reach every outcome")
    args = parser.parse_args(argv)
    if args.probe:
        return self_test()
    if self_test() != 0:
        return 1

    sources = sorted(RECORDS.glob("half1-*.json"))
    if not sources:
        print(f"no half1-*.json records under {RECORDS}", file=sys.stderr)
        return 2
    arms = [regrade_arm(source) for source in sources]

    width = max(len(a["arm"]) for a in arms)
    for arm in arms:
        print(f"  {arm['arm']:<{width}}  matched {arm['matched']:>2}"
              f"  unmeasured {arm['unmeasured']:>2}"
              f"  missed {arm['missed']:>2}"
              f"   of {arm['fixtures']}")
        for entry in arm["unmeasured_fixtures"]:
            print(f"      unmeasured: {entry['fixture']} -- {entry['why']}")
        for line in arm["disqualified_as_run"]:
            still = line in arm["disqualified"]
            print(f"      disqualifier as run: {line}"
                  f"  [{'stands' if still else 'VOID'}]")
        if arm["unverifiable_conditions"]:
            print("      no per-probe record, so the narrow reading of"
                  " unmeasured is unverifiable on: "
                  + ", ".join(arm["unverifiable_conditions"]))

    if args.show:
        return 0
    OUT.write_text(json.dumps({"note": __doc__.split("\n\n")[1].strip(),
                               "amended": AMENDED, "arms": arms},
                              indent=2) + "\n", encoding="utf-8")
    print(f"\n  -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
