## Verdict

**1 finding(s).** In the structure: 1 verbatim violation.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 47 |
| Claims extracted from `source_a.md` | 45 |
| Claims extracted from `source_b.md` | 46 |
| Forward — source claims accounted for in the merge | **91/91** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **45/45** |
| Forward — `source_b.md` claims accounted for | **46/46** |
| Reverse — merge claims found in a source | **47/47** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **138/138** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

None in the claims. The 1 finding(s) this run reports are structural and are listed under `## Structure` below.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 45 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 45 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The gateway answers 429 at the edge when the cap is spent. | 3 | carried | 'the gateway answers 429 at the edge without waking the service behind it' in `merged.md` -- The text states the gateway answers 429 at the edge when the cap is spent. |
| 2 | The gateway does not wake the service behind it when answering 429. | 3 | carried | 'the gateway answers 429 at the edge without waking the service behind it' in `merged.md` -- The text explicitly states the service behind it is not woken. |
| 3 | Requests are counted against the credential that presented them. | 5 | carried | 'Requests are counted against the credential that presented them rather than the connection' in `merged.md` -- Directly states counting is against the credential. |
| 4 | Requests are counted over a fixed window of 60 seconds. | 5 | carried | 'over a fixed window of 60 seconds whose start the gateway does not disclose' in `merged.md` -- Directly states the 60 second fixed window. |
| 5 | Requests are never counted against a connection. | 5 | carried | 'Requests are counted against the credential that presented them rather than the connection' in `merged.md` -- The exclusive phrasing 'rather than the connection' supports that requests are never counted against a connection. |
| 6 | Opening a second socket buys a caller nothing. | 5 | carried | 'Opening a second socket therefore buys a caller nothing.' in `merged.md` -- Directly states this. |
| 7 | A client spread across eight worker processes is throttled at exactly the point one process would have been. | 5 | carried | 'a client spread across eight worker processes is throttled at exactly the point one process would have been' in `merged.md` -- Directly matches the claim. |
| 8 | A client spread across eight worker processes pays for the extra file descriptors as well. | 5 | carried | 'and pays for the extra file descriptors as well' in `merged.md` -- Directly matches the claim. |
| 9 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- Directly states the default allowance. |
| 10 | A credential marked for batch work is allowed 1000 requests in the same window. | 7 | carried | 'a credential marked for batch work is allowed 1000 in the same window' in `merged.md` -- Directly matches the claim. |
| 11 | The refusal carries a Retry-After header. | 11 | carried | 'The refusal carries a header called Retry-After.' in `merged.md` -- Directly states this. |
| 12 | The Retry-After header's value is a whole number of seconds to wait. | 11 | carried | 'Its value is a whole number of seconds to wait' in `merged.md` -- Directly matches the claim. |
| 13 | The gateway keeps no memory of who backed off politely. | 11 | carried | 'The gateway keeps no memory of who backed off politely' in `merged.md` -- Directly matches the claim. |
| 14 | Waiting longer than the header asks earns a caller no credit at all. | 11 | carried | 'waiting longer than the header asks earns a caller no credit at all' in `merged.md` -- Directly matches the claim. |
| 15 | The body of the refusal is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- Directly matches the claim. |
| 16 | The body of the refusal names what the gateway calls the "window" it counted in. | 13 | carried | 'it names what the gateway calls the “window” it counted in, along with the cap and the tier' in `merged.md` -- Directly states the body names the window. |
| 17 | The body of the refusal names the cap. | 13 | carried | 'it names what the gateway calls the “window” it counted in, along with the cap and the tier' in `merged.md` -- Directly states the body names the cap. |
| 18 | The body of the refusal names the tier. | 13 | carried | 'it names what the gateway calls the “window” it counted in, along with the cap and the tier' in `merged.md` -- Directly states the body names the tier. |
| 19 | None of those fields is a substitute for the header. | 13 | carried | 'None of those fields is a substitute for the header' in `merged.md` -- Directly matches the claim. |
| 20 | A caller that parses the body to compute its own wait is doing the same arithmetic twice. | 13 | carried | 'a caller that parses the body to compute its own wait is doing the same arithmetic twice' in `merged.md` -- Directly matches the claim. |
| 21 | The gateway has already done that arithmetic with information the caller does not have. | 19 | carried | 'The gateway has already done that arithmetic, with information the caller does not have' in `merged.md` -- Directly matches the claim. |
| 22 | The gateway does the same arithmetic on the 503 path. | 19 | carried | 'and it does the same on the 503 path, even though the cause of that refusal is an entirely different one' in `merged.md` -- Directly matches the claim. |
| 23 | A 200 wants nothing. | 21 | carried | 'A 200 wants nothing' in `merged.md` -- Directly matches the claim. |
| 24 | A 429 wants the stated wait. | 21 | carried | 'a 429 wants the stated wait' in `merged.md` -- Directly matches the claim. |
| 25 | A 500 may be retried once that wait has passed. | 21 | carried | 'a 500 may be retried once that wait has passed' in `merged.md` -- Directly matches the claim. |
| 26 | A 503 is the overload path. | 21 | carried | 'a 503 is the overload path' in `merged.md` -- Directly stated in the retry rules section. |
| 27 | A batch credential is allowed fifty times the default allowance. | 23 | carried | 'A credential marked for batch work is allowed 1000 requests in a window — fifty times the default allowance' in `merged.md` -- States the batch allowance is fifty times the default. |
| 28 | The batch credential allowance is measured over exactly the same window. | 23 | carried | 'measured over exactly the same window, and it is not a separate counting scheme' in `merged.md` -- States the batch allowance is measured over the same window. |
| 29 | The tier is set on the credential when it is issued. | 23 | carried | 'The tier is set on the credential when it is issued' in `merged.md` -- Directly matches the claim. |
| 30 | The tier cannot be asked for per call. | 23 | carried | 'and cannot be asked for per call' in `merged.md` -- Directly matches the claim. |
| 31 | Nothing else about the two tiers differs in any way. | 23 | carried | 'Nothing else about the two tiers differs in any way.' in `merged.md` -- Directly matches the claim. |
| 32 | The gateway refuses a request for three reasons. | 29 | carried | 'The gateway refuses a request for three separate reasons' in `merged.md` -- States three reasons for refusal, matching the claim. |
| 33 | A credential may be suspended. | 29 | carried | 'A credential may be suspended' in `merged.md` -- Directly matches the claim. |
| 34 | A route may be closed for maintenance. | 29 | carried | 'a route may be closed for maintenance' in `merged.md` -- Directly matches the claim. |
| 35 | A body may exceed the 5 megabyte limit. | 29 | carried | 'a body may exceed the 5 megabyte limit and be refused before it has even been read' in `merged.md` -- Directly matches the claim. |
| 36 | None of those three refusal reasons clears itself by waiting for a stated number of seconds. | 29 | carried | 'None of those three clears itself by waiting for a stated number of seconds' in `merged.md` -- Directly matches the claim. |
| 37 | A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `merged.md` -- Directly matches the claim. |
| 38 | The log afterwards shows nothing at all except a long run of refusals. | 31 | carried | 'the log afterwards shows nothing at all except a long run of refusals and no successes' in `merged.md` -- The sentence entails that the log shows nothing but a long run of refusals. |
| 39 | A cap can be raised. | 35 | carried | 'A cap can be raised' in `merged.md` -- Directly matches the claim. |
| 40 | The number of caps raised without a measurement behind them is 0. | 35 | carried | 'the number of caps raised without a measurement behind them is 0' in `merged.md` -- Directly matches the claim. |
| 41 | The platform team looks at whether the load is smooth or bursty. | 35 | carried | 'The platform team wants to know whether the load is smooth or bursty before it looks at the number at all' in `merged.md` -- States the platform team considers whether load is smooth or bursty. |
| 42 | Requests reach the platform team through the usual channel. | 37 | carried | 'Requests reach the platform team through the usual channel' in `merged.md` -- Directly matches the claim. |
| 43 | Requests are answered within two working days. | 37 | carried | 'they are answered within two working days' in `merged.md` -- Directly matches the claim. |
| 44 | There is no expedited path. | 37 | carried | 'There is no expedited path' in `merged.md` -- Directly matches the claim. |
| 45 | There is no exception list. | 37 | carried | 'and no exception list' in `merged.md` -- Directly matches the claim. |

