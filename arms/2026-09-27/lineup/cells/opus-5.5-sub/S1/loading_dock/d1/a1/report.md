## Verdict

**5 finding(s).** In the claims: 1 partially dropped, 4 contradicted.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 18 |
| Claims extracted from `source_a.md` | 18 |
| Claims extracted from `source_b.md` | 14 |
| Forward — source claims accounted for in the merge | **27/32** |
| Forward — carried only in part | 1 |
| Forward — `source_a.md` claims accounted for | **18/18** |
| Forward — `source_b.md` claims accounted for | **9/14** (1 in part) |
| Reverse — merge claims found in a source | **18/18** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **50/50** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Partly dropped — the merge carries some of this claim

- **B-011** (`source_b.md:20`) — Drivers report to the gatehouse on the day of delivery.
  - evidence: 'Drivers report to the gatehouse with the booking reference.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The reference states drivers report to the gatehouse but does not say this happens on the day of delivery.

### Contradicted — the merge states something different

- **B-007** -- the two documents disagree
  - `source_b.md:14` says: If the facilities portal is down, dock slots can be requested by calling the dock booking line on extension 2140.
  - `merged.md` says: 'The dock booking phone line was retired and the number no longer connects. All bookings go through the portal.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference states the phone line was retired and all bookings go through the portal, which is incompatible with requesting slots by phone as a fallback.
- **B-008** -- the two documents disagree
  - `source_b.md:15` says: For phone requests, the dock supervisor enters the dock slot.
  - `merged.md` says: 'The dock booking phone line was retired and the number no longer connects. All bookings go through the portal.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: With the phone line retired and all bookings going through the portal, a phone request route handled by the dock supervisor is incompatible with the reference.
- **B-009** -- the two documents disagree
  - `source_b.md:15` says: Phone requests for dock slots are taken between 08:00 and 16:00.
  - `merged.md` says: 'The dock booking phone line was retired and the number no longer connects.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference states the phone line was retired, so phone requests are not taken during any hours.
- **B-010** -- the two documents disagree
  - `source_b.md:15` says: Phone requests for dock slots are taken on working days only.
  - `merged.md` says: 'The dock booking phone line was retired and the number no longer connects.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference states the phone line was retired, so phone requests are not taken on any days.

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
| 1 | All deliveries need a dock slot. | 5 | carried | 'Every delivery needs a dock slot' in `merged.md` -- The reference states every delivery needs a dock slot, which means the same as all deliveries needing one. |
| 2 | Dock slots are booked through the facilities portal. | 5 | carried | 'Every delivery needs a dock slot, booked through the facilities portal.' in `merged.md` -- The reference states dock slots are booked through the facilities portal. |
| 3 | A dock slot is 45 minutes. | 5 | carried | 'A slot is 45 minutes long.' in `merged.md` -- The reference states a slot is 45 minutes long. |
| 4 | A vehicle over 7.5 tonnes needs two consecutive dock slots. | 6 | carried | 'A vehicle over 7.5 tonnes needs two consecutive slots' in `merged.md` -- The reference states vehicles over 7.5 tonnes need two consecutive slots. |
| 5 | The facilities portal will not let you book the two consecutive slots for a vehicle over 7.5 tonnes separately. | 7 | carried | 'the portal will not let you book them separately' in `merged.md` -- The reference states the portal will not let you book the two consecutive slots separately. |
| 6 | Dock slots open 14 days ahead. | 11 | carried | 'Slots open 14 days ahead' in `merged.md` -- The reference states slots open 14 days ahead. |
| 7 | Dock slots close 4 hours before the slot starts. | 11 | carried | 'close 4 hours before the slot starts' in `merged.md` -- The reference states slots close 4 hours before the slot starts. |
| 8 | There is no same-hour dock booking. | 11 | carried | 'There is no same-hour booking.' in `merged.md` -- The reference states there is no same-hour booking. |
| 9 | The dock booking phone line was retired. | 16 | carried | 'The dock booking phone line was retired' in `merged.md` -- The reference states the dock booking phone line was retired. |
| 10 | The dock booking phone number no longer connects. | 16 | carried | 'the number no longer connects' in `merged.md` -- The reference states the phone line's number no longer connects. |
| 11 | All dock bookings go through the portal. | 16 | carried | 'All bookings go through the portal.' in `merged.md` -- The reference states all bookings go through the portal. |
| 12 | Drivers who call the old dock booking number hear a recorded message pointing them at the portal. | 17 | carried | 'Drivers who call the old number hear a recorded message pointing them at the portal.' in `merged.md` -- The reference states callers to the old number hear a recorded message pointing them at the portal. |
| 13 | Drivers report to the gatehouse with the booking reference. | 22 | carried | 'Drivers report to the gatehouse with the booking reference.' in `merged.md` -- The reference states drivers report to the gatehouse with the booking reference. |
| 14 | The gatehouse checks the booking reference against the day sheet. | 22 | carried | 'The gatehouse checks the reference against the day sheet' in `merged.md` -- The reference states the gatehouse checks the reference against the day sheet. |
| 15 | The gatehouse directs the vehicle to a bay. | 22 | carried | 'directs the vehicle to a bay' in `merged.md` -- The reference states the gatehouse directs the vehicle to a bay. |
| 16 | A driver without a booking reference waits in the holding area until a slot is free. | 23 | carried | 'A driver without a reference waits in the holding area until a slot is free.' in `merged.md` -- The reference states a driver without a reference waits in the holding area until a slot is free. |
| 17 | A vehicle still on the bay 15 minutes after its slot ends is logged as an overrun. | 28 | carried | 'A vehicle still on the bay 15 minutes after its slot ends is logged as an overrun.' in `merged.md` -- The reference states this overrun rule verbatim. |
| 18 | After three overruns in a quarter, the supplier is asked to rebook through their account manager. | 29 | carried | 'After three overruns in a quarter, the supplier is asked to rebook through their account manager.' in `merged.md` -- The reference states this rule verbatim. |

