#!/usr/bin/env python3
"""Does the arm's own request body survive each vendor?

`probe_vendors.py` asked which tiers a SKU supports. It answered with bodies it
built itself, and on Anthropic it asked the native Messages API. Neither is the
request an arm sends, so three things stayed unknown, and each of them would
invalidate an arm rather than degrade it:

  a. does `reasoning_effort: "none"` coexist with `response_format:
     json_schema` on the OpenAI 5.6 SKUs? The 400 already on record fired on
     `tools` + `reasoning_effort`; the pinned rung sends no tools, and that
     combination has never been tried.
  b. does Anthropic's OpenAI-compatible endpoint accept the pinned rung at all?
     It has never been called. The "ok" rows recorded elsewhere
     were measured on `/v1/messages` with
     `input_schema`, which says the models can do the job and nothing about the
     endpoint an arm speaks to.
  c. is `max_tokens` accepted, or must it be `max_completion_tokens`?
     `merge.py` alone passes a budget, so this fails on one role out of three -
     merge erroring while decompose and verify pass reads as a model result,
     not as a malformed field.

**The body comes from `structured.build_body`, never from this file.** A probe
that rebuilds the request shape proves the rebuild. Every payload below is the
shipped builder's output with the arm's own arguments, which is the only way the
answer transfers to the arm. `--self-test` asserts that the three payloads
differ in exactly the fields the three questions are about, so a probe that sent
one body three times cannot report three results.

**The endpoint is the arm's endpoint.** `{base}/chat/completions` for both
vendors, because that is the single URL `client.py:776` builds. Anthropic is the
priority here for that reason alone.

`--run` is the only mode that touches the network.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import spend
from spend import NO_DOCUMENT
from llossless import structured

# A cap of its own, not FIRST_PASS. The brief authorises $0.50 for this step
# and $6.00 for the block; running the probe under the block's cap would let a
# runaway retry spend the block's money on the probe's question.
SHAPE_CAP = spend.Caps(
    spend={"openai": 0.25, "anthropic": 0.25},
    calls=40,
    tokens=200_000,
    interval={"openai": 4.0, "anthropic": 8.0},
)

# One line, no document. `source_guard` still gates the call: this passes
# NO_DOCUMENT and says so, rather than passing an empty list.
PROMPT = "Reply with the three words: alpha, beta, gamma."
SCHEMA = {"type": "object",
          "properties": {"words": {"type": "array", "items": {"type": "string"}}},
          "required": ["words"], "additionalProperties": False}

BUDGET = 256      # the `max_tokens` value question (c) puts on the wire
ALLOWANCE = 4000  # ceiling handed to the cap for the unbudgeted thinking-on call

SKUS = {
    "openai": ("openai/gpt-5.6-luna", "openai/gpt-5.6-terra"),
    "anthropic": ("anthropic/claude-haiku-4-5-20251001",
                  "anthropic/claude-sonnet-5"),
}
BASE = {"openai": "https://api.openai.com/v1",
        "anthropic": "https://api.anthropic.com/v1"}
KEY_ENV = {"openai": "OPEN_AI_API_KEY", "anthropic": "ANTHROPIC_API_KEY"}


@dataclass(frozen=True)
class Shape:
    kind: str          # off | on | budget | ...
    question: str
    thinking: bool
    max_tokens: int | None
    allowance: int
    # A named, recorded departure from what `build_body` can currently
    # produce. `SHAPES` uses none of these: those twelve calls are the arm's
    # own body and nothing else, which is the only reason their answers
    # transfer. `FOLLOWUP` uses them to ask a different question - not "what
    # does the arm send", but "does the refusal the arm got have a legal
    # neighbour" - and the answer decides whether a code change is worth
    # proposing at all. The mutation is stored in the snapshot beside the
    # body, so a later reader cannot mistake a probed hypothetical for a
    # measurement of the shipped request.
    temperature: float | None = 0.0


SHAPES = (
    Shape("off", "a. reasoning_effort:none beside response_format:json_schema",
          thinking=False, max_tokens=None, allowance=600),
    Shape("on", "b. the thinking-on shape: no reasoning field at all",
          thinking=True, max_tokens=None, allowance=ALLOWANCE),
    Shape("budget", "c. max_tokens, or must it be max_completion_tokens",
          thinking=False, max_tokens=BUDGET, allowance=BUDGET),
)


FOLLOWUP = (
    Shape("off@1.0", "does reasoning-off accept temperature 1.0 - would a pair "
          "run at 1.0 hold temperature constant across both states?",
          thinking=False, max_tokens=None, allowance=600, temperature=1.0),
    Shape("on@1.0", "does the thinking-on shape accept the temperature the "
          "vendor named as the only supported one?",
          thinking=True, max_tokens=None, allowance=ALLOWANCE, temperature=1.0),
    Shape("off@omit", "is the body accepted with no temperature field at all - "
          "the shape sonnet's `deprecated` refusal points at?",
          thinking=False, max_tokens=None, allowance=600, temperature=None),
    Shape("on@omit", "the same, in the thinking-on state.",
          thinking=True, max_tokens=None, allowance=ALLOWANCE, temperature=None),
)


def body_for(sku: str, shape: Shape) -> dict:
    """The arm's body, from the arm's builder. Not a reconstruction."""
    body = structured.build_body(
        tier="json_schema",
        model=sku.split("/", 1)[1],
        messages=[{"role": "user", "content": PROMPT}],
        schema=SCHEMA,
        schema_name="words",
        max_tokens=shape.max_tokens,
        thinking=shape.thinking,
        **({} if shape.temperature is None else {"temperature": shape.temperature}),
    )
    if shape.temperature is None:
        # `build_body` always writes a temperature; there is no argument that
        # suppresses it. Removing it here is the mutation, and it is the whole
        # question - so it is done after the builder ran, never by rebuilding
        # the body without it.
        body.pop("temperature", None)
    return body


def expected_spend(plan: dict[str, tuple[Shape, ...]] | None = None
                   ) -> dict[str, float]:
    """Dollars this probe expects to be billed, per vendor.

    Costed on the allowance, not on an expected emission. The unbudgeted
    thinking-on call is the one step whose output nobody can predict - that is
    the number the whole block is missing - so the estimate is deliberately the
    pessimistic one and the reported figure is an upper bound.
    """
    plan = plan_for(False) if plan is None else plan
    out: dict[str, float] = {}
    for vendor, skus in SKUS.items():
        total = 0.0
        for sku in skus:
            for shape in plan.get(sku, ()):
                total += spend.cost(sku, input_tokens=60,
                                    output_tokens=shape.allowance)
        out[vendor] = total
    return out


def render_plan(plan: dict[str, tuple[Shape, ...]] | None = None) -> str:
    lines = ["request-shape probe (upper bound: every step costed at its "
             "full output allowance)", ""]
    plan = plan_for(False) if plan is None else plan
    per = expected_spend(plan)
    calls = sum(len(v) for v in plan.values())
    for vendor, skus in SKUS.items():
        lines.append(f"  {vendor}  {BASE[vendor]}/chat/completions")
        for sku in skus:
            for shape in plan.get(sku, ()):
                lines.append(f"    {sku:44s} {shape.kind:7s} {shape.question}")
        lines.append(f"    {'':44s} {'':7s} upper bound ${per[vendor]:.4f}")
        lines.append("")
    total = sum(per.values())
    lines.append(f"  {calls} calls, upper bound ${total:.4f} total")
    lines.append(f"  brief AH item 2 stops above $0.50: "
                 f"{'PROCEED' if total <= 0.50 else 'STOP'}")
    return "\n".join(lines)


class VendorError(RuntimeError):
    """An HTTP error with the vendor's own explanation attached.

    `urllib` raises `HTTPError` with the body unread, so an unhandled 400
    arrives as "Bad Request" and nothing else. The body names the field that
    was rejected, which is the entire finding here - without it a capability
    result and a malformed request of ours are indistinguishable.
    """


def post(url: str, payload: dict, headers: dict, timeout: int = 180) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST",
                                 headers={"content-type": "application/json",
                                          **headers})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:600]
        raise VendorError(f"HTTP {exc.code}: {detail}") from None


def live(vendor: str, sku: str, shape: Shape, key: str) -> dict:
    body = body_for(sku, shape)
    auth = {"authorization": f"Bearer {key}"}
    data = post(f"{BASE[vendor]}/chat/completions", body, auth)
    usage = data.get("usage", {})
    details = usage.get("completion_tokens_details") or {}
    message = (data.get("choices") or [{}])[0].get("message") or {}
    return {"text": (message.get("content") or "")[:200],
            "input": usage.get("prompt_tokens"),
            "output": usage.get("completion_tokens"),
            "reasoning": details.get("reasoning_tokens"),
            "cached": (usage.get("prompt_tokens_details") or {}
                       ).get("cached_tokens", 0) or 0}


class StubTransport:
    """Answers like a vendor without being one, so `--dry-run` walks the real
    ledger, the real caps, the real pacing and the real snapshot."""

    def __init__(self) -> None:
        self.bodies: list[dict] = []

    def __call__(self, vendor: str, sku: str, shape: Shape, key: str) -> dict:
        self.bodies.append(body_for(sku, shape))
        return {"text": '{"words":["alpha","beta","gamma"]}', "input": 60,
                "output": 30, "reasoning": 0, "cached": 0}


# Which follow-up each SKU needs. Haiku needs none: it answered all three
# questions. The map is empty for it rather than absent, so a SKU that starts
# refusing has to be added here deliberately.
FOLLOWUP_FOR = {
    "openai/gpt-5.6-luna": ("off@1.0", "on@1.0"),
    "openai/gpt-5.6-terra": ("off@1.0", "on@1.0"),
    "anthropic/claude-haiku-4-5-20251001": (),
    "anthropic/claude-sonnet-5": ("off@omit", "on@omit"),
}


def plan_for(followup: bool) -> dict[str, tuple[Shape, ...]]:
    if not followup:
        return {sku: SHAPES for skus in SKUS.values() for sku in skus}
    by_kind = {s.kind: s for s in FOLLOWUP}
    return {sku: tuple(by_kind[k] for k in kinds)
            for sku, kinds in FOLLOWUP_FOR.items() if kinds}


def execute(transport, keys: dict[str, str], *, out_path: Path,
            plan: dict[str, tuple[Shape, ...]] | None = None,
            pace: bool = True) -> int:
    # `sleep` is bound here rather than monkeypatched: `Ledger.__init__` takes
    # it as a default argument, so rebinding `spend.time.sleep` afterwards
    # reaches nothing and a "fast" dry run would really sleep.
    ledger = spend.Ledger(SHAPE_CAP, announce=lambda m: print(f"  {m}"),
                          **({} if pace else {"sleep": lambda _s: None}))
    plan = plan_for(False) if plan is None else plan
    findings: dict[str, dict] = {}
    for vendor, skus in SKUS.items():
        for sku in skus:
            if not plan.get(sku):
                continue
            findings[sku] = {"endpoint": f"{BASE[vendor]}/chat/completions",
                             "shapes": {}}
            for shape in plan[sku]:
                body = body_for(sku, shape)
                record = {"question": shape.question,
                          "request": body,
                          "mutation": (None if shape.temperature == 0.0 else
                                       f"temperature={shape.temperature!r}"),
                          "reasoning_field": body.get("reasoning_effort", None),
                          "carries_max_tokens": "max_tokens" in body}
                with ledger.call(vendor, sku, input_estimate=60,
                                 output_allowance=shape.allowance,
                                 documents=NO_DOCUMENT) as charge:
                    try:
                        result = transport(vendor, sku, shape, keys[vendor])
                    except Exception as exc:               # noqa: BLE001
                        record["ok"] = False
                        record["vendor_message"] = str(exc)
                        findings[sku]["shapes"][shape.kind] = record
                        print(f"  {sku} {shape.kind}: REFUSED {exc}")
                        continue
                    charge(input_tokens=result["input"],
                           output_tokens=result["output"],
                           cached_tokens=result["cached"])
                    record.update(ok=True, response=result)
                    findings[sku]["shapes"][shape.kind] = record
                    print(f"  {sku} {shape.kind}: ok  "
                          f"{result['input']} in / {result['output']} out "
                          f"(reasoning {result['reasoning']})  "
                          f"{result['text'][:60]!r}")
    snapshot = ledger.snapshot()
    snapshot["findings"] = findings
    out_path.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    print()
    print(spend.render(snapshot, []))
    print(f"\nsnapshot written to {out_path}")
    return 0


def self_test() -> int:
    """Everything about the probe that can be settled without spending."""
    failures: list[str] = []

    def check(ok, msg):
        if not ok:
            failures.append(msg)

    for vendor, skus in SKUS.items():
        for sku in skus:
            built = {s.kind: body_for(sku, s) for s in SHAPES}

            # The three questions are three bodies. If any two of them
            # serialise identically the probe reports three results from one
            # request, and the report is three times as confident as the
            # evidence.
            wire = {k: json.dumps(v, sort_keys=True) for k, v in built.items()}
            check(len(set(wire.values())) == 3,
                  f"{sku}: the three shapes must be three distinct bodies, got "
                  f"{len(set(wire.values()))} distinct of 3")

            check(built["off"].get("reasoning_effort") == "none",
                  f"{sku}: the off shape must carry reasoning_effort=none, got "
                  f"{built['off'].get('reasoning_effort')!r}")
            check("reasoning_effort" not in built["on"],
                  f"{sku}: the on shape must carry no reasoning field, got "
                  f"{built['on'].get('reasoning_effort')!r}")
            differ = {k for k in set(built["off"]) | set(built["on"])
                      if built["off"].get(k) != built["on"].get(k)}
            check(differ == {"reasoning_effort"},
                  f"{sku}: off and on must differ in reasoning_effort alone, "
                  f"they differ in {sorted(differ)}")

            check(built["budget"].get("max_tokens") == BUDGET,
                  f"{sku}: the budget shape must put max_tokens on the wire, "
                  f"got {built['budget'].get('max_tokens')!r}")
            check("max_completion_tokens" not in built["budget"],
                  f"{sku}: the builder must not send max_completion_tokens; "
                  f"question (c) is which name the vendor wants")
            budget_differ = {k for k in set(built["off"]) | set(built["budget"])
                             if built["off"].get(k) != built["budget"].get(k)}
            check(budget_differ == {"max_tokens"},
                  f"{sku}: budget must differ from off in max_tokens alone, "
                  f"it differs in {sorted(budget_differ)}")

            # The rung is the one the arms are pinned to. A probe that
            # answered on another rung would answer a question nobody asked.
            check(built["off"].get("response_format", {}).get("type")
                  == "json_schema",
                  f"{sku}: every shape must be the pinned json_schema rung")
            check("tools" not in built["off"],
                  f"{sku}: the pinned rung sends no tools - the 400 already on "
                  f"record fired on tools + reasoning_effort, and a probe that "
                  f"sent tools would reproduce that instead of answering")

    # The endpoint is the one an arm builds, not the one this file finds
    # convenient. Read it off the shipped call site rather than asserting a
    # string this file also wrote.
    call_site = (Path(__file__).resolve().parent.parent / "src" / "llossless"
                 / "client.py").read_text(encoding="utf-8")
    check('f"{self.settings.base_url_for(role)}/chat/completions"' in call_site,
          "client.py no longer builds {base_url_for(role)}/chat/completions, so this "
          "probe is no longer probing the endpoint an arm calls")
    for vendor, base in BASE.items():
        check(base.endswith("/v1"),
              f"{vendor}: base must end in /v1 like config.with_api_path "
              f"produces, got {base!r}")

    # A follow-up shape asks about one field. If it moved another, its answer
    # would not be about the refusal it was written for.
    for sku in FOLLOWUP_FOR:
        for shape in FOLLOWUP:
            base = body_for(sku, SHAPES[1] if shape.thinking else SHAPES[0])
            got = body_for(sku, shape)
            differ = {k for k in set(base) | set(got)
                      if base.get(k) != got.get(k)}
            check(differ == {"temperature"},
                  f"{sku} {shape.kind}: must differ from its base shape in "
                  f"temperature alone, it differs in {sorted(differ)}")
        check(FOLLOWUP_FOR[sku] == () or set(FOLLOWUP_FOR[sku])
              <= {s.kind for s in FOLLOWUP},
              f"{sku}: follow-up names a shape that does not exist")

    total = sum(expected_spend().values())
    check(total <= 0.50,
          f"brief AH item 2 authorises $0.50 for this probe; the plan's upper "
          f"bound is ${total:.4f}")
    check(sum(SHAPE_CAP.spend.values()) <= 0.50,
          f"the ledger cap must enforce the authorisation, not this file's "
          f"arithmetic; caps total ${sum(SHAPE_CAP.spend.values()):.2f}")
    check("google" not in SHAPE_CAP.spend and "google" not in SKUS,
          "google carries no credit and is out of scope for this probe")

    for msg in failures:
        print(f"  - {msg}")
    print(f"probe_shapes self-test: {'FAILED' if failures else 'ok'}"
          f" ({len(failures)} failing)")
    return 1 if failures else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--plan", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--followup", action="store_true",
                    help="ask whether each refusal has a legal neighbour")
    ap.add_argument("--out", default="probe-shapes.json")
    args = ap.parse_args()

    if args.plan:
        print(render_plan(plan_for(args.followup)))
        return 0
    if args.self_test:
        return self_test()
    plan = plan_for(args.followup)
    if args.dry_run:
        print(render_plan(plan))
        print()
        return execute(StubTransport(), {v: "stub" for v in SKUS},
                       out_path=Path(args.out), plan=plan, pace=False)
    if args.run:
        print(render_plan(plan))
        print()
        keys = {}
        for vendor in SKUS:
            value = os.environ.get(KEY_ENV[vendor], "").strip()
            if not value:
                raise SystemExit(f"{KEY_ENV[vendor]} is not set")
            keys[vendor] = value
        return execute(live, keys, out_path=Path(args.out), plan=plan)
    ap.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
