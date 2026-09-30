## Verdict

**14 finding(s).** In the claims: 2 partially dropped. In the structure: 2 undeclared absence, 10 undeclared rewording.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 82 |
| Claims extracted from `source_a.md` | 61 |
| Claims extracted from `source_b.md` | 67 |
| Forward — source claims accounted for in the merge | **126/128** |
| Forward — carried only in part | 2 |
| Forward — `source_a.md` claims accounted for | **61/61** |
| Forward — `source_b.md` claims accounted for | **65/67** (2 in part) |
| Reverse — merge claims found in a source | **82/82** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **210/210** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Partly dropped — the merge carries some of this claim

- **B-026** (`source_b.md:13`) — The response body repeats the window as a plain field.
  - evidence: 'it names what the gateway calls the “window” it counted in.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The body names the window, but the text does not specify that the window is a plain field.
- **B-048** (`source_b.md:25`) — A caller that cannot say how often it was refused cannot make a case for a larger cap.
  - evidence: 'A caller that cannot say how often it was refused last week cannot argue for a larger cap' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text says the caller must know how often it was refused last week, but does not state the claim without that timeframe.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 61 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 61 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Every credential has a cap. | 3 | carried | 'Every credential has a cap.' in `merged.md` -- The reference states that every credential has a cap. |
