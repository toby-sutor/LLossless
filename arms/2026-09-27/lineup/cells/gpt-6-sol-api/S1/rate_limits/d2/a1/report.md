## Verdict

**13 finding(s).** In the claims: 2 partially dropped, 7 contradicted. In the structure: 2 undeclared rewording, 1 unresolved replacement, 1 verbatim violation.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 60 |
| Claims extracted from `source_a.md` | 49 |
| Claims extracted from `source_b.md` | 65 |
| Forward — source claims accounted for in the merge | **105/114** |
| Forward — carried only in part | 2 |
| Forward — `source_a.md` claims accounted for | **46/49** |
| Forward — `source_b.md` claims accounted for | **59/65** (2 in part) |
| Reverse — merge claims found in a source | **60/60** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **174/174** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Partly dropped — the merge carries some of this claim

- **B-064** (`source_b.md:37`) — An answer takes two working days.
  - evidence: 'they are answered within two working days' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text gives two working days as an upper limit, not the exact time an answer takes.
- **B-065** (`source_b.md:37`) — Chasing an answer does not make it take fewer than two working days.
  - evidence: 'Chasing a request does not shorten the wait.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: Chasing does not shorten the wait, but the text does not establish a minimum wait of two working days.

### Contradicted — the merge states something different

- **A-027** -- the two documents disagree
  - `source_a.md:23` says: A batch credential is allowed fifty times the default allowance.
  - `merged.md` says: 'The default allowance is 100 requests in a window, and a credential marked for batch work is allowed 1000 in the same window.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The batch allowance is ten times, not fifty times, the default.
- **A-032** -- the two documents disagree
  - `source_a.md:29` says: The gateway refuses a request for three reasons.
  - `merged.md` says: 'Besides an exhausted cap, a credential may be suspended, a route may be closed for maintenance or repair, or a body may exceed the 5 megabyte limit.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text lists four reasons, including an exhausted cap, rather than three.
- **A-033** -- the two documents disagree
  - `source_a.md:29` says: Only one of the gateway's three reasons for refusing a request is a cap.
  - `merged.md` says: 'Besides an exhausted cap, a credential may be suspended, a route may be closed for maintenance or repair, or a body may exceed the 5 megabyte limit.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Although only one listed reason is a cap, the text lists four reasons, not three.
- **B-035** -- the two documents disagree
  - `source_b.md:23` says: The batch credential allowance is 50 times the default.
  - `merged.md` says: 'The default allowance is 100 requests in a window, and a credential marked for batch work is allowed 1000 in the same window.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The stated allowances make the batch tier 10 times the default, not 50 times.
- **B-043** -- the two documents disagree
  - `source_b.md:29` says: The gateway refuses a request for three separate reasons.
  - `merged.md` says: 'Besides an exhausted cap, a credential may be suspended, a route may be closed for maintenance or repair, or a body may exceed the 5 megabyte limit.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text lists four reasons for refusal, not three.
- **B-044** -- the two documents disagree
  - `source_b.md:29` says: Only one of the gateway's three reasons for refusing a request is a cap.
  - `merged.md` says: 'Besides an exhausted cap, a credential may be suspended, a route may be closed for maintenance or repair, or a body may exceed the 5 megabyte limit.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Although one listed reason is a cap, the text lists four reasons rather than three.
- **B-045** -- the two documents disagree
  - `source_b.md:29` says: Two of the gateway's three reasons for refusing a request have nothing to do with how much traffic a caller has sent in its current window.
  - `merged.md` says: 'Besides an exhausted cap, a credential may be suspended, a route may be closed for maintenance or repair, or a body may exceed the 5 megabyte limit.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The claim presumes three refusal reasons, but the text lists four.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 49 claim(s): 0 dropped, 3 contradicted, 0 carried in part, 46 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 27 | A batch credential is allowed fifty times the default allowance. | 23 | contradicted | 'The default allowance is 100 requests in a window, and a credential marked for batch work is allowed 1000 in the same window.' in `merged.md` -- The batch allowance is ten times, not fifty times, the default. |
