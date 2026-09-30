## Verdict

**3 finding(s).** In the structure: 2 false departure, 1 declared loss over budget.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 75 |
| Claims extracted from `source_a.md` | 49 |
| Claims extracted from `source_b.md` | 77 |
| Forward — source claims accounted for in the merge | **126/126** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **49/49** |
| Forward — `source_b.md` claims accounted for | **77/77** |
| Reverse — merge claims found in a source | **75/75** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **201/201** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

None in the claims. The 3 finding(s) this run reports are structural and are listed under `## Structure` below.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 49 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 49 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Every credential has a cap. | 3 | carried | 'Every credential has a cap of its own' in `merged.md` -- The reference states that every credential has its own cap. |
| 2 | When a credential's cap is spent, the gateway answers 429 at the edge without waking the service behind it. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge — without waking the service behind it' in `merged.md` -- The reference states the 429 edge answer without waking the service. |
| 3 | A 429 refusal at the edge costs the platform almost nothing. | 3 | carried | 'so the refusal costs the platform almost nothing' in `merged.md` -- The reference states the refusal costs the platform almost nothing. |
| 4 | Requests are counted against the credential that presented them. | 5 | carried | 'Requests are counted against the credential that presented them' in `merged.md` -- The reference states requests are counted against the presenting credential. |
| 5 | Requests are counted over a fixed window of 60 seconds. | 5 | carried | 'over a fixed window of 60 seconds' in `merged.md` -- The reference states the fixed 60-second window. |
| 6 | Requests are never counted against a connection. | 5 | carried | 'and never against a connection' in `merged.md` -- The reference states requests are never counted against a connection. |
| 7 | Opening a second socket buys a caller nothing in terms of rate limit. | 5 | carried | 'so opening a second socket buys a caller nothing' in `merged.md` -- The reference states a second socket buys a caller nothing. |
| 8 | A client spread across eight worker processes is throttled at exactly the point one process would have been. | 5 | carried | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `merged.md` -- The reference states this directly. |
| 9 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- The reference states the default allowance of 100 requests per window. |
| 10 | A credential marked for batch work is allowed 1000 requests in the same window. | 7 | carried | 'A credential marked for batch work is allowed 1000 in the same window' in `merged.md` -- The reference states batch credentials are allowed 1000 in the same window. |
| 11 | A refusal is not an outage. | 7 | carried | 'A refusal is not an outage' in `merged.md` -- The reference states a refusal is not an outage. |
| 12 | A refusal is the platform declining to spend capacity that has already been promised to somebody else. | 7 | carried | 'It is the platform declining to spend capacity that has already been promised to somebody else' in `merged.md` -- The reference states this directly. |
| 13 | Callers that retry at once are the largest single reason the cap exists. | 7 | carried | 'Callers that retry immediately are most of the reason the cap is there' in `merged.md` -- Being most of the reason entails being the largest single reason for the cap. |
| 14 | The refusal carries a Retry-After header. | 11 | carried | 'Every refusal the gateway sends carries a Retry-After header' in `merged.md` -- The reference states refusals carry a Retry-After header. |
| 15 | The Retry-After header value is a whole number of seconds to wait. | 11 | carried | 'whose value is a whole number of seconds to wait' in `merged.md` -- The reference states the header value is a whole number of seconds. |
| 16 | The gateway keeps no memory of who backed off politely. | 11 | carried | 'The gateway keeps no memory of who backed off politely' in `merged.md` -- The reference states this directly. |
| 17 | Waiting longer than the Retry-After header asks earns a caller no credit. | 11 | carried | 'so waiting longer than the header asks earns a caller no credit at all' in `merged.md` -- The reference states waiting longer earns no credit. |
| 18 | The body of the refusal is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- The reference states the refusal body is JSON. |
| 19 | The refusal body names the window the gateway counted in. | 13 | carried | 'it repeats as plain fields the cap, the tier and what the gateway calls the “window” it counted in' in `merged.md` -- The body includes the window the gateway counted in. |
| 20 | The refusal body names the cap. | 13 | carried | 'it repeats as plain fields the cap, the tier and what the gateway calls the “window” it counted in' in `merged.md` -- The body includes the cap. |
| 21 | The refusal body names the tier. | 13 | carried | 'it repeats as plain fields the cap, the tier and what the gateway calls the “window” it counted in' in `merged.md` -- The body includes the tier. |
| 22 | The refusal body is there so that a human reading a log afterwards can see why the request was refused. | 13 | carried | 'The body is there so that a human reading a log afterwards can see why the request was refused' in `merged.md` -- The reference states this directly. |
| 23 | Nothing in the refusal body is meant for the retry loop. | 13 | carried | 'nothing in it is meant for the retry loop' in `merged.md` -- The reference states nothing in the body is meant for the retry loop. |
| 24 | The gateway computes the wait with information the caller does not have. | 19 | carried | 'The gateway has already done that arithmetic, with information the caller does not have' in `merged.md` -- The reference states the gateway computes the wait with information the caller lacks. |
| 25 | The gateway computes the wait on the 503 path as well. | 19 | carried | 'and it does the same on the 503 path' in `merged.md` -- The reference states the gateway does the same arithmetic on the 503 path. |
| 26 | A 500 may be retried once the stated wait has passed. | 21 | carried | 'a 500 may be retried once that wait has passed' in `merged.md` -- The reference states a 500 may be retried after the stated wait. |
| 27 | A 503 is the overload path. | 21 | carried | 'a 503 means the platform itself is overloaded' in `merged.md` -- The reference describes 503 as platform overload. |
| 28 | A batch credential is allowed fifty times the default allowance. | 23 | carried | 'which is 50 times the default' in `merged.md` -- The reference states the batch allowance is 50 times the default. |
| 29 | A batch credential is measured over exactly the same window as the default. | 23 | carried | 'The window, the header and the body are identical to the interactive case' in `merged.md` -- The reference states the batch window is identical to the interactive case. |
| 30 | The tier is set on the credential when it is issued. | 23 | carried | 'The tier is set on the credential when it is issued' in `merged.md` -- The reference states this directly. |
| 31 | The tier cannot be asked for per call. | 23 | carried | 'cannot be asked for per call' in `merged.md` -- The reference states the tier cannot be asked for per call. |
| 32 | Nothing else about the batch and default tiers differs. | 23 | carried | 'Nothing else about the two tiers differs in any way' in `merged.md` -- The reference states nothing else about the tiers differs. |
| 33 | The refusal log line should carry the credential, the window and the wait. | 25 | carried | 'The log line should carry the credential, the window and the wait' in `merged.md` -- The reference states this directly. |
| 34 | The gateway refuses a request for three reasons. | 29 | carried | 'The gateway refuses a request for three separate reasons' in `merged.md` -- The reference states the gateway refuses for three reasons. |
| 35 | A credential may be suspended. | 29 | carried | 'A credential may be suspended' in `merged.md` -- The reference states this directly. |
| 36 | A route may be closed for maintenance. | 29 | carried | 'a route may be closed for maintenance' in `merged.md` -- The reference states this directly. |
| 37 | The request body limit is 5 megabyte. | 29 | carried | 'a body may exceed the 5 megabyte limit' in `merged.md` -- The reference states the 5 megabyte body limit. |
| 38 | None of the suspended-credential, maintenance, or body-size refusals clears itself by waiting for a stated number of seconds. | 29 | carried | 'None of those three clears itself by waiting for a stated number of seconds' in `merged.md` -- The reference states none of the three clears itself by waiting. |
| 39 | A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `merged.md` -- The reference states this directly. |
| 40 | Reading the status code rather than its class costs one comparison. | 31 | carried | 'Reading the status code rather than the class it belongs to is what separates the two cases, and it costs one comparison' in `merged.md` -- The reference states reading the status code costs one comparison. |
| 41 | A cap can be raised. | 35 | carried | 'A cap can be raised' in `merged.md` -- The reference states a cap can be raised. |
| 42 | The number of caps raised without a measurement behind them is 0. | 35 | carried | 'the number of caps raised without a measurement behind them is 0' in `merged.md` -- The reference states this directly. |
| 43 | The platform team looks at whether the load is smooth or bursty. | 35 | carried | 'the platform team looks at whether the load is smooth or bursty' in `merged.md` -- The reference states this directly. |
| 44 | A burst is cheaper to smooth than it is to serve at its peak. | 35 | carried | 'a burst is cheaper to smooth than it is to serve at its peak' in `merged.md` -- The reference states this directly. |
| 45 | A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap. | 35 | carried | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `merged.md` -- The reference states this directly. |
| 46 | Requests for a cap increase reach the platform team through the usual channel. | 37 | carried | 'Requests reach the platform team through the usual channel' in `merged.md` -- The reference states increase requests go through the usual channel. |
| 47 | Requests for a cap increase are answered within two working days. | 37 | carried | 'they are answered within two working days' in `merged.md` -- The reference states requests are answered within two working days. |
| 48 | There is no expedited path for cap increase requests. | 37 | carried | 'There is no expedited path and no exception list' in `merged.md` -- The reference states there is no expedited path. |
| 49 | There is no exception list for cap increase requests. | 37 | carried | 'There is no expedited path and no exception list' in `merged.md` -- The reference states there is no exception list. |

