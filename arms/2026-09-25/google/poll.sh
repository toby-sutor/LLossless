#!/bin/sh
# One plain call every 180 s, alternating the two models, until one answers 200.
cd "$(dirname "$0")"
P=<home>/Documents/Dev/vibe-coding/claimcheck/.venv/bin/python3
for i in $(seq 1 20); do
  for m in gemini-3.8-flash gemini-3.5-flash-lite; do
    out=$(PROBE_PACE=0 $P probe_google.py $m plain --state ../pilot_state.json 2>&1 | head -1 | cut -c1-160)
    echo "$(date -u +%T) $out" >> ../poll.log
    case "$out" in *"HTTP 200"*) echo "OK $m"; exit 0;; esac
    sleep 90
  done
done
echo "GAVE UP"
