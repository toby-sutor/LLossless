#!/usr/bin/env python3
"""Copy the grid's evidence into the repo, redacted. Two trees, as 2026-09-24/subscription:

- arms/2026-09-25/subscription-comparison/          published: no model text
- internal/arms/2026-09-25/subscription-comparison/ tracked, withheld: the runs

Redacted with `scripts/stream_redact.scrub`, the repository's one definition
of a secret: home paths read `<home>`, and any address the release scanner
refuses (the model's citations, in a `sourced` run) reads `<redacted>`. JSON is
redacted value by value, so it stays JSON. Vendor text (merged documents,
reports, found snippets, mahjongg sentences) stays in the internal tree.
"""
import json, pathlib, re, shutil, sys

D = pathlib.Path(__file__).resolve().parent
REPO = pathlib.Path.home() / "Documents" / "Dev" / "vibe-coding" / "claimcheck"
PUB = REPO / "arms" / "2026-09-25" / "subscription-comparison"
INT = REPO / "internal" / "arms" / "2026-09-25" / "subscription-comparison"
HOME = str(pathlib.Path.home())


sys.path.insert(0, str(REPO / "scripts"))
import stream_redact  # noqa: E402

FORMS, PATS = stream_redact.literal_forms(), stream_redact.patterns()
assert PATS, "the scanner's patterns did not load; refusing to redact with none"


def scrub(text: str) -> str:
    return stream_redact.scrub(text, FORMS, PATS)


def scrub_json(value):
    if isinstance(value, str):
        return scrub(value)
    if isinstance(value, list):
        return [scrub_json(v) for v in value]
    if isinstance(value, dict):
        return {scrub(k): scrub_json(v) for k, v in value.items()}
    return value


def put(src: pathlib.Path, dst: pathlib.Path, text: str | None = None) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    raw = src.read_text(encoding="utf-8") if text is None else text
    if dst.suffix == ".json":
        out = json.dumps(scrub_json(json.loads(raw)), indent=1, ensure_ascii=False) + "\n"
    else:
        out = scrub(raw)
    dst.write_text(out, encoding="utf-8")


for tree in (PUB, INT):
    if tree.exists():
        shutil.rmtree(tree)

# Published: the method, the records without text, the text-free tables.
for name in ("REGISTRATION.md", "REGISTRATION.sha256", "COMMIT", "bench.sh", "run_grid.py",
             "score_grid.py", "build_evidence.py", "bench.log"):
    put(D / name, PUB / name)
put(D / "bin" / "claude", PUB / "bin-claude.sh")
rows = json.loads((D / "results.json").read_text())
for r in rows:
    r.pop("stderr_tail", None)  # console text of a failed run: internal tree only
put(D / "results.json", PUB / "results.json", json.dumps(rows, indent=1))
scored = json.loads((D / "scored.json").read_text())
TEXT_KEYS = ("found", "licence_found", "changed", "declared_corrections", "unmatched")
bare = [{k: v for k, v in s.items() if k not in TEXT_KEYS} for s in scored]
put(D / "scored.json", PUB / "scored.json", json.dumps(bare, indent=1, ensure_ascii=False))
if (D / "tables-public.md").exists():
    put(D / "tables-public.md", PUB / "tables.md")

# Internal: everything a run left, redacted, plus the tables with text.
put(D / "scored.json", INT / "scored.json")
put(D / "tables.md", INT / "tables.md")
put(D / "results.json", INT / "results.json")
for run in sorted((D / "runs").glob("d*/*/a*")):
    rel = run.relative_to(D)
    for name in ("merged.md", "report.json", "stderr.log", "argv.json"):
        if (run / name).exists():
            put(run / name, INT / rel / name)
    calls = []
    for out in sorted((run / "calls").glob("*.out")):
        try:
            env = json.loads(out.read_text())
        except ValueError:
            env = {"unparsed": out.read_text()[:2000]}
        env.pop("result", None)  # the answer is merged.md and report.json already
        env["argv"] = out.with_suffix(".argv").read_text().split("\n")[:-1]
        calls.append(env)
    put(run / "argv.json", INT / rel / "calls.json", json.dumps(calls, indent=1))

left = [str(p) for tree in (PUB, INT) for p in tree.rglob("*")
        if p.is_file() and HOME in p.read_text(encoding="utf-8", errors="replace")]
print(f"published {sum(1 for p in PUB.rglob('*') if p.is_file())} files, "
      f"internal {sum(1 for p in INT.rglob('*') if p.is_file())} files; home path left in {left}")
sys.exit(1 if left else 0)
