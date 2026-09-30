#!/bin/sh
# The subscription routes over tests/pairs, from a clone pinned at one commit.
set -u
REPO=<home>/Documents/Dev/vibe-coding/claimcheck
D=<home>/Documents/Dev/claude-tmp/claimcheck/2026-09-24-ui/sub
PIN=${PIN:?set PIN to the commit to clone}
if [ ! -d "$D/tree" ]; then
  git clone -q "$REPO" "$D/tree" && git -C "$D/tree" checkout -q "$PIN" || { echo "ABORT: clone"; exit 1; }
fi
cd "$D/tree" || exit 1
[ "$(git rev-parse HEAD)" = "$(git -C "$REPO" rev-parse "$PIN")" ] || { echo "ABORT: clone is not at the pin"; exit 1; }
[ -e internal/assets ] && { echo "ABORT: internal/assets reached the clone"; exit 1; }
git rev-parse HEAD > "$D/COMMIT"
# The working repo's venv holds an editable install of the WORKING repo's src;
# PYTHONPATH puts the clone's src first, and the runner asserts it.
where=$(PYTHONPATH="$D/tree/src" "$REPO/.venv/bin/python3" -c 'import claimcheck; print(claimcheck.__file__)')
case "$where" in "$D/tree/src/"*) echo "code: clone ($where)";; *) echo "ABORT: claimcheck resolves to $where"; exit 1;; esac
echo "provenance: clone HEAD $(git rev-parse --short HEAD), dirty $(git status --porcelain | wc -l)"
[ "$(git status --porcelain | wc -l)" = 0 ] || { echo "ABORT: clone is dirty"; exit 1; }
BENCH_DIR="$D" "$REPO/.venv/bin/python3" "$D/run_subscription.py"
rc=$?
echo "runner exit=$rc"
echo "BENCHMARK DONE"
exit $rc
