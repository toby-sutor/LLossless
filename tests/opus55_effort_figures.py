#!/usr/bin/env python3
"""The catalogue's Opus 5.5 per-effort block, formed from the 2026-09-26 max run.

`src/llossless/web/catalogue.json` gives the `claude-opus` subscription route a
`pinned_by_effort` block for `claude-opus-5-5`: what the merge did at `xhigh`
and `max` when the CLI was asked for that id by name. The
page's effort card reads it beside the route's own 2026-09-25 block, which is
Opus 5 through the `opus` alias, before safe mode. This program is the block's
`derived_by`: every figure in it is formed here from
`arms/2026-09-26/opus-max/`, and nothing here calls a model.
`REGISTRATION.md` in that directory says what was measured.

Three layers, all re-run on every `--check`, following `effort_figures.py`:

  1. The records, checked against themselves and the runner. Every call of
     every run asked for `claude-opus-5-5` in safe mode, and every role was
     answered by it; the merge ran at the cell's level and decompose and
     verify at `low`; the tool commit is the registered pin (`COMMIT`). Each
     voyager record's `fixed`, `kept` and `other` add up to its `total` and
     equal the count of its own per-error `outcomes`; `retrieved` follows
     from `retrieval` and the search count. Re-scoring the published runs
     into those outcomes needs a withheld pipeline, which calls the
     now-published `tests/score_planted.py` over each run's
     own per-error outcome text; that text stays withheld, so this layer
     takes `scored.json`'s outcomes as given and says so. The mahjongg
     control's record needs no such text: `tests/mahjongg_figures.py`
     rescores it from its run with the corrected scorer,
     and every `--check` here runs that check for this run.
  2. The levels from the records, against `tables.md`: fixed, wall seconds,
     draws, runs that retrieved and the API-equivalent usage, per cell, read
     back from the table the scorer rendered. Two computations of one figure.
  3. The catalogue against the levels, field for field.

**Voyager only.** bip39 was not run at either level, and the mahjongg
false-correction control ran once at `max`; neither is in the block. The
block's `notes` state the control's count, rescored, and the count first
published; `--check` holds both to `mahjongg_figures` and `--write` writes
them (a prose figure is checked like a field).
**`api_equivalent_usd` is not a price**: it is each run's summed envelope
`total_cost_usd`, what the same tokens would have cost through the API. The
subscription billed nothing per call (`catalogue.EFFORT_USAGE_FIELD`). Beside
it, **`uncached_list_usd`**: the same run's tokens, every
input token at the model's uncached input rate and every output token at its
output rate in `pricing.py`, from the records' own per-model usage. The
envelope prices the CLI's own prompt cache (reads below the input rate, writes
at 1.25x or 2x it); this column prices none of it, so the two differ by the
cache alone. Web-search fees are not tokens and are in neither.

    python3 tests/opus55_effort_figures.py            print the block it forms
    python3 tests/opus55_effort_figures.py --check    compare with catalogue.json;
                                                      exit 1 on any difference
    python3 tests/opus55_effort_figures.py --write    write the formed block's
                                                      derived fields into
                                                      catalogue.json
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

import figure_rules  # noqa: E402
import mahjongg_figures  # noqa: E402
from llossless.web import catalogue  # noqa: E402

EVIDENCE = ROOT / "arms" / "2026-09-26" / "opus-max"
SCORED = EVIDENCE / "scored.json"
RESULTS = EVIDENCE / "results.json"
TABLES = EVIDENCE / "tables.md"
PIN_FILE = EVIDENCE / "COMMIT"
SCORER = "tests/score_planted.py"
WITHHELD_PIPELINE = "internal/arms/2026-09-26/opus-max/score_max.py"

ROUTE = "claude-opus"
MODEL = "claude-opus-5-5"
PAIR = "voyager"
# REGISTRATION.md, "Grid": xhigh K = 2 as the same-session comparator, max K = 3.
LEVELS = {"xhigh": 2, "max": 3}
FIDELITY = "sourced"
VERIFY_DEPTH = "full"
CHECK_EFFORT = "low"
# Every call carried `--safe-mode`; layer 1 holds each call's own record to it.
SAFE_MODE = True

DERIVED = ("measured_on", "claimcheck_commit", "fidelity", "verify_depth", "draws",
           "requested_model", "resolved_model", "safe_mode", "levels")

# The mahjongg count the block's notes state in prose, checked like a
# field: the rescore and the count first published. `FIRST_WORDING` is the
# sentence as it read before the rescore; `--write` replaces it once.
MAHJONGG_NOTE = re.compile(
    r"The mahjongg false-correction control ran once at max: (\d+) mechanical false "
    r"corrections, not all of them necessarily wrong, unreviewed \(rescored from the "
    r"published run with the corrected tests/score_planted\.py; "
    r"(\d+) as first published, which counted a declared correction of a changed "
    r"sentence twice\)")
FIRST_WORDING = re.compile(
    r"The mahjongg false-correction control ran once at max: (\d+) mechanical false "
    r"corrections, not all of them necessarily wrong, unreviewed(?=;)")


def mahjongg_note() -> tuple[str, tuple[int, int]]:
    """The notes' sentence, filled from the rescore, and its two figures."""
    draws = mahjongg_figures.figures(mahjongg_figures.OPUS_MAX)
    if list(draws) != ["d1"]:
        raise SystemExit(f"opus55_effort_figures: mahjongg draws {list(draws)}; the "
                         f"registration ran one")
    now, first = draws["d1"]
    text = (f"The mahjongg false-correction control ran once at max: {now} mechanical false "
            f"corrections, not all of them necessarily wrong, unreviewed (rescored from the "
            f"published run with the corrected tests/score_planted.py; "
            f"{first} as first published, which counted a declared correction of a changed "
            f"sentence twice)")
    if not MAHJONGG_NOTE.fullmatch(text):
        raise SystemExit("opus55_effort_figures: MAHJONGG_NOTE does not match its own sentence")
    return text, (now, first)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def whole(value):
    return int(value) if float(value).is_integer() else value


