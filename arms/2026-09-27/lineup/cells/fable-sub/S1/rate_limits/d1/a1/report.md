## Verdict

**No extracted claim was dropped, contradicted, invented, or carried only in part.** 109 source claim(s) checked against the merge, 71 merge claim(s) checked against the sources. The 9 mechanical checks under Structure below cover what the claims do not: titles, invariant-core tokens, and all 104 source segment(s) — including the ones no claim was drawn from.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 71 |
| Claims extracted from `source_a.md` | 45 |
| Claims extracted from `source_b.md` | 64 |
| Forward — source claims accounted for in the merge | **109/109** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **45/45** |
| Forward — `source_b.md` claims accounted for | **64/64** |
| Reverse — merge claims found in a source | **71/71** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **180/180** |
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

### `source_a.md` -- 45 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 45 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Every credential has a cap. | 3 | carried | 'Every credential has a cap' in `merged.md` -- The reference text states this directly. |
| 2 | When a credential's cap is spent the gateway answers 429 at the edge. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge' in `merged.md` -- The reference text states the 429 is answered at the edge when the cap is spent. |
| 3 | The gateway answers 429 without waking the service behind it. | 3 | carried | 'the gateway answers 429 at the edge — without waking the service behind it' in `merged.md` -- The reference text states the service behind the gateway is not woken. |
| 4 | Requests are counted against the credential that presented them. | 5 | carried | 'Requests are counted against the credential that presented them' in `merged.md` -- The reference text states this directly. |
| 5 | Requests are counted over a fixed window of 60 seconds. | 5 | carried | 'over a fixed window of 60 seconds' in `merged.md` -- The reference text states the fixed 60 second window. |
| 6 | Requests are never counted against a connection. | 5 | carried | 'and never against a connection' in `merged.md` -- The reference text states requests are never counted against a connection. |
| 7 | A client spread across eight worker processes is throttled at exactly the point one process would have been. | 5 | carried | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `merged.md` -- The reference text states this directly. |
| 8 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- The reference text states this directly. |
| 9 | A credential marked for batch work is allowed 1000 requests in the same window as the default allowance. | 7 | carried | 'a credential marked for batch work is allowed 1000 in the same window' in `merged.md` -- The reference text states the batch allowance of 1000 in the same window. |
| 10 | Callers that retry at once are the largest single reason the cap is there at all. | 7 | carried | 'Callers that retry at once are the largest single reason the cap is there at all' in `merged.md` -- The reference text states this directly. |
| 11 | The 429 refusal carries a Retry-After header. | 11 | carried | 'The refusal carries a Retry-After header' in `merged.md` -- The reference text states the refusal carries the header. |
| 12 | The Retry-After header's value is a whole number of seconds to wait. | 11 | carried | 'Its value is a whole number of seconds to wait' in `merged.md` -- The reference text states this directly. |
| 13 | The gateway keeps no memory of who backed off politely. | 11 | carried | 'The gateway keeps no memory of who backed off politely' in `merged.md` -- The reference text states this directly. |
| 14 | The body of the refusal is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- The reference text states this directly. |
| 15 | The body of the refusal names the window the gateway counted in. | 13 | carried | 'it names what the gateway calls the “window” it counted in' in `merged.md` -- The reference text states the body names the window. |
| 16 | The body of the refusal names the cap and the tier. | 13 | carried | 'It names the cap and the tier as well' in `merged.md` -- The reference text states the body names the cap and tier. |
| 17 | There are four rules for retrying, given in the order they should be applied. | 17 | carried | 'Four rules, given in the order they should be applied' in `merged.md` -- The reference text states four rules in order of application. |
| 18 | The gateway computes the wait on the 503 path as well as on the 429 path. | 19 | carried | 'The gateway has already done that arithmetic, with information the caller does not have, and it does the same on the 503 path' in `merged.md` -- The reference text states the gateway does the same arithmetic on the 503 path. |
| 19 | A 200 wants nothing. | 21 | carried | 'A 200 needs nothing' in `merged.md` -- Same meaning in different wording. |
| 20 | A 429 wants the stated wait. | 21 | carried | 'a 429 needs the stated wait' in `merged.md` -- Same meaning in different wording. |
| 21 | A 500 may be retried once the stated wait has passed. | 21 | carried | 'a 500 can be retried once that wait has passed' in `merged.md` -- The reference text states a 500 can be retried after the wait. |
| 22 | A 503 is the overload path. | 21 | carried | 'a 503 means the platform itself is overloaded' in `merged.md` -- The reference text identifies 503 as the overload case. |
| 23 | A batch credential is allowed fifty times the default allowance. | 23 | carried | 'which is 50 times the default' in `merged.md` -- The reference text states the batch allowance is 50 times the default. |
| 24 | A batch credential is measured over exactly the same window as the default tier. | 23 | carried | 'it is measured over exactly the same window' in `merged.md` -- The reference text states this directly. |
| 25 | The tier is set on the credential when it is issued. | 23 | carried | 'The tier is set on the credential when it is issued' in `merged.md` -- The reference text states this directly. |
| 26 | The tier cannot be asked for per call. | 23 | carried | 'cannot be asked for per call' in `merged.md` -- The reference text states the tier cannot be asked for per call. |
| 27 | Nothing about the two tiers differs other than the allowance. | 23 | carried | 'Nothing else about the two tiers differs in any way' in `merged.md` -- The reference text states nothing else differs between the tiers beyond the allowance. |
| 28 | The log line for a refusal should carry the credential, the window and the wait. | 25 | carried | 'The log line should carry the credential, the window and the wait' in `merged.md` -- The reference text states this directly. |
| 29 | The gateway refuses a request for three reasons, only one of which is the cap. | 29 | carried | 'The gateway refuses a request for three reasons and only one of them is the one above' in `merged.md` -- The reference text states three reasons with only one being the cap described above. |
| 30 | A credential may be suspended. | 29 | carried | 'A credential may be suspended' in `merged.md` -- The reference text states this directly. |
| 31 | A route may be closed for maintenance. | 29 | carried | 'a route may be closed for maintenance' in `merged.md` -- The reference text states this directly. |
| 32 | A request body may exceed the 5 megabyte limit. | 29 | carried | 'a body may exceed the 5 megabyte limit' in `merged.md` -- The reference text states this directly. |
| 33 | None of a suspended credential, a route closed for maintenance, or a body exceeding the 5 megabyte limit clears itself by waiting for a stated number of seconds. | 29 | carried | 'None of those three clears itself by waiting for a stated number of seconds' in `merged.md` -- The reference text states none of the three listed cases clears by waiting. |
| 34 | A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `merged.md` -- The reference text states this directly. |
| 35 | Reading the status code rather than the class it belongs to costs one comparison. | 31 | carried | 'Reading the status code rather than the class it belongs to is what separates the two cases, and it costs one comparison' in `merged.md` -- The reference text states reading the status code costs one comparison. |
| 36 | A cap can be raised. | 35 | carried | 'A cap can be raised' in `merged.md` -- The reference text states this directly. |
| 37 | The number of caps raised without a measurement behind them is 0. | 35 | carried | 'the number of caps raised without a measurement behind them is 0' in `merged.md` -- The reference text states this directly. |
| 38 | A request for a cap increase should bring a week of refusal counts, the shape of the traffic across the day, and the deadline that traffic is serving. | 35 | carried | 'Bring a week of refusal counts, the shape of the traffic across the day, and the deadline that traffic is serving' in `merged.md` -- The reference text lists the same three items to bring. |
| 39 | The platform team looks at whether the load is smooth or bursty. | 35 | carried | 'The platform team looks at whether the load is smooth or bursty' in `merged.md` -- The reference text states this directly. |
| 40 | A burst is cheaper to smooth than it is to serve at its peak. | 35 | carried | 'a burst is cheaper to smooth than it is to serve at its peak' in `merged.md` -- The reference text states this directly. |
| 41 | A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap. | 35 | carried | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `merged.md` -- The reference text states this directly. |
| 42 | Requests for a cap increase reach the platform team through the usual channel. | 37 | carried | 'Requests reach the platform team through the usual channel' in `merged.md` -- The reference text states this in the section on asking for an increase. |
| 43 | Requests for a cap increase are answered within two working days. | 37 | carried | 'they are answered within two working days' in `merged.md` -- The reference text states the two working day answer time. |
| 44 | There is no expedited path for cap increase requests. | 37 | carried | 'There is no expedited path and no exception list' in `merged.md` -- The reference text states there is no expedited path. |
| 45 | There is no exception list for cap increase requests. | 37 | carried | 'There is no expedited path and no exception list' in `merged.md` -- The reference text states there is no exception list. |

