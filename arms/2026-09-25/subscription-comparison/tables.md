## Cells

Median (min-max) over the draws that produced a report. `n` = draws scored of those run; `ret` = runs that retrieved.

| pair | model | merge effort | n | fixed | kept | other | licence | false corr. | wall s | ret | answered by |
|---|---|---|---|---|---|---|---|---|---|---|---|
| voyager | opus | low | 3/3 | 28 (20-33) | 11 (5-20) | 5 (4-6) |  |  | 160 (138-162) | 0/3 | claude-opus-5 |
| voyager | opus | medium | 3/3 | 36 (26-39) | 6 (5-12) | 2 (0-6) |  |  | 260 (235-304) | 3/3 | claude-opus-5 |
| voyager | opus | high | 3/3 | 37 (37-38) | 6 (5-6) | 1 (1-1) |  |  | 364 (355-387) | 3/3 | claude-opus-5 |
| voyager | opus | xhigh | 3/3 | 38 (37-39) | 5 (5-6) | 0 (0-2) |  |  | 403 (391-779) | 3/3 | claude-opus-5 |
| voyager | sonnet | low | 3/3 | 18 (8-19) | 22 (19-34) | 4 (2-6) |  |  | 261 (179-278) | 2/3 | claude-sonnet-5 |
| voyager | sonnet | medium | 3/3 | 30 (26-31) | 10 (6-13) | 5 (3-8) |  |  | 407 (332-416) | 3/3 | claude-sonnet-5 |
| voyager | sonnet | high | 3/3 | 28 (24-35) | 9 (5-11) | 7 (4-9) |  |  | 667 (512-1172) | 3/3 | claude-sonnet-5 |
| voyager | sonnet | xhigh | 3/3 | 31 (24-35) | 8 (7-10) | 5 (2-10) |  |  | 664 (639-748) | 3/3 | claude-sonnet-5 |
| voyager | haiku | medium | 3/3 | 6 (2-16) | 26 (16-32) | 12 (6-16) |  |  | 663 (532-877) | 0/3 | claude-haiku-4-5-20251001 |
| bip39 | opus | low | 3/3 | 12 (12-13) |  |  | other, other, other |  | 162 (124-171) | 0/3 | claude-opus-5 |
| bip39 | opus | medium | 3/3 | 13 (13-14) |  |  | other, fixed, fixed |  | 266 (214-267) | 3/3 | claude-opus-5 |
| bip39 | opus | high | 3/3 | 14 (13-14) |  |  | fixed, fixed, fixed |  | 216 (196-309) | 3/3 | claude-opus-5 |
| bip39 | opus | xhigh | 3/3 | 14 (14-14) |  |  | fixed, fixed, fixed |  | 266 (219-293) | 3/3 | claude-opus-5 |
| bip39 | sonnet | low | 3/3 | 11 (11-13) |  |  | fixed, fixed, fixed |  | 142 (131-183) | 3/3 | claude-sonnet-5 |
| bip39 | sonnet | medium | 3/3 | 13 (11-14) |  |  | fixed, fixed, fixed |  | 197 (191-206) | 3/3 | claude-sonnet-5 |
| bip39 | sonnet | high | 3/3 | 13 (12-14) |  |  | fixed, fixed, fixed |  | 309 (288-333) | 3/3 | claude-sonnet-5 |
| bip39 | sonnet | xhigh | 3/3 | 14 (14-14) |  |  | fixed, fixed, fixed |  | 359 (324-367) | 3/3 | claude-sonnet-5 |
| bip39 | haiku | medium | 3/3 | 9 (6-10) |  |  | kept, kept, kept |  | 578 (538-588) | 0/3 | claude-haiku-4-5-20251001 |
| mahjongg | opus | medium | 3/3 |  |  |  |  | 2 (1-2) | 1104 (1049-1315) | 1/3 | claude-opus-5 |
| mahjongg | sonnet | medium | 3/3 |  |  |  |  | 0 (0-1) | 1025 (909-1075) | 3/3 | claude-sonnet-5 |

`false corr.` above is rescored with the corrected `tests/score_planted.py` (DECISIONS 682 B10; see the mahjongg section below); first published as opus 3 (2-3), sonnet 0 (0-1).

## Separation (ranges over K do not overlap)