| 32 | The gateway refuses a request for three reasons. | 29 | contradicted | 'Besides an exhausted cap, a credential may be suspended, a route may be closed for maintenance or repair, or a body may exceed the 5 megabyte limit.' in `merged.md` -- The text lists four reasons, including an exhausted cap, rather than three. |
| 33 | Only one of the gateway's three reasons for refusing a request is a cap. | 29 | contradicted | 'Besides an exhausted cap, a credential may be suspended, a route may be closed for maintenance or repair, or a body may exceed the 5 megabyte limit.' in `merged.md` -- Although only one listed reason is a cap, the text lists four reasons, not three. |
| 1 | Every credential has a cap. | 3 | carried | 'Every credential has a cap.' in `merged.md` -- The text states the claim directly. |
| 2 | When a credential's cap is spent, the gateway answers 429 at the edge. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge' in `merged.md` -- The text states where and how the gateway responds to a spent cap. |
| 3 | When a credential's cap is spent, the gateway answers 429 without waking the service behind it. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge — without waking the service behind it' in `merged.md` -- The text states that the 429 response does not wake the service. |
| 4 | Requests are counted against the credential that presented them. | 5 | carried | 'Requests are counted against the credential that presented them' in `merged.md` -- The text states the claim directly. |
| 5 | Requests are counted over a fixed window of 60 seconds. | 5 | carried | 'over a fixed window of 60 seconds' in `merged.md` -- The text specifies the fixed counting window. |
| 6 | Requests are never counted against a connection. | 5 | carried | 'and never against a connection.' in `merged.md` -- The text explicitly excludes counting against a connection. |
| 7 | Opening a second socket does not increase a caller's allowance. | 5 | carried | 'Opening a second socket therefore buys a caller nothing.' in `merged.md` -- A second socket provides no additional allowance. |
| 8 | A client spread across eight worker processes is throttled at exactly the point one process would have been. | 5 | carried | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `merged.md` -- The text states the comparison directly. |
| 9 | A client spread across eight worker processes uses extra file descriptors. | 5 | carried | 'A client spread across eight worker processes is throttled at exactly the point one process would have been — and pays for the extra file descriptors as well.' in `merged.md` -- The text says the eight-process client pays for extra file descriptors. |
| 10 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- The text states the default allowance directly. |
| 11 | A credential marked for batch work is allowed 1000 in the same window. | 7 | carried | 'a credential marked for batch work is allowed 1000 in the same window' in `merged.md` -- The text states the batch allowance and its window. |
| 12 | A refusal is not an outage. | 7 | carried | 'A refusal is not an outage' in `merged.md` -- The text states the claim directly. |
| 13 | Callers that retry at once are the largest single reason the cap exists. | 7 | carried | 'Callers that retry at once are the largest single reason the cap is there at all.' in `merged.md` -- The text identifies immediate retries as the largest single reason for the cap. |
| 14 | A refusal carries a Retry-After header. | 11 | carried | 'The refusal carries a Retry-After header.' in `merged.md` -- The text states the claim directly. |
| 15 | The Retry-After header's value is a whole number of seconds to wait. | 11 | carried | 'Its value is a whole number of seconds to wait.' in `merged.md` -- The preceding sentence identifies the header, and this sentence specifies its value. |
| 16 | The gateway keeps no memory of who backed off politely. | 11 | carried | 'The gateway keeps no memory of who backed off politely' in `merged.md` -- The text states the claim directly. |
| 17 | Waiting longer than the Retry-After header asks earns a caller no credit. | 11 | carried | 'waiting longer than the header asks earns a caller no credit at all.' in `merged.md` -- The text says extra waiting earns no credit. |
| 18 | The body of a refusal is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- The text states the body format directly. |
| 19 | The body of a refusal names what the gateway calls the “window” it counted in. | 13 | carried | 'The body of the refusal is JSON, and it names what the gateway calls the “window” it counted in.' in `merged.md` -- The text says the refusal body names the counted window. |
| 20 | The body of a refusal names the cap. | 13 | carried | 'It names the cap and the tier as well.' in `merged.md` -- In context, “It” is the refusal body, which names the cap. |
| 21 | The body of a refusal names the tier. | 13 | carried | 'It names the cap and the tier as well.' in `merged.md` -- In context, “It” is the refusal body, which names the tier. |
| 22 | The gateway calculates the wait stated in the header using information the caller does not have. | 19 | carried | 'Honour the header, every time. The gateway has already done that arithmetic, with information the caller does not have' in `merged.md` -- The text says the gateway performs the header calculation using unavailable information. |
| 23 | The gateway calculates the wait stated in the header on the 503 path. | 19 | carried | 'The gateway has already done that arithmetic, with information the caller does not have, and it does the same on the 503 path' in `merged.md` -- The text says the gateway performs the same calculation on the 503 path. |
| 24 | A 429 calls for the stated wait. | 21 | carried | 'a 429 wants the stated wait' in `merged.md` -- The text directly prescribes the stated wait for a 429. |
| 25 | A 500 may be retried once the stated wait has passed. | 21 | carried | 'a 500 may be retried once that wait has passed' in `merged.md` -- The text states when a 500 may be retried. |
| 26 | A 503 is the overload path. | 21 | carried | 'a 503 is the overload path: the platform itself is overloaded' in `merged.md` -- The text identifies 503 as the overload path. |
| 28 | A batch credential is measured over exactly the same window as the default allowance. | 23 | carried | 'A batch credential is allowed 1000 requests in the same window as a default credential.' in `merged.md` -- The text explicitly says both credentials use the same window. |
| 29 | The tier is set on the credential when it is issued. | 23 | carried | 'The tier is set on the credential when it is issued' in `merged.md` -- The text states when the tier is set. |
| 30 | The tier cannot be asked for per call. | 23 | carried | 'cannot be asked for per call' in `merged.md` -- The text rules out asking for the tier per call. |
| 31 | Nothing else about the two tiers differs in any way. | 23 | carried | 'Nothing else about the two tiers differs in any way.' in `merged.md` -- The text states the claim directly. |
| 34 | The gateway may refuse a request because a credential is suspended. | 29 | carried | 'a credential may be suspended' in `merged.md` -- Suspension is listed as a reason for refusal. |
| 35 | The gateway may refuse a request because a route is closed for maintenance. | 29 | carried | 'a route may be closed for maintenance or repair' in `merged.md` -- A route closed for maintenance is listed as a reason for refusal. |
| 36 | The gateway may refuse a request because a body exceeds the 5 megabyte limit. | 29 | carried | 'a body may exceed the 5 megabyte limit' in `merged.md` -- Exceeding the stated body limit is listed as a reason for refusal. |
| 37 | Waiting for a stated number of seconds does not clear a refusal caused by a suspended credential. | 29 | carried | 'Suspension and route closure do not depend on traffic sent in the current window. None of those three clears itself by waiting for a stated number of seconds.' in `merged.md` -- Suspension is one of the three non-cap reasons that waiting does not clear. |
| 38 | Waiting for a stated number of seconds does not clear a refusal caused by a route closed for maintenance. | 29 | carried | 'Suspension and route closure do not depend on traffic sent in the current window. None of those three clears itself by waiting for a stated number of seconds.' in `merged.md` -- Route closure is one of the three non-cap reasons that waiting does not clear. |
| 39 | Waiting for a stated number of seconds does not clear a refusal caused by a body exceeding the 5 megabyte limit. | 29 | carried | 'Besides an exhausted cap, a credential may be suspended, a route may be closed for maintenance or repair, or a body may exceed the 5 megabyte limit. An oversized request body is refused before it has been read at all. Suspension and route closure do not depend on traffic sent in the current window. None of those three clears itself by waiting for a stated number of seconds.' in `merged.md` -- An oversized body is one of the three non-cap reasons that waiting does not clear. |
| 40 | A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `merged.md` -- The text states this outcome directly. |
| 41 | The log for a loop that waits and retries against a suspended credential shows nothing except a long run of refusals. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service — and the log afterwards shows nothing at all except a long run of refusals.' in `merged.md` -- The sentence describes the log produced by that loop. |
| 42 | A cap can be raised. | 35 | carried | 'A cap can be raised' in `merged.md` -- The text states the claim directly. |
| 43 | The number of caps raised without a measurement behind them is 0. | 35 | carried | 'the number of caps raised without a measurement behind them is 0' in `merged.md` -- The text gives the number as 0. |
| 44 | The platform team looks at whether the load is smooth or bursty. | 35 | carried | 'The platform team looks at whether the load is smooth or bursty' in `merged.md` -- The text states what the platform team examines. |
| 45 | A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap. | 35 | carried | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `merged.md` -- The text states this outcome directly. |
| 46 | Requests to raise a cap reach the platform team through the usual channel. | 37 | carried | 'Requests reach the platform team through the usual channel' in `merged.md` -- In the section about asking for an increase, the text specifies the usual channel. |
| 47 | Requests to raise a cap are answered within two working days. | 37 | carried | 'Requests reach the platform team through the usual channel, and they are answered within two working days.' in `merged.md` -- The text gives a response time of two working days. |
| 48 | There is no expedited path for requests to raise a cap. | 37 | carried | 'There is no expedited path and no exception list.' in `merged.md` -- The text rules out an expedited path for these requests. |
| 49 | There is no exception list for requests to raise a cap. | 37 | carried | 'There is no expedited path and no exception list.' in `merged.md` -- The text rules out an exception list for these requests. |

