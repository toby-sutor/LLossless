#!/usr/bin/env python3
"""The SKU and tier probe: plan it, size it, then run it.

Three things have to be true before any arm runs, and this file is where the
first two are settled without spending anything.

**The plan is data, not prose.** A probe described in a status report and a
probe encoded in a file look identical afterwards, and only one of them can be
checked. `PLAN` is the probe; `--plan` prints what it will cost; `--self-test`
asserts the properties that have to hold before the money moves.

**A probe below the dashboard's resolution cannot be reconciled.** Vendor
consoles round to the cent, so a probe that spends $0.004 and a console that
reads $0.00 agree on nothing - and a 1000x under-count hides exactly there.
Each billed vendor's plan is therefore sized deliberately
*above* $0.01, with margin, and `--self-test` refuses a plan that is not. A
larger output allowance is the cheapest lever for this, so that is the lever
used: one volume step per billed vendor whose job is to move the console needle
far enough that the comparison means something.

**Google spends nothing.** Its cap is $0.00 and its expected console figure is
$0.00, which is a stop with no tolerance rather than a number to compare. Its
steps are free-tier only and none of them may reach `cost`. The Google rows
in `PRICES` (the paid tier's rates) all price above zero, so a
Google SKU that tried would be refused by the $0.00 cap before the call.

`--run` is the only mode that touches the network. `--dry-run` walks the same
code - the source guard, the caps, the pacing, the ledger rows, the snapshot -
against a stub transport, so everything except the HTTP request is proved
offline. What `--dry-run` cannot prove is what a vendor actually returns; the
tier findings are the part that genuinely requires the call.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import spend
from spend import NO_DOCUMENT

# Three token counts, and they are not interchangeable.
#
#   input_est   what the prompt really is. Small: these prompts are one line
#               and carry no document.
#   allowance   the ceiling handed to the cap. Much larger than `emit`, and
#               that gap is where the cap's pessimism comes from - it trips on
#               the worst case rather than the expected one.
#   emit        what the model is expected to actually produce, and what the
#               plan is costed on. Deliberately a LOWER bound, so that a plan
#               clearing the console floor on paper still clears it in fact.
#
# Costing the plan on `allowance` would overstate the figure the operator is
# asked to compare against a console. The reconciliation itself is unaffected
# either way: it compares the ledger's measured usage to the console, never the
# plan. `emit` only has to be honest enough to size the probe and to be worth
# printing before the money moves.
@dataclass(frozen=True)
class Step:
    kind: str          # models | schema | tool | plain | volume
    sku: str           # "" for a vendor-level call that is not billed per SKU
    prompt: str
    input_est: int     # tokens, estimated for the cap
    allowance: int     # max output tokens, the ceiling handed to the cap
    emit: int          # tokens the step is expected to actually emit


_LADDER = "Reply with the three words: alpha, beta, gamma."
_VOLUME = (
    "List the integers from 1 to 2500, one per line, as plain digits with no "
    "commentary. Do not stop early and do not summarise."
)

# Sized so each billed vendor clears $0.01 by roughly an order of magnitude.
# The margin is not caution for its own sake: at 2x resolution a rounding
# difference and a real discrepancy look the same, and the whole point of the
# reconciliation is to tell them apart.
PLAN: dict[str, list[Step]] = {
    "openai": [
        Step("models", "", "", 0, 0, 0),
        Step("schema", "openai/gpt-5.6-luna", _LADDER, 30, 600, 30),
        Step("tool", "openai/gpt-5.6-luna", _LADDER, 30, 600, 30),
        Step("plain", "openai/gpt-5.6-luna", _LADDER, 30, 600, 30),
        Step("schema", "openai/gpt-5.6-terra", _LADDER, 30, 600, 30),
        Step("tool", "openai/gpt-5.6-terra", _LADDER, 30, 600, 30),
        Step("plain", "openai/gpt-5.6-terra", _LADDER, 30, 600, 30),
        Step("volume", "openai/gpt-5.6-terra", _VOLUME, 30, 16000, 6000),
    ],
    "anthropic": [
        Step("models", "", "", 0, 0, 0),
        Step("schema", "anthropic/claude-haiku-4-5-20251001", _LADDER, 30, 600, 30),
        Step("tool", "anthropic/claude-haiku-4-5-20251001", _LADDER, 30, 600, 30),
        Step("plain", "anthropic/claude-haiku-4-5-20251001", _LADDER, 30, 600, 30),
        Step("schema", "anthropic/claude-sonnet-5", _LADDER, 30, 600, 30),
        Step("tool", "anthropic/claude-sonnet-5", _LADDER, 30, 600, 30),
        Step("plain", "anthropic/claude-sonnet-5", _LADDER, 30, 600, 30),
        Step("volume", "anthropic/claude-sonnet-5", _VOLUME, 30, 16000, 6000),
    ],
    # Free tier only. No priced SKU, no volume step, nothing to reconcile
    # except that the console still reads $0.00.
    "google": [
        Step("models", "", "", 0, 0, 0),
    ],
}

# The console rounds to the cent, so this is the floor a plan has to clear to
# be comparable at all. Kept as its own name rather than reaching into
# `spend.DASHBOARD_RESOLUTION` inline, so the margin below is legible.
FLOOR = spend.DASHBOARD_RESOLUTION
MARGIN = 4.0    # times the floor, minimum. Below this, rounding is a rival cause.

BILLED = ("openai", "anthropic")
FREE = ("google",)


def expected_spend(vendor: str) -> float:
    """Dollars the plan expects to actually be billed for one vendor."""
    total = 0.0
    for step in PLAN[vendor]:
        if not step.sku:
            continue
        total += spend.cost(step.sku, input_tokens=step.input_est,
                            output_tokens=step.emit)
    return total


def render_plan() -> str:
    out = ["probe plan (expected billed spend, not the cap estimate)", ""]
    for vendor, steps in PLAN.items():
        total = expected_spend(vendor)
        interval = spend.FIRST_PASS.interval[vendor]
        cap = spend.FIRST_PASS.spend[vendor]
        out.append(f"  {vendor}  cap ${cap:.2f}  interval {interval}s  "
                   f"{len(steps)} steps  expected ${total:.4f}")
        for step in steps:
            if not step.sku:
                out.append(f"      {step.kind:<7} -                     free")
                continue
            each = spend.cost(step.sku, input_tokens=step.input_est,
                              output_tokens=step.emit)
            out.append(f"      {step.kind:<7} {step.sku.split('/')[1]:<28} "
                       f"{step.input_est:>5}in {step.emit:>5}out  ${each:.4f}")
        out.append("")
    grand = sum(expected_spend(v) for v in PLAN)
    out.append(f"  total expected ${grand:.4f}   "
               f"floor ${FLOOR:.2f}   required margin {MARGIN:g}x")
    return "\n".join(out)


# --------------------------------------------------------------------------
# transports


class StubTransport:
    """Answers like a vendor without being one. `--dry-run`'s whole point.

    Returns usage counts equal to the step's expectation, so a dry run produces
    the same ledger the plan predicts. That makes the dry run a check on the
    plan's arithmetic as well as on the plumbing.
    """

    def __init__(self) -> None:
        self.seen: list[tuple[str, str]] = []

    def __call__(self, vendor: str, step: Step, key: str) -> dict:
        self.seen.append((vendor, step.kind))
        if step.kind == "models":
            return {"skus": ["stub-a", "stub-b"], "input": 0, "output": 0}
        return {"text": "alpha beta gamma", "tier": step.kind,
                "input": step.input_est, "output": step.emit, "cached": 0}


class VendorError(RuntimeError):
    """An HTTP error with the vendor's explanation attached.

    `urllib` raises `HTTPError` with the body unread, so an unhandled 400 comes
    out as "Bad Request" and nothing else. The body is where the vendor says
    which field it rejected, which is the difference between a capability
    finding and a malformed request of ours - and a probe whose whole purpose
    is to find out which tiers a SKU supports cannot afford to lose it.
    """


def _post(url: str, payload: dict, headers: dict, timeout: int = 120) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST",
                                 headers={"content-type": "application/json",
                                          **headers})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:400]
        raise VendorError(f"HTTP {exc.code}: {detail}") from None


def _get(url: str, headers: dict, timeout: int = 60) -> dict:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


_SCHEMA = {"type": "object", "properties": {"words": {"type": "array",
           "items": {"type": "string"}}}, "required": ["words"],
           "additionalProperties": False}
_TOOL = {"name": "record", "description": "Record the words.",
         "parameters": _SCHEMA}


def _openai_like(base: str, auth: dict, vendor: str, step: Step) -> dict:
    if step.kind == "models":
        data = _get(f"{base}/models", auth)
        return {"skus": sorted(m["id"] for m in data.get("data", [])),
                "input": 0, "output": 0}
    model = step.sku.split("/", 1)[1]
    payload: dict = {"model": model, "max_completion_tokens": step.allowance,
                     "messages": [{"role": "user", "content": step.prompt}]}
    if step.kind == "schema":
        payload["response_format"] = {"type": "json_schema", "json_schema":
                                      {"name": "words", "strict": True,
                                       "schema": _SCHEMA}}
    elif step.kind == "tool":
        payload["tools"] = [{"type": "function", "function": _TOOL}]
        payload["tool_choice"] = {"type": "function",
                                  "function": {"name": "record"}}
    data = _post(f"{base}/chat/completions", payload, auth)
    usage = data.get("usage", {})
    details = usage.get("prompt_tokens_details") or {}
    return {"text": (data["choices"][0]["message"].get("content") or "")[:200],
            "tier": step.kind,
            "input": usage.get("prompt_tokens"),
            "output": usage.get("completion_tokens"),
            "cached": details.get("cached_tokens", 0) or 0}


def _anthropic(vendor: str, step: Step, key: str) -> dict:
    auth = {"x-api-key": key, "anthropic-version": "2023-06-01"}
    base = "https://api.anthropic.com/v1"
    if step.kind == "models":
        data = _get(f"{base}/models", auth)
        return {"skus": sorted(m["id"] for m in data.get("data", [])),
                "input": 0, "output": 0}
    model = step.sku.split("/", 1)[1]
    payload: dict = {"model": model, "max_tokens": step.allowance,
                     "messages": [{"role": "user", "content": step.prompt}]}
    if step.kind in ("schema", "tool"):
        payload["tools"] = [{"name": "record", "description": "Record.",
                             "input_schema": _SCHEMA}]
        payload["tool_choice"] = {"type": "tool", "name": "record"}
    data = _post(f"{base}/messages", payload, auth)
    usage = data.get("usage", {})
    blocks = data.get("content", [])
    text = next((b.get("text", "") for b in blocks if b.get("type") == "text"), "")
    return {"text": text[:200], "tier": step.kind,
            "input": usage.get("input_tokens"),
            "output": usage.get("output_tokens"),
            "cached": usage.get("cache_read_input_tokens", 0) or 0}


def _openai(vendor: str, step: Step, key: str) -> dict:
    return _openai_like("https://api.openai.com/v1",
                        {"authorization": f"Bearer {key}"}, vendor, step)


def _google(vendor: str, step: Step, key: str) -> dict:
    # Free tier only, and only the free call. Anything that could be billed is
    # deliberately absent: `PLAN["google"]` has no SKU step, so this never
    # reaches a completion. Listing models costs nothing on any tier.
    if step.kind != "models":
        raise AssertionError(
            f"google is capped at $0.00 and its plan carries no billable step; "
            f"a {step.kind!r} step reached the transport, which means the plan "
            f"was edited without the cap being reconsidered."
        )
    base = "https://generativelanguage.googleapis.com/v1beta"
    data = _get(f"{base}/models", {"x-goog-api-key": key})
    return {"skus": sorted(m["name"] for m in data.get("models", [])),
            "input": 0, "output": 0}


TRANSPORTS = {"openai": _openai, "anthropic": _anthropic, "google": _google}
KEY_ENV = {"openai": "OPEN_AI_API_KEY", "anthropic": "ANTHROPIC_API_KEY",
           "google": "GOOGLE_AI_API_KEY"}


# --------------------------------------------------------------------------


def _keys(vendors) -> dict[str, str]:
    """Read keys from the environment. Never printed, never logged, never
    written to the snapshot - only their presence is ever reported."""
    out = {}
    for vendor in vendors:
        value = os.environ.get(KEY_ENV[vendor], "").strip()
        if not value:
            raise SystemExit(f"{KEY_ENV[vendor]} is not set in the environment")
        out[vendor] = value
    return out


def execute(transport, keys: dict[str, str], *, vendors, out_path: Path,
            pace: bool = True) -> int:
    # `pace=False` is for the stub only. The interval has to be bound here
    # rather than monkeypatched later: `Ledger.__init__` takes `sleep` as a
    # default argument, so the real `time.sleep` is captured when the module
    # is defined and rebinding `spend.time.sleep` afterwards does nothing.
    ledger = spend.Ledger(spend.FIRST_PASS, announce=lambda m: print(f"  {m}"),
                          **({} if pace else {"sleep": lambda _s: None}))
    findings: dict[str, dict] = {}
    for vendor in vendors:
        findings[vendor] = {"skus": [], "tiers": {}, "errors": []}
        for step in PLAN[vendor]:
            label = f"{vendor}/{step.kind}" + (f" {step.sku}" if step.sku else "")
            if step.kind == "models":
                # Not a paid call and not costed: listing models is free on all
                # three, so it does not go through the ledger. It also carries
                # no document, which is why nothing here needs the source guard.
                try:
                    result = transport(vendor, step, keys[vendor])
                    findings[vendor]["skus"] = result["skus"]
                    print(f"  {label}: {len(result['skus'])} SKUs")
                except Exception as exc:                      # noqa: BLE001
                    findings[vendor]["errors"].append(f"{label}: {exc!r}")
                    print(f"  {label}: FAILED {exc!r}")
                continue
            with ledger.call(vendor, step.sku, input_estimate=step.input_est,
                             output_allowance=step.allowance,
                             documents=NO_DOCUMENT) as charge:
                try:
                    result = transport(vendor, step, keys[vendor])
                except Exception as exc:                      # noqa: BLE001
                    findings[vendor]["errors"].append(f"{label}: {exc!r}")
                    print(f"  {label}: FAILED {exc!r}")
                    continue
                charge(input_tokens=result["input"],
                       output_tokens=result["output"],
                       cached_tokens=result.get("cached", 0) or 0)
                findings[vendor]["tiers"].setdefault(step.sku, {})[step.kind] = {
                    "ok": True, "sample": result["text"][:80],
                    "input": result["input"], "output": result["output"],
                }
    snapshot = ledger.snapshot()
    snapshot["findings"] = findings
    out_path.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    print()
    print(spend.render(snapshot, []))
    print(f"\nsnapshot written to {out_path}")
    return 0


def self_test() -> int:
    """Everything about the plan that can be settled without spending."""
    failures: list[str] = []

    def check(ok, msg):
        if not ok:
            failures.append(msg)

    # 1. Every billed vendor clears the console's resolution with margin. This
    #    is that clause, held in code rather than in a
    #    report, so that shrinking the plan later turns something red.
    for vendor in BILLED:
        got = expected_spend(vendor)
        check(got >= FLOOR * MARGIN,
              f"{vendor} expects ${got:.4f}, under {MARGIN:g}x the ${FLOOR:.2f} "
              f"console floor; it would reconcile as UNANSWERABLE, not clean")

    # 2. The free vendor spends nothing, and cannot: no priced SKU in its plan,
    #    and every Google row in PRICES is refused by its $0.00 cap.
    for vendor in FREE:
        check(spend.FIRST_PASS.spend[vendor] == 0.0,
              f"{vendor} must stay capped at $0.00")
        check(expected_spend(vendor) == 0.0,
              f"{vendor} expects a non-zero spend against a $0.00 cap")
        check(all(not s.sku for s in PLAN[vendor]),
              f"{vendor}'s plan names a billable SKU")
    # Google rows exist since 2026-09-25: the paid tier's
    # rates, so a report can state what a free-tier run would cost if billed.
    # The protection is now the cap rather than the absence of a row: every
    # google row prices above zero, so `Ledger.call` refuses it against the
    # $0.00 cap before anything is sent. A zero row in the shipped table
    # would be the one way through, and it is refused here.
    google_rows = {k: v for k, v in spend.PRICES.items() if k.startswith("google/")}
    check(all(v.input > 0 and v.output > 0 for v in google_rows.values()),
          f"a google row in PRICES prices at zero, which the $0.00 cap would admit: "
          f"{sorted(k for k, v in google_rows.items() if not (v.input > 0 and v.output > 0))}")
    for sku in google_rows:
        try:
            with spend.Ledger(spend.FIRST_PASS).call(
                    "google", sku, input_estimate=1, output_allowance=1,
                    documents=spend.NO_DOCUMENT):
                failures.append(f"the $0.00 google cap admitted a call priced at {sku}")
        except spend.BudgetExceeded:
            pass

    # 3. Every priced step's SKU is in the table, and every table row that the
    #    plan uses carries its provenance.
    for vendor, steps in PLAN.items():
        for step in steps:
            if not step.sku:
                continue
            check(step.sku in spend.PRICES, f"{step.sku} is not in PRICES")
            price = spend.PRICES.get(step.sku)
            if price is None:
                continue
            check(price.read_on != "n/a" and price.source.startswith("http"),
                  f"{step.sku} has no dated URL; a price with no date is not "
                  f"checkable")
            # A per-1K figure entered against a per-1M table reads 1000x low.
            # Nothing real is under a cent per million, so a floor catches the
            # dangerous direction of a unit slip at the point of entry.
            check(price.output >= 0.05 and price.input >= 0.01,
                  f"{step.sku} rates look like a per-1K entry in a per-1M "
                  f"table: input {price.input}, output {price.output}")

    # 4. The unfilled-field check. 0.0 is what the field held before it was
    #    populated, not a decision that no pacing is needed.
    for vendor in PLAN:
        check(spend.FIRST_PASS.interval.get(vendor, 0.0) > 0.0,
              f"{vendor}'s interval is 0.0, which is unfilled rather than set")

    # 5. The long-context guard fires, and does not fire below the threshold.
    #    Must-fire and must-not-fire, on the shipped `cost`, not a copy.
    try:
        spend.cost("openai/gpt-5.6-terra", input_tokens=10**9, output_tokens=1)
        failures.append("cost() accepted an input above max_input; the vendor's "
                        "second, higher rate would go uncharged")
    except spend.UnknownPrice:
        pass
    try:
        spend.cost("openai/gpt-5.6-terra", input_tokens=2000, output_tokens=1)
    except spend.UnknownPrice:
        failures.append("cost() refused an ordinary short-context call; the "
                        "guard is over-tight and blocks the probe itself")

    # 6. The whole run walks end to end against the stub: source guard, caps,
    #    pacing, ledger rows, snapshot. Pacing is stubbed out or this sleeps for
    #    minutes; the intervals themselves are asserted at 4 above.
    stub = StubTransport()
    import tempfile
    snap = None
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "snap.json"
        try:
            execute(stub, {v: "not-a-key" for v in PLAN}, vendors=list(PLAN),
                    out_path=out, pace=False)
            snap = json.loads(out.read_text(encoding="utf-8"))
        except Exception as exc:                              # noqa: BLE001
            # A dry run that raises is a failed check, not a traceback. Letting
            # it propagate turns a red clause into a crash with no FAIL line,
            # and a crash reads like tooling trouble rather than a defect.
            failures.append(f"the dry run did not complete: {exc!r}")
    if snap is None:
        snap = {"calls": -1, "dollars": {}, "rows": []}
    priced = sum(1 for v in PLAN for s in PLAN[v] if s.sku)
    check(snap["calls"] == priced,
          f"dry run made {snap['calls']} ledger calls, plan has {priced} "
          f"priced steps")
    for vendor in BILLED:
        got, want = snap["dollars"].get(vendor, 0.0), expected_spend(vendor)
        check(abs(got - want) < 1e-9,
              f"dry run charged {vendor} ${got:.4f} but the plan predicted "
              f"${want:.4f}; the plan's arithmetic and the ledger's disagree")
    check(snap["dollars"].get("google", 0.0) == 0.0,
          "the dry run put a charge on google")
    check(all(r["documents"] == [] for r in snap["rows"]),
          "a probe step carried a document; every step passes NO_DOCUMENT")

    # 7. A step that tried to bill google must abort rather than proceed. Seeded
    #    against the shipped transport, since that is where the refusal lives.
    try:
        _google("google", Step("plain", "google/x", "hi", 1, 1, 1), "k")
        failures.append("the google transport accepted a billable step")
    except AssertionError:
        pass
    except Exception as exc:                                  # noqa: BLE001
        # Anything other than the refusal means the guard did not stop it before
        # the transport tried to reach the network. That is the same defect as
        # accepting the step; it just fails later and noisily.
        failures.append(f"the google transport did not refuse a billable step "
                        f"before attempting a request: {exc!r}")

    for line in failures:
        print(f"FAIL {line}")
    if failures:
        print(f"\n{len(failures)} failure(s)")
        return 1
    print(f"probe plan: {len(BILLED)} billed vendors clear the ${FLOOR:.2f} "
          f"console floor by >={MARGIN:g}x "
          f"({', '.join(f'{v} ${expected_spend(v):.4f}' for v in BILLED)}); "
          f"google is capped at $0.00, refuses its priced rows and carries no billable step; "
          f"intervals filled; long-context guard fires both ways; "
          f"{priced} steps walk the ledger end to end and match the plan.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--plan", action="store_true", help="print the costed plan")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--dry-run", action="store_true",
                    help="walk the whole path against a stub; no network")
    ap.add_argument("--run", action="store_true",
                    help="MAKE THE PAID CALLS. Requires the keys in the env.")
    ap.add_argument("--vendor", action="append", default=None,
                    help="restrict to one vendor; repeatable")
    ap.add_argument("--out", default="probe-snapshot.json")
    args = ap.parse_args()

    vendors = args.vendor or list(PLAN)
    unknown = [v for v in vendors if v not in PLAN]
    if unknown:
        raise SystemExit(f"unknown vendor(s): {unknown}")

    if args.self_test:
        return self_test()
    if args.plan:
        print(render_plan())
        return 0
    if args.dry_run:
        return execute(StubTransport(), {v: "stub" for v in vendors},
                       vendors=vendors, out_path=Path(args.out), pace=False)
    if args.run:
        print(render_plan())
        print("\nthis will spend real money. ", end="")
        total = sum(expected_spend(v) for v in vendors)
        print(f"expected ${total:.4f} across {', '.join(vendors)}.")
        return execute(lambda v, step, key: TRANSPORTS[v](v, step, key),
                       _keys(vendors), vendors=vendors, out_path=Path(args.out))
    print(render_plan())
    print("\nnothing run. --self-test, --dry-run or --run.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
