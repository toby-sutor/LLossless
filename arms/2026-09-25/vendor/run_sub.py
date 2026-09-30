#!/usr/bin/env python3
"""B2 of REGISTRATION.md: the subscription `opus` route, effort `high` for every role.

    run_sub.py PLAN          PLAN is pair:draw,pair:draw,... in order

The route's own environment from `commands.Route.environ()` at the pin, with
CLAIMCHECK_EFFORT=high, and the command's program swapped for bin/claude, a
transparent wrapper of the same name that keeps every call's envelope. Each run
is `python -m claimcheck merge`, the real command. Exactly the planned runs;
a usage limit stops the invocation.
"""
from __future__ import annotations

import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

D = Path(os.environ["BENCH_DIR"]).resolve()
TREE = Path(os.environ["BENCH_TREE"]).resolve()
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(TREE / "src"))
import claimcheck  # noqa: E402

if not claimcheck.__file__.startswith(str(TREE / "src") + os.sep):
    raise SystemExit(f"ABORT: claimcheck resolves to {claimcheck.__file__}")
from claimcheck import config  # noqa: E402
from claimcheck.web import commands  # noqa: E402

PIN = (D / "COMMIT").read_text().strip()
ARM = "claude-opus-route"
ROUTE = "claude-opus"
PAIRS_ROOT = TREE / "tests" / "pairs"
RESULTS = D / f"results_{ARM}.json"
DROP = re.compile(r"^(CLAUDE|AI_AGENT|CLAIMCHECK_|ANTHROPIC|OPENAI|VENDOR_KEY)")
LIMIT = re.compile(r"usage limit|limit reached|hit your limit|limit will reset|"
                   r"resets at|out of extra usage|rate limit", re.I)
EFFORT = "high"


def route_env() -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        book = commands.Commands(Path(tmp) / "commands.json")
        book.enable(ROUTE)
        env = book.get(ROUTE).environ()
    argv = shlex.split(env["CLAIMCHECK_COMMAND"])
    if os.path.basename(argv[0]) != "claude":
        raise SystemExit(f"ABORT: the route runs {argv[0]}, not claude")
    env["CLAIMCHECK_COMMAND"] = shlex.join([str(HERE / "bin" / "claude"), *argv[1:]])
    env["CLAIMCHECK_EFFORT"] = EFFORT
    return env


def results() -> list[dict]:
    return json.loads(RESULTS.read_text()) if RESULTS.exists() else []


def record(row: dict) -> None:
    tmp = RESULTS.with_suffix(".tmp")
    tmp.write_text(json.dumps(results() + [row], indent=1))
    os.replace(tmp, RESULTS)


def envelopes(calls: Path) -> dict:
    """The CLI's own usage, summed over every call of this run."""
    total = {"calls": 0, "input_tokens": 0, "output_tokens": 0,
             "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0,
             "total_cost_usd": 0.0, "num_turns": 0, "models": {}, "unreadable": 0,
             "nonzero_rc": 0}
    for out in sorted(calls.glob("*.out")):
        total["calls"] += 1
        rc = out.with_suffix(".rc")
        if rc.exists() and rc.read_text().strip() != "0":
            total["nonzero_rc"] += 1
        try:
            env = json.loads(out.read_text())
        except ValueError:
            total["unreadable"] += 1
            continue
        usage = env.get("usage") or {}
        for key in ("input_tokens", "output_tokens", "cache_creation_input_tokens",
                    "cache_read_input_tokens"):
            total[key] += usage.get(key) or 0
        total["total_cost_usd"] += env.get("total_cost_usd") or 0.0
        total["num_turns"] += env.get("num_turns") or 0
        for model, figures in (env.get("modelUsage") or {}).items():
            slot = total["models"].setdefault(model, {"inputTokens": 0, "outputTokens": 0,
                                                      "costUSD": 0.0})
            for key in slot:
                slot[key] += figures.get(key) or 0
    total["total_cost_usd"] = round(total["total_cost_usd"], 4)
    return total