### `source_b.md` -- 65 claim(s): 0 dropped, 4 contradicted, 2 carried in part, 59 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 35 | The batch credential allowance is 50 times the default. | 23 | contradicted | 'The default allowance is 100 requests in a window, and a credential marked for batch work is allowed 1000 in the same window.' in `merged.md` -- The stated allowances make the batch tier 10 times the default, not 50 times. |
| 43 | The gateway refuses a request for three separate reasons. | 29 | contradicted | 'Besides an exhausted cap, a credential may be suspended, a route may be closed for maintenance or repair, or a body may exceed the 5 megabyte limit.' in `merged.md` -- The text lists four reasons for refusal, not three. |
| 44 | Only one of the gateway's three reasons for refusing a request is a cap. | 29 | contradicted | 'Besides an exhausted cap, a credential may be suspended, a route may be closed for maintenance or repair, or a body may exceed the 5 megabyte limit.' in `merged.md` -- Although one listed reason is a cap, the text lists four reasons rather than three. |
| 45 | Two of the gateway's three reasons for refusing a request have nothing to do with how much traffic a caller has sent in its current window. | 29 | contradicted | 'Besides an exhausted cap, a credential may be suspended, a route may be closed for maintenance or repair, or a body may exceed the 5 megabyte limit.' in `merged.md` -- The claim presumes three refusal reasons, but the text lists four. |
| 64 | An answer takes two working days. | 37 | carried in part | 'they are answered within two working days' in `merged.md` -- The text gives two working days as an upper limit, not the exact time an answer takes. |
| 65 | Chasing an answer does not make it take fewer than two working days. | 37 | carried in part | 'Chasing a request does not shorten the wait.' in `merged.md` -- Chasing does not shorten the wait, but the text does not establish a minimum wait of two working days. |
| 1 | Every credential has a cap of its own. | 3 | carried | 'Every credential has a cap.' in `merged.md` -- The text assigns a cap to every credential. |
| 2 | When a credential's cap is spent, the gateway answers 429 at the edge. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge' in `merged.md` -- The text states that a spent cap produces a 429 at the edge. |
| 3 | When a credential's cap is spent, the gateway does not trouble the service behind it. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge — without waking the service behind it' in `merged.md` -- The gateway refuses the request without waking the service behind it. |
| 4 | Requests are counted against the credential rather than the connection. | 5 | carried | 'Requests are counted against the credential that presented them, over a fixed window of 60 seconds, and never against a connection.' in `merged.md` -- The text explicitly assigns the count to the credential, not the connection. |
| 5 | Requests are counted over a fixed window of 60 seconds. | 5 | carried | 'Requests are counted against the credential that presented them, over a fixed window of 60 seconds' in `merged.md` -- The counting window is explicitly fixed at 60 seconds. |
| 6 | The gateway does not disclose the start of the fixed window of 60 seconds. | 5 | carried | 'Requests are counted against the credential that presented them, over a fixed window of 60 seconds, and never against a connection. The gateway does not disclose when the window starts.' in `merged.md` -- The text identifies the 60-second window and says its start is not disclosed. |
| 7 | Opening more sockets does not increase a credential's allowance. | 5 | carried | 'Opening a second socket therefore buys a caller nothing.' in `merged.md` -- Another socket provides no additional allowance. |
| 8 | The request count follows the credential across hosts. | 5 | carried | 'The count follows the credential across hosts.' in `merged.md` -- The text states the claim directly. |
| 9 | A caller spread over many worker processes is throttled at the same point as a single process. | 5 | carried | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `merged.md` -- Eight worker processes are throttled at the same point as one. |
| 10 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- The default allowance is stated directly. |
| 11 | A caller that needs more than 100 requests in a window is almost always doing batch work under an interactive credential. | 7 | carried | 'The default allowance is 100 requests in a window, and a credential marked for batch work is allowed 1000 in the same window. The platform team has found 100 requests sufficient for every interactive use of this API it has seen; callers that need more are almost always doing batch work under an interactive credential.' in `merged.md` -- The text links needing more than the default 100 to batch work under an interactive credential. |
| 12 | A refusal caused by the cap is not an outage. | 7 | carried | 'A refusal is not an outage, whatever the error class in a client library happens to call it.' in `merged.md` -- In the discussion of cap refusals, the text says a refusal is not an outage. |
| 13 | A refusal caused by the cap is not a bug in the gateway. | 7 | carried | 'Nor is it a gateway bug.' in `merged.md` -- The text says the cap refusal is not a gateway bug. |
| 14 | A refusal caused by the cap holds capacity for a request somebody else has already been promised. | 7 | carried | 'It is the platform declining to spend capacity that has already been promised to somebody else' in `merged.md` -- The refusal preserves capacity already promised to someone else. |
| 15 | Callers that retry immediately are most of the reason the cap exists. | 7 | carried | 'Callers that retry at once are the largest single reason the cap is there at all.' in `merged.md` -- Immediate retries are identified as the largest single reason for the cap. |
| 16 | The header is called Retry-After. | 11 | carried | 'The refusal carries a Retry-After header.' in `merged.md` -- The text names the header Retry-After. |
| 17 | The Retry-After header's value is a whole number of seconds. | 11 | carried | 'The refusal carries a Retry-After header. Its value is a whole number of seconds to wait.' in `merged.md` -- The header's value is specified as a whole number of seconds. |
| 18 | The Retry-After header is present on every refusal the gateway sends. | 11 | carried | 'The header is present on every refusal the gateway sends.' in `merged.md` -- The text explicitly says the header appears on every gateway refusal. |
| 19 | The gateway's retry contract is to wait for the period in the Retry-After header before continuing. | 11 | carried | 'Waiting that long and then continuing is the whole of the contract' in `merged.md` -- The stated contract is to wait for the header's period and then continue. |
| 20 | The response body is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- The refusal body is explicitly described as JSON. |
| 21 | The response body repeats the cap as a plain field. | 13 | carried | 'It names the cap and the tier as well. These are plain fields.' in `merged.md` -- The body names the cap as a plain field. |
| 22 | The response body repeats the window as a plain field. | 13 | carried | 'The body of the refusal is JSON, and it names what the gateway calls the “window” it counted in. It names the cap and the tier as well. These are plain fields.' in `merged.md` -- The body names the counted window as a plain field. |
| 23 | The response body repeats the tier as a plain field. | 13 | carried | 'It names the cap and the tier as well. These are plain fields.' in `merged.md` -- The body names the tier as a plain field. |
| 24 | The response body's cap, window and tier fields are not substitutes for the Retry-After header. | 13 | carried | 'The body of the refusal is JSON, and it names what the gateway calls the “window” it counted in. It names the cap and the tier as well. These are plain fields. None of those fields is a substitute for the header' in `merged.md` -- The text identifies all three fields and says none substitutes for the header. |
| 25 | The response body is intended for a human reading the log afterwards. | 13 | carried | 'The body is there so that a human reading a log afterwards can see why the request was refused' in `merged.md` -- The body is explicitly intended to explain the refusal to a human reading a log. |
| 26 | The gateway computes the wait stated in the Retry-After header. | 19 | carried | 'Honour the header, every time. The gateway has already done that arithmetic, with information the caller does not have' in `merged.md` -- The text says the gateway has already calculated the wait conveyed by the header. |
| 27 | The gateway computes the wait using information the caller cannot see. | 19 | carried | 'The gateway has already done that arithmetic, with information the caller does not have' in `merged.md` -- The gateway calculates the wait using information unavailable to the caller. |
| 28 | The rule to honour the header and not compute a wait also applies on the 503 path. | 19 | carried | 'Honour the header, every time. The gateway has already done that arithmetic, with information the caller does not have, and it does the same on the 503 path, even though that refusal has a different cause. A wait derived on the client side is a guess about a counter it cannot see.' in `merged.md` -- The rule applies on the 503 path and rejects a client-computed wait. |
| 29 | A 503 refusal has a different cause from a cap refusal. | 19 | carried | 'it does the same on the 503 path, even though that refusal has a different cause' in `merged.md` -- The text explicitly distinguishes the cause of a 503 refusal. |
| 30 | A 200 needs nothing. | 21 | carried | 'A 200 wants nothing' in `merged.md` -- The text says a 200 requires no retry action. |
| 31 | A 429 needs the stated wait. | 21 | carried | 'a 429 wants the stated wait' in `merged.md` -- The text specifies the stated wait for a 429. |
| 32 | A 500 can be retried once the stated wait has passed. | 21 | carried | 'a 500 may be retried once that wait has passed' in `merged.md` -- The text permits retrying a 500 after the stated wait. |
| 33 | A 503 means the platform itself is overloaded. | 21 | carried | 'a 503 is the overload path: the platform itself is overloaded' in `merged.md` -- The text identifies platform overload as the meaning of a 503. |
| 34 | A batch credential is allowed 1000 requests in a window. | 23 | carried | 'A batch credential is allowed 1000 requests in the same window as a default credential.' in `merged.md` -- The batch allowance is stated as 1000 requests per window. |
| 36 | The batch tier does not use a separate counting scheme. | 23 | carried | 'The window, header and body are identical across tiers, so a client written for one tier needs no change to run against the other. Nothing else about the two tiers differs in any way.' in `merged.md` -- The text says the tiers share the window and have no other differences. |
| 37 | The window is identical for the batch and interactive tiers. | 23 | carried | 'The window, header and body are identical across tiers' in `merged.md` -- The window is explicitly described as identical across tiers. |
| 38 | The header is identical for the batch and interactive tiers. | 23 | carried | 'The window, header and body are identical across tiers' in `merged.md` -- The header is explicitly described as identical across tiers. |
| 39 | The body is identical for the batch and interactive tiers. | 23 | carried | 'The window, header and body are identical across tiers' in `merged.md` -- The body is explicitly described as identical across tiers. |
| 40 | A client written for one tier needs no change to run against the other tier. | 23 | carried | 'a client written for one tier needs no change to run against the other' in `merged.md` -- The text directly states that no client change is needed. |
| 41 | Nothing else about the batch tier differs from the default. | 23 | carried | 'Nothing else about the two tiers differs in any way.' in `merged.md` -- The text explicitly rules out other differences between the tiers. |
| 42 | The platform team will not assemble a caller's case for a larger cap on the caller's behalf. | 25 | carried | 'nobody at the far end will assemble that argument on its behalf' in `merged.md` -- The caller must assemble its own argument for a larger cap. |
| 46 | A credential can be suspended. | 29 | carried | 'a credential may be suspended' in `merged.md` -- The text states that a credential may be suspended. |
| 47 | A route can be closed while it is being repaired. | 29 | carried | 'a route may be closed for maintenance or repair' in `merged.md` -- The text includes repair as a reason a route may be closed. |
| 48 | A request body over the 5 megabyte limit is refused. | 29 | carried | 'An oversized request body is refused before it has been read at all.' in `merged.md` -- In context, an oversized body is one exceeding the stated 5 megabyte limit. |
| 49 | A request body over the 5 megabyte limit is refused before it has been read at all. | 29 | carried | 'or a body may exceed the 5 megabyte limit. An oversized request body is refused before it has been read at all.' in `merged.md` -- The text gives the size limit and says an oversized body is refused before being read. |
| 50 | A loop retrying against a suspended credential burns its whole budget. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `merged.md` -- The text directly says such a loop spends its whole budget. |
| 51 | A loop retrying against a suspended credential reaches nothing. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `merged.md` -- The loop never reaches the service. |
| 52 | The log after a loop retries against a suspended credential shows a long run of refusals. | 31 | carried | 'the log afterwards shows nothing at all except a long run of refusals' in `merged.md` -- The text describes the log after retries against a suspended credential. |
| 53 | The log after a loop retries against a suspended credential shows no successes at all. | 31 | carried | 'the log afterwards shows nothing at all except a long run of refusals' in `merged.md` -- A log containing nothing except refusals contains no successes. |
| 54 | A caller that can move half its work to a quieter hour usually does not need a larger cap. | 33 | carried | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `merged.md` -- Getting what it needs without a cap change means a larger cap is usually unnecessary. |
| 55 | A cap can be raised. | 33 | carried | 'A cap can be raised' in `merged.md` -- The text states this directly. |
| 56 | An assertion that the current cap is too small is not sufficient to have the cap raised. | 33 | carried | 'Without those counts, an assertion that the cap is too small is not enough.' in `merged.md` -- An assertion alone is insufficient. |
| 57 | A request for a larger cap requires refusal counts for a full week. | 33 | carried | 'Bring a week of refusal counts' in `merged.md` -- The text calls for a week of refusal counts when seeking an increase. |
| 58 | A request for a larger cap requires the shape of the traffic across the day. | 33 | carried | 'Bring a week of refusal counts, the shape of the traffic across the day, and the deadline that traffic is serving.' in `merged.md` -- The required information includes the traffic’s shape across the day. |
| 59 | A request for a larger cap requires the deadline the traffic exists to meet. | 33 | carried | 'Bring a week of refusal counts, the shape of the traffic across the day, and the deadline that traffic is serving.' in `merged.md` -- The required information includes the deadline the traffic serves. |
| 60 | The platform team wants to know whether the load is smooth or bursty before it looks at the number. | 35 | carried | 'The platform team looks at whether the load is smooth or bursty before it considers the cap itself' in `merged.md` -- The team assesses the load pattern before considering the cap. |
| 61 | A burst is cheaper to smooth out than to serve at its peak. | 35 | carried | 'a burst is cheaper to smooth than it is to serve at its peak' in `merged.md` -- The text states the cost comparison directly. |
| 62 | Requests go to the platform team through the usual channel. | 35 | carried | 'Requests reach the platform team through the usual channel' in `merged.md` -- The text states how requests reach the team. |
| 63 | There is no expedited path. | 37 | carried | 'There is no expedited path' in `merged.md` -- The text states this directly. |

