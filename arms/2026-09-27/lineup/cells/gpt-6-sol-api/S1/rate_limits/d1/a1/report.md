## Verdict

**11 finding(s).** In the claims: 2 partially dropped, 7 contradicted. In the structure: 1 unresolved replacement, 1 verbatim violation.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 70 |
| Claims extracted from `source_a.md` | 52 |
| Claims extracted from `source_b.md` | 61 |
| Forward — source claims accounted for in the merge | **104/113** |
| Forward — carried only in part | 2 |
| Forward — `source_a.md` claims accounted for | **49/52** |
| Forward — `source_b.md` claims accounted for | **55/61** (2 in part) |
| Reverse — merge claims found in a source | **70/70** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **183/183** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Partly dropped — the merge carries some of this claim

- **B-060** (`source_b.md:37`) — An answer takes two working days.
  - evidence: 'they are answered within two working days' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text gives a two-working-day maximum, not an exact time of two working days.
- **B-061** (`source_b.md:37`) — Chasing an answer doesn’t make it take fewer than two working days.
  - evidence: 'Chasing a request does not speed the answer.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: Chasing does not speed the answer, but the text does not establish two working days as a minimum.

### Contradicted — the merge states something different

- **A-029** -- the two documents disagree
  - `source_a.md:23` says: A batch credential is allowed fifty times the default allowance.
  - `merged.md` says: 'The default allowance is 100 requests in a window, and a credential marked for batch work is allowed 1000 in the same window.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The stated batch allowance is ten times the default, not fifty times.
- **A-034** -- the two documents disagree
  - `source_a.md:29` says: The gateway refuses a request for three reasons.
  - `merged.md` says: 'A cap is one reason for refusal. A credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text lists four reasons: a cap, suspension, route closure and an oversized body.
- **A-035** -- the two documents disagree
  - `source_a.md:29` says: Only one of the gateway’s three reasons for refusing a request is a cap.
  - `merged.md` says: 'A cap is one reason for refusal. A credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Although a cap is one listed reason, the text lists four reasons rather than three.
- **B-031** -- the two documents disagree
  - `source_b.md:23` says: The batch allowance is 50 times the default.
  - `merged.md` says: 'The default allowance is 100 requests in a window, and a credential marked for batch work is allowed 1000 in the same window.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The stated allowances make the batch allowance 10 times, not 50 times, the default.
- **B-039** -- the two documents disagree
  - `source_b.md:29` says: The gateway refuses a request for three separate reasons.
  - `merged.md` says: 'A cap is one reason for refusal. A credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text lists four reasons for refusal, not three.
- **B-040** -- the two documents disagree
  - `source_b.md:29` says: Only one of the gateway’s three reasons for refusing a request is a cap.
  - `merged.md` says: 'A cap is one reason for refusal. A credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: A cap is one of four listed reasons, not one of three.
- **B-041** -- the two documents disagree
  - `source_b.md:29` says: Two of the gateway’s three reasons for refusing a request have nothing to do with how much traffic a caller has sent in the current window.
  - `merged.md` says: 'Suspension, route closure and an oversized body are unrelated to traffic sent in the current window.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text identifies three traffic-independent reasons, in addition to a cap, rather than two of three.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 52 claim(s): 0 dropped, 3 contradicted, 0 carried in part, 49 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 29 | A batch credential is allowed fifty times the default allowance. | 23 | contradicted | 'The default allowance is 100 requests in a window, and a credential marked for batch work is allowed 1000 in the same window.' in `merged.md` -- The stated batch allowance is ten times the default, not fifty times. |
