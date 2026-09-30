#!/usr/bin/env python3
"""Assert one draw against the bar frozen at DECISIONS 160, before the next runs.

Adapted from the entry 156 gate. Two differences, both forced by what this arm
is registered to be allowed to do:

  exit codes  0 and 1 are both completions. Exit 1 is what every arm of the
              2026-08-28 sweep returned on this corpus, and the K=3 arms of
              entry 159 returned 0 and 1 between them. Only 2 is the failure
              branch, and the failure branch is a registered outcome here, not
              a reason to stop the chain.

  no report   at exit 2 the tool writes no report.json and a zero-byte
              report.md, so provenance does not exist to assert against. That
              is a property of the outcome. The evidence set becomes the
              driver's own captures and the tool's error line, which names the
              model, the stage, the tier and the thinking state in prose.

The error line is quotable at all only because of entry 158: before the label
reached the error path it carried the pod hostname. So this gate asserts, on
every exit-2 draw, that the line names the endpoint id and does not name the
host. A redaction nobody checks is a belief.

    assert_draw.py <armdir> <label> <model> <expect-thinking:yes|no> <order> <exitcode>
"""
import json, sys
from pathlib import Path

armdir, label, model, expect_think, order, code = (
    Path(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4] == "yes",
    sys.argv[5], int(sys.argv[6]))

ENDPOINT_ID = "29d412c5e668"
HOST = "<redacted>"
STAGES = ["decompose", "merge", "verify"]
BASELINE = ["merge"]

bad = []
def want(ok, why):
    if not ok:
        bad.append(why)

stderr = (armdir / "stderr.log").read_text(encoding="utf-8", errors="replace")

# Entry 158, on every draw of either branch: the label is set, so no message
# this run produced may name the host.
want(HOST not in stderr,
     f"stderr names the host; the label was set and entry 158 says it must not")

before = (armdir / "cache-before.txt").read_text(encoding="utf-8").strip()
after = (armdir / "cache-after.txt").read_text(encoding="utf-8").strip()
want(before and before == after,
     f"the response cache changed across the draw: {before[:12]} -> {after[:12]}. "
     f"--no-cache means neither read nor written; a draw that wrote to it may "
     f"also have read from it, and cache_hits only sees the read")

if code == 2:
    # The registered failure branch. Nothing is asserted into existence here --
    # what is asserted is that the failure is the one that was registered, and
    # that the record of it is complete enough to quote.
    want(not (armdir / "report.json").exists(),
         "exit 2 wrote a report.json; that is not the branch this describes")
    want(ENDPOINT_ID in stderr,
         f"stderr must name the endpoint id {ENDPOINT_ID} so the line can be "
         f"quoted and joined to the run; got {stderr[-300:]!r}")
    for word in (model, "empty"):
        want(word in stderr, f"the error line must name {word!r}")
    want("decompose" in stderr or "merge" in stderr,
         "the error line must name the stage that returned nothing")
    summary = (f"{label}: EXIT 2, no report, endpoint={ENDPOINT_ID}, "
               f"report.md {(armdir / 'report.md').stat().st_size} bytes")
elif code in (0, 1):
    blob = json.loads((armdir / "report.json").read_text(encoding="utf-8"))
    prov = blob.get("provenance") or {}
    counts, tier = prov.get("counts") or {}, prov.get("structured_output") or {}
    decoding, policy = prov.get("decoding") or {}, prov.get("merge_policy") or {}
    models, endpoint = prov.get("models") or {}, prov.get("endpoint") or {}

    want(tier.get("mode") == "json_schema", f"tier mode is {tier.get('mode')!r}")
    want(tier.get("how") == "pinned", f"tier arrived as {tier.get('how')!r}, bar says pinned")
    want(tier.get("field_order") == order, f"field_order is {tier.get('field_order')!r}")
    want(counts.get("cache_hits") == 0,
         f"cache_hits is {counts.get('cache_hits')!r}; a hit means this draw "
         "answered from disk and is not a draw")
    want(counts.get("replayed") == 0, f"replayed is {counts.get('replayed')!r}")
    want(prov.get("run_mode") == "live", f"run_mode is {prov.get('run_mode')!r}")
    want(decoding.get("temperature") == 0.0, f"temperature is {decoding.get('temperature')!r}")
    want(decoding.get("seed") == 0, f"seed is {decoding.get('seed')!r}")
    think = sorted(decoding.get("thinking") or [])
    want(think == (STAGES if expect_think else BASELINE),
         f"thinking is {think!r}, bar says {STAGES if expect_think else BASELINE!r}")
    want(policy.get("fidelity") == "off", f"fidelity is {policy.get('fidelity')!r}")
    want(policy.get("base") == "source_a.md", f"base is {policy.get('base')!r}")
    want(set(models.values()) == {model}, f"models are {models!r}")
    want(endpoint.get("id") == ENDPOINT_ID,
         f"endpoint id is {endpoint.get('id')!r}, label says {ENDPOINT_ID}")
    summary = (f"{label}: {tier.get('mode')}/{tier.get('how')} order={tier.get('field_order')} "
               f"calls={counts.get('calls')} cache_hits={counts.get('cache_hits')} "
               f"thinking={len(think)} endpoint={endpoint.get('id')} exit={code}")
else:
    bad.append(f"exit {code} is neither a completion (0, 1) nor the registered "
               f"failure branch (2); the bar does not describe this draw")
    summary = f"{label}: UNREGISTERED EXIT {code}"

print(summary)
if bad:
    print(f"DRAW ASSERTION FAILED for {label}:", file=sys.stderr)
    for why in bad:
        print(f"  - {why}", file=sys.stderr)
    sys.exit(9)