### `merged.md` -- 60 claim(s): 0 invented, 0 contradicted, 0 supported in part, 60 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Every credential has a cap. | supported | `source_a.md` | 'Every credential has a cap.' in `source_a.md` -- The source states the claim directly. |
| 2 | When a credential's cap is spent, the gateway answers 429 at the edge. | supported | `source_a.md` | 'When that cap is spent the gateway answers 429 at the edge' in `source_a.md` -- The source states that a spent cap produces a 429 at the edge. |
| 3 | When a credential's cap is spent, the gateway answers 429 without waking the service behind the gateway. | supported | `source_a.md` | 'When that cap is spent the gateway answers 429 at the edge — without waking the service behind it' in `source_a.md` -- The source states both the response and that the service is not woken. |
| 4 | An earlier draft proposed a client-side token bucket that mirrored the gateway’s counters. | supported | `source_b.md` | 'An earlier draft of this note argued for a client-side token bucket that mirrored the gateway’s own counters' in `source_b.md` -- The source describes the earlier draft’s proposal. |
| 5 | Requests are counted against the credential that presented them. | supported | `source_a.md` | 'Requests are counted against the credential that presented them' in `source_a.md` -- The source states the counting basis directly. |
| 6 | Requests are counted over a fixed window of 60 seconds. | supported | `source_a.md` | 'over a fixed window of 60 seconds' in `source_a.md` -- The source specifies the fixed counting window. |
| 7 | Requests are never counted against a connection. | supported | `source_a.md` | 'and never against a connection' in `source_a.md` -- The source explicitly excludes counting against a connection. |
| 8 | The gateway does not disclose when the window starts. | supported | `source_b.md` | 'whose start the gateway doesn’t disclose' in `source_b.md` -- The source says the gateway does not disclose the window’s start. |
| 9 | A client spread across eight worker processes is throttled at exactly the point one process would have been. | supported | `source_a.md` | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `source_a.md` -- The source states the eight-process comparison directly. |
| 10 | A client spread across eight worker processes uses extra file descriptors. | supported | `source_a.md` | 'A client spread across eight worker processes is throttled at exactly the point one process would have been — and pays for the extra file descriptors as well.' in `source_a.md` -- The source attributes extra file descriptors to the eight-process client. |
| 11 | The request count follows the credential across hosts. | supported | `source_b.md` | 'The count follows the credential wherever the caller happens to put it, including across hosts.' in `source_b.md` -- The source explicitly says the count follows the credential across hosts. |
| 12 | The default allowance is 100 requests in a window. | supported | `source_a.md` | 'The default allowance is 100 requests in a window' in `source_a.md` -- The source states the default allowance directly. |
| 13 | A credential marked for batch work is allowed 1000 requests in the same window. | supported | `source_a.md` | 'The default allowance is 100 requests in a window, and a credential marked for batch work is allowed 1000 in the same window.' in `source_a.md` -- The source gives the batch allowance and says it uses the same window. |
| 14 | The platform team has found 100 requests sufficient for every interactive use of this API it has seen. | supported | `source_b.md` | 'which is enough for every interactive use of this API the platform team has seen' in `source_b.md` -- In context, the source says the 100-request default has sufficed for those interactive uses. |
| 15 | Callers that need more than 100 requests in a window are almost always doing batch work under an interactive credential. | supported | `source_b.md` | 'a caller that needs more than that is almost always doing batch work under an interactive credential' in `source_b.md` -- In context, “that” refers to the 100-request default allowance. |
| 16 | Callers that retry at once are the largest single reason the cap is there at all. | supported | `source_a.md` | 'Callers that retry at once are the largest single reason the cap is there at all.' in `source_a.md` -- The source states the claim directly. |
| 17 | The refusal carries a Retry-After header. | supported | `source_a.md` | 'The refusal carries a Retry-After header.' in `source_a.md` -- The source states the claim directly. |
| 18 | The Retry-After header value is a whole number of seconds to wait. | supported | `source_a.md` | 'Its value is a whole number of seconds to wait.' in `source_a.md` -- In context, “Its” refers to the Retry-After header. |
| 19 | The Retry-After header is present on every refusal the gateway sends. | supported | `source_b.md` | 'The header is called Retry-After. Its value is a whole number of seconds, and it is present on every refusal the gateway sends.' in `source_b.md` -- The source identifies the header and says it is present on every refusal. |
| 20 | The gateway keeps no memory of who backed off politely. | supported | `source_a.md` | 'The gateway keeps no memory of who backed off politely' in `source_a.md` -- The source states the claim directly. |
| 21 | Waiting longer than the Retry-After header asks earns a caller no credit at all. | supported | `source_a.md` | 'waiting longer than the header asks earns a caller no credit at all' in `source_a.md` -- In context, the header is Retry-After. |
| 22 | The body of the refusal is JSON. | supported | `source_a.md` | 'The body of the refusal is JSON' in `source_a.md` -- The source states the claim directly. |
| 23 | The body of the refusal names what the gateway calls the “window” it counted in. | supported | `source_a.md` | 'The body of the refusal is JSON, and it names what the gateway calls the “window” it counted in.' in `source_a.md` -- The source explicitly says the refusal body names the counted window. |
| 24 | The body of the refusal names the cap. | supported | `source_a.md` | 'It names the cap and the tier as well.' in `source_a.md` -- In context, “It” refers to the refusal body. |
| 25 | The body of the refusal names the tier. | supported | `source_a.md` | 'It names the cap and the tier as well.' in `source_a.md` -- In context, “It” refers to the refusal body. |
| 26 | The gateway does the wait arithmetic using information the caller does not have. | supported | `source_a.md` | 'The gateway has already done that arithmetic, with information the caller does not have' in `source_a.md` -- The source explicitly says the gateway calculates the wait using information unavailable to the caller. |
| 27 | The gateway does the same wait arithmetic on the 503 path. | supported | `source_a.md` | 'The gateway has already done that arithmetic, with information the caller does not have, and it does the same on the 503 path.' in `source_a.md` -- The source explicitly extends the gateway's wait arithmetic to the 503 path. |
| 28 | A 503 refusal has a different cause from a 429 refusal. | supported | `source_b.md` | 'On the 503 path the same rule holds, even though the cause of the refusal is an entirely different one.' in `source_b.md` -- The source says the 503 refusal has a different cause. |
| 29 | A 200 wants nothing from a retry loop. | supported | `source_a.md` | 'A 200 wants nothing' in `source_a.md` -- The source gives this rule in its instructions for retrying. |
| 30 | A 429 wants the stated wait. | supported | `source_a.md` | 'a 429 wants the stated wait' in `source_a.md` -- The source states the claimed response to a 429. |
| 31 | A 500 may be retried once the stated wait has passed. | supported | `source_a.md` | 'a 500 may be retried once that wait has passed' in `source_a.md` -- The source states the claimed condition for retrying a 500. |
| 32 | A 503 is the overload path. | supported | `source_a.md` | 'a 503 is the overload path' in `source_a.md` -- The source calls the 503 path the overload path. |
| 33 | On the 503 path, the platform itself is overloaded. | supported | `source_b.md` | 'a 503 means the platform itself is overloaded' in `source_b.md` -- The source directly states what a 503 means. |
| 34 | A batch credential is allowed 1000 requests in the same window as a default credential. | supported | `source_a.md` | 'The default allowance is 100 requests in a window, and a credential marked for batch work is allowed 1000 in the same window.' in `source_a.md` -- The source gives the batch allowance and says it uses the same window. |
| 35 | The tier is set on the credential when it is issued. | supported | `source_a.md` | 'The tier is set on the credential when it is issued' in `source_a.md` -- The source states when the credential's tier is set. |
| 36 | The tier cannot be asked for per call. | supported | `source_a.md` | 'cannot be asked for per call' in `source_a.md` -- The source says the tier cannot be requested per call. |
| 37 | The window is identical across tiers. | supported | `source_b.md` | 'The window, the header and the body are identical to the interactive case' in `source_b.md` -- The source says the batch window is identical to the interactive window. |
| 38 | The header is identical across tiers. | supported | `source_b.md` | 'The window, the header and the body are identical to the interactive case' in `source_b.md` -- The source says the batch header is identical to the interactive header. |
| 39 | The body is identical across tiers. | supported | `source_b.md` | 'The window, the header and the body are identical to the interactive case' in `source_b.md` -- The source says the batch body is identical to the interactive body. |
| 40 | Nothing else about the two tiers differs in any way. | supported | `source_a.md` | 'Nothing else about the two tiers differs in any way.' in `source_a.md` -- The source states the claim verbatim. |
| 41 | Besides an exhausted cap, a credential may be suspended. | supported | `source_a.md` | 'Not all are caps. The gateway refuses a request for three reasons and only one of them is the one above. A credential may be suspended' in `source_a.md` -- The source lists suspension as a reason for refusal other than a cap. |
| 42 | Besides an exhausted cap, a route may be closed for maintenance or repair. | supported | `source_a.md` | 'a route may be closed for maintenance' in `source_a.md` -- The source lists route closure for maintenance among the other refusals. |
| 43 | Besides an exhausted cap, a body may exceed the 5 megabyte limit. | supported | `source_a.md` | 'a body may exceed the 5 megabyte limit' in `source_a.md` -- The source lists an oversized body among the other refusals. |
| 44 | An oversized request body is refused before it has been read at all. | supported | `source_b.md` | 'a request body over the 5 megabyte limit is refused before it has been read at all.' in `source_b.md` -- The source explicitly says an oversized body is refused before it is read. |
| 45 | Credential suspension does not depend on traffic sent in the current window. | supported | `source_b.md` | 'Two of the three have nothing to do with how much traffic a caller has sent in the window it is currently in. A credential can be suspended, a route can be closed while it is being repaired' in `source_b.md` -- The source identifies suspension as a refusal distinct from the traffic cap and describes non-traffic-based reasons. |
| 46 | Route closure does not depend on traffic sent in the current window. | supported | `source_b.md` | 'Two of the three have nothing to do with how much traffic a caller has sent in the window it is currently in. A credential can be suspended, a route can be closed while it is being repaired' in `source_b.md` -- The source identifies route closure as a refusal distinct from the traffic cap and describes non-traffic-based reasons. |
| 47 | Credential suspension does not clear itself by waiting for a stated number of seconds. | supported | `source_a.md` | 'A credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit. None of those three clears itself by waiting for a stated number of seconds.' in `source_a.md` -- The source explicitly includes suspension among the refusals that waiting does not clear. |
| 48 | Route closure does not clear itself by waiting for a stated number of seconds. | supported | `source_a.md` | 'A credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit. None of those three clears itself by waiting for a stated number of seconds.' in `source_a.md` -- The source explicitly includes route closure among the refusals that waiting does not clear. |
| 49 | A refusal caused by an oversized request body does not clear itself by waiting for a stated number of seconds. | supported | `source_a.md` | 'A credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit. None of those three clears itself by waiting for a stated number of seconds.' in `source_a.md` -- The source explicitly includes an oversized body among the refusals that waiting does not clear. |
| 50 | A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service. | supported | `source_a.md` | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `source_a.md` -- The source states the claim directly. |
| 51 | The log from a loop that waits and retries against a suspended credential shows nothing at all except a long run of refusals. | supported | `source_a.md` | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service — and the log afterwards shows nothing at all except a long run of refusals.' in `source_a.md` -- The source states what the log shows after that retry loop. |
| 52 | A cap can be raised. | supported | `source_a.md` | 'A cap can be raised, and the number of caps raised without a measurement behind them is 0.' in `source_a.md` -- The source explicitly says a cap can be raised. |
| 53 | The number of caps raised without a measurement behind them is 0. | supported | `source_a.md` | 'A cap can be raised, and the number of caps raised without a measurement behind them is 0.' in `source_a.md` -- The source gives the number as 0. |
| 54 | The platform team looks at whether the load is smooth or bursty before it considers the cap itself. | supported | `source_b.md` | 'The team wants to know whether the load is smooth or bursty before it looks at the number at all.' in `source_b.md` -- The source places assessment of the load before consideration of the cap number. |
| 55 | A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all. | supported | `source_a.md` | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `source_a.md` -- The source states the claim directly. |
| 56 | Requests for a cap increase reach the platform team through the usual channel. | supported | `source_a.md` | 'Requests reach the platform team through the usual channel' in `source_a.md` -- In the section on asking for an increase, the source gives this route for requests. |
| 57 | Requests for a cap increase are answered within two working days. | supported | `source_a.md` | 'they are answered within two working days' in `source_a.md` -- The source gives this response time for cap-increase requests. |
| 58 | There is no expedited path for requests for a cap increase. | supported | `source_a.md` | 'There is no expedited path and no exception list.' in `source_a.md` -- The source rules out an expedited path in its cap-increase section. |
| 59 | There is no exception list for requests for a cap increase. | supported | `source_a.md` | 'There is no expedited path and no exception list.' in `source_a.md` -- The source rules out an exception list in its cap-increase section. |
| 60 | Chasing a request for a cap increase does not shorten the wait. | supported | `source_b.md` | 'There is no expedited path. An answer takes two working days, and chasing it doesn’t make it take fewer.' in `source_b.md` -- The source says chasing the request does not reduce the response time. |

