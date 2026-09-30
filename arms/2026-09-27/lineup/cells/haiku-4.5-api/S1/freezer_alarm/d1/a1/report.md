## Verdict

**11 finding(s).** In the claims: 1 dropped. In the structure: 4 undeclared absence, 4 false departure, 1 declared loss over budget, 1 title not superseded. The merge declared **1** drop(s) of 33 source segment(s), **3.0%**, over the 3% budget: past that share the omissions are the finding, whatever each one says about itself.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 16 |
| Claims extracted from `source_a.md` | 7 |
| Claims extracted from `source_b.md` | 9 |
| Forward — source claims accounted for in the merge | **15/16** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **7/7** |
| Forward — `source_b.md` claims accounted for | **8/9** |
| Reverse — merge claims found in a source | **16/16** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **31/31** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Dropped — in a source, not in the merge

- **B-001** (`source_b.md:5`) — The alarm panel names the unit and shows the temperature that triggered it.
  - judged against: `merged.md`
  - rationale: The reference text does not state that the alarm panel names the unit or shows the temperature that triggered it.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 7 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 7 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Each freezer alarms when the internal temperature rises above its set point for more than 10 minutes. | 5 | carried | 'Each freezer alarms when the internal temperature rises above its set point for more than 10 minutes.' in `merged.md` -- The reference text states this claim exactly. |
| 2 | The alarm sounds locally and sends a message to the night phone. | 6 | carried | 'The alarm sounds locally and sends a message to the night phone.' in `merged.md` -- The reference text states this claim exactly. |
| 3 | The reading at the moment of arrival is the one the lab needs and it cannot be recovered later. | 12 | carried | 'The reading at the moment of arrival is the one the lab needs and it cannot be recovered later.' in `merged.md` -- The reference text states this claim exactly. |
| 4 | If the door is ajar, closing the door and waiting 20 minutes will result in logging it as a door event if the temperature falls back below the set point and no further action is needed. | 17 | carried | 'Close the door and wait 20 minutes. If the temperature falls back below the set point, log it as a door event and no further action is needed.' in `merged.md` -- The reference text states all elements of this claim in sequence: closing the door, waiting 20 minutes, and the conditional outcome. |
| 5 | Opening a door on a failing freezer to check the contents is the most common cause of loss in this building. | 22 | carried | 'Opening a door on a failing freezer to check the contents is the most common cause of loss in this building.' in `merged.md` -- The reference text states this claim exactly. |
| 6 | Contents are moved only on the technician's instruction and only into a freezer that already has space at the same set point. | 28 | carried | "Contents are moved only on the technician's instruction and only into a freezer that already has space at the same set point." in `merged.md` -- The reference text states this claim exactly. |
| 7 | A single study's samples must never be split across two freezers. | 29 | carried | "Never split a single study's samples across two freezers." in `merged.md` -- The reference text states this claim, expressing the prohibition in different wording. |

### `source_b.md` -- 9 claim(s): 1 dropped, 0 contradicted, 0 carried in part, 8 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The alarm panel names the unit and shows the temperature that triggered it. | 5 | dropped | The reference text does not state that the alarm panel names the unit or shows the temperature that triggered it. |
| 2 | There are three units on this floor. | 6 | carried | 'there are three units on this floor' in `merged.md` -- The reference text states this claim exactly. |
| 3 | Two of the three units on this floor alarm at the same set point. | 6 | carried | 'there are three units on this floor and two of them alarm at the same set point' in `merged.md` -- The reference text states this claim exactly. |
| 4 | Ice on the seal holds the door open by a few millimetres. | 11 | carried | 'Ice on the seal holds the door open by a few millimetres' in `merged.md` -- The reference text states this claim exactly. |
| 5 | Ice on the seal is the usual cause of a slow rise. | 12 | carried | 'Ice on the seal holds the door open by a few millimetres and is the usual cause of a slow rise.' in `merged.md` -- The reference text states this claim exactly. |
| 6 | The on-call technician should be called if the temperature is still rising 20 minutes after arrival. | 16 | carried | 'Call the on-call technician if the temperature is still rising 20 minutes after you arrive.' in `merged.md` -- The reference text states this claim with equivalent meaning. |
| 7 | Every alarm gets a line in the freezer log whether or not anything was wrong. | 22 | carried | 'Every alarm gets a line in the freezer log whether or not anything was wrong.' in `merged.md` -- The reference text states this claim exactly. |
| 8 | An alarm with no line in the log is indistinguishable from an alarm nobody attended. | 22 | carried | 'An alarm with no line in the log is indistinguishable from an alarm nobody attended.' in `merged.md` -- The reference text states this claim exactly. |
| 9 | The night phone is carried by the weekend duty officer from 18:00 on Friday until 08:00 on Monday. | 27 | carried | 'The night phone is carried by the weekend duty officer from 18:00 on Friday until 08:00 on Monday.' in `merged.md` -- The reference text states this claim exactly. |

