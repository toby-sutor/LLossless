## Verdict

**8 finding(s).** In the claims: 8 contradicted.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 18 |
| Claims extracted from `source_a.md` | 18 |
| Claims extracted from `source_b.md` | 14 |
| Forward — source claims accounted for in the merge | **28/32** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **18/18** |
| Forward — `source_b.md` claims accounted for | **10/14** |
| Reverse — merge claims found in a source | **14/18** |
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
  - why this was read as a contradiction: The reference text says the phone line was retired and all bookings go through the portal, which is incompatible with calling the line as a fallback.
- **B-008** -- the two documents disagree
  - `source_b.md:14` says: If the portal is down, the dock supervisor will enter the slot for the caller.
  - `merged.md` says: 'The dock booking phone line was retired and the number no longer connects.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference says the phone line is retired and all bookings go through the portal, which rules out a supervisor taking callers' bookings.
- **B-009** -- the two documents disagree
  - `source_b.md:15` says: Phone requests for dock slots are taken between 08:00 and 16:00.
  - `merged.md` says: 'The dock booking phone line was retired and the number no longer connects.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference states the phone line no longer connects, so phone requests are not taken during any hours.
- **B-010** -- the two documents disagree
  - `source_b.md:15` says: Phone requests for dock slots are taken on working days only.
  - `merged.md` says: 'The dock booking phone line was retired and the number no longer connects.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The phone line is retired, so phone requests are not taken on working days or any other days.
- **M-009** -- the two documents disagree
  - `merged.md:13` says: The dock booking phone line was retired.
  - `source_b.md` says: 'call the dock booking line on extension 2140' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source A says the phone line was retired, but source B says it is in service on extension 2140; the claim picks one side without reporting the conflict.
- **M-010** -- the two documents disagree
  - `merged.md:13` says: The dock booking phone number no longer connects.
  - `source_b.md` says: 'call the dock booking line on extension 2140' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source A says the number no longer connects, but source B directs callers to a working line where the supervisor takes requests.
- **M-011** -- the two documents disagree
  - `merged.md:13` says: All dock bookings go through the facilities portal.
  - `source_b.md` says: 'call the dock booking line on extension 2140' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source A says all bookings go through the portal, but source B allows phone bookings entered by the dock supervisor when the portal is down.