### `source_b.md` -- 46 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 46 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Every credential has a cap of its own. | 3 | carried | 'Every credential has a cap.' in `merged.md` -- States each credential has its own cap. |
| 2 | When the cap is spent, the gateway answers 429 at the edge, without troubling the service behind it. | 3 | carried | 'the gateway answers 429 at the edge without waking the service behind it' in `merged.md` -- Matches the claim about not troubling the service behind it. |
| 3 | Requests are counted against the credential rather than the connection. | 5 | carried | 'Requests are counted against the credential that presented them rather than the connection' in `merged.md` -- Directly matches the claim. |
| 4 | The window over which requests are counted is a fixed window of 60 seconds. | 5 | carried | 'over a fixed window of 60 seconds' in `merged.md` -- Directly matches the claim. |
| 5 | The gateway doesn't disclose the start of the counting window. | 5 | carried | 'whose start the gateway does not disclose' in `merged.md` -- Directly matches the claim. |
| 6 | The count follows the credential wherever the caller happens to put it, including across hosts. | 5 | carried | 'The count follows the credential wherever the caller places it, including across hosts' in `merged.md` -- The text states this almost verbatim. |
| 7 | A caller spread over many worker processes is throttled at the same point a single process would have been. | 5 | carried | 'so a client spread across eight worker processes is throttled at exactly the point one process would have been' in `merged.md` -- The specific instance of eight processes entails the general claim about many worker processes. |
| 8 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- Directly stated. |
| 9 | The header that communicates the wait time is called Retry-After. | 11 | carried | 'The refusal carries a header called Retry-After.' in `merged.md` -- Directly stated. |
| 10 | The value of the Retry-After header is a whole number of seconds. | 11 | carried | 'Its value is a whole number of seconds to wait' in `merged.md` -- Directly stated. |
| 11 | The Retry-After header is present on every refusal the gateway sends. | 11 | carried | 'it is present on every refusal the gateway sends' in `merged.md` -- Directly stated. |
| 12 | The response body is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- Directly stated. |
| 13 | The response body repeats the cap, the window and the tier as plain fields. | 13 | carried | 'it names what the gateway calls the “window” it counted in, along with the cap and the tier' in `merged.md` -- The body includes window, cap, and tier fields as described. |
| 14 | The gateway has already done the wait-time arithmetic. | 19 | carried | 'The gateway has already done that arithmetic' in `merged.md` -- Directly stated. |
| 15 | The gateway did the wait-time arithmetic with information the caller cannot see. | 19 | carried | 'with information the caller does not have' in `merged.md` -- Directly stated. |
| 16 | On the 503 path, the same rule of honouring the header and not computing your own wait holds. | 19 | carried | 'and it does the same on the 503 path' in `merged.md` -- The rule of honoring the header applies to the 503 path as well. |
| 17 | The cause of the refusal on the 503 path is an entirely different one from the 429 path. | 19 | carried | 'even though the cause of that refusal is an entirely different one' in `merged.md` -- Directly stated regarding the 503 cause differing from 429. |
| 18 | A 200 response needs nothing. | 21 | carried | 'A 200 wants nothing' in `merged.md` -- Directly stated. |
| 19 | A 429 response needs the stated wait. | 21 | carried | 'a 429 wants the stated wait' in `merged.md` -- Directly stated. |
| 20 | A 500 response can be retried once that wait has passed. | 21 | carried | 'a 500 may be retried once that wait has passed' in `merged.md` -- Directly stated. |
| 21 | A 503 response means the platform itself is overloaded. | 21 | carried | 'a 503 is the overload path' in `merged.md` -- The 503 being the overload path entails the platform being overloaded. |
| 22 | A batch credential is allowed 1000 requests in a window. | 23 | carried | 'A credential marked for batch work is allowed 1000 requests in a window' in `merged.md` -- Directly stated. |
| 23 | 1000 requests in a window is 50 times the default allowance. | 23 | carried | 'fifty times the default allowance' in `merged.md` -- Directly stated. |
| 24 | The batch credential's allowance is not a separate counting scheme. | 23 | carried | 'and it is not a separate counting scheme' in `merged.md` -- Directly stated. |
| 25 | The window, the header and the body are identical for the batch tier and the interactive case. | 23 | carried | 'the window, the header and the body are identical to the interactive case' in `merged.md` -- Directly stated. |
| 26 | A client written for one tier needs no change at all to run against the other tier. | 23 | carried | 'so a client written for one tier needs no change at all to run against the other' in `merged.md` -- Directly stated. |
| 27 | Nothing else about the batch tier differs from the default. | 23 | carried | 'Nothing else about the two tiers differs in any way.' in `merged.md` -- Directly stated. |
| 28 | The log of refusals should be kept for at least a week. | 25 | carried | 'keep the log for at least a week' in `merged.md` -- Directly stated. |
| 29 | The platform team will not assemble a case for a larger cap on a caller's behalf. | 25 | carried | 'nobody at the far end will assemble that argument on its behalf' in `merged.md` -- Directly stated. |
| 30 | The gateway refuses a request for three separate reasons. | 29 | carried | 'The gateway refuses a request for three separate reasons' in `merged.md` -- Directly stated. |
| 31 | Only one of the three reasons the gateway refuses a request is a cap. | 29 | carried | 'The gateway refuses a request for three separate reasons, and only one of them is the one above.' in `merged.md` -- Directly stated. |
| 32 | Two of the three reasons the gateway refuses a request have nothing to do with how much traffic a caller has sent in the window it is currently in. | 29 | carried | 'two of the three have nothing to do with how much traffic a caller has sent in the window it is currently in' in `merged.md` -- Directly stated. |
| 33 | A credential can be suspended. | 29 | carried | 'A credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit and be refused before it has even been read.' in `merged.md` -- Directly stated. |
| 34 | A route can be closed while it is being repaired. | 29 | carried | 'a route may be closed for maintenance' in `merged.md` -- Maintenance closure matches being repaired in meaning. |
| 35 | A request body over the 5 megabyte limit is refused before it has been read at all. | 29 | carried | 'a body may exceed the 5 megabyte limit and be refused before it has even been read' in `merged.md` -- Directly stated. |
| 36 | A loop retrying against a suspended credential burns its whole budget and reaches nothing. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `merged.md` -- Directly stated. |
| 37 | The log afterwards shows a long run of refusals and no successes at all. | 31 | carried | 'the log afterwards shows nothing at all except a long run of refusals and no successes' in `merged.md` -- Directly stated. |
| 38 | A cap can be raised. | 33 | carried | 'A cap can be raised, but not on the strength of an assertion that the current one is too small' in `merged.md` -- Directly stated. |
| 39 | A cap cannot be raised on the strength of an assertion that the current one is too small. | 33 | carried | 'A cap can be raised, but not on the strength of an assertion that the current one is too small — the number of caps raised without a measurement behind them is 0.' in `merged.md` -- Directly stated. |
| 40 | A caller seeking a larger cap should bring the refusal counts for a full week. | 33 | carried | 'Bring a week of refusal counts, the shape of the traffic across the day, and the deadline that traffic is serving.' in `merged.md` -- Directly stated. |
| 41 | A caller seeking a larger cap should bring the shape of the traffic across the day. | 33 | carried | 'the shape of the traffic across the day' in `merged.md` -- Directly stated. |
| 42 | A caller seeking a larger cap should bring the deadline the traffic exists to meet. | 33 | carried | 'the deadline that traffic is serving' in `merged.md` -- Directly stated. |
| 43 | The platform team wants to know whether the load is smooth or bursty before it looks at the number at all. | 35 | carried | 'The platform team wants to know whether the load is smooth or bursty before it looks at the number at all' in `merged.md` -- Directly stated. |
| 44 | Requests go to the platform team through the usual channel. | 35 | carried | 'Requests reach the platform team through the usual channel' in `merged.md` -- Directly stated. |
| 45 | There is no expedited path for requesting a cap increase. | 37 | carried | 'There is no expedited path and no exception list.' in `merged.md` -- Directly stated. |
| 46 | An answer to a cap increase request takes two working days. | 37 | carried | 'they are answered within two working days' in `merged.md` -- Directly stated. |

