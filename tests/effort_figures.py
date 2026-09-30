#!/usr/bin/env python3
"""The catalogue's per-effort figures for the subscription routes, formed from the 2026-09-25 grid.

`src/llossless/web/catalogue.json` gives each measured subscription route a
`measured_by_effort` block: what the merge did at each merge effort level the
registered grid ran. The page's effort slider reads it, one
level at a time. This program is that block's `derived_by`: every figure in it
is formed here from `arms/2026-09-25/subscription-comparison/`, and nothing
here calls a model. `REGISTRATION.md` in that directory says what was measured.

Three layers, all re-run on every `--check`:

  1. The scored records, checked against themselves and the runner. Each
     draw's calls in `results.json` ran at the level its record is filed
     under -- the merge at the cell's, decompose and verify at `low` -- from
     the registered pin. Each voyager and bip39
     record's `fixed`, `kept` and `other` must add up to its `total`, and each
     must equal the count of its own per-error `outcomes`; bip39's `licence`
     must be its error 4; `retrieved` must follow from `retrieval` and the
     search count the way `score_grid.py` forms it. A figure edited in
     `scored.json` without its outcomes fails here. **The raw runs
     are published** since the operator's ruling of 2026-09-25
     (`arms/2026-09-25/subscription-comparison/runs/`), but
     re-scoring them, turning a `merged.md` back into
     `fixed`/`kept`/`other` per planted error, needs the scorer,
     now published at `tests/score_planted.py`, and a withheld
     pipeline that calls it over each run's own per-error outcome
     text, which stays withheld. This layer takes `scored.json`'s
     outcomes as given and checks them for internal consistency;
     it does not re-derive them from the runs, and says so on
     every `--check`. The mahjongg control's records are the
     exception: they need no per-error text, and
     `tests/mahjongg_figures.py` rescores them from the runs with
     the corrected scorer; every `--check` here runs its check for
     this grid.
  2. The levels from the records, against the published table. Per route and
     level: fixed (median, min, max) and wall seconds (median, min, max) per
     pair, the licence on bip39, and runs that searched. The same cells are
     read back out of `tables.md`, which `score_grid.py` rendered when the
     grid was scored, and every one must match. Two computations of one
     figure, from the same records, that must agree.
  3. The catalogue against the levels. Every route's `measured_by_effort`
     must equal what layer 2 formed, field for field; a level the grid never
     ran is absent from `levels`, never zero; `claude-fable` carries null
     (never run). `claude-opus` carries null too (`DROPPED_FROM_CARD`
     below): not because the grid did not run it, but because the operator's
     ruling that Opus 5 is not Opus 5.5 removed that block from the card, so
     this layer stops expecting it there while layers 1 and 2 still form and
     check it for the history.

**Seconds are the whole `merge` run**, decompose and verify
included, because that is what `wall_seconds` timed and what a person waits
for. **`measured_on` is the grid's own date**, the directory's name: the first
draw started at 22:48 UTC on 2026-09-24, which was 00:48 on the 25th where it
was run, and the registration dates it the 25th. The check
holds every start inside that day or the two hours before it.

    python3 tests/effort_figures.py            print the blocks it forms
    python3 tests/effort_figures.py --check    compare with catalogue.json;
                                               exit 1 on any difference
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

socket_guard.install()

import mahjongg_figures  # noqa: E402
from llossless.web import catalogue  # noqa: E402

EVIDENCE = ROOT / "arms" / "2026-09-25" / "subscription-comparison"
SCORED = EVIDENCE / "scored.json"
RESULTS = EVIDENCE / "results.json"
TABLES = EVIDENCE / "tables.md"
# Published since the operator's ruling of 2026-09-25; the pipeline that would
# re-derive SCORED from these is not (see the module docstring, layer 1).
RAW_RUNS = EVIDENCE / "runs"
SCORER = "tests/score_planted.py"
WITHHELD_PIPELINE = "internal/arms/2026-09-25/subscription-comparison/score_grid.py"

# REGISTRATION.md, "Grid". Route id -> the alias it pins. `claude-fable` is
# not run: the operator did not want the most expensive model used.
ROUTES = {"claude-haiku": "haiku", "claude-sonnet": "sonnet", "claude-opus": "opus"}
NOT_RUN = ("claude-fable",)

# The operator's ruling that Opus 5 is not Opus 5.5 and is no longer
# credible removed claude-opus's `measured_by_effort` block from the card
# entirely: it was Claude Opus 5's own K=3 grid from this run, and the
# route's own figures moved to the release benchmark's Opus 5.5 measurement
# instead (tests/lineup_figures.py). `blocks()` and `table_problems()` still
# form and check claude-opus for the history; `catalogue_problems()` alone
# stops expecting the card to carry it, the same "removed by ruling, not
# by a broken check" exception `matrix_figures.REMOVED_FROM_CARD` documents.
DROPPED_FROM_CARD = {
    "claude-opus": "708: Claude Opus 5's own grid, superseded on the card by "
                   "the release benchmark's Opus 5.5 measurement; still formed "
                   "here for the history",
}
# The two pairs with planted errors. mahjongg is the false-correction control,
# run at `medium` only, and the slider's card does not show it.
PAIRS = ("voyager", "bip39")
LEVELS = ("low", "medium", "high", "xhigh")
DRAWS = 3
# bip39's error 4 is the licence: GPL planted, MIT the key.
LICENCE_ERROR = "4"
FIDELITY = "sourced"
VERIFY_DEPTH = "full"
# Whether the CLI ran in safe mode. Registered, not read off a record:
# the clone was pinned at the commit REGISTRATION.md's "Tool" line
# (`COMMIT`) names, which predates the `--safe-mode` flag, and no published
# record carries the argv. The
# check below holds the pin, so a block from another commit cannot inherit it.
SAFE_MODE = False
PINNED = "0418d4886ac7"
# What decompose and verify ran at in every draw: the shipped `low`, with only
# the merge varied (REGISTRATION.md, "Grid").
CHECK_EFFORT = "low"

# The fields of a block this program forms. `run`, `artefacts`, `derived_by`
# and `notes` say where the figures came from and are written by hand.
DERIVED = ("measured_on", "claimcheck_commit", "fidelity", "verify_depth", "draws",
           "resolved_model", "safe_mode", "levels")


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def whole(value):
    """A median of whole numbers, as a whole number when it is one."""
    return int(value) if float(value).is_integer() else value


def spread(values: list) -> dict:
    return {"median": whole(statistics.median(values)), "min": min(values),
            "max": max(values)}


def rate(count: int, over: int) -> float | None:
    return round(count / over, 2) if over else None


# -- layer 1 ------------------------------------------------------------------

def effort_problems(scored: list[dict], results: list[dict]) -> list[str]:
    """Each counted draw's calls against the level its cell names.

    Read off the runner's own per-call record in `results.json`: every merge
    call at the cell's level, every decompose and verify call at `low`. A
    record filed under a level its merge was not asked for fails here.
    """
    runs = {(r["dir"], r["attempt"]): r for r in results}
    out = []
    for record in scored:
        where = (f"{record['pair']}/{record['model']}/{record['effort']}/"
                 f"d{record['draw']}")
        run = runs.get((record["dir"], record["attempt"]))
        if run is None:
            out.append(f"{where}: no runner row for {record['dir']} attempt "
                       f"{record['attempt']}")
            continue
        for call in run.get("calls") or []:
            want = record["effort"] if call.get("role") == "merge" else CHECK_EFFORT
            if call.get("effort") != want:
                out.append(f"{where}: a {call.get('role')} call ran at "
                           f"{call.get('effort')!r}, not {want!r}")
        if str(run.get("claimcheck_commit"))[:12] != PINNED:
            out.append(f"{where}: ran at {run.get('claimcheck_commit')!r}, not the "
                       f"registered pin {PINNED}, so safe_mode={SAFE_MODE} is not "
                       f"known to hold for it")
    return out


def record_problems(scored: list[dict]) -> list[str]:
    """Each scored record against its own per-error outcomes."""
    out = []
    for r in scored:
        where = f"{r.get('pair')}/{r.get('model')}/{r.get('effort')}/d{r.get('draw')}"
        if r.get("failed"):
            out.append(f"{where}: a failed draw; the grid has none and the blocks "
                       f"count every draw")
            continue
        retrieved = (r.get("retrieval") == "retrieved"
                     or (r.get("web_search_requests") or 0) > 0)
        if r.get("retrieved") is not retrieved:
            out.append(f"{where}: retrieved is {r.get('retrieved')!r}, and retrieval "
                       f"{r.get('retrieval')!r} with {r.get('web_search_requests')} "
                       f"searches gives {retrieved!r}")
        if r.get("pair") not in PAIRS:
            continue
        outcomes = r.get("outcomes") or {}
        if len(outcomes) != r.get("total"):
            out.append(f"{where}: {len(outcomes)} outcomes for a total of {r.get('total')}")
        for field in ("fixed", "kept", "other"):
            counted = sum(1 for value in outcomes.values() if value == field)
            if r.get(field) != counted:
                out.append(f"{where}: {field} is {r.get(field)!r}, and its outcomes "
                           f"count {counted}")
        if (r.get("fixed") or 0) + (r.get("kept") or 0) + (r.get("other") or 0) != r.get("total"):
            out.append(f"{where}: fixed, kept and other do not add up to total")
        if r["pair"] == "bip39" and r.get("licence") != outcomes.get(LICENCE_ERROR):
            out.append(f"{where}: licence is {r.get('licence')!r}, and error "
                       f"{LICENCE_ERROR}'s outcome is {outcomes.get(LICENCE_ERROR)!r}")
    return out


# -- layer 2 ------------------------------------------------------------------

def cells(scored: list[dict]) -> dict[tuple[str, str, str], list[dict]]:
    out: dict[tuple[str, str, str], list[dict]] = {}
    for r in scored:
        out.setdefault((r["pair"], r["model"], r["effort"]), []).append(r)
    return out


def one(values: set, what: str):
    if len(values) != 1:
        raise SystemExit(f"effort_figures: expected one {what}, found "
                         f"{sorted(map(str, values))}")
    return next(iter(values))


def measured_on(results: list[dict]) -> str:
    """The grid's date, checked against when its draws really started."""
    day = date.fromisoformat(EVIDENCE.parent.name)
    earliest = datetime(day.year, day.month, day.day, tzinfo=timezone.utc) - timedelta(hours=2)
    latest = earliest + timedelta(hours=26)
    for row in results:
        started = datetime.fromisoformat(row["started_at"])
        if not earliest <= started < latest:
            raise SystemExit(f"effort_figures: a draw started at {row['started_at']}, "
                             f"outside the grid's day {day}")
    return day.isoformat()


