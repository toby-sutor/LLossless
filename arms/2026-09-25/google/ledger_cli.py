#!/usr/bin/env python3
"""claimcheck's own CLI, in process, every chat request charged to a persisted
spend.Ledger at Google's $0.00 cap, free tier only.

    ledger_cli.py --state LEDGER.json --model gemini-3.8-flash \
                  --cell LABEL --docs source_a.md source_b.md -- merge ...

The vendor run's ledger_cli.py (arms/2026-09-25/vendor/), adapted for the free
tier. Everything after `--` is handed to `claimcheck.cli.main` unchanged.

What differs, and why:

- **The ledger SKU is `google-free/<model>`, priced at zero here and nowhere
  else.** The shipped table's `google/<model>` rows are the paid tier's rates,
  and the $0.00 cap refuses them before any call. The free row is registered
  in this process only, from the pricing page's Free Tier column. The cap is
  $0.00 and is never raised.
- **Retries are the harness's, not the transport's**, so that every attempt is
  recorded with its status and body. `transport.MAX_ATTEMPTS` is set to 1 for
  this process; this wrapper retries at most 5 times per request, with
  exponential backoff and jitter: a 429 waits what Google names
  (`Retry-After`, `RetryInfo.retryDelay`) and at least 30 s, a 503 or other
  5xx from 60 s. A 429 on the per-day quota stops the cell and the arm. Every
  attempt is one ledger row at $0.00.
- **A billing signal stops everything.** Any error body that speaks of billing,
  prepayment or credit, other than the standard text of a free-tier quota 429,
  writes STOP-BILLING beside the ledger and exits 9.
- **Pacing** is the run's interval from REGISTRATION.md, in the ledger. The
  time spent pacing and backing off is recorded per cell so the figures can
  state the calls' own time.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
import time
from pathlib import Path

TREE = Path(os.environ["BENCH_TREE"]).resolve()
sys.path.insert(0, str(TREE / "tests"))
sys.path.insert(0, str(TREE / "src"))

import claimcheck  # noqa: E402

if not claimcheck.__file__.startswith(str(TREE / "src") + os.sep):
    raise SystemExit(f"ABORT: claimcheck resolves to {claimcheck.__file__}")

import source_guard  # noqa: E402
import spend  # noqa: E402
from claimcheck import cli, transport  # noqa: E402

HOST = os.environ.get("BENCH_HOST", "https://generativelanguage.googleapis.com/v1beta/openai/")
# Only the offline self-test (selftest_retry.py) sets these two.
SCALE = float(os.environ.get("BENCH_BACKOFF_SCALE", "1"))
# The free tier's per-minute limit is not on the rate-limit page (it points to
# AI Studio) and no 429 on this key has named one: every 429 seen named the
# per-day quota. So the interval is a stated policy, 20 s (3 requests a minute),
# 1.5x the minimum interval of the strictest free-tier limit this key could
# plausibly have, 5 requests a minute (12 s). Amendment of 2026-09-25, 20:30 UTC.
INTERVAL = float(os.environ.get("BENCH_INTERVAL", "20"))
CAPS = spend.Caps(spend={"google": 0.00}, calls=3000, tokens=60_000_000,
                  interval={"google": INTERVAL})
ALLOWANCE = 65_536          # the models' own output limit, GET /v1beta/models
FREE_SOURCE = ("https://ai.google.dev/gemini-api/docs/pricing, Free Tier column, "
               "\"Free of charge\" for input and output (read 2026-09-25)")
# One attempt and at most 5 retries per request, then the request fails and
# the tool's own handling takes over. Backoff is exponential with jitter: a
# 429 waits what Google names (`Retry-After`, or `RetryInfo.retryDelay`) and
# never less than 30 s, doubling from 30 s when it names nothing; a 503 is
# Google overloaded, not this caller, and waits from 60 s. Capped at 600 s.
MAX_TRIES = int(os.environ.get("BENCH_MAX_TRIES", "6"))
FLOOR_429, FLOOR_5XX, CEILING = 30.0, 60.0, 600.0
BILLING = re.compile(r"billing|prepa(y|id)|credit|payment|charge", re.I)
FREE_QUOTA_TEXT = "You exceeded your current quota"


class QuotaExhausted(SystemExit):
    pass


def load_state(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"rows": [], "refused": [], "attempts": []}


def save_state(path: Path, state: dict) -> None:
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=1), encoding="utf-8")
    os.replace(tmp, path)


def error_detail(body: str) -> dict:
    """Google's compat endpoint wraps its error object in a JSON list."""
    try:
        data = json.loads(body)
    except ValueError:
        return {"raw": body[:600]}
    if isinstance(data, list) and data:
        data = data[0]
    err = data.get("error", {}) if isinstance(data, dict) else {}
    out = {"status_text": err.get("status"), "message": str(err.get("message", ""))[:800],
           "quota_ids": [], "quota_values": [], "retry_delay": None}
    for d in err.get("details") or []:
        for v in d.get("violations") or []:
            out["quota_ids"].append(v.get("quotaId"))
            out["quota_values"].append(v.get("quotaValue"))
        if d.get("retryDelay"):
            out["retry_delay"] = d["retryDelay"]
    return out


