## Verdict

**5 finding(s).** In the claims: 3 partially dropped, 2 contradicted.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 24 |
| Claims extracted from `source_a.md` | 17 |
| Claims extracted from `source_b.md` | 13 |
| Forward — source claims accounted for in the merge | **26/30** |
| Forward — carried only in part | 3 |
| Forward — `source_a.md` claims accounted for | **17/17** |
| Forward — `source_b.md` claims accounted for | **9/13** (3 in part) |
| Reverse — merge claims found in a source | **23/24** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **53/54** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Partly dropped — the merge carries some of this claim

- **B-001** (`source_b.md:5`) — Riders call the support desk about bikes that will not release.
  - evidence: 'Riders call about bikes that will not release' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The reference text says riders call about bikes that will not release, but it does not say they call the support desk.
- **B-002** (`source_b.md:5`) — Riders call the support desk about bikes that will not lock.
  - evidence: 'bikes that will not lock' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The reference text says riders call about bikes that will not lock, but it does not say they call the support desk.
- **B-004** (`source_b.md:10`) — The support desk asks the rider to read the code on the dock display.
  - evidence: 'Ask the rider to read the code on the dock display.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The instruction to ask the rider is stated, but the reference text does not say the support desk is the one asking.

### Contradicted — the merge states something different

- **B-008** -- the two documents disagree
  - `source_b.md:15` says: If the field crew have already tried 3 times, an E2 fault is raised to the workshop instead.
  - `merged.md` says: 'Escalate E2 to the workshop after 2 failed attempts.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text sets the workshop threshold at 2 failed attempts, not 3.
- **M-003** -- the two documents disagree
  - `merged.md:9` says: The field crew should ask the rider to read the code on the dock display.
  - `source_b.md` says: 'Ask the rider to read the code on the dock display.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: This instruction is in the support desk document, so the support desk asks the rider, not the field crew as the claim states.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 17 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 17 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | A dock showing E2 has a jammed locking pin. | 5 | carried | 'A dock showing E2 has a jammed locking pin.' in `merged.md` -- The reference text states this verbatim. |
| 2 | A dock showing E4 has lost power to the point. | 5 | carried | 'A dock showing E4 has lost power to the point.' in `merged.md` -- The reference text states this verbatim. |
| 3 | E2 is a mechanical fault. | 6 | carried | 'E2 is a mechanical fault' in `merged.md` -- The reference text states that E2 is a mechanical fault. |
| 4 | E4 is an electrical fault. | 6 | carried | 'E4 an electrical one' in `merged.md`, **transcription_error** -- The reference text states that E4 is an electrical fault. |
| 5 | E2 and E4 are escalated differently. | 6 | carried | 'they are escalated differently' in `merged.md` -- The reference text states that E2 and E4 are escalated differently. |
| 6 | To clear E2 in the field, free the pin with the service key. | 11 | carried | 'Free the pin with the service key' in `merged.md` -- The Clearing E2 section says to free the pin with the service key. |
| 7 | To clear E2 in the field, cycle the dock twice. | 11 | carried | 'cycle the dock twice' in `merged.md` -- The Clearing E2 section says to cycle the dock twice. |
| 8 | If the dock takes a bike and releases it on both cycles, close the fault on the handheld. | 11 | carried | 'If the dock takes a bike and releases it on both cycles, close the fault on your handheld.' in `merged.md` -- The reference text states the same condition and action. |
| 9 | E2 is escalated to the workshop after 2 failed attempts. | 16 | carried | 'Escalate E2 to the workshop after 2 failed attempts.' in `merged.md` -- The reference text states the same threshold and destination. |
| 10 | Field crew should not keep cycling a dock that has failed twice. | 16 | carried | 'Do not keep cycling a dock that has failed twice' in `merged.md` -- The reference text gives this instruction in a section addressed to field crew. |
| 11 | Repeated forcing bends the pin. | 17 | carried | 'repeated forcing bends the pin' in `merged.md` -- The reference text states this directly. |
| 12 | Repeated forcing turns a 20 minute workshop job into a replacement. | 17 | carried | 'turns a 20 minute workshop job into a replacement' in `merged.md` -- The reference text states that repeated forcing turns a 20 minute workshop job into a replacement. |
| 13 | E4 is never a field fix. | 20 | carried | 'E4 is never a field fix' in `merged.md` -- The section heading states this verbatim. |
| 14 | E4 is reported to the electrical contractor the same day. | 22 | carried | 'Report E4 to the electrical contractor the same day.' in `merged.md` -- The reference text states the same recipient and timing. |
| 15 | Field crew do not open the power enclosure under any circumstances. | 22 | carried | 'Field crew do not open the power enclosure under any circumstances.' in `merged.md` -- The reference text states this verbatim. |
| 16 | A station with more than half its docks faulted is taken out of service in the app. | 27 | carried | 'The support desk takes a station out of service in the app when more than half its docks are faulted.' in `merged.md` -- The reference text states this, and it entails the claim. |
| 17 | The support desk must be told before a station is taken out of service, not after. | 28 | carried | 'Field crew who take a station out of service tell the support desk before they do it, not after.' in `merged.md` -- The reference text requires telling the support desk before, not after. |

