#!/usr/bin/env python3
"""The catalogue's `verify_depth` block, formed from the committed depth run.

`src/llossless/web/catalogue.json` publishes what the cheaper verification
depth costs in detection. This program is that block's `derived_by`: every
figure in it is formed here from `arms/2026-09-24/depth/` and each fixture's
`expected.json`, and nothing here calls a model.

Two layers, both re-derived on every `--check`:

  1. The regraded records from the committed reports. `run_detect.regrade`
     over `arms/2026-09-24/depth/r1` must give back `regraded/*.json` field for
     field, the two pointer fields aside (a fresh regrade writes absolute paths,
     the committed copy repository-relative ones). A change to `grade()` that
     moves any record fails here before it can move a published figure.
  2. The block from the regraded records. Per depth and per probe direction:
     plants, plants detected and the rate, how many of those detections no
     model made (the attributions check), guard probes, how many were graded,
     how many graded wrong and the rate. Plus model calls, seconds, the speedup
     against the comparator, and the plants a depth cannot reach.

**A plant is counted only where the fixture took a reading.** An `unmeasured`
fixture (the arm took a reading the fixture sanctions, `fixture_semantics`)
adds its plants to no depth's `plants`, as `run_detect` leaves them out of its
own "measured" count; its guard probes were answered and still count. An
`errored` fixture (exit 2, or no report) adds nothing at all: no plant, no
guard, no call, no second.

**What a depth cannot reach is named by the registration, not inferred from a
miss.** `REGISTRATION.md` prediction 2: a depth with no reverse pass detects no
plant whose detection needs a model pass over the merged document, and it names
`hallucination`. Those plants go to `cannot_detect` at such a depth and out of
its rate. If one was detected anyway, the registration is falsified and this
program refuses to form the block rather than filing it somewhere quieter.

    python3 tests/depth_figures.py            print the figures it forms
    python3 tests/depth_figures.py --check    compare with catalogue.json;
                                              exit 1 on any difference
    python3 tests/depth_figures.py --regrade  rewrite the committed regraded
                                              records from the committed
                                              reports (layer 1's product)
    python3 tests/depth_figures.py --write    write the formed block's
                                              derived fields into catalogue.json
"""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

socket_guard.install()

import figure_rules  # noqa: E402
import fixture_semantics  # noqa: E402
import run_detect  # noqa: E402
from llossless import config  # noqa: E402
from llossless.web import catalogue  # noqa: E402

EVIDENCE = ROOT / "arms" / "2026-09-24" / "depth"
RUN = EVIDENCE / "r1"
REGRADED = EVIDENCE / "regraded"
ARMS = ("full", "coverage")

# REGISTRATION.md, "Arms": `full` (comparator, first).
COMPARATOR = config.FULL_DEPTH
# REGISTRATION.md, prediction 2: the plants whose detection needs a model pass
# over the merged document.
NEEDS_REVERSE_PASS = ("hallucination",)

# The fields of the block this program forms. The rest -- `notes`, `run`,
# `artefacts`, `derived_by`, `registration` -- say where the figures came from
# and are written by hand.
DERIVED = ("comparator", "model", "draws", "fixtures", "plants", "depths",
           "measured_on", "claimcheck_commit")

# The two fields a fresh regrade writes as absolute paths.
POINTERS = ("report_ref", "regraded_from")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def committed(arm: str) -> dict:
    return load(REGRADED / f"{arm}.json")


def relative(blob: dict) -> dict:
    """A regrade's output with its pointers made repository-relative."""
    summary = blob["summary"]
    if summary.get("regraded_from"):
        summary["regraded_from"] = Path(summary["regraded_from"]).resolve() \
            .relative_to(ROOT).as_posix()
    for record in blob["records"]:
        if record.get("report_ref"):
            record["report_ref"] = Path(record["report_ref"]).resolve() \
                .relative_to(ROOT).as_posix()
    return blob


def regraded_now() -> dict[str, dict | None]:
    """Every arm's record as `run_detect.regrade` grades the committed reports today."""
    out = {}
    with tempfile.TemporaryDirectory() as tmp:
        with contextlib.redirect_stdout(io.StringIO()), \
                contextlib.redirect_stderr(io.StringIO()):
            run_detect.regrade(RUN, Path(tmp))
        for arm in ARMS:
            fresh = Path(tmp) / f"{arm}.json"
            out[arm] = relative(load(fresh)) if fresh.is_file() else None
    return out


