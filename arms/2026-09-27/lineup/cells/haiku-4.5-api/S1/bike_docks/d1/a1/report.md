## Verdict

**Inconclusive.** 1 unit(s) of work errored (title). The model could not be made to answer usably, so this run does not establish that the claims it did check are the only ones there were. Of what could be graded, 6 finding(s); see below. That total is over the graded part only.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 14 |
| Claims extracted from `source_a.md` | 14 |
| Claims extracted from `source_b.md` | 11 |
| Forward — source claims accounted for in the merge | **20/25** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **14/14** |
| Forward — `source_b.md` claims accounted for | **6/11** |
| Reverse — merge claims found in a source | **12/14** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **34/34** |
| Units of work errored | 1 |
| Claims submitted but not graded | 0 |

> **title errored.** verify: model did not return a usable response after 5 attempts: response does not match the schema: no verdict for claim title; return exactly one verdict for every claim id you were given
  raw response written to <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-27-release-lineup/cells/haiku-4.5-api/S1/bike_docks/d1/a1/cache/failures/20260927T154132Z-verify-0005-attempt5.txt

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **B-011** -- the two documents disagree
  - `source_b.md:30` says: The support desk takes a station out of service in the app when more than half its docks are faulted.
  - `merged.md` says: 'A station with more than half its docks faulted is taken out of service in the app. Tell the support desk before you do this, not after.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text indicates the field crew takes the station out of service, not the support desk.
- **M-008** -- the two documents disagree
  - `merged.md:15` says: If the field crew have already tried 3 times, raise E2 to the workshop.
  - `source_b.md` says: 'If the field crew have already tried 3 times, raise it to the workshop instead.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: source_a.md says escalate after 2 failed attempts; source_b.md says after 3 times. The claim matches source_b.md, contradicting source_a.md.

### Invented — in the merge, in neither source

- **M-012** (`merged.md:23`) — Tell the support desk before you take a station out of service, not after.
  - judged against: `source_a.md` and `source_b.md`
  - rationale: source_a.md instructs field crew to tell support desk before taking a station out of service, but source_b.md describes support desk taking stations out of service. No source addresses who tells whom in the support desk context.

## Length capped

- `$.dispositions[17].reason` was 81 characters, over the 80-character cap; capped to fit
- `$.decisions[0].reason` was 99 characters, over the 80-character cap; capped to fit

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 14 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 14 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | A dock showing E2 has a jammed locking pin. | 5 | carried | 'A dock showing E2 has a jammed locking pin.' in `merged.md` -- The reference text directly states this claim in the opening sentence of the Fault codes section. |
| 2 | A dock showing E4 has lost power to the point. | 5 | carried | 'A dock showing E4 has lost power to the point.' in `merged.md` -- The reference text directly states this claim in the opening sentence of the Fault codes section. |
| 3 | E2 is a mechanical fault. | 6 | carried | 'E2 is a mechanical fault' in `merged.md` -- The reference text explicitly states that E2 is a mechanical fault in the first paragraph. |
| 4 | E4 is an electrical fault. | 6 | carried | 'E4 is an electrical one' in `merged.md` -- The reference text explicitly states that E4 is an electrical fault in the first paragraph. |
| 5 | E2 and E4 are escalated differently. | 6 | carried | 'they are escalated differently' in `merged.md` -- The reference text states that E2 and E4 are escalated differently in the first paragraph. |
| 6 | Free the pin with the service key and cycle the dock twice to clear E2 in the field. | 11 | carried | 'Free the pin with the service key and cycle the dock twice.' in `merged.md` -- The reference text provides this exact procedure under the 'Clearing E2 in the field' section. |
| 7 | If the dock takes a bike and releases it on both cycles, close the fault on your handheld. | 11 | carried | 'If the dock takes a bike and releases it on both cycles, close the fault on your handheld.' in `merged.md` -- The reference text states this condition and action in the Clearing E2 in the field section. |
| 8 | Escalate E2 to the workshop after 2 failed attempts. | 16 | carried | 'Escalate E2 to the workshop after 2 failed attempts.' in `merged.md` -- The reference text explicitly states this escalation rule in the 'When to escalate E2' section. |
| 9 | Repeated forcing of a dock that has failed twice bends the pin and turns a 20 minute workshop job into a replacement. | 17 | carried | 'repeated forcing bends the pin and turns a 20 minute workshop job into a replacement' in `merged.md` -- The reference text states this consequence in the 'When to escalate E2' section. |
| 10 | E4 is never a field fix. | 20 | carried | 'E4 is never a field fix' in `merged.md` -- The reference text uses this exact phrase as the heading of the E4 section. |
| 11 | Report E4 to the electrical contractor the same day. | 22 | carried | 'Report E4 to the electrical contractor the same day.' in `merged.md` -- The reference text states this action in the E4 section. |
| 12 | Field crew do not open the power enclosure under any circumstances. | 22 | carried | 'Field crew do not open the power enclosure under any circumstances.' in `merged.md` -- The reference text explicitly states this restriction in the E4 section. |
| 13 | A station with more than half its docks faulted is taken out of service in the app. | 27 | carried | 'A station with more than half its docks faulted is taken out of service in the app.' in `merged.md` -- The reference text states this rule in the 'Taking a station out of service' section. |
| 14 | Tell the support desk before you take a station out of service, not after. | 28 | carried | 'Tell the support desk before you do this, not after.' in `merged.md` -- The reference text explicitly states this timing requirement in the 'Taking a station out of service' section. |

