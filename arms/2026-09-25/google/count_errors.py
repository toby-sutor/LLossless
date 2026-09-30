#!/usr/bin/env python3
"""Per model, how many Google requests got a 429 or a 503, in the pilot and in the measured run.

Reads the two state files the harness wrote (pilot/pilot_state.json, one row
per attempt; ledger_google.json, one row per attempt) and writes
error_counts.json beside them. The two native `generateContent` calls of
native_once.py printed their answer and wrote no state; they are added by hand
below, as the only attempts not in either file, and named as such.
"""
import collections
import json
import sys
from pathlib import Path

D = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent)
pilot = json.loads((D / "pilot" / "pilot_state.json").read_text()) \
    if (D / "pilot" / "pilot_state.json").exists() else json.loads((D / "pilot_state.json").read_text())
ledger = json.loads((D / "ledger_google.json").read_text())


def model_of_cell(cell: str) -> str:
    return "gemini-3.8-flash" if "gemini-3.8-flash" in cell else "gemini-3.5-flash-lite"


out = {}
for phase, rows in (("pilot", [(c["model"], c["status"]) for c in pilot["calls"]]),
                    ("measured", [(model_of_cell(r["cell"]), r.get("status") or r.get("failed"))
                                  for r in ledger["rows"]])):
    for model, status in rows:
        entry = out.setdefault(model, {}).setdefault(phase, collections.Counter())
        entry[str(status)] += 1
# native_once.py, 2026-09-25 ~18:02 and ~18:09 UTC: one call each, both 503.
out.setdefault("gemini-3.8-flash", {}).setdefault("native_once", collections.Counter())["503"] += 1
out.setdefault("gemini-3.1-flash-lite", {}).setdefault("native_once", collections.Counter())["503"] += 1

summary = {}
for model, phases in sorted(out.items()):
    total = collections.Counter()
    for counts in phases.values():
        total.update(counts)
    summary[model] = {"by_phase": {p: dict(sorted(c.items())) for p, c in phases.items()},
                      "requests": sum(total.values()), "http_429": total.get("429", 0),
                      "http_503": total.get("503", 0), "answered_200": total.get("200", 0)}
(D / "error_counts.json").write_text(json.dumps(summary, indent=1) + "\n")
for model, s in summary.items():
    print(f"{model}: {s['requests']} requests, {s['answered_200']} answered, "
          f"{s['http_429']} x 429, {s['http_503']} x 503  {s['by_phase']}")
