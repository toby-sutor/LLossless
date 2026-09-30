## Verdict

**4 finding(s).** In the claims: 2 contradicted. In the structure: 1 verbatim violation, 1 declared loss over budget.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 24 |
| Claims extracted from `source_a.md` | 15 |
| Claims extracted from `source_b.md` | 11 |
| Forward — source claims accounted for in the merge | **25/26** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **15/15** |
| Forward — `source_b.md` claims accounted for | **10/11** |
| Reverse — merge claims found in a source | **23/24** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **49/50** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **B-006** -- the two documents disagree
  - `source_b.md:15` says: If the field crew have already tried 3 times, the E2 fault is raised to the workshop instead.
  - `merged.md` says: 'Escalate E2 to the workshop after 2 failed attempts' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text specifies 2 failed attempts, not 3, contradicting the claim's number.
- **M-014** -- the two documents disagree
  - `merged.md:13` says: E2 should be escalated to the workshop after 2 failed attempts.
  - `source_b.md` says: 'If the field crew have already tried 3 times, raise it to the workshop instead.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source_a says escalate after 2 failed attempts but source_b gives a different threshold of 3 attempts, a conflicting value for the same fact.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 15 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 15 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | A dock showing E2 has a jammed locking pin. | 5 | carried | 'A dock showing E2 has a jammed locking pin' in `merged.md` -- Directly stated in the fault codes section. |
| 2 | A dock showing E4 has lost power to the point. | 5 | carried | 'one showing E4 has lost power to the point' in `merged.md` -- Directly stated in the fault codes section. |
| 3 | E2 is a mechanical fault. | 6 | carried | 'E2 is a mechanical fault' in `merged.md` -- Directly stated. |
| 4 | E4 is an electrical fault. | 6 | carried | 'E4 is... an electrical one' in `merged.md`, **transcription_error** -- Directly stated that E4 is an electrical fault. |
| 5 | E2 and E4 are escalated differently. | 6 | carried | 'they are escalated differently' in `merged.md` -- Directly stated that E2 and E4 are escalated differently. |
| 6 | The pin is freed with the service key. | 11 | carried | 'Free the pin with the service key' in `merged.md` -- Directly stated in clearing E2 section. |
| 7 | The dock is cycled twice. | 11 | carried | 'cycle the dock twice' in `merged.md` -- Directly stated. |
| 8 | If the dock takes a bike and releases it on both cycles, the fault is closed on the handheld. | 11 | carried | 'If the dock takes a bike and releases it on both cycles, close the fault on your handheld.' in `merged.md` -- Directly stated. |
| 9 | E2 is escalated to the workshop after 2 failed attempts. | 16 | carried | 'Escalate E2 to the workshop after 2 failed attempts' in `merged.md` -- Directly stated. |
| 10 | Repeated forcing bends the pin. | 17 | carried | 'repeated forcing bends the pin' in `merged.md` -- Directly stated. |
| 11 | Repeated forcing turns a 20 minute workshop job into a replacement. | 17 | carried | 'turns a 20 minute workshop job into a replacement' in `merged.md` -- Directly stated. |
| 12 | E4 is reported to the electrical contractor the same day. | 22 | carried | 'Report E4 to the electrical contractor the same day.' in `merged.md` -- Directly stated. |
| 13 | Field crew do not open the power enclosure under any circumstances. | 22 | carried | 'Field crew do not open the power enclosure under any circumstances.' in `merged.md` -- Directly stated. |
| 14 | A station with more than half its docks faulted is taken out of service in the app. | 27 | carried | "When more than half of a station's docks are faulted, the support desk takes the station out of service in the app." in `merged.md` -- Directly stated. |
| 15 | The support desk must be told before taking a station out of service, not after. | 28 | carried | 'Field crew must tell the support desk before this happens, not after.' in `merged.md` -- Directly stated. |