| 2 | When a credential's cap is spent, the gateway answers 429 at the edge. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge' in `merged.md` -- The reference says the gateway answers 429 at the edge when the cap is spent. |
| 3 | The gateway answers 429 without waking the service behind it. | 3 | carried | 'without waking the service behind it' in `merged.md` -- The reference states the gateway does not wake the service behind it. |
| 4 | Requests are counted against the credential that presented them. | 5 | carried | 'Requests are counted against the credential that presented them' in `merged.md` -- The reference identifies the presenting credential as the basis for counting requests. |
| 5 | Requests are counted over a fixed window of 60 seconds. | 5 | carried | 'over a fixed window of 60 seconds' in `merged.md` -- The reference specifies a fixed 60-second counting window. |
| 6 | Requests are never counted against a connection. | 5 | carried | 'and never against a connection' in `merged.md` -- The reference explicitly says requests are never counted against a connection. |
| 7 | A client spread across eight worker processes is throttled at exactly the point one process would have been. | 5 | carried | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `merged.md` -- The reference states that eight worker processes are throttled at the same point as one process. |
| 8 | A client spread across eight worker processes pays for the extra file descriptors. | 5 | carried | 'and pays for the extra file descriptors as well' in `merged.md` -- The reference says the multi-process client pays for the extra file descriptors. |
| 9 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- The reference gives the default allowance as 100 requests per window. |
| 10 | A credential marked for batch work is allowed 1000 requests in the same window. | 7 | carried | 'a credential marked for batch work is allowed 1000 in the same window' in `merged.md` -- The reference states that batch credentials are allowed 1000 in the same window. |
| 11 | A refusal is not an outage. | 7 | carried | 'A refusal is not an outage' in `merged.md` -- The reference explicitly says a refusal is not an outage. |
| 12 | The platform declines to spend capacity that has already been promised to somebody else. | 7 | carried | 'the platform declining to spend capacity that has already been promised to somebody else' in `merged.md` -- The reference describes the refusal as the platform declining to spend already-promised capacity. |
| 13 | Callers that retry at once are the largest single reason the cap exists. | 7 | carried | 'Callers that retry at once are the largest single reason the cap is there at all.' in `merged.md` -- The reference identifies callers retrying at once as the cap's largest single reason. |
| 14 | The refusal carries a Retry-After header. | 11 | carried | 'The refusal carries a Retry-After header' in `merged.md` -- The reference states that a refusal carries a Retry-After header. |
| 15 | The Retry-After header value is a whole number of seconds to wait. | 11 | carried | 'Its value is a whole number of seconds to wait.' in `merged.md` -- The reference specifies that the header value is a whole number of seconds to wait. |
| 16 | The gateway keeps no memory of who backed off politely. | 11 | carried | 'The gateway keeps no memory of who backed off politely' in `merged.md` -- The reference states that the gateway keeps no memory of callers who backed off politely. |
| 17 | Waiting longer than the header asks earns a caller no credit. | 11 | carried | 'waiting longer than the header asks earns a caller no credit at all' in `merged.md` -- The reference says waiting longer than requested by the header earns no credit. |
| 18 | The body of the refusal is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- The reference identifies the refusal body as JSON. |
| 19 | The body names what the gateway calls the “window” it counted in. | 13 | carried | 'it names what the gateway calls the “window” it counted in' in `merged.md` -- The reference says the body names the window used for counting. |
| 20 | The body names the cap. | 13 | carried | 'It names the cap' in `merged.md` -- The reference states that the body names the cap. |
| 21 | The body names the tier. | 13 | carried | 'and the tier as plain fields as well' in `merged.md` -- The reference states that the body names the tier as a plain field. |
| 22 | None of the body fields is a substitute for the header. | 13 | carried | 'None of those fields is a substitute for the header' in `merged.md` -- The reference says none of the body fields substitutes for the header. |
| 23 | A caller that parses the body to compute its own wait is doing the same arithmetic twice. | 13 | carried | 'a caller that parses the body to compute its own wait is doing the same arithmetic twice' in `merged.md` -- The reference says computing a wait from the body repeats the arithmetic. |
| 24 | The body is there so that a human reading a log afterwards can see why the request was refused. | 13 | carried | 'The body is there so that a human reading a log afterwards can see why the request was refused' in `merged.md` -- The reference says the body lets a human see the reason for refusal in a later log review. |
| 25 | Nothing in the body is meant for the retry loop. | 13 | carried | 'nothing in it is meant for the retry loop' in `merged.md` -- The reference states that nothing in the body is intended for the retry loop. |
| 26 | The gateway has already done the arithmetic using information the caller does not have. | 19 | carried | 'The gateway has already done that arithmetic, with information the caller does not have' in `merged.md` -- The text states that the gateway has done the arithmetic using information unavailable to the caller. |
| 27 | The gateway does the same arithmetic on the 503 path. | 19 | carried | 'and it does the same on the 503 path' in `merged.md` -- The text explicitly says the gateway does the same arithmetic on the 503 path. |
| 28 | A wait derived on the client side is a guess about a counter the client cannot see. | 19 | carried | 'A wait derived on the client side is a guess about a counter it cannot see.' in `merged.md` -- The text directly describes a client-derived wait as a guess about an unseen counter. |
| 29 | A 200 wants nothing. | 21 | carried | 'A 200 wants nothing' in `merged.md` -- The text explicitly says that a 200 wants nothing. |
| 30 | A 429 wants the stated wait. | 21 | carried | 'a 429 wants the stated wait' in `merged.md` -- The text explicitly says that a 429 wants the stated wait. |
| 31 | A 500 may be retried once that wait has passed. | 21 | carried | 'a 500 may be retried once that wait has passed' in `merged.md` -- The text explicitly permits retrying a 500 after the wait has passed. |
| 32 | A 503 is the overload path. | 21 | carried | 'a 503 is the overload path' in `merged.md` -- The text directly identifies a 503 as the overload path. |
| 33 | The four cases are not interchangeable. | 21 | carried | 'The four cases are not interchangeable.' in `merged.md` -- The text directly states that the four cases are not interchangeable. |
| 34 | A client that folds every non-success into one branch will retry hardest during the incident the cap was installed to survive. | 21 | carried | 'A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive.' in `merged.md` -- The text directly states that such a client will retry hardest during the incident the cap was installed to survive. |
| 35 | A batch credential is allowed fifty times the default allowance. | 23 | carried | 'A batch credential is allowed fifty times the default allowance' in `merged.md` -- The text explicitly gives a batch credential fifty times the default allowance. |
| 36 | A batch credential is measured over exactly the same window as the default allowance. | 23 | carried | 'A batch credential is allowed fifty times the default allowance, and it is measured over exactly the same window.' in `merged.md` -- The text states that the batch credential is measured over exactly the same window. |
| 37 | The tier is set on the credential when it is issued. | 23 | carried | 'The tier is set on the credential when it is issued' in `merged.md` -- The text directly states when the tier is set. |
| 38 | The tier cannot be asked for per call. | 23 | carried | 'and cannot be asked for per call' in `merged.md` -- The text explicitly says the tier cannot be asked for per call. |
| 39 | Nothing else about the two tiers differs in any way. | 23 | carried | 'Nothing else about the two tiers differs in any way.' in `merged.md` -- The text directly states that nothing else differs between the tiers. |
| 40 | A caller that cannot say how often it was refused last week cannot argue for a larger cap. | 25 | carried | 'A caller that cannot say how often it was refused last week cannot argue for a larger cap' in `merged.md` -- The text directly says a caller unable to report last week's refusals cannot argue for a larger cap. |
| 41 | Nobody at the far end will assemble that argument on the caller's behalf. | 25 | carried | 'nobody at the far end will assemble that argument on its behalf' in `merged.md` -- The text explicitly says nobody at the far end will assemble the argument for the caller. |
| 42 | The log line should carry the credential, the window and the wait. | 25 | carried | 'The log line should carry the credential, the window and the wait.' in `merged.md` -- The text directly lists the credential, window, and wait as contents of the log line. |
| 43 | The gateway refuses a request for three reasons. | 29 | carried | 'The gateway refuses a request for three reasons' in `merged.md` -- The text directly states that the gateway refuses requests for three reasons. |
| 44 | Only one of the gateway's three refusal reasons is the cap described above. | 29 | carried | 'and only one of them is the cap described above' in `merged.md` -- The text says only one of the three refusal reasons is the cap. |
| 45 | A credential may be suspended. | 29 | carried | 'A credential may be suspended' in `merged.md` -- The text explicitly identifies a suspended credential as a possible refusal reason. |
| 46 | A route may be closed for maintenance. | 29 | carried | 'a route may be closed for maintenance' in `merged.md` -- The text explicitly says a route may be closed for maintenance. |
| 47 | A body may exceed the 5 megabyte limit. | 29 | carried | 'a body may exceed the 5 megabyte limit' in `merged.md` -- The text explicitly identifies a body exceeding the 5 megabyte limit as a refusal reason. |
| 48 | None of those three refusal reasons clears itself by waiting for a stated number of seconds. | 29 | carried | 'None of those three clears itself by waiting for a stated number of seconds.' in `merged.md` -- The text directly says none of the three refusal reasons clears itself by waiting. |
| 49 | A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `merged.md` -- The text directly states that retrying against a suspended credential consumes the whole budget without reaching the service. |
| 50 | The log afterwards shows nothing except a long run of refusals. | 31 | carried | 'the log afterwards shows nothing at all except a long run of refusals' in `merged.md` -- The text says the log shows only a long run of refusals, matching the claim. |
| 51 | Reading the status code rather than the class it belongs to separates the two cases. | 31 | carried | 'Reading the status code rather than the class it belongs to is what separates the two cases' in `merged.md` -- The text says that reading the status code rather than its class separates the two cases. |
| 52 | Reading the status code rather than the class it belongs to costs one comparison. | 31 | carried | 'Reading the status code rather than the class it belongs to is what separates the two cases, and it costs one comparison.' in `merged.md` -- The sentence directly states that this distinction costs one comparison. |
| 53 | A cap can be raised. | 35 | carried | 'A cap can be raised' in `merged.md` -- The text explicitly says a cap can be raised. |
| 54 | The number of caps raised without a measurement behind them is 0. | 35 | carried | 'the number of caps raised without a measurement behind them is 0' in `merged.md` -- The text gives the number of unmeasured cap increases as 0. |
| 55 | The platform team looks at whether the load is smooth or bursty. | 35 | carried | 'The platform team looks at whether the load is smooth or bursty' in `merged.md` -- The text directly states that the platform team considers whether load is smooth or bursty. |
| 56 | A burst is cheaper to smooth than it is to serve at its peak. | 35 | carried | 'a burst is cheaper to smooth than it is to serve at its peak' in `merged.md` -- The text directly compares the lower cost of smoothing a burst with serving it at its peak. |
| 57 | A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap. | 35 | carried | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `merged.md` -- The text directly states that moving half the work usually meets the caller’s needs without changing the cap. |
| 58 | Requests reach the platform team through the usual channel. | 37 | carried | 'Requests reach the platform team through the usual channel' in `merged.md` -- The text says requests reach the platform team through the usual channel. |
| 59 | Requests are answered within two working days. | 37 | carried | 'they are answered within two working days' in `merged.md` -- The text says requests are answered within two working days. |
| 60 | There is no expedited path. | 37 | carried | 'There is no expedited path' in `merged.md` -- The text explicitly states there is no expedited path. |
| 61 | There is no exception list. | 37 | carried | 'There is no expedited path and no exception list.' in `merged.md` -- The text explicitly states there is no exception list. |