def run(env_route: dict, pair: str, draw: int) -> dict:
    label = f"{pair}-high-{ARM}-d{draw}"
    cell = D / "cells" / label
    if cell.exists():
        shutil.rmtree(cell)
    cell.mkdir(parents=True)
    for name in ("source_a.md", "source_b.md"):
        shutil.copy(PAIRS_ROOT / pair / name, cell / name)
    (cell / "tmp").mkdir()
    base = {k: v for k, v in os.environ.items() if not DROP.match(k)}
    env = {**base, **env_route, "PYTHONPATH": str(TREE / "src"),
           "BENCH_CALLS": str(cell / "calls"), "TMPDIR": str(cell / "tmp")}
    argv = [sys.executable, "-m", "claimcheck", "merge", "source_a.md", "source_b.md",
            "--base", "source_a.md", "--fidelity", "high", "--verify-depth", "full",
            "--no-cache", "--json", str(cell / "report.json"), "-o", str(cell / "merged.md")]
    started = datetime.now(timezone.utc).isoformat(timespec="seconds")
    print(f"  [{label}] start {started}", flush=True)
    t0 = time.monotonic()
    p = subprocess.run(argv, capture_output=True, text=True, env=env, cwd=str(cell))
    secs = round(time.monotonic() - t0, 1)
    (cell / "stderr.log").write_text(p.stderr or "")
    (cell / "stdout.log").write_text(p.stdout or "")
    usage = envelopes(cell / "calls")
    row = {"arm": ARM, "route": ROUTE, "model": env_route["CLAIMCHECK_MODEL"], "pair": pair,
           "draw": draw, "fidelity": "high", "verify_depth": "full",
           "exit_code": p.returncode, "wall_seconds": secs, "started_at": started,
           "cli_usage": usage}
    problems = []
    report = cell / "report.json"
    if report.exists():
        rep = json.loads(report.read_text())
        prov = rep.get("provenance") or {}
        counts = prov.get("counts") or {}
        decoding = prov.get("decoding") or {}
        isolation = prov.get("isolation") or {}
        row |= {"report": True, "claimcheck_commit": prov.get("claimcheck_commit"),
                "run_mode": prov.get("run_mode"), "calls_by_role": prov.get("calls_by_role"),
                "counts": counts, "structured_output": prov.get("structured_output"),
                "decoding": decoding, "isolation": isolation, "models": prov.get("models")}
        commit = str(prov.get("claimcheck_commit"))
        if commit.endswith("-dirty") or not PIN.startswith(commit):
            problems.append(f"report commit {commit} is not the pin {PIN}")
        if prov.get("run_mode") != "live" or counts.get("cache_hits") or counts.get("replayed"):
            problems.append(f"not a live run: {prov.get('run_mode')}, {counts}")
        roles = set(prov.get("calls_by_role") or {})
        if not {"decompose", "merge", "verify"} <= roles:
            problems.append(f"a role never called: {prov.get('calls_by_role')}")
        if decoding.get("effort") != {role: EFFORT for role in sorted(roles)}:
            problems.append(f"effort {decoding.get('effort')}")
        if any(isolation.get(role) != {"safe_mode": True, "tools": []} for role in roles):
            problems.append(f"isolation {isolation}")
        if counts.get("calls") != usage["calls"]:
            problems.append(f"report says {counts.get('calls')} calls, "
                            f"{usage['calls']} envelopes were kept")
    else:
        row["report"] = False
        row["stderr_tail"] = (p.stderr or "")[-600:]
    if p.returncode == 2 and LIMIT.search((p.stderr or "") + json.dumps(row.get("counts"))):
        row["usage_limit"] = True
    row["problems"] = problems
    record(row)
    print(f"  [{label}] exit={p.returncode} {secs}s calls={usage['calls']} "
          f"out={usage['output_tokens']} api-equiv ${usage['total_cost_usd']:.2f} "
          f"report={row['report']} problems={problems or 'none'}", flush=True)
    return row


def main() -> int:
    plan = [(item.split(":")[0], int(item.split(":")[1])) for item in sys.argv[1].split(",")]
    env_route = route_env()
    got = {role: config.effort_of(env_route["CLAIMCHECK_COMMAND"], role,
                                  config.effort_from_env(env_route)) for role in config.ROLES}
    if got != {role: EFFORT for role in config.ROLES}:
        raise SystemExit(f"ABORT: effort {got}")
    print(f"=== {ROUTE}: {env_route['CLAIMCHECK_COMMAND']} | profile "
          f"{env_route['CLAIMCHECK_PROFILE']} | effort {got}", flush=True)
    done = {(r["pair"], r["draw"]) for r in results()
            if r.get("report") and not r.get("usage_limit")}
    for pair, draw in plan:
        if (pair, draw) in done:
            print(f"  [{pair} d{draw}] skip, recorded", flush=True)
            continue
        row = run(env_route, pair, draw)
        if row["problems"]:
            print(f"STOP: assertion failed: {row['problems']}")
            return 5
        if row.get("usage_limit"):
            print("STOP: subscription usage limit")
            return 4
    rows = results()
    print(f"DONE {ARM}: {len(rows)} rows, {sum(1 for r in rows if r.get('report'))} with a "
          f"report, {sum(r['wall_seconds'] for r in rows):.0f}s wall")
    return 0


if __name__ == "__main__":
    sys.exit(main())
