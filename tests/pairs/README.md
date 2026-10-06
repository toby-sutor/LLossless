# The nine fixture pairs

These are the document pairs the benchmark merges. Each pair is two short documents that an organisation could plausibly have ended up with: the same procedure written twice, by different people, for different readers, at different times. A model is scored on merging each pair into one document that keeps everything true from both and says what it did with anything it changed. [The benchmark](../../docs/benchmark.md) explains the scoring.

Each pair directory holds four files:

| File | What it is |
|---|---|
| `source_a.md`, `source_b.md` | The two inputs. |
| `ideal.md` | A correct merge, written by hand. It carries source A's title. The benchmark counts how far a model's merge deviates from it. |
| `ideal.json` | The declarations of that merge: one record for each source segment it did not keep word for word, saying what happened to the segment (`superseded`, `duplicate` or `dropped`) and why. |

A *segment* is the unit the tool splits a document into: a title, a heading, a sentence, a list item, a table row or a fenced code block.

To merge a pair yourself, with the model you have configured (the README's ["Try it in two minutes"](../../README.md#try-it-in-two-minutes) shows how), run this from the repository root:

    P=tests/pairs/bike_docks
    llossless merge $P/source_a.md $P/source_b.md --base $P/source_a.md -o merged.md > report.md

Write the outputs outside this directory: `tests/test_segment.py` fails on any other `.md` file under `tests/pairs/` that it has no pin for.

Nothing here is taken from a real document. The names, numbers and wording were all invented for these fixtures. The pairs are under CC BY 4.0; see `LICENSE` in this directory.

## What each pair is

**badge_access** - Visitor badges at a front desk. Both documents describe the same routine (check ID, print the badge, collect it on the way out, chase the ones that never come back) and they barely disagree about anything. *Two versions of the same thing because:* one is the front desk's own procedure and the other is the version that was written up for the same desk under a shorter name; almost every step appears in both.

**payroll_cutoff** - When team leads have to submit timesheet totals. One document is the 2026 schedule, the other is the 2025 schedule it replaced. The deadline moved from 15:00 on the 20th to 12:00 on the 18th, and the weekend rule changed with it. *Two versions of the same thing because:* it is literally the same page, one year apart.

**loading_dock** - Booking a delivery slot at a loading dock. One document books slots through a web portal only and says the dock's phone line has been retired. The other still tells its reader to phone the dock supervisor on that line when the portal is down. *Two versions of the same thing because:* one was updated when the phone line went away and the other was not.

**freezer_alarm** - What the night shift does when a lab freezer alarms. The two documents cover the same call-out and write down different parts of it: one has the first reading, a door left ajar and when the contents may be moved, the other has the alarm panel, ice on the door seal, the log and weekend cover. Both say when to call the technician. *Two versions of the same thing because:* they are the same checklist as kept by two shifts, each of which wrote down the part it got asked about most.

**library_holds** - Reserved books waiting on a hold shelf. One document is written for library staff ("Shelve items alphabetically by the borrower's surname"), the other for borrowers ("Bring your library card"). Same seven-day rule, same one extension, opposite point of view. *Two versions of the same thing because:* they are the staff-facing and public-facing copy of one policy.

**bike_docks** - What to do when a bike docking station reports a fault. One is the field crew's guide, the other the support desk's. They agree on what the fault codes mean and disagree on how many failed attempts come before the workshop is called: the field crew say two, the support desk say three. *Two versions of the same thing because:* one team wrote down the escalation path from its own end and the numbers drifted apart. This is the pair in the README's section ["A real example"](../../README.md#a-real-example).

**index_429** - Why a clustered event ledger refuses an append with HTTP 429. One document is the general knowledge-base article: every release, every platform, three refusal paths, a fenced rejection envelope, a version-conditional footnote. The other is the write-up of one managed deployment where the refusals were traced to expensive queries. They put the same material under different headings and their `Environment` sections do not agree about scope: one says everywhere, the other lists a product, two versions, a platform and a service tier. *Two versions of the same thing because:* the general article was written first and the incident note was filed against a single customer later, and nobody folded the second into the first. This is the second-longest pair, and the only one where the correct merge has to keep two scope statements and say how they relate instead of choosing between them.

**trace_names** - A tracing agent that refuses a stream name containing a dot. Both documents quote the same validating regular expression and reach the same answer: rename the stream, and carry the original name somewhere else. They are written as support-ticket prose, with typing errors left in on purpose. *Two versions of the same thing because:* two engineers answered the same question on different days from the same product limitation. Source B states its workaround and its resolution in identical words, which is what the `duplicate` record is for.

**rate_limits** - What an HTTP 429 from an API gateway means and what a client should do about it. Both documents answer the same question and they agree on the substance: honour the Retry-After header, retry only what is safe to retry, know that the batch tier is the same scheme with a larger allowance, and log every refusal. One states the batch multiple in words where the other gives the numeral, and one carries an aside about a client-side design that was rejected and that the other never mentions. *Two versions of the same thing because:* two people on the same team answered the same question, one hedging and one asserting, and neither saw the other's reply. This is the long pair: at 104 segments it is about three times the size of the short ones, so results are not measured only on short documents.

## Which pair tests what

| Pair | Property |
| --- | --- |
| payroll_cutoff | A genuine title supersession. One document's title is the other's, one year older, so a correct merge has to pick the live one and say the other was replaced. |
| loading_dock | Correct behaviour requires declaring a loss. The instruction to phone the dock supervisor is not merely reworded, it is wrong now, so it has to be removed and the removal declared. This is also the pair where the loss budget is tightest: at the default 3%, 36 segments allow exactly one declared drop and the correct answer spends it. |
| rate_limits | Length. At 104 segments across 9,772 bytes it is the longest pair, so a model advantage that only appears on long input has somewhere to appear. It is also the only pair carrying non-ASCII punctuation, which the merge has to preserve byte for byte. |
| index_429 | A scope conflict that cannot be resolved by choosing. Source A's `Environment` covers every release on every platform; source B's names two versions on one platform. Neither supersedes the other, so a merge that keeps either alone loses a true statement, and the only correct answer keeps both and says which is the general case. |
| trace_names | The `duplicate` record, worked. Source B says the same sentence under `Workaround` and again under `Resolution`, so a merge that keeps both draws the "Stated twice" finding on its own output, and a merge that keeps one has to declare why the other is gone. |
| badge_access | Pasting the two sources together looks like a reasonable merge. The documents are so alike that a paste keeps every sentence and reads acceptably. It is still wrong: it carries two titles and states nine sentences twice. |

## Every pair has a correct answer, and a test proves it

A pair that nobody can answer correctly measures the pair, not the model: every model is charged the same unavoidable finding. So `tests/test_pairs.py` runs each pair's `ideal.md`, with its `ideal.json`, through the mechanical checks (the checks that compare text and use no model, the same ones a model's merge goes through) and requires that they report nothing. It does this at two fidelity levels: `verbatim`, the strictest, which the test code spells by its older name `off`, and `high`, the default. Source A is the base document and its title is kept (`--title-policy keep-base`), and the loss budget is the default 3%. All nine pairs pass at both levels.

