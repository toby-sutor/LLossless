## Verdict

**6 finding(s).** In the claims: 3 contradicted. In the structure: 3 verbatim violation.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 19 |
| Claims extracted from `source_a.md` | 18 |
| Claims extracted from `source_b.md` | 13 |
| Forward — source claims accounted for in the merge | **28/31** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **18/18** |
| Forward — `source_b.md` claims accounted for | **10/13** |
| Reverse — merge claims found in a source | **19/19** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **50/50** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **B-007** -- the two documents disagree
  - `source_b.md:14` says: If the portal is down, the dock booking line can be called on extension 2140.
  - `merged.md` says: 'The dock booking phone line was retired and the number no longer connects.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: A retired line whose number no longer connects cannot be called for booking when the portal is down.
- **B-008** -- the two documents disagree
  - `source_b.md:14` says: If the portal is down, the dock supervisor will enter the slot for the requester.
  - `merged.md` says: 'All bookings go through the portal.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text requires every booking to go through the portal, rather than providing for a supervisor to enter a slot when it is down.
- **B-009** -- the two documents disagree
  - `source_b.md:15` says: Phone requests are taken between 08:00 and 16:00 on working days only.
  - `merged.md` says: 'The dock booking phone line was retired and the number no longer connects. All bookings go through the portal.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Phone booking requests are not taken because the line has been retired.

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
| 1 | All deliveries need a dock slot. | 5 | carried | 'All deliveries need a dock slot.' in `merged.md` -- The text states the claim directly. |
| 2 | Slots are booked through the facilities portal. | 5 | carried | 'Book slots through the facilities portal.' in `merged.md` -- The text directs users to book slots through the facilities portal. |
| 3 | A slot is 45 minutes. | 5 | carried | 'A slot is 45 minutes.' in `merged.md` -- The stated slot length is 45 minutes. |
| 4 | A vehicle over 7.5 tonnes needs two consecutive slots. | 6 | carried | 'A vehicle over 7.5 tonnes needs two consecutive slots' in `merged.md` -- The text states this requirement directly. |
| 5 | The portal will not let users book the two consecutive slots separately. | 7 | carried | 'A vehicle over 7.5 tonnes needs two consecutive slots, and the portal will not let you book them separately.' in `merged.md` -- The portal does not allow the required consecutive slots to be booked separately. |
| 6 | Slots open 14 days ahead. | 11 | carried | 'Slots open 14 days ahead' in `merged.md` -- The opening window is stated directly. |
| 7 | Slots close 4 hours before the slot starts. | 11 | carried | 'close 4 hours before the slot starts' in `merged.md` -- The text gives this closing time for slots. |
| 8 | There is no same-hour booking. | 11 | carried | 'There is no same-hour booking.' in `merged.md` -- The text states the claim directly. |
| 9 | The dock booking phone line was retired. | 16 | carried | 'The dock booking phone line was retired' in `merged.md` -- The text states that the line was retired. |
| 10 | The dock booking phone line number no longer connects. | 16 | carried | 'The dock booking phone line was retired and the number no longer connects.' in `merged.md` -- The text states that the line's number no longer connects. |
| 11 | All bookings go through the portal. | 16 | carried | 'All bookings go through the portal.' in `merged.md` -- The text states the claim directly. |
| 12 | Drivers who call the old dock booking phone line number hear a recorded message pointing them at the portal. | 17 | carried | 'Drivers who call the old number hear a recorded message pointing them at the portal.' in `merged.md` -- In context, the old number is the dock booking phone line number. |
| 13 | Drivers report to the gatehouse with the booking reference. | 22 | carried | 'Drivers report to the gatehouse and give the booking reference.' in `merged.md` -- Reporting to the gatehouse and giving the reference supports the claim. |
| 14 | The gatehouse checks the booking reference against the day sheet. | 22 | carried | 'The gatehouse checks the reference against the day sheet' in `merged.md` -- In context, the reference is the booking reference. |
| 15 | The gatehouse directs the vehicle to a bay. | 23 | carried | 'directs the vehicle to a bay' in `merged.md` -- The sentence identifies the gatehouse as the party directing the vehicle. |
| 16 | A driver without a booking reference waits in the holding area until a slot is free. | 23 | carried | 'A driver without a reference waits in the holding area until a slot is free.' in `merged.md` -- In context, the reference is the booking reference. |
| 17 | A vehicle still on the bay 15 minutes after its slot ends is logged as an overrun. | 28 | carried | 'A vehicle still on the bay 15 minutes after its slot ends is logged as an overrun.' in `merged.md` -- The text states the overrun condition directly. |
| 18 | After three overruns in a quarter, the supplier is asked to rebook through their account manager. | 29 | carried | 'Three overruns in a quarter and the supplier is asked to rebook through their account manager.' in `merged.md` -- The text states the consequence of three overruns in a quarter. |

