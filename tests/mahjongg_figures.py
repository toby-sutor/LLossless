#!/usr/bin/env python3
"""The mahjongg false-correction control, rescored from the published runs. No model call.

Two registered runs carry the control: the 2026-09-25 subscription grid
(`arms/2026-09-25/subscription-comparison/`, Opus and Sonnet at
`medium`, three draws each) and the 2026-09-26 Opus 5.5 run
(`arms/2026-09-26/opus-max/`, one draw at `max`). Their
`scored.json` and `tables.md` were written by withheld pipelines (`score_grid.py`,
`score_max.py`) with the scorer as it was then, which counted a
declared correction beside the changed sentence it names: one correction,
counted twice. `tests/score_planted.py` counts it once, and the operator
ruled on 2026-09-28 to publish the rescored figures
with a note.

This program is that rescore. For every mahjongg record in an arm's
`scored.json` it reads the draw the record itself names (`dir`, `attempt`),
requires the runner's row for it in `results.json`, requires the scorer to
read that draw's own `merged.md`, and scores the report with
`score_planted.false_corrections`. It needs nothing withheld: the runs, the
sources in `tests/handwritten/mahjongg/` and the scorer are all published.

What it writes, and `--check` re-derives, per arm:

  * **`scored.json`**, each mahjongg record: `false_corrections`, its two
    columns and how many declared records name a changed sentence, and the
    sentence counts (`verbatim`, `sentences`, `added`, `dropped`,
    `unmatched`), all the corrected scorer's. The first scoring's values stay
    in the record under `rescored.first_scored`, and `--check` re-derives its
    `false_corrections` too: the first scoring's rule is changed sentences
    plus declared records, each counted.
  * **`tables.md`**, the rendered mahjongg figures: the cell's `false corr.`,
    a note under the cell table, the per-run lines and the section listing
    every draw, which says it was rescored and what was first published.

The voyager and bip39 records are not touched: their per-error outcomes are
the withheld pipelines'. `tests/effort_figures.py --check` and
`tests/opus55_effort_figures.py --check` run this check for their arm, and
the latter holds the catalogue note's count to it.

    python3 tests/mahjongg_figures.py            print the rescored records
    python3 tests/mahjongg_figures.py --check    rescore and compare; exit 1 on any difference
    python3 tests/mahjongg_figures.py --write    write scored.json and tables.md
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

socket_guard.install()

import score_planted  # noqa: E402

PAIR = "mahjongg"
ME = "tests/mahjongg_figures.py"
SCORER = "tests/score_planted.py"
DECISION = "DECISIONS 682 B10"
# What the corrected scorer writes into a record, and what the first scoring did.
FIELDS = ("false_corrections", "false_corrections_changed", "false_corrections_declared",
          "declared_naming_a_change", "verbatim", "sentences", "added", "dropped", "unmatched")
FIRST = ("false_corrections", "verbatim", "sentences", "added", "dropped")
NOTE_START = "`false corr.` above is rescored"


@dataclass(frozen=True)
class Arm:
    path: str          # under the repository root
    by: str            # the record field the draws are grouped by
    draws: dict        # registered draws per group (REGISTRATION.md, "Grid")

    @property
    def root(self) -> Path:
        return ROOT / self.path

    def label(self, record: dict) -> str:
        return f"{record[self.by]} d{record['draw']}" if self.by == "model" else f"d{record['draw']}"


SUBSCRIPTION = Arm("arms/2026-09-25/subscription-comparison", "model",
                   {"opus": 3, "sonnet": 3})
OPUS_MAX = Arm("arms/2026-09-26/opus-max", "effort", {"max": 1})
ARMS = (SUBSCRIPTION, OPUS_MAX)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(data) -> str:
    """`scored.json`'s own layout, as `build_evidence.py` wrote it."""
    return json.dumps(data, indent=1, ensure_ascii=False) + "\n"


def span(values: list) -> str:
    med = statistics.median(values)
    med = int(med) if float(med).is_integer() else med
    return f"{med} ({min(values)}-{max(values)})"


class Unscorable(Exception):
    pass


# -- the rescore ----------------------------------------------------------------

def mahjongg(scored: list[dict]) -> list[dict]:
    return [r for r in scored if r.get("pair") == PAIR]


