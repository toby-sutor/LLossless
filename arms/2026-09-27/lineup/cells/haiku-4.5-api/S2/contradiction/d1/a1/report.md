## Verdict

**2 finding(s).** In the claims: 2 contradicted.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 8 |
| Claims extracted from `source_a.md` | 6 |
| Claims extracted from `source_b.md` | 5 |
| Forward — source claims accounted for in the merge | **10/11** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **5/6** |
| Forward — `source_b.md` claims accounted for | **5/5** |
| Reverse — merge claims found in a source | **7/8** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **19/19** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **A-002** -- the two documents disagree
  - `source_a.md:8` says: The default connect timeout is 30 seconds.
  - `merged.md` says: 'The default connect timeout is 60 seconds.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text states the default connect timeout is 60 seconds, not 30 seconds as claimed.
- **M-002** -- the two documents disagree
  - `merged.md:8` says: The default connect timeout is 60 seconds.
  - `source_a.md` says: 'The default connect timeout is 30 seconds.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: source_a.md states the default connect timeout is 30 seconds, but source_b.md states it is 60 seconds. The claim reports 60 seconds, contradicting source_a.md.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 6 claim(s): 0 dropped, 1 contradicted, 0 carried in part, 5 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 2 | The default connect timeout is 30 seconds. | 8 | contradicted | 'The default connect timeout is 60 seconds.' in `merged.md` -- The reference text states the default connect timeout is 60 seconds, not 30 seconds as claimed. |
| 1 | Vandrell Relay listens on port 8443 by default. | 7 | carried | 'The relay listens on port 8443 by default.' in `merged.md` -- The reference text directly states that Vandrell Relay listens on port 8443 by default. |
| 3 | The default read timeout is 120 seconds. | 9 | carried | 'The default read timeout is 120 seconds.' in `merged.md` -- The reference text directly states the default read timeout is 120 seconds. |
| 4 | Vandrell Relay accepts at most 512 concurrent connections. | 13 | carried | 'The relay accepts at most 512 concurrent connections.' in `merged.md` -- The reference text directly states Vandrell Relay accepts at most 512 concurrent connections. |
| 5 | Each request is retried at most 3 times. | 14 | carried | 'Each request is retried at most 3 times.' in `merged.md` -- The reference text directly states each request is retried at most 3 times. |
| 6 | The minimum accepted TLS version is TLS 1.2. | 18 | carried | 'The minimum accepted TLS version is TLS 1.2.' in `merged.md` -- The reference text directly states the minimum accepted TLS version is TLS 1.2. |

### `source_b.md` -- 5 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 5 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Vandrell Relay listens on port 8443 by default. | 7 | carried | 'The relay listens on port 8443 by default.' in `merged.md` -- The reference text directly states that Vandrell Relay listens on port 8443 by default. |
| 2 | The default connect timeout is 60 seconds. | 8 | carried | 'The default connect timeout is 60 seconds.' in `merged.md` -- The reference text directly states the default connect timeout is 60 seconds. |
| 3 | The default read timeout is 120 seconds. | 9 | carried | 'The default read timeout is 120 seconds.' in `merged.md` -- The reference text directly states the default read timeout is 120 seconds. |
| 4 | Access logs are written in JSON Lines format. | 13 | carried | 'Access logs are written in JSON Lines format.' in `merged.md` -- The reference text directly states access logs are written in JSON Lines format. |
| 5 | The health check endpoint is /-/healthy. | 14 | carried | 'The health check endpoint is /-/healthy.' in `merged.md` -- The reference text directly states the health check endpoint is /-/healthy. |

### `merged.md` -- 8 claim(s): 0 invented, 1 contradicted, 0 supported in part, 7 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 2 | The default connect timeout is 60 seconds. | contradicted | `source_a.md` | 'The default connect timeout is 30 seconds.' in `source_a.md` -- source_a.md states the default connect timeout is 30 seconds, but source_b.md states it is 60 seconds. The claim reports 60 seconds, contradicting source_a.md. |
| 1 | The relay listens on port 8443 by default. | supported | `source_a.md` | 'The relay listens on port 8443 by default.' in `source_a.md` -- Both source_a.md and source_b.md state this claim identically. |
| 3 | The default read timeout is 120 seconds. | supported | `source_a.md` | 'The default read timeout is 120 seconds.' in `source_a.md` -- Both source_a.md and source_b.md state this claim identically. |
| 4 | The relay accepts at most 512 concurrent connections. | supported | `source_a.md` | 'The relay accepts at most 512 concurrent connections.' in `source_a.md` -- source_a.md states this claim. It does not appear in source_b.md, but support from one source is sufficient. |
| 5 | Each request is retried at most 3 times. | supported | `source_a.md` | 'Each request is retried at most 3 times.' in `source_a.md` -- source_a.md states this claim. It does not appear in source_b.md, but support from one source is sufficient. |
| 6 | The minimum accepted TLS version is TLS 1.2. | supported | `source_a.md` | 'The minimum accepted TLS version is TLS 1.2.' in `source_a.md` -- source_a.md states this claim. It does not appear in source_b.md, but support from one source is sufficient. |
| 7 | Access logs are written in JSON Lines format. | supported | `source_b.md` | 'Access logs are written in JSON Lines format.' in `source_b.md` -- source_b.md states this claim. It does not appear in source_a.md, but support from one source is sufficient. |
| 8 | The health check endpoint is /-/healthy. | supported | `source_b.md` | 'The health check endpoint is /-/healthy.' in `source_b.md` -- source_b.md states this claim. It does not appear in source_a.md, but support from one source is sufficient. |

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
| Tokens | 7,518 in, 2,661 out |
| Cost | ~$0.02 estimated (rates read 2026-08-31) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 20.8s |
| Generated | 2026-09-27T17:18:15+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