### `merged.md` -- 16 claim(s): 0 invented, 0 contradicted, 0 supported in part, 16 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Each freezer alarms when the internal temperature rises above its set point for more than 10 minutes. | supported | `source_a.md` | 'Each freezer alarms when the internal temperature rises above its set point for more than 10 minutes.' in `source_a.md` -- source_a.md states this claim directly in the section 'What triggers an alarm'. |
| 2 | The alarm sounds locally and sends a message to the night phone. | supported | `source_a.md` | 'The alarm sounds locally and sends a message to the night phone.' in `source_a.md` -- source_a.md states this claim directly in the section 'What triggers an alarm'. |
| 3 | There are three units on this floor. | supported | `source_b.md` | 'there are three units on this floor' in `source_b.md` -- source_b.md states 'there are three units on this floor and two of them alarm at the same set point'. |
| 4 | Two of the units on this floor alarm at the same set point. | supported | `source_b.md` | 'there are three units on this floor and two of them alarm at the same set point' in `source_b.md` -- source_b.md states this claim directly in the section 'Reading the alarm'. |
| 5 | Ice on the seal holds the door open by a few millimetres. | supported | `source_b.md` | 'Ice on the seal holds the door open by a few millimetres' in `source_b.md` -- source_b.md states this claim directly in the section 'Check the door seal'. |
| 6 | Ice on the seal is the usual cause of a slow rise. | supported | `source_b.md` | 'ice on the seal holds the door open by a few millimetres and is the usual cause of a slow rise' in `source_b.md` -- source_b.md states this claim directly in the section 'Check the door seal'. |
| 7 | After closing the door, one should wait 20 minutes. | supported | `source_a.md` | 'Close the door and wait 20 minutes.' in `source_a.md` -- source_a.md states this instruction in the section 'If the door is ajar'. |
| 8 | If the temperature falls back below the set point after 20 minutes, it should be logged as a door event. | supported | `source_a.md` | 'If the temperature falls back below the set point, log it as a door event and no further action is needed.' in `source_a.md` -- source_a.md states this claim in the section 'If the door is ajar'. |
| 9 | The on-call technician should be called if the temperature is still rising 20 minutes after arrival. | supported | `source_b.md` | 'Call the on-call technician if the temperature is still rising 20 minutes after you arrive.' in `source_b.md` -- source_b.md states this claim in the section 'Escalating'. |
| 10 | Opening a door on a failing freezer to check the contents is the most common cause of loss in this building. | supported | `source_a.md` | 'Opening a door on a failing freezer to check the contents is the most common cause of loss in this building.' in `source_a.md` -- source_a.md states this claim in the section 'If the temperature keeps rising'. |
| 11 | Every alarm gets a line in the freezer log whether or not anything was wrong. | supported | `source_b.md` | 'Every alarm gets a line in the freezer log whether or not anything was wrong.' in `source_b.md` -- source_b.md states this claim directly in the section 'Recording'. |
| 12 | An alarm with no line in the log is indistinguishable from an alarm nobody attended. | supported | `source_b.md` | 'An alarm with no line in the log is indistinguishable from an alarm nobody attended.' in `source_b.md` -- source_b.md states this claim directly in the section 'Recording'. |
| 13 | Contents are moved only on the technician's instruction. | supported | `source_a.md` | "Contents are moved only on the technician's instruction" in `source_a.md` -- source_a.md states this claim in the section 'Moving contents'. |
| 14 | Contents are moved only into a freezer that already has space at the same set point. | supported | `source_a.md` | 'only into a freezer that already has space at the same set point' in `source_a.md` -- source_a.md states this in the section 'Moving contents' regarding where contents may be moved. |
| 15 | A single study's samples must never be split across two freezers. | supported | `source_a.md` | "Never split a single study's samples across two freezers." in `source_a.md` -- source_a.md states this claim directly in the section 'Moving contents'. |
| 16 | The night phone is carried by the weekend duty officer from 18:00 on Friday until 08:00 on Monday. | supported | `source_b.md` | 'The night phone is carried by the weekend duty officer from 18:00 on Friday until 08:00 on Monday.' in `source_b.md` -- source_b.md states this claim directly in the section 'Weekend cover'. |