### `source_b.md` -- 11 claim(s): 0 dropped, 1 contradicted, 0 carried in part, 10 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 6 | If the field crew have already tried 3 times, the E2 fault is raised to the workshop instead. | 15 | contradicted | 'Escalate E2 to the workshop after 2 failed attempts' in `merged.md` -- The text specifies 2 failed attempts, not 3, contradicting the claim's number. |
| 1 | Riders call about bikes that will not release and bikes that will not lock. | 5 | carried | 'Riders call about bikes that will not release and bikes that will not lock' in `merged.md` -- Directly stated. |
| 2 | Both bikes that will not release and bikes that will not lock usually mean a dock fault rather than a bike fault. | 5 | carried | 'both usually indicate a dock fault rather than a bike fault' in `merged.md` -- Directly stated. |
| 3 | E2 is a jammed locking pin. | 10 | carried | 'A dock showing E2 has a jammed locking pin' in `merged.md` -- States E2 corresponds to a jammed locking pin. |
| 4 | E4 is a loss of power to the point. | 11 | carried | 'one showing E4 has lost power to the point' in `merged.md` -- States E4 corresponds to loss of power to the point. |
| 5 | An E2 fault is raised to the field crew. | 15 | carried | 'The support desk raises an E2 to the field crew.' in `merged.md` -- Directly stated. |
| 7 | An E4 fault is raised to the electrical contractor the same day. | 20 | carried | 'Report E4 to the electrical contractor the same day.' in `merged.md` -- Directly stated. |
| 8 | A rider charged for a journey that ended at a faulted dock gets the journey refunded. | 24 | carried | 'A rider charged for a journey that ended at a faulted dock gets the journey refunded.' in `merged.md` -- Directly stated. |
| 9 | The refund is given at the time of the call. | 25 | carried | 'Refund at the time of the call' in `merged.md` -- Directly stated. |
| 10 | The support desk does not wait for the fault to be confirmed before refunding. | 25 | carried | 'do not wait for the fault to be confirmed' in `merged.md` -- Directly stated. |
| 11 | The support desk takes a station out of service in the app when more than half its docks are faulted. | 30 | carried | "When more than half of a station's docks are faulted, the support desk takes the station out of service in the app." in `merged.md` -- The text directly states this condition and action. |

### `merged.md` -- 24 claim(s): 0 invented, 1 contradicted, 0 supported in part, 23 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 14 | E2 should be escalated to the workshop after 2 failed attempts. | contradicted | `source_b.md` | 'If the field crew have already tried 3 times, raise it to the workshop instead.' in `source_b.md` -- Source_a says escalate after 2 failed attempts but source_b gives a different threshold of 3 attempts, a conflicting value for the same fact. |
| 1 | Riders call about bikes that will not release. | supported | `source_b.md` | 'Riders call about bikes that will not release and bikes that will not lock.' in `source_b.md` -- Source_b states riders call about bikes that will not release. |
| 2 | Riders call about bikes that will not lock. | supported | `source_b.md` | 'Riders call about bikes that will not release and bikes that will not lock.' in `source_b.md` -- Source_b states riders call about bikes that will not lock. |
| 3 | Bikes that will not release and bikes that will not lock both usually indicate a dock fault rather than a bike fault. | supported | `source_b.md` | 'Both usually mean a dock fault rather than a bike fault.' in `source_b.md` -- Source_b states both symptoms usually indicate a dock fault rather than a bike fault. |
| 4 | A dock showing E2 has a jammed locking pin. | supported | `source_a.md` | 'A dock showing E2 has a jammed locking pin.' in `source_a.md` -- Source_a states this directly. |
| 5 | A dock showing E4 has lost power to the point. | supported | `source_a.md` | 'A dock showing E4 has lost power to the point.' in `source_a.md` -- Source_a states this directly. |
| 6 | The support desk asks the rider to read out the code on the dock display. | supported | `source_b.md` | 'Ask the rider to read the code on the dock display.' in `source_b.md` -- Source_b, the support desk document, instructs asking the rider to read the code. |
| 7 | E2 is a mechanical fault. | supported | `source_a.md` | 'E2 is a mechanical fault and E4 is an electrical one' in `source_a.md` -- Source_a states E2 is a mechanical fault. |
| 8 | E4 is an electrical fault. | supported | `source_a.md` | 'E2 is a mechanical fault and E4 is an electrical one' in `source_a.md` -- Source_a states E4 is an electrical one, i.e. an electrical fault. |
| 9 | E2 and E4 are escalated differently. | supported | `source_a.md` | 'and they are escalated differently.' in `source_a.md` -- Source_a explicitly states the two fault types are escalated differently. |
| 10 | The field crew should free the pin with the service key. | supported | `source_a.md` | 'Free the pin with the service key and cycle the dock twice.' in `source_a.md` -- Source_a instructs freeing the pin with the service key. |
| 11 | The field crew should cycle the dock twice. | supported | `source_a.md` | 'Free the pin with the service key and cycle the dock twice.' in `source_a.md` -- Source_a instructs cycling the dock twice. |
| 12 | If the dock takes a bike and releases it on both cycles, the fault should be closed on the handheld. | supported | `source_a.md` | 'If the dock takes a bike and releases it on both cycles, close the fault on your handheld.' in `source_a.md` -- Source_a states this exact procedure. |
| 13 | The support desk raises an E2 to the field crew. | supported | `source_b.md` | 'Raise an E2 to the field crew.' in `source_b.md` -- Source_b states the support desk raises E2 faults to the field crew. |
| 15 | A dock that has already failed twice should not be kept cycling. | supported | `source_a.md` | 'Do not keep cycling a dock that has failed twice' in `source_a.md` -- Source_a states this directly. |
| 16 | Repeated forcing bends the pin. | supported | `source_a.md` | 'repeated forcing bends the pin' in `source_a.md` -- Source_a states this directly. |
| 17 | Repeated forcing turns a 20 minute workshop job into a replacement. | supported | `source_a.md` | 'turns a 20 minute workshop job into a replacement.' in `source_a.md` -- Source_a states this directly. |
| 18 | E4 should be reported to the electrical contractor the same day. | supported | `source_a.md` | 'Report E4 to the electrical contractor the same day.' in `source_a.md` -- Source_a states E4 should be reported to the electrical contractor the same day. |
| 19 | Field crew do not open the power enclosure under any circumstances. | supported | `source_a.md` | 'Field crew do not open the power enclosure under any circumstances.' in `source_a.md` -- Source_a states this directly. |
| 20 | A rider charged for a journey that ended at a faulted dock gets the journey refunded. | supported | `source_b.md` | 'A rider charged for a journey that ended at a faulted dock gets the journey refunded.' in `source_b.md` -- Source_b states this directly. |
| 21 | The refund should occur at the time of the call. | supported | `source_b.md` | 'Refund at the time of the call; do not wait for the fault to be confirmed.' in `source_b.md` -- Source_b states refunds occur at the time of the call. |
| 22 | The refund process should not wait for the fault to be confirmed. | supported | `source_b.md` | 'do not wait for the fault to be confirmed.' in `source_b.md` -- Source_b explicitly states not to wait for fault confirmation. |
| 23 | When more than half of a station's docks are faulted, the support desk takes the station out of service in the app. | supported | `source_b.md` | 'The support desk takes a station out of service in the app when more than half its docks are faulted.' in `source_b.md` -- Source_b states this directly. |
| 24 | Field crew must tell the support desk before the station is taken out of service, not after. | supported | `source_a.md` | 'Tell the support desk before you do this, not after.' in `source_a.md` -- Source_a instructs field crew to tell the support desk before taking a station out of service, not after. |

