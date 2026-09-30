#!/usr/bin/env python3
"""A quality-first league table over recorded merge arms. No model call.

This is not a new quality instrument. It is `tests/measure_merges.py` --
`reconcile.reconcile`, unmodified -- pointed at runs that live outside the
repo, plus one join: the current merge tool writes declared dispositions to
its report, so `measure_merges`'s `absent` column (documented there as an
*upper bound on silent loss*, because the corpus it was built against
carries no disposition records at all) can be checked against what each merge
actually declared. What is left over after that check is a real defect count:

    silent_loss = segments the reconciler could not find in the merge,
                  AND NOT named in that run's own `declarations` list

A segment that is absent *and* declared (dropped, superseded, reworded,
subsumed -- anything in `parsing.DISPOSITIONS`) is the merge admitting what it
did; the reconciler's own `findings` step already checks a declaration against
the truth of what happened and would fail the run if the declaration lied.
Absent and undeclared is the merge saying nothing, which is the defect this project once set
out to measure and could not, for want of a denominator.

## What is NOT here

No weighted score. The operator's ranking is lexicographic -- quality, then
cost, then speed -- and a scalar composite is exactly the thing that has
already hidden a tradeoff in this project once (the
`length_ratio` figure). Disqualifying conditions are reported as
disqualifiers, not folded into a number: a model that staples two documents
end to end is unusable regardless of how cheap or fast it was getting there.

No threshold on any of the printed ratios. `length_ratio` and the old
concatenation-similarity ratio are both printed for the record and used for
nothing: a control corpus scored a *higher* ratio (0.970) than the positive
corpus's maximum (0.943), so no cut separates them, and a measured pair with
0 duplicates outscored one with 4 on the same ratio.
`runs`/`order.stapled` replaced it for
concatenation; nothing replaces it for anything else, because nothing here
needs it to.

## Where the inputs come from

Every run this script reads is a directory of the shape `<pair>-<fidelity>-
<arm>/` holding `merged.md` and `report.json`, indexed by a `results.json`
alongside it (`--run-dir`, repeatable). `report.json["documents"]` names each
source's *original* filename (e.g. `source_a.md -> chickens_1.md`); those
files are read from `--sources-root/<pair>/<original filename>`, and when
not there from `tests/handwritten/` by that original name, since not
every run directory keeps its own copy of the sources it merged
(`2026-09-16-phase4`'s run directories hold only `merged.md` and
`report.json`; `2026-09-17-frontier-thinking`'s hold copies too, and both read
identically because the reconciler only ever sees `documents["source_a.md"]`
etc., never the original filename).

A run with no `report.json` or no `merged.md` (the merge step errored before
writing one) is counted as a failure for that arm and left out of the
coverage/dup/staple arithmetic, which is disclosed in the table rather than
silently averaged in as zero.

Run with `python3 tests/league_table.py`. Exits 0: this measures, like
`measure_merges.py` does, and ranking is a separate, explicit step below the
raw numbers -- read the raw numbers first. `--check` compares with the
committed `tests/league_table.json` and exits 1 if it differs;
`tests/benchmark_matrix.py` makes the same comparison for its H rows.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

socket_guard.install()

from llossless import reconcile  # noqa: E402

# The recorded arms are published under `arms/`, and their
# sources are the hand-written pairs in `tests/handwritten/`, found by the
# original filename each pair's `meta.json` records. `LLOSSLESS_ARTEFACTS_ROOT`
# (the scratch mirror the runs were first written to), `--run-dir` and
# `--sources-root` override; a source not under `--sources-root` is looked up
# in `tests/handwritten/` by its original name.
_MIRROR = os.environ.get("LLOSSLESS_ARTEFACTS_ROOT")
DEFAULT_SOURCES_ROOT = Path(_MIRROR) if _MIRROR else ROOT / "tests" / "handwritten"
DEFAULT_RUN_DIRS = (
    (Path(_MIRROR) / "2026-09-17-frontier-thinking", Path(_MIRROR) / "2026-09-16-phase4")
    if _MIRROR else
    (ROOT / "arms" / "2026-09-17" / "frontier-thinking", ROOT / "arms" / "2026-09-16" / "phase4")
)
COMMITTED = ROOT / "tests" / "league_table.json"


def handwritten_by_origin() -> dict[str, Path]:
    """Original filename -> tracked copy, from each hand-written pair's meta.json."""
    out = {}
    for meta in sorted((ROOT / "tests" / "handwritten").glob("*/meta.json")):
        origin = json.loads(meta.read_text(encoding="utf-8")).get("origin") or {}
        for role, name in origin.items():
            if name and role.startswith("source_"):
                out[name] = meta.parent / f"{role}.md"
    return out