def spread(values: list) -> dict:
    return {"median": whole(statistics.median(values)), "min": min(values),
            "max": max(values)}


def money(values: list) -> dict:
    """The usage spread, to the cent, as the page's ratio needs and no finer."""
    return {name: round(float(value), 2) for name, value in spread(values).items()}


def uncached(record: dict) -> float:
    """One run's tokens at the uncached list price, from its per-model usage."""
    figure = figure_rules.uncached_list_usd((record.get("usage") or {}).get("per_model") or {})
    if figure is None or figure <= 0:
        raise SystemExit(f"opus55_effort_figures: {record.get('pair')}/{record.get('effort')}"
                         f"/d{record.get('draw')} has no priceable per-model usage")
    return figure


def rate(count: int, over: int) -> float | None:
    return round(count / over, 2) if over else None


def pin() -> str:
    return PIN_FILE.read_text(encoding="utf-8").strip()[:12]


# -- layer 1 ------------------------------------------------------------------

def run_problems(scored: list[dict], results: list[dict]) -> list[str]:
    """Each voyager record's runner row: the model, safe mode, efforts, pin."""
    runs = {(r["dir"], r["attempt"]): r for r in results}
    out = []
    for record in scored:
        if record.get("pair") != PAIR:
            continue
        where = f"{PAIR}/{record['effort']}/d{record['draw']}"
        run = runs.get((record["dir"], record["attempt"]))
        if run is None:
            out.append(f"{where}: no runner row for {record['dir']}")
            continue
        if str(run.get("claimcheck_commit"))[:12] != pin():
            out.append(f"{where}: ran at {run.get('claimcheck_commit')!r}, not the pin {pin()}")
        calls = run.get("calls") or []
        if not calls:
            out.append(f"{where}: no calls recorded")
        for call in calls:
            want = record["effort"] if call.get("role") == "merge" else CHECK_EFFORT
            if call.get("effort") != want:
                out.append(f"{where}: a {call.get('role')} call ran at "
                           f"{call.get('effort')!r}, not {want!r}")
            if call.get("model_flag") != MODEL:
                out.append(f"{where}: a {call.get('role')} call asked for "
                           f"{call.get('model_flag')!r}, not {MODEL}")
            if call.get("safe_mode") is not SAFE_MODE:
                out.append(f"{where}: a {call.get('role')} call ran with safe_mode "
                           f"{call.get('safe_mode')!r}")
        for role, ids in (run.get("answered_by") or {}).items():
            if ids != [MODEL]:
                out.append(f"{where}: {role} was answered by {ids}, not [{MODEL}]")
    return out