def rescore(arm: Arm, record: dict, results: list[dict]) -> dict:
    """The corrected scorer over the draw this record names; nothing else."""
    where = f"{arm.path} {arm.label(record)}"
    runs = [r for r in results if (r.get("dir"), r.get("attempt"))
            == (record.get("dir"), record.get("attempt"))]
    if len(runs) != 1 or runs[0].get("pair") != PAIR:
        raise Unscorable(f"{where}: {len(runs)} runner rows for {record.get('dir')} "
                         f"attempt {record.get('attempt')}")
    run_dir = arm.root / record["dir"]
    report, merged = run_dir / "report.json", run_dir / "merged.md"
    if not report.is_file() or not merged.is_file():
        raise Unscorable(f"{where}: {record['dir']} has no report.json and merged.md")
    if score_planted.load(report).text != merged.read_text(encoding="utf-8"):
        raise Unscorable(f"{where}: the scorer did not read {record['dir']}/merged.md")
    got = score_planted.false_corrections(report, PAIR)
    return {"false_corrections": got["false_corrections"],
            "false_corrections_changed": got["false_corrections_changed"],
            "false_corrections_declared": got["false_corrections_declared"],
            "declared_naming_a_change": got["declared_naming_a_change"],
            "verbatim": got["verbatim"], "sentences": got["sentences"],
            "added": len(got["added"]), "dropped": len(got["dropped"]),
            "unmatched": len(got["unmatched"]),
            "numeric": sum(1 for c in got["changed"] if c["numeric"])}


def first_rule(fresh: dict) -> int:
    """The first scoring's count: every changed sentence and every declared record."""
    return fresh["false_corrections_changed"] + fresh["false_corrections_declared"]


def rescored_record(record: dict, fresh: dict) -> dict:
    """The record with the corrected figures, the first scoring's kept beside them."""
    first = (record.get("rescored") or {}).get("first_scored") \
        or {k: record[k] for k in FIRST}
    out = dict(record)
    out.update({k: fresh[k] for k in FIELDS})
    out["rescored"] = {"by": ME, "scorer": SCORER, "decision": DECISION,
                       "first_scored": first}
    return out


def fresh_records(arm: Arm, scored: list[dict] | None = None) -> list[tuple[dict, dict]]:
    """(record as committed, the rescore) for every mahjongg record of an arm."""
    scored = load(arm.root / "scored.json") if scored is None else scored
    results = load(arm.root / "results.json")
    return [(r, rescore(arm, r, results)) for r in mahjongg(scored)]


# -- tables.md ----------------------------------------------------------------

def _cells(line: str) -> list[str]:
    return line.strip()[1:-1].split("|")


def _set_column(lines: list[str], header_start: str, key_of, column: str, values: dict) -> int:
    """Set `column` of every row `key_of` names in the table under `header_start`."""
    at = next(i for i, line in enumerate(lines) if line.startswith(header_start))
    names = [c.strip() for c in _cells(lines[at])]
    col = names.index(column)
    i = at + 2
    while i < len(lines) and lines[i].startswith("|"):
        cells = _cells(lines[i])
        key = key_of(dict(zip(names, (c.strip() for c in cells))))
        if key in values:
            cells[col] = f" {values[key]} "
            lines[i] = "|" + "|".join(cells) + "|"
        i += 1
    return i  # the line after the table


def _set_note(lines: list[str], after: int, note: str) -> None:
    """The note line after a table: blank, note, blank; replaced if there."""
    if after + 1 < len(lines) and lines[after + 1].startswith(NOTE_START):
        lines[after + 1] = note
    else:
        lines[after:after] = ["", note]


def first_text(arm: Arm, pairs: list[tuple[dict, dict]]) -> str:
    groups: dict[str, list[str]] = {}
    for record, _ in pairs:
        first = (record.get("rescored") or {}).get("first_scored") or record
        groups.setdefault(str(record[arm.by]), []).append(
            f"d{record['draw']} {first['false_corrections']}")
    if arm.by == "model":
        return "; ".join(f"{g} {', '.join(v)}" for g, v in groups.items())
    return ", ".join(v for vs in groups.values() for v in vs)


def section_note(arm: Arm, pairs: list[tuple[dict, dict]]) -> str:
    return (f"Rescored from the published runs by `{ME}` with the corrected `{SCORER}` "
            f"({DECISION}): a declared correction that names a sentence the merge changed "
            f"is that sentence's record and counts once, where the first scoring counted "
            f"it twice. The sentence counts are the corrected scorer's too. As first "
            f"published, false corrections: {first_text(arm, pairs)}; every first-scored "
            f"figure is in `scored.json` under `rescored.first_scored`.")


