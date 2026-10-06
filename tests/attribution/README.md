# The six audience pairs

A merge can keep every fact from both of its sources, invent nothing, and still be wrong: it can put instructions written for one audience under a title that names another. Take a courier's guide and a laboratory technician's guide to the same sample collection. Merged under the courier's title, with no section marked, the result tells a courier to break the tamper seal at the bench. Nothing was lost. The document now tells its reader to do a job that is not theirs.

This directory holds six small document pairs built to test for that defect. Two of them carry a merge that has the defect. The other four are correct merges that look similar and must not be flagged.

**No check in LLossless detects this defect today.** The corpus exists so that a check can be built against it, and `tests/test_attribution.py` records the gap: both defective merges pass every mechanical check, the checks that compare text and use no model, with no finding. The pairs are not part of the benchmark, and no published figure uses them.

Nothing here is taken from a real document. The names, numbers and wording were invented for these pairs.

## The question each pair asks

The title does not show the defect: the correct and the defective merge of the same two documents carry the same title. The content does not show it either: both merges hold the same facts. What differs is whether the merged document tells its reader which parts are theirs. So the question is:

> Would a reader who is the audience the title names attempt a step they cannot perform, or are not allowed to perform?

A correct merge of two audiences does one of two things. It takes a title that fits both, or it marks each section that belongs to one audience with its reader, as in `## Opening the box (laboratory technician only)`. This page calls the part of a title or heading that names its reader a *qualifier*.

## The six pairs

| Pair | The two sources | A check must | Why |
|---|---|---|---|
| `incident_pager` | The pager procedure as written for the on-call engineer, and as written for the duty manager | flag `inverted.md` | Under the engineer's title, with no section marked, the engineer is told to approve customer notices and to call the executive sponsor. No sentence contradicts another. Seeing the defect takes knowing what an on-call engineer is allowed to do. |
| `sample_intake` | Collecting pathology samples, for the courier and for the laboratory technician | flag `inverted.md` | Under the courier's title the document says "Do not open the box at any point" and also "Break the tamper seal at the bench". The two instructions cannot both be followed, so the defect shows in the text alone. |
| `parking_permits` | Staff parking permits, and visitor permits | stay silent | A correct merge of two audiences: it takes the neutral title of the two, and every section that belongs to one audience names its reader. A check that fires here fires on every legitimate merge of two audiences. |
| `fire_drill` | A fire drill procedure titled for the ground floor wardens, and the same content under a general title | stay silent | Only one title names a reader, and the other document is the same content in other words, not a wider document. Everything under the wardens' title is the wardens'. |
| `kettle_descaling` | Two notes on descaling an office kettle | stay silent | Neither title names a reader, so there is no audience to check. |
| `helpdesk_tickets` | Ticket triage for the "Support Desk", and for the "Service Desk" | stay silent | Two names for one team. A check that fires here compares the words of two titles, not their audiences. |

The two pairs that must be flagged are two different defects on purpose. `sample_intake` contradicts itself, and `incident_pager` only oversteps its reader's authority. A check that catches one of the two shows, by which one, whether it read the text or reasoned about the reader.

## The files in a pair directory

| File | In | What it is |
|---|---|---|
| `source_a.md`, `source_b.md` | all six | The two inputs. |
| `ideal.md` | all six | A correct merge. It carries source A's title. |
| `ideal.json` | all six | The merge's declarations: what it did to each source segment it did not keep word for word. In every pair this is one record, which declares source B's title `superseded` by source A's. |
| `shape.json` | all six | What the pair is for. The fields are listed below. |
| `inverted.md` | `incident_pager`, `sample_intake` | The defective merge: `ideal.md` with the qualifier removed from four section headings and nothing else changed. `## Opening the box (laboratory technician only)` becomes `## Opening the box`. |
| `inverted.json` | `incident_pager`, `sample_intake` | The declarations for `inverted.md`. Byte for byte the same as `ideal.json`: the defective merge declares exactly what the correct one does. |

A segment is a title, a heading or a sentence.

The fields of `shape.json`:

