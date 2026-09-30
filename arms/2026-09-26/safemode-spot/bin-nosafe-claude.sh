#!/bin/sh
# Diagnostic wrapper (Amendment 1): as bin/claude, but strips --safe-mode and
# --tools <value> so the CLI runs as it did before DECISIONS 610.
dir=${BENCH_CALLS:?BENCH_CALLS is not set}
mkdir -p "$dir"
n=$(date +%s%N)
printf '%s\n' "$@" > "$dir/$n.argv"
skip=0
for a in "$@"; do
  shift
  if [ $skip = 1 ]; then skip=0; continue; fi
  case "$a" in --safe-mode) continue;; --tools) skip=1; continue;; esac
  set -- "$@" "$a"
done
printf '%s\n' "$@" > "$dir/$n.argv-sent"
<home>/.local/share/claude/versions/2.1.283 "$@" > "$dir/$n.out" 2> "$dir/$n.err"
rc=$?
cat "$dir/$n.out"
cat "$dir/$n.err" >&2
exit $rc
