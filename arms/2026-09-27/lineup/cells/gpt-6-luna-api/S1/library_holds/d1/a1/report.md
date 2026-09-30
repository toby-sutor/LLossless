## Verdict

**7 finding(s).** In the claims: 6 partially dropped. In the structure: 1 undeclared rewording.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 20 |
| Claims extracted from `source_a.md` | 14 |
| Claims extracted from `source_b.md` | 13 |
| Forward — source claims accounted for in the merge | **21/27** |
| Forward — carried only in part | 6 |
| Forward — `source_a.md` claims accounted for | **11/14** (3 in part) |
| Forward — `source_b.md` claims accounted for | **10/13** (3 in part) |
| Reverse — merge claims found in a source | **20/20** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **47/47** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Partly dropped — the merge carries some of this claim

- **A-001** (`source_a.md:5`) — A hold slip is printed when a requested item arrives.
  - evidence: 'Print a hold slip' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text says to print a hold slip but does not say it is printed when the requested item arrives.
- **A-013** (`source_a.md:26`) — An item that has been on the hold shelf twice without being collected goes back to the shelves.
  - evidence: 'If an item has been on the hold shelf twice without being collected for the same reservation, it goes back to the shelves' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text states this outcome for the same reservation, but does not establish it without that condition.
- **A-014** (`source_a.md:27`) — The request is cancelled when an item has been on the hold shelf twice without being collected.
  - evidence: 'If an item has been on the hold shelf twice without being collected for the same reservation, it goes back to the shelves and the reservation is cancelled' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text states cancellation for the same reservation, but does not establish it without that condition.
- **B-007** (`source_b.md:15`) — If a person cannot get in within the week, they should ask the library before the 7 days are up.
  - evidence: 'A borrower who asks before the 7 days are up can have the item held for a further 7 days.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text says a timely request can secure more time, but does not say a borrower unable to collect should ask.
- **B-010** (`source_b.md:20`) — An item that a person does not collect goes back into circulation.
  - evidence: 'Items past 7 days go back into circulation, or on to the next borrower in the queue if there is one.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text states this outcome for items past seven days, not for every item a person does not collect.
- **B-011** (`source_b.md:20`) — An item that a person does not collect goes on to the next person waiting.
  - evidence: 'Items past 7 days go back into circulation, or on to the next borrower in the queue if there is one.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text states this outcome for items past seven days, not for every item a person does not collect.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 14 claim(s): 0 dropped, 0 contradicted, 3 carried in part, 11 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | A hold slip is printed when a requested item arrives. | 5 | carried in part | 'Print a hold slip' in `merged.md` -- The text says to print a hold slip but does not say it is printed when the requested item arrives. |
| 13 | An item that has been on the hold shelf twice without being collected goes back to the shelves. | 26 | carried in part | 'If an item has been on the hold shelf twice without being collected for the same reservation, it goes back to the shelves' in `merged.md` -- The text states this outcome for the same reservation, but does not establish it without that condition. |
| 14 | The request is cancelled when an item has been on the hold shelf twice without being collected. | 27 | carried in part | 'If an item has been on the hold shelf twice without being collected for the same reservation, it goes back to the shelves and the reservation is cancelled' in `merged.md` -- The text states cancellation for the same reservation, but does not establish it without that condition. |
| 2 | The hold slip is folded into the item. | 5 | carried | 'fold it into the item' in `merged.md` -- The text explicitly says to fold the hold slip into the item. |
| 3 | The borrower's name is visible from the spine. | 5 | carried | 'fold it into the item so the name is visible from the spine.' in `merged.md` -- The text says the name should be visible from the spine. |
| 4 | Items are shelved alphabetically by the borrower's surname. | 6 | carried | "Shelve items alphabetically by the borrower's surname." in `merged.md` -- This directly states the shelving order and sorting criterion. |
| 5 | An item waits on the hold shelf for 7 days. | 11 | carried | 'An item waits on the hold shelf for 7 days.' in `merged.md` -- This directly states the hold-shelf waiting period. |
| 6 | Day one is the day the borrower is notified. | 11 | carried | 'The 7-day period starts on the day the borrower is notified by email' in `merged.md` -- The text identifies the email-notification day as the start of the period. |
| 7 | Day one is not the day the item arrived. | 12 | carried | 'not the day the item arrives.' in `merged.md` -- The text explicitly says the period does not start on the item's arrival day. |
| 8 | The shelf is swept every morning before opening. | 16 | carried | 'Sweep the shelf every morning before opening.' in `merged.md` -- This directly states when the shelf is swept. |
| 9 | Items past 7 days go back into circulation. | 16 | carried | 'Items past 7 days go back into circulation' in `merged.md` -- The text directly states that items past 7 days go back into circulation. |
| 10 | Items past 7 days go to the next borrower in the queue if there is one. | 17 | carried | 'or on to the next borrower in the queue if there is one.' in `merged.md` -- The text directly states the next-borrower outcome when someone is in the queue. |
| 11 | A borrower who asks before the 7 days are up can have the item held for a further 7 days. | 21 | carried | 'A borrower who asks before the 7 days are up can have the item held for a further 7 days.' in `merged.md` -- This directly states the timely request and additional hold period. |
| 12 | The further hold is granted once per request. | 22 | carried | 'This is granted once per request.' in `merged.md` -- The text explicitly limits the further hold to once per request. |

