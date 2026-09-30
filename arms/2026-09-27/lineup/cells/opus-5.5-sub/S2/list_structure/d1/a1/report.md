## Verdict

**No extracted claim was dropped, contradicted, invented, or carried only in part.** 10 source claim(s) checked against the merge, 8 merge claim(s) checked against the sources. This covers the claims that were extracted, not the documents: titles, headings and formatting are not claims and were not checked.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 8 |
| Claims extracted from `source_a.md` | 5 |
| Claims extracted from `source_b.md` | 5 |
| Forward — source claims accounted for in the merge | **10/10** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **5/5** |
| Forward — `source_b.md` claims accounted for | **5/5** |
| Reverse — merge claims found in a source | **8/8** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **18/18** |
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

### `source_a.md` -- 5 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 5 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Vandrell Relay is a fictional HTTP relay. | 3 | carried | 'Vandrell Relay is a fictional HTTP relay.' in `merged.md` -- The reference text states this sentence verbatim. |
| 2 | The default listen port of Vandrell Relay is 8443. | 7 | carried | 'Listen port: 8443' in `merged.md` -- The defaults document lists the listen port as 8443. |
| 3 | The default connect timeout of Vandrell Relay is 30 seconds. | 8 | carried | 'Connect timeout: 30 seconds' in `merged.md` -- The defaults document lists the connect timeout as 30 seconds. |
| 4 | The default maximum concurrent connections of Vandrell Relay is 512. | 12 | carried | 'Maximum concurrent connections: 512' in `merged.md` -- The defaults document lists maximum concurrent connections as 512. |
| 5 | The default number of retry attempts of Vandrell Relay is 3. | 13 | carried | 'Retry attempts: 3' in `merged.md` -- The defaults document lists retry attempts as 3. |

### `source_b.md` -- 5 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 5 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Vandrell Relay is a fictional HTTP relay. | 3 | carried | 'Vandrell Relay is a fictional HTTP relay.' in `merged.md` -- The reference text states this sentence verbatim. |
| 2 | The Vandrell Relay default connect timeout is 30 seconds. | 7 | carried | 'Connect timeout: 30 seconds' in `merged.md` -- The defaults document lists the connect timeout as 30 seconds. |
| 3 | The Vandrell Relay default read timeout is 120 seconds. | 8 | carried | 'Read timeout: 120 seconds' in `merged.md` -- The defaults document lists the read timeout as 120 seconds. |
| 4 | The Vandrell Relay default access log format is JSON Lines. | 12 | carried | 'Access log format: JSON Lines' in `merged.md` -- The defaults document lists the access log format as JSON Lines. |
| 5 | The Vandrell Relay default health check path is /-/healthy. | 13 | carried | 'Health check path: /-/healthy' in `merged.md` -- The defaults document lists the health check path as /-/healthy. |

### `merged.md` -- 8 claim(s): 0 invented, 0 contradicted, 0 supported in part, 8 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Vandrell Relay is a fictional HTTP relay. | supported | `source_a.md` | 'Vandrell Relay is a fictional HTTP relay.' in `source_a.md` -- Source A states this verbatim. |
| 2 | The default listen port of Vandrell Relay is 8443. | supported | `source_a.md` | '- Listen port: 8443' in `source_a.md` -- Source A's defaults list the listen port as 8443. |
| 3 | The default connect timeout of Vandrell Relay is 30 seconds. | supported | `source_a.md` | '- Connect timeout: 30 seconds' in `source_a.md` -- Source A's defaults list the connect timeout as 30 seconds, and source B agrees. |
| 4 | The default read timeout of Vandrell Relay is 120 seconds. | supported | `source_b.md` | '- Read timeout: 120 seconds' in `source_b.md` -- Source B's defaults list the read timeout as 120 seconds. |
| 5 | The default maximum concurrent connections of Vandrell Relay is 512. | supported | `source_a.md` | '- Maximum concurrent connections: 512' in `source_a.md` -- Source A's defaults list maximum concurrent connections as 512. |
| 6 | The default number of retry attempts of Vandrell Relay is 3. | supported | `source_a.md` | '- Retry attempts: 3' in `source_a.md` -- Source A's defaults list retry attempts as 3. |
| 7 | The default access log format of Vandrell Relay is JSON Lines. | supported | `source_b.md` | '- Access log format: JSON Lines' in `source_b.md` -- Source B's defaults list the access log format as JSON Lines. |
| 8 | The default health check path of Vandrell Relay is /-/healthy. | supported | `source_b.md` | '- Health check path: /-/healthy' in `source_b.md` -- Source B's defaults list the health check path as /-/healthy. |

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
| Duration | 31.5s |
| Generated | 2026-09-27T21:32:13+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup opus-5.5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
