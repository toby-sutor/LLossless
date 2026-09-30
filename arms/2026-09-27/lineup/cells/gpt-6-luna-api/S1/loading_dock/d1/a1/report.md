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
  - `source_b.md:14` says: If the portal is down, call the dock booking line on extension 2140.
  - `merged.md` says: 'The dock booking phone line was retired and the number no longer connects.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text says the booking line is retired and its number no longer connects, contradicting the instruction to call it.
- **B-008** -- the two documents disagree
  - `source_b.md:14` says: If the portal is down, the dock supervisor will enter the slot for the requester.
  - `merged.md` says: 'All bookings go through the portal.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The claim describes a non-portal booking, while the text says all bookings go through the portal.
- **B-009** -- the two documents disagree
  - `source_b.md:15` says: Phone requests are taken between 08:00 and 16:00 on working days only.
  - `merged.md` says: 'The dock booking phone line was retired and the number no longer connects.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The phone line is retired and does not connect, which is incompatible with taking phone requests during stated hours.

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
| 1 | All deliveries need a dock slot. | 5 | carried | 'All deliveries need a dock slot.' in `merged.md` -- The text states that all deliveries need a dock slot. |
| 2 | Slots are booked through the facilities portal. | 5 | carried | 'Book slots through the facilities portal.' in `merged.md` -- The text directs users to book slots through the facilities portal. |
| 3 | A slot is 45 minutes. | 5 | carried | 'A slot is 45 minutes.' in `merged.md` -- The text specifies that a slot is 45 minutes. |
| 4 | A vehicle over 7.5 tonnes needs two consecutive slots. | 6 | carried | 'A vehicle over 7.5 tonnes needs two consecutive slots' in `merged.md` -- The text states this requirement for vehicles over 7.5 tonnes. |
| 5 | The portal will not let you book two consecutive slots separately. | 7 | carried | 'the portal will not let you book them separately.' in `merged.md` -- “Them” refers to the two consecutive slots required for a heavy vehicle. |
| 6 | Slots open 14 days ahead. | 11 | carried | 'Slots open 14 days ahead' in `merged.md` -- The text says slots open 14 days ahead. |
| 7 | Slots close 4 hours before the slot starts. | 11 | carried | 'close 4 hours before the slot starts.' in `merged.md` -- The text says slots close 4 hours before they start. |
| 8 | There is no same-hour booking. | 11 | carried | 'There is no same-hour booking.' in `merged.md` -- The text explicitly rules out same-hour booking. |
| 9 | The dock booking phone line was retired. | 16 | carried | 'The dock booking phone line was retired' in `merged.md` -- The text states that the dock booking phone line was retired. |
| 10 | The number for the dock booking phone line no longer connects. | 16 | carried | 'the number no longer connects.' in `merged.md` -- The text says the phone line’s number no longer connects. |
| 11 | All bookings go through the portal. | 16 | carried | 'All bookings go through the portal.' in `merged.md` -- The text states that all bookings go through the portal. |
| 12 | Drivers who call the old number hear a recorded message pointing them at the portal. | 17 | carried | 'Drivers who call the old number hear a recorded message that points them to the portal.' in `merged.md` -- The text states that callers hear a recorded message directing them to the portal. |
| 13 | Drivers report to the gatehouse with the booking reference. | 22 | carried | 'Drivers report to the gatehouse with the booking reference.' in `merged.md` -- The text states that drivers report to the gatehouse with the reference. |
| 14 | The gatehouse checks the reference against the day sheet. | 22 | carried | 'The gatehouse checks the reference against the day sheet' in `merged.md` -- The text says the gatehouse checks the reference against the day sheet. |
| 15 | The gatehouse directs the vehicle to a bay. | 23 | carried | 'directs the vehicle to a bay.' in `merged.md` -- The text states that the gatehouse directs the vehicle to a bay. |
| 16 | A driver without a reference waits in the holding area until a slot is free. | 23 | carried | 'A driver without a reference waits in the holding area until a slot is free.' in `merged.md` -- The text states this procedure for a driver without a reference. |
| 17 | A vehicle still on the bay 15 minutes after its slot ends is logged as an overrun. | 28 | carried | 'A vehicle still on the bay 15 minutes after its slot ends is logged as an overrun.' in `merged.md` -- The text defines an overrun in these terms. |
| 18 | The supplier is asked to rebook through their account manager after three overruns in a quarter. | 29 | carried | 'Three overruns in a quarter and the supplier is asked to rebook through their account manager.' in `merged.md` -- The text says the supplier is asked to rebook through their account manager at three overruns in a quarter. |

