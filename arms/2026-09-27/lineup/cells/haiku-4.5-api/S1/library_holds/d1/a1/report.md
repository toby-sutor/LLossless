## Verdict

**13 finding(s).** In the claims: 1 dropped. In the structure: 1 undeclared absence, 1 undeclared rewording, 9 false departure, 1 declared loss over budget. The merge declared **3** drop(s) of 29 source segment(s), **10.3%**, over the 3% budget: past that share the omissions are the finding, whatever each one says about itself. The 2 claim(s) they cost are listed in the review queue below.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 12 |
| Claims extracted from `source_a.md` | 12 |
| Claims extracted from `source_b.md` | 10 |
| Forward — source claims accounted for in the merge | **19/22** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **12/12** |
| Forward — `source_b.md` claims accounted for | **7/10** |
| Reverse — merge claims found in a source | **12/12** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **31/31** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Dropped — in a source, not in the merge

- **B-010** (`source_b.md:22`) — If a reservation is cancelled, you will need to reserve the item again.
  - judged against: `merged.md`
  - rationale: The reference text does not state that a cancelled reservation requires re-reserving the item.

## Length capped

- `$.decisions[2].reason` was 81 characters, over the 80-character cap; capped to fit

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 12 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 12 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | A hold slip is printed when a requested item arrives. | 5 | carried | 'When a requested item arrives, print a hold slip' in `merged.md` -- The reference text directly states that a hold slip is printed when a requested item arrives. |
| 2 | The hold slip is folded into the item so the name is visible from the spine. | 5 | carried | 'fold it into the item so the name is visible from the spine' in `merged.md` -- The reference text states the hold slip is folded into the item so the name is visible from the spine. |
| 3 | Items are shelved alphabetically by the borrower's surname. | 6 | carried | "Shelve items alphabetically by the borrower's surname." in `merged.md` -- The reference text directly states items are shelved alphabetically by the borrower's surname. |
| 4 | An item waits on the hold shelf for 7 days. | 11 | carried | 'An item waits on the hold shelf for 7 days.' in `merged.md` -- The reference text explicitly states that an item waits on the hold shelf for 7 days. |
| 5 | Day one is the day the borrower is notified, not the day the item arrived. | 11 | carried | 'Day one is the day the borrower is notified, not the day the item arrived.' in `merged.md` -- The reference text directly states this clarification about when the 7-day period begins. |
| 6 | The shelf is swept every morning before opening. | 16 | carried | 'Sweep the shelf every morning before opening.' in `merged.md` -- The reference text explicitly states the shelf is swept every morning before opening. |
| 7 | Items past 7 days go back into circulation. | 16 | carried | 'Items past 7 days go back into circulation' in `merged.md` -- The reference text states that items past 7 days go back into circulation. |
| 8 | Items past 7 days go on to the next borrower in the queue if there is one. | 16 | carried | 'or on to the next borrower in the queue if there is one' in `merged.md` -- The reference text states items past 7 days go on to the next borrower in the queue if there is one. |
| 9 | A borrower who asks before the 7 days are up can have the item held for a further 7 days. | 21 | carried | 'A borrower who asks before the 7 days are up can have the item held for a further 7 days.' in `merged.md` -- The reference text directly states borrowers can request the item be held for a further 7 days before the initial period expires. |
| 10 | A borrower can have an item held for a further 7 days once per request. | 22 | carried | 'This is granted once per request.' in `merged.md` -- The reference text explicitly states this extension is granted once per request. |
| 11 | An item that has been on the hold shelf twice without being collected goes back to the shelves. | 26 | carried | 'An item that is not collected goes back into circulation or on to the next person waiting. If this happens twice with the same request, the request is cancelled.' in `merged.md` -- The text indicates that after two non-collections with the same request, the request is cancelled, implying the item returns. |
| 12 | The request is cancelled for an item that has been on the hold shelf twice without being collected. | 27 | carried | 'If this happens twice with the same request, the request is cancelled.' in `merged.md` -- The reference text directly states the request is cancelled if an item is not collected twice with the same request. |