def record_problems(scored: list[dict]) -> list[str]:
    """Each scored voyager record against its own per-error outcomes."""
    out = []
    for r in scored:
        where = f"{r.get('pair')}/{r.get('effort')}/d{r.get('draw')}"
        if r.get("failed"):
            out.append(f"{where}: a failed draw; the block counts every draw")
            continue
        retrieved = (r.get("retrieval") == "retrieved"
                     or (r.get("web_search_requests") or 0) > 0)
        if r.get("retrieved") is not retrieved:
            out.append(f"{where}: retrieved is {r.get('retrieved')!r}, and retrieval "
                       f"{r.get('retrieval')!r} gives {retrieved!r}")
        if r.get("pair") != PAIR:
            continue
        outcomes = r.get("outcomes") or {}
        if len(outcomes) != r.get("total"):
            out.append(f"{where}: {len(outcomes)} outcomes for a total of {r.get('total')}")
        for field in ("fixed", "kept", "other"):
            counted = sum(1 for value in outcomes.values() if value == field)
            if r.get(field) != counted:
                out.append(f"{where}: {field} is {r.get(field)!r}, and its outcomes "
                           f"count {counted}")
        if sum(r.get(f) or 0 for f in ("fixed", "kept", "other")) != r.get("total"):
            out.append(f"{where}: fixed, kept and other do not add up to total")
        usage = (r.get("usage") or {}).get("total_cost_usd")
        if not isinstance(usage, (int, float)) or usage <= 0:
            out.append(f"{where}: no usage figure")
    return out


# -- layer 2 ------------------------------------------------------------------

def measured_on(results: list[dict]) -> str:
    day = date.fromisoformat(EVIDENCE.parent.name)
    start = datetime(day.year, day.month, day.day, tzinfo=timezone.utc)
    for row in results:
        started = datetime.fromisoformat(row["started_at"])
        if not start <= started < start + timedelta(days=1):
            raise SystemExit(f"opus55_effort_figures: a run started at "
                             f"{row['started_at']}, outside {day}")
    return day.isoformat()


