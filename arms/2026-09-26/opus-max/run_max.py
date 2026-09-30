#!/usr/bin/env python3
"""Merge effort `max` on Opus 5.5, 2026-09-26: draw-major, serial, from a pinned clone.

Adapted from 609's run_grid.py. Run by bench.sh with BENCH_DIR set. See
REGISTRATION.md. Each run goes to BENCH_DIR/runs/d<draw>/<pair>-<effort>/a<n>/;
one row per attempt is appended to BENCH_DIR/results.json. Resumable.
"""
import json, os, pathlib, re, shutil, signal, statistics, subprocess, sys, tempfile, time
from datetime import datetime, timezone

D = pathlib.Path(os.environ["BENCH_DIR"])
TREE = D / "tree"
PAIRS_ROOT = TREE / "tests" / "handwritten"
RESULTS = D / "results.json"
RUNS = D / "runs"
WRAPPER = D / "bin" / "claude"
MODEL = "claude-opus-5-5"
sys.path.insert(0, str(TREE / "src"))

import llossless  # noqa: E402
if not llossless.__file__.startswith(str(TREE / "src") + "/"):
    raise SystemExit(f"ABORT: llossless resolves to {llossless.__file__}")
from llossless import config  # noqa: E402
from llossless.web import commands  # noqa: E402

TIMEOUT = "1800"
RUN_LIMIT = 45 * 60
COST_FACTOR = 5
DRAWS = {1: [("voyager", "xhigh"), ("voyager", "max"), ("mahjongg", "max")],
         2: [("voyager", "xhigh"), ("voyager", "max")],
         3: [("voyager", "max")]}

DROP = re.compile(r"^(CLAUDE|AI_AGENT|LLOSSLESS_|CLAIMCHECK_)")
BASE = {k: v for k, v in os.environ.items() if not DROP.match(k)}
LIMIT = re.compile(r"usage limit|limit reached|hit your limit|limit will reset|"
                   r"resets at|out of extra usage|rate limit", re.I)


def route_env() -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        book = commands.Commands(pathlib.Path(tmp) / "commands.json")
        book.enable("claude-opus")
        env = dict(book.get("claude-opus").environ())
    argv = env["LLOSSLESS_COMMAND"].split()
    if os.path.basename(argv[0]) != "claude" or argv[-2:] != ["--model", "opus"]:
        raise SystemExit(f"ABORT: unexpected route {env['LLOSSLESS_COMMAND']}")
    env["LLOSSLESS_COMMAND"] = " ".join([str(WRAPPER), *argv[1:-1], MODEL])
    env["LLOSSLESS_MODEL"] = env["LLOSSLESS_MERGE_MODEL"] = MODEL
    return env


def load() -> list[dict]:
    return json.loads(RESULTS.read_text()) if RESULTS.exists() else []


def record(row: dict) -> None:
    data = load()
    data.append(row)
    tmp = RESULTS.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=1))
    tmp.replace(RESULTS)


def calls_of(work: pathlib.Path, ledger: list[dict]) -> list[dict]:
    out = []
    for n, path in enumerate(sorted((work / "calls").glob("*.out"))):
        argv = (path.with_suffix(".argv")).read_text().split("\n")
        try:
            env = json.loads(path.read_text())
        except ValueError:
            env = {}
        usage = env.get("modelUsage") or {}
        u = env.get("usage") or {}
        out.append({
            "role": ledger[n].get("role") if n < len(ledger) else None,
            "effort": argv[argv.index("--effort") + 1] if "--effort" in argv else None,
            "model_flag": argv[argv.index("--model") + 1] if "--model" in argv else None,
            "safe_mode": "--safe-mode" in argv,
            "tools": argv[argv.index("--tools") + 1] if "--tools" in argv else None,
            "is_error": env.get("is_error"),
            "subtype": env.get("subtype"),
            "num_turns": env.get("num_turns"),
            "models": sorted(usage),
            "model_usage": usage,
            "web_search_requests": sum(int((b or {}).get("webSearchRequests") or 0)
                                       for b in usage.values()),
            "total_cost_usd": env.get("total_cost_usd"),
            "input_tokens": u.get("input_tokens"),
            "output_tokens": u.get("output_tokens"),
            "thinking_tokens": (u.get("output_tokens_details") or {}).get("thinking_tokens"),
            "cache_read_input_tokens": u.get("cache_read_input_tokens"),
            "cache_creation_input_tokens": u.get("cache_creation_input_tokens"),
            "subagents_spawned": (env.get("subagent_stats") or {}).get("spawned"),
            "permission_denials": [d.get("tool_name") for d in env.get("permission_denials") or []],
            "duration_ms": env.get("duration_ms"),
        })
    return out