### `source_b.md` -- 10 claim(s): 3 dropped, 0 contradicted, 0 carried in part, 7 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | You can reserve an item that is on loan or held at another branch. | 5 | dropped | The reference text does not mention reserving items that are on loan or held at another branch. |
| 2 | The library will email you when the reserved item is ready to collect. | 5 | dropped | While the reference text mentions email notification, it does not explicitly state the library emails when items are ready to collect. |
| 10 | If a reservation is cancelled, you will need to reserve the item again. | 22 | dropped | The reference text does not state that a cancelled reservation requires re-reserving the item. |
| 3 | You must bring your library card to collect items. | 10 | carried | 'Bring your library card.' in `merged.md` -- The reference text states you must bring your library card to collect items. |
| 4 | Items are on the hold shelf under your surname. | 10 | carried | 'Items are on the hold shelf under your surname.' in `merged.md` -- The reference text directly states items are on the hold shelf under your surname. |
| 5 | You have 7 days from the day the library emails you to collect a reserved item. | 10 | carried | 'You have 7 days from the day we email you to collect.' in `merged.md` -- The reference text states you have 7 days from the day the library emails you to collect a reserved item. |
| 6 | If you cannot collect within the week, you can ask before the 7 days are up and the library will hold the item for another 7 days. | 15 | carried | 'A borrower who asks before the 7 days are up can have the item held for a further 7 days.' in `merged.md` -- The reference text supports this claim by stating borrowers can request a further 7-day hold if they ask before the initial period expires. |
| 7 | The library can extend the hold period once per reservation. | 16 | carried | 'This is granted once per request.' in `merged.md` -- The reference text states the extension is granted once per request, meaning once per reservation. |
| 8 | An item you do not collect goes back into circulation or on to the next person waiting. | 20 | carried | 'An item that is not collected goes back into circulation or on to the next person waiting.' in `merged.md` -- The reference text directly states uncollected items go back into circulation or to the next person waiting. |
| 9 | If you do not collect an item twice with the same reservation, the reservation is cancelled. | 21 | carried | 'If this happens twice with the same request, the request is cancelled.' in `merged.md` -- The reference text states that if an item is not collected twice with the same request, the request is cancelled. |

### `merged.md` -- 12 claim(s): 0 invented, 0 contradicted, 0 supported in part, 12 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | When a requested item arrives, a hold slip is printed and folded into the item so the name is visible from the spine. | supported | `source_a.md` | 'When a requested item arrives, print a hold slip and fold it into the item so the name is visible from the spine.' in `source_a.md` -- source_a.md states exactly this procedure for handling requested items upon arrival. |
| 2 | Items are shelved alphabetically by the borrower's surname. | supported | `source_a.md` | "Shelve items alphabetically by the borrower's surname." in `source_a.md` -- source_a.md directly states items are shelved alphabetically by the borrower's surname. |
| 3 | Items are on the hold shelf under the borrower's surname. | supported | `source_b.md` | 'Items are on the hold shelf under your surname.' in `source_b.md` -- source_b.md states items are on the hold shelf under the borrower's surname in its Collecting section. |
| 4 | A borrower has 7 days from the day the library emails them to collect. | supported | `source_b.md` | 'You have 7 days from the day we email you.' in `source_b.md` -- source_b.md states borrowers have 7 days from the day the library emails them to collect. |
| 5 | An item waits on the hold shelf for 7 days. | supported | `source_a.md` | 'An item waits on the hold shelf for 7 days.' in `source_a.md` -- source_a.md directly states items wait on the hold shelf for 7 days. |
| 6 | Day one is the day the borrower is notified, not the day the item arrived. | supported | `source_a.md` | 'Day one is the day the borrower is notified, not the day the item arrived.' in `source_a.md` -- source_a.md explicitly clarifies that day one is when the borrower is notified, not when the item arrived. |
| 7 | The shelf is swept every morning before opening. | supported | `source_a.md` | 'Sweep the shelf every morning before opening.' in `source_a.md` -- source_a.md states the shelf is swept every morning before opening. |
| 8 | Items past 7 days go back into circulation or on to the next borrower in the queue if there is one. | supported | `source_a.md` | 'Items past 7 days go back into circulation, or on to the next borrower in the queue if there is one.' in `source_a.md` -- source_a.md states items past 7 days go back into circulation or to the next borrower in the queue. |
| 9 | A borrower who asks before the 7 days are up can have the item held for a further 7 days. | supported | `source_a.md` | 'A borrower who asks before the 7 days are up can have the item held for a further 7 days.' in `source_a.md` -- source_a.md directly states borrowers can request to hold items for a further 7 days if asked before the deadline. |
| 10 | An item can be extended once per request. | supported | `source_a.md` | 'This is granted once per request.' in `source_a.md` -- source_a.md specifies that the extension is granted once per request. |
| 11 | An item that is not collected goes back into circulation or on to the next person waiting. | supported | `source_b.md` | 'An item you do not collect goes back into circulation or on to the next person waiting.' in `source_b.md` -- source_b.md states uncollected items go back into circulation or to the next person waiting. |
| 12 | If an item is not collected twice with the same request, the request is cancelled. | supported | `source_b.md` | 'If this happens twice with the same reservation, the reservation is cancelled and you will need to reserve it again.' in `source_b.md` -- source_b.md states the reservation is cancelled if an item is not collected twice with the same reservation. |