### `source_b.md` -- 13 claim(s): 0 dropped, 3 contradicted, 0 carried in part, 10 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 7 | If the portal is down, the dock booking line can be called on extension 2140. | 14 | contradicted | 'The dock booking phone line was retired and the number no longer connects.' in `merged.md` -- A retired line whose number no longer connects cannot be called for booking when the portal is down. |
| 8 | If the portal is down, the dock supervisor will enter the slot for the requester. | 14 | contradicted | 'All bookings go through the portal.' in `merged.md` -- The text requires every booking to go through the portal, rather than providing for a supervisor to enter a slot when it is down. |
| 9 | Phone requests are taken between 08:00 and 16:00 on working days only. | 15 | contradicted | 'The dock booking phone line was retired and the number no longer connects. All bookings go through the portal.' in `merged.md` -- Phone booking requests are not taken because the line has been retired. |
| 1 | Every delivery needs a dock slot. | 5 | carried | 'All deliveries need a dock slot.' in `merged.md` -- All deliveries means every delivery. |
| 2 | Slots are requested through the facilities portal. | 5 | carried | 'Book slots through the facilities portal.' in `merged.md` -- Booking slots through the portal supports requesting them there. |
| 3 | A slot is 45 minutes long. | 5 | carried | 'A slot is 45 minutes.' in `merged.md` -- The text states the slot length directly. |
| 4 | Vehicles over 7.5 tonnes need two consecutive slots. | 6 | carried | 'A vehicle over 7.5 tonnes needs two consecutive slots' in `merged.md` -- The text states this requirement directly. |
| 5 | Slots open 14 days ahead. | 10 | carried | 'Slots open 14 days ahead' in `merged.md` -- The opening window is stated directly. |
| 6 | Slots close 4 hours before the slot starts. | 10 | carried | 'close 4 hours before the slot starts' in `merged.md` -- The text gives this closing time for slots. |
| 10 | Drivers report to the gatehouse. | 20 | carried | 'Drivers report to the gatehouse' in `merged.md` -- The text states where drivers report. |
| 11 | Drivers give the booking reference. | 20 | carried | 'Drivers report to the gatehouse and give the booking reference.' in `merged.md` -- The text states that drivers give the booking reference. |
| 12 | Drivers without a reference wait in the holding area. | 20 | carried | 'A driver without a reference waits in the holding area until a slot is free.' in `merged.md` -- The text states that a driver without a reference waits in the holding area. |
| 13 | A vehicle still on the bay 15 minutes after its slot ends is logged as an overrun. | 25 | carried | 'A vehicle still on the bay 15 minutes after its slot ends is logged as an overrun.' in `merged.md` -- The text states the overrun condition exactly. |

### `merged.md` -- 19 claim(s): 0 invented, 0 contradicted, 0 supported in part, 19 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | All deliveries need a dock slot. | supported | `source_a.md` | 'All deliveries need a dock slot.' in `source_a.md` -- The source states the claim directly. |
| 2 | Dock slots are booked through the facilities portal. | supported | `source_a.md` | 'Book slots through the facilities portal.' in `source_a.md` -- The source identifies the facilities portal as the booking method. |
| 3 | A dock slot is 45 minutes. | supported | `source_a.md` | 'A\nslot is 45 minutes.' in `source_a.md` -- The source gives the slot duration as 45 minutes. |
| 4 | A vehicle over 7.5 tonnes needs two consecutive slots. | supported | `source_a.md` | 'A vehicle over 7.5 tonnes needs two consecutive slots' in `source_a.md` -- The source states the vehicle threshold and slot requirement. |
| 5 | The facilities portal will not let users book the two consecutive slots for a vehicle over 7.5 tonnes separately. | supported | `source_a.md` | 'A vehicle over 7.5 tonnes needs two consecutive slots and\nthe portal will not let you book them separately.' in `source_a.md` -- The source says the portal does not allow those slots to be booked separately. |
| 6 | Dock slots open 14 days ahead. | supported | `source_a.md` | 'Slots open 14 days ahead' in `source_a.md` -- The source states when slots open. |
| 7 | Dock slots close 4 hours before the slot starts. | supported | `source_a.md` | 'close 4 hours before the slot starts' in `source_a.md` -- The source states the closing time for slots. |
| 8 | There is no same-hour booking for dock slots. | supported | `source_a.md` | 'There is no\nsame-hour booking.' in `source_a.md` -- The source explicitly rules out same-hour booking. |
| 9 | The dock booking phone line was retired. | supported | `source_a.md` | 'The dock booking phone line was retired' in `source_a.md` -- The source states that the phone line was retired. |
| 10 | The dock booking phone number no longer connects. | supported | `source_a.md` | 'the number no longer connects' in `source_a.md` -- The source says the dock booking phone number no longer connects. |
| 11 | All dock bookings go through the facilities portal. | supported | `source_a.md` | 'All\nbookings go through the portal.' in `source_a.md` -- The source states that all bookings use the portal, although source_b.md describes a phone fallback. |
| 12 | Drivers who call the old dock booking phone number hear a recorded message pointing them at the facilities portal. | supported | `source_a.md` | 'Drivers who call the old number hear a recorded\nmessage pointing them at the portal.' in `source_a.md` -- The source describes the recorded message heard by callers to the old dock number. |
| 13 | Drivers report to the gatehouse. | supported | `source_a.md` | 'Drivers report to the gatehouse' in `source_a.md` -- The source states where drivers report. |
| 14 | Drivers give the booking reference at the gatehouse. | supported | `source_a.md` | 'Drivers report to the gatehouse with the booking reference.' in `source_a.md` -- Reporting with the booking reference supports giving it at the gatehouse. |
| 15 | The gatehouse checks the booking reference against the day sheet. | supported | `source_a.md` | 'The gatehouse checks\nthe reference against the day sheet' in `source_a.md` -- The source states the gatehouse's reference check. |
| 16 | The gatehouse directs the vehicle to a bay. | supported | `source_a.md` | 'directs the vehicle to a bay' in `source_a.md` -- The source assigns this action to the gatehouse. |
| 17 | A driver without a booking reference waits in the holding area until a slot is free. | supported | `source_a.md` | 'A driver\nwithout a reference waits in the holding area until a slot is free.' in `source_a.md` -- The source states both where the driver waits and when the wait ends. |
| 18 | A vehicle still on the bay 15 minutes after its slot ends is logged as an overrun. | supported | `source_a.md` | 'A vehicle still on the bay 15 minutes after its slot ends is logged as an\noverrun.' in `source_a.md` -- The source gives the same overrun threshold and consequence. |
| 19 | After three overruns in a quarter, the supplier is asked to rebook through their account manager. | supported | `source_a.md` | 'Three overruns in a quarter and the supplier is asked to rebook through\ntheir account manager.' in `source_a.md` -- The source states the three-overrun threshold and the request to rebook through the account manager. |