### `source_b.md` -- 13 claim(s): 0 dropped, 1 contradicted, 3 carried in part, 9 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 8 | If the field crew have already tried 3 times, an E2 fault is raised to the workshop instead. | 15 | contradicted | 'Escalate E2 to the workshop after 2 failed attempts.' in `merged.md` -- The reference text sets the workshop threshold at 2 failed attempts, not 3. |
| 1 | Riders call the support desk about bikes that will not release. | 5 | carried in part | 'Riders call about bikes that will not release' in `merged.md` -- The reference text says riders call about bikes that will not release, but it does not say they call the support desk. |
| 2 | Riders call the support desk about bikes that will not lock. | 5 | carried in part | 'bikes that will not lock' in `merged.md` -- The reference text says riders call about bikes that will not lock, but it does not say they call the support desk. |
| 4 | The support desk asks the rider to read the code on the dock display. | 10 | carried in part | 'Ask the rider to read the code on the dock display.' in `merged.md` -- The instruction to ask the rider is stated, but the reference text does not say the support desk is the one asking. |
| 3 | Bikes that will not release or will not lock usually mean a dock fault rather than a bike fault. | 6 | carried | 'Both usually mean a dock fault rather than a bike fault.' in `merged.md` -- The reference text states that both situations usually mean a dock fault rather than a bike fault. |
| 5 | Fault code E2 is a jammed locking pin. | 10 | carried | 'A dock showing E2 has a jammed locking pin.' in `merged.md` -- The reference text states that E2 means a jammed locking pin. |
| 6 | Fault code E4 is a loss of power to the point. | 11 | carried | 'A dock showing E4 has lost power to the point.' in `merged.md` -- The reference text states that E4 means loss of power to the point. |
| 7 | An E2 fault is raised to the field crew. | 15 | carried | 'The support desk raises an E2 to the field crew.' in `merged.md` -- The reference text states that E2 is raised to the field crew. |
| 9 | An E4 fault is raised to the electrical contractor the same day. | 20 | carried | 'Report E4 to the electrical contractor the same day.' in `merged.md` -- The reference text states that E4 goes to the electrical contractor the same day. |
| 10 | A rider charged for a journey that ended at a faulted dock gets the journey refunded. | 24 | carried | 'A rider charged for a journey that ended at a faulted dock gets the journey refunded.' in `merged.md` -- The reference text states this verbatim. |
| 11 | The refund for a journey that ended at a faulted dock is given at the time of the call. | 25 | carried | 'Refund at the time of the call' in `merged.md` -- The reference text states that the refund is given at the time of the call. |
| 12 | The support desk does not wait for the fault to be confirmed before refunding a journey that ended at a faulted dock. | 25 | carried | 'do not wait for the fault to be confirmed' in `merged.md` -- The reference text says not to wait for fault confirmation before refunding. |
| 13 | The support desk takes a station out of service in the app when more than half its docks are faulted. | 30 | carried | 'The support desk takes a station out of service in the app when more than half its docks are faulted.' in `merged.md` -- The reference text states this verbatim. |