### `source_b.md` -- 77 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 77 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Every credential has a cap of its own. | 3 | carried | 'Every credential has a cap of its own' in `merged.md` -- The reference states this directly. |
| 2 | When the cap is spent the gateway answers 429 at the edge. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge' in `merged.md` -- The reference states this directly. |
| 3 | When the cap is spent the gateway answers without troubling the service behind it. | 3 | carried | 'without waking the service behind it' in `merged.md` -- Not waking the service means the same as not troubling it. |
| 4 | An earlier draft of this note argued for a client-side token bucket that mirrored the gateway's own counters. | 3 | carried | 'This document deliberately leaves out the client-side token bucket, mirroring the gateway’s own counters, that an earlier draft argued for' in `merged.md` -- The reference states an earlier draft argued for the mirroring token bucket. |
| 5 | Requests are counted against the credential rather than the connection. | 5 | carried | 'Requests are counted against the credential that presented them, over a fixed window of 60 seconds whose start the gateway doesn’t disclose, and never against a connection' in `merged.md` -- The reference states counting is per credential and never per connection. |
| 6 | Requests are counted over a fixed window of 60 seconds. | 5 | carried | 'over a fixed window of 60 seconds' in `merged.md` -- The reference states the fixed 60-second window. |
| 7 | The gateway doesn't disclose the start of the 60-second window. | 5 | carried | 'whose start the gateway doesn’t disclose' in `merged.md` -- The reference states the window start is not disclosed. |
| 8 | There is nothing to be gained by opening more sockets. | 5 | carried | 'so opening a second socket buys a caller nothing' in `merged.md` -- Opening extra sockets gains nothing, which matches the claim. |
| 9 | The request count follows the credential wherever the caller puts it, including across hosts. | 5 | carried | 'The count follows the credential wherever the caller happens to put it, including across hosts' in `merged.md` -- The reference states this directly. |
| 10 | A caller spread over many worker processes is throttled at the same point a single process would have been. | 5 | carried | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `merged.md` -- The multi-process example, together with per-credential counting, carries the claim. |
| 11 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- The reference states this directly. |
| 12 | The default allowance of 100 requests in a window is enough for every interactive use of the API the platform team has seen. | 7 | carried | 'which is enough for every interactive use of this API the platform team has seen' in `merged.md` -- The reference states this directly. |
| 13 | A caller that needs more than the default allowance is almost always doing batch work under an interactive credential. | 7 | carried | 'a caller that needs more than that is almost always doing batch work under an interactive credential' in `merged.md` -- The reference states this directly. |
| 14 | The 429 refusal isn't an outage. | 7 | carried | 'A refusal is not an outage' in `merged.md` -- The reference states a refusal is not an outage. |
| 15 | The 429 refusal isn't a bug in the gateway. | 7 | carried | 'it isn’t a bug in the gateway' in `merged.md` -- The reference states a refusal is not a gateway bug. |
| 16 | The 429 refusal is capacity being held for a request somebody else has already been promised. | 7 | carried | 'It is the platform declining to spend capacity that has already been promised to somebody else' in `merged.md` -- Same meaning: the capacity is held because it was promised to someone else. |
| 17 | Callers that retry immediately are most of the reason the cap is there. | 7 | carried | 'Callers that retry immediately are most of the reason the cap is there' in `merged.md` -- The reference states this directly. |
| 18 | The header on a refusal is called Retry-After. | 11 | carried | 'Every refusal the gateway sends carries a Retry-After header' in `merged.md` -- The header on refusals is named Retry-After. |
| 19 | The Retry-After value is a whole number of seconds. | 11 | carried | 'whose value is a whole number of seconds to wait' in `merged.md` -- The reference states this directly. |
| 20 | The Retry-After header is present on every refusal the gateway sends. | 11 | carried | 'Every refusal the gateway sends carries a Retry-After header' in `merged.md` -- The reference states this directly. |
| 21 | Waiting as long as the Retry-After header specifies and then continuing is the entire contract. | 11 | carried | 'Waiting that long and then continuing is the whole of the contract' in `merged.md` -- The reference states this directly. |
| 22 | Waiting longer than the Retry-After header asks earns nothing. | 11 | carried | 'so waiting longer than the header asks earns a caller no credit at all' in `merged.md` -- The reference states waiting longer earns no credit. |
| 23 | Nobody at the gateway end is keeping score of how long callers wait. | 11 | carried | 'The gateway keeps no memory of who backed off politely' in `merged.md` -- Keeping no memory of polite backoff means no score is kept. |
| 24 | The refusal response body is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- The reference states this directly. |
| 25 | The refusal response body repeats the cap, the window and the tier as plain fields. | 13 | carried | 'it repeats as plain fields the cap, the tier and what the gateway calls the “window” it counted in' in `merged.md` -- The reference states the body repeats cap, tier and window as plain fields. |
| 26 | None of the response body fields is a substitute for the Retry-After header. | 13 | carried | 'None of those fields is a substitute for the header' in `merged.md` -- The reference states this directly. |
| 27 | The response body is for the human reading the log afterwards. | 13 | carried | 'The body is there so that a human reading a log afterwards can see why the request was refused' in `merged.md` -- The reference states the body is for a human reading the log. |
| 28 | There are four rules for what the client does. | 17 | carried | 'There are four rules' in `merged.md` -- The reference states there are four client retry rules. |
| 29 | The order the four client rules are given in is the order to apply them. | 17 | carried | 'the order they are given in is the order to apply them' in `merged.md` -- The reference states this directly. |
| 30 | The client should honour the Retry-After header and not compute its own wait. | 19 | carried | 'Honour the header, every time, and don’t compute your own wait' in `merged.md` -- The reference states this directly. |
| 31 | The gateway computes the wait using information the caller cannot see. | 19 | carried | 'The gateway has already done that arithmetic, with information the caller does not have' in `merged.md` -- The reference states this directly. |
| 32 | On the 503 path the rule of honouring the header also holds. | 19 | carried | 'and it does the same on the 503 path' in `merged.md` -- The gateway computes the wait on the 503 path, so honouring the header applies there too. |
| 33 | The cause of a 503 refusal is entirely different from the cause of a 429 refusal. | 19 | carried | 'even though the cause of that refusal is an entirely different one' in `merged.md` -- The reference states the 503 cause is entirely different. |
| 34 | A wait computed on the client side is a guess. | 19 | carried | 'A wait derived on the client side is a guess about a counter it cannot see' in `merged.md` -- The reference states a client-side wait is a guess. |
| 35 | The client should retry only what is safe to retry. | 21 | carried | 'Retry only what is safe to retry' in `merged.md` -- The reference states this directly. |
| 36 | The set of responses safe to retry is smaller than the set of responses that aren't a success. | 21 | carried | 'which is a smaller set than the set of responses that aren’t a success' in `merged.md` -- The reference states this directly. |
| 37 | A 200 response needs nothing. | 21 | carried | 'A 200 wants nothing' in `merged.md` -- The reference states a 200 wants nothing, which means it needs nothing. |
| 38 | A 429 response needs the stated wait. | 21 | carried | 'a 429 wants the stated wait' in `merged.md` -- The reference states a 429 wants the stated wait. |
| 39 | A 500 response can be retried once the stated wait has passed. | 21 | carried | 'a 500 may be retried once that wait has passed' in `merged.md` -- The reference states this directly. |
| 40 | A 503 response means the platform itself is overloaded. | 21 | carried | 'a 503 means the platform itself is overloaded' in `merged.md` -- The reference states this directly. |
| 41 | A caller that folds 200, 429, 500 and 503 into one branch will retry hardest during exactly the incident the cap was installed to survive. | 21 | carried | 'A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive' in `merged.md` -- Folding all four codes into one branch necessarily folds every non-success, so the statement entails the claim. |
| 42 | A batch credential is allowed 1000 requests in a window. | 23 | carried | 'A batch credential is allowed 1000 requests in a window' in `merged.md` -- The reference states this directly. |
| 43 | The batch allowance of 1000 requests is 50 times the default. | 23 | carried | 'which is 50 times the default' in `merged.md` -- The reference states the batch allowance is 50 times the default. |
| 44 | The batch allowance is not a separate counting scheme. | 23 | carried | 'not a separate counting scheme' in `merged.md` -- The reference states this directly. |
| 45 | The window, the header and the body for the batch tier are identical to the interactive case. | 23 | carried | 'The window, the header and the body are identical to the interactive case' in `merged.md` -- The reference states this directly. |
| 46 | A client written for one tier needs no change to run against the other tier. | 23 | carried | 'so a client written for one tier needs no change at all to run against the other' in `merged.md` -- The reference states this directly. |
| 47 | Nothing else about the batch tier differs from the default. | 23 | carried | 'Nothing else about the two tiers differs in any way' in `merged.md` -- The reference states nothing else differs between the tiers. |
| 48 | The client should log every refusal it sees. | 25 | carried | 'Log every refusal seen' in `merged.md` -- The reference states this directly. |
| 49 | The client should keep the refusal log for at least a week. | 25 | carried | 'keep the log for at least a week' in `merged.md` -- The reference states this directly. |
| 50 | A caller that cannot say how often it was refused can't make a case for a larger cap. | 25 | carried | 'A caller that cannot say how often it was refused last week cannot argue for a larger cap' in `merged.md` -- The reference states this, with the refusal count referring to last week. |
| 51 | The platform team won't assemble the case for a larger cap on a caller's behalf. | 25 | carried | 'nobody at the far end will assemble that argument on its behalf' in `merged.md` -- The far end, meaning the platform side, will not assemble the case for the caller. |
| 52 | The gateway refuses a request for three separate reasons. | 29 | carried | 'The gateway refuses a request for three separate reasons' in `merged.md` -- The reference text states the gateway refuses requests for three separate reasons. |
| 53 | Only one of the gateway's three reasons for refusing a request is a cap. | 29 | carried | 'only one of them is a cap' in `merged.md` -- The reference text states only one of the three reasons is a cap. |
| 54 | Two of the three refusal reasons have nothing to do with how much traffic a caller has sent in the current window. | 29 | carried | 'two of the three have nothing to do with how much traffic a caller has sent in the window it is currently in' in `merged.md` -- The reference text states two of the three reasons are unrelated to traffic sent in the current window. |
| 55 | A credential can be suspended. | 29 | carried | 'A credential may be suspended' in `merged.md` -- The reference text states a credential may be suspended. |
| 56 | A route can be closed while it is being repaired. | 29 | carried | 'a route may be closed for maintenance' in `merged.md` -- Closed for maintenance carries the same meaning as closed while being repaired. |
| 57 | There is a 5 megabyte limit on request bodies. | 29 | carried | 'a body may exceed the 5 megabyte limit' in `merged.md` -- The reference text refers to a 5 megabyte limit on request bodies. |
| 58 | A request body over the 5 megabyte limit is refused before it has been read at all. | 29 | carried | 'a body may exceed the 5 megabyte limit, in which case it is refused before it has been read at all' in `merged.md` -- The reference text states an oversized body is refused before it has been read at all. |
| 59 | A loop retrying against a suspended credential burns its whole budget. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget' in `merged.md` -- Spending its whole budget is the same as burning its whole budget. |
| 60 | A loop retrying against a suspended credential reaches nothing. | 31 | carried | 'without ever reaching the service' in `merged.md` -- The reference text states the loop never reaches the service, matching the claim that it reaches nothing. |
| 61 | The log after retrying against a suspended credential shows a long run of refusals and no successes. | 31 | carried | 'the log afterwards shows nothing but a long run of refusals and no successes' in `merged.md` -- The reference text states the log shows a long run of refusals and no successes. |
| 62 | A run of refusals against a suspended credential is not an outage. | 31 | carried | 'which reads like an outage and isn’t one' in `merged.md` -- The reference text states the run of refusals reads like an outage but is not one. |
| 63 | The budget wasted retrying against a suspended credential is the caller's own. | 31 | carried | 'the wasted budget is the caller’s own' in `merged.md` -- The reference text states the wasted budget is the caller's own. |
| 64 | A caller that can move half its work to a quieter hour usually finds it doesn't need a larger cap. | 33 | carried | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `merged.md` -- Getting what it needs without a cap change means it usually does not need a larger cap. |
| 65 | Moving work to a quieter hour is the cheapest fix available. | 33 | carried | 'the cheapest fix available to almost everybody' in `merged.md` -- The reference text calls moving work to a quieter hour the cheapest fix available. |
| 66 | Moving work to a quieter hour is available to almost everybody. | 33 | carried | 'the cheapest fix available to almost everybody' in `merged.md` -- The reference text states the fix is available to almost everybody. |
| 67 | A cap can be raised. | 33 | carried | 'A cap can be raised' in `merged.md` -- The reference text states a cap can be raised. |
| 68 | A cap is not raised on the strength of an assertion that the current one is too small. | 33 | carried | 'but not on the strength of an assertion that the current one is too small' in `merged.md` -- The reference text states a cap is not raised on the strength of an assertion that it is too small. |
| 69 | A request to raise a cap should include the refusal counts for a full week. | 33 | carried | 'Bring a full week of refusal counts' in `merged.md` -- The reference text asks for a full week of refusal counts. |
| 70 | A request to raise a cap should include the shape of the traffic across the day. | 33 | carried | 'the shape of the traffic across the day' in `merged.md` -- The reference text asks for the shape of the traffic across the day. |
| 71 | A request to raise a cap should include the deadline the traffic exists to meet. | 33 | carried | 'the deadline that traffic is serving' in `merged.md` -- The deadline the traffic is serving is the same as the deadline it exists to meet. |
| 72 | The platform team wants to know whether the load is smooth or bursty before it looks at the number. | 35 | carried | 'Before it looks at the number at all, the platform team looks at whether the load is smooth or bursty' in `merged.md` -- The reference text states the team checks whether the load is smooth or bursty before looking at the number. |
| 73 | A burst is cheaper to smooth out than to serve at its peak. | 35 | carried | 'a burst is cheaper to smooth than it is to serve at its peak' in `merged.md` -- The reference text states a burst is cheaper to smooth than to serve at its peak. |
| 74 | Requests to raise a cap go to the platform team through the usual channel. | 35 | carried | 'Requests reach the platform team through the usual channel' in `merged.md` -- The reference text states requests reach the platform team through the usual channel. |
| 75 | There is no expedited path for cap-raise requests. | 37 | carried | 'There is no expedited path' in `merged.md` -- The reference text states there is no expedited path. |
| 76 | An answer to a cap-raise request takes two working days. | 37 | carried | 'they are answered within two working days' in `merged.md` -- The reference text gives two working days as the answer time, and the following clause says chasing does not shorten it. |
| 77 | Chasing an answer to a cap-raise request doesn't make it take fewer days. | 37 | carried | 'chasing an answer doesn’t make it take fewer' in `merged.md` -- The reference text states chasing an answer does not make it take fewer days. |