### `merged.md` -- 47 claim(s): 0 invented, 0 contradicted, 0 supported in part, 47 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Every credential has a cap. | supported | `source_a.md` | 'Every credential has a cap.' in `source_a.md` -- Directly stated in source_a. |
| 2 | When that cap is spent, the gateway answers 429 at the edge without waking the service behind it. | supported | `source_a.md` | 'the gateway answers 429 at the edge — without waking the service behind it' in `source_a.md` -- Directly stated in source_a. |
| 3 | Requests are counted against the credential that presented them rather than the connection. | supported | `source_a.md` | 'Requests are counted against the credential that presented them, over a fixed window of 60 seconds, and never against a connection.' in `source_a.md` -- Directly stated in source_a. |
| 4 | The window used for counting requests is a fixed 60 seconds, and the gateway does not disclose when that window starts. | supported | `source_b.md` | 'over a fixed window of 60 seconds whose start the gateway doesn’t disclose' in `source_b.md` -- Directly stated in source_b. |
| 5 | Opening a second socket buys a caller nothing. | supported | `source_a.md` | 'Opening a second socket therefore buys a caller nothing.' in `source_a.md` -- Directly stated in source_a. |
| 6 | The count follows the credential wherever the caller places it, including across hosts. | supported | `source_b.md` | 'The count follows the credential wherever the caller happens to put it, including across hosts.' in `source_b.md` -- Directly stated in source_b. |
| 7 | A client spread across eight worker processes is throttled at exactly the point one process would have been. | supported | `source_a.md` | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `source_a.md` -- Directly stated in source_a. |
| 8 | A client spread across eight worker processes pays for the extra file descriptors as well. | supported | `source_a.md` | 'and pays for the extra file descriptors as well.' in `source_a.md` -- Directly stated in source_a. |
| 9 | The default allowance is 100 requests in a window. | supported | `source_a.md` | 'The default allowance is 100 requests in a window' in `source_a.md` -- Directly stated in source_a. |
| 10 | A credential marked for batch work is allowed 1000 requests in the same window. | supported | `source_a.md` | 'a credential marked for batch work is allowed 1000 in the same window.' in `source_a.md` -- Directly stated in source_a. |
| 11 | The refusal carries a header called Retry-After. | supported | `source_a.md` | 'The refusal carries a Retry-After header.' in `source_a.md` -- Directly stated in source_a. |
| 12 | The Retry-After header's value is a whole number of seconds to wait. | supported | `source_a.md` | 'Its value is a whole number of seconds to wait.' in `source_a.md` -- Directly stated in source_a. |
| 13 | The Retry-After header is present on every refusal the gateway sends. | supported | `source_b.md` | 'it is present on every refusal the gateway sends' in `source_b.md` -- Directly stated in source_b. |
| 14 | The gateway keeps no memory of who backed off politely. | supported | `source_a.md` | 'The gateway keeps no memory of who backed off politely' in `source_a.md` -- Directly stated in source_a. |
| 15 | Waiting longer than the Retry-After header asks earns a caller no credit at all. | supported | `source_a.md` | 'waiting longer than the header asks earns a caller no credit at all.' in `source_a.md` -- Directly stated in source_a. |
| 16 | The body of the refusal is JSON. | supported | `source_a.md` | 'The body of the refusal is JSON' in `source_a.md` -- Directly stated in source_a. |
| 17 | The body of the refusal names what the gateway calls the "window" it counted in, along with the cap and the tier. | supported | `source_a.md` | 'it names what the gateway calls the “window” it counted in. It names the cap and the tier as well.' in `source_a.md` -- Directly stated in source_a. |
| 18 | The body is there so that a human reading a log afterwards can see why the request was refused. | supported | `source_a.md` | 'The body is there so that a human reading a log afterwards can see why the request was refused' in `source_a.md` -- Directly stated in source_a. |
| 19 | The gateway has already done the wait-time arithmetic, with information the caller does not have. | supported | `source_a.md` | 'The gateway has already done that arithmetic, with information the caller does not have' in `source_a.md` -- Directly stated in source_a. |
| 20 | The gateway does the same wait-time arithmetic on the 503 path. | supported | `source_a.md` | 'and it does the same on the 503 path.' in `source_a.md` -- Directly stated in source_a. |
| 21 | The cause of a 503 refusal is an entirely different one from a 429 refusal. | supported | `source_b.md` | 'On the 503 path the same rule holds, even though the cause of the refusal is an entirely different one.' in `source_b.md` -- Directly stated in source_b. |
| 22 | A 500 response may be retried once that wait has passed. | supported | `source_a.md` | 'a 500 may be retried once that wait has passed' in `source_a.md` -- Directly stated in source_a. |
| 23 | A 503 response is the overload path. | supported | `source_a.md` | 'a 503 is the overload path.' in `source_a.md` -- Directly stated in source_a. |
| 24 | A credential marked for batch work is allowed 1000 requests in a window. | supported | `source_a.md` | 'a credential marked for batch work is allowed 1000 in the same window.' in `source_a.md` -- Directly stated in source_a, restating the batch allowance. |
| 25 | The batch allowance of 1000 requests is fifty times the default allowance. | supported | `source_a.md` | 'A batch credential is allowed fifty times the default allowance' in `source_a.md` -- Directly stated in source_a, and confirmed as 50 times in source_b. |
| 26 | The batch allowance is measured over exactly the same window as the interactive allowance. | supported | `source_a.md` | 'A batch credential is allowed fifty times the default allowance, and it is measured over exactly the same window.' in `source_a.md` -- Source_a states the batch allowance is measured over exactly the same window as the default. |
| 27 | The batch allowance is not a separate counting scheme. | supported | `source_b.md` | 'which is 50 times the default and not a separate counting scheme' in `source_b.md` -- Source_b explicitly states the batch allowance is not a separate counting scheme. |
| 28 | The tier is set on the credential when it is issued. | supported | `source_a.md` | 'The tier is set on the credential when it is issued and cannot be asked for per call.' in `source_a.md` -- Source_a states the tier is set when the credential is issued. |
| 29 | The tier cannot be asked for per call. | supported | `source_a.md` | 'The tier is set on the credential when it is issued and cannot be asked for per call.' in `source_a.md` -- Source_a states the tier cannot be requested per call. |
| 30 | The window, the header and the body are identical between the batch and interactive cases. | supported | `source_b.md` | 'The window, the header and the body are identical to the interactive case, so a client written for one tier needs no change at all to run against the other.' in `source_b.md` -- Source_b explicitly states these three elements are identical between tiers. |
| 31 | Nothing else about the batch and interactive tiers differs in any way. | supported | `source_a.md` | 'Nothing else about the two tiers differs in any way.' in `source_a.md` -- Source_a states this exact fact about the tiers. |
| 32 | The gateway refuses a request for three separate reasons. | supported | `source_b.md` | 'The gateway refuses a request for three separate reasons, and only one of them is a cap.' in `source_b.md` -- Source_b states the gateway refuses requests for three separate reasons. |
| 33 | Only one of the three reasons the gateway refuses a request is the rate-limiting cap. | supported | `source_b.md` | 'The gateway refuses a request for three separate reasons, and only one of them is a cap.' in `source_b.md` -- Source_b states only one of the three reasons is the rate-limiting cap. |
| 34 | A credential may be suspended. | supported | `source_a.md` | 'A credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit.' in `source_a.md` -- Source_a lists credential suspension as one of the three refusal reasons. |
| 35 | A route may be closed for maintenance. | supported | `source_a.md` | 'A credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit.' in `source_a.md` -- Source_a states a route may be closed for maintenance. |
| 36 | A body may exceed the 5 megabyte limit and be refused before it has even been read. | supported | `source_b.md` | 'a request body over the 5 megabyte limit is refused before it has been read at all' in `source_b.md` -- Source_b states the 5MB body limit results in refusal before the body is read. |
| 37 | None of the three refusal reasons clears itself by waiting for a stated number of seconds. | supported | `source_a.md` | 'None of those three clears itself by waiting for a stated number of seconds.' in `source_a.md` -- Source_a states none of the three refusal reasons clears with waiting. |
| 38 | Two of the three refusal reasons have nothing to do with how much traffic a caller has sent in the window it is currently in. | supported | `source_b.md` | 'Two of the three have nothing to do with how much traffic a caller has sent in the window it is currently in.' in `source_b.md` -- Source_b states this exact fact about two of the three refusal reasons. |
| 39 | A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service. | supported | `source_a.md` | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `source_a.md` -- Source_a states this exact fact about retry loops against suspended credentials. |
| 40 | In that case, the log afterwards shows nothing at all except a long run of refusals and no successes. | supported | `source_b.md` | 'The log afterwards shows a long run of refusals and no successes at all' in `source_b.md` -- Source_b states the log shows a long run of refusals and no successes. |
| 41 | A cap can be raised. | supported | `source_a.md` | 'A cap can be raised, and the number of caps raised without a measurement behind them is 0.' in `source_a.md` -- Source_a states a cap can be raised. |
| 42 | The number of caps raised without a measurement behind them is 0. | supported | `source_a.md` | 'A cap can be raised, and the number of caps raised without a measurement behind them is 0.' in `source_a.md` -- Source_a states the number of caps raised without measurement is 0. |
| 43 | The platform team wants to know whether the load is smooth or bursty before it looks at the number at all. | supported | `source_b.md` | 'The team wants to know whether the load is smooth or bursty before it looks at the number at all.' in `source_b.md` -- Source_b states this exact fact about the platform team's priorities. |
| 44 | Requests reach the platform team through the usual channel. | supported | `source_a.md` | 'Requests reach the platform team through the usual channel, and they are answered within two working days.' in `source_a.md` -- Source_a states requests reach the platform team through the usual channel. |
| 45 | Requests to the platform team are answered within two working days. | supported | `source_a.md` | 'Requests reach the platform team through the usual channel, and they are answered within two working days.' in `source_a.md` -- Source_a states requests are answered within two working days. |
| 46 | There is no expedited path. | supported | `source_a.md` | 'There is no expedited path and no exception list.' in `source_a.md` -- Source_a states there is no expedited path. |
| 47 | There is no exception list. | supported | `source_a.md` | 'There is no expedited path and no exception list.' in `source_a.md` -- Source_a states there is no exception list. |