### `merged.md` -- 24 claim(s): 0 invented, 1 contradicted, 0 supported in part, 23 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 3 | The field crew should ask the rider to read the code on the dock display. | contradicted | `source_b.md` | 'Ask the rider to read the code on the dock display.' in `source_b.md` -- This instruction is in the support desk document, so the support desk asks the rider, not the field crew as the claim states. |
| 1 | Riders call about bikes that will not release and bikes that will not lock. | supported | `source_b.md` | 'Riders call about bikes that will not release and bikes that will not lock.' in `source_b.md` -- Source_b states this verbatim. |
| 2 | Bikes that will not release and bikes that will not lock usually mean a dock fault rather than a bike fault. | supported | `source_b.md` | 'Both\nusually mean a dock fault rather than a bike fault.' in `source_b.md` -- Source_b says both kinds of report usually mean a dock fault rather than a bike fault. |
| 4 | A dock showing E2 has a jammed locking pin. | supported | `source_a.md` | 'A dock showing E2 has a jammed locking pin.' in `source_a.md` -- Source_a states this verbatim. |
| 5 | A dock showing E4 has lost power to the point. | supported | `source_a.md` | 'A dock showing E4 has lost power to\nthe point.' in `source_a.md` -- Source_a states this verbatim. |
| 6 | E2 is a mechanical fault. | supported | `source_a.md` | 'E2 is a mechanical fault' in `source_a.md` -- Source_a states that E2 is a mechanical fault. |
| 7 | E4 is an electrical fault. | supported | `source_a.md` | 'E4 is an electrical one' in `source_a.md` -- Source_a states that E4 is an electrical fault. |
| 8 | E2 and E4 are escalated differently. | supported | `source_a.md` | 'they are\nescalated differently' in `source_a.md` -- Source_a states that E2 and E4 are escalated differently. |
| 9 | To clear E2 in the field, free the pin with the service key. | supported | `source_a.md` | 'Free the pin with the service key' in `source_a.md` -- Source_a's section on clearing E2 in the field says to free the pin with the service key. |
| 10 | To clear E2 in the field, cycle the dock twice. | supported | `source_a.md` | 'cycle the dock twice' in `source_a.md` -- Source_a's section on clearing E2 in the field says to cycle the dock twice. |
| 11 | If the dock takes a bike and releases it on both cycles, close the fault on the handheld. | supported | `source_a.md` | 'If the dock takes a\nbike and releases it on both cycles, close the fault on your handheld.' in `source_a.md` -- Source_a states this with the same meaning. |
| 12 | The support desk raises an E2 to the field crew. | supported | `source_b.md` | 'Raise an E2 to the field crew.' in `source_b.md` -- The support desk document instructs raising an E2 to the field crew. |
| 13 | E2 is escalated to the workshop after 2 failed attempts. | supported | `source_a.md` | 'Escalate E2 to the workshop after 2 failed attempts.' in `source_a.md` -- Source_a states this verbatim, though source_b has the desk escalate to the workshop after 3 field crew attempts. |
| 14 | Field crew should not keep cycling a dock that has failed twice. | supported | `source_a.md` | 'Do not keep cycling a dock\nthat has failed twice' in `source_a.md` -- Source_a, the field crew document, instructs not to keep cycling a dock that has failed twice. |
| 15 | Repeated forcing of a dock bends the pin. | supported | `source_a.md` | 'repeated forcing bends the pin' in `source_a.md` -- Source_a states that repeated forcing bends the pin. |
| 16 | Repeated forcing of a dock turns a 20 minute workshop job into a replacement. | supported | `source_a.md` | 'turns a 20 minute\nworkshop job into a replacement' in `source_a.md` -- Source_a states that repeated forcing turns a 20 minute workshop job into a replacement. |
| 17 | E4 is never a field fix. | supported | `source_a.md` | 'E4 is never a field fix' in `source_a.md` -- Source_a's section heading states this verbatim. |
| 18 | E4 is reported to the electrical contractor the same day. | supported | `source_a.md` | 'Report E4 to the electrical contractor the same day.' in `source_a.md` -- Source_a states this, and source_b agrees. |
| 19 | Field crew do not open the power enclosure under any circumstances. | supported | `source_a.md` | 'Field crew do not open the\npower enclosure under any circumstances.' in `source_a.md` -- Source_a states this verbatim. |
| 20 | A rider charged for a journey that ended at a faulted dock gets the journey refunded. | supported | `source_b.md` | 'A rider charged for a journey that ended at a faulted dock gets the journey\nrefunded.' in `source_b.md` -- Source_b states this verbatim. |
| 21 | The refund is given at the time of the call. | supported | `source_b.md` | 'Refund at the time of the call' in `source_b.md` -- Source_b instructs that the refund is given at the time of the call. |
| 22 | The refund does not wait for the fault to be confirmed. | supported | `source_b.md` | 'do not wait for the fault to be\nconfirmed' in `source_b.md` -- Source_b says not to wait for the fault to be confirmed before refunding. |
| 23 | The support desk takes a station out of service in the app when more than half its docks are faulted. | supported | `source_b.md` | 'The support desk takes a station out of service in the app when more than half\nits docks are faulted.' in `source_b.md` -- Source_b states this verbatim. |
| 24 | Field crew who take a station out of service tell the support desk before they do it, not after. | supported | `source_a.md` | 'Tell the support desk before you do this, not after.' in `source_a.md` -- Source_a, addressed to field crew, says to tell the support desk before taking a station out of service, not after. |

