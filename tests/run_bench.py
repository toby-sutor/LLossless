#!/usr/bin/env python3
"""One command, one arm, both tasks: the benchmark runner.

Promoted from the two session shell scripts that ran the 2026-08-29 halves.
Those worked, and they were a session artifact: the arm's configuration lived in
the shell, the grading lived in two harnesses, the PASS lived in a summariser
written that morning, and the registration lived in a markdown file none of the
three read. Four places, and on 2026-08-27 the summariser reported a green over
two of the three registered members of a must-not-fire set. It was not wrong
about what it checked. It was wrong about what it was checking.

So: **the spec is the registration and this file reads it.** `docs/bench-spec.md`
section 8 is a tab-separated property registry; the runner parses it, evaluates
the properties it knows how to evaluate, and refuses to write a score at all if
that set is not exactly the registered set. Adding a property to the spec breaks
this file until somebody implements it, which is the direction the coupling has
to point.

What it does, in order:

  1. reads the spec version and the property registry
  2. refuses if the candidate is also the judge
  3. scores the two baselines -- byte-concatenation and base-only -- with the
     reconciler alone, no model, every run
  4. runs task `detect` through `tests/run_detect.py`, unchanged
  5. runs task `merge`: K draws per pair per fidelity level through the
     installed CLI, each scored by the reconciler
  6. aggregates as median with min and max, per stage, never blended
  7. evaluates every registered property and writes one JSON record with the
     full provenance

Usage:
    tests/run_bench.py --config arm.json --out DIR
    tests/run_bench.py --config arm.json --out DIR --baselines-only   # offline
    tests/run_bench.py --config arm.json --out DIR --dry-run          # the plan

The config, one JSON object:

    {"label": "A-27b", "model": "qwen3.8:27b", "merge_model": "qwen3.8:27b",
     "judge_model": "qwen3.8:27b", "field_order": "schema",
     "thinking": ["merge"], "draws": 3,
     "pairs": ["badge_access"], "levels": ["off", "high"]}

`judge_model` is the model that decomposes and verifies. It defaults to `model`,
which is exactly the case the refusal in step 2 exists for: the default is the
wrong thing for a scored run and has to be said out loud.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

# This module makes no socket of its own; the subprocesses do. Installed anyway,
# for the same reason `run_detect.py` installs it: the rule
# `tests/test_socket_guard.py` enforces has no exception in this directory, and
# a later refactor that pulls a call in-process must not quietly acquire an
# unguarded socket.
socket_guard.install()

from llossless import config, reconcile  # noqa: E402
from llossless.segment import segment_document  # noqa: E402

SPEC = ROOT / "docs" / "bench-spec.md"
PAIRS_DIR = ROOT / "tests" / "pairs"
VERSION_LINE = re.compile(r"\*\*Version\s+(\d+\.\d+\.\d+)")


# -- the registration, read rather than restated -----------------------------

def spec_version(text: str) -> str:
    match = VERSION_LINE.search(text)
    if not match:
        raise SystemExit(f"{SPEC} carries no `**Version x.y.z` line; a scored "
                         f"run has to name the version it was scored under")
    return match.group(1)


def registry(text: str) -> dict[str, dict[str, str]]:
    """Section 8's fenced ```registry block, as id -> row."""
    block = re.search(r"```registry\n(.*?)```", text, re.S)
    if not block:
        raise SystemExit(f"{SPEC} has no ```registry block. The registration is "
                         f"the file; without the block there is nothing to score "
                         f"against.")
    rows = [line.split("\t") for line in block.group(1).strip().splitlines()]
    header, body = rows[0], rows[1:]
    out = {}
    for row in body:
        if len(row) != len(header):
            raise SystemExit(f"registry row is not {len(header)} tab-separated "
                             f"fields: {row!r}")
        entry = dict(zip(header, row))
        # `task` and `assertion` were declared on every row and read by
        # nothing, so a row could say `merge` about a detect property and
        # register an empty assertion, and the run would score exactly the
        # same. Derived here rather than trusted, at the one site that reads
        # the block: the id prefix already says which task a property belongs
        # to, so a `task` column that disagrees with it is a mislabelled row
        # and not a second opinion.
        expected = {"detect": "detect", "merge": "merge", "run": "both"}
        prefix = entry["id"].split(".")[0]
        if prefix not in expected:
            raise SystemExit(f"registry id {entry['id']!r} is not prefixed "
                             f"detect./merge./run.; the prefix is what says "
                             f"which task the property belongs to")
        if entry["task"] != expected[prefix]:
            raise SystemExit(f"registry row {entry['id']!r} declares task "
                             f"{entry['task']!r}, but its id says "
                             f"{expected[prefix]!r}")
        if not entry["assertion"].strip():
            raise SystemExit(f"registry row {entry['id']!r} registers an empty "
                             f"assertion; a property with nothing written down "
                             f"is not registered")
        out[entry["id"]] = entry
    return out


