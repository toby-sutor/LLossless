#!/usr/bin/env bash
# The three arms the paper cites, one session, in the order the 80 GB card
# prefers: smallest first, so a failure surfaces before the two big loads.
SP="$(cd "$(dirname "$0")" && pwd)"
R="$SP/run_arm.sh"
THINK="--thinking merge --thinking verify --thinking decompose"
"$R" A1-27b-default  qwen3.8:27b     schema
"$R" B1-70b-default  deepseek-r1:70b any
"$R" C2-120b-think   gpt-oss:120b    schema $THINK
echo "CHAIN DONE $(date -Is)" >> "$SP/arms.log"
