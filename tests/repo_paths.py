#!/usr/bin/env python3
"""Where the things this repository withholds actually live. One definition.

Every gate that reads a withheld file used to spell its path out. Nine checks in
one test file alone named the same withheld document as a literal, and `docs/` was opened by
name in six more files. A literal path is fine until the file moves: a gate
pointed at a path that no longer exists reads nothing, finds nothing, and
reports green. That failure has been seen here before, and a migration
whose whole purpose is leak safety is the
worst possible place to repeat it.

So the paths live here and the gates import them. Moving a file becomes an edit
to one line in this module, and every gate follows it or fails loudly.

**Published on purpose.** `tests/source_guard.py` and `tests/run_vendor_arm.py`
are published and both need `ASSETS`; a published file importing a withheld
module is what the dependency scan refuses. Naming a withheld path is
not reading one, and nothing here opens anything.

`BENCH_SPEC` is the exception that proves the rule: it is the property registry
the paper promises ships with the harness, it is published by
`publication-manifest.txt`, and it does not move. It is named here so that the
one published file under `docs/` is visible beside the withheld ones rather
than looking like an oversight.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# The withheld set. One directory, tracked, never copied into a publication.
INTERNAL = ROOT / "internal"

HISTORY = INTERNAL / "HISTORY.md"
MEMORY = INTERNAL / "MEMORY.md"
AUDIT = INTERNAL / "AUDIT.md"
STATE = INTERNAL / "STATE.md"
CHANGELOG = INTERNAL / "CHANGELOG.md"
DOCS = INTERNAL / "docs"
FULL_AUDIT = INTERNAL / "full-audit"

# Gitignored as well as withheld: the source documents themselves. Committing
# them is a one-way door -- they would enter the object store, the crash mirror
# and every backup permanently -- and their change history has no audit value.
ASSETS = INTERNAL / "assets"

# Published, and the only file under `docs/` that is. See the module docstring.
#
# Deliberately *not* used by the two files that read it. `run_bench.py` and
# the paper's number check keep the literal `ROOT / "docs" / "bench-spec.md"`, because
# the dependency scan finds reads by walking literal path chains in the
# AST: routing one through a constant makes the read invisible to it. A path
# that does not move has nothing to gain from the indirection and something to
# lose, so only moving paths go through this module.
BENCH_SPEC = ROOT / "docs" / "bench-spec.md"

DECISIONS = DOCS / "DECISIONS.md"


def rel(path: Path) -> str:
    """Repo-relative POSIX string, which is how the manifest and git name things."""
    return path.relative_to(ROOT).as_posix()
