"""Up the ladder: sonnet-5 and opus-5 on `high` only, against the editor references.

`high` is the default and the product - the operator's own expected merges are
what they would expect at `high`, and `low` delivers the literal merge this tool
exists to flag. So this arm runs one rung, not two, and adds `toby-test-1` now
that it carries a reference too.

Ranked on **silent loss first** - dropping content and declaring it is
acceptable, dropping it silently is the defect the tool exists to catch - then
band deviation against the reference, then cost, then speed.

Both SKUs are confirmed by the capability sweep to drive all three roles, and
**The tier is deliberately NOT pinned here.** Pinning `json_schema` killed
`claude-sonnet-5` on `toby-test-2`: nine merge attempts, six of them a 200 with
an empty body, 1252s, and no report - because a pinned tier cannot fall back,
so a rung that fails has no escape. Entry-level rule for pinning ("a flake
re-keys every later request") is about *recording cassettes*; this run is
`--no-cache`, so there are no cassettes to re-key and pinning bought nothing.
The ladder now degrades json_schema -> tool_call -> prompt on its own, and
`tier_used` records where it settled.
"""
import json, os, pathlib, re, shutil, subprocess, sys, time, collections

B = pathlib.Path(__file__).resolve().parent
PAIRS_ROOT = pathlib.Path("<home>/Documents/Dev/claude-tmp/claimcheck")
REPO = pathlib.Path("<home>/Documents/Dev/vibe-coding/claimcheck")
RESULTS = B / "results.json"
BUDGET_USD = 3.00      # operator: the $5 is not a hard cap, the tests are worth finishing.
                       # Kept as a runaway guard only - projected total is ~$4.

PAIRS = {"toby-test-1": ("chris_birthday_1.md", "chris_birthday_2.md")}

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
# Gap-fill only: `gpt-5.6-terra` never ran `toby-test-1`, so that pair has no
# OpenAI comparator. Different vendor from the Anthropic ladder, so this runs
# alongside it without touching its rate limits or its cost accounting.
ARMS = [
    ("gpt-5.6-terra", "gpt-5.6-terra", "https://api.openai.com/v1",
     "OPEN_AI_API_KEY", "openai-reasoning", 2.00, 12.00, "prompt"),
]

def attempt_cost(stderr, pin, pout):
    """Every attempt's tokens, including the ones that produced no report.

    `results.json` derived cost from the final report, so a run that failed
    recorded $0.000 while the vendor billed it. Two failed Sonnet cells cost
    $1.355 that way. The tool dumps every response envelope -- including
    `EmptyResponse` -- with the vendor's own `usage` block, and prints the dump
    directory to stderr, so the real figure is recoverable per run rather than
    only visible later as a balance delta.
    """
    import glob, re as _re
    m = _re.search(r"dumps for this run go to (\S+)", stderr or "")
    if not m:
        return None
    tin = tout = 0
    seen = 0
    for f in glob.glob(m.group(1) + "/*/*.json"):
        try:
            d = json.loads(pathlib.Path(f).read_text())
        except Exception:
            continue
        u = ((d.get("envelope") or {}).get("usage")) or {}
        if u:
            tin += u.get("prompt_tokens", 0)
            tout += u.get("completion_tokens", 0)
            seen += 1
    if not seen:
        return None
    return {"attempts_dumped": seen, "attempt_tokens_in": tin,
            "attempt_tokens_out": tout,
            "attempt_cost_usd": round(tin * pin / 1e6 + tout * pout / 1e6, 4),
            "dump_dir": m.group(1)}

def done_cells():
    """(arm, pair, fidelity) already recorded WITH a report. A resume must not
    re-run a completed cell: `run` rmtree's the work dir first, so a re-run
    would pay for the same measurement twice and append a duplicate row."""
    if not RESULTS.exists():
        return set()
    # "has a report", not "has no note": the note text is prose and I broke this
    # once by rewriting a failure's note, which silently marked the failed cell
    # done and skipped the re-run. `tokens_in` is only ever set from a report
    # that was actually read, so it is the durable predicate.
    return {(r["arm"], r["pair"], r["fidelity"])
            for r in json.loads(RESULTS.read_text())
            if r.get("tokens_in") is not None}

def spent():
    if not RESULTS.exists():
        return 0.0
    # the guard must read what was BILLED, or it is blind exactly when spend
    # runs away: a failing cell reports 0.0 and bills in full.
    return sum(max(r.get("cost_usd") or 0.0, r.get("cost_usd_billed") or 0.0,
                   r.get("attempt_cost_usd") or 0.0)
               for r in json.loads(RESULTS.read_text()))

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
           # 443: these SKUs serve 200k-1M. Declaring 32768 was a limit of ours too --
           # `window.guard` charges the prompt against it, so an understated window
           # can refuse a pair the endpoint would have taken.
           "CLAIMCHECK_WINDOW": "200000",
           "CLAIMCHECK_PROFILE": profile,
           "CLAIMCHECK_TIMEOUT": "600",
           "CLAIMCHECK_THINKING": "decompose,merge,verify",
           "CLAIMCHECK_ENDPOINT_LABEL": label}
    if tier is not None:
        env["CLAIMCHECK_STRUCTURED"] = tier
    argv = [sys.executable, "-m", "claimcheck", "merge", a, b, "--base", a,
            "--fidelity", level, "--no-cache",
            "--json", str(work / "report.json"), "-o", str(work / "merged.md")]
    print(f"  [{label} {pair} {level}] start", flush=True)
    t0 = time.time()
    p = subprocess.run(argv, capture_output=True, text=True, env=env, cwd=str(work))
    secs = round(time.time() - t0, 1)
    row = {"arm": label, "model": model, "pair": pair, "fidelity": level,
           "tier_pinned": tier,          # None = ladder free to degrade
           "tier_used": None,            # filled from provenance below
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
        so = prov.get("structured_output") or {}
        row["tier_used"] = f"{so.get('mode')}/{so.get('how')}"
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
    extra = attempt_cost(p.stderr, pin, pout)
    if extra:
        row |= extra
        # the honest figure: billed attempts, not just the one that reported
        row["cost_usd_billed"] = max(row.get("cost_usd") or 0.0,
                                     extra["attempt_cost_usd"])
    record(row)
    print(f"  [{label} {pair} {level}] exit={row['exit_code']} "
          f"cost=${row.get('cost_usd', 0):.3f} xrep={row.get('cross_line_repeats')} "
          f"{secs}s  running total ${spent():.2f}", flush=True)

if __name__ == "__main__":
    for label, model, base, keyenv, profile, pin, pout, tier in ARMS:
        for pair in PAIRS:
            for level in ("high",):
                if (label, pair, level) in done_cells():
                    print(f"  [{label} {pair} {level}] skip, already recorded", flush=True)
                    continue
                if spent() >= BUDGET_USD:
                    print(f"\nBUDGET STOP: ${spent():.2f} >= ${BUDGET_USD}")
                    raise SystemExit(0)
                run(label, model, base, keyenv, profile, pin, pout, tier, pair, level)
    print(f"\nfrontier arms complete, total ${spent():.2f}")