### `source_b.md` -- 67 claim(s): 0 dropped, 0 contradicted, 2 carried in part, 65 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 26 | The response body repeats the window as a plain field. | 13 | carried in part | 'it names what the gateway calls the “window” it counted in.' in `merged.md` -- The body names the window, but the text does not specify that the window is a plain field. |
| 48 | A caller that cannot say how often it was refused cannot make a case for a larger cap. | 25 | carried in part | 'A caller that cannot say how often it was refused last week cannot argue for a larger cap' in `merged.md` -- The text says the caller must know how often it was refused last week, but does not state the claim without that timeframe. |
| 1 | Every credential has its own cap. | 3 | carried | 'Every credential has a cap.' in `merged.md` -- The text states that every credential has a cap. |
| 2 | When a credential’s cap is spent, the gateway answers 429. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge' in `merged.md` -- The text says spending the credential’s cap results in a gateway 429 response. |
| 3 | The gateway answers 429 at the edge. | 3 | carried | 'the gateway answers 429 at the edge' in `merged.md` -- The text explicitly locates the 429 response at the edge. |
| 4 | The gateway answers 429 without troubling the service behind it. | 3 | carried | 'without waking the service behind it' in `merged.md` -- The text says the gateway’s refusal does not wake the service behind it. |
| 5 | Requests are counted against the credential rather than the connection. | 5 | carried | 'Requests are counted against the credential that presented them, over a fixed window of 60 seconds, and never against a connection.' in `merged.md` -- The text says requests count against the presenting credential and never against a connection. |
| 6 | Requests are counted over a fixed window of 60 seconds. | 5 | carried | 'Requests are counted against the credential that presented them, over a fixed window of 60 seconds, and never against a connection.' in `merged.md` -- The text explicitly specifies a fixed 60-second counting window. |
| 7 | The gateway does not disclose the start of the fixed window. | 5 | carried | 'The gateway does not disclose where the window starts.' in `merged.md` -- The text directly says the gateway does not disclose the window’s start. |
| 8 | Opening more sockets does not gain anything. | 5 | carried | 'Opening a second socket therefore buys a caller nothing.' in `merged.md` -- The text says opening an additional socket provides no benefit. |
| 9 | The request count follows the credential across hosts. | 5 | carried | 'The count follows the credential across hosts.' in `merged.md` -- The text explicitly says the count follows the credential across hosts. |
| 10 | A caller spread over many worker processes is throttled at the same point as a single process. | 5 | carried | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `merged.md` -- The text says a client across eight processes is throttled at the same point as one process. |
| 11 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- The text directly states the default allowance and its amount. |
| 12 | The default allowance is enough for every interactive use of this API that the platform team has seen. | 7 | carried | 'The default is enough for every interactive use of the API the platform team has seen' in `merged.md` -- The text says the default covers every interactive API use the platform team has seen. |
| 13 | A caller that needs more than the default allowance is almost always doing batch work under an interactive credential. | 7 | carried | 'callers who need more are almost always doing batch work under an interactive credential' in `merged.md` -- The text directly describes callers needing more as almost always doing batch work under an interactive credential. |
| 14 | A refusal is not an outage. | 7 | carried | 'A refusal is not an outage or a bug in the gateway' in `merged.md` -- The text explicitly says a refusal is not an outage. |
| 15 | A refusal is not a bug in the gateway. | 7 | carried | 'A refusal is not an outage or a bug in the gateway' in `merged.md` -- The text explicitly says a refusal is not a bug in the gateway. |
| 16 | A refusal is capacity being held for a request that somebody else has already been promised. | 7 | carried | 'It is the platform declining to spend capacity that has already been promised to somebody else' in `merged.md` -- The text describes the refusal as declining to spend capacity already promised to somebody else. |
| 17 | Callers retrying immediately are most of the reason the cap exists. | 7 | carried | 'Callers that retry at once are the largest single reason the cap is there at all.' in `merged.md` -- The text identifies callers retrying at once as the largest single reason for the cap. |
| 18 | The header is called Retry-After. | 11 | carried | 'The refusal carries a Retry-After header' in `merged.md` -- The header is explicitly named Retry-After. |
| 19 | The Retry-After value is a whole number of seconds. | 11 | carried | 'Its value is a whole number of seconds to wait.' in `merged.md` -- The text says the header value is a whole number of seconds. |
| 20 | The Retry-After header is present on every refusal the gateway sends. | 11 | carried | 'which is present on every refusal the gateway sends.' in `merged.md` -- The text explicitly says the header is present on every refusal the gateway sends. |
| 21 | Waiting for the duration specified by the header and then continuing is the entire contract. | 11 | carried | 'Waiting that long and then continuing is the whole of the contract' in `merged.md` -- The text says waiting the header duration and then continuing is the whole contract. |
| 22 | Waiting longer than the header asks earns nothing. | 11 | carried | 'waiting longer than the header asks earns a caller no credit at all.' in `merged.md` -- The text explicitly says waiting longer earns no credit. |
| 23 | Nobody at the gateway end is keeping score. | 11 | carried | 'The gateway keeps no memory of who backed off politely' in `merged.md` -- The text says the gateway does not keep memory of callers who backed off politely. |
| 24 | The response body is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- The refusal body is explicitly described as JSON. |
| 25 | The response body repeats the cap as a plain field. | 13 | carried | 'It names the cap and the tier as plain fields as well.' in `merged.md` -- The text explicitly says the body names the cap as a plain field. |
| 27 | The response body repeats the tier as a plain field. | 13 | carried | 'It names the cap and the tier as plain fields as well.' in `merged.md` -- The text explicitly says the body names the tier as a plain field. |
| 28 | None of the response body fields is a substitute for the header. | 13 | carried | 'None of those fields is a substitute for the header' in `merged.md` -- The text explicitly says none of the body fields substitutes for the header. |
| 29 | The response body is for the human reading the log afterwards. | 13 | carried | 'The body is there so that a human reading a log afterwards can see why the request was refused' in `merged.md` -- The text says the body helps a human reading a log afterwards understand the refusal. |
| 30 | There are four rules. | 17 | carried | 'Four rules, given in the order they should be applied.' in `merged.md` -- The text introduces four rules. |
| 31 | The rules are given in the order they are to be applied. | 17 | carried | 'Four rules, given in the order they should be applied.' in `merged.md` -- The text explicitly says the rules are given in the order they should be applied. |
| 32 | The gateway has already done the arithmetic for the wait. | 19 | carried | 'The gateway has already done that arithmetic' in `merged.md` -- The text says the gateway has already done the arithmetic for the wait. |
| 33 | The gateway did the arithmetic with information the caller cannot see. | 19 | carried | 'with information the caller does not have' in `merged.md` -- The text says the gateway used information the caller does not have. |
| 34 | The same rule holds on the 503 path. | 19 | carried | 'Honour the header, every time. The gateway has already done that arithmetic, with information the caller does not have, and it does the same on the 503 path' in `merged.md` -- The text applies the header rule on the 503 path as well. |
| 35 | The cause of a refusal on the 503 path is different. | 19 | carried | 'whose cause is different.' in `merged.md` -- The text explicitly says the 503 path has a different cause. |
| 36 | A 200 needs nothing. | 21 | carried | 'A 200 wants nothing' in `merged.md` -- The text says a 200 wants nothing. |
| 37 | A 429 needs the stated wait. | 21 | carried | 'a 429 wants the stated wait' in `merged.md` -- The text says a 429 wants the stated wait. |
| 38 | A 500 can be retried once the stated wait has passed. | 21 | carried | 'a 500 may be retried once that wait has passed' in `merged.md` -- The text says a 500 may be retried after the stated wait has passed. |
| 39 | A 503 means the platform itself is overloaded. | 21 | carried | 'a 503 is the overload path: the platform itself is overloaded.' in `merged.md` -- The text explicitly describes a 503 as the platform overload path. |
| 40 | A batch credential is allowed 1000 requests in a window. | 23 | carried | 'The default allowance is 100 requests in a window, and a credential marked for batch work is allowed 1000 in the same window.' in `merged.md` -- The text explicitly gives the batch credential an allowance of 1000 requests in the same window. |
| 41 | The batch allowance is 50 times the default. | 23 | carried | 'The batch allowance is 50 times the default and uses the same counting scheme.' in `merged.md` -- The text explicitly states that the batch allowance is 50 times the default. |
| 42 | The batch tier does not use a separate counting scheme. | 23 | carried | 'The batch allowance is 50 times the default and uses the same counting scheme.' in `merged.md` -- The batch uses the same counting scheme as the default. |
| 43 | The window is identical for the batch and interactive cases. | 23 | carried | 'The window, header and body are identical for both tiers, so a client written for one tier needs no change to run against the other.' in `merged.md` -- The text explicitly says the window is identical for both tiers. |
| 44 | The header is identical for the batch and interactive cases. | 23 | carried | 'The window, header and body are identical for both tiers, so a client written for one tier needs no change to run against the other.' in `merged.md` -- The text explicitly says the header is identical for both tiers. |
| 45 | The body is identical for the batch and interactive cases. | 23 | carried | 'The window, header and body are identical for both tiers, so a client written for one tier needs no change to run against the other.' in `merged.md` -- The text explicitly says the body is identical for both tiers. |
| 46 | A client written for one tier needs no change to run against the other tier. | 23 | carried | 'The window, header and body are identical for both tiers, so a client written for one tier needs no change to run against the other.' in `merged.md` -- The text says a client written for either tier needs no change to run against the other. |
| 47 | Nothing else about the batch tier differs from the default. | 23 | carried | 'Nothing else about the two tiers differs in any way.' in `merged.md` -- The text explicitly states that nothing else differs between the tiers. |
| 49 | The platform team will not assemble the case for a larger cap on the caller’s behalf. | 25 | carried | 'A caller that cannot say how often it was refused last week cannot argue for a larger cap, and nobody at the far end will assemble that argument on its behalf.' in `merged.md` -- The text says nobody at the far end will assemble the case for the caller. |
| 50 | The gateway refuses a request for three separate reasons. | 29 | carried | 'The gateway refuses a request for three reasons and only one of them is the cap described above.' in `merged.md` -- The text explicitly states that there are three refusal reasons. |
| 51 | Only one of the three refusal reasons is a cap. | 29 | carried | 'The gateway refuses a request for three reasons and only one of them is the cap described above.' in `merged.md` -- The text explicitly says only one of the three reasons is the cap. |
| 52 | Two of the three refusal reasons have nothing to do with how much traffic a caller has sent in its current window. | 29 | carried | 'Two of the three have nothing to do with how much traffic a caller has sent in its current window.' in `merged.md` -- The text explicitly states that two refusal reasons are unrelated to current-window traffic. |
| 53 | A credential can be suspended. | 29 | carried | 'A credential may be suspended' in `merged.md` -- The text says a credential may be suspended. |
| 54 | A route can be closed while it is being repaired. | 29 | carried | 'a route may be closed for maintenance or while it is being repaired' in `merged.md` -- The text says a route may be closed while it is being repaired. |
| 55 | A request body over the 5 megabyte limit is refused before it has been read. | 29 | carried | 'A credential may be suspended, a route may be closed for maintenance or while it is being repaired, or a body may exceed the 5 megabyte limit. An oversized request body is refused before it has been read.' in `merged.md` -- Together these sentences state the 5 megabyte limit and that an oversized body is refused before being read. |
| 56 | A loop retrying against a suspended credential burns its whole budget and reaches nothing. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `merged.md` -- The text says the loop spends its whole budget without reaching the service. |
| 57 | The log afterwards shows a long run of refusals and no successes. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service — and the log afterwards shows nothing at all except a long run of refusals. That run has no successes' in `merged.md` -- The text says the log shows a long run of refusals and that the run has no successes. |
| 58 | The log afterwards reads like an outage. | 31 | carried | 'reads like an outage' in `merged.md` -- The text explicitly says the run of refusals reads like an outage. |
| 59 | A caller that can move half its work to a quieter hour usually finds it does not need a larger cap. | 33 | carried | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all, which is the outcome everyone prefers.' in `merged.md` -- The text says shifting half the work usually meets the caller’s needs without changing the cap. |
| 60 | A cap can be raised. | 33 | carried | 'A cap can be raised' in `merged.md` -- The text explicitly states that a cap can be raised. |
| 61 | A cap cannot be raised on the strength of an assertion that the current cap is too small. | 33 | carried | 'A cap increase is not granted on the strength of an assertion that the current cap is too small.' in `merged.md` -- The text explicitly rules out granting an increase based only on that assertion. |
| 62 | The team wants to know whether the load is smooth or bursty before it looks at the number. | 35 | carried | 'The platform team looks at whether the load is smooth or bursty — a burst is cheaper to smooth than it is to serve at its peak — before it looks at the requested number.' in `merged.md` -- The text says the team considers whether load is smooth or bursty before the requested number. |
| 63 | A burst is cheaper to smooth out than to serve at its peak. | 35 | carried | 'a burst is cheaper to smooth than it is to serve at its peak' in `merged.md` -- The text directly states that smoothing a burst is cheaper than serving it at peak. |
| 64 | Requests go to the platform team through the usual channel. | 35 | carried | 'Requests reach the platform team through the usual channel, and they are answered within two working days.' in `merged.md` -- The text says requests reach the team through the usual channel. |
| 65 | There is no expedited path. | 37 | carried | 'There is no expedited path' in `merged.md` -- The text explicitly states that there is no expedited path. |
| 66 | An answer takes two working days. | 37 | carried | 'they are answered within two working days.' in `merged.md` -- The text says requests are answered within two working days. |
| 67 | Chasing an answer does not make it take fewer days. | 37 | carried | 'Chasing a request does not make it take fewer days.' in `merged.md` -- The text states that chasing a request does not shorten the response time. |

