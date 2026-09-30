#!/usr/bin/env python3
"""Copy the 2026-09-25 Google free-tier run's evidence into arms/2026-09-25/google/, redacted.

The vendor run's build_evidence.py, for this run's files. Published in full,
vendor output included (the ruling of DECISIONS 616, applied to the API runs by
619). Redacted with `scripts/stream_redact.scrub`, the repository's one
definition of a secret: home paths read `<home>`, any address or key shape the
release scanner refuses reads `<redacted>`. JSON is redacted value by value.
The pilot's raw responses keep everything but Gemini's `thought_signature`, an
opaque blob with no bearing on any figure, which is replaced by its length.
The pinned clone and the per-cell temporary directories are not copied.
"""
import json
import os
import shutil
import sys
from pathlib import Path

D = Path(__file__).resolve().parent.parent
REPO = Path(os.environ["BENCH_REPO"]).resolve()
PUB = REPO / "arms" / "2026-09-25" / "google"

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
        return {scrub(k): (f"<{len(v)} characters, not published>"
                           if k == "thought_signature" and isinstance(v, str)
                           else scrub_json(v))
                for k, v in value.items()}
    return value


def put(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    raw = src.read_text(encoding="utf-8")
    if dst.suffix == ".json":
        out = json.dumps(scrub_json(json.loads(raw)), indent=1, ensure_ascii=False) + "\n"
    else:
        out = scrub(raw)
    dst.write_text(out, encoding="utf-8")


scored = PUB / "scored.json"
keep = scored.read_text(encoding="utf-8") if scored.exists() else None
if PUB.exists():
    shutil.rmtree(PUB)

for name in ("REGISTRATION.md", "REGISTRATION.sha256", "REGISTRATION.amended.sha256",
             "COMMIT", "bench.log", "error_counts.json", "pilot_state.json", "models-list.txt",
             "poll.log"):
    if (D / name).exists():
        put(D / name, PUB / ("pilot/" + name if name in ("pilot_state.json",
                                                          "models-list.txt", "poll.log")
                              else name))
for path in sorted(D.glob("ledger_*.json")) + sorted(D.glob("results_*.json")):
    put(path, PUB / path.name)
for name in ("bench.sh", "run_api.py", "ledger_cli.py", "probe_google.py", "probe_retry.sh",
             "poll.sh", "native_once.py", "build_evidence.py", "selftest_retry.py",
             "count_errors.py"):
    put(D / "run" / name, PUB / name)

cells = 0
for cell in sorted((D / "cells").iterdir()):
    for name in ("merged.md", "report.json", "stderr.log"):
        if (cell / name).exists():
            put(cell / name, PUB / "cells" / cell.name / name)
    # A cell that could not finish: the raw answers the tool refused.
    for failed in sorted((cell / "tmp").glob("claimcheck-run-*/failures/*.txt")):
        put(failed, PUB / "cells" / cell.name / "failures" / failed.name)
    cells += 1

for name in ("serve_for_drive.py", "drive_models.js", "drive-out.json"):
    if (D / "drive" / name).exists():
        put(D / "drive" / name, PUB / "drive" / name)
if keep is not None:
    scored.write_text(keep, encoding="utf-8")

print(f"wrote {PUB.relative_to(REPO)}: {cells} cells, "
      f"{sum(1 for p in PUB.rglob('*') if p.is_file())} files")
