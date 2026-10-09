#!/usr/bin/env python3
"""The source-survival instrument, run over the merges already on disk. No model call.

This script exists to measure what fraction of the sources survived a merge. A merge that was
a concatenation, and that had dropped both titles and both summary fields,
reported 12/12 forward, 14/14 reverse and 26/26 evidence grounded. Every number
was right. None of them was about what fraction of the sources survived, because
nothing in the tool measured that — the chain is `source -> decompose -> claims
-> verify` and only the verify half had a denominator.

This script supplies the missing half and points it at the corpus that already
exists, before any prompt is changed. **The instrument must predate the cure.**

## Read the absent column as an upper bound

The recorded merges were produced under a prompt whose lines 23-25 granted the
model the whole document skeleton — "Order, headings and wording are yours to
choose" — and they carry no disposition records. So a segment this script
cannot find in a merge is **unexplained**, not wrong: the model was allowed to
reword it, and there is nothing on file saying whether it did.

Reporting the absent count as a defect count would be this project's own earlier error committed
in the opposite direction, which is why the header says so and why every table
prints its denominator beside its figure.

## What is measured

    segments  the source's own segments -- the denominator that was missing
    present   found in the merge, whitespace and one capital aside
    near      not found, but close to something that is (>= NEAR_MATCH)
    absent    not found and not close to anything. Upper bound on silent loss.
    tokens    invariant-core tokens checked, and how many did not survive
    dup       content the merge states twice, exactly or nearly
    runs      contiguous blocks the merge falls into by source document, over
              the number of merge segments attributable to one source at all

`runs` is a correction to the old concatenation predicate, which called
a merge a concatenation when its text resembled the two sources stapled
together above a similarity ratio, which only fires on a near-total copy. Two
sources set end to end give `runs` of 2 however much was dropped on the way,
so a *partial* concatenation — the case that started this milestone — is
visible as a staple rather than lost under the ratio.

Both predicates are printed. Where they disagree, the ratio is the one that is
wrong, and the disagreement is the finding.

Run with `python3 tests/measure_merges.py`. Always exits 0 on a finding: this
measures, it does not grade.
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

socket_guard.install()

from llossless import reconcile  # noqa: E402

import analyse_merges  # noqa: E402

FIXTURES = ROOT / "tests" / "fixtures"
MERGES = ROOT / "tests" / "responses" / "m4" / "merges"

# Sources are read from each fixture's directory, every `source_<letter>.md`
# from `a` with no gap, by `analyse_merges.sources_of`. This was
# `source_names(2)`, which was right for the two-source corpus and silently wrong for
# `tests/handwritten/`'s three-source pairs: `source_c.md` was never read.

BANNER = (
    "=" * 78,
    "  INSTRUMENT: segment coverage over merges recorded under the OLD prompt.",
    "  The absent column is an UPPER BOUND ON SILENT LOSS, not a defect count. These",
    "  merges carry no disposition records, so an absence here is unexplained rather",
    "  than wrong: the prompt that produced them permitted rewording and restructuring",
    "  outright. Every figure below prints its denominator.",
    "=" * 78,
)


def measure(path: Path, fixtures_root: Path = FIXTURES) -> dict:
    """Every Phase 1 figure for one recorded merge, plus the old predicate."""
    fixture, condition, sample = path.stem.rsplit("-", 2)
    merged = path.read_text(encoding="utf-8")
    documents = analyse_merges.sources_of(fixture, fixtures_root)
    result = reconcile.reconcile(documents, merged)
    ratio = analyse_merges.concatenation_ratio(fixture, merged, fixtures_root)
    # `reference_is_concatenation` reads a fixture's own `merged.md` under
    # `fixtures_root/fixture/`. The two-source corpus carries one for every fixture;
    # a corpus promoted with no answer key (`tests/handwritten/`, by design:
    # its `reference.md` is a reference and not an oracle)
    # does not, so there is nothing to ask "was the hand answer itself a
    # staple" about. Missing means "no reference to except from the general
    # rule", not "not a staple" -- `totals()` reads the same way either way.
    has_reference = (fixtures_root / fixture / "merged.md").is_file()
    reference_stapled = (
        analyse_merges.reference_is_concatenation(fixture, fixtures_root)
        if has_reference else False
    )
    return {
        "fixture": fixture,
        "condition": condition,
        "sample": int(sample),
        "result": result,
        # The old predicate, kept beside the new one so the two can disagree in
        # public. `reference_is_concatenation` is why disjoint_sources is not a
        # defect when stapled: its own `merged.md` is a staple too.
        "ratio": ratio,
        "ratio_says_concatenated": ratio >= analyse_merges.CONCATENATION,
        "has_reference": has_reference,
        "reference_stapled": reference_stapled,
    }


def table(rows: list[dict]) -> None:
    header = (
        f"  {'fixture':22} {'cond':4} {'s':>1}  {'segs':>4} {'pres':>4} {'near':>4} "
        f"{'abs':>4}  {'tok':>4} {'miss':>4}  {'dup':>3}  {'runs':>7} {'head':>7}  notes"
    )
    print(f"\n  Per merge. `segs` is the denominator; every other count is out of it.\n")
    print(header)
    print("  " + "-" * (len(header) - 2))
    for row in sorted(rows, key=lambda r: (r["fixture"], r["condition"], r["sample"])):
        result = row["result"]
        order = result.order
        notes = []
        if order.stapled and not row["reference_stapled"]:
            notes.append("STAPLED")
        elif order.stapled:
            notes.append("stapled (correct here)")
        if row["ratio_says_concatenated"] != order.stapled:
            notes.append(
                "ratio says concatenated" if row["ratio_says_concatenated"]
                else "PARTIAL CONCATENATION -- the ratio predicate misses this"
            )
        if order.headings_present < order.headings_total:
            notes.append(f"{order.headings_total - order.headings_present} heading(s) gone")
        if result.missing:
            notes.append(f"{len(result.missing)} invariant token(s) changed")
        print(
            f"  {row['fixture']:22} {row['condition']:4} {row['sample']:1d}  "
            f"{result.total:4d} {result.present:4d} {result.reworded:4d} {result.absent:4d}  "
            f"{result.tokens:4d} {len(result.missing):4d}  {len(result.duplicates):3d}  "
            f"{order.runs:3d}/{order.attributed:<3d} "
            f"{order.headings_present:3d}/{order.headings_total:<3d}  "
            f"{', '.join(notes)}"
        )


def totals(rows: list[dict]) -> None:
    merges = len(rows)
    segments = sum(row["result"].total for row in rows)
    present = sum(row["result"].present for row in rows)
    near = sum(row["result"].reworded for row in rows)
    absent = sum(row["result"].absent for row in rows)
    tokens = sum(row["result"].tokens for row in rows)
    missing = sum(len(row["result"].missing) for row in rows)

    print(f"\n  Over {merges} recorded merge(s):")
    print(f"    segment coverage      {present}/{segments} present "
          f"({100 * present / segments:.1f}%), {near} near, {absent} absent")
    print(f"    upper bound on silent loss  {absent}/{segments} "
          f"({100 * absent / segments:.1f}%) -- unexplained, not wrong")
    print(f"    invariant-core tokens {tokens - missing}/{tokens} survived unchanged "
          f"({missing} did not)")

    stapled = [row for row in rows if row["result"].order.stapled]
    defect = [row for row in stapled if not row["reference_stapled"]]
    eligible = [row for row in rows if not row["reference_stapled"]]
    old = [row for row in eligible if row["ratio_says_concatenated"]]
    print(f"\n  Entry 3a, both predicates, over the {len(eligible)} merge(s) where "
          f"stapling is a defect:")
    print(f"    runs == documents (new)   {len(defect):3d} / {len(eligible)}")
    print(f"    similarity ratio (old)    {len(old):3d} / {len(eligible)}")
    caught = {(row["fixture"], row["condition"], row["sample"]) for row in defect}
    seen = {(row["fixture"], row["condition"], row["sample"]) for row in old}
    if caught - seen:
        print(f"    {len(caught - seen)} merge(s) are partial concatenations the ratio "
              f"predicate misses:")
        for fixture, condition, sample in sorted(caught - seen):
            print(f"      {fixture} [{condition}] sample {sample}")
    if seen - caught:
        print(f"    {len(seen - caught)} merge(s) the ratio calls concatenated and the "
              f"run count does not:")
        for fixture, condition, sample in sorted(seen - caught):
            print(f"      {fixture} [{condition}] sample {sample}")

    headings = sum(row["result"].order.headings_total for row in rows)
    kept = sum(row["result"].order.headings_present for row in rows)
    print(f"\n  Heading-set survival  {kept}/{headings} source titles and headings still "
          f"locatable ({headings - kept} gone)")

    by_kind: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for row in rows:
        for coverage in row["result"].coverages:
            for item in coverage.located:
                by_kind[item.segment.kind][1] += 1
                if item.verdict == reconcile.ABSENT:
                    by_kind[item.segment.kind][0] += 1
    print(f"\n  Absences by segment kind, each over its own denominator:")
    for kind in sorted(by_kind, key=lambda k: -by_kind[k][0]):
        gone, total = by_kind[kind]
        print(f"    {kind:12} {gone:4d} / {total:4d} absent ({100 * gone / total:5.1f}%)")


def worst(rows: list[dict], limit: int) -> None:
    print(f"\n  The {limit} absences most often repeated across the corpus, so a reader")
    print("  can judge the calls rather than take them:\n")
    counted: dict[tuple[str, str, str], int] = defaultdict(int)
    for row in rows:
        for coverage in row["result"].coverages:
            for item in coverage.of(reconcile.ABSENT):
                counted[(row["fixture"], item.segment.kind, item.segment.text)] += 1
    for (fixture, kind, text), n in sorted(counted.items(), key=lambda p: -p[1])[:limit]:
        print(f"    {n:3d}x {fixture:20} {kind:10} {text[:60]!r}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--merges", type=Path, default=MERGES)
    parser.add_argument("--fixture", action="append", help="restrict to this fixture")
    parser.add_argument("--worst", type=int, default=12)
    # Default is `FIXTURES` (byte-identical to the pre-flag behaviour), so the
    # two-source corpus still scores the same with no arguments. Added so a second
    # corpus -- `tests/handwritten/`, which deliberately sits outside
    # `tests/fixtures/` so it is invisible to `run_merge.fixture_names()` and
    # its sweep denominators, can be scored with this same instrument
    # rather than a second one.
    parser.add_argument("--fixtures-root", type=Path, default=FIXTURES)
    args = parser.parse_args(argv)

    if not args.merges.is_dir():
        print(f"no such directory: {args.merges}", file=sys.stderr)
        return 2
    if not args.fixtures_root.is_dir():
        print(f"no such directory: {args.fixtures_root}", file=sys.stderr)
        return 2
    paths = sorted(args.merges.glob("*.md"))
    if args.fixture:
        paths = [p for p in paths if p.stem.rsplit("-", 2)[0] in set(args.fixture)]
    if not paths:
        print(f"no merges in {args.merges}", file=sys.stderr)
        return 2

    # A fixture whose sources have a gap is refused before anything prints:
    # it is a corpus with a document missing, not a finding.
    try:
        rows = [measure(path, args.fixtures_root) for path in paths]
    except analyse_merges.SourceGap as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 2

    for line in BANNER:
        print(line)
    print(f"\n  Near-match threshold {reconcile.NEAR_MATCH}, chosen from the score distribution "
          f"over this corpus; the reasoning is beside NEAR_MATCH in src/llossless/reconcile.py.")

    table(rows)
    totals(rows)
    worst(rows, args.worst)

    print("\n  Absent means unexplained. This script measures and always exits 0.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
