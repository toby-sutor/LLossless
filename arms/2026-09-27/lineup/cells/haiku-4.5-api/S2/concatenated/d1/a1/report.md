## Verdict

**1 finding(s).** In the claims: 1 contradicted.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 12 |
| Claims extracted from `source_a.md` | 10 |
| Claims extracted from `source_b.md` | 9 |
| Forward — source claims accounted for in the merge | **18/19** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **10/10** |
| Forward — `source_b.md` claims accounted for | **8/9** |
| Reverse — merge claims found in a source | **12/12** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **31/31** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **B-004** -- the two documents disagree
  - `source_b.md:7` says: A full peal required fewer than eight ringers to not be attempted.
  - `merged.md` says: 'A full peal needs eight ringers' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text states a full peal needs eight ringers, which contradicts the claim that fewer than eight ringers were required to not attempt a peal.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 10 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 10 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Six bells hang in the tower on Carrow Hill. | 3 | carried | 'Six bells hang in the tower on Carrow Hill' in `merged.md` -- The reference text directly states that six bells hang in the tower on Carrow Hill. |
| 2 | No bell has been added or taken away since the tower was raised. | 3 | carried | 'no bell has been added or taken away since the tower was raised' in `merged.md` -- The reference text explicitly states that no bell has been added or taken away since the tower was raised. |
| 3 | All six bells were cast in 1782. | 5 | carried | 'All six were cast in 1782 by a founder who put his mark on the tenor alone.' in `merged.md` -- The reference text states all six bells were cast in 1782. |
| 4 | The bells were cast by a founder who put his mark on the tenor alone. | 5 | carried | 'All six were cast in 1782 by a founder who put his mark on the tenor alone.' in `merged.md` -- The reference text states the bells were cast by a founder who put his mark on the tenor alone. |
| 5 | A full peal needs eight ringers. | 7 | carried | 'A full peal needs eight ringers' in `merged.md` -- The reference text directly states that a full peal needs eight ringers. |
| 6 | The band could never attempt a full peal while a single ringer was missing. | 7 | carried | 'the band could never attempt one while a single ringer was missing' in `merged.md` -- The reference text states the band could never attempt a full peal while a single ringer was missing. |
| 7 | Once the ringing starts a full peal runs for two hours. | 9 | carried | 'Once the ringing starts a full peal runs for two hours' in `merged.md` -- The reference text directly states that once the ringing starts a full peal runs for two hours. |
| 8 | The band works through a full peal without a break. | 9 | carried | 'the band works through it without a break' in `merged.md` -- The reference text states the band works through a full peal without a break. |
| 9 | The bells are rung on the first Sunday of every month. | 11 | carried | 'The bells are rung on the first Sunday of every month' in `merged.md` -- The reference text directly states the bells are rung on the first Sunday of every month. |
| 10 | The village has always kept the hour by the bells. | 11 | carried | 'the village has always kept the hour by them' in `merged.md` -- The reference text states the village has always kept the hour by the bells. |

### `source_b.md` -- 9 claim(s): 0 dropped, 1 contradicted, 0 carried in part, 8 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 4 | A full peal required fewer than eight ringers to not be attempted. | 7 | contradicted | 'A full peal needs eight ringers' in `merged.md` -- The reference text states a full peal needs eight ringers, which contradicts the claim that fewer than eight ringers were required to not attempt a peal. |
| 1 | There were six bells in the tower above the village. | 3 | carried | 'we found six of them in the tower above the village' in `merged.md` -- The reference text states that six bells were found in the tower above the village. |
| 2 | The founder cut the year 1782 into the tenor. | 5 | carried | 'The founder cut the year 1782 into the tenor' in `merged.md` -- The reference text directly states the founder cut the year 1782 into the tenor. |
| 3 | The tenor was the only bell the founder signed. | 5 | carried | 'that was the only bell he signed' in `merged.md` -- The reference text states the tenor was the only bell the founder signed. |
| 5 | One absence was enough to call the whole thing off. | 7 | carried | 'one absence was enough to call the whole thing off' in `merged.md` -- The reference text states one absence was enough to call the whole thing off. |
| 6 | A full peal took two hours from the first stroke to the last. | 9 | carried | 'From the first stroke to the last a full peal took two hours' in `merged.md` -- The reference text states a full peal took two hours from the first stroke to the last. |
| 7 | Nobody left the ringing chamber during a full peal. | 9 | carried | 'nobody left the ringing chamber in between' in `merged.md` -- The reference text states nobody left the ringing chamber during a full peal. |
| 8 | Bells were rung on the first Sunday of the month, every month. | 11 | carried | 'We rang on the first Sunday of the month, every month' in `merged.md` -- The reference text states bells were rung on the first Sunday of the month, every month. |
| 9 | People in the village knew the hour from the sound of the bells. | 11 | carried | 'people in the village knew the hour from the sound' in `merged.md` -- The reference text states people in the village knew the hour from the sound of the bells. |

