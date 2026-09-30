## Verdict

**3 finding(s).** In the claims: 2 contradicted. In the structure: 1 declared loss over budget. The merge declared **2** drop(s) of 36 source segment(s), **5.6%**, over the 3% budget: past that share the omissions are the finding, whatever each one says about itself. The 1 claim(s) they cost are listed in the review queue below.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 18 |
| Claims extracted from `source_a.md` | 18 |
| Claims extracted from `source_b.md` | 8 |
| Forward — source claims accounted for in the merge | **24/26** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **18/18** |
| Forward — `source_b.md` claims accounted for | **6/8** |
| Reverse — merge claims found in a source | **17/18** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **43/43** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **B-007** -- the two documents disagree
  - `source_b.md:15` says: Phone requests are taken between 08:00 and 16:00 on working days only.
  - `merged.md` says: 'The dock booking phone line was retired and the number no longer connects.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text states the phone line was retired and no longer connects, contradicting the claim that phone requests are taken.
- **M-011** -- the two documents disagree
  - `merged.md:13` says: All bookings go through the portal
  - `source_b.md` says: 'If the portal is down, call the dock booking line on extension 2140 and the dock supervisor will enter the slot for you.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: source_a.md claims all bookings go through the portal, but source_b.md describes an alternative phone booking method, contradicting universal portal usage.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 18 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 18 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | All deliveries need a dock slot. | 5 | carried | 'All deliveries need a dock slot.' in `merged.md` -- The reference text states this claim exactly. |
| 2 | Slots are booked through the facilities portal. | 5 | carried | 'Book slots through the facilities portal.' in `merged.md` -- The reference text states that slots are booked through the facilities portal. |
| 3 | A slot is 45 minutes. | 5 | carried | 'A slot is 45 minutes.' in `merged.md` -- The reference text states this claim exactly. |
| 4 | A vehicle over 7.5 tonnes needs two consecutive slots. | 6 | carried | 'A vehicle over 7.5 tonnes needs two consecutive slots' in `merged.md` -- The reference text states this claim exactly. |
| 5 | The portal does not allow separate booking of two consecutive slots. | 7 | carried | 'the portal will not let you book them separately' in `merged.md` -- The reference text states the portal does not allow separate booking of consecutive slots. |
| 6 | Slots open 14 days ahead. | 11 | carried | 'Slots open 14 days ahead' in `merged.md` -- The reference text states this claim exactly. |
| 7 | Slots close 4 hours before the slot starts. | 11 | carried | 'close 4 hours before the slot starts' in `merged.md` -- The reference text states slots close 4 hours before the slot starts. |
| 8 | There is no same-hour booking. | 11 | carried | 'There is no same-hour booking.' in `merged.md` -- The reference text states this claim exactly. |
| 9 | The dock booking phone line was retired. | 16 | carried | 'The dock booking phone line was retired' in `merged.md` -- The reference text states the dock booking phone line was retired. |
| 10 | The dock booking phone line number no longer connects. | 16 | carried | 'the number no longer connects' in `merged.md` -- The reference text states the phone line number no longer connects. |
| 11 | All bookings go through the portal. | 16 | carried | 'All bookings go through the portal.' in `merged.md` -- The reference text states this claim exactly. |
| 12 | Drivers who call the old dock booking phone line number hear a recorded message directing them to the portal. | 17 | carried | 'Drivers who call the old number hear a recorded message pointing them at the portal.' in `merged.md` -- The reference text states drivers hear a recorded message pointing them at the portal when calling. |
| 13 | Drivers report to the gatehouse with the booking reference. | 22 | carried | 'Drivers report to the gatehouse with the booking reference.' in `merged.md` -- The reference text states this claim exactly. |
| 14 | The gatehouse checks the reference against the day sheet. | 22 | carried | 'The gatehouse checks the reference against the day sheet' in `merged.md` -- The reference text states this claim exactly. |
| 15 | The gatehouse directs the vehicle to a bay. | 23 | carried | 'directs the vehicle to a bay' in `merged.md` -- The reference text states the gatehouse directs the vehicle to a bay. |
| 16 | A driver without a booking reference waits in the holding area until a slot is free. | 23 | carried | 'A driver without a reference waits in the holding area until a slot is free.' in `merged.md` -- The reference text states this claim exactly. |
| 17 | A vehicle still on the bay 15 minutes after its slot ends is logged as an overrun. | 28 | carried | 'A vehicle still on the bay 15 minutes after its slot ends is logged as an overrun.' in `merged.md` -- The reference text states this claim exactly. |
| 18 | If a supplier has three overruns in a quarter, the supplier is asked to rebook through their account manager. | 29 | carried | 'Three overruns in a quarter and the supplier is asked to rebook through their account manager.' in `merged.md` -- The reference text states that three overruns in a quarter trigger a rebook request through account manager. |

