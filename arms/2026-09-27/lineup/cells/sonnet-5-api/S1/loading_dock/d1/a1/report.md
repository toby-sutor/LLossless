## Verdict

**7 finding(s).** In the claims: 1 dropped, 6 contradicted.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 18 |
| Claims extracted from `source_a.md` | 18 |
| Claims extracted from `source_b.md` | 13 |
| Forward — source claims accounted for in the merge | **28/31** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **18/18** |
| Forward — `source_b.md` claims accounted for | **10/13** |
| Reverse — merge claims found in a source | **14/18** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **47/48** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Dropped — in a source, not in the merge

- **B-008** (`source_b.md:14`) — If the portal is down, the dock supervisor will enter the slot for you.
  - judged against: `merged.md`
  - rationale: The reference text does not mention any fallback procedure for portal downtime.

### Contradicted — the merge states something different

- **B-007** -- the two documents disagree
  - `source_b.md:14` says: If the portal is down, the dock booking line can be called on extension 2140.
  - `merged.md` says: 'The dock booking phone line was retired and the number no longer connects. All bookings go through the portal.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states the phone line is retired and no longer connects, contradicting the claim that a working extension exists as a fallback.
- **B-009** -- the two documents disagree
  - `source_b.md:15` says: Phone requests are taken between 08:00 and 16:00 on working days only.
  - `merged.md` says: 'The dock booking phone line was retired and the number no longer connects.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states the phone line is retired and no longer connects, incompatible with phone requests being taken at all.
- **M-009** -- the two documents disagree
  - `merged.md:13` says: The dock booking phone line was retired.
  - `source_b.md` says: 'call the dock booking line on extension 2140 and the dock supervisor will enter the slot for you' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source_b describes an active dock booking phone line, contradicting source_a's claim that the line was retired.
- **M-010** -- the two documents disagree
  - `merged.md:13` says: The dock booking phone number no longer connects.
  - `source_b.md` says: 'call the dock booking line on extension 2140 and the dock supervisor will enter the slot for you' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source_b shows the phone line is functional and connects to a supervisor, contradicting the claim that the number no longer connects.
- **M-011** -- the two documents disagree
  - `merged.md:13` says: All bookings go through the portal.
  - `source_b.md` says: 'call the dock booking line on extension 2140 and the dock supervisor will enter the slot for you' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source_b allows phone-based bookings entered by a supervisor, contradicting the claim that all bookings go through the portal.
- **M-012** -- the two documents disagree
  - `merged.md:13` says: Drivers who call the old dock booking phone number hear a recorded message pointing them at the portal.
  - `source_b.md` says: 'call the dock booking line on extension 2140 and the dock supervisor will enter the slot for you' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source_b states callers reach a live supervisor, not a recorded message directing them to the portal.

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
| 1 | All deliveries need a dock slot. | 5 | carried | 'All deliveries need a dock slot.' in `merged.md` -- Directly stated in the text. |
| 2 | Slots are booked through the facilities portal. | 5 | carried | 'Book slots through the facilities portal.' in `merged.md` -- Directly stated in the text. |
| 3 | A slot is 45 minutes. | 5 | carried | 'A slot is 45 minutes.' in `merged.md` -- Directly stated in the text. |
| 4 | A vehicle over 7.5 tonnes needs two consecutive slots. | 6 | carried | 'A vehicle over 7.5 tonnes needs two consecutive slots' in `merged.md` -- Directly stated in the text. |
| 5 | The portal will not let you book two consecutive slots separately. | 7 | carried | 'the portal will not let you book them separately' in `merged.md` -- The text states the portal prevents booking the two consecutive slots separately. |
| 6 | Slots open 14 days ahead. | 11 | carried | 'Slots open 14 days ahead' in `merged.md` -- Directly stated in the text. |
| 7 | Slots close 4 hours before the slot starts. | 11 | carried | 'close 4 hours before the slot starts' in `merged.md` -- Directly stated in the text. |
| 8 | There is no same-hour booking. | 11 | carried | 'There is no same-hour booking.' in `merged.md` -- Directly stated in the text. |
| 9 | The dock booking phone line was retired. | 16 | carried | 'The dock booking phone line was retired' in `merged.md` -- Directly stated in the text. |
| 10 | The dock booking phone number no longer connects. | 16 | carried | 'the number no longer connects' in `merged.md` -- Directly stated in the text. |
| 11 | All bookings go through the portal. | 16 | carried | 'All bookings go through the portal.' in `merged.md` -- Directly stated in the text. |
| 12 | Drivers who call the old dock booking phone number hear a recorded message pointing them at the portal. | 17 | carried | 'Drivers who call the old number hear a recorded message pointing them at the portal.' in `merged.md` -- Directly stated in the text. |
| 13 | Drivers report to the gatehouse with the booking reference. | 22 | carried | 'Drivers report to the gatehouse with the booking reference.' in `merged.md` -- Directly stated in the text. |
| 14 | The gatehouse checks the reference against the day sheet. | 22 | carried | 'The gatehouse checks the reference against the day sheet' in `merged.md` -- Directly stated in the text. |
| 15 | The gatehouse directs the vehicle to a bay. | 23 | carried | 'directs the vehicle to a bay' in `merged.md` -- Directly stated in the text. |
| 16 | A driver without a reference waits in the holding area until a slot is free. | 23 | carried | 'A driver without a reference waits in the holding area until a slot is free.' in `merged.md` -- Directly stated in the text. |
| 17 | A vehicle still on the bay 15 minutes after its slot ends is logged as an overrun. | 28 | carried | 'A vehicle still on the bay 15 minutes after its slot ends is logged as an overrun.' in `merged.md` -- Directly stated in the text. |
| 18 | Three overruns in a quarter results in the supplier being asked to rebook through their account manager. | 29 | carried | 'Three overruns in a quarter and the supplier is asked to rebook through their account manager.' in `merged.md` -- Directly stated in the text. |

