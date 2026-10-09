#!/usr/bin/env python3
"""Re-score check 2 over recorded merges, so the paper can cite the split.

A later decision split `undeclared_absence` into an absence and a
rewording. Every figure in the paper that says "undeclared absence" was graded
before that split and counts both, which is the reading later found wrong:
a merge that rewrote six sentences and deleted eighteen was reported as having
lost twenty-four. The runs themselves are unaffected -- no model output changed,
and nothing here asks a model anything -- so the honest correction is to re-score
what was recorded rather than to re-run it.

What this re-scores is check 2 and only check 2. It needs three things from a
recorded run, all of which `report.json` and `merged.md` already carry:

  * the merged document, byte for byte, as the run wrote it
  * which segment ids carried a disposition record, from `declarations`
  * the two sources, passed in, because the record does not carry them

That is the whole of check 2's input -- `reconcile.py`'s check 2 reads
`located.segment.id in declared or located.found` and nothing else -- so the
re-score is exact rather than approximate, and the script proves it: for every
arm it asserts that its own absence-plus-rewording total and its own segment
set reproduce what the run recorded under the single old kind. An arm whose
re-score disagrees with the run is a bug in this file, and it stops the run.

It does not re-score checks 1 and 3 to 9. `report.json`'s `declarations` block
is a *graded* view that drops the `replacement` field, so a disposition read
back from it cannot be held against the merge text, and a title check run on it
reports every kept title as replaced by nothing. Checks that need the raw
disposition records need the response cassette, and this file deliberately does
not go there: it would be re-running the grader from a different input than the
one it is checking.

The output is a record in `paper/records/`, named `regrade-<label>.json` so that
the paper's own figure builder (not part of a published copy) gives it its own `regrade.<label>.*` key
prefix. It is not written back into the sweep record and does not share its
prefix. A sweep record is what a run produced on the day, and a number this
file derived afterwards has different provenance and has to say so in its own
name -- a reader who sees `regrade.pair429.B1-70b-default.undeclared_rewording`
knows it was not measured by the run that produced
`sweep.pair429.B1-70b-default.merged_bytes`.

Usage:

    tests/regrade_check2.py --pair tests/pairs/index_429 --label pair429 \\
        --sweep /path/to/sweep-pair429.json \\
        --arm B1-70b-default=/path/to/2026-08-30/2c/B1-70b-default \\
        --arm ...

Each `--arm` may name several directories separated by commas, which is how a
K-draw arm is passed. They must hold byte-identical merges: the sweep record
summarises K draws into one row, and re-scoring one of them is only legitimate
when the choice of draw could not have changed the answer. The script checks
that rather than assuming it.
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

from llossless import reconcile  # noqa: E402

socket_guard.install()

SOURCES = ("source_a.md", "source_b.md")
# The kind the runs recorded, before the split. Named as a literal rather than
# as `reconcile.UNDECLARED_ABSENCE` because it is a string in a file on disk
# written by an older version of that module: if the constant were renamed
# tomorrow this file would still have to read the old records.
RECORDED_KIND = "undeclared_absence"


def check_two(pair: dict[str, str], merged: str, declared: set[str]) -> tuple[list[dict], dict]:
    """Check 2's findings, and the per-source denominators they are fractions of.

    The denominators are written down because the interesting number is not
    "eighteen of sixty-three segments over two documents". A merge is entitled
    to compress what its two sources say twice; it is not entitled to empty one
    of them, and only a per-source count can tell those apart. Both totals are
    recorded so neither has to be arrived at by subtraction.
    """
    result = reconcile.reconcile(pair, merged)
    rows = []
    totals = {}
    for coverage in result.coverages:
        name = coverage.document.filename or coverage.document.id
        totals[name] = len(coverage.located)
        for located in coverage.located:
            if located.segment.id in declared or located.found:
                continue
            kind = (reconcile.UNDECLARED_ABSENCE if located.verdict == reconcile.ABSENT
                    else reconcile.UNDECLARED_REWORDING)
            rows.append({"segment": located.segment.id, "kind": kind,
                         "document": name, "nearest": located.nearest,
                         "ratio": round(located.ratio, 4)})
    return rows, totals


def regrade(pair: dict[str, str], directories: list[Path], recorded: dict) -> dict:
    """One arm. Raises on any disagreement with what the run recorded."""
    merges = {path.name: (path / "merged.md").read_bytes() for path in directories}
    distinct = set(merges.values())
    if len(distinct) != 1:
        sizes = {name: len(blob) for name, blob in merges.items()}
        raise SystemExit(f"draws are not byte-identical, so re-scoring one of them "
                         f"would be a choice: {sizes}")
    merged = distinct.pop().decode("utf-8")

    report = json.loads((directories[0] / "report.json").read_text(encoding="utf-8"))
    declared = {str(item.get("segment", "")).strip()
                for item in report.get("declarations", [])}
    was = [finding for finding in (report.get("structural") or {}).get("findings", [])
           if finding.get("kind") == RECORDED_KIND]

    rows, totals = check_two(pair, merged, declared)
    if len(rows) != len(was):
        raise SystemExit(f"re-scored {len(rows)} check-2 findings, the run recorded "
                         f"{len(was)}; the split must not change the total")
    if sorted(row["segment"] for row in rows) != sorted(str(f.get("segment")) for f in was):
        raise SystemExit(f"re-scored {sorted(row['segment'] for row in rows)}, the run "
                         f"recorded {sorted(str(f.get('segment')) for f in was)}")

    by_kind = collections.Counter(row["kind"] for row in rows)
    per_document = collections.Counter((row["document"], row["kind"]) for row in rows)
    fidelity = ((report.get("provenance") or {}).get("merge_policy") or {}).get("fidelity")
    return {
        "arm": recorded["arm"],
        "model": recorded.get("model"),
        "fidelity": fidelity,
        "merged_bytes": len(merged.encode("utf-8")),
        "structural": {
            "ran": True,
            "check": 2,
            "segments": (recorded.get("structural") or {}).get("segments"),
            "findings": len(rows),
            "by_kind": {
                reconcile.UNDECLARED_ABSENCE: by_kind.get(reconcile.UNDECLARED_ABSENCE, 0),
                reconcile.UNDECLARED_REWORDING: by_kind.get(reconcile.UNDECLARED_REWORDING, 0),
            },
            "by_document": {
                name: {
                    "segments": total,
                    reconcile.UNDECLARED_ABSENCE:
                        per_document.get((name, reconcile.UNDECLARED_ABSENCE), 0),
                    reconcile.UNDECLARED_REWORDING:
                        per_document.get((name, reconcile.UNDECLARED_REWORDING), 0),
                }
                for name, total in totals.items()
            },
            # Every row, so that a reader can check the split segment by segment
            # against `reconcile.NEAR_MATCH` instead of taking the counts on
            # trust. The ratio is the whole of the evidence for which kind a
            # segment got.
            "rows": rows,
            "near_match": reconcile.NEAR_MATCH,
        },
        # Named, because two of the sweep's arms have draws in more than one
        # directory and one of them has a `merged_bytes` that matches none of
        # them. What was re-scored is not inferable from the
        # arm label.
        "regraded_from": [str(path) for path in directories],
        "recorded_undeclared_absence": len(was),
    }


# --------------------------------------------------------------------------
# `--self-test`
# --------------------------------------------------------------------------
#
# This file writes a record the paper cites, and its only real safeguard is the
# pair of assertions in `regrade` that hold the re-score against the run. An
# assertion nobody exercises is the failure mode the never-
# wired reconciler already showed, so each one gets a probe that must fire and the
# correct case gets one that must not.

SELF_A = "# Relay Handbook\n\nThe relay listens on port 8443.\nThe connect timeout is 30 seconds.\n"
# Not the reconciler's own pair, whose two distinct facts are both timeout
# sentences and so score 0.80 against each other. A deleted segment there has
# the surviving twin to be matched to, which is the ambiguous case
# `tests/test_reconcile.py` registers; a probe should test the rule rather than
# the exception, so b3 here resembles nothing in the merge.
SELF_B = "# Relay Notes\n\nThe relay listens on port 8443.\nOperators are paged by the on-call rota.\n"
# a3 rewritten, b3 gone: one of each kind, which is the whole point of a probe
# for a split.
SELF_MERGE = ("# Relay Handbook\n\nThe relay listens on port 8443.\n"
              "The connect timeout is set to 30 seconds.\n")


def _self_report(count: int) -> dict:
    return {
        "provenance": {"merge_policy": {"fidelity": "off"}},
        "declarations": [{"segment": "b1", "disposition": "superseded"},
                         {"segment": "b2", "disposition": "duplicate"}],
        "structural": {"findings": [{"kind": RECORDED_KIND, "segment": segment}
                                    for segment in ("a3", "b3")[:count]]},
    }


def self_test() -> int:
    import tempfile

    pair = {"source_a.md": SELF_A, "source_b.md": SELF_B}
    recorded = {"arm": "self", "model": "none", "structural": {"segments": 6}}
    failures = []

    def probe(name: str, must_fire: bool, body) -> None:
        try:
            body()
        except SystemExit as exit:
            if not must_fire:
                failures.append(f"{name}: refused a correct input -- {exit}")
            return
        if must_fire:
            failures.append(f"{name}: accepted an input it must refuse")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        good, other = root / "d1", root / "d2"
        for directory, merged in ((good, SELF_MERGE), (other, SELF_MERGE + "Extra.\n")):
            directory.mkdir()
            (directory / "merged.md").write_text(merged, encoding="utf-8")
            (directory / "report.json").write_text(json.dumps(_self_report(2)), encoding="utf-8")

        probe("draws must be byte-identical", True,
              lambda: regrade(pair, [good, other], recorded))

        (good / "report.json").write_text(json.dumps(_self_report(1)), encoding="utf-8")
        probe("a total that disagrees with the run", True,
              lambda: regrade(pair, [good], recorded))

        (good / "report.json").write_text(json.dumps({
            **_self_report(2),
            "structural": {"findings": [{"kind": RECORDED_KIND, "segment": s}
                                        for s in ("a3", "b2")]},
        }), encoding="utf-8")
        probe("a segment set that disagrees with the run", True,
              lambda: regrade(pair, [good], recorded))

        (good / "report.json").write_text(json.dumps(_self_report(2)), encoding="utf-8")
        probe("the correct case", False, lambda: regrade(pair, [good], recorded))

        out = regrade(pair, [good], recorded)
        kinds = out["structural"]["by_kind"]
        if kinds != {reconcile.UNDECLARED_ABSENCE: 1, reconcile.UNDECLARED_REWORDING: 1}:
            failures.append(f"a3 was reworded and b3 removed, so one of each; got {kinds}")
        rows = {row["segment"]: row["kind"] for row in out["structural"]["rows"]}
        if rows.get("a3") != reconcile.UNDECLARED_REWORDING:
            failures.append(f"a3 was rewritten, not removed; got {rows.get('a3')}")
        if rows.get("b3") != reconcile.UNDECLARED_ABSENCE:
            failures.append(f"b3 is gone, not reworded; got {rows.get('b3')}")
        if out["fidelity"] != "off":
            failures.append(f"the level must be read from the run; got {out['fidelity']!r}")

    for line in failures:
        print(f"  FAIL {line}")
    if not failures:
        print("  self-test: 3 must-fire probe(s) fire, the correct case is quiet, "
              "the split is a rewording and an absence")
    return 1 if failures else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--self-test", action="store_true",
                    help="exercise the guards on a synthetic pair; no records read")
    ap.add_argument("--pair", type=Path,
                    help="directory holding source_a.md and source_b.md")
    ap.add_argument("--label", help="record label, e.g. pair429")
    ap.add_argument("--sweep", type=Path,
                    help="the sweep record this re-scores, for the arm rows")
    ap.add_argument("--arm", action="append", default=[], metavar="NAME=DIR[,DIR...]",
                    help="an arm and the run directories holding its draws")
    ap.add_argument("--out", type=Path, default=ROOT / "paper" / "records")
    args = ap.parse_args(argv)

    if args.self_test:
        return self_test()
    for required in ("pair", "label", "sweep"):
        if getattr(args, required) is None:
            ap.error(f"--{required} is required unless --self-test is given")

    pair = {name: (args.pair / name).read_text(encoding="utf-8") for name in SOURCES}
    sweep = {arm["arm"]: arm for arm in json.loads(args.sweep.read_text(encoding="utf-8"))}

    out = []
    for spec in args.arm:
        name, _, joined = spec.partition("=")
        if name not in sweep:
            raise SystemExit(f"{name!r} is not an arm of {args.sweep.name}")
        directories = [Path(part) for part in joined.split(",") if part]
        if not directories:
            raise SystemExit(f"{name}: no run directory given")
        out.append(regrade(pair, directories, sweep[name]))
        row = out[-1]["structural"]["by_kind"]
        print(f"  {name}: {out[-1]['recorded_undeclared_absence']} recorded -> "
              f"{row['undeclared_absence']} absent + {row['undeclared_rewording']} reworded "
              f"(fidelity {out[-1]['fidelity']})")
        for document, counts in sorted(out[-1]["structural"]["by_document"].items()):
            print(f"      {document}: {counts['undeclared_absence']} absent, "
                  f"{counts['undeclared_rewording']} reworded, of {counts['segments']}")

    args.out.mkdir(parents=True, exist_ok=True)
    target = args.out / f"regrade-{args.label}.json"
    target.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(f"  {len(out)} arm(s) -> {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