- voyager: opus/low (20, 33) vs opus/high (37, 38)
- voyager: opus/low (20, 33) vs opus/xhigh (37, 39)
- voyager: opus/low (20, 33) vs sonnet/low (8, 19)
- voyager: opus/low (20, 33) vs haiku/medium (2, 16)
- voyager: opus/medium (26, 39) vs sonnet/low (8, 19)
- voyager: opus/medium (26, 39) vs haiku/medium (2, 16)
- voyager: opus/high (37, 38) vs sonnet/low (8, 19)
- voyager: opus/high (37, 38) vs sonnet/medium (26, 31)
- voyager: opus/high (37, 38) vs sonnet/high (24, 35)
- voyager: opus/high (37, 38) vs sonnet/xhigh (24, 35)
- voyager: opus/high (37, 38) vs haiku/medium (2, 16)
- voyager: opus/xhigh (37, 39) vs sonnet/low (8, 19)
- voyager: opus/xhigh (37, 39) vs sonnet/medium (26, 31)
- voyager: opus/xhigh (37, 39) vs sonnet/high (24, 35)
- voyager: opus/xhigh (37, 39) vs sonnet/xhigh (24, 35)
- voyager: opus/xhigh (37, 39) vs haiku/medium (2, 16)
- voyager: sonnet/low (8, 19) vs sonnet/medium (26, 31)
- voyager: sonnet/low (8, 19) vs sonnet/high (24, 35)
- voyager: sonnet/low (8, 19) vs sonnet/xhigh (24, 35)
- voyager: sonnet/medium (26, 31) vs haiku/medium (2, 16)
- voyager: sonnet/high (24, 35) vs haiku/medium (2, 16)
- voyager: sonnet/xhigh (24, 35) vs haiku/medium (2, 16)
- bip39: opus/low (12, 13) vs opus/xhigh (14, 14)
- bip39: opus/low (12, 13) vs sonnet/xhigh (14, 14)
- bip39: opus/low (12, 13) vs haiku/medium (6, 10)
- bip39: opus/medium (13, 14) vs haiku/medium (6, 10)
- bip39: opus/high (13, 14) vs haiku/medium (6, 10)
- bip39: opus/xhigh (14, 14) vs sonnet/low (11, 13)
- bip39: opus/xhigh (14, 14) vs haiku/medium (6, 10)
- bip39: sonnet/low (11, 13) vs sonnet/xhigh (14, 14)
- bip39: sonnet/low (11, 13) vs haiku/medium (6, 10)
- bip39: sonnet/medium (11, 14) vs haiku/medium (6, 10)
- bip39: sonnet/high (12, 14) vs haiku/medium (6, 10)
- bip39: sonnet/xhigh (14, 14) vs haiku/medium (6, 10)

34 of 72 cell pairs separate.

## voyager: planted errors by fixed rate, hardest first (27 runs)

