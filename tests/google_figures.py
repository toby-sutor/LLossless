#!/usr/bin/env python3
"""The catalogue's Gemini rows, formed from the committed 2026-09-25 Google free-tier run.

`src/llossless/web/catalogue.json` publishes measured figures for
`gemini-3.8-flash` and `gemini-3.5-flash-lite`. This program is those rows'
`derived_by`: every figure is formed here from `arms/2026-09-25/google/`, by
the scoring `tests/rank_matrix.py` applies to the other hosted rows, and
nothing here calls a model. `REGISTRATION.md` in that directory says what was
measured.

The layers of `tests/vendor_figures.py`, with the free tier's differences:

  1. The scored cells from the raw runs: `rank_matrix.cell_figures` over each
     cell's `merged.md` and `report.json`, plus the runner's exit code, wall
     time, the harness's pacing and backoff waits and the ledger's tokens,
     must give back `scored.json` field for field.
  2. The rows from the scored cells, by `figure_rules`: silent
     loss and deviations with their rates over the pairs every counted model
     completed, each model's full row and the pairs it did not complete
     beside them, and seconds per merge as the mean of each report's own
     `duration_seconds` **less the harness's pacing and backoff waits**,
     which are the free tier's quota and not the model (the registration),
     rounded once. `usd_per_merge` is null: the run was billed $0.00 and a
     zero would read as "measured, and free". The paid-tier equivalent is
     computed here per answered call from the ledger's tokens at
     `pricing.py`'s rates, output taken as `total_tokens - prompt_tokens`
     where larger, and the row's notes must state it, and the raw
     seconds (the same `duration_seconds`, waits included), as this program
     forms them.

    python3 tests/google_figures.py            print the rows it forms
    python3 tests/google_figures.py --check    compare with catalogue.json;
                                               exit 1 on any difference
    python3 tests/google_figures.py --score    write scored.json from the
                                               raw runs
    python3 tests/google_figures.py --write    write the formed rows' derived
                                               fields, and the raw seconds its
                                               notes state, into catalogue.json
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
from llossless import pricing  # noqa: E402
from llossless.web import catalogue  # noqa: E402

EVIDENCE = ROOT / "arms" / "2026-09-25" / "google"
SCORED = EVIDENCE / "scored.json"
CELLS = EVIDENCE / "cells"
LEDGER = EVIDENCE / "ledger_google.json"
PAIRS = sorted(p.name for p in (ROOT / "tests" / "pairs").iterdir()
               if (p / "ideal.md").is_file())

ROWS = ("gemini-3.8-flash", "gemini-3.5-flash-lite")
CARRIED = ("arm", "model", "pair", "draw", "label", "fidelity", "exit_code", "wall_seconds",
           "paced_seconds", "backoff_seconds", "started_at", "claimcheck_commit",
           "ledger_usd", "ledger_calls", "ledger_attempts")
DERIVED = ("usd_per_merge", "seconds_per_merge", "silent_loss", "silent_loss_per_pair",
           "deviations", "deviations_per_pair", "pairs", "pairs_completed",
           "silent_loss_all_completed", "deviations_all_completed", "pairs_not_completed",
           "model_confirmed_declarations", "absent_behind_rejected_declarations",
           "spread_draws", "fidelity", "measured_on", "claimcheck_commit")
# The sentence of a row's notes that states the raw seconds, waits included.
RAW_SECONDS = re.compile(r"the raw wall is [\d.]+ s per merge")


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
    if row.get("billing_stop"):
        return "billing_stop"
    if row.get("quota_day"):
        return "quota_day"
    if row.get("exit_code") == 2:
        # Before `problems`: an exit 2 is a pipeline that stopped, and the
        # runner recorded the roles that never ran behind it as a problem
        # until the registration's 18:56 amendment.
        return "exit_2"
    if row.get("problems"):
        return "assertion"
    if not row.get("report"):
        return "no_report"
    return ""


def call_usd(row: dict) -> float:
    """One answered call at the paid tier's rate, as `pricing.estimate` costs it."""
    return pricing.estimate([{"model": row["served_model"],
                              "prompt_tokens": row["prompt_tokens"],
                              "completion_tokens": row["completion_tokens"],
                              "cached_tokens": row.get("cached_tokens") or 0,
                              **({"total_tokens": row["total_tokens"]}
                                 if row.get("total_tokens") is not None else {})}]).dollars


def paid_usd(cell_label: str, ledger: list[dict]) -> float | None:
    """What the cell's answered calls would cost on the paid tier; None if any is unmeasured."""
    answered = [r for r in ledger if r.get("cell") == cell_label and r.get("status") == 200]
    if not answered or any(r.get("prompt_tokens") is None for r in answered):
        return None
    total = 0.0
    for r in answered:
        dollars = call_usd(r)
        if dollars is None:
            return None
        total += dollars
    return round(total, 6)


