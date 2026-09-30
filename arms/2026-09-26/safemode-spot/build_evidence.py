#!/usr/bin/env python3
"""Build the safe-mode spot check's evidence, redacted, into scratch (not the repo).

Two trees under BENCH_DIR/evidence/, mirroring the repo paths the coordinator
copies them to, as opus-max's build_evidence.py (DECISIONS 616, 661):

- evidence/arms/2026-09-26/safemode-spot/           published: method, records
                                                     without answer-key text, raw runs
- evidence/internal/arms/2026-09-26/safemode-spot/  withheld: each voyager run's
                                                     per-error outcomes (planted.json)
                                                     and the scorer wrapper

Redacted with the pinned clone's `scripts/stream_redact.scrub`: home paths read
`<home>`, any address the release scanner refuses reads `<redacted>`. JSON is
redacted value by value. Not copied: `tree/`, each run's `tmp/`, the pair
sources (unchanged copies of tests/), `probe/done`.
"""
import json, os, pathlib, shutil, sys

D = pathlib.Path(os.environ.get("BENCH_DIR", pathlib.Path(__file__).resolve().parent))
OUT = D / "evidence"
PUB = OUT / "arms" / "2026-09-26" / "safemode-spot"
INT = OUT / "internal" / "arms" / "2026-09-26" / "safemode-spot"
HOME = str(pathlib.Path.home())

sys.path.insert(0, str(D / "tree" / "scripts"))
import stream_redact  # noqa: E402

FORMS, PATS = stream_redact.literal_forms(), stream_redact.patterns()
assert PATS, "the scanner's patterns did not load; refusing to redact with none"


def scrub(text):
    return stream_redact.scrub(text, FORMS, PATS)


def scrub_json(v):
    if isinstance(v, str):
        return scrub(v)
    if isinstance(v, list):
        return [scrub_json(x) for x in v]
    if isinstance(v, dict):
        return {scrub(k): scrub_json(x) for k, x in v.items()}
    return v


def put(src, dst, text=None):
    dst.parent.mkdir(parents=True, exist_ok=True)
    raw = src.read_text(encoding="utf-8") if text is None else text
    out = (json.dumps(scrub_json(json.loads(raw)), indent=1, ensure_ascii=False) + "\n"
           if dst.suffix == ".json" else scrub(raw))
    dst.write_text(out, encoding="utf-8")


def calls_of(directory):
    """Every call's envelope, answer text dropped unless it is an error, with its argv."""
    calls = []
    for out in sorted((directory / "calls").glob("*.out")):
        try:
            env = json.loads(out.read_text())
        except ValueError:
            env = {"unparsed": out.read_text()[:2000]}
        if env.get("is_error") is not True:
            env.pop("result", None)
        env["argv"] = out.with_suffix(".argv").read_text().split("\n")[:-1]
        sent = out.with_suffix(".argv-sent")
        if sent.exists():
            env["argv_sent"] = sent.read_text().split("\n")[:-1]
        err = out.with_suffix(".err")
        env["stderr"] = err.read_text()[:4000] if err.exists() else ""
        calls.append(env)
    return json.dumps(calls, indent=1)


if OUT.exists():
    shutil.rmtree(OUT)

for name in ("REGISTRATION.md", "REGISTRATION.sha256", "COMMIT", "CLI_VERSION", "bench.sh",
             "bench.log", "run_spot.py", "diag_nosafe.py", "diag_274.py", "bin-claude.sh",
             "bin-nosafe-claude.sh", "bin-274-nosafe-claude.sh", "bin-274-safe-claude.sh",
             "scored.json", "tables.md"):
    put(D / name, PUB / name)
put(pathlib.Path(__file__), PUB / "build_evidence.py")
for res in ("results.json", "diag/results.json"):
    rows = json.loads((D / res).read_text())
    for r in rows:
        r.pop("stderr_tail", None)
    put(D / res, PUB / res, json.dumps(rows, indent=1))
put(D / "diag" / "bench.log", PUB / "diag" / "bench.log")
for m in ("sonnet", "haiku"):
    put(D / "probe" / m / "probe.json", PUB / "probe" / m / "probe.json")
    put(D / "probe" / m / "probe.json", PUB / "probe" / m / "calls.json", calls_of(D / "probe" / m))
tp = json.loads((D / "diag" / "tool-probe" / "out.json").read_text())
put(D / "diag" / "tool-probe" / "out.json", PUB / "diag" / "tool-probe" / "out.json", json.dumps(tp))
for run in sorted([*D.glob("runs/*/a*"), *D.glob("diag/runs/*/a*")]):
    rel = run.relative_to(D)
    for name in ("merged.md", "report.json", "report.md", "stderr.log", "argv.json"):
        if (run / name).exists():
            put(run / name, PUB / rel / name)
    put(run / "argv.json", PUB / rel / "calls.json", calls_of(run))
    if (run / "planted.json").exists():
        put(run / "planted.json", INT / rel / "planted.json")
for name in ("score_spot.py", "READY-TO-COMMIT.txt"):
    put(D / name, INT / name)

left = [str(p) for t in (PUB, INT) for p in t.rglob("*")
        if p.is_file() and HOME in p.read_text(encoding="utf-8", errors="replace")]
print(f"published {sum(1 for p in PUB.rglob('*') if p.is_file())} files, "
      f"internal {sum(1 for p in INT.rglob('*') if p.is_file())} files; home path left in {left}")
sys.exit(1 if left else 0)
