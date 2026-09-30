#!/bin/sh
# run.sh <ver> <model> <tag> [extra args] ; sourced argv as llossless sends it, stream-json added for tracing
S=<home>/Documents/Dev/claude-tmp/claimcheck/2026-09-26-sourced-2183
v=$1; m=$2; tag=$3; shift 3
$S/cli.sh $v --print --output-format stream-json --verbose --model $m --allowed-tools WebSearch,WebFetch --safe-mode --tools WebSearch,WebFetch "$@" < $S/probe/prompt.txt > $S/probe/$tag.jsonl 2> $S/probe/$tag.err
echo "$tag rc=$?"
