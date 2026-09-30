## Verdict

**2 finding(s).** In the structure: 1 false departure, 1 declared loss over budget. The merge declared **1** drop(s) of 29 source segment(s), **3.4%**, over the 3% budget: past that share the omissions are the finding, whatever each one says about itself.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 14 |
| Claims extracted from `source_a.md` | 7 |
| Claims extracted from `source_b.md` | 8 |
| Forward — source claims accounted for in the merge | **15/15** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **7/7** |
| Forward — `source_b.md` claims accounted for | **8/8** |
| Reverse — merge claims found in a source | **14/14** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **29/29** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

None in the claims. The 2 finding(s) this run reports are structural and are listed under `## Structure` below.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 7 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 7 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | An item waits on the hold shelf for 7 days. | 11 | carried | 'A reserved item waits on the hold shelf for 7 days' in `merged.md` -- The reference text directly states this claim about the 7-day hold period. |
| 2 | Day one is the day the borrower is notified, not the day the item arrived. | 11 | carried | 'day one is the notification day, not the arrival day' in `merged.md` -- The reference text explicitly distinguishes notification day from arrival day as day one. |
| 3 | Items past 7 days go back into circulation, or on to the next borrower in the queue if there is one. | 16 | carried | 'Items not collected within 7 days go back into circulation or move to the next borrower in the queue if there is one' in `merged.md` -- The reference text covers both options for uncollected items past the 7-day period. |
| 4 | A borrower who asks before the 7 days are up can have the item held for a further 7 days. | 21 | carried | 'they can request a 7-day extension before the deadline expires' in `merged.md` -- The reference supports that borrowers can request extensions before the deadline. |
| 5 | An extension is granted once per request. | 22 | carried | 'This extension is granted once per reservation' in `merged.md` -- Request and reservation refer to the same holding arrangement; the reference states this limit explicitly. |
| 6 | An item that has been on the hold shelf twice without being collected goes back to the shelves. | 26 | carried | 'If an item remains uncollected after being held twice, it goes back to the shelves' in `merged.md` -- The reference text directly addresses items held twice without collection. |
| 7 | The request is cancelled for an item that has been on the hold shelf twice without being collected. | 27 | carried | 'the reservation is cancelled' in `merged.md` -- The reference cancels the reservation after an item is uncollected twice; reservation is the holding request. |

### `source_b.md` -- 8 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 8 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | An item that is on loan or held at another branch can be reserved. | 5 | carried | 'Borrowers can reserve items that are on loan or held at another branch' in `merged.md` -- The reference directly supports that these item types can be reserved. |
| 2 | The library will email the patron when the item is ready to collect. | 5 | carried | 'When the item is ready for collection, the borrower is notified by email' in `merged.md` -- The reference explicitly states borrowers are emailed when items are ready. |
| 3 | Reserved items are on the hold shelf under the patron's surname. | 10 | carried | "Shelve items alphabetically by the borrower's surname" in `merged.md` -- The reference states items are shelved by surname, placing them under the patron's name. |
| 4 | The patron has 7 days from the day the library emails them to collect their hold. | 10 | carried | 'A reserved item waits on the hold shelf for 7 days from when the borrower is notified' in `merged.md` -- The reference specifies the 7-day period runs from notification (when emailed). |
| 5 | The library will hold an item for another 7 days if requested before the initial 7 days expire. | 15 | carried | 'they can request a 7-day extension before the deadline expires' in `merged.md` -- The reference allows extension requests before the initial period expires. |
| 6 | The library can extend a hold once per reservation. | 16 | carried | 'This extension is granted once per reservation' in `merged.md` -- The reference explicitly limits extensions to one per reservation. |
| 7 | An uncollected item goes back into circulation or to the next person waiting. | 20 | carried | 'go back into circulation or move to the next borrower in the queue if there is one' in `merged.md` -- The reference covers both outcomes for uncollected items. |
| 8 | If an item is not collected twice with the same reservation, the reservation is cancelled. | 21 | carried | 'If an item remains uncollected after being held twice, it goes back to the shelves and the reservation is cancelled' in `merged.md` -- The reference states the reservation is cancelled when items are uncollected twice. |

