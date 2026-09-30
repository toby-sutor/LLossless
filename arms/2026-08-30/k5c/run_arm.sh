#!/usr/bin/env bash
# One 120B thinking-axis arm over `tests/pairs/index_429` (entry 160). Adapted from an
# earlier 2026-08-28 driver, not rebuilt: the configuration under test is
# that driver's, and a rewrite would make the configuration a second variable.
#
# Two deliberate differences from the original, each recorded:
#   tier       --structured json_schema, pinned. The original probed and
#              reached json_schema in every arm; pinning sends the same
#              requests and removes the flake that would silently rewrite
#              every later call in the arm.
#   ps.json    captured before AND after, so a digest is on record either side
#              of the arm rather than only at the end.
# $1 label  $2 model  $3 field-order  $4.. extra flags (thinking)
set -u
ROOT=<home>/Documents/Dev/vibe-coding/claimcheck
SP="$(cd "$(dirname "$0")" && pwd)"
PAIR="$ROOT/tests/pairs/index_429"
label=$1; model=$2; order=$3; shift 3
out="$SP/$label"; mkdir -p "$out"
export CLAIMCHECK_BASE_URL=$(cat "$SP/../pod-url-k5c.txt")
# Entry 2: set the label before the first call. The K=1 arms this replicates
# ran without it and carry the host digest 5cefcb5c2a07; these draws carry
# 1c859caa0f73. Same pod, same hour, two stamps -- recorded in the close-out
# rather than papered over, and material to nothing here: no cassettes are
# written, and --no-cache is passed below.
#
# It was not passed below until 08:52. The two lines above asserted the cache
# was off and no flag turned it off; entry 160 registered --no-cache and the
# driver, inherited from the K=3 arms, never carried it. C2-120b-think-d1
# answered one of eight calls from disk and the gate stopped the chain. A
# comment is not a switch: the flag is on the command line now, and the draw
# gate asserts the cache directory is byte-for-byte untouched across each draw
# rather than trusting cache_hits, because a hit is a symptom and an untouched
# directory is the property.
export CLAIMCHECK_ENDPOINT_LABEL=<redacted>-2026-08-31
ROOTURL="${CLAIMCHECK_BASE_URL%/v1}"
cd "$ROOT"
# Serial residency at 80 GB: nothing else stays loaded while this arm runs.
for other in qwen3.8:27b deepseek-r1:70b gpt-oss:120b qwen3:8b; do
  [ "$other" = "$model" ] && continue
  curl -s -A claimcheck "$ROOTURL/api/generate" \
    -d "{\"model\":\"$other\",\"keep_alive\":0}" -o /dev/null
done
# Item 1b: warm, then assert the served window is reported before the first
# measured call. The warm also gives ps-before a digest - an unloaded model is
# absent from /api/ps, so capturing "before" after the unload loop and before
# any load would have recorded nothing.
.venv/bin/python "$SP/window_assert.py" "$model" > "$out/window.json" 2>&1 || {
  echo "$label WINDOW ASSERTION FAILED, arm not run" >> "$SP/arms.log"; exit 97; }
curl -s -A claimcheck "$ROOTURL/api/ps" > "$out/ps-before.json"
cache_fingerprint () { find "$ROOT/.claimcheck-cache" -type f -printf "%T@ %s %p\n" \
  | sort | sha256sum | cut -d" " -f1; }
cache_fingerprint > "$out/cache-before.txt"
start=$(date +%s)
timeout 5400 .venv/bin/claimcheck merge "$PAIR/source_a.md" "$PAIR/source_b.md" \
  --base "$PAIR/source_a.md" \
  --model "$model" --merge-model "$model" \
  --field-order "$order" \
  --structured json_schema \
  --no-cache \
  -o "$out/merged.md" --json "$out/report.json" \
  "$@" -v > "$out/report.md" 2> "$out/stderr.log"
code=$?
end=$(date +%s)
printf '%s\n' "$label model=$model order=$order flags=$* exit=$code seconds=$((end-start))" >> "$SP/arms.log"
cache_fingerprint > "$out/cache-after.txt"
curl -s -A claimcheck "$ROOTURL/api/ps" > "$out/ps-after.json"
