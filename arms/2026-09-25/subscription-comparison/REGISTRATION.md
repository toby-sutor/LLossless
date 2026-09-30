# Block: which subscription model and merge effort catches the planted errors, used as intended

Registered 2026-09-25, before any live call. Not edited afterwards; corrections
are dated amendments at the bottom.

## The question

The operator: *"we do not have any sourced tests which would reveal if any of
the models is able to find all issues. What are the planted errors that are
usually not found?"* Measured here: the tool used as intended for fact
correction - `--fidelity sourced`, which asks the model to look facts up and
grants `WebSearch` and `WebFetch` - through the operator's Claude subscription,
over the two pairs with planted errors and one control.

## Tool

A clone of the working repo pinned at `0418d48` (recorded in `COMMIT`), which
carries DECISIONS 599 (each command call records the model ids that answered it)
and 600 (the keys, one error per changed unit). The clone's own `src/` runs,
asserted by `bench.sh` and `run_grid.py`; every report's
`provenance.claimcheck_commit` must be the pin with no `-dirty`, or the run
aborts.

## Grid

Every run: `claimcheck merge <the pair's sources> --base source_a.md
--fidelity sourced --verify-depth full --effort merge=LEVEL --timeout 1800
--no-cache`, under the environment the web UI gives the discovered route
(`commands.Route.environ()`): `subscription` profile, `prompt` tier, thinking
on for every role (the model's default; this profile cannot turn it off),
`--window 200000`, and the shipped per-role effort (`AUTO_EFFORT`: decompose
and verify `low`). Only the merge role's effort is varied.

| pair | models | merge effort | K |
|---|---|---|---|
| voyager (44 planted errors) | opus, sonnet | low, medium, high, xhigh | 3 |
| voyager | haiku (lower anchor) | medium | 3 |
| bip39 (14 planted errors) | opus, sonnet | low, medium, high, xhigh | 3 |
| bip39 | haiku | medium | 3 |
| mahjongg (none; false-correction control) | opus, sonnet | medium | 3 |

20 cells, 60 runs. Not `fable`: the operator does not want the most expensive
model used.

**Order: draw-major.** Draw 1 runs every cell once, then draw 2, then draw 3,
so drift across the session spreads evenly and a run cut short still has
complete draws. Within a draw: voyager, then bip39, then mahjongg; within a
pair, merge effort low to xhigh, Opus before Sonnet at each, Haiku last.
**Serial**, one run at a time.

**Departures from the route, stated:**

- `--timeout 1800` against the route's 890 s, so a long mahjongg merge is not a
  failed draw by construction. It bounds the call and changes no answer.
- The route's program is a transparent wrapper named `claude`
  (`bin/claude`): same argv, same stdin, stdout passed on unchanged; it keeps
  each call's result envelope beside the run. Named `claude` so the build's
  grant and effort tables apply as to the real CLI.
- The parent session's `CLAUDE*`, `AI_AGENT*` and `CLAIMCHECK_*` variables are
  removed from the child environment, as the web UI agent's runner did.
- The CLI loads the operator's user-level `~/.claude/CLAUDE.md`, as it does
  for every subscription run on this machine; the run directories have no
  project-level one.

**Before the first live call** the runner checks that no process's cwd is
under `2026-09-24-ui/` (sandbox and host), and waits up to 3 hours in a
bounded poll if one is; after that it starts anyway and says so.

**Failure:** a run with no report, or an exit code other than 0 or 1, is
retried once, then recorded as failed. A usage-limit message stops the run;
it is resumable and resumed draws are said to be resumed.

## Recorded per run

Wall seconds; exit code; the report (`report.json`, `report.md`,
`merged.md`); the resolved model ids per role (the ledger's `answered_by`,
599) and every id any envelope named; retrieval: `num_turns` per call and
claimcheck's `retrieval` state, and the `modelUsage` `webSearchRequests`
count per call from the kept envelopes. A run that did not retrieve is
**flagged, not dropped**.

## Scoring (offline, re-runnable from the saved outputs)

- voyager and bip39: `internal/scripts/score_planted.py --pair <pair>` at the
  pin: per error `fixed`, `kept` or `other`, on the merged text.
- bip39's licence is its error 4 (GPL planted, MIT the key; checked against
  `bip-0039.mediawiki` on 2026-09-25): reported per run as fixed or not, with
  the text found when not.
