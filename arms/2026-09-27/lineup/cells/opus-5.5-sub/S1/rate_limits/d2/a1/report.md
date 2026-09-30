## Verdict

**6 finding(s).** In the claims: 1 partially dropped, 2 contradicted. In the structure: 2 false departure, 1 verbatim violation.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 71 |
| Claims extracted from `source_a.md` | 60 |
| Claims extracted from `source_b.md` | 75 |
| Forward — source claims accounted for in the merge | **132/135** |
| Forward — carried only in part | 1 |
| Forward — `source_a.md` claims accounted for | **59/60** |
| Forward — `source_b.md` claims accounted for | **73/75** (1 in part) |
| Reverse — merge claims found in a source | **71/71** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **206/206** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Partly dropped — the merge carries some of this claim

- **B-016** (`source_b.md:7`) — Callers that retry immediately are most of the reason the cap is there.
  - evidence: 'Callers that retry at once are the largest single reason the cap is there at all' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text makes immediate retriers the largest single reason, which does not entail that they are most of the reason.

### Contradicted — the merge states something different

- **A-035** -- the two documents disagree
  - `source_a.md:23` says: A batch credential is allowed fifty times the default allowance.
  - `merged.md` says: 'A credential marked for batch work is allowed 1000 in the same window' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text gives 1000 against a default of 100, which is ten times the default, not fifty.
- **B-042** -- the two documents disagree
  - `source_b.md:23` says: The batch allowance of 1000 requests is 50 times the default.
  - `merged.md` says: 'The default allowance is 100 requests in a window' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: With a default of 100 and a batch allowance of 1000, the batch allowance is 10 times the default, not 50 times.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 60 claim(s): 0 dropped, 1 contradicted, 0 carried in part, 59 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 35 | A batch credential is allowed fifty times the default allowance. | 23 | contradicted | 'A credential marked for batch work is allowed 1000 in the same window' in `merged.md` -- The text gives 1000 against a default of 100, which is ten times the default, not fifty. |
