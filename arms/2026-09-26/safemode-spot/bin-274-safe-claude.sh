#!/bin/sh
# Transparent wrapper, named `claude` so llossless's grant, isolation and effort
# tables apply as they would to the real CLI (609's bin-claude.sh). Same argv,
# same stdin; the envelope (stdout) and stderr are kept per call, then passed on.
dir=${BENCH_CALLS:?BENCH_CALLS is not set}
mkdir -p "$dir"
n=$(date +%s%N)
printf '%s\n' "$@" > "$dir/$n.argv"
<home>/.local/share/claude/versions/2.1.274 "$@" > "$dir/$n.out" 2> "$dir/$n.err"
rc=$?
cat "$dir/$n.out"
cat "$dir/$n.err" >&2
exit $rc
