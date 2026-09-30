## Verdict

**1 finding(s).** In the claims: 1 dropped.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 10 |
| Claims extracted from `source_a.md` | 6 |
| Claims extracted from `source_b.md` | 7 |
| Forward — source claims accounted for in the merge | **12/13** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **6/6** |
| Forward — `source_b.md` claims accounted for | **6/7** |
| Reverse — merge claims found in a source | **10/10** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **22/22** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Dropped — in a source, not in the merge

- **B-004** (`source_b.md:13`) — Access logs are written in JSON Lines format.
  - judged against: `merged.md`
  - rationale: The reference text does not mention log format or JSON Lines anywhere.

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
| 2 | The default connect timeout is 30 seconds. | 8 | carried | 'The default connect timeout is 30 seconds.' in `merged.md` -- Directly stated in the Networking section. |
| 3 | The default read timeout is 120 seconds. | 9 | carried | 'The default read timeout is 120 seconds.' in `merged.md` -- Directly stated in the Networking section. |
| 4 | The relay accepts at most 512 concurrent connections. | 13 | carried | 'The relay accepts at most 512 concurrent connections.' in `merged.md` -- Directly stated in the Limits section. |
| 5 | Each request is retried at most 3 times. | 14 | carried | 'Each request is retried at most 3 times.' in `merged.md` -- Directly stated in the Limits section. |
| 6 | The minimum accepted TLS version is TLS 1.2. | 18 | carried | 'The minimum accepted TLS version is TLS 1.2.' in `merged.md` -- Directly stated in the Security section. |

### `source_b.md` -- 7 claim(s): 1 dropped, 0 contradicted, 0 carried in part, 6 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 4 | Access logs are written in JSON Lines format. | 13 | dropped | The reference text does not mention log format or JSON Lines anywhere. |
| 1 | The relay listens on port 8443 by default. | 7 | carried | 'The relay listens on port 8443 by default.' in `merged.md` -- Directly stated in the Networking section. |
| 2 | The relay accepts at most 512 concurrent connections. | 8 | carried | 'The relay accepts at most 512 concurrent connections.' in `merged.md` -- Directly stated in the Limits section. |
| 3 | One worker process is started per CPU core. | 9 | carried | 'One worker process is started per CPU core.' in `merged.md` -- Directly stated in the Limits section. |
| 5 | Log files are rotated when they reach 100 megabytes. | 14 | carried | 'Log files are rotated when they reach 100 megabytes.' in `merged.md` -- Directly stated in the Logging and health section. |
| 6 | The health check endpoint is /-/healthy. | 18 | carried | 'The health check endpoint is /-/healthy.' in `merged.md` -- Directly stated in the Logging and health section. |
| 7 | A relay that fails 3 consecutive health checks is removed from rotation. | 19 | carried | 'A relay that fails 3 consecutive health checks is removed from rotation.' in `merged.md` -- Directly stated in the Logging and health section. |

### `merged.md` -- 10 claim(s): 0 invented, 0 contradicted, 0 supported in part, 10 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | The relay listens on port 8443 by default. | supported | `source_a.md` | 'The relay listens on port 8443 by default.' in `source_a.md` -- Directly stated in source_a.md and also matched in source_b.md. |
| 2 | The default connect timeout is 30 seconds. | supported | `source_a.md` | 'The default connect timeout is 30 seconds.' in `source_a.md` -- Directly stated in source_a.md. |
| 3 | The default read timeout is 120 seconds. | supported | `source_a.md` | 'The default read timeout is 120 seconds.' in `source_a.md` -- Directly stated in source_a.md. |
| 4 | The relay accepts at most 512 concurrent connections. | supported | `source_a.md` | 'The relay accepts at most 512 concurrent connections.' in `source_a.md` -- Directly stated in source_a.md and also matched in source_b.md. |
| 5 | Each request is retried at most 3 times. | supported | `source_a.md` | 'Each request is retried at most 3 times.' in `source_a.md` -- Directly stated in source_a.md. |
| 6 | One worker process is started per CPU core. | supported | `source_b.md` | 'One worker process is started per CPU core.' in `source_b.md` -- Directly stated in source_b.md. |
| 7 | The minimum accepted TLS version is TLS 1.2. | supported | `source_a.md` | 'The minimum accepted TLS version is TLS 1.2.' in `source_a.md` -- Directly stated in source_a.md. |
| 8 | Log files are rotated when they reach 100 megabytes. | supported | `source_b.md` | 'Log files are rotated when they reach 100 megabytes.' in `source_b.md` -- Directly stated in source_b.md. |
| 9 | The health check endpoint is /-/healthy. | supported | `source_b.md` | 'The health check endpoint is /-/healthy.' in `source_b.md` -- Directly stated in source_b.md. |
| 10 | A relay that fails 3 consecutive health checks is removed from rotation. | supported | `source_b.md` | 'A relay that fails 3 consecutive health checks is removed from rotation.' in `source_b.md` -- Directly stated in source_b.md. |

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
| Calls | 6 live, 0 cached, 0 replayed |
| Tokens | 13,811 in, 4,725 out |
| Cost | ~$0.07 estimated (rates read 2026-08-31) |
| Schema repairs | 1 |
| Errors | 0 |
| Duration | 36.7s |
| Generated | 2026-09-27T17:31:02+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
