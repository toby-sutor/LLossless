#!/usr/bin/env python3
"""Measure the endpoint before planning anything against it.

Every schedule is derived from an earlier latency distribution, which was measured
on the local box with the pacing gap removed
arithmetically:

    mean 25.8 s   p95 63.6 s   max 276.1 s   tail ratio max/mean 10.7x
    (n=264, p95 by nearest-rank on the sorted sample)

That is a description of one machine. A later run records against another, so until
the same numbers exist for it, the schedule predicts nothing. This script produces them.

**Ten merge calls, one per fixture**, over the ten largest source pairs in the
suite. One call each rather than one fixture ten times: the spread of document
sizes is the thing a schedule is sensitive to, and repeating one document would
measure that document.

Method matched to the baseline so the two are comparable: same model, same
prompt, same `max_tokens` sizing (`merge.budget_tokens`), p95 by nearest-rank
on the sorted sample. **With n=10 the nearest-rank p95 is the maximum** — it is
reported anyway, and named, because a p95 that is definitionally the max is a
statement about the sample size rather than about the tail.

The endpoint comes from `LLOSSLESS_BASE_URL` and is never written down here or
in the report. Cassettes go to a gitignored exploratory corpus under `tests/eval/`,
since the schema for it does not exist yet, so anything recorded now is orphaned by
design and must not touch a corpus.

    LLOSSLESS_BASE_URL=... python3 tests/calibrate_endpoint.py [--calls 10]
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

from llossless import config, merge  # noqa: E402
from llossless.client import Client  # noqa: E402

# Every fixture is a pair, so the harness reads the two canonical names.
# From `merge.source_names` rather than written out: the pass names its own
# documents and this is a reader of that naming, not a second opinion on it.
SOURCES = merge.source_names(2)

FIXTURES_DIR = ROOT / "tests" / "fixtures"
CASSETTES = ROOT / "tests" / "eval" / "m7-calibration"


def load_sources(fixture: str) -> dict[str, str]:
    return {
        name: (FIXTURES_DIR / fixture / name).read_text(encoding="utf-8")
        for name in SOURCES
    }


def fixtures() -> list[str]:
    """Every fixture directory with two sources, largest pair first."""
    found = []
    for path in sorted(FIXTURES_DIR.iterdir()):
        if all((path / name).exists() for name in SOURCES):
            sources = load_sources(path.name)
            found.append((sum(len(s) for s in sources.values()), path.name))
    return [name for _size, name in sorted(found, reverse=True)]


def nearest_rank(sorted_values: list[float], percentile: float) -> float:
    """The baseline's own method, so the two numbers mean the same thing."""
    rank = -(-int(percentile * len(sorted_values) * 100) // 100)  # ceil(p*n)
    return sorted_values[max(1, rank) - 1]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--calls", type=int, default=10)
    parser.add_argument("--thinking", action="store_true", help="merge with thinking on")
    args = parser.parse_args(argv)

    settings = config.from_env()
    # `use_cache=False` is load-bearing, not tidiness. The first run of this
    # script reported `conflict_surfaced` at 0.00 s and 0 completion tokens: a
    # warm entry from `.llossless-cache/` served in place of a call. A cache
    # hit is a valid answer and a worthless measurement, and it pulled the mean
    # down without appearing as an error.
    settings = config.replace(
        settings, record_dir=CASSETTES, min_interval=0.0, use_cache=False
    )
    if settings.is_local:
        print("  refusing: LLOSSLESS_BASE_URL points at a local endpoint.")
        print("  This measures the remote machine a recording will run against.")
        return 2

    CASSETTES.mkdir(parents=True, exist_ok=True)
    client = Client(settings)

    chosen = fixtures()[: args.calls]
    print(f"  {len(chosen)} merge call(s), {settings.where} endpoint {settings.endpoint_id}")
    print(f"  thinking {'on' if args.thinking else 'off'}, model {settings.model_for('merge')}\n")

    records: list[dict] = []
    for n, fixture in enumerate(chosen, 1):
        sources = load_sources(fixture)
        budget = merge.budget_tokens(sources, settings.fidelity)
        before = client.usage.completion_tokens
        started = time.monotonic()
        try:
            document = merge.merge_documents(
                client, sources, max_tokens=budget, thinking=args.thinking
            ).document
            error = None
        except Exception as exc:  # noqa: BLE001 -- an error rate is one of the four figures
            document, error = "", f"{type(exc).__name__}: {exc}"
        elapsed = time.monotonic() - started
        tokens = client.usage.completion_tokens - before
        records.append(
            {
                "fixture": fixture,
                "seconds": round(elapsed, 2),
                "max_tokens": budget,
                "completion_tokens": tokens,
                "merged_chars": len(document),
                "error": error,
            }
        )
        state = error or f"{len(document)} chars, {tokens} completion tokens"
        print(f"  {n:2d}/{len(chosen)}  {fixture:<22} {elapsed:7.2f}s  {state}")
        if error is None and tokens == 0:
            print("      ^ 0 completion tokens: not a live call, so not a measurement")

    if client.usage.cache_hits:
        print(f"\n  ABORT: {client.usage.cache_hits} call(s) served from cache.")
        print("  A calibration over cached answers measures the disk, not the endpoint.")
        return 2

    ok = [r["seconds"] for r in records if r["error"] is None]
    print(f"\n  {len(ok)}/{len(records)} call(s) answered\n")
    if ok:
        ordered = sorted(ok)
        mean = statistics.fmean(ordered)
        p95 = nearest_rank(ordered, 0.95)
        print(f"    mean {mean:.1f} s   p95 {p95:.1f} s   max {max(ordered):.1f} s   "
              f"tail ratio max/mean {max(ordered) / mean:.1f}x")
        print(f"    (n={len(ordered)}, p95 by nearest-rank on the sorted sample)")
        if p95 == max(ordered):
            print("    p95 == max at this sample size; it describes n, not the tail.")
        print(f"\n    min {min(ordered):.1f} s   median {statistics.median(ordered):.1f} s")
    print(f"    error rate {len(records) - len(ok)}/{len(records)}")

    out = CASSETTES / "calibration.json"
    out.write_text(json.dumps({"calls": records}, indent=2) + "\n", encoding="utf-8")
    print(f"\n  per-call figures: {out}")
    return 0 if len(ok) == len(records) else 1


if __name__ == "__main__":
    sys.exit(main())