# -- the judge-free scorer ---------------------------------------------------

def score_merge(sources: dict[str, str], merged: str, dispositions: tuple[dict, ...],
                *, fidelity: str, base: str) -> dict:
    """Section 3's judge-free metrics over one merge. No model, no answer key.

    One implementation, called for the candidate's merges and for both
    baselines, because a baseline scored by a second implementation is a
    baseline for a different metric.
    """
    result = reconcile.reconcile(sources, merged)
    got = reconcile.findings(result, dispositions, fidelity=fidelity,
                             title_policy="keep-base", base=base,
                             budget=config.DEFAULT_DECLARED_LOSS_BUDGET,
                             )
    kinds: dict[str, int] = {}
    for finding in got.findings:
        kinds[finding.kind] = kinds.get(finding.kind, 0) + 1

    segments = got.segments
    merged_segments = len(segment_document(merged, reconcile.MERGE_LETTER).segments)
    undeclared = kinds.get(reconcile.UNDECLARED_ABSENCE, 0)
    declared = len(got.declared_drops)
    lost = declared + undeclared
    return {
        "source_segments": segments,
        "merged_segments": merged_segments,
        # The three section 3 formulas, each written once.
        "undeclared_absence_per_segment": undeclared / segments if segments else 0.0,
        "declared_loss_honesty": (declared / lost) if lost else None,
        "invention": (kinds.get(reconcile.INVENTED_SEGMENT, 0) / merged_segments
                      if merged_segments else 0.0),
        # By kind, never summed. Two merges with one finding each are not two
        # comparable merges.
        "structural_findings": kinds,
        "declared_drops": declared,
        "declared_loss": got.loss,
        "over_budget": reconcile.over_budget(declared, segments, config.DEFAULT_DECLARED_LOSS_BUDGET),
    }


def baselines(pair: Path, *, fidelity: str) -> dict[str, dict]:
    """Section 3's two baselines. Judge-free, model-free, every merge run.

    Scored here rather than argued about once in prose: a floor that is not
    measured in the same session as the candidate is a floor from another day.
    """
    sources = {name: (pair / name).read_text(encoding="utf-8")
               for name in ("source_a.md", "source_b.md")}
    concat = sources["source_a.md"].rstrip("\n") + "\n\n" + sources["source_b.md"]
    return {
        "byte_concatenation": score_merge(sources, concat, (), fidelity=fidelity,
                                          base="source_a.md"),
        "base_only": score_merge(sources, sources["source_a.md"], (),
                                 fidelity=fidelity, base="source_a.md"),
    }


# -- aggregation -------------------------------------------------------------

def aggregate(values: list[float | None]) -> dict | None:
    """Median, min and max. Section 4: never a mean, never a bare median.

    `None` values are dropped rather than counted as zero -- `n/a` honesty on a
    merge that lost nothing is not honesty of 0 -- and the count that survived
    is reported, so a median over one draw cannot be mistaken for one over five.
    """
    kept = [v for v in values if v is not None]
    if not kept:
        return None
    return {"median": statistics.median(kept), "min": min(kept), "max": max(kept),
            "draws": len(kept), "dropped": len(values) - len(kept)}


# -- the arm -----------------------------------------------------------------