### `source_b.md` -- 13 claim(s): 1 dropped, 2 contradicted, 0 carried in part, 10 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 8 | If the portal is down, the dock supervisor will enter the slot for you. | 14 | dropped | The reference text does not mention any fallback procedure for portal downtime. |
| 7 | If the portal is down, the dock booking line can be called on extension 2140. | 14 | contradicted | 'The dock booking phone line was retired and the number no longer connects. All bookings go through the portal.' in `merged.md` -- The text states the phone line is retired and no longer connects, contradicting the claim that a working extension exists as a fallback. |
| 9 | Phone requests are taken between 08:00 and 16:00 on working days only. | 15 | contradicted | 'The dock booking phone line was retired and the number no longer connects.' in `merged.md` -- The text states the phone line is retired and no longer connects, incompatible with phone requests being taken at all. |
| 1 | Every delivery needs a dock slot. | 5 | carried | 'All deliveries need a dock slot.' in `merged.md` -- Paraphrase of the same fact stated in the text. |
| 2 | Slots must be requested through the facilities portal. | 5 | carried | 'Book slots through the facilities portal.' in `merged.md` -- Paraphrase of the same fact stated in the text. |
| 3 | A slot is 45 minutes long. | 5 | carried | 'A slot is 45 minutes.' in `merged.md` -- Directly stated in the text. |
| 4 | Vehicles over 7.5 tonnes need two consecutive slots. | 6 | carried | 'A vehicle over 7.5 tonnes needs two consecutive slots' in `merged.md` -- Directly stated in the text. |
| 5 | Slots open 14 days ahead. | 10 | carried | 'Slots open 14 days ahead' in `merged.md` -- Directly stated in the text. |
| 6 | Slots close 4 hours before the slot starts. | 10 | carried | 'close 4 hours before the slot starts' in `merged.md` -- Directly stated in the text. |
| 10 | Drivers report to the gatehouse. | 20 | carried | 'Drivers report to the gatehouse with the booking reference.' in `merged.md` -- Directly stated in the text. |
| 11 | Drivers give the booking reference. | 20 | carried | 'Drivers report to the gatehouse with the booking reference.' in `merged.md` -- The text states drivers report with the booking reference, entailing they give it. |
| 12 | Drivers without a reference wait in the holding area. | 20 | carried | 'A driver without a reference waits in the holding area until a slot is free.' in `merged.md` -- Directly stated in the text. |
| 13 | A vehicle still on the bay 15 minutes after its slot ends is logged as an overrun. | 25 | carried | 'A vehicle still on the bay 15 minutes after its slot ends is logged as an overrun.' in `merged.md` -- Directly stated verbatim in the text. |

