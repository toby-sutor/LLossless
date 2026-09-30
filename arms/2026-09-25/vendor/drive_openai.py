#!/usr/bin/env python3
"""Arm A of REGISTRATION.md: Sol's sizing cell, Luna's reserve, Sol, then Luna.

Each step is one `bench.sh api ...` invocation; the reserve and the fallback
projections are computed here from the ledger and the results, and printed.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = HERE.parent
ORDER = ["badge_access", "payroll_cutoff", "loading_dock", "freezer_alarm", "bike_docks",
         "trace_names", "library_holds", "index_429", "rate_limits"]  # 2026-09-18 Terra cost


def results(arm):
    path = D / f"results_{arm}.json"
    return json.loads(path.read_text()) if path.exists() else []


def counted(row):
    return bool(row.get("report")) and row.get("exit_code") != 2 and not row.get("problems")


def probe_usd(arm):
    return next(r["ledger_usd"] for r in results(arm) if r["pair"] == "dedup" and counted(r))


def bench(*args, env_extra=None):
    env = {**os.environ, **(env_extra or {})}
    print(f"--- bench.sh {' '.join(args)}  {json.dumps(env_extra or {})}", flush=True)
    return subprocess.run([str(HERE / "bench.sh"), *args], env=env).returncode


def main():
    ratio = probe_usd("gpt-6-luna") / probe_usd("gpt-6-sol")
    cost0918 = {"badge_access": 0.1367, "payroll_cutoff": 0.1581, "loading_dock": 0.1631,
                "freezer_alarm": 0.1688, "bike_docks": 0.1697, "trace_names": 0.1782,
                "library_holds": 0.1988, "index_429": 0.3287, "rate_limits": 0.3552}
    # Before Sol's sizing cell: the runner's default projection (twice 2026-09-18).
    reserve = max(0.30, sum(v * 2 for v in cost0918.values()) * ratio * 1.5)
    print(f"luna/sol probe ratio {ratio:.4f}; reserve before sizing ${reserve:.3f}", flush=True)
    rc = bench("api", "cells", "gpt-6-sol", "badge_access:1",
               env_extra={"BENCH_RESERVE": f"{reserve:.4f}"})
    sized = [r for r in results("gpt-6-sol") if r["pair"] == "badge_access" and counted(r)]
    if rc or not sized:
        print("STOP: Sol's sizing cell did not complete")
        return 1
    first = sized[0]["ledger_usd"]
    sol_proj = {p: first * cost0918[p] / cost0918["badge_access"] for p in ORDER}
    reserve = max(0.30, sum(sol_proj.values()) * ratio * 1.5)
    print(f"Sol sizing ${first:.4f}; Sol nine-pair projection ${sum(sol_proj.values()):.3f}; "
          f"Luna reserve ${reserve:.3f}", flush=True)
    plan = ",".join(f"{p}:1" for p in ORDER[1:])
    bench("api", "cells", "gpt-6-sol", plan, env_extra={"BENCH_RESERVE": f"{reserve:.4f}"})
    sol_done = {r["pair"]: r["ledger_usd"] for r in results("gpt-6-sol")
                if counted(r) and r["pair"] != "dedup"}
    pairs = [p for p in ORDER if p in sol_done]
    print(f"Sol completed {len(pairs)} pairs: {pairs}", flush=True)
    fallback = {p: sol_done[p] * ratio for p in pairs}
    bench("api", "cells", "gpt-6-luna", ",".join(f"{p}:1" for p in pairs),
          env_extra={"BENCH_FALLBACK": json.dumps(fallback), "BENCH_RESERVE": "0"})
    luna_done = [r["pair"] for r in results("gpt-6-luna") if counted(r) and r["pair"] != "dedup"]
    print(f"Luna completed {len(luna_done)} pairs: {luna_done}", flush=True)
    print("ARM A DONE", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
