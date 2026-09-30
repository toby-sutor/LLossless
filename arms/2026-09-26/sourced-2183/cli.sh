#!/bin/sh
# usage: cli.sh <version> args...  runs the pinned CLI binary with a cleaned env, cwd = scratch work dir
v=$1; shift
case $v in
 274) B=<home>/.local/share/claude/versions/2.1.274;;
 281) B=<home>/Documents/Dev/claude-tmp/claimcheck/2026-09-26-opus-max/cli/claude-2.1.281;;
 283) B=<home>/.local/share/claude/versions/2.1.283;;
esac
cd <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-26-sourced-2183/work
exec env $(env | cut -d= -f1 | grep -E '^(CLAUDE|AI_AGENT|LLOSSLESS_|CLAIMCHECK_)' | sed 's/^/-u /') "$B" "$@"
