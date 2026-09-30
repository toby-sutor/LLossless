## Verdict

**1 finding(s).** In the claims: 1 partially invented.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 17 |
| Claims extracted from `source_a.md` | 11 |
| Claims extracted from `source_b.md` | 10 |
| Forward — source claims accounted for in the merge | **21/21** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **11/11** |
| Forward — `source_b.md` claims accounted for | **10/10** |
| Reverse — merge claims found in a source | **16/17** |
| Reverse — supported only in part | 1 |
| Evidence grounded | **38/38** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Partly invented — the sources carry some of this claim

- **M-001** (`merged.md:5`) — You can reserve an item that is on loan at another branch.
  - evidence: 'You can reserve an item that is on loan or held at another branch.' in `source_b.md` (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - rationale: The source allows reserving an item that is on loan, but does not specify that the on-loan item is at another branch as opposed to elsewhere.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 11 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 11 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | When a requested item arrives, a hold slip is printed and folded into the item so the name is visible from the spine. | 5 | carried | 'staff print a hold slip and fold it into the item so the name is visible from the spine' in `merged.md` -- Directly stated in the text about placing an item on the shelf. |
| 2 | Items are shelved alphabetically by the borrower's surname. | 6 | carried | "shelve items alphabetically by the borrower's surname" in `merged.md` -- Directly stated. |
| 3 | An item waits on the hold shelf for 7 days. | 11 | carried | 'An item waits on the hold shelf for 7 days' in `merged.md` -- Directly stated. |
| 4 | Day one is the day the borrower is notified, not the day the item arrived. | 11 | carried | 'counted from the day the borrower is notified by email, not the day the item arrived' in `merged.md` -- Directly stated. |
| 5 | The shelf is swept every morning before opening. | 16 | carried | 'Sweep the shelf every morning before opening' in `merged.md` -- Directly stated. |
| 6 | Items past 7 days go back into circulation. | 16 | carried | 'Items past 7 days go back into circulation' in `merged.md` -- Directly stated. |
| 7 | Items past 7 days go on to the next borrower in the queue if there is one. | 16 | carried | 'or on to the next borrower in the queue if there is one' in `merged.md` -- Directly stated. |
| 8 | A borrower who asks before the 7 days are up can have the item held for a further 7 days. | 21 | carried | 'A borrower who asks before the 7 days are up can have the item held for a further 7 days' in `merged.md` -- Directly stated. |
| 9 | This further hold is granted once per request. | 22 | carried | 'This is granted once per request' in `merged.md` -- Directly stated. |
| 10 | An item that has been on the hold shelf twice without being collected goes back to the shelves. | 26 | carried | 'An item that has been on the hold shelf twice without being collected goes back to the shelves' in `merged.md` -- Directly stated. |
| 11 | An item that has been on the hold shelf twice without being collected has its request cancelled. | 26 | carried | 'the request is cancelled' in `merged.md` -- Directly stated. |

### `source_b.md` -- 10 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 10 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | You can reserve an item that is on loan or held at another branch. | 5 | carried | 'You can reserve an item that is on loan or held at another branch' in `merged.md` -- Directly stated. |
| 2 | You will be emailed when the reserved item is ready to collect. | 5 | carried | 'you will be emailed when it is ready to collect' in `merged.md` -- Directly stated. |
| 3 | You need to bring your library card to collect a reserved item. | 10 | carried | 'Bring your library card when you come to collect your item' in `merged.md` -- States the requirement to bring the library card to collect. |
| 4 | Items are placed on the hold shelf under your surname. | 10 | carried | "shelve items alphabetically by the borrower's surname" in `merged.md` -- Items are shelved by surname, matching the claim that they are placed under your surname. |
| 5 | You have 7 days from the day the library emails you to collect the item. | 10 | carried | 'An item waits on the hold shelf for 7 days, counted from the day the borrower is notified by email, not the day the item arrived.' in `merged.md` -- States the 7-day window starts from the day the borrower is emailed. |
| 6 | If you ask before the 7 days are up, the library will hold the item for another 7 days. | 15 | carried | 'A borrower who asks before the 7 days are up can have the item held for a further 7 days' in `merged.md` -- Directly matches the claim. |
| 7 | This extension can be done once per reservation. | 16 | carried | 'This is granted once per request' in `merged.md` -- Request and reservation refer to the same thing in this context, so this supports the once-per-reservation claim. |
| 8 | An item that is not collected goes back into circulation or on to the next person waiting. | 20 | carried | 'Items past 7 days go back into circulation, or on to the next borrower in the queue if there is one.' in `merged.md` -- Directly matches the claim. |
| 9 | If an item is not collected twice with the same reservation, the reservation is cancelled. | 21 | carried | 'An item that has been on the hold shelf twice without being collected goes back to the shelves, the request is cancelled' in `merged.md` -- States that after two uncollected holds the request/reservation is cancelled. |
| 10 | If an item is not collected twice with the same reservation, you will need to reserve it again. | 22 | carried | 'the borrower will need to reserve it again' in `merged.md` -- Directly states the need to reserve again after two failed collections. |

### `merged.md` -- 17 claim(s): 0 invented, 0 contradicted, 1 supported in part, 16 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | You can reserve an item that is on loan at another branch. | supported in part | `source_b.md` | 'You can reserve an item that is on loan or held at another branch.' in `source_b.md` -- The source allows reserving an item that is on loan, but does not specify that the on-loan item is at another branch as opposed to elsewhere. |
| 2 | You can reserve an item that is held at another branch. | supported | `source_b.md` | 'You can reserve an item that is on loan or held at another branch.' in `source_b.md` -- The source states you can reserve an item held at another branch. |
| 3 | You will be emailed when the item is ready to collect. | supported | `source_b.md` | 'We will email\nyou when it is ready to collect.' in `source_b.md` -- Directly stated in source_b. |
| 4 | When a requested item arrives, staff print a hold slip. | supported | `source_a.md` | 'When a requested item arrives, print a hold slip' in `source_a.md` -- Matches source_a's instruction. |
| 5 | Staff fold the hold slip into the item so the name is visible from the spine. | supported | `source_a.md` | 'fold it into the item so the\nname is visible from the spine' in `source_a.md` -- Matches source_a's instruction. |
| 6 | Staff shelve items alphabetically by the borrower's surname. | supported | `source_a.md` | "Shelve items alphabetically by the borrower's\nsurname." in `source_a.md` -- Matches source_a's instruction. |
| 7 | Borrowers must bring their library card when they come to collect their item. | supported | `source_b.md` | 'Bring your library card.' in `source_b.md` -- Directly stated in source_b. |
| 8 | An item waits on the hold shelf for 7 days. | supported | `source_a.md` | 'An item waits on the hold shelf for 7 days.' in `source_a.md` -- Directly stated in source_a. |
| 9 | The 7 days are counted from the day the borrower is notified by email, not the day the item arrived. | supported | `source_a.md` | 'Day one is the day the borrower is notified, not the day the item arrived.' in `source_a.md` -- Source_a establishes the day count begins at notification not arrival, while source_b's 'You have 7 days from the day we email you' identifies the notification method as email, jointly entailing the claim. |
| 10 | The shelf is swept every morning before opening. | supported | `source_a.md` | 'Sweep the shelf every morning before opening.' in `source_a.md` -- Directly stated in source_a. |
| 11 | Items past 7 days go back into circulation. | supported | `source_a.md` | 'Items past 7 days go back into circulation, or on\nto the next borrower in the queue if there is one.' in `source_a.md` -- Directly stated in source_a. |
| 12 | Items past 7 days go on to the next borrower in the queue if there is one. | supported | `source_a.md` | 'Items past 7 days go back into circulation, or on\nto the next borrower in the queue if there is one.' in `source_a.md` -- Directly stated in source_a. |
| 13 | A borrower who asks before the 7 days are up can have the item held for a further 7 days. | supported | `source_a.md` | 'A borrower who asks before the 7 days are up can have the item held for a further\n7 days.' in `source_a.md` -- Directly stated in source_a. |
| 14 | This extension is granted once per request. | supported | `source_a.md` | 'This is granted once per request.' in `source_a.md` -- Directly stated in source_a. |
| 15 | An item that has been on the hold shelf twice without being collected goes back to the shelves. | supported | `source_a.md` | 'An item that has been on the hold shelf twice without being collected goes back\nto the shelves and the request is cancelled.' in `source_a.md` -- Directly stated in source_a. |
| 16 | The request is cancelled when an item has been on the hold shelf twice without being collected. | supported | `source_a.md` | 'An item that has been on the hold shelf twice without being collected goes back\nto the shelves and the request is cancelled.' in `source_a.md` -- Directly stated in source_a. |
| 17 | The borrower will need to reserve the item again if it has been on the hold shelf twice without being collected. | supported | `source_b.md` | 'If this happens twice with the same reservation, the reservation is\ncancelled and you will need to reserve it again.' in `source_b.md` -- Directly stated in source_b. |

## Structure

**9** mechanical check(s) over **29** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **17** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **21**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 3 run(s) over 14 attributed segment(s) — sources interleaved. 6 of 11 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

No structural finding.

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **19** departure(s) from its sources. Checking them confirms 15, rejects 0, and leaves 4 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 29 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | Base title chosen over this one. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Hold Shelf Management' and says so (no claim traced to it) |
| `b2` | superseded | Reservation content merged under base heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b3` | subsumed | Reservation fact folded into combined opening sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-001`) |
| `b4` | subsumed | Email notice folded into combined opening sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-002`) |
| `a3` | reworded | Merged with a4 into one process sentence with added subject. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-001`) |
| `a4` | reworded | Combined with a3 into one process sentence. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-002`) |
| `b5` | superseded | Collecting content merged under base heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b6` | subsumed | Patron instruction folded into placing/collecting paragraph. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-003`) |
| `b7` | duplicate | Same shelving-by-surname fact as a4. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-004`) |
| `a6` | reworded | Combined with a7 and b8 into one timing statement. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-003`) |
| `a7` | subsumed | Day-one detail folded into combined timing statement. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-004`) |
| `b8` | duplicate | Same 7-day timing fact as a6/a7. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-005`) |
| `b13` | duplicate | Same return/queue fact as a10. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-008`) |
| `b9` | superseded | Extending content merged under base heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b10` | duplicate | Same extension fact as a12. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-006`) |
| `b11` | duplicate | Same once-per-request limit as a13. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-007`) |
| `b12` | superseded | Non-collection content merged, largely under base heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a15` | reconciled | Combined with b14's re-reservation detail. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-010`, `A-011`) |
| `b14` | reconciled | Adds re-reservation detail combined with a15's cancellation fact. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-009`, `B-010`) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | ec0c9ecb43e3 (hosted) |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | claude-sonnet-5 |
| Model (decompose) | claude-sonnet-5 |
| Model (verify) | claude-sonnet-5 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile anthropic |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 6 live, 0 cached, 0 replayed |
| Tokens | 18,510 in, 26,494 out |
| Cost | ~$0.30 estimated (rates read 2026-08-31) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 228.9s |
| Generated | 2026-09-27T16:13:19+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