### `source_b.md` -- 14 claim(s): 0 dropped, 4 contradicted, 1 carried in part, 9 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 7 | If the facilities portal is down, dock slots can be requested by calling the dock booking line on extension 2140. | 14 | contradicted | 'The dock booking phone line was retired and the number no longer connects. All bookings go through the portal.' in `merged.md` -- The reference states the phone line was retired and all bookings go through the portal, which is incompatible with requesting slots by phone as a fallback. |
| 8 | For phone requests, the dock supervisor enters the dock slot. | 15 | contradicted | 'The dock booking phone line was retired and the number no longer connects. All bookings go through the portal.' in `merged.md` -- With the phone line retired and all bookings going through the portal, a phone request route handled by the dock supervisor is incompatible with the reference. |
| 9 | Phone requests for dock slots are taken between 08:00 and 16:00. | 15 | contradicted | 'The dock booking phone line was retired and the number no longer connects.' in `merged.md` -- The reference states the phone line was retired, so phone requests are not taken during any hours. |
| 10 | Phone requests for dock slots are taken on working days only. | 15 | contradicted | 'The dock booking phone line was retired and the number no longer connects.' in `merged.md` -- The reference states the phone line was retired, so phone requests are not taken on any days. |
| 11 | Drivers report to the gatehouse on the day of delivery. | 20 | carried in part | 'Drivers report to the gatehouse with the booking reference.' in `merged.md` -- The reference states drivers report to the gatehouse but does not say this happens on the day of delivery. |
| 1 | Every delivery needs a dock slot. | 5 | carried | 'Every delivery needs a dock slot' in `merged.md` -- The reference states every delivery needs a dock slot. |
| 2 | Dock slots are requested through the facilities portal. | 5 | carried | 'Every delivery needs a dock slot, booked through the facilities portal.' in `merged.md` -- The reference states dock slots are booked through the facilities portal, which carries the same meaning as requested through it. |
| 3 | A dock slot is 45 minutes long. | 6 | carried | 'A slot is 45 minutes long.' in `merged.md` -- The reference states a slot is 45 minutes long. |
| 4 | Vehicles over 7.5 tonnes need two consecutive dock slots. | 6 | carried | 'A vehicle over 7.5 tonnes needs two consecutive slots' in `merged.md` -- The reference states vehicles over 7.5 tonnes need two consecutive slots. |
| 5 | Dock slots open 14 days ahead. | 10 | carried | 'Slots open 14 days ahead' in `merged.md` -- The reference states slots open 14 days ahead. |
| 6 | Dock slots close 4 hours before the slot starts. | 10 | carried | 'close 4 hours before the slot starts' in `merged.md` -- The reference states slots close 4 hours before the slot starts. |
| 12 | Drivers give the booking reference at the gatehouse. | 20 | carried | 'Drivers report to the gatehouse with the booking reference. The gatehouse checks the reference against the day sheet' in `merged.md` -- The reference has drivers bring the booking reference to the gatehouse, which checks it, entailing that drivers give the reference there. |
| 13 | Drivers without a booking reference wait in the holding area. | 20 | carried | 'A driver without a reference waits in the holding area until a slot is free.' in `merged.md` -- The reference states drivers without a reference wait in the holding area, which entails the claim. |
| 14 | A vehicle still on the bay 15 minutes after its dock slot ends is logged as an overrun. | 25 | carried | 'A vehicle still on the bay 15 minutes after its slot ends is logged as an overrun.' in `merged.md` -- The reference states this overrun rule verbatim. |