- **M-012** -- the two documents disagree
  - `merged.md:13` says: Drivers who call the old dock booking phone number hear a recorded message pointing them at the facilities portal.
  - `source_b.md` says: 'call the dock booking line on extension 2140' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source A describes a recorded message on a dead line, but source B says calls reach a supervisor who enters the slot, which is incompatible.

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
| 1 | All deliveries need a dock slot. | 5 | carried | 'All deliveries need a dock slot.' in `merged.md` -- The reference text states this verbatim. |
| 2 | Dock slots are booked through the facilities portal. | 5 | carried | 'Book slots through the facilities portal.' in `merged.md` -- The reference text states that slots are booked through the facilities portal. |
| 3 | A dock slot is 45 minutes. | 6 | carried | 'A slot is 45 minutes.' in `merged.md` -- The reference text states the slot length as 45 minutes. |
| 4 | A vehicle over 7.5 tonnes needs two consecutive dock slots. | 6 | carried | 'A vehicle over 7.5 tonnes needs two consecutive slots' in `merged.md` -- The reference text states this requirement directly. |
| 5 | The facilities portal will not let you book the two consecutive slots for a vehicle over 7.5 tonnes separately. | 7 | carried | 'the portal will not let you book them separately' in `merged.md` -- The reference text states the portal will not allow the two slots to be booked separately. |
| 6 | Dock slots open 14 days ahead. | 11 | carried | 'Slots open 14 days ahead' in `merged.md` -- The reference text states slots open 14 days ahead. |
| 7 | Dock slots close 4 hours before the slot starts. | 11 | carried | 'close 4 hours before the slot starts' in `merged.md` -- The reference text states slots close 4 hours before the slot starts. |
| 8 | There is no same-hour dock booking. | 11 | carried | 'There is no same-hour booking.' in `merged.md` -- The reference text states there is no same-hour booking. |
| 9 | The dock booking phone line was retired. | 16 | carried | 'The dock booking phone line was retired' in `merged.md` -- The reference text states the phone line was retired. |
| 10 | The dock booking phone number no longer connects. | 16 | carried | 'the number no longer connects' in `merged.md` -- The reference text states the number no longer connects. |
| 11 | All dock bookings go through the portal. | 16 | carried | 'All bookings go through the portal.' in `merged.md` -- The reference text states all bookings go through the portal. |
| 12 | Drivers who call the old dock booking number hear a recorded message pointing them at the portal. | 17 | carried | 'Drivers who call the old number hear a recorded message pointing them at the portal.' in `merged.md` -- The reference text states this directly. |
| 13 | Drivers report to the gatehouse with the booking reference. | 22 | carried | 'Drivers report to the gatehouse with the booking reference.' in `merged.md` -- The reference text states this verbatim. |
| 14 | The gatehouse checks the booking reference against the day sheet. | 22 | carried | 'The gatehouse checks the reference against the day sheet' in `merged.md` -- The reference text states the gatehouse checks the reference against the day sheet. |
| 15 | The gatehouse directs the vehicle to a bay. | 22 | carried | 'directs the vehicle to a bay' in `merged.md` -- The reference text states the gatehouse directs the vehicle to a bay. |
| 16 | A driver without a booking reference waits in the holding area until a slot is free. | 23 | carried | 'A driver without a reference waits in the holding area until a slot is free.' in `merged.md` -- The reference text states this directly. |
| 17 | A vehicle still on the bay 15 minutes after its slot ends is logged as an overrun. | 28 | carried | 'A vehicle still on the bay 15 minutes after its slot ends is logged as an overrun.' in `merged.md` -- The reference text states this verbatim. |
| 18 | After three overruns in a quarter, the supplier is asked to rebook through their account manager. | 29 | carried | 'After three overruns in a quarter, the supplier is asked to rebook through their account manager.' in `merged.md` -- The reference text states this verbatim. |

### `source_b.md` -- 14 claim(s): 0 dropped, 4 contradicted, 0 carried in part, 10 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 7 | If the portal is down, the dock booking line can be called on extension 2140. | 14 | contradicted | 'The dock booking phone line was retired and the number no longer connects.' in `merged.md` -- The reference text says the phone line was retired and all bookings go through the portal, which is incompatible with calling the line as a fallback. |
| 8 | If the portal is down, the dock supervisor will enter the slot for the caller. | 14 | contradicted | 'The dock booking phone line was retired and the number no longer connects.' in `merged.md` -- The reference says the phone line is retired and all bookings go through the portal, which rules out a supervisor taking callers' bookings. |
| 9 | Phone requests for dock slots are taken between 08:00 and 16:00. | 15 | contradicted | 'The dock booking phone line was retired and the number no longer connects.' in `merged.md` -- The reference states the phone line no longer connects, so phone requests are not taken during any hours. |
| 10 | Phone requests for dock slots are taken on working days only. | 15 | contradicted | 'The dock booking phone line was retired and the number no longer connects.' in `merged.md` -- The phone line is retired, so phone requests are not taken on working days or any other days. |
| 1 | Every delivery needs a dock slot. | 5 | carried | 'All deliveries need a dock slot.' in `merged.md` -- Every delivery and all deliveries have the same meaning. |
| 2 | Dock slots are requested through the facilities portal. | 5 | carried | 'Book slots through the facilities portal.' in `merged.md` -- Requesting and booking slots through the portal have the same meaning here. |
| 3 | A dock slot is 45 minutes long. | 5 | carried | 'A slot is 45 minutes.' in `merged.md` -- The reference text states the slot length as 45 minutes. |
| 4 | Vehicles over 7.5 tonnes need two consecutive dock slots. | 6 | carried | 'A vehicle over 7.5 tonnes needs two consecutive slots' in `merged.md` -- The reference text states this requirement directly. |
| 5 | Dock slots open 14 days ahead. | 10 | carried | 'Slots open 14 days ahead' in `merged.md` -- The reference text states slots open 14 days ahead. |
| 6 | Dock slots close 4 hours before the slot starts. | 10 | carried | 'close 4 hours before the slot starts' in `merged.md` -- The reference text states slots close 4 hours before the slot starts. |
| 11 | Drivers report to the gatehouse. | 20 | carried | 'Drivers report to the gatehouse with the booking reference.' in `merged.md` -- The reference directly states that drivers report to the gatehouse. |
| 12 | Drivers give the booking reference at the gatehouse. | 20 | carried | 'Drivers report to the gatehouse with the booking reference.' in `merged.md` -- Drivers bring the booking reference to the gatehouse, where it is checked against the day sheet. |
| 13 | Drivers without a booking reference wait in the holding area. | 20 | carried | 'A driver without a reference waits in the holding area until a slot is free.' in `merged.md` -- The reference states that drivers without a reference wait in the holding area. |
| 14 | A vehicle still on the bay 15 minutes after its slot ends is logged as an overrun. | 25 | carried | 'A vehicle still on the bay 15 minutes after its slot ends is logged as an overrun.' in `merged.md` -- The reference states the claim verbatim. |