@dataclass
class ArmRun:
    """One recorded merge: identity from `results.json`, measurement from disk."""

    model: str          # the short label runs are grouped and ranked by
    full_model: str      # the vendor's own model id, informational only
    pair: str
    fidelity: str
    run_dir: Path
    exit_code: int | None
    wall_seconds: float | None
    cost_usd: float | None       # None means "not recorded", never 0
    # Filled in by `measure_run`; None means the run has no report to measure
    # (merge step errored before a report.json/merged.md existed).
    segments: int = 0
    present: int = 0
    near: int = 0
    absent: int = 0
    silent_loss: int = 0
    dup: int = 0
    stapled: bool = False
    measured: bool = False
    note: str = ""


def _label_of(row: dict) -> tuple[str, str, Path]:
    """(short label, full model id, run_dir) for one `results.json` row.

    Frontier rows carry `arm` (the short label the run directory and the
    ranking group on) separately from `model` (the vendor's full id, e.g.
    `claude-haiku-4-5-20251001` against a `claude-haiku-4-5` label and run
    directory -- `run_frontier.py:47`). Phase 4 rows carry neither `arm` nor a
    directory built the same way; they carry `run_dir` directly and a `model`
    that is already the full id, so the label is read off the directory name
    with the `<pair>-<fidelity>-` prefix removed instead.
    """
    if "arm" in row:
        label = row["arm"]
        run_dir_name = f"{row['pair']}-{row['fidelity']}-{label}"
    else:
        run_dir_name = row["run_dir"]
        prefix = f"{row['pair']}-{row['fidelity']}-"
        label = run_dir_name[len(prefix):] if run_dir_name.startswith(prefix) else run_dir_name
    return label, row.get("model", label), Path(run_dir_name)


def load_runs(run_dirs: list[Path]) -> list[ArmRun]:
    runs = []
    for run_dir in run_dirs:
        results_path = run_dir / "results.json"
        if not results_path.is_file():
            print(f"no results.json in {run_dir}, skipping", file=sys.stderr)
            continue
        rows = json.loads(results_path.read_text(encoding="utf-8"))
        for row in rows:
            label, full_model, subdir = _label_of(row)
            runs.append(ArmRun(
                model=label,
                full_model=full_model,
                pair=row["pair"],
                fidelity=row["fidelity"],
                run_dir=run_dir / subdir,
                exit_code=row.get("exit_code"),
                wall_seconds=row.get("wall_seconds"),
                cost_usd=row.get("cost_usd"),
            ))
    return runs


def measure_run(arm: ArmRun, sources_root: Path) -> None:
    """Fill in `arm`'s measured fields from its `report.json` and `merged.md`.

    Uses `reconcile.reconcile` exactly as `measure_merges.py` does -- this is
    not a second instrument. `silent_loss` is the one figure that instrument
    does not compute, because the corpus it was built for had no declarations
    to check `absent` against; this run's report does.
    """
    report_path = arm.run_dir / "report.json"
    merged_path = arm.run_dir / "merged.md"
    if not report_path.is_file() or not merged_path.is_file():
        arm.note = "no report.json/merged.md -- merge step did not complete"
        return

    report = json.loads(report_path.read_text(encoding="utf-8"))
    doc_map = report.get("documents", {})
    documents = {}
    for canonical, original in doc_map.items():
        if canonical == "merged.md":
            continue
        source_path = sources_root / arm.pair / original
        if not source_path.is_file():
            source_path = handwritten_by_origin().get(original, source_path)
        if not source_path.is_file():
            arm.note = f"source {source_path} not found"
            return
        documents[canonical] = source_path.read_text(encoding="utf-8")
    merged_text = merged_path.read_text(encoding="utf-8")

    result = reconcile.reconcile(documents, merged_text)

    declared_segments = {item["segment"] for item in report.get("declarations", [])}
    absent_ids = []
    for coverage in result.coverages:
        for item in coverage.located:
            if item.verdict == reconcile.ABSENT:
                absent_ids.append(item.segment.id)
    silent_ids = [sid for sid in absent_ids if sid not in declared_segments]

    arm.segments = result.total
    arm.present = result.present
    arm.near = result.reworded
    arm.absent = result.absent
    arm.silent_loss = len(silent_ids)
    arm.dup = len(result.duplicates)
    arm.stapled = result.order.stapled
    arm.measured = True


