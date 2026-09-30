## Verdict

**No extracted claim was dropped, contradicted, invented, or carried only in part.** 25 source claim(s) checked against the merge, 12 merge claim(s) checked against the sources. This covers the claims that were extracted, not the documents: titles, headings and formatting are not claims and were not checked.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 12 |
| Claims extracted from `source_a.md` | 12 |
| Claims extracted from `source_b.md` | 13 |
| Forward — source claims accounted for in the merge | **25/25** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **12/12** |
| Forward — `source_b.md` claims accounted for | **13/13** |
| Reverse — merge claims found in a source | **12/12** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **37/37** |
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

### `source_a.md` -- 12 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 12 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The relay listens on port 8443 by default. | 7 | carried | 'The relay listens on port 8443 by default.' in `merged.md` -- Stated verbatim. |
| 2 | The default connect timeout is 30 seconds. | 8 | carried | 'The default connect timeout is 30 seconds.' in `merged.md` -- Stated verbatim. |
| 3 | The default read timeout is 120 seconds. | 9 | carried | 'The default read timeout is 120 seconds.' in `merged.md` -- Stated verbatim. |
| 4 | The health check endpoint is /-/healthy. | 10 | carried | 'The health check endpoint is /-/healthy.' in `merged.md` -- Stated verbatim. |
| 5 | The relay accepts at most 512 concurrent connections. | 14 | carried | 'The relay accepts at most 512 concurrent connections.' in `merged.md` -- Stated verbatim. |
| 6 | Each request is retried at most 3 times. | 15 | carried | 'Each request is retried at most 3 times.' in `merged.md` -- Stated verbatim. |
| 7 | Retry backoff starts at 250 milliseconds. | 16 | carried | 'Retry backoff starts at 250 milliseconds and doubles on every attempt.' in `merged.md` -- Starting value is stated. |
| 8 | Retry backoff doubles on every attempt. | 16 | carried | 'Retry backoff starts at 250 milliseconds and doubles on every attempt.' in `merged.md` -- Doubling behavior is stated. |
| 9 | The minimum accepted TLS version is TLS 1.2. | 20 | carried | 'The minimum accepted TLS version is TLS 1.2.' in `merged.md` -- Stated verbatim. |
| 10 | Client certificate verification is disabled by default. | 21 | carried | 'Client certificate verification is disabled by default.' in `merged.md` -- Stated verbatim. |
| 11 | Access logs are written in JSON Lines format. | 25 | carried | 'Access logs are written in JSON Lines format.' in `merged.md` -- Stated verbatim. |
| 12 | Log files are rotated when they reach 100 megabytes. | 26 | carried | 'Log files are rotated when they reach 100 megabytes.' in `merged.md` -- Stated verbatim. |

### `source_b.md` -- 13 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 13 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Vandrell Relay is a fictional HTTP relay. | 3 | carried | 'Vandrell Relay is a fictional HTTP relay.' in `merged.md` -- Stated verbatim. |
| 2 | Access logs are written in JSON Lines format. | 7 | carried | 'Access logs are written in JSON Lines format.' in `merged.md` -- Stated verbatim. |
| 3 | Log files are rotated when they reach 100 megabytes. | 8 | carried | 'Log files are rotated when they reach 100 megabytes.' in `merged.md` -- Stated verbatim. |
| 4 | The minimum accepted TLS version is TLS 1.2. | 12 | carried | 'The minimum accepted TLS version is TLS 1.2.' in `merged.md` -- Stated verbatim. |
| 5 | Client certificate verification is disabled by default. | 13 | carried | 'Client certificate verification is disabled by default.' in `merged.md` -- Stated verbatim. |
| 6 | The relay accepts at most 512 concurrent connections. | 17 | carried | 'The relay accepts at most 512 concurrent connections.' in `merged.md` -- Stated verbatim. |
| 7 | Each request is retried at most 3 times. | 18 | carried | 'Each request is retried at most 3 times.' in `merged.md` -- Stated verbatim. |
| 8 | Retry backoff starts at 250 milliseconds. | 19 | carried | 'Retry backoff starts at 250 milliseconds and doubles on every attempt.' in `merged.md` -- Starting value is stated. |
| 9 | Retry backoff doubles on every attempt. | 19 | carried | 'Retry backoff starts at 250 milliseconds and doubles on every attempt.' in `merged.md` -- Doubling behavior is stated. |
| 10 | The relay listens on port 8443 by default. | 23 | carried | 'The relay listens on port 8443 by default.' in `merged.md` -- Stated verbatim. |
| 11 | The default connect timeout is 30 seconds. | 24 | carried | 'The default connect timeout is 30 seconds.' in `merged.md` -- Stated verbatim. |
| 12 | The default read timeout is 120 seconds. | 25 | carried | 'The default read timeout is 120 seconds.' in `merged.md` -- Stated verbatim. |
| 13 | The health check endpoint is /-/healthy. | 26 | carried | 'The health check endpoint is /-/healthy.' in `merged.md` -- Stated verbatim. |

