## Verdict

**1 finding(s).** In the claims: 1 contradicted.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 24 |
| Claims extracted from `source_a.md` | 16 |
| Claims extracted from `source_b.md` | 13 |
| Forward — source claims accounted for in the merge | **28/29** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **16/16** |
| Forward — `source_b.md` claims accounted for | **12/13** |
| Reverse — merge claims found in a source | **24/24** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **52/53** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **B-013** -- the two documents disagree
  - `source_b.md:30` says: The support desk takes a station out of service in the app when more than half its docks are faulted.
  - `merged.md` says: 'Tell the support desk before you do this, not after.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text says to notify the support desk before taking the station out of service, rather than the desk doing it.

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
| 1 | A dock showing E2 has a jammed locking pin. | 5 | carried | 'E2 is a jammed locking pin' in `merged.md` -- The reference directly identifies E2 as a jammed locking pin. |
| 2 | A dock showing E4 has lost power to the point. | 5 | carried | 'E4 is a loss of power to the point' in `merged.md` -- The reference directly identifies E4 as a loss of power to the point. |
| 3 | E2 is a mechanical fault. | 6 | carried | 'E2 is a mechanical fault' in `merged.md` -- The reference directly classifies E2 as a mechanical fault. |
| 4 | E4 is an electrical fault. | 6 | carried | 'E4 is an electrical one' in `merged.md` -- The reference directly classifies E4 as an electrical fault. |
| 5 | E2 and E4 are escalated differently. | 6 | carried | 'they are escalated differently' in `merged.md` -- The reference explicitly says E2 and E4 are escalated differently. |
| 6 | The field crew should free the pin with the service key. | 11 | carried | 'Free the pin with the service key' in `merged.md` -- The reference directs the field crew to free the pin using the service key. |
| 7 | The field crew should cycle the dock twice. | 11 | carried | 'cycle the dock twice' in `merged.md` -- The reference directs the crew to cycle the dock twice. |
| 8 | If the dock takes a bike and releases it on both cycles, the field crew should close the fault on their handheld. | 11 | carried | 'If the dock takes a bike and releases it on both cycles, close the fault on your handheld.' in `merged.md` -- The reference gives this condition and directs the crew to close the fault on the handheld. |
| 9 | E2 should be escalated to the workshop after 2 failed attempts. | 16 | carried | 'Escalate E2 to the workshop after 2 failed attempts.' in `merged.md` -- The reference specifies workshop escalation after two failed attempts. |
| 10 | The field crew should not keep cycling a dock that has failed twice. | 16 | carried | 'Do not keep cycling a dock that has failed twice' in `merged.md` -- The reference explicitly says not to keep cycling a dock after two failures. |
| 11 | Repeated forcing bends the pin. | 17 | carried | 'repeated forcing bends the pin' in `merged.md` -- The reference states that repeated forcing bends the pin. |
| 12 | Repeated forcing turns a 20 minute workshop job into a replacement. | 17 | carried | 'turns a 20 minute workshop job into a replacement' in `merged.md` -- The reference states that repeated forcing turns the workshop job into a replacement. |
| 13 | E4 should be reported to the electrical contractor the same day. | 22 | carried | 'Report E4 to the electrical contractor the same day.' in `merged.md` -- The reference directs same-day reporting of E4 to the electrical contractor. |
| 14 | Field crew do not open the power enclosure under any circumstances. | 22 | carried | 'Field crew do not open the power enclosure under any circumstances.' in `merged.md` -- The reference explicitly prohibits field crew from opening the power enclosure. |
| 15 | A station with more than half its docks faulted is taken out of service in the app. | 27 | carried | 'A station with more than half its docks faulted is taken out of service in the app.' in `merged.md` -- The reference gives this threshold and says the station is taken out of service in the app. |
| 16 | The support desk should be told before the station is taken out of service. | 28 | carried | 'Tell the support desk before you do this, not after.' in `merged.md` -- The reference directs the crew to tell the support desk before taking the station out of service. |

