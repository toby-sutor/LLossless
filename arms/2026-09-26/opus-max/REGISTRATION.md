# Block: merge effort `max` on Opus 5.5, subscription route, safe mode (TODO 615)

Registered 2026-09-26, before any live call. Not edited afterwards; corrections
are dated amendments at the bottom.

## The question

Does merge effort `max` catch more planted errors than `xhigh` on Opus 5.5,
through the operator's Claude subscription, on the route as shipped, and what
does it cost in wall time and usage? Operator approval, 2026-09-26: *"You can
do the opus 5.5 max tests now."*

## Tool

A clone of the working repo pinned at `a13818a` (full hash in `COMMIT`), run
with its own `src/` (`PYTHONPATH=<clone>/src`, asserted by `bench.sh` and the
runner: `llossless.__file__` under the clone's `src/`, clone not dirty). Every
report's `provenance.claimcheck_commit` must be the pin with no `-dirty`, or
the run aborts.

## Route

The shipped `claude-opus` route's environment (`commands.Route.environ()`),
with one change: `--model opus` becomes `--model claude-opus-5-5`, because on
2026-09-25 the `opus` alias still resolved to Opus 5. `LLOSSLESS_MODEL` and
`LLOSSLESS_MERGE_MODEL` name the same id. The program is a transparent wrapper
named `claude` (`bin/claude`, 609's `bin-claude.sh`) that keeps each call's
argv, envelope and stderr.

Every run: `llossless merge <the pair's sources> --base source_a.md
--fidelity sourced --verify-depth full --effort merge=LEVEL --timeout 1800
--no-cache`. Under it: `subscription` profile, thinking on for every role,
`--window 200000`, safe mode plus `--tools WebSearch,WebFetch` (610, appended
by `command_with_isolation`), decompose and verify at the shipped `low`
(`AUTO_EFFORT`). Only the merge effort varies. The parent session's
`CLAUDE*`, `AI_AGENT*`, `LLOSSLESS_*` and `CLAIMCHECK_*` variables are removed
from the child environment (`CLAUDE_EFFORT` among them).

## Grid, 6 runs, serial, draw-major

| cell | pair | merge effort | K |
|---|---|---|---|
| V-max | voyager (44 planted errors) | max | 3 |
| V-xhigh | voyager | xhigh | 2 (same-session comparator) |
| M-max | mahjongg (none; false-correction control) | max | 1 |

Order: draw 1 = V-xhigh, V-max, M-max; draw 2 = V-xhigh, V-max; draw 3 =
V-max. xhigh goes first in a draw so the usage guard below always has a
same-session comparator.

**Before the grid**, one probe call on the same argv shape (`--print
--output-format json --model claude-opus-5-5 --safe-mode --tools ""`, a
one-word prompt) confirms the resolved model id from `modelUsage`. If it is
not an Opus 5.5 id, nothing runs.

## Stop rules

- A run still going at 45 minutes wall is killed and the session stops.
- A V-max run whose summed envelope `total_cost_usd` exceeds 5x the median of
  the V-xhigh runs so far stops the session.
- A usage-limit message stops the session.
- A run with no report, or an exit code other than 0, 1 or 3, is retried
  once, then recorded as failed. Exit 3 (`RECORD_ONLY`) is a completed run
  (609 amendment 1).

## Recorded per run

Wall seconds; exit code; the report (`report.json`, `report.md`,
`merged.md`); the resolved model ids (ledger `answered_by`, 599/607, and
every id any envelope's `modelUsage` names); retrieval: `num_turns` per call,
llossless's `retrieval` state, `webSearchRequests` per call; usage per call
and summed: input, output, cache-read and cache-creation tokens, and the
envelope's `total_cost_usd` (an API-equivalent figure; the subscription bills
none per call).

## Scoring (offline)

`internal/scripts/score_planted.py` at the pin: voyager per error `fixed`,
`kept` or `other` out of 44; mahjongg `--control` false corrections, each
printed.

## Figures and use

Per cell: fixed, kept, other as median and range; mahjongg's false
corrections; median wall; retrieval rate; usage. **A difference exceeds the
draw spread only when the two ranges do not overlap.** With K = 3 against 2
this is coarse; an overlap is reported as within the spread, whatever the
medians say.

Not licensed: comparison with 609's figures as a baseline (Opus 5, before
safe mode, another day); other pairs, models or roles.

## Predictions (properties)

1. V-max and V-xhigh ranges of fixed overlap (effort does not separate).
2. V-max median wall time is above V-xhigh's.
3. V-max median summed `total_cost_usd` is above V-xhigh's.
4. No voyager run fixes all 44.
5. mahjongg at max carries no numeric substitution.
6. Every run retrieves (`retrieved`, or `webSearchRequests` > 0).

## Amendment 1, 2026-09-26, after the probe, before any grid call

**The installed CLI cannot run Opus 5.5.** The probe through
`~/.local/bin/claude` (2.1.274) returned `API Error: 400 Claude Code 2.1.274
does not support this model; version 2.1.280 or newer is required`, no model
answering (kept in `probe-2.1.274/`). The operator's installed CLI is not
updated by this block. Instead the wrapper runs a copy of the 2.1.281 native
binary that ships with the VSCodium Claude Code extension, copied to
`cli/claude-2.1.281` (sha256 beside it) so an extension update cannot swap it
mid-run. Its `--help` documents the same `--safe-mode`, `--tools`, `--effort
(low, medium, high, xhigh, max)` and `--model` flags this build reads. The
route's argv is otherwise unchanged. This is a CLI version departure from the
shipped route, stated; it applies to every run of the block alike. The probe
is repeated on the new binary.
