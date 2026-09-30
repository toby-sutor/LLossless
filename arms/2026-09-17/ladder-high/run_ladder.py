"""Up the ladder: sonnet-5 and opus-5 on `high` only, against the editor references.

`high` is the default and the product - the operator's own expected merges are
what they would expect at `high`, and `low` delivers the literal merge this tool
exists to flag. So this arm runs one rung, not two, and adds `toby-test-1` now
that it carries a reference too.

Ranked on **silent loss first** - dropping content and declaring it is
acceptable, dropping it silently is the defect the tool exists to catch - then
band deviation against the reference, then cost, then speed.

Both SKUs are confirmed by the capability sweep to drive all three roles, and
both report `structured_outputs: true`, so the tier is pinned to `json_schema`
as on haiku over the same endpoint and profile.
"""
import json, os, pathlib, re, shutil, subprocess, sys, time, collections

B = pathlib.Path(__file__).resolve().parent
PAIRS_ROOT = pathlib.Path("<home>/Documents/Dev/claude-tmp/claimcheck")
REPO = pathlib.Path("<home>/Documents/Dev/vibe-coding/claimcheck")
RESULTS = B / "results.json"
BUDGET_USD = 5.00      # hard stop. Sonnet ~$0.20/merge, Opus ~$0.55 projected.

PAIRS = {"toby-test-1": ("chris_birthday_1.md", "chris_birthday_2.md"),
         "toby-test-2": ("chickens_1.md", "chickens_2.md"),
         "toby-test-4": ("christianity_1.md", "christianity_2.md"),
         "toby-test-5": ("curry_1.md", "curry_2.md")}

def env_value(name):
    for l in (REPO / ".env").read_text().splitlines():
        n, _, v = l.strip().partition("=")
        if n.strip() == name:
            return v.strip().strip("'\"")
    raise SystemExit(f"{name} not in .env")

# (label, model, base_url, key env name in .env, profile, $in/1M, $out/1M)
# The last element is the structured-output tier, PINNED per arm rather than
# probed. Two reasons, and the second is the one that matters.
#
# `gpt-5.6-terra` with thinking ON cannot carry the `tool_call` rung at all:
# OpenAI applies its own default `reasoning_effort` when none is sent, and
# "Function tools with reasoning_effort are not supported ... in
# /v1/chat/completions" is a 400. `structured.py:329` guards that rung, but the
# guard sits inside `if not thinking`, so it does not fire here. Measured
# 2026-09-17, one 3.2s failure.
#
# And it holds the tier constant against each arm's own thinking-off
# comparator, so thinking is the only variable between the two runs. The
# comparators probed to `prompt` on terra and held `json_schema` on haiku.
ARMS = [
    ("claude-sonnet-5", "claude-sonnet-5", "https://api.anthropic.com/v1",
     "ANTHROPIC_API_KEY", "anthropic", 2.00, 10.00, "json_schema"),
    ("claude-opus-5", "claude-opus-5", "https://api.anthropic.com/v1",
     "ANTHROPIC_API_KEY", "anthropic", 5.00, 25.00, "json_schema"),
]

def spent():
    if not RESULTS.exists():
        return 0.0
    return sum(r.get("cost_usd") or 0.0 for r in json.loads(RESULTS.read_text()))

def record(row):
    data = json.loads(RESULTS.read_text()) if RESULTS.exists() else []
    data.append(row)
    RESULTS.write_text(json.dumps(data, indent=2))

