## Verdict

**62 finding(s).** In the claims: 5 dropped, 6 partially dropped, 5 contradicted. In the structure: 26 undeclared absence, 17 undeclared rewording, 1 verbatim violation, 2 declared loss over budget. The merge declared **6** drop(s) of 104 source segment(s), **5.8%**, over the 3% budget: past that share the omissions are the finding, whatever each one says about itself. The 1 claim(s) they cost are listed in the review queue below.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 46 |
| Claims extracted from `source_a.md` | 45 |
| Claims extracted from `source_b.md` | 53 |
| Forward — source claims accounted for in the merge | **81/98** |
| Forward — carried only in part | 6 |
| Forward — `source_a.md` claims accounted for | **43/45** |
| Forward — `source_b.md` claims accounted for | **38/53** (6 in part) |
| Reverse — merge claims found in a source | **46/46** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **137/138** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Dropped — in a source, not in the merge

- **B-007** (`source_b.md:7`) — A caller needing more than the default allowance is almost always doing batch work under an interactive credential.
  - judged against: `merged.md`
  - rationale: The text does not state whether batch work is usually done under batch or interactive credentials.
- **B-042** (`source_b.md:29`) — A request body over the 5 megabyte limit is refused before it has been read at all.
  - judged against: `merged.md`
  - rationale: The text states body size limits but does not specify when the refusal occurs in the processing.
- **B-045** (`source_b.md:31`) — The wasted budget is the caller's own.
  - judged against: `merged.md`
  - rationale: The text does not explicitly state that the wasted budget belongs to the caller themselves.
- **B-047** (`source_b.md:33`) — Moving work to a quieter hour is available to almost everybody.
  - judged against: `merged.md`
  - rationale: The text does not state whether load shifting is available to almost everybody.
- **B-053** (`source_b.md:37`) — Chasing the request doesn't make the answer take fewer days.
  - judged against: `merged.md`
  - rationale: The text does not state whether following up affects the response timeline.

### Partly dropped — the merge carries some of this claim

- **B-003** (`source_b.md:5`) — Requests are counted against the credential rather than the connection, over a fixed window of 60 seconds whose start the gateway doesn't disclose.
  - evidence: 'Requests are counted against the credential that presented them, over a fixed window of 60 seconds, and never against a connection.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text states the credential and fixed window but does not state whether the window's start is disclosed or not.
- **B-011** (`source_b.md:11`) — The Retry-After header is present on every refusal the gateway sends.
  - evidence: 'The refusal carries a Retry-After header with a whole number of seconds to wait.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text states the header is present on refusals due to rate limits but does not confirm it on all other refusals.
- **B-014** (`source_b.md:13`) — The response body repeats the cap, the window, and the tier as plain fields.
  - evidence: 'and it names what the gateway calls the "window" it counted in, the cap, and the tier as well.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text states these fields are named but does not specify they are plain fields or how they are presented.
- **B-020** (`source_b.md:19`) — The cause of a 503 refusal is an entirely different one than that of a 429 refusal.
  - evidence: 'and a 503 is the overload path.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text identifies 503 as the overload path but does not explicitly state the causes differ entirely.
- **B-034** (`source_b.md:25`) — The log should be kept for at least a week.
  - evidence: 'A caller that cannot say how often it was refused last week cannot argue for a larger cap' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text implies logs should be kept a week but does not explicitly state a minimum retention period.
- **B-049** (`source_b.md:35`) — The team wants to know whether the load is smooth or bursty before it looks at the number at all.
  - evidence: 'The platform team looks at whether the load is smooth or bursty' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text states the team looks at load pattern but does not explicitly state this occurs before examining the number.

### Contradicted — the merge states something different

- **A-024** -- the two documents disagree
  - `source_a.md:23` says: A batch credential is allowed fifty times the default allowance.
  - `merged.md` says: 'The default allowance is 100 requests in a window, and a credential marked for batch work is allowed 1000 in the same window.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states batch is 1000, which is 10 times the default of 100, not 50 times.
- **A-029** -- the two documents disagree
  - `source_a.md:29` says: The gateway refuses a request for three reasons and only one of them is the rate limit cap.
  - `merged.md` says: 'The gateway refuses a request for three reasons: a credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text lists three reasons that exclude rate limits; rate limits are a separate reason discussed earlier, making four reasons total, not three with one being the cap.
- **B-028** -- the two documents disagree
  - `source_b.md:23` says: 1000 is 50 times the default.
  - `merged.md` says: 'The default allowance is 100 requests in a window, and a credential marked for batch work is allowed 1000 in the same window.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states batch is 1000, which is 10 times the default of 100, not 50 times.
- **B-038** -- the two documents disagree
  - `source_b.md:29` says: Only one of the three refusal reasons is a cap.
  - `merged.md` says: 'The gateway refuses a request for three reasons: a credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The three listed reasons exclude rate limits; none of them are rate limit caps, contradicting the claim.
- **B-039** -- the two documents disagree
  - `source_b.md:29` says: Two of the three refusal reasons have nothing to do with how much traffic a caller has sent in the window it is currently in.
  - `merged.md` says: 'The gateway refuses a request for three reasons: a credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: All three reasons have nothing to do with traffic volume in the window, not just two.

## Length capped

