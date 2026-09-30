## Verdict

**5 finding(s).** In the claims: 1 partially dropped. In the structure: 2 undeclared absence, 1 false departure, 1 verbatim violation.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 60 |
| Claims extracted from `source_a.md` | 47 |
| Claims extracted from `source_b.md` | 65 |
| Forward — source claims accounted for in the merge | **111/112** |
| Forward — carried only in part | 1 |
| Forward — `source_a.md` claims accounted for | **47/47** |
| Forward — `source_b.md` claims accounted for | **64/65** (1 in part) |
| Reverse — merge claims found in a source | **60/60** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **172/172** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Partly dropped — the merge carries some of this claim

- **B-036** (`source_b.md:21`) — A caller that folds 200, 429, 500 and 503 into one branch will retry hardest during exactly the incident the cap was installed to survive.
  - evidence: 'A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text covers folding the non-success cases (429, 500, 503) into one branch, but it does not say that 200 is folded in as well.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 47 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 47 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Every credential has a cap. | 3 | carried | 'Every credential has a cap of its own.' in `merged.md` -- The text states directly that every credential has its own cap. |
| 2 | When a credential's cap is spent the gateway answers 429 at the edge. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge' in `merged.md` -- The text states that a 429 is answered at the edge once the cap is spent. |
| 3 | The gateway answers 429 without waking the service behind it. | 3 | carried | 'without waking the service behind it' in `merged.md` -- The text states that the 429 is sent without waking the service behind the gateway. |
| 4 | Requests are counted against the credential that presented them. | 5 | carried | 'Requests are counted against the credential that presented them' in `merged.md` -- The text states this directly. |
| 5 | Requests are counted over a fixed window of 60 seconds. | 5 | carried | 'over a fixed window of 60 seconds' in `merged.md` -- The text states that the counting window is a fixed 60 seconds. |
| 6 | Requests are never counted against a connection. | 5 | carried | 'never against a connection' in `merged.md` -- The text states that requests are never counted against a connection. |
| 7 | Opening a second socket buys a caller nothing in rate limiting. | 5 | carried | 'so opening a second socket buys a caller nothing' in `merged.md` -- The text states that a second socket gains a caller nothing. |
| 8 | A client spread across eight worker processes is throttled at exactly the point one process would have been. | 5 | carried | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `merged.md` -- The text states this directly. |
| 9 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- The text states the default allowance as 100 requests in a window. |
| 10 | A credential marked for batch work is allowed 1000 requests in the same window. | 7 | carried | 'a credential marked for batch work is allowed 1000 in the same window' in `merged.md` -- The text states 1000 for batch credentials; the separate fifty-times figure is a conflict to record, not a contradiction. |
| 11 | Callers that retry at once are the largest single reason the cap exists. | 7 | carried | 'Callers that retry at once are most of the reason the cap is there at all — the largest single reason for it.' in `merged.md` -- The text calls immediate retriers the largest single reason for the cap. |
| 12 | The refusal carries a Retry-After header. | 11 | carried | 'Every refusal the gateway sends carries a Retry-After header.' in `merged.md` -- The text states that every refusal carries a Retry-After header. |
| 13 | The Retry-After header value is a whole number of seconds to wait. | 11 | carried | 'Its value is a whole number of seconds to wait.' in `merged.md` -- The text states that the header value is a whole number of seconds. |
| 14 | The gateway keeps no memory of who backed off politely. | 11 | carried | 'The gateway keeps no memory of who backed off politely' in `merged.md` -- The text states this directly. |
| 15 | Waiting longer than the Retry-After header asks earns a caller no credit. | 11 | carried | 'waiting longer than the header asks earns a caller no credit at all' in `merged.md` -- The text states that waiting longer than the header asks earns no credit. |
| 16 | The body of the refusal is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- The text states that the refusal body is JSON. |
| 17 | The refusal body names the window the gateway counted in. | 13 | carried | 'it repeats the cap, the tier and what the gateway calls the “window” it counted in as plain fields' in `merged.md` -- The text states that the body includes the window as a field. |
| 18 | The refusal body names the cap. | 13 | carried | 'it repeats the cap, the tier and what the gateway calls the “window” it counted in as plain fields' in `merged.md` -- The text states that the body includes the cap as a field. |
| 19 | The refusal body names the tier. | 13 | carried | 'it repeats the cap, the tier and what the gateway calls the “window” it counted in as plain fields' in `merged.md` -- The text states that the body includes the tier as a field. |
| 20 | The refusal body is meant for humans reading logs, not for the retry loop. | 13 | carried | 'The body is there so that a human reading a log afterwards can see why the request was refused — nothing in it is meant for the retry loop.' in `merged.md` -- The text states that the body is for humans reading logs, not for the retry loop. |
| 21 | The gateway computes the wait on the 503 path as well. | 19 | carried | 'The gateway has already done that arithmetic, with information the caller does not have, and the same rule holds on the 503 path' in `merged.md` -- The text states that the gateway-computed-wait rule also holds on the 503 path. |
| 22 | A 429 wants the stated wait. | 21 | carried | 'a 429 needs the stated wait' in `merged.md` -- The text states that a 429 needs the stated wait. |
| 23 | A 500 may be retried once the stated wait has passed. | 21 | carried | 'a 500 can be retried once that wait has passed' in `merged.md` -- The text states that a 500 can be retried after the wait has passed. |
| 24 | A 503 is the overload path. | 21 | carried | 'a 503 means the platform itself is overloaded' in `merged.md` -- The text identifies the 503 as signalling platform overload. |
| 25 | A batch credential is allowed fifty times the default allowance. | 23 | carried | 'A batch credential is allowed fifty times the default allowance' in `merged.md` -- The text states fifty times the default; the conflict with the 1000 figure is to be recorded separately. |
| 26 | A batch credential is measured over exactly the same window as the default. | 23 | carried | 'measured over exactly the same window rather than under a separate counting scheme' in `merged.md` -- The text says the batch allowance is measured over exactly the same window as the default. |
| 27 | The tier is set on the credential when it is issued. | 23 | carried | 'The tier is set on the credential when it is issued' in `merged.md` -- The text states this directly. |
| 28 | The tier cannot be asked for per call. | 23 | carried | 'cannot be asked for per call' in `merged.md` -- The text says the tier cannot be asked for per call. |
| 29 | Nothing else about the two tiers differs. | 23 | carried | 'nothing else about the two tiers differs in any way' in `merged.md` -- The text states this directly. |
| 30 | The refusal log line should carry the credential, the window and the wait. | 25 | carried | 'The log line should carry the credential, the window and the wait.' in `merged.md` -- The text states this directly. |
| 31 | The gateway refuses a request for three reasons. | 29 | carried | 'The gateway refuses a request for three reasons' in `merged.md` -- The text states this directly. |
| 32 | A credential may be suspended. | 29 | carried | 'A credential may be suspended' in `merged.md` -- The text states this directly. |
| 33 | A route may be closed for maintenance. | 29 | carried | 'a route may be closed for maintenance' in `merged.md` -- The text states this directly. |
| 34 | The request body limit is 5 megabyte. | 29 | carried | 'a body may exceed the 5 megabyte limit' in `merged.md` -- The text gives a 5 megabyte body limit. |
| 35 | A suspended credential, a closed route, or an oversized body does not clear by waiting for a stated number of seconds. | 29 | carried | 'None of those three clears itself by waiting for a stated number of seconds.' in `merged.md` -- The text says none of the three cases clears by waiting a stated number of seconds. |
| 36 | A loop that waits and retries against a suspended credential never reaches the service. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget — the caller’s own — without ever reaching the service' in `merged.md` -- The text says such a loop never reaches the service. |
| 37 | Reading the status code rather than its class costs one comparison. | 31 | carried | 'Reading the status code rather than the class it belongs to is what separates the two cases, and it costs one comparison' in `merged.md` -- The text states this directly. |
| 38 | A cap can be raised. | 35 | carried | 'A cap can be raised' in `merged.md` -- The text states this directly. |
| 39 | The number of caps raised without a measurement behind them is 0. | 35 | carried | 'the number of caps raised without a measurement behind them is 0' in `merged.md` -- The text states this directly. |
| 40 | A cap increase request should include a week of refusal counts, the shape of the traffic across the day, and the deadline that traffic is serving. | 35 | carried | 'Bring a week of refusal counts, the shape of the traffic across the day, and the deadline that traffic is serving.' in `merged.md` -- The text lists the same three items to bring when asking for an increase. |
| 41 | The platform team looks at whether the load is smooth or bursty. | 35 | carried | 'the platform team looks at whether the load is smooth or bursty' in `merged.md` -- The text states this directly. |
| 42 | A burst is cheaper to smooth than to serve at its peak. | 35 | carried | 'a burst is cheaper to smooth than it is to serve at its peak' in `merged.md` -- The text states this directly. |
| 43 | A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap. | 35 | carried | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `merged.md` -- The text states this directly. |
| 44 | Requests reach the platform team through the usual channel. | 37 | carried | 'Requests reach the platform team through the usual channel' in `merged.md` -- The text states this directly. |
| 45 | Requests to the platform team are answered within two working days. | 37 | carried | 'they are answered within two working days' in `merged.md` -- The text says requests are answered within two working days. |
| 46 | There is no expedited path for cap increase requests. | 37 | carried | 'There is no expedited path' in `merged.md` -- The text states there is no expedited path, in the section on asking for an increase. |
| 47 | There is no exception list for cap increase requests. | 37 | carried | 'no exception list' in `merged.md` -- The text states there is no exception list, in the section on asking for an increase. |