### `source_b.md` -- 13 claim(s): 0 dropped, 0 contradicted, 3 carried in part, 10 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 7 | If a person cannot get in within the week, they should ask the library before the 7 days are up. | 15 | carried in part | 'A borrower who asks before the 7 days are up can have the item held for a further 7 days.' in `merged.md` -- The text says a timely request can secure more time, but does not say a borrower unable to collect should ask. |
| 10 | An item that a person does not collect goes back into circulation. | 20 | carried in part | 'Items past 7 days go back into circulation, or on to the next borrower in the queue if there is one.' in `merged.md` -- The text states this outcome for items past seven days, not for every item a person does not collect. |
| 11 | An item that a person does not collect goes on to the next person waiting. | 20 | carried in part | 'Items past 7 days go back into circulation, or on to the next borrower in the queue if there is one.' in `merged.md` -- The text states this outcome for items past seven days, not for every item a person does not collect. |
| 1 | A person can reserve an item that is on loan. | 5 | carried | 'You can reserve an item that is on loan' in `merged.md` -- This directly states that an item on loan can be reserved. |
| 2 | A person can reserve an item held at another branch. | 5 | carried | 'or held at another branch.' in `merged.md` -- This directly states that an item held at another branch can be reserved. |
| 3 | The library will email a person when a reserved item is ready to collect. | 5 | carried | 'We email you when it is ready to collect.' in `merged.md` -- The text says the library emails the borrower when the item is ready to collect. |
| 4 | A person must bring their library card to collect an item. | 10 | carried | 'Bring your library card.' in `merged.md` -- This directly instructs the borrower to bring their library card. |
| 5 | Items are on the hold shelf under the person's surname. | 10 | carried | 'Items are on the hold shelf under your surname.' in `merged.md` -- This directly states that items are held under the borrower's surname. |
| 6 | A person has 7 days from the day the library emails them to collect an item. | 10 | carried | 'The 7-day period starts on the day the borrower is notified by email, not the day the item arrives.' in `merged.md` -- The text establishes that the seven-day period begins with email notification. |
| 8 | If a person asks in time, the library will hold the item for another 7 days. | 15 | carried | 'A borrower who asks before the 7 days are up can have the item held for a further 7 days.' in `merged.md` -- This directly states that an on-time request can result in another seven days. |
| 9 | The library can extend a reservation once. | 16 | carried | 'This is granted once per request.' in `merged.md` -- The text directly says the extension is granted once per request. |
| 12 | If this happens twice with the same reservation, the reservation is cancelled. | 21 | carried | 'If an item has been on the hold shelf twice without being collected for the same reservation, it goes back to the shelves and the reservation is cancelled' in `merged.md` -- The reference states that after an item is uncollected twice for the same reservation, the reservation is cancelled. |
| 13 | After the reservation is cancelled, the person will need to reserve the item again. | 22 | carried | 'the borrower must reserve it again' in `merged.md` -- The reference explicitly says the borrower must reserve the item again after cancellation. |

