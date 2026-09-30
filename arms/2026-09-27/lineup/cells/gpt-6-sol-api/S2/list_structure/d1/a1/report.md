## Verdict

**No extracted claim was dropped, contradicted, invented, or carried only in part.** 10 source claim(s) checked against the merge, 8 merge claim(s) checked against the sources. This covers the claims that were extracted, not the documents: titles, headings and formatting are not claims and were not checked.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 8 |
| Claims extracted from `source_a.md` | 5 |
| Claims extracted from `source_b.md` | 5 |
| Forward — source claims accounted for in the merge | **10/10** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **5/5** |
| Forward — `source_b.md` claims accounted for | **5/5** |
| Reverse — merge claims found in a source | **8/8** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **18/18** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

None.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 5 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 5 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Vandrell Relay is a fictional HTTP relay. | 3 | carried | 'Vandrell Relay is a fictional HTTP relay.' in `merged.md` -- The reference states the claim directly. |
| 2 | Vandrell Relay's listen port is 8443. | 7 | carried | '- Listen port: 8443' in `merged.md` -- The listed listen port is 8443. |
| 3 | Vandrell Relay's connect timeout is 30 seconds. | 8 | carried | '- Connect timeout: 30 seconds' in `merged.md` -- The listed connect timeout is 30 seconds. |
| 4 | Vandrell Relay's maximum concurrent connections is 512. | 12 | carried | '- Maximum concurrent connections: 512' in `merged.md` -- The listed maximum concurrent connections is 512. |
| 5 | Vandrell Relay's retry attempts is 3. | 13 | carried | '- Retry attempts: 3' in `merged.md` -- The listed number of retry attempts is 3. |

### `source_b.md` -- 5 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 5 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Vandrell Relay is a fictional HTTP relay. | 3 | carried | 'Vandrell Relay is a fictional HTTP relay.' in `merged.md` -- The reference states the claim directly. |
| 2 | Vandrell Relay's connect timeout is 30 seconds. | 7 | carried | '- Connect timeout: 30 seconds' in `merged.md` -- The listed connect timeout is 30 seconds. |
| 3 | Vandrell Relay's read timeout is 120 seconds. | 8 | carried | '- Read timeout: 120 seconds' in `merged.md` -- The listed read timeout is 120 seconds. |
| 4 | Vandrell Relay's access log format is JSON Lines. | 12 | carried | '- Access log format: JSON Lines' in `merged.md` -- The listed access log format is JSON Lines. |
| 5 | Vandrell Relay's health check path is /-/healthy. | 13 | carried | '- Health check path: /-/healthy' in `merged.md` -- The listed health check path is /-/healthy. |

### `merged.md` -- 8 claim(s): 0 invented, 0 contradicted, 0 supported in part, 8 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Vandrell Relay is a fictional HTTP relay. | supported | `source_a.md` | 'Vandrell Relay is a fictional HTTP relay.' in `source_a.md` -- The source states this directly. |
| 2 | Vandrell Relay's listen port is 8443. | supported | `source_a.md` | '- Listen port: 8443' in `source_a.md` -- The source gives 8443 as the listen port. |
| 3 | Vandrell Relay's connect timeout is 30 seconds. | supported | `source_a.md` | '- Connect timeout: 30 seconds' in `source_a.md` -- The source gives a connect timeout of 30 seconds. |
| 4 | Vandrell Relay's read timeout is 120 seconds. | supported | `source_b.md` | '- Read timeout: 120 seconds' in `source_b.md` -- The source gives a read timeout of 120 seconds. |
| 5 | Vandrell Relay's maximum concurrent connections is 512. | supported | `source_a.md` | '- Maximum concurrent connections: 512' in `source_a.md` -- The source gives 512 as the maximum concurrent connections. |
| 6 | Vandrell Relay's retry attempts is 3. | supported | `source_a.md` | '- Retry attempts: 3' in `source_a.md` -- The source gives 3 retry attempts. |
| 7 | Vandrell Relay's access log format is JSON Lines. | supported | `source_b.md` | '- Access log format: JSON Lines' in `source_b.md` -- The source gives JSON Lines as the access log format. |
| 8 | Vandrell Relay's health check path is /-/healthy. | supported | `source_b.md` | '- Health check path: /-/healthy' in `source_b.md` -- The source gives /-/healthy as the health check path. |

## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | bf7d5842201d (hosted) |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | none — this run made no merge |
| Model (decompose) | gpt-6-sol |
| Model (verify) | gpt-6-sol |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed 0, thinking decompose, merge, verify, profile openai-reasoning |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 5 live, 0 cached, 0 replayed |
| Tokens | 6,528 in, 2,118 out, 0 cached, 277 reasoning |
| Cost | ~$0.03 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 26.5s |
| Generated | 2026-09-27T16:57:16+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `bf7d5842201d`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
