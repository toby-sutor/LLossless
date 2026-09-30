## Verdict

**2 finding(s).** In the structure: 2 undeclared rewording.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 17 |
| Claims extracted from `source_a.md` | 9 |
| Claims extracted from `source_b.md` | 9 |
| Forward — source claims accounted for in the merge | **18/18** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **9/9** |
| Forward — `source_b.md` claims accounted for | **9/9** |
| Reverse — merge claims found in a source | **17/17** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **35/35** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

None in the claims. The 2 finding(s) this run reports are structural and are listed under `## Structure` below.

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
| 1 | Each freezer alarms when the internal temperature rises above its set point for more than 10 minutes. | 5 | carried | 'Each freezer alarms when the internal temperature rises above its set point for more than 10 minutes.' in `merged.md` -- The reference states this alarm condition verbatim. |
| 2 | The alarm sounds locally. | 6 | carried | 'The alarm sounds locally' in `merged.md` -- The reference says the alarm sounds locally. |
| 3 | The alarm sends a message to the night phone. | 6 | carried | 'sends a message to the night phone' in `merged.md` -- The reference says the alarm sends a message to the night phone. |
| 4 | The reading at the moment of arrival is the one the lab needs. | 12 | carried | 'The reading at arrival is the one the lab needs' in `merged.md` -- The reference identifies the reading at arrival as the one the lab needs. |
| 5 | The reading at the moment of arrival cannot be recovered later. | 13 | carried | 'The reading at arrival is the one the lab needs and cannot be recovered later.' in `merged.md` -- The reference says the arrival reading cannot be recovered later. |
| 6 | No further action is needed if the temperature falls back below the set point. | 18 | carried | 'If the temperature falls back below the set point, log it as a door event; no further action is needed.' in `merged.md` -- The reference says no further action is needed when the temperature falls below the set point. |
| 7 | Opening a door on a failing freezer to check the contents is the most common cause of loss in this building. | 22 | carried | 'Opening a door on a failing freezer to check the contents is the most common cause of loss in this building.' in `merged.md` -- The reference states this as the most common cause of loss in the building. |
| 8 | Contents are moved only on the technician's instruction. | 28 | carried | "Contents are moved only on the technician's instruction" in `merged.md` -- The reference limits moving contents to the technician's instruction. |
| 9 | Contents are moved only into a freezer that already has space at the same set point. | 28 | carried | 'only into a freezer that already has space at the same set point.' in `merged.md` -- The reference specifies that contents go only into a freezer with space at the same set point. |

### `source_b.md` -- 9 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 9 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The alarm panel names the unit. | 5 | carried | 'The alarm panel names the unit' in `merged.md` -- The reference says the alarm panel names the unit. |
| 2 | The alarm panel shows the temperature that triggered the alarm. | 5 | carried | 'shows the temperature that triggered the alarm.' in `merged.md` -- The reference says the alarm panel shows the triggering temperature. |
| 3 | There are three units on this floor. | 6 | carried | 'there are three units on this floor' in `merged.md` -- The reference states there are three units on this floor. |
| 4 | Two of the units on this floor alarm at the same set point. | 6 | carried | 'two of them alarm at the same set point.' in `merged.md` -- The reference says two of the units alarm at the same set point. |
| 5 | Ice on the seal holds the door open by a few millimetres. | 11 | carried | 'Ice on the seal holds the door open by a few millimetres' in `merged.md` -- The reference states that ice on the seal holds the door open by a few millimetres. |
| 6 | Ice on the seal is the usual cause of a slow rise. | 12 | carried | 'Ice on the seal holds the door open by a few millimetres and is the usual cause of a slow rise.' in `merged.md` -- The reference identifies ice on the seal as the usual cause of a slow rise. |
| 7 | Every alarm gets a line in the freezer log whether or not anything was wrong. | 22 | carried | 'Every alarm gets a line in the freezer log, whether or not anything was wrong.' in `merged.md` -- The reference says every alarm is logged whether or not anything was wrong. |
| 8 | An alarm with no line in the log is indistinguishable from an alarm nobody attended. | 22 | carried | 'An alarm with no line in the log is indistinguishable from an alarm nobody attended.' in `merged.md` -- The reference states that an unlogged alarm is indistinguishable from one nobody attended. |
| 9 | The night phone is carried by the weekend duty officer from 18:00 on Friday until 08:00 on Monday. | 27 | carried | 'From 18:00 on Friday until 08:00 on Monday, the night phone is carried by the weekend duty officer.' in `merged.md` -- The reference gives this duty phone arrangement and time period. |

