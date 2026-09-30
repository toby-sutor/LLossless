#!/usr/bin/env bash
# The entry 160 chain: gpt-oss:120b, both thinking arms, K=5, serial, no cache.
#
# C1 first because it is the cheap one if it fails the way it failed privately
# (155s to three empty bodies), and a configuration mistake found in the first
# three minutes is worth more than a tidy final table. Both arms are the same
# model, so this is one load, not two.
#
# An exit 2 does not stop the chain: entry 160 registers it as one of the three
# readings. An assertion failure does stop it -- a draw that violated the bar is
# not a draw, and continuing would spend an hour producing a record to discard.
set -u
K5C="$(cd "$(dirname "$0")" && pwd)"

# The comment in run_arm.sh said the cache was off for four hours while it was
# on. Read the invocation itself before spending a pod minute on it.
grep -q -- "--no-cache" "$K5C/run_arm.sh" || {
  echo "PREFLIGHT FAILED: run_arm.sh does not pass --no-cache" >&2; exit 8; }
draw() {           # $1 arm  $2 think:yes|no  $3.. flags
  local arm=$1 think=$2; shift 2
  for d in 1 2 3 4 5; do
    "$K5C/run_arm.sh" "$arm-d$d" gpt-oss:120b schema "$@"
    local code
    code=$(awk -v a="$arm-d$d" '$1==a{for(i=1;i<=NF;i++) if($i ~ /^exit=/){sub("exit=","",$i); print $i}}' "$K5C/arms.log" | tail -1)
    if ! "$K5C/assert_draw.py" "$K5C/$arm-d$d" "$arm-d$d" gpt-oss:120b "$think" schema "$code" >> "$K5C/asserts.log" 2>> "$K5C/asserts.err"; then
      echo "CHAIN ABORTED at $arm-d$d: draw assertion failed" >> "$K5C/arms.log"
      exit 9
    fi
  done
}
draw C1-120b-default no
draw C2-120b-think  yes --thinking merge --thinking verify --thinking decompose
echo "K5C CHAIN DONE $(date -Is)" >> "$K5C/arms.log"