## Structure

**9** mechanical check(s) over **33** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **16** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **16**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 10 run(s) over 27 attributed segment(s) — sources interleaved. 8 of 12 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Absent and undeclared — in a source, not in the merge, and no record explains it

- `a13` (`source_a.md`) — 'Call the on-call technician.' is not in the merge and no disposition record explains it (nearest merge segment m16 at 0.47)

  ```text
  In the source: Call the on-call technician.
  ```
- `b1` (`source_b.md`) — 'Cold Storage Alarm Checklist' is not in the merge and no disposition record explains it (nearest merge segment m2 at 0.44)

  ```text
  In the source: Cold Storage Alarm Checklist
  ```
- `b2` (`source_b.md`) — 'Reading the alarm' is not in the merge and no disposition record explains it (nearest merge segment m11 at 0.53)

  ```text
  In the source: Reading the alarm
  ```
- `b8` (`source_b.md`) — 'Escalating' is not in the merge and no disposition record explains it (nearest merge segment m20 at 0.53)

  ```text
  In the source: Escalating
  ```

### Declared gone, still here — a record says the content departed and the merge carries the segment unchanged

- `b4` (`source_b.md`) — 'Note the unit name; there are three units on this floor and two of them alarm at the same set point.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Note the unit name; there are three units on this floor and two of them alarm at the same set point.
  In the merge:  Note the unit name; there are three units on this floor and two of them alarm at the same set point.
  ```
- `b9` (`source_b.md`) — 'Call the on-call technician if the temperature is still rising 20 minutes after you arrive.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Call the on-call technician if the temperature is still rising 20 minutes after you arrive.
  In the merge:  Call the on-call technician if the temperature is still rising 20 minutes after you arrive.
  ```
- `b10` (`source_b.md`) — 'Give the unit name, the reading you took on arrival and the reading now.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Give the unit name, the reading you took on arrival and the reading now.
  In the merge:  Give the unit name, the reading you took on arrival and the reading now.
  ```
- `b13` (`source_b.md`) — 'An alarm with no line in the log is indistinguishable from an alarm nobody attended.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: An alarm with no line in the log is indistinguishable from an alarm nobody attended.
  In the merge:  An alarm with no line in the log is indistinguishable from an alarm nobody attended.
  ```

### Over budget — declared loss past the ceiling

- 1 of 33 segments are declared dropped (3.0%), over the 3% budget

### Title dropped in silence — a source title is gone and no record names what replaced it

- `b1` (`source_b.md`) — source title 'Cold Storage Alarm Checklist' is not the merged title and carries no record; every title not taken needs a superseded record naming what replaced it

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

> **Over budget.** The merge declared **1** drop(s) of 33 source segment(s), **3.0%**, over the 3% budget: past that share the omissions are the finding, whatever each one says about itself.

## Declarations

The merge declared **7** departure(s) from its sources. Checking them confirms 4, rejects 2, and leaves 1 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 1 of 33 source segment(s) declared gone, **3.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b3` | subsumed | Merged into the first response section as part of initial actions. | **rejected** | declared 'subsumed', which predicts SUPPORTED; B-001 came back MISSING (`B-001`) |
| `b4` | subsumed | Content subsumed in unit name instruction. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-002`, `B-003`) |
| `b6` | reworded | Hyphenated compound retained as single phrase for clarity. | **rejected** | declared 'reworded', and its text is in the merge (no claim traced to it) |
| `a9` | dropped | Section heading subsumed; content retained under Check the door seal. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b9` | subsumed | Integrated into If the temperature keeps rising section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-006`) |
| `b10` | subsumed | Escalation instruction combined with technician call guidance. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b13` | subsumed | Content carried in recording section as part of logging requirement. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-008`) |


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
| Calls | 7 live, 0 cached, 0 replayed |
| Tokens | 17,631 in, 7,271 out |
| Cost | ~$0.05 estimated (rates read 2026-08-31) |
| Schema repairs | 1 |
| Errors | 0 |
| Duration | 50.8s |
| Generated | 2026-09-27T15:45:02+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
