## Verdict

**Inconclusive.** 1 unit(s) of work errored (verify (reverse)). The model could not be made to answer usably, so this run does not establish that the claims it did check are the only ones there were. Of what could be graded, 7 finding(s); see below. That total is over the graded part only. **Nothing was retrieved.** This run was made at fidelity sourced, which asks the model to retrieve rather than recall, and none of its 6 call(s) took the turns a retrieval costs, so every source it names is a recollection, exactly as it would be at open. 8 number-format warning(s), on numerals that could be misread, are listed under Number format below and do not move the exit code.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 27 |
| Claims extracted from `source_a.md` | 12 |
| Claims extracted from `source_b.md` | 14 |
| Forward — source claims accounted for in the merge | **22/26** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **8/12** |
| Forward — `source_b.md` claims accounted for | **14/14** |
| Reverse — merge claims found in a source | not checked (27 claim(s) extracted) |
| Reverse — supported only in part | 0 |
| Evidence grounded | **26/26** |
| Units of work errored | 1 |
| Claims submitted but not graded | 0 |

> **verify (reverse) errored.** verify: sonnet gave every field this response needs, valid, and in the wrong order -- response does not match the schema: $.verdicts[0] emits verdict, evidence, evidence_source, claim_id, rationale; emit exactly claim_id, verdict, evidence, evidence_source, rationale, in that order; $.verdicts[1] emits verdict, evidence, evidence_source, claim_id, rationale; emit exactly claim_id, verdict, evidence, evidence_source, rationale, in that order; $.verdicts[2] emits verdict, evidence, evidence_source, claim_id, rationale; emit exactly claim_id, verdict, evidence, evidence_source, rationale, in that order; $.verdicts[3] emits verdict, evidence, evidence_source, claim_id, rationale; emit exactly claim_id, verdict, evidence, evidence_source, rationale, in that order; $.verdicts[4] emits verdict, evidence, evidence_source, claim_id, rationale; emit exactly claim_id, verdict, evidence, evidence_source, rationale, in that order. It was not asked again. Field order is a property of how a model serializes JSON, so a second attempt spends another full generation and returns the same order; and the prompt tier did not constrain it either, because declaring an order in a schema does not make an endpoint enforce one. Re-run with --field-order any to accept a complete, valid answer whose keys arrived in another order, or use a model that emits them in the order the schema declares.
  raw response written to <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-26-safemode-spot/runs/B-sonnet-voyager-d1/a1/tmp/llossless-run-0fcy440y/failures/20260926T161341Z-verify-0001-attempt1.txt

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **A-001** -- the two documents disagree
  - `source_a.md:3` says: Voyager 3 had fulfilled its primary mission goals with the three planetary encounters.
  - `merged.md` says: 'Although Voyager 2 had fulfilled its primary mission goals with the three planetary encounters' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text says Voyager 2, not Voyager 3.
- **A-006** -- the two documents disagree
  - `source_a.md:7` says: Voyager 1 had only 6.4 days of close study during its flyby.
  - `merged.md` says: 'Voyager 2 had only 6.4 days of close study during its flyby.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text attributes this to Voyager 2, not Voyager 1.
