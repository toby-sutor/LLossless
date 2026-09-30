## Verdict

**2 finding(s).** In the claims: 1 hallucinated. In the attributions: 1 credited to a source that does not state it.

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
| Evidence grounded | **10/10** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Invented — in the merge, in neither source

- **M-004** (`merged.md:6`) — According to the Operator Guide, the Vandrell Relay minimum TLS version is 1.2.
  - judged against: `source_a.md` and `source_b.md`
  - rationale: The claim attributes the TLS minimum to the Operator Guide (source_a.md), which does not mention TLS; only the Deployment Notes (source_b.md) state it, so the attribution was invented by the merge.

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
| 1 | The Vandrell Relay listens on port 8443. | 3 | carried | 'The relay listens on port 8443.' in `merged.md` -- The merged document, titled for the Vandrell Relay, states the relay listens on port 8443. |
| 2 | The Vandrell Relay read timeout is 30 seconds. | 4 | carried | 'The read timeout is 30 seconds.' in `merged.md` -- The merged Vandrell Relay configuration states the read timeout is 30 seconds. |
| 3 | The Vandrell Relay health check path is /healthz. | 5 | carried | 'The health check path is /healthz.' in `merged.md` -- The merged Vandrell Relay configuration states the health check path is /healthz. |

### `source_b.md` -- 3 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 3 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The Vandrell Relay listens on port 8443. | 3 | carried | 'The relay listens on port 8443.' in `merged.md` -- The merged document, titled for the Vandrell Relay, states the relay listens on port 8443. |
| 2 | The minimum TLS version for the Vandrell Relay is 1.2. | 4 | carried | 'According to the Operator Guide, the minimum TLS version is 1.2.' in `merged.md` -- The merged text attributes a minimum TLS version of 1.2 to the Operator Guide, and attribution still counts as stating the claim. |
| 3 | The maximum concurrent connections for the Vandrell Relay is 512. | 5 | carried | 'The maximum concurrent connections is 512.' in `merged.md` -- The merged Vandrell Relay configuration states the maximum concurrent connections is 512. |

### `merged.md` -- 5 claim(s): 1 invented, 0 contradicted, 0 supported in part, 4 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 4 | According to the Operator Guide, the Vandrell Relay minimum TLS version is 1.2. | invented | -- | The claim attributes the TLS minimum to the Operator Guide (source_a.md), which does not mention TLS; only the Deployment Notes (source_b.md) state it, so the attribution was invented by the merge. |
| 1 | The Vandrell Relay listens on port 8443. | supported | `source_a.md` | 'The relay listens on port 8443.' in `source_a.md` -- Both sources state that the relay listens on port 8443, and source_a.md is the one quoted. |
| 2 | The Vandrell Relay read timeout is 30 seconds. | supported | `source_a.md` | 'The read timeout is 30 seconds.' in `source_a.md` -- The Operator Guide states the read timeout is 30 seconds, which is the same as the claim. |
| 3 | The Vandrell Relay health check path is /healthz. | supported | `source_a.md` | 'The health check path is /healthz.' in `source_a.md` -- The Operator Guide states the health check path is /healthz, which is the same as the claim. |
| 5 | The Vandrell Relay maximum concurrent connections is 512. | supported | `source_b.md` | 'The maximum concurrent connections is 512.' in `source_b.md` -- The Deployment Notes state the maximum concurrent connections is 512, which is the same as the claim. |

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
| Duration | 36.4s |
| Generated | 2026-09-27T20:06:12+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup opus-5.5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