| # | original -> planted | all | opus | sonnet | haiku | kept/other in all |
|---|---|---|---|---|---|---|
| 34 | `opacity.` -> `transparency.` | 0% | 0/12 | 0/12 | 0/3 | 27/0 |
| 3 | `4.5 years.` -> `4,5 years.` | 7% | 0/12 | 0/12 | 2/3 | 25/0 |
| 11 | `2.5 hours` -> `2,5 hours` | 7% | 0/12 | 0/12 | 2/3 | 25/0 |
| 39 | `17,560 miles` -> `17.560 miles` | 19% | 3/12 | 0/12 | 2/3 | 21/1 |
| 40 | `(28,260 kilometers),` -> `(28.260 kilometers),` | 19% | 3/12 | 0/12 | 2/3 | 21/1 |
| 42 | `week` -> `day` | 30% | 7/12 | 1/12 | 0/3 | 9/10 |
| 9 | `long-range` -> `short-range` | 37% | 8/12 | 2/12 | 0/3 | 15/2 |
| 10 | `Nov. 4, 1985,` -> `Jan. 31, 1987,` | 41% | 9/12 | 2/12 | 0/3 | 0/16 |
| 16 | `10` -> `11` | 41% | 6/12 | 5/12 | 0/3 | 16/0 |
| 28 | `55 degrees` -> `66 degrees` | 41% | 9/12 | 2/12 | 0/3 | 6/10 |
| 31 | `ocean` -> `lake` | 44% | 7/12 | 5/12 | 0/3 | 14/1 |
| 38 | `larger` -> `smaller` | 44% | 12/12 | 0/12 | 0/3 | 9/6 |
| 7 | `5.5 hours` -> `6.4 days` | 48% | 9/12 | 4/12 | 0/3 | 12/2 |
| 25 | `1787),` -> `1687),` | 48% | 8/12 | 5/12 | 0/3 | 2/12 |
| 12 | `400` -> `five-hundred` | 52% | 9/12 | 5/12 | 0/3 | 7/6 |
| 29 | `450 miles per hour` -> `450 km/h` | 52% | 8/12 | 6/12 | 0/3 | 11/2 |
| 30 | `(724 kilometers per hour)` -> `(72400 meters per hour)` | 52% | 8/12 | 6/12 | 0/3 | 2/11 |
| 14 | `50,640 miles` -> `50,640 kilometers` | 59% | 10/12 | 6/12 | 0/3 | 5/6 |
| 2 | `two` -> `three` | 63% | 11/12 | 6/12 | 0/3 | 9/1 |
| 13 | `17:59 UT Jan. 24, 1986,` -> `17:59 ED Jan. 24, 1968,` | 63% | 12/12 | 5/12 | 0/3 | 0/10 |
| 32 | `497 miles` -> `479 miles` | 63% | 11/12 | 6/12 | 0/3 | 3/7 |
| 26 | `two` -> `three` | 67% | 9/12 | 9/12 | 0/3 | 9/0 |
| 6 | `2` -> `1` | 70% | 12/12 | 7/12 | 0/3 | 8/0 |
| 5 | `Neptune:` -> `Saturn:` | 74% | 12/12 | 8/12 | 0/3 | 7/0 |
| 27 | `nine` -> `eight` | 74% | 11/12 | 9/12 | 0/3 | 7/0 |
| 33 | `(800 kilometers)` -> `(900 kilometers)` | 74% | 12/12 | 8/12 | 0/3 | 7/0 |
| 41 | `decade-long` -> `century-long` | 74% | 12/12 | 8/12 | 0/3 | 4/3 |
| 8 | `2's` -> `1's` | 78% | 8/12 | 12/12 | 1/3 | 0/6 |
| 15 | `(81,500 kilometers).` -> `(81,500 miles).` | 81% | 11/12 | 11/12 | 0/3 | 4/1 |
| 17 | `Puck,` -> `Pucka,` | 81% | 11/12 | 11/12 | 0/3 | 3/2 |
| 18 | `Portia,` -> `Portila,` | 85% | 11/12 | 11/12 | 1/3 | 3/1 |
| 19 | `Juliet,` -> `Juliette,` | 85% | 11/12 | 11/12 | 1/3 | 3/1 |
| 20 | `Cressida,` -> `Kressida,` | 85% | 11/12 | 11/12 | 1/3 | 3/1 |
| 21 | `Rosalind,` -> `Rosalinde,` | 85% | 11/12 | 11/12 | 1/3 | 3/1 |
| 22 | `Cordelia,` -> `Cordelina,` | 85% | 11/12 | 11/12 | 1/3 | 3/1 |
| 23 | `` -> `II` | 85% | 11/12 | 11/12 | 1/3 | 3/1 |
| 24 | `Shakespeare,` -> `Goethe,` | 85% | 12/12 | 11/12 | 0/3 | 2/2 |
| 43 | `seven` -> `six` | 85% | 12/12 | 11/12 | 0/3 | 4/0 |
| 35 | `Ariel,` -> `Ariele,` | 89% | 11/12 | 12/12 | 1/3 | 3/0 |
| 36 | `Umbriel,` -> `Umbrella,` | 89% | 11/12 | 12/12 | 1/3 | 3/0 |
| 44 | `Jan. 28, 1986.` -> `Feb. 28, 1986.` | 89% | 12/12 | 12/12 | 0/3 | 0/3 |
| 37 | `Titania,` -> `Titan,` | 93% | 12/12 | 12/12 | 1/3 | 2/0 |
| 1 | `2` -> `3` | 100% | 12/12 | 12/12 | 3/3 | 0/0 |
| 4 | `Uranus` -> `Ur anus` | 100% | 12/12 | 12/12 | 3/3 | 0/0 |

Runs fixing all 44: 0

## bip39: planted errors by fixed rate, hardest first (27 runs)