- **A-007** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1 was the first human-made object to fly past Uranus.
  - `merged.md` says: "The first human-made object to fly past Uranus, Voyager 2's short-range observations" (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text says Voyager 2 was first, not Voyager 1.
- **A-008** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1's short-range observations of Uranus began Jan. 31, 1987.
  - `merged.md` says: "Voyager 2's short-range observations of the planet began Jan. 31, 1987" (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text says Voyager 2, not Voyager 1.

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
- **other convention** `m5` (`merged.md`) - '2,5' (merged.md, line 9) is written in the decimal comma convention, where it reads 2.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 25
- **readable two ways** `m12` (`merged.md`) - '17.560' (merged.md, line 15) can be read two ways: this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and reads it 17.56, a three-place fraction; in the decimal comma convention it is 17560. Which is meant is the author's call
- **readable two ways** `m12` (`merged.md`) - '28.260' (merged.md, line 15) can be read two ways: this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and reads it 28.26, a three-place fraction; in the decimal comma convention it is 28260. Which is meant is the author's call

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 12 claim(s): 0 dropped, 4 contradicted, 0 carried in part, 8 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Voyager 3 had fulfilled its primary mission goals with the three planetary encounters. | 3 | contradicted | 'Although Voyager 2 had fulfilled its primary mission goals with the three planetary encounters' in `merged.md` -- The text says Voyager 2, not Voyager 3. |
| 6 | Voyager 1 had only 6.4 days of close study during its flyby. | 7 | contradicted | 'Voyager 2 had only 6.4 days of close study during its flyby.' in `merged.md` -- Text attributes this to Voyager 2, not Voyager 1. |
| 7 | Voyager 1 was the first human-made object to fly past Uranus. | 9 | contradicted | "The first human-made object to fly past Uranus, Voyager 2's short-range observations" in `merged.md` -- Text says Voyager 2 was first, not Voyager 1. |
| 8 | Voyager 1's short-range observations of Uranus began Jan. 31, 1987. | 9 | contradicted | "Voyager 2's short-range observations of the planet began Jan. 31, 1987" in `merged.md` -- Text says Voyager 2, not Voyager 1. |
| 2 | Mission planners directed the veteran spacecraft to Uranus. | 3 | carried | 'mission planners directed the veteran spacecraft to Uranus' in `merged.md` -- Directly stated. |
| 3 | The journey to Uranus would take about 4,5 years. | 3 | carried | 'a journey that would take about 4,5 years' in `merged.md` -- Directly stated. |
| 4 | Voyager's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | 5 | carried | 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' in `merged.md` -- Stated for Voyager 2's Jupiter encounter. |
| 5 | The Uranus encounter's geometry was also defined by the possibility of a future encounter with Saturn. | 7 | carried | 'The Uranus encounter’s geometry was also defined by the possibility of a future encounter with Saturn' in `merged.md` -- Directly stated. |
| 9 | Signals took approximately 2,5 hours to reach Earth when short-range observations began. | 9 | carried | 'when signals took approximately 2,5 hours to reach Earth' in `merged.md` -- Directly stated. |
| 10 | Light conditions at Uranus were five-hundred times less than terrestrial conditions. | 9 | carried | 'Light conditions were five-hundred times less than terrestrial conditions.' in `merged.md` -- Directly stated. |
| 11 | Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968. | 9 | carried | 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' in `merged.md` -- Directly stated. |
| 12 | Closest approach to Uranus was at a range of about 50,640 kilometers (81,500 miles). | 9 | carried | 'at a range of about 50,640 kilometers (81,500 miles)' in `merged.md` -- Directly stated. |

### `source_b.md` -- 14 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 14 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | During its flyby, Voyager 2 discovered 11 new moons. | 3 | carried | 'Voyager 2 discovered 11 new moons' in `merged.md` -- Directly stated. |
| 2 | The naming tradition for Uranus' moons was begun in 1687. | 3 | carried | 'continuing a naming tradition begun in 1687' in `merged.md` -- Directly stated. |
| 3 | Voyager 2 discovered three new rings in addition to the "older" eight rings. | 3 | carried | 'three new rings in addition to the “older” eight rings' in `merged.md` -- Directly stated. |
| 4 | Voyager 2 discovered a magnetic field tilted at 66 degrees off-axis and off-center. | 3 | carried | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `merged.md` -- Directly stated. |
| 5 | The spacecraft found wind speeds in Uranus' atmosphere as high as 450 km/h (72400 meters per hour). | 5 | carried | 'wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour)' in `merged.md` -- Directly stated. |
| 6 | The spacecraft found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface. | 5 | carried | 'found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' in `merged.md` -- Directly stated. |
| 7 | Uranus' rings were found to be extremely variable in thickness and transparency. | 5 | carried | 'Its rings were found to be extremely variable in thickness and transparency.' in `merged.md` -- Directly stated. |
| 8 | Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus' smaller moons. | 7 | carried | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.' in `merged.md` -- Directly stated. |
| 9 | Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers). | 7 | carried | 'In flying by Miranda at a range of only 17.560 miles (28.260 kilometers)' in `merged.md` -- Directly stated. |
| 10 | Flying by Miranda was the closest the spacecraft had come to any object so far in its travels. | 7 | carried | 'the spacecraft came closest to any object so far in its nearly century-long travels' in `merged.md` -- Stated. |
| 11 | Uranus itself appeared generally featureless. | 7 | carried | 'Uranus itself appeared generally featureless.' in `merged.md` -- Directly stated. |
| 12 | The Uranus encounter news was interrupted the same day by the Challenger accident. | 9 | carried | 'The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident' in `merged.md` -- Directly stated. |
| 13 | The Challenger accident killed six astronauts during their space shuttle launch. | 9 | carried | 'the tragic Challenger accident that killed six astronauts during their space shuttle launch' in `merged.md` -- Directly stated. |
| 14 | The Challenger space shuttle launch took place on Feb. 28, 1986. | 9 | carried | 'space shuttle launch Feb. 28, 1986' in `merged.md` -- Directly stated. |

