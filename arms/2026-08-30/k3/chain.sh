#!/usr/bin/env bash
# Four arms x three draws over the public pair, per the bar frozen at
# DECISIONS 156. The driver is the surviving 2026-08-28 run_arm.sh, re-pointed
# and not rebuilt, so the configuration under test stays the driver's.
#
# Grouped by model so the endpoint loads two and not four: run_arm.sh's
# eviction loop skips the target, so three consecutive draws of one arm keep it
# resident. A1 is the cheapest arm on the 2026-08-28 timings (501 s against
# 684, 1391 and 1274) and runs first, so a configuration error surfaces in the
# first ten minutes rather than at the end of a three-hour chain.
#
# --no-cache is load-bearing: with the cache on, draws 2 and 3 answer from disk
# and return draw 1 three times, which is indistinguishable from the identity
# result D5 predicts. A cache hit would manufacture the finding.
#
# Every draw is asserted against the bar before the next one starts. A draw
# that violated it is not a draw, and two more hours spent after one would
# produce a record that has to be thrown away.
set -u
SP="$(cd "$(dirname "$0")" && pwd)"
R="$SP/run_arm.sh"
ROOT=<home>/Documents/Dev/vibe-coding/claimcheck
THINK="--thinking merge --thinking verify --thinking decompose"

draw () {  # $1 label  $2 model  $3 order  $4 yes|no thinking
  local label=$1 model=$2 order=$3 think=$4 n
  local flags=""; [ "$think" = yes ] && flags="$THINK"
  for n in 1 2 3; do
    "$R" "$label-d$n" "$model" "$order" --no-cache $flags
    "$ROOT/.venv/bin/python" "$SP/assert_draw.py" \
      "$SP/$label-d$n/report.json" "$label-d$n" "$model" "$think" "$order" \
      >> "$SP/asserts.log" 2>&1 || {
        echo "CHAIN ABORTED at $label-d$n $(date -Is)" >> "$SP/arms.log"
        cat "$SP/asserts.log" >&2
        exit 9; }
  done
}

draw A1-27b-default qwen3.8:27b     schema no
draw A2-27b-think   qwen3.8:27b     schema yes
echo "MODEL A DONE $(date -Is)" >> "$SP/arms.log"
draw B1-70b-default deepseek-r1:70b any    no
draw B2-70b-think   deepseek-r1:70b any    yes
echo "K3 CHAIN DONE $(date -Is)" >> "$SP/arms.log"
