## Verdict

**No extracted claim was dropped, contradicted, invented, or carried only in part.** 6 source claim(s) checked against the merge, 4 merge claim(s) checked against the sources. This covers the claims that were extracted, not the documents: titles, headings and formatting are not claims and were not checked.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 4 |
| Claims extracted from `source_a.md` | 3 |
| Claims extracted from `source_b.md` | 3 |
| Forward — source claims accounted for in the merge | **6/6** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **3/3** |
| Forward — `source_b.md` claims accounted for | **3/3** |
| Reverse — merge claims found in a source | **4/4** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **10/10** |
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

### `source_a.md` -- 3 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 3 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The Vandrell Relay listens on port 8443. | 3 | carried | 'The relay listens on port 8443.' in `merged.md` -- The merged document, titled for the Vandrell Relay, states the relay listens on port 8443. |
| 2 | The Vandrell Relay health check path is /healthz. | 4 | carried | 'The health check path is /healthz.' in `merged.md` -- The Vandrell Relay document states the health check path is /healthz. |
| 3 | The Vandrell Relay read timeout is 30 seconds. | 5 | carried | 'The read timeout is 30 seconds.' in `merged.md` -- The Vandrell Relay document states the read timeout is 30 seconds. |

### `source_b.md` -- 3 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 3 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The Vandrell Relay listens on port 8443. | 3 | carried | 'The relay listens on port 8443.' in `merged.md` -- The merged document, titled for the Vandrell Relay, states the relay listens on port 8443. |
| 2 | The Vandrell Relay health check path is /healthz. | 4 | carried | 'The health check path is /healthz.' in `merged.md` -- The Vandrell Relay document states the health check path is /healthz. |
| 3 | The Vandrell Relay minimum TLS version is 1.2. | 5 | carried | 'The minimum TLS version is 1.2.' in `merged.md` -- The Vandrell Relay document states the minimum TLS version is 1.2. |

### `merged.md` -- 4 claim(s): 0 invented, 0 contradicted, 0 supported in part, 4 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | The Vandrell Relay listens on port 8443. | supported | `source_a.md` | 'The relay listens on port 8443.' in `source_a.md` -- Both sources state the relay listens on port 8443, and the heading identifies it as the Vandrell Relay. |
| 2 | The Vandrell Relay health check path is /healthz. | supported | `source_a.md` | 'The health check path is /healthz.' in `source_a.md` -- Both sources state the health check path is /healthz for the Vandrell Relay. |
| 3 | The Vandrell Relay read timeout is 30 seconds. | supported | `source_a.md` | 'The read timeout is 30 seconds.' in `source_a.md` -- The operator guide states the read timeout is 30 seconds. |
| 4 | The Vandrell Relay minimum TLS version is 1.2. | supported | `source_b.md` | 'The minimum TLS version is 1.2.' in `source_b.md` -- The deployment notes state the minimum TLS version is 1.2. |

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
| Duration | 28.7s |
| Generated | 2026-09-27T20:18:53+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup opus-5.5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
