## Verdict

**4 finding(s).** In the claims: 1 contradicted. In the structure: 1 undeclared absence, 1 undeclared rewording, 1 declared loss over budget. The merge declared **3** drop(s) of 35 source segment(s), **8.6%**, over the 3% budget: past that share the omissions are the finding, whatever each one says about itself.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 14 |
| Claims extracted from `source_a.md` | 9 |
| Claims extracted from `source_b.md` | 6 |
| Forward — source claims accounted for in the merge | **14/15** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **9/9** |
| Forward — `source_b.md` claims accounted for | **5/6** |
| Reverse — merge claims found in a source | **14/14** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **29/29** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **B-006** -- the two documents disagree
  - `source_b.md:30` says: The support desk takes a station out of service in the app when more than half its docks are faulted.
  - `merged.md` says: 'A station with more than half its docks faulted is taken out of service in the app. Notify the support desk before this happens, not after.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The passive voice and instruction to notify support desk before removal happens indicates the support desk is not the agent performing this action, contradicting the claim.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 9 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 9 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | A dock showing E2 has a jammed locking pin. | 5 | carried | 'E2 indicates a jammed locking pin' in `merged.md` -- The reference text explicitly states that E2 indicates a jammed locking pin. |
| 2 | A dock showing E4 has lost power to the point. | 5 | carried | 'E4 indicates a loss of power to the point' in `merged.md` -- The reference text explicitly states that E4 indicates a loss of power to the point. |
| 3 | E2 is a mechanical fault. | 6 | carried | 'E2 is a mechanical fault' in `merged.md` -- The reference text explicitly states that E2 is a mechanical fault. |
| 4 | E4 is an electrical fault. | 6 | carried | 'E4 is an electrical one' in `merged.md` -- The reference text states E4 is an electrical one, which equates to an electrical fault. |
| 5 | E2 and E4 are escalated differently. | 6 | carried | 'they are escalated differently' in `merged.md` -- The reference text explicitly states that E2 and E4 are escalated differently. |
| 6 | Repeated forcing bends the pin. | 17 | carried | 'repeated forcing bends the pin' in `merged.md` -- The reference text explicitly states that repeated forcing bends the pin. |
| 7 | Repeated forcing turns a 20 minute workshop job into a replacement. | 17 | carried | 'repeated forcing bends the pin and turns a 20 minute workshop job into a replacement' in `merged.md` -- The reference text explicitly states both that repeated forcing bends the pin and turns a workshop job into a replacement. |
| 8 | E4 is never a field fix. | 20 | carried | 'E4 is never a field fix' in `merged.md` -- The reference text explicitly states that E4 is never a field fix. |
| 9 | A station with more than half its docks faulted is taken out of service in the app. | 27 | carried | 'A station with more than half its docks faulted is taken out of service in the app' in `merged.md` -- The reference text explicitly states that a station with more than half its docks faulted is taken out of service in the app. |

### `source_b.md` -- 6 claim(s): 0 dropped, 1 contradicted, 0 carried in part, 5 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 6 | The support desk takes a station out of service in the app when more than half its docks are faulted. | 30 | contradicted | 'A station with more than half its docks faulted is taken out of service in the app. Notify the support desk before this happens, not after.' in `merged.md` -- The passive voice and instruction to notify support desk before removal happens indicates the support desk is not the agent performing this action, contradicting the claim. |
| 1 | Riders call about bikes that will not release. | 5 | carried | 'Riders call about bikes that will not lock or release' in `merged.md` -- The claim that riders call about bikes that will not release is contained in the statement that riders call about bikes that will not lock or release. |
| 2 | Riders call about bikes that will not lock. | 5 | carried | 'Riders call about bikes that will not lock or release' in `merged.md` -- The claim that riders call about bikes that will not lock is contained in the statement that riders call about bikes that will not lock or release. |
| 3 | E2 is a jammed locking pin. | 10 | carried | 'E2 indicates a jammed locking pin' in `merged.md` -- The reference text explicitly states that E2 indicates a jammed locking pin. |
| 4 | E4 is a loss of power to the point. | 11 | carried | 'E4 indicates a loss of power to the point' in `merged.md` -- The reference text explicitly states that E4 indicates a loss of power to the point. |
| 5 | A rider charged for a journey that ended at a faulted dock gets the journey refunded. | 24 | carried | 'Riders charged for journeys that ended at a faulted dock receive a refund' in `merged.md` -- The reference text explicitly states that riders charged for journeys ending at a faulted dock receive a refund. |