@dataclass
class ModelRow:
    model: str
    full_models: set[str] = field(default_factory=set)
    runs_expected: int = 0
    runs_measured: int = 0
    runs_failed: list[str] = field(default_factory=list)
    segments: int = 0
    present: int = 0
    near: int = 0
    silent_loss: int = 0
    dup: int = 0
    stapled_runs: list[str] = field(default_factory=list)
    costs: list[float] = field(default_factory=list)
    cost_missing: int = 0
    speeds: list[float] = field(default_factory=list)

    @property
    def coverage(self) -> float:
        return (self.present + self.near) / self.segments if self.segments else 0.0

    @property
    def disqualifiers(self) -> list[str]:
        out = []
        if self.stapled_runs:
            out.append(f"staples ({len(self.stapled_runs)} run(s): {', '.join(self.stapled_runs)})")
        if self.dup:
            out.append(f"duplicates content ({self.dup} instance(s) across its runs)")
        if self.silent_loss:
            out.append(f"loses content silently ({self.silent_loss} segment(s) absent with no "
                        f"disposition declared)")
        return out

    @property
    def mean_cost(self) -> float | None:
        if not self.costs or self.cost_missing:
            return None
        return sum(self.costs) / len(self.costs)

    @property
    def mean_speed(self) -> float | None:
        if not self.speeds:
            return None
        return sum(self.speeds) / len(self.speeds)


def aggregate(runs: list[ArmRun]) -> list[ModelRow]:
    by_model: dict[str, ModelRow] = {}
    for arm in runs:
        row = by_model.setdefault(arm.model, ModelRow(model=arm.model))
        row.full_models.add(arm.full_model)
        row.runs_expected += 1
        if arm.cost_usd is None:
            row.cost_missing += 1
        else:
            row.costs.append(arm.cost_usd)
        if arm.wall_seconds is not None:
            row.speeds.append(arm.wall_seconds)
        if not arm.measured:
            row.runs_failed.append(f"{arm.pair}-{arm.fidelity} ({arm.note})")
            continue
        row.runs_measured += 1
        row.segments += arm.segments
        row.present += arm.present
        row.near += arm.near
        row.silent_loss += arm.silent_loss
        row.dup += arm.dup
        if arm.stapled:
            row.stapled_runs.append(f"{arm.pair}-{arm.fidelity}")
    return list(by_model.values())


def rank(rows: list[ModelRow]) -> tuple[list[ModelRow], list[ModelRow]]:
    """Disqualify, then order survivors quality -> cost -> speed. No composite."""
    disqualified = [r for r in rows if r.disqualifiers]
    survivors = [r for r in rows if not r.disqualifiers]
    # Missing cost/speed sort last within their tier rather than raising or
    # being treated as free/instant -- `float("inf")` says "unknown, not zero".
    survivors.sort(key=lambda r: (
        -r.coverage,
        r.mean_cost if r.mean_cost is not None else float("inf"),
        r.mean_speed if r.mean_speed is not None else float("inf"),
    ))
    return survivors, disqualified


