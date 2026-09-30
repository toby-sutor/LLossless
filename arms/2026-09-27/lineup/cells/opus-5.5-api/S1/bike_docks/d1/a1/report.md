## Verdict

**4 finding(s).** In the claims: 1 partially dropped, 3 contradicted.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 25 |
| Claims extracted from `source_a.md` | 16 |
| Claims extracted from `source_b.md` | 13 |
| Forward — source claims accounted for in the merge | **26/29** |
| Forward — carried only in part | 1 |
| Forward — `source_a.md` claims accounted for | **16/16** |
| Forward — `source_b.md` claims accounted for | **10/13** (1 in part) |
| Reverse — merge claims found in a source | **24/25** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **54/54** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Partly dropped — the merge carries some of this claim

- **B-012** (`source_b.md:25`) — The support desk does not wait for the fault to be confirmed before refunding.
  - evidence: 'do not wait for the fault to be confirmed' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The instruction not to wait for fault confirmation is stated, but the reference text never says the support desk is the party that issues refunds.

### Contradicted — the merge states something different

- **B-008** -- the two documents disagree
  - `source_b.md:15` says: If the field crew have already tried 3 times on an E2 fault, the fault is raised to the workshop instead.
  - `merged.md` says: 'Escalate E2 to the workshop after 2 failed attempts.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text sets the escalation threshold at 2 failed attempts, not 3.
- **B-013** -- the two documents disagree
  - `source_b.md:30` says: The support desk takes a station out of service in the app when more than half its docks are faulted.
  - `merged.md` says: 'Tell the support desk before you do this, not after.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text has the field crew take the station out of service after telling the support desk, which is incompatible with the support desk doing it.
- **M-014** -- the two documents disagree
  - `merged.md:17` says: E2 is escalated to the workshop after 2 failed attempts.
  - `source_b.md` says: 'If the field crew have already tried 3 times,\nraise it to the workshop instead.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source A says 2 failed attempts but source B says 3, and the claim states 2 without reporting the disagreement.

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
| 1 | A dock showing E2 has a jammed locking pin. | 5 | carried | 'A dock showing E2 has a jammed locking pin.' in `merged.md` -- The reference text states this verbatim. |
| 2 | A dock showing E4 has lost power to the point. | 5 | carried | 'A dock showing E4 has lost power to the point.' in `merged.md` -- The reference text states this verbatim. |
| 3 | E2 is a mechanical fault. | 6 | carried | 'E2 is a mechanical fault' in `merged.md` -- The reference text states that E2 is a mechanical fault. |
| 4 | E4 is an electrical fault. | 6 | carried | 'E4 is an electrical one' in `merged.md` -- The reference text states that E4 is an electrical fault. |
| 5 | E2 and E4 are escalated differently. | 6 | carried | 'so the two are escalated differently' in `merged.md` -- The reference text states that E2 and E4 are escalated differently. |
| 6 | To clear E2 in the field, free the pin with the service key and cycle the dock twice. | 11 | carried | 'Free the pin with the service key and cycle the dock twice.' in `merged.md` -- This instruction appears under the heading about clearing E2 in the field. |
| 7 | If the dock takes a bike and releases it on both cycles, the fault is closed on the handheld. | 11 | carried | 'If the dock takes a bike and releases it on both cycles, close the fault on your handheld.' in `merged.md` -- The reference text states the same condition and action. |
| 8 | E2 is escalated to the workshop after 2 failed attempts. | 16 | carried | 'Escalate E2 to the workshop after 2 failed attempts.' in `merged.md` -- The reference text states this directly. |
| 9 | A dock that has failed twice should not keep being cycled. | 16 | carried | 'Do not keep cycling a dock that has failed twice' in `merged.md` -- The reference text states this directly. |
| 10 | Repeated forcing bends the pin. | 17 | carried | 'repeated forcing bends the pin' in `merged.md` -- The reference text states this directly. |
| 11 | Repeated forcing turns a 20 minute workshop job into a replacement. | 17 | carried | 'turns a 20 minute workshop job into a replacement' in `merged.md` -- The reference text states that repeated forcing has this effect. |
| 12 | E4 is never a field fix. | 20 | carried | 'E4 is never a field fix' in `merged.md` -- The section heading states this. |
| 13 | E4 is reported to the electrical contractor the same day. | 22 | carried | 'Report E4 to the electrical contractor the same day.' in `merged.md` -- The reference text states this directly. |
| 14 | Field crew do not open the power enclosure under any circumstances. | 22 | carried | 'Field crew do not open the power enclosure under any circumstances.' in `merged.md` -- The reference text states this verbatim. |
| 15 | A station with more than half its docks faulted is taken out of service in the app. | 27 | carried | 'A station with more than half its docks faulted is taken out of service in the app.' in `merged.md` -- The reference text states this verbatim. |
| 16 | The support desk must be told before a station is taken out of service, not after. | 28 | carried | 'Tell the support desk before you do this, not after.' in `merged.md` -- The reference text requires telling the support desk before taking a station out of service. |

