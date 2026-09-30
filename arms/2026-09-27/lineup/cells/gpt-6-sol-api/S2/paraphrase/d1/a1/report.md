## Verdict

**1 finding(s).** In the claims: 1 partially invented.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 9 |
| Claims extracted from `source_a.md` | 9 |
| Claims extracted from `source_b.md` | 10 |
| Forward — source claims accounted for in the merge | **19/19** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **9/9** |
| Forward — `source_b.md` claims accounted for | **10/10** |
| Reverse — merge claims found in a source | **8/9** |
| Reverse — supported only in part | 1 |
| Evidence grounded | **28/28** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Partly invented — the sources carry some of this claim

- **M-003** (`merged.md:8`) — Connections that do not complete a handshake inside 30 seconds are dropped.
  - evidence: 'A connection that has not been established within 30 seconds is abandoned.' in `source_a.md` (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - rationale: The source gives a 30-second limit for establishing a connection, but does not identify an incomplete handshake as the condition.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 9 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 9 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Vandrell Relay is a fictional HTTP relay. | 3 | carried | 'Vandrell Relay is a fictional HTTP relay.' in `merged.md` -- The reference states the claim directly. |
| 2 | Unless overridden, Vandrell Relay binds to port 8443. | 7 | carried | "The relay's default listen port is 8443." in `merged.md` -- A default listen port is the port used unless overridden. |
| 3 | A connection that has not been established within 30 seconds is abandoned. | 8 | carried | 'Connections that do not complete a handshake inside 30 seconds are dropped.' in `merged.md` -- The reference says connections without a completed handshake are dropped after 30 seconds. |
| 4 | Once connected, Vandrell Relay waits up to 120 seconds for a response. | 9 | carried | 'The relay allows a response 120 seconds to arrive before it times out.' in `merged.md` -- The reference gives a 120-second wait for a response. |
| 5 | No more than 512 connections may be open at the same time. | 13 | carried | 'At most 512 connections may be held open concurrently.' in `merged.md` -- The stated limit is 512 simultaneously open connections. |
| 6 | A failed request is attempted again up to 3 times. | 14 | carried | 'The relay makes up to 3 further attempts after a request fails.' in `merged.md` -- The further attempts are retries after a failed request. |
| 7 | Vandrell Relay rejects anything older than TLS 1.2. | 18 | carried | 'The relay will not negotiate any protocol version below TLS 1.2.' in `merged.md` -- Versions older than TLS 1.2 will not be negotiated. |
| 8 | Every Vandrell Relay access log line is a single JSON object. | 22 | carried | 'Access log records are emitted one JSON object per line.' in `merged.md` -- The reference specifies one JSON access-log object per line. |
| 9 | Vandrell Relay reports liveness at /-/healthy. | 23 | carried | 'The endpoint /-/healthy answers health checks.' in `merged.md` -- The named endpoint answers health checks. |

### `source_b.md` -- 10 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 10 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Vandrell Relay is a fictional HTTP relay. | 3 | carried | 'Vandrell Relay is a fictional HTTP relay.' in `merged.md` -- The reference states the claim directly. |
| 2 | The Vandrell Relay listen port is 8443. | 7 | carried | "The relay's default listen port is 8443." in `merged.md` -- The reference identifies 8443 as the relay's default listen port. |
| 3 | The Vandrell Relay connect timeout is 30 seconds. | 8 | carried | 'Connections that do not complete a handshake inside 30 seconds are dropped.' in `merged.md` -- The 30-second handshake limit states the connection timeout. |
| 4 | The Vandrell Relay read timeout is 120 seconds. | 9 | carried | 'The relay allows a response 120 seconds to arrive before it times out.' in `merged.md` -- The reference states a 120-second timeout while waiting for a response. |
| 5 | The Vandrell Relay maximum concurrent connections is 512. | 10 | carried | 'At most 512 connections may be held open concurrently.' in `merged.md` -- This sets the maximum concurrent connection count at 512. |
| 6 | The Vandrell Relay retry attempts per request is 3. | 11 | carried | 'The relay makes up to 3 further attempts after a request fails.' in `merged.md` -- The reference sets a maximum of three retry attempts after failure. |
| 7 | TLS 1.2 is the oldest protocol version Vandrell Relay will negotiate. | 15 | carried | 'The relay will not negotiate any protocol version below TLS 1.2.' in `merged.md` -- The reference sets TLS 1.2 as the minimum negotiable version. |
| 8 | The Vandrell Relay access log uses JSON Lines. | 16 | carried | 'Access log records are emitted one JSON object per line.' in `merged.md` -- One JSON object per line describes JSON Lines format. |
| 9 | The Vandrell Relay access log has one record per line. | 16 | carried | 'Access log records are emitted one JSON object per line.' in `merged.md` -- The reference explicitly specifies one access-log record per line. |
| 10 | Vandrell Relay health checks should target /-/healthy. | 17 | carried | 'The endpoint /-/healthy answers health checks.' in `merged.md` -- Because this endpoint answers health checks, it is the stated health-check target. |

### `merged.md` -- 9 claim(s): 0 invented, 0 contradicted, 1 supported in part, 8 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 3 | Connections that do not complete a handshake inside 30 seconds are dropped. | supported in part | `source_a.md` | 'A connection that has not been established within 30 seconds is abandoned.' in `source_a.md` -- The source gives a 30-second limit for establishing a connection, but does not identify an incomplete handshake as the condition. |
| 1 | Vandrell Relay is a fictional HTTP relay. | supported | `source_a.md` | 'Vandrell Relay is a fictional HTTP relay.' in `source_a.md` -- The source states the claim directly. |
| 2 | The relay's default listen port is 8443. | supported | `source_a.md` | 'Unless you override it, the relay binds to port 8443.' in `source_a.md` -- The port used unless overridden is the default listen port. |
| 4 | Vandrell Relay allows a response 120 seconds to arrive before it times out. | supported | `source_a.md` | 'Once connected, the relay waits up to 120 seconds for a response.' in `source_a.md` -- The source states the response wait limit directly. |
| 5 | At most 512 connections may be held open concurrently. | supported | `source_a.md` | 'No more than 512 connections may be open at the same time.' in `source_a.md` -- The source states the concurrent open-connection limit directly. |
| 6 | Vandrell Relay makes up to 3 further attempts after a request fails. | supported | `source_a.md` | 'A failed request is attempted again up to 3 times.' in `source_a.md` -- Attempts made again after failure are further attempts. |
| 7 | Vandrell Relay will not negotiate any protocol version below TLS 1.2. | supported | `source_b.md` | 'TLS 1.2 is the oldest protocol version the relay will negotiate.' in `source_b.md` -- The source rules out negotiating versions below TLS 1.2. |
| 8 | Access log records are emitted one JSON object per line. | supported | `source_a.md` | 'Every access log line is a single JSON object.' in `source_a.md` -- The source specifies one JSON object on each access log line. |
| 9 | The endpoint /-/healthy answers health checks. | supported | `source_a.md` | 'Liveness is reported at /-/healthy.' in `source_a.md` -- The source identifies /-/healthy as the liveness endpoint. |

## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | bf7d5842201d (hosted) |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | none — this run made no merge |
| Model (decompose) | gpt-6-sol |
| Model (verify) | gpt-6-sol |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed 0, thinking decompose, merge, verify, profile openai-reasoning |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 5 live, 0 cached, 0 replayed |
| Tokens | 7,107 in, 3,808 out, 0 cached, 566 reasoning |
| Cost | ~$0.05 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 46.8s |
| Generated | 2026-09-27T16:49:16+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `bf7d5842201d`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