def block(scored: list[dict], results: list[dict]) -> dict:
    """Layer 2: the block from the records."""
    levels = {}
    for level, draws in LEVELS.items():
        records = [r for r in scored if r["pair"] == PAIR and r["effort"] == level]
        if len(records) != draws:
            raise SystemExit(f"opus55_effort_figures: {PAIR}/{level} has {len(records)} "
                             f"draws; the registration says {draws}")
        planted = {r["total"] for r in records}
        if len(planted) != 1:
            raise SystemExit(f"opus55_effort_figures: {PAIR}/{level} totals {planted}")
        searched = sum(1 for r in records if r["retrieved"])
        levels[level] = {
            "pairs": {PAIR: {
                "planted": planted.pop(),
                "draws": len(records),
                "fixed": spread([r["fixed"] for r in records]),
                "seconds": spread([round(r["wall_seconds"]) for r in records]),
            }},
            "runs": len(records),
            "searched": searched,
            "searched_rate": rate(searched, len(records)),
            catalogue.EFFORT_USAGE_FIELD: money([r["usage"]["total_cost_usd"]
                                                 for r in records]),
            catalogue.EFFORT_UNCACHED_FIELD: money([uncached(r) for r in records]),
        }
    commits = {str(r["claimcheck_commit"])[:12] for r in results}
    resolved = {i for r in scored if r["pair"] == PAIR
                for ids in (r.get("answered_by") or {}).values() for i in ids}
    if len(commits) != 1 or len(resolved) != 1:
        raise SystemExit(f"opus55_effort_figures: commits {commits}, models {resolved}")
    return {
        "measured_on": measured_on(results),
        "claimcheck_commit": commits.pop(),
        "fidelity": FIDELITY,
        "verify_depth": VERIFY_DEPTH,
        "draws": max(LEVELS.values()),
        "requested_model": MODEL,
        "resolved_model": resolved.pop(),
        "safe_mode": SAFE_MODE,
        "levels": levels,
    }


def table_rows() -> dict[str, dict[str, str]]:
    lines = TABLES.read_text(encoding="utf-8").splitlines()
    header = next(i for i, line in enumerate(lines) if line.startswith("| cell | n |"))
    names = [cell.strip() for cell in lines[header].strip("|").split("|")]
    out = {}
    for line in lines[header + 2:]:
        if not line.startswith("|"):
            break
        values = dict(zip(names, (cell.strip() for cell in line.strip("|").split("|"))))
        out[values["cell"]] = values
    return out


def parse_spread(text: str) -> tuple[float, float, float] | None:
    found = re.fullmatch(r"([\d.]+) \(([\d.]+)-([\d.]+)\)", text or "")
    return tuple(float(x) for x in found.groups()) if found else None


def table_problems(formed: dict) -> list[str]:
    """Layer 2: the formed figures against the cells the scorer rendered."""
    published = table_rows()
    out = []
    for level, figures in formed["levels"].items():
        row = published.get(f"{PAIR} {level}")
        if row is None:
            out.append(f"tables.md has no {PAIR} {level} cell")
            continue
        cell = figures["pairs"][PAIR]
        usage = figures[catalogue.EFFORT_USAGE_FIELD]
        for column, figure, places in (("fixed /44", cell["fixed"], 0),
                                       ("wall s", cell["seconds"], 0),
                                       ("usage USD (API-equiv.)", usage, 2)):
            said = parse_spread(row.get(column, ""))
            want = (figure["median"], figure["min"], figure["max"])
            if said is None or any(abs(a - b) > (0.5 if places == 0 else 0.006)
                                   for a, b in zip(said, want)):
                out.append(f"{PAIR} {level} {column}: tables.md says {row.get(column)!r}, "
                           f"the records give {want}")
        if row.get("n") != f"{cell['draws']}/{LEVELS[level]}":
            out.append(f"{PAIR} {level} n: tables.md says {row.get('n')!r}")
        if row.get("retrieved") != f"{figures['searched']}/{figures['runs']}":
            out.append(f"{PAIR} {level} retrieved: tables.md says {row.get('retrieved')!r}, "
                       f"the records give {figures['searched']}/{figures['runs']}")
    return out


# -- layer 3 ------------------------------------------------------------------