### `merged.md` -- 75 claim(s): 0 invented, 0 contradicted, 0 supported in part, 75 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Every credential has a cap of its own. | supported | `source_b.md` | 'Every credential has a cap of its own.' in `source_b.md` -- Source B states this verbatim. |
| 2 | When a credential's cap is spent the gateway answers 429 at the edge. | supported | `source_a.md` | 'When that cap is spent the gateway answers 429 at the edge' in `source_a.md` -- Source A states the gateway answers 429 at the edge when the cap is spent. |
| 3 | When a credential's cap is spent the gateway answers without waking the service behind it. | supported | `source_a.md` | 'without waking the service behind it' in `source_a.md` -- Source A says the refusal happens without waking the service behind it. |
| 4 | A 429 refusal costs the platform almost nothing. | supported | `source_a.md` | 'the refusal costs the platform almost nothing' in `source_a.md` -- Source A states the refusal costs the platform almost nothing. |
| 5 | An earlier draft of the document argued for a client-side token bucket mirroring the gateway's own counters. | supported | `source_b.md` | 'An earlier draft of this note argued for a client-side token bucket that mirrored the gateway’s own counters' in `source_b.md` -- Source B describes the earlier draft's token-bucket argument. |
| 6 | Requests are counted against the credential that presented them. | supported | `source_a.md` | 'Requests are counted against the credential that presented them' in `source_a.md` -- Source A states this directly. |
| 7 | Requests are counted over a fixed window of 60 seconds. | supported | `source_a.md` | 'over a fixed window of 60 seconds' in `source_a.md` -- Source A gives the fixed 60-second window. |
| 8 | The gateway doesn't disclose the start of the 60-second counting window. | supported | `source_b.md` | 'whose start the gateway doesn’t disclose' in `source_b.md` -- Source B says the gateway doesn't disclose the window's start. |
| 9 | Requests are never counted against a connection. | supported | `source_a.md` | 'and never against a connection' in `source_a.md` -- Source A says requests are never counted against a connection. |
| 10 | The request count follows the credential wherever the caller puts it, including across hosts. | supported | `source_b.md` | 'The count follows the credential wherever the caller happens to put it, including across hosts.' in `source_b.md` -- Source B states this directly. |
| 11 | Opening a second socket buys a caller nothing in terms of rate limit. | supported | `source_a.md` | 'Opening a second socket therefore buys a caller nothing.' in `source_a.md` -- Source A states a second socket buys the caller nothing. |
| 12 | A client spread across eight worker processes is throttled at exactly the point one process would have been. | supported | `source_a.md` | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `source_a.md` -- Source A states this with the eight-process example. |
| 13 | The default allowance is 100 requests in a window. | supported | `source_a.md` | 'The default allowance is 100 requests in a window' in `source_a.md` -- Both sources give a default allowance of 100 requests per window. |
| 14 | The default allowance of 100 requests is enough for every interactive use of the API the platform team has seen. | supported | `source_b.md` | 'which is enough for every interactive use of this API the platform team has seen' in `source_b.md` -- Source B says the default is enough for every interactive use the team has seen. |
| 15 | A caller that needs more than the default allowance is almost always doing batch work under an interactive credential. | supported | `source_b.md` | 'a caller that needs more than that is almost always doing batch work under an interactive credential' in `source_b.md` -- Source B states this directly. |
| 16 | A credential marked for batch work is allowed 1000 requests in the same window. | supported | `source_a.md` | 'a credential marked for batch work is allowed 1000 in the same window' in `source_a.md` -- Source A gives the batch allowance of 1000 in the same window. |
| 17 | A 429 refusal is not an outage. | supported | `source_a.md` | 'A refusal is not an outage' in `source_a.md` -- Source A states a refusal is not an outage. |
| 18 | A 429 refusal isn't a bug in the gateway. | supported | `source_b.md` | 'it isn’t a bug in the gateway' in `source_b.md` -- Source B says the refusal isn't a bug in the gateway. |
| 19 | A 429 refusal is the platform declining to spend capacity that has already been promised to somebody else. | supported | `source_a.md` | 'It is the platform declining to spend capacity that has already been promised to somebody else' in `source_a.md` -- Source A states this directly. |
| 20 | Callers that retry immediately are most of the reason the cap exists. | supported | `source_b.md` | 'Callers that retry immediately are most of the reason the cap is there.' in `source_b.md` -- Source B states immediate retriers are most of the reason for the cap. |
| 21 | Every refusal the gateway sends carries a Retry-After header. | supported | `source_b.md` | 'it is present on every refusal the gateway sends' in `source_b.md` -- Source B says the Retry-After header is present on every refusal. |
| 22 | The Retry-After header's value is a whole number of seconds to wait. | supported | `source_a.md` | 'Its value is a whole number of seconds to wait.' in `source_a.md` -- Source A states the header value is a whole number of seconds to wait. |
| 23 | The gateway keeps no memory of who backed off politely. | supported | `source_a.md` | 'The gateway keeps no memory of who backed off politely' in `source_a.md` -- Source A states this directly. |
| 24 | Waiting longer than the Retry-After header asks earns a caller no credit. | supported | `source_a.md` | 'waiting longer than the header asks earns a caller no credit at all' in `source_a.md` -- Source A states waiting longer earns no credit. |
| 25 | The body of the refusal is JSON. | supported | `source_a.md` | 'The body of the refusal is JSON' in `source_a.md` -- Source A states the refusal body is JSON. |
| 26 | The refusal body repeats as plain fields the cap, the tier and the window the gateway counted in. | supported | `source_b.md` | 'it repeats the cap, the window and the tier as plain fields' in `source_b.md` -- Source B says the body repeats cap, window and tier as plain fields. |
| 27 | The refusal body is there so that a human reading a log afterwards can see why the request was refused. | supported | `source_a.md` | 'The body is there so that a human reading a log afterwards can see why the request was refused' in `source_a.md` -- Source A states this directly. |
| 28 | Nothing in the refusal body is meant for the retry loop. | supported | `source_a.md` | 'nothing in it is meant for the retry loop' in `source_a.md` -- Source A says nothing in the body is meant for the retry loop. |
| 29 | There are four rules for retrying. | supported | `source_b.md` | 'There are four rules' in `source_b.md` -- Source B states there are four rules. |
| 30 | The retry rules are to be applied in the order they are given. | supported | `source_b.md` | 'the order they are given in is the order to apply them' in `source_b.md` -- Source B says the rules are applied in the given order. |
| 31 | The gateway computes the wait with information the caller does not have. | supported | `source_a.md` | 'with information the caller does not have' in `source_a.md` -- Source A says the gateway computed the wait with information the caller lacks. |
| 32 | The gateway also computes the wait on the 503 path. | supported | `source_a.md` | 'and it does the same on the 503 path' in `source_a.md` -- Source A says the gateway does the same arithmetic on the 503 path. |
| 33 | The cause of a 503 refusal is entirely different from that of a 429. | supported | `source_b.md` | 'On the 503 path the same rule holds, even though the cause of the refusal is an entirely different one.' in `source_b.md` -- Source B says the 503 refusal has an entirely different cause. |
| 34 | The set of responses safe to retry is smaller than the set of non-success responses. | supported | `source_b.md` | 'which is a smaller set than the set of responses that aren’t a success' in `source_b.md` -- Source B states the retry-safe set is smaller than the non-success set. |
| 35 | A 200 response wants nothing. | supported | `source_a.md` | 'A 200 wants nothing' in `source_a.md` -- Source A states this directly. |
| 36 | A 429 response wants the stated wait. | supported | `source_a.md` | 'a 429 wants the stated wait' in `source_a.md` -- Source A states this directly. |
| 37 | A 500 response may be retried once the stated wait has passed. | supported | `source_a.md` | 'a 500 may be retried once that wait has passed' in `source_a.md` -- Source A states this directly. |
| 38 | A 503 response means the platform itself is overloaded. | supported | `source_b.md` | 'a 503 means the platform itself is overloaded' in `source_b.md` -- Source B states this directly. |
| 39 | The four response cases (200, 429, 500, 503) are not interchangeable. | supported | `source_a.md` | 'The four cases are not interchangeable.' in `source_a.md` -- Source A states the four cases are not interchangeable. |
| 40 | A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive. | supported | `source_a.md` | 'A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive.' in `source_a.md` -- Source A states this verbatim. |
| 41 | A batch credential is allowed 1000 requests in a window. | supported | `source_b.md` | 'A batch credential is allowed 1000 requests in a window' in `source_b.md` -- Source B states this directly. |
| 42 | The batch allowance is 50 times the default. | supported | `source_b.md` | 'which is 50 times the default' in `source_b.md` -- Source B (and Source A) state the batch allowance is 50 times the default. |
| 43 | The batch allowance is not a separate counting scheme. | supported | `source_b.md` | 'not a separate counting scheme' in `source_b.md` -- Source B states the batch allowance is not a separate counting scheme. |
| 44 | The window, the header and the body for batch credentials are identical to the interactive case. | supported | `source_b.md` | 'The window, the header and the body are identical to the interactive case' in `source_b.md` -- Source B states this directly. |
| 45 | A client written for one tier needs no change to run against the other tier. | supported | `source_b.md` | 'so a client written for one tier needs no change at all to run against the other' in `source_b.md` -- Source B states this directly. |
| 46 | The tier is set on the credential when it is issued. | supported | `source_a.md` | 'The tier is set on the credential when it is issued' in `source_a.md` -- Source A states this directly. |
| 47 | The tier cannot be requested per call. | supported | `source_a.md` | 'cannot be asked for per call' in `source_a.md` -- Source A says the tier cannot be asked for per call. |
| 48 | Nothing else about the batch and interactive tiers differs. | supported | `source_a.md` | 'Nothing else about the two tiers differs in any way.' in `source_a.md` -- Source A states nothing else differs between the tiers. |
| 49 | Callers should log every refusal seen. | supported | `source_a.md` | 'Log every refusal seen.' in `source_a.md` -- Source A instructs logging every refusal seen. |
| 50 | Callers should keep the refusal log for at least a week. | supported | `source_b.md` | 'keep the log for at least a week' in `source_b.md` -- Source B says to keep the log for at least a week. |
| 51 | Nobody at the far end will assemble the argument for a larger cap on a caller's behalf. | supported | `source_a.md` | 'nobody at the far end will assemble that argument on its behalf' in `source_a.md` -- Source A states this directly. |
| 52 | The refusal log line should carry the credential, the window and the wait. | supported | `source_a.md` | 'The log line should carry the credential, the window and the wait.' in `source_a.md` -- Source A states this verbatim. |
| 53 | Not all refusals are caps. | supported | `source_a.md` | 'Not all are caps.' in `source_a.md` -- Source A states not all refusals are caps. |
| 54 | The gateway refuses a request for three separate reasons. | supported | `source_b.md` | 'The gateway refuses a request for three separate reasons' in `source_b.md` -- Source B states this directly. |
| 55 | Only one of the gateway's refusal reasons is a cap. | supported | `source_b.md` | 'and only one of them is a cap' in `source_b.md` -- Source B says only one of the three reasons is a cap. |
| 56 | Two of the three refusal reasons have nothing to do with how much traffic a caller has sent in the current window. | supported | `source_b.md` | 'Two of the three have nothing to do with how much traffic a caller has sent in the window it is currently in.' in `source_b.md` -- Source B states this directly. |
| 57 | A credential may be suspended. | supported | `source_a.md` | 'A credential may be suspended' in `source_a.md` -- Source A states this directly. |
| 58 | A route may be closed for maintenance. | supported | `source_a.md` | 'a route may be closed for maintenance' in `source_a.md` -- Source A states this directly. |
| 59 | The request body limit is 5 megabyte. | supported | `source_a.md` | 'a body may exceed the 5 megabyte limit' in `source_a.md` -- Source A gives the 5 megabyte body limit. |
| 60 | A body exceeding the 5 megabyte limit is refused before it has been read at all. | supported | `source_b.md` | 'a request body over the 5 megabyte limit is refused before it has been read at all' in `source_b.md` -- Source B states this directly. |
| 61 | A suspended credential, a route closed for maintenance and an oversized body do not clear by waiting for a stated number of seconds. | supported | `source_a.md` | 'None of those three clears itself by waiting for a stated number of seconds.' in `source_a.md` -- Source A states none of the three clears by waiting. |
| 62 | A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service. | supported | `source_a.md` | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `source_a.md` -- Source A states this directly. |
| 63 | The log of a loop retrying against a suspended credential shows nothing but a long run of refusals and no successes. | supported | `source_b.md` | 'The log afterwards shows a long run of refusals and no successes at all' in `source_b.md` -- Source B states the log shows only refusals and no successes. |
| 64 | Reading the status code rather than its class costs one comparison. | supported | `source_a.md` | 'Reading the status code rather than the class it belongs to is what separates the two cases, and it costs one comparison.' in `source_a.md` -- Source A states reading the status code costs one comparison. |
| 65 | A cap can be raised. | supported | `source_a.md` | 'A cap can be raised' in `source_a.md` -- Both sources state a cap can be raised. |
| 66 | The number of caps raised without a measurement behind them is 0. | supported | `source_a.md` | 'the number of caps raised without a measurement behind them is 0' in `source_a.md` -- Source A states this directly. |
| 67 | A cap increase request should bring a full week of refusal counts, the shape of the traffic across the day, and the deadline that traffic is serving. | supported | `source_b.md` | 'Bring the refusal counts for a full week, the shape of the traffic across the day, and the deadline the traffic exists to meet.' in `source_b.md` -- Source B lists the same three items including a full week of counts. |
| 68 | The platform team looks at whether the load is smooth or bursty before looking at the number. | supported | `source_b.md` | 'The team wants to know whether the load is smooth or bursty before it looks at the number at all.' in `source_b.md` -- Source B states this directly. |
| 69 | A burst is cheaper to smooth than to serve at its peak. | supported | `source_a.md` | 'a burst is cheaper to smooth than it is to serve at its peak' in `source_a.md` -- Source A states this directly. |
| 70 | A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap. | supported | `source_a.md` | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `source_a.md` -- Source A states this directly. |
| 71 | Cap increase requests reach the platform team through the usual channel. | supported | `source_a.md` | 'Requests reach the platform team through the usual channel' in `source_a.md` -- Source A states this directly. |
| 72 | Cap increase requests are answered within two working days. | supported | `source_a.md` | 'they are answered within two working days' in `source_a.md` -- Source A states requests are answered within two working days. |
| 73 | Chasing an answer to a cap increase request doesn't make it take fewer days. | supported | `source_b.md` | 'chasing it doesn’t make it take fewer' in `source_b.md` -- Source B states chasing doesn't shorten the wait. |
| 74 | There is no expedited path for cap increase requests. | supported | `source_a.md` | 'There is no expedited path' in `source_a.md` -- Both sources state there is no expedited path. |
| 75 | There is no exception list for cap increase requests. | supported | `source_a.md` | 'no exception list' in `source_a.md` -- Source A states there is no exception list. |

