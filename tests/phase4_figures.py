#!/usr/bin/env python3
"""The catalogue's two Qwen rows, formed from the committed 2026-09-16 Phase 4 run.

`src/llossless/web/catalogue.json` publishes measured figures for `qwen3-8b`
and `qwen3.8-27b-fp8` from the self-hosted run of 2026-09-16: `toby-test-2`,
`-4` and `-5` at `low` and `high` on a serverless
vLLM endpoint. The run is published at `arms/2026-09-16/phase4/`, and this
program is those rows' `derived_by`. Before it the
rows said they were derived by hand. Nothing here calls a model.

The pairs are documents from `tests/handwritten/`, tracked under
the names they have now: `toby-test-2` is `tests/handwritten/chickens/`,
`-4` is `christianity/`, `-5` is `curry/` (`tests/rank_arms.py`'s `PAIRS`;
each `meta.json` names the original files, which are byte-identical).
Each merge is scored against that pair's `reference.md` by
`rank_arms.cell_figures`: it does not forgive
a confirmed declaration or the title, as `rank_matrix.cell_figures` does for
the nine pairs. Under that other scoring these rows' deviations would read 12
(8B) and 28 (27B), not 15 and 35; the rows were made with this one.

Two layers, as `tests/vendor_figures.py` has:

  1. The scored cells from the raw runs must give back `scored.json`.
  2. The rows from the scored cells, at `high` only: a cell with exit 2 or
     with no report is excluded and named (`toby-test-5` on the 8B, whose
     reverse verify stream ended without a finish_reason: exit 2, 1204.6 s).
     Seconds are the mean wall time over the counted cells, to one decimal.
     No dollar figure: the endpoint billed by the minute, not by the merge.

    python3 tests/phase4_figures.py            print the rows it forms
    python3 tests/phase4_figures.py --check    compare with catalogue.json;
                                               exit 1 on any difference
    python3 tests/phase4_figures.py --score    write scored.json from the
                                               raw runs
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

socket_guard.install()

import rank_arms  # noqa: E402
from llossless.web import catalogue  # noqa: E402

EVIDENCE = ROOT / "arms" / "2026-09-16" / "phase4"
SCORED = EVIDENCE / "scored.json"
RESULTS = EVIDENCE / "results.json"
# catalogue id -> the model id the run sent
ROWS = {"qwen3-8b": "qwen/qwen3-8b", "qwen3.8-27b-fp8": "Qwen/Qwen3.8-27B-FP8"}
CARRIED = ("run_dir", "model", "pair", "fidelity", "exit_code", "wall_seconds")
DERIVED = ("usd_per_merge", "seconds_per_merge", "silent_loss", "silent_loss_per_pair",
           "deviations", "deviations_per_pair", "pairs", "fidelity", "measured_on",
           "claimcheck_commit")


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def score() -> list[dict]:
    """Layer 1's product: one record per runner row, in runner order."""
    out = []
    for row in load(RESULTS):
        record = {key: row.get(key) for key in CARRIED}
        where = EVIDENCE / row["run_dir"]
        if not (where / "merged.md").is_file() or not (where / "report.json").is_file():
            record["excluded"] = "no_report"
        elif row.get("exit_code") in (2, None):
            record["excluded"] = "exit_2"
        else:
            record["excluded"] = ""
        if not record["excluded"]:
            report = load(where / "report.json")
            provenance = report.get("provenance") or {}
            record["claimcheck_commit"] = str(provenance.get("claimcheck_commit"))[:12]
            record["generated_on"] = str(provenance.get("generated_at"))[:10]
            record["handwritten"] = rank_arms.PAIRS[row["pair"]]
            record.update(rank_arms.cell_figures(
                rank_arms.PAIRS[row["pair"]],
                (where / "merged.md").read_text(encoding="utf-8"), report))
        out.append(record)
    return out


