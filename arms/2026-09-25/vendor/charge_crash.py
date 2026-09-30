#!/usr/bin/env python3
"""Book an attempt a machine crash interrupted, so it counts against the cap and never the figures.

The four calls the ledger charged stay as they are, relabelled to the crashed
attempt. The call in flight at the crash never reported; it is charged the
estimate, as a failed call is (REGISTRATION.md, "Money"). The runner's results
get a row saying the attempt was interrupted, which no figure counts.
"""
import json, os, shutil, sys
from datetime import datetime, timezone
from pathlib import Path
D = Path(os.environ["BENCH_DIR"]); TREE = Path(os.environ["BENCH_TREE"])
sys.path.insert(0, str(TREE / "tests")); sys.path.insert(0, str(TREE / "src"))
sys.path.insert(0, str(Path(__file__).parent))
import spend, ledger_cli
label, arm, pair, sku = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
crashed = label + "-crashed"
state_path = D / "ledger_openai.json"
state = ledger_cli.load_state(state_path)
mine = [r for r in state["rows"] if r.get("cell") == label]
assert mine, f"no ledger rows for {label}"
for r in mine:
    r["cell"] = crashed
ledger = spend.Ledger(ledger_cli.CAPS)
for row in state["rows"]:
    ledger.spent.calls += 1; ledger.spent.input_tokens += row["input_tokens"]
    ledger.spent.output_tokens += row["output_tokens"]
    ledger.spent.dollars[row["vendor"]] = ledger.spent.dollars.get(row["vendor"], 0.0) + row["dollars"]
ledger.rows = list(state["rows"])
docs = [(TREE / "tests" / "pairs" / pair / n).read_text() for n in ("source_a.md", "source_b.md")]
largest_input = max(r["input_tokens"] for r in mine)
with ledger.call("openai", sku, input_estimate=largest_input,
                 output_allowance=ledger_cli.ALLOWANCE["openai"], documents=docs) as charge:
    charge(input_tokens=None, output_tokens=None)
ledger.rows[-1].update({"cell": crashed, "path": "/chat/completions", "failed": "machine_crash",
                        "lost_in_crash": True})
state["rows"] = ledger.rows
ledger_cli.save_state(state_path, state)
cell = D / "cells" / label
if cell.exists():
    shutil.move(str(cell), str(D / "cells" / crashed))
booked = [r for r in state["rows"] if r.get("cell") == crashed]
row = {"arm": arm, "model": sku.split("/", 1)[1], "pair": pair, "draw": 1, "fidelity": "high",
       "verify_depth": "full", "exit_code": None, "report": False, "interrupted": "machine_crash",
       "label": crashed, "ledger_calls": len(booked) - 1, "ledger_lost_calls": 1,
       "ledger_usd": round(sum(r["dollars"] for r in booked), 6),
       "recorded_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "problems": []}
res = D / f"results_{arm}.json"
data = json.loads(res.read_text()); data.append(row); res.write_text(json.dumps(data, indent=1))
print(json.dumps(row))
print(f"openai ledger now ${sum(r['dollars'] for r in state['rows']):.4f}")
