#!/usr/bin/env python3
"""The API arms of REGISTRATION.md, one cell at a time, each through ledger_cli.py.

    run_api.py probe  ARM          one merge of tests/fixtures/dedup
    run_api.py cells  ARM PLAN     PLAN is pair:draw,pair:draw,... in order

BENCH_DIR is the run directory (ledgers, results, cells), BENCH_TREE the pinned
clone. Keys are read from the working repo's .env into the child's environment
only. A cell is started only if the gate allows it; a refusal, a failed
assertion or a ledger refusal stops the invocation.
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
import spend  # noqa: E402

PIN = (D / "COMMIT").read_text().strip()
PAIRS_ROOT = TREE / "tests" / "pairs"
PROBE_PAIR = TREE / "tests" / "fixtures" / "dedup"

ARMS = {
    "gpt-6-sol": dict(vendor="openai", sku="openai/gpt-6-sol", base="https://api.openai.com/v1",
                      key="OPEN_AI_API_KEY", profile="openai-reasoning"),
    "gpt-6-luna": dict(vendor="openai", sku="openai/gpt-6-luna", base="https://api.openai.com/v1",
                       key="OPEN_AI_API_KEY", profile="openai-reasoning"),
    "claude-opus-5": dict(vendor="anthropic", sku="anthropic/claude-opus-5",
                          base="https://api.anthropic.com/v1", key="ANTHROPIC_API_KEY",
                          profile="anthropic"),
    "claude-opus-5-5": dict(vendor="anthropic", sku="anthropic/claude-opus-5-5",
                            base="https://api.anthropic.com/v1", key="ANTHROPIC_API_KEY",
                            profile="anthropic"),
}
CAP = {"openai": 3.90, "anthropic": 8.60}
ALLOWANCE = {"openai": 24_000, "anthropic": 40_000}
MARGIN = 1.25
DROP = re.compile(r"^(CLAUDE|AI_AGENT|CLAIMCHECK_|ANTHROPIC|OPENAI|VENDOR_KEY)")
INFRA = re.compile(r"HTTP (429|5\d\d)|timed out|timeout|usage limit|overloaded", re.I)

# Measured 2026-09-18 at cf30209 (claude-tmp 2026-09-18-matrix, results_*.json):
# the completed cell's cost per pair. Only ratios between pairs are used.
COST_0918 = {
    "openai": {"badge_access": 0.1367, "payroll_cutoff": 0.1581, "loading_dock": 0.1631,
               "freezer_alarm": 0.1688, "bike_docks": 0.1697, "trace_names": 0.1782,
               "library_holds": 0.1988, "index_429": 0.3287, "rate_limits": 0.3552},
    "anthropic": {"badge_access": 0.3631, "payroll_cutoff": 0.3729, "library_holds": 0.3892,
                  "trace_names": 0.4165, "bike_docks": 0.4518, "loading_dock": 0.4618,
                  "freezer_alarm": 0.4654, "index_429": 1.1506, "rate_limits": 1.4313},
}


def env_value(name: str) -> str:
    for line in (REPO / ".env").read_text().splitlines():
        key, _, value = line.strip().partition("=")
        if key.strip().removeprefix("export ").strip() == name:
            return value.strip().strip("'\"")
    raise SystemExit(f"{name} not in .env")


def ledger_path(vendor: str) -> Path:
    return D / f"ledger_{vendor}.json"


def ledger_rows(vendor: str) -> list[dict]:
    path = ledger_path(vendor)
    return json.loads(path.read_text())["rows"] if path.exists() else []


def spent(vendor: str) -> float:
    return sum(r["dollars"] for r in ledger_rows(vendor))


def call_estimate(vendor: str, sku: str) -> float:
    return spend.cost(sku, input_tokens=10_000, output_tokens=ALLOWANCE[vendor])


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
    spec = ARMS[arm]
    model = spec["sku"].split("/", 1)[1]
    tmp = cell / "tmp"
    tmp.mkdir(exist_ok=True)
    base = {k: v for k, v in os.environ.items() if not DROP.match(k)}
    return {**base,
            "PYTHONPATH": str(TREE / "src"), "BENCH_TREE": str(TREE), "TMPDIR": str(tmp),
            "VENDOR_KEY_FOR_RUN": env_value(spec["key"]),
            "CLAIMCHECK_API_KEY_ENV": "VENDOR_KEY_FOR_RUN",
            "CLAIMCHECK_BASE_URL": spec["base"],
            "CLAIMCHECK_MODEL": model, "CLAIMCHECK_MERGE_MODEL": model,
            "CLAIMCHECK_WINDOW": "200000", "CLAIMCHECK_PROFILE": spec["profile"],
            "CLAIMCHECK_TIMEOUT": "600",
            "CLAIMCHECK_THINKING": "decompose,merge,verify",
            "CLAIMCHECK_STRUCTURED": "prompt",
            "CLAIMCHECK_ENDPOINT_LABEL": arm}


def run_cell(arm: str, pair: str, draw: int, source: Path, label: str) -> dict:
    spec = ARMS[arm]
    vendor, sku = spec["vendor"], spec["sku"]
    model = sku.split("/", 1)[1]
    cell = D / "cells" / label
    if cell.exists():
        shutil.rmtree(cell)
    cell.mkdir(parents=True)
    for name in ("source_a.md", "source_b.md"):
        shutil.copy(source / name, cell / name)
    argv = [sys.executable, str(HERE / "ledger_cli.py"), "--state", str(ledger_path(vendor)),
            "--vendor", vendor, "--sku", sku, "--cell", label,
            "--docs", "source_a.md", "source_b.md", "--",
            "merge", "source_a.md", "source_b.md", "--base", "source_a.md",
            "--fidelity", "high", "--verify-depth", "full", "--no-cache",
            "--json", str(cell / "report.json"), "-o", str(cell / "merged.md")]
    before = len(ledger_rows(vendor))
    started = datetime.now(timezone.utc).isoformat(timespec="seconds")
    print(f"  [{label}] start {started}  spent {vendor} ${spent(vendor):.4f}", flush=True)
    t0 = time.monotonic()
    p = subprocess.run(argv, capture_output=True, text=True, env=child_env(arm, cell),
                       cwd=str(cell))
    secs = round(time.monotonic() - t0, 1)
    (cell / "stderr.log").write_text(p.stderr or "")
    (cell / "stdout.log").write_text(p.stdout or "")
    mine = [r for r in ledger_rows(vendor)[before:] if r.get("cell") == label]
    live = [r for r in mine if not r.get("retried_attempt")]
    row = {"arm": arm, "model": model, "pair": pair, "draw": draw, "label": label,
           "fidelity": "high",
           "verify_depth": "full", "exit_code": p.returncode, "wall_seconds": secs,
           "started_at": started, "ledger_calls": len(live),
           "ledger_retried_attempts": len(mine) - len(live),
           "ledger_usd": round(sum(r["dollars"] for r in mine), 6),
           "ledger_all_measured": all(r["measured"] for r in mine),
           "served_models": sorted({str(r.get("served_model")) for r in live}),
           "reasoning_tokens": sum(r.get("reasoning_tokens") or 0 for r in live)}
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
        if not {"decompose", "merge", "verify"} <= set(prov.get("calls_by_role") or {}):
            problems.append(f"a role never called: {prov.get('calls_by_role')}")
        if counts.get("calls") != len(live):
            problems.append(f"report says {counts.get('calls')} calls, ledger charged {len(live)}")
        if (so.get("mode"), so.get("how")) != ("prompt", "pinned"):
            problems.append(f"tier {so}")
        if set((prov.get("models") or {}).values()) != {model}:
            problems.append(f"models {prov.get('models')}")
    else:
        row["report"] = False
        row["stderr_tail"] = (p.stderr or "")[-600:]
    row["problems"] = problems
    record(arm, row)
    print(f"  [{label}] exit={p.returncode} {secs}s ${row['ledger_usd']:.4f} "
          f"calls={row['ledger_calls']} report={row['report']} "
          f"problems={problems or 'none'}  spent {vendor} ${spent(vendor):.4f}", flush=True)
    return row


def refused(vendor: str) -> list:
    path = ledger_path(vendor)
    return json.loads(path.read_text()).get("refused", []) if path.exists() else []


def counted(row: dict) -> bool:
    return bool(row.get("report")) and row.get("exit_code") != 2 and not row.get("problems")


def projection(arm: str, pair: str, fallback: dict) -> float:
    """REGISTRATION.md's per-cell projection.

    The largest cost already measured on this pair in this arm; else the arm's
    first measured cell scaled by the two pairs' 2026-09-18 cost ratio; else the
    driver's stated fallback for the pair; else twice the 2026-09-18 cost.
    """
    vendor = ARMS[arm]["vendor"]
    rows = [r for r in results(arm) if counted(r) and r["pair"] in COST_0918[vendor]]
    seen = [r["ledger_usd"] for r in rows if r["pair"] == pair]
    if seen:
        return max(seen)
    if rows:
        ref = rows[0]
        return ref["ledger_usd"] * COST_0918[vendor][pair] / COST_0918[vendor][ref["pair"]]
    if pair in fallback:
        return fallback[pair]
    return COST_0918[vendor][pair] * 2


def main() -> int:
    mode, arm = sys.argv[1], sys.argv[2]
    spec = ARMS[arm]
    vendor, sku = spec["vendor"], spec["sku"]
    if mode == "probe":
        est = call_estimate(vendor, sku) * 7
        if CAP[vendor] - spent(vendor) < est:
            print(f"GATE: probe for {arm} needs ${est:.2f}, remaining "
                  f"${CAP[vendor] - spent(vendor):.2f}")
            return 3
        row = run_cell(arm, "dedup", 0, PROBE_PAIR, f"probe-dedup-{arm}")
        return 0 if row.get("report") and not row["problems"] else 1
    # cells
    plan = [(item.split(":")[0], int(item.split(":")[1])) for item in sys.argv[3].split(",")]
    fallback = json.loads(os.environ.get("BENCH_FALLBACK", "{}"))
    reserve = float(os.environ.get("BENCH_RESERVE", "0"))
    done = {(r["pair"], r["draw"]) for r in results(arm) if counted(r)}
    for pair, draw in plan:
        if (pair, draw) in done:
            print(f"  [{pair} d{draw}] skip, recorded", flush=True)
            continue
        if refused(vendor):
            print(f"STOP: the ledger refused a call: {refused(vendor)[-1]}")
            return 4
        proj = projection(arm, pair, fallback)
        need = proj * MARGIN + call_estimate(vendor, sku)
        left = CAP[vendor] - spent(vendor) - reserve
        if left < need:
            print(f"GATE: {arm} {pair} d{draw} needs ${need:.3f} (projection ${proj:.3f}), "
                  f"${left:.3f} left after a ${reserve:.2f} reserve; not run", flush=True)
            record(arm, {"arm": arm, "pair": pair, "draw": draw, "gated": True,
                         "projection": round(proj, 4), "need": round(need, 4),
                         "left": round(left, 4)})
            continue
        label = f"{pair}-high-{arm}-d{draw}"
        row = run_cell(arm, pair, draw, PAIRS_ROOT / pair, label)
        if row["problems"]:
            print(f"STOP: assertion failed on {label}: {row['problems']}")
            return 5
        if not row.get("report") or row["exit_code"] == 2:
            tail = (Path(D / "cells" / label / "stderr.log").read_text())[-2000:]
            if INFRA.search(tail) and not refused(vendor):
                again = CAP[vendor] - spent(vendor) - reserve
                if again >= need:
                    print(f"  [{label}] infrastructure fault; one re-run", flush=True)
                    row = run_cell(arm, pair, draw, PAIRS_ROOT / pair, label + "-rerun")
                    if row["problems"]:
                        print(f"STOP: assertion failed on the re-run: {row['problems']}")
                        return 5
    print(f"DONE {arm}: spent {vendor} ${spent(vendor):.4f} of ${CAP[vendor]:.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