### `source_b.md` -- 64 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 64 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Every credential has a cap of its own. | 3 | carried | 'Every credential has a cap' in `merged.md` -- Every credential having a cap carries the same meaning as each having a cap of its own. |
| 2 | When the cap is spent the gateway answers 429 at the edge. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge' in `merged.md` -- The reference text states this directly. |
| 3 | When the cap is spent the gateway answers 429 without troubling the service behind the gateway. | 3 | carried | 'the gateway answers 429 at the edge — without waking the service behind it' in `merged.md` -- Not waking the service is the same as not troubling it. |
| 4 | An earlier draft of the note argued for a client-side token bucket that mirrored the gateway's own counters. | 3 | carried | 'An earlier draft of this note argued for a client-side token bucket that mirrored the gateway’s own counters' in `merged.md` -- The reference text states this directly. |
| 5 | Requests are counted against the credential rather than the connection. | 5 | carried | 'Requests are counted against the credential that presented them, over a fixed window of 60 seconds whose start the gateway doesn’t disclose, and never against a connection' in `merged.md` -- The reference text states counting is by credential and never by connection. |
| 6 | Requests are counted over a fixed window of 60 seconds. | 5 | carried | 'over a fixed window of 60 seconds' in `merged.md` -- The reference text states the fixed 60 second window. |
| 7 | The gateway doesn't disclose the start of the 60 second window. | 5 | carried | 'whose start the gateway doesn’t disclose' in `merged.md` -- The reference text states the window start is not disclosed. |
| 8 | There is nothing to be gained by opening more sockets to the gateway. | 5 | carried | 'Opening a second socket therefore buys a caller nothing' in `merged.md` -- The reference text states extra sockets buy the caller nothing. |
| 9 | The request count follows the credential wherever the caller puts it, including across hosts. | 5 | carried | 'The count follows the credential wherever the caller happens to put it, including across hosts' in `merged.md` -- The reference text states this directly. |
| 10 | A caller spread over many worker processes is throttled at the same point a single process would have been. | 5 | carried | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `merged.md` -- The reference text states the same point with eight worker processes as the instance of many. |
| 11 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- The reference text states this directly. |
| 12 | The default allowance of 100 requests in a window is enough for every interactive use of the API the platform team has seen. | 7 | carried | 'The default is enough for every interactive use of this API the platform team has seen' in `merged.md` -- The reference text states the default suffices for every interactive use seen. |
| 13 | A caller that needs more than the default allowance is almost always doing batch work under an interactive credential. | 7 | carried | 'a caller that needs more than that is almost always doing batch work under an interactive credential' in `merged.md` -- The reference text states this directly. |
| 14 | A 429 refusal is capacity being held for a request somebody else has already been promised. | 7 | carried | 'It is the platform declining to spend capacity that has already been promised to somebody else' in `merged.md` -- The reference text describes the refusal as protecting capacity already promised to somebody else. |
| 15 | Callers that retry immediately are most of the reason the cap is there. | 7 | carried | 'Callers that retry at once are the largest single reason the cap is there at all' in `merged.md` -- Retrying at once being the largest single reason for the cap conveys the same meaning in different words. |
| 16 | The header is called Retry-After. | 11 | carried | 'The refusal carries a Retry-After header' in `merged.md` -- The reference text names the header Retry-After. |
| 17 | The value of the Retry-After header is a whole number of seconds. | 11 | carried | 'Its value is a whole number of seconds to wait' in `merged.md` -- The reference text states this directly. |
| 18 | The Retry-After header is present on every refusal the gateway sends. | 11 | carried | 'it is present on every refusal the gateway sends' in `merged.md` -- The reference text states the header is on every refusal. |
| 19 | Waiting as long as the Retry-After header states and then continuing is the entire contract. | 11 | carried | 'Waiting that long and then continuing is the whole of the contract' in `merged.md` -- The reference text states waiting and continuing is the whole contract. |
| 20 | Waiting longer than the Retry-After header asks earns nothing. | 11 | carried | 'waiting longer than the header asks earns a caller no credit at all' in `merged.md` -- The reference text states waiting longer earns no credit. |
| 21 | The response body of a refusal is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- The reference text states this directly. |
| 22 | The response body of a refusal repeats the cap, the window and the tier as plain fields. | 13 | carried | 'it names what the gateway calls the “window” it counted in. It names the cap and the tier as well, all as plain fields' in `merged.md` -- The reference text states the body names the window, cap and tier as plain fields. |
| 23 | There are four rules for what the client does. | 17 | carried | 'Four rules, given in the order they should be applied' in `merged.md` -- The reference text gives four rules for how the client retries. |
| 24 | The order the client rules are given in is the order to apply them. | 17 | carried | 'Four rules, given in the order they should be applied' in `merged.md` -- The reference text states the rules are given in the order of application. |
| 25 | The first rule is to honour the Retry-After header and not compute a client-side wait. | 19 | carried | 'Honour the header, every time. The gateway has already done that arithmetic, with information the caller does not have, and it does the same on the 503 path, even though the cause of the refusal there is an entirely different one. A wait derived on the client side is a guess about a counter it cannot see' in `merged.md` -- Rule one is to honour the header, and a client-derived wait is dismissed as a guess. |
| 26 | The gateway computes the wait with information the caller cannot see. | 19 | carried | 'The gateway has already done that arithmetic, with information the caller does not have' in `merged.md` -- The reference text states the gateway computes with information the caller lacks. |
| 27 | On the 503 path the rule to honour the header holds. | 19 | carried | 'it does the same on the 503 path' in `merged.md` -- Under the honour-the-header rule the text states the gateway does the same on the 503 path, so the rule holds there. |
| 28 | The cause of a 503 refusal is different from the cause of a 429 refusal. | 19 | carried | 'even though the cause of the refusal there is an entirely different one' in `merged.md` -- The reference text states the cause on the 503 path is entirely different. |
| 29 | The set of responses that are safe to retry is smaller than the set of responses that aren't a success. | 21 | carried | 'Retry only what is safe to retry, which is a smaller set than the set of responses that aren’t a success' in `merged.md` -- The reference text states this directly. |
| 30 | A 200 response needs nothing. | 21 | carried | 'A 200 needs nothing' in `merged.md` -- The reference text states this directly. |
| 31 | A 429 response needs the stated wait. | 21 | carried | 'a 429 needs the stated wait' in `merged.md` -- The reference text states this directly. |
| 32 | A 500 response can be retried once the stated wait has passed. | 21 | carried | 'a 500 can be retried once that wait has passed' in `merged.md` -- The reference text states this directly. |
| 33 | A 503 response means the platform itself is overloaded. | 21 | carried | 'a 503 means the platform itself is overloaded' in `merged.md` -- The reference text states this directly. |
| 34 | A caller that folds the 200, 429, 500 and 503 responses into one branch will retry hardest during the incident the cap was installed to survive. | 21 | carried | 'The four cases are not interchangeable. A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive' in `merged.md` -- The text says the four cases are not interchangeable and that folding them into one branch retries hardest during the incident. |
| 35 | A batch credential is allowed 1000 requests in a window. | 23 | carried | 'A batch credential is allowed 1000 requests in a window' in `merged.md` -- The reference text states this directly. |
| 36 | The batch allowance of 1000 requests in a window is 50 times the default. | 23 | carried | 'A batch credential is allowed 1000 requests in a window, which is 50 times the default' in `merged.md` -- The reference text states the batch allowance is 50 times the default. |
| 37 | The batch allowance is not a separate counting scheme. | 23 | carried | 'not a separate counting scheme' in `merged.md` -- The reference text states the batch allowance is not a separate counting scheme. |
| 38 | The window, the header and the body for the batch tier are identical to the interactive case. | 23 | carried | 'The window, the header and the body are identical to the interactive case' in `merged.md` -- The reference text states this under the batch rule. |
| 39 | A client written for one tier needs no change to run against the other tier. | 23 | carried | 'a client written for one tier needs no change at all to run against the other' in `merged.md` -- The reference text states this directly. |
| 40 | Nothing about the batch tier other than the allowance differs from the default. | 23 | carried | 'Nothing else about the two tiers differs in any way' in `merged.md` -- The reference text states nothing else differs between the tiers beyond the allowance. |
| 41 | The fourth rule is to log every refusal seen. | 25 | carried | 'Log every refusal seen, and keep the log for at least a week' in `merged.md` -- The fourth numbered rule is to log every refusal seen. |
| 42 | The refusal log should be kept for at least a week. | 25 | carried | 'keep the log for at least a week' in `merged.md` -- The reference text states the log retention of at least a week. |
| 43 | The platform team won't assemble the case for a larger cap on a caller's behalf. | 25 | carried | 'nobody at the far end will assemble that argument on its behalf' in `merged.md` -- The reference text states nobody at the far end will assemble the argument for the caller. |
| 44 | The gateway refuses a request for three separate reasons. | 29 | carried | 'The gateway refuses a request for three reasons' in `merged.md` -- The reference text states three reasons for refusal. |
| 45 | Only one of the gateway's reasons for refusing a request is a cap. | 29 | carried | 'The gateway refuses a request for three reasons and only one of them is the one above' in `merged.md` -- The reference text states only one of the three reasons is the cap described above. |
| 46 | Two of the three reasons for refusal have nothing to do with how much traffic a caller has sent in the current window. | 29 | carried | 'Two of the three have nothing to do with how much traffic a caller has sent in the window it is currently in' in `merged.md` -- The reference text states this directly. |
| 47 | A credential can be suspended. | 29 | carried | 'A credential may be suspended' in `merged.md` -- The reference text states this directly. |
| 48 | A route can be closed while it is being repaired. | 29 | carried | 'a route may be closed for maintenance' in `merged.md` -- Closed for maintenance carries the same meaning as closed while being repaired. |
| 49 | The request body limit is 5 megabyte. | 29 | carried | 'a body may exceed the 5 megabyte limit' in `merged.md` -- The reference text states the 5 megabyte body limit. |
| 50 | A request body over the 5 megabyte limit is refused before it has been read. | 29 | carried | 'a body may exceed the 5 megabyte limit, in which case it is refused before it has been read at all' in `merged.md` -- The reference text states an oversized body is refused before being read. |
| 51 | A loop retrying against a suspended credential burns its whole budget and reaches nothing. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `merged.md` -- The reference text states the loop spends its whole budget and never reaches the service. |
| 52 | The log after a loop retries against a suspended credential shows a long run of refusals and no successes. | 31 | carried | 'the log afterwards shows nothing at all except a long run of refusals' in `merged.md` -- A log showing nothing except refusals entails a long run of refusals and no successes. |
| 53 | A caller that can move half its work to a quieter hour usually finds it doesn't need a larger cap. | 33 | carried | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `merged.md` -- Getting what it needs without a cap change means the caller does not need a larger cap. |
| 54 | A cap can be raised. | 33 | carried | 'A cap can be raised' in `merged.md` -- The reference text states this directly. |
| 55 | A cap is not raised on the strength of an assertion that the current cap is too small. | 33 | carried | 'An assertion that the current cap is too small is not enough' in `merged.md` -- The reference text states an assertion alone is not enough to raise a cap. |
| 56 | A request for a larger cap should bring the refusal counts for a full week. | 33 | carried | 'Bring a week of refusal counts' in `merged.md` -- The text tells a requester to bring a week of refusal counts. |
| 57 | A request for a larger cap should bring the shape of the traffic across the day. | 33 | carried | 'the shape of the traffic across the day' in `merged.md` -- The text lists the shape of the traffic across the day among the things to bring. |
| 58 | A request for a larger cap should bring the deadline the traffic exists to meet. | 33 | carried | 'the deadline that traffic is serving' in `merged.md` -- The text lists the deadline the traffic is serving, which is the same meaning as the deadline it exists to meet. |
| 59 | The platform team wants to know whether the load is smooth or bursty before it looks at the number. | 35 | carried | 'The platform team looks at whether the load is smooth or bursty before it looks at the number at all' in `merged.md` -- The text states the platform team considers smooth versus bursty load before the number. |
| 60 | A burst is cheaper to smooth out than it is to serve at its peak. | 35 | carried | 'a burst is cheaper to smooth than it is to serve at its peak' in `merged.md` -- The text states this directly. |
| 61 | Requests for a larger cap go to the platform team through the usual channel. | 35 | carried | 'Requests reach the platform team through the usual channel' in `merged.md` -- The text, in the section on asking for an increase, says requests reach the platform team through the usual channel. |
| 62 | There is no expedited path for requests to raise a cap. | 37 | carried | 'There is no expedited path and no exception list' in `merged.md` -- The text states there is no expedited path for these requests. |
| 63 | An answer to a request to raise a cap takes two working days. | 37 | carried | 'they are answered within two working days' in `merged.md` -- The text gives two working days as the answer time for requests, stated as answered within that period. |
| 64 | Chasing an answer to a request to raise a cap doesn't make it take fewer than two working days. | 37 | carried | 'they are answered within two working days; chasing an answer doesn’t make it take fewer' in `merged.md` -- The text states that chasing an answer does not reduce the two working days. |