def merge_once(pair: Path, out: Path, config: dict, level: str,
               draw: int) -> tuple[dict | None, str]:
    """One `llossless merge` through the installed CLI. Returns (report, error)."""
    merged = out / f"{pair.name}-{level}-{draw}.md"
    report = out / f"{pair.name}-{level}-{draw}.json"
    argv = [
        "llossless", "merge",
        str(pair / "source_a.md"), str(pair / "source_b.md"),
        "--base", str(pair / "source_a.md"),
        "--fidelity", level, "--title-policy", "keep-base",
        "--model", config["judge_model"], "--merge-model", config["merge_model"],
        "--field-order", config.get("field_order", "schema"),
        "--no-cache", "--colour", "never",
        "-o", str(merged), "--json", str(report),
    ]
    for role in config.get("thinking", ()):
        argv += ["--thinking", role]
    done = subprocess.run(argv, capture_output=True, text=True)
    if not report.is_file():
        return None, f"no report written (exit {done.returncode}): {done.stderr[-400:]}"
    blob = json.loads(report.read_text(encoding="utf-8"))
    blob["_merged_path"] = str(merged)
    blob["_exit_code"] = done.returncode
    return blob, ""


def run_merge_task(config: dict, out: Path, live: bool) -> dict:
    pairs = [PAIRS_DIR / name for name in config["pairs"]]
    missing = [p.name for p in pairs if not p.is_dir()]
    if missing:
        raise SystemExit(f"config names pairs that are not in tests/pairs/: {missing}")

    per_pair: dict[str, dict] = {}
    for pair in pairs:
        for level in config["levels"]:
            key = f"{pair.name}/{level}"
            entry = {"baselines": baselines(pair, fidelity=level), "draws": []}
            if live:
                for draw in range(config.get("draws", 3)):
                    blob, error = merge_once(pair, out, config, level, draw)
                    if blob is None:
                        entry["draws"].append({"draw": draw, "error": error})
                        continue
                    sources = {name: (pair / name).read_text(encoding="utf-8")
                               for name in ("source_a.md", "source_b.md")}
                    text = Path(blob["_merged_path"]).read_text(encoding="utf-8")
                    declared = tuple(blob.get("declarations", ()))
                    scored = score_merge(sources, text, declared,
                                         fidelity=level, base="source_a.md")
                    scored.update({"draw": draw, "exit_code": blob["_exit_code"],
                                   "provenance": blob.get("provenance")})
                    entry["draws"].append(scored)
            per_pair[key] = entry

    metrics = {}
    for metric in ("undeclared_absence_per_segment", "declared_loss_honesty",
                   "invention"):
        values = [draw.get(metric) for entry in per_pair.values()
                  for draw in entry["draws"] if "error" not in draw]
        metrics[metric] = aggregate(values)
        for name in ("byte_concatenation", "base_only"):
            metrics[f"baseline.{name}.{metric}"] = aggregate(
                [entry["baselines"][name][metric] for entry in per_pair.values()])
    return {"per_unit": per_pair, "metrics": metrics}


