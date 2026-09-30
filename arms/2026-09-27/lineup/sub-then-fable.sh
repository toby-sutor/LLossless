#!/bin/sh
# Subscription lane, then Fable last (amendment 1). Fable runs only if the subscription lane ended cleanly (exit 0 or 7).
D=<home>/Documents/Dev/claude-tmp/claimcheck/2026-09-27-release-lineup
cd "$D/tree" || exit 1
export PYTHONDONTWRITEBYTECODE=1
python3 tests/run_lineup.py run --registration "$D/REGISTRATION.md" --lane subscription >> "$D/lane-subscription.log" 2>&1
rc=$?
echo "$(date -u +%FT%TZ) subscription lane exit $rc" >> "$D/sub-then-fable.log"
if [ "$rc" -ne 0 ] && [ "$rc" -ne 7 ]; then
    echo "$(date -u +%FT%TZ) Fable not started (subscription exit $rc)" >> "$D/sub-then-fable.log"; exit "$rc"
fi
python3 tests/run_lineup.py run --registration "$D/REGISTRATION.md" --lane fable >> "$D/lane-fable.log" 2>&1
echo "$(date -u +%FT%TZ) fable lane exit $?" >> "$D/sub-then-fable.log"