### `merged.md` -- 12 claim(s): 0 invented, 0 contradicted, 0 supported in part, 12 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Six bells hang in the tower on Carrow Hill. | supported | `source_a.md` | 'Six bells hang in the tower on Carrow Hill' in `source_a.md` -- Source A directly states this claim about the six bells in the tower on Carrow Hill. |
| 2 | No bell has been added or taken away since the tower was raised. | supported | `source_a.md` | 'no bell has been added or taken away since the tower was raised' in `source_a.md` -- Source A explicitly states that no bell has been added or taken away since the tower was raised. |
| 3 | All six bells were cast in 1782. | supported | `source_a.md` | 'All six were cast in 1782 by a founder' in `source_a.md` -- Source A states all six bells were cast in 1782 by a founder. |
| 4 | The founder put his mark on the tenor alone. | supported | `source_a.md` | 'a founder who put his mark on the tenor alone' in `source_a.md` -- Source A states the founder put his mark on the tenor alone. |
| 5 | The founder cut the year 1782 into the tenor. | supported | `source_b.md` | 'The founder cut the year 1782 into the tenor' in `source_b.md` -- Source B explicitly states the founder cut the year 1782 into the tenor. |
| 6 | The tenor was the only bell the founder signed. | supported | `source_b.md` | 'that was the only bell he signed' in `source_b.md` -- Source B states that the tenor was the only bell the founder signed. |
| 7 | A full peal needs eight ringers. | supported | `source_a.md` | 'A full peal needs eight ringers' in `source_a.md` -- Source A directly states that a full peal needs eight ringers. |
| 8 | A full peal runs for two hours. | supported | `source_a.md` | 'Once the ringing starts a full peal runs for two hours' in `source_a.md` -- Source A states that a full peal runs for two hours once ringing starts. |
| 9 | The band works through a full peal without a break. | supported | `source_a.md` | 'the band works through it without a break' in `source_a.md` -- Source A states the band works through a full peal without a break. |
| 10 | From the first stroke to the last a full peal took two hours. | supported | `source_b.md` | 'From the first stroke to the last a full peal took two hours' in `source_b.md` -- Source B explicitly states this claim about the duration of a full peal. |
| 11 | Nobody left the ringing chamber in between during a full peal. | supported | `source_b.md` | 'nobody left the ringing chamber in between' in `source_b.md` -- Source B states that nobody left the ringing chamber during a full peal. |
| 12 | The bells are rung on the first Sunday of every month. | supported | `source_a.md` | 'The bells are rung on the first Sunday of every month' in `source_a.md` -- Source A directly states the bells are rung on the first Sunday of every month. |

## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | ec0c9ecb43e3 (hosted) |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | none — this run made no merge |
| Model (decompose) | claude-haiku-4-5-20251001 |
| Model (verify) | claude-haiku-4-5-20251001 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile anthropic, effort decompose one level (extended thinking on/off; default kept), verify one level (extended thinking on/off; default kept) |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 5 live, 0 cached, 0 replayed |
| Tokens | 8,090 in, 4,202 out |
| Cost | ~$0.03 estimated (rates read 2026-08-31) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 31.3s |
| Generated | 2026-09-27T17:41:22+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
