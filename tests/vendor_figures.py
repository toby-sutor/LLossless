#!/usr/bin/env python3
"""The catalogue's GPT-6 and Opus 5.5 rows, formed from the committed 2026-09-25 vendor run.

`gpt-6-sol`, `gpt-6-luna` and `claude-opus-5-5` were measured here; the
release benchmark superseded all three in the catalogue (2026-09-28),
which now names `derived_by tests/lineup_figures.py` for them. `ROWS`
below still forms all three rows, this run's own scored cells for them
are unchanged, and the history that reads them
(`tests/benchmark_matrix.py`, `tests/test_figure_rules.py`) still needs
them. Layer 2's catalogue check looks only at the rows `catalogue.json`
still attributes to this script by name (`measured.derived_by`), which
today is none of them. Every figure is still formed here from
`arms/2026-09-25/vendor/`, by the scoring `tests/rank_matrix.py` applies
to the 2026-09-18 hosted rows, and nothing here calls a model.
`REGISTRATION.md` in that directory says what was measured and what the
figures may be used for; later rulings say what happened, what
superseded these rows, and how the check still finds them.

Two layers, as `tests/subscription_figures.py` has:

  1. The scored cells from the raw runs. `rank_matrix.cell_figures` over each
     cell's `merged.md` and `report.json`, plus the runner's exit code, wall
     time and the dollars the spend ledger charged for the cell, and the
     priced cost and seconds `figure_rules` reads off the report, must give
     back `scored.json` field for field. The raw runs are published in that
     directory (the operator's ruling of 2026-09-25, applied to
     these API runs as well).
  2. The rows from the scored cells, by `figure_rules`: one
     figure per (model, pair), draw 1 of each; silent loss and deviations
     over the pairs every counted model completed, with each model's own
     full row and the pairs it did not complete beside them; dollars per
     merge as the exact mean of each cell's priced cost of its answered
     calls (the report's own ledger at `pricing.py`'s rates), rounded once,
     with the runner's billed ledger as the separate billed upper bound;
     seconds per merge from the report's own `duration_seconds`, rounded
     once. A probe of `tests/fixtures/dedup`, a cell the gate refused, an
     exit 2 and a cell that failed an assertion are excluded and named.

    python3 tests/vendor_figures.py            print the rows it forms
    python3 tests/vendor_figures.py --check    compare with catalogue.json;
                                               exit 1 on any difference
    python3 tests/vendor_figures.py --score    write scored.json from the
                                               raw runs
    python3 tests/vendor_figures.py --write    write the formed rows' derived
                                               fields into catalogue.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

socket_guard.install()

import figure_rules  # noqa: E402
import rank_matrix  # noqa: E402
from llossless.web import catalogue  # noqa: E402

EVIDENCE = ROOT / "arms" / "2026-09-25" / "vendor"
SCORED = EVIDENCE / "scored.json"
CELLS = EVIDENCE / "cells"
PAIRS = sorted(p.name for p in (ROOT / "tests" / "pairs").iterdir()
               if (p / "ideal.md").is_file())

SCRIPT = "tests/vendor_figures.py"
# The model rows this run forms, in catalogue order. The retired Opus row's refused cells
# are scored too, as exclusions, and form no row. Kept in
# full for the history: the catalogue comparison in row_problems()
# checks only what catalogue.json still attributes to this script.
ROWS = ("claude-opus-5-5", "gpt-6-sol", "gpt-6-luna")
ARMS = ("gpt-6-sol", "gpt-6-luna", "claude-opus-5", "claude-opus-5-5")
CARRIED = ("arm", "model", "pair", "draw", "fidelity", "exit_code", "wall_seconds",
           "started_at", "claimcheck_commit", "ledger_usd")
DERIVED = ("usd_per_merge", "billed_upper_bound_usd_per_merge", "seconds_per_merge",
           "silent_loss", "silent_loss_per_pair", "deviations", "deviations_per_pair",
           "pairs", "pairs_completed", "silent_loss_all_completed",
           "deviations_all_completed", "pairs_not_completed", "model_confirmed_declarations",
           "absent_behind_rejected_declarations", "spread_draws", "fidelity", "measured_on",
           "claimcheck_commit")


# A figure a row's notes state in prose: a prose claim is checked like a
# field, and rewritten by `--write`, never typed.
SHARE = re.compile(r"(\d+) of its (\d+) deviations are on one pair, rate_limits")


def note_claims(scored: list[dict], formed: dict[str, dict]) -> dict[str, list]:
    """Per row: (pattern, the figures it must state) for every prose claim checked."""
    out = {}
    for arm, row in formed.items():
        on = [c for c in scored if c["arm"] == arm and not c["excluded"]
              and c["pair"] == "rate_limits" and c["draw"] == figure_rules.HEADLINE_DRAW]
        if len(on) == 1 and arm in ("claude-opus-5-5", "gpt-6-luna"):
            out[arm] = [(SHARE, (figure_rules.deviations(on[0]), row["deviations"]))]
    return out


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def results(arm: str) -> list[dict]:
    path = EVIDENCE / f"results_{arm}.json"
    return load(path) if path.is_file() else []


def label(row: dict) -> str:
    return row.get("label") or f"{row['pair']}-high-{row['arm']}-d{row['draw']}"


def exclusion(row: dict) -> str:
    """Why a runner row is left out of the rows, or "" when it is counted."""
    if row.get("pair") not in PAIRS:
        return "probe"
    if row.get("gated"):
        return "gated"
    if row.get("interrupted"):
        # A machine crash mid-cell (2026-09-25): its charged calls count
        # against the cap, never against the figures.
        return "interrupted"
    if row.get("problems"):
        return "assertion"
    if row.get("exit_code") == 2:
        return "exit_2"
    if not row.get("report"):
        return "no_report"
    return ""


def score() -> list[dict]:
    """Layer 1's product: one scored record per runner row, from the raw runs."""
    out = []
    for arm in ARMS:
        for row in results(arm):
            record = {key: row.get(key) for key in CARRIED}
            record["arm"] = arm
            record["excluded"] = exclusion(row)
            if not record["excluded"]:
                where = CELLS / label(row)
                report = load(where / "report.json")
                record.update(rank_matrix.cell_figures(
                    row["pair"], (where / "merged.md").read_text(encoding="utf-8"), report))
                record["usd"] = figure_rules.exact_usd(report)
                record["seconds"] = figure_rules.answer_seconds(report)
            out.append(record)
    return out