def level_figures(runs_by_pair: dict[str, list[dict]]) -> dict:
    """One level's figures for one model, from its voyager and bip39 records."""
    pairs, runs, searched = {}, 0, 0
    for pair in PAIRS:
        records = runs_by_pair[pair]
        figures = {
            "planted": one({r["total"] for r in records}, f"total for {pair}"),
            "draws": len(records),
            "fixed": spread([r["fixed"] for r in records]),
            # `score_grid.py`'s arithmetic: whole seconds per draw.
            "seconds": spread([round(r["wall_seconds"]) for r in records]),
        }
        if pair == "bip39":
            fixed = sum(1 for r in records if r.get("licence") == "fixed")
            figures["licence_fixed"] = fixed
            figures["licence_fixed_rate"] = rate(fixed, len(records))
        pairs[pair] = figures
        runs += len(records)
        searched += sum(1 for r in records if r["retrieved"])
    return {"pairs": pairs, "runs": runs, "searched": searched,
            "searched_rate": rate(searched, runs)}


def blocks(scored: list[dict], results: list[dict]) -> dict[str, dict]:
    """Layer 2: each route's derived block from its records."""
    grid = cells(scored)
    day = measured_on(results)
    out = {}
    for route, model in ROUTES.items():
        levels = {}
        for level in LEVELS:
            runs_by_pair = {pair: grid.get((pair, model, level), []) for pair in PAIRS}
            if not any(runs_by_pair.values()):
                continue
            for pair, records in runs_by_pair.items():
                if len(records) != DRAWS:
                    raise SystemExit(f"effort_figures: {pair}/{model}/{level} has "
                                     f"{len(records)} draws; the grid registered {DRAWS}")
            levels[level] = level_figures(runs_by_pair)
        mine = [r for r in results if r["model"] == model and r["pair"] in PAIRS]
        records = [r for r in scored if r["model"] == model and r["pair"] in PAIRS]
        out[route] = {
            "measured_on": day,
            "claimcheck_commit": one({str(r["claimcheck_commit"])[:12] for r in mine},
                                     f"tool commit for {route}"),
            "fidelity": FIDELITY,
            "verify_depth": VERIFY_DEPTH,
            "draws": DRAWS,
            # The id the alias answered as, from every call's envelope.
            "resolved_model": one({i for r in records
                                   for ids in (r.get("authors") or {}).values() for i in ids},
                                  f"resolved model for {route}"),
            "safe_mode": SAFE_MODE,
            "levels": levels,
        }
    return out