| 34 | The gateway refuses a request for three reasons. | 29 | contradicted | 'A cap is one reason for refusal. A credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit.' in `merged.md` -- The text lists four reasons: a cap, suspension, route closure and an oversized body. |
| 35 | Only one of the gateway’s three reasons for refusing a request is a cap. | 29 | contradicted | 'A cap is one reason for refusal. A credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit.' in `merged.md` -- Although a cap is one listed reason, the text lists four reasons rather than three. |
| 1 | Every credential has a cap. | 3 | carried | 'Every credential has a cap.' in `merged.md` -- The text states the claim directly. |
| 2 | When a credential’s cap is spent, the gateway answers 429 at the edge. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge' in `merged.md` -- The text states what happens when the cap is spent. |
| 3 | The gateway answers 429 without waking the service behind it. | 3 | carried | 'the gateway answers 429 at the edge — without waking the service behind it' in `merged.md` -- The text says the 429 response does not wake the service. |
| 4 | Requests are counted against the credential that presented them. | 5 | carried | 'Requests are counted against the credential that presented them' in `merged.md` -- The text states the counting basis directly. |
| 5 | Requests are counted over a fixed window of 60 seconds. | 5 | carried | 'over a fixed window of 60 seconds' in `merged.md` -- The text gives the fixed counting window. |
| 6 | Requests are never counted against a connection. | 5 | carried | 'never against a connection' in `merged.md` -- The text explicitly excludes connection-based counting. |
| 7 | Opening a second socket does not increase a caller’s allowance. | 5 | carried | 'Opening a second socket therefore buys a caller nothing.' in `merged.md` -- A second socket provides no additional allowance. |
| 8 | A client spread across eight worker processes is throttled at exactly the point one process would have been. | 5 | carried | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `merged.md` -- The text states the same throttling point for eight processes and one. |
| 9 | A client spread across eight worker processes uses extra file descriptors. | 5 | carried | 'A client spread across eight worker processes is throttled at exactly the point one process would have been — and pays for the extra file descriptors as well.' in `merged.md` -- The text says the eight-process client pays for extra file descriptors. |
| 10 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- The text gives the default allowance. |
| 11 | A credential marked for batch work is allowed 1000 in the same window. | 7 | carried | 'a credential marked for batch work is allowed 1000 in the same window' in `merged.md` -- The text gives the batch allowance and its window. |
| 12 | A refusal is not an outage. | 7 | carried | 'A refusal is not an outage' in `merged.md` -- The text states the claim directly. |
| 13 | The refusal carries a Retry-After header. | 11 | carried | 'The refusal carries a Retry-After header.' in `merged.md` -- The text states the claim directly. |
| 14 | The Retry-After header’s value is a whole number of seconds to wait. | 11 | carried | 'Its value is a whole number of seconds to wait.' in `merged.md` -- In context, “Its” refers to the Retry-After header. |
| 15 | The gateway keeps no memory of who backed off politely. | 11 | carried | 'The gateway keeps no memory of who backed off politely' in `merged.md` -- The text states the claim directly. |
| 16 | Waiting longer than the Retry-After header asks earns a caller no credit at all. | 11 | carried | 'waiting longer than the header asks earns a caller no credit at all' in `merged.md` -- In context, the header is Retry-After. |
| 17 | The body of the refusal is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- The text states the body format directly. |
| 18 | The body of the refusal names what the gateway calls the “window” it counted in. | 13 | carried | 'it names what the gateway calls the “window” it counted in' in `merged.md` -- In context, “it” is the refusal body. |
| 19 | The body of the refusal names the cap. | 13 | carried | 'It names the cap and the tier as well.' in `merged.md` -- In context, “It” is the refusal body, which names the cap. |
| 20 | The body of the refusal names the tier. | 13 | carried | 'It names the cap and the tier as well.' in `merged.md` -- In context, “It” is the refusal body, which names the tier. |
| 21 | Nothing in the body of the refusal is meant for the retry loop. | 13 | carried | 'nothing in it is meant for the retry loop' in `merged.md` -- In context, “it” is the refusal body. |
| 22 | The gateway has already calculated the wait given in the Retry-After header. | 19 | carried | 'Honour the header, every time. The gateway has already done that arithmetic' in `merged.md` -- The text says the gateway has already calculated the header’s wait. |
| 23 | The gateway calculates the wait with information the caller does not have. | 19 | carried | 'The gateway has already done that arithmetic, with information the caller does not have' in `merged.md` -- The text says the calculation uses information unavailable to the caller. |
| 24 | The gateway calculates the wait on the 503 path. | 19 | carried | 'The gateway has already done that arithmetic, with information the caller does not have, and it does the same on the 503 path.' in `merged.md` -- The text says the gateway also performs that calculation on the 503 path. |
| 25 | A caller cannot see the gateway’s counter. | 19 | carried | 'a counter it cannot see' in `merged.md` -- In context, the caller cannot see the gateway’s counter. |
| 26 | A 429 calls for the stated wait. | 21 | carried | 'a 429 wants the stated wait' in `merged.md` -- The text says a 429 calls for the stated wait. |
| 27 | A 500 may be retried once the stated wait has passed. | 21 | carried | 'a 500 may be retried once that wait has passed' in `merged.md` -- The text permits retrying a 500 after the wait. |
| 28 | A 503 is the overload path. | 21 | carried | 'a 503 is the overload path' in `merged.md` -- The text identifies 503 as the overload path. |
| 30 | A batch credential is measured over exactly the same window as a default credential. | 23 | carried | 'A batch credential is allowed 1000 requests in the same window as the default tier; it does not use a separate counting scheme.' in `merged.md` -- The batch and default tiers use the same window. |
| 31 | The tier is set on the credential when it is issued. | 23 | carried | 'The tier is set on the credential when it is issued' in `merged.md` -- The text states when the tier is set. |
| 32 | The tier cannot be asked for per call. | 23 | carried | 'cannot be asked for per call' in `merged.md` -- The text rules out requesting the tier per call. |
| 33 | Nothing else about the two tiers differs in any way. | 23 | carried | 'Nothing else about the two tiers differs in any way.' in `merged.md` -- The text states the claim directly. |
| 36 | The gateway may refuse a request because a credential is suspended. | 29 | carried | 'A credential may be suspended' in `merged.md` -- Suspension is listed as a reason for refusal. |
| 37 | The gateway may refuse a request because a route is closed for maintenance. | 29 | carried | 'a route may be closed for maintenance' in `merged.md` -- A maintenance closure is listed as a reason for refusal. |
| 38 | The gateway may refuse a request because a body exceeds the 5 megabyte limit. | 29 | carried | 'a body may exceed the 5 megabyte limit' in `merged.md` -- An oversized body is listed as a reason for refusal. |
| 39 | A refusal caused by a suspended credential does not clear itself by waiting for a stated number of seconds. | 29 | carried | 'Suspension, route closure and an oversized body are unrelated to traffic sent in the current window. None of those three clears itself by waiting for a stated number of seconds.' in `merged.md` -- The statement that none of the three clears by waiting includes suspension. |
| 40 | A refusal caused by a route closed for maintenance does not clear itself by waiting for a stated number of seconds. | 29 | carried | 'Suspension, route closure and an oversized body are unrelated to traffic sent in the current window. None of those three clears itself by waiting for a stated number of seconds.' in `merged.md` -- The statement that none of the three clears by waiting includes route closure. |
| 41 | A refusal caused by a body exceeding the 5 megabyte limit does not clear itself by waiting for a stated number of seconds. | 29 | carried | 'Suspension, route closure and an oversized body are unrelated to traffic sent in the current window. None of those three clears itself by waiting for a stated number of seconds.' in `merged.md` -- The statement that none of the three clears by waiting includes an oversized body. |
| 42 | A loop that waits and retries against a suspended credential does not reach the service. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `merged.md` -- The text says the loop never reaches the service. |
| 43 | After a loop waits and retries against a suspended credential, the log shows a long run of refusals. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service — and the log afterwards shows nothing at all except a long run of refusals.' in `merged.md` -- The text describes a long run of refusals in the log after that loop. |
| 44 | A cap can be raised. | 35 | carried | 'A cap can be raised' in `merged.md` -- The text states the claim directly. |
| 45 | The number of caps raised without a measurement behind them is 0. | 35 | carried | 'the number of caps raised without a measurement behind them is 0' in `merged.md` -- The text gives zero as the number raised without measurement. |
| 46 | The platform team looks at whether the load is smooth or bursty. | 35 | carried | 'The platform team looks at whether the load is smooth or bursty before considering a higher cap' in `merged.md` -- The text says the team examines whether load is smooth or bursty. |
| 47 | A burst is cheaper to smooth than it is to serve at its peak. | 35 | carried | 'a burst is cheaper to smooth than it is to serve at its peak' in `merged.md` -- The text states the cost comparison directly. |
| 48 | A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all. | 35 | carried | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `merged.md` -- The text states the effect of moving half the work to a quieter hour. |
| 49 | Requests reach the platform team through the usual channel. | 37 | carried | 'Requests reach the platform team through the usual channel' in `merged.md` -- The text states how requests reach the platform team. |
| 50 | Requests to the platform team are answered within two working days. | 37 | carried | 'Requests reach the platform team through the usual channel, and they are answered within two working days.' in `merged.md` -- The text says those requests are answered within two working days. |
| 51 | There is no expedited path for requests to raise a cap. | 37 | carried | 'There is no expedited path and no exception list.' in `merged.md` -- The text rules out an expedited path for cap-increase requests. |
| 52 | There is no exception list for requests to raise a cap. | 37 | carried | 'There is no expedited path and no exception list.' in `merged.md` -- The text rules out an exception list for cap-increase requests. |