## Structure

**9** mechanical check(s) over **104** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **60** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **114**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 15 run(s) over 56 attributed segment(s) — sources interleaved. 6 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

`[-...-]` is what the source said and `{+...+}` is what the merge says.

### Reworded and undeclared — in the merge in altered wording, and no record explains it. At off this also covers layout: a segment whose source line breaks the merge ran together is altered and undeclared, and 380 reuses this kind rather than moving FINDING_KINDS off 12

- `a23` (`source_a.md`) — 'The gateway has already done that arithmetic, with information the caller does not have, and it does the same on the 503 path.' is reworded in the merge and no disposition record explains it (nearest merge segment m30 at 0.84)

  ```text
  In the source: The gateway has already done that arithmetic, with information the caller does not have, and it does the same on the 503 path.
  In the merge:  The gateway has already done that arithmetic, with information the caller does not have, and it does the same on the 503 path, even though that refusal has a different cause.
  What changed:  The gateway has already done that arithmetic, with information the caller does not have, and it does the same on the 503 [-path.-] {+path, even though that refusal has a different cause.+}
  ```
- `a27` (`source_a.md`) — 'A 200 wants nothing, a 429 wants the stated wait, a 500 may be retried once that wait has passed, and a 503 is the overload path.' is reworded in the merge and no disposition record explains it (nearest merge segment m34 at 0.88)

  ```text
  In the source: A 200 wants nothing, a 429 wants the stated wait, a 500 may be retried once that wait has passed, and a 503 is the overload path.
  In the merge:  A 200 wants nothing, a 429 wants the stated wait, a 500 may be retried once that wait has passed, and a 503 is the overload path: the platform itself is overloaded.
  What changed:  A 200 wants nothing, a 429 wants the stated wait, a 500 may be retried once that wait has passed, and a 503 is the overload [-path.-] {+path: the platform itself is overloaded.+}
  ```