def run_detect_task(config: dict, out: Path, live: bool) -> dict:
    if not live:
        return {"skipped": "detect needs an endpoint; --baselines-only was set"}
    target = out / f"detect-{config['label']}.json"
    argv = [sys.executable, str(ROOT / "tests" / "run_detect.py"),
            "--label", config["label"], "--out", str(target), "--",
            "--model", config["judge_model"],
            "--field-order", config.get("field_order", "schema")]
    for role in config.get("thinking", ()):
        argv += ["--thinking", role]
    done = subprocess.run(argv, capture_output=True, text=True)
    if not target.is_file():
        return {"error": f"run_detect.py wrote nothing (exit {done.returncode})",
                "stderr": done.stderr[-800:]}
    blob = json.loads(target.read_text(encoding="utf-8"))
    summary = blob["summary"]
    findings_total = sum(r.get("findings_total", 0) for r in blob["records"])
    # Both rates are over what this arm was measured on, not over the corpus. A
    # fixture that took no reading is in neither numerator nor denominator
    # of either rate, and the counts it was excluded from travel beside the
    # rates so a reader is never handed one without the other. `.get` with the
    # corpus figure behind it, because a record written before the third
    # outcome existed has no unmeasured column and none of its fixtures were
    # unmeasured.
    fixtures = summary.get("fixtures_measured", summary["fixtures"])
    plants = summary["plants_total"] - summary.get("plants_unmeasured", 0)
    return {
        "record": target.name,
        "metrics": {
            "detection_rate": (summary["plants_detected"] / plants
                               if plants else None),
            "false_finding_rate": (summary["invented_total"] / findings_total
                                   if findings_total else None),
            "invented_total": summary["invented_total"],
            "exit_code_agreement": (len(summary["exit_code_matched"]) / fixtures
                                    if fixtures else None),
        },
        "fixtures_measured": fixtures,
        "plants_measured": plants,
        "unmeasured": summary.get("exit_code_unmeasured", []),
        "disqualified": summary["disqualified"],
        "exit_code_matched": summary["exit_code_matched"],
    }


# -- the properties ----------------------------------------------------------

def evaluate(registered: dict[str, dict], config: dict, detect: dict,
             merge: dict, control: dict | None) -> dict[str, dict]:
    """Every registered property, or a refusal. Section 6.

    Each returns a verdict of `pass`, `fail`, or `not_evaluated` with a reason.
    `not_evaluated` is deliberately not `pass`: a property that did not run is
    the failure this file was promoted to prevent.
    """
    out: dict[str, dict] = {}

    def put(pid: str, ok: bool | None, why: str) -> None:
        out[pid] = {"verdict": "not_evaluated" if ok is None
                    else ("pass" if ok else "fail"), "why": why}

    disq = detect.get("disqualified")
    put("detect.no_seeded_defect_exits_clean",
        None if disq is None else not any("exits 0" in d or "seeded" in d for d in disq),
        f"run_detect disqualifiers: {disq}")
    put("detect.no_invented_finding_on_clean",
        None if disq is None else not any("invented" in d for d in disq),
        f"run_detect disqualifiers: {disq}")

    matched = detect.get("exit_code_matched")
    if matched is None or control is None:
        put("detect.matches_at_least_the_control", None,
            "needs this arm and the control arm in the same session")
    else:
        # Over the fixtures that measured both arms. A fixture that took no
        # reading on either one cannot support "matched at least" in either
        # direction, and counting it as a shortfall would fail an arm for a
        # measurement nobody has. This clause is the one the
        # broken `conflict_surfaced` decided in 2026-08-30's block.
        skip = set(detect.get("unmeasured", ())) | set(control.get("unmeasured", ()))
        base = set(control.get("exit_code_matched", ())) - skip
        short = sorted(base - set(matched))
        put("detect.matches_at_least_the_control", not short,
            f"control matched {short} that this arm did not"
            + (f"; {sorted(skip)} measured neither arm and is excluded" if skip else ""))

    metrics = merge.get("metrics", {})

    def median(key: str):
        got = metrics.get(key)
        return None if got is None else got["median"]

    arm = median("undeclared_absence_per_segment")
    concat = median("baseline.byte_concatenation.undeclared_absence_per_segment")
    only = median("baseline.base_only.undeclared_absence_per_segment")
    put("merge.beats_concatenation_on_absence",
        None if arm is None or concat is None else arm <= concat,
        f"arm {arm}, byte-concatenation {concat}")
    put("merge.beats_base_only_on_absence",
        None if arm is None or only is None else arm < only,
        f"arm {arm}, base-only {only}")

    draws = [d for entry in merge.get("per_unit", {}).values()
             for d in entry["draws"] if "error" not in d]
    put("merge.no_invented_segment",
        None if not draws else not any(d["structural_findings"].get(
            reconcile.INVENTED_SEGMENT) for d in draws),
        f"{len(draws)} scored draw(s)")
    put("merge.declared_loss_within_budget",
        None if not draws else not any(d["over_budget"] for d in draws),
        f"{sum(1 for d in draws if d['over_budget'])} of {len(draws)} draw(s) over budget")
    put("merge.honesty_reported",
        bool(merge.get("per_unit")),
        f"{len(merge.get('per_unit', {}))} unit(s) carry an honesty value or n/a")

    judge = config["judge_model"]
    put("run.candidate_is_not_the_judge",
        judge != config["merge_model"],
        f"merge {config['merge_model']}, judge {judge}")

    seen = {json.dumps(d.get("provenance"), sort_keys=True) for d in draws
            if d.get("provenance") is not None}
    put("run.provenance_read_back",
        None if not seen else len(seen) == 1,
        f"{len(seen)} distinct configuration(s) read back across {len(draws)} draw(s)")

    unknown = sorted(set(out) - set(registered))
    unimplemented = sorted(set(registered) - set(out))
    if unknown or unimplemented:
        raise SystemExit(
            "the property set this runner evaluated is not the set "
            f"docs/bench-spec.md registers.\n"
            f"  evaluated but not registered: {unknown}\n"
            f"  registered but not evaluated: {unimplemented}\n"
            "  Neither is a warning. A property nobody implemented is a "
            "property that passes by not being checked.")
    return out


