## Verdict

**1 finding(s).** In the claims: 1 dropped.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 11 |
| Claims extracted from `source_a.md` | 7 |
| Claims extracted from `source_b.md` | 8 |
| Forward — source claims accounted for in the merge | **14/15** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **7/7** |
| Forward — `source_b.md` claims accounted for | **7/8** |
| Reverse — merge claims found in a source | **11/11** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **25/25** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Dropped — in a source, not in the merge

- **B-005** (`source_b.md:13`) — Access logs are written in JSON Lines format.
  - judged against: `merged.md`
  - rationale: The reference does not specify the format of access logs.

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
| 1 | Vandrell Relay is a fictional HTTP relay. | 3 | carried | 'Vandrell Relay is a fictional HTTP relay.' in `merged.md` -- The reference states the claim directly. |
| 2 | The relay listens on port 8443 by default. | 7 | carried | 'The relay listens on port 8443 by default.' in `merged.md` -- The reference states the claim directly. |
| 3 | The default connect timeout is 30 seconds. | 8 | carried | 'The default connect timeout is 30 seconds.' in `merged.md` -- The reference states the claim directly. |
| 4 | The default read timeout is 120 seconds. | 9 | carried | 'The default read timeout is 120 seconds.' in `merged.md` -- The reference states the claim directly. |
| 5 | The relay accepts at most 512 concurrent connections. | 13 | carried | 'The relay accepts at most 512 concurrent connections.' in `merged.md` -- The reference states the claim directly. |
| 6 | Each request is retried at most 3 times. | 14 | carried | 'Each request is retried at most 3 times.' in `merged.md` -- The reference states the claim directly. |
| 7 | The minimum accepted TLS version is TLS 1.2. | 18 | carried | 'The minimum accepted TLS version is TLS 1.2.' in `merged.md` -- The reference states the claim directly. |

### `source_b.md` -- 8 claim(s): 1 dropped, 0 contradicted, 0 carried in part, 7 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 5 | Access logs are written in JSON Lines format. | 13 | dropped | The reference does not specify the format of access logs. |
| 1 | Vandrell Relay is a fictional HTTP relay. | 3 | carried | 'Vandrell Relay is a fictional HTTP relay.' in `merged.md` -- The reference states the claim directly. |
| 2 | The relay listens on port 8443 by default. | 7 | carried | 'The relay listens on port 8443 by default.' in `merged.md` -- The reference states the claim directly. |
| 3 | The relay accepts at most 512 concurrent connections. | 8 | carried | 'The relay accepts at most 512 concurrent connections.' in `merged.md` -- The reference states the claim directly. |
| 4 | One worker process is started per CPU core. | 9 | carried | 'One worker process is started per CPU core.' in `merged.md` -- The reference states the claim directly. |
| 6 | Log files are rotated when they reach 100 megabytes. | 14 | carried | 'Log files are rotated when they reach 100 megabytes.' in `merged.md` -- The reference states the claim directly. |
| 7 | The health check endpoint is /-/healthy. | 18 | carried | 'The health check endpoint is /-/healthy.' in `merged.md` -- The reference states the claim directly. |
| 8 | A relay that fails 3 consecutive health checks is removed from rotation. | 19 | carried | 'A relay that fails 3 consecutive health checks is removed from rotation.' in `merged.md` -- The reference states the claim directly. |

### `merged.md` -- 11 claim(s): 0 invented, 0 contradicted, 0 supported in part, 11 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Vandrell Relay is a fictional HTTP relay. | supported | `source_a.md` | 'Vandrell Relay is a fictional HTTP relay.' in `source_a.md` -- The source states this directly. |
| 2 | The relay listens on port 8443 by default. | supported | `source_a.md` | 'The relay listens on port 8443 by default.' in `source_a.md` -- The source states the default listening port. |
| 3 | The default connect timeout is 30 seconds. | supported | `source_a.md` | 'The default connect timeout is 30 seconds.' in `source_a.md` -- The source states the default connect timeout. |
| 4 | The default read timeout is 120 seconds. | supported | `source_a.md` | 'The default read timeout is 120 seconds.' in `source_a.md` -- The source states the default read timeout. |
| 5 | The relay accepts at most 512 concurrent connections. | supported | `source_a.md` | 'The relay accepts at most 512 concurrent connections.' in `source_a.md` -- The source states the concurrent connection limit. |
| 6 | Each request is retried at most 3 times. | supported | `source_a.md` | 'Each request is retried at most 3 times.' in `source_a.md` -- The source states the retry limit. |
| 7 | One worker process is started per CPU core. | supported | `source_b.md` | 'One worker process is started per CPU core.' in `source_b.md` -- The source states the worker-process allocation. |
| 8 | The minimum accepted TLS version is TLS 1.2. | supported | `source_a.md` | 'The minimum accepted TLS version is TLS 1.2.' in `source_a.md` -- The source states the minimum accepted TLS version. |
| 9 | Log files are rotated when they reach 100 megabytes. | supported | `source_b.md` | 'Log files are rotated when they reach 100 megabytes.' in `source_b.md` -- The source states the log rotation threshold. |
| 10 | The health check endpoint is /-/healthy. | supported | `source_b.md` | 'The health check endpoint is /-/healthy.' in `source_b.md` -- The source states the health check endpoint. |
| 11 | A relay that fails 3 consecutive health checks is removed from rotation. | supported | `source_b.md` | 'A relay that fails 3 consecutive health checks is removed from rotation.' in `source_b.md` -- The source states when a relay is removed from rotation. |

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
| Calls | 6 live, 0 cached, 0 replayed |
| Tokens | 9,320 in, 3,947 out, 0 cached, 303 reasoning |
| Cost | ~$0.06 estimated (rates read 2026-09-25) |
| Schema repairs | 1 |
| Errors | 0 |
| Duration | 40.3s |
| Generated | 2026-09-27T16:44:37+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `bf7d5842201d`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