- `$.dispositions[2].reason` was 92 characters, over the 80-character cap; capped to fit
- `$.dispositions[3].reason` was 96 characters, over the 80-character cap; capped to fit
- `$.dispositions[5].reason` was 88 characters, over the 80-character cap; capped to fit
- `$.dispositions[7].reason` was 103 characters, over the 80-character cap; capped to fit
- `$.dispositions[18].reason` was 107 characters, over the 80-character cap; capped to fit
- `$.dispositions[19].reason` was 88 characters, over the 80-character cap; capped to fit

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 45 claim(s): 0 dropped, 2 contradicted, 0 carried in part, 43 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 24 | A batch credential is allowed fifty times the default allowance. | 23 | contradicted | 'The default allowance is 100 requests in a window, and a credential marked for batch work is allowed 1000 in the same window.' in `merged.md` -- The text states batch is 1000, which is 10 times the default of 100, not 50 times. |
| 29 | The gateway refuses a request for three reasons and only one of them is the rate limit cap. | 29 | contradicted | 'The gateway refuses a request for three reasons: a credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit.' in `merged.md` -- The text lists three reasons that exclude rate limits; rate limits are a separate reason discussed earlier, making four reasons total, not three with one being the cap. |
| 1 | Every credential has a cap. | 3 | carried | 'Every credential has a cap.' in `merged.md` -- The reference text explicitly states that every credential has a cap. |
| 2 | When that cap is spent the gateway answers 429 at the edge. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge without waking the service behind it' in `merged.md` -- The text states the gateway answers 429 at the edge when the cap is spent. |
| 3 | Requests are counted against the credential that presented them, over a fixed window of 60 seconds. | 5 | carried | 'Requests are counted against the credential that presented them, over a fixed window of 60 seconds' in `merged.md` -- The reference text directly states this claim about request counting and the 60-second window. |
| 4 | Requests are never counted against a connection. | 5 | carried | 'and never against a connection.' in `merged.md` -- The text explicitly states requests are never counted against a connection. |
| 5 | Opening a second socket buys a caller nothing. | 5 | carried | 'Opening a second socket therefore buys a caller nothing.' in `merged.md` -- The reference text directly states this claim about opening a second socket. |
| 6 | A client spread across eight worker processes is throttled at exactly the point one process would have been. | 5 | carried | 'A client spread across multiple worker processes is throttled at exactly the point a single process would have been' in `merged.md` -- The text states this for multiple processes, which includes eight as a specific instance. |
| 7 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- The reference text explicitly states the default allowance. |
| 8 | A credential marked for batch work is allowed 1000 in the same window. | 7 | carried | 'and a credential marked for batch work is allowed 1000 in the same window.' in `merged.md` -- The text explicitly states the batch allowance of 1000 requests. |
| 9 | The refusal carries a Retry-After header. | 11 | carried | 'The refusal carries a Retry-After header with a whole number of seconds to wait.' in `merged.md` -- The reference text states the refusal carries a Retry-After header. |
| 10 | The value of the Retry-After header is a whole number of seconds to wait. | 11 | carried | 'The refusal carries a Retry-After header with a whole number of seconds to wait.' in `merged.md` -- The text specifies the header value is a whole number of seconds to wait. |
| 11 | The gateway keeps no memory of who backed off politely. | 11 | carried | 'The gateway keeps no memory of who backed off politely' in `merged.md` -- The reference text directly states this claim. |
| 12 | The body of the refusal is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- The text explicitly states the refusal body is JSON. |
| 13 | The body of the refusal names what the gateway calls the "window" it counted in. | 13 (unverified) | carried | 'and it names what the gateway calls the "window" it counted in, the cap, and the tier as well.' in `merged.md` -- The text states the body names the window, cap, and tier. |
| 14 | The body of the refusal names the cap and the tier. | 13 | carried | 'and it names what the gateway calls the "window" it counted in, the cap, and the tier as well.' in `merged.md` -- The text explicitly names both the cap and tier in the body. |
| 15 | A caller that parses the body to compute its own wait is doing the same arithmetic twice. | 13 | carried | 'a caller that parses the body to compute its own wait is doing the same arithmetic twice.' in `merged.md` -- The reference text directly states this claim. |
| 16 | The gateway has already done that arithmetic, with information the caller does not have. | 19 | carried | 'The gateway has already done that arithmetic, with information the caller does not have' in `merged.md` -- The text explicitly states this point about the gateway's superior information. |
| 17 | The gateway does the same arithmetic on the 503 path. | 19 | carried | 'and it does the same on the 503 path.' in `merged.md` -- The text states the gateway does the same arithmetic on the 503 path. |
| 18 | A 200 wants nothing. | 21 | carried | 'A 200 wants nothing' in `merged.md` -- The reference text directly states this claim about the 200 response. |
| 19 | A 429 wants the stated wait. | 21 | carried | 'a 429 wants the stated wait' in `merged.md` -- The text explicitly states what a 429 response wants. |
| 20 | A 500 may be retried once that wait has passed. | 21 | carried | 'a 500 may be retried once that wait has passed' in `merged.md` -- The text directly states this claim about 500 responses. |
| 21 | A 503 is the overload path. | 21 | carried | 'and a 503 is the overload path.' in `merged.md` -- The text explicitly identifies 503 as the overload path. |
| 22 | The four cases are not interchangeable. | 21 | carried | 'The four cases are not interchangeable.' in `merged.md` -- The reference text directly states this claim. |
| 23 | A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive. | 21 | carried | 'A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive.' in `merged.md` -- The text directly states this claim about retry behavior. |
| 25 | A batch credential is measured over exactly the same window. | 23 | carried | 'A batch credential is allowed 1000 requests in a window, measured over exactly the same window.' in `merged.md` -- The text explicitly states batch credentials are measured over exactly the same window. |
| 26 | The tier is set on the credential when it is issued. | 23 | carried | 'The tier is set on the credential when it is issued' in `merged.md` -- The reference text directly states when the tier is set. |
| 27 | The tier cannot be asked for per call. | 23 | carried | 'and cannot be asked for per call.' in `merged.md` -- The text explicitly states the tier cannot be requested per call. |
| 28 | Nothing else about the two tiers differs in any way. | 23 | carried | 'Nothing else about the two tiers differs in any way.' in `merged.md` -- The reference text directly states this about the tiers. |
| 30 | A credential may be suspended. | 29 | carried | 'a credential may be suspended' in `merged.md` -- The text explicitly states this as one refusal reason. |
| 31 | A route may be closed for maintenance. | 29 | carried | 'a route may be closed for maintenance' in `merged.md` -- The text explicitly lists this as a refusal reason. |
| 32 | A body may exceed the 5 megabyte limit. | 29 | carried | 'or a body may exceed the 5 megabyte limit.' in `merged.md` -- The text explicitly lists this as a refusal reason. |
| 33 | None of those three reasons clears itself by waiting for a stated number of seconds. | 29 | carried | 'None of those three clears itself by waiting for a stated number of seconds.' in `merged.md` -- The reference text directly states this about the three reasons. |
| 34 | A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `merged.md` -- The text directly states this consequence of retrying against a suspended credential. |
| 35 | The log afterwards shows nothing at all except a long run of refusals. | 31 | carried | 'and the log afterwards shows nothing at all except a long run of refusals.' in `merged.md` -- The text explicitly states what the log shows in this scenario. |
| 36 | Reading the status code rather than the class it belongs to is what separates the two cases. | 31 | carried | 'Reading the status code rather than the class it belongs to is what separates the two cases' in `merged.md` -- The reference text directly states this about separating the cases. |
| 37 | Reading the status code rather than the class costs one comparison. | 31 | carried | 'and it costs one comparison.' in `merged.md` -- The text states that reading the status code costs one comparison. |
| 38 | A cap can be raised. | 35 | carried | 'A cap can be raised' in `merged.md` -- The reference text directly states this claim. |
| 39 | The number of caps raised without a measurement behind them is 0. | 35 | carried | 'but the number of caps raised without a measurement behind them is zero.' in `merged.md` -- The text explicitly states that zero caps are raised without measurement. |
| 40 | The platform team looks at whether the load is smooth or bursty. | 35 | carried | 'The platform team looks at whether the load is smooth or bursty' in `merged.md` -- The reference text directly states what the platform team examines. |
| 41 | A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all. | 35 | carried | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `merged.md` -- The text directly states this about the outcome of load shifting. |
| 42 | Requests reach the platform team through the usual channel. | 37 | carried | 'Requests reach the platform team through the usual channel' in `merged.md` -- The reference text explicitly states this about the communication channel. |
| 43 | Requests are answered within two working days. | 37 | carried | 'and they are answered within two working days.' in `merged.md` -- The text states the response timeframe for requests. |
| 44 | There is no expedited path. | 37 | carried | 'There is no expedited path' in `merged.md` -- The reference text directly states this claim. |
| 45 | There is no exception list. | 36 (unverified) | carried | 'and no exception list.' in `merged.md` -- The text explicitly states there is no exception list. |