### `source_b.md` -- 13 claim(s): 0 dropped, 1 contradicted, 0 carried in part, 12 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 13 | The support desk takes a station out of service in the app when more than half its docks are faulted. | 30 | contradicted | 'Tell the support desk before you do this, not after.' in `merged.md` -- The text says to notify the support desk before taking the station out of service, rather than the desk doing it. |
| 1 | Riders call about bikes that will not release. | 5 | carried | 'Riders call about bikes that will not release' in `merged.md` -- The reference states that riders call about bikes that will not release. |
| 2 | Riders call about bikes that will not lock. | 5 | carried | 'bikes that will not lock' in `merged.md` -- The reference states that riders call about bikes that will not lock. |
| 3 | Bikes that will not release usually indicate a dock fault rather than a bike fault. | 5 | carried | 'Both usually mean a dock fault rather than a bike fault.' in `merged.md` -- “Both” refers to bikes that will not release and bikes that will not lock, and the sentence says they usually indicate a dock fault. |
| 4 | Bikes that will not lock usually indicate a dock fault rather than a bike fault. | 5 | carried | 'Both usually mean a dock fault rather than a bike fault.' in `merged.md` -- “Both” includes bikes that will not lock, and the sentence says they usually indicate a dock fault. |
| 5 | E2 is a jammed locking pin. | 10 | carried | 'E2 is a jammed locking pin' in `merged.md` -- The reference directly identifies E2 as a jammed locking pin. |
| 6 | E4 is a loss of power to the point. | 11 | carried | 'E4 is a loss of power to the point' in `merged.md` -- The reference directly identifies E4 as a loss of power to the point. |
| 7 | An E2 should be raised to the field crew. | 15 | carried | 'Raise an E2 to the field crew.' in `merged.md` -- The reference directs that an E2 be raised to the field crew. |
| 8 | If the field crew have already tried 3 times, an E2 should be raised to the workshop instead. | 15 | carried | 'Escalate E2 to the workshop after 2 failed attempts.' in `merged.md` -- Three failed attempts exceed the stated two-attempt threshold for workshop escalation. |
| 9 | An E4 should be raised to the electrical contractor the same day. | 20 | carried | 'Report E4 to the electrical contractor the same day.' in `merged.md` -- The reference directs same-day reporting of E4 to the electrical contractor. |
| 10 | A rider charged for a journey that ended at a faulted dock gets the journey refunded. | 24 | carried | 'A rider charged for a journey that ended at a faulted dock gets the journey refunded.' in `merged.md` -- The text directly states that such a rider gets the journey refunded. |
| 11 | The refund should be issued at the time of the call. | 25 | carried | 'Refund at the time of the call' in `merged.md` -- The text says to issue the refund at the time of the call. |
| 12 | The fault should not need to be confirmed before the refund is issued. | 25 | carried | 'do not wait for the fault to be confirmed.' in `merged.md` -- The text explicitly says confirmation is not required before refunding. |

### `merged.md` -- 24 claim(s): 0 invented, 0 contradicted, 0 supported in part, 24 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Riders call about bikes that will not release. | supported | `source_b.md` | 'Riders call about bikes that will not release' in `source_b.md` -- Source_b.md states that riders call about bikes that will not release. |
| 2 | Riders call about bikes that will not lock. | supported | `source_b.md` | 'Riders call about bikes that will not lock' in `source_b.md`, **transcription_error** -- Source_b.md states that riders call about bikes that will not lock. |
| 3 | Bikes that will not release and bikes that will not lock usually mean a dock fault rather than a bike fault. | supported | `source_b.md` | 'Both usually mean a dock fault rather than a bike fault.' in `source_b.md` -- Source_b.md says both kinds of rider reports usually mean a dock fault rather than a bike fault. |
| 4 | The rider should be asked to read the code on the dock display. | supported | `source_b.md` | 'Ask the rider to read the code on the dock display.' in `source_b.md` -- Source_b.md instructs the support desk to ask the rider to read the display code. |
| 5 | E2 is a jammed locking pin. | supported | `source_b.md` | 'E2 is a jammed locking pin' in `source_b.md` -- Source_b.md directly identifies E2 as a jammed locking pin. |
| 6 | E4 is a loss of power to the point. | supported | `source_b.md` | 'E4 is a loss of power to the point.' in `source_b.md` -- Source_b.md directly identifies E4 as a loss of power to the point. |
| 7 | E2 is a mechanical fault. | supported | `source_a.md` | 'E2 is a mechanical fault' in `source_a.md` -- Source_a.md states that E2 is a mechanical fault. |
| 8 | E4 is an electrical fault. | supported | `source_a.md` | 'E2 is a mechanical fault and E4 is an electrical one' in `source_a.md` -- “An electrical one” refers to E4, supporting that E4 is an electrical fault. |
| 9 | E2 and E4 are escalated differently. | supported | `source_a.md` | 'E2 is a mechanical fault and E4 is an electrical one, and they are escalated differently.' in `source_a.md` -- Source_a.md explicitly says E2 and E4 are escalated differently. |
| 10 | The pin should be freed with the service key. | supported | `source_a.md` | 'Free the pin with the service key' in `source_a.md` -- Source_a.md instructs the field crew to free the pin with the service key. |
| 11 | The dock should be cycled twice. | supported | `source_a.md` | 'cycle the dock twice.' in `source_a.md` -- Source_a.md says to cycle the dock twice. |
| 12 | If the dock takes a bike and releases it on both cycles, the fault should be closed on the handheld. | supported | `source_a.md` | 'If the dock takes a bike and releases it on both cycles, close the fault on your handheld.' in `source_a.md` -- Source_a.md gives this condition for closing the fault on the handheld. |
| 13 | An E2 should be raised to the field crew. | supported | `source_b.md` | 'Raise an E2 to the field crew.' in `source_b.md` -- Source_b.md instructs the support desk to raise an E2 to the field crew. |
| 14 | E2 should be escalated to the workshop after 2 failed attempts. | supported | `source_a.md` | 'Escalate E2 to the workshop after 2 failed attempts.' in `source_a.md` -- Source_a.md gives the threshold of 2 failed attempts for workshop escalation. |
| 15 | A dock that has failed twice should not be cycled again. | supported | `source_a.md` | 'Do not keep cycling a dock that has failed twice;' in `source_a.md` -- Source_a.md says not to keep cycling a dock after it has failed twice. |
| 16 | Repeated forcing bends the pin. | supported | `source_a.md` | 'repeated forcing bends the pin' in `source_a.md` -- Source_a.md states that repeated forcing bends the pin. |
| 17 | Repeated forcing turns a 20 minute workshop job into a replacement. | supported | `source_a.md` | 'turns a 20 minute workshop job into a replacement.' in `source_a.md` -- Source_a.md states that repeated forcing turns a 20 minute workshop job into a replacement. |
| 18 | E4 should be reported to the electrical contractor the same day. | supported | `source_a.md` | 'Report E4 to the electrical contractor the same day.' in `source_a.md` -- Source_a.md instructs the crew to report E4 to the electrical contractor the same day. |
| 19 | Field crew do not open the power enclosure under any circumstances. | supported | `source_a.md` | 'Field crew do not open the power enclosure under any circumstances.' in `source_a.md` -- Source_a.md directly states that field crew do not open the power enclosure under any circumstances. |
| 20 | A station with more than half its docks faulted is taken out of service in the app. | supported | `source_a.md` | 'A station with more than half its docks faulted is taken out of service in the app.' in `source_a.md` -- Source_a.md states that a station exceeding this fault threshold is taken out of service in the app. |
| 21 | The support desk should be told before the station is taken out of service. | supported | `source_a.md` | 'Tell the support desk before you do this, not after.' in `source_a.md` -- Source_a.md says to tell the support desk before taking the station out of service. |
| 22 | A rider charged for a journey that ended at a faulted dock gets the journey refunded. | supported | `source_b.md` | 'A rider charged for a journey that ended at a faulted dock gets the journey refunded.' in `source_b.md` -- Source_b.md states that such a rider gets the journey refunded. |
| 23 | The refund should be made at the time of the call. | supported | `source_b.md` | 'Refund at the time of the call;' in `source_b.md` -- Source_b.md instructs the desk to refund at the time of the call. |
| 24 | The refund should not be delayed until the fault is confirmed. | supported | `source_b.md` | 'do not wait for the fault to be confirmed.' in `source_b.md` -- Source_b.md explicitly says not to wait for confirmation of the fault. |