### `merged.md` -- 82 claim(s): 0 invented, 0 contradicted, 0 supported in part, 82 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Every credential has a cap. | supported | `source_a.md` | 'Every credential has a cap.' in `source_a.md` -- Source_a.md directly states that every credential has a cap. |
| 2 | The gateway answers 429 at the edge. | supported | `source_a.md` | 'the gateway answers 429 at the edge' in `source_a.md` -- Source_a.md directly says the gateway answers 429 at the edge. |
| 3 | The gateway answers without waking the service behind it. | supported | `source_a.md` | 'without waking the service behind it' in `source_a.md` -- This directly supports that the gateway answers without waking the service. |
| 4 | Requests are counted against the credential that presented them. | supported | `source_a.md` | 'Requests are counted against the credential that presented them' in `source_a.md` -- Source_a.md directly identifies the presenting credential as the basis for counting requests. |
| 5 | Requests are counted over a fixed window of 60 seconds. | supported | `source_a.md` | 'over a fixed window of 60 seconds' in `source_a.md` -- Source_a.md states that requests are counted over a fixed 60-second window. |
| 6 | Requests are never counted against a connection. | supported | `source_a.md` | 'and never against a connection.' in `source_a.md` -- Source_a.md directly says requests are never counted against a connection. |
| 7 | The gateway does not disclose where the window starts. | supported | `source_b.md` | 'whose start the gateway doesn’t disclose.' in `source_b.md` -- Source_b.md explicitly says the gateway does not disclose the window’s start. |
| 8 | Opening a second socket buys a caller nothing. | supported | `source_a.md` | 'Opening a second socket therefore buys a caller nothing.' in `source_a.md` -- Source_a.md directly states that opening a second socket buys a caller nothing. |
| 9 | The count follows the credential across hosts. | supported | `source_b.md` | 'The count follows the credential wherever the caller happens to put it, including across hosts.' in `source_b.md` -- Source_b.md explicitly says the count follows the credential across hosts. |
| 10 | A client spread across eight worker processes is throttled at exactly the point one process would have been. | supported | `source_a.md` | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `source_a.md` -- Source_a.md directly states this about a client spread across eight worker processes. |
| 11 | A client spread across eight worker processes pays for the extra file descriptors. | supported | `source_a.md` | 'and pays for the extra file descriptors as well.' in `source_a.md` -- Source_a.md states that the eight-process client pays for extra file descriptors. |
| 12 | The default allowance is 100 requests in a window. | supported | `source_a.md` | 'The default allowance is 100 requests in a window' in `source_a.md` -- Source_a.md directly gives the default allowance as 100 requests in a window. |
| 13 | A credential marked for batch work is allowed 1000 in the same window. | supported | `source_a.md` | 'a credential marked for batch work is allowed 1000 in the same window.' in `source_a.md` -- Source_a.md directly states the batch credential allowance and that it uses the same window. |
| 14 | The batch allowance is 50 times the default. | supported | `source_a.md` | 'A batch credential is allowed fifty times the default allowance' in `source_a.md` -- Source_a.md directly states that the batch allowance is fifty times the default. |
| 15 | The batch allowance uses the same counting scheme as the default allowance. | supported | `source_b.md` | 'not a separate counting scheme.' in `source_b.md` -- Source_b.md says the batch allowance does not use a separate counting scheme. |
| 16 | Callers who need more are almost always doing batch work under an interactive credential. | supported | `source_b.md` | 'a caller that needs more than that is almost always doing batch work under an interactive credential.' in `source_b.md` -- Source_b.md directly makes this statement about callers needing more than the default allowance. |
| 17 | A refusal is not an outage or a bug in the gateway. | supported | `source_b.md` | 'The refusal isn’t an outage and it isn’t a bug in the gateway' in `source_b.md` -- Source_b.md directly says a refusal is neither an outage nor a gateway bug. |
| 18 | A client library may call a refusal a particular error class. | supported | `source_a.md` | 'whatever the error class in a client library happens to call it.' in `source_a.md` -- Source_a.md says the refusal may be called an error class by a client library. |
| 19 | A refusal is the platform declining to spend capacity that has already been promised to somebody else. | supported | `source_a.md` | 'It is the platform declining to spend capacity that has already been promised to somebody else' in `source_a.md` -- Source_a.md directly describes a refusal as the platform declining to spend already-promised capacity. |
| 20 | Callers that retry at once are the largest single reason the cap is there at all. | supported | `source_a.md` | 'Callers that retry at once are the largest single reason the cap is there at all.' in `source_a.md` -- Source_a.md directly identifies callers retrying at once as the largest single reason for the cap. |
| 21 | Every refusal the gateway sends carries a Retry-After header. | supported | `source_b.md` | 'it is present on every refusal the gateway sends.' in `source_b.md` -- Source_b.md explicitly states that the Retry-After header is present on every refusal. |
| 22 | The Retry-After header value is a whole number of seconds to wait. | supported | `source_a.md` | 'Its value is a whole number of seconds to wait.' in `source_a.md` -- Source_a.md directly describes the header value as a whole number of seconds to wait. |
| 23 | The contract is to wait the time specified by the header and then continue. | supported | `source_a.md` | 'Waiting that long and then continuing is the whole of the contract' in `source_a.md` -- Source_a.md directly states that waiting the header’s duration and then continuing is the contract. |
| 24 | The gateway keeps no memory of who backed off politely. | supported | `source_a.md` | 'The gateway keeps no memory of who backed off politely' in `source_a.md` -- Source_a.md directly says the gateway keeps no memory of callers who backed off politely. |
| 25 | Waiting longer than the header asks earns a caller no credit. | supported | `source_a.md` | 'waiting longer than the header asks earns a caller no credit at all.' in `source_a.md` -- Source_a.md directly says that waiting longer than the header requests earns no credit. |
| 26 | The refusal body is JSON. | supported | `source_a.md` | 'The body of the refusal is JSON' in `source_a.md` -- Source_a.md explicitly says the refusal body is JSON. |
| 27 | The refusal body names the “window” the gateway counted in. | supported | `source_a.md` | 'The body of the refusal is JSON, and it names what the gateway calls the “window” it counted in.' in `source_a.md` -- This directly states that the body names the window the gateway counted in. |
| 28 | The refusal body names the cap as a plain field. | supported | `source_b.md` | 'The response body is JSON and it repeats the cap, the window and the tier as plain fields.' in `source_b.md` -- Source_b.md says the body repeats the cap as a plain field. |
| 29 | The refusal body names the tier as a plain field. | supported | `source_b.md` | 'The response body is JSON and it repeats the cap, the window and the tier as plain fields.' in `source_b.md` -- Source_b.md says the body repeats the tier as a plain field. |
| 30 | None of the refusal body fields is a substitute for the header. | supported | `source_a.md` | 'None of those fields is a substitute for the header' in `source_a.md` -- The source explicitly says none of the body fields substitutes for the header. |
| 31 | A caller that parses the body to compute its own wait does the same arithmetic twice. | supported | `source_a.md` | 'a caller that parses the body to compute its own wait is doing the same arithmetic twice.' in `source_a.md` -- This is stated directly in source_a.md. |
| 32 | A caller that parses the body to compute its own wait risks disagreeing with the gateway. | supported | `source_b.md` | 'a caller that parses the body in order to compute its own wait has written code whose only possible future is to disagree with the gateway it is talking to.' in `source_b.md` -- Source_b.md says parsing the body to calculate a wait risks disagreement with the gateway. |
| 33 | The refusal body is intended to let a human reading a log afterwards see why the request was refused. | supported | `source_a.md` | 'The body is there so that a human reading a log afterwards can see why the request was refused' in `source_a.md` -- The source directly states the body’s purpose for a human reading the log. |
| 34 | The gateway has already done the arithmetic for the wait. | supported | `source_a.md` | 'The gateway has already done that arithmetic, with information the caller does not have' in `source_a.md` -- The gateway is stated to have already done the wait arithmetic. |
| 35 | The gateway has information the caller does not have. | supported | `source_a.md` | 'with information the caller does not have' in `source_a.md` -- This directly states that the caller lacks information the gateway used. |
| 36 | The gateway does the same arithmetic on the 503 path. | supported | `source_a.md` | 'and it does the same on the 503 path.' in `source_a.md` -- The source says the gateway uses the same arithmetic on the 503 path. |
| 37 | The cause of the 503 path is different. | supported | `source_b.md` | 'even though the cause of the refusal is an entirely different one.' in `source_b.md` -- This states that the cause on the 503 path differs. |
| 38 | A wait derived on the client side is a guess about a counter the client cannot see. | supported | `source_a.md` | 'A wait derived on the client side is a guess about a counter it cannot see.' in `source_a.md` -- This is stated verbatim in source_a.md. |
| 39 | A 200 wants nothing. | supported | `source_a.md` | 'A 200 wants nothing' in `source_a.md` -- The source directly says a 200 wants nothing. |
| 40 | A 429 wants the stated wait. | supported | `source_a.md` | 'a 429 wants the stated wait' in `source_a.md` -- The source directly says a 429 wants the stated wait. |
| 41 | A 500 may be retried once the stated wait has passed. | supported | `source_a.md` | 'a 500 may be retried once that wait has passed' in `source_a.md` -- The source directly states when a 500 may be retried. |
| 42 | A 503 is the overload path. | supported | `source_a.md` | 'a 503 is the overload path.' in `source_a.md` -- This is stated directly in the retry rules. |
| 43 | The platform itself is overloaded on the 503 path. | supported | `source_b.md` | 'a 503 means the platform itself is overloaded.' in `source_b.md` -- Source_b.md explicitly describes a 503 as the platform being overloaded. |
| 44 | The four cases are not interchangeable. | supported | `source_a.md` | 'The four cases are not interchangeable.' in `source_a.md` -- The source explicitly says the four response cases are not interchangeable. |
| 45 | A client that folds every non-success into one branch will retry hardest during the incident the cap was installed to survive. | supported | `source_a.md` | 'A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive.' in `source_a.md` -- This directly states the claimed consequence of folding non-success responses into one branch. |
| 46 | A batch credential is allowed fifty times the default allowance. | supported | `source_a.md` | 'A batch credential is allowed fifty times the default allowance' in `source_a.md` -- The source directly gives the batch allowance as fifty times the default. |
| 47 | A batch credential is measured over exactly the same window as the default tier. | supported | `source_a.md` | 'and it is measured over exactly the same window.' in `source_a.md` -- This directly states that the batch allowance uses the same window. |
| 48 | The window is identical for both tiers. | supported | `source_b.md` | 'The window, the header and the body are identical to the interactive case' in `source_b.md` -- The source explicitly says the window is identical across tiers. |
| 49 | The header is identical for both tiers. | supported | `source_b.md` | 'The window, the header and the body are identical to the interactive case' in `source_b.md` -- The source explicitly says the header is identical across tiers. |
| 50 | The body is identical for both tiers. | supported | `source_b.md` | 'The window, the header and the body are identical to the interactive case' in `source_b.md` -- The source explicitly says the body is identical across tiers. |
| 51 | A client written for one tier needs no change to run against the other tier. | supported | `source_b.md` | 'The window, the header and the body are identical to the interactive case, so a client written for one tier needs no change at all to run against the other.' in `source_b.md` -- The source states that a client for one tier needs no change to run against the other. |
| 52 | The tier is set on the credential when it is issued. | supported | `source_a.md` | 'The tier is set on the credential when it is issued and cannot be asked for per call.' in `source_a.md` -- The source directly states when the tier is set. |
| 53 | The tier cannot be asked for per call. | supported | `source_a.md` | 'The tier is set on the credential when it is issued and cannot be asked for per call.' in `source_a.md` -- The source directly states that the tier cannot be requested per call. |
| 54 | The gateway refuses a request for three reasons. | supported | `source_a.md` | 'The gateway refuses a request for three reasons and only one of them is the one above.' in `source_a.md` -- The source explicitly says the gateway refuses requests for three reasons. |
| 55 | Only one of the three refusal reasons is the cap described above. | supported | `source_b.md` | 'The gateway refuses a request for three separate reasons, and only one of them is a cap.' in `source_b.md` -- The source directly states that only one of the three reasons is a cap. |
| 56 | Two of the three refusal reasons have nothing to do with how much traffic a caller has sent in its current window. | supported | `source_b.md` | 'Two of the three have nothing to do with how much traffic a caller has sent in the window it is currently in.' in `source_b.md` -- The source directly states this about two of the three refusal reasons. |
| 57 | A credential may be suspended. | supported | `source_a.md` | 'A credential may be suspended' in `source_a.md` -- The source states that a credential may be suspended. |
| 58 | A route may be closed for maintenance. | supported | `source_a.md` | 'a route may be closed for maintenance' in `source_a.md` -- The source states that a route may be closed for maintenance. |
| 59 | A route may be closed while it is being repaired. | supported | `source_b.md` | 'a route can be closed while it is being repaired' in `source_b.md` -- The source directly states that a route can be closed while being repaired. |
| 60 | A body may exceed the 5 megabyte limit. | supported | `source_a.md` | 'a body may exceed the 5 megabyte limit' in `source_a.md` -- The source directly states that a body may exceed this limit. |
| 61 | An oversized request body is refused before it has been read. | supported | `source_b.md` | 'a request body over the 5 megabyte limit is refused before it has been read at all.' in `source_b.md` -- The source directly states that an oversized request body is refused before being read. |
| 62 | None of those three refusal reasons clears itself by waiting for a stated number of seconds. | supported | `source_a.md` | 'None of those three clears itself by waiting for a stated number of seconds.' in `source_a.md` -- The source directly states that none of the three refusal reasons clears by waiting. |
| 63 | A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service. | supported | `source_a.md` | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `source_a.md` -- The source directly states that such a loop spends its budget without reaching the service. |
| 64 | The log afterwards shows nothing except a long run of refusals. | supported | `source_a.md` | 'the log afterwards shows nothing at all except a long run of refusals.' in `source_a.md` -- The source says the log shows nothing except a long run of refusals. |
| 65 | A long run of refusals has no successes. | supported | `source_b.md` | 'The log afterwards shows a long run of refusals and no successes at all, which reads like an outage and isn’t one — and the wasted budget is the caller’s own.' in `source_b.md` -- The source explicitly says the log shows no successes. |
| 66 | A long run of refusals reads like an outage. | supported | `source_b.md` | 'The log afterwards shows a long run of refusals and no successes at all, which reads like an outage and isn’t one — and the wasted budget is the caller’s own.' in `source_b.md` -- The source says the long run of refusals reads like an outage. |
| 67 | A long run of refusals is not an outage. | supported | `source_b.md` | 'The log afterwards shows a long run of refusals and no successes at all, which reads like an outage and isn’t one — and the wasted budget is the caller’s own.' in `source_b.md` -- The source explicitly says the apparent outage isn’t one. |
| 68 | Reading the status code rather than the class it belongs to separates the two cases. | supported | `source_a.md` | 'Reading the status code rather than the class it belongs to is what separates the two cases' in `source_a.md` -- The source directly states that reading the status code separates the cases. |
| 69 | Reading the status code rather than the class it belongs to costs one comparison. | supported | `source_a.md` | 'and it costs one comparison.' in `source_a.md` -- The source states that this distinction costs one comparison. |
| 70 | A cap can be raised. | supported | `source_a.md` | 'A cap can be raised' in `source_a.md` -- The source directly states that a cap can be raised. |
| 71 | The number of caps raised without a measurement behind them is 0. | supported | `source_a.md` | 'the number of caps raised without a measurement behind them is 0.' in `source_a.md` -- The source directly gives the number as zero. |
| 72 | The platform team looks at whether the load is smooth or bursty before it looks at the requested number. | supported | `source_b.md` | 'The team wants to know whether the load is smooth or bursty before it looks at the number at all.' in `source_b.md` -- Source_b gives the ordering, while source_a identifies the team assessing whether load is smooth or bursty as the platform team. |
| 73 | A burst is cheaper to smooth than it is to serve at its peak. | supported | `source_a.md` | 'A burst is cheaper to smooth than it is to serve at its peak.' in `source_a.md` -- The source directly states that smoothing a burst is cheaper than serving it at peak. |
| 74 | A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap. | supported | `source_a.md` | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `source_a.md` -- The source directly states that moving half the work usually avoids a cap change. |
| 75 | Moving work to a quieter hour is the cheapest fix available. | supported | `source_b.md` | 'That is the cheapest fix available to anybody, and it is available to almost everybody.' in `source_b.md` -- “That” refers to moving half the work to a quieter hour, which the preceding sentence describes as avoiding a larger cap. |
| 76 | Moving work to a quieter hour is available to almost everybody. | supported | `source_b.md` | 'That is the cheapest fix available to anybody, and it is available to almost everybody.' in `source_b.md` -- The source explicitly says moving work to a quieter hour is available to almost everybody. |
| 77 | A cap increase is not granted on the strength of an assertion that the current cap is too small. | supported | `source_b.md` | 'A cap can be raised, but not on the strength of an assertion that the current one is too small.' in `source_b.md` -- The source directly states that an assertion the cap is too small is not sufficient grounds for an increase. |
| 78 | Requests reach the platform team through the usual channel. | supported | `source_a.md` | 'Requests reach the platform team through the usual channel, and they are answered within two working days.' in `source_a.md` -- The source says requests reach the platform team through the usual channel. |
| 79 | Requests are answered within two working days. | supported | `source_a.md` | 'Requests reach the platform team through the usual channel, and they are answered within two working days.' in `source_a.md` -- The source explicitly says requests are answered within two working days. |
| 80 | There is no expedited path. | supported | `source_a.md` | 'There is no expedited path and no exception list.' in `source_a.md` -- The source directly states that there is no expedited path. |
| 81 | There is no exception list. | supported | `source_a.md` | 'There is no expedited path and no exception list.' in `source_a.md` -- The source directly states that there is no exception list. |
| 82 | Chasing a request does not make it take fewer days. | supported | `source_b.md` | 'There is no expedited path. An answer takes two working days, and chasing it doesn’t make it take fewer.' in `source_b.md` -- In context, “take fewer” refers to the stated two working days for an answer. |