| 1 | Every credential has a cap. | 3 | carried | 'Every credential has its own cap.' in `merged.md` -- The text states that each credential has its own cap. |
| 2 | When a credential's cap is spent the gateway answers 429 at the edge. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge' in `merged.md` -- The text states the gateway answers 429 at the edge once the cap is spent. |
| 3 | When a credential's cap is spent the gateway answers 429 without waking the service behind it. | 3 | carried | 'without waking the service behind it' in `merged.md` -- The text states the 429 is given without waking the service behind it. |
| 4 | The 429 refusal costs the platform almost nothing. | 3 | carried | 'so the refusal costs the platform almost nothing' in `merged.md` -- The text states the refusal costs the platform almost nothing. |
| 5 | Requests are counted against the credential that presented them. | 5 | carried | 'Requests are counted against the credential that presented them' in `merged.md` -- The text states requests are counted against the presenting credential. |
| 6 | Requests are counted over a fixed window of 60 seconds. | 5 | carried | 'over a fixed window of 60 seconds' in `merged.md` -- The text states counting is over a fixed 60-second window. |
| 7 | Requests are never counted against a connection. | 5 | carried | 'never against a connection' in `merged.md` -- The text states requests are never counted against a connection. |
| 8 | Opening a second socket buys a caller nothing in rate limit allowance. | 5 | carried | 'Opening more sockets therefore buys a caller nothing' in `merged.md` -- Opening more sockets buying nothing entails that a second socket buys nothing. |
| 9 | A client spread across eight worker processes is throttled at exactly the point one process would have been. | 5 | carried | 'A client spread across many worker processes, eight say, is throttled at exactly the point one process would have been' in `merged.md` -- The text gives eight worker processes as the example and states the same throttle point. |
| 10 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- The text states the default allowance is 100 requests in a window. |
| 11 | A credential marked for batch work is allowed 1000 requests in the same window. | 7 | carried | 'A credential marked for batch work is allowed 1000 in the same window' in `merged.md` -- The text states batch credentials are allowed 1000 in the same window. |
| 12 | A 429 refusal is not an outage. | 7 | carried | 'A refusal is not an outage' in `merged.md` -- The text states a refusal is not an outage. |
| 13 | A 429 refusal is the platform declining to spend capacity that has already been promised to somebody else. | 7 | carried | 'It is the platform declining to spend capacity that has already been promised to somebody else' in `merged.md` -- The text states the refusal is the platform declining to spend capacity promised to somebody else. |
| 14 | Waiting is the only correct answer to a 429 refusal. | 7 | carried | 'waiting is the only correct answer' in `merged.md` -- The text states waiting is the only correct answer. |
| 15 | Callers that retry at once are the largest single reason the cap exists. | 7 | carried | 'Callers that retry at once are the largest single reason the cap is there at all' in `merged.md` -- The text states callers retrying at once are the largest single reason for the cap. |
| 16 | The 429 refusal carries a Retry-After header. | 11 | carried | 'Every refusal carries a Retry-After header' in `merged.md` -- The text states every refusal carries a Retry-After header, which includes the 429. |
| 17 | The Retry-After header value is a whole number of seconds to wait. | 11 | carried | 'its value is a whole number of seconds to wait' in `merged.md` -- The text states the header value is a whole number of seconds to wait. |
| 18 | Waiting the Retry-After duration and then continuing is the whole of the contract. | 11 | carried | 'Waiting that long and then continuing is the whole of the contract' in `merged.md` -- The text states waiting that long and continuing is the whole contract. |
| 19 | The gateway keeps no memory of who backed off politely. | 11 | carried | 'The gateway keeps no memory of who backed off politely' in `merged.md` -- The text states the gateway keeps no memory of polite back-off. |
| 20 | Waiting longer than the Retry-After header asks earns a caller no credit. | 11 | carried | 'so waiting longer than the header asks earns a caller nothing' in `merged.md` -- Earning nothing by waiting longer is the same as earning no credit. |
| 21 | The body of the 429 refusal is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- The text states the refusal body is JSON. |
| 22 | The body of the 429 refusal names the window the gateway counted in. | 13 | carried | 'what the gateway calls the “window” it counted in' in `merged.md` -- The text states the body repeats the window the gateway counted in. |
| 23 | The body of the 429 refusal names the cap. | 13 | carried | 'it repeats as plain fields the cap' in `merged.md` -- The text states the body repeats the cap as a plain field. |
| 24 | The body of the 429 refusal names the tier. | 13 | carried | 'it repeats as plain fields the cap, the tier' in `merged.md` -- The text states the body repeats the tier as a plain field. |
| 25 | None of the fields in the 429 refusal body is a substitute for the Retry-After header. | 13 | carried | 'None of those fields is a substitute for the header' in `merged.md` -- The text states none of the body fields substitutes for the header. |
| 26 | The body of the 429 refusal is there so that a human reading a log afterwards can see why the request was refused. | 13 | carried | 'The body is there so that a human reading a log afterwards can see why the request was refused' in `merged.md` -- The text states the stated purpose of the body directly. |
| 27 | Nothing in the 429 refusal body is meant for the retry loop. | 13 | carried | 'nothing in it is meant for the retry loop' in `merged.md` -- The text states nothing in the body is meant for the retry loop. |
| 28 | The gateway computes the Retry-After wait with information the caller does not have. | 19 | carried | 'The gateway has already done that arithmetic with information the caller cannot see' in `merged.md` -- Information the caller cannot see is information the caller does not have. |
| 29 | The gateway computes the wait on the 503 path as well. | 19 | carried | 'the same rule holds on the 503 path' in `merged.md` -- The rule to honour the gateway's header rather than compute a wait holds on the 503 path, so the gateway supplies the wait there too. |
| 30 | A 200 response wants nothing. | 21 | carried | 'A 200 wants nothing' in `merged.md` -- The text states a 200 wants nothing. |
| 31 | A 429 response wants the stated wait. | 21 | carried | 'a 429 wants the stated wait' in `merged.md` -- The text states a 429 wants the stated wait. |
| 32 | A 500 response may be retried once the stated wait has passed. | 21 | carried | 'a 500 may be retried once that wait has passed' in `merged.md` -- The text states a 500 may be retried once the wait has passed. |
| 33 | A 503 response is the overload path. | 21 | carried | 'a 503 is the overload path' in `merged.md` -- The text states a 503 is the overload path. |
| 34 | A client that folds every non-success response into one branch will retry hardest during exactly the incident the cap was installed to survive. | 21 | carried | 'A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive' in `merged.md` -- The text states this directly. |
| 36 | A batch credential is measured over exactly the same window as the default allowance. | 23 | carried | 'A batch credential’s allowance is measured over exactly the same window as the default' in `merged.md` -- The text states batch allowance uses exactly the same window as the default. |
| 37 | The tier is set on the credential when it is issued. | 23 | carried | 'The tier is set on the credential when it is issued' in `merged.md` -- The text states the tier is set when the credential is issued. |
| 38 | The tier cannot be asked for per call. | 23 | carried | 'cannot be asked for per call' in `merged.md` -- The text states the tier cannot be asked for per call. |
| 39 | Nothing else about the batch and default tiers differs. | 23 | carried | 'Nothing else about the two tiers differs.' in `merged.md` -- The text states nothing else about the two tiers differs. |
| 40 | Nobody at the far end will assemble the argument for a larger cap on a caller's behalf. | 25 | carried | 'nobody at the far end will assemble that argument on its behalf' in `merged.md` -- The text states nobody at the far end will assemble the larger-cap argument for the caller. |
| 41 | The refusal log line should carry the credential, the window and the wait. | 25 | carried | 'The log line should carry the credential, the window and the wait' in `merged.md` -- The text states the log line contents directly. |
| 42 | The gateway refuses a request for three reasons. | 29 | carried | 'The gateway refuses a request for three reasons' in `merged.md` -- The text states the gateway refuses a request for three reasons. |
| 43 | Only one of the gateway's refusal reasons is the cap. | 29 | carried | 'only one of them is the cap described above' in `merged.md` -- The text states only one of the reasons is the cap. |
| 44 | A credential may be suspended. | 29 | carried | 'A credential may be suspended' in `merged.md` -- The text states a credential may be suspended. |
| 45 | A route may be closed for maintenance. | 29 | carried | 'a route may be closed for maintenance' in `merged.md` -- The text states a route may be closed for maintenance. |
| 46 | The request body limit is 5 megabyte. | 29 | carried | 'a body may exceed the 5 megabyte limit' in `merged.md` -- The text refers to the 5 megabyte body limit. |
| 47 | None of the suspended credential, closed route, or oversized body refusals clears itself by waiting for a stated number of seconds. | 29 | carried | 'None of those three clears itself by waiting for a stated number of seconds.' in `merged.md` -- The text states none of the three clears itself by waiting. |
| 48 | A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `merged.md` -- The text states this directly. |
| 49 | Reading the status code rather than its class separates a cap refusal from other refusals. | 31 | carried | 'Reading the status code rather than the class it belongs to is what separates the two cases' in `merged.md` -- The text states reading the status code rather than its class separates the cases. |
| 50 | Reading the status code costs one comparison. | 31 | carried | 'it costs one comparison' in `merged.md` -- The text states it costs one comparison. |
| 51 | A cap can be raised. | 35 | carried | 'A cap can be raised' in `merged.md` -- The text states a cap can be raised. |
| 52 | The number of caps raised without a measurement behind them is 0. | 35 | carried | 'the number of caps raised without a measurement behind them is 0' in `merged.md` -- The text states the count is 0. |
| 53 | A cap increase request should include a week of refusal counts, the shape of the traffic across the day, and the deadline that traffic is serving. | 35 | carried | 'Bring the refusal counts for a full week, the shape of the traffic across the day, and the deadline that traffic is serving' in `merged.md` -- The text lists the same three items for an increase request. |
| 54 | The platform team looks at whether the load is smooth or bursty. | 35 | carried | 'The platform team looks at whether the load is smooth or bursty' in `merged.md` -- The text states this directly. |
| 55 | A burst is cheaper to smooth than it is to serve at its peak. | 35 | carried | 'a burst is cheaper to smooth out than it is to serve at its peak' in `merged.md` -- The text states a burst is cheaper to smooth than to serve at peak. |
| 56 | A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap. | 35 | carried | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `merged.md` -- The text states this directly. |
| 57 | Cap increase requests reach the platform team through the usual channel. | 37 | carried | 'Requests reach the platform team through the usual channel' in `merged.md` -- The text states increase requests reach the team through the usual channel. |
| 58 | Cap increase requests are answered within two working days. | 37 | carried | 'are answered within two working days' in `merged.md` -- The text states requests are answered within two working days. |
| 59 | There is no expedited path for cap increase requests. | 37 | carried | 'There is no expedited path' in `merged.md` -- The text states there is no expedited path. |
| 60 | There is no exception list for cap increase requests. | 37 | carried | 'no exception list' in `merged.md` -- The text states there is no exception list. |

