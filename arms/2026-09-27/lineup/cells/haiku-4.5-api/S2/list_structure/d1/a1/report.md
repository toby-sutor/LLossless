## Verdict

**No extracted claim was dropped, contradicted, invented, or carried only in part.** 8 source claim(s) checked against the merge, 7 merge claim(s) checked against the sources. This covers the claims that were extracted, not the documents: titles, headings and formatting are not claims and were not checked.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 7 |
| Claims extracted from `source_a.md` | 4 |
| Claims extracted from `source_b.md` | 4 |
| Forward — source claims accounted for in the merge | **8/8** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **4/4** |
| Forward — `source_b.md` claims accounted for | **4/4** |
| Reverse — merge claims found in a source | **7/7** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **15/15** |
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

### `source_a.md` -- 4 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 4 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Vandrell Relay listens on port 8443. | 7 | carried | 'Listen port: 8443' in `merged.md` -- The reference text states the listen port is 8443, which means Vandrell Relay listens on port 8443. |
| 2 | The connect timeout is 30 seconds. | 8 | carried | 'Connect timeout: 30 seconds' in `merged.md` -- The reference text directly states the connect timeout is 30 seconds. |
| 3 | The maximum concurrent connections is 512. | 12 | carried | 'Maximum concurrent connections: 512' in `merged.md` -- The reference text directly states the maximum concurrent connections is 512. |
| 4 | Retry attempts is 3. | 13 | carried | 'Retry attempts: 3' in `merged.md` -- The reference text directly states retry attempts is 3. |

### `source_b.md` -- 4 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 4 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Connect timeout is 30 seconds. | 7 | carried | 'Connect timeout: 30 seconds' in `merged.md` -- The reference text directly states connect timeout is 30 seconds. |
| 2 | Read timeout is 120 seconds. | 8 | carried | 'Read timeout: 120 seconds' in `merged.md` -- The reference text directly states read timeout is 120 seconds. |
| 3 | Access log format is JSON Lines. | 12 | carried | 'Access log format: JSON Lines' in `merged.md` -- The reference text directly states access log format is JSON Lines. |
| 4 | Health check path is /-/healthy. | 13 | carried | 'Health check path: /-/healthy' in `merged.md` -- The reference text directly states health check path is /-/healthy. |

### `merged.md` -- 7 claim(s): 0 invented, 0 contradicted, 0 supported in part, 7 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Vandrell Relay listens on port 8443. | supported | `source_a.md` | 'Listen port: 8443' in `source_a.md` -- Source A directly states the listen port is 8443. |
| 2 | The connect timeout is 30 seconds. | supported | `source_a.md` | 'Connect timeout: 30 seconds' in `source_a.md` -- Both sources state the connect timeout is 30 seconds; source A is quoted. |
| 3 | The read timeout is 120 seconds. | supported | `source_b.md` | 'Read timeout: 120 seconds' in `source_b.md` -- Source B directly states the read timeout is 120 seconds. |
| 4 | The maximum concurrent connections is 512. | supported | `source_a.md` | 'Maximum concurrent connections: 512' in `source_a.md` -- Source A directly states the maximum concurrent connections is 512. |
| 5 | Retry attempts is 3. | supported | `source_a.md` | 'Retry attempts: 3' in `source_a.md` -- Source A directly states retry attempts is 3. |
| 6 | The access log format is JSON Lines. | supported | `source_b.md` | 'Access log format: JSON Lines' in `source_b.md` -- Source B directly states the access log format is JSON Lines. |
| 7 | The health check path is /-/healthy. | supported | `source_b.md` | 'Health check path: /-/healthy' in `source_b.md` -- Source B directly states the health check path is /-/healthy. |

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
| Tokens | 7,159 in, 1,854 out |
| Cost | ~$0.02 estimated (rates read 2026-08-31) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 15.2s |
| Generated | 2026-09-27T17:49:07+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
