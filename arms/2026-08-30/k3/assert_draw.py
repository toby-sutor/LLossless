#!/usr/bin/env python3
"""Assert one draw against the bar frozen at DECISIONS 156, before the next runs.

Checked here rather than in the close-out because a draw that violated the bar
is not a draw: continuing the chain after one would spend two more hours
producing a record that has to be thrown away. The structured tier in
particular latches down and persists, so a single unpinned draw can rewrite
every later request in the arm.

Read out of `provenance`, not out of the recorded command. `command` is the
subcommand name -- the string "merge" -- so asserting flag spellings against it
would have passed by never matching anything. What the run actually did is in
`decoding`, `structured_output`, `merge_policy` and `counts`.

    assert_draw.py <report.json> <label> <model> <expect-thinking:yes|no> <order>
"""
import json, sys
from pathlib import Path

report, label, model, expect_think, order = (
    Path(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4] == "yes", sys.argv[5])
blob = json.loads(report.read_text(encoding="utf-8"))
prov = blob.get("provenance") or {}
counts = prov.get("counts") or {}
tier = prov.get("structured_output") or {}
decoding = prov.get("decoding") or {}
policy = prov.get("merge_policy") or {}
models = prov.get("models") or {}
endpoint = prov.get("endpoint") or {}

# `--thinking` replaces the default set rather than adding to it, and the
# default set is {merge}. So the "default" arms reason on merge and the think
# arms add decompose and verify. Entry 157; 156 called them "no thinking".
STAGES = ["decompose", "merge", "verify"]
BASELINE = ["merge"]
bad = []
def want(ok, why):
    if not ok:
        bad.append(why)

want(tier.get("mode") == "json_schema", f"tier mode is {tier.get('mode')!r}, bar says json_schema")
want(tier.get("how") == "pinned", f"tier arrived as {tier.get('how')!r}, bar says pinned")
want(tier.get("field_order") == order, f"field_order is {tier.get('field_order')!r}, bar says {order!r}")
want(counts.get("cache_hits") == 0,
     f"cache_hits is {counts.get('cache_hits')!r}; --no-cache is non-negotiable, "
     "a hit means this draw answered from disk and is not a draw")
want(counts.get("replayed") == 0, f"replayed is {counts.get('replayed')!r}")
want(prov.get("run_mode") == "live", f"run_mode is {prov.get('run_mode')!r}")
want(decoding.get("temperature") == 0.0, f"temperature is {decoding.get('temperature')!r}")
want(decoding.get("seed") == 0, f"seed is {decoding.get('seed')!r}")
think = sorted(decoding.get("thinking") or [])
expected = STAGES if expect_think else BASELINE
want(think == expected, f"thinking is {think!r}, bar says {expected!r} for {label}")
want(policy.get("fidelity") == "off", f"fidelity is {policy.get('fidelity')!r}, bar says off")
want(policy.get("base") == "source_a.md", f"base is {policy.get('base')!r}")
want(set(models.values()) == {model}, f"models are {models!r}, bar says {model!r} on every stage")
want(bool(endpoint.get("id")), "no endpoint id stamped")

print(f"{label}: {tier.get('mode')}/{tier.get('how')} order={tier.get('field_order')} "
      f"calls={counts.get('calls')} cache_hits={counts.get('cache_hits')} "
      f"thinking={len(think)} endpoint={endpoint.get('id')} exit={blob.get('exit_code')}")
if bad:
    print(f"DRAW ASSERTION FAILED for {label}:", file=sys.stderr)
    for why in bad:
        print(f"  - {why}", file=sys.stderr)
    sys.exit(9)
