## Verdict

**3 finding(s).** In the claims: 1 partially dropped, 2 partially invented.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 9 |
| Claims extracted from `source_a.md` | 8 |
| Claims extracted from `source_b.md` | 10 |
| Forward — source claims accounted for in the merge | **17/18** |
| Forward — carried only in part | 1 |
| Forward — `source_a.md` claims accounted for | **8/8** |
| Forward — `source_b.md` claims accounted for | **9/10** (1 in part) |
| Reverse — merge claims found in a source | **7/9** |
| Reverse — supported only in part | 2 |
| Evidence grounded | **27/27** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Partly dropped — the merge carries some of this claim

- **B-006** (`source_b.md:11`) — The number of retry attempts per request is 3.
  - evidence: 'The relay makes up to 3 further attempts after a request fails.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The reference gives a maximum of three retries but does not state that every request gets exactly three.

### Partly invented — the sources carry some of this claim

- **M-003** (`merged.md:8`) — Connections that do not complete a handshake inside 30 seconds are dropped.
  - evidence: 'A connection that has not been established within 30 seconds is abandoned.' in `source_a.md` (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - rationale: The source supports abandoning a connection after 30 seconds, but does not specify that this is a handshake.
- **M-009** (`merged.md:20`) — The endpoint /-/healthy answers health checks.
  - evidence: '- Health checks should target /-/healthy.' in `source_b.md` (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - rationale: The source identifies this endpoint as the health-check target, but does not explicitly state that it answers the checks.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 8 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 8 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The relay binds to port 8443 unless overridden. | 7 | carried | "The relay's default listen port is 8443." in `merged.md` -- The reference identifies 8443 as the relay's default listen port. |
| 2 | A connection that has not been established within 30 seconds is abandoned. | 8 | carried | 'Connections that do not complete a handshake inside 30 seconds are dropped.' in `merged.md` -- The reference says connections that fail to complete a handshake within 30 seconds are dropped. |
| 3 | Once connected, the relay waits up to 120 seconds for a response. | 9 | carried | 'The relay allows a response 120 seconds to arrive before it times out.' in `merged.md` -- The reference gives 120 seconds for a response to arrive before timeout. |
| 4 | No more than 512 connections may be open at the same time. | 13 | carried | 'At most 512 connections may be held open concurrently.' in `merged.md` -- The reference sets the concurrent open-connection limit at 512. |
| 5 | A failed request is attempted again up to 3 times. | 14 | carried | 'The relay makes up to 3 further attempts after a request fails.' in `merged.md` -- The reference states that a failed request may receive up to three further attempts. |
| 6 | Anything older than TLS 1.2 is rejected. | 18 | carried | 'The relay will not negotiate any protocol version below TLS 1.2.' in `merged.md` -- The reference says versions below TLS 1.2 are not negotiated. |
| 7 | Every access log line is a single JSON object. | 22 | carried | 'Access log records are emitted one JSON object per line.' in `merged.md` -- The reference specifies one JSON object on each access-log line. |
| 8 | Liveness is reported at /-/healthy. | 23 | carried | 'The endpoint /-/healthy answers health checks.' in `merged.md` -- The reference identifies /-/healthy as the endpoint that answers health checks. |

### `source_b.md` -- 10 claim(s): 0 dropped, 0 contradicted, 1 carried in part, 9 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 6 | The number of retry attempts per request is 3. | 11 | carried in part | 'The relay makes up to 3 further attempts after a request fails.' in `merged.md` -- The reference gives a maximum of three retries but does not state that every request gets exactly three. |
| 1 | Vandrell Relay is a fictional HTTP relay. | 3 | carried | 'Vandrell Relay is a fictional HTTP relay.' in `merged.md` -- The reference states this directly. |
| 2 | The listen port is 8443. | 7 | carried | "The relay's default listen port is 8443." in `merged.md` -- The reference gives 8443 as the listen port's default value. |
| 3 | The connect timeout is 30 seconds. | 8 | carried | 'Connections that do not complete a handshake inside 30 seconds are dropped.' in `merged.md` -- The reference sets the connection-handshake limit at 30 seconds. |
| 4 | The read timeout is 120 seconds. | 9 | carried | 'The relay allows a response 120 seconds to arrive before it times out.' in `merged.md` -- The reference states the response timeout is 120 seconds. |
| 5 | The maximum number of concurrent connections is 512. | 10 | carried | 'At most 512 connections may be held open concurrently.' in `merged.md` -- The reference gives 512 as the maximum number of concurrently open connections. |
| 7 | TLS 1.2 is the oldest protocol version the relay will negotiate. | 15 | carried | 'The relay will not negotiate any protocol version below TLS 1.2.' in `merged.md` -- The reference makes TLS 1.2 the lowest negotiable protocol version. |
| 8 | The access log uses JSON Lines. | 16 | carried | 'Access log records are emitted one JSON object per line.' in `merged.md` -- The reference describes newline-separated JSON objects, consistent with JSON Lines. |
| 9 | The access log has one record per line. | 16 | carried | 'Access log records are emitted one JSON object per line.' in `merged.md` -- The reference states that each access-log line contains one record as a JSON object. |
| 10 | Health checks should target /-/healthy. | 17 | carried | 'The endpoint /-/healthy answers health checks.' in `merged.md` -- The reference identifies /-/healthy as the endpoint for health checks. |

### `merged.md` -- 9 claim(s): 0 invented, 0 contradicted, 2 supported in part, 7 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 3 | Connections that do not complete a handshake inside 30 seconds are dropped. | supported in part | `source_a.md` | 'A connection that has not been established within 30 seconds is abandoned.' in `source_a.md` -- The source supports abandoning a connection after 30 seconds, but does not specify that this is a handshake. |
| 9 | The endpoint /-/healthy answers health checks. | supported in part | `source_b.md` | '- Health checks should target /-/healthy.' in `source_b.md` -- The source identifies this endpoint as the health-check target, but does not explicitly state that it answers the checks. |
| 1 | Vandrell Relay is a fictional HTTP relay. | supported | `source_a.md` | 'Vandrell Relay is a fictional HTTP relay.' in `source_a.md` -- The source states that Vandrell Relay is a fictional HTTP relay. |
| 2 | The relay's default listen port is 8443. | supported | `source_a.md` | 'Unless you override it, the relay binds to port 8443.' in `source_a.md` -- The source identifies 8443 as the default listening port. |
| 4 | The relay allows a response 120 seconds to arrive before it times out. | supported | `source_a.md` | 'Once connected, the relay waits up to 120 seconds for a response.' in `source_a.md` -- This states the 120-second response wait that the claim describes. |
| 5 | At most 512 connections may be held open concurrently. | supported | `source_a.md` | 'No more than 512 connections may be open at the same time.' in `source_a.md` -- This directly states the maximum number of concurrently open connections. |
| 6 | The relay makes up to 3 further attempts after a request fails. | supported | `source_a.md` | 'A failed request is attempted again up to 3 times.' in `source_a.md` -- The source says a failed request is retried up to three times. |
| 7 | The relay will not negotiate any protocol version below TLS 1.2. | supported | `source_a.md` | 'Anything older than TLS 1.2 is rejected.' in `source_a.md` -- Rejecting anything older than TLS 1.2 means the relay will not negotiate a lower version. |
| 8 | Access log records are emitted one JSON object per line. | supported | `source_a.md` | 'Every access log line is a single JSON object.' in `source_a.md` -- This directly states that each access log line contains one JSON object. |

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
| Tokens | 7,060 in, 5,409 out, 0 cached, 3,087 reasoning |
| Cost | ~$0.00 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 44.0s |
| Generated | 2026-09-27T16:48:29+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `bf7d5842201d`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
