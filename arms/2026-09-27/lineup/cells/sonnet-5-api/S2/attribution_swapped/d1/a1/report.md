## Verdict

**4 finding(s).** In the claims: 2 contradicted. In the attributions: 2 credited to a source that does not state it.

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
| Reverse — merge claims found in a source | **2/4** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **10/10** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **M-003** -- the two documents disagree
  - `merged.md:7` says: According to the Deployment Notes, the read timeout is 30 seconds.
  - `source_b.md` says: 'The read timeout is 60 seconds.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The Deployment Notes document states the read timeout is 60 seconds, not 30 seconds as claimed.
- **M-004** -- the two documents disagree
  - `merged.md:8` says: According to the Operator Guide, the read timeout is 60 seconds.
  - `source_a.md` says: 'The read timeout is 30 seconds.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The Operator Guide document states the read timeout is 30 seconds, not 60 seconds as claimed.

## Attributions

Each sentence below credits a named source with a statement that source does not contain, while another source contains it word for word. The name was matched to one source by its title or its filename, and no model was asked anything. A sentence the merge copied from a source as written is never listed, and neither is one whose statement no source contains or whose name fits two sources.

- `m5` (`source_b.md`) - the merge credits 'the read timeout is 30 seconds' to the Deployment Notes (source_b.md), which does not state it; source_a.md does

  ```text
  In the source: The read timeout is 30 seconds.
  In the merge:  According to the Deployment Notes, the read timeout is 30 seconds.
  ```
- `m6` (`source_a.md`) - the merge credits 'the read timeout is 60 seconds' to the Operator Guide (source_a.md), which does not state it; source_b.md does

  ```text
  In the source: The read timeout is 60 seconds.
  In the merge:  According to the Operator Guide, the read timeout is 60 seconds.
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
| 1 | The relay listens on port 8443. | 3 | carried | 'The relay listens on port 8443.' in `merged.md` -- The reference text directly states this fact. |
| 2 | The read timeout is 30 seconds. | 4 | carried | 'According to the Deployment Notes, the read timeout is 30 seconds.' in `merged.md` -- The Deployment Notes are cited as stating a 30 second read timeout, satisfying attribution rules. |
| 3 | The health check path is /healthz. | 5 | carried | 'The health check path is /healthz.' in `merged.md` -- The reference text directly states this fact. |

### `source_b.md` -- 3 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 3 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The Vandrell Relay listens on port 8443. | 3 | carried | 'The relay listens on port 8443.' in `merged.md` -- The document title identifies this as the Vandrell Relay configuration, and the relay listens on port 8443 as stated. |
| 2 | The read timeout is 60 seconds. | 4 | carried | 'According to the Operator Guide, the read timeout is 60 seconds.' in `merged.md` -- The Operator Guide is cited as stating a 60 second read timeout, satisfying attribution rules. |
| 3 | The health check path is /healthz. | 5 | carried | 'The health check path is /healthz.' in `merged.md` -- The reference text directly states this fact. |

### `merged.md` -- 4 claim(s): 0 invented, 2 contradicted, 0 supported in part, 2 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 3 | According to the Deployment Notes, the read timeout is 30 seconds. | contradicted | `source_b.md` | 'The read timeout is 60 seconds.' in `source_b.md` -- The Deployment Notes document states the read timeout is 60 seconds, not 30 seconds as claimed. |
| 4 | According to the Operator Guide, the read timeout is 60 seconds. | contradicted | `source_a.md` | 'The read timeout is 30 seconds.' in `source_a.md` -- The Operator Guide document states the read timeout is 30 seconds, not 60 seconds as claimed. |
| 1 | The relay listens on port 8443. | supported | `source_a.md` | 'The relay listens on port 8443.' in `source_a.md` -- Both sources state the relay listens on port 8443. |
| 2 | The health check path is /healthz. | supported | `source_a.md` | 'The health check path is /healthz.' in `source_a.md` -- Both sources state the health check path is /healthz. |

## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | ec0c9ecb43e3 (hosted) |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | none — this run made no merge |
| Model (decompose) | claude-sonnet-5 |
| Model (verify) | claude-sonnet-5 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile anthropic |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 5 live, 0 cached, 0 replayed |
| Tokens | 9,093 in, 1,601 out |
| Cost | ~$0.03 estimated (rates read 2026-08-31) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 17.0s |
| Generated | 2026-09-27T17:14:53+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
