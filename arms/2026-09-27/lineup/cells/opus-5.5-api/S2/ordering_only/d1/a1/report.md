## Verdict

**No extracted claim was dropped, contradicted, invented, or carried only in part.** 26 source claim(s) checked against the merge, 13 merge claim(s) checked against the sources. This covers the claims that were extracted, not the documents: titles, headings and formatting are not claims and were not checked.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 13 |
| Claims extracted from `source_a.md` | 13 |
| Claims extracted from `source_b.md` | 13 |
| Forward — source claims accounted for in the merge | **26/26** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **13/13** |
| Forward — `source_b.md` claims accounted for | **13/13** |
| Reverse — merge claims found in a source | **13/13** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **39/39** |
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

### `source_a.md` -- 13 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 13 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Vandrell Relay is a fictional HTTP relay. | 3 | carried | 'Vandrell Relay is a fictional HTTP relay.' in `merged.md` -- The reference text states this verbatim. |
| 2 | The Vandrell Relay listens on port 8443 by default. | 7 | carried | 'The relay listens on port 8443 by default.' in `merged.md` -- The default port 8443 is stated directly. |
| 3 | The Vandrell Relay default connect timeout is 30 seconds. | 8 | carried | 'The default connect timeout is 30 seconds.' in `merged.md` -- The connect timeout of 30 seconds is stated directly. |
| 4 | The Vandrell Relay default read timeout is 120 seconds. | 9 | carried | 'The default read timeout is 120 seconds.' in `merged.md` -- The read timeout of 120 seconds is stated directly. |
| 5 | The Vandrell Relay health check endpoint is /-/healthy. | 10 | carried | 'The health check endpoint is /-/healthy.' in `merged.md` -- The health check endpoint is stated directly. |
| 6 | The Vandrell Relay accepts at most 512 concurrent connections. | 14 | carried | 'The relay accepts at most 512 concurrent connections.' in `merged.md` -- The connection limit of 512 is stated directly. |
| 7 | Each request to the Vandrell Relay is retried at most 3 times. | 15 | carried | 'Each request is retried at most 3 times.' in `merged.md` -- The retry limit of 3 is stated directly. |
| 8 | The Vandrell Relay retry backoff starts at 250 milliseconds. | 16 | carried | 'Retry backoff starts at 250 milliseconds' in `merged.md` -- The backoff start value of 250 milliseconds is stated directly. |
| 9 | The Vandrell Relay retry backoff doubles on every attempt. | 16 | carried | 'doubles on every attempt' in `merged.md` -- Backoff doubling on every attempt is stated directly. |
| 10 | The minimum TLS version accepted by the Vandrell Relay is TLS 1.2. | 20 | carried | 'The minimum accepted TLS version is TLS 1.2.' in `merged.md` -- The minimum TLS version of 1.2 is stated directly. |
| 11 | Client certificate verification in the Vandrell Relay is disabled by default. | 21 | carried | 'Client certificate verification is disabled by default.' in `merged.md` -- The client certificate verification default is stated directly. |
| 12 | Vandrell Relay access logs are written in JSON Lines format. | 25 | carried | 'Access logs are written in JSON Lines format.' in `merged.md` -- The JSON Lines log format is stated directly. |
| 13 | Vandrell Relay log files are rotated when they reach 100 megabytes. | 26 | carried | 'Log files are rotated when they reach 100 megabytes.' in `merged.md` -- The 100 megabyte rotation threshold is stated directly. |