### `merged.md` -- 71 claim(s): 0 invented, 0 contradicted, 0 supported in part, 71 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Every credential has a cap. | supported | `source_a.md` | 'Every credential has a cap.' in `source_a.md` -- Stated verbatim in source A. |
| 2 | When a credential's cap is spent the gateway answers 429 at the edge. | supported | `source_a.md` | 'When that cap is spent the gateway answers 429 at the edge' in `source_a.md` -- Source A states this directly. |
| 3 | The gateway answers 429 without waking the service behind it. | supported | `source_a.md` | 'without waking the service behind it' in `source_a.md` -- Source A states the 429 is answered without waking the backing service. |
| 4 | An earlier draft of the note argued for a client-side token bucket that mirrored the gateway's own counters. | supported | `source_b.md` | 'An earlier draft of this note argued for a client-side token bucket that mirrored the gateway’s own counters' in `source_b.md` -- Source B states this directly. |
| 5 | Requests are counted against the credential that presented them. | supported | `source_a.md` | 'Requests are counted against the credential that presented them' in `source_a.md` -- Stated directly in source A. |
| 6 | Requests are counted over a fixed window of 60 seconds. | supported | `source_a.md` | 'over a fixed window of 60 seconds' in `source_a.md` -- Both sources give a fixed 60 second window. |
| 7 | The gateway doesn't disclose the start of the counting window. | supported | `source_b.md` | 'over a fixed window of 60 seconds whose start the gateway doesn’t disclose' in `source_b.md` -- Source B states the window start is not disclosed. |
| 8 | Requests are never counted against a connection. | supported | `source_a.md` | 'and never against a connection' in `source_a.md` -- Source A states requests are never counted against a connection. |
| 9 | Opening a second socket buys a caller nothing with respect to the rate limit. | supported | `source_a.md` | 'Opening a second socket therefore buys a caller nothing.' in `source_a.md` -- Stated directly in source A. |
| 10 | The request count follows the credential across hosts. | supported | `source_b.md` | 'The count follows the credential wherever the caller happens to put it, including across hosts.' in `source_b.md` -- Source B states the count follows the credential across hosts. |
| 11 | A client spread across eight worker processes is throttled at exactly the point one process would have been. | supported | `source_a.md` | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `source_a.md` -- Stated directly in source A. |
| 12 | The default allowance is 100 requests in a window. | supported | `source_a.md` | 'The default allowance is 100 requests in a window' in `source_a.md` -- Both sources state the default of 100 per window. |
| 13 | A credential marked for batch work is allowed 1000 requests in the same window as the default allowance. | supported | `source_a.md` | 'a credential marked for batch work is allowed 1000 in the same window' in `source_a.md` -- Stated directly in source A. |
| 14 | The default allowance is enough for every interactive use of the API the platform team has seen. | supported | `source_b.md` | 'which is enough for every interactive use of this API the platform team has seen' in `source_b.md` -- Source B states this about the default allowance. |
| 15 | A caller that needs more than the default allowance is almost always doing batch work under an interactive credential. | supported | `source_b.md` | 'a caller that needs more than that is almost always doing batch work under an interactive credential' in `source_b.md` -- Stated directly in source B. |
| 16 | Callers that retry at once are the largest single reason the cap is there. | supported | `source_a.md` | 'Callers that retry at once are the largest single reason the cap is there at all.' in `source_a.md` -- Stated directly in source A. |
| 17 | The refusal carries a Retry-After header. | supported | `source_a.md` | 'The refusal carries a Retry-After header.' in `source_a.md` -- Stated directly in source A. |
| 18 | The Retry-After header value is a whole number of seconds to wait. | supported | `source_a.md` | 'Its value is a whole number of seconds to wait.' in `source_a.md` -- Stated directly in source A. |
| 19 | The Retry-After header is present on every refusal the gateway sends. | supported | `source_b.md` | 'it is present on every refusal the gateway sends' in `source_b.md` -- Source B states the header is present on every refusal. |
| 20 | The gateway keeps no memory of who backed off politely. | supported | `source_a.md` | 'The gateway keeps no memory of who backed off politely' in `source_a.md` -- Stated directly in source A. |
| 21 | Waiting longer than the Retry-After header asks earns a caller no credit. | supported | `source_a.md` | 'waiting longer than the header asks earns a caller no credit at all' in `source_a.md` -- Stated directly in source A. |
| 22 | The body of the refusal is JSON. | supported | `source_a.md` | 'The body of the refusal is JSON' in `source_a.md` -- Both sources state the body is JSON. |
| 23 | The body of the refusal names what the gateway calls the "window" it counted in. | supported | `source_a.md` | 'it names what the gateway calls the “window” it counted in' in `source_a.md` -- Stated directly in source A. |
| 24 | The body of the refusal names the cap and the tier as plain fields. | supported | `source_b.md` | 'it repeats the cap, the window and the tier as plain fields' in `source_b.md` -- Source B states the cap and tier appear as plain fields in the body. |
| 25 | The refusal body is there so that a human reading a log afterwards can see why the request was refused. | supported | `source_a.md` | 'The body is there so that a human reading a log afterwards can see why the request was refused' in `source_a.md` -- Stated directly in source A. |
| 26 | Nothing in the refusal body is meant for the retry loop. | supported | `source_a.md` | 'nothing in it is meant for the retry loop' in `source_a.md` -- Stated directly in source A. |
| 27 | There are four rules for retrying, given in the order they should be applied. | supported | `source_a.md` | 'Four rules, given in the order they should be applied.' in `source_a.md` -- Stated directly in source A. |
| 28 | The gateway computes the wait with information the caller does not have. | supported | `source_a.md` | 'The gateway has already done that arithmetic, with information the caller does not have' in `source_a.md` -- Stated directly in source A. |
| 29 | The gateway also provides the computed wait on the 503 path. | supported | `source_a.md` | 'and it does the same on the 503 path' in `source_a.md` -- Source A says the gateway does the same arithmetic on the 503 path. |
| 30 | The cause of the refusal on the 503 path is an entirely different one from the 429 refusal. | supported | `source_b.md` | 'On the 503 path the same rule holds, even though the cause of the refusal is an entirely different one.' in `source_b.md` -- Source B states the 503 cause is an entirely different one. |
| 31 | The client cannot see the gateway's counter. | supported | `source_a.md` | 'A wait derived on the client side is a guess about a counter it cannot see.' in `source_a.md` -- Source A states the client cannot see the counter. |
| 32 | The set of responses that are safe to retry is smaller than the set of responses that aren't a success. | supported | `source_b.md` | 'Retry only what is safe to retry, which is a smaller set than the set of responses that aren’t a success.' in `source_b.md` -- Stated directly in source B. |
| 33 | A 200 needs nothing. | supported | `source_b.md` | 'A 200 needs nothing' in `source_b.md` -- Stated directly in source B. |
| 34 | A 429 needs the stated wait. | supported | `source_b.md` | 'a 429 needs the stated wait' in `source_b.md` -- Stated directly in source B. |
| 35 | A 500 can be retried once the stated wait has passed. | supported | `source_b.md` | 'a 500 can be retried once that wait has passed' in `source_b.md` -- Stated directly in source B. |
| 36 | A 503 means the platform itself is overloaded. | supported | `source_b.md` | 'a 503 means the platform itself is overloaded' in `source_b.md` -- Stated directly in source B. |
| 37 | A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive. | supported | `source_a.md` | 'A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive.' in `source_a.md` -- Stated directly in source A. |
| 38 | A batch credential is allowed 1000 requests in a window. | supported | `source_b.md` | 'A batch credential is allowed 1000 requests in a window' in `source_b.md` -- Stated directly in source B. |
| 39 | The batch allowance of 1000 requests in a window is 50 times the default. | supported | `source_b.md` | 'which is 50 times the default' in `source_b.md` -- Source B states 1000 is 50 times the default. |
| 40 | The batch allowance is not a separate counting scheme. | supported | `source_b.md` | 'which is 50 times the default and not a separate counting scheme' in `source_b.md` -- Stated directly in source B. |
| 41 | The batch allowance is measured over exactly the same window as the default. | supported | `source_a.md` | 'it is measured over exactly the same window' in `source_a.md` -- Stated directly in source A. |
| 42 | The tier is set on the credential when the credential is issued. | supported | `source_a.md` | 'The tier is set on the credential when it is issued' in `source_a.md` -- Stated directly in source A. |
| 43 | The tier cannot be asked for per call. | supported | `source_a.md` | 'cannot be asked for per call' in `source_a.md` -- Stated directly in source A. |
| 44 | The window, the header and the body for the batch tier are identical to the interactive case. | supported | `source_b.md` | 'The window, the header and the body are identical to the interactive case' in `source_b.md` -- Stated directly in source B. |
| 45 | A client written for one tier needs no change to run against the other tier. | supported | `source_b.md` | 'a client written for one tier needs no change at all to run against the other' in `source_b.md` -- Stated directly in source B. |
| 46 | Nothing other than the allowance differs between the two tiers. | supported | `source_a.md` | 'Nothing else about the two tiers differs in any way.' in `source_a.md` -- Source A says nothing else differs, following its statement of the allowance difference. |
| 47 | Callers should log every refusal seen and keep the log for at least a week. | supported | `source_b.md` | 'Log every refusal you see, and keep the log for at least a week.' in `source_b.md` -- Stated directly in source B. |
| 48 | Nobody at the platform end will assemble the argument for a larger cap on a caller's behalf. | supported | `source_a.md` | 'nobody at the far end will assemble that argument on its behalf' in `source_a.md` -- Stated directly in source A. |
| 49 | The refusal log line should carry the credential, the window and the wait. | supported | `source_a.md` | 'The log line should carry the credential, the window and the wait.' in `source_a.md` -- Stated directly in source A. |
| 50 | The gateway refuses a request for three reasons and only one of them is the cap. | supported | `source_b.md` | 'The gateway refuses a request for three separate reasons, and only one of them is a cap.' in `source_b.md` -- Stated directly in source B. |
| 51 | Two of the three refusal reasons have nothing to do with how much traffic a caller has sent in the window it is currently in. | supported | `source_b.md` | 'Two of the three have nothing to do with how much traffic a caller has sent in the window it is currently in.' in `source_b.md` -- Stated directly in source B. |
| 52 | A credential may be suspended. | supported | `source_a.md` | 'A credential may be suspended' in `source_a.md` -- Stated directly in source A. |
| 53 | A route may be closed for maintenance. | supported | `source_a.md` | 'a route may be closed for maintenance' in `source_a.md` -- Stated directly in source A. |
| 54 | The request body limit is 5 megabyte. | supported | `source_a.md` | 'a body may exceed the 5 megabyte limit' in `source_a.md` -- Both sources give a 5 megabyte body limit. |
| 55 | A body that exceeds the 5 megabyte limit is refused before it has been read at all. | supported | `source_b.md` | 'a request body over the 5 megabyte limit is refused before it has been read at all' in `source_b.md` -- Stated directly in source B. |
| 56 | None of a suspended credential, a route closed for maintenance, or an oversized body clears itself by waiting for a stated number of seconds. | supported | `source_a.md` | 'None of those three clears itself by waiting for a stated number of seconds.' in `source_a.md` -- Source A says this of the three listed conditions. |
| 57 | A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service. | supported | `source_a.md` | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `source_a.md` -- Stated directly in source A. |
| 58 | After a loop retries against a suspended credential, the log shows nothing except a long run of refusals. | supported | `source_a.md` | 'the log afterwards shows nothing at all except a long run of refusals' in `source_a.md` -- Stated directly in source A. |
| 59 | Reading the status code rather than the class it belongs to costs one comparison. | supported | `source_a.md` | 'Reading the status code rather than the class it belongs to is what separates the two cases, and it costs one comparison.' in `source_a.md` -- Stated directly in source A. |
| 60 | A cap can be raised. | supported | `source_a.md` | 'A cap can be raised' in `source_a.md` -- Both sources state a cap can be raised. |
| 61 | The number of caps raised without a measurement behind them is 0. | supported | `source_a.md` | 'the number of caps raised without a measurement behind them is 0' in `source_a.md` -- Stated directly in source A. |
| 62 | An assertion that the current cap is too small is not enough to get a cap raised. | supported | `source_b.md` | 'A cap can be raised, but not on the strength of an assertion that the current one is too small.' in `source_b.md` -- Stated directly in source B. |
| 63 | A request for a cap increase should bring a week of refusal counts, the shape of the traffic across the day, and the deadline that traffic is serving. | supported | `source_a.md` | 'Bring a week of refusal counts, the shape of the traffic across the day, and the deadline that traffic is serving.' in `source_a.md` -- Stated directly in source A. |
| 64 | The platform team looks at whether the load is smooth or bursty before it looks at the number. | supported | `source_b.md` | 'The team wants to know whether the load is smooth or bursty before it looks at the number at all.' in `source_b.md` -- Source B states the ordering of smooth-or-bursty before the number. |
| 65 | A burst is cheaper to smooth than it is to serve at its peak. | supported | `source_a.md` | 'a burst is cheaper to smooth than it is to serve at its peak' in `source_a.md` -- Both sources state this. |
| 66 | A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap. | supported | `source_a.md` | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `source_a.md` -- Stated directly in source A. |
| 67 | Requests for a cap increase reach the platform team through the usual channel. | supported | `source_a.md` | 'Requests reach the platform team through the usual channel' in `source_a.md` -- Stated in source A within the section on asking for an increase. |
| 68 | Requests for a cap increase are answered within two working days. | supported | `source_a.md` | 'they are answered within two working days' in `source_a.md` -- Stated directly in source A. |
| 69 | Chasing an answer to a cap increase request doesn't make it take fewer than two working days. | supported | `source_b.md` | 'An answer takes two working days, and chasing it doesn’t make it take fewer.' in `source_b.md` -- Stated directly in source B. |
| 70 | There is no expedited path for cap increase requests. | supported | `source_a.md` | 'There is no expedited path and no exception list.' in `source_a.md` -- Both sources state there is no expedited path. |
| 71 | There is no exception list for cap increase requests. | supported | `source_a.md` | 'There is no expedited path and no exception list.' in `source_a.md` -- Source A states there is no exception list. |

