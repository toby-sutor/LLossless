#!/usr/bin/env python3
"""The Google free-tier arms of REGISTRATION.md, one cell at a time, each through ledger_cli.py.

    run_api.py probe  ARM          one merge of tests/fixtures/dedup
    run_api.py cells  ARM PLAN     PLAN is pair:draw,pair:draw,... in order

The vendor run's run_api.py (arms/2026-09-25/vendor/), adapted: one vendor,
free tier, $0.00 cap, no dollar gate. A cell stops the arm when the free
tier's daily quota runs out (ledger_cli exit 8) or a billing signal appears
(exit 9, and STOP-BILLING beside the ledger). BENCH_DIR is the run directory,
BENCH_TREE the pinned clone. The key is read from the working repo's .env into
the child's environment only.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

D = Path(os.environ["BENCH_DIR"]).resolve()
TREE = Path(os.environ["BENCH_TREE"]).resolve()
REPO = Path(os.environ["BENCH_REPO"]).resolve()
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(TREE / "tests"))
sys.path.insert(0, str(TREE / "src"))
import claimcheck  # noqa: E402

if not claimcheck.__file__.startswith(str(TREE / "src") + os.sep):
    raise SystemExit(f"ABORT: claimcheck resolves to {claimcheck.__file__}")

PIN = (D / "COMMIT").read_text().strip()
PAIRS_ROOT = TREE / "tests" / "pairs"
PROBE_PAIR = TREE / "tests" / "fixtures" / "dedup"
BASE = "https://generativelanguage.googleapis.com/v1beta/openai"
TIER = os.environ.get("BENCH_TIER", "prompt")
PROFILE = os.environ.get("BENCH_PROFILE", "google")
ARMS = ("gemini-3.8-flash", "gemini-3.5-flash-lite")
DROP = re.compile(r"^(CLAUDE|AI_AGENT|CLAIMCHECK_|ANTHROPIC|OPENAI|VENDOR_KEY|GOOGLE)")
INFRA = re.compile(r"HTTP (429|5\d\d)|timed out|timeout|overloaded|UNAVAILABLE", re.I)
LEDGER = D / "ledger_google.json"


def env_value(name: str) -> str:
    for line in (REPO / ".env").read_text().splitlines():
        key, _, value = line.strip().partition("=")
        if key.strip().removeprefix("export ").strip() == name:
            return value.strip().strip("'\"")
    raise SystemExit(f"{name} not in .env")


def ledger() -> dict:
    return json.loads(LEDGER.read_text()) if LEDGER.exists() else {"rows": [], "attempts": []}


def results_path(arm: str) -> Path:
    return D / f"results_{arm}.json"


def results(arm: str) -> list[dict]:
    path = results_path(arm)
    return json.loads(path.read_text()) if path.exists() else []


def record(arm: str, row: dict) -> None:
    data = results(arm) + [row]
    tmp = results_path(arm).with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=1))
    os.replace(tmp, results_path(arm))


def child_env(arm: str, cell: Path) -> dict:
    tmp = cell / "tmp"
    tmp.mkdir(exist_ok=True)
    base = {k: v for k, v in os.environ.items() if not DROP.match(k)}
    return {**base,
            "PYTHONPATH": str(TREE / "src"), "BENCH_TREE": str(TREE), "TMPDIR": str(tmp),
            "BENCH_INTERVAL": os.environ.get("BENCH_INTERVAL", "20"),
            "VENDOR_KEY_FOR_RUN": env_value("GOOGLE_AI_API_KEY"),
            "CLAIMCHECK_API_KEY_ENV": "VENDOR_KEY_FOR_RUN",
            "CLAIMCHECK_BASE_URL": BASE,
            "CLAIMCHECK_MODEL": arm, "CLAIMCHECK_MERGE_MODEL": arm,
            "CLAIMCHECK_WINDOW": "200000", "CLAIMCHECK_PROFILE": PROFILE,
            "CLAIMCHECK_TIMEOUT": "600",
            "CLAIMCHECK_THINKING": "decompose,merge,verify",
            "CLAIMCHECK_STRUCTURED": TIER,
            "CLAIMCHECK_ENDPOINT_LABEL": arm}


def run_cell(arm: str, pair: str, draw: int, source: Path, label: str) -> dict:
    cell = D / "cells" / label
    if cell.exists():
        shutil.rmtree(cell)
    cell.mkdir(parents=True)
    for name in ("source_a.md", "source_b.md"):
        shutil.copy(source / name, cell / name)
    argv = [sys.executable, str(HERE / "ledger_cli.py"), "--state", str(LEDGER),
            "--model", arm, "--cell", label,
            "--docs", "source_a.md", "source_b.md", "--",
            "merge", "source_a.md", "source_b.md", "--base", "source_a.md",
            "--fidelity", "high", "--verify-depth", "full", "--no-cache",
            "--json", str(cell / "report.json"), "-o", str(cell / "merged.md")]
    before = len(ledger()["rows"])
    started = datetime.now(timezone.utc).isoformat(timespec="seconds")
    print(f"  [{label}] start {started}", flush=True)
    t0 = time.monotonic()
    p = subprocess.run(argv, capture_output=True, text=True, env=child_env(arm, cell),
                       cwd=str(cell))
    secs = round(time.monotonic() - t0, 1)
    (cell / "stderr.log").write_text(p.stderr or "")
    (cell / "stdout.log").write_text(p.stdout or "")
    state = ledger()
    mine = [r for r in state["rows"][before:] if r.get("cell") == label]
    answered = [r for r in mine if r.get("status") == 200]
    waits = (state.get("waits") or {}).get(label, {})
    row = {"arm": arm, "model": arm, "pair": pair, "draw": draw, "label": label,
           "fidelity": "high", "verify_depth": "full", "exit_code": p.returncode,
           "wall_seconds": secs, "started_at": started,
           "ledger_attempts": len(mine), "ledger_calls": len(answered),
           "ledger_failed_attempts": len(mine) - len(answered),
           "attempt_statuses": sorted({str(r.get("status") or r.get("failed")) for r in mine}),
           "ledger_usd": round(sum(r["dollars"] for r in mine), 6),
           "ledger_all_measured": all(r.get("prompt_tokens") is not None for r in answered),
           "paced_seconds": waits.get("pace", 0.0), "backoff_seconds": waits.get("backoff", 0.0),
           "served_models": sorted({str(r.get("served_model")) for r in answered}),
           "prompt_tokens": sum(r.get("prompt_tokens") or 0 for r in answered),
           "completion_tokens": sum(r.get("completion_tokens") or 0 for r in answered),
           "total_tokens": sum(r.get("total_tokens") or 0 for r in answered),
           "cached_tokens": sum(r.get("cached_tokens") or 0 for r in answered),
           "reasoning_tokens": sum(r.get("reasoning_tokens") or 0 for r in answered)}
    if p.returncode == 8:
        row["quota_day"] = True
    if p.returncode == 9:
        row["billing_stop"] = True
    report = cell / "report.json"
    problems = []
    if report.exists():
        rep = json.loads(report.read_text())
        prov = rep.get("provenance") or {}
        counts = prov.get("counts") or {}
        so = prov.get("structured_output") or {}
        row |= {"report": True, "claimcheck_commit": prov.get("claimcheck_commit"),
                "run_mode": prov.get("run_mode"), "calls_by_role": prov.get("calls_by_role"),
                "counts": counts, "tokens": prov.get("tokens"),
                "structured_output": so, "decoding": prov.get("decoding"),
                "models": prov.get("models"), "errors": counts.get("errors")}
        commit = str(prov.get("claimcheck_commit"))
        if commit.endswith("-dirty") or not PIN.startswith(commit):
            problems.append(f"report commit {commit} is not the pin {PIN}")
        if prov.get("run_mode") != "live" or counts.get("cache_hits") or counts.get("replayed"):
            problems.append(f"not a live run: {prov.get('run_mode')}, {counts}")
        # An exit 2 is a pipeline that stopped (the registration excludes and
        # names it); the roles after the one that failed never ran, by design.
        if p.returncode != 2 and \
                not {"decompose", "merge", "verify"} <= set(prov.get("calls_by_role") or {}):
            problems.append(f"a role never called: {prov.get('calls_by_role')}")
        if counts.get("calls") != len(answered):
            problems.append(f"report says {counts.get('calls')} calls, ledger answered "
                            f"{len(answered)}")
        if (so.get("mode"), so.get("how")) != (TIER, "pinned"):
            problems.append(f"tier {so}")
        if set((prov.get("models") or {}).values()) != {arm}:
            problems.append(f"models {prov.get('models')}")
    else:
        row["report"] = False
        row["stderr_tail"] = (p.stderr or "")[-600:]
    if row["ledger_usd"] != 0.0:
        problems.append(f"the ledger charged ${row['ledger_usd']} on a $0.00 cap")
    row["problems"] = problems
    record(arm, row)
    print(f"  [{label}] exit={p.returncode} {secs}s paced={row['paced_seconds']}s "
          f"backoff={row['backoff_seconds']}s calls={row['ledger_calls']}/"
          f"{row['ledger_attempts']} statuses={row['attempt_statuses']} "
          f"report={row['report']} problems={problems or 'none'}", flush=True)
    return row


def counted(row: dict) -> bool:
    return bool(row.get("report")) and row.get("exit_code") != 2 and not row.get("problems")


def stopped(row: dict) -> str:
    if row.get("billing_stop") or (D / "STOP-BILLING").exists():
        return "STOP: a billing signal; see STOP-BILLING"
    if row.get("quota_day"):
        return "STOP: the free tier's daily quota is exhausted"
    return ""


def main() -> int:
    mode, arm = sys.argv[1], sys.argv[2]
    if arm not in ARMS:
        raise SystemExit(f"unknown arm {arm}")
    if (D / "STOP-BILLING").exists():
        print("STOP: STOP-BILLING exists")
        return 9
    if mode == "probe":
        row = run_cell(arm, "dedup", 0, PROBE_PAIR, f"probe-dedup-{arm}")
        if stopped(row):
            print(stopped(row))
            return 8
        return 0 if row.get("report") and not row["problems"] else 1
    plan = [(item.split(":")[0], int(item.split(":")[1])) for item in sys.argv[3].split(",")]
    done = {(r["pair"], r["draw"]) for r in results(arm) if counted(r)}
    for pair, draw in plan:
        if (pair, draw) in done:
            print(f"  [{pair} d{draw}] skip, recorded", flush=True)
            continue
        label = f"{pair}-high-{arm}-d{draw}"
        row = run_cell(arm, pair, draw, PAIRS_ROOT / pair, label)
        if stopped(row):
            print(stopped(row), flush=True)
            return 8
        if row["problems"]:
            print(f"STOP: assertion failed on {label}: {row['problems']}")
            return 5
        if not row.get("report") or row["exit_code"] == 2:
            tail = (Path(D / "cells" / label / "stderr.log").read_text())[-2000:]
            if INFRA.search(tail):
                print(f"  [{label}] infrastructure fault; one re-run", flush=True)
                row = run_cell(arm, pair, draw, PAIRS_ROOT / pair, label + "-rerun")
                if stopped(row):
                    print(stopped(row), flush=True)
                    return 8
                if row["problems"]:
                    print(f"STOP: assertion failed on the re-run: {row['problems']}")
                    return 5
    print(f"DONE {arm}: ledger charged ${sum(r['dollars'] for r in ledger()['rows']):.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