### `source_b.md` -- 53 claim(s): 6 dropped, 3 contradicted, 6 carried in part, 38 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 4 | The request count follows the credential wherever the caller places it, including across hosts. | 5 | dropped | The text mentions spreading across processes but does not state the request count follows across hosts. |
| 7 | A caller needing more than the default allowance is almost always doing batch work under an interactive credential. | 7 | dropped | The text does not state whether batch work is usually done under batch or interactive credentials. |
| 42 | A request body over the 5 megabyte limit is refused before it has been read at all. | 29 | dropped | The text states body size limits but does not specify when the refusal occurs in the processing. |
| 45 | The wasted budget is the caller's own. | 31 (unverified) | dropped | The text does not explicitly state that the wasted budget belongs to the caller themselves. |
| 47 | Moving work to a quieter hour is available to almost everybody. | 33 | dropped | The text does not state whether load shifting is available to almost everybody. |
| 53 | Chasing the request doesn't make the answer take fewer days. | 37 (unverified) | dropped | The text does not state whether following up affects the response timeline. |
| 28 | 1000 is 50 times the default. | 23 | contradicted | 'The default allowance is 100 requests in a window, and a credential marked for batch work is allowed 1000 in the same window.' in `merged.md` -- The text states batch is 1000, which is 10 times the default of 100, not 50 times. |
| 38 | Only one of the three refusal reasons is a cap. | 29 | contradicted | 'The gateway refuses a request for three reasons: a credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit.' in `merged.md` -- The three listed reasons exclude rate limits; none of them are rate limit caps, contradicting the claim. |
| 39 | Two of the three refusal reasons have nothing to do with how much traffic a caller has sent in the window it is currently in. | 29 | contradicted | 'The gateway refuses a request for three reasons: a credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit.' in `merged.md` -- All three reasons have nothing to do with traffic volume in the window, not just two. |
| 3 | Requests are counted against the credential rather than the connection, over a fixed window of 60 seconds whose start the gateway doesn't disclose. | 5 (unverified) | carried in part | 'Requests are counted against the credential that presented them, over a fixed window of 60 seconds, and never against a connection.' in `merged.md` -- The text states the credential and fixed window but does not state whether the window's start is disclosed or not. |
| 11 | The Retry-After header is present on every refusal the gateway sends. | 11 | carried in part | 'The refusal carries a Retry-After header with a whole number of seconds to wait.' in `merged.md` -- The text states the header is present on refusals due to rate limits but does not confirm it on all other refusals. |
| 14 | The response body repeats the cap, the window, and the tier as plain fields. | 13 | carried in part | 'and it names what the gateway calls the "window" it counted in, the cap, and the tier as well.' in `merged.md` -- The text states these fields are named but does not specify they are plain fields or how they are presented. |
| 20 | The cause of a 503 refusal is an entirely different one than that of a 429 refusal. | 19 | carried in part | 'and a 503 is the overload path.' in `merged.md` -- The text identifies 503 as the overload path but does not explicitly state the causes differ entirely. |
| 34 | The log should be kept for at least a week. | 25 | carried in part | 'A caller that cannot say how often it was refused last week cannot argue for a larger cap' in `merged.md` -- The text implies logs should be kept a week but does not explicitly state a minimum retention period. |
| 49 | The team wants to know whether the load is smooth or bursty before it looks at the number at all. | 35 | carried in part | 'The platform team looks at whether the load is smooth or bursty' in `merged.md` -- The text states the team looks at load pattern but does not explicitly state this occurs before examining the number. |
| 1 | Every credential has a cap of its own. | 3 | carried | 'Every credential has a cap.' in `merged.md` -- Stating every credential has a cap necessarily entails each has its own cap. |
| 2 | When a credential's cap is spent, the gateway answers 429 at the edge without troubling the service behind it. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge without waking the service behind it' in `merged.md` -- The text uses equivalent terms: 'without waking' means 'without troubling' the service. |
| 5 | A caller spread over many worker processes is throttled at the same point a single process would have been. | 5 | carried | 'A client spread across multiple worker processes is throttled at exactly the point a single process would have been' in `merged.md` -- Multiple processes includes many, and the throttling point is the same as for a single process. |
| 6 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- The reference text directly states the default allowance. |
| 8 | Callers that retry immediately are most of the reason the cap exists. | 7 | carried | 'Callers that retry at once are the largest single reason the cap is there at all.' in `merged.md` -- Retrying immediately is retrying at once; largest single reason equals most of the reason. |
| 9 | The header is called Retry-After. | 11 | carried | 'The refusal carries a Retry-After header' in `merged.md` -- The reference text names the header as Retry-After. |
| 10 | The Retry-After header's value is a whole number of seconds. | 11 | carried | 'The refusal carries a Retry-After header with a whole number of seconds to wait.' in `merged.md` -- The text specifies the header value is a whole number of seconds. |
| 12 | Waiting longer than the Retry-After header specifies earns nothing. | 11 | carried | 'The gateway keeps no memory of who backed off politely, so waiting longer than the header asks earns a caller no credit at all.' in `merged.md` -- The text directly states that waiting longer than the header specifies earns no benefit. |
| 13 | The response body is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- The reference text directly states the body is JSON. |
| 15 | There are four rules. | 17 | carried | 'Four rules, given in the order they should be applied.' in `merged.md` -- The reference text explicitly states there are four rules. |
| 16 | The rules should be applied in the order they are given. | 17 | carried | 'Four rules, given in the order they should be applied.' in `merged.md` -- The text states the rules should be applied in the order they are given. |
| 17 | The gateway has already done the arithmetic for the wait time. | 19 | carried | 'The gateway has already done that arithmetic' in `merged.md` -- The reference text directly states this about the gateway's computation. |
| 18 | The gateway computed the wait time with information the caller cannot see. | 19 | carried | 'with information the caller does not have' in `merged.md` -- The text states the gateway used information the caller cannot access. |
| 19 | The same rule about honouring the header holds on the 503 path. | 19 | carried | 'and it does the same on the 503 path.' in `merged.md` -- The text directly states the same arithmetic rule applies to the 503 path. |
| 21 | Only safe requests should be retried. | 21 | carried | 'Retry only what is safe to retry.' in `merged.md` -- The reference text directly states that only safe requests should be retried. |
| 22 | Safe requests constitute a smaller set than all responses that are not a success. | 21 (unverified) | carried | 'Retry only what is safe to retry. A 200 wants nothing, a 429 wants the stated wait, a 500 may be retried once that wait has passed, and a 503 is the overload path.' in `merged.md` -- Safe-to-retry responses are specified; not all non-success responses appear in this list. |
| 23 | A 200 response requires no retry action. | 21 | carried | 'A 200 wants nothing' in `merged.md` -- The text states that a 200 response wants no action. |
| 24 | A 429 response requires waiting the stated wait time. | 21 | carried | 'a 429 wants the stated wait' in `merged.md` -- The reference text directly states what a 429 requires. |
| 25 | A 500 response can be retried once the stated wait time has passed. | 21 | carried | 'a 500 may be retried once that wait has passed' in `merged.md` -- The text explicitly states when a 500 can be retried. |
| 26 | A 503 response indicates that the platform itself is overloaded. | 21 | carried | 'and a 503 is the overload path.' in `merged.md` -- The text identifies the 503 response as indicating platform overload. |
| 27 | A batch credential is allowed 1000 requests in a window. | 23 | carried | 'a credential marked for batch work is allowed 1000 in the same window.' in `merged.md` -- The reference text explicitly states the batch allowance of 1000 requests. |
| 29 | The batch tier is not a separate counting scheme. | 23 | carried | 'A batch credential is allowed 1000 requests in a window, measured over exactly the same window.' in `merged.md` -- The text states batch uses exactly the same window, so it is not a separate counting scheme. |
| 30 | The window, the header and the body are identical in the batch case to the interactive case. | 23 | carried | 'Nothing else about the two tiers differs in any way.' in `merged.md` -- The text states nothing else differs, which entails the window, header, and body are identical. |
| 31 | A client written for one tier needs no change to run against the other tier. | 23 | carried | 'Nothing else about the two tiers differs in any way.' in `merged.md` -- If nothing differs between tiers, a client needs no changes to work with either tier. |
| 32 | Nothing else about the batch tier differs from the default tier. | 23 | carried | 'Nothing else about the two tiers differs in any way.' in `merged.md` -- The reference text directly states this about the tiers. |
| 33 | Every refusal should be logged. | 25 | carried | 'Log every refusal seen.' in `merged.md` -- The text directly states that every refusal should be logged. |
| 35 | A caller that cannot report how often it was refused cannot make a case for a larger cap. | 25 (unverified) | carried | 'A caller that cannot say how often it was refused last week cannot argue for a larger cap' in `merged.md` -- The text states that inability to report refusals prevents arguing for increased capacity. |
| 36 | The platform team will not assemble a case for a larger cap on behalf of a caller. | 25 (unverified) | carried | 'and nobody at the far end will assemble that argument on its behalf.' in `merged.md` -- The text states the platform team will not make a case for the caller. |
| 37 | The gateway refuses requests for three separate reasons. | 29 | carried | 'The gateway refuses a request for three reasons' in `merged.md` -- The reference text states there are three reasons for refusals. |
| 40 | A credential can be suspended. | 29 | carried | 'a credential may be suspended' in `merged.md` -- The text explicitly states credentials can be suspended. |
| 41 | A route can be closed while it is being repaired. | 29 | carried | 'a route may be closed for maintenance' in `merged.md` -- The text states routes can be closed for maintenance, which includes repair. |
| 43 | A loop retrying against a suspended credential burns its whole budget and reaches nothing. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `merged.md` -- Spending whole budget without reaching service is equivalent to burning budget and reaching nothing. |
| 44 | The log afterwards shows a long run of refusals and no successes at all. | 31 | carried | 'and the log afterwards shows nothing at all except a long run of refusals.' in `merged.md` -- The text shows a long run of refusals and no other activity, meaning no successes. |
| 46 | A caller that can move half its work to a quieter hour usually finds it doesn't need a larger cap in the first place. | 33 (unverified) | carried | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `merged.md` -- Getting what it needs without cap change means not needing a larger cap in the first place. |
| 48 | A cap can be raised. | 33 | carried | 'A cap can be raised' in `merged.md` -- The reference text directly states this claim. |
| 50 | Requests go to the platform team through the usual channel. | 35 | carried | 'Requests reach the platform team through the usual channel' in `merged.md` -- The text directly states the channel for requests. |
| 51 | There is no expedited path. | 37 | carried | 'There is no expedited path' in `merged.md` -- The reference text explicitly states this claim. |
| 52 | An answer takes two working days. | 37 | carried | 'and they are answered within two working days.' in `merged.md` -- The text specifies the response timeframe as two working days. |