def run(label, model, base, keyenv, profile, pin, pout, tier, pair, level):
    a, b = PAIRS[pair]
    work = B / f"{pair}-{level}-{label}"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    for f in (a, b):
        shutil.copy(PAIRS_ROOT / pair / f, work / f)
    env = {**os.environ,
           "PYTHONPATH": str(REPO / "src"),
           "VENDOR_KEY_FOR_RUN": env_value(keyenv),
           "CLAIMCHECK_API_KEY_ENV": "VENDOR_KEY_FOR_RUN",
           "CLAIMCHECK_BASE_URL": base,
           "CLAIMCHECK_MODEL": model,
           "CLAIMCHECK_MERGE_MODEL": model,
           "CLAIMCHECK_WINDOW": "32768",
           "CLAIMCHECK_PROFILE": profile,
           "CLAIMCHECK_TIMEOUT": "600",
           "CLAIMCHECK_THINKING": "decompose,merge,verify",
           "CLAIMCHECK_STRUCTURED": tier,
           "CLAIMCHECK_ENDPOINT_LABEL": label}
    argv = [sys.executable, "-m", "claimcheck", "merge", a, b, "--base", a,
            "--fidelity", level, "--no-cache",
            "--json", str(work / "report.json"), "-o", str(work / "merged.md")]
    print(f"  [{label} {pair} {level}] start", flush=True)
    t0 = time.time()
    p = subprocess.run(argv, capture_output=True, text=True, env=env, cwd=str(work))
    secs = round(time.time() - t0, 1)
    row = {"arm": label, "model": model, "pair": pair, "fidelity": level,
           "tier_pinned": tier,
           "exit_code": p.returncode, "wall_seconds": secs}
    rp = work / "report.json"
    if rp.exists():
        rep = json.loads(rp.read_text())
        prov = rep.get("provenance") or {}
        tok = prov.get("tokens") or {}
        ti, to = tok.get("input", 0), tok.get("output", 0)
        merged = [c for c in rep.get("claims", []) if c.get("source") == "merged.md"]
        texts = collections.Counter(c["text"] for c in merged)
        lines = collections.defaultdict(set)
        for c in merged:
            lines[c["text"]].add(c.get("line"))
        st = (rep.get("structural") or {}).get("findings", [])
        rc = (rep.get("restated_claims") or {}).get("findings", [])
        src = sum(len((PAIRS_ROOT / pair / f).read_text()) for f in (a, b))
        md = work / "merged.md"
        row |= {"tokens_in": ti, "tokens_out": to,
                "cost_usd": round(ti * pin / 1e6 + to * pout / 1e6, 4),
                "calls_by_role": prov.get("calls_by_role"),
                "claims_extracted": (rep.get("coverage") or {}).get("extracted", len(rep.get("claims", []))),
                "merged_claims": len(merged),
                "cross_line_repeats": sum(1 for t, n in texts.items()
                                          if n > 1 and len(lines[t]) > 1),
                "structural_findings": len(st),
                "restated_findings": len(rc),
                "claim_findings": len(rep.get("findings") or []),
                "length_ratio": round(len(md.read_text()) / src, 3) if md.exists() else None,
                "errors": (rep.get("provenance") or {}).get("errors"),
                # Entry 348's rule: measure the thinking condition, do not
                # declare it. `decoding.thinking` is what was asked for;
                # `wire_thinking` is derived from `"reasoning_effort" not in
                # body` on the request actually sent (client.py:1176-1180).
                "thinking_asked": (prov.get("decoding") or {}).get("thinking"),
                "wire_thinking": (prov.get("decoding") or {}).get("wire_thinking"),
                "reasoned_anyway": (prov.get("decoding") or {}).get("reasoned_anyway"),
                "reasoning_tokens": tok.get("thought")}
    else:
        (work / "stderr.txt").write_text(p.stderr or "")
        row["note"] = "no report"
        row["stderr_tail"] = (p.stderr or "")[-300:]
    record(row)
    print(f"  [{label} {pair} {level}] exit={row['exit_code']} "
          f"cost=${row.get('cost_usd', 0):.3f} xrep={row.get('cross_line_repeats')} "
          f"{secs}s  running total ${spent():.2f}", flush=True)

if __name__ == "__main__":
    for label, model, base, keyenv, profile, pin, pout, tier in ARMS:
        for pair in PAIRS:
            for level in ("high",):
                if spent() >= BUDGET_USD:
                    print(f"\nBUDGET STOP: ${spent():.2f} >= ${BUDGET_USD}")
                    raise SystemExit(0)
                run(label, model, base, keyenv, profile, pin, pout, tier, pair, level)
    print(f"\nfrontier arms complete, total ${spent():.2f}")
