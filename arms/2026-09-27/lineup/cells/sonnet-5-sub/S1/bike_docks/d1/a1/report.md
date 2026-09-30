## Verdict

**7 finding(s).** In the claims: 2 contradicted. In the structure: 1 undeclared absence, 1 undeclared rewording, 2 unresolved replacement, 1 verbatim violation.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 24 |
| Claims extracted from `source_a.md` | 17 |
| Claims extracted from `source_b.md` | 12 |
| Forward — source claims accounted for in the merge | **27/29** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **17/17** |
| Forward — `source_b.md` claims accounted for | **10/12** |
| Reverse — merge claims found in a source | **24/24** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **53/53** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **B-007** -- the two documents disagree
  - `source_b.md:15` says: If the field crew have already tried 3 times, an E2 is raised to the workshop instead.
  - `merged.md` says: 'Escalate E2 to the workshop after 2 failed attempts' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text states 2 failed attempts, not 3.
- **B-012** -- the two documents disagree
  - `source_b.md:30` says: The support desk takes a station out of service in the app when more than half its docks are faulted.
  - `merged.md` says: 'A station with more than half its docks faulted is taken out of service in the app. Tell the support desk before you do this, not after.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The field crew takes the station out of service and merely tells the support desk beforehand, not the support desk itself.

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
| 1 | A dock showing E2 has a jammed locking pin. | 5 | carried | 'A dock showing E2 has a jammed locking pin.' in `merged.md` -- Directly stated. |
| 2 | A dock showing E4 has lost power to the point. | 5 | carried | 'A dock showing E4 has lost power to the point.' in `merged.md` -- Directly stated. |
| 3 | E2 is a mechanical fault. | 6 | carried | 'E2 is a mechanical fault' in `merged.md` -- Directly stated. |
| 4 | E4 is an electrical fault. | 6 | carried | 'E4 is an electrical one' in `merged.md` -- Directly stated as an electrical fault. |
| 5 | E2 and E4 are escalated differently. | 6 | carried | 'they are escalated differently' in `merged.md` -- Directly stated. |
| 6 | To clear E2 in the field, you free the pin with the service key. | 11 | carried | 'Free the pin with the service key' in `merged.md` -- Directly stated. |
| 7 | To clear E2 in the field, you cycle the dock twice. | 11 | carried | 'cycle the dock twice' in `merged.md` -- Directly stated. |
| 8 | If the dock takes a bike and releases it on both cycles, you close the fault on your handheld. | 11 | carried | 'If the dock takes a bike and releases it on both cycles, close the fault on your handheld.' in `merged.md` -- Directly stated. |
| 9 | E2 is escalated to the workshop after 2 failed attempts. | 16 | carried | 'Escalate E2 to the workshop after 2 failed attempts' in `merged.md` -- Directly stated. |
| 10 | You should not keep cycling a dock that has failed twice. | 16 | carried | 'do not keep cycling a dock that has failed twice' in `merged.md` -- Directly stated. |
| 11 | Repeated forcing bends the pin. | 17 | carried | 'repeated forcing bends the pin' in `merged.md` -- Directly stated. |
| 12 | Repeated forcing turns a 20 minute workshop job into a replacement. | 17 | carried | 'turns a 20 minute workshop job into a replacement' in `merged.md` -- Directly stated. |
| 13 | E4 is never a field fix. | 20 | carried | 'E4 is never a field fix' in `merged.md` -- Directly stated as a heading and confirmed in body. |
| 14 | E4 is reported to the electrical contractor the same day. | 22 | carried | 'Report E4 to the electrical contractor the same day.' in `merged.md` -- Directly stated. |
| 15 | Field crew do not open the power enclosure under any circumstances. | 22 | carried | 'Field crew do not open the power enclosure under any circumstances.' in `merged.md` -- Directly stated. |
| 16 | A station with more than half its docks faulted is taken out of service in the app. | 27 | carried | 'A station with more than half its docks faulted is taken out of service in the app.' in `merged.md` -- Directly stated. |
| 17 | The support desk is told before taking a station out of service, not after. | 28 | carried | 'Tell the support desk before you do this, not after.' in `merged.md` -- Directly stated. |