### `source_b.md` -- 65 claim(s): 0 dropped, 0 contradicted, 1 carried in part, 64 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 36 | A caller that folds 200, 429, 500 and 503 into one branch will retry hardest during exactly the incident the cap was installed to survive. | 21 | carried in part | 'A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive.' in `merged.md` -- The text covers folding the non-success cases (429, 500, 503) into one branch, but it does not say that 200 is folded in as well. |
| 1 | Every credential has a cap of its own. | 3 | carried | 'Every credential has a cap of its own.' in `merged.md` -- The text states this directly. |
| 2 | When the cap is spent the gateway answers 429 at the edge. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge' in `merged.md` -- The text states this directly. |
| 3 | When the cap is spent the gateway answers 429 without troubling the service behind it. | 3 | carried | 'without waking the service behind it' in `merged.md` -- 'Without waking the service' has the same meaning as not troubling the service behind it. |
| 4 | Requests are counted against the credential rather than the connection. | 5 | carried | 'Requests are counted against the credential that presented them, never against a connection' in `merged.md` -- The text states that counting is per credential, never per connection. |
| 5 | Requests are counted over a fixed window of 60 seconds. | 5 | carried | 'over a fixed window of 60 seconds' in `merged.md` -- The text states a fixed 60-second window. |
| 6 | The gateway doesn't disclose the start of the 60-second window. | 5 | carried | 'whose start the gateway doesn’t disclose' in `merged.md` -- The text states that the gateway doesn't disclose when the window starts. |
| 7 | There is nothing to be gained by opening more sockets. | 5 | carried | 'opening a second socket buys a caller nothing' in `merged.md` -- Opening more sockets gains nothing, as the text states. |
| 8 | The request count follows the credential wherever the caller puts it, including across hosts. | 5 | carried | 'The count follows the credential wherever the caller puts it, including across hosts' in `merged.md` -- The text states this directly. |
| 9 | A caller spread over many worker processes is throttled at the same point a single process would have been. | 5 | carried | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `merged.md` -- The text illustrates the multi-process case with eight workers throttled at the same point as a single process. |
| 10 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- The text states the default of 100 requests per window. |
| 11 | The default allowance of 100 requests is enough for every interactive use of the API the platform team has seen. | 7 | carried | 'which is enough for every interactive use of this API the platform team has seen' in `merged.md` -- The text states this directly. |
| 12 | A caller that needs more than the default allowance is almost always doing batch work under an interactive credential. | 7 | carried | 'A caller that needs more than the default is almost always doing batch work under an interactive credential' in `merged.md` -- The text states this directly. |
| 13 | The 429 refusal isn't an outage. | 7 | carried | 'A refusal is not an outage and not a bug in the gateway' in `merged.md` -- The text states that a refusal is not an outage. |
| 14 | The 429 refusal isn't a bug in the gateway. | 7 | carried | 'A refusal is not an outage and not a bug in the gateway' in `merged.md` -- The text states that a refusal is not a gateway bug. |
| 15 | The 429 refusal is capacity being held for a request somebody else has already been promised. | 7 | carried | 'It is the platform declining to spend capacity that has already been promised to somebody else' in `merged.md` -- The text describes a refusal as holding capacity already promised to somebody else. |
| 16 | Callers that retry immediately are most of the reason the cap is there. | 7 | carried | 'Callers that retry at once are most of the reason the cap is there at all' in `merged.md` -- The text states this directly. |
| 17 | The header on a refusal is called Retry-After. | 11 | carried | 'Every refusal the gateway sends carries a Retry-After header' in `merged.md` -- The text names the header Retry-After. |
| 18 | The value of the Retry-After header is a whole number of seconds. | 11 | carried | 'Its value is a whole number of seconds to wait' in `merged.md` -- The text states the value is a whole number of seconds. |
| 19 | The Retry-After header is present on every refusal the gateway sends. | 11 | carried | 'Every refusal the gateway sends carries a Retry-After header' in `merged.md` -- The text states the header is present on every refusal. |
| 20 | Waiting the Retry-After duration and then continuing is the entire contract. | 11 | carried | 'Waiting that long and then continuing is the whole of the contract' in `merged.md` -- The text states this directly. |
| 21 | Waiting longer than the Retry-After header asks earns nothing. | 11 | carried | 'waiting longer than the header asks earns a caller no credit at all' in `merged.md` -- The text states that waiting longer earns nothing. |
| 22 | The refusal response body is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- The text states the body is JSON. |
| 23 | The refusal response body repeats the cap, the window and the tier as plain fields. | 13 | carried | 'it repeats the cap, the tier and what the gateway calls the “window” it counted in as plain fields' in `merged.md` -- The text lists the cap, the tier and the window as plain fields. |
| 24 | None of the response body fields is a substitute for the Retry-After header. | 13 | carried | 'None of those fields is a substitute for the header' in `merged.md` -- The text states this directly. |
| 25 | The refusal response body is for the human reading the log afterwards. | 13 | carried | 'The body is there so that a human reading a log afterwards can see why the request was refused' in `merged.md` -- The text states the body is meant for a human reading the log. |
| 26 | There are four rules for what the client does. | 17 | carried | 'Four rules, given in the order they should be applied.' in `merged.md` -- The text states there are four rules. |
| 27 | The rules should be applied in the order they are given. | 17 | carried | 'Four rules, given in the order they should be applied.' in `merged.md` -- The text states the rules should be applied in the order given. |
| 28 | The gateway computes the wait with information the caller cannot see. | 19 | carried | 'The gateway has already done that arithmetic, with information the caller does not have' in `merged.md` -- The text states the gateway computes the wait with information the caller lacks. |
| 29 | On the 503 path the rule of honouring the header holds. | 19 | carried | 'the same rule holds on the 503 path' in `merged.md` -- The text states the honour-the-header rule also holds on the 503 path. |
| 30 | The cause of a 503 refusal is different from the cause of a 429 refusal. | 19 | carried | 'even though the cause of that refusal is an entirely different one' in `merged.md` -- The text says the 503 refusal has an entirely different cause from the 429 refusal. |
| 31 | The set of responses safe to retry is smaller than the set of responses that aren't a success. | 21 | carried | 'Retry only what is safe to retry, which is a smaller set than the set of responses that aren’t a success' in `merged.md` -- The text directly states that the safe-to-retry set is smaller than the non-success set. |
| 32 | A 200 response needs nothing. | 21 | carried | 'A 200 needs nothing' in `merged.md` -- The text states this directly. |
| 33 | A 429 response needs the stated wait. | 21 | carried | 'a 429 needs the stated wait' in `merged.md` -- The text states this directly. |
| 34 | A 500 response can be retried once the stated wait has passed. | 21 | carried | 'a 500 can be retried once that wait has passed' in `merged.md` -- The text states this directly. |
| 35 | A 503 response means the platform itself is overloaded. | 21 | carried | 'a 503 means the platform itself is overloaded' in `merged.md` -- The text states this directly. |
| 37 | A batch credential is allowed 1000 requests in a window. | 23 | carried | 'a credential marked for batch work is allowed 1000 in the same window' in `merged.md` -- The text states that a batch credential is allowed 1000 requests per window. |
| 38 | The batch allowance is 50 times the default. | 23 | carried | 'A batch credential is allowed fifty times the default allowance' in `merged.md` -- Fifty times the default is stated directly. |
| 39 | The batch allowance is not a separate counting scheme. | 23 | carried | 'measured over exactly the same window rather than under a separate counting scheme' in `merged.md` -- The text states that the batch allowance does not use a separate counting scheme. |
| 40 | The window, the header and the body for the batch tier are identical to the interactive case. | 23 | carried | 'The window, the header and the body are identical to the interactive case' in `merged.md` -- The text states this directly. |
| 41 | A client written for one tier needs no change to run against the other tier. | 23 | carried | 'a client written for one tier needs no change at all to run against the other' in `merged.md` -- The text states this directly. |
| 42 | Nothing else about the batch tier differs from the default. | 23 | carried | 'nothing else about the two tiers differs in any way' in `merged.md` -- The text states that nothing else differs between the tiers. |
| 43 | Clients should log every refusal they see. | 25 | carried | 'Log every refusal seen' in `merged.md` -- The text states this directly as a rule. |
| 44 | Clients should keep the refusal log for at least a week. | 25 | carried | 'keep the log for at least a week' in `merged.md` -- The text states this directly. |
| 45 | A caller that cannot say how often it was refused can't make a case for a larger cap. | 25 | carried | 'A caller that cannot say how often it was refused last week cannot argue for a larger cap' in `merged.md` -- The text states the same point, using last week as the reference period. |
| 46 | The platform team won't assemble the case for a larger cap on a caller's behalf. | 25 | carried | 'nobody at the far end will assemble that argument on its behalf' in `merged.md` -- The far end, meaning the platform side, will not build the argument for the caller. |
| 47 | The gateway refuses a request for three separate reasons. | 29 | carried | 'The gateway refuses a request for three reasons' in `merged.md` -- The text states that there are three reasons for refusal. |
| 48 | Only one of the gateway's reasons for refusing a request is a cap. | 29 | carried | 'The gateway refuses a request for three reasons and only one of them is the one above' in `merged.md` -- Only one of the reasons is the cap described above. |
| 49 | Two of the three refusal reasons have nothing to do with how much traffic a caller has sent in the current window. | 29 | carried | 'Two of the three have nothing to do with how much traffic a caller has sent in the window it is currently in' in `merged.md` -- The text states this directly. |
| 50 | A credential can be suspended. | 29 | carried | 'A credential may be suspended' in `merged.md` -- The text states this directly. |
| 51 | A route can be closed while it is being repaired. | 29 | carried | 'a route may be closed for maintenance while it is being repaired' in `merged.md` -- The text states this directly. |
| 52 | The request body limit is 5 megabyte. | 29 | carried | 'a body may exceed the 5 megabyte limit' in `merged.md` -- The text states a 5 megabyte body limit. |
| 53 | A request body over the 5 megabyte limit is refused before it has been read at all. | 29 | carried | 'a body may exceed the 5 megabyte limit, in which case it is refused before it has been read at all' in `merged.md` -- The text states this directly. |
| 54 | A loop retrying against a suspended credential burns its whole budget and reaches nothing. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget — the caller’s own — without ever reaching the service' in `merged.md` -- The reference text states that such a loop spends its whole budget without ever reaching the service. |
| 55 | The log after retrying against a suspended credential shows a long run of refusals and no successes. | 31 | carried | 'the log afterwards shows nothing but a long run of refusals and no successes' in `merged.md` -- The reference text states the claim directly. |
| 56 | A caller that can move half its work to a quieter hour usually finds it doesn't need a larger cap. | 33 | carried | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `merged.md` -- Getting what it needs without any change to the cap means the caller does not need a larger cap. |
| 57 | A cap can be raised. | 33 | carried | 'A cap can be raised' in `merged.md` -- The reference text states the claim directly. |
| 58 | A cap is not raised on the strength of an assertion that the current one is too small. | 33 | carried | 'but not on the strength of an assertion that the current one is too small' in `merged.md` -- The reference text states that a cap is not raised on the strength of an assertion alone. |
| 59 | A request for a larger cap should bring the refusal counts for a full week, the shape of the traffic across the day, and the deadline the traffic exists to meet. | 33 | carried | 'Bring a week of refusal counts, the shape of the traffic across the day, and the deadline that traffic is serving.' in `merged.md` -- All three items the claim lists are named in the reference text. |
| 60 | The platform team wants to know whether the load is smooth or bursty before it looks at the number. | 35 | carried | 'Before it looks at the number at all, the platform team looks at whether the load is smooth or bursty' in `merged.md` -- The reference text states the same ordering of checks with the same meaning. |
| 61 | A burst is cheaper to smooth out than to serve at its peak. | 35 | carried | 'a burst is cheaper to smooth than it is to serve at its peak' in `merged.md` -- The reference text states the claim directly. |
| 62 | Cap increase requests go to the platform team through the usual channel. | 35 | carried | 'Requests reach the platform team through the usual channel' in `merged.md` -- The reference text states that requests reach the platform team through the usual channel. |
| 63 | There is no expedited path for cap increase requests. | 37 | carried | 'There is no expedited path' in `merged.md` -- The reference text states the claim directly. |
| 64 | An answer to a cap increase request takes two working days. | 37 | carried | 'they are answered within two working days' in `merged.md` -- The reference text gives the same two-working-day timeframe for answering cap increase requests. |
| 65 | Chasing an answer doesn't make it take fewer than two working days. | 37 | carried | 'chasing an answer doesn’t make it come sooner' in `merged.md` -- The reference text states that chasing an answer does not make it arrive sooner. |

