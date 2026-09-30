## Part A: 597 cells, old (pre-safe-mode, 3480292) against new (6cc1b17)

| model | pair | figure | old | new | diff | tol | call |
|---|---|---|---|---|---|---|---|
| sonnet | rate_limits | silent | 0 | 0 | +0 | 0 | no measured effect |
| sonnet | rate_limits | deviations | 18 | 19 | +1 | 3 | no measured effect |
| sonnet | rate_limits | wall s | 382.0 | 157.3 | -224.7 | 280.3 | no measured effect |
| sonnet | trace_names | silent | 0 | 0 | +0 | 0 | no measured effect |
| sonnet | trace_names | deviations | 3 | 2 | -1 | 18 | no measured effect |
| sonnet | trace_names | wall s | 188.6 | 77.5 | -111.1 | 284.6 | no measured effect |
| sonnet | badge_access | silent | 0 | 0 | +0 | 0 | no measured effect |
| sonnet | badge_access | deviations | 0 | 0 | +0 | 18 | no measured effect |
| sonnet | badge_access | wall s | 97.4 | 61.0 | -36.4 | 231.9 | no measured effect |
| haiku | rate_limits | silent | 34 | 1 | -33 | 1 | MOVED |
| haiku | rate_limits | deviations | 9 | 4 | -5 | 7 | no measured effect |
| haiku | rate_limits | wall s | 1080.8 | 1200.9 | +120.1 | 361 | no measured effect |
| haiku | trace_names | silent | 0 | 1 | +1 | 34 | no measured effect |
| haiku | trace_names | deviations | 3 | 6 | +3 | 9 | no measured effect |
| haiku | trace_names | wall s | 610.5 | 610.1 | -0.4 | 679.5 | no measured effect |
| haiku | badge_access | silent | 0 | 0 | +0 | 34 | no measured effect |
| haiku | badge_access | deviations | 0 | 0 | +0 | 9 | no measured effect |
| haiku | badge_access | wall s | 481.3 | 468.0 | -13.3 | 679.5 | no measured effect |

## Part B: voyager, Sonnet, merge medium, sourced (609 range 26-31 fixed of 44)

| run | exit | wall s | fixed | kept | other | searches |
|---|---|---|---|---|---|---|

Failed draws (registered rule: exit 2 is a failed attempt, not counted). Their merged text scored anyway, descriptive only, not in the verdict:

| run | exit | wall s | fixed | kept | other | retrieval | searches | errors |
|---|---|---|---|---|---|---|---|---|
| B-sonnet-voyager-d1 a1 | 2 | 80.1 | 4 | 40 | 0 | not-retrieved | 0 | 1 |
| B-sonnet-voyager-d1 a2 | 2 | 90.1 | 4 | 39 | 1 | not-retrieved | 0 | 1 |
| B-sonnet-voyager-d2 a1 | 2 | 76.8 | 1 | 43 | 0 | not-retrieved | 0 | 1 |
| B-sonnet-voyager-d2 a2 | 2 | 82.9 | 4 | 40 | 0 | not-retrieved | 0 | 1 |

Total envelope total_cost_usd over 10 attempts: $3.29 (plus probes, in probe/*/probe.json)

## Verdicts

- sonnet: inconclusive
- haiku: moved, re-measure

## Diagnostics (Amendments 1-2, descriptive, not in the verdict rule)

voyager, Sonnet, merge medium, sourced, same pin, K = 1 each.

| run | CLI | safe mode | exit | wall s | fixed | kept | other | retrieval | searches | merge turns | usd |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-sonnet-voyager-nosafe | 2.1.283 | off | 1 | 126.2 | 10 | 33 | 1 | not-retrieved | 0 | [1] | 0.5224 |
| B-sonnet-voyager-274-nosafe | 2.1.274 | off | 1 | 455.5 | 30 | 11 | 3 | retrieved | 13 | [18] | 1.5258 |
| B-sonnet-voyager-274-safe | 2.1.274 | on | 1 | 1052.9 | 42 | 1 | 1 | retrieved | 37 | [62] | 3.6421 |

Reference: 609 Sonnet medium, CLI 2.1.274 (most likely), no safe mode: fixed 26-31, retrieved 3/3, merge turns 12-14; today's scorer reproduces 30, 26, 31.

## Usage (envelope total_cost_usd, API-equivalent)

registered runs $3.29; alias probes $0.0095; tool probe $0.0311; diagnostics $5.69; **total $9.02**