### `source_b.md` -- 12 claim(s): 0 dropped, 2 contradicted, 0 carried in part, 10 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 7 | If the field crew have already tried 3 times, an E2 is raised to the workshop instead. | 15 | contradicted | 'Escalate E2 to the workshop after 2 failed attempts' in `merged.md` -- Text states 2 failed attempts, not 3. |
| 12 | The support desk takes a station out of service in the app when more than half its docks are faulted. | 30 | contradicted | 'A station with more than half its docks faulted is taken out of service in the app. Tell the support desk before you do this, not after.' in `merged.md` -- The field crew takes the station out of service and merely tells the support desk beforehand, not the support desk itself. |
| 1 | Riders call about bikes that will not release. | 5 | carried | 'Riders call about bikes that will not release' in `merged.md` -- Directly stated. |
| 2 | Riders call about bikes that will not lock. | 5 | carried | 'bikes that will not lock' in `merged.md` -- Directly stated. |
| 3 | Bikes that will not release and bikes that will not lock usually mean a dock fault rather than a bike fault. | 5 | carried | 'both usually indicate a dock fault rather than a bike fault' in `merged.md` -- Directly stated. |
| 4 | E2 is a jammed locking pin. | 10 | carried | 'A dock showing E2 has a jammed locking pin.' in `merged.md` -- Directly stated. |
| 5 | E4 is a loss of power to the point. | 11 | carried | 'A dock showing E4 has lost power to the point.' in `merged.md` -- Same meaning as loss of power to the point. |
| 6 | An E2 is raised to the field crew. | 15 | carried | 'Support desk raises an E2 fault to the field crew.' in `merged.md` -- Directly stated. |
| 8 | An E4 is raised to the electrical contractor the same day. | 20 | carried | 'Report E4 to the electrical contractor the same day.' in `merged.md` -- Directly stated as raised/reported to the electrical contractor same day. |
| 9 | A rider charged for a journey that ended at a faulted dock gets the journey refunded. | 24 | carried | 'A rider charged for a journey that ended at a faulted dock gets the journey refunded.' in `merged.md` -- Directly stated. |
| 10 | The refund is given at the time of the call. | 25 | carried | 'Refund at the time of the call' in `merged.md` -- Directly stated. |
| 11 | The refund does not wait for the fault to be confirmed. | 25 | carried | 'do not wait for the fault to be confirmed' in `merged.md` -- Directly stated. |

### `merged.md` -- 24 claim(s): 0 invented, 0 contradicted, 0 supported in part, 24 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Riders call about bikes that will not release. | supported | `source_b.md` | 'Riders call about bikes that will not release' in `source_b.md` -- Source_b states this directly. |
| 2 | Riders call about bikes that will not lock. | supported | `source_b.md` | 'and bikes that will not lock' in `source_b.md` -- Source_b states this directly. |
| 3 | Bikes that will not release or will not lock usually indicate a dock fault rather than a bike fault. | supported | `source_b.md` | 'Both usually mean a dock fault rather than a bike fault.' in `source_b.md` -- Source_b states this generalization directly. |
| 4 | The rider should be asked to read the fault code from the dock display. | supported | `source_b.md` | 'Ask the rider to read the code on the dock display.' in `source_b.md` -- Matches source_b's instruction directly. |
| 5 | A dock showing E2 has a jammed locking pin. | supported | `source_a.md` | 'A dock showing E2 has a jammed locking pin.' in `source_a.md` -- Stated directly in source_a. |
| 6 | A dock showing E4 has lost power to the point. | supported | `source_a.md` | 'A dock showing E4 has lost power to the point.' in `source_a.md` -- Stated directly in source_a. |
| 7 | E2 is a mechanical fault. | supported | `source_a.md` | 'E2 is a mechanical fault' in `source_a.md` -- Stated directly in source_a. |
| 8 | E4 is an electrical fault. | supported | `source_a.md` | 'E4 is an electrical one' in `source_a.md` -- Stated directly in source_a, meaning E4 is electrical fault. |
| 9 | E2 and E4 are escalated differently. | supported | `source_a.md` | 'they are\nescalated differently' in `source_a.md` -- Stated directly in source_a. |
| 10 | The pin should be freed with the service key. | supported | `source_a.md` | 'Free the pin with the service key' in `source_a.md` -- Stated directly in source_a. |
| 11 | The dock should be cycled twice after freeing the pin. | supported | `source_a.md` | 'cycle the dock twice' in `source_a.md` -- Stated directly in source_a. |
| 12 | If the dock takes a bike and releases it on both cycles, the fault should be closed on the handheld. | supported | `source_a.md` | 'If the dock takes a bike and releases it on both cycles, close the fault on your handheld.' in `source_a.md` -- Stated directly in source_a. |
| 13 | Support desk raises an E2 fault to the field crew. | supported | `source_b.md` | 'Raise an E2 to the field crew.' in `source_b.md` -- Stated directly in source_b. |
| 14 | E2 should be escalated to the workshop after 2 failed attempts. | supported | `source_a.md` | 'Escalate E2 to the workshop after 2 failed attempts.' in `source_a.md` -- Stated directly in source_a; single-source support suffices. |
| 15 | A dock that has failed twice should not keep being cycled. | supported | `source_a.md` | 'Do not keep cycling a dock\nthat has failed twice' in `source_a.md` -- Stated directly in source_a. |
| 16 | Repeated forcing bends the pin. | supported | `source_a.md` | 'repeated forcing bends the pin' in `source_a.md` -- Stated directly in source_a. |
| 17 | Repeated forcing turns a 20 minute workshop job into a replacement. | supported | `source_a.md` | 'turns a 20 minute workshop job into a replacement' in `source_a.md` -- Stated directly in source_a. |
| 18 | E4 should be reported to the electrical contractor the same day. | supported | `source_a.md` | 'Report E4 to the electrical contractor the same day.' in `source_a.md` -- Stated directly in source_a, also matched in source_b. |
| 19 | Field crew do not open the power enclosure under any circumstances. | supported | `source_a.md` | 'Field crew do not open the\npower enclosure under any circumstances.' in `source_a.md` -- Stated directly in source_a. |
| 20 | A rider charged for a journey that ended at a faulted dock gets the journey refunded. | supported | `source_b.md` | 'A rider charged for a journey that ended at a faulted dock gets the journey\nrefunded.' in `source_b.md` -- Stated directly in source_b. |
| 21 | Refund should occur at the time of the call. | supported | `source_b.md` | 'Refund at the time of the call' in `source_b.md` -- Stated directly in source_b. |
| 22 | The refund should not wait for the fault to be confirmed. | supported | `source_b.md` | 'do not wait for the fault to be\nconfirmed' in `source_b.md` -- Stated directly in source_b. |
| 23 | A station with more than half its docks faulted is taken out of service in the app. | supported | `source_a.md` | 'A station with more than half its docks faulted is taken out of service in the\napp.' in `source_a.md` -- Stated directly in source_a, matched in source_b. |
| 24 | The support desk should be told before taking a station out of service, not after. | supported | `source_a.md` | 'Tell the support desk before you do this, not after.' in `source_a.md` -- Stated directly in source_a. |

