# Lineup figures, pin 73b61563c13c

Rules (688): refusal_counts row (a refusal counts against its row, flagged "refused (prompt or guardrail)"); an unruled cell counts against its row (a model failure on a vendor row; `limit` or `config` on a self-hosted row); a cell still failing after every retry pass is the row's "endpoint failed while reference worked" when the reference route answered; nothing shrinks the common pairs.

## S1: the pairs, lowest counted draw, over the 9 common pairs

Disqualify, then rank: silent loss disqualifies; the complete rows by deviations per pair, equal deviations sharing a rank unless every row in the tie is list-priced (then list dollars, then seconds). A row's own exit 2, window cell, refusal, unruled cell or failed endpoint, and a pair it was not measured on, never shrink another row's pairs: it is listed after every complete row with its figures over the pairs it completed. One draw a cell: an order by the rule, not a ranking claim (plan 9.3).

| # | row | pairs | silent | /pair | dev | /pair | vs union | $ / merge | unit | billed $ | s / merge | tokens / merge | model-conf | incomplete | excluded | unruled calls | reused calls | not completed |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | gpt-6-sol-api | 9 of 9 | 0 | 0.00 | 37 | 4.11 | below (70) | 0.189 | list | 0.189 | 158.4 | 34956 | 19 | - | 0 | 0 | 0 | - |
| 2 | opus-5.5-sub | 9 of 9 | 0 | 0.00 | 63 | 7.00 | below (70) | 0.614 | api_equivalent | 0.614 | 164.1 | 55453 | 37 | - | 0 | 0 | 0 | - |
| 3 | sonnet-5-api | 9 of 9 | 0 | 0.00 | 73 | 8.11 | NO BETTER (70) | 0.462 | list | 0.462 | 332.4 | 67974 | 42 | - | 0 | 0 | 0 | - |
| DQ | gpt-6-luna-api | 9 of 9 | 2 | 0.22 | 51 | 5.67 | below (70) | 0.012 | list | 0.012 | 141.3 | 39666 | 22 | - | 0 | 0 | 0 | - |
| DQ | opus-5.5-api | 9 of 9 | 2 | 0.22 | 61 | 6.78 | below (70) | 0.485 | list | 0.485 | 142.7 | 47656 | 35 | - | 0 | 0 | 0 | - |
| DQ | haiku-4.5-sub | 9 of 9 | 3 | 0.33 | 68 | 7.56 | below (70) | 0.483 | api_equivalent | 0.483 | 676.5 | 122847 | 26 | - | 0 | 0 | 0 | - |
| DQ | sonnet-5-sub | 9 of 9 | 5 | 0.56 | 66 | 7.33 | below (70) | 0.309 | api_equivalent | 0.309 | 186.5 | 73188 | 36 | - | 0 | 0 | 0 | - |
| DQ | haiku-4.5-api | 8 of 9 | 13 | 1.62 | 50 | 6.25 | below (63) | 0.069 | list | 0.069 | 69.1 | 30132 | 6 | exit 2 on 1 of 9 | 0 | 0 | 0 | bike_docks (model_failure) |
| base | concatenation | 9 of 9 | 0 | 0.00 | 79 | 8.78 | - | - | no model | - | - | - | - | - | - | - | - | - |
| base | union | 9 of 9 | 0 | 0.00 | 70 | 7.78 | - | - | no model | - | - | - | - | - | - | - | - | - |
| base | base_only | 9 of 9 | 129 | 14.33 | 68 | 7.56 | - | - | no model | - | - | - | - | - | - | - | - | - |

Floors (plan 4), scored by the same scorer from the sources with no model call: byte-concatenation, a mechanical union (the base, then every paragraph of the other not already in it, its title dropped) and base-only. `vs union` holds each row against the union on the same pairs; no better than a mechanical union: sonnet-5-api.

Rows (688, rulings 10 and 11): the route, the effort as run, and every model id the row's reports say answered (a subscription row served by another model than its API row shows here).

| row | route | effort | answered as |
|---|---|---|---|
| gpt-6-sol-api | http | vendor default | gpt-6-sol |
| opus-5.5-sub | claude | medium on every role (CLI) | claude-opus-5-5 |
| sonnet-5-api | http | vendor default | claude-sonnet-5 |
| gpt-6-luna-api | http | vendor default | gpt-6-luna |
| opus-5.5-api | http | vendor default | claude-opus-5-5 |
| haiku-4.5-sub | claude | one level (extended thinking on/off; default kept) | claude-haiku-4-5-20251001 |
| sonnet-5-sub | claude | medium on every role (CLI) | claude-sonnet-5 |
| haiku-4.5-api | http | one level (extended thinking on/off; default kept) | claude-haiku-4-5-20251001 |

Spread pairs, every counted draw (min / median / max):