def catalogue_problems(routes) -> list[str]:
    """Layer 3: the published block against the block formed from the records."""
    if not isinstance(routes, list):
        return ["catalogue.json carries no command_routes block to check"]
    entry = next((e for e in routes if e.get("route") == ROUTE), None)
    if entry is None:
        return [f"command_routes has no row for {ROUTE}"]
    pinned = [b for b in entry.get("pinned_by_effort") or []
              if b.get("requested_model") == MODEL]
    if len(pinned) != 1:
        return [f"command_routes.{ROUTE}.pinned_by_effort has {len(pinned)} blocks for "
                f"{MODEL}; the run gives one"]
    formed = block(load(SCORED), load(RESULTS))
    out = []
    for key in DERIVED:
        if pinned[0].get(key, "absent") != formed[key]:
            out.append(f"command_routes.{ROUTE}.pinned_by_effort[{MODEL}].{key}: "
                       f"catalogue.json says {json.dumps(pinned[0].get(key, 'absent'))[:300]}, "
                       f"the records give {json.dumps(formed[key])[:300]}")
    _, values = mahjongg_note()
    out += [f"command_routes.{ROUTE}.pinned_by_effort[{MODEL}].notes: {line}"
            for line in figure_rules.stated(str(pinned[0].get("notes", "")),
                                            MAHJONGG_NOTE, values)[0]]
    for other in routes:
        if other is not entry and any(b.get("requested_model") == MODEL
                                      for b in other.get("pinned_by_effort") or []):
            out.append(f"command_routes.{other.get('route')} carries {MODEL} figures; the "
                       f"run was through the claude CLI and is filed under {ROUTE}")
    return out


def scorer_note() -> str:
    return (f"UNMEASURED: outcomes come from {SCORED.relative_to(ROOT)} as given, not "
            f"re-derived from the published runs -- {SCORER} is published, but re-scoring "
            f"them needs {WITHHELD_PIPELINE}, which calls it over each run's own "
            f"per-error outcome text, and that stays withheld; the mahjongg control is "
            f"rescored from its run by {mahjongg_figures.ME}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true",
                      help="compare with catalogue.json and exit 1 on any difference")
    mode.add_argument("--write", action="store_true",
                      help="write the formed block's derived fields into catalogue.json")
    args = parser.parse_args(argv)
    if not SCORED.is_file():
        print(f"no run at {EVIDENCE.relative_to(ROOT)}", file=sys.stderr)
        return 2
    scored, results = load(SCORED), load(RESULTS)
    formed = block(scored, results)
    if args.write:
        data = figure_rules.raw_catalogue()
        route = figure_rules.entry_index(data, "command_routes", "route", ROUTE)
        pinned = [i for i, b in enumerate(data["command_routes"][route].get("pinned_by_effort")
                                          or []) if b.get("requested_model") == MODEL]
        if len(pinned) != 1:
            raise SystemExit(f"opus55_effort_figures: {len(pinned)} pinned blocks for {MODEL}")
        where = ["command_routes", route, "pinned_by_effort", pinned[0]]
        edits = [(where, key, formed[key]) for key in DERIVED]
        sentence, values = mahjongg_note()
        notes = str(data["command_routes"][route]["pinned_by_effort"][pinned[0]].get("notes", ""))
        if not MAHJONGG_NOTE.search(notes) and len(FIRST_WORDING.findall(notes)) == 1:
            notes = FIRST_WORDING.sub(sentence, notes)
        edits.append((where, "notes", figure_rules.stated(notes, MAHJONGG_NOTE, values)[1]))
        changed = figure_rules.write_catalogue(catalogue.DEFAULT_PATH, edits)
        print(f"{'wrote' if changed else 'unchanged:'} {catalogue.DEFAULT_PATH.relative_to(ROOT)}")
        return 0
    if not args.check:
        print(json.dumps(formed, indent=2))
        return 0
    found = record_problems(scored) + run_problems(scored, results)
    found += table_problems(formed)
    found += catalogue_problems(catalogue.load().get("command_routes"))
    found += mahjongg_figures.problems(mahjongg_figures.OPUS_MAX)
    for line in found:
        print(f"  DIFFERS  {line}")
    print(scorer_note())
    print(f"opus55_effort_figures: {'clean' if not found else f'{len(found)} difference(s)'}"
          f" -- {len(scored)} records, {len(formed['levels'])} levels against "
          f"{TABLES.relative_to(ROOT)} and catalogue.json")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
