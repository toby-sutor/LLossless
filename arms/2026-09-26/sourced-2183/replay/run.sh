#!/bin/sh
# run.sh <ver> <model> <tag> <format json|stream-json> [extra args]: exact merge prompt, exact sourced argv
S=<home>/Documents/Dev/claude-tmp/claimcheck/2026-09-26-sourced-2183
v=$1; m=$2; tag=$3; fmt=$4; shift 4
if [ "$fmt" = stream-json ]; then F="--output-format stream-json --verbose"; else F="--output-format json"; fi
$S/cli.sh $v --print $F --model $m --allowed-tools WebSearch,WebFetch --safe-mode --tools WebSearch,WebFetch "$@" < $S/replay/merge-prompt.txt > $S/replay/$tag.out 2> $S/replay/$tag.err
echo "$tag rc=$?"
