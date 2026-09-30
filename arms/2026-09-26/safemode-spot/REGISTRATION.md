# Block: do the subscription figures move under safe mode? (spot check)

Registered 2026-09-26, before any live call. Not edited afterwards; corrections
are dated amendments at the bottom.

## The question

The subscription rows on the model card were measured before DECISIONS 610
made the `claude` CLI run isolated (`--safe-mode`, `--tools` naming only the
granted web tools). Then the operator's user-level CLAUDE.md was loaded and the
full tool set, subagents included, was available. The rows carry a "before
safe mode" caveat. Operator-approved question: do the figures move under safe
mode? If not, the caveat can go for those rows; if so, they need re-measuring.

In scope: Sonnet and Haiku. Out of scope: Opus, because the `opus` alias now
resolves to `claude-opus-5-5` and the old Opus rows describe Opus 5.

## Tool

A clone of the working repo pinned at `6cc1b17` (full hash in `COMMIT`), run
with its own `src/` (`PYTHONPATH=<clone>/src`; `bench.sh` and the runner
assert `llossless.__file__` is under the clone's `src/` and the clone is not
dirty). Every report's `provenance.claimcheck_commit` must be the pin with no
`-dirty`, or the run aborts.

## Route

The shipped `claude-sonnet` and `claude-haiku` routes' environment
(`commands.Route.environ()`): `subscription` profile, `prompt` tier, thinking
on for every role, `--window 200000`, call timeout 890 s, merge effort
`medium` and decompose/verify `low` (`AUTO_EFFORT` + `AUTO_EFFORT_BY_MODEL`,
asserted). `command_with_isolation` appends `--safe-mode` and `--tools ""`
(at `high`) or `--tools WebSearch,WebFetch` (at `sourced`). The program is a
transparent wrapper named `claude` (609's `bin-claude.sh`) that runs the
installed CLI by its versioned path, `~/.local/share/claude/versions/2.1.283`
(what `~/.local/bin/claude` points at today), so an auto-update cannot swap it
mid-block, and keeps each call's argv, envelope
and stderr. The parent session's `CLAUDE*`, `AI_AGENT*`, `LLOSSLESS_*` and
`CLAIMCHECK_*` variables are removed from the child environment.

**Before the runs** one probe per alias on the route's argv shape plus
`--safe-mode --tools ""` and a one-word prompt confirms the resolved id from
`modelUsage`: `sonnet` must answer as `claude-sonnet-5`, `haiku` as
`claude-haiku-4-5-20251001`. Otherwise nothing runs.

## Runs, 8, serial

Part A, 597 spot check (runner: 597's `run_subscription.py`, adapted): pairs
`rate_limits`, `trace_names`, `badge_access` in `tests/pairs/`, sources
`source_a.md source_b.md --base source_a.md --fidelity high --verify-depth
full --no-cache`, route timeout. K = 1. Order: Sonnet on the three pairs, then
Haiku on the three.

Part B, 609 spot check (runner: 609's `run_grid.py`, adapted): Sonnet, merge
`medium`, `tests/handwritten/voyager`, `--fidelity sourced --verify-depth full
--effort merge=medium --timeout 1800 --no-cache`. K = 2.

A run with no report, or an exit code other than 0, 1 or 3, is retried once,
then recorded as failed.

## Recorded per run

Resolved model ids (every id in any envelope's `modelUsage`, and the ledger's
`answered_by`); `provenance.isolation` (safe mode and tools per role); wall
seconds; exit code; the figures below; the envelopes' summed usage:
`total_cost_usd` (API-equivalent; the subscription bills none per call),
input, output, cache-read and cache-creation tokens.

## Stop rules

- Summed envelope `total_cost_usd` over all runs above $20 after any run:
  stop, report what exists.
- A usage-limit message: stop.
- A resolved id other than the expected one for the alias (the CLI's own
  side calls on `claude-haiku-4-5-20251001` are expected on every route): stop.
- A run still going at 60 minutes wall is killed and the session stops
  (runaway guard; 597's longest run was 1081 s).

## Figures

Part A, per pair and model, by `rank_matrix.cell_figures` (as
`tests/subscription_figures.py` forms 597's `scored.json`): silent loss;
deviations = lost + bloat + dup; wall seconds of the whole merge process.
Part B: `internal/scripts/score_planted.py --pair voyager` at the pin: fixed,
kept, other out of 44.

## Comparison rule

Part A, per pair and model, against the 597 cell of the same pair and model
(`arms/2026-09-24/subscription/scored.json`). K = 1 on both sides, so the only
noise yardstick is the old run's pair-to-pair spread. **Tolerance for a
figure on pair p = max - min of that figure over the old run's other eight
pairs, same model** (leave-one-out: a pair's own value does not set its own
tolerance). |new - old| <= tolerance is "no measured effect"; above it is
"moved". Reported per pair and per figure, never blended.

Part B: the new K = 2 range of fixed overlaps 609's Sonnet `medium` range
26-31: "within 609's spread"; no overlap: "moved".

## Verdict per model

- Every compared figure on every pair "no measured effect" (and, for Sonnet,
  voyager within 609's spread): **unchanged under safe mode, caveat can go**.
- Any figure "moved": **moved, re-measure**.
- A pair that could not be compared (no report, exit 2, failed twice, or the
  stop rule reached before it) and nothing moved: **inconclusive**.

## Confounds, stated

Safe mode is not the only change between the old runs and these. Also
different: the tool commit (597 at `3480292`, 609 at `0418d48`, now
`6cc1b17`), the CLI version (the old runs recorded none; by the file times
`~/.local/bin/claude` was 2.1.274 from 2026-09-17 until 2026-09-26 17:04, so
most likely 2.1.274; now 2.1.283), the day, and the model draw. So "moved"
means the rows no longer describe the shipped route, not that safe mode
caused the move; "no measured effect" means the rows still describe it within
the yardstick. Three of nine pairs is a spot check of the row, not a
re-measurement of it.

## Not licensed

Opus rows; pairs not run; any claim of cause; cost per merge on the card
(still null by rule for a subscription).

## Tolerances, computed from 597's scored.json before any call

| model | pair | old silent | tol | old dev | tol | old wall s | tol |
|---|---|---|---|---|---|---|---|
| sonnet | rate_limits | 0 | 0 | 18 | 3 | 382.0 | 280.3 |
| sonnet | trace_names | 0 | 0 | 3 | 18 | 188.6 | 284.6 |
| sonnet | badge_access | 0 | 0 | 0 | 18 | 97.4 | 231.9 |
| haiku | rate_limits | 34 | 1 | 9 | 7 | 1080.8 | 361.0 |
| haiku | trace_names | 0 | 34 | 3 | 9 | 610.5 | 679.5 |
| haiku | badge_access | 0 | 34 | 0 | 9 | 481.3 | 679.5 |

## Amendment 1, 2026-09-26, after all 8 registered runs

All four voyager attempts exited 2 (one verify call errored on JSON field
order) and none retrieved (0 searches, merge num_turns 1); by the rule above
Part B has no counted draw. A tool probe on the same argv
(`diag/tool-probe/`) shows WebSearch works under `--safe-mode` on 2.1.283 when
asked. The merge prompt is unchanged since 609's pin but for the rename.

**Diagnostic, not part of the verdict rule:** one voyager Sonnet `medium`
`sourced` run on the same pin and CLI 2.1.283, with a wrapper that strips
`--safe-mode` and `--tools <value>` from the argv before calling the CLI
(`bin-nosafe/claude`), so the CLI loads the user-level CLAUDE.md and the full
tool set as before 610. It separates safe mode from the CLI version and the
day. Recorded as in Part B; scored the same way, descriptively. One run, K = 1.

## Amendment 2, 2026-09-26, after the Amendment 1 diagnostic

The no-safe-mode run on 2.1.283 also did not retrieve (fixed 10 of 44). Its
argv matches 609's exactly. Two more diagnostic runs, same pin, same Part B
settings, K = 1 each, on CLI 2.1.274 (the binary 609 most likely used, still
installed): `bin-274-nosafe/claude` (argv as 609's) and `bin-274-safe/claude`
(safe mode on, argv as shipped). They separate the CLI version from safe mode
and the day. Descriptive, not part of the verdict rule.
