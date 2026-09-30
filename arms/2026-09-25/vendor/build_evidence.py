#!/usr/bin/env python3
"""Copy the 2026-09-25 vendor run's evidence into arms/2026-09-25/vendor/, redacted.

Published in full, vendor output included: the operator ruled on 2026-09-25 that
the subscription runs' raw output is published (DECISIONS 616), and the same
ruling applies to these API runs. Redacted with `scripts/stream_redact.scrub`,
the repository's one definition of a secret: home paths read `<home>`, and any
address or key shape the release scanner refuses reads `<redacted>`. JSON is
redacted value by value, so it stays JSON. The pinned clone and the per-cell
temporary directories are not copied, except the discarded envelopes of the
refused Opus cells, which are the evidence for DECISIONS 617.
"""
import json
import os
import shutil
import sys
from pathlib import Path

D = Path(__file__).resolve().parent.parent
REPO = Path(os.environ["BENCH_REPO"]).resolve()
PUB = REPO / "arms" / "2026-09-25" / "vendor"

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


def put(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    raw = src.read_text(encoding="utf-8")
    if dst.suffix == ".json":
        out = json.dumps(scrub_json(json.loads(raw)), indent=1, ensure_ascii=False) + "\n"
    else:
        out = scrub(raw)
    dst.write_text(out, encoding="utf-8")


# An arm still recording is left for a later build: its cells are incomplete
# and its vendor's ledger is still moving (BENCH_EXCLUDE="arm,vendor").
EXCLUDE = [x for x in os.environ.get("BENCH_EXCLUDE", "").split(",") if x]


def wanted(name: str) -> bool:
    return not any(name.endswith("-" + x) or name.endswith("_" + x + ".json")
                   or ("-" + x + "-d") in name or name == f"ledger_{x}.json" for x in EXCLUDE)


if PUB.exists():
    shutil.rmtree(PUB)

for name in ("REGISTRATION.md", "REGISTRATION.sha256", "REGISTRATION.amended.sha256", "COMMIT",
             "bench.log", "bench-a.log", "bench-b1.log", "bench-b.log"):
    if name == "bench-b.log" and EXCLUDE:
        continue
    if (D / name).exists():
        put(D / name, PUB / name)
for path in sorted(D.glob("ledger_*.json")) + sorted(D.glob("results_*.json")):
    if wanted(path.name):
        put(path, PUB / path.name)
for name in ("bench.sh", "run_api.py", "ledger_cli.py", "drive_openai.py", "drive_opus55.py",
             "run_sub.py", "capture_body.py", "diag_native.py", "charge_crash.py",
             "build_evidence.py"):
    put(D / "run" / name, PUB / name)
put(D / "run" / "bin" / "claude", PUB / "bin-claude.sh")

cells = 0
for cell in sorted((D / "cells").iterdir()):
    if not wanted(cell.name):
        continue
    for name in ("merged.md", "report.json", "stderr.log"):
        if (cell / name).exists():
            put(cell / name, PUB / "cells" / cell.name / name)
    for discard in sorted((cell / "tmp").glob("claimcheck-run-*/discards/*.json")):
        put(discard, PUB / "cells" / cell.name / "discards" / discard.name)
    cells += 1

for path in sorted((D / "diag").glob("*.json")):
    put(path, PUB / "diag" / path.name)

# The page check (DECISIONS 619, 620): the server fixture, the browser drive and
# what it read back off the rendered table, English and German.
for name in ("serve_for_drive.py", "drive_models.js", "drive-out.json"):
    if (D / "drive" / name).exists():
        put(D / "drive" / name, PUB / "drive" / name)

print(f"wrote {PUB.relative_to(REPO)}: {cells} cells, "
      f"{sum(1 for p in PUB.rglob('*') if p.is_file())} files")