def regrade_problems() -> list[str]:
    """Layer 1: the committed reports, graded now, against the committed records."""
    out = []
    for arm, now in regraded_now().items():
        if now is None:
            out.append(f"regrading {RUN.relative_to(ROOT)} wrote no {arm}.json")
            continue
        then = committed(arm)
        if now != then:
            moved = [r["fixture"] for r, s in zip(now["records"], then["records"])
                     if r != s]
            out.append(
                f"{arm}: the committed reports, graded with today's grade(), "
                f"no longer give the committed regraded record"
                + (f" (records differ: {', '.join(moved)})" if moved
                   else " (the summary differs)"))
    return out


def rate(count: int, denominator: int):
    return round(count / denominator, 2) if denominator else None


def one(values: set, what: str):
    if len(values) != 1:
        raise SystemExit(f"depth_figures: expected one {what} across the run, "
                         f"found {sorted(map(str, values))}")
    return next(iter(values))


def depth_entry(arm: str, blob: dict) -> tuple[str, dict, dict]:
    """(depth, entry, provenance facts) for one arm's regraded record."""
    reports = [load(ROOT / r["report_ref"]) for r in blob["records"]]
    depth = one({r["provenance"]["merge_policy"]["verify_depth"] for r in reports},
                f"verification depth in {arm}")
    shape = config.VERIFY_DEPTH_SHAPES[depth]
    facts = {
        "model": {m for r in blob["records"] for m in r["harvest"]["models"].values()},
        "date": {r["provenance"]["generated_at"][:10] for r in reports},
        "commit": {r["provenance"]["claimcheck_commit"] for r in reports},
    }

    figures = {d: dict.fromkeys(catalogue.VERIFY_DEPTH_DIRECTION_FIELDS, 0)
               for d in catalogue.VERIFY_DEPTH_DIRECTIONS}
    unreachable: dict[str, dict] = {}
    # An errored fixture took no reading at all; an unmeasured one took
    # none of its plants (its guards were answered, and count).
    graded = [r for r in blob["records"] if r["outcome"] != fixture_semantics.ERRORED]
    for record in graded:
        expected = run_detect.load_expected(record["fixture"])
        direction = {p["probe_id"]: p["direction"] for p in expected["probes"]}
        for probe in (record["probes"]
                      if record["outcome"] != fixture_semantics.UNMEASURED else []):
            where = direction[probe["probe_id"]]
            found = probe["verdict"] == "detected"
            if not shape.detects_invention and record["fixture"] in NEEDS_REVERSE_PASS:
                if found:
                    raise SystemExit(
                        f"depth_figures: {depth} detected {record['fixture']}'s "
                        f"{probe['probe_id']}, which the registration says it "
                        f"cannot reach; prediction 2 is falsified and there is "
                        f"no block to form")
                gap = unreachable.setdefault(record["fixture"], {
                    "class": record["fixture"], "direction": where,
                    "plants": 0, "detected": 0})
                gap["plants"] += 1
                continue
            figures[where]["plants"] += 1
            figures[where]["plants_detected"] += found
            # A model's verdict is always about a claim. A finding with no
            # claim id is a mechanical one: the attribution check that reads the text directly.
            figures[where]["plants_detected_mechanically"] += \
                found and probe.get("claim_id") is None
        for guard in record["guard_probes"]:
            where = direction[guard["probe_id"]]
            figures[where]["guards"] += 1
            figures[where]["guards_graded"] += guard["verdict"] != "unclaimed"
            figures[where]["guards_wrong"] += guard["verdict"] in (
                "wrong_verdict", "false_alarm")

    for where in figures.values():
        where["plants_detected_rate"] = rate(where["plants_detected"], where["plants"])
        where["guards_wrong_rate"] = rate(where["guards_wrong"], where["guards_graded"])
        for key in where:
            where[key] = int(where[key]) if isinstance(where[key], bool) else where[key]

    # Guard: the per-direction figures add back up to the harness's own totals.
    summary = blob["summary"]
    assert sum(f["guards"] for f in figures.values()) == summary["guard_probes_total"]
    assert sum(f["guards_wrong"] for f in figures.values()) == summary["guard_wrong_total"]
    assert sum(f["plants_detected"] for f in figures.values()) == summary["plants_detected"]
    assert (sum(f["plants"] for f in figures.values())
            + sum(g["plants"] for g in unreachable.values())
            == summary["plants_total"] - summary["plants_unmeasured"]
            - summary["plants_errored"])

    entry = {
        "value": depth,
        **figures,
        "cannot_detect": list(unreachable.values()),
        "model_calls": sum(r["harvest"]["calls"] for r in graded),
        "seconds": round(sum(r["wall_seconds"] for r in graded), 1),
    }
    return depth, entry, facts


