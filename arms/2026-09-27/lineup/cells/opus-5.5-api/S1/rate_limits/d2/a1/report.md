## Verdict

**3 finding(s).** In the structure: 1 false departure, 1 verbatim violation, 1 declared loss over budget.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 64 |
| Claims extracted from `source_a.md` | 42 |
| Claims extracted from `source_b.md` | 70 |
| Forward — source claims accounted for in the merge | **112/112** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **42/42** |
| Forward — `source_b.md` claims accounted for | **70/70** |
| Reverse — merge claims found in a source | **64/64** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **176/176** |
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

### `source_a.md` -- 42 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 42 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Every credential has a cap. | 3 | carried | 'Every credential has a cap of its own.' in `merged.md` -- The text states directly that every credential has its own cap. |
| 2 | When a credential's cap is spent the gateway answers 429 at the edge. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge' in `merged.md` -- The text states that the gateway answers 429 at the edge when the cap is spent. |
| 3 | The gateway's 429 refusal does not wake the service behind the gateway. | 3 | carried | 'without waking the service behind it' in `merged.md` -- The text says the 429 is answered without waking the service behind the gateway. |
| 4 | Requests are counted against the credential that presented them. | 5 | carried | 'Requests are counted against the credential that presented them' in `merged.md` -- The text states this directly. |
| 5 | Requests are counted over a fixed window of 60 seconds. | 5 | carried | 'over a fixed window of 60 seconds' in `merged.md` -- The text states that the counting window is a fixed 60 seconds. |
| 6 | Requests are never counted against a connection. | 5 | carried | 'and never against a connection' in `merged.md` -- The text states that requests are never counted against a connection. |
| 7 | Opening a second socket does not increase a caller's allowance. | 5 | carried | 'so opening a second socket buys a caller nothing' in `merged.md` -- Saying a second socket buys nothing means it does not increase the caller's allowance. |
| 8 | A client spread across eight worker processes is throttled at exactly the point one process would have been. | 5 | carried | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `merged.md` -- The text states this directly. |
| 9 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- The text states the default allowance directly. |
| 10 | A credential marked for batch work is allowed 1000 requests in the same window. | 7 | carried | 'A credential marked for batch work is allowed 1000 in the same window.' in `merged.md` -- The text states this value, although it elsewhere also gives fifty times the default, which is a conflict for separate recording. |
| 11 | Callers that retry at once are the largest single reason the cap exists. | 7 | carried | 'Callers that retry at once are most of the reason the cap is there at all.' in `merged.md` -- Being most of the reason entails being the largest single reason the cap exists. |
| 12 | The 429 refusal carries a Retry-After header. | 11 | carried | 'Every refusal carries a Retry-After header' in `merged.md` -- In the context of the 429 refusal, every refusal carries a Retry-After header. |
| 13 | The Retry-After header value is a whole number of seconds to wait. | 11 | carried | 'whose value is a whole number of seconds to wait' in `merged.md` -- The text states that the header value is a whole number of seconds to wait. |
| 14 | The gateway keeps no memory of who backed off politely. | 11 | carried | 'The gateway keeps no memory of who backed off politely' in `merged.md` -- The text states this directly. |
| 15 | Waiting longer than the Retry-After header asks earns a caller no credit. | 11 | carried | 'waiting longer than the header asks earns a caller no credit at all' in `merged.md` -- The text states this directly. |
| 16 | The body of the 429 refusal is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- The text states that the refusal body is JSON. |
| 17 | The body of the 429 refusal names the window the gateway counted in. | 13 | carried | 'it repeats the cap, the tier and what the gateway calls the “window” it counted in as plain fields' in `merged.md` -- The text says the body includes the window the gateway counted in. |
| 18 | The body of the 429 refusal names the cap. | 13 | carried | 'it repeats the cap, the tier and what the gateway calls the “window” it counted in as plain fields' in `merged.md` -- The text says the body includes the cap. |
| 19 | The body of the 429 refusal names the tier. | 13 | carried | 'it repeats the cap, the tier and what the gateway calls the “window” it counted in as plain fields' in `merged.md` -- The text says the body includes the tier. |
| 20 | The gateway computes the Retry-After wait on the 503 path as well. | 19 | carried | 'the same rule holds on the 503 path' in `merged.md` -- The rule of honouring the gateway-computed header wait is stated to hold on the 503 path as well. |
| 21 | A 500 response may be retried once the stated wait has passed. | 21 | carried | 'a 500 may be retried once that wait has passed' in `merged.md` -- The text states this directly. |
| 22 | A 503 response is the overload path. | 21 | carried | 'a 503 is the overload path' in `merged.md` -- The text states this directly. |
| 23 | A batch credential is allowed fifty times the default allowance. | 23 | carried | 'A batch credential is allowed fifty times the default allowance' in `merged.md` -- The text states this value, which conflicts with the 1000 figure given elsewhere, a conflict to be recorded separately. |
| 24 | A batch credential is measured over exactly the same window as the default tier. | 23 | carried | 'it is measured over exactly the same window' in `merged.md` -- The text states that the batch credential is measured over exactly the same window. |
| 25 | The tier is set on the credential when it is issued. | 23 | carried | 'The tier is set on the credential when it is issued' in `merged.md` -- The text states this directly. |
| 26 | The tier cannot be requested per call. | 23 | carried | 'The tier is set on the credential when it is issued and cannot be asked for per call.' in `merged.md` -- The text states the tier cannot be asked for per call. |
| 27 | Nothing else about the batch and default tiers differs. | 23 | carried | 'nothing else about the two tiers differs in any way' in `merged.md` -- The text states nothing else about the two tiers differs. |
| 28 | The gateway refuses a request for three reasons. | 29 | carried | 'The gateway refuses a request for three separate reasons' in `merged.md` -- The text states the gateway refuses requests for three separate reasons. |
| 29 | A credential may be suspended. | 29 | carried | 'A credential may be suspended' in `merged.md` -- The text states this directly. |
| 30 | A route may be closed for maintenance. | 29 | carried | 'a route may be closed for maintenance while it is repaired' in `merged.md` -- The text states a route may be closed for maintenance. |
| 31 | The request body limit is 5 megabytes. | 29 | carried | 'a body may exceed the 5 megabyte limit' in `merged.md` -- The text gives a 5 megabyte body limit. |
| 32 | Suspended credentials, closed routes and oversized bodies do not clear by waiting for a stated number of seconds. | 29 | carried | 'None of those three clears itself by waiting for a stated number of seconds.' in `merged.md` -- The three refusal types are stated not to clear by waiting a stated number of seconds. |
| 33 | A loop that waits and retries against a suspended credential never reaches the service. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget — the caller’s own — without ever reaching the service' in `merged.md` -- The text states such a loop never reaches the service. |
| 34 | A cap can be raised. | 35 | carried | 'A cap can be raised' in `merged.md` -- The text states a cap can be raised. |
| 35 | The number of caps raised without a measurement behind them is 0. | 35 | carried | 'the number of caps raised without a measurement behind them is 0' in `merged.md` -- The text states this figure exactly. |
| 36 | The platform team looks at whether the load is smooth or bursty. | 35 | carried | 'the platform team looks at whether the load is smooth or bursty' in `merged.md` -- The text states the platform team examines whether load is smooth or bursty. |
| 37 | A burst is cheaper to smooth than to serve at its peak. | 35 | carried | 'a burst is cheaper to smooth than it is to serve at its peak' in `merged.md` -- The text states this directly. |
| 38 | A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap. | 35 | carried | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `merged.md` -- The text states this directly. |
| 39 | Requests for a cap increase reach the platform team through the usual channel. | 37 | carried | 'Requests reach the platform team through the usual channel' in `merged.md` -- In the increase section, requests are stated to reach the team through the usual channel. |
| 40 | Requests for a cap increase are answered within two working days. | 37 | carried | 'they are answered within two working days' in `merged.md` -- The text states requests are answered within two working days. |
| 41 | There is no expedited path for cap increase requests. | 37 | carried | 'There is no expedited path and no exception list.' in `merged.md` -- The text states there is no expedited path. |
| 42 | There is no exception list for cap increase requests. | 37 | carried | 'There is no expedited path and no exception list.' in `merged.md` -- The text states there is no exception list. |

