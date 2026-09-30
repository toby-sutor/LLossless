#!/usr/bin/env python3
"""Copy the Opus 5.5 max block's evidence into the repo, redacted (DECISIONS 616, 661).

Two trees, as 2026-09-25/subscription-comparison after 616:

- arms/2026-09-26/opus-max/          published: the method, the records without
                                      answer-key text, and the raw runs
- internal/arms/2026-09-26/opus-max/ tracked, withheld: the scorer's own
                                      records and tables, which carry the answer
                                      key, and the scorer, which imports the
                                      withheld internal/scripts/score_planted.py

Redacted with `scripts/stream_redact.scrub`, the repository's one definition
of a secret: home paths read `<home>`, and any address the release scanner
refuses reads `<redacted>`. JSON is redacted value by value, so it stays JSON.
Not copied: `tree/` (the pinned clone), `cli/` (the 2.1.281 binary, 227 MB),
`dryrun/`, and each run's `tmp/` and copies of the pair's two sources, which
are `tests/handwritten/<pair>/` unchanged.
"""
import json, pathlib, shutil, sys

D = pathlib.Path("<home>/Documents/Dev/claude-tmp/claimcheck/2026-09-26-opus-max")
REPO = pathlib.Path.home() / "Documents" / "Dev" / "vibe-coding" / "claimcheck"
PUB = REPO / "arms" / "2026-09-26" / "opus-max"
INT = REPO / "internal" / "arms" / "2026-09-26" / "opus-max"
HOME = str(pathlib.Path.home())

sys.path.insert(0, str(REPO / "scripts"))
import stream_redact  # noqa: E402

FORMS, PATS = stream_redact.literal_forms(), stream_redact.patterns()
assert PATS, "the scanner's patterns did not load; refusing to redact with none"

# Fields of a scored record that quote text: which wording a draw was scored as
# having found, and mahjongg's changed and declared sentences. The published
# scored.json carries the counts and the per-error outcomes, not these.
TEXT_KEYS = ("found", "licence_found", "changed", "declared_corrections", "unmatched")
# Sections of tables.md that quote the answer key or the changed sentences.
TEXT_SECTIONS = ("## voyager per-error outcomes", "## mahjongg false corrections")


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


def calls_of(directory: pathlib.Path) -> str:
    """Every call's envelope, without the answer text, with its argv."""
    calls = []
    for out in sorted((directory / "calls").glob("*.out")):
        try:
            env = json.loads(out.read_text())
        except ValueError:
            env = {"unparsed": out.read_text()[:2000]}
        if env.get("is_error") is not True:
            env.pop("result", None)  # the answer is merged.md and report.json already
        env["argv"] = out.with_suffix(".argv").read_text().split("\n")[:-1]
        err = out.with_suffix(".err")
        env["stderr"] = err.read_text()[:4000] if err.exists() else ""
        calls.append(env)
    return json.dumps(calls, indent=1)


def public_tables(text: str) -> str:
    out, skipping = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            skipping = line.startswith(TEXT_SECTIONS)
            if line.startswith("## mahjongg false corrections"):
                out.append("## mahjongg false corrections")
                out.append("")
                out.append("- d1: 7 mechanical (the sentences are in the withheld copy of this "
                           "file; the counts are in scored.json)")
                out.append("")
        if line.startswith("Attempts "):
            skipping = False
        if not skipping:
            out.append(line)
    return "\n".join(out) + "\n"


for tree in (PUB, INT):
    if tree.exists():
        shutil.rmtree(tree)

for name in ("REGISTRATION.md", "REGISTRATION.sha256", "COMMIT", "bench.sh", "run_max.py",
             "bench.log"):
    put(D / name, PUB / name)
put(pathlib.Path(__file__), PUB / "build_evidence.py")
put(D / "bin" / "claude", PUB / "bin-claude.sh")
rows = json.loads((D / "results.json").read_text())
for r in rows:
    r.pop("stderr_tail", None)
put(D / "results.json", PUB / "results.json", json.dumps(rows, indent=1))
scored = json.loads((D / "scored.json").read_text())
bare = [{k: v for k, v in s.items() if k not in TEXT_KEYS} for s in scored]
put(D / "scored.json", PUB / "scored.json", json.dumps(bare, indent=1, ensure_ascii=False))
put(D / "tables.md", PUB / "tables.md", public_tables((D / "tables.md").read_text()))
for probe in ("probe", "probe-2.1.274"):
    put(D / probe / "probe.json", PUB / probe / "probe.json")
    put(D / probe / "probe.json", PUB / probe / "calls.json", calls_of(D / probe))
for run in sorted((D / "runs").glob("d*/*/a*")):
    rel = run.relative_to(D)
    for name in ("merged.md", "report.json", "report.md", "stderr.log", "argv.json"):
        if (run / name).exists():
            put(run / name, PUB / rel / name)
    put(run / "argv.json", PUB / rel / "calls.json", calls_of(run))

for name in ("scored.json", "results.json", "tables.md", "score_max.py",
             "catalogue-block-DRAFT.json", "READY-TO-COMMIT.txt"):
    put(D / name, INT / name)

left = [str(p) for tree in (PUB, INT) for p in tree.rglob("*")
        if p.is_file() and HOME in p.read_text(encoding="utf-8", errors="replace")]
print(f"published {sum(1 for p in PUB.rglob('*') if p.is_file())} files, "
      f"internal {sum(1 for p in INT.rglob('*') if p.is_file())} files; home path left in {left}")
sys.exit(1 if left else 0)
