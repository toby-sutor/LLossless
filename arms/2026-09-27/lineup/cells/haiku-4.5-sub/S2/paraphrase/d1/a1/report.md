## Verdict

**No extracted claim was dropped, contradicted, invented, or carried only in part.** 17 source claim(s) checked against the merge, 8 merge claim(s) checked against the sources. This covers the claims that were extracted, not the documents: titles, headings and formatting are not claims and were not checked.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 8 |
| Claims extracted from `source_a.md` | 8 |
| Claims extracted from `source_b.md` | 9 |
| Forward — source claims accounted for in the merge | **17/17** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **8/8** |
| Forward — `source_b.md` claims accounted for | **9/9** |
| Reverse — merge claims found in a source | **8/8** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **25/25** |
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
| 1 | The relay binds to port 8443. | 7 | carried | "The relay's default listen port is 8443." in `merged.md` -- The reference text states the relay's default listen port, which establishes the port it binds to. |
| 2 | A connection that has not been established within 30 seconds is abandoned. | 8 | carried | 'Connections that do not complete a handshake inside 30 seconds are dropped.' in `merged.md` -- The reference text directly states that connections not completing a handshake within 30 seconds are dropped, meaning abandoned. |
| 3 | The relay waits up to 120 seconds for a response. | 9 | carried | 'The relay allows a response 120 seconds to arrive before it times out.' in `merged.md` -- The reference text states the relay allows responses 120 seconds to arrive, equivalent to waiting up to 120 seconds. |
| 4 | No more than 512 connections may be open at the same time. | 13 | carried | 'At most 512 connections may be held open concurrently.' in `merged.md` -- The reference text states the maximum concurrent connections is 512, matching the claim's statement. |
| 5 | A failed request is attempted again up to 3 times. | 14 | carried | 'The relay makes up to 3 further attempts after a request fails.' in `merged.md` -- The reference text states the relay makes up to 3 further attempts after a request fails. |
| 6 | Anything older than TLS 1.2 is rejected. | 18 | carried | 'The relay will not negotiate any protocol version below TLS 1.2.' in `merged.md` -- The reference text states the relay will not negotiate versions below TLS 1.2, equivalent to rejecting older versions. |
| 7 | Every access log line is a single JSON object. | 22 | carried | 'Access log records are emitted one JSON object per line.' in `merged.md` -- The reference text directly states access log records are emitted one JSON object per line. |
| 8 | Liveness is reported at /-/healthy. | 23 | carried | 'The endpoint /-/healthy answers health checks.' in `merged.md` -- The reference text directly states the /-/healthy endpoint answers health checks. |

### `source_b.md` -- 9 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 9 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Vandrell Relay is a fictional HTTP relay. | 3 | carried | 'Vandrell Relay is a fictional HTTP relay.' in `merged.md` -- The reference text explicitly states this definition in the opening paragraph. |
| 2 | The listen port is 8443. | 7 | carried | "The relay's default listen port is 8443." in `merged.md` -- The reference text states the default listen port is 8443, supporting the claim that the listen port is 8443. |
| 3 | The connect timeout is 30 seconds. | 8 | carried | 'Connections that do not complete a handshake inside 30 seconds are dropped.' in `merged.md` -- The reference text establishes a 30-second connect timeout by stating connections incomplete after 30 seconds are dropped. |
| 4 | The read timeout is 120 seconds. | 9 | carried | 'The relay allows a response 120 seconds to arrive before it times out.' in `merged.md` -- The reference text establishes a 120-second read timeout for responses to arrive before timeout. |
| 5 | The maximum concurrent connections is 512. | 10 | carried | 'At most 512 connections may be held open concurrently.' in `merged.md` -- The reference text directly states the maximum concurrent connections is 512. |
| 6 | The retry attempts per request is 3. | 11 | carried | 'The relay makes up to 3 further attempts after a request fails.' in `merged.md` -- The reference text states the relay makes up to 3 further attempts after a request fails. |
| 7 | TLS 1.2 is the oldest protocol version the relay will negotiate. | 15 | carried | 'The relay will not negotiate any protocol version below TLS 1.2.' in `merged.md` -- The reference text states the relay will not negotiate below TLS 1.2, making 1.2 the oldest negotiable version. |
| 8 | The access log uses JSON Lines, one record per line. | 16 | carried | 'Access log records are emitted one JSON object per line.' in `merged.md` -- The reference text describes the JSON Lines format by stating one JSON object is emitted per line. |
| 9 | Health checks should target /-/healthy. | 17 | carried | 'The endpoint /-/healthy answers health checks.' in `merged.md` -- The reference text states the endpoint answers health checks, implying health checks should target it. |

### `merged.md` -- 8 claim(s): 0 invented, 0 contradicted, 0 supported in part, 8 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | The relay's default listen port is 8443. | supported | `source_a.md` | 'Unless you override it, the relay binds to port 8443.' in `source_a.md` -- Source_a.md directly states that the relay binds to port 8443 by default. |
| 2 | Connections that do not complete a handshake inside 30 seconds are dropped. | supported | `source_a.md` | 'A connection that has not been established within 30 seconds is abandoned.' in `source_a.md` -- A connection not established within 30 seconds is abandoned, equivalent to not completing a handshake. |
| 3 | The relay allows a response 120 seconds to arrive before it times out. | supported | `source_a.md` | 'Once connected, the relay waits up to 120 seconds for a response.' in `source_a.md` -- Source_a.md directly states the relay waits up to 120 seconds for a response. |
| 4 | At most 512 connections may be held open concurrently. | supported | `source_a.md` | 'No more than 512 connections may be open at the same time.' in `source_a.md` -- Source_a.md states no more than 512 connections may be open concurrently. |
| 5 | The relay makes up to 3 further attempts after a request fails. | supported | `source_a.md` | 'A failed request is attempted again up to 3 times.' in `source_a.md` -- Source_a.md states failed requests are attempted again up to 3 times. |
| 6 | The relay will not negotiate any protocol version below TLS 1.2. | supported | `source_a.md` | 'Anything older than TLS 1.2 is rejected.' in `source_a.md` -- Rejecting anything older than TLS 1.2 means the relay will not negotiate below TLS 1.2. |
| 7 | Access log records are emitted one JSON object per line. | supported | `source_a.md` | 'Every access log line is a single JSON object.' in `source_a.md` -- Source_a.md directly states every access log line is a single JSON object. |
| 8 | The endpoint /-/healthy answers health checks. | supported | `source_b.md` | 'Health checks should target /-/healthy.' in `source_b.md` -- Source_b.md states health checks should target the /-/healthy endpoint. |

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
| Duration | 155.8s |
| Generated | 2026-09-27T21:06:34+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup haiku-4.5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