### `source_b.md` -- 8 claim(s): 1 dropped, 1 contradicted, 0 carried in part, 6 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 6 | The dock booking line is on extension 2140. | 14 | dropped | The reference text does not mention any extension number for the dock booking line. |
| 7 | Phone requests are taken between 08:00 and 16:00 on working days only. | 15 | contradicted | 'The dock booking phone line was retired and the number no longer connects.' in `merged.md` -- The reference text states the phone line was retired and no longer connects, contradicting the claim that phone requests are taken. |
| 1 | Every delivery needs a dock slot. | 5 | carried | 'All deliveries need a dock slot.' in `merged.md` -- The reference text states this; 'every' and 'all' are equivalent when referring to deliveries. |
| 2 | A slot is 45 minutes long. | 5 | carried | 'A slot is 45 minutes.' in `merged.md` -- The reference text states a slot is 45 minutes; '45 minutes long' conveys the same meaning. |
| 3 | Vehicles over 7.5 tonnes need two consecutive slots. | 6 | carried | 'A vehicle over 7.5 tonnes needs two consecutive slots' in `merged.md` -- The reference text states this; 'a vehicle' and 'vehicles' both refer to the same category. |
| 4 | Slots open 14 days ahead. | 10 | carried | 'Slots open 14 days ahead' in `merged.md` -- The reference text states this claim exactly. |
| 5 | Slots close 4 hours before the slot starts. | 10 | carried | 'close 4 hours before the slot starts' in `merged.md` -- The reference text states slots close 4 hours before the slot starts. |
| 8 | A vehicle still on the bay 15 minutes after its slot ends is logged as an overrun. | 25 | carried | 'A vehicle still on the bay 15 minutes after its slot ends is logged as an overrun.' in `merged.md` -- The reference text states this claim exactly. |

### `merged.md` -- 18 claim(s): 0 invented, 1 contradicted, 0 supported in part, 17 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 11 | All bookings go through the portal | contradicted | `source_b.md` | 'If the portal is down, call the dock booking line on extension 2140 and the dock supervisor will enter the slot for you.' in `source_b.md` -- source_a.md claims all bookings go through the portal, but source_b.md describes an alternative phone booking method, contradicting universal portal usage. |
| 1 | All deliveries need a dock slot | supported | `source_a.md` | 'All deliveries need a dock slot.' in `source_a.md` -- source_a.md directly states this claim. |
| 2 | Slots are booked through the facilities portal | supported | `source_a.md` | 'Book slots through the facilities portal.' in `source_a.md` -- source_a.md states that slots are booked through the facilities portal. |
| 3 | A slot is 45 minutes | supported | `source_a.md` | 'A slot is 45 minutes.' in `source_a.md` -- source_a.md directly states the slot duration. |
| 4 | A vehicle over 7.5 tonnes needs two consecutive slots | supported | `source_a.md` | 'A vehicle over 7.5 tonnes needs two consecutive slots' in `source_a.md` -- source_a.md states this requirement for larger vehicles. |
| 5 | The portal will not let you book two consecutive slots separately | supported | `source_a.md` | 'the portal will not let you book them separately' in `source_a.md` -- source_a.md specifies the portal's restriction on separate booking of consecutive slots. |
| 6 | Slots open 14 days ahead | supported | `source_a.md` | 'Slots open 14 days ahead' in `source_a.md` -- source_a.md states the booking window opening time. |
| 7 | Slots close 4 hours before the slot starts | supported | `source_a.md` | 'close 4 hours before the slot starts' in `source_a.md` -- source_a.md specifies when the booking window closes. |
| 8 | There is no same-hour booking | supported | `source_a.md` | 'There is no same-hour booking.' in `source_a.md` -- source_a.md directly states this booking restriction. |
| 9 | The dock booking phone line was retired | supported | `source_a.md` | 'The dock booking phone line was retired' in `source_a.md` -- source_a.md states the phone line was retired. |
| 10 | The dock booking phone number no longer connects | supported | `source_a.md` | 'the number no longer connects' in `source_a.md` -- source_a.md states the retired phone line no longer connects. |
| 12 | Drivers who call the old dock booking phone number hear a recorded message pointing them at the portal | supported | `source_a.md` | 'Drivers who call the old number hear a recorded message pointing them at the portal.' in `source_a.md` -- source_a.md states what drivers hear when calling the retired phone line. |
| 13 | Drivers report to the gatehouse with the booking reference | supported | `source_a.md` | 'Drivers report to the gatehouse with the booking reference.' in `source_a.md` -- source_a.md states this procedure on arrival at the dock. |
| 14 | The gatehouse checks the reference against the day sheet | supported | `source_a.md` | 'The gatehouse checks the reference against the day sheet' in `source_a.md` -- source_a.md describes the gatehouse's verification process. |
| 15 | The gatehouse directs the vehicle to a bay | supported | `source_a.md` | 'directs the vehicle to a bay' in `source_a.md` -- source_a.md states the gatehouse directs vehicles to bays. |
| 16 | A driver without a reference waits in the holding area until a slot is free | supported | `source_a.md` | 'A driver without a reference waits in the holding area until a slot is free.' in `source_a.md` -- source_a.md fully states this procedure for drivers without a booking reference. |
| 17 | A vehicle still on the bay 15 minutes after its slot ends is logged as an overrun | supported | `source_a.md` | 'A vehicle still on the bay 15 minutes after its slot ends is logged as an overrun.' in `source_a.md` -- Both sources state this overrun definition; source_a.md provides the full claim. |
| 18 | A supplier with three overruns in a quarter is asked to rebook through their account manager | supported | `source_a.md` | 'Three overruns in a quarter and the supplier is asked to rebook through their account manager.' in `source_a.md` -- source_a.md states the consequence of three quarterly overruns. |