# -- the self-test -----------------------------------------------------------

def self_test() -> int:
    """Nine of this file's ten refusals, seeded to fire and seeded not to.

    The tenth is `main`'s PATH check. It is not seeded in either direction:
    firing it needs a machine without `llossless` installed, and the
    distinct-judge probe below accommodates it (`want = 0 if on_path else 2`)
    rather than exercising it. Counted and named rather than left out, because
    the count in this docstring is what the paper's methodology section reads.

    This file held seven refusals and `tests/run_all.py` ran none of them: it
    is not in the tool list, has no self-test, and needs a card and a paid
    endpoint to reach `main`. That seven is the count at the moment of the
    finding, before the commit that added this self-test also added the three
    registry-row refusals; it is history, not the current total. So the gate
    the availability section claims --
    that a registered property with no implementation, or an implemented one
    with no registration, aborts before a score is written -- had never run
    outside the two bench sessions that happened to invoke it. A gate reachable
    only from a run nobody can afford to repeat is a pattern seen here
    more than once: it exists, and it does not run where the
    defect occurs.

    Each clause below is probed twice. The must-not-fire probes run against the
    real `docs/bench-spec.md` and the real property set, so the registration
    and the implementation are compared on every commit rather than once per
    bench run. The must-fire probes seed a defect into a copy of the spec text
    and hand it to the shipped function; nothing here restates a condition
    `main` evaluates, because a self-test that rebuilds the expression stays
    green when the expression is reverted.
    """
    failures: list[str] = []

    # `SystemExit` and nothing else. A seeded defect that reaches a `KeyError`
    # deeper in has not been refused -- it has crashed, which on a scored run
    # is a traceback partway through a paid sweep rather than a refusal before
    # it starts. Both probes distinguish the two, because removing a clause and
    # watching the self-test still fail for a different reason is how a probe
    # that proves nothing looks green.
    def fires(what: str, fn) -> None:
        try:
            fn()
        except SystemExit as exc:
            print(f"  ok    fires      {what}: {str(exc).splitlines()[0][:72]}")
            return
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{what}: crashed instead of refusing: "
                            f"{type(exc).__name__}: {exc}")
            print(f"  FAIL  crashed    {what}: {type(exc).__name__}: {exc}")
            return
        failures.append(f"{what}: did not refuse")
        print(f"  FAIL  silent     {what}")

    def holds(what: str, fn) -> None:
        try:
            fn()
        except SystemExit as exc:
            failures.append(f"{what}: refused a clean input: {exc}")
            print(f"  FAIL  refused    {what}: {exc}")
            return
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{what}: crashed on a clean input: "
                            f"{type(exc).__name__}: {exc}")
            print(f"  FAIL  crashed    {what}: {type(exc).__name__}: {exc}")
            return
        print(f"  ok    holds      {what}")

    text = SPEC.read_text(encoding="utf-8")

    holds("spec_version on the real spec", lambda: spec_version(text))
    fires("spec_version with no version line",
          lambda: spec_version(VERSION_LINE.sub("**Vsn", text)))

    holds("registry on the real spec", lambda: registry(text))
    fires("registry with no ```registry block",
          lambda: registry(text.replace("```registry", "```notregistry")))
    fires("registry row short a column",
          lambda: registry(_seed_row(text, lambda r: r[:-1])))
    fires("registry row whose id carries no task prefix",
          lambda: registry(_seed_row(text, lambda r: ["nosuchtask.x"] + r[1:])))
    fires("registry row whose task contradicts its id",
          lambda: registry(_seed_row(
              text, lambda r: [r[0], "merge" if r[1] != "merge" else "detect"] + r[2:])))
    fires("registry row registering an empty assertion",
          lambda: registry(_seed_row(text, lambda r: r[:-1] + ["   "])))

    # The bidirectional property check. `evaluate` needs no endpoint and no
    # draws to build its key set: every `put` runs, and a property with no
    # data reaches `not_evaluated`, which is the verdict this file exists to
    # keep distinct from `pass`.
    registered = registry(text)
    stub = ({"judge_model": "j", "merge_model": "m"}, {}, {}, None)
    holds("evaluate: the spec registry is the implemented property set",
          lambda: evaluate(registered, *stub))
    fires("evaluate: a property implemented but not registered",
          lambda: evaluate({k: v for k, v in registered.items()
                            if k != sorted(registered)[0]}, *stub))
    fires("evaluate: a property registered but not implemented",
          lambda: evaluate({**registered, "merge.not_implemented": {
              "id": "merge.not_implemented", "task": "merge",
              "kind": "judge-free", "role": "gate", "assertion": "x"}}, *stub))

    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        fires("run_merge_task on a config naming a pair that is not there",
              lambda: run_merge_task(
                  {"pairs": ["no_such_pair"], "levels": ["off"]}, out, False))
        real = sorted(p.name for p in PAIRS_DIR.iterdir() if p.is_dir())
        holds("run_merge_task on a config naming a real pair",
              lambda: run_merge_task(
                  {"pairs": real[:1], "levels": ["off"]}, out, False))

        # `main`'s own two refusals, through the command rather than the
        # function: they are argparse-and-exit-code behaviour, and three of
        # this project's defects have lived only on the CLI path. Only the
        # first of the two is seeded; the PATH refusal is read off the
        # environment below, which is why the docstring counts nine of ten.
        def cli(config: dict) -> subprocess.CompletedProcess:
            path = out / "arm.json"
            path.write_text(json.dumps(config), encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(Path(__file__).resolve()),
                 "--config", str(path), "--out", str(out / "run"), "--dry-run"],
                capture_output=True, text=True)

        base = {"label": "selftest", "model": "m", "pairs": real[:1],
                "levels": ["off"], "draws": 1}
        done = cli({**base, "judge_model": "m", "merge_model": "m"})
        if done.returncode == 2 and "also the judge" in done.stderr:
            print("  ok    fires      main: the candidate is also the judge")
        else:
            failures.append(f"candidate-is-judge: exit {done.returncode}")
            print(f"  FAIL  silent     main: candidate is judge, "
                  f"exit {done.returncode}")

        done = cli({**base, "judge_model": "j", "merge_model": "m"})
        on_path = shutil.which("llossless")
        want = 0 if on_path else 2
        if done.returncode == want:
            print(f"  ok    holds      main: distinct judge accepted "
                  f"(llossless {'on' if on_path else 'not on'} PATH, "
                  f"exit {want})")
        else:
            failures.append(f"distinct judge: exit {done.returncode}, "
                            f"wanted {want}")
            print(f"  FAIL             main: distinct judge, "
                  f"exit {done.returncode}, wanted {want}")

    print(f"\n  {len(registered)} registered propert(ies), "
          f"{len(evaluate(registered, *stub))} evaluated, "
          f"{len(failures)} failure(s)")
    for line in failures:
        print(f"    - {line}")
    return 1 if failures else 0