## Structure

**9** mechanical check(s) over **104** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **82** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **128**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 19 run(s) over 58 attributed segment(s) — sources interleaved. 6 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

`[-...-]` is what the source said and `{+...+}` is what the merge says.

### Absent and undeclared — in a source, not in the merge, and no record explains it

- `a12` (`source_a.md`) — 'The refusal carries a Retry-After header.' is not in the merge and no disposition record explains it (nearest merge segment m17 at 0.61)

  ```text
  In the source: The refusal carries a Retry-After header.
  ```
- `a35` (`source_a.md`) — 'Log every refusal seen.' is not in the merge and no disposition record explains it (nearest merge segment m43 at 0.55)

  ```text
  In the source: Log every refusal seen.
  ```

### Reworded and undeclared — in the merge in altered wording, and no record explains it. At off this also covers layout: a segment whose source line breaks the merge ran together is altered and undeclared, and 380 reuses this kind rather than moving FINDING_KINDS off 12

- `a8` (`source_a.md`) — 'A refusal is not an outage, whatever the error class in a client library happens to call it.' is reworded in the merge and no disposition record explains it (nearest merge segment m13 at 0.88)

  ```text
  In the source: A refusal is not an outage, whatever the error class in a client library happens to call it.
  In the merge:  A refusal is not an outage or a bug in the gateway, whatever the error class in a client library happens to call it.
  What changed:  A refusal is not an [-outage,-] {+outage or a bug in the gateway,+} whatever the error class in a client library happens to call it.
  ```
