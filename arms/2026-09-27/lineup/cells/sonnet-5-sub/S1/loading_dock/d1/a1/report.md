## Verdict

**7 finding(s).** In the claims: 7 contradicted.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 18 |
| Claims extracted from `source_a.md` | 18 |
| Claims extracted from `source_b.md` | 12 |
| Forward — source claims accounted for in the merge | **27/30** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **18/18** |
| Forward — `source_b.md` claims accounted for | **9/12** |
| Reverse — merge claims found in a source | **14/18** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **48/48** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **B-007** -- the two documents disagree
  - `source_b.md:14` says: If the portal is down, one can call the dock booking line on extension 2140.
  - `merged.md` says: 'The dock booking phone line was retired and the number no longer connects.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states the phone line was retired and no longer connects, contradicting the claim that one can call an extension if the portal is down.
- **B-008** -- the two documents disagree
  - `source_b.md:14` says: The dock supervisor will enter the slot for a caller if the portal is down.
  - `merged.md` says: 'The dock booking phone line was retired and the number no longer connects. All bookings go through the portal.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The phone line is retired and all bookings go through the portal, contradicting any claim of a dock supervisor entering slots via phone.
- **B-009** -- the two documents disagree
  - `source_b.md:15` says: Phone requests are taken between 08:00 and 16:00 on working days only.
  - `merged.md` says: 'The dock booking phone line was retired and the number no longer connects.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Since the phone line is retired entirely, the claim of specific phone request hours is incompatible with the text.
- **M-009** -- the two documents disagree
  - `merged.md:13` says: The dock booking phone line was retired.
  - `source_b.md` says: 'If the portal is down, call the dock booking line on extension 2140 and the dock supervisor will enter the slot for you.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source_b describes the dock booking phone line as active and in use, contradicting source_a's claim that it was retired.
- **M-010** -- the two documents disagree
  - `merged.md:13` says: The dock booking phone number no longer connects.
  - `source_b.md` says: 'If the portal is down, call the dock booking line on extension 2140 and the dock supervisor will enter the slot for you.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source_b shows the number connects and is answered by a supervisor, contradicting the claim that it no longer connects.
- **M-011** -- the two documents disagree
  - `merged.md:13` says: All bookings go through the portal.
  - `source_b.md` says: 'Phone requests are taken between 08:00 and 16:00 on working days only.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source_b describes a valid phone booking channel, contradicting the claim that all bookings go through the portal.
- **M-012** -- the two documents disagree
  - `merged.md:13` says: Drivers who call the old dock booking phone number hear a recorded message pointing them at the portal.
  - `source_b.md` says: 'If the portal is down, call the dock booking line on extension 2140 and the dock supervisor will enter the slot for you.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source_b indicates the line is live and staffed rather than playing a recorded message, contradicting source_a's claim on this same phone line.

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
| 1 | All deliveries need a dock slot. | 5 | carried | 'All deliveries need a dock slot.' in `merged.md` -- Directly stated. |
| 2 | Slots are booked through the facilities portal. | 5 | carried | 'Book slots through the facilities portal.' in `merged.md` -- Directly stated. |
| 3 | A slot is 45 minutes. | 5 | carried | 'A slot is 45 minutes.' in `merged.md` -- Directly stated. |
| 4 | A vehicle over 7.5 tonnes needs two consecutive slots. | 6 | carried | 'A vehicle over 7.5 tonnes needs two consecutive slots' in `merged.md` -- Directly stated. |
| 5 | The portal will not let you book two consecutive slots separately. | 7 | carried | 'and the portal will not let you book them separately.' in `merged.md` -- Directly stated. |
| 6 | Slots open 14 days ahead. | 11 | carried | 'Slots open 14 days ahead' in `merged.md` -- Directly stated. |
| 7 | Slots close 4 hours before the slot starts. | 11 | carried | 'and close 4 hours before the slot starts.' in `merged.md` -- Directly stated. |
| 8 | There is no same-hour booking. | 11 | carried | 'There is no same-hour booking.' in `merged.md` -- Directly stated. |
| 9 | The dock booking phone line was retired. | 16 | carried | 'The dock booking phone line was retired' in `merged.md` -- Directly stated. |
| 10 | The dock booking phone number no longer connects. | 16 | carried | 'and the number no longer connects.' in `merged.md` -- Directly stated. |
| 11 | All bookings go through the portal. | 16 | carried | 'All bookings go through the portal.' in `merged.md` -- Directly stated. |
| 12 | Drivers who call the old number hear a recorded message pointing them at the portal. | 17 | carried | 'Drivers who call the old number hear a recorded message pointing them at the portal.' in `merged.md` -- Directly stated. |
| 13 | Drivers report to the gatehouse with the booking reference. | 22 | carried | 'Drivers report to the gatehouse with the booking reference.' in `merged.md` -- Directly stated. |
| 14 | The gatehouse checks the reference against the day sheet. | 22 | carried | 'The gatehouse checks the reference against the day sheet' in `merged.md` -- Directly stated. |
| 15 | The gatehouse directs the vehicle to a bay. | 23 | carried | 'and directs the vehicle to a bay.' in `merged.md` -- Directly stated. |
| 16 | A driver without a reference waits in the holding area until a slot is free. | 23 | carried | 'A driver without a reference waits in the holding area until a slot is free.' in `merged.md` -- Directly stated. |
| 17 | A vehicle still on the bay 15 minutes after its slot ends is logged as an overrun. | 28 | carried | 'A vehicle still on the bay 15 minutes after its slot ends is logged as an overrun.' in `merged.md` -- Directly stated. |
| 18 | Three overruns in a quarter results in the supplier being asked to rebook through their account manager. | 29 | carried | 'Three overruns in a quarter and the supplier is asked to rebook through their account manager.' in `merged.md` -- Directly stated. |