### `merged.md` -- 17 claim(s): 0 invented, 0 contradicted, 0 supported in part, 17 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Each freezer alarms when the internal temperature rises above its set point for more than 10 minutes. | supported | `source_a.md` | 'Each freezer alarms when the internal temperature rises above its set point for\nmore than 10 minutes.' in `source_a.md` -- The source states this alarm condition directly. |
| 2 | The alarm sounds locally. | supported | `source_a.md` | 'The alarm sounds locally' in `source_a.md` -- The source directly says the alarm sounds locally. |
| 3 | The alarm sends a message to the night phone. | supported | `source_a.md` | 'sends a message to the night\nphone.' in `source_a.md` -- The source directly states that the alarm sends a message to the night phone. |
| 4 | The alarm panel names the unit. | supported | `source_b.md` | 'The alarm panel names the unit' in `source_b.md` -- The source directly states that the panel names the unit. |
| 5 | The alarm panel shows the temperature that triggered the alarm. | supported | `source_b.md` | 'shows the temperature that triggered it.' in `source_b.md` -- The source directly states that the panel shows the triggering temperature. |
| 6 | There are three units on this floor. | supported | `source_b.md` | 'there are three units on this floor' in `source_b.md` -- The source states there are three units on the floor. |
| 7 | Two of the units alarm at the same set point. | supported | `source_b.md` | 'two of them alarm at the\nsame set point.' in `source_b.md` -- The source states that two units alarm at the same set point. |
| 8 | The reading at arrival is the one the lab needs. | supported | `source_a.md` | 'The reading at the moment of arrival\nis the one the lab needs' in `source_a.md` -- The source says the arrival reading is the one the lab needs. |
| 9 | The reading at arrival cannot be recovered later. | supported | `source_a.md` | 'it cannot be recovered later.' in `source_a.md` -- The source states that the arrival reading cannot be recovered later. |
| 10 | Every alarm gets a line in the freezer log, whether or not anything was wrong. | supported | `source_b.md` | 'Every alarm gets a line in the freezer log whether or not anything was wrong.' in `source_b.md` -- The source directly states that every alarm gets a log line regardless of whether anything was wrong. |
| 11 | An alarm with no line in the log is indistinguishable from an alarm nobody attended. | supported | `source_b.md` | 'An alarm with no line in the log is indistinguishable from an alarm nobody attended.' in `source_b.md` -- The source states this directly. |
| 12 | From 18:00 on Friday until 08:00 on Monday, the night phone is carried by the weekend duty officer. | supported | `source_b.md` | 'The night phone is carried by the weekend duty officer from 18:00 on Friday\nuntil 08:00 on Monday.' in `source_b.md` -- The source gives the same coverage period and phone-carrying responsibility. |
| 13 | Ice on the seal holds the door open by a few millimetres. | supported | `source_b.md` | 'Ice on the seal holds the door open by a few\nmillimetres' in `source_b.md` -- The source directly states this effect of ice on the seal. |
| 14 | Ice on the seal is the usual cause of a slow rise. | supported | `source_b.md` | 'is the usual cause of a slow rise.' in `source_b.md` -- The source identifies ice on the seal as the usual cause of a slow rise. |
| 15 | Opening a door on a failing freezer to check the contents is the most common cause of loss in this building. | supported | `source_a.md` | 'Opening a\n door on a failing freezer to check the contents is the most common cause of loss\nin this building.' in `source_a.md` -- The source directly identifies opening the door to check contents as the most common cause of loss. |
| 16 | Contents are moved only on the technician's instruction. | supported | `source_a.md` | "Contents are moved only on the technician's instruction" in `source_a.md` -- The source directly states that moving contents requires the technician's instruction. |
| 17 | Contents are moved only into a freezer that already has space at the same set point. | supported | `source_a.md` | 'only into a freezer\nthat already has space at the same set point.' in `source_a.md` -- The source states the destination must have space at the same set point. |