### `merged.md` -- 18 claim(s): 0 invented, 0 contradicted, 0 supported in part, 18 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Every delivery needs a dock slot. | supported | `source_b.md` | 'Every delivery needs a dock slot.' in `source_b.md` -- Source B states this directly, and source A says the same thing in other words. |
| 2 | Dock slots are booked through the facilities portal. | supported | `source_a.md` | 'Book slots through the facilities portal.' in `source_a.md` -- Source A states that slots are booked through the facilities portal. |
| 3 | A dock slot is 45 minutes long. | supported | `source_b.md` | 'slot is 45 minutes long.' in `source_b.md` -- Source B states the 45-minute slot length, and source A matches it. |
| 4 | A vehicle over 7.5 tonnes needs two consecutive dock slots. | supported | `source_b.md` | 'Vehicles over 7.5 tonnes need two consecutive slots.' in `source_b.md` -- Source B states this directly, and source A agrees. |
| 5 | The facilities portal will not let you book the two consecutive slots for a vehicle over 7.5 tonnes separately. | supported | `source_a.md` | 'the portal will not let you book them separately.' in `source_a.md` -- Source A states that the portal will not allow the two consecutive slots to be booked separately. |
| 6 | Dock slots open 14 days ahead. | supported | `source_a.md` | 'Slots open 14 days ahead and close 4 hours before the slot starts.' in `source_a.md` -- Both sources state that slots open 14 days ahead. |
| 7 | Dock slots close 4 hours before the slot starts. | supported | `source_a.md` | 'Slots open 14 days ahead and close 4 hours before the slot starts.' in `source_a.md` -- Both sources state that slots close 4 hours before the slot starts. |
| 8 | There is no same-hour dock booking. | supported | `source_a.md` | 'There is no\nsame-hour booking.' in `source_a.md` -- Source A states that there is no same-hour booking. |
| 9 | The dock booking phone line was retired. | supported | `source_a.md` | 'The dock booking phone line was retired' in `source_a.md` -- Source A states this, but source B conflicts with it by describing an active booking line on extension 2140, and the claim does not report that disagreement. |
| 10 | The dock booking phone number no longer connects. | supported | `source_a.md` | 'the number no longer connects' in `source_a.md` -- Source A states this, but source B conflicts with it by telling users to call extension 2140 when the portal is down. |
| 11 | All dock bookings go through the portal. | supported | `source_a.md` | 'All\nbookings go through the portal.' in `source_a.md` -- Source A states this, but source B conflicts with it by allowing phone requests when the portal is down. |
| 12 | Drivers who call the old dock booking number hear a recorded message pointing them at the portal. | supported | `source_a.md` | 'Drivers who call the old number hear a recorded\nmessage pointing them at the portal.' in `source_a.md` -- Source A states this directly, although source B describes the phone line as still in use. |
| 13 | Drivers report to the gatehouse with the booking reference. | supported | `source_a.md` | 'Drivers report to the gatehouse with the booking reference.' in `source_a.md` -- Source A states this directly, and source B agrees. |
| 14 | The gatehouse checks the booking reference against the day sheet. | supported | `source_a.md` | 'The gatehouse checks\nthe reference against the day sheet' in `source_a.md` -- Source A states that the gatehouse checks the reference against the day sheet. |
| 15 | The gatehouse directs the vehicle to a bay. | supported | `source_a.md` | 'directs the vehicle to a bay' in `source_a.md` -- Source A states that the gatehouse directs the vehicle to a bay. |
| 16 | A driver without a booking reference waits in the holding area until a slot is free. | supported | `source_a.md` | 'A driver\nwithout a reference waits in the holding area until a slot is free.' in `source_a.md` -- Source A states this in full, including the condition 'until a slot is free'. |
| 17 | A vehicle still on the bay 15 minutes after its slot ends is logged as an overrun. | supported | `source_b.md` | 'A vehicle still on the bay 15 minutes after its slot ends is logged as an\noverrun.' in `source_b.md` -- Both sources state this, and the span is quoted from source B. |
| 18 | After three overruns in a quarter, the supplier is asked to rebook through their account manager. | supported | `source_a.md` | 'Three overruns in a quarter and the supplier is asked to rebook through\ntheir account manager.' in `source_a.md` -- Source A states this directly. |

