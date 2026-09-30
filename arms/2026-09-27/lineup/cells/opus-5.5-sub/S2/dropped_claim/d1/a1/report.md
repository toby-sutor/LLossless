## Verdict

**1 finding(s).** In the claims: 1 dropped.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 11 |
| Claims extracted from `source_a.md` | 7 |
| Claims extracted from `source_b.md` | 8 |
| Forward — source claims accounted for in the merge | **14/15** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **7/7** |
| Forward — `source_b.md` claims accounted for | **7/8** |
| Reverse — merge claims found in a source | **11/11** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **25/25** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Dropped — in a source, not in the merge

- **B-005** (`source_b.md:13`) — Vandrell Relay access logs are written in JSON Lines format.
  - judged against: `merged.md`
  - rationale: The reference text says nothing about access log format or JSON Lines.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 7 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 7 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Vandrell Relay is a fictional HTTP relay. | 3 | carried | 'Vandrell Relay is a fictional HTTP relay.' in `merged.md` -- The reference text states this verbatim. |
| 2 | The Vandrell Relay listens on port 8443 by default. | 7 | carried | 'The relay listens on port 8443 by default.' in `merged.md` -- The reference text states the default listening port is 8443. |
| 3 | The default connect timeout of the Vandrell Relay is 30 seconds. | 8 | carried | 'The default connect timeout is 30 seconds.' in `merged.md` -- The reference text states the default connect timeout is 30 seconds. |
| 4 | The default read timeout of the Vandrell Relay is 120 seconds. | 9 | carried | 'The default read timeout is 120 seconds.' in `merged.md` -- The reference text states the default read timeout is 120 seconds. |
| 5 | The Vandrell Relay accepts at most 512 concurrent connections. | 13 | carried | 'The relay accepts at most 512 concurrent connections.' in `merged.md` -- The reference text states the 512 concurrent connection limit. |
| 6 | Each request to the Vandrell Relay is retried at most 3 times. | 14 | carried | 'Each request is retried at most 3 times.' in `merged.md` -- The reference text states each request is retried at most 3 times. |
| 7 | The minimum TLS version accepted by the Vandrell Relay is TLS 1.2. | 18 | carried | 'The minimum accepted TLS version is TLS 1.2.' in `merged.md` -- The reference text states the minimum accepted TLS version is TLS 1.2. |

### `source_b.md` -- 8 claim(s): 1 dropped, 0 contradicted, 0 carried in part, 7 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 5 | Vandrell Relay access logs are written in JSON Lines format. | 13 | dropped | The reference text says nothing about access log format or JSON Lines. |
| 1 | Vandrell Relay is a fictional HTTP relay. | 3 | carried | 'Vandrell Relay is a fictional HTTP relay.' in `merged.md` -- The reference text states this verbatim. |
| 2 | The Vandrell Relay listens on port 8443 by default. | 7 | carried | 'The relay listens on port 8443 by default.' in `merged.md` -- The reference text states the default listening port is 8443. |
| 3 | The Vandrell Relay accepts at most 512 concurrent connections. | 8 | carried | 'The relay accepts at most 512 concurrent connections.' in `merged.md` -- The reference text states the 512 concurrent connection limit. |
| 4 | The Vandrell Relay starts one worker process per CPU core. | 9 | carried | 'One worker process is started per CPU core.' in `merged.md` -- The reference text states one worker process is started per CPU core. |
| 6 | Vandrell Relay log files are rotated when they reach 100 megabytes. | 14 | carried | 'Log files are rotated when they reach 100 megabytes.' in `merged.md` -- The reference text states log files rotate at 100 megabytes. |
| 7 | The Vandrell Relay health check endpoint is /-/healthy. | 18 | carried | 'The health check endpoint is /-/healthy.' in `merged.md` -- The reference text states the health check endpoint is /-/healthy. |
| 8 | A Vandrell Relay that fails 3 consecutive health checks is removed from rotation. | 19 | carried | 'A relay that fails 3 consecutive health checks is removed from rotation.' in `merged.md` -- The reference text states this rule directly. |

### `merged.md` -- 11 claim(s): 0 invented, 0 contradicted, 0 supported in part, 11 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Vandrell Relay is a fictional HTTP relay. | supported | `source_a.md` | 'Vandrell Relay is a fictional HTTP relay.' in `source_a.md` -- Both sources state this verbatim; source_a.md is quoted. |
| 2 | The Vandrell Relay listens on port 8443 by default. | supported | `source_a.md` | 'The relay listens on port 8443 by default.' in `source_a.md` -- Both sources state the default port is 8443. |
| 3 | The default connect timeout of the Vandrell Relay is 30 seconds. | supported | `source_a.md` | 'The default connect timeout is 30 seconds.' in `source_a.md` -- source_a.md states the default connect timeout is 30 seconds. |
| 4 | The default read timeout of the Vandrell Relay is 120 seconds. | supported | `source_a.md` | 'The default read timeout is 120 seconds.' in `source_a.md` -- source_a.md states the default read timeout is 120 seconds. |
| 5 | The Vandrell Relay accepts at most 512 concurrent connections. | supported | `source_a.md` | 'The relay accepts at most 512 concurrent connections.' in `source_a.md` -- Both sources state the 512 concurrent connection limit. |
| 6 | Each request to the Vandrell Relay is retried at most 3 times. | supported | `source_a.md` | 'Each request is retried at most 3 times.' in `source_a.md` -- source_a.md states each request is retried at most 3 times. |
| 7 | The Vandrell Relay starts one worker process per CPU core. | supported | `source_b.md` | 'One worker process is started per CPU core.' in `source_b.md` -- source_b.md states one worker process is started per CPU core. |
| 8 | The minimum TLS version accepted by the Vandrell Relay is TLS 1.2. | supported | `source_a.md` | 'The minimum accepted TLS version is TLS 1.2.' in `source_a.md` -- source_a.md states the minimum accepted TLS version is TLS 1.2. |
| 9 | Vandrell Relay log files are rotated when they reach 100 megabytes. | supported | `source_b.md` | 'Log files are rotated when they reach 100 megabytes.' in `source_b.md` -- source_b.md states log files rotate at 100 megabytes. |
| 10 | The Vandrell Relay health check endpoint is /-/healthy. | supported | `source_b.md` | 'The health check endpoint is /-/healthy.' in `source_b.md` -- source_b.md states the health check endpoint is /-/healthy. |
| 11 | A Vandrell Relay that fails 3 consecutive health checks is removed from rotation. | supported | `source_b.md` | 'A relay that fails 3 consecutive health checks is removed from rotation.' in `source_b.md` -- source_b.md states this in the same words. |

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
| Calls | 6 live, 0 cached, 0 replayed |
| Tokens | unknown (6 call(s) reported no usage) |
| Cost | unmeasured (6 call(s) reported no tokens, so no figure can be derived) |
| Schema repairs | 1 |
| Isolation | decompose, verify: safe mode, no tools |
| Errors | 0 |
| Duration | 54.3s |
| Generated | 2026-09-27T20:52:52+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup opus-5.5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