### `merged.md` -- 14 claim(s): 0 invented, 0 contradicted, 0 supported in part, 14 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Borrowers can reserve items that are on loan or held at another branch. | supported | `source_b.md` | 'You can reserve an item that is on loan or held at another branch.' in `source_b.md` -- Source B directly states that borrowers can reserve items on loan or held at another branch. |
| 2 | When the item is ready for collection, the borrower is notified by email. | supported | `source_b.md` | 'We will email you when it is ready to collect.' in `source_b.md` -- Source B states that borrowers are notified by email when items are ready to collect. |
| 3 | When a reserved item arrives, a hold slip is printed and folded into the item so the name is visible from the spine. | supported | `source_a.md` | 'When a requested item arrives, print a hold slip and fold it into the item so the name is visible from the spine.' in `source_a.md` -- Source A describes the exact procedure for handling reserved items upon arrival. |
| 4 | Items are shelved alphabetically by the borrower's surname. | supported | `source_a.md` | "Shelve items alphabetically by the borrower's surname." in `source_a.md` -- Source A directly states items are shelved alphabetically by borrower's surname. |
| 5 | A reserved item waits on the hold shelf for 7 days from when the borrower is notified. | supported | `source_b.md` | 'You have 7 days from the day we email you.' in `source_b.md` -- Source B indicates the 7-day hold period starts from notification, matching the claim. |
| 6 | Day one is the notification day, not the arrival day. | supported | `source_a.md` | 'Day one is the day the borrower is notified, not the day the item arrived.' in `source_a.md` -- Source A explicitly clarifies that day one is the notification day, not arrival day. |
| 7 | The shelf is swept every morning before opening. | supported | `source_a.md` | 'Sweep the shelf every morning before opening.' in `source_a.md` -- Source A directly states the shelf is swept every morning before opening. |
| 8 | Items not collected within 7 days go back into circulation. | supported | `source_b.md` | 'An item you do not collect goes back into circulation or on to the next person waiting.' in `source_b.md` -- Source B states uncollected items go back into circulation. |
| 9 | Items not collected within 7 days move to the next borrower in the queue if there is one. | supported | `source_a.md` | 'Items past 7 days go back into circulation, or on to the next borrower in the queue if there is one.' in `source_a.md` -- Source A states uncollected items move to the next borrower in the queue if available. |
| 10 | If a borrower cannot collect within 7 days, they can request a 7-day extension before the deadline expires. | supported | `source_b.md` | 'If you cannot get in within the week, ask us before the 7 days are up and we will hold the item for another 7 days.' in `source_b.md` -- Source B describes the extension process, matching the claim's conditions. |
| 11 | The extension is granted once per reservation. | supported | `source_b.md` | 'We can do this once per reservation.' in `source_b.md` -- Source B explicitly states the extension is granted once per reservation. |
| 12 | If an item remains uncollected after being held twice, the item goes back to the shelves. | supported | `source_a.md` | 'An item that has been on the hold shelf twice without being collected goes back to the shelves and the request is cancelled.' in `source_a.md` -- Source A states the item goes back to the shelves after being held twice without collection. |
| 13 | If an item remains uncollected after being held twice, the reservation is cancelled. | supported | `source_b.md` | 'If this happens twice with the same reservation, the reservation is cancelled and you will need to reserve it again.' in `source_b.md` -- Source B states the reservation is cancelled if the item is not collected twice. |
| 14 | The borrower must place a new reservation if they wish to request the item again. | supported | `source_b.md` | 'you will need to reserve it again.' in `source_b.md` -- Source B indicates that a new reservation must be placed to request the item after cancellation. |

## Structure

**9** mechanical check(s) over **29** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **14** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **15**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 5 run(s) over 10 attributed segment(s) — sources interleaved. 4 of 11 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Declared gone, still here — a record says the content departed and the merge carries the segment unchanged

- `b9` (`source_b.md`) — 'Extending' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Extending
  In the merge:  ## Extending holds
  ```

### Over budget — declared loss past the ceiling

- 1 of 29 segments are declared dropped (3.4%), over the 3% budget

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

> **Over budget.** The merge declared **1** drop(s) of 29 source segment(s), **3.4%**, over the 3% budget: past that share the omissions are the finding, whatever each one says about itself.

## Declarations

The merge declared **25** departure(s) from its sources. Checking them confirms 16, rejects 0, and leaves 9 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 1 of 29 source segment(s) declared gone, **3.4%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a2` | reworded | Added 'on the hold shelf' for clarity. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a3` | reworded | Changed 'requested' to 'reserved' for terminology consistency. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a5` | reworded | Improved clarity and grammatical parallelism. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a6` | reconciled | Combined with a7 and b8 to specify holding period from notification. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-001`) |
| `a7` | reconciled | Combined with a6 and b8 into comprehensive holding period statement. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-002`) |
| `a10` | reworded | Reworded 'past 7 days' to 'not collected within 7 days' for clarity. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-003`) |
| `a11` | reworded | Simplified heading for conciseness and clarity. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a12` | reworded | Restructured for clarity and consistency with merged context. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-004`) |
| `a13` | reworded | Changed 'request' to 'reservation' for terminology consistency. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-005`) |
| `a14` | reworded | Simplified heading for clarity and conciseness. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a15` | reconciled | Combined with b14 to include new reservation requirement. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-006`, `A-007`) |
| `b1` | superseded | Base document's title chosen as it better fits merged scope. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Hold Shelf Management' and says so (no claim traced to it) |
| `b2` | reworded | Heading rephrased for conciseness while maintaining meaning. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b3` | reworded | Converted from customer perspective to staff perspective. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-001`) |
| `b4` | reworded | Converted from customer perspective to staff perspective. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-002`) |
| `b5` | subsumed | Section content integrated into merged structure. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b6` | dropped | Customer instruction outside scope of staff procedures. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b7` | duplicate | Same fact already expressed in a4. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-003`) |
| `b8` | reconciled | Combined with a6, a7 to establish holding period from notification. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-004`) |
| `b9` | subsumed | Section merged under base document's heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b10` | reworded | Converted from customer to staff perspective. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-005`) |
| `b11` | reworded | Converted from customer to staff perspective. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-006`) |
| `b12` | subsumed | Section content merged under consolidated heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b13` | superseded | Same content in a10 version retained. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-007`) |
| `b14` | reconciled | Combined with a15 to include borrower re-reservation requirement. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-008`) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | 45fff742d0ed (command) -- lineup haiku-4.5-sub |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | claude-haiku-4-5-20251001 -> claude-haiku-4-5-20251001 |
| Model (decompose) | claude-haiku-4-5-20251001 -> claude-haiku-4-5-20251001 |
| Model (verify) | claude-haiku-4-5-20251001 -> claude-haiku-4-5-20251001 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile subscription, effort decompose one level (extended thinking on/off; default kept), merge one level (extended thinking on/off; default kept), verify one level (extended thinking on/off; default kept) |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 6 live, 0 cached, 0 replayed |
| Tokens | unknown (6 call(s) reported no usage) |
| Cost | unmeasured (6 call(s) reported no tokens, so no figure can be derived) |
| Schema repairs | 0 |
| Isolation | decompose, merge, verify: safe mode, no tools |
| Errors | 0 |
| Duration | 592.2s |
| Generated | 2026-09-27T16:52:12+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup haiku-4.5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