### `source_b.md` -- 11 claim(s): 4 dropped, 1 contradicted, 0 carried in part, 6 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Riders call about bikes that will not release. | 5 | dropped | The reference text does not mention riders calling about bikes that will not release. |
| 2 | Riders call about bikes that will not lock. | 5 | dropped | The reference text does not mention riders calling about bikes that will not lock. |
| 3 | Bikes that will not release usually mean a dock fault rather than a bike fault. | 5 | dropped | The reference text does not address whether bike release issues usually indicate dock faults. |
| 4 | Bikes that will not lock usually mean a dock fault rather than a bike fault. | 5 | dropped | The reference text does not address whether bike locking issues usually indicate dock faults. |
| 11 | The support desk takes a station out of service in the app when more than half its docks are faulted. | 30 | contradicted | 'A station with more than half its docks faulted is taken out of service in the app. Tell the support desk before you do this, not after.' in `merged.md` -- The reference text indicates the field crew takes the station out of service, not the support desk. |
| 5 | E2 is a jammed locking pin. | 10 | carried | 'A dock showing E2 has a jammed locking pin.' in `merged.md` -- This claim restates the definition of E2 that appears in the reference text. |
| 6 | E4 is a loss of power to the point. | 11 | carried | 'A dock showing E4 has lost power to the point.' in `merged.md` -- This claim restates the definition of E4 that appears in the reference text. |
| 7 | If the field crew have already tried 3 times an E2, raise it to the workshop instead. | 15 | carried | 'If the field crew have already tried 3 times, raise it to the workshop instead.' in `merged.md` -- The reference text states this rule in the 'When to escalate E2' section. |
| 8 | Raise an E4 to the electrical contractor the same day. | 20 | carried | 'Report E4 to the electrical contractor the same day.' in `merged.md` -- This claim matches the escalation action stated for E4 in the reference text. |
| 9 | A rider charged for a journey that ended at a faulted dock gets the journey refunded. | 24 | carried | 'A rider charged for a journey that ended at a faulted dock gets the journey refunded.' in `merged.md` -- The reference text states this refund policy in the 'Rider refunds' section. |
| 10 | Refund at the time of the call; do not wait for the fault to be confirmed. | 25 | carried | 'Refund at the time of the call; do not wait for the fault to be confirmed.' in `merged.md` -- The reference text states this timing requirement in the 'Rider refunds' section. |