## Structure

**9** mechanical check(s) over **33** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **17** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **18**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 9 run(s) over 25 attributed segment(s) — sources interleaved. 6 of 12 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

`[-...-]` is what the source said and `{+...+}` is what the merge says.

### Reworded and undeclared — in the merge in altered wording, and no record explains it. At off this also covers layout: a segment whose source line breaks the merge ran together is altered and undeclared, and 380 reuses this kind rather than moving FINDING_KINDS off 12

- `b3` (`source_b.md`) — 'The alarm panel names the unit and shows the temperature that triggered it.' is reworded in the merge and no disposition record explains it (nearest merge segment m7 at 0.94)

  ```text
  In the source: The alarm panel names the unit and shows the temperature that triggered it.
  In the merge:  The alarm panel names the unit and shows the temperature that triggered the alarm.
  What changed:  The alarm panel names the unit and shows the temperature that triggered [-it.-] {+the alarm.+}
  ```
- `b12` (`source_b.md`) — 'Every alarm gets a line in the freezer log whether or not anything was wrong.' is reworded in the merge and no disposition record explains it (nearest merge segment m11 at 0.99)

  ```text
  In the source: Every alarm gets a line in the freezer log whether or not anything was wrong.
  In the merge:  Every alarm gets a line in the freezer log, whether or not anything was wrong.
  What changed:  Every alarm gets a line in the freezer log{+,+} whether or not anything was wrong.
  ```

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **21** departure(s) from its sources. Checking them confirms 11, rejects 1, and leaves 9 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 33 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a3` | reworded | Alarm trigger is retained with the source line break removed. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-001`) |
| `a4` | reworded | Alarm notification is retained with the source line break removed. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-002`, `A-003`) |
| `a7` | reworded | First-response logging instruction is retained. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a8` | reworded | Arrival-reading importance is retained. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-004`, `A-005`) |
| `a11` | reworded | Door-event condition and follow-up are retained. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-006`) |
| `a13` | reconciled | The call instruction is combined with the 20-minute threshold. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `a15` | reworded | The warning is retained with the source line breaks removed. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-007`) |
| `a17` | reworded | Transfer conditions are retained with the source line break removed. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-008`, `A-009`) |
| `a18` | reworded | The sample-splitting prohibition is retained with the source line break removed. | **rejected** | declared 'reworded', and its text is in the merge (no claim traced to it) |
| `b1` | superseded | The base document's title is retained. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Freezer Alarm Response - Night Shift' and says so (no claim traced to it) |
| `b2` | superseded | Alarm-reading instructions are placed under First response. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b4` | reworded | Unit-identification instruction and unit count are retained. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-003`, `B-004`) |
| `b5` | superseded | Seal-check instructions are consolidated under the base door heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b7` | reworded | Seal-ice cause and effect are retained. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-005`, `B-006`) |
| `b8` | superseded | Escalation instructions use the base's rising-temperature heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b9` | reconciled | The 20-minute condition narrows the call instruction. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b10` | reworded | Information to provide the technician is retained. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b11` | superseded | Recording requirements are placed under First response. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b13` | reworded | The reason for logging every alarm is retained. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-008`) |
| `b14` | superseded | Weekend phone coverage is placed with night-phone response information. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b15` | reworded | Weekend phone coverage and its hours are retained. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-009`) |


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
| Calls | 6 live, 0 cached, 0 replayed |
| Tokens | 13,310 in, 12,387 out, 0 cached, 7,204 reasoning |
| Cost | ~$0.01 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 98.1s |
| Generated | 2026-09-27T15:22:20+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `bf7d5842201d`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