- `a17` (`source_a.md`) — 'It names the cap and the tier as well.' is reworded in the merge and no disposition record explains it (nearest merge segment m23 at 0.83)

  ```text
  In the source: It names the cap and the tier as well.
  In the merge:  It names the cap and the tier as plain fields as well.
  What changed:  It names the cap and the tier as {+plain fields as+} well.
  ```
- `a18` (`source_a.md`) — 'None of those fields is a substitute for the header, and a caller that parses the body to compute its own wait is doing the same arithmetic twice.' is reworded in the merge and no disposition record explains it (nearest merge segment m24 at 0.88)

  ```text
  In the source: None of those fields is a substitute for the header, and a caller that parses the body to compute its own wait is doing the same arithmetic twice.
  In the merge:  None of those fields is a substitute for the header, and a caller that parses the body to compute its own wait is doing the same arithmetic twice and risks disagreeing with the gateway.
  What changed:  None of those fields is a substitute for the header, and a caller that parses the body to compute its own wait is doing the same arithmetic [-twice.-] {+twice and risks disagreeing with the gateway.+}
  ```
- `a23` (`source_a.md`) — 'The gateway has already done that arithmetic, with information the caller does not have, and it does the same on the 503 path.' is reworded in the merge and no disposition record explains it (nearest merge segment m29 at 0.91)

  ```text
  In the source: The gateway has already done that arithmetic, with information the caller does not have, and it does the same on the 503 path.
  In the merge:  The gateway has already done that arithmetic, with information the caller does not have, and it does the same on the 503 path, whose cause is different.
  What changed:  The gateway has already done that arithmetic, with information the caller does not have, and it does the same on the 503 [-path.-] {+path, whose cause is different.+}
  ```