### `merged.md` -- 14 claim(s): 1 invented, 1 contradicted, 0 supported in part, 12 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 12 | Tell the support desk before you take a station out of service, not after. | invented | -- | source_a.md instructs field crew to tell support desk before taking a station out of service, but source_b.md describes support desk taking stations out of service. No source addresses who tells whom in the support desk context. |
| 8 | If the field crew have already tried 3 times, raise E2 to the workshop. | contradicted | `source_b.md` | 'If the field crew have already tried 3 times, raise it to the workshop instead.' in `source_b.md` -- source_a.md says escalate after 2 failed attempts; source_b.md says after 3 times. The claim matches source_b.md, contradicting source_a.md. |
| 1 | A dock showing E2 has a jammed locking pin. | supported | `source_a.md` | 'A dock showing E2 has a jammed locking pin.' in `source_a.md` -- source_a.md states this directly in the section on fault codes, and source_b.md confirms it with identical wording. |
| 2 | A dock showing E4 has lost power to the point. | supported | `source_a.md` | 'A dock showing E4 has lost power to the point.' in `source_a.md` -- source_a.md states this directly, and source_b.md confirms it with identical wording. |
| 3 | E2 is a mechanical fault. | supported | `source_a.md` | 'E2 is a mechanical fault' in `source_a.md` -- source_a.md explicitly states this in the fault codes section. |
| 4 | E4 is an electrical fault. | supported | `source_a.md` | 'E4 is an electrical one' in `source_a.md` -- source_a.md states E4 is an electrical fault in the fault codes section. |
| 5 | E2 and E4 are escalated differently. | supported | `source_a.md` | 'E2 is a mechanical fault and E4 is an electrical one, and they are escalated differently.' in `source_a.md` -- source_a.md explicitly states that E2 and E4 are escalated differently. |
| 6 | Escalate E2 to the workshop after 2 failed attempts. | supported | `source_a.md` | 'Escalate E2 to the workshop after 2 failed attempts.' in `source_a.md` -- source_a.md states this directly in the section on when to escalate E2. |
| 7 | Repeated forcing of a dock that has failed twice bends the pin and turns a 20 minute workshop job into a replacement. | supported | `source_a.md` | 'repeated forcing bends the pin and turns a 20 minute workshop job into a replacement.' in `source_a.md` -- source_a.md states this consequence of repeated forcing in the escalation section. |
| 9 | Report E4 to the electrical contractor the same day. | supported | `source_a.md` | 'Report E4 to the electrical contractor the same day.' in `source_a.md` -- source_a.md states this in the section on E4 field handling, matching source_b.md's wording. |
| 10 | Field crew do not open the power enclosure under any circumstances. | supported | `source_a.md` | 'Field crew do not open the power enclosure under any circumstances.' in `source_a.md` -- source_a.md explicitly states this prohibition in the E4 section. |
| 11 | A station with more than half its docks faulted is taken out of service in the app. | supported | `source_a.md` | 'A station with more than half its docks faulted is taken out of service in the app.' in `source_a.md` -- source_a.md states this, and source_b.md confirms it with identical wording. |
| 13 | A rider charged for a journey that ended at a faulted dock gets the journey refunded. | supported | `source_b.md` | 'A rider charged for a journey that ended at a faulted dock gets the journey refunded.' in `source_b.md` -- source_b.md states this directly in the Refunds section. |
| 14 | Refund the journey at the time of the call; do not wait for the fault to be confirmed. | supported | `source_b.md` | 'Refund at the time of the call; do not wait for the fault to be confirmed.' in `source_b.md` -- source_b.md states this instruction directly in the Refunds section. |

## Structure

**9** mechanical check(s) over **35** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **14** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **25**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 4 run(s) over 20 attributed segment(s) — sources interleaved. 8 of 13 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Absent and undeclared — in a source, not in the merge, and no record explains it

- `b8` (`source_b.md`) — 'Escalating E2' is not in the merge and no disposition record explains it (nearest merge segment m9 at 0.62)

  ```text
  In the source: Escalating E2
  ```

### Over budget — declared loss past the ceiling

- 6 of 35 segments are declared dropped (17.1%), over the 3% budget

### Title dropped in silence — a source title is gone and no record names what replaced it

- `a1` (`source_a.md`) — source title 'Dock Fault Escalation - Field Crew' is not the merged title and carries a 'reworded' record; every title not taken needs a superseded record naming what replaced it

## Review queue

**4** claim(s) the merge declared dropped and the forward pass confirms are gone. Each is a decision to review — put the fact back, or agree it stays out — and none of them is counted as a finding above.

- **B-001** (`source_b.md:5`) — Riders call about bikes that will not release.
  - left out of: `b3`
  - the merge's reason: Rider-facing content not relevant to merged fault escalation guide.
  - confirmed absent: the forward pass looked for this claim in `merged.md` and did not find it -- The reference text does not mention riders calling about bikes that will not release.