### `merged.md` -- 18 claim(s): 0 invented, 4 contradicted, 0 supported in part, 14 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 9 | The dock booking phone line was retired. | contradicted | `source_b.md` | 'call the dock booking line on extension 2140 and the dock supervisor will enter the slot for you' in `source_b.md` -- Source_b describes an active dock booking phone line, contradicting source_a's claim that the line was retired. |
| 10 | The dock booking phone number no longer connects. | contradicted | `source_b.md` | 'call the dock booking line on extension 2140 and the dock supervisor will enter the slot for you' in `source_b.md` -- Source_b shows the phone line is functional and connects to a supervisor, contradicting the claim that the number no longer connects. |
| 11 | All bookings go through the portal. | contradicted | `source_b.md` | 'call the dock booking line on extension 2140 and the dock supervisor will enter the slot for you' in `source_b.md` -- Source_b allows phone-based bookings entered by a supervisor, contradicting the claim that all bookings go through the portal. |
| 12 | Drivers who call the old dock booking phone number hear a recorded message pointing them at the portal. | contradicted | `source_b.md` | 'call the dock booking line on extension 2140 and the dock supervisor will enter the slot for you' in `source_b.md` -- Source_b states callers reach a live supervisor, not a recorded message directing them to the portal. |
| 1 | All deliveries need a dock slot. | supported | `source_a.md` | 'All deliveries need a dock slot.' in `source_a.md` -- This is stated verbatim in source_a. |
| 2 | Slots are booked through the facilities portal. | supported | `source_a.md` | 'Book slots through the facilities portal.' in `source_a.md` -- Source_a states slots are booked through the facilities portal. |
| 3 | A slot is 45 minutes. | supported | `source_a.md` | 'A slot is 45 minutes.' in `source_a.md` -- Source_a states the slot length directly. |
| 4 | A vehicle over 7.5 tonnes needs two consecutive slots. | supported | `source_a.md` | 'A vehicle over 7.5 tonnes needs two consecutive slots' in `source_a.md` -- Source_a directly states this requirement. |
| 5 | The portal will not let you book two consecutive slots separately for a vehicle over 7.5 tonnes. | supported | `source_a.md` | 'the portal will not let you book them separately.' in `source_a.md` -- Source_a states this restriction on the portal explicitly. |
| 6 | Slots open 14 days ahead. | supported | `source_a.md` | 'Slots open 14 days ahead' in `source_a.md` -- Source_a states the booking window opening period. |
| 7 | Slots close 4 hours before the slot starts. | supported | `source_a.md` | 'close 4 hours before the slot starts.' in `source_a.md` -- Source_a states the closing window before the slot. |
| 8 | There is no same-hour booking. | supported | `source_a.md` | 'There is no same-hour booking.' in `source_a.md` -- Source_a states this directly. |
| 13 | Drivers report to the gatehouse with the booking reference. | supported | `source_a.md` | 'Drivers report to the gatehouse with the booking reference.' in `source_a.md` -- Source_a states this directly. |
| 14 | The gatehouse checks the booking reference against the day sheet. | supported | `source_a.md` | 'The gatehouse checks the reference against the day sheet.' in `source_a.md`, **transcription_error** -- Source_a states this directly. |
| 15 | The gatehouse directs the vehicle to a bay. | supported | `source_a.md` | 'directs the vehicle to a bay.' in `source_a.md` -- Source_a states this directly. |
| 16 | A driver without a reference waits in the holding area until a slot is free. | supported | `source_a.md` | 'A driver without a reference waits in the holding area until a slot is free.' in `source_a.md` -- Source_a states this directly. |
| 17 | A vehicle still on the bay 15 minutes after its slot ends is logged as an overrun. | supported | `source_a.md` | 'A vehicle still on the bay 15 minutes after its slot ends is logged as an\noverrun.' in `source_a.md` -- Both sources state this overrun rule identically. |
| 18 | Three overruns in a quarter results in the supplier being asked to rebook through their account manager. | supported | `source_a.md` | 'Three overruns in a quarter and the supplier is asked to rebook through\ntheir account manager.' in `source_a.md` -- Source_a states this consequence directly. |

## Structure

**9** mechanical check(s) over **36** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **18** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **31**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 1 run(s) over 18 attributed segment(s) — not conclusive on this evidence base. 6 of 12 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

No structural finding.

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **16** departure(s) from its sources. Checking them confirms 10, rejects 1, and leaves 5 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 36 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | Base title chosen over source_b's title. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Loading Dock Booking - Standard Operating Procedure' and says so (no claim traced to it) |
| `b2` | superseded | Base heading kept for consolidated section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b3` | superseded | Same fact as a3, base wording kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-001`) |
| `b4` | superseded | Same fact as a4, base wording kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-002`) |
| `b5` | superseded | Same fact as a5, base wording kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-003`) |
| `b6` | subsumed | Fact already covered, with extra detail, by a6. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-004`) |
| `b7` | superseded | Base heading kept for consolidated section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b8` | duplicate | Identical statement to a8. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-005`, `B-006`) |
| `b9` | superseded | Base heading chosen, describing line as closed. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b10` | superseded | Disagreement resolved in favour of base's retired-line account. | **rejected** | declared 'superseded', which predicts SUPPORTED or CONTRADICTED or PARTIAL; B-008 came back MISSING (`B-008`) |
| `b11` | superseded | Phone-line hours no longer apply once line is retired. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-009`) |
| `b12` | superseded | Base heading kept for consolidated section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b13` | superseded | Same fact as a15, base wording kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-010`, `B-011`) |
| `b14` | superseded | Same fact as a17, base wording kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-012`) |
| `b15` | superseded | Base heading kept for consolidated section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b16` | duplicate | Identical statement to a19. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-013`) |


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
| Calls | 8 live, 0 cached, 0 replayed |
| Tokens | 25,490 in, 22,545 out |
| Cost | ~$0.28 estimated (rates read 2026-08-31) |
| Schema repairs | 1 |
| Errors | 0 |
| Duration | 179.8s |
| Generated | 2026-09-27T16:21:22+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