## Structure

**9** mechanical check(s) over **29** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **12** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **22**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 6 run(s) over 20 attributed segment(s) — sources interleaved. 7 of 11 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Absent and undeclared — in a source, not in the merge, and no record explains it

- `a11` (`source_a.md`) — 'Borrowers who cannot collect in time' is not in the merge and no disposition record explains it (nearest merge segment m18 at 0.55)

  ```text
  In the source: Borrowers who cannot collect in time
  ```

### Reworded and undeclared — in the merge in altered wording, and no record explains it. At off this also covers layout: a segment whose source line breaks the merge ran together is altered and undeclared, and 380 reuses this kind rather than moving FINDING_KINDS off 12

- `a14` (`source_a.md`) — 'Items nobody collects twice' is reworded in the merge and no disposition record explains it (nearest merge segment m18 at 0.74)

  ```text
  In the source: Items nobody collects twice
  In the merge:  Items not collected
  ```

### Declared gone, still here — a record says the content departed and the merge carries the segment unchanged

- `a3` (`source_a.md`) — 'When a requested item arrives, print a hold slip and fold it into the item so the name is visible from the spine.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: When a requested item arrives, print a hold slip and fold it into the item so the name is visible from the spine.
  In the merge:  When a requested item arrives, print a hold slip and fold it into the item so the name is visible from the spine.
  ```
- `a4` (`source_a.md`) — "Shelve items alphabetically by the borrower's surname." is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Shelve items alphabetically by the borrower's surname.
  In the merge:  Shelve items alphabetically by the borrower's surname.
  ```
- `a6` (`source_a.md`) — 'An item waits on the hold shelf for 7 days.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: An item waits on the hold shelf for 7 days.
  In the merge:  An item waits on the hold shelf for 7 days.
  ```
- `a7` (`source_a.md`) — 'Day one is the day the borrower is notified, not the day the item arrived.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Day one is the day the borrower is notified, not the day the item arrived.
  In the merge:  Day one is the day the borrower is notified, not the day the item arrived.
  ```
- `a9` (`source_a.md`) — 'Sweep the shelf every morning before opening.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Sweep the shelf every morning before opening.
  In the merge:  Sweep the shelf every morning before opening.
  ```
- `a13` (`source_a.md`) — 'This is granted once per request.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: This is granted once per request.
  In the merge:  This is granted once per request.
  ```
- `b5` (`source_b.md`) — 'Collecting' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Collecting
  In the merge:  ## Collecting

Bring your library card. Items are on the hold shelf under your surname. You have 7 days from the day we email you to collect.
  ```
- `b6` (`source_b.md`) — 'Bring your library card.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Bring your library card.
  In the merge:  Bring your library card. Items are on the hold shelf under your surname. You have 7 days from the day we email you to collect.
  ```
