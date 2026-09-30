## Verdict

**No extracted claim was dropped, contradicted, invented, or carried only in part.** 5 source claim(s) checked against the merge, 4 merge claim(s) checked against the sources. This covers the claims that were extracted, not the documents: titles, headings and formatting are not claims and were not checked.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 4 |
| Claims extracted from `source_a.md` | 2 |
| Claims extracted from `source_b.md` | 3 |
| Forward — source claims accounted for in the merge | **5/5** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **2/2** |
| Forward — `source_b.md` claims accounted for | **3/3** |
| Reverse — merge claims found in a source | **4/4** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **9/9** |
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

### `source_a.md` -- 2 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 2 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The relay listens on port 8443. | 3 | carried | 'The relay listens on port 8443.' in `merged.md` -- The reference text states that the relay listens on port 8443. |
| 2 | The read timeout is 30 seconds. | 4 | carried | 'The read timeout is 30 seconds.' in `merged.md` -- The reference text states that the read timeout is 30 seconds. |

### `source_b.md` -- 3 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 3 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The relay listens on port 8443. | 3 | carried | 'The relay listens on port 8443.' in `merged.md` -- The reference text states that the relay listens on port 8443. |
| 2 | The health check path is /healthz. | 4 | carried | 'The health check path is /healthz.' in `merged.md` -- The reference text states that the health check path is /healthz. |
| 3 | The minimum TLS version is 1.2. | 5 | carried | 'The minimum TLS version is 1.2.' in `merged.md` -- The reference text states that the minimum TLS version is 1.2. |

### `merged.md` -- 4 claim(s): 0 invented, 0 contradicted, 0 supported in part, 4 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | The relay listens on port 8443. | supported | `source_a.md` | 'The relay listens on port 8443.' in `source_a.md` -- The source states that the relay listens on port 8443. |
| 2 | The read timeout is 30 seconds. | supported | `source_a.md` | 'The read timeout is 30 seconds.' in `source_a.md` -- The source states that the read timeout is 30 seconds. |
| 3 | The health check path is /healthz. | supported | `source_b.md` | 'The health check path is /healthz.' in `source_b.md` -- The source states that the health check path is /healthz. |
| 4 | The minimum TLS version is 1.2. | supported | `source_b.md` | 'The minimum TLS version is 1.2.' in `source_b.md` -- The source states that the minimum TLS version is 1.2. |

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
| Tokens | 6,269 in, 1,156 out, 0 cached, 407 reasoning |
| Cost | ~$0.00 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 13.2s |
| Generated | 2026-09-27T16:49:45+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `bf7d5842201d`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
