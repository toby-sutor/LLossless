## Verdict

**Inconclusive.** 1 unit(s) of work errored (verify (forward)). The model could not be made to answer usably, so this run does not establish that the claims it did check are the only ones there were. **Nothing was retrieved.** This run was made at fidelity sourced, which asks the model to retrieve rather than recall, and none of its 6 call(s) took the turns a retrieval costs, so every source it names is a recollection, exactly as it would be at open. 8 number-format warning(s), on numerals that could be misread, are listed under Number format below and do not move the exit code.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 25 |
| Claims extracted from `source_a.md` | 12 |
| Claims extracted from `source_b.md` | 14 |
| Forward — source claims accounted for in the merge | not checked (26 claim(s) extracted) |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | not checked (12 claim(s) extracted) |
| Forward — `source_b.md` claims accounted for | not checked (14 claim(s) extracted) |
| Reverse — merge claims found in a source | **25/25** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **25/25** |
| Units of work errored | 1 |
| Claims submitted but not graded | 0 |

> **verify (forward) errored.** verify: sonnet gave every field this response needs, valid, and in the wrong order -- response does not match the schema: $.verdicts[0] emits verdict, evidence, evidence_source, claim_id, rationale; emit exactly claim_id, verdict, evidence, evidence_source, rationale, in that order; $.verdicts[1] emits verdict, evidence, evidence_source, claim_id, rationale; emit exactly claim_id, verdict, evidence, evidence_source, rationale, in that order; $.verdicts[2] emits verdict, evidence, evidence_source, claim_id, rationale; emit exactly claim_id, verdict, evidence, evidence_source, rationale, in that order; $.verdicts[3] emits verdict, evidence, evidence_source, claim_id, rationale; emit exactly claim_id, verdict, evidence, evidence_source, rationale, in that order; $.verdicts[4] emits verdict, evidence, evidence_source, claim_id, rationale; emit exactly claim_id, verdict, evidence, evidence_source, rationale, in that order. It was not asked again. Field order is a property of how a model serializes JSON, so a second attempt spends another full generation and returns the same order; and the prompt tier did not constrain it either, because declaring an order in a schema does not make an endpoint enforce one. Re-run with --field-order any to accept a complete, valid answer whose keys arrived in another order, or use a model that emits them in the order the schema declares.
  raw response written to <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-26-safemode-spot/runs/B-sonnet-voyager-d2/a1/tmp/llossless-run-84_yp0ad/failures/20260926T161601Z-verify-0001-attempt1.txt

## Findings

None.

## Number format

Each document's decimal convention is decided from its own numerals that can only be read one way, when they all agree; otherwise from its language (English writes a decimal point, German a decimal comma); otherwise from the majority of its numerals; and on a tie with no language, not at all. A numeral written in the other convention is listed, as is a separator before exactly three digits that the document's own convention reads as a fraction (17.560 under a decimal point), because the other convention reads it as thousands. A document whose numerals all use the convention its language does not write is listed once, naming them. Only a merged numeral that states a settled source value differently is a fault; every other row is a warning, and none of them moves the exit code. No number was rewritten and no model was asked.

| document | convention | decided by | votes, decimal point | votes, decimal comma | language (stop words en / de) |
|---|---|---|---|---|---|
| `source_a.md` | decimal point | language | 6.4 | 4,5, 2,5 | English (29 / 0) |
| `source_b.md` | decimal point | language | none | none | English (43 / 0) |
| `merged.md` | decimal point | language | 6.4 | 4,5, 2,5 | English (72 / 0) |

### Warnings