## Structure

**9** mechanical check(s) over **104** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **47** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **91**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 23 run(s) over 43 attributed segment(s) — sources interleaved. 6 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Verbatim violation — an invariant-core token did not survive unchanged

- `b31` (`source_b.md`) — numeric '50' (times) does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **89** departure(s) from its sources. Checking them confirms 51, rejects 5, and leaves 33 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 104 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | Base title chosen over b1's alternative. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Rate limiting and the 429 contract for gateway clients' and says so (no claim traced to it) |
| `a3` | reworded | Punctuation simplified from dashes to commas. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-001`, `A-002`) |
| `b2` | superseded | a2's simpler wording kept for the same fact. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-001`) |
| `b3` | superseded | a3's fuller wording kept for the same fact. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-002`) |
| `b4` | reworded | Unique content kept, lightly reworded for flow. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a4` | reconciled | Combined with b5's detail about the undisclosed window start. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-003`, `A-004`, `A-005`) |
| `b5` | reconciled | Combined with a4's phrasing of the same counting rule. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-003`, `B-004`, `B-005`) |
| `b6` | superseded | a5's wording kept for the same fact. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a6` | reworded | Combined with b7 and b8's detail on placement across hosts. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-007`, `A-008`) |
| `b7` | subsumed | Cross-host detail folded into the combined sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-006`) |
| `b8` | subsumed | General 'many processes' narrowed by a6's specific eight. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-007`) |
| `a7` | reconciled | Combined with b9's note on interactive sufficiency. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-009`, `A-010`) |
| `b9` | reconciled | Combined with a7's default and batch figures. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-008`) |
| `a8` | reconciled | Combined with a9 and b10 into one statement. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `a9` | reconciled | Combined with a8 and b10 into one statement. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b10` | reconciled | Its 'not a bug' detail combined with a8 and a9. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b11` | superseded | a10's wording kept for the same fact. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b12` | duplicate | Identical heading text to a11, kept once. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `a12` | reworded | Merged with b13's phrasing of the same fact. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-011`) |
| `b13` | duplicate | Same fact as a12, stated once. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-009`) |
| `a13` | reconciled | Combined with b14's detail that it is always present. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-012`) |
| `b14` | reconciled | Its presence detail combined with a13's value format. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-010`, `B-011`) |
| `a14` | reconciled | Combined with b15's addendum about the note's purpose. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b15` | reconciled | Its addendum combined with a14's core statement. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b16` | superseded | a15's wording kept for the same fact. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a16` | reworded | Combined with a17's detail and matches b17. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-015`, `A-016`) |
| `a17` | subsumed | Folded into the combined sentence about body fields. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-017`, `A-018`) |
| `b17` | duplicate | Same fields as a16/a17, stated once. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-012`, `B-013`) |
| `a18` | reconciled | Combined a18's arithmetic point with b18's drift point. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-019`, `A-020`) |
| `b18` | reconciled | Its drift point combined with a18's arithmetic point. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b19` | superseded | a19's fuller wording kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b20` | superseded | Base heading chosen over b's alternative for this section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b21` | superseded | a21's concise wording kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a22` | reconciled | Combined with b22's explicit instruction not to compute a wait. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b22` | reconciled | Its instruction combined with a22's rule. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `a23` | reconciled | Combined with b24's nuance about the differing cause. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-021`, `A-022`) |
| `b24` | reconciled | Its nuance combined with a23's statement. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-016`, `B-017`) |
| `b23` | duplicate | Restates a23's fact, folded into the combined sentence. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-014`, `B-015`) |
| `a24` | reworded | a24's more specific wording kept over b25. | **rejected** | declared 'reworded', and its text is in the merge (no claim traced to it) |
| `b25` | superseded | Same fact as a24, base wording kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a25` | reworded | a25's wording kept over b26. | **rejected** | declared 'reworded', and its text is in the merge (no claim traced to it) |
| `b26` | superseded | Same fact as a25, base wording kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a26` | reconciled | Combined with b27's clarifying clause. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b27` | reconciled | Its clarifying clause combined with a26's rule. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `a27` | reworded | a27's wording kept over b28. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-023`, `A-024`, `A-025`, `A-026`) |
| `b28` | superseded | Same fact as a27, base wording kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-018`, `B-019`, `B-020`, `B-021`) |
| `a28` | reworded | Joined with a29 into one sentence. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a29` | reworded | a29's wording kept over b29, joined with a28. | **rejected** | declared 'reworded', and its text is in the merge (no claim traced to it) |
| `b29` | superseded | Same fact as a29, base wording kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b30` | superseded | a30's imperative kept over b30's explanation. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a32` | reconciled | Combined with b31's ratio and 'not a separate scheme' detail. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-027`, `A-028`) |
| `b31` | reconciled | Its detail combined with a32's statement of the tier. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-022`, `B-023`, `B-024`) |
| `a33` | reconciled | Combined with b32's point about identical fields. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-029`, `A-030`) |
| `b32` | reconciled | Its equivalence point combined with a33's issuance rule. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-025`, `B-026`) |
| `b33` | superseded | a34's wording kept for the same fact. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-027`) |
| `a35` | reconciled | Combined with b34's added retention detail. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b34` | reconciled | Its retention detail combined with a35's instruction. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-028`) |
| `a36` | reworded | a36's wording kept over b35. | **rejected** | declared 'reworded', and its text is in the merge (no claim traced to it) |
| `b35` | superseded | Same fact as a36, base wording kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-029`) |
| `a37` | reconciled | Combined with b36's point about counts being the argument. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b36` | reconciled | Its point combined with a37's list of log fields. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b37` | superseded | Base heading chosen for this section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a39` | reworded | Clarified with 'refusals' for readability. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a40` | reconciled | Same fact as b38, stated once. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-032`) |
| `b38` | reconciled | Duplicate of a40, folded into one statement. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-030`, `B-031`) |
| `a41` | reconciled | Combined with b40's detail that oversized bodies are refused unread. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-033`, `A-034`, `A-035`) |
| `b40` | reconciled | Its detail combined with a41's list of causes. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-033`, `B-034`, `B-035`) |
| `a42` | reconciled | Combined with b39's point about traffic-unrelated causes. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-036`) |
| `b39` | reconciled | Its point combined with a42's statement. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-032`) |
| `a43` | reconciled | Combined with b41's comparison to a reader. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b41` | reconciled | Its comparison combined with a43's statement. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `a44` | reconciled | Combined with b42 and b43's added detail. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-037`, `A-038`) |
| `b42` | reconciled | Its budget statement combined with a44 and b43. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-036`) |
| `b43` | reconciled | Its added detail combined with a44 and b42. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-037`) |
| `a47` | reconciled | Combined a47's figure with b46's phrasing. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-039`, `A-040`) |
| `b46` | reconciled | Its phrasing combined with a47's figure of 0. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-038`, `B-039`) |
| `a48` | reworded | a48's wording kept over b47. | **rejected** | declared 'reworded', and its text is in the merge (no claim traced to it) |
| `b47` | superseded | Same fact as a48, base wording kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-040`, `B-041`, `B-042`) |
| `a49` | reconciled | Combined with b48's 'before the number' detail and b49. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-041`) |
| `b48` | reconciled | Its 'before the number' detail combined with a49. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-043`) |
| `b49` | reconciled | Duplicate clause folded into the combined sentence. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `a50` | reconciled | Combined with b44 and b45's addendum. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b44` | reconciled | Its phrasing combined with a50's statement. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b45` | reconciled | Its addendum combined with a50 and b44. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `a51` | reconciled | Combined with b50 and b52's addendum about chasing. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-042`, `A-043`) |
| `b50` | reconciled | Its channel statement combined with a51. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-044`) |
| `b52` | reconciled | Its addendum about chasing combined with a51. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-046`) |
| `a52` | reworded | a52's fuller wording kept over b51. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-044`, `A-045`) |
| `b51` | superseded | Same fact as a52, base wording kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-045`) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | ec0c9ecb43e3 (hosted) |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | claude-sonnet-5 |
| Model (decompose) | claude-sonnet-5 |
| Model (verify) | claude-sonnet-5 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile anthropic |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 10 live, 0 cached, 0 replayed |
| Tokens | 50,396 in, 94,952 out |
| Cost | ~$1.05 estimated (rates read 2026-08-31) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 733.7s |
| Generated | 2026-09-27T16:39:01+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