## Structure

**9** mechanical check(s) over **104** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **71** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **109**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 31 run(s) over 60 attributed segment(s) — sources interleaved. 6 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

No structural finding.

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **57** departure(s) from its sources. Checking them confirms 44, rejects 0, and leaves 13 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 104 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a4` | subsumed | Counting rule extended with b5's undisclosed window start. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-004`, `A-005`, `A-006`) |
| `a8` | subsumed | Not-an-outage sentence extended with b10's not-a-bug point. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a13` | subsumed | Header value sentence extended with b14's presence fact. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-012`) |
| `a14` | subsumed | Contract sentence extended with b15's closing remark. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a17` | subsumed | Body fields sentence extended with b17's plain-fields detail. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-016`) |
| `a18` | subsumed | Body-parsing sentence combined with b18's consequence. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a23` | subsumed | Rule 1 rationale extended with b24's differing-cause detail. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-018`) |
| `a26` | subsumed | Rule 2 statement carried inside b27's fuller wording. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a27` | superseded | Status code list: b28's wording is more explicit about 503. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`A-019`, `A-020`, `A-021`, `A-022`) |
| `a32` | subsumed | Batch allowance combined with b31's figure and scheme note. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-023`, `A-024`) |
| `a35` | subsumed | Rule 4 statement extended with b34's retention period. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a41` | subsumed | Refusal reasons extended with b40's refused-before-read detail. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-030`, `A-031`, `A-032`) |
| `a43` | superseded | Distinction sentence: b41's fuller wording used. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a49` | subsumed | Load-shape sentence extended with b48's ordering detail. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-039`, `A-040`) |
| `a51` | subsumed | Channel and turnaround extended with b52's chasing remark. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-042`, `A-043`) |
| `b1` | superseded | Title: base title kept. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Rate limiting and the 429 contract for gateway clients' and says so (no claim traced to it) |
| `b2` | superseded | Same fact; base wording kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-001`) |
| `b3` | superseded | Same fact; base wording kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-002`, `B-003`) |
| `b5` | subsumed | Counting rule merged with a4; undisclosed start retained. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-005`, `B-006`, `B-007`) |
| `b6` | superseded | Same point about sockets; base wording kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-008`) |
| `b8` | superseded | Same point; base wording is more specific. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-010`) |
| `b9` | subsumed | Default allowance stated by a7; remainder split into next sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-011`, `B-012`, `B-013`) |
| `b10` | subsumed | Not-a-bug point added to a8; capacity point carried by a9. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-014`) |
| `b11` | superseded | Same point; base wording kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-015`) |
| `b13` | superseded | Header name; base wording kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-016`) |
| `b14` | subsumed | Header value merged with a13; presence fact retained. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-017`, `B-018`) |
| `b15` | subsumed | Contract sentence merged with a14; closing remark retained. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-019`) |
| `b16` | superseded | Same point; base wording kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-020`) |
| `b17` | subsumed | Body description carried by a16 and the extended a17. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-021`, `B-022`) |
| `b18` | subsumed | Body-parsing sentence merged with a18. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b19` | superseded | Same point; base wording is fuller. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b20` | superseded | Section heading: base heading kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b21` | superseded | Same statement; base wording kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-023`, `B-024`) |
| `b22` | subsumed | Rule 1: base wording kept; own-wait point carried by a24. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-025`) |
| `b23` | subsumed | Same rationale; carried in the combined sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-026`) |
| `b24` | subsumed | 503 rule merged into the rule 1 rationale sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-027`, `B-028`) |
| `b25` | superseded | Same point; base wording kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b26` | superseded | Same point; base wording kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b29` | superseded | Same point; base wording kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-034`) |
| `b31` | subsumed | Rule 3 content merged with a32 under the base's rule label. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-035`, `B-036`, `B-037`) |
| `b33` | superseded | Same point; base wording kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-040`) |
| `b34` | subsumed | Rule 4 merged with a35; retention period retained. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-041`, `B-042`) |
| `b35` | superseded | Same point; base wording kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-043`) |
| `b37` | superseded | Section heading: base heading kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b38` | superseded | Same point; base wording kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-044`, `B-045`) |
| `b40` | subsumed | Refusal reasons merged with a41; before-read detail retained. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-047`, `B-048`, `B-049`, `B-050`) |
| `b42` | superseded | Same point; base wording kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-051`) |
| `b43` | subsumed | Log point carried by a44; outage and budget remarks added after. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-052`) |
| `b44` | superseded | Same point; base wording kept, moved to increase section. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-053`) |
| `b45` | reworded | Pronoun replaced with its referent for clarity. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b46` | subsumed | Raising carried by a47; assertion point as its own sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-054`, `B-055`) |
| `b47` | superseded | Same list; base wording kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-056`, `B-057`, `B-058`) |
| `b48` | subsumed | Load-shape sentence merged with a49; ordering retained. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-059`) |
| `b49` | superseded | Same point; base wording kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-060`) |
| `b50` | superseded | Same point; base wording kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-061`) |
| `b51` | superseded | Same point; base sentence is fuller. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-062`) |
| `b52` | subsumed | Turnaround merged with a51; chasing remark retained. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-063`, `B-064`) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | 640c0f94c750 (command) -- lineup fable-sub |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | fable -> claude-fable-5-1 |
| Model (decompose) | fable -> claude-fable-5-1 |
| Model (verify) | fable -> claude-fable-5-1 |
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
| Duration | 409.1s |
| Generated | 2026-09-28T01:21:09+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup fable-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