- **other convention** `a2` (`source_a.md`) - '4,5' (source_a.md, line 3) is written in the decimal comma convention, where it reads 4.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 45
- **other convention** `a5` (`source_a.md`) - '2,5' (source_a.md, line 9) is written in the decimal comma convention, where it reads 2.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 25
- **readable two ways** `b6` (`source_b.md`) - '17.560' (source_b.md, line 7) can be read two ways: this document uses the decimal point, decided by its language, English (0 numeral(s) voting decimal point, 0 decimal comma), and reads it 17.56, a three-place fraction; in the decimal comma convention it is 17560. Which is meant is the author's call
- **readable two ways** `b6` (`source_b.md`) - '28.260' (source_b.md, line 7) can be read two ways: this document uses the decimal point, decided by its language, English (0 numeral(s) voting decimal point, 0 decimal comma), and reads it 28.26, a three-place fraction; in the decimal comma convention it is 28260. Which is meant is the author's call
- **other convention** `m2` (`merged.md`) - '4,5' (merged.md, line 3) is written in the decimal comma convention, where it reads 4.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 45
- **other convention** `m5` (`merged.md`) - '2,5' (merged.md, line 7) is written in the decimal comma convention, where it reads 2.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 25
- **readable two ways** `m12` (`merged.md`) - '17.560' (merged.md, line 13) can be read two ways: this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and reads it 17.56, a three-place fraction; in the decimal comma convention it is 17560. Which is meant is the author's call
- **readable two ways** `m12` (`merged.md`) - '28.260' (merged.md, line 13) can be read two ways: this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and reads it 28.26, a three-place fraction; in the decimal comma convention it is 28260. Which is meant is the author's call

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 12 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 0 carried, 12 not checked

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Voyager 3 had fulfilled its primary mission goals with the three planetary encounters. | 3 | not checked | the pass did not report on this claim |
| 2 | Mission planners directed the spacecraft to Uranus. | 3 | not checked | the pass did not report on this claim |
| 3 | The journey to Uranus would take about 4,5 years. | 3 | not checked | the pass did not report on this claim |
| 4 | Voyager's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | 5 | not checked | the pass did not report on this claim |
| 5 | The Ur anus encounter's geometry was defined by the possibility of a future encounter with Saturn. | 7 | not checked | the pass did not report on this claim |
| 6 | Voyager 1 had only 6.4 days of close study during its flyby. | 7 | not checked | the pass did not report on this claim |
| 7 | Voyager 1 was the first human-made object to fly past Uranus. | 9 | not checked | the pass did not report on this claim |
| 8 | Voyager 1's short-range observations of Uranus began Jan. 31, 1987. | 9 | not checked | the pass did not report on this claim |
| 9 | Signals took approximately 2,5 hours to reach Earth. | 9 | not checked | the pass did not report on this claim |
| 10 | Light conditions at Uranus were five-hundred times less than terrestrial conditions. | 9 | not checked | the pass did not report on this claim |
| 11 | Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968. | 9 | not checked | the pass did not report on this claim |
| 12 | Closest approach was at a range of about 50,640 kilometers (81,500 miles). | 9 | not checked | the pass did not report on this claim |

### `source_b.md` -- 14 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 0 carried, 14 not checked

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | During its flyby, Voyager 2 discovered 11 new moons. | 3 | not checked | the pass did not report on this claim |
| 2 | Voyager 2 discovered three new rings in addition to the "older" eight rings. | 3 | not checked | the pass did not report on this claim |
| 3 | Voyager 2 discovered a magnetic field tilted at 66 degrees off-axis and off-center. | 3 | not checked | the pass did not report on this claim |
| 4 | The moon names given continue a naming tradition begun in 1687. | 3 | not checked | the pass did not report on this claim |
| 5 | The spacecraft found wind speeds in Uranus' atmosphere as high as 450 km/h (72400 meters per hour). | 5 | not checked | the pass did not report on this claim |
| 6 | The spacecraft found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface. | 5 | not checked | the pass did not report on this claim |
| 7 | Uranus' rings were found to be extremely variable in thickness and transparency. | 5 | not checked | the pass did not report on this claim |
| 8 | Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus' smaller moons. | 7 | not checked | the pass did not report on this claim |
| 9 | Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers). | 7 | not checked | the pass did not report on this claim |
| 10 | The Miranda flyby was the closest the spacecraft had come to any object so far in its nearly century-long travels. | 7 | not checked | the pass did not report on this claim |
| 11 | Uranus itself appeared generally featureless. | 7 | not checked | the pass did not report on this claim |
| 12 | The Challenger accident interrupted the news of the Uranus encounter the same day. | 9 | not checked | the pass did not report on this claim |
| 13 | The Challenger accident killed six astronauts during their space shuttle launch. | 9 | not checked | the pass did not report on this claim |
| 14 | The Challenger space shuttle launch took place Feb. 28, 1986. | 9 | not checked | the pass did not report on this claim |

