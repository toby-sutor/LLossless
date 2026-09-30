## Verdict

**1 finding(s), all in the merge's account of itself.** 1 false departure. The merged document itself carries no finding: 18 source claim(s) checked against the merge, 30 merge claim(s) checked against the sources, and none of the reconciler's checks found content missing, invented, altered or repeated. What is wrong is what the merge said it did. The 9 mechanical checks under Structure below cover what the claims do not: titles, invariant-core tokens, and all 33 source segment(s) — including the ones no claim was drawn from.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 30 |
| Claims extracted from `source_a.md` | 9 |
| Claims extracted from `source_b.md` | 9 |
| Forward — source claims accounted for in the merge | **18/18** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **9/9** |
| Forward — `source_b.md` claims accounted for | **9/9** |
| Reverse — merge claims found in a source | **30/30** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **48/48** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

None in the claims. The 1 finding(s) this run reports are structural and are listed under `## Structure` below.

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
| 1 | Each freezer alarms when the internal temperature rises above its set point for more than 10 minutes. | 5 | carried | 'Each freezer alarms when the internal temperature rises above its set point for more than 10 minutes.' in `merged.md` -- The reference states the alarm threshold and duration. |
| 2 | The alarm sounds locally. | 6 | carried | 'The alarm sounds locally' in `merged.md` -- The reference states that the alarm sounds locally. |
| 3 | The alarm sends a message to the night phone. | 6 | carried | 'sends a message to the night phone' in `merged.md` -- The reference states that the alarm sends a message to the night phone. |
| 4 | The reading at the moment of arrival is the one the lab needs. | 12 | carried | 'The reading at the moment of arrival is the one the lab needs' in `merged.md` -- The reference identifies the arrival reading as the one the lab needs. |
| 5 | The reading at the moment of arrival cannot be recovered later. | 13 | carried | 'The reading at the moment of arrival is the one the lab needs and it cannot be recovered later.' in `merged.md` -- The reference says the arrival reading cannot be recovered later. |
| 6 | If the temperature falls back below the set point, no further action is needed. | 18 | carried | 'If the temperature falls back below the set point, log it as a door event and no further action is needed.' in `merged.md` -- The reference says no further action is needed when the temperature falls back below the set point. |
| 7 | Opening a door on a failing freezer to check the contents is the most common cause of loss in this building. | 22 | carried | 'Opening a door on a failing freezer to check the contents is the most common cause of loss in this building.' in `merged.md` -- The reference states this claim directly. |
| 8 | Contents are moved only on the technician's instruction. | 28 | carried | "Contents are moved only on the technician's instruction" in `merged.md` -- The reference makes the technician's instruction a condition for moving contents. |
| 9 | Contents are moved only into a freezer that already has space at the same set point. | 28 | carried | 'only into a freezer that already has space at the same set point' in `merged.md` -- The reference specifies both available space and the same set point for a destination freezer. |

### `source_b.md` -- 9 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 9 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The alarm panel names the unit. | 5 | carried | 'The alarm panel names the unit' in `merged.md` -- The reference states that the panel names the unit. |
| 2 | The alarm panel shows the temperature that triggered the alarm. | 5 | carried | 'The alarm panel names the unit and shows the temperature that triggered it.' in `merged.md` -- The reference states that the panel shows the temperature that triggered the alarm. |
| 3 | There are three units on this floor. | 6 | carried | 'there are three units on this floor' in `merged.md` -- The reference gives the number of units on this floor as three. |
| 4 | Two of the units on this floor alarm at the same set point. | 6 | carried | 'there are three units on this floor and two of them alarm at the same set point' in `merged.md` -- The reference says two of the three units on this floor alarm at the same set point. |
| 5 | Ice on the seal holds the door open by a few millimetres. | 11 | carried | 'Ice on the seal holds the door open by a few millimetres' in `merged.md` -- The reference states this claim directly. |
| 6 | Ice on the seal is the usual cause of a slow rise. | 12 | carried | 'Ice on the seal holds the door open by a few millimetres and is the usual cause of a slow rise.' in `merged.md` -- The reference identifies ice on the seal as the usual cause of a slow rise. |
| 7 | Every alarm gets a line in the freezer log whether or not anything was wrong. | 22 | carried | 'Every alarm gets a line in the freezer log whether or not anything was wrong.' in `merged.md` -- The reference states this claim directly. |
| 8 | An alarm with no line in the log is indistinguishable from an alarm nobody attended. | 22 | carried | 'An alarm with no line in the log is indistinguishable from an alarm nobody attended.' in `merged.md` -- The reference states this claim directly. |
| 9 | The night phone is carried by the weekend duty officer from 18:00 on Friday until 08:00 on Monday. | 27 | carried | 'The night phone is carried by the weekend duty officer from 18:00 on Friday until 08:00 on Monday.' in `merged.md` -- The reference states who carries the night phone and the specified times. |

