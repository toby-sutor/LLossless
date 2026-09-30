## Verdict

**2 finding(s).** In the claims: 2 partially dropped.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 8 |
| Claims extracted from `source_a.md` | 8 |
| Claims extracted from `source_b.md` | 8 |
| Forward — source claims accounted for in the merge | **14/16** |
| Forward — carried only in part | 2 |
| Forward — `source_a.md` claims accounted for | **6/8** (2 in part) |
| Forward — `source_b.md` claims accounted for | **8/8** |
| Reverse — merge claims found in a source | **8/8** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **24/24** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Partly dropped — the merge carries some of this claim

- **A-001** (`source_a.md:7`) — The relay binds to port 8443 unless overridden.
  - evidence: "The relay's default listen port is 8443." in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The reference text states the default port is 8443 but does not explicitly state it can be overridden.
- **A-005** (`source_a.md:14`) — A failed request is attempted again up to 3 times.
  - evidence: 'The relay makes up to 3 further attempts after a request fails.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text states 3 further attempts after failure, but the claim says '3 times' total which could mean 3 additional attempts, leaving ambiguity.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 8 claim(s): 0 dropped, 0 contradicted, 2 carried in part, 6 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The relay binds to port 8443 unless overridden. | 7 | carried in part | "The relay's default listen port is 8443." in `merged.md` -- The reference text states the default port is 8443 but does not explicitly state it can be overridden. |
| 5 | A failed request is attempted again up to 3 times. | 14 | carried in part | 'The relay makes up to 3 further attempts after a request fails.' in `merged.md` -- The text states 3 further attempts after failure, but the claim says '3 times' total which could mean 3 additional attempts, leaving ambiguity. |
| 2 | A connection that has not been established within 30 seconds is abandoned. | 8 | carried | 'Connections that do not complete a handshake inside 30 seconds are dropped.' in `merged.md` -- The reference text directly states that connections not completing handshake within 30 seconds are dropped, matching the claim. |
| 3 | The relay waits up to 120 seconds for a response once connected. | 9 | carried | 'The relay allows a response 120 seconds to arrive before it times out.' in `merged.md` -- The reference text states the relay allows 120 seconds for a response, which matches the claim about waiting up to that duration. |
| 4 | No more than 512 connections may be open at the same time. | 13 | carried | 'At most 512 connections may be held open concurrently.' in `merged.md` -- The reference text directly states the maximum concurrent connections is 512. |
| 6 | Anything older than TLS 1.2 is rejected. | 18 | carried | 'The relay will not negotiate any protocol version below TLS 1.2.' in `merged.md` -- The reference text directly states the relay rejects anything below TLS 1.2. |
| 7 | Every access log line is a single JSON object. | 22 | carried | 'Access log records are emitted one JSON object per line.' in `merged.md` -- The reference text states that each access log line is one JSON object. |
| 8 | Liveness is reported at /-/healthy. | 23 | carried | 'The endpoint /-/healthy answers health checks.' in `merged.md` -- The reference text directly states the /-/healthy endpoint answers health checks. |

### `source_b.md` -- 8 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 8 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Vandrell Relay listens on port 8443. | 7 | carried | "The relay's default listen port is 8443." in `merged.md` -- The reference text states the relay listens on port 8443 by default. |
| 2 | Vandrell Relay has a connect timeout of 30 seconds. | 8 | carried | 'Connections that do not complete a handshake inside 30 seconds are dropped.' in `merged.md` -- The reference text establishes a 30-second connect timeout by stating connections not completing handshake in that period are dropped. |
| 3 | Vandrell Relay has a read timeout of 120 seconds. | 9 | carried | 'The relay allows a response 120 seconds to arrive before it times out.' in `merged.md` -- The reference text states the relay allows 120 seconds for response arrival, matching the read timeout claim. |
| 4 | Vandrell Relay has a maximum of 512 concurrent connections. | 10 | carried | 'At most 512 connections may be held open concurrently.' in `merged.md` -- The reference text directly states the maximum concurrent connections is 512. |
| 5 | Vandrell Relay performs 3 retry attempts per request. | 11 | carried | 'The relay makes up to 3 further attempts after a request fails.' in `merged.md` -- The reference text states the relay makes 3 further retry attempts after a request fails. |
| 6 | TLS 1.2 is the oldest protocol version the relay will negotiate. | 15 | carried | 'The relay will not negotiate any protocol version below TLS 1.2.' in `merged.md` -- The reference text establishes TLS 1.2 as the minimum by stating no versions below it are negotiated. |
| 7 | The access log uses JSON Lines, one record per line. | 16 | carried | 'Access log records are emitted one JSON object per line.' in `merged.md` -- The reference text states access logs use one JSON object per line, matching JSON Lines format. |
| 8 | Health checks should target /-/healthy. | 17 | carried | 'The endpoint /-/healthy answers health checks.' in `merged.md` -- The reference text directly states that /-/healthy answers health checks. |

### `merged.md` -- 8 claim(s): 0 invented, 0 contradicted, 0 supported in part, 8 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | The relay's default listen port is 8443. | supported | `source_a.md` | 'Unless you override it, the relay binds to port 8443.' in `source_a.md` -- source_a.md directly states the relay binds to port 8443 by default, which is equivalent to saying the default listen port is 8443. |
| 2 | Connections that do not complete a handshake inside 30 seconds are dropped. | supported | `source_a.md` | 'A connection that has not been established within 30 seconds is abandoned.' in `source_a.md` -- source_a.md states connections not established within 30 seconds are abandoned, which is synonymous with being dropped. |
| 3 | The relay allows a response 120 seconds to arrive before it times out. | supported | `source_a.md` | 'Once connected, the relay waits up to 120 seconds for a response.' in `source_a.md` -- source_a.md directly states the relay waits up to 120 seconds for a response, which means it times out if response does not arrive within 120 seconds. |
| 4 | At most 512 connections may be held open concurrently. | supported | `source_a.md` | 'No more than 512 connections may be open at the same time.' in `source_a.md` -- source_a.md directly states the maximum of 512 concurrent open connections, which is equivalent to the claim. |
| 5 | The relay makes up to 3 further attempts after a request fails. | supported | `source_a.md` | 'A failed request is attempted again up to 3 times.' in `source_a.md` -- source_a.md directly states failed requests are retried up to 3 times, which means 3 further attempts after initial failure. |
| 6 | The relay will not negotiate any protocol version below TLS 1.2. | supported | `source_a.md` | 'Anything older than TLS 1.2 is rejected.' in `source_a.md` -- source_a.md states protocols older than TLS 1.2 are rejected, meaning TLS 1.2 is the minimum version negotiated. |
| 7 | Access log records are emitted one JSON object per line. | supported | `source_a.md` | 'Every access log line is a single JSON object.' in `source_a.md` -- source_a.md directly states each access log line is a single JSON object, which matches the claim about one record per line. |
| 8 | The endpoint /-/healthy answers health checks. | supported | `source_a.md` | 'Liveness is reported at /-/healthy.' in `source_a.md` -- source_a.md states liveness is reported at /-/healthy, indicating that endpoint answers health checks. |

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
| Tokens | 7,885 in, 3,501 out |
| Cost | ~$0.03 estimated (rates read 2026-08-31) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 25.7s |
| Generated | 2026-09-27T17:37:25+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
