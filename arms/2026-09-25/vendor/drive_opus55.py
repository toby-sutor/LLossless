#!/usr/bin/env python3
"""Arm B as amended by DECISIONS 618: API claude-opus-5-5 on the nine pairs, K = 1.

A probe of tests/fixtures/dedup, then badge_access as the sizing cell, then the
other eight pairs cheapest first by the 2026-09-18 Opus 5 cost, each through
run_api.py's per-cell gate under what remains of the Anthropic cap.
"""
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ORDER = ["badge_access", "payroll_cutoff", "library_holds", "trace_names", "bike_docks",
         "loading_dock", "freezer_alarm", "index_429", "rate_limits"]  # 2026-09-18 Opus 5 cost


def bench(*args):
    print(f"--- bench.sh {' '.join(args)}", flush=True)
    return subprocess.run([str(HERE / "bench.sh"), *args], env=dict(os.environ)).returncode


def main():
    if bench("api", "probe", "claude-opus-5-5"):
        print("STOP: the Opus 5.5 probe did not pass")
        return 1
    if bench("api", "cells", "claude-opus-5-5", "badge_access:1"):
        print("STOP: the sizing cell did not pass")
        return 1
    bench("api", "cells", "claude-opus-5-5", ",".join(f"{p}:1" for p in ORDER[1:]))
    print("ARM B (OPUS 5.5) DONE", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