### `source_b.md` -- 13 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 13 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Vandrell Relay is a fictional HTTP relay. | 3 | carried | 'Vandrell Relay is a fictional HTTP relay.' in `merged.md` -- The reference text states this verbatim. |
| 2 | Vandrell Relay access logs are written in JSON Lines format. | 7 | carried | 'Access logs are written in JSON Lines format.' in `merged.md` -- The JSON Lines log format is stated directly. |
| 3 | Vandrell Relay log files are rotated when they reach 100 megabytes. | 8 | carried | 'Log files are rotated when they reach 100 megabytes.' in `merged.md` -- The 100 megabyte rotation threshold is stated directly. |
| 4 | The minimum accepted TLS version for Vandrell Relay is TLS 1.2. | 12 | carried | 'The minimum accepted TLS version is TLS 1.2.' in `merged.md` -- The minimum TLS version of 1.2 is stated directly. |
| 5 | Vandrell Relay client certificate verification is disabled by default. | 13 | carried | 'Client certificate verification is disabled by default.' in `merged.md` -- The client certificate verification default is stated directly. |
| 6 | The Vandrell Relay accepts at most 512 concurrent connections. | 17 | carried | 'The relay accepts at most 512 concurrent connections.' in `merged.md` -- The connection limit of 512 is stated directly. |
| 7 | Each Vandrell Relay request is retried at most 3 times. | 18 | carried | 'Each request is retried at most 3 times.' in `merged.md` -- The retry limit of 3 is stated directly. |
| 8 | Vandrell Relay retry backoff starts at 250 milliseconds. | 19 | carried | 'Retry backoff starts at 250 milliseconds' in `merged.md` -- The backoff start value of 250 milliseconds is stated directly. |
| 9 | Vandrell Relay retry backoff doubles on every attempt. | 19 | carried | 'doubles on every attempt' in `merged.md` -- Backoff doubling on every attempt is stated directly. |
| 10 | The Vandrell Relay listens on port 8443 by default. | 23 | carried | 'The relay listens on port 8443 by default.' in `merged.md` -- The default port 8443 is stated directly. |
| 11 | The Vandrell Relay default connect timeout is 30 seconds. | 24 | carried | 'The default connect timeout is 30 seconds.' in `merged.md` -- The connect timeout of 30 seconds is stated directly. |
| 12 | The Vandrell Relay default read timeout is 120 seconds. | 25 | carried | 'The default read timeout is 120 seconds.' in `merged.md` -- The read timeout of 120 seconds is stated directly. |
| 13 | The Vandrell Relay health check endpoint is /-/healthy. | 26 | carried | 'The health check endpoint is /-/healthy.' in `merged.md` -- The reference text states the relay's health check endpoint is /-/healthy, matching the claim exactly. |

### `merged.md` -- 13 claim(s): 0 invented, 0 contradicted, 0 supported in part, 13 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Vandrell Relay is a fictional HTTP relay. | supported | `source_a.md` | 'Vandrell Relay is a fictional HTTP relay.' in `source_a.md` -- Source A states this verbatim. |
| 2 | The Vandrell Relay accepts at most 512 concurrent connections. | supported | `source_a.md` | 'The relay accepts at most 512 concurrent connections.' in `source_a.md` -- Source A states the 512 concurrent connection limit. |
| 3 | Each request to the Vandrell Relay is retried at most 3 times. | supported | `source_a.md` | 'Each request is retried at most 3 times.' in `source_a.md` -- Source A states the retry limit of 3. |
| 4 | Vandrell Relay retry backoff starts at 250 milliseconds. | supported | `source_a.md` | 'Retry backoff starts at 250 milliseconds and doubles on every attempt.' in `source_a.md` -- Source A states backoff starts at 250 milliseconds. |
| 5 | Vandrell Relay retry backoff doubles on every attempt. | supported | `source_a.md` | 'Retry backoff starts at 250 milliseconds and doubles on every attempt.' in `source_a.md` -- Source A states backoff doubles on every attempt. |
| 6 | Vandrell Relay access logs are written in JSON Lines format. | supported | `source_a.md` | 'Access logs are written in JSON Lines format.' in `source_a.md` -- Source A states access logs use JSON Lines. |
| 7 | Vandrell Relay log files are rotated when they reach 100 megabytes. | supported | `source_a.md` | 'Log files are rotated when they reach 100 megabytes.' in `source_a.md` -- Source A states rotation at 100 megabytes. |
| 8 | The Vandrell Relay listens on port 8443 by default. | supported | `source_a.md` | 'The relay listens on port 8443 by default.' in `source_a.md` -- Source A states the default port 8443. |
| 9 | The Vandrell Relay default connect timeout is 30 seconds. | supported | `source_a.md` | 'The default connect timeout is 30 seconds.' in `source_a.md` -- Source A states the 30 second connect timeout. |
| 10 | The Vandrell Relay default read timeout is 120 seconds. | supported | `source_a.md` | 'The default read timeout is 120 seconds.' in `source_a.md` -- Source A states the 120 second read timeout. |
| 11 | The Vandrell Relay health check endpoint is /-/healthy. | supported | `source_a.md` | 'The health check endpoint is /-/healthy.' in `source_a.md` -- Source A states the health check endpoint. |
| 12 | The minimum TLS version accepted by the Vandrell Relay is TLS 1.2. | supported | `source_a.md` | 'The minimum accepted TLS version is TLS 1.2.' in `source_a.md` -- Source A states the minimum TLS version is 1.2. |
| 13 | Vandrell Relay client certificate verification is disabled by default. | supported | `source_a.md` | 'Client certificate verification is disabled by default.' in `source_a.md` -- Source A states client certificate verification is disabled by default. |

## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | ec0c9ecb43e3 (hosted) |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | none — this run made no merge |
| Model (decompose) | claude-opus-5-5 |
| Model (verify) | claude-opus-5-5 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile anthropic |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 6 live, 0 cached, 0 replayed |
| Tokens | 14,217 in, 5,666 out |
| Cost | ~$0.17 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 48.8s |
| Generated | 2026-09-27T17:36:59+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
