#!/usr/bin/env python3
"""Safe-mode spot check, 2026-09-26: 597's and 609's subscription cells re-run under 610.

Adapted from 597's run_subscription.py (part A) and 609's run_grid.py via
opus-max's run_max.py (part B, envelope capture). Run by bench.sh with BENCH_DIR
set. See REGISTRATION.md. Each run goes to BENCH_DIR/runs/<cell>/a<n>/; one row
per attempt is appended to BENCH_DIR/results.json. Resumable. Serial.
"""
import json, os, pathlib, re, shlex, shutil, signal, subprocess, sys, tempfile, time
from datetime import datetime, timezone

D = pathlib.Path(os.environ["BENCH_DIR"])
TREE = D / "tree"
RESULTS = D / "results.json"
RUNS = D / "runs"
WRAPPER = D / "bin" / "claude"
CLI = pathlib.Path("<home>/.local/share/claude/versions/2.1.283")
sys.path.insert(0, str(TREE / "src"))

import llossless  # noqa: E402
if not llossless.__file__.startswith(str(TREE / "src") + "/"):
    raise SystemExit(f"ABORT: llossless resolves to {llossless.__file__}")
from llossless import config  # noqa: E402
from llossless.web import commands  # noqa: E402

EXPECT = {"sonnet": "claude-sonnet-5", "haiku": "claude-haiku-4-5-20251001"}
SIDE = "claude-haiku-4-5-20251001"  # the CLI's own side calls, on every route
USD_STOP = 20.0
RUN_LIMIT = 60 * 60

# (cell id, part, model, pair root, pair, fidelity, extra argv)
A_ARGS = ["--fidelity", "high", "--verify-depth", "full", "--no-cache"]
B_ARGS = ["--fidelity", "sourced", "--verify-depth", "full", "--effort", "merge=medium",
          "--timeout", "1800", "--no-cache"]
PLAN = [(f"A-{m}-{p}", "A", m, "pairs", p, A_ARGS)
        for m in ("sonnet", "haiku") for p in ("rate_limits", "trace_names", "badge_access")]
PLAN += [(f"B-sonnet-voyager-d{k}", "B", "sonnet", "handwritten", "voyager", B_ARGS)
         for k in (1, 2)]

DROP = re.compile(r"^(CLAUDE|AI_AGENT|LLOSSLESS_|CLAIMCHECK_)")
BASE = {k: v for k, v in os.environ.items() if not DROP.match(k)}
LIMIT = re.compile(r"usage limit|limit reached|hit your limit|limit will reset|"
                   r"resets at|out of extra usage|rate limit", re.I)


def route_env(model: str) -> dict:
    """The web UI's environment for the discovered route, program swapped for the wrapper."""
    rid = f"claude-{model}"
    with tempfile.TemporaryDirectory() as tmp:
        book = commands.Commands(pathlib.Path(tmp) / "commands.json")
        book.enable(rid)
        env = dict(book.get(rid).environ())
    argv = env["LLOSSLESS_COMMAND"].split()
    if os.path.basename(argv[0]) != "claude" or argv[-2:] != ["--model", model]:
        raise SystemExit(f"ABORT: unexpected route {env['LLOSSLESS_COMMAND']}")
    env["LLOSSLESS_COMMAND"] = " ".join([str(WRAPPER), *argv[1:]])
    got = {r: config.effort_of(env["LLOSSLESS_COMMAND"], r) for r in config.ROLES}
    if got != {"merge": "medium", "decompose": "low", "verify": "low"}:
        raise SystemExit(f"ABORT: {rid} efforts {got}")
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
        argv = path.with_suffix(".argv").read_text().split("\n")
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
    for c in calls:
        for k in tot:
            tot[k] += c.get(k) or 0
    tot["total_cost_usd"] = round(tot["total_cost_usd"], 4)
    return tot


def probe(model: str, env_route: dict) -> dict:
    """One-word call on the route's argv shape plus isolation; the id that answered."""
    work = D / "probe" / model
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    cmd = config.command_with_isolation(env_route["LLOSSLESS_COMMAND"])
    argv = shlex.split(cmd)
    env = {**BASE, "BENCH_CALLS": str(work / "calls")}
    p = subprocess.run(argv, input="Reply with the single word: ok", capture_output=True,
                       text=True, env=env, cwd=str(work), timeout=300)
    calls = calls_of(work, [])
    ids = sorted({m for c in calls for m in c["models"]})
    res = {"model": model, "argv": argv[1:], "exit_code": p.returncode, "ids": ids,
           "usage": usage_sum(calls)}
    (work / "probe.json").write_text(json.dumps(res, indent=1))
    return res


