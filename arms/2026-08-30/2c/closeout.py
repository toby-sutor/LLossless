#!/usr/bin/env python3
"""Brief O v3 item 4, per arm, read back from the record rather than retyped.

Every column here comes out of report.json's provenance block or out of the
/api/ps snapshots the arm took either side of itself. Nothing is carried in
from the session's narration: the point of the close-out is that the record
can produce it without me.

The tier assertion is the one that has to be mechanical. The tier latches down
and persists, so an arm that dropped from json_schema to tool_call mid-run
would still finish and still look finished; only structured_output.how ==
"pinned" and mode == "json_schema" read back together say it did not drift.
"""
import json, sys
from pathlib import Path

SP = Path(__file__).resolve().parent
ARMS = ["A1-27b-default", "B1-70b-default", "C2-120b-think"]


def kinds(report):
    out = {}
    for f in report["structural"]["findings"]:
        out[f["kind"]] = out.get(f["kind"], 0) + 1
    return out


def digests(d, model):
    seen = {}
    for when in ("before", "after"):
        p = d / f"ps-{when}.json"
        if not p.exists():
            continue
        for e in json.loads(p.read_text()).get("models", []):
            if e["name"] == model:
                seen[when] = e["digest"]
    return seen


rows = []
for arm in ARMS:
    d = SP / arm
    rp = d / "report.json"
    if not rp.exists():
        rows.append({"arm": arm, "status": "no report.json"})
        continue
    r = json.loads(rp.read_text())
    pv = r["provenance"]
    model = pv["models"]["merge"]
    seen = digests(d, model)
    drift = len(set(seen.values())) > 1
    so = pv["structured_output"]
    row = {
        "arm": arm,
        "model": model,
        "digest": (sorted(set(seen.values())) or [None])[0],
        "digest_seen_at": sorted(seen),
        "digest_moved_mid_arm": drift,
        "wall_seconds": pv["duration_seconds"],
        "tokens_in": pv["tokens"]["input"],
        "tokens_out": pv["tokens"]["output"],
        "measured_calls": pv["tokens"]["measured_calls"],
        "unmeasured_calls": pv["tokens"]["unmeasured_calls"],
        "schema_repairs": pv["counts"]["schema_repairs"],
        "errors": pv["counts"]["errors"],
        "model_loads": pv["counts"]["model_loads"],
        "tier_mode": so["mode"],
        "tier_how": so["how"],
        "tier_held": so["mode"] == "json_schema" and so["how"] == "pinned",
        "field_order": so["field_order"],
        "thinking": pv["decoding"]["thinking"],
        "temperature": pv["decoding"]["temperature"],
        "seed": pv["decoding"]["seed"],
        "commit": pv["claimcheck_commit"],
        "segments": r["structural"]["segments"],
        "structural_findings": len(r["structural"]["findings"]),
        "by_kind": kinds(r),
        "declared_drops": r["declared_loss"]["drops"],
        "over_budget": r["declared_loss"]["over_budget"],
        "verify_findings": len(r["findings"]),
        "exit_code": r["exit_code"],
    }
    row["undeclared_absence"] = row["by_kind"].get("undeclared_absence", 0)
    rows.append(row)

print(json.dumps(rows, indent=1))
(SP / "closeout.json").write_text(json.dumps(rows, indent=1))

bad = [r for r in rows if r.get("status") or r.get("digest_moved_mid_arm")
       or not r.get("tier_held")]
if bad:
    print("\nNOT CLEAN:", [r["arm"] for r in bad], file=sys.stderr)
    sys.exit(1)
commits = {r["commit"] for r in rows}
if len(commits) > 1:
    print(f"\nHEAD MOVED BETWEEN ARMS: {commits}", file=sys.stderr)
    sys.exit(1)
print(f"\nall three arms clean, one commit {commits.pop()}, tier pinned throughout")