- `a27` (`source_a.md`) — 'A 200 wants nothing, a 429 wants the stated wait, a 500 may be retried once that wait has passed, and a 503 is the overload path.' is reworded in the merge and no disposition record explains it (nearest merge segment m34 at 0.88)

  ```text
  In the source: A 200 wants nothing, a 429 wants the stated wait, a 500 may be retried once that wait has passed, and a 503 is the overload path.
  In the merge:  A 200 wants nothing, a 429 wants the stated wait, a 500 may be retried once that wait has passed, and a 503 is the overload path: the platform itself is overloaded.
  What changed:  A 200 wants nothing, a 429 wants the stated wait, a 500 may be retried once that wait has passed, and a 503 is the overload [-path.-] {+path: the platform itself is overloaded.+}
  ```
- `a39` (`source_a.md`) — 'Not all are caps.' is reworded in the merge and no disposition record explains it (nearest merge segment m48 at 0.79)

  ```text
  In the source: Not all are caps.
  In the merge:  Not all refusals are caps.
  ```
- `a40` (`source_a.md`) — 'The gateway refuses a request for three reasons and only one of them is the one above.' is reworded in the merge and no disposition record explains it (nearest merge segment m49 at 0.92)

  ```text
  In the source: The gateway refuses a request for three reasons and only one of them is the one above.
  In the merge:  The gateway refuses a request for three reasons and only one of them is the cap described above.
  What changed:  The gateway refuses a request for three reasons and only one of them is the [-one-] {+cap described+} above.
  ```