### `merged.md` -- 20 claim(s): 0 invented, 0 contradicted, 0 supported in part, 20 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | A borrower can reserve an item that is on loan. | supported | `source_b.md` | 'You can reserve an item that is on loan or held at another branch.' in `source_b.md` -- Source_b.md explicitly says an item on loan can be reserved. |
| 2 | A borrower can reserve an item that is held at another branch. | supported | `source_b.md` | 'You can reserve an item that is on loan or held at another branch.' in `source_b.md` -- Source_b.md explicitly says an item held at another branch can be reserved. |
| 3 | The library emails the borrower when the item is ready to collect. | supported | `source_b.md` | 'We will email you when it is ready to collect.' in `source_b.md` -- Source_b.md states that the library emails the borrower when the item is ready. |
| 4 | A borrower should bring their library card. | supported | `source_b.md` | 'Bring your library card.' in `source_b.md` -- Source_b.md directly instructs the borrower to bring their library card. |
| 5 | A hold slip should be printed. | supported | `source_a.md` | 'print a hold slip' in `source_a.md` -- Source_a.md says to print a hold slip when a requested item arrives. |
| 6 | The hold slip should be folded into the item. | supported | `source_a.md` | 'fold it into the item' in `source_a.md` -- Source_a.md directly says to fold the hold slip into the item. |
| 7 | The name on the hold slip should be visible from the spine. | supported | `source_a.md` | 'the name is visible from the spine' in `source_a.md` -- Source_a.md says the folded slip should show the name from the spine. |
| 8 | Items should be shelved alphabetically by the borrower's surname. | supported | `source_a.md` | "Shelve items alphabetically by the borrower's surname." in `source_a.md` -- Source_a.md directly gives this shelving order. |
| 9 | Items are on the hold shelf under the borrower's surname. | supported | `source_b.md` | 'Items are on the hold shelf under your surname.' in `source_b.md` -- Source_b.md states that items are on the hold shelf under the borrower's surname. |
| 10 | An item waits on the hold shelf for 7 days. | supported | `source_a.md` | 'An item waits on the hold shelf for 7 days.' in `source_a.md` -- Source_a.md directly states the hold shelf waiting period. |
| 11 | The 7-day period starts on the day the borrower is notified by email. | supported | `source_b.md` | '7 days from the day we email you.' in `source_b.md` -- Source_b.md says the 7-day period starts on the day the library emails the borrower. |
| 12 | The 7-day period does not start on the day the item arrives. | supported | `source_a.md` | 'not the day the item arrived.' in `source_a.md` -- Source_a.md explicitly says the waiting period does not begin on the item's arrival day. |
| 13 | The shelf should be swept every morning before opening. | supported | `source_a.md` | 'Sweep the shelf every morning before opening.' in `source_a.md` -- Source_a.md directly states when the shelf should be swept. |
| 14 | Items past 7 days go back into circulation. | supported | `source_a.md` | 'Items past 7 days go back into circulation' in `source_a.md` -- Source_a.md states that items past 7 days go back into circulation. |
| 15 | Items past 7 days go to the next borrower in the queue if there is one. | supported | `source_a.md` | 'on to the next borrower in the queue if there is one.' in `source_a.md` -- Source_a.md says overdue items go to the next borrower in the queue if there is one. |
| 16 | A borrower who asks before the 7 days are up can have the item held for a further 7 days. | supported | `source_a.md` | 'A borrower who asks before the 7 days are up can have the item held for a further 7 days.' in `source_a.md` -- Source_a.md directly states this extension rule. |
| 17 | The further 7 days are granted once per request. | supported | `source_a.md` | 'This is granted once per request.' in `source_a.md` -- Source_a.md says the further hold is granted once per request. |
| 18 | If an item has been on the hold shelf twice without being collected for the same reservation, the item goes back to the shelves. | supported | `source_a.md` | 'An item that has been on the hold shelf twice without being collected goes back to the shelves and the request is cancelled.' in `source_a.md` -- Source_a.md gives the twice-uncollected hold-shelf outcome; source_b.md specifies twice with the same reservation. |
| 19 | If an item has been on the hold shelf twice without being collected for the same reservation, the reservation is cancelled. | supported | `source_b.md` | 'If this happens twice with the same reservation, the reservation is cancelled and you will need to reserve it again.' in `source_b.md` -- Source_b.md states cancellation for the same reservation; source_a.md specifies the twice-uncollected hold-shelf circumstance. |
| 20 | If an item has been on the hold shelf twice without being collected for the same reservation, the borrower must reserve it again. | supported | `source_b.md` | 'If this happens twice with the same reservation, the reservation is cancelled and you will need to reserve it again.' in `source_b.md` -- Source_b.md says to reserve again after two failures with the same reservation; source_a.md supplies the twice-uncollected hold-shelf condition. |