def score_problems() -> tuple[list[str], str]:
    now, then = score(), load(SCORED)
    if len(now) != len(then):
        return [f"the runner rows score to {len(now)} records, and scored.json holds "
                f"{len(then)}"], ""
    moved = [a["run_dir"] for a, b in zip(now, then) if a != b]
    return ([f"the raw runs, scored with today's rank_arms.cell_figures, no longer give "
             f"scored.json ({', '.join(moved)})"] if moved else []), \
        f"{len(now)} records re-derived from {EVIDENCE.relative_to(ROOT)}"


def one(values: set, what: str):
    if len(values) != 1:
        raise SystemExit(f"phase4_figures: expected one {what}, found "
                         f"{sorted(map(str, values))}")
    return next(iter(values))


def rows(scored: list[dict]) -> dict[str, dict]:
    """Layer 2: each model's `high` figures from its counted cells."""
    out = {}
    for row_id, model in ROWS.items():
        cells = [c for c in scored if c["model"] == model and c["fidelity"] == "high"
                 and not c["excluded"]]
        if not cells:
            continue
        n = len(cells)
        silent = sum(c["silent"] for c in cells)
        deviations = sum(c["lost"] + c["bloat"] + c["dup"] for c in cells)
        out[row_id] = {
            "usd_per_merge": None,
            "seconds_per_merge": round(sum(c["wall_seconds"] for c in cells) / n, 1),
            "silent_loss": silent,
            "silent_loss_per_pair": round(silent / n, 2),
            "deviations": deviations,
            "deviations_per_pair": round(deviations / n, 2),
            "pairs": n,
            "fidelity": "high",
            "measured_on": min(c["generated_on"] for c in cells),
            "claimcheck_commit": one({c["claimcheck_commit"] for c in cells},
                                     f"tool commit for {row_id}"),
        }
    return out


def excluded(scored: list[dict]) -> list[str]:
    return [f"{c['run_dir']} ({c['excluded']})" for c in scored if c["excluded"]]


def row_problems(models: list[dict]) -> list[str]:
    formed = rows(load(SCORED))
    published = {entry.get("id"): entry for entry in models}
    out = []
    for row_id in ROWS:
        entry = published.get(row_id)
        if entry is None:
            out.append(f"catalogue.json has no row for {row_id}")
            continue
        measured = entry.get("measured")
        if not isinstance(measured, dict):
            out.append(f"{row_id} has no measured block; the run gives "
                       f"{json.dumps(formed.get(row_id))[:200]}")
            continue
        if measured.get("run") != "2026-09-16-phase4":
            out.append(f"{row_id}.measured.run is {measured.get('run')!r}, not this run")
            continue
        for key in DERIVED:
            if measured.get(key, "absent") != formed[row_id][key]:
                out.append(f"{row_id}.measured.{key}: catalogue.json says "
                           f"{json.dumps(measured.get(key, 'absent'))}, the cells give "
                           f"{json.dumps(formed[row_id][key])}")
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true",
                      help="compare with catalogue.json and exit 1 on any difference")
    mode.add_argument("--score", action="store_true",
                      help="write scored.json from the raw runs")
    args = parser.parse_args(argv)
    if not EVIDENCE.is_dir():
        print(f"no Phase 4 run at {EVIDENCE.relative_to(ROOT)}", file=sys.stderr)
        return 2
    if args.score:
        SCORED.write_text(json.dumps(score(), indent=1) + "\n", encoding="utf-8")
        print(f"wrote {SCORED.relative_to(ROOT)}")
        return 0
    if not args.check:
        print(json.dumps(rows(load(SCORED)), indent=2))
        print(f"excluded: {', '.join(excluded(load(SCORED))) or 'none'}")
        return 0
    found, said = score_problems()
    found += row_problems(catalogue.load()["models"])
    for line in found:
        print(f"  DIFFERS  {line}")
    print(f"phase4_figures: {'clean' if not found else f'{len(found)} difference(s)'}"
          f" -- {said}; {len(ROWS)} models' rows re-derived from "
          f"{SCORED.relative_to(ROOT)}")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