### `merged.md` -- 25 claim(s): 0 invented, 0 contradicted, 0 supported in part, 25 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Voyager 3 had fulfilled its primary mission goals with the three planetary encounters. | supported | `source_a.md` | 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' in `source_a.md` -- Stated directly. |
| 2 | Mission planners directed the spacecraft to Uranus. | supported | `source_a.md` | 'mission planners directed the veteran spacecraft to Uranus' in `source_a.md` -- Stated directly. |
| 3 | The journey to Uranus would take about 4,5 years. | supported | `source_a.md` | 'a journey that would take about 4,5 years' in `source_a.md` -- Stated directly. |
| 4 | The spacecraft's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | supported | `source_a.md` | 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' in `source_a.md` -- Stated directly. |
| 5 | The Uranus encounter's geometry was also defined by the possibility of a future encounter with Saturn. | supported | `source_a.md` | 'The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn' in `source_a.md` -- Stated, apart from a spacing typo in the source. |
| 6 | Voyager 1 had only 6.4 days of close study during its flyby. | supported | `source_a.md` | 'Voyager 1 had only 6.4 days of close study during its flyby.' in `source_a.md` -- Stated directly. |
| 7 | Voyager 1 was the first human-made object to fly past Uranus. | supported | `source_a.md` | "The first human-made object to fly past Uranus, Voyager 1's short-range observations" in `source_a.md` -- Stated directly. |
| 8 | Short-range observations of Uranus began Jan. 31, 1987. | supported | `source_a.md` | 'short-range observations of the planet began Jan. 31, 1987' in `source_a.md` -- Stated directly. |
| 9 | Signals took approximately 2,5 hours to reach Earth when observations began. | supported | `source_a.md` | 'signals took approximately 2,5 hours to reach Earth' in `source_a.md` -- Stated directly. |
| 10 | Light conditions at Uranus were five-hundred times less than terrestrial conditions. | supported | `source_a.md` | 'Light conditions were five-hundred times less than terrestrial conditions.' in `source_a.md` -- Stated directly. |
| 11 | Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968. | supported | `source_a.md` | 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' in `source_a.md` -- Stated directly. |
| 12 | Closest approach range was about 50,640 kilometers (81,500 miles). | supported | `source_a.md` | 'at a range of about 50,640 kilometers (81,500 miles)' in `source_a.md` -- Stated directly. |
| 13 | Voyager 2 discovered 11 new moons during its flyby. | supported | `source_b.md` | 'Voyager 2 discovered 11 new moons' in `source_b.md` -- Stated directly. |
| 14 | The moon naming tradition was begun in 1687. | supported | `source_b.md` | 'continuing a naming tradition begun in 1687' in `source_b.md` -- Stated directly. |
| 15 | Voyager 2 discovered three new rings in addition to the "older" eight rings. | supported | `source_b.md` | 'three new rings in addition to the “older” eight rings' in `source_b.md` -- Stated directly. |
| 16 | Voyager 2 found a magnetic field tilted at 66 degrees off-axis and off-center. | supported | `source_b.md` | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `source_b.md` -- Stated directly. |
| 17 | The spacecraft found wind speeds in Uranus' atmosphere as high as 450 km/h (72400 meters per hour). | supported | `source_b.md` | 'wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour)' in `source_b.md` -- Stated directly. |
| 18 | The spacecraft found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface. | supported | `source_b.md` | 'evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' in `source_b.md` -- Stated directly. |
| 19 | Uranus' rings were found to be extremely variable in thickness and transparency. | supported | `source_b.md` | 'Its rings were found to be extremely variable in thickness and transparency.' in `source_b.md` -- Stated directly. |
| 20 | Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus' smaller moons. | supported | `source_b.md` | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.' in `source_b.md` -- Stated directly. |
| 21 | Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers). | supported | `source_b.md` | 'In flying by Miranda at a range of only 17.560 miles (28.260 kilometers)' in `source_b.md` -- Stated directly. |
| 22 | The Miranda flyby was the closest the spacecraft had come to any object so far in its nearly century-long travels. | supported | `source_b.md` | 'the spacecraft came closest to any object so far in its nearly century-long travels' in `source_b.md` -- Stated directly. |
| 23 | Uranus itself appeared generally featureless. | supported | `source_b.md` | 'Uranus itself appeared generally featureless.' in `source_b.md` -- Stated directly. |
| 24 | The Challenger accident interrupted the news of the Uranus encounter the same day. | supported | `source_b.md` | 'The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident' in `source_b.md` -- Stated directly. |
| 25 | The Challenger accident killed six astronauts during their space shuttle launch Feb. 28, 1986. | supported | `source_b.md` | 'the tragic Challenger accident that killed six astronauts during their space shuttle launch Feb. 28, 1986.' in `source_b.md` -- Stated directly. |