### `source_b.md` -- 75 claim(s): 0 dropped, 1 contradicted, 1 carried in part, 73 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 42 | The batch allowance of 1000 requests is 50 times the default. | 23 | contradicted | 'The default allowance is 100 requests in a window' in `merged.md` -- With a default of 100 and a batch allowance of 1000, the batch allowance is 10 times the default, not 50 times. |
| 16 | Callers that retry immediately are most of the reason the cap is there. | 7 | carried in part | 'Callers that retry at once are the largest single reason the cap is there at all' in `merged.md` -- The text makes immediate retriers the largest single reason, which does not entail that they are most of the reason. |
| 1 | Every credential has a cap of its own. | 3 | carried | 'Every credential has its own cap.' in `merged.md` -- The text states every credential has its own cap. |
| 2 | When the cap is spent the gateway answers 429 at the edge. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge' in `merged.md` -- The text states the gateway answers 429 at the edge when the cap is spent. |
| 3 | When the cap is spent the gateway answers without troubling the service behind it. | 3 | carried | 'without waking the service behind it' in `merged.md` -- Not waking the service is the same as not troubling it. |
| 4 | Requests are counted against the credential rather than the connection. | 5 | carried | 'Requests are counted against the credential that presented them, never against a connection' in `merged.md` -- The text states counting is per credential and never per connection. |
| 5 | Requests are counted over a fixed window of 60 seconds. | 5 | carried | 'over a fixed window of 60 seconds' in `merged.md` -- The text states a fixed 60-second window. |
| 6 | The gateway doesn't disclose the start of the fixed window. | 5 | carried | 'whose start the gateway does not disclose' in `merged.md` -- The text states the gateway does not disclose the window start. |
| 7 | There is nothing to be gained by opening more sockets. | 5 | carried | 'Opening more sockets therefore buys a caller nothing' in `merged.md` -- Buying nothing is the same as nothing to be gained. |
| 8 | The request count follows the credential wherever the caller puts it, including across hosts. | 5 | carried | 'the count follows the credential wherever the caller puts it, including across hosts' in `merged.md` -- The text states this directly. |
| 9 | A caller spread over many worker processes is throttled at the same point a single process would have been. | 5 | carried | 'A client spread across many worker processes, eight say, is throttled at exactly the point one process would have been' in `merged.md` -- The text states many worker processes are throttled at the single-process point. |
| 10 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- The text states the default allowance is 100 requests in a window. |
| 11 | The default allowance of 100 requests in a window is enough for every interactive use of the API the platform team has seen. | 7 | carried | 'which covers every interactive use of this API the platform team has seen' in `merged.md` -- The text states the default covers every interactive use the team has seen. |
| 12 | A caller that needs more than the default allowance is almost always doing batch work under an interactive credential. | 7 | carried | 'a caller that needs more is almost always doing batch work under an interactive credential' in `merged.md` -- The text states this directly. |
| 13 | The 429 refusal isn't an outage. | 7 | carried | 'A refusal is not an outage' in `merged.md` -- The text states a refusal is not an outage. |
| 14 | The 429 refusal isn't a bug in the gateway. | 7 | carried | 'not a bug in the gateway' in `merged.md` -- The text states a refusal is not a bug in the gateway. |
| 15 | The 429 refusal is capacity being held for a request somebody else has already been promised. | 7 | carried | 'It is the platform declining to spend capacity that has already been promised to somebody else' in `merged.md` -- Declining to spend capacity already promised to someone else carries the same meaning. |
| 17 | The header on a gateway refusal is called Retry-After. | 11 | carried | 'Every refusal carries a Retry-After header' in `merged.md` -- The text names the refusal header Retry-After. |
| 18 | The Retry-After value is a whole number of seconds. | 11 | carried | 'its value is a whole number of seconds to wait' in `merged.md` -- The text states the value is a whole number of seconds. |
| 19 | The Retry-After header is present on every refusal the gateway sends. | 11 | carried | 'Every refusal carries a Retry-After header' in `merged.md` -- The text states every refusal carries the header. |
| 20 | Waiting the Retry-After duration and then continuing is the entire contract. | 11 | carried | 'Waiting that long and then continuing is the whole of the contract' in `merged.md` -- The whole of the contract is the same as the entire contract. |
| 21 | Waiting longer than the Retry-After header asks earns nothing. | 11 | carried | 'so waiting longer than the header asks earns a caller nothing' in `merged.md` -- The text states waiting longer earns nothing. |
| 22 | Nobody at the gateway end is keeping score of how long callers wait. | 11 | carried | 'The gateway keeps no memory of who backed off politely' in `merged.md` -- Keeping no memory of polite back-off means no score is kept of how long callers wait. |
| 23 | The refusal response body is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- The text states the refusal body is JSON. |
| 24 | The refusal response body repeats the cap, the window and the tier as plain fields. | 13 | carried | 'it repeats as plain fields the cap, the tier and what the gateway calls the “window” it counted in' in `merged.md` -- The text states the body repeats the cap, tier and window as plain fields. |
| 25 | None of the refusal response body fields is a substitute for the Retry-After header. | 13 | carried | 'None of those fields is a substitute for the header' in `merged.md` -- The text states none of the fields substitutes for the header. |
| 26 | The refusal response body is for the human reading the log afterwards. | 13 | carried | 'The body is there so that a human reading a log afterwards can see why the request was refused' in `merged.md` -- The text states the body is for a human reading the log afterwards. |
| 27 | There are four rules for what the client does. | 17 | carried | 'There are four rules' in `merged.md` -- The text states there are four rules. |
| 28 | The four client rules are to be applied in the order they are given. | 17 | carried | 'the order they are given in is the order to apply them' in `merged.md` -- The text states the rules are applied in the order given. |
| 29 | The client should honour the Retry-After header and not compute its own wait. | 19 | carried | 'Honour the header, every time, and do not compute your own wait' in `merged.md` -- The text states this rule directly. |
| 30 | The gateway computes the wait using information the caller cannot see. | 19 | carried | 'The gateway has already done that arithmetic with information the caller cannot see' in `merged.md` -- The text states the gateway computes the wait with information the caller cannot see. |
| 31 | On the 503 path the rule to honour the header holds as well. | 19 | carried | 'the same rule holds on the 503 path' in `merged.md` -- The text states the honour-the-header rule holds on the 503 path. |
| 32 | The cause of a 503 refusal is different from the cause of a 429 refusal. | 19 | carried | 'even though the cause of that refusal is entirely different' in `merged.md` -- The text states the 503 refusal has an entirely different cause. |
| 33 | Anything computed on the client side is a guess. | 19 | carried | 'A wait derived on the client side is a guess' in `merged.md` -- In the context of computing waits, the text states a client-side derivation is a guess. |
| 34 | The client should retry only what is safe to retry. | 21 | carried | 'Retry only what is safe to retry' in `merged.md` -- The text states this rule directly. |
| 35 | The set of responses safe to retry is smaller than the set of responses that aren't a success. | 21 | carried | 'which is a smaller set than the set of responses that are not a success' in `merged.md` -- The text states the safe-to-retry set is smaller than the non-success set. |
| 36 | A 200 response needs nothing. | 21 | carried | 'A 200 wants nothing' in `merged.md` -- Wants nothing is the same as needs nothing. |
| 37 | A 429 response needs the stated wait. | 21 | carried | 'a 429 wants the stated wait' in `merged.md` -- The text states a 429 wants the stated wait. |
| 38 | A 500 response can be retried once the stated wait has passed. | 21 | carried | 'a 500 may be retried once that wait has passed' in `merged.md` -- The text states a 500 may be retried after the wait. |
| 39 | A 503 response means the platform itself is overloaded. | 21 | carried | 'the platform itself is overloaded' in `merged.md` -- The text states a 503 means the platform itself is overloaded. |
| 40 | A caller that folds 200, 429, 500 and 503 into one branch will retry hardest during exactly the incident the cap was installed to survive. | 21 | carried | 'A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive' in `merged.md` -- A client folding all four codes into one branch necessarily folds every non-success, so the stated consequence applies. |
| 41 | A batch credential is allowed 1000 requests in a window. | 23 | carried | 'A credential marked for batch work is allowed 1000 in the same window.' in `merged.md` -- The reference text states the batch allowance is 1000 in the same window. |
| 43 | The batch allowance is not a separate counting scheme. | 23 | carried | 'A batch credential’s allowance is measured over exactly the same window as the default, not under a separate counting scheme.' in `merged.md` -- The text explicitly says the batch allowance is not under a separate counting scheme. |
| 44 | The window, the header and the body for the batch tier are identical to the interactive case. | 23 | carried | 'The window, the header and the body are identical to the interactive case' in `merged.md` -- The text states the window, header and body are identical to the interactive case. |
| 45 | A client written for one tier needs no change to run against the other tier. | 23 | carried | 'so a client written for one tier needs no change at all to run against the other' in `merged.md` -- The text states a client for one tier needs no change to run against the other. |
| 46 | Nothing else about the batch tier differs from the default. | 23 | carried | 'Nothing else about the two tiers differs.' in `merged.md` -- The text states nothing else about the two tiers differs. |
| 47 | The client should log every refusal it sees. | 25 | carried | 'Log every refusal seen' in `merged.md` -- The text instructs logging every refusal seen. |
| 48 | The client should keep the refusal log for at least a week. | 25 | carried | 'keep the log for at least a week' in `merged.md` -- The text instructs keeping the log for at least a week. |
| 49 | A caller that cannot say how often it was refused can't make a case for a larger cap. | 25 | carried | 'A caller that cannot say how often it was refused last week cannot argue for a larger cap' in `merged.md` -- The text states such a caller cannot argue for a larger cap. |
| 50 | The platform team won't assemble the case for a larger cap on a caller's behalf. | 25 | carried | 'nobody at the far end will assemble that argument on its behalf' in `merged.md` -- Nobody at the far end, which includes the platform team, will assemble the argument on the caller's behalf. |
| 51 | The gateway refuses a request for three separate reasons. | 29 | carried | 'The gateway refuses a request for three reasons' in `merged.md` -- The text states the gateway refuses a request for three reasons. |
| 52 | Only one of the gateway's three refusal reasons is a cap. | 29 | carried | 'only one of them is the cap described above' in `merged.md` -- The text states only one of the three reasons is the cap. |
| 53 | Two of the three gateway refusal reasons have nothing to do with how much traffic a caller has sent in the current window. | 29 | carried | 'the other two have nothing to do with how much traffic a caller has sent in the window it is currently in' in `merged.md` -- The text states the other two reasons are unrelated to traffic sent in the current window. |
| 54 | A credential can be suspended. | 29 | carried | 'A credential may be suspended' in `merged.md` -- The text states a credential may be suspended. |
| 55 | A route can be closed while it is being repaired. | 29 | carried | 'a route may be closed for maintenance' in `merged.md` -- The text states a route may be closed for maintenance, which matches closure while being repaired. |
| 56 | The request body limit is 5 megabyte. | 29 | carried | 'a body may exceed the 5 megabyte limit' in `merged.md` -- The text states the body limit is 5 megabyte. |
| 57 | A request body over the 5 megabyte limit is refused before it has been read at all. | 29 | carried | 'a body may exceed the 5 megabyte limit, in which case it is refused before it has been read at all' in `merged.md` -- The text states an oversized body is refused before it has been read at all. |
| 58 | A loop retrying against a suspended credential burns its whole budget and reaches nothing. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `merged.md` -- The text states the loop spends its whole budget without reaching the service. |
| 59 | The log after retrying against a suspended credential shows a long run of refusals and no successes. | 31 | carried | 'the log afterwards shows nothing but a long run of refusals and no successes' in `merged.md` -- The text states the log shows a long run of refusals and no successes. |
| 60 | Refusals from a suspended credential are not an outage. | 31 | carried | 'which reads like an outage and is not one' in `merged.md` -- The text states the situation reads like an outage but is not one. |
| 61 | The budget wasted retrying against a suspended credential is the caller's own. | 31 | carried | 'the wasted budget is the caller’s own' in `merged.md` -- The text states the wasted budget is the caller's own. |
| 62 | A caller that can move half its work to a quieter hour usually finds it doesn't need a larger cap. | 33 | carried | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all.' in `merged.md` -- Getting what it needs without any change to the cap means it does not need a larger cap. |
| 63 | Moving work to a quieter hour is the cheapest fix available. | 33 | carried | 'That is the cheapest fix available to anybody' in `merged.md` -- The text calls moving work to a quieter hour the cheapest fix available. |
| 64 | Moving work to a quieter hour is available to almost everybody. | 33 | carried | 'it is available to almost everybody' in `merged.md` -- The text states the fix is available to almost everybody. |
| 65 | A cap can be raised. | 33 | carried | 'A cap can be raised' in `merged.md` -- The text states a cap can be raised. |
| 66 | A cap is not raised on the strength of an assertion that the current one is too small. | 33 | carried | 'but not on the strength of an assertion that the current one is too small' in `merged.md` -- The text states caps are not raised on the strength of such an assertion. |
| 67 | A request to raise a cap should include the refusal counts for a full week. | 33 | carried | 'Bring the refusal counts for a full week' in `merged.md` -- The text instructs bringing refusal counts for a full week. |
| 68 | A request to raise a cap should include the shape of the traffic across the day. | 33 | carried | 'the shape of the traffic across the day' in `merged.md` -- The text lists the shape of traffic across the day as something to bring. |
| 69 | A request to raise a cap should include the deadline the traffic exists to meet. | 33 | carried | 'the deadline that traffic is serving' in `merged.md` -- The text lists the deadline the traffic serves as something to bring. |
| 70 | The platform team wants to know whether the load is smooth or bursty before it looks at the number. | 35 | carried | 'The platform team looks at whether the load is smooth or bursty before it looks at the number at all' in `merged.md` -- The text states the team examines smoothness or burstiness before the number. |
| 71 | A burst is cheaper to smooth out than to serve at its peak. | 35 | carried | 'a burst is cheaper to smooth out than it is to serve at its peak' in `merged.md` -- The text states a burst is cheaper to smooth out than to serve at its peak. |
| 72 | Cap-raise requests go to the platform team through the usual channel. | 35 | carried | 'Requests reach the platform team through the usual channel' in `merged.md` -- The text states requests reach the platform team through the usual channel. |
| 73 | There is no expedited path for cap-raise requests. | 37 | carried | 'There is no expedited path' in `merged.md` -- The text states there is no expedited path. |
| 74 | An answer to a cap-raise request takes two working days. | 37 | carried | 'are answered within two working days' in `merged.md` -- The text states requests are answered within two working days. |
| 75 | Chasing a cap-raise request doesn't make the answer take fewer than two working days. | 37 | carried | 'chasing an answer does not make it arrive any sooner' in `merged.md` -- The text states chasing an answer does not make it arrive any sooner. |

