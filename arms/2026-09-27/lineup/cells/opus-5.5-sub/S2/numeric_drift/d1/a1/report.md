## Verdict

**1 finding(s).** In the claims: 1 contradicted.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 5 |
| Claims extracted from `source_a.md` | 5 |
| Claims extracted from `source_b.md` | 5 |
| Forward — source claims accounted for in the merge | **9/10** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **4/5** |
| Forward — `source_b.md` claims accounted for | **5/5** |
| Reverse — merge claims found in a source | **5/5** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **15/15** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **A-002** -- the two documents disagree
  - `source_a.md:7` says: The Vandrell Relay handles approximately 500 concurrent connections.
  - `merged.md` says: 'The connection limit is 512 concurrent connections.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives an exact limit of 512 concurrent connections, a different value from the approximate 500 the claim states for the same attribute.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 5 claim(s): 0 dropped, 1 contradicted, 0 carried in part, 4 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 2 | The Vandrell Relay handles approximately 500 concurrent connections. | 7 | contradicted | 'The connection limit is 512 concurrent connections.' in `merged.md` -- The reference gives an exact limit of 512 concurrent connections, a different value from the approximate 500 the claim states for the same attribute. |
| 1 | Vandrell Relay is a fictional HTTP relay. | 3 | carried | 'Vandrell Relay is a fictional HTTP relay.' in `merged.md` -- The reference text states this verbatim. |
| 3 | Each Vandrell Relay request is retried at most 3 times. | 8 | carried | 'Each request is retried at most 3 times.' in `merged.md` -- The reference text states the retry limit of 3 for each request. |
| 4 | The Vandrell Relay listens on port 8443 by default. | 12 | carried | 'The relay listens on port 8443 by default.' in `merged.md` -- The reference text states the default port is 8443. |
| 5 | The Vandrell Relay default connect timeout is 30 seconds. | 13 | carried | 'The default connect timeout is 30 seconds.' in `merged.md` -- The reference text states the default connect timeout is 30 seconds. |

### `source_b.md` -- 5 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 5 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Vandrell Relay is a fictional HTTP relay. | 3 | carried | 'Vandrell Relay is a fictional HTTP relay.' in `merged.md` -- The reference text states this verbatim. |
| 2 | The Vandrell Relay connection limit is 512 concurrent connections. | 7 | carried | 'The connection limit is 512 concurrent connections.' in `merged.md` -- The reference text states the connection limit is 512 concurrent connections. |
| 3 | Each Vandrell Relay request is retried at most 3 times. | 8 | carried | 'Each request is retried at most 3 times.' in `merged.md` -- The reference text states the retry limit of 3 for each request. |
| 4 | The Vandrell Relay listens on port 8443 by default. | 12 | carried | 'The relay listens on port 8443 by default.' in `merged.md` -- The reference text states the default port is 8443. |
| 5 | The Vandrell Relay default connect timeout is 30 seconds. | 13 | carried | 'The default connect timeout is 30 seconds.' in `merged.md` -- The reference text states the default connect timeout is 30 seconds. |

### `merged.md` -- 5 claim(s): 0 invented, 0 contradicted, 0 supported in part, 5 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Vandrell Relay is a fictional HTTP relay. | supported | `source_a.md` | 'Vandrell Relay is a fictional HTTP relay.' in `source_a.md` -- Both sources state this sentence verbatim. |
| 2 | The Vandrell Relay connection limit is 512 concurrent connections. | supported | `source_b.md` | 'The connection limit is 512 concurrent connections.' in `source_b.md` -- source_b.md states the 512 limit directly; source_a.md's 'approximately 500' is an approximate handling figure, and support from one source is sufficient. |
| 3 | Each Vandrell Relay request is retried at most 3 times. | supported | `source_a.md` | 'Each request is retried at most 3 times.' in `source_a.md` -- Both sources state that each request is retried at most 3 times. |
| 4 | The Vandrell Relay listens on port 8443 by default. | supported | `source_a.md` | 'The relay listens on port 8443 by default.' in `source_a.md` -- Both sources state the default listening port is 8443. |
| 5 | The Vandrell Relay default connect timeout is 30 seconds. | supported | `source_a.md` | 'The default connect timeout is 30 seconds.' in `source_a.md` -- Both sources state the default connect timeout is 30 seconds. |

## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | 31c2462e2828 (command) -- lineup opus-5.5-sub |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | none — this run made no merge |
| Model (decompose) | claude-opus-5-5 -> claude-opus-5-5 |
| Model (verify) | claude-opus-5-5 -> claude-opus-5-5 |
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
| Duration | 40.9s |
| Generated | 2026-09-27T20:56:33+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup opus-5.5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