### `merged.md` -- 60 claim(s): 0 invented, 0 contradicted, 0 supported in part, 60 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Every credential has a cap of its own. | supported | `source_b.md` | 'Every credential has a cap of its own.' in `source_b.md` -- Source B states this verbatim. |
| 2 | When a credential's cap is spent, the gateway answers 429 at the edge without waking the service behind it. | supported | `source_a.md` | 'When that cap is spent the gateway answers 429 at the edge — without waking the service behind it' in `source_a.md` -- Source A states the same behaviour. |
| 3 | Requests are counted against the credential that presented them, never against a connection. | supported | `source_a.md` | 'Requests are counted against the credential that presented them, over a fixed window of 60 seconds, and never against a connection.' in `source_a.md` -- Source A states requests are counted per credential and never per connection. |
| 4 | Requests are counted over a fixed window of 60 seconds. | supported | `source_b.md` | 'over a fixed window of 60 seconds whose start the gateway doesn’t disclose' in `source_b.md` -- Source B gives a fixed 60-second window. |
| 5 | The gateway doesn't disclose the start of the 60-second window. | supported | `source_b.md` | 'over a fixed window of 60 seconds whose start the gateway doesn’t disclose' in `source_b.md` -- Source B states the window start is not disclosed. |
| 6 | The request count follows the credential across hosts. | supported | `source_b.md` | 'The count follows the credential wherever the caller happens to put it, including across hosts.' in `source_b.md` -- Source B states this directly. |
| 7 | A client spread across eight worker processes is throttled at exactly the point one process would have been. | supported | `source_a.md` | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `source_a.md` -- Source A states this verbatim. |
| 8 | The default allowance is 100 requests in a window. | supported | `source_a.md` | 'The default allowance is 100 requests in a window' in `source_a.md` -- Both sources state this, and Source A is quoted. |
| 9 | 100 requests in a window is enough for every interactive use of the API the platform team has seen. | supported | `source_b.md` | 'which is enough for every interactive use of this API the platform team has seen' in `source_b.md` -- Source B states this. |
| 10 | A credential marked for batch work is allowed 1000 requests in the same window. | supported | `source_a.md` | 'a credential marked for batch work is allowed 1000 in the same window' in `source_a.md` -- Source A states this. |
| 11 | A caller that needs more than the default is almost always doing batch work under an interactive credential. | supported | `source_b.md` | 'a caller that needs more than that is almost always doing batch work under an interactive credential' in `source_b.md` -- Source B states this. |
| 12 | A rate-limit refusal is not an outage and not a bug in the gateway. | supported | `source_b.md` | 'The refusal isn’t an outage and it isn’t a bug in the gateway' in `source_b.md` -- Source B states this. |
| 13 | Callers that retry at once are the largest single reason the cap exists. | supported | `source_a.md` | 'Callers that retry at once are the largest single reason the cap is there at all.' in `source_a.md` -- Source A states this. |
| 14 | Every refusal the gateway sends carries a Retry-After header. | supported | `source_b.md` | 'it is present on every refusal the gateway sends' in `source_b.md` -- Source B says the Retry-After header is present on every refusal. |
| 15 | The Retry-After header value is a whole number of seconds to wait. | supported | `source_a.md` | 'Its value is a whole number of seconds to wait.' in `source_a.md` -- Source A states this. |
| 16 | The gateway keeps no memory of who backed off politely. | supported | `source_a.md` | 'The gateway keeps no memory of who backed off politely' in `source_a.md` -- Source A states this. |
| 17 | Waiting longer than the Retry-After header asks earns a caller no credit. | supported | `source_a.md` | 'waiting longer than the header asks earns a caller no credit at all' in `source_a.md` -- Source A states this. |
| 18 | The body of a refusal is JSON. | supported | `source_a.md` | 'The body of the refusal is JSON' in `source_a.md` -- Source A states this. |
| 19 | The refusal body repeats the cap, the tier and the window as plain fields. | supported | `source_b.md` | 'it repeats the cap, the window and the tier as plain fields' in `source_b.md` -- Source B states this. |
| 20 | The refusal body is there so that a human reading a log afterwards can see why the request was refused. | supported | `source_a.md` | 'The body is there so that a human reading a log afterwards can see why the request was refused' in `source_a.md` -- Source A states this. |
| 21 | Nothing in the refusal body is meant for the retry loop. | supported | `source_a.md` | 'nothing in it is meant for the retry loop' in `source_a.md` -- Source A states this. |
| 22 | The guidance gives four rules for retrying. | supported | `source_a.md` | 'Four rules, given in the order they should be applied.' in `source_a.md` -- Source A gives four retry rules. |
| 23 | The rule to honour the header also holds on the 503 path. | supported | `source_b.md` | 'On the 503 path the same rule holds' in `source_b.md` -- Source B states this. |
| 24 | The cause of a 503 refusal is different from the cause of a 429 refusal. | supported | `source_b.md` | 'even though the cause of the refusal is an entirely different one' in `source_b.md` -- Source B says the 503 refusal has an entirely different cause. |
| 25 | A 200 response needs nothing. | supported | `source_b.md` | 'A 200 needs nothing' in `source_b.md` -- Source B states this. |
| 26 | A 429 response needs the stated wait. | supported | `source_b.md` | 'a 429 needs the stated wait' in `source_b.md` -- Source B states that a 429 needs the stated wait. |
| 27 | A 500 response can be retried once the stated wait has passed. | supported | `source_b.md` | 'a 500 can be retried once that wait has passed' in `source_b.md` -- Source B states this directly. |
| 28 | A 503 response means the platform itself is overloaded. | supported | `source_b.md` | 'a 503 means the platform itself is overloaded' in `source_b.md` -- Source B states this directly. |
| 29 | A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive. | supported | `source_a.md` | 'A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive.' in `source_a.md` -- Source A states this verbatim. |
| 30 | A batch credential is allowed fifty times the default allowance. | supported | `source_a.md` | 'A batch credential is allowed fifty times the default allowance' in `source_a.md` -- Source A states this directly. |
| 31 | The batch allowance is measured over exactly the same window as the default, not under a separate counting scheme. | supported | `source_a.md` | 'it is measured over exactly the same window' in `source_a.md` -- Source A says the same window is used, and Source B says the same thing in different words: not a separate counting scheme. |
| 32 | The tier is set on the credential when it is issued. | supported | `source_a.md` | 'The tier is set on the credential when it is issued' in `source_a.md` -- Source A states this directly. |
| 33 | The tier cannot be asked for per call. | supported | `source_a.md` | 'cannot be asked for per call' in `source_a.md` -- Source A states that the tier cannot be asked for per call. |
| 34 | The window, the header and the body are identical for batch and interactive tiers. | supported | `source_b.md` | 'The window, the header and the body are identical to the interactive case' in `source_b.md` -- Source B states this directly. |
| 35 | A client written for one tier needs no change to run against the other tier. | supported | `source_b.md` | 'a client written for one tier needs no change at all to run against the other' in `source_b.md` -- Source B states this directly. |
| 36 | Nothing else about the batch and interactive tiers differs. | supported | `source_a.md` | 'Nothing else about the two tiers differs in any way.' in `source_a.md` -- Source A states this directly. |
| 37 | Refusal logs should be kept for at least a week. | supported | `source_b.md` | 'keep the log for at least a week' in `source_b.md` -- Source B states this directly. |
| 38 | The refusal log line should carry the credential, the window and the wait. | supported | `source_a.md` | 'The log line should carry the credential, the window and the wait.' in `source_a.md` -- Source A states this verbatim. |
| 39 | The gateway refuses a request for three reasons. | supported | `source_a.md` | 'The gateway refuses a request for three reasons' in `source_a.md` -- Source A states this directly. |
| 40 | Only one of the gateway's three refusal reasons is the rate cap. | supported | `source_b.md` | 'only one of them is a cap' in `source_b.md` -- Source B states that only one of the three reasons is a cap. |
| 41 | Two of the three refusal reasons have nothing to do with how much traffic a caller has sent in the current window. | supported | `source_b.md` | 'Two of the three have nothing to do with how much traffic a caller has sent in the window it is currently in.' in `source_b.md` -- Source B states this directly. |
| 42 | A credential may be suspended. | supported | `source_a.md` | 'A credential may be suspended' in `source_a.md` -- Source A states this directly. |
| 43 | A route may be closed for maintenance while it is being repaired. | supported | `source_a.md` | 'a route may be closed for maintenance' in `source_a.md` -- Source A says closed for maintenance, and Source B says closed while being repaired, which has the same meaning. |
| 44 | The request body limit is 5 megabytes. | supported | `source_a.md` | 'the 5 megabyte limit' in `source_a.md` -- Source A gives a 5 megabyte body limit. |
| 45 | A body exceeding the 5 megabyte limit is refused before it has been read. | supported | `source_b.md` | 'a request body over the 5 megabyte limit is refused before it has been read at all' in `source_b.md` -- Source B states this directly. |
| 46 | None of the suspended-credential, closed-route or oversized-body refusals clears by waiting for a stated number of seconds. | supported | `source_a.md` | 'None of those three clears itself by waiting for a stated number of seconds.' in `source_a.md` -- Source A states this about the three non-cap refusal cases. |
| 47 | A loop that waits and retries against a suspended credential never reaches the service. | supported | `source_a.md` | 'spends its whole budget without ever reaching the service' in `source_a.md` -- Source A states that such a loop never reaches the service. |
| 48 | Reading the status code rather than its class distinguishes a rate-cap refusal from other refusals. | supported | `source_a.md` | 'Reading the status code rather than the class it belongs to is what separates the two cases' in `source_a.md` -- Source A states this directly. |
| 49 | Distinguishing the cases by status code costs one comparison. | supported | `source_a.md` | 'it costs one comparison' in `source_a.md` -- Source A states this directly. |
| 50 | A cap can be raised. | supported | `source_a.md` | 'A cap can be raised' in `source_a.md` -- Both sources state that a cap can be raised. |
| 51 | The number of caps raised without a measurement behind them is 0. | supported | `source_a.md` | 'the number of caps raised without a measurement behind them is 0' in `source_a.md` -- Source A states this directly. |
| 52 | An increase request should include a week of refusal counts, the shape of the traffic across the day, and the deadline the traffic is serving. | supported | `source_a.md` | 'Bring a week of refusal counts, the shape of the traffic across the day, and the deadline that traffic is serving.' in `source_a.md` -- Source A lists exactly these three items for an increase request. |
| 53 | Before looking at the number, the platform team looks at whether the load is smooth or bursty. | supported | `source_b.md` | 'The team wants to know whether the load is smooth or bursty before it looks at the number at all.' in `source_b.md` -- Source B states the team checks smoothness or burstiness before looking at the number. |
| 54 | A burst is cheaper to smooth than to serve at its peak. | supported | `source_a.md` | 'a burst is cheaper to smooth than it is to serve at its peak' in `source_a.md` -- Source A states this directly. |
| 55 | A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap. | supported | `source_a.md` | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `source_a.md` -- Source A states this directly. |
| 56 | Increase requests reach the platform team through the usual channel. | supported | `source_a.md` | 'Requests reach the platform team through the usual channel' in `source_a.md` -- Source A states this directly. |
| 57 | Increase requests are answered within two working days. | supported | `source_a.md` | 'they are answered within two working days' in `source_a.md` -- Source A states requests are answered within two working days. |
| 58 | Chasing an answer to an increase request doesn't make it come sooner. | supported | `source_b.md` | 'chasing it doesn’t make it take fewer' in `source_b.md` -- Source B says chasing the answer doesn't make it take fewer days, the same meaning as not coming sooner. |
| 59 | There is no expedited path for increase requests. | supported | `source_a.md` | 'There is no expedited path and no exception list.' in `source_a.md` -- Source A states there is no expedited path. |
| 60 | There is no exception list for increase requests. | supported | `source_a.md` | 'There is no expedited path and no exception list.' in `source_a.md` -- Source A states there is no exception list. |