### `source_b.md` -- 13 claim(s): 0 dropped, 2 contradicted, 1 carried in part, 10 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 8 | If the field crew have already tried 3 times on an E2 fault, the fault is raised to the workshop instead. | 15 | contradicted | 'Escalate E2 to the workshop after 2 failed attempts.' in `merged.md` -- The reference text sets the escalation threshold at 2 failed attempts, not 3. |
| 13 | The support desk takes a station out of service in the app when more than half its docks are faulted. | 30 | contradicted | 'Tell the support desk before you do this, not after.' in `merged.md` -- The reference text has the field crew take the station out of service after telling the support desk, which is incompatible with the support desk doing it. |
| 12 | The support desk does not wait for the fault to be confirmed before refunding. | 25 | carried in part | 'do not wait for the fault to be confirmed' in `merged.md` -- The instruction not to wait for fault confirmation is stated, but the reference text never says the support desk is the party that issues refunds. |
| 1 | Riders call about bikes that will not release. | 5 | carried | 'Riders call about bikes that will not release' in `merged.md` -- The reference text states this directly. |
| 2 | Riders call about bikes that will not lock. | 5 | carried | 'bikes that will not lock' in `merged.md` -- The reference text states that riders call about bikes that will not lock. |
| 3 | Bikes that will not release or will not lock usually mean a dock fault rather than a bike fault. | 5 | carried | 'Both usually mean a dock fault rather than a bike fault.' in `merged.md` -- The reference text states that both cases usually mean a dock fault. |
| 4 | The support desk should ask the rider to read the code on the dock display. | 10 | carried | 'When a rider calls, the support desk asks the rider to read the code on the dock display.' in `merged.md` -- The reference text states that the support desk asks the rider to read the code. |
| 5 | Fault code E2 is a jammed locking pin. | 10 | carried | 'A dock showing E2 has a jammed locking pin.' in `merged.md` -- The reference text states the same meaning in different words. |
| 6 | Fault code E4 is a loss of power to the point. | 11 | carried | 'A dock showing E4 has lost power to the point.' in `merged.md` -- The reference text states the same meaning in different words. |
| 7 | An E2 fault is raised to the field crew. | 15 | carried | 'The support desk raises an E2 to the field crew.' in `merged.md` -- The reference text states that E2 is raised to the field crew. |
| 9 | An E4 fault is raised to the electrical contractor the same day. | 20 | carried | 'Report E4 to the electrical contractor the same day.' in `merged.md` -- The reference text states that E4 goes to the electrical contractor the same day. |
| 10 | A rider charged for a journey that ended at a faulted dock gets the journey refunded. | 24 | carried | 'A rider charged for a journey that ended at a faulted dock gets the journey refunded.' in `merged.md` -- The reference text states this claim word for word. |
| 11 | The refund is given at the time of the call. | 25 | carried | 'Refund at the time of the call' in `merged.md` -- The reference text instructs that the refund is made at the time of the call. |