### `merged.md` -- 46 claim(s): 0 invented, 0 contradicted, 0 supported in part, 46 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Every credential has a cap. | supported | `source_a.md` | 'Every credential has a cap.' in `source_a.md` -- Exact statement in source_a. |
| 2 | When the cap is spent the gateway answers 429 at the edge without waking the service behind it. | supported | `source_a.md` | 'When that cap is spent the gateway answers 429 at the edge — without waking the service behind it' in `source_a.md` -- Source states this precisely. |
| 3 | Requests are counted against the credential that presented them. | supported | `source_a.md` | 'Requests are counted against the credential that presented them' in `source_a.md` -- Exact statement in source_a. |
| 4 | Requests are counted over a fixed window of 60 seconds. | supported | `source_a.md` | 'over a fixed window of 60 seconds' in `source_a.md` -- Source directly states this. |
| 5 | Requests are never counted against a connection. | supported | `source_a.md` | 'and never against a connection' in `source_a.md` -- Explicit statement in source_a. |
| 6 | Opening a second socket provides no benefit to a caller. | supported | `source_a.md` | 'Opening a second socket therefore buys a caller nothing.' in `source_a.md` -- Restates the source claim in different words. |
| 7 | A client spread across multiple worker processes is throttled at exactly the point a single process would have been. | supported | `source_a.md` | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `source_a.md` -- Source directly supports this statement. |
| 8 | A client spread across multiple worker processes pays for the extra file descriptors. | supported | `source_a.md` | 'and pays for the extra file descriptors as well.' in `source_a.md` -- Exact statement from source_a. |
| 9 | The default allowance is 100 requests in a window. | supported | `source_a.md` | 'The default allowance is 100 requests in a window' in `source_a.md` -- Stated identically in source_a. |
| 10 | A credential marked for batch work is allowed 1000 requests in the same window. | supported | `source_a.md` | 'a credential marked for batch work is allowed 1000 in the same window' in `source_a.md` -- Source states the 1000 request allowance for batch. |
| 11 | Callers that retry at once are the largest single reason the cap is there at all. | supported | `source_a.md` | 'Callers that retry at once are the largest single reason the cap is there at all.' in `source_a.md` -- Exact statement in source_a. |
| 12 | The refusal carries a Retry-After header with a whole number of seconds to wait. | supported | `source_a.md` | 'The refusal carries a Retry-After header. Its value is a whole number of seconds to wait.' in `source_a.md` -- Source states both the header presence and its whole-number value. |
| 13 | The gateway keeps no memory of who backed off politely. | supported | `source_a.md` | 'The gateway keeps no memory of who backed off politely' in `source_a.md` -- Exact statement from source_a. |
| 14 | Waiting longer than the header asks earns a caller no credit at all. | supported | `source_a.md` | 'Waiting longer than the header asks earns a caller no credit at all.' in `source_a.md` -- Source provides exact statement. |
| 15 | The body of the refusal is JSON. | supported | `source_a.md` | 'The body of the refusal is JSON' in `source_a.md` -- Stated in source_a. |
| 16 | The body names what the gateway calls the "window" it counted in, the cap, and the tier. | supported | `source_a.md` | 'It names what the gateway calls the "window" it counted in. It names the cap and the tier as well.' in `source_a.md`, **transcription_error** -- Source describes what the response body contains. |
| 17 | None of those fields is a substitute for the header. | supported | `source_a.md` | 'None of those fields is a substitute for the header' in `source_a.md` -- Exact statement in source_a. |
| 18 | The gateway has already done that arithmetic, with information the caller does not have. | supported | `source_a.md` | 'The gateway has already done that arithmetic, with information the caller does not have' in `source_a.md` -- Source directly states this. |
| 19 | The gateway does the same on the 503 path. | supported | `source_a.md` | 'and it does the same on the 503 path' in `source_a.md` -- Explicit statement in source_a. |
| 20 | A 200 wants nothing. | supported | `source_a.md` | 'A 200 wants nothing' in `source_a.md` -- Source states this case. |
| 21 | A 429 wants the stated wait. | supported | `source_a.md` | 'a 429 wants the stated wait' in `source_a.md` -- Stated in source_a's retry rules. |
| 22 | A 500 may be retried once that wait has passed. | supported | `source_a.md` | 'a 500 may be retried once that wait has passed' in `source_a.md` -- Source explicitly covers this case. |
| 23 | A 503 is the overload path. | supported | `source_a.md` | 'and a 503 is the overload path' in `source_a.md` -- Exact phrase in source_a. |
| 24 | The four cases are not interchangeable. | supported | `source_a.md` | 'The four cases are not interchangeable.' in `source_a.md` -- Stated explicitly in source_a. |
| 25 | A batch credential is allowed 1000 requests in a window, measured over exactly the same window. | supported | `source_a.md` | 'a credential marked for batch work is allowed 1000 in the same window' in `source_a.md` -- Source supports the 1000 request allowance and same window measurement. |
| 26 | The tier is set on the credential when it is issued. | supported | `source_a.md` | 'The tier is set on the credential when it is issued' in `source_a.md` -- Explicit statement in source_a rule 3. |
| 27 | The tier cannot be asked for per call. | supported | `source_a.md` | 'and cannot be asked for per call' in `source_a.md` -- Source directly states this constraint. |
| 28 | Nothing else about the two tiers differs in any way. | supported | `source_a.md` | 'Nothing else about the two tiers differs in any way.' in `source_a.md` -- Exact statement in source_a. |
| 29 | A caller that cannot say how often it was refused last week cannot argue for a larger cap. | supported | `source_a.md` | 'A caller that cannot say how often it was refused last week cannot argue for a larger cap' in `source_a.md` -- Stated precisely in source_a rule 4. |
| 30 | Nobody at the far end will assemble that argument on the caller's behalf. | supported | `source_a.md` | 'and nobody at the far end will assemble that argument on its behalf' in `source_a.md` -- Source provides this exact statement. |
| 31 | Not all 429 responses are due to caps. | supported | `source_a.md` | 'Not all are caps.' in `source_a.md` -- Source opens the Other refusals section with this statement. |
| 32 | A credential may be suspended as a reason for gateway refusal. | supported | `source_a.md` | 'A credential may be suspended' in `source_a.md` -- Listed as a reason for gateway refusal in source_a. |
| 33 | A route may be closed for maintenance as a reason for gateway refusal. | supported | `source_a.md` | 'a route may be closed for maintenance' in `source_a.md` -- Specified as one of three non-cap refusal reasons. |
| 34 | A body may exceed the 5 megabyte limit as a reason for gateway refusal. | supported | `source_a.md` | 'or a body may exceed the 5 megabyte limit' in `source_a.md` -- Listed as a third refusal reason in source_a. |
| 35 | None of those three reasons clear itself by waiting for a stated number of seconds. | supported | `source_a.md` | 'None of those three clears itself by waiting for a stated number of seconds.' in `source_a.md` -- Source explicitly states this property. |
| 36 | A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service. | supported | `source_a.md` | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `source_a.md` -- Exact statement from source_a. |
| 37 | The log afterwards shows nothing at all except a long run of refusals. | supported | `source_a.md` | 'and the log afterwards shows nothing at all except a long run of refusals' in `source_a.md` -- Source provides this exact description. |
| 38 | Reading the status code rather than the class it belongs to separates the two cases. | supported | `source_a.md` | 'Reading the status code rather than the class it belongs to is what separates the two cases' in `source_a.md` -- Source states this diagnostic principle. |
| 39 | A cap can be raised. | supported | `source_a.md` | 'A cap can be raised' in `source_a.md` -- Opening statement in the Asking for an increase section. |
| 40 | The number of caps raised without a measurement behind them is zero. | supported | `source_a.md` | 'the number of caps raised without a measurement behind them is 0' in `source_a.md` -- Source explicitly quantifies this. |
| 41 | A burst is cheaper to smooth than it is to serve at its peak. | supported | `source_a.md` | 'a burst is cheaper to smooth than it is to serve at its peak' in `source_a.md` -- Stated in source_a. |
| 42 | A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all. | supported | `source_a.md` | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `source_a.md` -- Source provides this statement. |
| 43 | Requests reach the platform team through the usual channel. | supported | `source_a.md` | 'Requests reach the platform team through the usual channel' in `source_a.md` -- Final section of source_a states this. |
| 44 | Requests are answered within two working days. | supported | `source_a.md` | 'they are answered within two working days' in `source_a.md` -- Source specifies this response time. |
| 45 | There is no expedited path. | supported | `source_a.md` | 'There is no expedited path' in `source_a.md` -- Explicitly stated in source_a. |
| 46 | There is no exception list. | supported | `source_a.md` | 'and no exception list' in `source_a.md` -- Final statement in source_a. |

