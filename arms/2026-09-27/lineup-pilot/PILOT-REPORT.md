# Release pilot report, 2026-09-27 (plan section 7; never counted)

Pin 73b6156, CLI 2.1.283 (sha256 1859583c...). 25 cells, all `ok`, no retry,
no reference check, no halt. Lanes: openai, anthropic, subscription.

## Instrument checks

| check | result |
|---|---|
| Environment: no proxy or base-URL variable in any cell's env | pass |
| Pinned CLI binary sha256 (runner refuses otherwise) | pass |
| Safe mode: every subscription call one turn, `--tools` set | pass |
| Answering model per call equals the row's model (vendor responses and CLI modelUsage) | pass; fable answers as claude-fable-5-1 |
| Haiku: no `--effort` on either route, recorded "one level" | pass |
| The clone runs: `llossless` resolves inside `tree/src` in a child with the cells' env (preflight) | pass |
| Metering: journal `calls` equals recorded responses on every cell | pass |
| Tier: `prompt`, `how: pinned`, on every cell | pass |
| Refusals: Haiku and Sonnet API answer the merge prompt | pass |
| Figures re-derive: `lineup_figures.py --write`, then `--check` clean | pass |

## Budget against the plan's 0.2 x T9 estimate

| row | estimate | actual | move |
|---|---|---|---|
| opus-5.5-api | 0.84 | 0.9609 | +14% |
| sonnet-5-api | 0.74 | 0.9538 | +29% (bip39 $0.72, 499 s) |
| haiku-4.5-api | 0.13 | 0.1328 | +2% |
| gpt-6-sol-api | 0.38 | 0.3819 | 0% |
| gpt-6-luna-api | 0.02 | 0.0226 | +13% |

Subscription, API-equivalent (not spend): opus 1.2720, sonnet 0.5318,
haiku 0.8677 (about 6.5x its API row: the CLI's Haiku thinks longer, 70-163 s
a call), fable 0.9939 on badge_access alone.

Sonnet 5 API moved by more than 25%: the Anthropic estimate is re-scaled and
goes back to the operator (about $36 counted against about $37 left).

## Defects found

None. The pin stays (plan section 7, exit).