### `merged.md` -- 27 claim(s): 0 invented, 0 contradicted, 0 supported in part, 0 supported, 27 not checked

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Voyager 2 had fulfilled its primary mission goals with the three planetary encounters. | not checked | -- | the pass did not report on this claim |
| 2 | Mission planners directed Voyager 2 to Uranus. | not checked | -- | the pass did not report on this claim |
| 3 | The journey to Uranus would take about 4,5 years. | not checked | -- | the pass did not report on this claim |
| 4 | Voyager 2's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | not checked | -- | the pass did not report on this claim |
| 5 | The Uranus encounter's geometry was defined by the possibility of a future encounter with Saturn. | not checked | -- | the pass did not report on this claim |
| 6 | Voyager 2 had only 6.4 days of close study during its Uranus flyby. | not checked | -- | the pass did not report on this claim |
| 7 | Voyager 2 was the first human-made object to fly past Uranus. | not checked | -- | the pass did not report on this claim |
| 8 | Voyager 2's short-range observations of Uranus began Jan. 31, 1987. | not checked | -- | the pass did not report on this claim |
| 9 | Signals took approximately 2,5 hours to reach Earth when observations began. | not checked | -- | the pass did not report on this claim |
| 10 | Light conditions at Uranus were five-hundred times less than terrestrial conditions. | not checked | -- | the pass did not report on this claim |
| 11 | Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968. | not checked | -- | the pass did not report on this claim |
| 12 | Closest approach to Uranus was at a range of about 50,640 kilometers (81,500 miles). | not checked | -- | the pass did not report on this claim |
| 13 | Voyager 2 discovered 11 new moons during its Uranus flyby. | not checked | -- | the pass did not report on this claim |
| 14 | The moons' names allude to Goethe. | not checked | -- | the pass did not report on this claim |
| 15 | The moon naming tradition was begun in 1687. | not checked | -- | the pass did not report on this claim |
| 16 | Voyager 2 discovered three new rings in addition to the "older" eight rings. | not checked | -- | the pass did not report on this claim |
| 17 | Voyager 2 found a magnetic field tilted at 66 degrees off-axis and off-center. | not checked | -- | the pass did not report on this claim |
| 18 | Voyager 2 found wind speeds in Uranus' atmosphere as high as 450 km/h (72400 meters per hour). | not checked | -- | the pass did not report on this claim |
| 19 | Voyager 2 found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface. | not checked | -- | the pass did not report on this claim |
| 20 | Uranus' rings were found to be extremely variable in thickness and transparency. | not checked | -- | the pass did not report on this claim |
| 21 | Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus' smaller moons. | not checked | -- | the pass did not report on this claim |
| 22 | Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers). | not checked | -- | the pass did not report on this claim |
| 23 | The Miranda flyby was the closest the spacecraft had come to any object so far in its travels. | not checked | -- | the pass did not report on this claim |
| 24 | Voyager 2's travels were nearly century-long. | not checked | -- | the pass did not report on this claim |
| 25 | Uranus itself appeared generally featureless. | not checked | -- | the pass did not report on this claim |
| 26 | The Challenger accident interrupted the news of the Uranus encounter the same day. | not checked | -- | the pass did not report on this claim |
| 27 | The Challenger accident killed six astronauts during their space shuttle launch Feb. 28, 1986. | not checked | -- | the pass did not report on this claim |