## Structure

**9** mechanical check(s) over **104** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **46** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **98**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 1 run(s) over 45 attributed segment(s) — not conclusive on this evidence base. 6 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

`[-...-]` is what the source said and `{+...+}` is what the merge says.

### Absent and undeclared — in a source, not in the merge, and no record explains it

- `a17` (`source_a.md`) — 'It names the cap and the tier as well.' is not in the merge and no disposition record explains it (nearest merge segment m35 at 0.50)

  ```text
  In the source: It names the cap and the tier as well.
  ```
- `a39` (`source_a.md`) — 'Not all are caps.' is not in the merge and no disposition record explains it (nearest merge segment m36 at 0.62)

  ```text
  In the source: Not all are caps.
  ```
- `a40` (`source_a.md`) — 'The gateway refuses a request for three reasons and only one of them is the one above.' is not in the merge and no disposition record explains it (nearest merge segment m37 at 0.53)

  ```text
  In the source: The gateway refuses a request for three reasons and only one of them is the one above.
  ```
- `b3` (`source_b.md`) — 'When the cap is spent the gateway answers 429 at the edge, without troubling the service behind it.' is not in the merge and no disposition record explains it (nearest merge segment m15 at 0.46)

  ```text
  In the source: When the cap is spent the gateway answers 429 at the edge, without troubling the service behind it.
  ```