| row | pair | draws | silent | deviations |
|---|---|---|---|---|
| gpt-6-sol-api | badge_access | 3 | 0 / 0 / 0 | 0 / 0 / 1 |
| gpt-6-sol-api | trace_names | 3 | 0 / 0 / 0 | 8 / 9 / 10 |
| gpt-6-sol-api | rate_limits | 3 | 0 / 0 / 1 | 9 / 9 / 9 |
| opus-5.5-sub | badge_access | 3 | 0 / 0 / 0 | 0 / 0 / 0 |
| opus-5.5-sub | trace_names | 3 | 0 / 0 / 0 | 7 / 7 / 8 |
| opus-5.5-sub | rate_limits | 3 | 0 / 0 / 0 | 25 / 26 / 28 |
| gpt-6-luna-api | badge_access | 3 | 0 / 0 / 0 | 0 / 1 / 1 |
| gpt-6-luna-api | trace_names | 3 | 0 / 0 / 0 | 8 / 8 / 9 |
| gpt-6-luna-api | rate_limits | 3 | 1 / 2 / 2 | 16 / 19 / 22 |
| opus-5.5-api | badge_access | 3 | 0 / 0 / 0 | 0 / 0 / 0 |
| opus-5.5-api | trace_names | 3 | 0 / 0 / 0 | 7 / 7 / 9 |
| opus-5.5-api | rate_limits | 3 | 0 / 0 / 2 | 24 / 24 / 27 |
| haiku-4.5-sub | badge_access | 3 | 0 / 0 / 0 | 0 / 0 / 0 |
| haiku-4.5-sub | trace_names | 3 | 0 / 0 / 0 | 9 / 10 / 10 |
| haiku-4.5-sub | rate_limits | 3 | 2 / 10 / 26 | 9 / 10 / 14 |
| sonnet-5-sub | badge_access | 3 | 0 / 0 / 0 | 0 / 0 / 0 |
| sonnet-5-sub | trace_names | 3 | 0 / 0 / 0 | 4 / 5 / 7 |
| sonnet-5-sub | rate_limits | 3 | 0 / 0 / 4 | 21 / 21 / 26 |

Side table, fable-sub against opus-5.5-sub, over 2 common pair(s):

| row | pairs | silent | dev | $ / merge | unit | s / merge | incomplete | not completed |
|---|---|---|---|---|---|---|---|---|
| fable-sub | 2 of 2 | 0 | 21 | 2.721 | api_equivalent | 359.9 | - | - |
| opus-5.5-sub | 2 of 2 | 0 | 32 | 1.177 | api_equivalent | 329.6 | - | - |

## S2: detection, over the 13 common fixtures

A row's own exit 2 on a fixture never shrinks another row's fixtures (684); such a row follows the complete ones, over what it measured.

| row | fixtures | exit codes matched | plants detected | invented | guards wrong | incomplete | disqualified |
|---|---|---|---|---|---|---|---|
| opus-5.5-api | 13 of 13 | 12/13 | 7/7 | 2 | 1 | - | 2 |
| sonnet-5-api | 13 of 13 | 13/13 | 7/7 | 0 | 0 | - | 0 |
| haiku-4.5-api | 13 of 13 | 12/13 | 7/7 | 2 | 1 | - | 2 |
| gpt-6-sol-api | 13 of 13 | 11/13 | 6/6 | 1 | 0 | - | 1 |
| gpt-6-luna-api | 13 of 13 | 10/13 | 6/6 | 4 | 1 | - | 3 |
| opus-5.5-sub | 13 of 13 | 11/13 | 7/7 | 4 | 3 | - | 4 |
| sonnet-5-sub | 13 of 13 | 13/13 | 7/7 | 0 | 0 | - | 0 |
| haiku-4.5-sub | 13 of 13 | 12/13 | 7/7 | 1 | 1 | - | 2 |

## S3: planted errors (fixed, min / median / max over draws)

| row | voyager | bip39 | mahjongg |
|---|---|---|---|
| opus-5.5-api | 28 / 29 / 32 of 44, 3 draw(s) | 13 / 13 / 13 of 14, 3 draw(s) | false corrections [0] |
| sonnet-5-api | 20 / 21 / 23 of 44, 3 draw(s) | 12 / 12 / 12 of 14, 3 draw(s) | false corrections [0] |
| haiku-4.5-api | 6 / 11 / 18 of 44, 3 draw(s) | 8 / 8 / 9 of 14, 3 draw(s) | false corrections [1] |
| gpt-6-sol-api | 22 / 23 / 29 of 44, 3 draw(s) | 10 / 11 / 12 of 14, 3 draw(s) | false corrections [2] |
| gpt-6-luna-api | 18 / 19 / 19 of 44, 3 draw(s) | 7 / 8 / 10 of 14, 3 draw(s) | false corrections [0] |
| opus-5.5-sub | 30 / 32 / 35 of 44, 3 draw(s) | 13 / 13 / 13 of 14, 3 draw(s) | false corrections [1] |
| sonnet-5-sub | 18 / 20 / 23 of 44, 3 draw(s) | 12 / 12 / 12 of 14, 3 draw(s) | false corrections [0] |
| haiku-4.5-sub | 2 / 6 / 17 of 44, 3 draw(s) | 6 / 8 / 9 of 14, 3 draw(s) | - (not completed: d1 (model_failure)) |
| fable-sub | 38 / 38 / 38 of 44, 1 draw(s) | - | - |
