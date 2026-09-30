#!/usr/bin/env python3
"""One captured claimcheck request, sent to the native Messages API under the ledger.

    diag_native.py BODY.json MODEL LABEL DOC [DOC...]
Reads the captured chat-completions body, sends its messages to POST /v1/messages
with max_tokens 256 (the question is stop_reason, not the answer), charges the
call to ledger_anthropic.json, and prints stop_reason, stop_details and usage.
"""
import json, os, sys, urllib.request, urllib.error
from pathlib import Path
D = Path(os.environ["BENCH_DIR"]); TREE = Path(os.environ["BENCH_TREE"]); REPO = Path(os.environ["BENCH_REPO"])
sys.path.insert(0, str(TREE / "tests")); sys.path.insert(0, str(TREE / "src"))
import spend
sys.path.insert(0, str(Path(__file__).parent))
import ledger_cli
body_path, model, label, *docs = sys.argv[1:]
payload = json.loads(Path(body_path).read_text())["body"]
key = None
for line in (REPO / ".env").read_text().splitlines():
    k, _, v = line.strip().partition("=")
    if k.strip() == "ANTHROPIC_API_KEY": key = v.strip().strip("'\"")
state_path = D / "ledger_anthropic.json"
state = ledger_cli.load_state(state_path)
ledger = spend.Ledger(ledger_cli.CAPS)
for row in state["rows"]:
    ledger.spent.calls += 1; ledger.spent.input_tokens += row["input_tokens"]
    ledger.spent.output_tokens += row["output_tokens"]
    ledger.spent.dollars[row["vendor"]] = ledger.spent.dollars.get(row["vendor"], 0.0) + row["dollars"]
ledger.rows = list(state["rows"])
documents = [Path(p).read_text() for p in docs]
native = {"model": model, "max_tokens": 256, "messages": payload["messages"]}
data = json.dumps(native).encode()
est_in = len(json.dumps(payload["messages"])) // 3 + 1
result = {}
with ledger.call("anthropic", f"anthropic/{model}", input_estimate=est_in, output_allowance=256,
                 documents=documents) as charge:
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=data, method="POST",
                                 headers={"x-api-key": key, "anthropic-version": "2023-06-01",
                                          "content-type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            result = json.loads(r.read())
    except urllib.error.HTTPError as exc:
        result = {"http_error": exc.code, "body": exc.read().decode()[:500]}
    u = result.get("usage") or {}
    charge(input_tokens=u.get("input_tokens"), output_tokens=u.get("output_tokens"))
ledger.rows[-1].update({"cell": label, "path": "/messages (diagnostic)"})
state["rows"] = ledger.rows; ledger_cli.save_state(state_path, state)
print(json.dumps({"stop_reason": result.get("stop_reason"), "stop_details": result.get("stop_details"),
                  "usage": result.get("usage"), "content_types": [c.get("type") for c in result.get("content", [])],
                  "error": result.get("http_error"), "error_body": result.get("body")}, indent=1))
print(f"ledger anthropic ${ledger.spent.dollars.get('anthropic', 0):.4f}")
