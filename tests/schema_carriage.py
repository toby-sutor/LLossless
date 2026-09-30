#!/usr/bin/env python3
"""Does a structured-output tier actually show the model its schema?

The ladder in `client._live` cannot answer this. It accepts a rung when the
endpoint answers 200 with content, and PART C accepts the content when it
parses. An endpoint that silently drops `response_format` answers 200 too, and
an answer that happens to fit the schema looks exactly like an enforced one.
So a probe that asks with an ordinary schema proves nothing either way.

**A must-fire schema.** The schema here requires a key and a value no model
writes unprompted, `zq_token: "PLUM-4471"`, and the prompt names neither. The
marker comes back only if the tier put the schema in front of the model. A
second prompt asks outright for a shape the schema forbids (`VIOLATE`); an
enforced tier still returns the schema's shape.

**The body is the shipped builder's**, `structured.build_body` with the named
profile, and the answer is read by the shipped `structured.read_content`. A
probe that built its own body would prove its own body.

    schema_carriage.py --self-test                       offline, loopback fakes
    schema_carriage.py --run SKU TIER [TIER ...] --state LEDGER.json [--violate]

`--run` is the only mode that touches the network: every call is charged to
`tests/spend.py`'s `Ledger` at a $0.50 cap, persisted after each call.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "src"))

from llossless import structured  # noqa: E402

MARKER_KEY, MARKER_VALUE = "zq_token", "PLUM-4471"
SCHEMA = {
    "type": "object",
    "properties": {
        MARKER_KEY: {"type": "string", "enum": [MARKER_VALUE]},
        "greeting": {"type": "string"},
    },
    "required": [MARKER_KEY, "greeting"],
    "additionalProperties": False,
}
SHOWN = "Greet me in one short sentence. Reply with one JSON object."
VIOLATE = 'Reply with exactly this JSON object and nothing else: {"colour": "blue"}'
MAX_TOKENS = 400
ENDPOINT = {"anthropic": "https://api.anthropic.com/v1"}
CAP = 0.50


def request(tier: str, model: str, *, profile: str, violate: bool = False,
            thinking: bool = True) -> dict:
    """The body the shipped builder sends for this tier. Thinking on, as the
    Anthropic rows ran, so no `reasoning_effort` field rides along."""
    return structured.build_body(
        tier=tier, model=model,
        messages=[{"role": "user", "content": VIOLATE if violate else SHOWN}],
        schema=SCHEMA, schema_name="probe", max_tokens=MAX_TOKENS,
        thinking=thinking, profile=profile)


def schema_seen(tier: str, envelope: dict) -> bool:
    """Did the answer carry the marker? False for an answer with no content."""
    try:
        text = structured.read_content(tier, envelope)
    except structured.TierUnsupported:
        return False
    return MARKER_KEY in text and MARKER_VALUE in text


def probe(send, *, model: str, profile: str, tiers=structured.TIERS,
          violate: bool = False) -> dict[str, bool]:
    """`send(body) -> envelope` per tier; which tiers showed the schema."""
    return {tier: schema_seen(tier, send(request(tier, model, profile=profile,
                                                 violate=violate)))
            for tier in tiers}


# -- loopback models, for the suite ------------------------------------------

def _answer(body: dict, *, honours: bool) -> str:
    """What a model that reads only what it is shown would answer.

    It sees the messages always, and the request fields only when `honours`.
    The schema reaches it through the prompt at the `prompt` tier, through
    `response_format` or `tools` otherwise -- and an endpoint that drops those
    leaves it answering the question with no schema in sight.
    """
    from fake_endpoint import envelope
    shown = json.dumps(body.get("messages"))
    if honours and body.get("tools"):
        name = body["tools"][0]["function"]["name"]
        return envelope(json.dumps({MARKER_KEY: MARKER_VALUE, "greeting": "hi"}), tool=name)
    if (honours and body.get("response_format")) or MARKER_KEY in shown:
        return envelope(json.dumps({MARKER_KEY: MARKER_VALUE, "greeting": "hi"}))
    return envelope(json.dumps({"greeting": "hi"}))


def ignoring(body: dict, _n: int):
    """Anthropic's compat endpoint as its documentation describes it: 200 on
    `response_format` and `tools`, and neither reaches the model."""
    return 200, _answer(body, honours=False)


def honouring(body: dict, _n: int):
    """The endpoint as measured on 2026-09-25: both request fields reach it."""
    return 200, _answer(body, honours=True)


def loopback(responder, **kwargs) -> dict[str, bool]:
    """`probe` over real HTTP on a loopback port, through the shipped transport."""
    from llossless import transport
    from fake_endpoint import FakeEndpoint
    with FakeEndpoint(responder) as base_url:
        def send(body: dict) -> dict:
            return json.loads(transport.post_json(
                f"{base_url}/chat/completions", body, api_key=None, timeout=10,
                ca_bundle=None, host="loopback", model=body["model"]).body)
        return probe(send, model="test-model", profile="anthropic", **kwargs)


def self_test() -> int:
    failures: list[str] = []
    dropped = loopback(ignoring)
    if dropped != {"json_schema": False, "tool_call": False, "prompt": True}:
        failures.append(f"an endpoint that drops the fields must fire on both, got {dropped}")
    carried = loopback(honouring)
    if carried != dict.fromkeys(structured.TIERS, True):
        failures.append(f"an endpoint that honours them must not fire, got {carried}")
    for failure in failures:
        print(f"  - {failure}")
    print("schema carriage: " + ("FAIL" if failures else "self-test passes"))
    return 1 if failures else 0


# -- the paid probe ------------------------------------------------------------

def run(sku: str, tiers: list[str], *, state_path: Path, violate: bool) -> int:
    import spend
    import source_guard
    from llossless import transport

    vendor, model = sku.split("/", 1)
    spend.price_for(sku)  # an unpriced SKU aborts before anything is sent
    key_name = {"anthropic": "ANTHROPIC_API_KEY"}[vendor]
    api_key = next(line.split("=", 1)[1].strip().strip('"')
                   for line in (HERE.parent / ".env").read_text("utf-8").splitlines()
                   if line.startswith(key_name + "="))
    state = (json.loads(state_path.read_text("utf-8")) if state_path.exists()
             else {"rows": [], "results": []})
    ledger = spend.Ledger(spend.Caps(spend={vendor: CAP}, calls=24, tokens=60_000,
                                     interval={vendor: 0.0}))
    for row in state["rows"]:  # every earlier call of this probe counts against the cap
        ledger.spent.calls += 1
        ledger.spent.input_tokens += row["input_tokens"]
        ledger.spent.output_tokens += row["output_tokens"]
        ledger.spent.dollars[vendor] = ledger.spent.dollars.get(vendor, 0.0) + row["dollars"]
    ledger.rows = list(state["rows"])
    for tier in tiers:
        body = request(tier, model, profile="anthropic", violate=violate)
        result = {"sku": sku, "tier": tier, "violate": violate, "fields": sorted(body)}
        with ledger.call(vendor, sku, input_estimate=600, output_allowance=MAX_TOKENS,
                         documents=source_guard.NO_DOCUMENT) as charge:
            try:
                envelope = json.loads(transport.post_json(
                    f"{ENDPOINT[vendor]}/chat/completions", body, api_key=api_key,
                    timeout=120, ca_bundle=None, host=vendor, model=model).body)
                usage = envelope.get("usage") or {}
                charge(input_tokens=usage.get("prompt_tokens"),
                       output_tokens=usage.get("completion_tokens"))
                message = envelope["choices"][0]["message"]
                result.update(finish_reason=envelope["choices"][0].get("finish_reason"),
                              content=message.get("content"),
                              tool_calls=message.get("tool_calls"),
                              schema_seen=schema_seen(tier, envelope))
            except Exception as exc:  # noqa: BLE001 - recorded, not hidden
                result["error"] = f"{type(exc).__name__}: {getattr(exc, 'status', '')}"
        result["dollars"] = ledger.rows[-1]["dollars"]
        state["rows"], state["results"] = ledger.rows, state["results"] + [result]
        state_path.write_text(json.dumps(state, indent=1) + "\n", encoding="utf-8")
        print(json.dumps(result)[:600])
    print(f"{vendor} charged ${ledger.spent.dollars.get(vendor, 0.0):.6f} of ${CAP:.2f}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--run", nargs="+", metavar=("SKU", "TIER"))
    parser.add_argument("--state", type=Path)
    parser.add_argument("--violate", action="store_true")
    args = parser.parse_args()
    if args.run:
        if not args.state:
            parser.error("--run needs --state")
        return run(args.run[0], args.run[1:], state_path=args.state, violate=args.violate)
    return self_test()


if __name__ == "__main__":
    sys.exit(main())