### `merged.md` -- 14 claim(s): 0 invented, 0 contradicted, 0 supported in part, 14 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Riders call about bikes that will not lock or release. | supported | `source_b.md` | 'Riders call about bikes that will not release and bikes that will not lock.' in `source_b.md` -- Source_b.md directly states this claim about riders calling regarding bikes that will not lock or release. |
| 2 | That bikes will not lock or release usually indicates a dock fault rather than a bike fault. | supported | `source_b.md` | 'Both usually mean a dock fault rather than a bike fault.' in `source_b.md` -- Source_b.md states that bikes not locking or releasing usually indicate dock faults rather than bike faults. |
| 3 | The dock display shows an error code. | supported | `source_b.md` | 'Ask the rider to read the code on the dock display.' in `source_b.md` -- Source_b.md indicates that a code appears on the dock display that can be read. |
| 4 | E2 indicates a jammed locking pin. | supported | `source_b.md` | 'E2 is a jammed locking pin' in `source_b.md` -- Source_b.md directly defines E2 as a jammed locking pin. |
| 5 | E4 indicates a loss of power to the point. | supported | `source_b.md` | 'E4 is a loss of power to the point.' in `source_b.md` -- Source_b.md directly defines E4 as a loss of power to the point. |
| 6 | E2 is a mechanical fault. | supported | `source_a.md` | 'E2 is a mechanical fault' in `source_a.md` -- Source_a.md directly states that E2 is a mechanical fault. |
| 7 | E4 is an electrical fault. | supported | `source_a.md` | 'E4 is an electrical one' in `source_a.md` -- Source_a.md directly states that E4 is an electrical fault. |
| 8 | E2 and E4 are escalated differently. | supported | `source_a.md` | 'they are escalated differently' in `source_a.md` -- Source_a.md directly states that E2 and E4 are escalated differently. |
| 9 | Repeated forcing bends the pin. | supported | `source_a.md` | 'repeated forcing bends the pin' in `source_a.md` -- Source_a.md directly states that repeated forcing bends the pin. |
| 10 | Repeated forcing turns a 20 minute workshop job into a replacement. | supported | `source_a.md` | 'repeated forcing bends the pin and turns a 20 minute workshop job into a replacement.' in `source_a.md` -- Source_a.md directly states that repeated forcing turns a workshop job into a replacement. |
| 11 | Field crew do not open the power enclosure under any circumstances. | supported | `source_a.md` | 'Field crew do not open the power enclosure under any circumstances.' in `source_a.md` -- Source_a.md directly states that field crew do not open the power enclosure under any circumstances. |
| 12 | A station with more than half its docks faulted is taken out of service in the app. | supported | `source_a.md` | 'A station with more than half its docks faulted is taken out of service in the app.' in `source_a.md` -- Source_a.md directly states this claim about stations with more than half faulted docks being taken out of service. |
| 13 | Riders charged for journeys that ended at a faulted dock receive a refund. | supported | `source_b.md` | 'A rider charged for a journey that ended at a faulted dock gets the journey refunded.' in `source_b.md` -- Source_b.md directly states that riders charged for journeys ending at faulted docks receive refunds. |
| 14 | The support desk refunds at the time of the call without waiting for the fault to be confirmed. | supported | `source_b.md` | 'Refund at the time of the call; do not wait for the fault to be confirmed.' in `source_b.md` -- Source_b.md directly states that the support desk refunds at time of call without waiting for fault confirmation. |

## Structure

**9** mechanical check(s) over **35** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **14** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **15**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 4 run(s) over 18 attributed segment(s) — sources interleaved. 8 of 13 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

