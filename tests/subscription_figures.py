#!/usr/bin/env python3
"""The catalogue's subscription-route rows, formed from the committed 2026-09-24 run.

`haiku`, `sonnet` and, for a time, `opus` were all checked here, against
this program's re-derivation of `arms/2026-09-24/subscription/`, until the
release benchmark superseded all three in the catalogue (haiku and sonnet
first, opus later, on the operator's ruling that Opus 5 is not Opus 5.5 and
is no longer credible on the card), which now names `derived_by
tests/lineup_figures.py` for all three. `ROUTES` below still forms every
row: this run's own scored cells are unchanged, and the history that reads
them still needs them. The catalogue check looks only at the routes
`catalogue.json` still attributes to this script by name
(`measured.derived_by`), which today is none of them: `opus` stayed checked
here for a while after haiku and sonnet moved on, on purpose, while its own
figures were still Claude Opus 5's from this run; once the alias and the
route's `resolved_model` agreed (`claude-opus-5-5` throughout), its
`measured` block moved to the release benchmark's own figures too
(`opus-5.5-sub` in `arms/2026-09-27/lineup/figures.json`), and its
`alias_now`/`measured_by_effort` history was dropped with it: the two no
longer disagreeing is exactly why `alias_now` is gone (the schema forbids
it equalling `resolved_model`). `NOT_RUN` keeps `claude-fable`, registered
here as not run at the time this run was measured; it is measured now too,
by the lineup run, checked through `lineup_figures.py`, not here. Every
figure this script forms is read from `arms/2026-09-24/subscription/`, by
the scoring `tests/rank_matrix.py` applies to the hosted rows, and nothing
here calls a model. `REGISTRATION.md` in that directory says what was
measured and what the figures may be used for; later rulings say what
superseded haiku and sonnet, how the check found opus among them, and when
opus was superseded too.

Two layers, as `tests/depth_figures.py` has:

  1. The scored cells from the raw runs. `rank_matrix.cell_figures` over each
     cell's `merged.md` and `report.json`, plus the runner's exit code and wall
     time, must give back `scored.json` field for field. **The raw runs are
     published** (`arms/2026-09-24/subscription/<pair>-<fidelity>-<route>/`),
     at the operator's ruling of 2026-09-25; `arms/README.md` says why they
     were withheld until then. Where a checkout does not carry them this layer
     prints `UNMEASURED:` and does not pass or fail, so the guard still holds
     for a partial or pre-ruling copy.
  2. The rows from the scored cells, by `figure_rules`. Per
     route: silent loss and deviations with their rates over the pairs every
     route completed, each route's full row and the pairs it did not
     complete beside them, and seconds per merge as the mean of the reports'
     own `duration_seconds`, rounded once. `usd_per_merge` is null by rule:
     the calls are included in the subscription and not priced per call; this
     run kept no CLI envelopes, so it has no API-equivalent figure either (and
     so no uncached list-price column beside one, B4). A cell that exited 2
     is excluded and named; a cell stopped by a usage limit must have been
     re-run. `merge_effort` is the level the merge was asked for, read off
     every counted run's own `decoding.effort` in `results.json`: the page
     names it beside these figures, because the effort slider shows figures
     measured at other levels, and a row that did not say which level it was
     would read as true of all of them.

    python3 tests/subscription_figures.py            print the rows it forms
    python3 tests/subscription_figures.py --check    compare with catalogue.json;
                                                     exit 1 on any difference
    python3 tests/subscription_figures.py --score    write scored.json from the
                                                     raw runs
    python3 tests/subscription_figures.py --write    write the formed rows' derived
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

EVIDENCE = ROOT / "arms" / "2026-09-24" / "subscription"
RESULTS = EVIDENCE / "results.json"
SCORED = EVIDENCE / "scored.json"
# The raw runs are published beside the scored cells since 2026-09-25 (the
# operator's ruling); RAW is kept as its own name because it means something
# different -- vendor model text, not the tool's own records -- even though
# it now resolves to the same directory as EVIDENCE.
RAW = EVIDENCE

SCRIPT = "tests/subscription_figures.py"
# REGISTRATION.md, "What is measured" (2026-09-24). Kept in full for the
# history: the catalogue comparison in row_problems() checks only the
# routes catalogue.json still attributes to this script, which today is
# none of them (see the module docstring).
ROUTES = ("claude-haiku", "claude-sonnet", "claude-opus")
NOT_RUN = ("claude-fable",)
FIGURES = ("silent", "decl", "lost", "bloat", "dup")
# The runner's fields a scored cell carries over unchanged.
CARRIED = ("route", "model", "pair", "fidelity", "exit_code", "wall_seconds",
           "started_at", "claimcheck_commit")

# The fields of a row this program forms. `run`, `artefacts` and `derived_by`
# say where the figures came from and are written by hand.
DERIVED = ("usd_per_merge", "seconds_per_merge", "silent_loss", "silent_loss_per_pair",
           "deviations", "deviations_per_pair", "pairs", "pairs_completed",
           "silent_loss_all_completed", "deviations_all_completed", "pairs_not_completed",
           "model_confirmed_declarations", "absent_behind_rejected_declarations",
           "spread_draws", "fidelity", "measured_on", "claimcheck_commit", "merge_effort")
PAIRS = sorted(p.name for p in (ROOT / "tests" / "pairs").iterdir()
               if (p / "ideal.md").is_file())


# A figure a row's notes state in prose, checked like a field and
# rewritten by `--write`.
SILENT_SHARE = re.compile(r"(\d+) of its (\d+) silent losses are on one pair, rate_limits")


def note_claims(scored: list[dict], formed: dict[str, dict]) -> dict[str, list]:
    """Per row: (pattern, the figures it must state) for every prose claim checked."""
    out = {}
    for route, row in formed.items():
        on = [c for c in scored if c["route"] == route and not c["excluded"]
              and c["pair"] == "rate_limits"]
        if route == "claude-haiku" and len(on) == 1:
            out[route] = [(SILENT_SHARE, (on[0]["silent"], row["silent_loss"]))]
    return out


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def cell_dir(row: dict) -> Path:
    return RAW / f"{row['pair']}-{row['fidelity']}-{row['route']}"


def exclusion(row: dict) -> str:
    """Why a runner row is left out of the rows, or "" when it is counted."""
    if row.get("usage_limit"):
        return "usage_limit"
    if row.get("exit_code") == 2:
        return "exit_2"
    if not row.get("report"):
        return "no_report"
    return ""


def score(results: list[dict]) -> list[dict]:
    """Layer 1's product: one scored record per runner row, from the raw runs."""
    out = []
    for row in results:
        record = {key: row.get(key) for key in CARRIED}
        record["excluded"] = exclusion(row)
        if not record["excluded"]:
            where = cell_dir(row)
            report = load(where / "report.json")
            record.update(rank_matrix.cell_figures(
                row["pair"], (where / "merged.md").read_text(encoding="utf-8"), report))
            record["seconds"] = figure_rules.answer_seconds(report)
        out.append(record)
    return out