### `source_b.md` -- 61 claim(s): 0 dropped, 4 contradicted, 2 carried in part, 55 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 31 | The batch allowance is 50 times the default. | 23 | contradicted | 'The default allowance is 100 requests in a window, and a credential marked for batch work is allowed 1000 in the same window.' in `merged.md` -- The stated allowances make the batch allowance 10 times, not 50 times, the default. |
| 39 | The gateway refuses a request for three separate reasons. | 29 | contradicted | 'A cap is one reason for refusal. A credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit.' in `merged.md` -- The text lists four reasons for refusal, not three. |
| 40 | Only one of the gateway’s three reasons for refusing a request is a cap. | 29 | contradicted | 'A cap is one reason for refusal. A credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit.' in `merged.md` -- A cap is one of four listed reasons, not one of three. |
| 41 | Two of the gateway’s three reasons for refusing a request have nothing to do with how much traffic a caller has sent in the current window. | 29 | contradicted | 'Suspension, route closure and an oversized body are unrelated to traffic sent in the current window.' in `merged.md` -- The text identifies three traffic-independent reasons, in addition to a cap, rather than two of three. |
| 60 | An answer takes two working days. | 37 | carried in part | 'they are answered within two working days' in `merged.md` -- The text gives a two-working-day maximum, not an exact time of two working days. |
| 61 | Chasing an answer doesn’t make it take fewer than two working days. | 37 | carried in part | 'Chasing a request does not speed the answer.' in `merged.md` -- Chasing does not speed the answer, but the text does not establish two working days as a minimum. |
| 1 | Every credential has a cap of its own. | 3 | carried | 'Every credential has a cap.' in `merged.md` -- The text assigns a cap to every credential. |
| 2 | When a credential’s cap is spent, the gateway answers 429 at the edge. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge' in `merged.md` -- The text says a spent cap produces a 429 at the edge. |
| 3 | When a credential’s cap is spent, the gateway answers without troubling the service behind it. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge — without waking the service behind it' in `merged.md` -- The gateway answers without waking the service behind it. |
| 4 | Requests are counted against the credential rather than the connection. | 5 | carried | 'Requests are counted against the credential that presented them, over a fixed window of 60 seconds, and never against a connection.' in `merged.md` -- Counting is tied to the credential, not the connection. |
| 5 | Requests are counted over a fixed window of 60 seconds. | 5 | carried | 'Requests are counted against the credential that presented them, over a fixed window of 60 seconds' in `merged.md` -- The counting window is expressly fixed at 60 seconds. |
| 6 | The gateway doesn’t disclose the start of the fixed window of 60 seconds. | 5 | carried | 'Requests are counted against the credential that presented them, over a fixed window of 60 seconds, and never against a connection. The gateway does not disclose when the window starts.' in `merged.md` -- The text identifies the 60-second window and says its start is not disclosed. |
| 7 | Opening more sockets does not increase the credential’s allowance. | 5 | carried | 'Opening a second socket therefore buys a caller nothing.' in `merged.md` -- An additional socket does not improve the caller’s allowance. |
| 8 | The request count follows the credential across hosts. | 5 | carried | 'The count follows the credential across hosts.' in `merged.md` -- The text directly states that the count follows the credential across hosts. |
| 9 | A caller spread over many worker processes is throttled at the same point a single process would have been. | 5 | carried | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `merged.md` -- The eight-process example states that using multiple workers does not change the throttling point. |
| 10 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- The default allowance and its window are stated directly. |
| 11 | A caller that needs more than 100 requests in a window is almost always doing batch work under an interactive credential. | 7 | carried | 'The default allowance is 100 requests in a window, and a credential marked for batch work is allowed 1000 in the same window. The default allowance is enough for every interactive use of this API the platform team has seen; a caller that needs more is almost always doing batch work under an interactive credential.' in `merged.md` -- The text sets the default at 100 per window and describes callers needing more as almost always doing batch work under an interactive credential. |
| 12 | A refusal caused by the cap isn’t an outage. | 7 | carried | 'A refusal is not an outage, whatever the error class in a client library happens to call it.' in `merged.md` -- The text explicitly distinguishes a cap refusal from an outage. |
| 13 | A refusal caused by the cap isn’t a bug in the gateway. | 7 | carried | 'It is not a gateway bug.' in `merged.md` -- The text explicitly says the refusal is not a gateway bug. |
| 14 | The cap holds capacity for a request somebody else has already been promised. | 7 | carried | 'It is the platform declining to spend capacity that has already been promised to somebody else' in `merged.md` -- The text says the refusal preserves capacity already promised to somebody else. |
| 15 | Callers that retry immediately are most of the reason the cap is there. | 7 | carried | 'Callers that retry at once are the largest single reason the cap is there at all.' in `merged.md` -- Immediate retries are identified as the largest single reason for the cap. |
| 16 | The header is called Retry-After. | 11 | carried | 'The refusal carries a Retry-After header.' in `merged.md` -- The text names the header Retry-After. |
| 17 | The Retry-After header’s value is a whole number of seconds. | 11 | carried | 'The refusal carries a Retry-After header. Its value is a whole number of seconds to wait.' in `merged.md` -- The text gives the Retry-After value as a whole number of seconds. |
| 18 | The Retry-After header is present on every refusal the gateway sends. | 11 | carried | 'The refusal carries a Retry-After header. Its value is a whole number of seconds to wait. The header is present on every refusal the gateway sends.' in `merged.md` -- The text says the Retry-After header is present on every gateway refusal. |
| 19 | The gateway does not keep score of callers that wait longer than the Retry-After header asks. | 11 | carried | 'The gateway keeps no memory of who backed off politely, so waiting longer than the header asks earns a caller no credit at all.' in `merged.md` -- The gateway neither remembers polite backoff nor credits extra waiting. |
| 20 | The response body is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- The refusal body is expressly described as JSON. |
| 21 | The response body repeats the cap as a plain field. | 13 | carried | 'The body of the refusal is JSON, and it names what the gateway calls the “window” it counted in. It names the cap and the tier as well. Those values are plain fields.' in `merged.md` -- The text says the refusal body names the cap as a plain field. |
| 22 | The response body repeats the window as a plain field. | 13 | carried | 'The body of the refusal is JSON, and it names what the gateway calls the “window” it counted in. It names the cap and the tier as well. Those values are plain fields.' in `merged.md` -- The text says the refusal body names the window as a plain field. |
| 23 | The response body repeats the tier as a plain field. | 13 | carried | 'The body of the refusal is JSON, and it names what the gateway calls the “window” it counted in. It names the cap and the tier as well. Those values are plain fields.' in `merged.md` -- The text says the refusal body names the tier as a plain field. |
| 24 | The gateway computes the wait stated in the header. | 19 | carried | 'The gateway has already done that arithmetic' in `merged.md` -- The gateway calculates the wait given in the header. |
| 25 | The gateway computes the wait using information the caller cannot see. | 19 | carried | 'The gateway has already done that arithmetic, with information the caller does not have' in `merged.md` -- The gateway calculates the wait using information unavailable to the caller. |
| 26 | The cause of a 503 refusal differs from the cause of a cap refusal. | 19 | carried | 'On the 503 path, the platform itself is overloaded. The four cases are not interchangeable.' in `merged.md` -- A 503 indicates platform overload rather than a spent credential cap. |
| 27 | A 429 response needs the stated wait. | 21 | carried | 'a 429 wants the stated wait' in `merged.md` -- The text explicitly assigns the stated wait to a 429. |
| 28 | A 500 response can be retried once the stated wait has passed. | 21 | carried | 'a 500 may be retried once that wait has passed' in `merged.md` -- The text permits retrying a 500 after the wait. |
| 29 | A 503 response means the platform itself is overloaded. | 21 | carried | 'On the 503 path, the platform itself is overloaded.' in `merged.md` -- The text directly identifies platform overload as the 503 condition. |
| 30 | A batch credential is allowed 1000 requests in a window. | 23 | carried | 'A batch credential is allowed 1000 requests in the same window as the default tier' in `merged.md` -- The stated batch allowance is 1000 requests per window. |
| 32 | The batch tier does not use a separate counting scheme. | 23 | carried | 'it does not use a separate counting scheme' in `merged.md` -- The text explicitly rules out a separate batch counting scheme. |
| 33 | The window is identical for the batch tier and the interactive case. | 23 | carried | 'The window, the header and the body are identical to the interactive case' in `merged.md` -- The window is expressly included among the identical features. |
| 34 | The header is identical for the batch tier and the interactive case. | 23 | carried | 'The window, the header and the body are identical to the interactive case' in `merged.md` -- The header is expressly included among the identical features. |
| 35 | The body is identical for the batch tier and the interactive case. | 23 | carried | 'The window, the header and the body are identical to the interactive case' in `merged.md` -- The body is expressly included among the identical features. |
| 36 | A client written for one tier needs no change to run against the other. | 23 | carried | 'a client written for one tier needs no change at all to run against the other' in `merged.md` -- The text directly states that no client change is needed. |
| 37 | Nothing else about the batch tier differs from the default. | 23 | carried | 'Nothing else about the two tiers differs in any way.' in `merged.md` -- The text explicitly says there are no other differences between the tiers. |
| 38 | The platform team won’t assemble a caller’s case for a larger cap on the caller’s behalf. | 25 | carried | 'nobody at the far end will assemble that argument on its behalf' in `merged.md` -- The caller must assemble its own argument for a larger cap. |
| 42 | A credential can be suspended. | 29 | carried | 'A credential may be suspended' in `merged.md` -- Credential suspension is explicitly stated. |
| 43 | A route can be closed while it is being repaired. | 29 | carried | 'A route may also be closed while it is being repaired' in `merged.md` -- The text explicitly describes route closure during repair. |
| 44 | A request body over the 5 megabyte limit is refused. | 29 | carried | 'a body may exceed the 5 megabyte limit' in `merged.md` -- The text lists exceeding the body-size limit as a reason for refusal. |
| 45 | A request body over the 5 megabyte limit is refused before it has been read at all. | 29 | carried | 'an oversized body is refused before it has been read at all' in `merged.md` -- The oversized body refers to one exceeding the stated 5 megabyte limit. |
| 46 | A loop retrying against a suspended credential burns its whole budget. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `merged.md` -- The loop is stated to spend its entire budget. |
| 47 | A loop retrying against a suspended credential reaches nothing. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `merged.md` -- The retries never reach the service. |
| 48 | The log after retrying against a suspended credential shows a long run of refusals. | 31 | carried | 'the log afterwards shows nothing at all except a long run of refusals' in `merged.md` -- The text describes the log following retries against a suspended credential. |
| 49 | The log after retrying against a suspended credential shows no successes at all. | 31 | carried | 'the log afterwards shows nothing at all except a long run of refusals' in `merged.md` -- A log containing only refusals shows no successes. |
| 50 | A caller that can move half its work to a quieter hour usually finds it doesn’t need a larger cap. | 33 | carried | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `merged.md` -- The caller usually meets its needs without a larger cap. |
| 51 | A cap can be raised. | 33 | carried | 'A cap can be raised' in `merged.md` -- The text explicitly says a cap can be raised. |
| 52 | A cap cannot be raised solely on the strength of an assertion that the current cap is too small. | 33 | carried | 'the number of caps raised without a measurement behind them is 0' in `merged.md` -- An assertion without a measurement is insufficient to obtain an increase. |
| 53 | A request for a larger cap requires refusal counts for a full week. | 33 | carried | 'Bring a week of refusal counts' in `merged.md` -- The text requires a week of refusal counts when seeking an increase. |
| 54 | A request for a larger cap requires the shape of the traffic across the day. | 33 | carried | 'Bring a week of refusal counts, the shape of the traffic across the day, and the deadline that traffic is serving.' in `merged.md` -- The required information includes the traffic’s shape across the day. |
| 55 | A request for a larger cap requires the deadline the traffic exists to meet. | 33 | carried | 'Bring a week of refusal counts, the shape of the traffic across the day, and the deadline that traffic is serving.' in `merged.md` -- The required information includes the deadline the traffic serves. |
| 56 | The team wants to know whether the load is smooth or bursty before it looks at the number. | 35 | carried | 'The platform team looks at whether the load is smooth or bursty before considering a higher cap' in `merged.md` -- The team checks the load pattern before considering a higher cap. |
| 57 | A burst is cheaper to smooth out than to serve at its peak. | 35 | carried | 'a burst is cheaper to smooth than it is to serve at its peak' in `merged.md` -- The text makes the same cost comparison. |
| 58 | Requests go to the platform team through the usual channel. | 35 | carried | 'Requests reach the platform team through the usual channel' in `merged.md` -- The text states where requests go and how they reach the team. |
| 59 | There is no expedited path. | 37 | carried | 'There is no expedited path' in `merged.md` -- The text explicitly rules out an expedited path. |

