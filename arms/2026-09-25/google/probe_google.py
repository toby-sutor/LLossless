#!/usr/bin/env python3
"""The Google pilot: which request fields and which structured tiers Gemini's
OpenAI-compatible endpoint accepts, free tier only, one small call at a time.

    probe_google.py MODEL STEP [STEP ...] --state STATE.json

Every call goes through tests/spend.py's Ledger at Google's $0.00 cap, on a
free-tier SKU the harness prices at zero (`google-free/<model>`), and is paced
serially. Raw status, headers of interest and body are kept for every attempt,
a 429 included, because a free-tier 429 names the quota it hit.
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(os.environ.get("BENCH_REPO", "<home>/Documents/Dev/vibe-coding/claimcheck"))
sys.path.insert(0, str(REPO / "tests"))
sys.path.insert(0, str(REPO / "src"))
import spend  # noqa: E402
import source_guard  # noqa: E402
from claimcheck import structured  # noqa: E402

BASE = "https://generativelanguage.googleapis.com/v1beta/openai"
PACE = float(os.environ.get("PROBE_PACE", "15"))
FREE_SOURCE = ("https://ai.google.dev/gemini-api/docs/pricing, Free Tier column: "
               "\"Free of charge\" for input and output")

MARKER_KEY, MARKER_VALUE = "zq_token", "PLUM-4471"
SCHEMA = {"type": "object",
          "properties": {MARKER_KEY: {"type": "string", "enum": [MARKER_VALUE]},
                         "greeting": {"type": "string"}},
          "required": [MARKER_KEY, "greeting"], "additionalProperties": False}
SHOWN = "Greet me in one short sentence. Reply with one JSON object."
PLAIN = [{"role": "user", "content": "Say hello in three words."}]


def key() -> str:
    for line in (REPO / ".env").read_text().splitlines():
        k, _, v = line.strip().partition("=")
        if k.strip().removeprefix("export ").strip() == "GOOGLE_AI_API_KEY":
            return v.strip().strip("'\"")
    raise SystemExit("GOOGLE_AI_API_KEY not in .env")


def steps(model: str) -> dict[str, dict]:
    tier = lambda t, thinking=True: structured.build_body(  # noqa: E731
        tier=t, model=model, messages=[{"role": "user", "content": SHOWN}], schema=SCHEMA,
        schema_name="probe", max_tokens=2000, thinking=thinking, profile="google")
    return {
        "plain": {"model": model, "messages": PLAIN},
        "temperature": {"model": model, "messages": PLAIN, "temperature": 0.0},
        "seed": {"model": model, "messages": PLAIN, "seed": 0},
        "max_tokens": {"model": model, "messages": PLAIN, "max_tokens": 2000},
        "max_completion_tokens": {"model": model, "messages": PLAIN,
                                  "max_completion_tokens": 2000},
        "effort_none": {"model": model, "messages": PLAIN, "reasoning_effort": "none"},
        "effort_low": {"model": model, "messages": PLAIN, "reasoning_effort": "low"},
        "effort_minimal": {"model": model, "messages": PLAIN, "reasoning_effort": "minimal"},
        "default_body": {"model": model, "messages": PLAIN, "temperature": 0.0, "seed": 0,
                         "max_tokens": 2000},
        "json_schema": tier("json_schema"),
        "tool_call": tier("tool_call"),
        "prompt": tier("prompt"),
    }


def schema_seen(t: str, env: dict) -> bool | None:
    try:
        text = structured.read_content(t, env)
    except structured.TierUnsupported:
        return None
    return MARKER_KEY in text and MARKER_VALUE in text


def main() -> int:
    model = sys.argv[1]
    names = [a for a in sys.argv[2:] if not a.startswith("--")]
    state_path = Path(sys.argv[sys.argv.index("--state") + 1])
    names = [n for n in names if n != str(state_path)]
    sku = f"probe/google-free/{model}"
    spend.PRICES[sku] = spend.Price(input=0.0, output=0.0, source=FREE_SOURCE,
                                    read_on="2026-09-25")
    state = json.loads(state_path.read_text()) if state_path.exists() else {"rows": [], "calls": []}
    ledger = spend.Ledger(spend.Caps(spend={"google": 0.00}, calls=200, tokens=2_000_000,
                                     interval={"google": 0.0}))
    for row in state["rows"]:
        ledger.spent.calls += 1
        ledger.spent.dollars["google"] = ledger.spent.dollars.get("google", 0.0) + row["dollars"]
    ledger.rows = list(state["rows"])
    api_key = key()
    table = steps(model)
    for name in names:
        body = table[name]
        rec = {"model": model, "step": name, "fields": sorted(body),
               "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
        with ledger.call("google", sku, input_estimate=800, output_allowance=2000,
                         documents=source_guard.NO_DOCUMENT) as charge:
            req = urllib.request.Request(f"{BASE}/chat/completions",
                                         data=json.dumps(body).encode(),
                                         headers={"Content-Type": "application/json",
                                                  "Authorization": "Bearer " + api_key})
            t0 = time.monotonic()
            try:
                with urllib.request.urlopen(req, timeout=180) as r:
                    status, raw = r.status, r.read().decode()
            except urllib.error.HTTPError as exc:
                status, raw = exc.code, exc.read().decode(errors="replace")
            rec["seconds"] = round(time.monotonic() - t0, 2)
            rec["status"] = status
            try:
                env = json.loads(raw)
            except ValueError:
                env = {"_raw": raw[:2000]}
            rec["response"] = env
            usage = env.get("usage") if isinstance(env, dict) else None
            if status == 200 and usage:
                charge(input_tokens=usage.get("prompt_tokens"),
                       output_tokens=usage.get("completion_tokens"))
                rec["usage"] = usage
            else:
                charge(input_tokens=0, output_tokens=0)  # a free SKU: zero either way
            if status == 200 and name in ("json_schema", "tool_call", "prompt",
                                          "json_schema_off", "tool_call_off"):
                t = name.removesuffix("_off")
                rec["schema_seen"] = schema_seen(t, env)
        rec["dollars"] = ledger.rows[-1]["dollars"]
        state["rows"] = ledger.rows
        state["calls"].append(rec)
        state_path.write_text(json.dumps(state, indent=1))
        msg = env.get("error", {}) if isinstance(env, dict) else env
        print(f"{model} {name}: HTTP {status} {rec['seconds']}s usage={rec.get('usage')} "
              f"seen={rec.get('schema_seen')} err={str(msg)[:400]}", flush=True)
        time.sleep(PACE)
    print(f"google charged ${ledger.spent.dollars.get('google', 0.0):.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
