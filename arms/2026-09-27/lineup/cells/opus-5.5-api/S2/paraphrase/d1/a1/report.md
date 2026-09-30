## Verdict

**2 finding(s).** In the claims: 2 partially dropped.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 9 |
| Claims extracted from `source_a.md` | 9 |
| Claims extracted from `source_b.md` | 10 |
| Forward — source claims accounted for in the merge | **17/19** |
| Forward — carried only in part | 2 |
| Forward — `source_a.md` claims accounted for | **9/9** |
| Forward — `source_b.md` claims accounted for | **8/10** (2 in part) |
| Reverse — merge claims found in a source | **9/9** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **28/28** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Partly dropped — the merge carries some of this claim

- **B-005** (`source_b.md:10`) — The default maximum concurrent connections of Vandrell Relay is 512.
  - evidence: 'At most 512 connections may be held open concurrently.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The 512 concurrent connection limit is stated, but the text does not say it is a default value.
- **B-006** (`source_b.md:11`) — The default number of retry attempts per request in Vandrell Relay is 3.
  - evidence: 'The relay makes up to 3 further attempts after a request fails.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: Up to 3 retry attempts is stated, but the text does not say this is a default value.

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
| 1 | Vandrell Relay is a fictional HTTP relay. | 3 | carried | 'Vandrell Relay is a fictional HTTP relay.' in `merged.md` -- The reference text states this verbatim. |
| 2 | By default, the Vandrell Relay binds to port 8443. | 7 | carried | "The relay's default listen port is 8443." in `merged.md` -- A default listen port of 8443 means the relay binds to port 8443 by default. |
| 3 | A Vandrell Relay connection that has not been established within 30 seconds is abandoned. | 8 | carried | 'Connections that do not complete a handshake inside 30 seconds are dropped.' in `merged.md` -- Connections not established within 30 seconds are dropped, which means abandoned. |
| 4 | Once connected, the Vandrell Relay waits up to 120 seconds for a response. | 9 | carried | 'The relay allows a response 120 seconds to arrive before it times out.' in `merged.md` -- The relay waits up to 120 seconds for a response. |
| 5 | No more than 512 connections may be open at the same time on the Vandrell Relay. | 13 | carried | 'At most 512 connections may be held open concurrently.' in `merged.md` -- At most 512 concurrent open connections matches the claim. |
| 6 | A failed request on the Vandrell Relay is attempted again up to 3 times. | 14 | carried | 'The relay makes up to 3 further attempts after a request fails.' in `merged.md` -- Up to 3 further attempts after a failure means the request is retried up to 3 times. |
| 7 | The Vandrell Relay rejects anything older than TLS 1.2. | 18 | carried | 'The relay will not negotiate any protocol version below TLS 1.2.' in `merged.md` -- Refusing versions below TLS 1.2 means rejecting anything older than TLS 1.2. |
| 8 | Every Vandrell Relay access log line is a single JSON object. | 22 | carried | 'Access log records are emitted one JSON object per line.' in `merged.md` -- One JSON object per line means each line is a single JSON object. |
| 9 | The Vandrell Relay reports liveness at /-/healthy. | 23 | carried | 'The endpoint /-/healthy answers health checks.' in `merged.md` -- The /-/healthy endpoint answers health checks, which is liveness reporting. |

