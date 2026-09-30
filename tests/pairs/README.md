# The nine fixture pairs

These are the document pairs the benchmark merges. Each pair is two short documents that a real organisation could plausibly have ended up with: the same procedure written twice, by different people, for different readers, at different times. The job a model is scored on is merging each pair into one document that keeps everything true from both and says what it did with anything it changed.

In each directory, `source_a.md` and `source_b.md` are the two inputs. `ideal.md` is a correct merge, written by hand. `ideal.json` is the record of what that merge did to every sentence it did not keep word for word.

Nothing here is taken from a real document. The names, numbers and wording were all invented for these fixtures. The pairs are under CC BY 4.0; see `LICENSE` in this directory.

## What each pair is

**badge_access** - Visitor badges at a front desk. Both documents describe the same routine (check ID, print the badge, collect it on the way out, chase the ones that never come back) and they barely disagree about anything. *Two versions of the same thing because:* one is the front desk's own procedure and the other is the version that was written up for the same desk under a shorter name; almost every step appears in both.

**payroll_cutoff** - When team leads have to submit timesheet totals. One document is the 2026 schedule, the other is the 2025 schedule it replaced. The deadline moved from 15:00 on the 20th to 12:00 on the 18th, and the weekend rule changed with it. *Two versions of the same thing because:* it is literally the same page, one year apart.

**loading_dock** - Booking a delivery slot at a loading dock. One document books slots through a web portal; the other still tells drivers to phone the dock supervisor on an extension that the first document says has been retired. *Two versions of the same thing because:* one was updated when the phone line went away and the other was not.

**freezer_alarm** - What the night shift does when a lab freezer alarms. The two documents cover the same call-out but stop at different points: one is stronger on logging and weekend cover, the other on the door seal and when to call the technician. *Two versions of the same thing because:* they are the same checklist as kept by two shifts, each of which wrote down the part it got asked about most.

**library_holds** - Reserved books waiting on a hold shelf. One document is written for library staff ("shelve them by the borrower's surname"), the other for borrowers ("bring your library card"). Same seven-day rule, same one extension, opposite point of view. *Two versions of the same thing because:* they are the staff-facing and public-facing copy of one policy.

**bike_docks** - What to do when a bike docking station reports a fault. One is the field crew's guide, the other the support desk's. They agree on what the fault codes mean and disagree on how many failed attempts come before the workshop is called: the field crew say two, the support desk say three. *Two versions of the same thing because:* one team wrote down the escalation path from its own end and the numbers drifted apart. This is the pair behind the README's opening example.

**index_429** - Why a clustered event ledger refuses an append with HTTP 429. One document is the general knowledge-base article: every release, every platform, three refusal paths, a fenced rejection envelope, a version-conditional footnote. The other is the write-up of one managed deployment where the refusals were traced to expensive queries. They put the same material under different headings and their `Environment` sections do not agree about scope: one says everywhere, the other lists a product, two versions, a platform and a service tier. *Two versions of the same thing because:* the general article was written first and the incident note was filed against a single customer later, and nobody folded the second into the first. This is the other real-article-scale pair, and the only one where the correct merge has to keep two scope statements and say how they relate rather than choose between them.

**trace_names** - A tracing agent that refuses a stream name containing a dot. Both documents quote the same validating regular expression and reach the same answer: rename the stream, and carry the original name somewhere else. They are support-ticket prose, unedited, with the typing errors left in. *Two versions of the same thing because:* two engineers answered the same question on different days from the same product limitation. Source B states its workaround and its resolution in identical words, which is what the `duplicate` disposition is for.

**rate_limits** - What an HTTP 429 from an API gateway means and what a client should do about it. Both documents answer the same question and they agree on the substance: honour the Retry-After header, retry only what is safe to retry, know that the batch tier is the same scheme with a larger allowance, and log every refusal. One states the batch multiple in words where the other gives the numeral, and one carries an aside about a client-side design that was rejected and that the other never mentions. *Two versions of the same thing because:* two people on the same team answered the same question, one hedging and one asserting, and neither saw the other's reply. This is the long pair: at 104 segments it is roughly three times the size of the others, so results are not measured only on short documents.

## Which pair tests what

| Pair | Property |
| --- | --- |
| payroll_cutoff | A genuine title supersession. One document's title is the other's, one year older, so a correct merge has to pick the live one and say the other was replaced. |
| loading_dock | Correct behaviour requires declaring a loss. The instruction to phone the dock supervisor is not merely reworded, it is wrong now, so it has to be removed and the removal declared. No other pair requires that, and it is the pair where the loss budget is tightest: at the default 3%, 36 segments allow exactly one declared drop and the correct answer spends it. |
| rate_limits | Length. At 104 segments across 9,772 bytes it is the only pair at the scale of a real article, so a model advantage that only appears on long input has somewhere to appear. It is also the only pair carrying non-ASCII punctuation, which the merge has to preserve byte for byte. |
| index_429 | A scope conflict that cannot be resolved by choosing. Source A's `Environment` covers every release on every platform; source B's names one version range on one platform. Neither supersedes the other, so a merge that keeps either alone loses a true statement, and the only correct answer keeps both and says which is the general case. |
| trace_names | The `duplicate` disposition, worked. Source B says the same sentence under `Workaround` and again under `Resolution`, so a merge that keeps both draws the duplicated-content check on its own output, and a merge that keeps one has to declare why the other is gone. |
| badge_access | Would score full marks under naive concatenation. The two documents are so alike that gluing them end to end looks like a reasonable merge, which is exactly the failure the headline measurement is designed to catch. |

## Every pair is proven answerable before a model sees it

A measurement over a pair nobody can answer correctly measures the pair, not the model. An earlier round of measurement showed this: three models made the same single mistake on the same fixture, byte for byte, because the fixture left no other move.

So `tests/test_pairs.py` proves each pair is answerable: `ideal.md` plus `ideal.json` is run through the same checks a model's output would be, at both strictness settings, and every pair has to come back with zero complaints. All nine do. Whatever the models get charged for, it will not be for being handed an impossible pair.

The same file also measures what the headline number rests on: stapling the two sources together, with no merging at all, keeps every sentence of both and therefore passes every check except one: it cannot choose between the two titles. That leaves exactly one countable mistake per pair per setting.

**There are two denominators.** Runs made before `index_429` and `trace_names` existed were scored over the seven pairs there were then: 7 pairs x 2 settings x 1 title = **14**, fixed before the first call. The two newer pairs are not in that figure and cannot be, or the recorded results would be fractions of a number that moved under them; the seven are named in `tests/run_arm.py` as `M9_PAIRS` for that reason. Over the corpus as it now stands the same arithmetic gives 9 x 2 x 1 = **18**, which is what a new run is scored against. `tests/test_pairs.py` counts both and asserts both.

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

A "segment" is a title, a heading or a sentence. At the default loss budget of 3%, a merge may declare it dropped at most 3% of the source segments. The one dropped segment in loading_dock is 1 of 36, which is inside that budget with no margin: two drops would be over. rate_limits at 104 segments permits three drops and the ideal merge declares one. bike_docks (35 segments) and index_429 (63) permit one drop each, and the other five pairs permit none. None of the other seven ideal merges declares a drop, because in each pair everything either survives or is superseded by something that carries it.

Two of rate_limits' 52 records are over source A's segments rather than source B's. Source B spells a count as `50` where source A spells it `fifty`; numerals must survive a merge exactly and A's words are not protected that way, so B's sentence is the one that survives and A's two lead sentences carry the superseded records.