def score_problems() -> tuple[list[str], str]:
    """Layer 1: the raw runs, scored now, against the committed scored cells."""
    if not RAW.is_dir():
        return [], (f"UNMEASURED: the raw runs are withheld "
                    f"({RAW.relative_to(ROOT)} is not in this checkout); the scored "
                    f"cells were not re-derived from them")
    now, then = score(load(RESULTS)), load(SCORED)
    if len(now) != len(then):
        return [f"{len(now)} runner rows score to {len(now)} cells, and scored.json "
                f"holds {len(then)}"], ""
    moved = [f"{a['route']}/{a['pair']}" for a, b in zip(now, then) if a != b]
    return ([f"the raw runs, scored with today's rank_matrix.cell_figures, no longer "
             f"give scored.json ({', '.join(moved)})"] if moved else []), \
        f"{len(now)} scored cells re-derived from {RAW.relative_to(ROOT)}"


def one(values: set, what: str):
    if len(values) != 1:
        raise SystemExit(f"subscription_figures: expected one {what}, found "
                         f"{sorted(map(str, values))}")
    return next(iter(values))


def merge_effort(results: list[dict], route: str, counted: list[dict]) -> str:
    """The merge effort every counted run of this route was asked for."""
    kept = {(c["route"], c["pair"], c["started_at"]) for c in counted}
    return one({str(((row.get("decoding") or {}).get("effort") or {}).get("merge"))
                for row in results
                if (row["route"], row["pair"], row["started_at"]) in kept},
               f"merge effort for {route}")


def rows(scored: list[dict], results: list[dict] | None = None) -> dict[str, dict]:
    """Layer 2: each route's derived figures from its counted cells."""
    if results is None:
        results = load(RESULTS)
    for cell in scored:
        if cell["excluded"] == "usage_limit" and not any(
                other["excluded"] != "usage_limit" for other in scored
                if (other["route"], other["pair"]) == (cell["route"], cell["pair"])):
            raise SystemExit(f"subscription_figures: {cell['route']}/{cell['pair']} "
                             f"stopped on a usage limit and was never re-run")
    # The date the run started, for a run that crossed midnight: one run, one day.
    started = min(cell["started_at"] for cell in scored)[:10]
    out = {}
    for route, group in figure_rules.groups(scored, ROUTES, "route", PAIRS,
                                            registered_k1=True).items():
        cells, every = group["cells"], group["all_cells"]
        out[route] = {
            "usd_per_merge": None,
            "seconds_per_merge": figure_rules.per_merge([c["seconds"] for c in cells],
                                                        figure_rules.SECONDS_PLACES),
            **figure_rules.quality(group),
            "spread_draws": group["spread_draws"],
            "fidelity": one({c["fidelity"] for c in every}, f"fidelity for {route}"),
            "measured_on": started,
            "claimcheck_commit": figure_rules.commit_of(every, f"tool commit for {route}"),
            "merge_effort": merge_effort(results, route, every),
        }
    return out