### `merged.md` -- 70 claim(s): 0 invented, 0 contradicted, 0 supported in part, 70 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Every credential has a cap. | supported | `source_a.md` | 'Every credential has a cap.' in `source_a.md` -- The source states the claim directly. |
| 2 | When a credential’s cap is spent, the gateway answers 429 at the edge. | supported | `source_a.md` | 'When that cap is spent the gateway answers 429 at the edge' in `source_a.md` -- The source states what happens when the cap is spent. |
| 3 | When a credential’s cap is spent, the gateway answers 429 without waking the service behind it. | supported | `source_a.md` | 'When that cap is spent the gateway answers 429 at the edge — without waking the service behind it' in `source_a.md` -- The source states both the response and that the service is not woken. |
| 4 | Requests are counted against the credential that presented them. | supported | `source_a.md` | 'Requests are counted against the credential that presented them' in `source_a.md` -- The source states the counting basis directly. |
| 5 | Requests are counted over a fixed window of 60 seconds. | supported | `source_a.md` | 'over a fixed window of 60 seconds' in `source_a.md` -- The source gives the window type and duration. |
| 6 | Requests are never counted against a connection. | supported | `source_a.md` | 'Requests are counted against the credential that presented them, over a fixed window of 60 seconds, and never against a connection.' in `source_a.md` -- The source explicitly excludes counting against a connection. |
| 7 | The gateway does not disclose when the window starts. | supported | `source_b.md` | 'over a fixed window of 60 seconds whose start the gateway doesn’t disclose.' in `source_b.md` -- The source says the gateway does not disclose the window’s start. |
| 8 | The count follows the credential across hosts. | supported | `source_b.md` | 'The count follows the credential wherever the caller happens to put it, including across hosts.' in `source_b.md` -- The source explicitly says the count follows the credential across hosts. |
| 9 | Opening a second socket does not change the count against a credential. | supported | `source_a.md` | 'Requests are counted against the credential that presented them, over a fixed window of 60 seconds, and never against a connection. Opening a second socket therefore buys a caller nothing.' in `source_a.md` -- Counting by credential rather than connection means a second socket does not change that count. |
| 10 | A client spread across eight worker processes is throttled at exactly the point one process would have been. | supported | `source_a.md` | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `source_a.md` -- The source states the comparison directly. |
| 11 | A client spread across eight worker processes uses extra file descriptors. | supported | `source_a.md` | 'A client spread across eight worker processes is throttled at exactly the point one process would have been — and pays for the extra file descriptors as well.' in `source_a.md` -- The source says the eight-process client pays for extra file descriptors. |
| 12 | The default allowance is 100 requests in a window. | supported | `source_a.md` | 'The default allowance is 100 requests in a window' in `source_a.md` -- The source gives the default allowance directly. |
| 13 | A credential marked for batch work is allowed 1000 in the same window. | supported | `source_a.md` | 'a credential marked for batch work is allowed 1000 in the same window.' in `source_a.md` -- The source gives the batch allowance and says it uses the same window. |
| 14 | The default allowance is enough for every interactive use of this API the platform team has seen. | supported | `source_b.md` | 'which is enough for every interactive use of this API the platform team has seen' in `source_b.md` -- The source characterizes the default allowance as sufficient for those interactive uses. |
| 15 | A caller that needs more than the default allowance is almost always doing batch work under an interactive credential. | supported | `source_b.md` | 'a caller that needs more than that is almost always doing batch work under an interactive credential.' in `source_b.md` -- In context, “that” refers to the default allowance. |
| 16 | A refusal is not an outage. | supported | `source_a.md` | 'A refusal is not an outage' in `source_a.md` -- The source states the claim directly. |
| 17 | A refusal is not a gateway bug. | supported | `source_b.md` | 'The refusal isn’t an outage and it isn’t a bug in the gateway' in `source_b.md` -- The source explicitly says the refusal is not a gateway bug. |
| 18 | Capacity declined by the platform after a cap is spent has already been promised to somebody else. | supported | `source_a.md` | 'It is the platform declining to spend capacity that has already been promised to somebody else' in `source_a.md` -- In context, “It” is the refusal after the cap is spent. |
| 19 | Callers that retry at once are the largest single reason the cap exists. | supported | `source_a.md` | 'Callers that retry at once are the largest single reason the cap is there at all.' in `source_a.md` -- The source states the claim directly. |
| 20 | A refusal carries a Retry-After header. | supported | `source_a.md` | 'The refusal carries a Retry-After header.' in `source_a.md` -- The source states the claim directly. |
| 21 | The Retry-After header’s value is a whole number of seconds to wait. | supported | `source_a.md` | 'The refusal carries a Retry-After header. Its value is a whole number of seconds to wait.' in `source_a.md` -- The source identifies the header and specifies its value. |
| 22 | The Retry-After header is present on every refusal the gateway sends. | supported | `source_b.md` | 'The header is called Retry-After. Its value is a whole number of seconds, and it is present on every refusal the gateway sends.' in `source_b.md` -- The source explicitly says Retry-After is present on every refusal. |
| 23 | The gateway keeps no memory of who backed off politely. | supported | `source_a.md` | 'The gateway keeps no memory of who backed off politely' in `source_a.md` -- The source states the claim directly. |
| 24 | Waiting longer than the Retry-After header asks earns a caller no credit. | supported | `source_a.md` | 'waiting longer than the header asks earns a caller no credit at all.' in `source_a.md` -- In context, the header is Retry-After. |
| 25 | The body of a refusal is JSON. | supported | `source_a.md` | 'The body of the refusal is JSON' in `source_a.md` -- The source states the claim directly. |
| 26 | The body of a refusal names what the gateway calls the “window” it counted in. | supported | `source_a.md` | 'The body of the refusal is JSON, and it names what the gateway calls the “window” it counted in.' in `source_a.md` -- The source states that the refusal body names the counted window. |
| 27 | The body of a refusal names the cap. | supported | `source_a.md` | 'It names the cap and the tier as well.' in `source_a.md` -- The source states that the body names the cap. |
| 28 | The body of a refusal names the tier. | supported | `source_a.md` | 'It names the cap and the tier as well.' in `source_a.md` -- The source states that the body names the tier. |
| 29 | The window, cap and tier values in the refusal body are plain fields. | supported | `source_b.md` | 'The response body is JSON and it repeats the cap, the window and the tier as plain fields.' in `source_b.md` -- The source identifies all three values as plain fields in the response body. |
| 30 | The gateway calculates the wait given in the Retry-After header. | supported | `source_a.md` | 'The gateway has already done that arithmetic, with information the caller does not have, and it does the same on the 503 path.' in `source_a.md` -- In the rule to honour the header, the source says the gateway has calculated the wait. |
| 31 | The gateway calculates the wait using information the caller does not have. | supported | `source_a.md` | 'The gateway has already done that arithmetic, with information the caller does not have, and it does the same on the 503 path.' in `source_a.md` -- The source explicitly says the gateway uses information the caller does not have. |
| 32 | The gateway calculates a wait on the 503 path. | supported | `source_a.md` | 'The gateway has already done that arithmetic, with information the caller does not have, and it does the same on the 503 path.' in `source_a.md` -- The source says the gateway does the same wait arithmetic on the 503 path. |
| 33 | A caller cannot see the gateway’s counter. | supported | `source_a.md` | 'A wait derived on the client side is a guess about a counter it cannot see.' in `source_a.md` -- The source says the client cannot see the counter. |
| 34 | A 500 may be retried once the stated wait has passed. | supported | `source_a.md` | 'a 500 may be retried once that wait has passed' in `source_a.md` -- The source gives this retry condition for a 500. |
| 35 | A 503 is the overload path. | supported | `source_a.md` | 'a 503 is the overload path' in `source_a.md` -- The source directly identifies 503 as the overload path. |
| 36 | On the 503 path, the platform itself is overloaded. | supported | `source_b.md` | 'a 503 means the platform itself is overloaded.' in `source_b.md` -- The source directly associates a 503 with platform overload. |
| 37 | A client that folds every non-success into one branch will retry hardest during the incident the cap was installed to survive. | supported | `source_a.md` | 'A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive.' in `source_a.md` -- The source states the claimed consequence of combining non-success responses. |
| 38 | A batch credential is allowed 1000 requests in the same window as the default tier. | supported | `source_a.md` | 'The default allowance is 100 requests in a window, and a credential marked for batch work is allowed 1000 in the same window.' in `source_a.md` -- The source states the batch allowance and that it uses the same window. |
| 39 | A batch credential does not use a separate counting scheme. | supported | `source_b.md` | 'A batch credential is allowed 1000 requests in a window, which is 50 times the default and not a separate counting scheme.' in `source_b.md` -- The source explicitly rules out a separate counting scheme. |
| 40 | The tier is set on the credential when it is issued. | supported | `source_a.md` | 'The tier is set on the credential when it is issued and cannot be asked for per call.' in `source_a.md` -- The source states when the credential’s tier is set. |
| 41 | The tier cannot be asked for per call. | supported | `source_a.md` | 'The tier is set on the credential when it is issued and cannot be asked for per call.' in `source_a.md` -- The source explicitly says the tier cannot be asked for per call. |
| 42 | The window is identical for the batch and interactive tiers. | supported | `source_b.md` | 'The window, the header and the body are identical to the interactive case' in `source_b.md` -- The source says the batch window is identical to the interactive window. |
| 43 | The header is identical for the batch and interactive tiers. | supported | `source_b.md` | 'The window, the header and the body are identical to the interactive case' in `source_b.md` -- The source says the batch header is identical to the interactive header. |
| 44 | The body is identical for the batch and interactive tiers. | supported | `source_b.md` | 'The window, the header and the body are identical to the interactive case' in `source_b.md` -- The source says the batch body is identical to the interactive body. |
| 45 | A client written for one tier needs no change to run against the other tier. | supported | `source_b.md` | 'a client written for one tier needs no change at all to run against the other.' in `source_b.md` -- The source directly states that a client needs no change between tiers. |
| 46 | Nothing else about the batch and interactive tiers differs. | supported | `source_a.md` | 'Nothing else about the two tiers differs in any way.' in `source_a.md` -- The source explicitly says nothing else differs between the tiers. |
| 47 | A credential may be suspended. | supported | `source_a.md` | 'A credential may be suspended' in `source_a.md` -- The source states that a credential may be suspended. |
| 48 | A route may be closed for maintenance. | supported | `source_a.md` | 'a route may be closed for maintenance' in `source_a.md` -- The source states that a route may be closed for maintenance. |
| 49 | The body limit is 5 megabyte. | supported | `source_a.md` | 'a body may exceed the 5 megabyte limit.' in `source_a.md` -- The source gives the body limit as 5 megabyte. |
| 50 | A route may be closed while it is being repaired. | supported | `source_b.md` | 'a route can be closed while it is being repaired' in `source_b.md` -- The source states that a route can be closed during repair. |
| 51 | An oversized body is refused before it has been read at all. | supported | `source_b.md` | 'a request body over the 5 megabyte limit is refused before it has been read at all' in `source_b.md` -- The source states when an oversized body is refused. |
| 52 | Suspension is unrelated to traffic sent in the current window. | supported | `source_b.md` | 'The gateway refuses a request for three separate reasons, and only one of them is a cap. Two of the three have nothing to do with how much traffic a caller has sent in the window it is currently in. A credential can be suspended, a route can be closed while it is being repaired, and a request body over the 5 megabyte limit is refused before it has been read at all.' in `source_b.md` -- Suspension is described as a separate refusal reason, rather than a refusal for exceeding the current window's cap. |
| 53 | Route closure is unrelated to traffic sent in the current window. | supported | `source_b.md` | 'The gateway refuses a request for three separate reasons, and only one of them is a cap. Two of the three have nothing to do with how much traffic a caller has sent in the window it is currently in. A credential can be suspended, a route can be closed while it is being repaired, and a request body over the 5 megabyte limit is refused before it has been read at all.' in `source_b.md` -- The source describes route closure for repairs as a refusal reason distinct from the traffic cap. |
| 54 | An oversized body is unrelated to traffic sent in the current window. | supported | `source_b.md` | 'The gateway refuses a request for three separate reasons, and only one of them is a cap. Two of the three have nothing to do with how much traffic a caller has sent in the window it is currently in. A credential can be suspended, a route can be closed while it is being repaired, and a request body over the 5 megabyte limit is refused before it has been read at all.' in `source_b.md` -- The body-size limit concerns the size of a request, not the amount of traffic sent in the current window. |
| 55 | Suspension does not clear itself by waiting for a stated number of seconds. | supported | `source_a.md` | 'A credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit. None of those three clears itself by waiting for a stated number of seconds.' in `source_a.md` -- The source expressly includes suspension among refusals that do not clear after the stated wait. |
| 56 | Route closure does not clear itself by waiting for a stated number of seconds. | supported | `source_a.md` | 'A credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit. None of those three clears itself by waiting for a stated number of seconds.' in `source_a.md` -- The source expressly includes route closure among refusals that do not clear after the stated wait. |
| 57 | An oversized-body refusal does not clear itself by waiting for a stated number of seconds. | supported | `source_a.md` | 'A credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit. None of those three clears itself by waiting for a stated number of seconds.' in `source_a.md` -- The source expressly includes an oversized body among refusals that do not clear after the stated wait. |
| 58 | A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service. | supported | `source_a.md` | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `source_a.md` -- The source states the claim directly. |
| 59 | The log from a loop that waits and retries against a suspended credential shows nothing except a long run of refusals. | supported | `source_a.md` | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service — and the log afterwards shows nothing at all except a long run of refusals.' in `source_a.md` -- The source states what that loop's log shows. |
| 60 | A cap can be raised. | supported | `source_a.md` | 'A cap can be raised' in `source_a.md` -- The source states the claim directly. |
| 61 | The number of caps raised without a measurement behind them is 0. | supported | `source_a.md` | 'the number of caps raised without a measurement behind them is 0' in `source_a.md` -- The source gives the claimed number. |
| 62 | The platform team looks at whether the load is smooth or bursty before considering a higher cap. | supported | `source_b.md` | 'The team wants to know whether the load is smooth or bursty before it looks at the number at all.' in `source_b.md` -- The source says the team considers the traffic shape before the cap number. |
| 63 | A burst is cheaper to smooth than it is to serve at its peak. | supported | `source_b.md` | 'A burst is cheaper to smooth out than it is to serve at its peak.' in `source_b.md` -- The source states the same comparison. |
| 64 | A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap. | supported | `source_a.md` | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `source_a.md` -- The source states the claimed usual outcome. |
| 65 | Moving work to a quieter hour is available to almost everybody. | supported | `source_b.md` | 'A caller that can move half its work to a quieter hour usually finds it doesn’t need a larger cap in the first place. That is the cheapest fix available to anybody, and it is available to almost everybody.' in `source_b.md` -- The source says this fix is available to almost everybody. |
| 66 | Requests reach the platform team through the usual channel. | supported | `source_a.md` | 'Requests reach the platform team through the usual channel' in `source_a.md` -- The source states the claim directly. |
| 67 | Requests to the platform team are answered within two working days. | supported | `source_a.md` | 'Requests reach the platform team through the usual channel, and they are answered within two working days.' in `source_a.md` -- The source gives the claimed response time. |
| 68 | Chasing a request does not speed the answer. | supported | `source_b.md` | 'An answer takes two working days, and chasing it doesn’t make it take fewer.' in `source_b.md` -- The source states that chasing does not shorten the wait. |
| 69 | There is no expedited path. | supported | `source_b.md` | 'There is no expedited path.' in `source_b.md` -- The source states the claim directly. |
| 70 | There is no exception list. | supported | `source_a.md` | 'There is no expedited path and no exception list.' in `source_a.md` -- The source expressly says there is no exception list. |

