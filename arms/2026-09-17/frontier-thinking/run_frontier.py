"""Frontier arms on the same pairs, levels and flags Phase 4 used.

Joins directly onto `2026-09-16-phase4/results.json`: same three operator pairs,
same two fidelity levels, same `--no-cache`, so the Qwen 27B and 8B rows are
comparators rather than a separate experiment. Qwen is NOT re-run - the operator
pays per minute for that endpoint and has ruled it out for now.

Priority, in the operator's words: prove the tool works on frontier models. If it
breaks there, that is the finding. Cost is guarded below and the run stops rather
than overrunning it.
"""
import json, os, pathlib, re, shutil, subprocess, sys, time, collections

B = pathlib.Path(__file__).resolve().parent
PAIRS_ROOT = pathlib.Path("<home>/Documents/Dev/claude-tmp/claimcheck")
REPO = pathlib.Path("<home>/Documents/Dev/vibe-coding/claimcheck")
RESULTS = B / "results.json"
BUDGET_USD = 4.00      # hard stop. Reasoning tokens are the unknown here.

PAIRS = {"toby-test-2": ("chickens_1.md", "chickens_2.md"),
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
    ("gpt-5.6-terra", "gpt-5.6-terra", "https://api.openai.com/v1",
     "OPEN_AI_API_KEY", "openai-reasoning", 2.00, 12.00, "prompt"),
    ("claude-haiku-4-5", "claude-haiku-4-5-20251001", "https://api.anthropic.com/v1",
     "ANTHROPIC_API_KEY", "anthropic", 1.00, 5.00, "json_schema"),
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
            for level in ("low", "high"):
                if spent() >= BUDGET_USD:
                    print(f"\nBUDGET STOP: ${spent():.2f} >= ${BUDGET_USD}")
                    raise SystemExit(0)
                run(label, model, base, keyenv, profile, pin, pout, tier, pair, level)
    print(f"\nfrontier arms complete, total ${spent():.2f}")
