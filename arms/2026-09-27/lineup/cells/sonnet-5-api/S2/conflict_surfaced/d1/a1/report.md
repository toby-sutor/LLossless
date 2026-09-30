## Verdict

**No extracted claim was dropped, contradicted, invented, or carried only in part.** 11 source claim(s) checked against the merge, 10 merge claim(s) checked against the sources. This covers the claims that were extracted, not the documents: titles, headings and formatting are not claims and were not checked.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 10 |
| Claims extracted from `source_a.md` | 6 |
| Claims extracted from `source_b.md` | 5 |
| Forward — source claims accounted for in the merge | **11/11** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **6/6** |
| Forward — `source_b.md` claims accounted for | **5/5** |
| Reverse — merge claims found in a source | **10/10** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **21/21** |
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

### `source_a.md` -- 6 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 6 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The relay listens on port 8443 by default. | 7 | carried | 'The relay listens on port 8443 by default.' in `merged.md` -- Directly stated in the Networking section. |
| 2 | The default connect timeout is 30 seconds. | 8 | carried | 'According to the Operator Guide, the default connect timeout is 30 seconds.' in `merged.md` -- The Operator Guide attributed value of 30 seconds is stated in the reference text. |
| 3 | The default read timeout is 120 seconds. | 9 | carried | 'The default read timeout is 120 seconds.' in `merged.md` -- Directly stated in the Networking section. |
| 4 | The relay accepts at most 512 concurrent connections. | 13 | carried | 'The relay accepts at most 512 concurrent connections.' in `merged.md` -- Directly stated in the Limits section. |
| 5 | Each request is retried at most 3 times. | 14 | carried | 'Each request is retried at most 3 times.' in `merged.md` -- Directly stated in the Limits section. |
| 6 | The minimum accepted TLS version is TLS 1.2. | 18 | carried | 'The minimum accepted TLS version is TLS 1.2.' in `merged.md` -- Directly stated in the Security section. |

### `source_b.md` -- 5 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 5 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The relay listens on port 8443 by default. | 7 | carried | 'The relay listens on port 8443 by default.' in `merged.md` -- Directly stated in the Networking section. |
| 2 | The default connect timeout is 60 seconds. | 8 | carried | 'According to the Deployment Notes, the default connect timeout is 60 seconds.' in `merged.md` -- The Deployment Notes attributed value of 60 seconds is stated in the reference text. |
| 3 | The default read timeout is 120 seconds. | 9 | carried | 'The default read timeout is 120 seconds.' in `merged.md` -- Directly stated in the Networking section. |
| 4 | Access logs are written in JSON Lines format. | 13 | carried | 'Access logs are written in JSON Lines format.' in `merged.md` -- Directly stated in the Operations section. |
| 5 | The health check endpoint is /-/healthy. | 14 | carried | 'The health check endpoint is /-/healthy.' in `merged.md` -- Directly stated in the Operations section. |

### `merged.md` -- 10 claim(s): 0 invented, 0 contradicted, 0 supported in part, 10 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Vandrell Relay is a fictional HTTP relay. | supported | `source_a.md` | 'Vandrell Relay is a fictional HTTP relay.' in `source_a.md` -- Both sources state this exact sentence. |
| 2 | The relay listens on port 8443 by default. | supported | `source_a.md` | 'The relay listens on port 8443 by default.' in `source_a.md` -- Both sources state this exact sentence. |
| 3 | The default read timeout is 120 seconds. | supported | `source_a.md` | 'The default read timeout is 120 seconds.' in `source_a.md` -- Both sources agree on this value. |
| 4 | According to the Operator Guide, the default connect timeout is 30 seconds. | supported | `source_a.md` | 'The default connect timeout is 30 seconds.' in `source_a.md` -- source_a.md is titled Operator Guide and states this timeout value. |
| 5 | According to the Deployment Notes, the default connect timeout is 60 seconds. | supported | `source_b.md` | 'The default connect timeout is 60 seconds.' in `source_b.md` -- source_b.md is titled Deployment Notes and states this timeout value. |
| 6 | The relay accepts at most 512 concurrent connections. | supported | `source_a.md` | 'The relay accepts at most 512 concurrent connections.' in `source_a.md` -- Directly stated in source_a.md. |
| 7 | Each request is retried at most 3 times. | supported | `source_a.md` | 'Each request is retried at most 3 times.' in `source_a.md` -- Directly stated in source_a.md. |
| 8 | The minimum accepted TLS version is TLS 1.2. | supported | `source_a.md` | 'The minimum accepted TLS version is TLS 1.2.' in `source_a.md` -- Directly stated in source_a.md. |
| 9 | Access logs are written in JSON Lines format. | supported | `source_b.md` | 'Access logs are written in JSON Lines format.' in `source_b.md` -- Directly stated in source_b.md. |
| 10 | The health check endpoint is /-/healthy. | supported | `source_b.md` | 'The health check endpoint is /-/healthy.' in `source_b.md` -- Directly stated in source_b.md. |

## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | ec0c9ecb43e3 (hosted) |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | none — this run made no merge |
| Model (decompose) | claude-sonnet-5 |
| Model (verify) | claude-sonnet-5 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile anthropic |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 5 live, 0 cached, 0 replayed |
| Tokens | 10,272 in, 3,625 out |
| Cost | ~$0.06 estimated (rates read 2026-08-31) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 29.1s |
| Generated | 2026-09-27T17:16:52+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
