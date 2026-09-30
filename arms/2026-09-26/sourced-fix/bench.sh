#!/bin/sh
# Usage: bench.sh ROUND CELL... ; from the round's pinned clone tree-ROUND.
set -u
REPO=<home>/Documents/Dev/vibe-coding/claimcheck
D=<home>/Documents/Dev/claude-tmp/claimcheck/2026-09-26-sourced-fix/bench
R=$1; shift
T="$D/tree-$R"
cd "$T" || exit 1
[ "$(git rev-parse HEAD)" = "$(cat $D/COMMIT-$R)" ] || { echo "ABORT: clone is not at the pin"; exit 1; }
[ -e internal/assets ] && { echo "ABORT: internal/assets reached the clone"; exit 1; }
where=$(PYTHONPATH="$T/src" "$REPO/.venv/bin/python3" -c 'import llossless; print(llossless.__file__)')
case "$where" in "$T/src/"*) echo "code: clone ($where)";; *) echo "ABORT: llossless resolves to $where"; exit 1;; esac
[ "$(git status --porcelain | wc -l)" = 0 ] || { echo "ABORT: clone is dirty"; exit 1; }
echo "provenance: clone HEAD $(git rev-parse --short HEAD), clean; CLI $($D/bin/claude --version 2>/dev/null || true)"
BENCH_DIR="$D" TREE="$T" ROUND="$R" "$REPO/.venv/bin/python3" "$D/run_fix.py" "$@"
echo "runner exit=$?"