- `b9` (`source_b.md`) — 'Extending' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Extending
  In the merge:  A borrower who asks before the 7 days are up can have the item held for a further 7 days.
  ```

### Over budget — declared loss past the ceiling

- 3 of 29 segments are declared dropped (10.3%), over the 3% budget

## Review queue

**2** claim(s) the merge declared dropped and the forward pass confirms are gone. Each is a decision to review — put the fact back, or agree it stays out — and none of them is counted as a finding above.

- **B-001** (`source_b.md:5`) — You can reserve an item that is on loan or held at another branch.
  - left out of: `b3`
  - the merge's reason: Content about reserving items outside hold shelf scope of merged document.
  - confirmed absent: the forward pass looked for this claim in `merged.md` and did not find it -- The reference text does not mention reserving items that are on loan or held at another branch.
- **B-002** (`source_b.md:5`) — The library will email you when the reserved item is ready to collect.
  - left out of: `b4`
  - the merge's reason: Content about reserving items outside hold shelf scope of merged document.
  - confirmed absent: the forward pass looked for this claim in `merged.md` and did not find it -- While the reference text mentions email notification, it does not explicitly state the library emails when items are ready to collect.

> **Over budget.** The merge declared **3** drop(s) of 29 source segment(s), **10.3%**, over the 3% budget: past that share the omissions are the finding, whatever each one says about itself.

## Declarations

The merge declared **23** departure(s) from its sources. Checking them confirms 19, rejects 1, and leaves 3 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 3 of 29 source segment(s) declared gone, **10.3%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | Base document title was chosen over this alternative. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Hold Shelf Management' and says so (no claim traced to it) |
| `b2` | dropped | Content about reserving items outside hold shelf scope of merged document. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b3` | dropped | Content about reserving items outside hold shelf scope of merged document. | **confirmed** | declared 'dropped' and every claim from it came back MISSING (`B-001`) |
| `b4` | dropped | Content about reserving items outside hold shelf scope of merged document. | **confirmed** | declared 'dropped' and every claim from it came back MISSING (`B-002`) |
| `b5` | subsumed | Heading integrated into merged document structure. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b6` | subsumed | Content carried in collecting section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-003`) |
| `b7` | reworded | Changed from 'held at another branch' context to hold shelf context. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-004`) |
| `b8` | subsumed | Content carried in collecting section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-005`) |
| `b9` | subsumed | Content reconciled with source_a.md into extending section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b10` | reconciled | Combined with a12-a13 to state policy once. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-006`) |
| `b11` | superseded | Source a.md wording used; same meaning as 'once per reservation'. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-007`) |
| `b12` | subsumed | Content carried in items not collected section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b13` | reconciled | Combined with a10 to unify content about uncollected items. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-008`) |
| `b14` | reconciled | Combined with a15 to unify content about twice-uncollected items. | **rejected** | declared 'reconciled', which predicts SUPPORTED; B-010 came back MISSING (`B-010`) |
| `a3` | subsumed | Content carried in placing section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-001`, `A-002`) |
| `a4` | subsumed | Content carried in placing section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-003`) |
| `a6` | subsumed | Content carried in how long items wait section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-004`) |
| `a7` | subsumed | Content carried in how long items wait section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-005`) |
| `a9` | subsumed | Content carried in clearing section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-006`) |
| `a10` | reconciled | Combined with b13 to unify content about uncollected items. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-007`, `A-008`) |
| `a12` | reconciled | Combined with b10 to state extension policy once. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-009`) |
| `a13` | subsumed | Content carried in extending section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-010`) |
| `a15` | reconciled | Combined with b14 to unify content about twice-uncollected items. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-011`, `A-012`) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | ec0c9ecb43e3 (hosted) |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | claude-haiku-4-5-20251001 |
| Model (decompose) | claude-haiku-4-5-20251001 |
| Model (verify) | claude-haiku-4-5-20251001 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile anthropic, effort decompose one level (extended thinking on/off; default kept), merge one level (extended thinking on/off; default kept), verify one level (extended thinking on/off; default kept) |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 7 live, 0 cached, 0 replayed |
| Tokens | 17,089 in, 9,050 out |
| Cost | ~$0.06 estimated (rates read 2026-08-31) |
| Schema repairs | 1 |
| Errors | 0 |
| Duration | 69.4s |
| Generated | 2026-09-27T16:14:29+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