def range_text(figure: dict) -> str:
    return f"{figure['median']:g} ({figure['min']}-{figure['max']})"


def table_rows() -> dict[tuple[str, str, str], dict[str, str]]:
    """The published cells, read out of `tables.md` by column name."""
    lines = TABLES.read_text(encoding="utf-8").splitlines()
    header = next(i for i, line in enumerate(lines) if line.startswith("| pair | model |"))
    names = [cell.strip() for cell in lines[header].strip("|").split("|")]
    out = {}
    for line in lines[header + 2:]:
        if not line.startswith("|"):
            break
        values = dict(zip(names, (cell.strip() for cell in line.strip("|").split("|"))))
        out[(values["pair"], values["model"], values["merge effort"])] = values
    return out


def table_problems(formed: dict[str, dict]) -> list[str]:
    """Layer 2: the formed figures against the cells `score_grid.py` rendered."""
    published = table_rows()
    out = []
    for route, block in formed.items():
        model = ROUTES[route]
        for level, figures in block["levels"].items():
            searched = 0
            for pair, cell in figures["pairs"].items():
                row = published.get((pair, model, level))
                if row is None:
                    out.append(f"tables.md has no {pair}/{model}/{level} cell")
                    continue
                for column, formed_text in (("fixed", range_text(cell["fixed"])),
                                            ("wall s", range_text(cell["seconds"])),
                                            ("n", f"{cell['draws']}/{DRAWS}")):
                    if row.get(column) != formed_text:
                        out.append(f"{pair}/{model}/{level} {column}: tables.md says "
                                   f"{row.get(column)!r}, the records give {formed_text!r}")
                ret = re.fullmatch(r"(\d+)/(\d+)", row.get("ret", ""))
                searched += int(ret.group(1)) if ret else -1
                if pair == "bip39":
                    words = [w.strip() for w in row.get("licence", "").split(",")]
                    if words.count("fixed") != cell["licence_fixed"]:
                        out.append(f"bip39/{model}/{level} licence: tables.md says "
                                   f"{row.get('licence')!r}, the records give "
                                   f"{cell['licence_fixed']} fixed")
            if searched != figures["searched"]:
                out.append(f"{model}/{level}: tables.md's ret columns give {searched} "
                           f"runs that searched, the records {figures['searched']}")
    return out