## Structure

**9** mechanical check(s) over **104** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **60** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **112**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 23 run(s) over 52 attributed segment(s) — sources interleaved. 6 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

`[-...-]` is what the source said and `{+...+}` is what the merge says.

### Absent and undeclared — in a source, not in the merge, and no record explains it

- `b20` (`source_b.md`) — 'What the client does' is not in the merge and no disposition record explains it (nearest merge segment m39 at 0.44)

  ```text
  In the source: What the client does
  ```
- `b37` (`source_b.md`) — 'Other kinds of refusal' is not in the merge and no disposition record explains it (nearest merge segment m12 at 0.56)

  ```text
  In the source: Other kinds of refusal
  ```

### Declared gone, still here — a record says the content departed and the merge carries the segment unchanged

- `a34` (`source_a.md`) — 'Nothing else about the two tiers differs in any way.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Nothing else about the two tiers differs in any way.
  In the merge:  nothing else about the two tiers differs in any way.
  What changed:  [-N-]{+n+}othing else about the two tiers differs in any way.
  ```

### Verbatim violation — an invariant-core token did not survive unchanged

- `b31` (`source_b.md`) — numeric '50' (times) does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **73** departure(s) from its sources. Checking them confirms 55, rejects 4, and leaves 14 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 104 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | Base title kept. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Rate limiting and the 429 contract for gateway clients' and says so (no claim traced to it) |
| `a2` | superseded | b2 wording used; same fact. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`A-001`) |
| `b3` | duplicate | a3 carries the same edge-refusal fact. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-002`, `B-003`) |
| `b4` | reworded | Draft history recast as general guidance under rule 1. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a4` | reconciled | Counting basis combined with undisclosed window start. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-004`, `A-005`, `A-006`) |
| `b5` | reconciled | Counting basis combined with undisclosed window start. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-004`, `B-005`, `B-006`) |
| `a5` | reconciled | Socket point joined with cross-host counting. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-007`) |
| `b7` | reconciled | Socket point joined with cross-host counting. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-008`) |
| `b6` | duplicate | Same point as a5. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-007`) |
| `b8` | duplicate | a6 carries the same point. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-009`) |
| `a7` | reconciled | Allowances combined with b9's interactive-use note. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-009`, `A-010`) |
| `b9` | reconciled | Interactive-use note merged into allowance paragraph. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-010`, `B-011`, `B-012`) |
| `a8` | reconciled | Not-an-outage point joined with not-a-bug. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b10` | reconciled | Not-a-bug and held-capacity points merged with a8/a9. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-013`, `B-014`, `B-015`) |
| `a10` | reconciled | Both characterisations of immediate retries kept. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-011`) |
| `b11` | reconciled | Both characterisations of immediate retries kept. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-016`) |
| `a12` | reconciled | Header name combined with presence on every refusal. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-012`) |
| `b13` | duplicate | Header name already stated. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-017`) |
| `b14` | reconciled | Presence on every refusal merged; seconds duplicates a13. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-018`, `B-019`) |
| `a14` | reworded | Extended with b15's aside. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b15` | subsumed | Same contract statement, aside retained. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-020`) |
| `b16` | duplicate | a15 carries the same point. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-021`) |
| `a16` | reconciled | Body field lists from a16, a17 and b17 combined. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-016`, `A-017`) |
| `a17` | reconciled | Body field lists from a16, a17 and b17 combined. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-018`, `A-019`) |
| `b17` | reconciled | Body field lists from a16, a17 and b17 combined. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-022`, `B-023`) |
| `a18` | reconciled | Both consequences of parsing the body kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b18` | reconciled | Both consequences of parsing the body kept. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-024`) |
| `b19` | duplicate | a19 carries the same point. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-025`) |
| `b21` | duplicate | a21 carries the same statement. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-026`, `B-027`) |
| `a22` | reconciled | Rule 1 headings from both documents combined. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b22` | reconciled | Rule 1 headings from both documents combined. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `a23` | reconciled | 503 point joined with b24's different-cause note. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-021`) |
| `b23` | duplicate | Same point as a23. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-028`) |
| `b24` | reconciled | 503 point joined with a23. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-029`, `B-030`) |
| `a24` | reworded | Joined with a25 into one sentence. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a25` | reworded | Joined with a24 into one sentence. | **rejected** | declared 'reworded', and its text is in the merge (no claim traced to it) |
| `b25` | duplicate | Same point as a24. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b26` | duplicate | Same point as a25. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `a26` | superseded | b27 states the rule more fully. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a27` | superseded | b28 describes the 503 case more clearly. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`A-022`, `A-023`, `A-024`) |
| `b29` | duplicate | a29 carries the same point. | **rejected** | declared 'duplicate', which predicts SUPPORTED; B-036 came back PARTIAL (`B-036`) |
| `a30` | reworded | Joined with b30. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b30` | subsumed | Carried alongside a30. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a32` | reconciled | Batch multiple joined with no-separate-scheme note. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-025`, `A-026`) |
| `b31` | reconciled | 1000 figure already in intro; rest merged with a32. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-037`, `B-038`, `B-039`) |
| `a34` | subsumed | Joined to b32's identical-interface sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-029`) |
| `b32` | reworded | Joined with a34. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-040`, `B-041`) |
| `b33` | duplicate | Same point as a34. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-042`) |
| `a35` | reconciled | Logging rule joined with b34's retention period. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b34` | reconciled | Retention period added to a35's rule. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-043`, `B-044`) |
| `a37` | reworded | Moved directly after the rule statement. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-030`) |
| `b35` | duplicate | a36 carries the same point. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-045`, `B-046`) |
| `b38` | duplicate | a40 carries the same point. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-047`, `B-048`) |
| `a41` | reconciled | Three causes combined with b40's detail. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-032`, `A-033`, `A-034`) |
| `b40` | reconciled | Three causes combined with a41. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-050`, `B-051`, `B-052`, `B-053`) |
| `a43` | reconciled | a43 and b41 combined. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b41` | reconciled | a43 and b41 combined. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `a44` | reconciled | Suspended-credential loop merged from a44, b42, b43. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-036`) |
| `b42` | reconciled | Suspended-credential loop merged from a44, b42, b43. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-054`) |
| `b43` | reconciled | Suspended-credential loop merged from a44, b42, b43. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-055`) |
| `a47` | reconciled | Raise condition combined with b46. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-038`, `A-039`) |
| `b46` | reconciled | Moved into Asking for an increase; combined with a47. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-057`, `B-058`) |
| `b47` | duplicate | a48 carries the same list. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-059`) |
| `a49` | reconciled | Load-shape check joined with b48's ordering. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-041`, `A-042`) |
| `b48` | reconciled | Moved into Asking for an increase; combined with a49. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-060`) |
| `b49` | duplicate | Same point as a49. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-061`) |
| `a50` | reconciled | Quieter-hour point joined with b45's cheapest-fix note. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-043`) |
| `b44` | duplicate | Same point as a50. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-056`) |
| `b45` | reconciled | Cheapest-fix note merged into a50. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `a51` | reconciled | Response time joined with b52's no-chasing note. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-044`, `A-045`) |
| `b52` | reconciled | No-chasing note merged into a51. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-064`, `B-065`) |
| `b50` | duplicate | Same point as a51. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-062`) |
| `b51` | duplicate | a52 carries the same point. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-063`) |


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
| Tokens | 61,217 in, 47,680 out |
| Cost | ~$1.20 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 355.7s |
| Generated | 2026-09-27T16:47:07+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
