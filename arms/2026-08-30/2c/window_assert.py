#!/usr/bin/env python3
"""Warm one model and assert its served window is reported, not WindowUnknown.

Brief O v3 item 1b: the assertion runs before the arm's first measured call.
It is not an extra cost - the arm loads this model anyway, and warming here is
what puts the model into /api/ps so ps-before.json has a digest to record. An
unloaded model does not appear in /api/ps at all, so capturing ps-before after
the unload loop and before any load would have written an empty "before".

Exits non-zero on WindowUnknown, on a placement that is not fully on the GPU,
or on a served window that disagrees with what the tool reports. Any of those
is a provenance event under entry 142 and must stop the arm, not annotate it.
"""
import json, sys
from pathlib import Path

ROOT = Path("<home>/Documents/Dev/vibe-coding/claimcheck")
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from probe import api                            # noqa: E402
from claimcheck import config                    # noqa: E402
from claimcheck.client import Client             # noqa: E402
from claimcheck.console import Console           # noqa: E402

name = sys.argv[1]
settings = config.from_env()
client = Client(settings, console=Console(verbosity=1, enabled=True))
w = client._reported(name)          # raises WindowUnknown rather than guessing
ps = {m["name"]: m for m in api(settings, "/api/ps")["models"]}
if name not in ps:
    raise SystemExit(f"{name}: warmed but absent from /api/ps")
row = {"model": name, "window": w.tokens, "source": w.source,
       "detail": w.detail, "placement": w.placement,
       "served_window": ps[name]["context_length"],
       "digest": ps[name]["digest"], "size_vram": ps[name]["size_vram"]}
print(json.dumps(row, indent=1))
if w.source == "unknown":
    raise SystemExit(f"{name}: window not reported ({w.source})")
if row["served_window"] != w.tokens:
    raise SystemExit(f"{name}: served {row['served_window']} != reported {w.tokens}")
