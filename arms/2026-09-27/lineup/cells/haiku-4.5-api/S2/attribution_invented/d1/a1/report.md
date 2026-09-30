## Verdict

**2 finding(s).** In the claims: 1 contradicted. In the attributions: 1 credited to a source that does not state it.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 5 |
| Claims extracted from `source_a.md` | 3 |
| Claims extracted from `source_b.md` | 3 |
| Forward — source claims accounted for in the merge | **6/6** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **3/3** |
| Forward — `source_b.md` claims accounted for | **3/3** |
| Reverse — merge claims found in a source | **4/5** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **11/11** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **M-004** -- the two documents disagree
  - `merged.md:6` says: According to the Operator Guide, the minimum TLS version is 1.2.
  - `source_b.md` says: 'The minimum TLS version is 1.2.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The claim attributes this fact to the Operator Guide (source_a.md), but source_b.md (Deployment Notes) states it, not source_a.md.

## Attributions

Each sentence below credits a named source with a statement that source does not contain, while another source contains it word for word. The name was matched to one source by its title or its filename, and no model was asked anything. A sentence the merge copied from a source as written is never listed, and neither is one whose statement no source contains or whose name fits two sources.

- `m5` (`source_a.md`) - the merge credits 'the minimum TLS version is 1.2' to the Operator Guide (source_a.md), which does not state it; source_b.md does

  ```text
  In the source: The minimum TLS version is 1.2.
  In the merge:  According to the Operator Guide, the minimum TLS version is 1.2.
  ```

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 3 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 3 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The relay listens on port 8443. | 3 | carried | 'The relay listens on port 8443.' in `merged.md` -- The reference text directly states that the relay listens on port 8443. |
| 2 | The read timeout is 30 seconds. | 4 | carried | 'The read timeout is 30 seconds.' in `merged.md` -- The reference text directly states that the read timeout is 30 seconds. |
| 3 | The health check path is /healthz. | 5 | carried | 'The health check path is /healthz.' in `merged.md` -- The reference text directly states that the health check path is /healthz. |

### `source_b.md` -- 3 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 3 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The relay listens on port 8443. | 3 | carried | 'The relay listens on port 8443.' in `merged.md` -- The reference text directly states that the relay listens on port 8443. |
| 2 | The minimum TLS version is 1.2. | 4 | carried | 'According to the Operator Guide, the minimum TLS version is 1.2.' in `merged.md` -- The reference text states that the minimum TLS version is 1.2; attribution to a source does not prevent the claim from being supported. |
| 3 | The maximum concurrent connections is 512. | 5 | carried | 'The maximum concurrent connections is 512.' in `merged.md` -- The reference text directly states that the maximum concurrent connections is 512. |

### `merged.md` -- 5 claim(s): 0 invented, 1 contradicted, 0 supported in part, 4 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 4 | According to the Operator Guide, the minimum TLS version is 1.2. | contradicted | `source_b.md` | 'The minimum TLS version is 1.2.' in `source_b.md` -- The claim attributes this fact to the Operator Guide (source_a.md), but source_b.md (Deployment Notes) states it, not source_a.md. |
| 1 | The relay listens on port 8443. | supported | `source_a.md` | 'The relay listens on port 8443.' in `source_a.md` -- This claim is stated identically in both source documents; source_a.md provides direct support. |
| 2 | The read timeout is 30 seconds. | supported | `source_a.md` | 'The read timeout is 30 seconds.' in `source_a.md` -- source_a.md explicitly states this claim. |
| 3 | The health check path is /healthz. | supported | `source_a.md` | 'The health check path is /healthz.' in `source_a.md` -- source_a.md explicitly states this claim. |
| 5 | The maximum concurrent connections is 512. | supported | `source_b.md` | 'The maximum concurrent connections is 512.' in `source_b.md` -- source_b.md explicitly states this claim. |

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
| Tokens | 6,806 in, 1,497 out |
| Cost | ~$0.01 estimated (rates read 2026-08-31) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 12.5s |
| Generated | 2026-09-27T17:14:35+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