### `merged.md` -- 25 claim(s): 0 invented, 1 contradicted, 0 supported in part, 24 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 14 | E2 is escalated to the workshop after 2 failed attempts. | contradicted | `source_b.md` | 'If the field crew have already tried 3 times,\nraise it to the workshop instead.' in `source_b.md` -- Source A says 2 failed attempts but source B says 3, and the claim states 2 without reporting the disagreement. |
| 1 | Riders call about bikes that will not release. | supported | `source_b.md` | 'Riders call about bikes that will not release and bikes that will not lock.' in `source_b.md` -- Source B states riders call about bikes that will not release. |
| 2 | Riders call about bikes that will not lock. | supported | `source_b.md` | 'Riders call about bikes that will not release and bikes that will not lock.' in `source_b.md` -- Source B states riders call about bikes that will not lock. |
| 3 | Bikes that will not release or will not lock usually mean a dock fault rather than a bike fault. | supported | `source_b.md` | 'Both\nusually mean a dock fault rather than a bike fault.' in `source_b.md` -- Source B states both complaints usually mean a dock fault rather than a bike fault. |
| 4 | A dock showing E2 has a jammed locking pin. | supported | `source_a.md` | 'A dock showing E2 has a jammed locking pin.' in `source_a.md` -- Source A states this verbatim. |
| 5 | A dock showing E4 has lost power to the point. | supported | `source_a.md` | 'A dock showing E4 has lost power to\nthe point.' in `source_a.md` -- Source A states this verbatim. |
| 6 | E2 is a mechanical fault. | supported | `source_a.md` | 'E2 is a mechanical fault and E4 is an electrical one' in `source_a.md` -- Source A states E2 is a mechanical fault. |
| 7 | E4 is an electrical fault. | supported | `source_a.md` | 'E2 is a mechanical fault and E4 is an electrical one' in `source_a.md` -- Source A states E4 is an electrical fault. |
| 8 | E2 and E4 faults are escalated differently. | supported | `source_a.md` | 'they are\nescalated differently' in `source_a.md` -- Source A states E2 and E4 are escalated differently. |
| 9 | When a rider calls, the support desk asks the rider to read the code on the dock display. | supported | `source_b.md` | 'Ask the rider to read the code on the dock display.' in `source_b.md` -- Source B, the support desk guide, instructs asking the rider to read the dock display code. |
| 10 | To clear E2 in the field, free the pin with the service key. | supported | `source_a.md` | 'Free the pin with the service key and cycle the dock twice.' in `source_a.md` -- Source A states freeing the pin with the service key to clear E2. |
| 11 | To clear E2 in the field, cycle the dock twice. | supported | `source_a.md` | 'Free the pin with the service key and cycle the dock twice.' in `source_a.md` -- Source A states cycling the dock twice to clear E2. |
| 12 | If the dock takes a bike and releases it on both cycles, close the fault on the handheld. | supported | `source_a.md` | 'If the dock takes a\nbike and releases it on both cycles, close the fault on your handheld.' in `source_a.md` -- Source A states this with minor rewording. |
| 13 | The support desk raises an E2 to the field crew. | supported | `source_b.md` | 'Raise an E2 to the field crew.' in `source_b.md` -- Source B, the support desk guide, states this. |
| 15 | Field crew should not keep cycling a dock that has failed twice. | supported | `source_a.md` | 'Do not keep cycling a dock\nthat has failed twice' in `source_a.md` -- Source A, the field crew guide, states this. |
| 16 | Repeated forcing of a dock bends the pin. | supported | `source_a.md` | 'repeated forcing bends the pin' in `source_a.md` -- Source A states repeated forcing bends the pin. |
| 17 | Repeated forcing turns a 20 minute workshop job into a replacement. | supported | `source_a.md` | 'turns a 20 minute\nworkshop job into a replacement' in `source_a.md` -- Source A states repeated forcing turns a 20 minute workshop job into a replacement. |
| 18 | E4 is never a field fix. | supported | `source_a.md` | 'E4 is never a field fix' in `source_a.md` -- Source A's section heading states this. |
| 19 | E4 is reported to the electrical contractor the same day. | supported | `source_a.md` | 'Report E4 to the electrical contractor the same day.' in `source_a.md` -- Source A states this, and source B agrees. |
| 20 | Field crew do not open the power enclosure under any circumstances. | supported | `source_a.md` | 'Field crew do not open the\npower enclosure under any circumstances.' in `source_a.md` -- Source A states this verbatim. |
| 21 | A rider charged for a journey that ended at a faulted dock gets the journey refunded. | supported | `source_b.md` | 'A rider charged for a journey that ended at a faulted dock gets the journey\nrefunded.' in `source_b.md` -- Source B states this verbatim. |
| 22 | Refunds are made at the time of the call. | supported | `source_b.md` | 'Refund at the time of the call' in `source_b.md` -- Source B states refunds are made at the time of the call. |
| 23 | Refunds do not wait for the fault to be confirmed. | supported | `source_b.md` | 'do not wait for the fault to be\nconfirmed' in `source_b.md` -- Source B states refunds do not wait for fault confirmation. |
| 24 | A station with more than half its docks faulted is taken out of service in the app. | supported | `source_a.md` | 'A station with more than half its docks faulted is taken out of service in the\napp.' in `source_a.md` -- Source A states this verbatim, and source B agrees. |
| 25 | The support desk must be told before a station is taken out of service, not after. | supported | `source_a.md` | 'Tell the support desk before you do this, not after.' in `source_a.md` -- Source A instructs field crew to tell the support desk before taking a station out of service. |