## Structure

**9** mechanical check(s) over **35** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **24** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **30**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 8 run(s) over 23 attributed segment(s) — sources interleaved. 9 of 13 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

No structural finding.

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **21** departure(s) from its sources. Checking them confirms 17, rejects 0, and leaves 4 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 35 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a4` | reworded | Hard line break unwrapped into paragraph prose. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-002`) |
| `a5` | reworded | Hard line break unwrapped into paragraph prose. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-003`, `A-004`, `A-005`) |
| `a8` | reworded | Hard line break unwrapped into paragraph prose. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-008`) |
| `a11` | reworded | Hard line breaks unwrapped into paragraph prose. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-010`, `A-011`, `A-012`) |
| `a14` | reworded | Hard line break unwrapped into paragraph prose. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-015`) |
| `a16` | reconciled | Out-of-service rule combined with b18's statement of who does it. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-016`) |
| `a17` | reworded | Instruction restated generally for field crew. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-017`) |
| `b1` | superseded | Base title kept. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Dock Fault Escalation - Field Crew' and says so (no claim traced to it) |
| `b4` | reworded | Hard line break unwrapped into paragraph prose. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-003`) |
| `b5` | superseded | Base heading kept for the fault code section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b7` | duplicate | a3 and a4 already state both code meanings. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-005`, `B-006`) |
| `b8` | superseded | Base heading kept for E2 escalation. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b9` | reworded | Actor made explicit in the field crew document. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-007`) |
| `b10` | superseded | Threshold of 2 from base chosen over 3. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-008`) |
| `b11` | superseded | Workshop escalation carried by base sentence. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b12` | superseded | Base heading kept for E4. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b13` | duplicate | a13 states the same instruction. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-009`) |
| `b15` | reworded | Hard line break unwrapped into paragraph prose. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-010`) |
| `b16` | reworded | Hard line break unwrapped into paragraph prose. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-011`, `B-012`) |
| `b17` | duplicate | Identical heading already in base. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b18` | reconciled | Support desk actor combined with a16/a17 field crew rule. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-013`) |


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
| Duration | 127.2s |
| Generated | 2026-09-27T15:57:33+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup opus-5.5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