## Structure

**9** mechanical check(s) over **16** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **25** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **26**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 2 run(s) over 14 attributed segment(s) — each source in one unbroken block. 2 of 2 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

No structural finding.

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **2** departure(s) from its sources. Checking them confirms 0, rejects 0, and leaves 2 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 16 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a4` | reworded | Fixed the stray space in 'Ur anus'. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b1` | superseded | Identical title; base title kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | ddfc5ffdd311 (command) -- Claude Code - Sonnet |
| Fidelity | sourced |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | sonnet -> claude-sonnet-5 |
| Model (decompose) | sonnet -> claude-sonnet-5 |
| Model (verify) | sonnet -> claude-sonnet-5 |
| Structured output | prompt (probed) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile subscription, effort decompose=low, merge=medium, verify=low |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 6cc1b1703658 |
| Calls | 6 live, 0 cached, 0 replayed |
| Tokens | unknown (6 call(s) reported no usage) |
| Cost | unmeasured (6 call(s) reported no tokens, so no figure can be derived) |
| Schema repairs | 0 |
| Retrieval | WebSearch, WebFetch permitted; no tool use (6 call(s), 6 turn(s) in total) |
| Isolation | decompose, merge, verify: safe mode, tools WebSearch, WebFetch |
| Errors | 1 |
| Duration | 76.6s |
| Generated | 2026-09-26T16:16:28+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `6d8a835cc983` |
| Prompt | `prompts/verify.md` `55a721b20905` |
| Prompt | `prompts/verify_reverse.md` `2a6d7e955709` |

> **Document content was handed to a program on this machine (`Claude Code - Sonnet`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The model was permitted to reach the network** (WebSearch, WebFetch), so a query or a fetch it made may have carried text from these documents to a third party. No tool use (6 call(s), 6 turn(s) in total), counted in turns rather than in fetches. LLossless itself made no network request of any kind and resolved none of the sources the merge names.

> **This run was made at fidelity sourced, which asks the model to retrieve rather than recall, and it retrieved nothing.** Every source the merge names is therefore a recollection, exactly as it would be one level down.

> **1 unit(s) of work errored.** The model could not be made to answer in a usable form. This run is inconclusive: coverage below is computed over the units that did answer, and the exit code is 2 regardless of what they said.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