def excluded(scored: list[dict]) -> list[str]:
    return [f"{c['route']}/{c['pair']} ({c['excluded']})" for c in scored if c["excluded"]]


def _superseded(measured) -> bool:
    """True once catalogue.json attributes a measured block to a different
    script: `derived_by` is set and does not name this one."""
    return isinstance(measured, dict) and SCRIPT not in str(measured.get("derived_by"))


def row_problems(block) -> list[str]:
    """Layer 2: the published routes against the rows formed from the cells.

    Checked only for the routes `catalogue.json`'s own `measured.derived_by`
    still names this script; a route it now names to another script
    (the release benchmark superseded haiku and sonnet) is left alone,
    not compared. A route that still names this script but that `ROUTES`
    does not form is reported, not silently skipped.
    """
    if not isinstance(block, list):
        return ["catalogue.json carries no command_routes block to check"]
    formed = rows(load(SCORED))
    published = {entry.get("route"): entry for entry in block}
    out = []
    for route in (*ROUTES, *NOT_RUN):
        if route not in published:
            out.append(f"command_routes has no row for {route}")
    owned = set()
    for route in ROUTES:
        entry = published.get(route)
        if entry is None:
            continue
        measured = entry.get("measured")
        if _superseded(measured):
            continue
        owned.add(route)
        if route not in formed:
            if measured is not None:
                out.append(f"command_routes.{route} carries figures this run did not "
                           f"measure")
            continue
        if not isinstance(measured, dict):
            out.append(f"command_routes.{route} has no measured block; the run gives "
                       f"{json.dumps(formed[route])[:200]}")
            continue
        for key in DERIVED:
            if measured.get(key, "absent") != formed[route][key]:
                out.append(f"command_routes.{route}.measured.{key}: catalogue.json says "
                           f"{json.dumps(measured.get(key, 'absent'))}, the cells give "
                           f"{json.dumps(formed[route][key])}")
    for route, entry in published.items():
        if route in ROUTES:
            continue
        measured = entry.get("measured")
        if isinstance(measured, dict) and SCRIPT in str(measured.get("derived_by")):
            out.append(f"command_routes.{route} names this script but is not one of "
                       f"the routes it forms")
    for route, claims in note_claims(load(SCORED), formed).items():
        if route not in owned:
            continue
        notes = str((published.get(route) or {}).get("notes", ""))
        for pattern, values in claims:
            out += [f"command_routes.{route}.notes: {line}"
                    for line in figure_rules.stated(notes, pattern, values)[0]]
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
    if not RESULTS.is_file():
        print(f"no subscription run at {EVIDENCE.relative_to(ROOT)}", file=sys.stderr)
        return 2
    if args.score:
        SCORED.write_text(json.dumps(score(load(RESULTS)), indent=1) + "\n",
                          encoding="utf-8")
        print(f"wrote {SCORED.relative_to(ROOT)}")
        return 0
    if args.write:
        data = figure_rules.raw_catalogue()
        edits = [(["command_routes",
                   figure_rules.entry_index(data, "command_routes", "route", route), "measured"],
                  key, figures[key])
                 for route, figures in rows(load(SCORED)).items() for key in DERIVED]
        for route, claims in note_claims(load(SCORED), rows(load(SCORED))).items():
            index = figure_rules.entry_index(data, "command_routes", "route", route)
            notes = str(data["command_routes"][index].get("notes", ""))
            for pattern, values in claims:
                notes = figure_rules.stated(notes, pattern, values)[1]
            edits.append((["command_routes", index], "notes", notes))
        changed = figure_rules.write_catalogue(catalogue.DEFAULT_PATH, edits)
        print(f"{'wrote' if changed else 'unchanged:'} {catalogue.DEFAULT_PATH.relative_to(ROOT)}")
        return 0
    if not args.check:
        print(json.dumps(rows(load(SCORED)), indent=2))
        print(f"excluded: {', '.join(excluded(load(SCORED))) or 'none'}")
        return 0
    found, said = score_problems()
    block = catalogue.load().get("command_routes")
    found += row_problems(block)
    for line in found:
        print(f"  DIFFERS  {line}")
    if said.startswith("UNMEASURED"):
        print(said)
    print(f"subscription_figures: {'clean' if not found else f'{len(found)} difference(s)'}"
          f" -- {said if not said.startswith('UNMEASURED') else 'layer 1 not run'}; "
          f"{len(ROUTES)} routes' rows re-derived from {SCORED.relative_to(ROOT)}")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