def _seed_row(text: str, mangle) -> str:
    """The spec text with `mangle` applied to the registry's first data row."""
    block = re.search(r"```registry\n(.*?)```", text, re.S)
    rows = block.group(1).strip().splitlines()
    rows[1] = "\t".join(mangle(rows[1].split("\t")))
    return text[:block.start(1)] + "\n".join(rows) + "\n" + text[block.end(1):]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--self-test", action="store_true",
                    help="nine of this file's ten refusals, seeded to fire and not to")
    ap.add_argument("--config", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--control", type=Path,
                    help="a scored record from the control arm in THIS session")
    ap.add_argument("--baselines-only", action="store_true",
                    help="judge-free baselines and the property machinery, no endpoint")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.config or not args.out:
        ap.error("--config and --out are required unless --self-test")

    text = SPEC.read_text(encoding="utf-8")
    version, registered = spec_version(text), registry(text)
    config = json.loads(args.config.read_text(encoding="utf-8"))
    config.setdefault("merge_model", config["model"])
    config.setdefault("judge_model", config["model"])
    config.setdefault("pairs", list(config.get("pairs", [])))
    config.setdefault("levels", ["off", "high"])

    # Refused here, before anything runs, because the failure is silent: a
    # model scoring its own merge measures its agreement with itself and the
    # number looks exactly like the others.
    if config["judge_model"] == config["merge_model"]:
        print(f"REFUSED: the candidate is also the judge "
              f"({config['merge_model']}). A model that scores its own merge "
              f"is measuring its agreement with itself. Set `judge_model` to "
              f"something else, or say so in the config and score it as a "
              f"self-judged run under a different label.", file=sys.stderr)
        return 2

    if not shutil.which("llossless") and not args.baselines_only:
        print("REFUSED: `llossless` is not on PATH. The instrument is the "
              "installed CLI, not this repository's source tree.", file=sys.stderr)
        return 2

    live = not args.baselines_only
    if args.dry_run:
        print(f"  spec {version}, {len(registered)} registered propert(ies)")
        print(f"  arm {config['label']}: merge {config['merge_model']}, "
              f"judge {config['judge_model']}, K={config.get('draws', 3)}")
        print(f"  {len(config['pairs'])} pair(s) x {len(config['levels'])} level(s)"
              f" x {config.get('draws', 3)} draw(s), plus 2 baselines per unit")
        return 0

    args.out.mkdir(parents=True, exist_ok=True)
    started = time.time()
    merge = run_merge_task(config, args.out, live)
    detect = run_detect_task(config, args.out, live)
    control = (json.loads(args.control.read_text(encoding="utf-8")).get("detect")
               if args.control else None)
    properties = evaluate(registered, config, detect, merge, control)

    gates = [pid for pid, row in registered.items() if row["role"] in ("gate", "disqualifier")]
    verdicts = {pid: properties[pid]["verdict"] for pid in gates}
    record = {
        "spec_version": version,
        "label": config["label"],
        "config": config,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "wall_seconds": round(time.time() - started, 1),
        "commit": subprocess.run(["git", "-C", str(ROOT), "describe", "--always", "--dirty"],
                                 capture_output=True, text=True).stdout.strip(),
        "live": live,
        "scores": {"detect": detect.get("metrics", {}), "merge": merge["metrics"]},
        "detect": detect,
        "merge": merge,
        "properties": properties,
        "pass": all(v == "pass" for v in verdicts.values()),
        "gate_verdicts": verdicts,
    }
    target = args.out / f"bench-{config['label']}.json"
    target.write_text(json.dumps(record, indent=1, sort_keys=True) + "\n", encoding="utf-8")

    failed = [p for p, v in verdicts.items() if v != "pass"]
    print(f"\n  spec {version}, arm {config['label']}: "
          f"{len(properties)} propert(ies) evaluated, "
          f"{len(gates) - len(failed)}/{len(gates)} gate(s) pass")
    for pid in failed:
        print(f"    {properties[pid]['verdict'].upper():14} {pid}  "
              f"{properties[pid]['why']}")
    print(f"  {target}")
    return 0 if record["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
