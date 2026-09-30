## Verdict

**6 finding(s).** In the claims: 5 partially dropped, 1 contradicted.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 25 |
| Claims extracted from `source_a.md` | 16 |
| Claims extracted from `source_b.md` | 14 |
| Forward — source claims accounted for in the merge | **24/30** |
| Forward — carried only in part | 5 |
| Forward — `source_a.md` claims accounted for | **16/16** |
| Forward — `source_b.md` claims accounted for | **8/14** (5 in part) |
| Reverse — merge claims found in a source | **25/25** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **55/55** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Partly dropped — the merge carries some of this claim

- **B-005** (`source_b.md:10`) — The support desk asks the rider to read the code on the dock display.
  - evidence: 'Ask the rider to read the code on the dock display.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The instruction to ask the rider is stated, but it does not identify the support desk as the person asking.
- **B-008** (`source_b.md:15`) — The support desk raises an E2 to the field crew.
  - evidence: 'Raise an E2 to the field crew.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text specifies raising E2 to the field crew but does not say the support desk does it.
- **B-010** (`source_b.md:20`) — The support desk raises an E4 to the electrical contractor the same day.
  - evidence: 'Report E4 to the electrical contractor the same day.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The same-day report is stated, but the text does not say the support desk makes it.
- **B-012** (`source_b.md:25`) — The support desk refunds the journey at the time of the call.
  - evidence: 'Refund at the time of the call' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The timing is stated, but the text does not identify the support desk as the party issuing the refund.
- **B-013** (`source_b.md:25`) — The support desk does not wait for the fault to be confirmed before refunding the journey.
  - evidence: 'do not wait for the fault to be confirmed.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text says not to wait for confirmation before refunding, but does not assign that action to the support desk.

### Contradicted — the merge states something different

- **B-009** -- the two documents disagree
  - `source_b.md:15` says: If the field crew have already tried 3 times, the support desk raises an E2 to the workshop instead.
  - `merged.md` says: 'Escalate E2 to the workshop after 2 failed attempts.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text sets the workshop escalation threshold at 2 failed attempts, not 3.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 16 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 16 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | A dock showing E2 has a jammed locking pin. | 5 | carried | 'A dock showing E2 has a jammed locking pin.' in `merged.md` -- The text states the claim directly. |
| 2 | A dock showing E4 has lost power to the point. | 5 | carried | 'A dock showing E4 has lost power to the point.' in `merged.md` -- The text states the claim directly. |
| 3 | E2 is a mechanical fault. | 6 | carried | 'E2 is a mechanical fault' in `merged.md` -- The text identifies E2 as a mechanical fault. |
| 4 | E4 is an electrical fault. | 6 | carried | 'E4 is an electrical one' in `merged.md` -- In context, “electrical one” means an electrical fault. |
| 5 | E2 and E4 are escalated differently. | 6 | carried | 'E2 is a mechanical fault and E4 is an electrical one, and they are escalated differently.' in `merged.md` -- The text explicitly says they are escalated differently. |
| 6 | The pin of a dock showing E2 is freed with the service key. | 11 | carried | '## Clearing E2 in the field\n\nFree the pin with the service key' in `merged.md` -- The E2 clearing instructions specify freeing the pin with the service key. |
| 7 | A dock showing E2 is cycled twice. | 11 | carried | '## Clearing E2 in the field\n\nFree the pin with the service key and cycle the dock twice.' in `merged.md` -- The E2 clearing instructions say to cycle the dock twice. |
| 8 | If a dock takes a bike and releases it on both cycles, the fault is closed on the field crew member's handheld. | 11 | carried | 'If the dock takes a bike and releases it on both cycles, close the fault on your handheld.' in `merged.md` -- The text gives that condition and directs the worker to close the fault on their handheld. |
| 9 | E2 is escalated to the workshop after 2 failed attempts. | 16 | carried | 'Escalate E2 to the workshop after 2 failed attempts.' in `merged.md` -- The escalation threshold and destination match the claim. |
| 10 | A dock that has failed twice must not be cycled further. | 16 | carried | 'Do not keep cycling a dock that has failed twice' in `merged.md` -- The text prohibits further cycling after two failures. |
| 11 | Repeated forcing bends the pin. | 17 | carried | 'repeated forcing bends the pin' in `merged.md` -- The text states this consequence of repeated forcing. |
| 12 | Repeated forcing turns a 20 minute workshop job into a replacement. | 17 | carried | 'repeated forcing bends the pin and turns a 20 minute workshop job into a replacement.' in `merged.md` -- The text says repeated forcing turns the workshop job into a replacement. |
| 13 | E4 is reported to the electrical contractor the same day. | 22 | carried | 'Report E4 to the electrical contractor the same day.' in `merged.md` -- The reporting destination and timing match the claim. |
| 14 | Field crew do not open the power enclosure under any circumstances. | 22 | carried | 'Field crew do not open the power enclosure under any circumstances.' in `merged.md` -- The text states the prohibition directly. |
| 15 | A station with more than half its docks faulted is taken out of service in the app. | 27 | carried | 'The support desk takes a station out of service in the app when more than half its docks are faulted.' in `merged.md` -- The text specifies the same threshold and action. |
| 16 | The support desk is told before a station is taken out of service in the app. | 28 | carried | 'Field crew tell the support desk before the station is taken out of service, not after.' in `merged.md` -- The text requires notifying the support desk beforehand. |