### `source_b.md` -- 70 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 70 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Every credential has a cap of its own. | 3 | carried | 'Every credential has a cap of its own.' in `merged.md` -- The text states this verbatim. |
| 2 | When the cap is spent the gateway answers 429 at the edge. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge' in `merged.md` -- The text states the gateway answers 429 at the edge when the cap is spent. |
| 3 | When the cap is spent the gateway answers without troubling the service behind it. | 3 | carried | 'without waking the service behind it' in `merged.md` -- Not waking the service behind it means not troubling it. |
| 4 | Requests are counted against the credential rather than the connection. | 5 | carried | 'Requests are counted against the credential that presented them, over a fixed window of 60 seconds whose start the gateway does not disclose, and never against a connection.' in `merged.md` -- Requests are counted against the credential and never against a connection. |
| 5 | Requests are counted over a fixed window of 60 seconds. | 5 | carried | 'over a fixed window of 60 seconds' in `merged.md` -- The text states a fixed 60-second window. |
| 6 | The gateway doesn't disclose the start of the 60-second window. | 5 | carried | 'whose start the gateway does not disclose' in `merged.md` -- The text states the gateway does not disclose the window start. |
| 7 | There is nothing to be gained by opening more sockets to avoid the gateway's cap. | 5 | carried | 'so opening a second socket buys a caller nothing' in `merged.md` -- Opening additional sockets is stated to gain nothing. |
| 8 | The request count follows the credential wherever the caller puts it, including across hosts. | 5 | carried | 'The count follows the credential wherever the caller puts it, including across hosts' in `merged.md` -- The text states this directly. |
| 9 | A caller spread over many worker processes is throttled at the same point a single process would have been. | 5 | carried | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `merged.md` -- The text says a client spread across multiple worker processes is throttled at the same point as a single process, because the count follows the credential. |
| 10 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- The text states the default allowance directly. |
| 11 | The default allowance of 100 requests is enough for every interactive use of the API the platform team has seen. | 7 | carried | 'which is enough for every interactive use of this API the platform team has seen' in `merged.md` -- The text states that 100 requests suffices for every interactive use the team has seen. |
| 12 | A caller that needs more than the default allowance is almost always doing batch work under an interactive credential. | 7 | carried | 'a caller that needs more than that is almost always doing batch work under an interactive credential' in `merged.md` -- The text states this directly. |
| 13 | A 429 refusal is not an outage. | 7 | carried | 'A refusal is not an outage' in `merged.md` -- The text states that a refusal is not an outage. |
| 14 | A 429 refusal is not a bug in the gateway. | 7 | carried | 'it is not a bug in the gateway' in `merged.md` -- The text states that a refusal is not a gateway bug. |
| 15 | A 429 refusal is capacity being held for a request somebody else has already been promised. | 7 | carried | 'It is the platform declining to spend capacity that has already been promised to somebody else' in `merged.md` -- The text describes a refusal as capacity already promised to somebody else. |
| 16 | Callers that retry immediately are most of the reason the cap exists. | 7 | carried | 'Callers that retry at once are most of the reason the cap is there at all.' in `merged.md` -- Retrying at once means retrying immediately, so the text states the claim. |
| 17 | The header on a refusal is called Retry-After. | 11 | carried | 'Every refusal carries a Retry-After header' in `merged.md` -- The text names the header Retry-After. |
| 18 | The Retry-After value is a whole number of seconds. | 11 | carried | 'whose value is a whole number of seconds to wait' in `merged.md` -- The text states the value is a whole number of seconds. |
| 19 | The Retry-After header is present on every refusal the gateway sends. | 11 | carried | 'Every refusal carries a Retry-After header' in `merged.md` -- The text says every refusal carries the header. |
| 20 | Waiting the Retry-After duration and then continuing is the entire contract. | 11 | carried | 'Waiting that long and then continuing is the whole of the contract' in `merged.md` -- The text states waiting then continuing is the whole contract. |
| 21 | Waiting longer than the Retry-After header asks earns nothing. | 11 | carried | 'waiting longer than the header asks earns a caller no credit at all' in `merged.md` -- The text states that waiting longer earns nothing. |
| 22 | The refusal response body is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- The text states the body is JSON. |
| 23 | The refusal response body repeats the cap, the window and the tier as plain fields. | 13 | carried | 'it repeats the cap, the tier and what the gateway calls the “window” it counted in as plain fields' in `merged.md` -- The same three fields are listed as plain fields. |
| 24 | None of the refusal response body fields is a substitute for the Retry-After header. | 13 | carried | 'None of those fields is a substitute for the header' in `merged.md` -- The text states this directly. |
| 25 | The refusal response body is for the human reading the log afterwards. | 13 | carried | 'The body is there so that a human reading a log afterwards can see why the request was refused' in `merged.md` -- The text says the body is for a human reading the log afterwards. |
| 26 | There are four rules for what the client does. | 17 | carried | 'Four rules, given in the order they should be applied.' in `merged.md` -- The text states there are four rules. |
| 27 | The four client rules should be applied in the order they are given. | 17 | carried | 'Four rules, given in the order they should be applied.' in `merged.md` -- The text states the rules are given in the order they should be applied. |
| 28 | Clients should honour the Retry-After header and not compute their own wait. | 19 | carried | 'Honour the header, every time, and never compute your own wait.' in `merged.md` -- The text states rule 1 directly. |
| 29 | The gateway computes the wait with information the caller cannot see. | 19 | carried | 'The gateway has already done that arithmetic, with information the caller does not have' in `merged.md` -- The text states the gateway computes the wait with information the caller lacks. |
| 30 | On the 503 path the rule to honour the header also holds. | 19 | carried | 'the same rule holds on the 503 path' in `merged.md` -- The text states the rule holds on the 503 path. |
| 31 | The cause of a 503 refusal is different from the cause of a 429 refusal. | 19 | carried | 'even though the cause of that refusal is an entirely different one' in `merged.md` -- The text states the 503 cause differs from the cap refusal. |
| 32 | Clients should retry only what is safe to retry. | 21 | carried | 'Retry only what is safe to retry' in `merged.md` -- The text states rule 2 directly. |
| 33 | The set of responses safe to retry is smaller than the set of responses that aren't a success. | 21 | carried | 'which is a smaller set than the set of responses that are not a success' in `merged.md` -- The text states the safe-to-retry set is smaller than the non-success set. |
| 34 | A 200 response needs nothing. | 21 | carried | 'A 200 wants nothing' in `merged.md` -- The text states directly that a 200 wants nothing. |
| 35 | A 429 response needs the stated wait. | 21 | carried | 'a 429 wants the stated wait' in `merged.md` -- The text states directly that a 429 wants the stated wait. |
| 36 | A 500 response can be retried once the stated wait has passed. | 21 | carried | 'a 500 may be retried once that wait has passed' in `merged.md` -- The text states that a 500 may be retried after the wait has passed. |
| 37 | A 503 response means the platform itself is overloaded. | 21 | carried | 'a 503 is the overload path, meaning the platform itself is overloaded' in `merged.md` -- The text states that a 503 means the platform itself is overloaded. |
| 38 | A caller that folds 200, 429, 500 and 503 into one branch will retry hardest during the incident the cap was installed to survive. | 21 | carried | 'A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive.' in `merged.md` -- The text makes the same point about folding response cases into one branch and retrying hardest during the incident the cap exists for. |
| 39 | A batch credential is allowed 1000 requests in a window. | 23 | carried | 'A credential marked for batch work is allowed 1000 in the same window.' in `merged.md` -- The text states that a batch credential is allowed 1000 requests per window. |
| 40 | The batch allowance is 50 times the default. | 23 | carried | 'A batch credential is allowed fifty times the default allowance' in `merged.md` -- The text states that the batch allowance is fifty times the default. |
| 41 | The batch allowance is not a separate counting scheme. | 23 | carried | 'not by a separate counting scheme' in `merged.md` -- The text states that batch is not measured by a separate counting scheme. |
| 42 | The window, the header and the body for the batch tier are identical to the interactive case. | 23 | carried | 'it is measured over exactly the same window, not by a separate counting scheme. The tier is set on the credential when it is issued and cannot be asked for per call. The header and the body are identical to the interactive case too' in `merged.md` -- This span states that the window is the same and that the header and body are identical to the interactive case. |
| 43 | A client written for one tier needs no change to run against the other tier. | 23 | carried | 'a client written for one tier needs no change at all to run against the other' in `merged.md` -- The text states directly that a client written for one tier needs no change to run against the other. |
| 44 | Nothing else about the batch tier differs from the default. | 23 | carried | 'nothing else about the two tiers differs in any way' in `merged.md` -- The text states that nothing else about the two tiers differs. |
| 45 | Clients should log every refusal they see. | 25 | carried | 'Log every refusal seen' in `merged.md` -- The text instructs clients to log every refusal seen. |
| 46 | Clients should keep the refusal log for at least a week. | 25 | carried | 'keep the log for at least a week' in `merged.md` -- The text instructs clients to keep the log for at least a week. |
| 47 | A caller that cannot say how often it was refused can't make a case for a larger cap. | 25 | carried | 'A caller that cannot say how often it was refused last week cannot argue for a larger cap' in `merged.md` -- The text states that such a caller cannot argue for a larger cap. |
| 48 | The platform team won't assemble the case for a larger cap on a caller's behalf. | 25 | carried | 'nobody at the far end will assemble that argument on its behalf' in `merged.md` -- The far end, meaning the platform side, will not assemble the argument on the caller's behalf. |
| 49 | The gateway refuses a request for three separate reasons. | 29 | carried | 'The gateway refuses a request for three separate reasons' in `merged.md` -- The text states directly that there are three separate refusal reasons. |
| 50 | Only one of the gateway's three refusal reasons is a cap. | 29 | carried | 'only one of them is the cap described above' in `merged.md` -- The text states that only one of the three refusal reasons is the cap. |
| 51 | Two of the three refusal reasons have nothing to do with how much traffic a caller has sent in the current window. | 29 | carried | 'the other two have nothing to do with how much traffic a caller has sent in the current window' in `merged.md` -- The text states that the other two reasons are unrelated to traffic in the current window. |
| 52 | A credential can be suspended. | 29 | carried | 'A credential may be suspended' in `merged.md` -- The text states that a credential may be suspended. |
| 53 | A route can be closed while it is being repaired. | 29 | carried | 'a route may be closed for maintenance while it is repaired' in `merged.md` -- The text states that a route may be closed while it is repaired. |
| 54 | The request body limit is 5 megabyte. | 29 | carried | 'a body may exceed the 5 megabyte limit' in `merged.md` -- The text states that the body limit is 5 megabyte. |
| 55 | A request body over the 5 megabyte limit is refused before it has been read. | 29 | carried | 'in which case it is refused before it has been read at all' in `merged.md` -- The text states that an oversized body is refused before it has been read. |
| 56 | A loop retrying against a suspended credential burns its whole budget and reaches nothing. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget — the caller’s own — without ever reaching the service' in `merged.md` -- The text states that such a loop spends its whole budget without reaching the service. |
| 57 | The log after retrying against a suspended credential shows a long run of refusals and no successes. | 31 | carried | 'the log afterwards shows nothing but a long run of refusals and no successes' in `merged.md` -- The text states that the log shows a long run of refusals and no successes. |
| 58 | A long run of refusals against a suspended credential is not an outage. | 31 | carried | 'which reads like an outage and is not one' in `merged.md` -- The text states that the run of refusals looks like an outage but is not one. |
| 59 | A caller that can move half its work to a quieter hour usually finds it doesn't need a larger cap. | 33 | carried | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `merged.md` -- Getting what it needs without any change to the cap means it does not need a larger cap. |
| 60 | A cap can be raised. | 33 | carried | 'A cap can be raised' in `merged.md` -- The text states verbatim that a cap can be raised. |
| 61 | A cap is not raised on the strength of an assertion that the current one is too small. | 33 | carried | 'but not on the strength of an assertion that the current one is too small' in `merged.md` -- The text states a cap is not raised on the strength of an assertion that the current one is too small. |
| 62 | A request for a larger cap should include the refusal counts for a full week. | 33 | carried | 'Bring a full week of refusal counts' in `merged.md` -- Requesters are told to bring a full week of refusal counts. |
| 63 | A request for a larger cap should include the shape of the traffic across the day. | 33 | carried | 'the shape of the traffic across the day' in `merged.md` -- The shape of the traffic across the day is listed among the things to bring. |
| 64 | A request for a larger cap should include the deadline the traffic exists to meet. | 33 | carried | 'the deadline that traffic is serving' in `merged.md` -- The deadline the traffic is serving is listed among the things to bring. |
| 65 | The platform team wants to know whether the load is smooth or bursty before it looks at the number. | 35 | carried | 'Before looking at the number at all, the platform team looks at whether the load is smooth or bursty' in `merged.md` -- The team checks smoothness or burstiness before looking at the number. |
| 66 | A burst is cheaper to smooth out than to serve at its peak. | 35 | carried | 'a burst is cheaper to smooth than it is to serve at its peak' in `merged.md` -- The text states a burst is cheaper to smooth than to serve at its peak. |
| 67 | Cap increase requests go to the platform team through the usual channel. | 35 | carried | 'Requests reach the platform team through the usual channel' in `merged.md` -- Requests reach the platform team through the usual channel. |
| 68 | There is no expedited path for cap increase requests. | 37 | carried | 'There is no expedited path and no exception list.' in `merged.md` -- The text states there is no expedited path. |
| 69 | An answer to a cap increase request takes two working days. | 37 | carried | 'they are answered within two working days' in `merged.md` -- Requests are answered within two working days, which carries the claimed two-working-day answer time. |
| 70 | Chasing an answer to a cap increase request doesn't make it take fewer days. | 37 | carried | 'chasing an answer does not make it take fewer' in `merged.md` -- The text states chasing an answer does not make it take fewer days. |