## Structure

**9** mechanical check(s) over **104** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **70** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **113**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 17 run(s) over 57 attributed segment(s) — sources interleaved. 6 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Unresolved replacement — a record points at text the merge does not contain

- `b24` — segment b24 is declared 'subsumed' with replacement 'The gateway has already done that arithmetic, with information the caller does not have, and it does the same on the 503 path. On the 503 path, the platform itself is overloaded.', which is not in the merged document

  ```text
  In the merge: The gateway has already done that arithmetic, with information the caller does not have, and it does the same on the 503 path. On the 503 path, the platform itself is overloaded.
  ```

### Verbatim violation — an invariant-core token did not survive unchanged

- `b31` (`source_b.md`) — numeric '50' (times) does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **66** departure(s) from its sources. Checking them confirms 43, rejects 13, and leaves 10 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 104 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a5` | reworded | Socket advice was made direct. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-007`) |
| `a23` | reworded | List indentation was removed. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-022`, `A-023`, `A-024`) |
| `a24` | reworded | List indentation was removed. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-025`) |
| `a25` | reworded | List indentation was removed. | **rejected** | declared 'reworded', and its text is in the merge (no claim traced to it) |
| `a27` | reworded | List indentation was removed. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-026`, `A-027`, `A-028`) |
| `a28` | reworded | List indentation was removed. | **rejected** | declared 'reworded', and its text is in the merge (no claim traced to it) |
| `a29` | reworded | List indentation was removed. | **rejected** | declared 'reworded', and its text is in the merge (no claim traced to it) |
| `a30` | reworded | List indentation was removed. | **rejected** | declared 'reworded', and its text is in the merge (no claim traced to it) |
| `a32` | superseded | Batch allowance uses the explicit cap, not the conflicting multiplier. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`A-029`, `A-030`) |
| `a33` | reworded | List indentation was removed. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-031`, `A-032`) |
| `a34` | reworded | List indentation was removed. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-033`) |
| `a36` | reworded | List indentation was removed. | **rejected** | declared 'reworded', and its text is in the merge (no claim traced to it) |
| `a37` | reworded | List indentation was removed. | **rejected** | declared 'reworded', and its text is in the merge (no claim traced to it) |
| `a40` | superseded | The enumerated refusals take precedence over the conflicting total. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`A-034`, `A-035`) |
| `a49` | reworded | Increase review also retains when the team considers the cap. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-046`, `A-047`) |
| `b1` | superseded | The base title was chosen. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Rate limiting and the 429 contract for gateway clients' and says so (no claim traced to it) |
| `b2` | duplicate | The base states the credential-level cap. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-001`) |
| `b3` | subsumed | The base carries the edge refusal and its effect. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-002`, `B-003`) |
| `b5` | subsumed | Counting retains the undisclosed window start. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-004`, `B-005`, `B-006`) |
| `b6` | duplicate | The socket advice appears once. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-007`) |
| `b7` | reworded | Cross-host counting was shortened. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-008`) |
| `b8` | subsumed | The base gives the process example and its additional cost. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-009`) |
| `b9` | reworded | Allowance and observed interactive use were kept together. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-010`, `B-011`) |
| `b10` | subsumed | The refusal explanation retains the gateway-bug distinction. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-012`, `B-013`, `B-014`) |
| `b11` | duplicate | The base states why immediate retries matter. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-015`) |
| `b12` | duplicate | The heading is identical. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b13` | duplicate | The header name appears once. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-016`) |
| `b14` | subsumed | The header description retains its stated presence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-017`, `B-018`) |
| `b15` | subsumed | The base states the complete client contract. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b16` | duplicate | The base gives the same no-credit rule. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-019`) |
| `b17` | subsumed | The body description includes the field format. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-020`, `B-021`, `B-022`, `B-023`) |
| `b18` | subsumed | The header rule retains the risk of client-side calculation. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b19` | duplicate | The base states the body's purpose. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b20` | superseded | The base retry heading was chosen. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b21` | duplicate | The base gives the same ordering. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b22` | subsumed | The first rule covers the header and client-side waits. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b23` | duplicate | The base explains why the gateway calculates the wait. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-024`, `B-025`) |
| `b24` | subsumed | The retry rules retain the separate 503 cause. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-026`) |
| `b25` | duplicate | The base calls a client-calculated wait a guess. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b26` | duplicate | The base rejects that guess. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b27` | subsumed | The second rule retains the distinction from non-success. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b28` | subsumed | The status-code rule retains the meaning of 503. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-027`, `B-028`, `B-029`) |
| `b29` | duplicate | The base states the shared-branch risk. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'duplicate' is what happened to it (no claim traced to it) |
| `b30` | duplicate | The base supplies the instruction. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b31` | superseded | The explicit batch cap replaces the conflicting multiplier. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-030`, `B-031`, `B-032`) |
| `b32` | reworded | List indentation was removed. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-033`, `B-034`, `B-035`, `B-036`) |
| `b33` | duplicate | The base states that the tiers otherwise match. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-037`) |
| `b34` | subsumed | The logging rule retains the minimum retention period. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b35` | duplicate | The base states who must provide the counts. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-038`) |
| `b36` | subsumed | The logging rule retains the role of counts in a request. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b37` | superseded | The base heading was chosen. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b38` | superseded | The enumerated refusals take precedence over the conflicting total. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-039`, `B-040`) |
| `b39` | superseded | The enumerated refusals replace the conflicting count. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-041`) |
| `b40` | subsumed | The refusal list retains repair and the unread-body detail. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-042`, `B-043`, `B-044`, `B-045`) |
| `b41` | duplicate | The base states why the distinction matters. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b42` | duplicate | The base gives the exhausted-budget result. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-046`, `B-047`) |
| `b43` | subsumed | The retry example retains the misleading log and caller's cost. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-048`, `B-049`) |
| `b44` | duplicate | The base gives the quieter-hour alternative. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-050`) |
| `b45` | reworded | The increase section keeps the fix's cost and availability. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b46` | subsumed | The base requires measurement for an increase. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-051`, `B-052`) |
| `b47` | duplicate | The base lists the same evidence. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-053`, `B-054`, `B-055`) |
| `b48` | subsumed | The review sentence retains when the team considers the cap. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-056`) |
| `b49` | duplicate | The burst-cost point appears in the review sentence. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-057`) |
| `b50` | duplicate | The base gives the same request channel. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-058`) |
| `b51` | duplicate | The base rules out an expedited path. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-059`) |
| `b52` | subsumed | The response timing retains the effect of chasing. | **rejected** | declared 'subsumed', which predicts SUPPORTED; B-060 came back PARTIAL, B-061 came back PARTIAL (`B-060`, `B-061`) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | bf7d5842201d (hosted) |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | gpt-6-sol |
| Model (decompose) | gpt-6-sol |
| Model (verify) | gpt-6-sol |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed 0, thinking decompose, merge, verify, profile openai-reasoning |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 12 live, 0 cached, 0 replayed |
| Tokens | 42,180 in, 33,420 out, 0 cached, 4,972 reasoning |
| Cost | ~$0.42 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 338.4s |
| Generated | 2026-09-27T15:51:51+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `bf7d5842201d`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
