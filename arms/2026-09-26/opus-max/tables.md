## Cells (model claude-opus-5-5, safe mode, sourced, verify full)

| cell | n | fixed /44 | kept | other | false corr. | wall s | retrieved | searches | usage USD (API-equiv.) | output tok | merge USD |
|---|---|---|---|---|---|---|---|---|---|---|---|
| voyager xhigh | 2/2 | 38 (38-38) | 5 (5-5) | 1 (1-1) |  | 278.5 (256-301) | 2/2 | 0.5 (0-1) | 0.99685 (0.9872-1.0065) | 31918.5 (28590-35247) | 0.62555 (0.6087-0.6424) |
| voyager max | 3/3 | 38 (37-38) | 5 (5-5) | 1 (1-2) |  | 606 (574-866) | 3/3 | 2 (0-4) | 2.0426 (1.8706-3.0006) | 70464 (67482-96266) | 1.6365 (1.4989-2.6243) |
| mahjongg max | 1/1 |  |  |  | 4 (4-4) | 1608 (1608-1608) | 1/1 | 5 (5-5) | 6.4502 (6.4502-6.4502) | 208917 (208917-208917) | 3.2967 (3.2967-3.2967) |

`false corr.` above is rescored with the corrected `tests/score_planted.py` (DECISIONS 682 B10; see the mahjongg section below); first published as max 7 (7-7).

## Per run

- d1 mahjongg max a1: exit 1, 1608.1s, fixed None kept None other None fc 7, ids ['claude-haiku-4-5-20251001', 'claude-opus-5-5'], answered {'merge': ['claude-opus-5-5'], 'decompose': ['claude-opus-5-5'], 'verify': ['claude-opus-5-5']}, merge effort ['max'] checks ['low'], safe True, subagents 0, turns [20, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], searches 5, retrieval retrieved, usd 6.4502
- d1 voyager max a1: exit 1, 574.2s, fixed 38 kept 5 other 1 fc None, ids ['claude-haiku-4-5-20251001', 'claude-opus-5-5'], answered {'merge': ['claude-opus-5-5'], 'decompose': ['claude-opus-5-5'], 'verify': ['claude-opus-5-5']}, merge effort ['max'] checks ['low'], safe True, subagents 0, turns [6, 1, 1, 1, 1, 1], searches 2, retrieval retrieved, usd 1.8706
- d2 voyager max a1: exit 1, 865.9s, fixed 37 kept 5 other 2 fc None, ids ['claude-haiku-4-5-20251001', 'claude-opus-5-5'], answered {'merge': ['claude-opus-5-5'], 'decompose': ['claude-opus-5-5'], 'verify': ['claude-opus-5-5']}, merge effort ['max'] checks ['low'], safe True, subagents 0, turns [14, 1, 1, 1, 1, 1], searches 4, retrieval retrieved, usd 3.0006
- d3 voyager max a1: exit 1, 605.9s, fixed 38 kept 5 other 1 fc None, ids ['claude-haiku-4-5-20251001', 'claude-opus-5-5'], answered {'merge': ['claude-opus-5-5'], 'decompose': ['claude-opus-5-5'], 'verify': ['claude-opus-5-5']}, merge effort ['max'] checks ['low'], safe True, subagents 0, turns [8, 1, 1, 1, 1, 1], searches 0, retrieval retrieved, usd 2.0426
- d1 voyager xhigh a1: exit 1, 256.0s, fixed 38 kept 5 other 1 fc None, ids ['claude-haiku-4-5-20251001', 'claude-opus-5-5'], answered {'merge': ['claude-opus-5-5'], 'decompose': ['claude-opus-5-5'], 'verify': ['claude-opus-5-5']}, merge effort ['xhigh'] checks ['low'], safe True, subagents 0, turns [5, 1, 1, 1, 1, 1], searches 1, retrieval retrieved, usd 0.9872
- d2 voyager xhigh a1: exit 1, 301.3s, fixed 38 kept 5 other 1 fc None, ids ['claude-haiku-4-5-20251001', 'claude-opus-5-5'], answered {'merge': ['claude-opus-5-5'], 'decompose': ['claude-opus-5-5'], 'verify': ['claude-opus-5-5']}, merge effort ['xhigh'] checks ['low'], safe True, subagents 0, turns [3, 1, 1, 1, 1, 1], searches 0, retrieval retrieved, usd 1.0065

## Separation

- voyager max 37-38 vs xhigh 38-38: overlap, within the draw spread

## mahjongg false corrections

Rescored from the published runs by `tests/mahjongg_figures.py` with the corrected `tests/score_planted.py` (DECISIONS 682 B10): a declared correction that names a sentence the merge changed is that sentence's record and counts once, where the first scoring counted it twice. The sentence counts are the corrected scorer's too. As first published, false corrections: d1 7; every first-scored figure is in `scored.json` under `rescored.first_scored`.

- d1: 4 mechanical (changed 4, declared 3, 3 of them naming a changed sentence; the sentences are in the withheld copy of this file, as first scored; the counts are in scored.json)

Attempts 6, cell-draws 6, failed 0, retries kept not counted 0, total wall 1.17 h.
Usage summed over all attempts: {"total_cost_usd": 15.36, "input_tokens": 160, "output_tokens": 506966, "cache_read_input_tokens": 1693878, "cache_creation_input_tokens": 488478}
