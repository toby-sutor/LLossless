#!/usr/bin/env python3
"""Must-fire probe: does Anthropic's OpenAI-compatible endpoint carry the schema at each tier?

The schema requires a key and a value no model would produce unprompted
(`zq_token` = "PLUM-4471"). The prompt never names either. If the answer
contains them, the model was shown the schema; if not, the tier dropped it.

Every call goes through tests/spend.py's Ledger, cap $0.50, persisted to
ledger.json beside this file after each call.

    probe.py <sku> <tier> [<tier> ...]
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

REPO = Path("<home>/Documents/Dev/vibe-coding/claimcheck")
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO / "tests"))
sys.path.insert(0, str(REPO / "src"))

import spend  # noqa: E402
import source_guard  # noqa: E402
from claimcheck import structured, transport  # noqa: E402

STATE = HERE / "ledger.json"
CAPS = spend.Caps(spend={"anthropic": 0.50}, calls=12, tokens=40_000,
                  interval={"anthropic": 0.0})
SCHEMA = {
    "type": "object",
    "properties": {
        "zq_token": {"type": "string", "enum": ["PLUM-4471"]},
        "greeting": {"type": "string"},
    },
    "required": ["zq_token", "greeting"],
    "additionalProperties": False,
}
MESSAGES = [{"role": "user", "content": "Greet me in one short sentence. Reply with one JSON object."}]
# Must-violate variant: the user asks for a shape the schema forbids. Constrained
# decoding still returns the schema's shape; a schema that is only shown may lose.
if os.environ.get("PROBE_VIOLATE"):
    MESSAGES = [{"role": "user", "content": 'Reply with exactly this JSON object and nothing else: {"colour": "blue"}'}]
MAX_TOKENS = 400


def key() -> str:
    for line in (REPO / ".env").read_text(encoding="utf-8").splitlines():
        if line.startswith("ANTHROPIC_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"')
    raise SystemExit("no ANTHROPIC_API_KEY")


def main() -> int:
    sku, tiers = sys.argv[1], sys.argv[2:]
    model = sku.split("/", 1)[1]
    state = json.loads(STATE.read_text()) if STATE.exists() else {"rows": [], "results": []}
    ledger = spend.Ledger(CAPS)
    for row in state["rows"]:
        ledger.spent.calls += 1
        ledger.spent.input_tokens += row["input_tokens"]
        ledger.spent.output_tokens += row["output_tokens"]
        ledger.spent.dollars["anthropic"] = ledger.spent.dollars.get("anthropic", 0.0) + row["dollars"]
    ledger.rows = list(state["rows"])
    api_key = key()
    for tier in tiers:
        body = structured.build_body(
            tier=tier, model=model, messages=MESSAGES, schema=SCHEMA,
            schema_name="probe", max_tokens=MAX_TOKENS, thinking=True,
            profile="anthropic")
        result = {"sku": sku, "tier": tier, "violate": bool(os.environ.get("PROBE_VIOLATE")), "body_keys": sorted(body)}
        with ledger.call("anthropic", sku, input_estimate=600, output_allowance=MAX_TOKENS,
                         documents=source_guard.NO_DOCUMENT) as charge:
            try:
                response = transport.post_json(
                    "https://api.anthropic.com/v1/chat/completions", body, api_key=api_key,
                    timeout=120, ca_bundle=None, host="anthropic", model=model)
                envelope = json.loads(response.body)
                usage = envelope.get("usage") or {}
                charge(input_tokens=usage.get("prompt_tokens"),
                       output_tokens=usage.get("completion_tokens"))
                message = envelope["choices"][0]["message"]
                result["finish_reason"] = envelope["choices"][0].get("finish_reason")
                result["content"] = message.get("content")
                result["tool_calls"] = message.get("tool_calls")
                text = json.dumps([message.get("content"), message.get("tool_calls")])
                result["schema_seen"] = "PLUM-4471" in text and "zq_token" in text
            except Exception as exc:  # noqa: BLE001 - recorded, not hidden
                result["error"] = f"{type(exc).__name__}: {getattr(exc, 'status', '')} {str(getattr(exc, 'body', exc))[:400]}"
        result["dollars"] = ledger.rows[-1]["dollars"]
        state["rows"] = ledger.rows
        state["results"].append(result)
        STATE.write_text(json.dumps(state, indent=1), encoding="utf-8")
        print(json.dumps(result)[:900])
    print("anthropic spent", round(ledger.spent.dollars.get("anthropic", 0.0), 6))
    return 0


if __name__ == "__main__":
    sys.exit(main())