### `source_b.md` -- 12 claim(s): 0 dropped, 3 contradicted, 0 carried in part, 9 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 7 | If the portal is down, one can call the dock booking line on extension 2140. | 14 | contradicted | 'The dock booking phone line was retired and the number no longer connects.' in `merged.md` -- The text states the phone line was retired and no longer connects, contradicting the claim that one can call an extension if the portal is down. |
| 8 | The dock supervisor will enter the slot for a caller if the portal is down. | 14 | contradicted | 'The dock booking phone line was retired and the number no longer connects. All bookings go through the portal.' in `merged.md` -- The phone line is retired and all bookings go through the portal, contradicting any claim of a dock supervisor entering slots via phone. |
| 9 | Phone requests are taken between 08:00 and 16:00 on working days only. | 15 | contradicted | 'The dock booking phone line was retired and the number no longer connects.' in `merged.md` -- Since the phone line is retired entirely, the claim of specific phone request hours is incompatible with the text. |
| 1 | Every delivery needs a dock slot. | 5 | carried | 'All deliveries need a dock slot.' in `merged.md` -- 'Every delivery' and 'All deliveries' express the same meaning. |
| 2 | Slots are requested through the facilities portal. | 5 | carried | 'Book slots through the facilities portal.' in `merged.md` -- 'Requested' and 'Book' both describe obtaining a slot via the portal. |
| 3 | A slot is 45 minutes long. | 5 | carried | 'A slot is 45 minutes.' in `merged.md` -- Directly stated. |
| 4 | Vehicles over 7.5 tonnes need two consecutive slots. | 6 | carried | 'A vehicle over 7.5 tonnes needs two consecutive slots' in `merged.md` -- Directly stated, plural phrasing equivalent. |
| 5 | Slots open 14 days ahead. | 10 | carried | 'Slots open 14 days ahead' in `merged.md` -- Directly stated. |
| 6 | Slots close 4 hours before the slot starts. | 10 | carried | 'and close 4 hours before the slot starts.' in `merged.md` -- Directly stated. |
| 10 | Drivers report to the gatehouse and give the booking reference. | 20 | carried | 'Drivers report to the gatehouse with the booking reference.' in `merged.md` -- Directly stated. |
| 11 | Drivers without a reference wait in the holding area. | 20 | carried | 'A driver without a reference waits in the holding area until a slot is free.' in `merged.md` -- Directly stated, extra detail about slot availability doesn't negate the core claim. |
| 12 | A vehicle still on the bay 15 minutes after its slot ends is logged as an overrun. | 25 | carried | 'A vehicle still on the bay 15 minutes after its slot ends is logged as an overrun.' in `merged.md` -- Directly stated. |