### `merged.md` -- 12 claim(s): 0 invented, 0 contradicted, 0 supported in part, 12 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | The relay accepts at most 512 concurrent connections. | supported | `source_a.md` | 'The relay accepts at most 512 concurrent connections.' in `source_a.md` -- Directly stated in both sources. |
| 2 | Each request is retried at most 3 times. | supported | `source_a.md` | 'Each request is retried at most 3 times.' in `source_a.md` -- Directly stated in both sources. |
| 3 | Retry backoff starts at 250 milliseconds. | supported | `source_a.md` | 'Retry backoff starts at 250 milliseconds and doubles on every attempt.' in `source_a.md` -- Directly stated. |
| 4 | Retry backoff doubles on every attempt. | supported | `source_a.md` | 'Retry backoff starts at 250 milliseconds and doubles on every attempt.' in `source_a.md` -- Directly stated. |
| 5 | Access logs are written in JSON Lines format. | supported | `source_a.md` | 'Access logs are written in JSON Lines format.' in `source_a.md` -- Directly stated in both sources. |
| 6 | Log files are rotated when they reach 100 megabytes. | supported | `source_a.md` | 'Log files are rotated when they reach 100 megabytes.' in `source_a.md` -- Directly stated in both sources. |
| 7 | The relay listens on port 8443 by default. | supported | `source_a.md` | 'The relay listens on port 8443 by default.' in `source_a.md` -- Directly stated in both sources. |
| 8 | The default connect timeout is 30 seconds. | supported | `source_a.md` | 'The default connect timeout is 30 seconds.' in `source_a.md` -- Directly stated in both sources. |
| 9 | The default read timeout is 120 seconds. | supported | `source_a.md` | 'The default read timeout is 120 seconds.' in `source_a.md` -- Directly stated in both sources. |
| 10 | The health check endpoint is /-/healthy. | supported | `source_a.md` | 'The health check endpoint is /-/healthy.' in `source_a.md` -- Directly stated in both sources. |
| 11 | The minimum accepted TLS version is TLS 1.2. | supported | `source_a.md` | 'The minimum accepted TLS version is TLS 1.2.' in `source_a.md` -- Directly stated in both sources. |
| 12 | Client certificate verification is disabled by default. | supported | `source_a.md` | 'Client certificate verification is disabled by default.' in `source_a.md` -- Directly stated in both sources. |

## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | d320da0eb7ed (command) -- lineup sonnet-5-sub |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | none — this run made no merge |
| Model (decompose) | claude-sonnet-5 -> claude-sonnet-5 |
| Model (verify) | claude-sonnet-5 -> claude-sonnet-5 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile subscription, effort decompose=medium, merge=medium, verify=medium |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 5 live, 0 cached, 0 replayed |
| Tokens | unknown (5 call(s) reported no usage) |
| Cost | unmeasured (5 call(s) reported no tokens, so no figure can be derived) |
| Schema repairs | 0 |
| Isolation | decompose, verify: safe mode, no tools |
| Errors | 0 |
| Duration | 50.2s |
| Generated | 2026-09-27T20:59:40+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup sonnet-5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