## Structure

**9** mechanical check(s) over **35** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **25** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **29**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 9 run(s) over 24 attributed segment(s) — sources interleaved. 9 of 13 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

No structural finding.

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **21** departure(s) from its sources. Checking them confirms 15, rejects 1, and leaves 5 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 35 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a4` | reworded | Line break removed to join the paragraph. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-002`) |
| `a5` | reworded | Line break removed and sentence lightly smoothed. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-003`, `A-004`, `A-005`) |
| `a8` | reworded | Line break removed to join the paragraph. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-007`) |
| `a11` | reworded | Line breaks removed to join the paragraph. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-009`, `A-010`, `A-011`) |
| `a14` | reworded | Line break removed to join the paragraph. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-014`) |
| `a16` | reworded | Line break removed to join the paragraph. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-015`) |
| `b1` | superseded | Base title kept; this title not taken. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Dock Fault Escalation - Field Crew' and says so (no claim traced to it) |
| `b4` | reworded | Line break removed to join the paragraph. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-003`) |
| `b5` | superseded | Section consolidated under the base heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b6` | reworded | Desk instruction rephrased to fit the shared fault code section. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-004`) |
| `b7` | duplicate | Code meanings already stated by the base. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-005`, `B-006`) |
| `b8` | superseded | Section consolidated under the base heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b9` | reworded | Actor made explicit in the shared section. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-007`) |
| `b10` | superseded | Threshold conflict resolved in favour of the base value. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b11` | superseded | Workshop escalation carried by the base sentence. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b12` | superseded | Section consolidated under the base heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b13` | duplicate | Same-day contractor escalation already stated by the base. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-009`) |
| `b15` | reworded | Line break removed to join the paragraph. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-010`) |
| `b16` | reworded | Line break removed to join the paragraph. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-012 came back PARTIAL (`B-012`) |
| `b17` | duplicate | Identical heading already present in the base. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b18` | superseded | Actor conflict resolved in favour of the base procedure. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-013`) |


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
| Tokens | 22,648 in, 12,780 out |
| Cost | ~$0.35 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 105.0s |
| Generated | 2026-09-27T15:44:11+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