## Structure

**9** mechanical check(s) over **29** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **20** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **27**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 5 run(s) over 19 attributed segment(s) — sources interleaved. 6 of 11 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

`[-...-]` is what the source said and `{+...+}` is what the merge says.

### Reworded and undeclared — in the merge in altered wording, and no record explains it. At off this also covers layout: a segment whose source line breaks the merge ran together is altered and undeclared, and 380 reuses this kind rather than moving FINDING_KINDS off 12

- `a3` (`source_a.md`) — 'When a requested item arrives, print a hold slip and fold it into the item so the name is visible from the spine.' is reworded in the merge and no disposition record explains it (nearest merge segment m6 at 0.84)

  ```text
  In the source: When a requested item arrives, print a hold slip and fold it into the item so the name is visible from the spine.
  In the merge:  Print a hold slip and fold it into the item so the name is visible from the spine.
  What changed:  [-When a requested item arrives, print-] {+Print+} a hold slip and fold it into the item so the name is visible from the spine.
  ```

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **14** departure(s) from its sources. Checking them confirms 9, rejects 1, and leaves 4 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 29 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a7` | reconciled | The timing rule combines notification with the email start date. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-006`, `A-007`) |
| `a15` | reconciled | The twice-uncollected rule combines the return and cancellation outcomes. | **rejected** | declared 'reconciled', which predicts SUPPORTED; A-013 came back PARTIAL, A-014 came back PARTIAL (`A-013`, `A-014`) |
| `b1` | superseded | The base title is retained. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Hold Shelf Management' and says so (no claim traced to it) |
| `b2` | superseded | The base heading holds the reservation and placement instructions. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b4` | reworded | The notification instruction is stated in the present tense. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-003`) |
| `b5` | superseded | Collection instructions are consolidated under the base placement heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b7` | reworded | The collection location is stated directly. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-005`) |
| `b8` | reconciled | The timing rule combines notification with the email start date. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-006`) |
| `b9` | superseded | The base heading describes the extension section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b10` | superseded | The base wording states the same extension rule. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-007`, `B-008`) |
| `b11` | superseded | The base wording states the same one-time limit. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-009`) |
| `b12` | subsumed | The general non-collection heading maps to shelf clearing. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b13` | superseded | The base sentence states the same return rule. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-010`, `B-011`) |
| `b14` | reconciled | The twice-uncollected rule combines the return and cancellation outcomes. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-012`, `B-013`) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | bf7d5842201d (hosted) |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | gpt-6-luna |
| Model (decompose) | gpt-6-luna |
| Model (verify) | gpt-6-luna |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed 0, thinking decompose, merge, verify, profile openai-reasoning |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 7 live, 0 cached, 0 replayed |
| Tokens | 15,014 in, 16,439 out, 0 cached, 10,449 reasoning |
| Cost | ~$0.01 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 124.7s |
| Generated | 2026-09-27T15:34:01+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `bf7d5842201d`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