## Structure

**9** mechanical check(s) over **35** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **24** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **26**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 7 run(s) over 19 attributed segment(s) — sources interleaved. 9 of 13 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Verbatim violation — an invariant-core token did not survive unchanged

- `b10` (`source_b.md`) — numeric '3' (times) does not survive into the merge unchanged

### Over budget — declared loss past the ceiling

- 4 absent segments are declared replaced by the same replacement (a3, a4, b6, b7), over the ceiling of 3. One replacement standing in for that many segments has not replaced them, it has dropped them: the detail it names is gone from the document

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **20** departure(s) from its sources. Checking them confirms 14, rejects 0, and leaves 6 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 35 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | Base title kept over support desk's title. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Dock Fault Escalation - Field Crew' and says so (no claim traced to it) |
| `a3` | reworded | Combined with a4 and b's rider-reporting detail. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-001`) |
| `a4` | reworded | Merged with a3 into one sentence. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-002`) |
| `b6` | subsumed | Rider-reads-code detail folded into fault code sentence. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b7` | duplicate | Restates E2/E4 meanings already given by a3 and a4. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-003`, `B-004`) |
| `b5` | superseded | Consolidated under the base's heading for this topic. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b3` | reworded | Merged with b4 into one sentence. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-001`) |
| `b4` | subsumed | Folded into the combined rider-report sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-002`) |
| `b8` | superseded | Consolidated under the base's escalation heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b9` | reworded | Initial escalation step kept with tightened wording. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-005`) |
| `b10` | superseded | Attempt-count disagreement resolved to the base's value of 2. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b11` | superseded | Folded into the chosen-threshold sentence. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a10` | reworded | Combined with a11 into one sentence. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-009`) |
| `a11` | reworded | Combined with a10, wording tightened. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-010`, `A-011`) |
| `b12` | superseded | Consolidated under the base's escalation heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b13` | duplicate | Restates a13's fact about same-day reporting. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-007`) |
| `a16` | reconciled | Threshold and who performs the action are one fact combined. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-014`) |
| `b18` | reconciled | Threshold and who performs the action are one fact combined. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-011`) |
| `a17` | reworded | Instruction kept with tightened wording. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-015`) |
| `b17` | duplicate | Identical heading already carried from the base's a15. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |


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
| Calls | 7 live, 0 cached, 0 replayed |
| Tokens | 22,518 in, 27,171 out |
| Cost | ~$0.32 estimated (rates read 2026-08-31) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 219.9s |
| Generated | 2026-09-27T15:41:10+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