### `source_b.md` -- 13 claim(s): 0 dropped, 3 contradicted, 0 carried in part, 10 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 7 | If the portal is down, call the dock booking line on extension 2140. | 14 | contradicted | 'The dock booking phone line was retired and the number no longer connects.' in `merged.md` -- The text says the booking line is retired and its number no longer connects, contradicting the instruction to call it. |
| 8 | If the portal is down, the dock supervisor will enter the slot for the requester. | 14 | contradicted | 'All bookings go through the portal.' in `merged.md` -- The claim describes a non-portal booking, while the text says all bookings go through the portal. |
| 9 | Phone requests are taken between 08:00 and 16:00 on working days only. | 15 | contradicted | 'The dock booking phone line was retired and the number no longer connects.' in `merged.md` -- The phone line is retired and does not connect, which is incompatible with taking phone requests during stated hours. |
| 1 | Every delivery needs a dock slot. | 5 | carried | 'All deliveries need a dock slot.' in `merged.md` -- The text states that all deliveries need a dock slot. |
| 2 | Delivery slot requests are made through the facilities portal. | 5 | carried | 'Book slots through the facilities portal.' in `merged.md` -- The text directs slot bookings through the facilities portal. |
| 3 | A slot is 45 minutes long. | 5 | carried | 'A slot is 45 minutes.' in `merged.md` -- The text specifies that a slot lasts 45 minutes. |
| 4 | Vehicles over 7.5 tonnes need two consecutive slots. | 6 | carried | 'A vehicle over 7.5 tonnes needs two consecutive slots' in `merged.md` -- The text states that vehicles over 7.5 tonnes need two consecutive slots. |
| 5 | Slots open 14 days ahead. | 10 | carried | 'Slots open 14 days ahead' in `merged.md` -- The text says slots open 14 days ahead. |
| 6 | Slots close 4 hours before the slot starts. | 10 | carried | 'close 4 hours before the slot starts.' in `merged.md` -- The text says slots close four hours before the slot starts. |
| 10 | Drivers report to the gatehouse. | 20 | carried | 'Drivers report to the gatehouse with the booking reference.' in `merged.md` -- The text explicitly says drivers report to the gatehouse. |
| 11 | Drivers give the booking reference. | 20 | carried | 'Drivers report to the gatehouse with the booking reference.' in `merged.md` -- The text says drivers report with the booking reference. |
| 12 | Drivers without a reference wait in the holding area. | 20 | carried | 'A driver without a reference waits in the holding area until a slot is free.' in `merged.md` -- The text explicitly says a driver without a reference waits in the holding area. |
| 13 | A vehicle still on the bay 15 minutes after its slot ends is logged as an overrun. | 25 | carried | 'A vehicle still on the bay 15 minutes after its slot ends is logged as an overrun.' in `merged.md` -- The text states this exact condition and classification. |

