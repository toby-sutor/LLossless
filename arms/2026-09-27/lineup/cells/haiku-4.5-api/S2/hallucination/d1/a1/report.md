## Verdict

**1 finding(s).** In the claims: 1 hallucinated.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 8 |
| Claims extracted from `source_a.md` | 4 |
| Claims extracted from `source_b.md` | 4 |
| Forward — source claims accounted for in the merge | **8/8** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **4/4** |
| Forward — `source_b.md` claims accounted for | **4/4** |
| Reverse — merge claims found in a source | **7/8** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **15/15** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Invented — in the merge, in neither source

- **M-004** (`merged.md:10`) — Upstream traffic can be forwarded through a SOCKS5 proxy.
  - judged against: `source_a.md` and `source_b.md`
  - rationale: No source document mentions SOCKS5 proxy forwarding or upstream traffic forwarding.

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
| 1 | The relay listens on port 8443 by default. | 7 | carried | 'The relay listens on port 8443 by default.' in `merged.md` -- The reference text states exactly this claim in the Networking section. |
| 2 | The default connect timeout is 30 seconds. | 8 | carried | 'The default connect timeout is 30 seconds.' in `merged.md` -- The reference text states exactly this claim in the Networking section. |
| 3 | The minimum accepted TLS version is TLS 1.2. | 12 | carried | 'The minimum accepted TLS version is TLS 1.2.' in `merged.md` -- The reference text states exactly this claim in the Security section. |
| 4 | Client certificate verification is disabled by default. | 13 | carried | 'Client certificate verification is disabled by default.' in `merged.md` -- The reference text states exactly this claim in the Security section. |

### `source_b.md` -- 4 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 4 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The relay listens on port 8443 by default. | 7 | carried | 'The relay listens on port 8443 by default.' in `merged.md` -- The reference text states exactly this claim in the Networking section. |
| 2 | The relay accepts at most 512 concurrent connections. | 8 | carried | 'The relay accepts at most 512 concurrent connections.' in `merged.md` -- The reference text states exactly this claim in the Networking section. |
| 3 | Access logs are written in JSON Lines format. | 12 | carried | 'Access logs are written in JSON Lines format.' in `merged.md` -- The reference text states exactly this claim in the Operations section. |
| 4 | The health check endpoint is /-/healthy. | 13 | carried | 'The health check endpoint is /-/healthy.' in `merged.md` -- The reference text states exactly this claim in the Operations section. |

### `merged.md` -- 8 claim(s): 1 invented, 0 contradicted, 0 supported in part, 7 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 4 | Upstream traffic can be forwarded through a SOCKS5 proxy. | invented | -- | No source document mentions SOCKS5 proxy forwarding or upstream traffic forwarding. |
| 1 | The relay listens on port 8443 by default. | supported | `source_a.md` | 'The relay listens on port 8443 by default.' in `source_a.md` -- This claim is stated identically in both source_a.md and source_b.md under their Networking sections. |
| 2 | The default connect timeout is 30 seconds. | supported | `source_a.md` | 'The default connect timeout is 30 seconds.' in `source_a.md` -- This claim is stated verbatim in source_a.md under the Networking section. |
| 3 | The relay accepts at most 512 concurrent connections. | supported | `source_b.md` | 'The relay accepts at most 512 concurrent connections.' in `source_b.md` -- This claim is stated verbatim in source_b.md under the Networking section. |
| 5 | The minimum accepted TLS version is TLS 1.2. | supported | `source_a.md` | 'The minimum accepted TLS version is TLS 1.2.' in `source_a.md` -- This claim is stated verbatim in source_a.md under the Security section. |
| 6 | Client certificate verification is disabled by default. | supported | `source_a.md` | 'Client certificate verification is disabled by default.' in `source_a.md` -- This claim is stated verbatim in source_a.md under the Security section. |
| 7 | Access logs are written in JSON Lines format. | supported | `source_b.md` | 'Access logs are written in JSON Lines format.' in `source_b.md` -- This claim is stated verbatim in source_b.md under the Operations section. |
| 8 | The health check endpoint is /-/healthy. | supported | `source_b.md` | 'The health check endpoint is /-/healthy.' in `source_b.md` -- This claim is stated verbatim in source_b.md under the Operations section. |

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
| Tokens | 7,341 in, 2,134 out |
| Cost | ~$0.02 estimated (rates read 2026-08-31) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 16.7s |
| Generated | 2026-09-27T17:32:37+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
