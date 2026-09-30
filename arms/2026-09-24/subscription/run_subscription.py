#!/usr/bin/env python3
"""The subscription routes over tests/pairs at `high`, serially, from a pinned clone.

Run by bench.sh with BENCH_DIR set. Cells go to BENCH_DIR/cells/<pair>-high-<route>/,
one results row per cell to BENCH_DIR/results.json. See REGISTRATION.md.
"""
import json, os, pathlib, re, shutil, subprocess, sys, tempfile, time
from datetime import datetime, timezone

D = pathlib.Path(os.environ["BENCH_DIR"])
TREE = D / "tree"
PAIRS_ROOT = TREE / "tests" / "pairs"
RESULTS = D / "results.json"
CELLS = D / "cells"
sys.path.insert(0, str(TREE / "src"))

import claimcheck  # noqa: E402
if not claimcheck.__file__.startswith(str(TREE / "src") + "/"):
    raise SystemExit(f"ABORT: claimcheck resolves to {claimcheck.__file__}")
from claimcheck import config  # noqa: E402
from claimcheck.web import commands  # noqa: E402

# Cheapest first. claude-fable is not run (operator: not the most expensive model).
ROUTES = ("claude-haiku", "claude-sonnet", "claude-opus")
PAIRS = sorted(p.name for p in PAIRS_ROOT.iterdir() if (p / "ideal.md").is_file())
assert len(PAIRS) == 9, PAIRS
LEVEL = "high"

# The parent session's variables (CLAUDE_EFFORT among them) are not what a
# server's child process sees, and CLAIMCHECK_* from this shell are not the route's.
DROP = re.compile(r"^(CLAUDE|AI_AGENT|CLAIMCHECK_)")
BASE = {k: v for k, v in os.environ.items() if not DROP.match(k)}

LIMIT = re.compile(r"usage limit|limit reached|hit your limit|limit will reset|"
                   r"resets at|out of extra usage|rate limit", re.I)


def route_env(route_id: str) -> dict:
    """The environment the web UI gives this discovered route, from the route itself."""
    with tempfile.TemporaryDirectory() as tmp:
        book = commands.Commands(pathlib.Path(tmp) / "commands.json")
        book.enable(route_id)
        return book.get(route_id).environ()


def load():
    return json.loads(RESULTS.read_text()) if RESULTS.exists() else []


def record(row):
    data = load()
    data.append(row)
    RESULTS.write_text(json.dumps(data, indent=2))


def done():
    """Cells attempted once already. A usage-limit cell is the only one re-run."""
    return {(r["route"], r["pair"]) for r in load() if not r.get("usage_limit")}


def run(route_id: str, env_route: dict, pair: str) -> bool:
    work = CELLS / f"{pair}-{LEVEL}-{route_id}"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    for name in ("source_a.md", "source_b.md"):
        shutil.copy(PAIRS_ROOT / pair / name, work / name)
    env = {**BASE, **env_route, "PYTHONPATH": str(TREE / "src")}
    argv = [sys.executable, "-m", "claimcheck", "merge", "source_a.md", "source_b.md",
            "--base", "source_a.md", "--fidelity", LEVEL, "--no-cache",
            "--json", str(work / "report.json"), "-o", str(work / "merged.md")]
    started = datetime.now(timezone.utc).isoformat(timespec="seconds")
    print(f"  [{route_id} {pair}] start {started}", flush=True)
    t0 = time.monotonic()
    p = subprocess.run(argv, capture_output=True, text=True, env=env, cwd=str(work))
    secs = round(time.monotonic() - t0, 1)
    (work / "stderr.log").write_text(p.stderr or "")
    row = {"route": route_id, "model": env_route["CLAIMCHECK_MODEL"], "pair": pair,
           "fidelity": LEVEL, "exit_code": p.returncode, "wall_seconds": secs,
           "started_at": started}
    rp = work / "report.json"
    if rp.exists():
        rep = json.loads(rp.read_text())
        prov = rep.get("provenance") or {}
        row |= {"report": True,
                "claimcheck_commit": prov.get("claimcheck_commit"),
                "calls_by_role": prov.get("calls_by_role"),
                "decoding": prov.get("decoding"),
                "structured_output": prov.get("structured_output"),
                "errors": prov.get("errors")}
    else:
        row["report"] = False
    text = (p.stderr or "") + json.dumps(row.get("errors") or "")
    if p.returncode == 2 and LIMIT.search(text):
        row["usage_limit"] = True
        row["stderr_tail"] = (p.stderr or "")[-400:]
    record(row)
    print(f"  [{route_id} {pair}] exit={p.returncode} {secs}s "
          f"report={row['report']} commit={row.get('claimcheck_commit')}", flush=True)
    return not row.get("usage_limit")


def main() -> int:
    CELLS.mkdir(exist_ok=True)
    pin = (D / "COMMIT").read_text().strip()
    for route_id in ROUTES:
        env_route = route_env(route_id)
        # The shipped effort table, stated per role, is what the route applies.
        want = config.AUTO_EFFORT["claude"]
        got = {role: config.effort_of(env_route["CLAIMCHECK_COMMAND"], role)
               for role in config.ROLES}
        if got != want:
            raise SystemExit(f"ABORT: {route_id} effort {got} is not AUTO_EFFORT {want}")
        print(f"=== {route_id}: model {env_route['CLAIMCHECK_MODEL']}, "
              f"profile {env_route['CLAIMCHECK_PROFILE']}, effort {got}", flush=True)
        for pair in PAIRS:
            if (route_id, pair) in done():
                print(f"  [{route_id} {pair}] skip, attempted", flush=True)
                continue
            if not run(route_id, env_route, pair):
                print(f"\nUSAGE LIMIT on {route_id}/{pair}; stopping. Re-run after reset.",
                      flush=True)
                return 4
            last = load()[-1]
            commit = str(last.get("claimcheck_commit") or "")
            if last["report"] and not pin.startswith(commit.replace("-dirty", "")[:12]) \
                    or commit.endswith("-dirty"):
                raise SystemExit(f"ABORT: report commit {commit} is not the pin {pin}")
    rows = load()
    print(f"\nSUBSCRIPTION RUN COMPLETE: {len(rows)} rows, "
          f"{sum(1 for r in rows if r['report'])} with a report, "
          f"{sum(r['wall_seconds'] for r in rows):.0f}s wall")
    return 0


if __name__ == "__main__":
    sys.exit(main())