### `merged.md` -- 64 claim(s): 0 invented, 0 contradicted, 0 supported in part, 64 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Every credential has a cap of its own. | supported | `source_b.md` | 'Every credential has a cap of its own.' in `source_b.md` -- Source B states this verbatim. |
| 2 | When a credential's cap is spent the gateway answers 429 at the edge without waking the service behind it. | supported | `source_a.md` | 'When that cap is spent the gateway answers 429 at the edge — without waking the service behind it' in `source_a.md` -- Source A states the edge 429 without waking the backend service. |
| 3 | A 429 refusal at the gateway edge costs the platform almost nothing. | supported | `source_a.md` | 'so the refusal costs the platform almost nothing' in `source_a.md` -- Source A states the refusal costs the platform almost nothing. |
| 4 | An earlier draft of the rate limiting note argued for a client-side token bucket that mirrored the gateway's own counters. | supported | `source_b.md` | 'An earlier draft of this note argued for a client-side token bucket that mirrored the gateway’s own counters' in `source_b.md` -- Source B describes the earlier draft's token bucket argument. |
| 5 | Requests are counted against the credential that presented them. | supported | `source_a.md` | 'Requests are counted against the credential that presented them' in `source_a.md` -- Source A states this directly. |
| 6 | Requests are counted over a fixed window of 60 seconds. | supported | `source_a.md` | 'over a fixed window of 60 seconds' in `source_a.md` -- Both sources give a fixed 60-second window. |
| 7 | The gateway does not disclose the start of the 60-second counting window. | supported | `source_b.md` | 'whose start the gateway doesn’t disclose' in `source_b.md` -- Source B says the gateway doesn't disclose the window start. |
| 8 | Requests are never counted against a connection. | supported | `source_a.md` | 'and never against a connection' in `source_a.md` -- Source A states requests are never counted against a connection. |
| 9 | The request count follows the credential across hosts. | supported | `source_b.md` | 'The count follows the credential wherever the caller happens to put it, including across hosts.' in `source_b.md` -- Source B states the count follows the credential across hosts. |
| 10 | Opening a second socket gives a caller no additional request allowance. | supported | `source_a.md` | 'Opening a second socket therefore buys a caller nothing.' in `source_a.md` -- Source A says a second socket buys the caller nothing. |
| 11 | A client spread across eight worker processes is throttled at exactly the point one process would have been. | supported | `source_a.md` | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `source_a.md` -- Source A states this directly. |
| 12 | The default allowance is 100 requests in a window. | supported | `source_a.md` | 'The default allowance is 100 requests in a window' in `source_a.md` -- Both sources state a default of 100 requests per window. |
| 13 | The default allowance of 100 requests is enough for every interactive use of the API the platform team has seen. | supported | `source_b.md` | 'which is enough for every interactive use of this API the platform team has seen' in `source_b.md` -- Source B states the default suffices for all interactive uses seen. |
| 14 | A caller that needs more than 100 requests in a window is almost always doing batch work under an interactive credential. | supported | `source_b.md` | 'a caller that needs more than that is almost always doing batch work under an interactive credential' in `source_b.md` -- Source B states this directly. |
| 15 | A credential marked for batch work is allowed 1000 requests in the same window. | supported | `source_a.md` | 'a credential marked for batch work is allowed 1000 in the same window' in `source_a.md` -- Source A states batch credentials get 1000 in the same window. |
| 16 | A 429 refusal is not an outage. | supported | `source_a.md` | 'A refusal is not an outage' in `source_a.md` -- Source A states a refusal is not an outage. |
| 17 | A 429 refusal is not a bug in the gateway. | supported | `source_b.md` | 'The refusal isn’t an outage and it isn’t a bug in the gateway' in `source_b.md` -- Source B states the refusal isn't a gateway bug. |
| 18 | A 429 refusal is the platform declining to spend capacity that has already been promised to somebody else. | supported | `source_a.md` | 'It is the platform declining to spend capacity that has already been promised to somebody else' in `source_a.md` -- Source A states this directly. |
| 19 | Callers that retry at once are most of the reason the cap exists. | supported | `source_b.md` | 'Callers that retry immediately are most of the reason the cap is there.' in `source_b.md` -- Source B says immediate retriers are most of the reason for the cap. |
| 20 | Every refusal carries a Retry-After header. | supported | `source_b.md` | 'it is present on every refusal the gateway sends' in `source_b.md` -- Source B says the Retry-After header is present on every refusal. |
| 21 | The Retry-After header value is a whole number of seconds to wait. | supported | `source_a.md` | 'Its value is a whole number of seconds to wait.' in `source_a.md` -- Source A states the header value is whole seconds to wait. |
| 22 | The gateway keeps no memory of which callers backed off politely. | supported | `source_a.md` | 'The gateway keeps no memory of who backed off politely' in `source_a.md` -- Source A states this directly. |
| 23 | Waiting longer than the Retry-After header asks earns a caller no credit. | supported | `source_a.md` | 'so waiting longer than the header asks earns a caller no credit at all' in `source_a.md` -- Source A states waiting longer earns no credit. |
| 24 | The body of a refusal is JSON. | supported | `source_a.md` | 'The body of the refusal is JSON' in `source_a.md` -- Source A states the refusal body is JSON. |
| 25 | The refusal body repeats the cap, the tier and the window as plain fields. | supported | `source_b.md` | 'it repeats the cap, the window and the tier as plain fields' in `source_b.md` -- Source B states the body repeats cap, window and tier as plain fields. |
| 26 | The refusal body is there so a human reading a log afterwards can see why the request was refused. | supported | `source_a.md` | 'The body is there so that a human reading a log afterwards can see why the request was refused' in `source_a.md` -- Source A states this purpose of the refusal body directly. |
| 27 | Nothing in the refusal body is meant for the retry loop. | supported | `source_a.md` | 'nothing in it is meant for the retry loop' in `source_a.md` -- Source A states that nothing in the body is meant for the retry loop. |
| 28 | The gateway computes the wait with information the caller does not have. | supported | `source_a.md` | 'The gateway has already done that arithmetic, with information the caller does not have' in `source_a.md` -- Source A states the gateway computes the wait with information the caller lacks. |
| 29 | The rule to honour the header also holds on the 503 path. | supported | `source_b.md` | 'On the 503 path the same rule holds' in `source_b.md` -- Source B states the honour-the-header rule holds on the 503 path. |
| 30 | The cause of a 503 refusal is different from the cause of a 429 refusal. | supported | `source_b.md` | 'even though the cause of the refusal is an entirely different one' in `source_b.md` -- Source B says the cause of the 503 refusal is entirely different. |
| 31 | A 200 response requires no retry action. | supported | `source_a.md` | 'A 200 wants nothing' in `source_a.md` -- Source A states a 200 needs no action. |
| 32 | A 429 response requires waiting the stated time. | supported | `source_a.md` | 'a 429 wants the stated wait' in `source_a.md` -- Source A states a 429 requires the stated wait. |
| 33 | A 500 response may be retried once the stated wait has passed. | supported | `source_a.md` | 'a 500 may be retried once that wait has passed' in `source_a.md` -- Source A states a 500 may be retried after the wait. |
| 34 | A 503 response is the overload path, meaning the platform itself is overloaded. | supported | `source_b.md` | 'a 503 means the platform itself is overloaded' in `source_b.md` -- Source B says a 503 means the platform is overloaded, and Source A calls it the overload path. |
| 35 | A client that folds every non-success response into one branch will retry hardest during the incident the cap was installed to survive. | supported | `source_a.md` | 'A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive.' in `source_a.md` -- Source A states this directly. |
| 36 | A batch credential is allowed fifty times the default allowance. | supported | `source_a.md` | 'A batch credential is allowed fifty times the default allowance' in `source_a.md` -- Source A states the batch allowance is fifty times the default. |
| 37 | A batch credential is measured over exactly the same window as the default, not by a separate counting scheme. | supported | `source_b.md` | 'which is 50 times the default and not a separate counting scheme' in `source_b.md` -- Source B says batch is not a separate counting scheme, and Source A says it uses exactly the same window. |
| 38 | The tier is set on the credential when it is issued. | supported | `source_a.md` | 'The tier is set on the credential when it is issued' in `source_a.md` -- Source A states the tier is set when the credential is issued. |
| 39 | The tier cannot be requested per call. | supported | `source_a.md` | 'cannot be asked for per call' in `source_a.md` -- Source A states the tier cannot be requested per call. |
| 40 | The header and the body of a refusal are identical for the batch and interactive tiers. | supported | `source_b.md` | 'The window, the header and the body are identical to the interactive case' in `source_b.md` -- Source B states the header and body are identical across tiers. |
| 41 | A client written for one tier needs no change to run against the other tier. | supported | `source_b.md` | 'so a client written for one tier needs no change at all to run against the other' in `source_b.md` -- Source B states this directly. |
| 42 | Nothing else about the batch and interactive tiers differs. | supported | `source_a.md` | 'Nothing else about the two tiers differs in any way.' in `source_a.md` -- Source A states nothing else differs between the tiers. |
| 43 | Callers should keep the log of refusals for at least a week. | supported | `source_b.md` | 'keep the log for at least a week' in `source_b.md` -- Source B states the log should be kept at least a week. |
| 44 | The refusal log line should carry the credential, the window and the wait. | supported | `source_a.md` | 'The log line should carry the credential, the window and the wait.' in `source_a.md` -- Source A states this directly. |
| 45 | The gateway refuses a request for three separate reasons. | supported | `source_b.md` | 'The gateway refuses a request for three separate reasons' in `source_b.md` -- Source B states three separate refusal reasons. |
| 46 | Only one of the gateway's refusal reasons is the cap. | supported | `source_b.md` | 'only one of them is a cap' in `source_b.md` -- Source B states only one reason is a cap. |
| 47 | A credential may be suspended. | supported | `source_a.md` | 'A credential may be suspended' in `source_a.md` -- Source A states a credential may be suspended. |
| 48 | A route may be closed for maintenance while it is repaired. | supported | `source_b.md` | 'a route can be closed while it is being repaired' in `source_b.md` -- Source B says a route can be closed while being repaired, and Source A says it can be closed for maintenance. |
| 49 | The request body limit is 5 megabyte. | supported | `source_a.md` | 'a body may exceed the 5 megabyte limit' in `source_a.md` -- Source A gives the 5 megabyte body limit. |
| 50 | A body exceeding the 5 megabyte limit is refused before it has been read. | supported | `source_b.md` | 'a request body over the 5 megabyte limit is refused before it has been read at all' in `source_b.md` -- Source B states oversized bodies are refused before being read. |
| 51 | None of the three non-cap refusals clears by waiting for a stated number of seconds. | supported | `source_a.md` | 'None of those three clears itself by waiting for a stated number of seconds.' in `source_a.md` -- Source A states that none of the three other refusals clears itself by waiting for a stated number of seconds. |
| 52 | A loop that waits and retries against a suspended credential never reaches the service. | supported | `source_a.md` | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `source_a.md` -- Source A states the loop never reaches the service. |
| 53 | Reading the status code rather than its class distinguishes a suspended credential from a cap refusal. | supported | `source_a.md` | 'Reading the status code rather than the class it belongs to is what separates the two cases' in `source_a.md` -- Source A says reading the status code rather than its class separates the suspended-credential case from the cap case. |
| 54 | Reading the status code costs one comparison. | supported | `source_a.md` | 'and it costs one comparison' in `source_a.md` -- Source A states that reading the status code costs one comparison. |
| 55 | A cap can be raised. | supported | `source_a.md` | 'A cap can be raised' in `source_a.md` -- Both sources state that a cap can be raised; Source A is quoted. |
| 56 | The number of caps raised without a measurement behind them is 0. | supported | `source_a.md` | 'the number of caps raised without a measurement behind them is 0' in `source_a.md` -- Source A states this figure directly. |
| 57 | A request for a cap increase should include a full week of refusal counts, the shape of traffic across the day, and the deadline that traffic is serving. | supported | `source_a.md` | 'Bring a week of refusal counts, the shape of the traffic across the day, and the deadline that traffic is serving.' in `source_a.md` -- Source A lists the same three items, and Source B specifies that the refusal counts should cover a full week. |
| 58 | Before looking at the number, the platform team looks at whether the load is smooth or bursty. | supported | `source_b.md` | 'The team wants to know whether the load is smooth or bursty before it looks at the number at all.' in `source_b.md` -- Source B states that the team checks whether load is smooth or bursty before looking at the number. |
| 59 | A burst is cheaper to smooth than to serve at its peak. | supported | `source_a.md` | 'a burst is cheaper to smooth than it is to serve at its peak' in `source_a.md` -- Source A states this directly. |
| 60 | A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap. | supported | `source_a.md` | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `source_a.md` -- Source A states this directly. |
| 61 | Requests for a cap increase reach the platform team through the usual channel. | supported | `source_a.md` | 'Requests reach the platform team through the usual channel' in `source_a.md` -- Source A states that requests reach the platform team through the usual channel. |
| 62 | Requests for a cap increase are answered within two working days. | supported | `source_a.md` | 'they are answered within two working days' in `source_a.md` -- Source A states that requests are answered within two working days. |
| 63 | There is no expedited path for cap increase requests. | supported | `source_a.md` | 'There is no expedited path and no exception list.' in `source_a.md` -- Source A states that there is no expedited path. |
| 64 | There is no exception list for cap increase requests. | supported | `source_a.md` | 'There is no expedited path and no exception list.' in `source_a.md` -- Source A states that there is no exception list. |