## Structure

**9** mechanical check(s) over **36** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **19** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **31**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 3 run(s) over 18 attributed segment(s) — sources interleaved. 6 of 12 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Verbatim violation — an invariant-core token did not survive unchanged

- `b10` (`source_b.md`) — numeric '2140' (and) does not survive into the merge unchanged
- `b11` (`source_b.md`) — numeric '08:00' (and) does not survive into the merge unchanged
- `b11` (`source_b.md`) — numeric '16:00' (on) does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **25** departure(s) from its sources. Checking them confirms 20, rejects 0, and leaves 5 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 36 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a5` | reworded | The booking length is placed on one prose line. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-003`) |
| `a6` | reworded | The vehicle rule is placed on one prose line. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-004`, `A-005`) |
| `a9` | reworded | The booking restriction is placed on one prose line. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-008`) |
| `a12` | reworded | The portal rule is placed on one prose line. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-011`) |
| `a13` | reworded | The recorded-message detail is placed on one prose line. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-012`) |
| `a15` | superseded | The arrival section uses the more precise gatehouse wording. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`A-013`) |
| `a16` | reworded | The gatehouse check is placed on one prose line. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-014`, `A-015`) |
| `a17` | reworded | The holding-area rule is placed on one prose line. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-016`) |
| `a19` | reworded | The overrun definition is placed on one prose line. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-017`) |
| `a20` | reworded | The supplier consequence is placed on one prose line. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-018`) |
| `b1` | superseded | The base title is retained. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Loading Dock Booking - Standard Operating Procedure' and says so (no claim traced to it) |
| `b2` | superseded | The booking section keeps the base heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b3` | superseded | The booking requirement is stated once in the base wording. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-001`) |
| `b4` | superseded | The portal instruction is stated once in the base wording. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-002`) |
| `b5` | superseded | The slot length is stated once in the base wording. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-003`) |
| `b6` | subsumed | The vehicle rule includes the portal restriction. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-004`) |
| `b7` | superseded | The booking window keeps the base heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b8` | duplicate | The booking window is already stated by source_a.md. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-005`, `B-006`) |
| `b9` | superseded | The phone section keeps the heading matching the chosen procedure. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b10` | superseded | The phone section follows the retired-line account. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-007`, `B-008`) |
| `b11` | superseded | Phone-request hours do not apply to the retired line. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-009`) |
| `b12` | superseded | The arrival section keeps the base heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b14` | subsumed | The holding-area rule includes when the wait ends. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-012`) |
| `b15` | superseded | The overrun section keeps the base heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b16` | duplicate | The overrun definition is already stated by source_a.md. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-013`) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | bf7d5842201d (hosted) |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | gpt-6-sol |
| Model (decompose) | gpt-6-sol |
| Model (verify) | gpt-6-sol |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed 0, thinking decompose, merge, verify, profile openai-reasoning |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 7 live, 0 cached, 0 replayed |
| Tokens | 15,065 in, 10,779 out, 0 cached, 2,640 reasoning |
| Cost | ~$0.14 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 113.2s |
| Generated | 2026-09-27T15:37:38+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `bf7d5842201d`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