def table_note(arm: Arm, pairs: list[tuple[dict, dict]]) -> str:
    firsts: dict[str, list[int]] = {}
    for record, _ in pairs:
        first = (record.get("rescored") or {}).get("first_scored") or record
        firsts.setdefault(str(record[arm.by]), []).append(first["false_corrections"])
    said = ", ".join(f"{g} {span(v)}" for g, v in firsts.items())
    return (f"{NOTE_START} with the corrected `{SCORER}` ({DECISION}; see the mahjongg "
            f"section below); first published as {said}.")


def detail(fresh: dict) -> str:
    return (f"changed {fresh['false_corrections_changed']}, declared "
            f"{fresh['false_corrections_declared']}, {fresh['declared_naming_a_change']} "
            f"of them naming a changed sentence")


def render_subscription(text: str, pairs: list[tuple[dict, dict]]) -> str:
    arm = SUBSCRIPTION
    lines = text.split("\n")
    by_group: dict[str, list[int]] = {}
    for record, fresh in pairs:
        by_group.setdefault(record["model"], []).append(fresh["false_corrections"])
    values = {(PAIR, g, "medium"): span(v) for g, v in by_group.items()}
    after = _set_column(lines, "| pair | model |",
                        lambda row: (row["pair"], row["model"], row["merge effort"]),
                        "false corr.", values)
    _set_note(lines, after, table_note(arm, pairs))
    body = [section_note(arm, pairs), ""] + [
        f"- {arm.label(r)}: {f['false_corrections']} ({detail(f)}; verbatim "
        f"{f['verbatim']}/{f['sentences']}, adds-only {f['added']}, drops-only "
        f"{f['dropped']}, no source {f['unmatched']})" for r, f in pairs]
    _replace_section(lines, "## mahjongg false corrections, every one", body)
    return "\n".join(lines)


def render_opus_max(text: str, pairs: list[tuple[dict, dict]]) -> str:
    arm = OPUS_MAX
    lines = text.split("\n")
    by_group: dict[str, list[int]] = {}
    for record, fresh in pairs:
        by_group.setdefault(record["effort"], []).append(fresh["false_corrections"])
    values = {f"{PAIR} {g}": span(v) for g, v in by_group.items()}
    after = _set_column(lines, "| cell | n |", lambda row: row["cell"], "false corr.", values)
    _set_note(lines, after, table_note(arm, pairs))
    fc = {(r["draw"], r["effort"], r["attempt"]): f["false_corrections"] for r, f in pairs}
    per_run = re.compile(rf"^(- d(\d+) {PAIR} (\w+) a(\d+): .*?, fc )(\d+)(,)")
    for i, line in enumerate(lines):
        found = per_run.match(line)
        if found:
            key = (int(found.group(2)), found.group(3), int(found.group(4)))
            lines[i] = (line[:found.start(5)] + str(fc[key]) + line[found.end(5):])
    body = [section_note(arm, pairs), ""] + [
        f"- {arm.label(r)}: {f['false_corrections']} mechanical ({detail(f)}; the sentences "
        f"are in the withheld copy of this file, as first scored; the counts are in "
        f"scored.json)" for r, f in pairs]
    _replace_section(lines, "## mahjongg false corrections", body)
    return "\n".join(lines)


def _replace_section(lines: list[str], heading: str, body: list[str]) -> None:
    """Replace a section's body: up to the next heading, or, for the last section,
    up to the blank line after its list (the file's closing lines stay)."""
    at = lines.index(heading)
    end = next((i for i in range(at + 1, len(lines)) if lines[i].startswith("## ")), None)
    if end is None:
        i = at + 1
        while i < len(lines) and lines[i] == "":
            i += 1
        # the body: a paragraph (the note, once written), blank, a list
        seen_list = False
        while i < len(lines):
            if lines[i].startswith("- "):
                seen_list = True
            elif lines[i] == "" and seen_list:
                break
            i += 1
        end = i
        lines[at + 1:end] = ["", *body]
        return
    lines[at + 1:end] = ["", *body, ""]


RENDER = {SUBSCRIPTION.path: render_subscription, OPUS_MAX.path: render_opus_max}


# -- check and write ----------------------------------------------------------

