#!/bin/sh
# Opus 5.5 merge effort max, from a clone pinned at one commit. See REGISTRATION.md.
set -u
REPO=<home>/Documents/Dev/vibe-coding/claimcheck
D=<home>/Documents/Dev/claude-tmp/claimcheck/2026-09-26-opus-max
PIN=$(cat "$D/COMMIT")
cd "$D/tree" || exit 1
[ "$(git rev-parse HEAD)" = "$PIN" ] || { echo "ABORT: clone is not at the pin"; exit 1; }
[ -e internal/assets ] && { echo "ABORT: internal/assets reached the clone"; exit 1; }
where=$(PYTHONPATH="$D/tree/src" "$REPO/.venv/bin/python3" -c 'import llossless; print(llossless.__file__)')
case "$where" in "$D/tree/src/"*) echo "code: clone ($where)";; *) echo "ABORT: llossless resolves to $where"; exit 1;; esac
[ "$(git status --porcelain | wc -l)" = 0 ] || { echo "ABORT: clone is dirty"; exit 1; }
echo "provenance: clone HEAD $(git rev-parse --short HEAD), clean"
BENCH_DIR="$D" "$REPO/.venv/bin/python3" "$D/run_max.py"
rc=$?
echo "runner exit=$rc"
echo "BENCHMARK DONE"
exit $rc