| Field | In | Meaning |
|---|---|---|
| `shape` | all six | A number for the kind of pair. The numbers are labels, and these five are the only ones in use: `1`, `6`, `7`, `8` and `9`. |
| `name` | all six | The kind of pair, in words: "audience inversion" (`1`), "a legitimate two-audience merge" (`6`), "a one-sided qualifier over the same scope" (`7`), "no qualifier on either title" (`8`), "a qualifier that differs in wording and not in scope" (`9`). |
| `must_fire` | all six | `true` when a check must flag the document named in `merged_under_audit`. It is `true` exactly on the two `shape` 1 pairs. |
| `merged_under_audit` | all six | The merged document the pair tests: `inverted.md` on the two `shape` 1 pairs, `ideal.md` on the others. |
| `title_audience` | all six | The reader the merged title names, in words. |
| `why` | all six | The reason for `must_fire`. |
| `defect` | `shape` 1 only | `self_contradiction` (`sample_intake`) or `authority_mismatch` (`incident_pager`). |
| `audience_model_required` | `shape` 1 only | `true` when the defect cannot be seen from the text alone (`incident_pager`). |
| `giveaway` | `shape` 1 only | One sentence of `inverted.md` that comes from source B, the source whose title was not taken. |
| `defect_why` | `shape` 1 only | The defect, described in a paragraph. |
| `inverted_differs_from_ideal_by` | `shape` 1 only | A statement that only the heading qualifiers differ. |

Two of the `why` texts cite "section 4" of a design note that is not part of the published copy. The rule they take from it is the one above: a reader must be able to tell which part of the document is theirs.

## What uses these pairs today

**One test module, and no check in the tool.** `python3 tests/test_attribution.py` runs offline and ends with `attribution: 15 checks pass over 6 pair(s), 8 merged document(s), 0 predicates`. The `0 predicates` says that no check for this defect exists. The module asserts:

- **Every `ideal.md` is a correct answer.** With its `ideal.json` it draws no finding from the mechanical checks at two fidelity levels, `verbatim` (the strictest, spelled `off` in the test code) and `high` (the default), with source A's title kept and the default loss budget of 3%.
- **Every `inverted.md` passes the same checks, also with no finding,** and keeps exactly the source segments its `ideal.md` keeps. This is the gap, written down as an assertion. It fails on the day a mechanical check starts to flag an inverted merge, so whoever adds such a check has to update this test and this page.
- **No finding kind has a name that claims this check.** A finding kind whose name contains `audience`, `scope` or `coheren` fails the module. If such a check is real, this corpus has to be updated with it. If it is not, the name has to change.
- **The corpus has the shape described above:** six complete pairs, two that must be flagged with two different defects, four that must not, an `inverted.md` that differs from its `ideal.md` only in heading qualifiers, and a `giveaway` sentence that is in `inverted.md` and in source B only.

`tests/test_segment.py` also reads the directory: it pins how each document here splits into segments, in `tests/segment_pins.json`.

Nothing else reads these pairs. No command, harness or benchmark run uses them, and no recorded run in this repository merged them, so whether the model-based claim checks would notice the defect has not been measured.

**This is not the report's Attributions check.** That check finds a merged sentence that credits a statement to the wrong source, for example "according to source A" on a fact only source B states. It exists, and its test cases are `tests/fixtures/attribution_invented/` and `tests/fixtures/attribution_swapped/`.

## If you change this corpus

- **Keep one difference between `inverted.md` and `ideal.md`.** Same line count, same section order, same sentences: every differing line must be a `##` heading whose `ideal.md` form is the `inverted.md` form plus a qualifier in parentheses. If the two also differed in section order, a check could score on order and appear to detect audience. `test_the_inversion_differs_from_the_ideal_in_one_variable` enforces it.
- **Keep the pairs small and single-purpose.** Every pair is 25 to 29 segments and declares one record. A long pair, or one that declares drops, would test document length or the loss budget at the same time as the audience question.
- **Do not read the report's `Ordering:` line as a sign of this defect.** That line describes how the merge arranged its sources. Here it reads "each source in one unbroken block" for `ideal.md` and `inverted.md` of both flagged pairs alike, and for `parking_permits/ideal.md`: a correct merge of two audiences is grouped by audience, which is one block per source. `test_the_order_members_that_point_the_wrong_way_are_pinned` holds the measured values.
- **A new document needs a segment pin.** Add it with `python3 tests/test_segment.py --pin`. An edited document fails `tests/test_segment.py` until its entry in `tests/segment_pins.json` is replaced.

## Sizes

| Pair | Source A | Source B | Segments in both |
|---|---|---|---|
| `fire_drill` | 13 segments, 127 words | 14 segments, 143 words | 27 |
| `helpdesk_tickets` | 14 segments, 142 words | 14 segments, 129 words | 28 |
| `incident_pager` | 15 segments, 154 words | 14 segments, 140 words | 29 |
| `kettle_descaling` | 14 segments, 130 words | 14 segments, 125 words | 28 |
| `parking_permits` | 13 segments, 125 words | 12 segments, 124 words | 25 |
| `sample_intake` | 14 segments, 130 words | 14 segments, 131 words | 28 |

The pairs are about the size of the short pairs in `tests/pairs/`, which run from 27 to 36 segments.
