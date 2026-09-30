## Verdict

**1 finding(s).** In the claims: 1 contradicted.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 9 |
| Claims extracted from `source_a.md` | 7 |
| Claims extracted from `source_b.md` | 6 |
| Forward — source claims accounted for in the merge | **12/13** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **6/7** |
| Forward — `source_b.md` claims accounted for | **6/6** |
| Reverse — merge claims found in a source | **9/9** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **22/22** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **A-003** -- the two documents disagree
  - `source_a.md:8` says: The default connect timeout is 30 seconds.
  - `merged.md` says: 'The default connect timeout is 60 seconds.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference states a 60-second timeout, not the claimed 30 seconds.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 7 claim(s): 0 dropped, 1 contradicted, 0 carried in part, 6 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 3 | The default connect timeout is 30 seconds. | 8 | contradicted | 'The default connect timeout is 60 seconds.' in `merged.md` -- The reference states a 60-second timeout, not the claimed 30 seconds. |
| 1 | Vandrell Relay is a fictional HTTP relay. | 3 | carried | 'Vandrell Relay is a fictional HTTP relay.' in `merged.md` -- The reference text states that Vandrell Relay is a fictional HTTP relay. |
| 2 | The relay listens on port 8443 by default. | 7 | carried | 'The relay listens on port 8443 by default.' in `merged.md` -- The reference text gives the same default listening port. |
| 4 | The default read timeout is 120 seconds. | 9 | carried | 'The default read timeout is 120 seconds.' in `merged.md` -- The reference text states the claimed default read timeout. |
| 5 | The relay accepts at most 512 concurrent connections. | 13 | carried | 'The relay accepts at most 512 concurrent connections.' in `merged.md` -- The reference text states the same maximum number of concurrent connections. |
| 6 | Each request is retried at most 3 times. | 14 | carried | 'Each request is retried at most 3 times.' in `merged.md` -- The reference text states the same retry limit for each request. |
| 7 | The minimum accepted TLS version is TLS 1.2. | 18 | carried | 'The minimum accepted TLS version is TLS 1.2.' in `merged.md` -- The reference text states the same minimum accepted TLS version. |

### `source_b.md` -- 6 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 6 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Vandrell Relay is a fictional HTTP relay. | 3 | carried | 'Vandrell Relay is a fictional HTTP relay.' in `merged.md` -- The reference text states that Vandrell Relay is a fictional HTTP relay. |
| 2 | The relay listens on port 8443 by default. | 7 | carried | 'The relay listens on port 8443 by default.' in `merged.md` -- The reference text gives the same default listening port. |
| 3 | The default connect timeout is 60 seconds. | 8 | carried | 'The default connect timeout is 60 seconds.' in `merged.md` -- The reference text states the claimed default connect timeout. |
| 4 | The default read timeout is 120 seconds. | 9 | carried | 'The default read timeout is 120 seconds.' in `merged.md` -- The reference text states the claimed default read timeout. |
| 5 | Access logs are written in JSON Lines format. | 13 | carried | 'Access logs are written in JSON Lines format.' in `merged.md` -- The reference text states the claimed access-log format. |
| 6 | The health check endpoint is /-/healthy. | 14 | carried | 'The health check endpoint is /-/healthy.' in `merged.md` -- The reference text states the claimed health check endpoint. |

### `merged.md` -- 9 claim(s): 0 invented, 0 contradicted, 0 supported in part, 9 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Vandrell Relay is a fictional HTTP relay. | supported | `source_a.md` | 'Vandrell Relay is a fictional HTTP relay.' in `source_a.md` -- The source states that Vandrell Relay is a fictional HTTP relay. |
| 2 | The relay listens on port 8443 by default. | supported | `source_a.md` | 'The relay listens on port 8443 by default.' in `source_a.md` -- The source states the default listening port is 8443. |
| 3 | The default connect timeout is 60 seconds. | supported | `source_b.md` | 'The default connect timeout is 60 seconds.' in `source_b.md` -- Source_b.md states a 60-second default connect timeout. |
| 4 | The default read timeout is 120 seconds. | supported | `source_a.md` | 'The default read timeout is 120 seconds.' in `source_a.md` -- The source states the default read timeout is 120 seconds. |
| 5 | The relay accepts at most 512 concurrent connections. | supported | `source_a.md` | 'The relay accepts at most 512 concurrent connections.' in `source_a.md` -- The source states the limit is 512 concurrent connections. |
| 6 | Each request is retried at most 3 times. | supported | `source_a.md` | 'Each request is retried at most 3 times.' in `source_a.md` -- The source states each request is retried at most 3 times. |
| 7 | The minimum accepted TLS version is TLS 1.2. | supported | `source_a.md` | 'The minimum accepted TLS version is TLS 1.2.' in `source_a.md` -- The source specifies TLS 1.2 as the minimum accepted version. |
| 8 | Access logs are written in JSON Lines format. | supported | `source_b.md` | 'Access logs are written in JSON Lines format.' in `source_b.md` -- The source states that access logs use JSON Lines format. |
| 9 | The health check endpoint is /-/healthy. | supported | `source_b.md` | 'The health check endpoint is /-/healthy.' in `source_b.md` -- The source identifies /-/healthy as the health check endpoint. |

## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | bf7d5842201d (hosted) |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | none — this run made no merge |
| Model (decompose) | gpt-6-luna |
| Model (verify) | gpt-6-luna |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed 0, thinking decompose, merge, verify, profile openai-reasoning |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 5 live, 0 cached, 0 replayed |
| Tokens | 6,748 in, 2,975 out, 0 cached, 1,102 reasoning |
| Cost | ~$0.00 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 23.6s |
| Generated | 2026-09-27T16:33:30+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `bf7d5842201d`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
