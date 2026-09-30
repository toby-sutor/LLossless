#!/bin/sh
# One phase of REGISTRATION.md, from the clone pinned in COMMIT. Asserts the
# clone before anything runs:  bench.sh api probe gemini-3.8-flash
#                               bench.sh api cells gemini-3.8-flash PLAN
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
D=$(dirname "$HERE")
REPO=${BENCH_REPO:?set BENCH_REPO to the working repository}
TREE="$D/tree"
PIN=$(cat "$D/COMMIT")
cd "$TREE" || exit 1
[ "$(git rev-parse HEAD)" = "$PIN" ] || { echo "ABORT: clone is not at the pin"; exit 1; }
[ -e internal/assets ] && { echo "ABORT: internal/assets reached the clone"; exit 1; }
[ "$(git status --porcelain | wc -l)" = 0 ] || { echo "ABORT: clone is dirty"; exit 1; }
where=$(PYTHONPATH="$TREE/src" "$REPO/.venv/bin/python3" -c 'import claimcheck; print(claimcheck.__file__)')
case "$where" in "$TREE/src/"*) ;; *) echo "ABORT: claimcheck resolves to $where"; exit 1;; esac
echo "clone $(git rev-parse --short HEAD), clean, claimcheck from the clone's src"
kind=$1; shift
export BENCH_DIR="$D" BENCH_TREE="$TREE" BENCH_REPO="$REPO" PYTHONPATH="$TREE/src"
case "$kind" in
  api) "$REPO/.venv/bin/python3" "$HERE/run_api.py" "$@";;
  *) echo "unknown phase $kind"; exit 2;;
esac
rc=$?
echo "phase exit=$rc"
exit $rc