### `merged.md` -- 18 claim(s): 0 invented, 4 contradicted, 0 supported in part, 14 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 9 | The dock booking phone line was retired. | contradicted | `source_b.md` | 'call the dock booking line on extension 2140' in `source_b.md` -- Source A says the phone line was retired, but source B says it is in service on extension 2140; the claim picks one side without reporting the conflict. |
| 10 | The dock booking phone number no longer connects. | contradicted | `source_b.md` | 'call the dock booking line on extension 2140' in `source_b.md` -- Source A says the number no longer connects, but source B directs callers to a working line where the supervisor takes requests. |
| 11 | All dock bookings go through the facilities portal. | contradicted | `source_b.md` | 'call the dock booking line on extension 2140' in `source_b.md` -- Source A says all bookings go through the portal, but source B allows phone bookings entered by the dock supervisor when the portal is down. |
| 12 | Drivers who call the old dock booking phone number hear a recorded message pointing them at the facilities portal. | contradicted | `source_b.md` | 'call the dock booking line on extension 2140' in `source_b.md` -- Source A describes a recorded message on a dead line, but source B says calls reach a supervisor who enters the slot, which is incompatible. |
| 1 | All deliveries need a dock slot. | supported | `source_a.md` | 'All deliveries need a dock slot.' in `source_a.md` -- Source A states this verbatim. |
| 2 | Dock slots are booked through the facilities portal. | supported | `source_a.md` | 'Book slots through the facilities portal.' in `source_a.md` -- Source A states that slots are booked through the facilities portal. |
| 3 | A dock slot is 45 minutes. | supported | `source_a.md` | 'A\nslot is 45 minutes.' in `source_a.md` -- Source A states that a slot is 45 minutes. |
| 4 | A vehicle over 7.5 tonnes needs two consecutive dock slots. | supported | `source_b.md` | 'Vehicles over 7.5 tonnes need two consecutive slots.' in `source_b.md` -- Both sources state this, and source B is the one quoted. |
| 5 | The facilities portal will not let you book the two consecutive slots for a vehicle over 7.5 tonnes separately. | supported | `source_a.md` | 'the portal will not let you book them separately.' in `source_a.md` -- Source A states the portal will not allow the two slots to be booked separately. |
| 6 | Dock slots open 14 days ahead. | supported | `source_a.md` | 'Slots open 14 days ahead' in `source_a.md` -- Source A states slots open 14 days ahead. |
| 7 | Dock slots close 4 hours before the slot starts. | supported | `source_a.md` | 'close 4 hours before the slot starts' in `source_a.md` -- Source A states slots close 4 hours before the slot starts. |
| 8 | There is no same-hour dock booking. | supported | `source_a.md` | 'There is no\nsame-hour booking.' in `source_a.md` -- Source A states there is no same-hour booking. |
| 13 | Drivers report to the gatehouse with the booking reference. | supported | `source_a.md` | 'Drivers report to the gatehouse with the booking reference.' in `source_a.md` -- Source A states this verbatim. |
| 14 | The gatehouse checks the booking reference against the day sheet. | supported | `source_a.md` | 'The gatehouse checks\nthe reference against the day sheet' in `source_a.md` -- Source A states the gatehouse checks the reference against the day sheet. |
| 15 | The gatehouse directs the vehicle to a bay. | supported | `source_a.md` | 'directs the vehicle to a bay' in `source_a.md` -- Source A states the gatehouse directs the vehicle to a bay. |
| 16 | A driver without a booking reference waits in the holding area until a slot is free. | supported | `source_a.md` | 'A driver\nwithout a reference waits in the holding area until a slot is free.' in `source_a.md` -- Source A states this. |
| 17 | A vehicle still on the bay 15 minutes after its slot ends is logged as an overrun. | supported | `source_b.md` | 'A vehicle still on the bay 15 minutes after its slot ends is logged as an\noverrun.' in `source_b.md` -- Both sources state this, and source B is the one quoted. |
| 18 | After three overruns in a quarter, the supplier is asked to rebook through their account manager. | supported | `source_a.md` | 'Three overruns in a quarter and the supplier is asked to rebook through\ntheir account manager.' in `source_a.md` -- Source A states this. |