## Structure

**9** mechanical check(s) over **35** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **24** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **29**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 7 run(s) over 22 attributed segment(s) — sources interleaved. 9 of 13 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

`[-...-]` is what the source said and `{+...+}` is what the merge says.

### Absent and undeclared — in a source, not in the merge, and no record explains it

- `a10` (`source_a.md`) — 'Escalate E2 to the workshop after 2 failed attempts.' is not in the merge and no disposition record explains it (nearest merge segment m13 at 0.43)

  ```text
  In the source: Escalate E2 to the workshop after 2 failed attempts.
  ```

### Reworded and undeclared — in the merge in altered wording, and no record explains it. At off this also covers layout: a segment whose source line breaks the merge ran together is altered and undeclared, and 380 reuses this kind rather than moving FINDING_KINDS off 12

- `a11` (`source_a.md`) — 'Do not keep cycling a dock that has failed twice; repeated forcing bends the pin and turns a 20 minute workshop job into a replacement.' is reworded in the merge and no disposition record explains it (nearest merge segment m14 at 0.81)

  ```text
  In the source: Do not keep cycling a dock that has failed twice; repeated forcing bends the pin and turns a 20 minute workshop job into a replacement.
  In the merge:  Escalate E2 to the workshop after 2 failed attempts; do not keep cycling a dock that has failed twice, since repeated forcing bends the pin and turns a 20 minute workshop job into a replacement.
  What changed:  [-Do-] {+Escalate E2 to the workshop after 2 failed attempts; do+} not keep cycling a dock that has failed [-twice;-] {+twice, since+} repeated forcing bends the pin and turns a 20 minute workshop job into a replacement.
  ```

### Unresolved replacement — a record points at text the merge does not contain

- `b10` — segment b10 is declared 'superseded' with replacement 'Escalate E2 to the workshop after 2 failed attempts.', which is not in the merged document

  ```text
  In the merge: Escalate E2 to the workshop after 2 failed attempts.
  ```
- `b11` — segment b11 is declared 'superseded' with replacement 'Escalate E2 to the workshop after 2 failed attempts.', which is not in the merged document

  ```text
  In the merge: Escalate E2 to the workshop after 2 failed attempts.
  ```

### Verbatim violation — an invariant-core token did not survive unchanged

- `b10` (`source_b.md`) — numeric '3' (times) does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **15** departure(s) from its sources. Checking them confirms 7, rejects 1, and leaves 7 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 35 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | Base title chosen over this one. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Dock Fault Escalation - Field Crew' and says so (no claim traced to it) |
| `b2` | duplicate | Same heading text used as-is for the new section. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b3` | subsumed | Combined with b4 into one sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-001`, `B-002`) |
| `b4` | subsumed | Combined with b3 into one sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-003`) |
| `b5` | superseded | Base heading kept for the consolidated section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b6` | reworded | Same instruction, moved into riders section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b7` | duplicate | Same fault definitions already stated in a3/a4. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-004`, `B-005`) |
| `b8` | superseded | Base heading kept for the consolidated section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b9` | reworded | Same routing fact, reworded to fit the section. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-006`) |
| `b10` | superseded | Conflicting attempt count; base's 2 attempts chosen instead. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b11` | superseded | Conflicting attempt count; base's 2 attempts chosen instead. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b12` | superseded | Base heading kept for the consolidated section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b13` | duplicate | Same fact as a13, already stated. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-008`) |
| `b17` | superseded | Base heading kept for the consolidated section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b18` | duplicate | Same fact as a16, already stated. | **rejected** | declared 'duplicate', which predicts SUPPORTED; B-012 came back CONTRADICTED (`B-012`) |


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
| Duration | 149.9s |
| Generated | 2026-09-27T15:42:52+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup sonnet-5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
