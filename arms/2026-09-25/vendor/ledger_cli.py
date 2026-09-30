#!/usr/bin/env python3
"""claimcheck's own CLI, in process, with every chat request charged to a persisted spend.Ledger.

    ledger_cli.py --state LEDGER.json --vendor openai --sku openai/gpt-6-sol \
                  --cell LABEL --docs source_a.md source_b.md -- merge ...

Everything after `--` is handed to `claimcheck.cli.main` unchanged, the function
`python -m claimcheck` calls, so argument parsing, preflight and exit codes are
the command's own. The one thing added is a wrapper around
`claimcheck.transport.post_json`, the seam every chat request goes through: each
request is approved, estimated, refused or run, and charged inside
`tests/spend.py`'s `Ledger.call`, and the ledger's rows are written to disk after
every call so that every cell and every probe of one vendor shares one cap.

BENCH_TREE names the pinned clone. Its `src/` and `tests/` are imported, and
`claimcheck` is asserted to resolve inside it.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
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

# REGISTRATION.md, "Money: the ledger". Run-specific; FIRST_PASS is not used.
CAPS = spend.Caps(
    spend={"openai": 3.90, "anthropic": 8.60, "google": 0.00},
    calls=400,
    tokens=4_000_000,
    interval={"openai": 0.0, "anthropic": 0.0, "google": 0.0},
)
ALLOWANCE = {"openai": 24_000, "anthropic": 40_000}
HOSTS = {"openai": "https://api.openai.com/v1/", "anthropic": "https://api.anthropic.com/v1/"}


def load_state(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"rows": [], "refused": []}


def save_state(path: Path, state: dict) -> None:
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=1), encoding="utf-8")
    os.replace(tmp, path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", required=True, type=Path)
    parser.add_argument("--vendor", required=True, choices=sorted(HOSTS))
    parser.add_argument("--sku", required=True)
    parser.add_argument("--cell", required=True)
    parser.add_argument("--docs", nargs="+", required=True, type=Path)
    parser.add_argument("rest", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    argv = args.rest[1:] if args.rest[:1] == ["--"] else args.rest
    vendor, sku = args.vendor, args.sku
    model = sku.split("/", 1)[1]
    spend.price_for(sku)  # an unpriced SKU aborts before anything is sent

    state = load_state(args.state)
    ledger = spend.Ledger(CAPS)
    # Restore what earlier cells and probes of this vendor already spent.
    for row in state["rows"]:
        ledger.spent.calls += 1
        ledger.spent.input_tokens += row["input_tokens"]
        ledger.spent.output_tokens += row["output_tokens"]
        ledger.spent.dollars[row["vendor"]] = (ledger.spent.dollars.get(row["vendor"], 0.0)
                                               + row["dollars"])
    ledger.rows = list(state["rows"])
    documents = [p.read_text(encoding="utf-8") for p in args.docs]
    source_guard.approve(documents)  # fail before the first call, not at it

    real = transport.post_json

    def persist(extra: dict) -> None:
        ledger.rows[-1].update(extra)
        state["rows"] = ledger.rows
        save_state(args.state, state)

    def charged(url, payload, **kwargs):
        if not url.startswith(HOSTS[vendor]):
            raise SystemExit(f"ledger_cli: refusing a request outside {HOSTS[vendor]}")
        if payload.get("model") != model:
            raise SystemExit(f"ledger_cli: body names model {payload.get('model')!r}, "
                             f"the ledger was opened for {model!r}")
        chars = len(json.dumps(payload.get("messages", [])))
        input_estimate = chars // 3 + 1
        ceiling = payload.get("max_tokens") or payload.get("max_completion_tokens")
        allowance = int(ceiling) if ceiling else ALLOWANCE[vendor]
        extra = {"cell": args.cell, "path": url[len(HOSTS[vendor]) - 1:],
                 "input_estimate": input_estimate, "output_allowance": allowance}
        response = None
        try:
            with ledger.call(vendor, sku, input_estimate=input_estimate,
                             output_allowance=allowance, documents=documents) as charge:
                response = real(url, payload, **kwargs)
                usage, served = {}, None
                try:
                    envelope = json.loads(response.body)
                    usage = envelope.get("usage") or {}
                    served = envelope.get("model")
                except (ValueError, AttributeError):
                    pass
                cached = (usage.get("prompt_tokens_details") or {}).get("cached_tokens") or 0
                charge(input_tokens=usage.get("prompt_tokens"),
                       output_tokens=usage.get("completion_tokens"),
                       cached_tokens=cached)
                extra.update(served_model=served, attempts=response.attempts,
                             latency_ms=response.latency_ms,
                             reasoning_tokens=(usage.get("completion_tokens_details")
                                               or {}).get("reasoning_tokens"))
        except spend.BudgetExceeded as exc:
            state.setdefault("refused", []).append({"cell": args.cell, "reason": str(exc)})
            save_state(args.state, state)
            raise
        except Exception as exc:
            # The transport retries a timeout or a retryable status up to
            # MAX_ATTEMPTS times before raising, and a request that timed out
            # after it was sent may have been generated and billed. The ledger
            # charged one estimate; the other attempts are charged here. A fatal
            # status (400, 401, ...) is raised on the first attempt and is not.
            fatal = (isinstance(exc, transport.HTTPStatusError)
                     and exc.status in transport.FATAL_STATUS)
            if ledger.rows and "cell" not in ledger.rows[-1]:
                extra["failed"] = type(exc).__name__
                persist(extra)
            if not fatal and not isinstance(exc, SystemExit):
                for _ in range(transport.MAX_ATTEMPTS - 1):
                    with ledger.call(vendor, sku, input_estimate=input_estimate,
                                     output_allowance=allowance,
                                     documents=documents) as charge:
                        charge(input_tokens=None, output_tokens=None)
                    persist({"cell": args.cell, "path": extra["path"],
                             "retried_attempt": True, "failed": type(exc).__name__})
            raise
        finally:
            if ledger.rows and "cell" not in ledger.rows[-1]:
                if response is None:
                    extra["failed"] = True
                persist(extra)
        # Attempts the transport retried before this answer: each may have been
        # billed and none reported usage, so each is charged the estimate.
        for _ in range(max(0, (response.attempts or 1) - 1)):
            with ledger.call(vendor, sku, input_estimate=input_estimate,
                             output_allowance=allowance, documents=documents) as charge:
                charge(input_tokens=None, output_tokens=None)
            persist({"cell": args.cell, "path": extra["path"], "retried_attempt": True})
        return response

    transport.post_json = charged
    return cli.main(argv)


if __name__ == "__main__":
    sys.exit(main())
