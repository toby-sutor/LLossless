## Verdict

**No extracted claim was dropped, contradicted, invented, or carried only in part.** 18 source claim(s) checked against the merge, 8 merge claim(s) checked against the sources. This covers the claims that were extracted, not the documents: titles, headings and formatting are not claims and were not checked.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 8 |
| Claims extracted from `source_a.md` | 8 |
| Claims extracted from `source_b.md` | 10 |
| Forward — source claims accounted for in the merge | **18/18** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **8/8** |
| Forward — `source_b.md` claims accounted for | **10/10** |
| Reverse — merge claims found in a source | **8/8** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **26/26** |
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

### `source_a.md` -- 8 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 8 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Unless overridden, the relay binds to port 8443. | 7 | carried | "The relay's default listen port is 8443." in `merged.md` -- The default port is explicitly stated as 8443, implying it applies unless overridden. |
| 2 | A connection that has not been established within 30 seconds is abandoned. | 8 | carried | 'Connections that do not complete a handshake inside 30 seconds are dropped.' in `merged.md` -- Failing to complete a handshake within 30 seconds and being dropped matches an unestablished connection being abandoned. |
| 3 | Once connected, the relay waits up to 120 seconds for a response. | 9 | carried | 'The relay allows a response 120 seconds to arrive before it times out.' in `merged.md` -- The relay waiting up to 120 seconds for a response matches the claim directly. |
| 4 | No more than 512 connections may be open at the same time. | 13 | carried | 'At most 512 connections may be held open concurrently.' in `merged.md` -- This directly matches the maximum concurrent connections claim. |
| 5 | A failed request is attempted again up to 3 times. | 14 | carried | 'The relay makes up to 3 further attempts after a request fails.' in `merged.md` -- This matches the retry claim exactly in meaning. |
| 6 | Anything older than TLS 1.2 is rejected. | 18 | carried | 'The relay will not negotiate any protocol version below TLS 1.2.' in `merged.md` -- Not negotiating below TLS 1.2 means anything older is rejected. |
| 7 | Every access log line is a single JSON object. | 22 | carried | 'Access log records are emitted one JSON object per line.' in `merged.md` -- This directly states one JSON object per log line. |
| 8 | Liveness is reported at /-/healthy. | 23 | carried | 'The endpoint /-/healthy answers health checks.' in `merged.md` -- The endpoint is described as answering health checks, consistent with liveness reporting. |

### `source_b.md` -- 10 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 10 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Vandrell Relay is a fictional HTTP relay. | 3 | carried | 'Vandrell Relay is a fictional HTTP relay.' in `merged.md` -- This is stated verbatim in the text. |
| 2 | The listen port is 8443. | 7 | carried | "The relay's default listen port is 8443." in `merged.md` -- The listen port is explicitly given as 8443. |
| 3 | The connect timeout is 30 seconds. | 8 | carried | 'Connections that do not complete a handshake inside 30 seconds are dropped.' in `merged.md` -- This describes a 30 second timeout for connection establishment, matching connect timeout. |
| 4 | The read timeout is 120 seconds. | 9 | carried | 'The relay allows a response 120 seconds to arrive before it times out.' in `merged.md` -- The 120 second response wait time matches the read timeout claim. |
| 5 | The maximum concurrent connections is 512. | 10 | carried | 'At most 512 connections may be held open concurrently.' in `merged.md` -- This matches the max concurrent connections claim of 512. |
| 6 | The retry attempts per request is 3. | 11 | carried | 'The relay makes up to 3 further attempts after a request fails.' in `merged.md` -- This matches the retry attempts per request claim of 3. |
| 7 | TLS 1.2 is the oldest protocol version the relay will negotiate. | 15 | carried | 'The relay will not negotiate any protocol version below TLS 1.2.' in `merged.md` -- This confirms TLS 1.2 as the oldest negotiable protocol version. |
| 8 | The access log uses JSON Lines. | 16 | carried | 'Access log records are emitted one JSON object per line.' in `merged.md` -- One JSON object per line describes the JSON Lines format even though the term isn't used. |
| 9 | The access log has one record per line. | 16 | carried | 'Access log records are emitted one JSON object per line.' in `merged.md` -- This states one record per line explicitly. |
| 10 | Health checks should target /-/healthy. | 17 | carried | 'The endpoint /-/healthy answers health checks.' in `merged.md` -- This states that health checks target the /-/healthy endpoint. |

### `merged.md` -- 8 claim(s): 0 invented, 0 contradicted, 0 supported in part, 8 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | The relay's default listen port is 8443. | supported | `source_a.md` | 'Unless you override it, the relay binds to port 8443.' in `source_a.md` -- Source_a states the default listen port is 8443, matching the claim. |
| 2 | Connections that do not complete a handshake inside 30 seconds are dropped. | supported | `source_a.md` | 'A connection that has not been established within 30 seconds is abandoned.' in `source_a.md` -- This describes connections failing to complete within 30 seconds being dropped, matching the claim. |
| 3 | The relay allows a response 120 seconds to arrive before it times out. | supported | `source_a.md` | 'Once connected, the relay waits up to 120 seconds for a response.' in `source_a.md` -- The relay allowing up to 120 seconds for a response matches the claim directly. |
| 4 | At most 512 connections may be held open concurrently. | supported | `source_a.md` | 'No more than 512 connections may be open at the same time.' in `source_a.md` -- This directly states the concurrent connection limit of 512. |
| 5 | The relay makes up to 3 further attempts after a request fails. | supported | `source_a.md` | 'A failed request is attempted again up to 3 times.' in `source_a.md` -- This matches the claim of up to 3 retries after a failed request. |
| 6 | The relay will not negotiate any protocol version below TLS 1.2. | supported | `source_a.md` | 'Anything older than TLS 1.2 is rejected.' in `source_a.md` -- This states the relay rejects protocol versions older than TLS 1.2, matching the claim. |
| 7 | Access log records are emitted one JSON object per line. | supported | `source_a.md` | 'Every access log line is a single JSON object.' in `source_a.md` -- This matches the claim about one JSON object per log line. |
| 8 | The endpoint /-/healthy answers health checks. | supported | `source_a.md` | 'Liveness is reported at /-/healthy.' in `source_a.md` -- This confirms /-/healthy is used for health/liveness checks, matching the claim. |

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
| Tokens | 10,502 in, 5,801 out |
| Cost | ~$0.08 estimated (rates read 2026-08-31) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 45.9s |
| Generated | 2026-09-27T17:38:59+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