- `a41` (`source_a.md`) — 'A credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit.' is reworded in the merge and no disposition record explains it (nearest merge segment m51 at 0.88)

  ```text
  In the source: A credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit.
  In the merge:  A credential may be suspended, a route may be closed for maintenance or while it is being repaired, or a body may exceed the 5 megabyte limit.
  What changed:  A credential may be suspended, a route may be closed for [-maintenance,-] {+maintenance or while it is being repaired,+} or a body may exceed the 5 megabyte limit.
  ```
- `a43` (`source_a.md`) — 'The distinction matters to a retry loop.' is reworded in the merge and no disposition record explains it (nearest merge segment m54 at 0.78)

  ```text
  In the source: The distinction matters to a retry loop.
  In the merge:  The distinction matters more to a retry loop than to a reader.
  ```
- `a49` (`source_a.md`) — 'The platform team looks at whether the load is smooth or bursty — a burst is cheaper to smooth than it is to serve at its peak.' is reworded in the merge and no disposition record explains it (nearest merge segment m61 at 0.86)

  ```text
  In the source: The platform team looks at whether the load is smooth or bursty — a burst is cheaper to smooth than it is to serve at its peak.
  In the merge:  The platform team looks at whether the load is smooth or bursty — a burst is cheaper to smooth than it is to serve at its peak — before it looks at the requested number.
  What changed:  The platform team looks at whether the load is smooth or bursty — a burst is cheaper to smooth than it is to serve at its [-peak.-] {+peak — before it looks at the requested number.+}
  ```

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **52** departure(s) from its sources. Checking them confirms 36, rejects 4, and leaves 12 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 104 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | Title slot uses the base title. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Rate limiting and the 429 contract for gateway clients' and says so (no claim traced to it) |
| `b2` | duplicate | Opening statement already carries the credential cap. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-001`) |
| `b3` | duplicate | Opening refusal behavior is already stated. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-002`, `B-003`, `B-004`) |
| `b4` | reworded | Intro retains the omitted draft and its rationale. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b5` | subsumed | Counting basis is retained; the undisclosed start is added. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-005`, `B-006`, `B-007`) |
| `b6` | duplicate | The socket advice is already stated. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-008`) |
| `b7` | reworded | Intro states that the count follows the credential across hosts. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-009`) |
| `b8` | duplicate | Worker-process throttling is already stated. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-010`) |
| `b9` | reworded | The allowance and interactive-use context are retained. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-011`, `B-012`, `B-013`) |
| `b10` | reworded | The refusal is clarified as neither outage nor gateway bug. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-014`, `B-015`, `B-016`) |
| `b11` | duplicate | Immediate retries are already identified as a reason for the cap. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-017`) |
| `b12` | superseded | The shared heading is retained in the base wording. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b13` | reworded | The header name and its presence are stated. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-018`) |
| `b14` | subsumed | Header presence and whole-second value are both retained. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-019`, `B-020`) |
| `b15` | reworded | The contract and intended outcome are retained. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-021`) |
| `b16` | duplicate | Waiting longer earns no credit, as already stated. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-022`, `B-023`) |
| `b17` | subsumed | The JSON body fields are retained, including their plain-field form. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-024`, `B-025`, `B-027`) |
| `b18` | reworded | The body cannot replace the header or safely compute a wait. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-028`) |
| `b19` | duplicate | The body’s purpose is already stated. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-029`) |
| `b20` | superseded | The base heading more specifically describes the section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b21` | duplicate | The four-rule ordering is already stated. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-030`, `B-031`) |
| `b22` | subsumed | The rule to honour the header and avoid client calculation remains. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b23` | duplicate | Gateway-side arithmetic and hidden information are already stated. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-032`, `B-033`) |
| `b24` | reworded | The distinct 503 cause is retained. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-034`, `B-035`) |
| `b25` | duplicate | Client-side calculation is already called a guess. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b26` | duplicate | The client-side guess is already rejected. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b27` | reworded | The safe-to-retry set is distinguished from all failures. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b28` | subsumed | The response-specific retry actions and overload meaning remain. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-036`, `B-037`, `B-038`, `B-039`) |
| `b29` | duplicate | The risk of one retry branch is already stated. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'duplicate' is what happened to it (no claim traced to it) |
| `b30` | duplicate | The instruction against that retry loop is retained. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b31` | duplicate | The batch allowance and its ratio are already stated. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-040`, `B-041`, `B-042`) |
| `b32` | reworded | The shared tier behavior and no-change client requirement remain. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-043`, `B-044`, `B-045`, `B-046`) |
| `b33` | duplicate | The tiers’ other behavior is already stated as identical. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-047`) |
| `b34` | subsumed | Logging every refusal and retaining it for a week are stated. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b35` | duplicate | The need for refusal counts to support an increase is already stated. | **rejected** | declared 'duplicate', which predicts SUPPORTED; B-048 came back PARTIAL (`B-048`) |
| `b36` | reworded | The counts’ role in an increase request is retained. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b37` | superseded | The base heading includes the section’s code guidance. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b38` | duplicate | The three refusal reasons and single cap reason are already stated. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-050`, `B-051`) |
| `b39` | reworded | The two non-cap reasons are distinguished from traffic volume. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-052`) |
| `b40` | subsumed | All three refusal causes and pre-read rejection are retained. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-053`, `B-054`, `B-055`) |
| `b41` | reworded | The importance of the distinction to retry behavior is retained. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b42` | duplicate | The suspended-credential retry cost is already stated. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-056`) |
| `b43` | reworded | The log’s appearance, lack of success, and wasted budget remain. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-057`, `B-058`) |
| `b44` | duplicate | Moving half the work to a quieter hour is already advised. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-059`) |
| `b45` | reworded | The fix’s low cost and broad availability are retained. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b46` | reworded | An assertion alone is not grounds for an increase. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-060`, `B-061`) |
| `b47` | duplicate | The increase request already specifies these materials. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'duplicate' is what happened to it (no claim traced to it) |
| `b48` | reworded | Load shape is considered before the requested number. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-062`) |
| `b49` | duplicate | The relative cost of smoothing a burst is already stated. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-063`) |
| `b50` | duplicate | The usual request channel is already stated. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-064`) |
| `b51` | duplicate | The lack of an expedited path is already stated. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-065`) |
| `b52` | reworded | The response time cannot be shortened by chasing. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-066`, `B-067`) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | bf7d5842201d (hosted) |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | gpt-6-luna |
| Model (decompose) | gpt-6-luna |
| Model (verify) | gpt-6-luna |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed 0, thinking decompose, merge, verify, profile openai-reasoning |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 14 live, 0 cached, 0 replayed |
| Tokens | 49,525 in, 36,977 out, 10,748 cached, 13,965 reasoning |
| Cost | ~$0.02 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 270.8s |
| Generated | 2026-09-27T16:09:33+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `bf7d5842201d`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