## Structure

**9** mechanical check(s) over **16** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **27** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **26**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 2 run(s) over 14 attributed segment(s) — each source in one unbroken block. 2 of 2 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Verbatim violation — an invariant-core token did not survive unchanged

- `a2` (`source_a.md`) — numeric '3' (had) does not survive into the merge unchanged
- `a4` (`source_a.md`) — numeric '1' (had) does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '1' does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **4** departure(s) from its sources. Checking them confirms 1, rejects 3, and leaves 0 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 16 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | duplicate | Same title as base. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `a2` | reworded | Spacecraft name corrected to match title. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-001 came back CONTRADICTED (`A-001`) |
| `a4` | reworded | Typo 'Ur anus' fixed; spacecraft name corrected. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-006 came back CONTRADICTED (`A-006`) |
| `a5` | reworded | Spacecraft name corrected to match title. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-007 came back CONTRADICTED, A-008 came back CONTRADICTED (`A-007`, `A-008`) |

## Added from outside the documents

The merge declared 3 statement(s) that your documents do not contain. **Nothing here has been verified against them**, because they are the only thing this tool checks against. Each is the model's own claim, and reviewing them is the reader's job rather than the tool's.

LLossless did not fetch, resolve or check any source listed here. LLossless itself opens no socket to do it. No call the model made took more turns than a call that retrieves nothing can take, so it retrieved nothing and every source here is recalled rather than looked up. **This run was made at fidelity sourced, which asks the model to retrieve rather than recall, and nothing was retrieved.** Every source listed here is therefore a recollection, exactly as it would be at open.

3 of them correct(s) something a document states. A correction is a departure from your documents, so it is also reported as a finding and it moves the exit code: nothing here can tell a correction from a corruption, and the declaration buys you this row rather than a clean run.

| Statement | Corrects | Basis | Source | The merge's reason | Claims it covers |
|---|---|---|---|---|---|
| Although Voyager 2 had fulfilled its primary mission goals with the three planetary encounters | Although Voyager 3 had fulfilled its primary mission goals | the model's own knowledge | *no source* | Title and other segments say Voyager 2; no Voyager 3 encountered Uranus. | *none* |
| Voyager 2 had only 6.4 days of close study during its flyby. | Voyager 1 had only 6.4 days of close study during its flyby. | the model's own knowledge | *no source* | Document is about Voyager 2's Uranus flyby. | *none* |
| Voyager 2's short-range observations of the planet began Jan. 31, 1987 | Voyager 1's short-range observations of the planet began Jan. 31, 1987 | the model's own knowledge | *no source* | Voyager 2 alone flew past Uranus. | *none* |

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
| Duration | 79.9s |
| Generated | 2026-09-26T16:13:41+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `6d8a835cc983` |
| Prompt | `prompts/verify.md` `55a721b20905` |
| Prompt | `prompts/verify_reverse.md` `2a6d7e955709` |

> **Document content was handed to a program on this machine (`Claude Code - Sonnet`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The model was permitted to reach the network** (WebSearch, WebFetch), so a query or a fetch it made may have carried text from these documents to a third party. No tool use (6 call(s), 6 turn(s) in total), counted in turns rather than in fetches. LLossless itself made no network request of any kind and resolved none of the sources the merge names.

> **This run was made at fidelity sourced, which asks the model to retrieve rather than recall, and it retrieved nothing.** Every source the merge names is therefore a recollection, exactly as it would be one level down.

> **1 unit(s) of work errored.** The model could not be made to answer in a usable form. This run is inconclusive: coverage below is computed over the units that did answer, and the exit code is 2 regardless of what they said.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