### `merged.md` -- 71 claim(s): 0 invented, 0 contradicted, 0 supported in part, 71 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Every credential has its own cap. | supported | `source_b.md` | 'Every credential has a cap of its own.' in `source_b.md` -- Source B states directly that each credential has its own cap. |
| 2 | When a credential's cap is spent, the gateway answers 429 at the edge. | supported | `source_a.md` | 'When that cap is spent the gateway answers 429 at the edge' in `source_a.md` -- Source A states that the gateway answers 429 at the edge once the cap is spent. |
| 3 | When a credential's cap is spent, the gateway answers without waking the service behind it. | supported | `source_a.md` | 'without waking the service behind it' in `source_a.md` -- Source A states that the 429 is given without waking the service behind the gateway. |
| 4 | A 429 refusal at the gateway edge costs the platform almost nothing. | supported | `source_a.md` | 'the refusal costs the platform almost nothing' in `source_a.md` -- Source A states that the refusal costs the platform almost nothing. |
| 5 | Requests to the gateway are counted against the credential that presented them. | supported | `source_a.md` | 'Requests are counted against the credential that presented them' in `source_a.md` -- Source A states that requests are counted against the presenting credential. |
| 6 | Requests to the gateway are never counted against a connection. | supported | `source_a.md` | 'and never against a connection' in `source_a.md` -- Source A states that requests are never counted against a connection. |
| 7 | Requests are counted over a fixed window of 60 seconds. | supported | `source_a.md` | 'over a fixed window of 60 seconds' in `source_a.md` -- Source A states that the counting window is a fixed 60 seconds. |
| 8 | The gateway does not disclose the start of the 60-second counting window. | supported | `source_b.md` | 'over a fixed window of 60 seconds whose start the gateway doesn’t disclose' in `source_b.md` -- Source B states that the gateway does not disclose when the window starts. |
| 9 | Opening more sockets does not increase a caller's allowance. | supported | `source_b.md` | 'There is nothing to be gained by opening more sockets.' in `source_b.md` -- Source B states that opening more sockets gains the caller nothing. |
| 10 | The request count follows the credential across hosts. | supported | `source_b.md` | 'The count follows the credential wherever the caller happens to put it, including across hosts.' in `source_b.md` -- Source B states that the count follows the credential across hosts. |
| 11 | A client spread across many worker processes is throttled at exactly the point one process would have been. | supported | `source_b.md` | 'A caller spread over many worker processes is throttled at the same point a single process would have been.' in `source_b.md` -- Source B states the same thing for many worker processes, and Source A says it for eight processes. |
| 12 | The default allowance is 100 requests in a window. | supported | `source_a.md` | 'The default allowance is 100 requests in a window' in `source_a.md` -- Both sources state a default allowance of 100 requests per window. |
| 13 | The default allowance of 100 requests covers every interactive use of the API the platform team has seen. | supported | `source_b.md` | 'which is enough for every interactive use of this API the platform team has seen' in `source_b.md` -- Source B states that 100 requests covers every interactive use the team has seen. |
| 14 | A caller that needs more than the default allowance is almost always doing batch work under an interactive credential. | supported | `source_b.md` | 'a caller that needs more than that is almost always doing batch work under an interactive credential' in `source_b.md` -- Source B states this directly. |
| 15 | A credential marked for batch work is allowed 1000 requests in the same window. | supported | `source_a.md` | 'a credential marked for batch work is allowed 1000 in the same window' in `source_a.md` -- Source A states that batch credentials are allowed 1000 requests in the same window. |
| 16 | A 429 refusal is not an outage. | supported | `source_a.md` | 'A refusal is not an outage' in `source_a.md` -- Source A states that a refusal is not an outage. |
| 17 | A 429 refusal is not a bug in the gateway. | supported | `source_b.md` | 'it isn’t a bug in the gateway' in `source_b.md` -- Source B states that the refusal is not a gateway bug. |
| 18 | A 429 refusal is the platform declining to spend capacity that has already been promised to somebody else. | supported | `source_a.md` | 'It is the platform declining to spend capacity that has already been promised to somebody else' in `source_a.md` -- Source A states this directly. |
| 19 | Callers that retry at once are the largest single reason the cap exists. | supported | `source_a.md` | 'Callers that retry at once are the largest single reason the cap is there at all.' in `source_a.md` -- Source A states that immediate retriers are the largest single reason for the cap. |
| 20 | An earlier draft of the guidance argued for a client-side token bucket that mirrored the gateway's own counters. | supported | `source_b.md` | 'An earlier draft of this note argued for a client-side token bucket that mirrored the gateway’s own counters' in `source_b.md` -- Source B states this about its own earlier draft. |
| 21 | Every refusal carries a Retry-After header. | supported | `source_b.md` | 'it is present on every refusal the gateway sends' in `source_b.md` -- Source B states that Retry-After is present on every refusal. |
| 22 | The Retry-After header value is a whole number of seconds to wait. | supported | `source_a.md` | 'Its value is a whole number of seconds to wait.' in `source_a.md` -- Source A states that the header value is a whole number of seconds to wait. |
| 23 | The gateway keeps no memory of who backed off politely. | supported | `source_a.md` | 'The gateway keeps no memory of who backed off politely' in `source_a.md` -- Source A states this directly. |
| 24 | Waiting longer than the Retry-After header asks earns a caller nothing. | supported | `source_b.md` | 'Waiting longer than the header asks earns nothing' in `source_b.md` -- Source B states that waiting longer than asked earns nothing. |
| 25 | The body of the refusal is JSON. | supported | `source_a.md` | 'The body of the refusal is JSON' in `source_a.md` -- Source A states that the refusal body is JSON. |
| 26 | The refusal body repeats as plain fields the cap, the tier and the window the gateway counted in. | supported | `source_b.md` | 'it repeats the cap, the window and the tier as plain fields' in `source_b.md` -- Source B states that the body repeats the cap, window and tier as plain fields, and Source A calls the window the one the gateway counted in. |
| 27 | The refusal body is there so that a human reading a log afterwards can see why the request was refused. | supported | `source_a.md` | 'The body is there so that a human reading a log afterwards can see why the request was refused' in `source_a.md` -- Source A states the purpose of the body directly. |
| 28 | Nothing in the refusal body is meant for the retry loop. | supported | `source_a.md` | 'nothing in it is meant for the retry loop' in `source_a.md` -- Source A states that nothing in the body is meant for the retry loop. |
| 29 | There are four retry rules. | supported | `source_b.md` | 'There are four rules' in `source_b.md` -- Source B states that there are four rules. |
| 30 | The retry rules are to be applied in the order they are given. | supported | `source_b.md` | 'the order they are given in is the order to apply them' in `source_b.md` -- Source B states that the rules are applied in the order given. |
| 31 | The gateway computes the wait with information the caller cannot see. | supported | `source_b.md` | 'it did it with information the caller cannot see' in `source_b.md` -- Source B states that the gateway computes the wait with information the caller cannot see. |
| 32 | The rule to honour the Retry-After header holds on the 503 path. | supported | `source_b.md` | 'On the 503 path the same rule holds' in `source_b.md` -- Source B states that the honour-the-header rule holds on the 503 path. |
| 33 | The cause of a 503 refusal is entirely different from the cause of a 429 refusal. | supported | `source_b.md` | 'even though the cause of the refusal is an entirely different one' in `source_b.md` -- Source B states that the 503 refusal has an entirely different cause. |
| 34 | The set of responses safe to retry is smaller than the set of responses that are not a success. | supported | `source_b.md` | 'which is a smaller set than the set of responses that aren’t a success' in `source_b.md` -- Source B states that the safe-to-retry set is smaller than the set of non-success responses. |
| 35 | A 200 response wants nothing. | supported | `source_a.md` | 'A 200 wants nothing' in `source_a.md` -- Source A states this directly. |
| 36 | A 429 response wants the stated wait. | supported | `source_a.md` | 'a 429 wants the stated wait' in `source_a.md` -- Source A states this directly. |
| 37 | A 500 response may be retried once the wait has passed. | supported | `source_a.md` | 'a 500 may be retried once that wait has passed' in `source_a.md` -- Source A states this directly. |
| 38 | A 503 response is the overload path, meaning the platform itself is overloaded. | supported | `source_b.md` | 'a 503 means the platform itself is overloaded' in `source_b.md` -- Source B gives this meaning, and Source A calls the 503 the overload path. |
| 39 | A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive. | supported | `source_a.md` | 'A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive.' in `source_a.md` -- Source A states this verbatim. |
| 40 | A batch credential's allowance is measured over exactly the same window as the default. | supported | `source_a.md` | 'it is measured over exactly the same window' in `source_a.md` -- Source A states that the batch allowance uses exactly the same window. |
| 41 | A batch credential's allowance is not measured under a separate counting scheme. | supported | `source_b.md` | 'not a separate counting scheme' in `source_b.md` -- Source B states that batch is not a separate counting scheme. |
| 42 | The tier is set on the credential when it is issued. | supported | `source_a.md` | 'The tier is set on the credential when it is issued' in `source_a.md` -- Source A states this directly. |
| 43 | The tier cannot be asked for per call. | supported | `source_a.md` | 'cannot be asked for per call' in `source_a.md` -- Source A states that the tier cannot be requested per call. |
| 44 | The window, the header and the body are identical for the batch tier and the interactive tier. | supported | `source_b.md` | 'The window, the header and the body are identical to the interactive case' in `source_b.md` -- Source B states this directly. |
| 45 | A client written for one tier needs no change to run against the other tier. | supported | `source_b.md` | 'so a client written for one tier needs no change at all to run against the other' in `source_b.md` -- Source B states this directly. |
| 46 | Nothing else about the batch and interactive tiers differs. | supported | `source_a.md` | 'Nothing else about the two tiers differs in any way.' in `source_a.md` -- Source A states that nothing else differs between the tiers. |
| 47 | Every refusal seen should be logged. | supported | `source_a.md` | 'Log every refusal seen.' in `source_a.md` -- Source A states this directly. |
| 48 | The refusal log should be kept for at least a week. | supported | `source_b.md` | 'keep the log for at least a week' in `source_b.md` -- Source B states the one-week minimum retention. |
| 49 | The refusal log line should carry the credential, the window and the wait. | supported | `source_a.md` | 'The log line should carry the credential, the window and the wait.' in `source_a.md` -- Source A states this verbatim. |
| 50 | Nobody at the platform end will assemble the argument for a larger cap on a caller's behalf. | supported | `source_a.md` | 'nobody at the far end will assemble that argument on its behalf' in `source_a.md` -- Source A states that nobody at the far end will build the argument for the caller. |
| 51 | Not all refusals are caps. | supported | `source_a.md` | 'Not all are caps.' in `source_a.md` -- Source A states that not all refusals are caps. |
| 52 | The gateway refuses a request for three reasons. | supported | `source_a.md` | 'The gateway refuses a request for three reasons' in `source_a.md` -- Source A states this directly. |
| 53 | Only one of the gateway's three refusal reasons is the cap. | supported | `source_b.md` | 'only one of them is a cap' in `source_b.md` -- Source B states that only one of the three reasons is a cap. |
| 54 | A credential may be suspended. | supported | `source_a.md` | 'A credential may be suspended' in `source_a.md` -- Source A states this directly. |
| 55 | A route may be closed for maintenance. | supported | `source_a.md` | 'a route may be closed for maintenance' in `source_a.md` -- Source A states this directly. |
| 56 | The request body limit is 5 megabyte. | supported | `source_a.md` | 'the 5 megabyte limit' in `source_a.md` -- Source A states that the body limit is 5 megabytes. |
| 57 | A body exceeding the 5 megabyte limit is refused before it has been read at all. | supported | `source_b.md` | 'a request body over the 5 megabyte limit is refused before it has been read at all' in `source_b.md` -- Source B states this directly. |
| 58 | A suspended credential, a route closed for maintenance and an oversized body do not clear by waiting for a stated number of seconds. | supported | `source_a.md` | 'None of those three clears itself by waiting for a stated number of seconds.' in `source_a.md` -- Source A states that none of the three clears by waiting. |
| 59 | A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service. | supported | `source_a.md` | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `source_a.md` -- Source A states this verbatim. |
| 60 | Distinguishing the refusal cases by reading the status code costs one comparison. | supported | `source_a.md` | 'Reading the status code rather than the class it belongs to is what separates the two cases, and it costs one comparison.' in `source_a.md` -- Source A states that reading the status code separates the cases at the cost of one comparison. |
| 61 | A cap can be raised. | supported | `source_a.md` | 'A cap can be raised' in `source_a.md` -- Source A states this directly. |
| 62 | The number of caps raised without a measurement behind them is 0. | supported | `source_a.md` | 'the number of caps raised without a measurement behind them is 0' in `source_a.md` -- Source A states this directly. |
| 63 | A cap increase request should include the refusal counts for a full week, the shape of the traffic across the day, and the deadline that traffic is serving. | supported | `source_b.md` | 'Bring the refusal counts for a full week, the shape of the traffic across the day, and the deadline the traffic exists to meet.' in `source_b.md` -- Source B lists the same three items, and Source A matches. |
| 64 | The platform team looks at whether the load is smooth or bursty before it looks at the number. | supported | `source_b.md` | 'The team wants to know whether the load is smooth or bursty before it looks at the number at all.' in `source_b.md` -- Source B states this directly. |
| 65 | A burst is cheaper to smooth out than to serve at its peak. | supported | `source_b.md` | 'A burst is cheaper to smooth out than it is to serve at its peak.' in `source_b.md` -- Source B states this directly. |
| 66 | A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap. | supported | `source_a.md` | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `source_a.md` -- Source A states this directly. |
| 67 | Requests for a cap increase reach the platform team through the usual channel. | supported | `source_b.md` | 'Requests go to the platform team through the usual channel.' in `source_b.md` -- Source B states that requests go through the usual channel. |
| 68 | Requests for a cap increase are answered within two working days. | supported | `source_a.md` | 'they are answered within two working days' in `source_a.md` -- Source A states the two-working-day answer time. |
| 69 | There is no expedited path for cap increase requests. | supported | `source_a.md` | 'There is no expedited path' in `source_a.md` -- Both sources state that there is no expedited path. |
| 70 | There is no exception list for cap increase requests. | supported | `source_a.md` | 'There is no expedited path and no exception list.' in `source_a.md` -- Source A states that there is no exception list. |
| 71 | Chasing an answer to a cap increase request does not make it arrive any sooner. | supported | `source_b.md` | 'chasing it doesn’t make it take fewer' in `source_b.md` -- Source B states that chasing the answer does not make it arrive sooner. |