### `source_b.md` -- 14 claim(s): 0 dropped, 1 contradicted, 5 carried in part, 8 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 9 | If the field crew have already tried 3 times, the support desk raises an E2 to the workshop instead. | 15 | contradicted | 'Escalate E2 to the workshop after 2 failed attempts.' in `merged.md` -- The text sets the workshop escalation threshold at 2 failed attempts, not 3. |
| 5 | The support desk asks the rider to read the code on the dock display. | 10 | carried in part | 'Ask the rider to read the code on the dock display.' in `merged.md` -- The instruction to ask the rider is stated, but it does not identify the support desk as the person asking. |
| 8 | The support desk raises an E2 to the field crew. | 15 | carried in part | 'Raise an E2 to the field crew.' in `merged.md` -- The text specifies raising E2 to the field crew but does not say the support desk does it. |
| 10 | The support desk raises an E4 to the electrical contractor the same day. | 20 | carried in part | 'Report E4 to the electrical contractor the same day.' in `merged.md` -- The same-day report is stated, but the text does not say the support desk makes it. |
| 12 | The support desk refunds the journey at the time of the call. | 25 | carried in part | 'Refund at the time of the call' in `merged.md` -- The timing is stated, but the text does not identify the support desk as the party issuing the refund. |
| 13 | The support desk does not wait for the fault to be confirmed before refunding the journey. | 25 | carried in part | 'do not wait for the fault to be confirmed.' in `merged.md` -- The text says not to wait for confirmation before refunding, but does not assign that action to the support desk. |
| 1 | Riders call about bikes that will not release. | 5 | carried | 'Riders call about bikes that will not release' in `merged.md` -- The text states that riders call about bikes that will not release. |
| 2 | Riders call about bikes that will not lock. | 5 | carried | 'Riders call about bikes that will not release and bikes that will not lock.' in `merged.md` -- The text includes calls about bikes that will not lock. |
| 3 | Bikes that will not release usually mean a dock fault rather than a bike fault. | 5 | carried | 'Riders call about bikes that will not release and bikes that will not lock. Both usually mean a dock fault rather than a bike fault.' in `merged.md` -- “Both” includes bikes that will not release. |
| 4 | Bikes that will not lock usually mean a dock fault rather than a bike fault. | 5 | carried | 'Riders call about bikes that will not release and bikes that will not lock. Both usually mean a dock fault rather than a bike fault.' in `merged.md` -- “Both” includes bikes that will not lock. |
| 6 | E2 is a jammed locking pin. | 10 | carried | 'A dock showing E2 has a jammed locking pin.' in `merged.md` -- The text identifies a jammed locking pin as the E2 condition. |
| 7 | E4 is a loss of power to the point. | 11 | carried | 'A dock showing E4 has lost power to the point.' in `merged.md` -- The text identifies loss of power to the point as the E4 condition. |
| 11 | A rider charged for a journey that ended at a faulted dock gets the journey refunded. | 24 | carried | 'A rider charged for a journey that ended at a faulted dock gets the journey refunded.' in `merged.md` -- The text states the claim directly. |
| 14 | The support desk takes a station out of service in the app when more than half its docks are faulted. | 30 | carried | 'The support desk takes a station out of service in the app when more than half its docks are faulted.' in `merged.md` -- The text states the claim directly. |

