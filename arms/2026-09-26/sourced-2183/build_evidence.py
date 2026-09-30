#!/usr/bin/env python3
"""Build the sourced-2183 diagnosis evidence, redacted, into scratch (not the repo).

Published tree: the probes, replays, captured argv and prompt, the field-order
runs and one full run, with the scripts that made them. Internal tree: the
diagnosis hand-off and the two patches it proposed. Redacted with the repo's
`scripts/stream_redact.scrub` (home paths read `<home>`); `rate_limit_event`
lines of the stream-json files are dropped (plan state, not evidence). Not
copied: `strings/` (155 MB of text extracted from the CLI binaries; the
figures quoted from it are in the hand-off), `tree*/`, `work/`, `testlog/`,
the wrapper binaries, `newtest.py` (a draft of the test now in
`tests/test_cli.py`).
"""
import json, pathlib, shutil, sys

S = pathlib.Path("<home>/Documents/Dev/claude-tmp/claimcheck/2026-09-26-sourced-2183")
OUT = pathlib.Path(sys.argv[1])
PUB = OUT / "arms" / "2026-09-26" / "sourced-2183"
INT = OUT / "internal" / "arms" / "2026-09-26" / "sourced-2183"
HOME = str(pathlib.Path.home())
sys.path.insert(0, "<home>/Documents/Dev/vibe-coding/claimcheck/scripts")
import stream_redact  # noqa: E402
FORMS, PATS = stream_redact.literal_forms(), stream_redact.patterns()
assert PATS, "the scanner's patterns did not load"


def scrub(text):
    return stream_redact.scrub(text, FORMS, PATS)


def put(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    raw = src.read_text(encoding="utf-8", errors="replace")
    if src.suffix in (".jsonl", ".out"):
        raw = "".join(l for l in raw.splitlines(keepends=True)
                      if '"type":"rate_limit_event"' not in l.replace(" ", ""))
    dst.write_text(scrub(raw), encoding="utf-8")


if OUT.exists():
    shutil.rmtree(OUT)
for name in ("COMMIT", "cli.sh", "capture.py"):
    put(S / name, PUB / name)
for sub in ("init", "probe", "replay", "order", "sysprobe", "cap", "full-283"):
    for p in sorted((S / sub).rglob("*")):
        if p.is_file() and "/tmp/" not in str(p.relative_to(S)) + "/":
            put(p, PUB / p.relative_to(S))
put(pathlib.Path(__file__), PUB / "build_evidence.py")
for name in ("READY-TO-COMMIT.txt", "sourced-retrieval-guard.diff", "field-order-prompt.OPTIONAL.diff"):
    put(S / name, INT / name)
left = [str(p) for t in (PUB, INT) for p in t.rglob("*")
        if p.is_file() and HOME in p.read_text(encoding="utf-8", errors="replace")]
print(f"published {sum(1 for p in PUB.rglob('*') if p.is_file())} files, "
      f"internal {sum(1 for p in INT.rglob('*') if p.is_file())}; home path left in {left}")
sys.exit(1 if left else 0)