- `b16` (`source_b.md`) — 'Waiting longer than the header asks earns nothing, because nobody at this end is keeping score.' is not in the merge and no disposition record explains it (nearest merge segment m14 at 0.50)

  ```text
  In the source: Waiting longer than the header asks earns nothing, because nobody at this end is keeping score.
  ```
- `b17` (`source_b.md`) — 'The response body is JSON and it repeats the cap, the window and the tier as plain fields.' is not in the merge and no disposition record explains it (nearest merge segment m34 at 0.55)

  ```text
  In the source: The response body is JSON and it repeats the cap, the window and the tier as plain fields.
  ```
- `b19` (`source_b.md`) — 'The body is for the human reading the log afterwards.' is not in the merge and no disposition record explains it (nearest merge segment m17 at 0.49)

  ```text
  In the source: The body is for the human reading the log afterwards.
  ```
- `b20` (`source_b.md`) — 'What the client does' is not in the merge and no disposition record explains it (nearest merge segment m35 at 0.44)

  ```text
  In the source: What the client does
  ```
- `b21` (`source_b.md`) — 'There are four rules, and the order they are given in is the order to apply them.' is not in the merge and no disposition record explains it (nearest merge segment m19 at 0.55)

  ```text
  In the source: There are four rules, and the order they are given in is the order to apply them.
  ```
- `b24` (`source_b.md`) — 'On the 503 path the same rule holds, even though the cause of the refusal is an entirely different one.' is not in the merge and no disposition record explains it (nearest merge segment m47 at 0.44)

  ```text
  In the source: On the 503 path the same rule holds, even though the cause of the refusal is an entirely different one.
  ```
- `b25` (`source_b.md`) — 'Anything computed on the client side is a guess.' is not in the merge and no disposition record explains it (nearest merge segment m22 at 0.59)

  ```text
  In the source: Anything computed on the client side is a guess.
  ```
- `b26` (`source_b.md`) — 'That guess is not worth having.' is not in the merge and no disposition record explains it (nearest merge segment m26 at 0.49)

  ```text
  In the source: That guess is not worth having.
  ```
- `b30` (`source_b.md`) — 'That is the behaviour this rule exists to prevent.' is not in the merge and no disposition record explains it (nearest merge segment m31 at 0.41)

  ```text
  In the source: That is the behaviour this rule exists to prevent.
  ```
- `b32` (`source_b.md`) — 'The window, the header and the body are identical to the interactive case, so a client written for one tier needs no change at all to run against the other.' is not in the merge and no disposition record explains it (nearest merge segment m13 at 0.48)

  ```text
  In the source: The window, the header and the body are identical to the interactive case, so a client written for one tier needs no change at all to run against the other.
  ```
- `b36` (`source_b.md`) — 'The counts are the whole of the argument, and without them a request is only a preference.' is not in the merge and no disposition record explains it (nearest merge segment m44 at 0.45)

  ```text
  In the source: The counts are the whole of the argument, and without them a request is only a preference.
  ```
- `b38` (`source_b.md`) — 'The gateway refuses a request for three separate reasons, and only one of them is a cap.' is not in the merge and no disposition record explains it (nearest merge segment m37 at 0.52)

  ```text
  In the source: The gateway refuses a request for three separate reasons, and only one of them is a cap.
  ```
- `b39` (`source_b.md`) — 'Two of the three have nothing to do with how much traffic a caller has sent in the window it is currently in.' is not in the merge and no disposition record explains it (nearest merge segment m38 at 0.42)

  ```text
  In the source: Two of the three have nothing to do with how much traffic a caller has sent in the window it is currently in.
  ```
- `b41` (`source_b.md`) — 'The difference matters more to a retry loop than it does to a reader.' is not in the merge and no disposition record explains it (nearest merge segment m39 at 0.61)

  ```text
  In the source: The difference matters more to a retry loop than it does to a reader.
  ```
- `b42` (`source_b.md`) — 'A loop retrying against a suspended credential burns its whole budget and reaches nothing.' is not in the merge and no disposition record explains it (nearest merge segment m40 at 0.57)

  ```text
  In the source: A loop retrying against a suspended credential burns its whole budget and reaches nothing.
  ```
- `b43` (`source_b.md`) — 'The log afterwards shows a long run of refusals and no successes at all, which reads like an outage and isn’t one — and the wasted budget is the caller’s own.' is not in the merge and no disposition record explains it (nearest merge segment m23 at 0.42)

  ```text
  In the source: The log afterwards shows a long run of refusals and no successes at all, which reads like an outage and isn’t one — and the wasted budget is the caller’s own.
  ```
- `b45` (`source_b.md`) — 'That is the cheapest fix available to anybody, and it is available to almost everybody.' is not in the merge and no disposition record explains it (nearest merge segment m9 at 0.40)

  ```text
  In the source: That is the cheapest fix available to anybody, and it is available to almost everybody.
  ```
- `b46` (`source_b.md`) — 'A cap can be raised, but not on the strength of an assertion that the current one is too small.' is not in the merge and no disposition record explains it (nearest merge segment m43 at 0.43)

  ```text
  In the source: A cap can be raised, but not on the strength of an assertion that the current one is too small.
  ```
- `b48` (`source_b.md`) — 'The team wants to know whether the load is smooth or bursty before it looks at the number at all.' is not in the merge and no disposition record explains it (nearest merge segment m45 at 0.60)

  ```text
  In the source: The team wants to know whether the load is smooth or bursty before it looks at the number at all.
  ```
- `b49` (`source_b.md`) — 'A burst is cheaper to smooth out than it is to serve at its peak.' is not in the merge and no disposition record explains it (nearest merge segment m45 at 0.64)

  ```text
  In the source: A burst is cheaper to smooth out than it is to serve at its peak.
  ```
- `b50` (`source_b.md`) — 'Requests go to the platform team through the usual channel.' is not in the merge and no disposition record explains it (nearest merge segment m47 at 0.65)

  ```text
  In the source: Requests go to the platform team through the usual channel.
  ```
- `b52` (`source_b.md`) — 'An answer takes two working days, and chasing it doesn’t make it take fewer.' is not in the merge and no disposition record explains it (nearest merge segment m45 at 0.37)

  ```text
  In the source: An answer takes two working days, and chasing it doesn’t make it take fewer.
  ```

### Reworded and undeclared — in the merge in altered wording, and no record explains it. At off this also covers layout: a segment whose source line breaks the merge ran together is altered and undeclared, and 380 reuses this kind rather than moving FINDING_KINDS off 12

