"""`python -m llossless`, so the package runs without an installed script.

F6 in `internal/docs/plan-2026-09.md`, found again by `tests/smoke_vendor.py`:
the console script in `pyproject.toml` is the documented way in, and it only
exists after an install. Anyone running from a checkout -- a contributor, CI, or
a tool in this repository invoking the CLI as a subprocess to test the command
rather than the function -- reached `No module named claimcheck.__main__`.

Delegating to the same `cli.main` the console script names, rather than
repeating any of it: two entry points that each built their own argument parser
would be two tools, and the one nobody runs would be the one that drifts.
"""

from __future__ import annotations

import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())