`[-...-]` is what the source said and `{+...+}` is what the merge says.

### Absent and undeclared — in a source, not in the merge, and no record explains it

- `b18` (`source_b.md`) — 'The support desk takes a station out of service in the app when more than half its docks are faulted.' is not in the merge and no disposition record explains it (nearest merge segment m21 at 0.52)

  ```text
  In the source: The support desk takes a station out of service in the app when more than half its docks are faulted.
  ```

### Reworded and undeclared — in the merge in altered wording, and no record explains it. At off this also covers layout: a segment whose source line breaks the merge ran together is altered and undeclared, and 380 reuses this kind rather than moving FINDING_KINDS off 12

- `b13` (`source_b.md`) — 'Raise an E4 to the electrical contractor the same day.' is reworded in the merge and no disposition record explains it (nearest merge segment m14 at 0.91)

  ```text
  In the source: Raise an E4 to the electrical contractor the same day.
  In the merge:  Report E4 to the electrical contractor the same day.
  What changed:  [-Raise an-] {+Report+} E4 to the electrical contractor the same day.
  ```

### Over budget — declared loss past the ceiling

- 3 of 35 segments are declared dropped (8.6%), over the 3% budget

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

> **Over budget.** The merge declared **3** drop(s) of 35 source segment(s), **8.6%**, over the 3% budget: past that share the omissions are the finding, whatever each one says about itself.

## Declarations

The merge declared **19** departure(s) from its sources. Checking them confirms 8, rejects 2, and leaves 9 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 3 of 35 source segment(s) declared gone, **8.6%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a3` | reworded | Simplified phrasing while preserving meaning. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-001`) |
| `a4` | reworded | Simplified phrasing while preserving meaning. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-002`) |
| `a17` | reworded | Rephrased for clarity in merged context. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b1` | superseded | Base document title was retained. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Dock Fault Escalation - Field Crew' and says so (no claim traced to it) |
| `b2` | superseded | Base document heading retained for fault section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b3` | reworded | Rephrased rider reports for clarity. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-001`, `B-002`) |
| `b4` | superseded | Base document heading retained for fault section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b5` | dropped | Support desk specific; not applicable to field crew. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b6` | superseded | Base document fault descriptions used instead. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b7` | superseded | Base document heading retained. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-003`, `B-004`) |
| `b8` | dropped | Support desk specific escalation step. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b9` | superseded | Field crew threshold from base document chosen (2 vs 3). | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b10` | superseded | Field crew threshold from base document chosen (2 vs 3). | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b11` | superseded | Base document heading retained. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b12` | superseded | Base document E4 instruction used instead. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b14` | reworded | Rephrased for consistency with merged document. | **rejected** | declared 'reworded', and its text is in the merge (no claim traced to it) |
| `b15` | reworded | Rephrased to clarify support desk handles refunds. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-005`) |
| `b16` | duplicate | Identical heading to base document section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'duplicate' is what happened to it (no claim traced to it) |
| `b17` | dropped | Support desk action implicit in merged instruction. | **rejected** | declared 'dropped', and its text is in the merge (no claim traced to it) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | 45fff742d0ed (command) -- lineup haiku-4.5-sub |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | claude-haiku-4-5-20251001 -> claude-haiku-4-5-20251001 |
| Model (decompose) | claude-haiku-4-5-20251001 -> claude-haiku-4-5-20251001 |
| Model (verify) | claude-haiku-4-5-20251001 -> claude-haiku-4-5-20251001 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile subscription, effort decompose one level (extended thinking on/off; default kept), merge one level (extended thinking on/off; default kept), verify one level (extended thinking on/off; default kept) |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 7 live, 0 cached, 0 replayed |
| Tokens | unknown (7 call(s) reported no usage) |
| Cost | unmeasured (7 call(s) reported no tokens, so no figure can be derived) |
| Schema repairs | 1 |
| Isolation | decompose, merge, verify: safe mode, no tools |
| Errors | 0 |
| Duration | 751.0s |
| Generated | 2026-09-27T15:55:24+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup haiku-4.5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