- `a3` (`source_a.md`) — 'When that cap is spent the gateway answers 429 at the edge — without waking the service behind it — so the refusal costs the platform almost nothing and costs a caller that files it under transport error a great deal.' is reworded in the merge and no disposition record explains it (nearest merge segment m3 at 0.99)

  ```text
  In the source: When that cap is spent the gateway answers 429 at the edge — without waking the service behind it — so the refusal costs the platform almost nothing and costs a caller that files it under transport error a great deal.
  In the merge:  When that cap is spent the gateway answers 429 at the edge without waking the service behind it, so the refusal costs the platform almost nothing and costs a caller that files it under transport error a great deal.
  What changed:  When that cap is spent the gateway answers 429 at the edge [-—-] without waking the service behind [-it —-] {+it,+} so the refusal costs the platform almost nothing and costs a caller that files it under transport error a great deal.
  ```
- `a16` (`source_a.md`) — 'The body of the refusal is JSON, and it names what the gateway calls the “window” it counted in.' is reworded in the merge and no disposition record explains it (nearest merge segment m15 at 0.84)

  ```text
  In the source: The body of the refusal is JSON, and it names what the gateway calls the “window” it counted in.
  In the merge:  The body of the refusal is JSON, and it names what the gateway calls the "window" it counted in, the cap, and the tier as well.
  What changed:  The body of the refusal is JSON, and it names what the gateway calls the [-“window”-] {+"window"+} it counted [-in.-] {+in, the cap, and the tier as well.+}
  ```
- `a19` (`source_a.md`) — 'The body is there so that a human reading a log afterwards can see why the request was refused — nothing in it is meant for the retry loop.' is reworded in the merge and no disposition record explains it (nearest merge segment m17 at 0.99)

  ```text
  In the source: The body is there so that a human reading a log afterwards can see why the request was refused — nothing in it is meant for the retry loop.
  In the merge:  The body is there so that a human reading a log afterwards can see why the request was refused—nothing in it is meant for the retry loop.
  What changed:  The body is there so that a human reading a log afterwards can see why the request was refused[- -]—[- -]nothing in it is meant for the retry loop.
  ```
- `a32` (`source_a.md`) — 'A batch credential is allowed fifty times the default allowance, and it is measured over exactly the same window.' is reworded in the merge and no disposition record explains it (nearest merge segment m29 at 0.75)

  ```text
  In the source: A batch credential is allowed fifty times the default allowance, and it is measured over exactly the same window.
  In the merge:  A batch credential is allowed 1000 requests in a window, measured over exactly the same window.
  ```
- `a44` (`source_a.md`) — 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service — and the log afterwards shows nothing at all except a long run of refusals.' is reworded in the merge and no disposition record explains it (nearest merge segment m40 at 0.99)

  ```text
  In the source: A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service — and the log afterwards shows nothing at all except a long run of refusals.
  In the merge:  A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service—and the log afterwards shows nothing at all except a long run of refusals.
  What changed:  A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service[- -]—[- -]and the log afterwards shows nothing at all except a long run of refusals.
  ```
- `a47` (`source_a.md`) — 'A cap can be raised, and the number of caps raised without a measurement behind them is 0.' is reworded in the merge and no disposition record explains it (nearest merge segment m43 at 0.94)

  ```text
  In the source: A cap can be raised, and the number of caps raised without a measurement behind them is 0.
  In the merge:  A cap can be raised, but the number of caps raised without a measurement behind them is zero.
  What changed:  A cap can be raised, [-and-] {+but+} the number of caps raised without a measurement behind them is [-0.-] {+zero.+}
  ```
- `a49` (`source_a.md`) — 'The platform team looks at whether the load is smooth or bursty — a burst is cheaper to smooth than it is to serve at its peak.' is reworded in the merge and no disposition record explains it (nearest merge segment m45 at 0.99)

  ```text
  In the source: The platform team looks at whether the load is smooth or bursty — a burst is cheaper to smooth than it is to serve at its peak.
  In the merge:  The platform team looks at whether the load is smooth or bursty—a burst is cheaper to smooth than it is to serve at its peak.
  What changed:  The platform team looks at whether the load is smooth or bursty[- -]—[- -]a burst is cheaper to smooth than it is to serve at its peak.
  ```
- `b2` (`source_b.md`) — 'Every credential has a cap of its own.' is reworded in the merge and no disposition record explains it (nearest merge segment m2 at 0.83)

  ```text
  In the source: Every credential has a cap of its own.
  In the merge:  Every credential has a cap.
  What changed:  Every credential has a [-cap of its own.-] {+cap.+}
  ```
- `b18` (`source_b.md`) — 'None of those fields is a substitute for the header, and a caller that parses the body in order to compute its own wait has written code whose only possible future is to disagree with the gateway it is talking to.' is reworded in the merge and no disposition record explains it (nearest merge segment m16 at 0.74)

  ```text
  In the source: None of those fields is a substitute for the header, and a caller that parses the body in order to compute its own wait has written code whose only possible future is to disagree with the gateway it is talking to.
  In the merge:  None of those fields is a substitute for the header, and a caller that parses the body to compute its own wait is doing the same arithmetic twice.
  ```
- `b23` (`source_b.md`) — 'The gateway has already done that arithmetic and it did it with information the caller cannot see.' is reworded in the merge and no disposition record explains it (nearest merge segment m21 at 0.72)

  ```text
  In the source: The gateway has already done that arithmetic and it did it with information the caller cannot see.
  In the merge:  The gateway has already done that arithmetic, with information the caller does not have, and it does the same on the 503 path.
  ```
- `b28` (`source_b.md`) — 'A 200 needs nothing, a 429 needs the stated wait, a 500 can be retried once that wait has passed, and a 503 means the platform itself is overloaded.' is reworded in the merge and no disposition record explains it (nearest merge segment m25 at 0.83)

  ```text
  In the source: A 200 needs nothing, a 429 needs the stated wait, a 500 can be retried once that wait has passed, and a 503 means the platform itself is overloaded.
  In the merge:  A 200 wants nothing, a 429 wants the stated wait, a 500 may be retried once that wait has passed, and a 503 is the overload path.
  What changed:  A 200 [-needs-] {+wants+} nothing, a 429 [-needs-] {+wants+} the stated wait, a 500 [-can-] {+may+} be retried once that wait has passed, and a 503 [-means-] {+is+} the [-platform itself is overloaded.-] {+overload path.+}
  ```
- `b29` (`source_b.md`) — 'A caller that folds all four into one branch will retry hardest during exactly the incident the cap was installed to survive.' is reworded in the merge and no disposition record explains it (nearest merge segment m27 at 0.90)

  ```text
  In the source: A caller that folds all four into one branch will retry hardest during exactly the incident the cap was installed to survive.
  In the merge:  A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive.
  What changed:  A [-caller-] {+client+} that folds [-all four-] {+every non-success+} into one branch will retry hardest during exactly the incident the cap was installed to survive.
  ```
- `b33` (`source_b.md`) — 'Nothing else about the batch tier differs from the default.' is reworded in the merge and no disposition record explains it (nearest merge segment m31 at 0.76)

  ```text
  In the source: Nothing else about the batch tier differs from the default.
  In the merge:  Nothing else about the two tiers differs in any way.
  ```