## Structure

**9** mechanical check(s) over **36** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **18** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **32**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 3 run(s) over 17 attributed segment(s) — sources interleaved. 6 of 12 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

No structural finding.

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **27** departure(s) from its sources. Checking them confirms 21, rejects 1, and leaves 5 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 36 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a3` | subsumed | Slot requirement combined with booking channel. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-001`) |
| `a4` | subsumed | Booking channel combined with slot requirement. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-002`) |
| `a5` | superseded | Slot length; b5 wording used. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`A-003`) |
| `a6` | reworded | Heavy vehicle rule; line break joined and comma added. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-004`, `A-005`) |
| `a9` | reworded | Line break joined into prose. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-008`) |
| `a12` | reworded | Line break joined into prose. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-011`) |
| `a13` | reworded | Line break joined into prose. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-012`) |
| `a16` | reworded | Line break joined into prose. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-014`, `A-015`) |
| `a17` | reworded | Line break joined into prose. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-016`) |
| `a19` | reworded | Line break joined into prose. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-017`) |
| `a20` | reworded | Overrun consequence; sentence smoothed. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-018`) |
| `b1` | superseded | Base title kept. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Loading Dock Booking - Standard Operating Procedure' and says so (no claim traced to it) |
| `b2` | superseded | Base heading for booking section kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b3` | subsumed | Same slot requirement; b3 wording used in combined sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-001`) |
| `b4` | subsumed | Same booking channel as a4. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-002`) |
| `b5` | reworded | Slot length; line break joined. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-003`) |
| `b6` | duplicate | Heavy vehicle rule already carried from a6. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-004`) |
| `b7` | superseded | Base heading for booking window kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b8` | duplicate | Identical to a8. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-005`, `B-006`) |
| `b9` | superseded | Phone section; base heading and position kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b10` | superseded | Phone booking conflicts with base retirement; base chosen. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-007`, `B-008`) |
| `b11` | superseded | Phone hours moot once the line is retired; base chosen. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-009`, `B-010`) |
| `b12` | superseded | Base heading for arrival section kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b13` | duplicate | Same as a15. | **rejected** | declared 'duplicate', which predicts SUPPORTED; B-011 came back PARTIAL (`B-011`) |
| `b14` | duplicate | Same as a17, which is more specific. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-013`) |
| `b15` | superseded | Base heading for overrun section kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b16` | duplicate | Same as a19. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-014`) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | 31c2462e2828 (command) -- lineup opus-5.5-sub |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | claude-opus-5-5 -> claude-opus-5-5 |
| Model (decompose) | claude-opus-5-5 -> claude-opus-5-5 |
| Model (verify) | claude-opus-5-5 -> claude-opus-5-5 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile subscription, effort decompose=medium, merge=medium, verify=medium |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 6 live, 0 cached, 0 replayed |
| Tokens | unknown (6 call(s) reported no usage) |
| Cost | unmeasured (6 call(s) reported no tokens, so no figure can be derived) |
| Schema repairs | 0 |
| Isolation | decompose, merge, verify: safe mode, no tools |
| Errors | 0 |
| Duration | 113.4s |
| Generated | 2026-09-27T17:05:05+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup opus-5.5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