### `source_b.md` -- 10 claim(s): 0 dropped, 0 contradicted, 2 carried in part, 8 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 5 | The default maximum concurrent connections of Vandrell Relay is 512. | 10 | carried in part | 'At most 512 connections may be held open concurrently.' in `merged.md` -- The 512 concurrent connection limit is stated, but the text does not say it is a default value. |
| 6 | The default number of retry attempts per request in Vandrell Relay is 3. | 11 | carried in part | 'The relay makes up to 3 further attempts after a request fails.' in `merged.md` -- Up to 3 retry attempts is stated, but the text does not say this is a default value. |
| 1 | Vandrell Relay is a fictional HTTP relay. | 3 | carried | 'Vandrell Relay is a fictional HTTP relay.' in `merged.md` -- The reference text states this verbatim. |
| 2 | The default listen port of Vandrell Relay is 8443. | 7 | carried | "The relay's default listen port is 8443." in `merged.md` -- The default listen port is stated as 8443. |
| 3 | The default connect timeout of Vandrell Relay is 30 seconds. | 8 | carried | 'Connections that do not complete a handshake inside 30 seconds are dropped.' in `merged.md` -- Under the Network defaults section, the connection establishment timeout is 30 seconds. |
| 4 | The default read timeout of Vandrell Relay is 120 seconds. | 9 | carried | 'The relay allows a response 120 seconds to arrive before it times out.' in `merged.md` -- Under the Network defaults section, the response (read) timeout is 120 seconds. |
| 7 | TLS 1.2 is the oldest protocol version the Vandrell Relay will negotiate. | 15 | carried | 'The relay will not negotiate any protocol version below TLS 1.2.' in `merged.md` -- Not negotiating below TLS 1.2 makes TLS 1.2 the oldest negotiable version. |
| 8 | The Vandrell Relay access log uses JSON Lines. | 16 | carried | 'Access log records are emitted one JSON object per line.' in `merged.md` -- One JSON object per line is the JSON Lines format. |
| 9 | The Vandrell Relay access log has one record per line. | 16 | carried | 'Access log records are emitted one JSON object per line.' in `merged.md` -- Records are emitted one per line. |
| 10 | Health checks for Vandrell Relay should target /-/healthy. | 17 | carried | 'The endpoint /-/healthy answers health checks.' in `merged.md` -- Health checks are answered at /-/healthy, so they should target that endpoint. |

### `merged.md` -- 9 claim(s): 0 invented, 0 contradicted, 0 supported in part, 9 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Vandrell Relay is a fictional HTTP relay. | supported | `source_a.md` | 'Vandrell Relay is a fictional HTTP relay.' in `source_a.md` -- Both sources state this sentence verbatim. |
| 2 | The Vandrell Relay's default listen port is 8443. | supported | `source_a.md` | 'Unless you override it, the relay binds to port 8443.' in `source_a.md` -- Binding to port 8443 unless overridden means the default listen port is 8443. |
| 3 | Vandrell Relay drops connections that do not complete a handshake inside 30 seconds. | supported | `source_a.md` | 'A connection that has not been established within 30 seconds is abandoned.' in `source_a.md` -- Abandoning a connection not established within 30 seconds is a rewording of dropping connections that fail to complete their handshake within 30 seconds. |
| 4 | Vandrell Relay allows a response 120 seconds to arrive before it times out. | supported | `source_a.md` | 'Once connected, the relay waits up to 120 seconds for a response.' in `source_a.md` -- Waiting up to 120 seconds for a response is the same as allowing a response 120 seconds before timing out. |
| 5 | At most 512 connections may be held open concurrently on Vandrell Relay. | supported | `source_a.md` | 'No more than 512 connections may be open at the same time.' in `source_a.md` -- This states the same concurrent connection limit of 512 in different words. |
| 6 | Vandrell Relay makes up to 3 further attempts after a request fails. | supported | `source_a.md` | 'A failed request is attempted again up to 3 times.' in `source_a.md` -- Being attempted again up to 3 times after failure means up to 3 further attempts. |
| 7 | Vandrell Relay will not negotiate any protocol version below TLS 1.2. | supported | `source_b.md` | 'TLS 1.2 is the oldest protocol version the relay will negotiate.' in `source_b.md` -- If TLS 1.2 is the oldest version negotiated, no version below it is negotiated. |
| 8 | Vandrell Relay emits access log records one JSON object per line. | supported | `source_a.md` | 'Every access log line is a single JSON object.' in `source_a.md` -- Each log line being a single JSON object means one JSON object per line. |
| 9 | The Vandrell Relay endpoint /-/healthy answers health checks. | supported | `source_b.md` | 'Health checks should target /-/healthy.' in `source_b.md` -- Health checks targeting /-/healthy means that endpoint answers health checks. |

## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | ec0c9ecb43e3 (hosted) |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | none — this run made no merge |
| Model (decompose) | claude-opus-5-5 |
| Model (verify) | claude-opus-5-5 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile anthropic |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 5 live, 0 cached, 0 replayed |
| Tokens | 10,750 in, 5,265 out |
| Cost | ~$0.15 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 47.9s |
| Generated | 2026-09-27T17:38:13+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
