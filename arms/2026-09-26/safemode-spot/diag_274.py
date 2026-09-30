#!/usr/bin/env python3
"""Amendment 2 diagnostic: voyager Sonnet medium sourced on CLI 2.1.274, without and with safe mode."""
import json, os, pathlib, sys
D = pathlib.Path(os.environ["BENCH_DIR"])
sys.path.insert(0, str(D))
import run_spot as R  # noqa: E402

R.RUNS = D / "diag" / "runs"
R.RESULTS = D / "diag" / "results.json"
pin = (D / "COMMIT").read_text().strip()
for name in ("274-nosafe", "274-safe"):
    R.WRAPPER = D / f"bin-{name}" / "claude"
    env = R.route_env("sonnet")
    print("route:", env["LLOSSLESS_COMMAND"], flush=True)
    row = R.run(f"B-sonnet-voyager-{name}", "B-diag", "sonnet", "handwritten", "voyager",
                R.B_ARGS, 1, env)
    c = str(row.get("claimcheck_commit") or "")
    assert row["report"] and not c.endswith("-dirty") and pin.startswith(c[:7]), c
    calls = R.RUNS / f"B-sonnet-voyager-{name}" / "a1" / "calls"
    if name.endswith("nosafe"):
        sent = [p.read_text().split("\n") for p in sorted(calls.glob("*.argv-sent"))]
        assert sent and all("--safe-mode" not in s and "--tools" not in s for s in sent)
    else:
        sent = [p.read_text().split("\n") for p in sorted(calls.glob("*.argv"))]
        assert sent and all("--safe-mode" in s for s in sent)
    print(f"{name}: argv checked on {len(sent)} calls", flush=True)