def score() -> list[dict]:
    """Layer 1's product: one scored record per runner row, from the raw runs."""
    ledger = load(LEDGER)["rows"] if LEDGER.is_file() else []
    out = []
    for arm in ROWS:
        for row in results(arm):
            record = {key: row.get(key) for key in CARRIED}
            record["arm"] = arm
            record["excluded"] = exclusion(row)
            record["paid_usd"] = paid_usd(label(row), ledger)
            if not record["excluded"]:
                where = CELLS / label(row)
                report = load(where / "report.json")
                record.update(rank_matrix.cell_figures(
                    row["pair"], (where / "merged.md").read_text(encoding="utf-8"), report))
                record["seconds_raw"] = figure_rules.answer_seconds(report)
                record["seconds"] = figure_rules.answer_seconds(
                    report, harness_waits=row["paced_seconds"] + row["backoff_seconds"])
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
        raise SystemExit(f"google_figures: expected one {what}, found "
                         f"{sorted(map(str, values))}")
    return next(iter(values))


def rows(scored: list[dict]) -> dict[str, dict]:
    """Layer 2: each model's derived figures, by `figure_rules`."""
    out = {}
    for arm, group in figure_rules.groups(scored, ROWS, "arm", PAIRS,
                                          registered_k1=False).items():
        cells, every = group["cells"], group["all_cells"]
        paid = [c["paid_usd"] for c in cells]
        out[arm] = {
            "usd_per_merge": None,
            "seconds_per_merge": figure_rules.per_merge([c["seconds"] for c in cells],
                                                        figure_rules.SECONDS_PLACES),
            **figure_rules.quality(group),
            "spread_draws": group["spread_draws"],
            "fidelity": one({c["fidelity"] for c in every}, f"fidelity for {arm}"),
            "measured_on": min(c["started_at"] for c in every)[:10],
            "claimcheck_commit": figure_rules.commit_of(every, f"tool commit for {arm}"),
        }
        raw = figure_rules.per_merge([c["seconds_raw"] for c in cells],
                                     figure_rules.SECONDS_PLACES)
        out[arm]["_notes"] = {
            "wall": f"the raw wall is {raw:.1f} s per merge",
            "paid": (None if None in paid else f"${sum(paid) / len(paid):.4f} per merge"),
            "billed": f"${sum(c['ledger_usd'] or 0.0 for c in cells):.2f}",
        }
    return out


def excluded(scored: list[dict]) -> list[str]:
    return [f"{c['arm']}/{c['pair']}/d{c['draw']} ({c['excluded']})"
            for c in scored if c["excluded"]]


def row_problems(models: list[dict]) -> list[str]:
    """Layer 2: the published rows against the rows formed from the cells."""
    formed = rows(load(SCORED))
    published = {entry.get("id"): entry for entry in models}
    out = []
    for arm in ROWS:
        entry = published.get(arm)
        if arm not in formed:
            if entry is not None and entry.get("measured") is not None:
                out.append(f"{arm} carries figures this run did not measure")
            continue
        if entry is None:
            out.append(f"catalogue.json has no row for {arm}")
            continue
        measured = entry.get("measured")
        if not isinstance(measured, dict):
            out.append(f"{arm} has no measured block")
            continue
        for key in DERIVED:
            if measured.get(key, "absent") != formed[arm][key]:
                out.append(f"{arm}.measured.{key}: catalogue.json says "
                           f"{json.dumps(measured.get(key, 'absent'))}, the cells give "
                           f"{json.dumps(formed[arm][key])}")
        notes = str(entry.get("notes", ""))
        said = formed[arm]["_notes"]
        for what in ("free tier", "not billed", said["wall"], said["billed"] + " billed"):
            if what not in notes:
                out.append(f"{arm}.notes does not say {what!r}")
        if said["paid"] is None:
            if "unmeasured" not in notes:
                out.append(f"{arm}: a call reported no tokens, and notes do not say "
                           f"the paid-tier figure is unmeasured")
        elif said["paid"] not in notes:
            out.append(f"{arm}.notes does not state the paid-tier figure {said['paid']!r}")
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
        print(f"no Google run at {EVIDENCE.relative_to(ROOT)}", file=sys.stderr)
        return 2
    if args.score:
        SCORED.write_text(json.dumps(score(), indent=1) + "\n", encoding="utf-8")
        print(f"wrote {SCORED.relative_to(ROOT)}")
        return 0
    if args.write:
        data = figure_rules.raw_catalogue()
        edits = []
        for arm, figures in rows(load(SCORED)).items():
            index = figure_rules.entry_index(data, "models", "id", arm)
            edits += [(["models", index, "measured"], key, figures[key]) for key in DERIVED]
            notes = str(data["models"][index].get("notes", ""))
            if len(RAW_SECONDS.findall(notes)) != 1:
                raise SystemExit(f"google_figures: {arm}.notes does not state the raw "
                                 f"seconds in one sentence to rewrite")
            edits.append((["models", index], "notes",
                          RAW_SECONDS.sub(figures["_notes"]["wall"], notes)))
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
    formed = rows(load(SCORED))
    print(f"google_figures: {'clean' if not found else f'{len(found)} difference(s)'}"
          f" -- {said if not said.startswith('UNMEASURED') else 'layer 1 not run'}; "
          f"{len(formed)} models' rows re-derived from {SCORED.relative_to(ROOT)}")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