# -- layer 3 ------------------------------------------------------------------

def catalogue_problems(block) -> list[str]:
    """Layer 3: the published blocks against the blocks formed from the records."""
    if not isinstance(block, list):
        return ["catalogue.json carries no command_routes block to check"]
    formed = blocks(load(SCORED), load(RESULTS))
    published = {entry.get("route"): entry for entry in block}
    out = []
    for route in (*ROUTES, *NOT_RUN):
        if route not in published:
            out.append(f"command_routes has no row for {route}")
    for route, entry in published.items():
        measured = entry.get("measured_by_effort", "absent")
        if route not in formed:
            if measured is not None:
                out.append(f"command_routes.{route}.measured_by_effort is "
                           f"{json.dumps(measured)[:80]}; the grid did not run this "
                           f"route, so it is null")
            continue
        if not isinstance(measured, dict):
            if route in DROPPED_FROM_CARD:
                continue
            out.append(f"command_routes.{route} has no measured_by_effort block; the "
                       f"grid gives {json.dumps(formed[route])[:200]}")
            continue
        for key in DERIVED:
            if measured.get(key, "absent") != formed[route][key]:
                out.append(f"command_routes.{route}.measured_by_effort.{key}: "
                           f"catalogue.json says {json.dumps(measured.get(key, 'absent'))[:300]}, "
                           f"the records give {json.dumps(formed[route][key])[:300]}")
    return out


def scorer_note() -> str:
    """Layer 1's limit: the raw runs are here now; the pipeline that scores them is not."""
    where = "published" if RAW_RUNS.is_dir() else "not in this checkout"
    return (f"UNMEASURED: outcomes come from {SCORED.relative_to(ROOT)} as given, not "
            f"re-derived from the raw runs ({RAW_RUNS.relative_to(ROOT)}, {where}) -- {SCORER} "
            f"is published, but re-scoring them needs {WITHHELD_PIPELINE}, which calls it over "
            f"each run's own per-error outcome text, and that stays withheld; the mahjongg "
            f"control is rescored from the runs by {mahjongg_figures.ME}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true",
                        help="compare with catalogue.json and exit 1 on any difference")
    args = parser.parse_args(argv)
    if not SCORED.is_file():
        print(f"no grid at {EVIDENCE.relative_to(ROOT)}", file=sys.stderr)
        return 2
    scored, results = load(SCORED), load(RESULTS)
    formed = blocks(scored, results)
    if not args.check:
        print(json.dumps(formed, indent=2))
        return 0
    found = record_problems(scored) + effort_problems(scored, results)
    found += table_problems(formed)
    found += catalogue_problems(catalogue.load().get("command_routes"))
    found += mahjongg_figures.problems(mahjongg_figures.SUBSCRIPTION)
    for line in found:
        print(f"  DIFFERS  {line}")
    print(scorer_note())
    print(f"effort_figures: {'clean' if not found else f'{len(found)} difference(s)'} -- "
          f"{len(scored)} records checked against their outcomes, "
          f"{sum(len(b['levels']) for b in formed.values())} levels over "
          f"{len(formed)} routes against {TABLES.relative_to(ROOT)} and catalogue.json")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
