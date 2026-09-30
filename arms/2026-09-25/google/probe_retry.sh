#!/bin/sh
# Each named step until it answers something other than 503, at most 3 tries,
# 60 s apart (a 503 counts against the free tier's daily request quota). Stops
# at the first 429.
cd "$(dirname "$0")"
M=$1; shift
for step in "$@"; do
  for t in 1 2 3; do
    out=$(PROBE_PACE=0 <home>/Documents/Dev/vibe-coding/claimcheck/.venv/bin/python3 probe_google.py $M $step --state ../pilot_state.json 2>&1 | head -1)
    echo "$(date -u +%T) try$t $out" | cut -c1-420
    case "$out" in
      *"HTTP 429"*) echo QUOTA; exit 8;;
      *"HTTP 503"*|*"HTTP 500"*) sleep 60;;
      *) sleep 12; break;;
    esac
  done
done