def block() -> dict:
    """Every derived field of the `verify_depth` block, from the records."""
    blobs = {arm: committed(arm) for arm in ARMS}
    entries, facts = {}, {"model": set(), "date": set(), "commit": set()}
    raw_seconds = {}
    for arm, blob in blobs.items():
        depth, entry, seen = depth_entry(arm, blob)
        entries[depth] = entry
        # Unrounded, so the ratio is not formed from two rounded figures.
        raw_seconds[depth] = sum(r["wall_seconds"] for r in blob["records"]
                                 if r["outcome"] != fixture_semantics.ERRORED)
        for key in facts:
            facts[key] |= seen[key]
    for depth, entry in entries.items():
        if depth != COMPARATOR:
            entry["speedup"] = round(raw_seconds[COMPARATOR] / raw_seconds[depth], 2)
    return {
        "comparator": COMPARATOR,
        "model": one(facts["model"], "model"),
        # One run directory per draw, as the launcher writes them.
        "draws": len([p for p in EVIDENCE.glob("r[0-9]*") if p.is_dir()]),
        "fixtures": one({b["summary"]["fixtures"] for b in blobs.values()},
                        "fixture count"),
        "plants": one({b["summary"]["plants_total"] for b in blobs.values()},
                      "plant count"),
        "depths": [entries[d] for d in config.VERIFY_DEPTHS if d in entries],
        "measured_on": one(facts["date"], "run date"),
        "claimcheck_commit": one(facts["commit"], "tool commit"),
    }


def block_problems(published: dict | None) -> list[str]:
    """Layer 2: the published block against the one formed from the records."""
    if published is None:
        return ["catalogue.json carries no verify_depth block to check"]
    formed = block()
    out = []
    for key in DERIVED:
        if published.get(key) != formed[key]:
            out.append(f"verify_depth.{key}: catalogue.json says "
                       f"{json.dumps(published.get(key))[:300]}, the records give "
                       f"{json.dumps(formed[key])[:300]}")
    return out


def problems(published: dict | None = None) -> list[str]:
    if published is None:
        published = catalogue.load().get("verify_depth")
    return regrade_problems() + block_problems(published)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true",
                      help="compare with catalogue.json and exit 1 on any difference")
    mode.add_argument("--regrade", action="store_true",
                      help="rewrite the committed regraded records from the committed reports")
    mode.add_argument("--write", action="store_true",
                      help="write the formed block's derived fields into catalogue.json")
    args = parser.parse_args(argv)
    if not RUN.is_dir():
        print(f"no depth run at {RUN.relative_to(ROOT)}", file=sys.stderr)
        return 2
    if args.regrade:
        for arm, blob in regraded_now().items():
            if blob is None:
                print(f"regrading {RUN.relative_to(ROOT)} wrote no {arm}.json", file=sys.stderr)
                return 1
            (REGRADED / f"{arm}.json").write_text(json.dumps(blob, indent=2) + "\n",
                                                  encoding="utf-8")
            print(f"wrote {(REGRADED / f'{arm}.json').relative_to(ROOT)}")
        return 0
    if args.write:
        edits = [(["verify_depth"], key, value) for key, value in block().items()]
        changed = figure_rules.write_catalogue(catalogue.DEFAULT_PATH, edits)
        print(f"{'wrote' if changed else 'unchanged:'} {catalogue.DEFAULT_PATH.relative_to(ROOT)}")
        return 0
    if not args.check:
        print(json.dumps(block(), indent=2))
        return 0
    found = problems()
    for line in found:
        print(f"  DIFFERS  {line}")
    print(f"depth_figures: {'clean' if not found else f'{len(found)} difference(s)'}"
          f" -- 2 regraded records re-derived from "
          f"{len(list(RUN.glob('*-reports/*.json')))} committed reports, "
          f"{len(DERIVED)} block fields re-derived from them")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