## Structure

**9** mechanical check(s) over **35** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **24** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **29**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 6 run(s) over 22 attributed segment(s) — sources interleaved. 8 of 13 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

No structural finding.

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **18** departure(s) from its sources. Checking them confirms 12, rejects 0, and leaves 6 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 35 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a3` | superseded | The fault-code slot uses the combined wording from source_b.md. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`A-001`) |
| `a4` | superseded | The fault-code slot uses the combined wording from source_b.md. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`A-002`) |
| `a8` | reworded | The field test instruction is retained with line wrapping removed. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-008`) |
| `a11` | reworded | The warning is retained with line wrapping removed. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-010`, `A-011`, `A-012`) |
| `a14` | reworded | The field restriction is retained with line wrapping removed. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-014`) |
| `a16` | reworded | The station threshold is retained with line wrapping removed. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-015`) |
| `b1` | superseded | The base document's title is retained. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Dock Fault Escalation - Field Crew' and says so (no claim traced to it) |
| `b2` | superseded | Rider reports are consolidated under the base fault-code heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b4` | reworded | The rider-report wording is retained with line wrapping removed. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-003`, `B-004`) |
| `b5` | superseded | Code reading is consolidated under the base fault-code heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b8` | superseded | The E2 escalation guidance uses the base heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b10` | superseded | The base document's threshold is chosen for workshop escalation. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b11` | superseded | The base document's threshold is chosen for workshop escalation. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b12` | superseded | E4 guidance uses the base heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b13` | duplicate | The same-day contractor instruction already appears in this section. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-009`) |
| `b15` | reworded | The refund eligibility statement is retained with line wrapping removed. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-010`) |
| `b16` | reworded | The refund timing instruction is retained with line wrapping removed. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-011`, `B-012`) |
| `b18` | superseded | The base instruction is chosen for the station-action responsibility. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-013`) |


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
| Tokens | 15,542 in, 16,982 out, 0 cached, 9,446 reasoning |
| Cost | ~$0.01 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 123.0s |
| Generated | 2026-09-27T15:16:27+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `bf7d5842201d`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