## Structure

**9** mechanical check(s) over **104** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **64** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **112**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 25 run(s) over 48 attributed segment(s) — sources interleaved. 6 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

`[-...-]` is what the source said and `{+...+}` is what the merge says.

### Declared gone, still here — a record says the content departed and the merge carries the segment unchanged

- `b36` (`source_b.md`) — 'The counts are the whole of the argument, and without them a request is only a preference.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: The counts are the whole of the argument, and without them a request is only a preference.
  In the merge:  the counts are the whole of the argument, and without them a request is only a preference.
  What changed:  [-T-]{+t+}he counts are the whole of the argument, and without them a request is only a preference.
  ```

### Verbatim violation — an invariant-core token did not survive unchanged

- `b31` (`source_b.md`) — numeric '50' (times) does not survive into the merge unchanged

### Over budget — declared loss past the ceiling

- 4 absent segments are declared replaced by the same replacement (a12, a13, b13, b14), over the ceiling of 3. One replacement standing in for that many segments has not replaced them, it has dropped them: the detail it names is gone from the document

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **81** departure(s) from its sources. Checking them confirms 63, rejects 3, and leaves 15 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 104 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a2` | reworded | Intro opening merged with b2's wording. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-001`) |
| `b2` | duplicate | Same opening fact as a2. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-001`) |
| `b3` | duplicate | a3 carries the same fact. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-002`, `B-003`) |
| `a4` | reconciled | Counting rule combined with undisclosed window start. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-004`, `A-005`, `A-006`) |
| `b5` | reconciled | Counting rule combined with undisclosed window start. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-004`, `B-005`, `B-006`) |
| `a5` | subsumed | Socket point folded into the cross-host sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-007`) |
| `b6` | duplicate | Same point as a5. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-007`) |
| `b7` | subsumed | Cross-host counting carried in combined sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-008`) |
| `b8` | superseded | a6 states the same with more detail. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-009`) |
| `a7` | subsumed | Allowances split around b9's interactive context. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-009`, `A-010`) |
| `a8` | reworded | Added b10's not-a-bug point. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b10` | subsumed | Carried by a8 and a9 wording. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-013`, `B-014`, `B-015`) |
| `a10` | superseded | b11's 'most of the reason' kept; it implies largest single. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`A-011`) |
| `b11` | reworded | Fitted to base phrasing. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-016`) |
| `b12` | duplicate | Identical heading stated once. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `a12` | reconciled | Header combined with b14's every-refusal fact. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-012`) |
| `b14` | reconciled | Header combined with b14's every-refusal fact. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-018`, `B-019`) |
| `a13` | subsumed | Value unit folded into header sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-013`) |
| `b13` | duplicate | Header name already carried. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-017`) |
| `a14` | reworded | Extended with b15's purpose clause. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b15` | subsumed | Contract and purpose clause carried. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-020`) |
| `b16` | duplicate | a15 states the same. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-021`) |
| `a16` | subsumed | Body fields combined into one sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-016`, `A-017`) |
| `a17` | subsumed | Body fields combined into one sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-018`, `A-019`) |
| `b17` | subsumed | Body fields combined into one sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-022`, `B-023`) |
| `a18` | reworded | Merged with b18's consequence. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b18` | subsumed | Carried in merged sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-024`) |
| `b19` | duplicate | a19 states the same. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-025`) |
| `b20` | superseded | Base heading kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b21` | duplicate | a21 states the same. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-026`, `B-027`) |
| `a22` | reworded | Rule 1 heading merged with b22. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b22` | subsumed | Rule 1 heading merged with a22. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-028`) |
| `a23` | reworded | Added b24's different-cause detail. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-020`) |
| `b23` | duplicate | Same as a23. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-029`) |
| `b24` | subsumed | 503 rule carried in merged sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-030`, `B-031`) |
| `b25` | duplicate | a24 states the same. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b26` | duplicate | a25 states the same. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `a26` | reworded | Extended with b27's clause. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b27` | subsumed | Carried in rule 2 opening. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-032`, `B-033`) |
| `a27` | reworded | Added b28's 503 meaning. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-021`, `A-022`) |
| `b28` | subsumed | Status cases carried in merged sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-034`, `B-035`, `B-036`, `B-037`) |
| `b29` | duplicate | a29 states the same. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-038`) |
| `b30` | duplicate | a30 makes the same point. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `a32` | reworded | Added b31's no-separate-scheme point. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-023`, `A-024`) |
| `b31` | subsumed | Multiplier here; 1000 already in the intro allowance sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-039`, `B-040`, `B-041`) |
| `b32` | subsumed | Identical tiers point carried. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-042`, `B-043`) |
| `a34` | reworded | Joined with b32's detail. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-027`) |
| `b33` | duplicate | Same as a34. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-044`) |
| `a35` | reworded | Added b34's retention rule. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b34` | subsumed | Retention carried in rule 4 opening. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-045`, `B-046`) |
| `a36` | reworded | Joined with b36. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b35` | duplicate | Same as a36. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-047`, `B-048`) |
| `b36` | subsumed | Carried in merged rule 4 sentence. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b37` | superseded | Base heading kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a39` | reworded | Subject made explicit. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a40` | reworded | Merged with b38 and b39. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-028`) |
| `b38` | subsumed | Carried in merged sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-049`, `B-050`) |
| `b39` | subsumed | Carried in merged sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-051`) |
| `a41` | reworded | Added b40's details. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-029`, `A-030`, `A-031`) |
| `b40` | subsumed | Carried in merged sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-052`, `B-053`, `B-054`, `B-055`) |
| `a43` | reworded | Took b41's comparison. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b41` | subsumed | Carried in merged sentence. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a44` | reworded | Merged with b42 and b43. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-033`) |
| `b42` | subsumed | Carried in merged sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-056`) |
| `b43` | subsumed | Carried in merged sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-057`, `B-058`) |
| `a47` | reworded | Merged with b46. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-034`, `A-035`) |
| `b46` | subsumed | Carried in merged sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-060`, `B-061`) |
| `a48` | reworded | Added b47's 'full'. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b47` | duplicate | Same as a48. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-062`, `B-063`, `B-064`) |
| `a49` | reworded | Added b48's ordering. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-036`, `A-037`) |
| `b48` | subsumed | Carried in merged sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-065`) |
| `b49` | duplicate | Same as a49. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-066`) |
| `a50` | reworded | Joined with b45. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-038`) |
| `b44` | duplicate | Same as a50. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-059`) |
| `b45` | subsumed | Carried in merged sentence. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a51` | reworded | Added b52's chasing point. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-039`, `A-040`) |
| `b50` | duplicate | Same as a51. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-067`) |
| `b52` | subsumed | Carried in merged sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-069`, `B-070`) |
| `b51` | duplicate | a52 states the same. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-068`) |
| `b1` | superseded | Base title kept. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Rate limiting and the 429 contract for gateway clients' and says so (no claim traced to it) |
| `b9` | reworded | Placed in base intro slot. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-010`, `B-011`, `B-012`) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | ec0c9ecb43e3 (hosted) |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | claude-opus-5-5 |
| Model (decompose) | claude-opus-5-5 |
| Model (verify) | claude-opus-5-5 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile anthropic |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 12 live, 0 cached, 0 replayed |
| Tokens | 61,279 in, 46,914 out |
| Cost | ~$1.18 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 349.3s |
| Generated | 2026-09-27T17:01:25+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