def usage_sum(calls: list[dict]) -> dict:
    tot = {"total_cost_usd": 0.0, "input_tokens": 0, "output_tokens": 0,
           "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0}
    per_model: dict[str, dict] = {}
    for c in calls:
        for k in tot:
            tot[k] += c.get(k) or 0
        for m, b in (c.get("model_usage") or {}).items():
            pm = per_model.setdefault(m, {"inputTokens": 0, "outputTokens": 0,
                                          "cacheReadInputTokens": 0,
                                          "cacheCreationInputTokens": 0, "costUSD": 0.0})
            for k in pm:
                pm[k] += (b or {}).get(k) or 0
    tot["total_cost_usd"] = round(tot["total_cost_usd"], 4)
    tot["per_model"] = per_model
    return tot


def run(pair: str, effort: str, draw: int, attempt: int, env_route: dict) -> dict:
    work = RUNS / f"d{draw}" / f"{pair}-{effort}" / f"a{attempt}"
    if work.exists():
        shutil.rmtree(work)
    (work / "tmp").mkdir(parents=True)
    names = sorted(p.name for p in (PAIRS_ROOT / pair).glob("source_*.md"))
    for name in names:
        shutil.copy(PAIRS_ROOT / pair / name, work / name)
    env = {**BASE, **env_route, "PYTHONPATH": str(TREE / "src"),
           "BENCH_CALLS": str(work / "calls"), "TMPDIR": str(work / "tmp")}
    argv = [sys.executable, "-m", "llossless", "merge", *names,
            "--base", "source_a.md", "--fidelity", "sourced", "--verify-depth", "full",
            "--effort", f"merge={effort}", "--timeout", TIMEOUT, "--no-cache",
            "--json", str(work / "report.json"), "-o", str(work / "merged.md"), "-v"]
    (work / "argv.json").write_text(json.dumps(argv[1:], indent=1))
    started = datetime.now(timezone.utc).isoformat(timespec="seconds")
    print(f"  [d{draw} {pair} {effort} a{attempt}] start {started}", flush=True)
    t0 = time.monotonic()
    killed = False
    p = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                         env=env, cwd=str(work), start_new_session=True)
    try:
        out, err = p.communicate(timeout=RUN_LIMIT)
        code = p.returncode
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGTERM)
        try:
            out, err = p.communicate(timeout=60)
        except subprocess.TimeoutExpired:
            os.killpg(p.pid, signal.SIGKILL)
            out, err = p.communicate()
        code, killed = "killed-45min", True
    secs = round(time.monotonic() - t0, 1)
    (work / "report.md").write_text(out or "")
    (work / "stderr.log").write_text(err or "")
    row = {"pair": pair, "model": MODEL, "effort": effort, "draw": draw, "attempt": attempt,
           "started_at": started, "wall_seconds": secs, "exit_code": code,
           "killed_at_limit": killed, "dir": str(work.relative_to(D))}
    rp = work / "report.json"
    calls = []
    if rp.exists():
        rep = json.loads(rp.read_text())
        prov = rep.get("provenance") or {}
        ledger = prov.get("ledger") or []
        answered = {}
        for r in ledger:
            block = r.get("answered_by") or {}
            if block.get("output"):
                answered.setdefault(r.get("role"), [])
                if block["output"] not in answered[r.get("role")]:
                    answered[r.get("role")].append(block["output"])
        calls = calls_of(work, ledger)
        row |= {"report": True,
                "claimcheck_commit": prov.get("claimcheck_commit"),
                "models": prov.get("models"),
                "answered_by": answered,
                "all_model_ids": sorted({m for c in calls for m in c["models"]}),
                "decoding": prov.get("decoding"),
                "calls_by_role": prov.get("calls_by_role"),
                "retrieval": (prov.get("retrieval") or {}).get("tool_use"),
                "retrieval_permitted": (prov.get("retrieval") or {}).get("permitted"),
                "num_turns": [c["num_turns"] for c in calls],
                "web_search_requests": sum(c["web_search_requests"] for c in calls),
                "merge_turns": [c["num_turns"] for c in calls if c["role"] == "merge"],
                "merge_web_search_requests": sum(c["web_search_requests"] for c in calls
                                                 if c["role"] == "merge"),
                "calls": calls,
                "errors": (prov.get("counts") or {}).get("errors")}
    else:
        row["report"] = False
        if (work / "calls").exists():
            calls = calls_of(work, [])
            row["calls"] = calls
    row["usage"] = usage_sum(calls)
    row["failed"] = (not row["report"]) or code not in (0, 1, 3)
    row["usage_limit"] = bool(row["failed"] and LIMIT.search(err or ""))
    if row["failed"]:
        row["stderr_tail"] = (err or "")[-600:]
    record(row)
    print(f"  [d{draw} {pair} {effort} a{attempt}] exit={code} {secs}s "
          f"report={row['report']} ids={row.get('all_model_ids')} "
          f"retrieval={(row.get('retrieval') or {}).get('retrieval')} "
          f"searches={row.get('web_search_requests')} "
          f"cost_usd={row['usage']['total_cost_usd']} "
          f"out_tok={row['usage']['output_tokens']}", flush=True)
    return row