### `merged.md` -- 30 claim(s): 0 invented, 0 contradicted, 0 supported in part, 30 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Each freezer alarms when the internal temperature rises above its set point for more than 10 minutes. | supported | `source_a.md` | 'Each freezer alarms when the internal temperature rises above its set point for\nmore than 10 minutes.' in `source_a.md` -- The source states the alarm threshold and duration. |
| 2 | The freezer alarm sounds locally. | supported | `source_a.md` | 'The alarm sounds locally and sends a message to the night\nphone.' in `source_a.md` -- The source says the alarm sounds locally. |
| 3 | The freezer alarm sends a message to the night phone. | supported | `source_a.md` | 'The alarm sounds locally and sends a message to the night\nphone.' in `source_a.md` -- The source says the alarm sends a message to the night phone. |
| 4 | The night phone is carried by the weekend duty officer from 18:00 on Friday until 08:00 on Monday. | supported | `source_b.md` | 'The night phone is carried by the weekend duty officer from 18:00 on Friday\nuntil 08:00 on Monday.' in `source_b.md` -- The source gives the carrier and the stated weekend hours. |
| 5 | The alarm panel names the unit that triggered the alarm. | supported | `source_b.md` | 'The alarm panel names the unit and shows the temperature that triggered it.' in `source_b.md` -- The source says the panel names the unit. |
| 6 | The alarm panel shows the temperature that triggered the alarm. | supported | `source_b.md` | 'The alarm panel names the unit and shows the temperature that triggered it.' in `source_b.md` -- The source says the panel shows the triggering temperature. |
| 7 | There are three freezer units on this floor. | supported | `source_b.md` | 'there are three units on this floor' in `source_b.md` -- The cold storage checklist states that there are three units on the floor. |
| 8 | Two of the freezer units on this floor alarm at the same set point. | supported | `source_b.md` | 'there are three units on this floor and two of them alarm at the\nsame set point.' in `source_b.md` -- The source says two of the floor's units alarm at the same set point. |
| 9 | The responding officer must note the freezer unit name. | supported | `source_b.md` | 'Note\nthe unit name;' in `source_b.md` -- The checklist directs the responder to note the unit name. |
| 10 | The responding officer must go to the freezer and read the display. | supported | `source_a.md` | 'Go to the freezer and read the display.' in `source_a.md` -- The first-response instructions state this action directly. |
| 11 | The responding officer must write the display reading and the time in the freezer log before touching anything else. | supported | `source_a.md` | 'Write the reading and the time in the\nfreezer log before touching anything else.' in `source_a.md` -- The source requires both entries before anything else is touched. |
| 12 | The lab needs the freezer reading at the moment of arrival. | supported | `source_a.md` | 'The reading at the moment of arrival\nis the one the lab needs and it cannot be recovered later.' in `source_a.md` -- The source identifies the arrival reading as the one the lab needs. |
| 13 | The freezer reading at the moment of arrival cannot be recovered later. | supported | `source_a.md` | 'The reading at the moment of arrival\nis the one the lab needs and it cannot be recovered later.' in `source_a.md` -- The source says that reading cannot be recovered later. |
| 14 | Every freezer alarm gets a line in the freezer log whether or not anything was wrong. | supported | `source_b.md` | 'Every alarm gets a line in the freezer log whether or not anything was wrong.' in `source_b.md` -- The source requires a log line for every alarm. |
| 15 | A freezer alarm with no line in the log is indistinguishable from an alarm nobody attended. | supported | `source_b.md` | 'alarm with no line in the log is indistinguishable from an alarm nobody attended.' in `source_b.md` -- The source states this consequence of a missing log entry. |
| 16 | When responding to an ajar freezer door, run a finger along the seal. | supported | `source_b.md` | 'Run a finger along the seal.' in `source_b.md` -- The alarm checklist gives this instruction under its door-seal check. |
| 17 | Ice on the freezer seal holds the door open by a few millimetres. | supported | `source_b.md` | 'Ice on the seal holds the door open by a few\nmillimetres and is the usual cause of a slow rise.' in `source_b.md` -- The source says ice holds the door open by a few millimetres. |
| 18 | Ice on the freezer seal is the usual cause of a slow temperature rise. | supported | `source_b.md` | 'Ice on the seal holds the door open by a few\nmillimetres and is the usual cause of a slow rise.' in `source_b.md` -- The source identifies ice on the seal as the usual cause of a slow rise. |
| 19 | When responding to an ajar freezer door, close the door and wait 20 minutes. | supported | `source_a.md` | '## If the door is ajar\n\nClose the door and wait 20 minutes.' in `source_a.md` -- The source gives this response for an ajar door. |
| 20 | If the freezer temperature falls back below the set point, log the alarm as a door event. | supported | `source_a.md` | 'If the temperature falls back below the set\npoint, log it as a door event and no further action is needed.' in `source_a.md` -- The source directs staff to log a door event if the temperature falls below the set point. |
| 21 | If the freezer temperature falls back below the set point, no further action is needed. | supported | `source_a.md` | 'If the temperature falls back below the set\npoint, log it as a door event and no further action is needed.' in `source_a.md` -- The source says no further action is needed under this condition. |
| 22 | If the freezer temperature is still rising 20 minutes after arrival, call the on-call technician. | supported | `source_b.md` | 'Call the on-call technician if the temperature is still rising 20 minutes after\nyou arrive.' in `source_b.md` -- The source states the escalation condition and timing. |
| 23 | Give the on-call technician the freezer unit name. | supported | `source_b.md` | 'Give the unit name, the reading you took on arrival and the reading\nnow.' in `source_b.md` -- The source says to give the technician the unit name. |
| 24 | Give the on-call technician the freezer reading taken on arrival. | supported | `source_b.md` | 'Give the unit name, the reading you took on arrival and the reading\nnow.' in `source_b.md` -- The source says to give the technician the arrival reading. |
| 25 | Give the on-call technician the current freezer reading. | supported | `source_b.md` | 'Give the unit name, the reading you took on arrival and the reading\nnow.' in `source_b.md` -- The reading taken now is the current reading to give the technician. |
| 26 | Do not open the freezer door while waiting for the on-call technician. | supported | `source_a.md` | 'While waiting, do not open the door.' in `source_a.md` -- The instruction applies while waiting for the on-call technician. |
| 27 | Opening a door on a failing freezer to check the contents is the most common cause of loss in this building. | supported | `source_a.md` | 'Opening a\ndoor on a failing freezer to check the contents is the most common cause of loss\nin this building.' in `source_a.md` -- The source states the claim directly. |
| 28 | Freezer contents are moved only on the technician's instruction. | supported | `source_a.md` | "Contents are moved only on the technician's instruction" in `source_a.md` -- The source makes the technician's instruction a condition for moving contents. |
| 29 | Freezer contents are moved only into a freezer that already has space at the same set point. | supported | `source_a.md` | 'only into a freezer\nthat already has space at the same set point.' in `source_a.md` -- The source specifies both available space and the same set point. |
| 30 | A single study's samples must not be split across two freezers. | supported | `source_a.md` | "Never split a single study's\nsamples across two freezers." in `source_a.md` -- The source explicitly prohibits splitting one study's samples across two freezers. |