def score_problems() -> tuple[list[str], str]:
    """Layer 1: the raw runs, scored now, against the committed scored cells."""
    if not CELLS.is_dir():
        return [], (f"UNMEASURED: the raw runs are not in this checkout "
                    f"({CELLS.relative_to(ROOT)})")
    now, then = score(), load(SCORED)
    if len(now) != len(then):
        return [f"the runner rows score to {len(now)} cells, and scored.json holds "
                f"{len(then)}"], ""
    moved = [f"{a['arm']}/{a['pair']}/d{a['draw']}" for a, b in zip(now, then) if a != b]
    return ([f"the raw runs, scored with today's rank_matrix.cell_figures, no longer give "
             f"scored.json ({', '.join(moved)})"] if moved else []), \
        f"{len(now)} scored cells re-derived from {CELLS.relative_to(ROOT)}"


def one(values: set, what: str):
    if len(values) != 1:
        raise SystemExit(f"vendor_figures: expected one {what}, found "
                         f"{sorted(map(str, values))}")
    return next(iter(values))


def rows(scored: list[dict]) -> dict[str, dict]:
    """Layer 2: each model's derived figures, by `figure_rules`."""
    out = {}
    for arm, group in figure_rules.groups(scored, ROWS, "arm", PAIRS,
                                          registered_k1=False).items():
        cells, every = group["cells"], group["all_cells"]
        out[arm] = {
            "usd_per_merge": figure_rules.per_merge([c["usd"] for c in cells],
                                                    figure_rules.USD_PLACES),
            "billed_upper_bound_usd_per_merge": figure_rules.per_merge(
                [c["ledger_usd"] for c in cells], figure_rules.USD_PLACES),
            "seconds_per_merge": figure_rules.per_merge([c["seconds"] for c in cells],
                                                        figure_rules.SECONDS_PLACES),
            **figure_rules.quality(group),
            "spread_draws": group["spread_draws"],
            "fidelity": one({c["fidelity"] for c in every}, f"fidelity for {arm}"),
            "measured_on": min(c["started_at"] for c in every)[:10],
            "claimcheck_commit": figure_rules.commit_of(every, f"tool commit for {arm}"),
        }
    return out


def excluded(scored: list[dict]) -> list[str]:
    return [f"{c['arm']}/{c['pair']}/d{c['draw']} ({c['excluded']})"
            for c in scored if c["excluded"]]


def _superseded(measured) -> bool:
    """True once catalogue.json attributes a measured block to a different
    script: `derived_by` is set and does not name this one."""
    return isinstance(measured, dict) and SCRIPT not in str(measured.get("derived_by"))


def row_problems(models: list[dict]) -> list[str]:
    """Layer 2: the published rows against the rows formed from the cells.

    Checked only for the ids `catalogue.json`'s own `measured.derived_by`
    still names this script; an id it now names to another script (the
    release benchmark superseded all three of these) is left alone, not
    compared. An id that still names this script but that `ROWS` does not
    form is reported, not silently skipped.
    """
    formed = rows(load(SCORED))
    published = {entry.get("id"): entry for entry in models}
    out = []
    owned = set()
    for arm in ROWS:
        entry = published.get(arm)
        if entry is None:
            out.append(f"catalogue.json has no row for {arm}")
            continue
        measured = entry.get("measured")
        if _superseded(measured):
            continue
        owned.add(arm)
        if arm not in formed:
            if measured is not None:
                out.append(f"{arm} carries figures this run did not measure")
            continue
        if not isinstance(measured, dict):
            out.append(f"{arm} has no measured block; the run gives "
                       f"{json.dumps(formed[arm])[:200]}")
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
    for arm, claims in note_claims(load(SCORED), formed).items():
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
        print(f"no vendor run at {EVIDENCE.relative_to(ROOT)}", file=sys.stderr)
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
        for arm, claims in note_claims(load(SCORED), formed).items():
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
    if said.startswith("UNMEASURED"):
        print(said)
    print(f"vendor_figures: {'clean' if not found else f'{len(found)} difference(s)'}"
          f" -- {said if not said.startswith('UNMEASURED') else 'layer 1 not run'}; "
          f"{len(ROWS)} models' rows re-derived from {SCORED.relative_to(ROOT)}")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
