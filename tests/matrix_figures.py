#!/usr/bin/env python3
"""The catalogue's 2026-09-18 API rows, formed from the committed 2026-09-18 matrix.

`src/llossless/web/catalogue.json` publishes measured figures for
`claude-opus-5` and `gpt-5.6-terra` from the matrix run of 2026-09-18, the
nine pairs in `tests/pairs/` at `high`. The run used to live
outside the repository and `tests/rank_matrix.py` read it there; it is
published now, at `arms/2026-09-18/matrix/`, and this program is
those rows' `derived_by`. Nothing here calls a model.

`claude-sonnet-5` and `claude-haiku-4-5` were also measured here; the release
benchmark superseded both in the catalogue (2026-09-28), which now names
`derived_by tests/lineup_figures.py` for them. `ROWS` below still forms both
rows -- this run's own scored cells for them are unchanged, and the history
that reads them (`tests/benchmark_matrix.py`, `tests/test_figure_rules.py`)
still needs them. Layer 2's catalogue check looks only at the rows
`catalogue.json` still attributes to this script by name (`measured.derived_by`);
a row it now names to another script is left alone, and a row that still
names this script but that `ROWS` does not form is reported, not silently
skipped.

Two layers, as `tests/vendor_figures.py` has:

  1. The scored cells from the raw runs. `rank_matrix.cell_figures` over each
     cell's `merged.md` and `report.json`, plus the runner's exit code, wall
     time and dollars, and the priced cost and seconds `figure_rules` reads
     off the report, must give back `scored.json` field for field.
  2. The rows from the scored cells, by `figure_rules`. The
     runner files hold more than one row for some cells (a first pass that
     stopped at exit 2 in under a second, then the re-run); as in
     `rank_matrix.py` the last row for an arm and pair is the cell, and the
     earlier ones are excluded as `superseded`. A cell with exit 2, or with no
     `merged.md` or `report.json`, is excluded and named. One figure per
     (model, pair); silent loss and deviations over the pairs every counted
     model completed, each model's full row beside them. Dollars per merge
     are the exact mean of each cell's priced cost (the report's own ledger at
     `pricing.py`'s rates, which must round to the runner's `cost_usd`),
     rounded once; the runner's `max(cost_usd, cost_usd_billed)` is the
     billed upper bound beside it. Seconds per merge are the reports' own
     `duration_seconds`, rounded once.

    python3 tests/matrix_figures.py            print the rows it forms
    python3 tests/matrix_figures.py --check    compare with catalogue.json;
                                               exit 1 on any difference
    python3 tests/matrix_figures.py --score    write scored.json from the
                                               raw runs
    python3 tests/matrix_figures.py --write    write the formed rows' derived
                                               fields into catalogue.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import namedtuple
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

socket_guard.install()

import figure_rules  # noqa: E402
import rank_matrix  # noqa: E402
from llossless.web import catalogue  # noqa: E402

EVIDENCE = ROOT / "arms" / "2026-09-18" / "matrix"
SCORED = EVIDENCE / "scored.json"
RESULTS = ("results_anthropic.json", "results_openai.json")
SCRIPT = "tests/matrix_figures.py"
# Every id this run ever measured, kept in full for the history: the
# catalogue comparison in row_problems() checks only the ones catalogue.json
# still attributes to this script.
ROWS = ("claude-opus-5", "claude-sonnet-5", "claude-haiku-4-5", "gpt-5.6-terra")

# The check assumes rows are superseded in place: a row missing from the card is
# reported, since a supersede never actually deletes a row, only re-attributes its
# `derived_by`. Removal by ruling is a third case, so it gets its own named,
# documented exception here rather than weakening the "missing row" check for
# every row this script ever formed.
RemovedFromCard = namedtuple("RemovedFromCard", ("decision", "reason"))
REMOVED_FROM_CARD = {
    "claude-opus-5": RemovedFromCard(
        decision=708,
        reason="retired 2026-09-25 and no longer credible on the card, per "
               "the operator's 2026-09-28 ruling: \"Opus 5 is NOT Opus 5.5. And we "
               "should remove Opus 5 entries if they are no longer credible.\" Removed "
               "from catalogue.json entirely, not superseded in place; this script "
               "still forms the row for the history, and its own figures are unchanged."),
}
CARRIED = ("arm", "model", "pair", "fidelity", "exit_code", "wall_seconds")
DERIVED = ("usd_per_merge", "billed_upper_bound_usd_per_merge", "seconds_per_merge",
           "silent_loss", "silent_loss_per_pair", "deviations", "deviations_per_pair",
           "pairs", "pairs_completed", "silent_loss_all_completed",
           "deviations_all_completed", "pairs_not_completed", "model_confirmed_declarations",
           "absent_behind_rejected_declarations", "spread_draws", "fidelity", "measured_on",
           "claimcheck_commit")
PAIRS = sorted(p.name for p in (ROOT / "tests" / "pairs").iterdir()
               if (p / "ideal.md").is_file())


# A figure a row's notes state in prose, checked like a field and
# rewritten by `--write`.
SILENT = re.compile(r"silent loss of (\d+) across (\d+) pairs")


def note_claims(formed: dict[str, dict]) -> dict[str, list]:
    """Per row: (pattern, the figures it must state) for every prose claim checked."""
    row = formed.get("claude-haiku-4-5")
    return {"claude-haiku-4-5": [(SILENT, (row["silent_loss"], row["pairs"]))]} if row else {}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def runner_rows() -> list[dict]:
    out = []
    for name in RESULTS:
        path = EVIDENCE / name
        if path.is_file():
            out.extend(load(path))
    return out


def score() -> list[dict]:
    """Layer 1's product: one record per runner row, in runner order."""
    rows = runner_rows()
    last = {(r["arm"], r["pair"]): i for i, r in enumerate(rows)}
    out = []
    for i, row in enumerate(rows):
        record = {key: row.get(key) for key in CARRIED}
        record["usd"] = max(row.get("cost_usd") or 0, row.get("cost_usd_billed") or 0)
        where = EVIDENCE / f"{row['pair']}-high-{row['arm']}"
        if last[(row["arm"], row["pair"])] != i:
            record["excluded"] = "superseded"
        elif not (where / "merged.md").is_file() or not (where / "report.json").is_file():
            record["excluded"] = "no_report"
        elif row.get("exit_code") == 2:
            record["excluded"] = "exit_2"
        else:
            record["excluded"] = ""
        if not record["excluded"]:
            report = load(where / "report.json")
            provenance = report.get("provenance") or {}
            # Whole: a `-dirty` stamp cut to twelve characters reads as the pin.
            record["claimcheck_commit"] = str(provenance.get("claimcheck_commit"))
            record["generated_on"] = str(provenance.get("generated_at"))[:10]
            record.update(rank_matrix.cell_figures(
                row["pair"], (where / "merged.md").read_text(encoding="utf-8"), report))
            record["usd_priced"] = figure_rules.exact_usd(report, recorded=row.get("cost_usd"))
            record["seconds"] = figure_rules.answer_seconds(report)
        out.append(record)
    return out


