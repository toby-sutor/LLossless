#!/usr/bin/env python3
"""Build the sourced prompt-fix measurement's evidence, redacted, into scratch.

Published: runner, bench script, wrapper, results, scored counts, and each
run's merged.md, report.json, report.md, stderr.log, argv.json and calls.json
(envelopes, answer text dropped unless an error). Internal: each run's
per-error outcomes from internal/scripts/score_planted.py --json.
"""
import json, pathlib, shutil, subprocess, sys

D = pathlib.Path("<home>/Documents/Dev/claude-tmp/claimcheck/2026-09-26-sourced-fix/bench")
REPO = pathlib.Path("<home>/Documents/Dev/vibe-coding/claimcheck")
OUT = pathlib.Path(sys.argv[1])
PUB = OUT / "arms" / "2026-09-26" / "sourced-fix"
INT = OUT / "internal" / "arms" / "2026-09-26" / "sourced-fix"
HOME = str(pathlib.Path.home())
sys.path.insert(0, str(REPO / "scripts"))
import stream_redact  # noqa: E402
FORMS, PATS = stream_redact.literal_forms(), stream_redact.patterns()
assert PATS


def scrub(t):
    return stream_redact.scrub(t, FORMS, PATS)


def scrub_json(v):
    if isinstance(v, str):
        return scrub(v)
    if isinstance(v, list):
        return [scrub_json(x) for x in v]
    if isinstance(v, dict):
        return {scrub(k): scrub_json(x) for k, x in v.items()}
    return v


def put(dst, text, is_json=False):
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(scrub_json(json.loads(text)), indent=1, ensure_ascii=False) + "\n"
                   if is_json else scrub(text), encoding="utf-8")


def calls_of(run):
    calls = []
    for out in sorted((run / "calls").glob("*.out")):
        try:
            env = json.loads(out.read_text())
        except ValueError:
            env = {"unparsed": out.read_text()[:2000]}
        if env.get("is_error") is not True:
            env.pop("result", None)
        env["argv"] = out.with_suffix(".argv").read_text().split("\n")[:-1]
        err = out.with_suffix(".err")
        env["stderr"] = err.read_text()[:4000] if err.exists() else ""
        calls.append(env)
    return json.dumps(calls)


if OUT.exists():
    shutil.rmtree(OUT)
for name in ("run_fix.py", "bench.sh", "bin-claude.sh", "COMMIT-r1"):
    put(PUB / name, (D / name).read_text())
put(PUB / "build_evidence.py", pathlib.Path(__file__).read_text())
put(PUB / "prompt-round1.diff", (D.parent / "prompt-round1.diff").read_text())
for log in sorted(D.glob("bench-*.log")):
    put(PUB / log.name, log.read_text())
rows = json.loads((D / "results-r1.json").read_text())
for r in rows:
    r.pop("stderr_tail", None)
put(PUB / "results-r1.json", json.dumps(rows), True)
scored = []
for run in sorted(D.glob("runs/*/*/a*")):
    rel = run.relative_to(D)
    for name in ("merged.md", "report.md", "stderr.log"):
        if (run / name).exists():
            put(PUB / rel / name, (run / name).read_text())
    for name in ("report.json", "argv.json"):
        if (run / name).exists():
            put(PUB / rel / name, (run / name).read_text(), True)
    put(PUB / rel / "calls.json", calls_of(run), True)
    pair = "bip39" if "bip39" in run.parts[-2] else "voyager"
    got = subprocess.run([str(REPO / ".venv/bin/python3"), str(REPO / "internal/scripts/score_planted.py"),
                          "--pair", pair, "--json", str(run / "merged.md")],
                         capture_output=True, text=True, check=True).stdout
    put(INT / rel / "planted.json", got, True)
    data = json.loads(got)
    rec = data[0] if isinstance(data, list) else data
    counts = {k: rec.get(k) for k in ("fixed", "kept", "other", "planted", "total") if k in rec}
    rep = json.loads((run / "report.json").read_text())
    scored.append({"run": str(rel), "pair": pair, **counts, "exit_code": rep["exit_code"],
                   "retrieval": rep["sourcing"]["retrieval"],
                   "merge_turns": rep["sourcing"]["tool_use"]["turns"]})
put(PUB / "scored.json", json.dumps(scored), True)
left = [str(p) for t in (PUB, INT) for p in t.rglob("*")
        if p.is_file() and HOME in p.read_text(encoding="utf-8", errors="replace")]
print(json.dumps(scored, indent=1))
print(f"published {sum(1 for p in PUB.rglob('*') if p.is_file())}, internal "
      f"{sum(1 for p in INT.rglob('*') if p.is_file())}; home path left in {left}")
sys.exit(1 if left else 0)
