## Verdict

**1 finding(s).** In the claims: 1 contradicted.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 4 |
| Claims extracted from `source_a.md` | 4 |
| Claims extracted from `source_b.md` | 4 |
| Forward — source claims accounted for in the merge | **7/8** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **3/4** |
| Forward — `source_b.md` claims accounted for | **4/4** |
| Reverse — merge claims found in a source | **4/4** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **12/12** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **A-001** -- the two documents disagree
  - `source_a.md:7` says: The relay handles approximately 500 concurrent connections.
  - `merged.md` says: 'The connection limit is 512 concurrent connections.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The claim states approximately 500 concurrent connections, but the reference specifies the connection limit is exactly 512.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 4 claim(s): 0 dropped, 1 contradicted, 0 carried in part, 3 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The relay handles approximately 500 concurrent connections. | 7 | contradicted | 'The connection limit is 512 concurrent connections.' in `merged.md` -- The claim states approximately 500 concurrent connections, but the reference specifies the connection limit is exactly 512. |
| 2 | Each request is retried at most 3 times. | 8 | carried | 'Each request is retried at most 3 times.' in `merged.md` -- The reference text states this claim verbatim. |
| 3 | The relay listens on port 8443 by default. | 12 | carried | 'The relay listens on port 8443 by default.' in `merged.md` -- The reference text states this claim verbatim. |
| 4 | The default connect timeout is 30 seconds. | 13 | carried | 'The default connect timeout is 30 seconds.' in `merged.md` -- The reference text states this claim verbatim. |

### `source_b.md` -- 4 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 4 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The connection limit is 512 concurrent connections. | 7 | carried | 'The connection limit is 512 concurrent connections.' in `merged.md` -- The reference text states this claim verbatim. |
| 2 | Each request is retried at most 3 times. | 8 | carried | 'Each request is retried at most 3 times.' in `merged.md` -- The reference text states this claim verbatim. |
| 3 | The relay listens on port 8443 by default. | 12 | carried | 'The relay listens on port 8443 by default.' in `merged.md` -- The reference text states this claim verbatim. |
| 4 | The default connect timeout is 30 seconds. | 13 | carried | 'The default connect timeout is 30 seconds.' in `merged.md` -- The reference text states this claim verbatim. |

### `merged.md` -- 4 claim(s): 0 invented, 0 contradicted, 0 supported in part, 4 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | The connection limit is 512 concurrent connections. | supported | `source_b.md` | 'The connection limit is 512 concurrent connections.' in `source_b.md` -- source_b.md directly states this claim with identical wording. |
| 2 | Each request is retried at most 3 times. | supported | `source_a.md` | 'Each request is retried at most 3 times.' in `source_a.md` -- This statement appears identically in both source documents. |
| 3 | The relay listens on port 8443 by default. | supported | `source_a.md` | 'The relay listens on port 8443 by default.' in `source_a.md` -- This statement appears identically in both source documents. |
| 4 | The default connect timeout is 30 seconds. | supported | `source_a.md` | 'The default connect timeout is 30 seconds.' in `source_a.md` -- This statement appears identically in both source documents. |

## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | 45fff742d0ed (command) -- lineup haiku-4.5-sub |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | none — this run made no merge |
| Model (decompose) | claude-haiku-4-5-20251001 -> claude-haiku-4-5-20251001 |
| Model (verify) | claude-haiku-4-5-20251001 -> claude-haiku-4-5-20251001 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile subscription, effort decompose one level (extended thinking on/off; default kept), verify one level (extended thinking on/off; default kept) |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 5 live, 0 cached, 0 replayed |
| Tokens | unknown (5 call(s) reported no usage) |
| Cost | unmeasured (5 call(s) reported no tokens, so no figure can be derived) |
| Schema repairs | 0 |
| Isolation | decompose, verify: safe mode, no tools |
| Errors | 0 |
| Duration | 102.6s |
| Generated | 2026-09-27T20:58:49+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup haiku-4.5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