The same test shows that pasting the two sources together is never a correct answer. A paste keeps every source segment, so nothing is reported missing. On all nine pairs it still draws a "Title dropped in silence" finding: source B's title is not the merged title, and no record says what replaced it. On four pairs (`badge_access`, `loading_dock`, `payroll_cutoff`, `trace_names`) it also draws a "Stated twice" finding for each sentence it now repeats.

## Which runs use all nine

The release benchmark of 2026-09-27 scores all nine pairs. `index_429` and `trace_names` were added on 2026-08-30. One older harness, `tests/run_arm.py`, which drove a model-size study in August 2026, runs only the seven pairs that existed before that date: its constant `M9_PAIRS` names them, so adding a pair here does not change what that study covered. `tests/test_pairs.py` asserts both sets. It counts one source title that cannot be the merged title, per pair and per fidelity level: 14 over the seven pairs in that constant, 18 over the nine in this directory.

## If you add or change a pair

Published results were measured on these exact files, and `tests/test_segment.py` pins how each of them splits into segments (`tests/segment_pins.json`). Editing a source or an `ideal.md` makes that test fail. A new pair is pinned with `python3 tests/test_segment.py --pin`.

`tests/test_pairs.py` requires of every pair:

- **The four files, and nine directories in total.** The count is written into the test, and into `tests/test_reconcile.py` and `tests/test_handwritten.py`, so a new pair stops the suite until each count is changed on purpose.
- **One title per source, and the two titles differ.** A merge then always has one title to give up and declare replaced.
- **No source title longer than 64 characters.** A record's reason is capped at 80 characters and usually quotes the title, so a longer title gets the reason cut off and the record rejected.
- **An `ideal.md` that draws no finding** at `verbatim` and at `high`, as described above.
- **Only `superseded`, `duplicate` and `dropped` in `ideal.json`.** These are the records `verbatim` accepts. A `duplicate` record must name a segment that another source segment repeats character for character.
- **A known result for a paste of the two sources:** every segment kept, one finding for the second title, and as many "Stated twice" findings as the test's `STAPLE_REPEATS` table lists for the pair.

## Sizes

| Pair | Source A | Source B | Segments | Records in the ideal merge |
| --- | --- | --- | --- | --- |
| badge_access | 17 segments, 202 words | 16 segments, 187 words | 33 | 1 superseded |
| bike_docks | 17 segments, 185 words | 18 segments, 167 words | 35 | 8 superseded |
| freezer_alarm | 18 segments, 191 words | 15 segments, 159 words | 33 | 5 superseded |
| library_holds | 15 segments, 165 words | 14 segments, 136 words | 29 | 5 superseded |
| loading_dock | 20 segments, 187 words | 16 segments, 133 words | 36 | 13 superseded, 1 dropped |
| payroll_cutoff | 19 segments, 185 words | 14 segments, 137 words | 33 | 6 superseded |
| rate_limits | 52 segments, 843 words | 52 segments, 966 words | 104 | 50 superseded, 1 duplicate, 1 dropped |
| index_429 | 33 segments, 556 words | 30 segments, 331 words | 63 | 4 superseded |
| trace_names | 14 segments, 162 words | 13 segments, 108 words | 27 | 4 superseded, 1 duplicate |

The nine pairs hold 393 source segments in total. At the default loss budget of 3%, a merge may declare at most 3% of the source segments dropped: three segments on rate_limits, one each on loading_dock, bike_docks and index_429, and none on the other five pairs. Only two ideal merges declare a drop, loading_dock and rate_limits, one segment each. In the other seven, everything either survives or is superseded by something that carries it.

Two of rate_limits' 52 records are over source A's segments, not source B's. Source B writes a count as `50` where source A writes `fifty`. Numerals must survive a merge exactly and number words are not protected that way, so B's sentence is the one that survives and A's two lead sentences carry the superseded records.