- **B-002** (`source_b.md:5`) — Riders call about bikes that will not lock.
  - left out of: `b3`
  - the merge's reason: Rider-facing content not relevant to merged fault escalation guide.
  - confirmed absent: the forward pass looked for this claim in `merged.md` and did not find it -- The reference text does not mention riders calling about bikes that will not lock.
- **B-003** (`source_b.md:5`) — Bikes that will not release usually mean a dock fault rather than a bike fault.
  - left out of: `b4`
  - the merge's reason: Distinction between bike and dock faults not essential to escalation procedures.
  - confirmed absent: the forward pass looked for this claim in `merged.md` and did not find it -- The reference text does not address whether bike release issues usually indicate dock faults.
- **B-004** (`source_b.md:5`) — Bikes that will not lock usually mean a dock fault rather than a bike fault.
  - left out of: `b4`
  - the merge's reason: Distinction between bike and dock faults not essential to escalation procedures.
  - confirmed absent: the forward pass looked for this claim in `merged.md` and did not find it -- The reference text does not address whether bike locking issues usually indicate dock faults.

> **Over budget.** The merge declared **6** drop(s) of 35 source segment(s), **17.1%**, over the 3% budget: past that share the omissions are the finding, whatever each one says about itself.

## Declarations

The merge declared **18** departure(s) from its sources. Checking them confirms 11, rejects 3, and leaves 4 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 6 of 35 source segment(s) declared gone, **17.1%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a1` | reworded | Title changed to cover both field crew and support desk audiences. | **rejected** | no claim is drawn from a title, and the title check rejected this one: it is not the merged title and its 'reworded' record does not name the title that replaced it (no claim traced to it) |
| `b1` | superseded | Base document title was adapted; this source title was not used. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Dock Fault Escalation' and says so (no claim traced to it) |
| `b2` | dropped | Heading 'What riders report' serves no purpose in merged scope. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b3` | dropped | Rider-facing content not relevant to merged fault escalation guide. | **confirmed** | declared 'dropped' and every claim from it came back MISSING (`B-001`, `B-002`) |
| `b4` | dropped | Distinction between bike and dock faults not essential to escalation procedures. | **confirmed** | declared 'dropped' and every claim from it came back MISSING (`B-003`, `B-004`) |
| `b5` | dropped | Support desk heading 'Reading the fault code' superseded by field procedures. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b6` | dropped | Instruction to ask rider for code not relevant to field crew guide. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b7` | duplicate | Same fault code definitions already stated in merged document. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-005`, `B-006`) |
| `b9` | subsumed | Field crew escalation procedure subsumed in escalation section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b10` | reconciled | Support desk threshold of 3 attempts combined with field crew's 2-attempt rule. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `a10` | reconciled | Field crew 2-attempt threshold and support desk 3-attempt threshold reconciled. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-008`) |
| `b12` | superseded | Field crew language used; support desk phrasing was not retained. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b13` | duplicate | Same escalation requirement already in merged document. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-008`) |
| `b14` | dropped | Heading 'Refunds' created; support desk section moved to new section. | **rejected** | declared 'dropped', and its text is in the merge (no claim traced to it) |
| `b15` | reworded | Phrasing simplified; content preserved in new Rider refunds section. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-009`) |
| `b16` | reworded | Content preserved in new Rider refunds section. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-010`) |
| `b17` | subsumed | Support desk action subsumed in field crew instruction to notify support desk. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b18` | duplicate | Same station out-of-service condition already stated from field crew perspective | **rejected** | declared 'duplicate', which predicts SUPPORTED; B-011 came back CONTRADICTED (`B-011`) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | ec0c9ecb43e3 (hosted) |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | claude-haiku-4-5-20251001 |
| Model (decompose) | claude-haiku-4-5-20251001 |
| Model (verify) | claude-haiku-4-5-20251001 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile anthropic, effort decompose one level (extended thinking on/off; default kept), merge one level (extended thinking on/off; default kept), verify one level (extended thinking on/off; default kept) |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 12 live, 0 cached, 0 replayed |
| Tokens | 32,777 in, 9,590 out |
| Cost | ~$0.08 estimated (rates read 2026-08-31) |
| Schema repairs | 1 |
| Errors | 1 |
| Duration | 75.0s |
| Generated | 2026-09-27T15:42:25+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **1 unit(s) of work errored.** The model could not be made to answer in a usable form. This run is inconclusive: coverage below is computed over the units that did answer, and the exit code is 2 regardless of what they said.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
