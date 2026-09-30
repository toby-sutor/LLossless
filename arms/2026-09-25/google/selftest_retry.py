#!/usr/bin/env python3
"""Offline: ledger_cli.py's pacing and retry policy, through its real wrapper.

A loopback endpoint (tests/fake_endpoint.py) answers the script's own
requests; `cli.main` is replaced by a function that sends them through
`transport.post_json`, so what is exercised is the wrapper ledger_cli installs.
Backoff is scaled by 1/1000 (BENCH_BACKOFF_SCALE) so the test runs in seconds;
the waits it asserts are read back unscaled from stderr.

  1. 503, 503, 200: two retries, each waiting at least 60 s, the second longer.
  2. 429 naming retryDelay 7s: the wait is at least 30 s, not 7.
  3. a 429 on the per-day quota: exit 8, no retry.
  4. 503 six times: five retries, then the request fails.
  5. a billing error: exit 9 and STOP-BILLING.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = Path(os.environ.get("BENCH_REPO", "<home>/Documents/Dev/vibe-coding/claimcheck"))
TREE = Path(os.environ.get("BENCH_TREE", str(HERE.parent / "tree")))

CHILD = r'''
import json, sys
sys.argv = ["ledger_cli.py", "--state", sys.argv[1], "--model", "m", "--cell", "t",
            "--docs", sys.argv[2], "--", "x"]
import ledger_cli
from claimcheck import transport
def fake_main(argv):
    url = ledger_cli.HOST + "chat/completions"
    r = transport.post_json(url, {"model": "m", "messages": [{"role": "user", "content": "hi"}]},
                            api_key=None, timeout=10, ca_bundle=None, host="loopback", model="m")
    print("ANSWERED", r.attempts)
    return 0
ledger_cli.cli.main = fake_main
sys.exit(ledger_cli.main())
'''


def err(code, message, details=()):
    return json.dumps([{"error": {"code": code, "message": message, "status": "X",
                                  "details": list(details)}}])


OK = json.dumps({"model": "m", "choices": [{"message": {"content": "hello"}}],
                 "usage": {"prompt_tokens": 3, "completion_tokens": 1, "total_tokens": 4}})
DAY = {"@type": "<redacted>/google.rpc.QuotaFailure", "violations": [
    {"quotaId": "GenerateRequestsPerDayPerProjectPerModel-FreeTier", "quotaValue": "20"}]}
MINUTE = {"@type": "<redacted>/google.rpc.QuotaFailure", "violations": [
    {"quotaId": "GenerateRequestsPerMinutePerProjectPerModel-FreeTier", "quotaValue": "5"}]}
DELAY = {"@type": "<redacted>/google.rpc.RetryInfo", "retryDelay": "7s"}
QUOTA = "You exceeded your current quota, please check your plan and billing details."


def run(script):
    sys.path.insert(0, str(REPO / "tests"))
    from fake_endpoint import FakeEndpoint
    with tempfile.TemporaryDirectory() as tmp, FakeEndpoint(lambda _b, n: script[min(n, len(script)) - 1]) as base:
        doc = REPO / "tests" / "fixtures" / "dedup" / "source_a.md"
        env = {**os.environ, "BENCH_TREE": str(TREE), "BENCH_HOST": base + "/",
               "BENCH_BACKOFF_SCALE": "0.001", "BENCH_INTERVAL": "0",
               "PYTHONPATH": f"{HERE}:{TREE / 'src'}"}
        p = subprocess.run([sys.executable, "-c", CHILD, str(Path(tmp) / "l.json"),
                            str(TREE / "tests" / "fixtures" / "dedup" / "source_a.md")],
                           capture_output=True, text=True, env=env, cwd=tmp)
        waits = [float(w) for w in re.findall(r"waiting (\d+)s", p.stderr)]
        state = json.loads((Path(tmp) / "l.json").read_text()) if (Path(tmp) / "l.json").exists() else {}
        stopped = (Path(tmp) / "STOP-BILLING").exists()
        return p.returncode, p.stdout, p.stderr, waits, state, stopped, doc


def main() -> int:
    failures = []

    def check(ok, msg):
        if not ok:
            failures.append(msg)

    rc, out, errtext, waits, state, _, _ = run([(503, err(503, "high demand")),
                                                (503, err(503, "high demand")), (200, OK)])
    check(rc == 0 and "ANSWERED 3" in out, f"1: {rc} {out} {errtext[-300:]}")
    check(len(waits) == 2 and all(w >= 60 for w in waits) and waits[1] > waits[0],
          f"1: 503 waits {waits}")
    check(len(state.get("attempts", [])) == 3, "1: every attempt recorded")

    rc, out, errtext, waits, _, _, _ = run([(429, err(429, QUOTA, [MINUTE, DELAY])), (200, OK)])
    check(rc == 0 and len(waits) == 1 and waits[0] >= 30, f"2: 429 wait {waits} rc {rc}")

    rc, out, errtext, waits, _, _, _ = run([(429, err(429, QUOTA, [DAY, DELAY])), (200, OK)])
    check(rc == 8 and not waits and "QUOTA-DAY" in errtext, f"3: per-day 429: rc {rc} {waits}")

    rc, out, errtext, waits, state, _, _ = run([(503, err(503, "high demand"))] * 7)
    check(rc != 0 and len(waits) == 5 and len(state.get("attempts", [])) == 6,
          f"4: retries capped at 5: rc {rc} waits {waits}")
    check(all(w <= 600 for w in waits), f"4: a wait above the ceiling: {waits}")

    rc, out, errtext, waits, _, stopped, _ = run([(403, err(403, "Billing account disabled"))])
    check(rc == 9 and stopped, f"5: billing signal: rc {rc} stopped {stopped}")

    for f in failures:
        print("FAIL", f)
    print("selftest_retry:", "FAIL" if failures else "5 cases pass")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
