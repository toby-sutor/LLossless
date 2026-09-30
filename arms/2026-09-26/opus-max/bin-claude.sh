#!/bin/sh
# Transparent wrapper, named `claude` so claimcheck's grant and effort tables
# apply as they would to the real CLI. Same argv, same stdin; the CLI's stdout
# (the JSON result envelope) and stderr are kept per call, then passed on.
dir=${BENCH_CALLS:?BENCH_CALLS is not set}
mkdir -p "$dir"
n=$(date +%s%N)
printf '%s\n' "$@" > "$dir/$n.argv"
<home>/Documents/Dev/claude-tmp/claimcheck/2026-09-26-opus-max/cli/claude-2.1.281 "$@" > "$dir/$n.out" 2> "$dir/$n.err"
rc=$?
cat "$dir/$n.out"
cat "$dir/$n.err" >&2
exit $rc