## Structure

**9** mechanical check(s) over **33** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **30** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **18**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 11 run(s) over 26 attributed segment(s) — sources interleaved. 6 of 12 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Declared gone, still here — a record says the content departed and the merge carries the segment unchanged

- `a13` (`source_a.md`) — 'Call the on-call technician.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Call the on-call technician.
  In the merge:  If the temperature is still rising 20 minutes after you arrive, call the on-call technician.
  ```

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **21** departure(s) from its sources. Checking them confirms 11, rejects 3, and leaves 7 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 33 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a3` | reworded | The trigger is retained with its wrapped line joined. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-001`) |
| `a4` | reworded | The notification is retained with its wrapped line joined. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-002`, `A-003`) |
| `a7` | reworded | The first-response log instruction is retained on one line. | **rejected** | declared 'reworded', and its text is in the merge (no claim traced to it) |
| `a8` | reworded | The arrival-reading rationale is retained on one line. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-004`, `A-005`) |
| `a11` | reworded | The door-event instruction is retained on one line. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-006`) |
| `a13` | subsumed | The escalation instruction is stated with its specific timing. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a15` | reworded | The warning is retained with its wrapped lines joined. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-007`) |
| `a17` | reworded | The moving restriction is retained on one line. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-008`, `A-009`) |
| `a18` | reworded | The sample restriction is retained on one line. | **rejected** | declared 'reworded', and its text is in the merge (no claim traced to it) |
| `b1` | superseded | The base title is used. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Freezer Alarm Response - Night Shift' and says so (no claim traced to it) |
| `b2` | superseded | Alarm reading is placed under the base heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b4` | reworded | The unit-identification instruction is retained on one line. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-003`, `B-004`) |
| `b5` | superseded | The seal check is placed under the base door heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b7` | reworded | The seal explanation is retained on one line. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-005`, `B-006`) |
| `b8` | superseded | Escalation is placed under the base heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b9` | reworded | The timed escalation instruction is retained on one line. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b10` | reworded | The technician handoff instruction is retained on one line. | **rejected** | declared 'reworded', and its text is in the merge (no claim traced to it) |
| `b11` | superseded | Recording is placed under the base first-response heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b13` | reworded | The recording rationale is retained on one line. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-008`) |
| `b14` | superseded | Weekend phone cover is placed with alarm notification. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b15` | reworded | Weekend phone cover is retained on one line. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-009`) |


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
| Tokens | 15,694 in, 11,444 out, 0 cached, 3,212 reasoning |
| Cost | ~$0.15 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 125.6s |
| Generated | 2026-09-27T15:20:42+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `bf7d5842201d`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