- mahjongg: `score_planted.py --pair mahjongg --control`: substituting
  sentences plus declared corrections, each printed.

The operator is still reviewing how the keys count (the timestamp; "byts").
The scoring is a command over the saved outputs, so a changed ruling is a
rescore, not a re-run.

## Figures and what each may be used for

- **Per cell: median, minimum and maximum fixed over K**; for voyager also
  kept and other; for bip39 the licence; for mahjongg the false corrections;
  median wall time; retrieval rate. For comparing cells of this grid, in this
  session, on these three pairs.
- **A difference between two cells exceeds the draw spread only when their
  ranges (minimum to maximum over the K draws) do not overlap.** Otherwise it
  is reported as within the spread, whatever the medians say. With K = 3 this
  rule is coarse on purpose.
- **The hardest-errors table**: each planted error's fixed rate over all runs
  of the grid, split by model, hardest first. Descriptive of this grid.
- **The recommendation** is a model and merge effort for the subscription
  route. It changes no shipped default; the operator decides.

**Not licensed:** comparisons with the 2026-09-23/24 figures (another day,
another request, another key); anything about thinking (not varied); cost
(a subscription reports none per call); decompose or verify effort; other
documents or model families; a model's knowledge outside these pairs. The
mahjongg count is mechanical: a substitution may be a harmless rewording, so
each is read, and any reading of one as fact-changing is marked as a reading.

## Predictions (properties, registered before the call)

1. **No voyager cell fixes all 44 in every draw.**
2. **Opus beats Sonnet on voyager at every merge effort**: Opus's median fixed
   exceeds Sonnet's at each of low, medium, high, xhigh.
3. **Haiku is the floor**: Haiku's median fixed on voyager is below the
   median of every Opus and Sonnet voyager cell.
4. **Merge effort does not separate**: for neither Opus nor Sonnet do two
   effort levels' voyager ranges fail to overlap.
5. **bip39 is easier than voyager**: for every Opus and Sonnet effort cell,
   the median fraction fixed on bip39 exceeds that cell's median fraction on
   voyager.
6. **The number-format errors are among the hardest**: each of voyager's four
   format-only errors ("4,5", "2,5", "17.560", "28.260") has a fixed rate over
   all runs below the median error's fixed rate.
7. **Retrieval happens**: at least 80% of Opus and Sonnet runs record
   retrieval (`retrieved`).
8. **The licence is caught**: MIT is restored in at least 75% of Opus and
   Sonnet bip39 runs.
9. **mahjongg is not "corrected" by number**: no mahjongg run carries a
   substituting sentence that changes a number.

## Falsified by

Any voyager cell at 44/44 in all three draws (1); an effort at which Sonnet's
median is at or above Opus's (2); an Opus or Sonnet voyager cell whose median
is at or below Haiku's (3); two non-overlapping effort ranges for one model
(4); a cell whose bip39 fraction is at or below its voyager fraction (5); a
format error at or above the median rate (6); fewer than 80% retrieving (7);
fewer than 75% restoring MIT (8); a numeric substitution in mahjongg (9).

## Expected cost

About 7-8 hours of subscription time on the stored durations (voyager 4-14
minutes a run, bip39 2-7, mahjongg about 25 at `low`), longer than the brief's
4-5 hour estimate. Draw-major order means a stop leaves complete draws.

## Amendment 1, 2026-09-25 03:45 UTC, during draw 2

**Exit code 3 is a completed run, and the registration called it a failure.**
`report.RECORD_ONLY = 3` (DECISIONS 420) means the merged document is sound as
far as the tool looked and only the merge's account of itself drew findings.
The pinned build's terminal line for it read "Could not complete", which 603
has since corrected on master. The first exit 3 was `d2 mahjongg opus medium
a1` (report complete: 485 of 485 claims graded, 0 errored); the runner, per
the rule above, retried it. The runner is not restarted.

Scoring rule from here on: **a draw is the first attempt that finished with a
report and exit 0, 1 or 3.** A retry made because of an exit 3 is kept in
`results.json` and listed, and is not counted in any cell figure. A draw with
no such attempt is failed.
