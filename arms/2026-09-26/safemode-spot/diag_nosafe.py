#!/usr/bin/env python3
"""Amendment 1 diagnostic: one voyager Sonnet medium sourced run with safe mode stripped."""
import json, os, pathlib, sys
D = pathlib.Path(os.environ["BENCH_DIR"])
sys.path.insert(0, str(D))
import run_spot as R  # noqa: E402

R.WRAPPER = D / "bin-nosafe" / "claude"
R.RUNS = D / "diag" / "runs"
R.RESULTS = D / "diag" / "results.json"
R.RUNS.mkdir(parents=True, exist_ok=True)
env = R.route_env("sonnet")
print("route:", env["LLOSSLESS_COMMAND"], flush=True)
row = R.run("B-sonnet-voyager-nosafe", "B-diag", "sonnet", "handwritten", "voyager", R.B_ARGS, 1, env)
pin = (D / "COMMIT").read_text().strip()
c = str(row.get("claimcheck_commit") or "")
assert row["report"] and not c.endswith("-dirty") and pin.startswith(c[:7]), c
sent = [p.read_text().split("\n") for p in sorted((R.RUNS / "B-sonnet-voyager-nosafe" / "a1" / "calls").glob("*.argv-sent"))]
assert sent and all("--safe-mode" not in s and "--tools" not in s for s in sent), "strip failed"
print("argv-sent checked: no --safe-mode, no --tools on", len(sent), "calls", flush=True)