### `merged.md` -- 18 claim(s): 0 invented, 4 contradicted, 0 supported in part, 14 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 9 | The dock booking phone line was retired. | contradicted | `source_b.md` | 'If the portal is down, call the dock booking line on extension 2140 and the dock supervisor will enter the slot for you.' in `source_b.md` -- Source_b describes the dock booking phone line as active and in use, contradicting source_a's claim that it was retired. |
| 10 | The dock booking phone number no longer connects. | contradicted | `source_b.md` | 'If the portal is down, call the dock booking line on extension 2140 and the dock supervisor will enter the slot for you.' in `source_b.md` -- Source_b shows the number connects and is answered by a supervisor, contradicting the claim that it no longer connects. |
| 11 | All bookings go through the portal. | contradicted | `source_b.md` | 'Phone requests are taken between 08:00 and 16:00 on working days only.' in `source_b.md` -- Source_b describes a valid phone booking channel, contradicting the claim that all bookings go through the portal. |
| 12 | Drivers who call the old dock booking phone number hear a recorded message pointing them at the portal. | contradicted | `source_b.md` | 'If the portal is down, call the dock booking line on extension 2140 and the dock supervisor will enter the slot for you.' in `source_b.md` -- Source_b indicates the line is live and staffed rather than playing a recorded message, contradicting source_a's claim on this same phone line. |
| 1 | All deliveries need a dock slot. | supported | `source_a.md` | 'All deliveries need a dock slot.' in `source_a.md` -- Source_a states this exactly. |
| 2 | Slots are booked through the facilities portal. | supported | `source_a.md` | 'Book slots through the facilities portal.' in `source_a.md` -- Source_a states slots are booked through the portal. |
| 3 | A slot is 45 minutes. | supported | `source_a.md` | 'A slot is 45 minutes.' in `source_a.md` -- Source_a states the slot length exactly. |
| 4 | A vehicle over 7.5 tonnes needs two consecutive slots. | supported | `source_a.md` | 'A vehicle over 7.5 tonnes needs two consecutive slots' in `source_a.md` -- Source_a states this exactly. |
| 5 | The portal will not let you book two consecutive slots separately for a vehicle over 7.5 tonnes. | supported | `source_a.md` | 'the portal will not let you book them separately.' in `source_a.md` -- Source_a states this exactly. |
| 6 | Slots open 14 days ahead. | supported | `source_a.md` | 'Slots open 14 days ahead and close 4 hours before the slot starts.' in `source_a.md` -- Source_a states the opening window. |
| 7 | Slots close 4 hours before the slot starts. | supported | `source_a.md` | 'Slots open 14 days ahead and close 4 hours before the slot starts.' in `source_a.md` -- Source_a states the closing window. |
| 8 | There is no same-hour booking. | supported | `source_a.md` | 'There is no same-hour booking.' in `source_a.md` -- Source_a states this exactly. |
| 13 | Drivers report to the gatehouse with the booking reference. | supported | `source_a.md` | 'Drivers report to the gatehouse with the booking reference.' in `source_a.md` -- Source_a states this exactly. |
| 14 | The gatehouse checks the booking reference against the day sheet. | supported | `source_a.md` | 'The gatehouse checks the reference against the day sheet' in `source_a.md` -- Source_a states this exactly. |
| 15 | The gatehouse directs the vehicle to a bay. | supported | `source_a.md` | 'directs the vehicle to a bay.' in `source_a.md` -- Source_a states this exactly. |
| 16 | A driver without a booking reference waits in the holding area until a slot is free. | supported | `source_a.md` | 'A driver without a reference waits in the holding area until a slot is free.' in `source_a.md` -- Source_a states this exactly. |
| 17 | A vehicle still on the bay 15 minutes after its slot ends is logged as an overrun. | supported | `source_a.md` | 'A vehicle still on the bay 15 minutes after its slot ends is logged as an\noverrun.' in `source_a.md` -- Both sources state this overrun rule identically. |
| 18 | Three overruns in a quarter results in the supplier being asked to rebook through their account manager. | supported | `source_a.md` | 'Three overruns in a quarter and the supplier is asked to rebook through their account manager.' in `source_a.md` -- Source_a states this exactly. |

## Structure

**9** mechanical check(s) over **36** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **18** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **30**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 1 run(s) over 18 attributed segment(s) — not conclusive on this evidence base. 6 of 12 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

No structural finding.

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **16** departure(s) from its sources. Checking them confirms 10, rejects 5, and leaves 1 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 1 of 36 source segment(s) declared gone, **2.8%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | Base title chosen over this one. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Loading Dock Booking - Standard Operating Procedure' and says so (no claim traced to it) |
| `b2` | duplicate | Same section heading purpose as a2. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b3` | duplicate | Same fact as a3. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-001`) |
| `b4` | superseded | Same instruction, a4's wording kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-002`) |
| `b5` | superseded | Same fact, a5's wording kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-003`) |
| `b6` | subsumed | a6 already carries this fact plus more detail. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-004`) |
| `b7` | duplicate | Same section heading purpose as a7. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b8` | duplicate | Identical fact to a8. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-005`, `B-006`) |
| `b9` | superseded | Section replaced by base's current phone-line status. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b10` | superseded | Contradicted by base; base's status chosen (see decision). | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-007`, `B-008`) |
| `b11` | dropped | Phone hours are moot once the line is described as retired. | **rejected** | declared 'dropped', which predicts MISSING; B-009 came back CONTRADICTED (`B-009`) |
| `b12` | duplicate | Same section heading purpose as a14. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b13` | subsumed | Same fact as a15, one wording kept. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-010`) |
| `b14` | subsumed | Same fact as a17, one wording kept. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-011`) |
| `b15` | duplicate | Same section heading purpose as a18. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b16` | duplicate | Identical text to a19. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-012`) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | d320da0eb7ed (command) -- lineup sonnet-5-sub |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | claude-sonnet-5 -> claude-sonnet-5 |
| Model (decompose) | claude-sonnet-5 -> claude-sonnet-5 |
| Model (verify) | claude-sonnet-5 -> claude-sonnet-5 |
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
| Duration | 201.7s |
| Generated | 2026-09-27T17:08:28+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup sonnet-5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