def print_table(survivors: list[ModelRow], disqualified: list[ModelRow]) -> None:
    print("=" * 100)
    print("  QUALITY-FIRST LEAGUE TABLE -- lexicographic: coverage, then cost, then speed.")
    print("  No composite score. Disqualifiers are stated, not scored.")
    print("=" * 100)

    if disqualified:
        print("\n  DISQUALIFIED (unusable regardless of cost or speed):\n")
        for row in sorted(disqualified, key=lambda r: r.model):
            cov = f"{row.present + row.near}/{row.segments} ({100 * row.coverage:.1f}%)"
            cost = f"${row.mean_cost:.4f}" if row.mean_cost is not None else "n/a"
            speed = f"{row.mean_speed:.1f}s" if row.mean_speed is not None else "n/a"
            print(f"    {row.model}  ({', '.join(sorted(row.full_models))})  "
                  f"-- for the record: coverage {cov}, {cost}/merge, {speed}/merge")
            for reason in row.disqualifiers:
                print(f"      - {reason}")
            if row.runs_failed:
                print(f"      - {len(row.runs_failed)} run(s) produced no report: "
                      f"{'; '.join(row.runs_failed)}")

    print("\n  SURVIVORS, ranked coverage desc, then cost asc, then speed asc:\n")
    header = (f"  {'model':26} {'silent-loss':>11} {'coverage':>18} {'dup':>4} "
              f"{'staple?':>8} {'$/merge':>10} {'s/merge':>10}  runs")
    print(header)
    print("  " + "-" * (len(header) - 2))
    for row in survivors:
        cov = f"{row.present + row.near:3d}/{row.segments:<3d} ({100 * row.coverage:5.1f}%)"
        cost = f"${row.mean_cost:.4f}" if row.mean_cost is not None else "n/a"
        speed = f"{row.mean_speed:.1f}s" if row.mean_speed is not None else "n/a"
        runs_note = f"{row.runs_measured}/{row.runs_expected} measured"
        if row.cost_missing:
            runs_note += f", cost unrecorded on {row.cost_missing}"
        if row.runs_failed:
            runs_note += f", {len(row.runs_failed)} failed"
        print(f"  {row.model:26} {row.silent_loss:11d} {cov:>18} {row.dup:4d} "
              f"{'no':>8} {cost:>10} {speed:>10}  {runs_note}")

    print("\n  silent_loss = segments the reconciler could not find in the merge AND that "
          "run's own")
    print("  `declarations` list (report.json) names no disposition for. 0 does not mean "
          "\"nothing")
    print("  was dropped\" -- it means every drop was declared, which the reconciler's own "
          "findings")
    print("  step already checked for truthfulness.")


def to_json(survivors: list[ModelRow], disqualified: list[ModelRow]) -> dict:
    def row_dict(row: ModelRow) -> dict:
        return {
            "model": row.model,
            "full_models": sorted(row.full_models),
            "runs_expected": row.runs_expected,
            "runs_measured": row.runs_measured,
            "runs_failed": row.runs_failed,
            "segments": row.segments,
            "present": row.present,
            "near": row.near,
            "coverage": round(row.coverage, 4),
            "silent_loss": row.silent_loss,
            "dup": row.dup,
            "stapled_runs": row.stapled_runs,
            "mean_cost_usd": row.mean_cost,
            "cost_missing_runs": row.cost_missing,
            "mean_wall_seconds": row.mean_speed,
            "disqualifiers": row.disqualifiers,
        }
    return {
        "survivors_ranked": [row_dict(r) for r in survivors],
        "disqualified": [row_dict(r) for r in sorted(disqualified, key=lambda r: r.model)],
    }


def league(run_dirs=None, sources_root: Path = DEFAULT_SOURCES_ROOT):
    """(survivors, disqualified) over `run_dirs`, the default the two published runs."""
    runs = load_runs(list(run_dirs or DEFAULT_RUN_DIRS))
    for arm in runs:
        measure_run(arm, sources_root)
    return rank(aggregate(runs)) if runs else ([], [])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--run-dir", type=Path, action="append", dest="run_dirs",
                         help="a directory holding results.json and one subdir per arm "
                              "(repeatable; default both recorded runs)")
    parser.add_argument("--sources-root", type=Path, default=DEFAULT_SOURCES_ROOT,
                         help="where <pair>/<original filename> is read from")
    parser.add_argument("--json", type=Path, help="also write the table as JSON here")
    parser.add_argument("--check", action="store_true",
                         help="compare with tests/league_table.json; exit 1 if it differs")
    args = parser.parse_args(argv)

    survivors, disqualified = league(args.run_dirs, args.sources_root)
    if not survivors and not disqualified:
        print("no runs found", file=sys.stderr)
        return 2
    if args.check:
        fresh = to_json(survivors, disqualified)
        same = fresh == json.loads(COMMITTED.read_text(encoding="utf-8"))
        print(f"league_table: {'clean' if same else 'DIFFERS'} -- "
              f"{COMMITTED.relative_to(ROOT)} against the published runs")
        return 0 if same else 1
    print_table(survivors, disqualified)

    if args.json:
        args.json.write_text(json.dumps(to_json(survivors, disqualified), indent=2) + "\n",
                              encoding="utf-8")
        print(f"\n  Wrote {args.json}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
