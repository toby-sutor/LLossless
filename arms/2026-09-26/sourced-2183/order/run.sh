#!/bin/sh
S=<home>/Documents/Dev/claude-tmp/claimcheck/2026-09-26-sourced-2183
cd $S/order
for k in 1 2 3 4 5; do for v in 274 283; do for p in fwd rev; do
  $S/cli.sh $v --print --output-format json --model sonnet --allowed-tools WebSearch,WebFetch --safe-mode --tools WebSearch,WebFetch --effort low < verify-$p.txt > o-$v-$p-$k.json 2> o-$v-$p-$k.err
done; done; done
echo done