def billing_signal(status: int, detail: dict) -> bool:
    text = str(detail.get("message", "")) + " " + str(detail.get("raw", ""))
    if not BILLING.search(text):
        return False
    # Google's standard quota 429 says "check your plan and billing details"
    # and names the quota it hit. When every quota named is a free-tier one,
    # that is the free tier's rate limit, not billing.
    if status == 429 and FREE_QUOTA_TEXT in text and detail.get("quota_ids") and \
            all("FreeTier" in str(q) or "free_tier" in str(q) for q in detail["quota_ids"]):
        return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", required=True, type=Path)
    parser.add_argument("--model", required=True)
    parser.add_argument("--cell", required=True)
    parser.add_argument("--docs", nargs="+", required=True, type=Path)
    parser.add_argument("rest", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    argv = args.rest[1:] if args.rest[:1] == ["--"] else args.rest
    model = args.model
    sku = f"probe/google-free/{model}"
    spend.PRICES[sku] = spend.Price(input=0.0, output=0.0, source=FREE_SOURCE,
                                    read_on="2026-09-25")
    stop_file = args.state.parent / "STOP-BILLING"
    if stop_file.exists():
        raise SystemExit(f"ABORT: {stop_file} exists")

    state = load_state(args.state)
    state.setdefault("attempts", [])
    state.setdefault("waits", {})
    ledger = spend.Ledger(CAPS)
    for row in state["rows"]:
        ledger.spent.calls += 1
        ledger.spent.input_tokens += row["input_tokens"]
        ledger.spent.output_tokens += row["output_tokens"]
        ledger.spent.dollars["google"] = ledger.spent.dollars.get("google", 0.0) + row["dollars"]
    ledger.rows = list(state["rows"])
    documents = [p.read_text(encoding="utf-8") for p in args.docs]
    source_guard.approve(documents)

    real = transport.post_json
    transport.MAX_ATTEMPTS = 1
    # The transport reads `Retry-After` and, with one attempt, never waits on
    # it; the value is kept here so the harness can.
    told = {"retry_after": None}
    real_retry_after = transport._retry_after

    def retry_after(headers):
        told["retry_after"] = real_retry_after(headers)
        return told["retry_after"]
    transport._retry_after = retry_after
    waited = {"pace": 0.0, "backoff": 0.0}
    real_pace = ledger._pace

    def pace(vendor):
        w = real_pace(vendor)
        waited["pace"] += w
        return w
    ledger._pace = pace

    def save() -> None:
        state["rows"] = ledger.rows
        state["waits"][args.cell] = {k: round(v, 1) for k, v in waited.items()}
        save_state(args.state, state)

    def attempt(url, payload, kwargs, n):
        chars = len(json.dumps(payload.get("messages", [])))
        extra = {"cell": args.cell, "path": url[len(HOST) - 1:], "try": n,
                 "input_estimate": chars // 3 + 1}
        rec = {"cell": args.cell, "try": n,
               "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
        result = (None, None, {})
        with ledger.call("google", sku, input_estimate=chars // 3 + 1,
                         output_allowance=ALLOWANCE, documents=documents) as charge:
            try:
                response = real(url, payload, **kwargs)
            except transport.HTTPStatusError as exc:
                detail = error_detail(exc.body)
                rec.update(status=exc.status, **detail)
                extra["status"] = exc.status
                charge(input_tokens=0, output_tokens=0)
                result = (None, exc, detail)
            except Exception as exc:  # noqa: BLE001 - timeout, cut stream, empty body
                rec.update(status=None, error=type(exc).__name__, message=str(exc)[:300])
                extra["failed"] = type(exc).__name__
                charge(input_tokens=0, output_tokens=0)
                result = (None, exc, {})
            else:
                usage, served = {}, None
                try:
                    envelope = json.loads(response.body)
                    usage = envelope.get("usage") or {}
                    served = envelope.get("model")
                except (ValueError, AttributeError):
                    pass
                cached = (usage.get("prompt_tokens_details") or {}).get("cached_tokens") or 0
                charge(input_tokens=usage.get("prompt_tokens"),
                       output_tokens=usage.get("completion_tokens"), cached_tokens=cached)
                details = usage.get("completion_tokens_details") or {}
                extra.update(status=200, served_model=served, latency_ms=response.latency_ms,
                             prompt_tokens=usage.get("prompt_tokens"),
                             completion_tokens=usage.get("completion_tokens"),
                             total_tokens=usage.get("total_tokens"),
                             cached_tokens=cached,
                             reasoning_tokens=details.get("reasoning_tokens"),
                             usage_keys=sorted(usage))
                rec.update(status=200, latency_ms=response.latency_ms)
                result = (response, None, {})
        ledger.rows[-1].update(extra)
        state["attempts"].append(rec)
        save()
        return result

    def charged(url, payload, **kwargs):
        if not url.startswith(HOST):
            raise SystemExit(f"ledger_cli: refusing a request outside {HOST}")
        if payload.get("model") != model:
            raise SystemExit(f"ledger_cli: body names model {payload.get('model')!r}, "
                             f"the ledger was opened for {model!r}")
        last = None
        for n in range(1, MAX_TRIES + 1):
            response, exc, detail = attempt(url, payload, kwargs, n)
            if response is not None:
                return transport.Response(status=response.status, body=response.body,
                                          latency_ms=response.latency_ms, attempts=n)
            status = getattr(exc, "status", None)
            if status is not None and billing_signal(status, detail):
                stop_file.write_text(json.dumps({"cell": args.cell, "status": status,
                                                 **detail}, indent=1))
                print(f"STOP-BILLING: HTTP {status}: {detail.get('message')}",
                      file=sys.stderr, flush=True)
                os._exit(9)
            if status == 429 and any("PerDay" in str(q) for q in detail.get("quota_ids") or []):
                print(f"QUOTA-DAY: {detail.get('quota_ids')} {detail.get('quota_values')}",
                      file=sys.stderr, flush=True)
                save()
                os._exit(8)
            if status is not None and status in transport.FATAL_STATUS:
                raise exc
            last = exc
            if n == MAX_TRIES:
                break
            doubling = 2 ** (n - 1)
            if status == 429:
                named = told["retry_after"]
                try:
                    named = named if named is not None else \
                        float(str(detail.get("retry_delay") or "").rstrip("s") or "nan")
                except ValueError:
                    named = float("nan")
                base = FLOOR_429 * doubling
                wait = max(named, FLOOR_429) if named == named else base
            else:
                wait = FLOOR_5XX * doubling
            wait = min(wait * random.uniform(1.0, 1.25), CEILING)
            told["retry_after"] = None
            print(f"  retry {n}: {status or type(exc).__name__}, waiting {wait:.0f}s",
                  file=sys.stderr, flush=True)
            waited["backoff"] += wait * SCALE
            time.sleep(wait * SCALE)
        raise last

    transport.post_json = charged
    try:
        return cli.main(argv)
    finally:
        save()


if __name__ == "__main__":
    sys.exit(main())