def run(cell, part, model, root, pair, extra, attempt, env_route) -> dict:
    work = RUNS / cell / f"a{attempt}"
    if work.exists():
        shutil.rmtree(work)
    (work / "tmp").mkdir(parents=True)
    src = TREE / "tests" / root / pair
    names = sorted(p.name for p in src.glob("source_*.md"))
    for name in names:
        shutil.copy(src / name, work / name)
    env = {**BASE, **env_route, "PYTHONPATH": str(TREE / "src"),
           "BENCH_CALLS": str(work / "calls"), "TMPDIR": str(work / "tmp")}
    argv = [sys.executable, "-m", "llossless", "merge", *names, "--base", "source_a.md",
            *extra, "--json", str(work / "report.json"), "-o", str(work / "merged.md")]
    (work / "argv.json").write_text(json.dumps(argv[1:], indent=1))
    started = datetime.now(timezone.utc).isoformat(timespec="seconds")
    print(f"  [{cell} a{attempt}] start {started}", flush=True)
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
        code, killed = "killed-60min", True
    secs = round(time.monotonic() - t0, 1)
    (work / "report.md").write_text(out or "")
    (work / "stderr.log").write_text(err or "")
    row = {"cell": cell, "part": part, "pair": pair, "model": model, "attempt": attempt,
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
                "isolation": prov.get("isolation"),
                "answered_by": answered,
                "all_model_ids": sorted({m for c in calls for m in c["models"]}),
                "decoding": prov.get("decoding"),
                "calls_by_role": prov.get("calls_by_role"),
                "structured_output": prov.get("structured_output"),
                "retrieval": (prov.get("retrieval") or {}).get("tool_use"),
                "web_search_requests": sum(c["web_search_requests"] for c in calls),
                "subagents_spawned": sum(c["subagents_spawned"] or 0 for c in calls),
                "calls": calls,
                "errors": (prov.get("counts") or {}).get("errors")}
    else:
        row["report"] = False
        if (work / "calls").exists():
            calls = calls_of(work, [])
            row["calls"] = calls
            row["all_model_ids"] = sorted({m for c in calls for m in c["models"]})
    row["usage"] = usage_sum(calls)
    row["failed"] = (not row["report"]) or code not in (0, 1, 3)
    row["usage_limit"] = bool(row["failed"] and LIMIT.search(err or ""))
    if row["failed"]:
        row["stderr_tail"] = (err or "")[-600:]
    record(row)
    print(f"  [{cell} a{attempt}] exit={code} {secs}s report={row['report']} "
          f"ids={row.get('all_model_ids')} cost_usd={row['usage']['total_cost_usd']} "
          f"out_tok={row['usage']['output_tokens']}", flush=True)
    return row


def main() -> int:
    RUNS.mkdir(exist_ok=True)
    pin = (D / "COMMIT").read_text().strip()
    envs = {m: route_env(m) for m in ("sonnet", "haiku")}
    for m, env in envs.items():
        print(f"route {m}: {config.command_with_isolation(env['LLOSSLESS_COMMAND'])}", flush=True)
    if not (D / "probe" / "done").exists():
        for m in ("sonnet", "haiku"):
            res = probe(m, envs[m])
            print(f"probe {m}: exit={res['exit_code']} ids={res['ids']} "
                  f"cost={res['usage']['total_cost_usd']}", flush=True)
            if EXPECT[m] not in res["ids"] or set(res["ids"]) - {EXPECT[m], SIDE}:
                print(f"STOP: {m} resolved to {res['ids']}", flush=True)
                return 5
        (D / "probe" / "done").write_text("ok\n")
    for cell, part, model, root, pair, extra in PLAN:
        prior = [r for r in load() if r["cell"] == cell and not r.get("usage_limit")]
        if any(not r["failed"] for r in prior) or len(prior) >= 2:
            continue
        for attempt in range(len(prior) + 1, 3):
            if not CLI.exists():
                raise SystemExit(f"ABORT: {CLI} is gone")
            row = run(cell, part, model, root, pair, extra, attempt, envs[model])
            commit = str(row.get("claimcheck_commit") or "")
            if row["report"] and (commit.endswith("-dirty") or not pin.startswith(commit[:7])):
                raise SystemExit(f"ABORT: report commit {commit} is not the pin {pin}")
            ids = set(row.get("all_model_ids") or [])
            if ids - {EXPECT[model], SIDE}:
                print(f"\nSTOP: {model} run answered by {sorted(ids)}", flush=True)
                return 5
            spent = sum(r["usage"]["total_cost_usd"] for r in load())
            spent += sum(json.loads((D / "probe" / m / "probe.json").read_text())
                         ["usage"]["total_cost_usd"] for m in ("sonnet", "haiku"))
            print(f"  spent so far ${spent:.2f}", flush=True)
            if row["usage_limit"]:
                print(f"\nUSAGE LIMIT at {cell}; stopping.", flush=True)
                return 4
            if row["killed_at_limit"]:
                print(f"\nSTOP: {cell} passed 60 min.", flush=True)
                return 6
            if spent > USD_STOP:
                print(f"\nSTOP: spent ${spent:.2f} > ${USD_STOP}", flush=True)
                return 7
            if not row["failed"]:
                break
    rows = load()
    print(f"\nSPOT CHECK COMPLETE: {len(rows)} attempts, "
          f"{sum(1 for r in rows if not r['failed'])} succeeded, "
          f"{sum(r['wall_seconds'] for r in rows):.0f}s wall, "
          f"cost_usd {sum(r['usage']['total_cost_usd'] for r in rows):.2f}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