## Structure

**9** mechanical check(s) over **104** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **71** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **135**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 25 run(s) over 48 attributed segment(s) — sources interleaved. 6 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Declared gone, still here — a record says the content departed and the merge carries the segment unchanged

- `a13` (`source_a.md`) — 'Its value is a whole number of seconds to wait.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Its value is a whole number of seconds to wait.
  In the merge:  Every refusal carries a Retry-After header, and its value is a whole number of seconds to wait.
  ```
- `a25` (`source_a.md`) — 'There is no case at all where a guess is the better of the two.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: There is no case at all where a guess is the better of the two.
  In the merge:  A wait derived on the client side is a guess about a counter it cannot see, and there is no case at all where a guess is the better of the two.
  ```

### Verbatim violation — an invariant-core token did not survive unchanged

- `b31` (`source_b.md`) — numeric '50' (times) does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **85** departure(s) from its sources. Checking them confirms 70, rejects 2, and leaves 13 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 104 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | Base title kept. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Rate limiting and the 429 contract for gateway clients' and says so (no claim traced to it) |
| `a2` | reworded | Opening line takes b2's 'own' phrasing. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-001`) |
| `b2` | subsumed | Same opening fact, stated once. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-001`) |
| `a3` | reworded | Dashes replaced with commas. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-002`, `A-003`, `A-004`) |
| `b3` | duplicate | Same edge-refusal fact as a3. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-002`, `B-003`) |
| `b4` | reworded | Token-bucket rationale kept, header named. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a4` | subsumed | Counting rule merged with b5's undisclosed window start. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-005`, `A-006`, `A-007`) |
| `b5` | subsumed | Undisclosed start added to a4's counting rule. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-004`, `B-005`, `B-006`) |
| `a5` | reworded | Sockets point joined with b7's across-hosts detail. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-008`) |
| `b6` | duplicate | Same sockets point as a5. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-007`) |
| `b7` | subsumed | Across-hosts detail carried in the sockets sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-008`) |
| `a6` | reconciled | Eight-process example combined with b8's general case. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-009`) |
| `b8` | reconciled | General case combined with a6's eight-process example. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-009`) |
| `a7` | reworded | Allowances split around b9's interactive-use note. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-010`, `A-011`) |
| `b9` | subsumed | Interactive-use note attached to the default allowance. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-010`, `B-011`, `B-012`) |
| `a8` | reworded | b10's not-a-bug point added. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-012`) |
| `b10` | subsumed | Carried by a8 and a9 together. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-013`, `B-014`, `B-015`) |
| `b11` | duplicate | Same point as a10. | **rejected** | declared 'duplicate', which predicts SUPPORTED; B-016 came back PARTIAL (`B-016`) |
| `b12` | duplicate | Identical heading. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `a12` | subsumed | Header fact merged with its value and b14's every-refusal. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-016`) |
| `a13` | subsumed | Value merged into header sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-017`) |
| `b13` | duplicate | Header name already carried. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-017`) |
| `b14` | subsumed | Present-on-every-refusal carried by 'Every refusal'. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-018`, `B-019`) |
| `a14` | reworded | Contract sentence merged with b15's aside. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-018`) |
| `b15` | subsumed | Aside carried in merged contract sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-020`) |
| `a15` | reworded | Tightened wording. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-019`, `A-020`) |
| `b16` | duplicate | Same point as a15. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-021`, `B-022`) |
| `a16` | subsumed | Body fields merged into one sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-021`, `A-022`) |
| `a17` | subsumed | Cap and tier listed with the window. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-023`, `A-024`) |
| `b17` | subsumed | Plain-fields detail carried. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-023`, `B-024`) |
| `a18` | reworded | Joined with b18's consequence. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-025`) |
| `b18` | subsumed | Consequence carried in merged sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-025`) |
| `a19` | reworded | Dash replaced with semicolon. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-026`, `A-027`) |
| `b19` | duplicate | Same point as a19. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-026`) |
| `b20` | superseded | Base heading kept for the retry rules. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a21` | superseded | b21's full sentence used for the rules intro. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a22` | subsumed | Rule 1 heading merged with b22. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b22` | subsumed | Rule 1 heading merged with a22. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-029`) |
| `a23` | subsumed | Merged with b24's different-cause detail. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-028`, `A-029`) |
| `b23` | duplicate | Same point as a23. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-030`) |
| `b24` | subsumed | 503 detail carried in merged sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-031`, `B-032`) |
| `a24` | subsumed | Joined with a25. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a25` | subsumed | Joined with a24. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b25` | duplicate | Same point as a24. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-033`) |
| `b26` | subsumed | Carried by a25's stronger statement. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a26` | subsumed | Rule 2 heading merged with b27. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b27` | subsumed | Rule 2 heading merged with a26. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-034`, `B-035`) |
| `a27` | reworded | Adds b28's platform-overloaded gloss. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-030`, `A-031`, `A-032`, `A-033`) |
| `b28` | subsumed | Same four cases, stated once. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-036`, `B-037`, `B-038`, `B-039`) |
| `b29` | duplicate | Same point as a29. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-040`) |
| `b30` | duplicate | Same instruction as a30. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `a32` | superseded | 'Fifty times' conflicts with 100/1000; explicit 1000 kept, window kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`A-035`, `A-036`) |
| `b31` | superseded | 1000 carried in intro; '50 times' conflicts and was not kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-041`, `B-042`, `B-043`) |
| `a34` | reworded | Redundant 'in any way' removed. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-039`) |
| `b33` | duplicate | Same point as a34. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-046`) |
| `a35` | subsumed | Rule 4 heading merged with b34's retention. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b34` | subsumed | Retention period carried in rule 4. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-047`, `B-048`) |
| `b35` | duplicate | Same point as a36. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-049`, `B-050`) |
| `b37` | superseded | Base heading kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a39` | reworded | Subject made explicit. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a40` | subsumed | Merged with b39. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-042`, `A-043`) |
| `b38` | duplicate | Same point as a40. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-051`, `B-052`) |
| `b39` | subsumed | Carried in merged sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-053`) |
| `a41` | subsumed | Merged with b40's refused-before-read detail. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-044`, `A-045`, `A-046`) |
| `b40` | subsumed | Repair/maintenance same; unread-body detail kept. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-054`, `B-055`, `B-056`, `B-057`) |
| `a43` | subsumed | b41's fuller comparison used. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b41` | reworded | 'Difference' changed to base's 'distinction'. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a44` | subsumed | Merged with b43. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-048`) |
| `b42` | duplicate | Same point as a44. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-058`) |
| `b43` | subsumed | Outage-lookalike and own-budget details carried. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-059`, `B-060`, `B-061`) |
| `a47` | subsumed | Merged with b46. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-051`, `A-052`) |
| `b46` | subsumed | Moved to the increase section and merged with a47. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-065`, `B-066`) |
| `a48` | reworded | Uses b47's 'full week' phrasing. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-053`) |
| `b47` | subsumed | Same list as a48. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-067`, `B-068`, `B-069`) |
| `a49` | subsumed | Merged with b48's ordering detail. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-054`, `A-055`) |
| `b48` | subsumed | Before-the-number detail carried. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-070`) |
| `b49` | duplicate | Same point as a49. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-071`) |
| `a50` | subsumed | Merged with b45. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-056`) |
| `b44` | duplicate | Same point as a50. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-062`) |
| `b45` | subsumed | Carried with a50's closing clause. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-063`, `B-064`) |
| `a51` | reworded | Tightened wording. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-057`, `A-058`) |
| `b50` | duplicate | Same channel fact as a51. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-072`) |
| `b52` | subsumed | Response time and no-chasing point carried. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-074`, `B-075`) |
| `a52` | subsumed | Merged with b52's chasing point. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-059`, `A-060`) |
| `b51` | duplicate | Same point as a52. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-073`) |


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
| Duration | 427.0s |
| Generated | 2026-09-27T18:42:26+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup opus-5.5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