### `merged.md` -- 19 claim(s): 0 invented, 0 contradicted, 0 supported in part, 19 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | All deliveries need a dock slot. | supported | `source_a.md` | 'All deliveries need a dock slot.' in `source_a.md` -- Source_a.md states that every delivery needs a dock slot. |
| 2 | Slots must be booked through the facilities portal. | supported | `source_a.md` | 'Book slots through the facilities portal.' in `source_a.md` -- The source directs users to book slots through the facilities portal. |
| 3 | A slot is 45 minutes. | supported | `source_a.md` | 'A slot is 45 minutes.' in `source_a.md` -- The source states the slot duration is 45 minutes. |
| 4 | A vehicle over 7.5 tonnes needs two consecutive slots. | supported | `source_a.md` | 'A vehicle over 7.5 tonnes needs two consecutive slots' in `source_a.md` -- The source states that a vehicle over 7.5 tonnes needs two consecutive slots. |
| 5 | The portal will not let users book the two consecutive slots separately. | supported | `source_a.md` | 'the portal will not let you book them separately.' in `source_a.md` -- The source explicitly says the portal will not allow the two slots to be booked separately. |
| 6 | Slots open 14 days ahead. | supported | `source_a.md` | 'Slots open 14 days ahead' in `source_a.md` -- The source states that slots open 14 days ahead. |
| 7 | Slots close 4 hours before the slot starts. | supported | `source_a.md` | 'close 4 hours before the slot starts.' in `source_a.md` -- The source states that slots close four hours before the slot starts. |
| 8 | There is no same-hour booking. | supported | `source_a.md` | 'There is no same-hour booking.' in `source_a.md` -- The source explicitly states that there is no same-hour booking. |
| 9 | The dock booking phone line was retired. | supported | `source_a.md` | 'The dock booking phone line was retired' in `source_a.md` -- The source states that the dock booking phone line was retired. |
| 10 | The dock booking phone number no longer connects. | supported | `source_a.md` | 'the number no longer connects.' in `source_a.md` -- The source states that the phone number no longer connects. |
| 11 | All bookings go through the portal. | supported | `source_a.md` | 'All bookings go through the portal.' in `source_a.md` -- The source explicitly states that all bookings go through the portal. |
| 12 | Drivers who call the old number hear a recorded message. | supported | `source_a.md` | 'Drivers who call the old number hear a recorded\nmessage pointing them at the portal.' in `source_a.md` -- The source states that drivers calling the old number hear a recorded message. |
| 13 | The recorded message points drivers to the portal. | supported | `source_a.md` | 'pointing them at the portal.' in `source_a.md` -- The source states that the recorded message points drivers to the portal. |
| 14 | Drivers report to the gatehouse with the booking reference. | supported | `source_a.md` | 'Drivers report to the gatehouse with the booking reference.' in `source_a.md` -- The source states that drivers report to the gatehouse with the booking reference. |
| 15 | The gatehouse checks the reference against the day sheet. | supported | `source_a.md` | 'The gatehouse checks the\nreference against the day sheet' in `source_a.md` -- The source says the gatehouse checks the reference against the day sheet. |
| 16 | The gatehouse directs the vehicle to a bay. | supported | `source_a.md` | 'and directs the vehicle to a bay.' in `source_a.md` -- The source says the gatehouse directs the vehicle to a bay. |
| 17 | A driver without a reference waits in the holding area until a slot is free. | supported | `source_a.md` | 'A driver\nwithout a reference waits in the holding area until a slot is free.' in `source_a.md` -- The source states that a driver without a reference waits there until a slot is free. |
| 18 | A vehicle still on the bay 15 minutes after its slot ends is logged as an overrun. | supported | `source_a.md` | 'A vehicle still on the bay 15 minutes after its slot ends is logged as an\noverrun.' in `source_a.md` -- The source states that this situation is logged as an overrun. |
| 19 | When there are three overruns in a quarter, the supplier is asked to rebook through their account manager. | supported | `source_a.md` | 'Three overruns in a quarter and the supplier is asked to rebook through\ntheir account manager.' in `source_a.md` -- The source states that after three quarterly overruns the supplier is asked to rebook through their account manager. |

## Structure

**9** mechanical check(s) over **36** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **19** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **31**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 1 run(s) over 18 attributed segment(s) — not conclusive on this evidence base. 6 of 12 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

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
| `b1` | superseded | The base title is chosen. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Loading Dock Booking - Standard Operating Procedure' and says so (no claim traced to it) |
| `b2` | superseded | The base booking heading is chosen. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b3` | duplicate | The booking requirement is stated once. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-001`) |
| `b4` | duplicate | The booking method is stated once. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-002`) |
| `b5` | duplicate | The slot duration is stated once. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-003`) |
| `b6` | subsumed | The combined sentence includes the weight and slot requirements. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-004`) |
| `b7` | superseded | The base booking-window heading is chosen. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b8` | duplicate | The booking window is stated once. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-005`, `B-006`) |
| `b9` | superseded | The base heading reflects the chosen phone-line status. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b10` | superseded | The base procedure says the phone line no longer connects. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-007`, `B-008`) |
| `b11` | superseded | Phone-request hours do not apply when the line no longer connects. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-009`) |
| `b12` | superseded | The base arrival heading is chosen. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b13` | duplicate | The gatehouse reporting instruction is stated once. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-010`, `B-011`) |
| `b14` | subsumed | The base instruction includes the holding-area wait. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-012`) |
| `b15` | superseded | The base overrun heading is chosen. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b16` | duplicate | The overrun threshold is stated once. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-013`) |
| `a5` | reworded | The slot duration is set as a single-line sentence. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-003`) |
| `a6` | reworded | The weight and portal restriction are combined clearly. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-004`, `A-005`) |
| `a9` | reworded | The wrapped sentence is set on one line. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-008`) |
| `a12` | reworded | The wrapped sentence is set on one line. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-011`) |
| `a13` | reworded | The message direction is stated more clearly. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-012`) |
| `a16` | reworded | The wrapped sentence is set on one line. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-014`, `A-015`) |
| `a17` | reworded | The wrapped sentence is set on one line. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-016`) |
| `a19` | reworded | The wrapped sentence is set on one line. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-017`) |
| `a20` | reworded | The wrapped sentence is set on one line. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-018`) |


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
| Tokens | 15,035 in, 14,208 out, 0 cached, 7,347 reasoning |
| Cost | ~$0.01 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 102.3s |
| Generated | 2026-09-27T15:35:44+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `bf7d5842201d`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