- `b35` (`source_b.md`) — 'A caller that cannot say how often it was refused can’t make a case for a larger cap, and the platform team won’t assemble that case on its behalf.' is reworded in the merge and no disposition record explains it (nearest merge segment m33 at 0.80)

  ```text
  In the source: A caller that cannot say how often it was refused can’t make a case for a larger cap, and the platform team won’t assemble that case on its behalf.
  In the merge:  A caller that cannot say how often it was refused last week cannot argue for a larger cap, and nobody at the far end will assemble that argument on its behalf.
  ```
- `b44` (`source_b.md`) — 'A caller that can move half its work to a quieter hour usually finds it doesn’t need a larger cap in the first place.' is reworded in the merge and no disposition record explains it (nearest merge segment m46 at 0.68)

  ```text
  In the source: A caller that can move half its work to a quieter hour usually finds it doesn’t need a larger cap in the first place.
  In the merge:  A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all, which is the outcome everyone prefers.
  ```
- `b47` (`source_b.md`) — 'Bring the refusal counts for a full week, the shape of the traffic across the day, and the deadline the traffic exists to meet.' is reworded in the merge and no disposition record explains it (nearest merge segment m44 at 0.81)

  ```text
  In the source: Bring the refusal counts for a full week, the shape of the traffic across the day, and the deadline the traffic exists to meet.
  In the merge:  Bring a week of refusal counts, the shape of the traffic across the day, and the deadline that traffic is serving.
  What changed:  Bring [-the-] {+a week of+} refusal [-counts for a full week,-] {+counts,+} the shape of the traffic across the day, and the deadline [-the-] {+that+} traffic [-exists to meet.-] {+is serving.+}
  ```
- `b51` (`source_b.md`) — 'There is no expedited path.' is reworded in the merge and no disposition record explains it (nearest merge segment m48 at 0.71)

  ```text
  In the source: There is no expedited path.
  In the merge:  There is no expedited path and no exception list.
  ```

### Verbatim violation — an invariant-core token did not survive unchanged

- `a47` (`source_a.md`) — numeric '0' does not survive into the merge unchanged

### Over budget — declared loss past the ceiling

- 4 absent segments are declared replaced by the same replacement (a12, a13, b13, b14), over the ceiling of 3. One replacement standing in for that many segments has not replaced them, it has dropped them: the detail it names is gone from the document
- 6 of 104 segments are declared dropped (5.8%), over the 3% budget

## Review queue

**1** claim(s) the merge declared dropped and the forward pass confirms are gone. Each is a decision to review — put the fact back, or agree it stays out — and none of them is counted as a finding above.

- **B-004** (`source_b.md:5`) — The request count follows the credential wherever the caller places it, including across hosts.
  - left out of: `b7`
  - the merge's reason: Fact that credential follows across hosts is supplementary detail not in base st
  - confirmed absent: the forward pass looked for this claim in `merged.md` and did not find it -- The text mentions spreading across processes but does not state the request count follows across hosts.

> **Over budget.** The merge declared **6** drop(s) of 104 source segment(s), **5.8%**, over the 3% budget: past that share the omissions are the finding, whatever each one says about itself.

## Declarations

The merge declared **23** departure(s) from its sources. Checking them confirms 12, rejects 6, and leaves 5 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 6 of 104 source segment(s) declared gone, **5.8%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a6` | reworded | Changed 'eight' to 'multiple' for greater generality. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-006`) |
| `b1` | superseded | Base document title retained; narrower alternative not used. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Rate limiting and the 429 contract for gateway clients' and says so (no claim traced to it) |
| `b4` | dropped | Explanation of editorial choice about earlier draft removed; not germane to syst | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b5` | dropped | Detail that window start is not disclosed is supplementary context not covered b | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'dropped' is what happened to it (no claim traced to it) |
| `b6` | duplicate | Same fact already stated in source_a.md a5. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b7` | dropped | Fact that credential follows across hosts is supplementary detail not in base st | **confirmed** | declared 'dropped' and every claim from it came back MISSING (`B-004`) |
| `b8` | duplicate | Restates the multi-process throttling point covered by source_a.md a6. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-005`) |
| `b9` | dropped | Editorial context about why 100 requests is sufficient and batch use cases dropp | **rejected** | declared 'dropped', which predicts MISSING; B-006 came back SUPPORTED (`B-006`) |
| `b10` | duplicate | Same reasoning restated; source_a.md a8-a9 retained instead. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b11` | duplicate | Same fact stated in source_a.md a10. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-008`) |
| `a12` | reworded | Simplified without loss of meaning; combined with segments a13-a14. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-009`) |
| `a13` | subsumed | Merged into single sentence covering header value and waiting instruction. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-010`) |
| `a14` | subsumed | Integrated into expanded opening sentence of How to read a refusal section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b13` | superseded | Source_a.md version with same content kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-009`) |
| `b14` | duplicate | Same header fact already stated. | **rejected** | declared 'duplicate', which predicts SUPPORTED; B-011 came back PARTIAL (`B-011`) |
| `b15` | superseded | Source_a.md a14 provides same contract statement. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b22` | superseded | Source_a.md a22-a23 version of rule 1 used instead. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b27` | superseded | Source_a.md a26-a27 version of rule 2 kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-021`) |
| `a31` | dropped | Claim that batch is 'fifty times the default' contradicts explicit numbers (100 | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b31` | dropped | Same '50 times the default' claim contradicts explicit numbers stated in both do | **rejected** | declared 'dropped', which predicts MISSING; B-027 came back SUPPORTED, B-028 came back CONTRADICTED, B-029 came back SUPPORTED (`B-027`, `B-028`, `B-029`) |
| `b34` | superseded | Source_a.md a35-a36 version of rule 4 retained. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-033`, `B-034`) |
| `b37` | superseded | Source_a.md a39 version kept; conveys same fact. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b40` | superseded | Source_a.md a41 lists same three reasons. | **rejected** | declared 'superseded', which predicts SUPPORTED or CONTRADICTED or PARTIAL; B-042 came back MISSING (`B-042`) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | 45fff742d0ed (command) -- lineup haiku-4.5-sub |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | claude-haiku-4-5-20251001 -> claude-haiku-4-5-20251001 |
| Model (decompose) | claude-haiku-4-5-20251001 -> claude-haiku-4-5-20251001 |
| Model (verify) | claude-haiku-4-5-20251001 -> claude-haiku-4-5-20251001 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile subscription, effort decompose one level (extended thinking on/off; default kept), merge one level (extended thinking on/off; default kept), verify one level (extended thinking on/off; default kept) |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 7 live, 0 cached, 0 replayed |
| Tokens | unknown (7 call(s) reported no usage) |
| Cost | unmeasured (7 call(s) reported no tokens, so no figure can be derived) |
| Schema repairs | 1 |
| Isolation | decompose, merge, verify: safe mode, no tools |
| Errors | 0 |
| Duration | 1076.5s |
| Generated | 2026-09-27T18:35:18+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup haiku-4.5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