def score_problems() -> tuple[list[str], str]:
    """Layer 1: the raw runs, scored now, against the committed scored cells."""
    now, then = score(), load(SCORED)
    if len(now) != len(then):
        return [f"the runner rows score to {len(now)} records, and scored.json holds "
                f"{len(then)}"], ""
    moved = [f"{a['arm']}/{a['pair']}" for a, b in zip(now, then) if a != b]
    return ([f"the raw runs, scored with today's rank_matrix.cell_figures, no longer give "
             f"scored.json ({', '.join(moved)})"] if moved else []), \
        f"{len(now)} records re-derived from {EVIDENCE.relative_to(ROOT)}"


def one(values: set, what: str):
    if len(values) != 1:
        raise SystemExit(f"matrix_figures: expected one {what}, found "
                         f"{sorted(map(str, values))}")
    return next(iter(values))


def rows(scored: list[dict]) -> dict[str, dict]:
    """Layer 2: each model's figures from its counted cells, by `figure_rules`."""
    out = {}
    for arm, group in figure_rules.groups(scored, ROWS, "arm", PAIRS,
                                          registered_k1=True).items():
        cells, every = group["cells"], group["all_cells"]
        out[arm] = {
            "usd_per_merge": figure_rules.per_merge([c["usd_priced"] for c in cells],
                                                    figure_rules.USD_PLACES),
            "billed_upper_bound_usd_per_merge": figure_rules.per_merge(
                [c["usd"] for c in cells], figure_rules.USD_PLACES),
            "seconds_per_merge": figure_rules.per_merge([c["seconds"] for c in cells],
                                                        figure_rules.SECONDS_PLACES),
            **figure_rules.quality(group),
            "spread_draws": group["spread_draws"],
            "fidelity": one({c["fidelity"] for c in every}, f"fidelity for {arm}"),
            "measured_on": min(c["generated_on"] for c in every),
            "claimcheck_commit": figure_rules.commit_of(every, f"tool commit for {arm}"),
        }
    return out


def excluded(scored: list[dict]) -> list[str]:
    return [f"{c['arm']}/{c['pair']} ({c['excluded']})" for c in scored
            if c["excluded"] and c["excluded"] != "superseded"]