def problems(arm: Arm, scored: list[dict] | None = None,
             text: str | None = None) -> list[str]:
    """Every mahjongg figure of an arm against the rescore of its own runs.

    `scored` and `text` stand in for the committed `scored.json` and
    `tables.md`, for a seeded probe; by default both are read from disk.
    """
    try:
        pairs = fresh_records(arm, scored)
    except Unscorable as e:
        return [str(e)]
    out = []
    counts: dict[str, int] = {}
    for record, fresh in pairs:
        where = f"{arm.path} {arm.label(record)}"
        counts[str(record[arm.by])] = counts.get(str(record[arm.by]), 0) + 1
        for key in FIELDS:
            if record.get(key, "absent") != fresh[key]:
                out.append(f"{where}: scored.json says {key} {record.get(key, 'absent')!r}; "
                           f"the corrected scorer gives {fresh[key]}")
        stamp = record.get("rescored") or {}
        if (stamp.get("by"), stamp.get("scorer"), stamp.get("decision")) != (ME, SCORER, DECISION):
            out.append(f"{where}: scored.json carries no rescored stamp from {ME}")
        first = stamp.get("first_scored") or {}
        if sorted(first) != sorted(FIRST):
            out.append(f"{where}: rescored.first_scored holds {sorted(first)}, not {list(FIRST)}")
        elif first["false_corrections"] != first_rule(fresh):
            out.append(f"{where}: first_scored.false_corrections is "
                       f"{first['false_corrections']}; the first scoring's rule, every "
                       f"changed sentence and every declared record, gives {first_rule(fresh)}")
    if counts != {str(k): v for k, v in arm.draws.items()}:
        out.append(f"{arm.path}: mahjongg records {counts}; the registration says {arm.draws}")
    if text is None:
        text = (arm.root / "tables.md").read_text(encoding="utf-8")
    if RENDER[arm.path](text, pairs) != text:
        out.append(f"{arm.path}/tables.md: its mahjongg figures are not the rescore's "
                   f"(python3 {ME} --write)")
    if arm is SUBSCRIPTION:
        # REGISTRATION.md prediction 9, as `score_grid.py` rendered its verdict.
        numeric = sum(f["numeric"] for _, f in pairs)
        if numeric or "- HELD: 9 no numeric substitution in mahjongg -- []" not in text:
            out.append(f"{arm.path}: prediction 9 reads HELD in tables.md, and the rescore "
                       f"finds {numeric} numeric substitution(s)")
    return out


def write(arm: Arm) -> list[str]:
    scored_path = arm.root / "scored.json"
    scored = load(scored_path)
    results = load(arm.root / "results.json")
    pairs = []
    for i, record in enumerate(scored):
        if record.get("pair") == PAIR:
            fresh = rescore(arm, record, results)
            scored[i] = rescored_record(record, fresh)
            pairs.append((scored[i], fresh))
    wrote = []
    if dump(scored) != scored_path.read_text(encoding="utf-8"):
        scored_path.write_text(dump(scored), encoding="utf-8")
        wrote.append(str(scored_path.relative_to(ROOT)))
    tables = arm.root / "tables.md"
    old = tables.read_text(encoding="utf-8")
    new = RENDER[arm.path](old, pairs)
    if new != old:
        tables.write_text(new, encoding="utf-8")
        wrote.append(str(tables.relative_to(ROOT)))
    return wrote


def figures(arm: Arm) -> dict[str, tuple[int, int]]:
    """(rescored, first published) false corrections per draw, for other scripts' notes."""
    out = {}
    for record, fresh in fresh_records(arm):
        first = (record.get("rescored") or {}).get("first_scored") or record
        out[arm.label(record)] = (fresh["false_corrections"], first["false_corrections"])
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true",
                      help="rescore the runs and compare; exit 1 on any difference")
    mode.add_argument("--write", action="store_true",
                      help="write the rescore into scored.json and tables.md")
    args = parser.parse_args(argv)
    if args.write:
        for arm in ARMS:
            wrote = write(arm)
            print(f"{arm.path}: {'wrote ' + ', '.join(wrote) if wrote else 'unchanged'}")
        return 0
    if not args.check:
        for arm in ARMS:
            for record, fresh in fresh_records(arm):
                print(f"{arm.path} {arm.label(record)}: "
                      f"{json.dumps({k: fresh[k] for k in FIELDS})}")
        return 0
    found = [p for arm in ARMS for p in problems(arm)]
    for line in found:
        print(f"  DIFFERS  {line}")
    n = sum(sum(arm.draws.values()) for arm in ARMS)
    print(f"mahjongg_figures: {'clean' if not found else f'{len(found)} difference(s)'} -- "
          f"{n} mahjongg draws rescored from their runs against scored.json and tables.md "
          f"in {len(ARMS)} arms")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
