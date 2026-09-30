# Lineup figures, pin 73b61563c13c

Rules (688): refusal_counts row (a refusal counts against its row, flagged "refused (prompt or guardrail)"); an unruled cell counts against its row (a model failure on a vendor row; `limit` or `config` on a self-hosted row); a cell still failing after every retry pass is the row's "endpoint failed while reference worked" when the reference route answered; nothing shrinks the common pairs.

## S1: the pairs, lowest counted draw, over the 1 common pairs

Disqualify, then rank: silent loss disqualifies; the complete rows by deviations per pair, equal deviations sharing a rank unless every row in the tie is list-priced (then list dollars, then seconds). A row's own exit 2, window cell, refusal, unruled cell or failed endpoint, and a pair it was not measured on, never shrink another row's pairs: it is listed after every complete row with its figures over the pairs it completed. One draw a cell: an order by the rule, not a ranking claim (plan 9.3).

| # | row | pairs | silent | /pair | dev | /pair | vs union | $ / merge | unit | billed $ | s / merge | tokens / merge | model-conf | incomplete | excluded | unruled calls | reused calls | not completed |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | gpt-6-sol-api | 1 of 1 | 0 | 0.00 | 0 | 0.00 | NO BETTER (0) | 0.141 | list | 0.141 | 111.0 | 26579 | 0 | - | 0 | 0 | 0 | - |
| 2 | gpt-6-luna-api | 1 of 1 | 0 | 0.00 | 1 | 1.00 | NO BETTER (0) | 0.007 | list | 0.007 | 83.5 | 26260 | 0 | - | 0 | 0 | 0 | - |
| 3 | haiku-4.5-api | 0 of 1 | - | - | - | - | - | - | list | - | - | - | 0 | not measured (not_run) on 1 of 1 | 1 | 0 | 0 | badge_access (not_run) |
| 4 | haiku-4.5-sub | 0 of 1 | - | - | - | - | - | - | api_equivalent | - | - | - | 0 | not measured (not_run) on 1 of 1 | 1 | 0 | 0 | badge_access (not_run) |
| 5 | opus-5.5-api | 0 of 1 | - | - | - | - | - | - | list | - | - | - | 0 | not measured (not_run) on 1 of 1 | 1 | 0 | 0 | badge_access (not_run) |
| 6 | opus-5.5-sub | 0 of 1 | - | - | - | - | - | - | api_equivalent | - | - | - | 0 | not measured (not_run) on 1 of 1 | 1 | 0 | 0 | badge_access (not_run) |
| 7 | sonnet-5-api | 0 of 1 | - | - | - | - | - | - | list | - | - | - | 0 | not measured (not_run) on 1 of 1 | 1 | 0 | 0 | badge_access (not_run) |
| 8 | sonnet-5-sub | 0 of 1 | - | - | - | - | - | - | api_equivalent | - | - | - | 0 | not measured (not_run) on 1 of 1 | 1 | 0 | 0 | badge_access (not_run) |
| base | concatenation | 1 of 1 | 0 | 0.00 | 9 | 9.00 | - | - | no model | - | - | - | - | - | - | - | - | - |
| base | union | 1 of 1 | 0 | 0.00 | 0 | 0.00 | - | - | no model | - | - | - | - | - | - | - | - | - |
| base | base_only | 1 of 1 | 3 | 3.00 | 3 | 3.00 | - | - | no model | - | - | - | - | - | - | - | - | - |

Floors (plan 4), scored by the same scorer from the sources with no model call: byte-concatenation, a mechanical union (the base, then every paragraph of the other not already in it, its title dropped) and base-only. `vs union` holds each row against the union on the same pairs; no better than a mechanical union: gpt-6-sol-api, gpt-6-luna-api.

Rows (688, rulings 10 and 11): the route, the effort as run, and every model id the row's reports say answered (a subscription row served by another model than its API row shows here).

| row | route | effort | answered as |
|---|---|---|---|
| gpt-6-sol-api | http | vendor default | gpt-6-sol |
| gpt-6-luna-api | http | vendor default | gpt-6-luna |
| haiku-4.5-api | http | one level (extended thinking on/off; default kept) | - |
| haiku-4.5-sub | claude | one level (extended thinking on/off; default kept) | - |
| opus-5.5-api | http | vendor default | - |
| opus-5.5-sub | claude | medium on every role (CLI) | - |
| sonnet-5-api | http | vendor default | - |
| sonnet-5-sub | claude | medium on every role (CLI) | - |

Side table, fable-sub against opus-5.5-sub, over 1 common pair(s):

| row | pairs | silent | dev | $ / merge | unit | s / merge | incomplete | not completed |
|---|---|---|---|---|---|---|---|---|
| fable-sub | 0 of 1 | - | - | - | api_equivalent | - | not measured (not_run) on 1 of 1 | badge_access (not_run) |
| opus-5.5-sub | 0 of 1 | - | - | - | api_equivalent | - | not measured (not_run) on 1 of 1 | badge_access (not_run) |

## S2: detection, over the 1 common fixtures

A row's own exit 2 on a fixture never shrinks another row's fixtures (684); such a row follows the complete ones, over what it measured.

| row | fixtures | exit codes matched | plants detected | invented | guards wrong | incomplete | disqualified |
|---|---|---|---|---|---|---|---|
| gpt-6-sol-api | 1 of 1 | 1/1 | 0/0 | 0 | 0 | - | 0 |
| gpt-6-luna-api | 1 of 1 | 1/1 | 0/0 | 0 | 0 | - | 0 |
| opus-5.5-api | 0 of 1 | 0/0 | 0/0 | 0 | 0 | not measured (not_run) on 1 of 1 | 0 |
| sonnet-5-api | 0 of 1 | 0/0 | 0/0 | 0 | 0 | not measured (not_run) on 1 of 1 | 0 |
| haiku-4.5-api | 0 of 1 | 0/0 | 0/0 | 0 | 0 | not measured (not_run) on 1 of 1 | 0 |
| opus-5.5-sub | 0 of 1 | 0/0 | 0/0 | 0 | 0 | not measured (not_run) on 1 of 1 | 0 |
| sonnet-5-sub | 0 of 1 | 0/0 | 0/0 | 0 | 0 | not measured (not_run) on 1 of 1 | 0 |
| haiku-4.5-sub | 0 of 1 | 0/0 | 0/0 | 0 | 0 | not measured (not_run) on 1 of 1 | 0 |

## S3: planted errors (fixed, min / median / max over draws)

| row | bip39 |
|---|---|
| opus-5.5-api | - (not completed: d1 (not_run)) |
| sonnet-5-api | - (not completed: d1 (not_run)) |
| haiku-4.5-api | - (not completed: d1 (not_run)) |
| gpt-6-sol-api | 11 / 11 / 11 of 14, 1 draw(s) |
| gpt-6-luna-api | 6 / 6 / 6 of 14, 1 draw(s) |
| opus-5.5-sub | - (not completed: d1 (not_run)) |
| sonnet-5-sub | - (not completed: d1 (not_run)) |
| haiku-4.5-sub | - (not completed: d1 (not_run)) |