def _superseded(measured) -> bool:
    """True once catalogue.json attributes a measured block to a different
    script: `derived_by` is set and does not name this one."""
    return isinstance(measured, dict) and SCRIPT not in str(measured.get("derived_by"))


def row_problems(models: list[dict]) -> list[str]:
    """Layer 2: the published rows against the rows formed from the cells.

    Checked only for the ids `catalogue.json`'s own `measured.derived_by`
    still names this script; an id it now names to another script (the
    release benchmark superseded two of these) is left alone, not
    compared. An id that still names this script but that `ROWS` does not
    form is reported, not silently skipped. An id in `REMOVED_FROM_CARD` is
    also left alone when missing entirely: it was taken off the card by
    ruling, not superseded, so "no row" is the expected, documented state
    rather than a regression.
    """
    formed = rows(load(SCORED))
    published = {entry.get("id"): entry for entry in models}
    out = []
    owned = set()
    for arm in ROWS:
        entry = published.get(arm)
        if entry is None:
            if arm in REMOVED_FROM_CARD:
                continue
            out.append(f"catalogue.json has no row for {arm}")
            continue
        measured = entry.get("measured")
        if _superseded(measured):
            continue
        owned.add(arm)
        if not isinstance(measured, dict):
            out.append(f"{arm} has no measured block; the run gives "
                       f"{json.dumps(formed.get(arm))[:200]}")
            continue
        if measured.get("run") != "2026-09-18-matrix":
            out.append(f"{arm}.measured.run is {measured.get('run')!r}, not this run")
            continue
        for key in DERIVED:
            if measured.get(key, "absent") != formed[arm][key]:
                out.append(f"{arm}.measured.{key}: catalogue.json says "
                           f"{json.dumps(measured.get(key, 'absent'))}, the cells give "
                           f"{json.dumps(formed[arm][key])}")
    for entry in models:
        arm = entry.get("id")
        if arm in ROWS:
            continue
        measured = entry.get("measured")
        if isinstance(measured, dict) and SCRIPT in str(measured.get("derived_by")):
            out.append(f"catalogue.json attributes {arm} to {SCRIPT}, but it is not one "
                       f"of the rows this script forms")
    for arm, claims in note_claims(formed).items():
        if arm not in owned:
            continue
        notes = str((published.get(arm) or {}).get("notes", ""))
        for pattern, values in claims:
            out += [f"{arm}.notes: {line}" for line in figure_rules.stated(notes, pattern, values)[0]]
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true",
                      help="compare with catalogue.json and exit 1 on any difference")
    mode.add_argument("--score", action="store_true",
                      help="write scored.json from the raw runs")
    mode.add_argument("--write", action="store_true",
                      help="write the formed rows' derived fields into catalogue.json")
    args = parser.parse_args(argv)
    if not EVIDENCE.is_dir():
        print(f"no matrix run at {EVIDENCE.relative_to(ROOT)}", file=sys.stderr)
        return 2
    if args.score:
        SCORED.write_text(json.dumps(score(), indent=1) + "\n", encoding="utf-8")
        print(f"wrote {SCORED.relative_to(ROOT)}")
        return 0
    if args.write:
        data = figure_rules.raw_catalogue()
        formed = rows(load(SCORED))
        edits = [(["models", figure_rules.entry_index(data, "models", "id", arm), "measured"],
                  key, figures[key])
                 for arm, figures in formed.items() for key in DERIVED]
        for arm, claims in note_claims(formed).items():
            index = figure_rules.entry_index(data, "models", "id", arm)
            notes = str(data["models"][index].get("notes", ""))
            for pattern, values in claims:
                notes = figure_rules.stated(notes, pattern, values)[1]
            edits.append((["models", index], "notes", notes))
        changed = figure_rules.write_catalogue(catalogue.DEFAULT_PATH, edits)
        print(f"{'wrote' if changed else 'unchanged:'} {catalogue.DEFAULT_PATH.relative_to(ROOT)}")
        return 0
    if not args.check:
        print(json.dumps(rows(load(SCORED)), indent=2))
        print(f"excluded: {', '.join(excluded(load(SCORED))) or 'none'}")
        return 0
    found, said = score_problems()
    found += row_problems(catalogue.load()["models"])
    for line in found:
        print(f"  DIFFERS  {line}")
    print(f"matrix_figures: {'clean' if not found else f'{len(found)} difference(s)'}"
          f" -- {said}; {len(ROWS)} models' rows re-derived from "
          f"{SCORED.relative_to(ROOT)}")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