| # | original -> planted | all | opus | sonnet | haiku | kept/other in all |
|---|---|---|---|---|---|---|
| 6 | `randomness` -> `determinism` | 63% | 9/12 | 8/12 | 0/3 | 10/0 |
| 4 | `MIT` -> `GPL` | 74% | 8/12 | 12/12 | 0/3 | 3/4 |
| 5 | `seed.` -> `satoshis.` | 78% | 11/12 | 10/12 | 0/3 | 5/1 |
| 13 | `end` -> `start` | 78% | 12/12 | 7/12 | 2/3 | 6/0 |
| 3 | `binary` -> `ASCII` | 85% | 12/12 | 11/12 | 0/3 | 3/1 |
| 14 | `11 bits,` -> `12 bits,` | 89% | 12/12 | 10/12 | 2/3 | 3/0 |
| 2 | `wallets.` -> `UTOXs.` | 93% | 12/12 | 12/12 | 1/3 | 1/1 |
| 1 | `words` -> `letters` | 96% | 12/12 | 12/12 | 2/3 | 1/0 |
| 7 | `seed.` -> `süeed.` | 100% | 12/12 | 12/12 | 3/3 | 0/0 |
| 8 | `mnemonic` -> `memonic` | 100% | 12/12 | 12/12 | 3/3 | 0/0 |
| 9 | `mnemonic` -> `demonic` | 100% | 12/12 | 12/12 | 3/3 | 0/0 |
| 10 | `32 bits.` -> `23 bits.` | 100% | 12/12 | 12/12 | 3/3 | 0/0 |
| 11 | `128-256 bits.` -> `1024-2048 byts.` | 100% | 12/12 | 12/12 | 3/3 | 0/0 |
| 12 | `SHA256` -> `SHA652` | 100% | 12/12 | 12/12 | 3/3 | 0/0 |

Runs fixing all 14: 11 [('opus', 'high', 1), ('opus', 'high', 3), ('opus', 'medium', 2), ('opus', 'xhigh', 1), ('opus', 'xhigh', 2), ('opus', 'xhigh', 3), ('sonnet', 'high', 1), ('sonnet', 'medium', 1), ('sonnet', 'xhigh', 1), ('sonnet', 'xhigh', 2), ('sonnet', 'xhigh', 3)]

## mahjongg false corrections, every one

Rescored from the published runs by `tests/mahjongg_figures.py` with the corrected `tests/score_planted.py` (DECISIONS 682 B10): a declared correction that names a sentence the merge changed is that sentence's record and counts once, where the first scoring counted it twice. The sentence counts are the corrected scorer's too. As first published, false corrections: opus d1 2, d2 3, d3 3; sonnet d1 0, d2 1, d3 0; every first-scored figure is in `scored.json` under `rescored.first_scored`.

- opus d1: 1 (changed 1, declared 1, 1 of them naming a changed sentence; verbatim 214/215, adds-only 0, drops-only 0, no source 0)
- opus d2: 2 (changed 2, declared 1, 1 of them naming a changed sentence; verbatim 210/215, adds-only 2, drops-only 1, no source 0)
- opus d3: 2 (changed 2, declared 1, 1 of them naming a changed sentence; verbatim 214/216, adds-only 0, drops-only 0, no source 0)
- sonnet d1: 0 (changed 0, declared 0, 0 of them naming a changed sentence; verbatim 215/215, adds-only 0, drops-only 0, no source 0)
- sonnet d2: 1 (changed 0, declared 1, 0 of them naming a changed sentence; verbatim 215/216, adds-only 0, drops-only 0, no source 1)
- sonnet d3: 0 (changed 0, declared 0, 0 of them naming a changed sentence; verbatim 215/215, adds-only 0, drops-only 0, no source 0)

## Registered predictions

- HELD: 1 no voyager cell fixes all in every draw -- []
- HELD: 2 Opus median above Sonnet's on voyager at every effort -- low: opus 28 sonnet 18, medium: opus 36 sonnet 30, high: opus 37 sonnet 28, xhigh: opus 38 sonnet 31
- HELD: 3 Haiku below every Opus and Sonnet voyager median -- haiku 6; at or below: []
- FAILED: 4 no two effort levels of one model separate on voyager -- opus low (20, 33) vs high (37, 38); opus low (20, 33) vs xhigh (37, 39); sonnet low (8, 19) vs medium (26, 31); sonnet low (8, 19) vs high (24, 35); sonnet low (8, 19) vs xhigh (24, 35)
- HELD: 5 bip39 fraction above voyager's in every Opus/Sonnet cell -- []
- HELD: 6 the four format errors below the median error's rate -- median 0.6851851851851851; #3 7%, #11 7%, #39 19%, #40 19%
- HELD: 7 at least 80% of Opus/Sonnet runs retrieve -- 83% of 54
- HELD: 8 MIT restored in at least 75% of Opus/Sonnet bip39 runs -- 83% of 24
- HELD: 9 no numeric substitution in mahjongg -- []

Retries after a completed exit 3, kept and not counted: d2 mahjongg opus medium a2 exit 0

Attempts 61, cell-draws 60, failed 0, total wall 7.58 h.