### `merged.md` -- 25 claim(s): 0 invented, 0 contradicted, 0 supported in part, 25 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Riders call about bikes that will not release. | supported | `source_b.md` | 'Riders call about bikes that will not release and bikes that will not lock.' in `source_b.md` -- The source says riders call about bikes that will not release. |
| 2 | Riders call about bikes that will not lock. | supported | `source_b.md` | 'Riders call about bikes that will not release and bikes that will not lock.' in `source_b.md` -- The source says riders call about bikes that will not lock. |
| 3 | A bike that will not release usually means a dock fault rather than a bike fault. | supported | `source_b.md` | 'Riders call about bikes that will not release and bikes that will not lock. Both\nusually mean a dock fault rather than a bike fault.' in `source_b.md` -- The source says this applies to bikes that will not release. |
| 4 | A bike that will not lock usually means a dock fault rather than a bike fault. | supported | `source_b.md` | 'Riders call about bikes that will not release and bikes that will not lock. Both\nusually mean a dock fault rather than a bike fault.' in `source_b.md` -- The source says this applies to bikes that will not lock. |
| 5 | Riders are asked to read the code on the dock display. | supported | `source_b.md` | 'Ask the rider to read the code on the dock display.' in `source_b.md` -- The source instructs staff to ask the rider to read the display code. |
| 6 | A dock showing E2 has a jammed locking pin. | supported | `source_a.md` | 'A dock showing E2 has a jammed locking pin.' in `source_a.md` -- The source states the claim directly. |
| 7 | A dock showing E4 has lost power to the point. | supported | `source_a.md` | 'A dock showing E4 has lost power to\nthe point.' in `source_a.md` -- The source states the claim directly. |
| 8 | E2 is a mechanical fault. | supported | `source_a.md` | 'E2 is a mechanical fault and E4 is an electrical one, and they are\nescalated differently.' in `source_a.md` -- The source identifies E2 as a mechanical fault. |
| 9 | E4 is an electrical one. | supported | `source_a.md` | 'E2 is a mechanical fault and E4 is an electrical one, and they are\nescalated differently.' in `source_a.md` -- The source identifies E4 as an electrical fault. |
| 10 | E2 and E4 are escalated differently. | supported | `source_a.md` | 'E2 is a mechanical fault and E4 is an electrical one, and they are\nescalated differently.' in `source_a.md` -- The source explicitly says they are escalated differently. |
| 11 | The pin is freed with the service key. | supported | `source_a.md` | 'Free the pin with the service key and cycle the dock twice.' in `source_a.md` -- The source instructs field crew to free the pin with the service key. |
| 12 | The dock is cycled twice. | supported | `source_a.md` | 'Free the pin with the service key and cycle the dock twice.' in `source_a.md` -- The source instructs field crew to cycle the dock twice. |
| 13 | The fault is closed on the handheld if the dock takes a bike and releases it on both cycles. | supported | `source_a.md` | 'If the dock takes a\nbike and releases it on both cycles, close the fault on your handheld.' in `source_a.md` -- The source gives that condition for closing the fault on the handheld. |
| 14 | An E2 is raised to the field crew. | supported | `source_b.md` | 'Raise an E2 to the field crew.' in `source_b.md` -- The source states the claim directly. |
| 15 | E2 is escalated to the workshop after 2 failed attempts. | supported | `source_a.md` | 'Escalate E2 to the workshop after 2 failed attempts.' in `source_a.md` -- The source states the claim directly. |
| 16 | A dock that has failed twice is not kept cycling. | supported | `source_a.md` | 'Do not keep cycling a dock\nthat has failed twice;' in `source_a.md` -- The source explicitly says not to keep cycling a dock that has failed twice. |
| 17 | Repeated forcing bends the pin. | supported | `source_a.md` | 'repeated forcing bends the pin' in `source_a.md` -- The source states the claim directly. |
| 18 | Repeated forcing turns a 20 minute workshop job into a replacement. | supported | `source_a.md` | 'repeated forcing bends the pin and turns a 20 minute\nworkshop job into a replacement.' in `source_a.md` -- The source says repeated forcing has this consequence. |
| 19 | E4 is reported to the electrical contractor the same day. | supported | `source_a.md` | 'Report E4 to the electrical contractor the same day.' in `source_a.md` -- The source states the claim directly. |
| 20 | Field crew do not open the power enclosure under any circumstances. | supported | `source_a.md` | 'Field crew do not open the\npower enclosure under any circumstances.' in `source_a.md` -- The source states the claim directly. |
| 21 | The support desk takes a station out of service in the app when more than half its docks are faulted. | supported | `source_b.md` | 'The support desk takes a station out of service in the app when more than half\nits docks are faulted.' in `source_b.md` -- The source states the claim directly. |
| 22 | Field crew tell the support desk before the station is taken out of service. | supported | `source_a.md` | 'A station with more than half its docks faulted is taken out of service in the\napp. Tell the support desk before you do this, not after.' in `source_a.md` -- The field-crew source says to tell the support desk before taking the station out of service. |
| 23 | A rider charged for a journey that ended at a faulted dock gets the journey refunded. | supported | `source_b.md` | 'A rider charged for a journey that ended at a faulted dock gets the journey\nrefunded.' in `source_b.md` -- The source states the claim directly. |
| 24 | The journey is refunded at the time of the call. | supported | `source_b.md` | 'Refund at the time of the call;' in `source_b.md` -- The source specifies when to issue the refund. |
| 25 | The refund does not wait for the fault to be confirmed. | supported | `source_b.md` | 'do not wait for the fault to be\nconfirmed.' in `source_b.md` -- The source says not to wait for fault confirmation before refunding. |