## Structure

**9** mechanical check(s) over **36** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **18** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **26**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 1 run(s) over 18 attributed segment(s) — not conclusive on this evidence base. 6 of 12 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Over budget — declared loss past the ceiling

- 2 of 36 segments are declared dropped (5.6%), over the 3% budget

## Review queue

**1** claim(s) the merge declared dropped and the forward pass confirms are gone. Each is a decision to review — put the fact back, or agree it stays out — and none of them is counted as a finding above.

- **B-006** (`source_b.md:14`) — The dock booking line is on extension 2140.
  - left out of: `b10`
  - the merge's reason: conflicts with base statement that phone line was retired
  - confirmed absent: the forward pass looked for this claim in `merged.md` and did not find it -- The reference text does not mention any extension number for the dock booking line.

> **Over budget.** The merge declared **2** drop(s) of 36 source segment(s), **5.6%**, over the 3% budget: past that share the omissions are the finding, whatever each one says about itself.

## Declarations

The merge declared **16** departure(s) from its sources. Checking them confirms 7, rejects 1, and leaves 8 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 2 of 36 source segment(s) declared gone, **5.6%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | base document title retained in merged document | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Loading Dock Booking - Standard Operating Procedure' and says so (no claim traced to it) |
| `b2` | superseded | base document heading; both sections consolidate same topic | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b3` | superseded | base document wording; equivalent facts stated once | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-001`) |
| `b4` | superseded | base document wording; equivalent facts stated once | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b5` | superseded | base document wording; equivalent facts stated once | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-002`) |
| `b6` | superseded | base version includes portal restriction detail not in source_b | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-003`) |
| `b7` | superseded | base document heading; both sections consolidate same topic | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b8` | duplicate | identical text in both documents; stated once in merge | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-004`, `B-005`) |
| `b9` | superseded | base document section heading; phone procedures differ significantly | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b10` | dropped | conflicts with base statement that phone line was retired | **confirmed** | declared 'dropped' and every claim from it came back MISSING (`B-006`) |
| `b11` | dropped | conflicts with base statement that phone line was retired | **rejected** | declared 'dropped', which predicts MISSING; B-007 came back CONTRADICTED (`B-007`) |
| `b12` | superseded | base document heading; both sections consolidate same topic | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b13` | superseded | base document wording; equivalent facts stated once | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b14` | superseded | base version specifies timing condition not in source_b | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b15` | superseded | base document heading; both sections consolidate same topic | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b16` | duplicate | identical text in both documents; stated once in merge | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-008`) |


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
| Calls | 7 live, 0 cached, 0 replayed |
| Tokens | unknown (7 call(s) reported no usage) |
| Cost | unmeasured (7 call(s) reported no tokens, so no figure can be derived) |
| Schema repairs | 1 |
| Isolation | decompose, merge, verify: safe mode, no tools |
| Errors | 0 |
| Duration | 547.5s |
| Generated | 2026-09-27T17:03:11+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup haiku-4.5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