### Unresolved replacement — a record points at text the merge does not contain

- `b46` — segment b46 is declared 'subsumed' with replacement 'A cap can be raised, and the number of caps raised without a measurement behind them is 0. Without those counts, an assertion that the cap is too small is not enough.', which is not in the merged document

  ```text
  In the merge: A cap can be raised, and the number of caps raised without a measurement behind them is 0. Without those counts, an assertion that the cap is too small is not enough.
  ```

### Verbatim violation — an invariant-core token did not survive unchanged

- `b31` (`source_b.md`) — numeric '50' (times) does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **56** departure(s) from its sources. Checking them confirms 40, rejects 5, and leaves 11 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 104 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | Title: the base title was chosen. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Rate limiting and the 429 contract for gateway clients' and says so (no claim traced to it) |
| `b2` | duplicate | Credential cap: the base wording carries the fact. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-001`) |
| `b3` | duplicate | Edge refusal: the base wording carries the fact. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-002`, `B-003`) |
| `b4` | reworded | Introduction: retained the draft history and its rationale. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b5` | subsumed | Counting: combined the shared rule with the undisclosed start. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-004`, `B-005`, `B-006`) |
| `b6` | duplicate | Sockets: the base wording carries the fact. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-007`) |
| `b7` | reworded | Counting: retained the cross-host detail. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-008`) |
| `b8` | subsumed | Workers: the base gives the same rule more specifically. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-009`) |
| `b9` | subsumed | Allowances: retained the usage observations with the shared limit. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-010`, `B-011`) |
| `b10` | subsumed | Refusal meaning: retained the gateway-bug distinction. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-012`, `B-013`, `B-014`) |
| `b11` | duplicate | Immediate retries: the base wording carries the point. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-015`) |
| `b12` | duplicate | Heading: the shared heading appears once. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b13` | duplicate | Header name: the base wording carries it. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-016`) |
| `b14` | subsumed | Header: retained its value and stated availability. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-017`, `B-018`) |
| `b15` | subsumed | Contract: kept the shared operational point. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-019`) |
| `b16` | duplicate | Extra waiting: the base wording carries the fact. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b17` | subsumed | Body: retained its format, fields and plain-field detail. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-020`, `B-021`, `B-022`, `B-023`) |
| `b18` | subsumed | Wait calculation: retained the risk of disagreeing counters. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-024`) |
| `b19` | duplicate | Body purpose: the base wording carries it. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-025`) |
| `b20` | superseded | Retry heading: the base heading was chosen. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b21` | duplicate | Rule order: the base wording carries it. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b22` | subsumed | First rule: retained the ban on computing a client-side wait. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b23` | duplicate | First rule: the base carries the information asymmetry. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-026`, `B-027`) |
| `b24` | subsumed | First rule: retained the distinct cause on the 503 path. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-028`, `B-029`) |
| `b25` | duplicate | First rule: the base carries the guess warning. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b26` | duplicate | First rule: the base carries the conclusion. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b27` | subsumed | Second rule: retained the narrower safe-retry set. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b28` | subsumed | Status handling: retained the overload explanation. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-030`, `B-031`, `B-032`, `B-033`) |
| `b29` | duplicate | Second rule: the base carries the retry consequence. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'duplicate' is what happened to it (no claim traced to it) |
| `b30` | subsumed | Second rule: the base carries the instruction. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a32` | superseded | Batch allowance: the explicit limit replaces the conflicting multiplier. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`A-027`, `A-028`) |
| `b31` | superseded | Batch allowance: kept the limit and shared window, not the multiplier. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-034`, `B-035`, `B-036`) |
| `b32` | subsumed | Batch tier: retained client compatibility and shared behaviour. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-037`, `B-038`, `B-039`, `B-040`) |
| `b33` | duplicate | Batch tier: the base carries the shared rule. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-041`) |
| `b34` | subsumed | Logging: retained the minimum retention period. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b35` | duplicate | Increase evidence: the base carries the same requirement. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-042`) |
| `b36` | superseded | Increase evidence: counts are essential, but other evidence is required. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b37` | superseded | Other refusals heading: the base heading was chosen. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a40` | superseded | Refusal causes: the named causes replace the conflicting total. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`A-032`, `A-033`) |
| `a41` | subsumed | Refusal causes: retained all listed non-cap causes. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-034`, `A-035`, `A-036`) |
| `b38` | superseded | Refusal causes: the named causes replace the conflicting total. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-043`, `B-044`) |
| `b39` | superseded | Refusal causes: retained the traffic distinction, not the total. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-045`) |
| `b40` | subsumed | Refusal causes: retained repair and the early body refusal. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-046`, `B-047`, `B-048`, `B-049`) |
| `b41` | subsumed | Retry distinction: the base states the operational point. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b42` | duplicate | Suspension: the base carries the wasted-budget consequence. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-050`, `B-051`) |
| `b43` | subsumed | Suspension: retained the misleading log and caller-owned cost. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-052`, `B-053`) |
| `b44` | duplicate | Traffic shifting: the base carries the same option. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-054`) |
| `b45` | reworded | Increase guidance: retained cost and broad availability. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b46` | subsumed | Increase evidence: retained the need for measurements. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-055`, `B-056`) |
| `b47` | duplicate | Increase evidence: the base carries all requested items. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-057`, `B-058`, `B-059`) |
| `a49` | subsumed | Increase review: retained the load comparison and cost. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-044`) |
| `b48` | subsumed | Increase review: retained the order of assessment. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-060`) |
| `b49` | subsumed | Increase review: retained the burst-cost comparison. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-061`) |
| `b50` | duplicate | Request channel: the base carries it. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-062`) |
| `b51` | duplicate | Expedition: the base carries the restriction. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-063`) |
| `b52` | subsumed | Response time: retained the effect of chasing a request. | **rejected** | declared 'subsumed', which predicts SUPPORTED; B-064 came back PARTIAL, B-065 came back PARTIAL (`B-064`, `B-065`) |


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
| Tokens | 41,842 in, 31,449 out, 10,748 cached, 5,147 reasoning |
| Cost | ~$0.38 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 338.6s |
| Generated | 2026-09-27T16:05:02+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `bf7d5842201d`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