## Structure

**9** mechanical check(s) over **35** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **25** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **30**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 6 run(s) over 22 attributed segment(s) — sources interleaved. 8 of 13 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

No structural finding.

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **21** departure(s) from its sources. Checking them confirms 14, rejects 1, and leaves 6 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 35 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a4` | reworded | The fault-code sentence is joined across its source line break. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-002`) |
| `a5` | reworded | The fault-code sentence is joined across its source line break. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-003`, `A-004`, `A-005`) |
| `a8` | reworded | The field-clearing sentence is joined across its source line break. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-008`) |
| `a11` | reworded | The E2 warning is joined across its source line breaks. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-010`, `A-011`, `A-012`) |
| `a14` | reworded | The E4 safety instruction is joined across its source line break. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-014`) |
| `a16` | superseded | The station-action slot uses the support desk as the app actor. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`A-015`) |
| `a17` | reworded | The station-notice instruction retains its timing without the app action. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-016`) |
| `b1` | superseded | The title slot uses the base title. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Dock Fault Escalation - Field Crew' and says so (no claim traced to it) |
| `b2` | superseded | The rider-report content sits under the base fault-code heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b4` | reworded | The rider-report sentence is joined across its source line break. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-003`, `B-004`) |
| `b5` | superseded | The base fault-code heading serves the same purpose. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b7` | subsumed | The fault-code definitions use the base document's wording. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-006`, `B-007`) |
| `b8` | superseded | The base heading sets the E2 escalation slot. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b10` | superseded | The E2 threshold uses the base document's safer value. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b11` | subsumed | The E2 instruction retains workshop escalation. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b12` | superseded | The base heading sets the E4 escalation slot. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b13` | superseded | The E4 instruction uses the base wording. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-010`) |
| `b15` | reworded | The refund sentence is joined across its source line break. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-011`) |
| `b16` | reworded | The refund-timing sentence is joined across its source line break. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-012 came back PARTIAL, B-013 came back PARTIAL (`B-012`, `B-013`) |
| `b17` | duplicate | The station heading already appears in the base document. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b18` | reworded | The station-action sentence is joined across its source line break. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-014`) |


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
| Tokens | 15,623 in, 11,601 out, 0 cached, 2,625 reasoning |
| Cost | ~$0.15 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 128.1s |
| Generated | 2026-09-27T15:18:36+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `bf7d5842201d`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