## Structure

**9** mechanical check(s) over **36** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **18** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **32**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 1 run(s) over 18 attributed segment(s) — not conclusive on this evidence base. 6 of 12 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

No structural finding.

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **25** departure(s) from its sources. Checking them confirms 20, rejects 0, and leaves 5 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 36 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a5` | reworded | Slot length: line break joined into prose. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-003`) |
| `a6` | reworded | Heavy vehicle rule: line break joined, comma added. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-004`, `A-005`) |
| `a9` | reworded | Booking window: line break joined into prose. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-008`) |
| `a12` | reworded | Phone section: line break joined into prose. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-011`) |
| `a13` | reworded | Phone section: line break joined into prose. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-012`) |
| `a16` | reworded | Arriving: line break joined into prose. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-014`, `A-015`) |
| `a17` | reworded | Arriving: line break joined into prose. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-016`) |
| `a19` | reworded | Overrun definition: line break joined into prose. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-017`) |
| `a20` | reworded | Overrun penalty: sentence smoothed, line break joined. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-018`) |
| `b1` | superseded | Title: base title kept. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Loading Dock Booking - Standard Operating Procedure' and says so (no claim traced to it) |
| `b2` | superseded | Section heading: base heading kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b3` | duplicate | Same fact as a3. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-001`) |
| `b4` | duplicate | Same fact as a4. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-002`) |
| `b5` | duplicate | Same fact as a5. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-003`) |
| `b6` | subsumed | Heavy vehicle rule carried in a6's fuller sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-004`) |
| `b7` | superseded | Section heading: base heading kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b8` | duplicate | Same fact as a8. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-005`, `B-006`) |
| `b9` | superseded | Phone section: base's retired-line version chosen. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b10` | superseded | Phone booking conflicts with retired line; base chosen. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-007`, `B-008`) |
| `b11` | superseded | Phone hours moot since line is retired; base chosen. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-009`, `B-010`) |
| `b12` | superseded | Section heading: base heading kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b13` | duplicate | Same fact as a15. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-011`, `B-012`) |
| `b14` | subsumed | Carried in a17's fuller sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-013`) |
| `b15` | superseded | Section heading: base heading kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b16` | duplicate | Same fact as a19. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-014`) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | ec0c9ecb43e3 (hosted) |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | claude-opus-5-5 |
| Model (decompose) | claude-opus-5-5 |
| Model (verify) | claude-opus-5-5 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile anthropic |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 7 live, 0 cached, 0 replayed |
| Tokens | 22,150 in, 11,367 out |
| Cost | ~$0.32 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 92.5s |
| Generated | 2026-09-27T16:18:22+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