def main() -> int:
    RUNS.mkdir(exist_ok=True)
    pin = (D / "COMMIT").read_text().strip()
    env = route_env()
    cmd = env["LLOSSLESS_COMMAND"]
    got = {role: config.effort_of(cmd, role, {"merge": "max"}) for role in config.ROLES}
    if got != {"merge": "max", "decompose": "low", "verify": "low"}:
        raise SystemExit(f"ABORT: efforts {got}")
    print(f"route: {cmd}", flush=True)
    for draw, cells in DRAWS.items():
        print(f"=== draw {draw}", flush=True)
        for pair, effort in cells:
            prior = [r for r in load() if (r["pair"], r["effort"], r["draw"])
                     == (pair, effort, draw) and not r.get("usage_limit")]
            if any(not r["failed"] for r in prior) or len(prior) >= 2:
                continue
            for attempt in range(len(prior) + 1, 3):
                row = run(pair, effort, draw, attempt, env)
                commit = str(row.get("claimcheck_commit") or "")
                if row["report"] and (commit.endswith("-dirty") or not pin.startswith(commit[:7])):
                    raise SystemExit(f"ABORT: report commit {commit} is not the pin {pin}")
                bad_ids = [i for i in row.get("all_model_ids") or [] if "opus" in i and i != "claude-opus-5-5"
                           and not i.startswith("claude-opus-5-5")]
                if bad_ids:
                    print(f"\nSTOP: an Opus id other than 5.5 answered: {bad_ids}", flush=True)
                    return 5
                if row["usage_limit"]:
                    print(f"\nUSAGE LIMIT at d{draw} {pair} {effort}; stopping.", flush=True)
                    return 4
                if row["killed_at_limit"]:
                    print(f"\nSTOP: d{draw} {pair} {effort} passed 45 min.", flush=True)
                    return 6
                if pair == "voyager" and effort == "max":
                    xh = [r["usage"]["total_cost_usd"] for r in load()
                          if r["pair"] == "voyager" and r["effort"] == "xhigh" and not r["failed"]]
                    if xh and row["usage"]["total_cost_usd"] > COST_FACTOR * statistics.median(xh):
                        print(f"\nSTOP: max cost {row['usage']['total_cost_usd']} > "
                              f"{COST_FACTOR}x xhigh median {statistics.median(xh)}", flush=True)
                        return 7
                if not row["failed"]:
                    break
    rows = load()
    print(f"\nGRID COMPLETE: {len(rows)} attempts, "
          f"{sum(1 for r in rows if not r['failed'])} succeeded, "
          f"{sum(r['wall_seconds'] for r in rows):.0f}s wall, "
          f"cost_usd {sum(r['usage']['total_cost_usd'] for r in rows):.2f}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