## Structure

**9** mechanical check(s) over **104** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **75** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **126**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 27 run(s) over 48 attributed segment(s) — sources interleaved. 6 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

`[-...-]` is what the source said and `{+...+}` is what the merge says.

### Declared gone, still here — a record says the content departed and the merge carries the segment unchanged

- `b36` (`source_b.md`) — 'The counts are the whole of the argument, and without them a request is only a preference.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: The counts are the whole of the argument, and without them a request is only a preference.
  In the merge:  the counts are the whole of the argument, and without them a request is only a preference.
  What changed:  [-T-]{+t+}he counts are the whole of the argument, and without them a request is only a preference.
  ```
- `b39` (`source_b.md`) — 'Two of the three have nothing to do with how much traffic a caller has sent in the window it is currently in.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Two of the three have nothing to do with how much traffic a caller has sent in the window it is currently in.
  In the merge:  two of the three have nothing to do with how much traffic a caller has sent in the window it is currently in.
  What changed:  [-T-]{+t+}wo of the three have nothing to do with how much traffic a caller has sent in the window it is currently in.
  ```

### Over budget — declared loss past the ceiling

- 4 absent segments are declared replaced by the same replacement (a12, a13, b13, b14), over the ceiling of 3. One replacement standing in for that many segments has not replaced them, it has dropped them: the detail it names is gone from the document

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **79** departure(s) from its sources. Checking them confirms 60, rejects 2, and leaves 17 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 104 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a2` | superseded | Opening sentence: source_b wording kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`A-001`) |
| `b3` | duplicate | a3 carries the same edge refusal fact. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-002`, `B-003`) |
| `b4` | reworded | Token bucket omission restated in general terms. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-004`) |
| `a4` | reconciled | Counting rule combined with undisclosed window start. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-004`, `A-005`, `A-006`) |
| `b5` | reconciled | Counting rule combined with undisclosed window start. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-005`, `B-006`, `B-007`) |
| `a5` | reworded | Joined with the across-hosts statement. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-007`) |
| `b7` | subsumed | Across-hosts fact carried in the joined sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-009`) |
| `b6` | duplicate | Same point as a5. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-008`) |
| `b8` | duplicate | a6 carries the worker-process point more specifically. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-010`) |
| `a7` | reworded | Allowance sentence split around source_b's interactive-use detail. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-009`, `A-010`) |
| `b9` | subsumed | Default allowance and interactive-use detail merged. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-011`, `B-012`, `B-013`) |
| `a8` | reworded | Adds source_b's not-a-bug point. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-011`) |
| `b10` | subsumed | Not-outage and held-capacity points carried by a8 and a9. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-014`, `B-015`, `B-016`) |
| `a10` | superseded | source_b wording chosen; see decision. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`A-013`) |
| `a12` | reconciled | Header presence combined with every-refusal detail. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-014`) |
| `b14` | reconciled | Header presence combined with every-refusal detail. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-019`, `B-020`) |
| `a13` | subsumed | Header value folded into header sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-015`) |
| `b13` | subsumed | Header name carried in the combined sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-018`) |
| `a14` | reworded | Adds source_b's purpose clause. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b15` | subsumed | Contract and purpose carried; aside folded in. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-021`) |
| `b16` | duplicate | a15 states the same point. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-022`, `B-023`) |
| `a16` | reworded | Body fields combined into one sentence. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-018`, `A-019`) |
| `a17` | subsumed | Cap and tier listed in combined sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-020`, `A-021`) |
| `b17` | subsumed | Plain-fields detail carried in combined sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-024`, `B-025`) |
| `a18` | reworded | Joined with source_b's consequence clause. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b18` | subsumed | Disagreement consequence carried in joined sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-026`) |
| `b19` | duplicate | a19 states the same purpose. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-027`) |
| `b12` | duplicate | Identical heading to a11. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b20` | superseded | Base heading kept; see decision. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a21` | superseded | source_b wording is a full sentence. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a22` | reworded | Rule 1 heading combined with source_b's. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b22` | subsumed | Rule 1 heading combined with a22. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-030`) |
| `a23` | reworded | Adds source_b's different-cause clause. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-024`, `A-025`) |
| `b23` | duplicate | a23 states the same point. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-031`) |
| `b24` | subsumed | 503 rule and different cause carried. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-032`, `B-033`) |
| `a24` | reworded | Joined with a25. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a25` | reworded | Joined with a24. | **rejected** | declared 'reworded', and its text is in the merge (no claim traced to it) |
| `b25` | duplicate | a24 carries the same point. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-034`) |
| `b26` | duplicate | a25 carries the same point. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `a26` | superseded | source_b's fuller rule 2 heading kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a27` | reworded | 503 case stated with source_b's clearer wording. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-026`, `A-027`) |
| `b28` | subsumed | Status-code cases carried in one sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-037`, `B-038`, `B-039`, `B-040`) |
| `b29` | duplicate | a29 states the same point. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-041`) |
| `a30` | reworded | Joined with b30. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b30` | subsumed | Joined with a30. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a32` | subsumed | Multiplier and same window carried by b31 and b32. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-028`, `A-029`) |
| `b33` | duplicate | a34 states the same point. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-047`) |
| `a35` | reworded | Adds source_b's retention period. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b34` | subsumed | Retention carried in rule 4 heading. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-048`, `B-049`) |
| `a36` | reworded | Joined with b36. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b35` | duplicate | a36 states the same point. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-050`, `B-051`) |
| `b36` | subsumed | Joined onto a36. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b37` | superseded | Base heading kept; see decision. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a39` | reworded | Completed the elliptical sentence. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a40` | reworded | Joined with b38 and b39. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-034`) |
| `b38` | subsumed | Same statement as a40. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-052`, `B-053`) |
| `b39` | subsumed | Joined onto the three-reasons sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-054`) |
| `a41` | reworded | Adds source_b's before-read detail. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-035`, `A-036`, `A-037`) |
| `b40` | subsumed | Three causes and before-read detail carried. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-055`, `B-056`, `B-057`, `B-058`) |
| `a43` | reworded | Takes source_b's comparison. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b41` | subsumed | Same point as a43. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a44` | reworded | Joined with b43's outage point. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-039`) |
| `b42` | duplicate | a44 states the same point. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-059`, `B-060`) |
| `b43` | subsumed | Log and budget points carried. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-061`, `B-062`, `B-063`) |
| `a47` | reworded | Joined with b46. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-041`, `A-042`) |
| `b46` | subsumed | Joined with a47. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-067`, `B-068`) |
| `a48` | reworded | Adds full from b47. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b47` | subsumed | Same list as a48. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-069`, `B-070`, `B-071`) |
| `a49` | reworded | Adds source_b's ordering detail. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-043`, `A-044`) |
| `b48` | subsumed | Ordering detail carried. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-072`) |
| `b49` | duplicate | a49 states the same point. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-073`) |
| `a50` | reworded | Joined with b45. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-045`) |
| `b44` | duplicate | a50 states the same point. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-064`) |
| `b45` | subsumed | Cheapest-fix point joined onto a50. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-065`, `B-066`) |
| `a51` | reworded | Adds source_b's chasing point. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-046`, `A-047`) |
| `b50` | duplicate | a51 states the same point. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-074`) |
| `b52` | subsumed | Timing and chasing point carried. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-076`, `B-077`) |
| `b51` | duplicate | a52 states the same point. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-075`) |
| `b1` | superseded | Base title kept; see decision. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Rate limiting and the 429 contract for gateway clients' and says so (no claim traced to it) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | 31c2462e2828 (command) -- lineup opus-5.5-sub |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | claude-opus-5-5 -> claude-opus-5-5 |
| Model (decompose) | claude-opus-5-5 -> claude-opus-5-5 |
| Model (verify) | claude-opus-5-5 -> claude-opus-5-5 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile subscription, effort decompose=medium, merge=medium, verify=medium |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 7 live, 0 cached, 0 replayed |
| Tokens | unknown (7 call(s) reported no usage) |
| Cost | unmeasured (7 call(s) reported no tokens, so no figure can be derived) |
| Schema repairs | 0 |
| Isolation | decompose, merge, verify: safe mode, no tools |
| Errors | 0 |
| Duration | 385.2s |
| Generated | 2026-09-27T17:50:28+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup opus-5.5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
