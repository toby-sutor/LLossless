## Verdict

**4 finding(s).** In the claims: 2 partially dropped, 1 contradicted. In the structure: 1 verbatim violation.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 82 |
| Claims extracted from `source_a.md` | 53 |
| Claims extracted from `source_b.md` | 73 |
| Forward — source claims accounted for in the merge | **123/126** |
| Forward — carried only in part | 2 |
| Forward — `source_a.md` claims accounted for | **52/53** |
| Forward — `source_b.md` claims accounted for | **71/73** (2 in part) |
| Reverse — merge claims found in a source | **82/82** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **208/208** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Partly dropped — the merge carries some of this claim

- **B-040** (`source_b.md:21`) — A caller that folds 200, 429, 500 and 503 into one branch will retry hardest during exactly the incident the cap was installed to survive.
  - evidence: 'A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text states this for folding every non-success into one branch; it does not state it for a branch that also includes 200.
- **B-072** (`source_b.md:37`) — An answer to a cap increase request takes two working days.
  - evidence: 'they are answered within two working days' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The reference text gives two working days as an upper bound; it does not say an answer takes exactly two working days.

### Contradicted — the merge states something different

- **A-037** -- the two documents disagree
  - `source_a.md:29` says: The gateway refuses a request for three reasons besides the cap.
  - `merged.md` says: 'The gateway refuses a request for three reasons and only one of them is the one above' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text says three reasons including the cap, not three besides it.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 53 claim(s): 0 dropped, 1 contradicted, 0 carried in part, 52 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 37 | The gateway refuses a request for three reasons besides the cap. | 29 | contradicted | 'The gateway refuses a request for three reasons and only one of them is the one above' in `merged.md` -- The reference text says three reasons including the cap, not three besides it. |
| 1 | Every credential has a cap. | 3 | carried | 'Every credential has a cap.' in `merged.md` -- The reference text states this verbatim. |
| 2 | When a credential's cap is spent, the gateway answers 429 at the edge without waking the service behind it. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge — without waking the service behind it' in `merged.md` -- The reference text states the 429 at the edge without waking the service. |
| 3 | A 429 refusal costs the platform almost nothing. | 3 | carried | 'the refusal costs the platform almost nothing' in `merged.md` -- The reference text states the refusal costs the platform almost nothing. |
| 4 | Requests are counted against the credential that presented them. | 5 | carried | 'Requests are counted against the credential that presented them' in `merged.md` -- The reference text states this directly. |
| 5 | Requests are counted over a fixed window of 60 seconds. | 5 | carried | 'over a fixed window of 60 seconds' in `merged.md` -- The reference text states the fixed 60-second window. |
| 6 | Requests are never counted against a connection. | 5 | carried | 'never against a connection' in `merged.md` -- The reference text states requests are never counted against a connection. |
| 7 | Opening a second socket buys a caller nothing in terms of rate limit. | 5 | carried | 'so opening a second socket buys a caller nothing' in `merged.md` -- The reference text states a second socket buys a caller nothing. |
| 8 | A client spread across eight worker processes is throttled at exactly the point one process would have been. | 5 | carried | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `merged.md` -- The reference text states this directly. |
| 9 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- The reference text states the default allowance of 100 requests. |
| 10 | A credential marked for batch work is allowed 1000 requests in the same window. | 7 | carried | 'a credential marked for batch work is allowed 1000 in the same window' in `merged.md` -- The reference text states the batch allowance of 1000 in the same window. |
| 11 | A 429 refusal is not an outage. | 7 | carried | 'A refusal is not an outage' in `merged.md` -- The reference text states a refusal is not an outage. |
| 12 | A 429 refusal is the platform declining to spend capacity that has already been promised to somebody else. | 7 | carried | 'It is the platform declining to spend capacity that has already been promised to somebody else' in `merged.md` -- The reference text states this directly. |
| 13 | Callers that retry at once are the largest single reason the cap exists. | 7 | carried | 'Callers that retry at once are the largest single reason the cap is there at all' in `merged.md` -- The reference text states callers retrying at once are the largest single reason for the cap. |
| 14 | The 429 refusal carries a Retry-After header. | 11 | carried | 'The refusal carries a Retry-After header' in `merged.md` -- The reference text states the refusal carries a Retry-After header. |
| 15 | The Retry-After header value is a whole number of seconds to wait. | 11 | carried | 'Its value is a whole number of seconds to wait.' in `merged.md` -- The reference text states the value is a whole number of seconds to wait. |
| 16 | The gateway keeps no memory of who backed off politely. | 11 | carried | 'The gateway keeps no memory of who backed off politely' in `merged.md` -- The reference text states this directly. |
| 17 | Waiting longer than the Retry-After header asks earns a caller no credit. | 11 | carried | 'waiting longer than the header asks earns a caller no credit at all' in `merged.md` -- The reference text states waiting longer earns no credit. |
| 18 | The body of the 429 refusal is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- The reference text states the body is JSON. |
| 19 | The body of the 429 refusal names the window the gateway counted in. | 13 | carried | 'it names the cap, the tier and what the gateway calls the “window” it counted in' in `merged.md` -- The reference text states the body names the window the gateway counted in. |
| 20 | The body of the 429 refusal names the cap. | 13 | carried | 'it names the cap' in `merged.md` -- The reference text states the body names the cap. |
| 21 | The body of the 429 refusal names the tier. | 13 | carried | 'it names the cap, the tier' in `merged.md` -- The reference text states the body names the tier. |
| 22 | The body of the 429 refusal is there so that a human reading a log afterwards can see why the request was refused. | 13 | carried | 'The body is there so that a human reading a log afterwards can see why the request was refused' in `merged.md` -- The reference text states this directly. |
| 23 | Nothing in the body of the 429 refusal is meant for the retry loop. | 13 | carried | 'nothing in it is meant for the retry loop' in `merged.md` -- The reference text states nothing in the body is meant for the retry loop. |
| 24 | The gateway computes the wait with information the caller does not have. | 19 | carried | 'The gateway has already done that arithmetic, with information the caller does not have' in `merged.md` -- The reference text states the gateway computes the wait with information the caller lacks. |
| 25 | The gateway computes the wait on the 503 path as well. | 19 | carried | 'it does the same on the 503 path' in `merged.md` -- The reference text states the gateway does the same arithmetic on the 503 path. |
| 26 | A 200 response wants nothing. | 21 | carried | 'A 200 wants nothing' in `merged.md` -- The reference text states this directly. |
| 27 | A 429 response wants the stated wait. | 21 | carried | 'a 429 wants the stated wait' in `merged.md` -- The reference text states this directly. |
| 28 | A 500 response may be retried once the stated wait has passed. | 21 | carried | 'a 500 may be retried once that wait has passed' in `merged.md` -- The reference text states a 500 may be retried once the wait has passed. |
| 29 | A 503 response is the overload path. | 21 | carried | 'a 503 means the platform itself is overloaded' in `merged.md` -- The reference text ties 503 to platform overload, which is the overload path. |
| 30 | A client that folds every non-success response into one branch will retry hardest during exactly the incident the cap was installed to survive. | 21 | carried | 'A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive.' in `merged.md` -- The reference text states this directly. |
| 31 | A batch credential is allowed fifty times the default allowance. | 23 | carried | 'fifty times the default allowance' in `merged.md` -- The reference text states the batch allowance is fifty times the default. |
| 32 | A batch credential is measured over exactly the same window as the default allowance. | 23 | carried | 'it is measured over exactly the same window' in `merged.md` -- The reference text states batch is measured over exactly the same window. |
| 33 | The tier is set on the credential when it is issued. | 23 | carried | 'The tier is set on the credential when it is issued' in `merged.md` -- The reference text states this directly. |
| 34 | The tier cannot be asked for per call. | 23 | carried | 'cannot be asked for per call' in `merged.md` -- The reference text states the tier cannot be asked for per call. |
| 35 | Nothing else differs between the default and batch tiers. | 23 | carried | 'Nothing else about the two tiers differs in any way.' in `merged.md` -- The reference text states nothing else differs between the tiers. |
| 36 | The log line for a refusal should carry the credential, the window and the wait. | 25 | carried | 'The log line should carry the credential, the window and the wait.' in `merged.md` -- The reference text states this directly. |
| 38 | The gateway refuses a request for three reasons, only one of which is the cap. | 29 | carried | 'The gateway refuses a request for three reasons and only one of them is the one above' in `merged.md` -- The reference text states three reasons, one of which is the cap. |
| 39 | A credential may be suspended. | 29 | carried | 'A credential may be suspended' in `merged.md` -- The reference text states this directly. |
| 40 | A route may be closed for maintenance. | 29 | carried | 'a route may be closed for maintenance' in `merged.md` -- The reference text states this directly. |
| 41 | The request body limit is 5 megabyte. | 29 | carried | 'a body may exceed the 5 megabyte limit' in `merged.md` -- The reference text states a 5 megabyte body limit. |
| 42 | None of the three non-cap refusal conditions (suspended credential, route closed for maintenance, body over the 5 megabyte limit) clears itself by waiting for a stated number of seconds. | 29 | carried | 'None of those three clears itself by waiting for a stated number of seconds.' in `merged.md` -- The reference text states none of the three non-cap conditions clears by waiting. |
| 43 | A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `merged.md` -- The reference text states this directly. |
| 44 | Reading the status code rather than its class costs one comparison. | 31 | carried | 'Reading the status code rather than the class it belongs to is what separates the two cases, and it costs one comparison.' in `merged.md` -- The reference text states reading the status code costs one comparison. |
| 45 | A cap can be raised. | 35 | carried | 'A cap can be raised' in `merged.md` -- The reference text states this directly. |
| 46 | The number of caps raised without a measurement behind them is 0. | 35 | carried | 'the number of caps raised without a measurement behind them is 0' in `merged.md` -- The reference text states this directly. |
| 47 | The platform team looks at whether the load is smooth or bursty when considering a cap increase. | 35 | carried | 'The platform team looks at whether the load is smooth or bursty before it looks at the number at all' in `merged.md` -- The reference text states the team looks at smooth versus bursty load in considering increases. |
| 48 | A burst is cheaper to smooth than it is to serve at its peak. | 35 | carried | 'a burst is cheaper to smooth than it is to serve at its peak' in `merged.md` -- The reference text states this directly. |
| 49 | A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap. | 35 | carried | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `merged.md` -- The reference text states this directly. |
| 50 | Cap increase requests reach the platform team through the usual channel. | 37 | carried | 'Requests reach the platform team through the usual channel' in `merged.md` -- The reference text states this directly. |
| 51 | Cap increase requests are answered within two working days. | 37 | carried | 'they are answered within two working days' in `merged.md` -- The reference text states requests are answered within two working days. |
| 52 | There is no expedited path for cap increase requests. | 37 | carried | 'There is no expedited path' in `merged.md` -- The reference text states there is no expedited path. |
| 53 | There is no exception list for cap increase requests. | 37 | carried | 'no exception list' in `merged.md` -- The reference text states there is no exception list. |

### `source_b.md` -- 73 claim(s): 0 dropped, 0 contradicted, 2 carried in part, 71 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 40 | A caller that folds 200, 429, 500 and 503 into one branch will retry hardest during exactly the incident the cap was installed to survive. | 21 | carried in part | 'A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive.' in `merged.md` -- The text states this for folding every non-success into one branch; it does not state it for a branch that also includes 200. |
| 72 | An answer to a cap increase request takes two working days. | 37 | carried in part | 'they are answered within two working days' in `merged.md` -- The reference text gives two working days as an upper bound; it does not say an answer takes exactly two working days. |
| 1 | Every credential has a cap of its own. | 3 | carried | 'Every credential has a cap.' in `merged.md` -- Each credential having a cap, counted against that credential, means each has its own cap. |
| 2 | When the cap is spent the gateway answers 429 at the edge. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge' in `merged.md` -- The reference text states this directly. |
| 3 | When the cap is spent, the gateway's 429 response does not involve the service behind the gateway. | 3 | carried | 'without waking the service behind it' in `merged.md` -- The reference text states the 429 is given without waking the service behind the gateway. |
| 4 | Requests are counted against the credential rather than the connection. | 5 | carried | 'Requests are counted against the credential that presented them, never against a connection' in `merged.md` -- The reference text states counting is per credential, never per connection. |
| 5 | Requests are counted over a fixed window of 60 seconds. | 5 | carried | 'over a fixed window of 60 seconds' in `merged.md` -- The reference text states the fixed 60-second window. |
| 6 | The gateway doesn't disclose the start of the 60-second counting window. | 5 | carried | 'whose start the gateway does not disclose' in `merged.md` -- The reference text states the gateway does not disclose the window start. |
| 7 | Opening more sockets gains nothing against the rate limit. | 5 | carried | 'so opening a second socket buys a caller nothing' in `merged.md` -- Since counting follows the credential, opening more sockets gains nothing, as the text states for a second socket. |
| 8 | The request count follows the credential wherever the caller puts it, including across hosts. | 5 | carried | 'The count follows the credential wherever the caller puts it, including across hosts' in `merged.md` -- The reference text states this directly. |
| 9 | A caller spread over many worker processes is throttled at the same point a single process would have been. | 5 | carried | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `merged.md` -- The text states this for eight processes, and credential-based counting entails it for many processes. |
| 10 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- The reference text states this directly. |
| 11 | The default allowance of 100 requests is enough for every interactive use of the API the platform team has seen. | 7 | carried | 'The default is enough for every interactive use of this API the platform team has seen' in `merged.md` -- The reference text states this directly. |
| 12 | A caller that needs more than 100 requests in a window is almost always doing batch work under an interactive credential. | 7 | carried | 'a caller that needs more than that is almost always doing batch work under an interactive credential' in `merged.md` -- The reference text states this directly. |
| 13 | A 429 refusal is not an outage. | 7 | carried | 'A refusal is not an outage' in `merged.md` -- The reference text states this directly. |
| 14 | A 429 refusal is not a bug in the gateway. | 7 | carried | 'A refusal is not an outage and not a bug in the gateway' in `merged.md` -- The reference text states a refusal is not a bug in the gateway. |
| 15 | A 429 refusal is capacity being held for a request somebody else has already been promised. | 7 | carried | 'It is the platform declining to spend capacity that has already been promised to somebody else' in `merged.md` -- The reference text states the same meaning in different words. |
| 16 | Callers that retry immediately are most of the reason the cap exists. | 7 | carried | 'Callers that retry at once are the largest single reason the cap is there at all, accounting for most of it.' in `merged.md` -- The reference text states immediate retriers account for most of the reason for the cap. |
| 17 | The refusal header is called Retry-After. | 11 | carried | 'The refusal carries a Retry-After header' in `merged.md` -- The reference text names the header Retry-After. |
| 18 | The Retry-After value is a whole number of seconds. | 11 | carried | 'Its value is a whole number of seconds to wait.' in `merged.md` -- The reference text states the value is a whole number of seconds. |
| 19 | The Retry-After header is present on every refusal the gateway sends. | 11 | carried | 'present on every refusal the gateway sends' in `merged.md` -- The reference text states this directly. |
| 20 | Waiting the Retry-After duration and then continuing is the entire contract. | 11 | carried | 'Waiting that long and then continuing is the whole of the contract' in `merged.md` -- The reference text states this directly. |
| 21 | Waiting longer than the Retry-After header asks earns nothing. | 11 | carried | 'waiting longer than the header asks earns a caller no credit at all' in `merged.md` -- The reference text states waiting longer earns no credit. |
| 22 | Nobody at the gateway end is keeping score of how long callers wait. | 11 | carried | 'The gateway keeps no memory of who backed off politely' in `merged.md` -- Keeping no memory of polite back-off means nobody is keeping score of waits. |
| 23 | The refusal response body is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- The reference text states this directly. |
| 24 | The refusal response body repeats the cap, the window and the tier as plain fields. | 13 | carried | 'it names the cap, the tier and what the gateway calls the “window” it counted in, as plain fields' in `merged.md` -- The reference text states the body names the cap, tier and window as plain fields. |
| 25 | None of the response body fields is a substitute for the Retry-After header. | 13 | carried | 'None of those fields is a substitute for the header' in `merged.md` -- The reference text states this directly. |
| 26 | The refusal response body is for the human reading the log afterwards. | 13 | carried | 'The body is there so that a human reading a log afterwards can see why the request was refused' in `merged.md` -- The reference text states the body is for a human reading the log. |
| 27 | There are four rules for the client. | 17 | carried | 'Four rules, given in the order they should be applied.' in `merged.md` -- The reference text states there are four rules. |
| 28 | The four client rules are to be applied in the order they are given. | 17 | carried | 'Four rules, given in the order they should be applied.' in `merged.md` -- The reference text states the rules are given in the order they should be applied. |
| 29 | The client should honour the Retry-After header and not compute its own wait. | 19 | carried | 'Honour the header, every time, and do not compute your own wait.' in `merged.md` -- The reference text states this directly. |
| 30 | The gateway computes the wait using information the caller cannot see. | 19 | carried | 'The gateway has already done that arithmetic, with information the caller does not have' in `merged.md` -- The reference text states the same meaning. |
| 31 | On the 503 path, the rule to honour the header and not compute your own wait also holds. | 19 | carried | 'it does the same on the 503 path' in `merged.md` -- The gateway computing the wait on the 503 path means the honour-the-header rule holds there too. |
| 32 | The cause of a 503 refusal is different from the cause of a 429 refusal. | 19 | carried | 'even though the cause of that refusal is an entirely different one' in `merged.md` -- The reference text states the 503 cause is entirely different. |
| 33 | Any wait computed on the client side is a guess. | 19 | carried | 'A wait derived on the client side is a guess about a counter it cannot see.' in `merged.md` -- The reference text states a client-side wait is a guess. |
| 34 | The client should retry only what is safe to retry. | 21 | carried | 'Retry only what is safe to retry' in `merged.md` -- The reference text states this directly. |
| 35 | The set of responses safe to retry is smaller than the set of non-success responses. | 21 | carried | 'which is a smaller set than the set of responses that are not a success' in `merged.md` -- The reference text states this directly. |
| 36 | A 200 response needs nothing. | 21 | carried | 'A 200 wants nothing' in `merged.md` -- The reference text states the same meaning. |
| 37 | A 429 response needs the stated wait. | 21 | carried | 'a 429 wants the stated wait' in `merged.md` -- The reference text states the same meaning. |
| 38 | A 500 response can be retried once the stated wait has passed. | 21 | carried | 'a 500 may be retried once that wait has passed' in `merged.md` -- The reference text states the same meaning. |
| 39 | A 503 response means the platform itself is overloaded. | 21 | carried | 'a 503 means the platform itself is overloaded' in `merged.md` -- The reference text states this directly. |
| 41 | A batch credential is allowed 1000 requests in a window. | 23 | carried | 'A batch credential is allowed 1000 requests in a window' in `merged.md` -- The reference text states this directly. |
| 42 | The batch allowance of 1000 requests is 50 times the default. | 23 | carried | 'fifty times the default allowance' in `merged.md` -- The reference text states the batch allowance of 1000 is fifty times the default. |
| 43 | The batch allowance is not a separate counting scheme. | 23 | carried | 'rather than a separate counting scheme' in `merged.md` -- The reference text states batch is not a separate counting scheme. |
| 44 | The window, the header and the body for the batch tier are identical to the interactive case. | 23 | carried | 'it is measured over exactly the same window with the same header and the same body' in `merged.md` -- The reference text states the window, header and body are the same. |
| 45 | A client written for one tier needs no change to run against the other tier. | 23 | carried | 'a client written for one tier needs no change at all to run against the other' in `merged.md` -- The reference text states this directly. |
| 46 | Nothing else about the batch tier differs from the default. | 23 | carried | 'Nothing else about the two tiers differs in any way.' in `merged.md` -- The reference text states nothing else differs between the tiers. |
| 47 | The client should log every refusal it sees. | 25 | carried | 'Log every refusal seen' in `merged.md` -- The reference text states the client should log every refusal seen. |
| 48 | The client should keep the refusal log for at least a week. | 25 | carried | 'Log every refusal seen, and keep the log for at least a week.' in `merged.md` -- The reference text directly instructs keeping the refusal log for at least a week. |
| 49 | A caller that cannot say how often it was refused can't make a case for a larger cap. | 25 | carried | 'A caller that cannot say how often it was refused last week cannot argue for a larger cap' in `merged.md` -- The reference text states that a caller unable to report its refusal frequency cannot argue for a larger cap. |
| 50 | The platform team won't assemble the case for a larger cap on a caller's behalf. | 25 | carried | 'nobody at the far end will assemble that argument on its behalf' in `merged.md` -- The reference text says nobody at the far end, meaning the platform side, will assemble the argument for the caller. |
| 51 | The gateway refuses a request for three separate reasons. | 29 | carried | 'The gateway refuses a request for three reasons' in `merged.md` -- The reference text states that the gateway refuses requests for three reasons. |
| 52 | Only one of the gateway's three refusal reasons is a cap. | 29 | carried | 'only one of them is the one above' in `merged.md` -- The reference text says only one of the three reasons is the cap described above, under the heading noting not all refusals are caps. |
| 53 | Two of the three refusal reasons have nothing to do with how much traffic a caller has sent in the current window. | 29 | carried | 'the other two have nothing to do with how much traffic a caller has sent in the window it is currently in' in `merged.md` -- The reference text states that the other two reasons are unrelated to traffic sent in the current window. |
| 54 | A credential can be suspended. | 29 | carried | 'A credential may be suspended' in `merged.md` -- The reference text states that a credential may be suspended. |
| 55 | A route can be closed while it is being repaired. | 29 | carried | 'a route may be closed for maintenance' in `merged.md` -- Being closed for maintenance has the same meaning as being closed while it is repaired. |
| 56 | The request body limit is 5 megabyte. | 29 | carried | 'a body may exceed the 5 megabyte limit' in `merged.md` -- The reference text gives the body limit as 5 megabyte. |
| 57 | A request body over the 5 megabyte limit is refused before it has been read at all. | 29 | carried | 'a body may exceed the 5 megabyte limit, in which case it is refused before it has been read at all' in `merged.md` -- The reference text states that an oversized body is refused before it has been read at all. |
| 58 | A loop retrying against a suspended credential burns its whole budget and reaches nothing. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `merged.md` -- The reference text states the loop spends its whole budget without ever reaching the service. |
| 59 | The log after retrying against a suspended credential shows a long run of refusals and no successes. | 31 | carried | 'the log afterwards shows nothing at all except a long run of refusals' in `merged.md` -- The reference text says the log shows nothing except a long run of refusals, which entails that it shows no successes. |
| 60 | Retrying against a suspended credential is not an outage. | 31 | carried | 'which reads like an outage and is not one' in `merged.md` -- The reference text states the situation reads like an outage but is not one. |
| 61 | The budget wasted retrying against a suspended credential is the caller's own. | 31 | carried | "the wasted budget is the caller's own" in `merged.md` -- The reference text states the wasted budget is the caller's own. |
| 62 | A caller that can move half its work to a quieter hour usually finds it doesn't need a larger cap. | 33 | carried | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `merged.md` -- The reference text says such a caller usually gets what it needs without a cap change. |
| 63 | A cap can be raised. | 33 | carried | 'A cap can be raised' in `merged.md` -- The reference text states that a cap can be raised. |
| 64 | A cap will not be raised on the strength of an assertion that the current one is too small. | 33 | carried | 'but not on the strength of an assertion that the current one is too small' in `merged.md` -- The reference text states a cap is not raised on the strength of an assertion that the current one is too small. |
| 65 | A request for a larger cap should include the refusal counts for a full week. | 33 | carried | 'Bring a week of refusal counts' in `merged.md` -- The reference text asks for a week of refusal counts with an increase request. |
| 66 | A request for a larger cap should include the shape of the traffic across the day. | 33 | carried | 'the shape of the traffic across the day' in `merged.md` -- The reference text lists the shape of the traffic across the day among the items to bring. |
| 67 | A request for a larger cap should include the deadline the traffic exists to meet. | 33 | carried | 'the deadline that traffic is serving' in `merged.md` -- The reference text lists the deadline the traffic is serving among the items to bring. |
| 68 | The platform team wants to know whether the load is smooth or bursty before it looks at the requested number. | 35 | carried | 'The platform team looks at whether the load is smooth or bursty before it looks at the number at all' in `merged.md` -- The reference text states the team checks whether the load is smooth or bursty before looking at the number. |
| 69 | A burst is cheaper to smooth out than to serve at its peak. | 35 | carried | 'a burst is cheaper to smooth than it is to serve at its peak' in `merged.md` -- The reference text states that a burst is cheaper to smooth than to serve at its peak. |
| 70 | Cap increase requests go to the platform team through the usual channel. | 35 | carried | 'Requests reach the platform team through the usual channel' in `merged.md` -- The reference text states that requests reach the platform team through the usual channel. |
| 71 | There is no expedited path for cap increase requests. | 37 | carried | 'There is no expedited path' in `merged.md` -- The reference text states there is no expedited path. |
| 73 | Chasing a cap increase request doesn't make the answer take fewer than two working days. | 37 | carried | 'chasing an answer does not make it take fewer' in `merged.md` -- The reference text states that chasing does not make the answer take fewer than the two working days just mentioned. |

### `merged.md` -- 82 claim(s): 0 invented, 0 contradicted, 0 supported in part, 82 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Every credential has a cap. | supported | `source_a.md` | 'Every credential has a cap.' in `source_a.md` -- Source A states this verbatim. |
| 2 | When a credential's cap is spent, the gateway answers 429 at the edge. | supported | `source_a.md` | 'When that cap is spent the gateway answers 429 at the edge' in `source_a.md` -- Source A states the gateway answers 429 at the edge when the cap is spent. |
| 3 | When a credential's cap is spent, the gateway answers 429 without waking the service behind it. | supported | `source_a.md` | 'without waking the service behind it' in `source_a.md` -- Source A states the 429 is answered without waking the service behind it. |
| 4 | A 429 refusal at the gateway edge costs the platform almost nothing. | supported | `source_a.md` | 'the refusal costs the platform almost nothing' in `source_a.md` -- Source A states the refusal costs the platform almost nothing. |
| 5 | Requests are counted against the credential that presented them. | supported | `source_a.md` | 'Requests are counted against the credential that presented them' in `source_a.md` -- Source A states this directly. |
| 6 | Requests are never counted against a connection. | supported | `source_a.md` | 'never against a connection' in `source_a.md` -- Source A states requests are never counted against a connection. |
| 7 | Requests are counted over a fixed window of 60 seconds. | supported | `source_a.md` | 'over a fixed window of 60 seconds' in `source_a.md` -- Source A states the fixed 60-second window. |
| 8 | The gateway does not disclose the start of the 60-second counting window. | supported | `source_b.md` | 'over a fixed window of 60 seconds whose start the gateway doesn’t disclose' in `source_b.md` -- Source B states the gateway does not disclose the window's start. |
| 9 | The request count follows the credential across hosts. | supported | `source_b.md` | 'The count follows the credential wherever the caller happens to put it, including across hosts.' in `source_b.md` -- Source B states the count follows the credential across hosts. |
| 10 | Opening a second socket does not increase a caller's allowance. | supported | `source_a.md` | 'Opening a second socket therefore buys a caller nothing.' in `source_a.md` -- Source A states a second socket buys the caller nothing, which means the same. |
| 11 | A client spread across eight worker processes is throttled at exactly the point one process would have been. | supported | `source_a.md` | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `source_a.md` -- Source A states this directly. |
| 12 | The default allowance is 100 requests in a window. | supported | `source_a.md` | 'The default allowance is 100 requests in a window' in `source_a.md` -- Both sources state the default allowance of 100 requests per window. |
| 13 | A credential marked for batch work is allowed 1000 requests in the same window. | supported | `source_a.md` | 'a credential marked for batch work is allowed 1000 in the same window' in `source_a.md` -- Source A states this directly. |
| 14 | The default allowance is enough for every interactive use of the API the platform team has seen. | supported | `source_b.md` | 'which is enough for every interactive use of this API the platform team has seen' in `source_b.md` -- Source B states the default allowance suffices for every interactive use seen. |
| 15 | A caller that needs more than the default allowance is almost always doing batch work under an interactive credential. | supported | `source_b.md` | 'a caller that needs more than that is almost always doing batch work under an interactive credential' in `source_b.md` -- Source B states this directly. |
| 16 | A 429 refusal is not an outage. | supported | `source_a.md` | 'A refusal is not an outage' in `source_a.md` -- Source A states a refusal is not an outage. |
| 17 | A 429 refusal is not a bug in the gateway. | supported | `source_b.md` | 'The refusal isn’t an outage and it isn’t a bug in the gateway' in `source_b.md` -- Source B states the refusal is not a bug in the gateway. |
| 18 | A 429 refusal is the platform declining to spend capacity that has already been promised to somebody else. | supported | `source_a.md` | 'It is the platform declining to spend capacity that has already been promised to somebody else' in `source_a.md` -- Source A states this directly. |
| 19 | Callers that retry at once are the largest single reason the cap exists. | supported | `source_a.md` | 'Callers that retry at once are the largest single reason the cap is there at all.' in `source_a.md` -- Source A states immediate retriers are the largest single reason for the cap. |
| 20 | Callers that retry at once account for most of the reason the cap exists. | supported | `source_b.md` | 'Callers that retry immediately are most of the reason the cap is there.' in `source_b.md` -- Source B states immediate retriers are most of the reason for the cap. |
| 21 | The 429 refusal carries a Retry-After header. | supported | `source_a.md` | 'The refusal carries a Retry-After header.' in `source_a.md` -- Source A states this verbatim. |
| 22 | The Retry-After header is present on every refusal the gateway sends. | supported | `source_b.md` | 'it is present on every refusal the gateway sends' in `source_b.md` -- Source B states the header is present on every refusal. |
| 23 | The Retry-After header value is a whole number of seconds to wait. | supported | `source_a.md` | 'Its value is a whole number of seconds to wait.' in `source_a.md` -- Source A states this verbatim. |
| 24 | Waiting the Retry-After duration and then continuing is the whole of the contract. | supported | `source_a.md` | 'Waiting that long and then continuing is the whole of the contract' in `source_a.md` -- Source A states this directly. |
| 25 | The gateway keeps no memory of who backed off politely. | supported | `source_a.md` | 'The gateway keeps no memory of who backed off politely' in `source_a.md` -- Source A states this directly. |
| 26 | Waiting longer than the Retry-After header asks earns a caller no credit. | supported | `source_a.md` | 'waiting longer than the header asks earns a caller no credit at all' in `source_a.md` -- Source A states this directly. |
| 27 | The body of the 429 refusal is JSON. | supported | `source_a.md` | 'The body of the refusal is JSON' in `source_a.md` -- Source A states the refusal body is JSON. |
| 28 | The body of the 429 refusal names the cap, the tier and the window as plain fields. | supported | `source_b.md` | 'it repeats the cap, the window and the tier as plain fields' in `source_b.md` -- Source B states the body carries the cap, window and tier as plain fields. |
| 29 | None of the refusal body fields is a substitute for the Retry-After header. | supported | `source_a.md` | 'None of those fields is a substitute for the header' in `source_a.md` -- Both sources state this directly. |
| 30 | The refusal body exists so that a human reading a log afterwards can see why the request was refused. | supported | `source_a.md` | 'The body is there so that a human reading a log afterwards can see why the request was refused' in `source_a.md` -- Source A states this directly. |
| 31 | Nothing in the refusal body is meant for the retry loop. | supported | `source_a.md` | 'nothing in it is meant for the retry loop' in `source_a.md` -- Source A states this directly. |
| 32 | There are four rules for retrying well. | supported | `source_a.md` | 'Four rules, given in the order they should be applied.' in `source_a.md` -- Source A states there are four rules for retrying. |
| 33 | Clients should honour the Retry-After header every time and not compute their own wait. | supported | `source_b.md` | 'Honour the header and don’t compute your own wait.' in `source_b.md` -- Source B states this directly; Source A adds every time. |
| 34 | The gateway computes the wait with information the caller does not have. | supported | `source_a.md` | 'The gateway has already done that arithmetic, with information the caller does not have' in `source_a.md` -- Source A states this directly. |
| 35 | The gateway also computes the wait on the 503 path. | supported | `source_a.md` | 'it does the same on the 503 path' in `source_a.md` -- Source A states the gateway does the same arithmetic on the 503 path. |
| 36 | The cause of a 503 refusal is different from the cause of a 429 refusal. | supported | `source_b.md` | 'even though the cause of the refusal is an entirely different one' in `source_b.md` -- Source B states the 503 refusal has an entirely different cause. |
| 37 | A wait derived on the client side is a guess about a counter the client cannot see. | supported | `source_a.md` | 'A wait derived on the client side is a guess about a counter it cannot see.' in `source_a.md` -- Source A states this verbatim. |
| 38 | An earlier draft of the document argued for a client-side token bucket that mirrored the gateway's own counters. | supported | `source_b.md` | 'An earlier draft of this note argued for a client-side token bucket that mirrored the gateway’s own counters' in `source_b.md` -- Source B states this directly. |
| 39 | Clients should retry only what is safe to retry. | supported | `source_a.md` | 'Retry only what is safe to retry.' in `source_a.md` -- Source A states this verbatim. |
| 40 | The set of responses safe to retry is smaller than the set of non-success responses. | supported | `source_b.md` | 'which is a smaller set than the set of responses that aren’t a success' in `source_b.md` -- Source B states the safe-to-retry set is smaller than the non-success set. |
| 41 | A 200 response wants nothing. | supported | `source_a.md` | 'A 200 wants nothing' in `source_a.md` -- Source A states this verbatim. |
| 42 | A 429 response wants the stated wait. | supported | `source_a.md` | 'a 429 wants the stated wait' in `source_a.md` -- Source A states this verbatim. |
| 43 | A 500 response may be retried once the stated wait has passed. | supported | `source_a.md` | 'a 500 may be retried once that wait has passed' in `source_a.md` -- Source A states this verbatim. |
| 44 | A 503 response means the platform itself is overloaded. | supported | `source_b.md` | 'a 503 means the platform itself is overloaded' in `source_b.md` -- Source B states this verbatim. |
| 45 | The 200, 429, 500 and 503 cases are not interchangeable. | supported | `source_a.md` | 'The four cases are not interchangeable.' in `source_a.md` -- Source A states this verbatim. |
| 46 | A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive. | supported | `source_a.md` | 'A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive.' in `source_a.md` -- Source A states this verbatim. |
| 47 | A batch credential is allowed 1000 requests in a window. | supported | `source_b.md` | 'A batch credential is allowed 1000 requests in a window' in `source_b.md` -- Source B states this verbatim. |
| 48 | The batch allowance is fifty times the default allowance. | supported | `source_a.md` | 'A batch credential is allowed fifty times the default allowance' in `source_a.md` -- Source A states the batch allowance is fifty times the default; Source B says 50 times. |
| 49 | The batch allowance is not a separate counting scheme. | supported | `source_b.md` | 'not a separate counting scheme' in `source_b.md` -- Source B states the batch allowance is not a separate counting scheme. |
| 50 | A batch credential is measured over exactly the same window as the default tier. | supported | `source_a.md` | 'it is measured over exactly the same window' in `source_a.md` -- Source A states the batch credential uses exactly the same window. |
| 51 | A batch credential's refusals use the same header and the same body as the default tier. | supported | `source_b.md` | 'The window, the header and the body are identical to the interactive case' in `source_b.md` -- Source B states the header and body are identical across tiers. |
| 52 | A client written for one tier needs no change to run against the other tier. | supported | `source_b.md` | 'a client written for one tier needs no change at all to run against the other' in `source_b.md` -- Source B states this directly. |
| 53 | The tier is set on the credential when it is issued. | supported | `source_a.md` | 'The tier is set on the credential when it is issued' in `source_a.md` -- Source A states this directly. |
| 54 | The tier cannot be asked for per call. | supported | `source_a.md` | 'cannot be asked for per call' in `source_a.md` -- Source A states the tier cannot be requested per call. |
| 55 | Nothing else about the default and batch tiers differs. | supported | `source_a.md` | 'Nothing else about the two tiers differs in any way.' in `source_a.md` -- Source A states this verbatim. |
| 56 | Clients should log every refusal seen. | supported | `source_a.md` | 'Log every refusal seen.' in `source_a.md` -- Source A states this verbatim. |
| 57 | Clients should keep the refusal log for at least a week. | supported | `source_b.md` | 'keep the log for at least a week' in `source_b.md` -- Source B states the log should be kept for at least a week. |
| 58 | Nobody at the far end will assemble the argument for a larger cap on the caller's behalf. | supported | `source_a.md` | 'nobody at the far end will assemble that argument on its behalf' in `source_a.md` -- Source A states this directly. |
| 59 | The refusal log line should carry the credential, the window and the wait. | supported | `source_a.md` | 'The log line should carry the credential, the window and the wait.' in `source_a.md` -- Source A states this verbatim. |
| 60 | Not all gateway refusals are caps. | supported | `source_a.md` | 'Not all are caps.' in `source_a.md` -- Source A states not all refusals are caps. |
| 61 | The gateway refuses a request for three reasons. | supported | `source_a.md` | 'The gateway refuses a request for three reasons' in `source_a.md` -- Source A states this directly. |
| 62 | Only one of the gateway's refusal reasons is the rate cap. | supported | `source_a.md` | 'only one of them is the one above' in `source_a.md` -- Source A states only one of the three reasons is the cap. |
| 63 | A credential may be suspended. | supported | `source_a.md` | 'A credential may be suspended' in `source_a.md` -- Source A states this verbatim. |
| 64 | A route may be closed for maintenance. | supported | `source_a.md` | 'a route may be closed for maintenance' in `source_a.md` -- Source A states this verbatim. |
| 65 | The request body limit is 5 megabytes. | supported | `source_a.md` | 'a body may exceed the 5 megabyte limit' in `source_a.md` -- Source A states the body limit is 5 megabytes. |
| 66 | A body exceeding the 5 megabyte limit is refused before it has been read. | supported | `source_b.md` | 'a request body over the 5 megabyte limit is refused before it has been read at all' in `source_b.md` -- Source B states this directly. |
| 67 | None of the suspended credential, closed route or oversized body refusals clears itself by waiting for a stated number of seconds. | supported | `source_a.md` | 'None of those three clears itself by waiting for a stated number of seconds.' in `source_a.md` -- Source A states this verbatim. |
| 68 | A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service. | supported | `source_a.md` | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `source_a.md` -- Source A states this directly. |
| 69 | The log of a loop retrying against a suspended credential shows only a long run of refusals. | supported | `source_a.md` | 'the log afterwards shows nothing at all except a long run of refusals' in `source_a.md` -- Source A states this directly. |
| 70 | Reading the status code rather than its class separates cap refusals from other refusals. | supported | `source_a.md` | 'Reading the status code rather than the class it belongs to is what separates the two cases' in `source_a.md` -- Source A states this directly. |
| 71 | Reading the status code costs one comparison. | supported | `source_a.md` | 'it costs one comparison' in `source_a.md` -- Source A states this directly. |
| 72 | A cap can be raised. | supported | `source_a.md` | 'A cap can be raised' in `source_a.md` -- Source A states this directly. |
| 73 | The number of caps raised without a measurement behind them is 0. | supported | `source_a.md` | 'the number of caps raised without a measurement behind them is 0' in `source_a.md` -- Source A states this directly. |
| 74 | A request for a cap increase should include a week of refusal counts, the shape of the traffic across the day, and the deadline that traffic is serving. | supported | `source_a.md` | 'Bring a week of refusal counts, the shape of the traffic across the day, and the deadline that traffic is serving.' in `source_a.md` -- Source A states this verbatim. |
| 75 | The platform team looks at whether the load is smooth or bursty before it looks at the number. | supported | `source_b.md` | 'The team wants to know whether the load is smooth or bursty before it looks at the number at all.' in `source_b.md` -- Source B states the team checks smooth versus bursty before looking at the number. |
| 76 | A burst is cheaper to smooth than to serve at its peak. | supported | `source_a.md` | 'a burst is cheaper to smooth than it is to serve at its peak' in `source_a.md` -- Source A states this directly. |
| 77 | A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap. | supported | `source_a.md` | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `source_a.md` -- Source A states this directly. |
| 78 | Cap increase requests reach the platform team through the usual channel. | supported | `source_a.md` | 'Requests reach the platform team through the usual channel' in `source_a.md` -- Source A states this directly. |
| 79 | Cap increase requests are answered within two working days. | supported | `source_a.md` | 'they are answered within two working days' in `source_a.md` -- Source A states this directly. |
| 80 | Chasing an answer to a cap increase request does not make it take fewer days. | supported | `source_b.md` | 'chasing it doesn’t make it take fewer' in `source_b.md` -- Source B states chasing the answer does not make it take fewer days. |
| 81 | There is no expedited path for cap increase requests. | supported | `source_a.md` | 'There is no expedited path' in `source_a.md` -- Both sources state there is no expedited path. |
| 82 | There is no exception list for cap increase requests. | supported | `source_a.md` | 'no exception list' in `source_a.md` -- Source A states there is no exception list. |

## Structure

**9** mechanical check(s) over **104** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **82** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **126**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 21 run(s) over 51 attributed segment(s) — sources interleaved. 6 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Verbatim violation — an invariant-core token did not survive unchanged

- `b31` (`source_b.md`) — numeric '50' (times) does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **74** departure(s) from its sources. Checking them confirms 58, rejects 5, and leaves 11 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 104 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | Base title kept. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Rate limiting and the 429 contract for gateway clients' and says so (no claim traced to it) |
| `b2` | duplicate | Same fact as a2. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-001`) |
| `b3` | duplicate | Same fact as a3. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-002`, `B-003`) |
| `b4` | reworded | Moved to the honour-the-header rule it justifies. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a4` | reconciled | Counting unit and window combined with undisclosed start. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-004`, `A-005`, `A-006`) |
| `b5` | reconciled | Counting unit and window combined with undisclosed start. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-004`, `B-005`, `B-006`) |
| `a5` | reconciled | Socket point combined with count following credential. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-007`) |
| `b7` | reconciled | Socket point combined with count following credential. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-008`) |
| `b6` | duplicate | Same point as a5. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-007`) |
| `b8` | duplicate | Same point as a6. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-009`) |
| `b9` | subsumed | Allowance duplicates a7; interactive-use detail added. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-010`, `B-011`, `B-012`) |
| `a8` | reworded | Not-a-bug point from b10 added. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-011`) |
| `b10` | subsumed | Carried by a8 and a9 wording. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-013`, `B-014`, `B-015`) |
| `a10` | reworded | Extended with b11's 'most of the reason'. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-013`) |
| `b11` | subsumed | Majority point folded into a10. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-016`) |
| `b12` | duplicate | Identical heading to a11. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `a12` | reworded | Extended with b14's presence on every refusal. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-014`) |
| `b13` | duplicate | Header name already given. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-017`) |
| `b14` | subsumed | Unit duplicates a13; presence folded into a12. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-018`, `B-019`) |
| `a14` | reworded | Extended with b15's closing remark. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b15` | subsumed | Folded into a14. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-020`) |
| `b16` | duplicate | Same point as a15. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-021`, `B-022`) |
| `a16` | reworded | Merged with a17 into one sentence. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-018`, `A-019`) |
| `a17` | subsumed | Cap and tier folded into body sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-020`, `A-021`) |
| `b17` | duplicate | Same fields as a16 and a17. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-023`, `B-024`) |
| `a18` | reworded | Extended with b18's consequence. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b18` | subsumed | Folded into a18. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-025`) |
| `b19` | duplicate | Same point as a19. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-026`) |
| `b20` | superseded | Base heading kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b21` | duplicate | Same as a21. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-027`, `B-028`) |
| `a22` | reworded | Extended with b22's instruction. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b22` | subsumed | Folded into a22. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-029`) |
| `a23` | reworded | Extended with b24's different-cause note. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-024`, `A-025`) |
| `b23` | duplicate | Same point as a23. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-030`) |
| `b24` | subsumed | Folded into a23. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-031`, `B-032`) |
| `b25` | duplicate | Same point as a24. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-033`) |
| `b26` | duplicate | Same point as a25. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `a26` | reworded | Extended with b27's qualifier. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b27` | subsumed | Folded into a26. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-034`, `B-035`) |
| `a27` | reworded | b28's clearer 503 wording used. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-026`, `A-027`, `A-028`, `A-029`) |
| `b28` | subsumed | 503 wording carried in a27's sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-036`, `B-037`, `B-038`, `B-039`) |
| `b29` | duplicate | Same as a29. | **rejected** | declared 'duplicate', which predicts SUPPORTED; B-040 came back PARTIAL (`B-040`) |
| `b30` | duplicate | Same point as a30. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `a32` | reconciled | Batch allowance, window, header and body combined. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-031`, `A-032`) |
| `b31` | reconciled | Batch allowance, window, header and body combined. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-041`, `B-042`, `B-043`) |
| `b32` | reconciled | Batch allowance, window, header and body combined. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-044`, `B-045`) |
| `b33` | duplicate | Same point as a34. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-046`) |
| `a35` | reworded | Extended with b34's retention period. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b34` | subsumed | Folded into a35. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-047`, `B-048`) |
| `b35` | duplicate | Same point as a36. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-049`, `B-050`) |
| `b37` | superseded | Base heading kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a40` | reworded | Extended with b39's point. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-037 came back CONTRADICTED (`A-037`) |
| `b38` | duplicate | Same point as a40. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-051`, `B-052`) |
| `b39` | subsumed | Folded into a40. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-053`) |
| `a41` | reworded | Extended with b40's before-read detail. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-039`, `A-040`, `A-041`) |
| `b40` | subsumed | Folded into a41. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-054`, `B-055`, `B-056`, `B-057`) |
| `a43` | reworded | b41's comparison added. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b41` | subsumed | Folded into a43. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a44` | reworded | Extended with b43's outage and budget points. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-043`) |
| `b42` | duplicate | Same point as a44. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-058`) |
| `b43` | subsumed | Folded into a44. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-059`, `B-060`, `B-061`) |
| `a47` | reworded | Combined with b46's condition. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-045`, `A-046`) |
| `b46` | subsumed | Folded into a47. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-063`, `B-064`) |
| `b47` | duplicate | Same list as a48. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-065`, `B-066`, `B-067`) |
| `a49` | reworded | b48's ordering detail added. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-047`, `A-048`) |
| `b48` | subsumed | Folded into a49. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-068`) |
| `b49` | duplicate | Same point as a49. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-069`) |
| `a50` | reworded | Extended with b45's cheapest-fix point. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-049`) |
| `b44` | duplicate | Same point as a50. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-062`) |
| `b45` | subsumed | Folded into a50. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a51` | reworded | Extended with b52's chasing point. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-050`, `A-051`) |
| `b50` | duplicate | Same point as a51. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-070`) |
| `b51` | duplicate | Same point as a52. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-071`) |
| `b52` | subsumed | Folded into a51. | **rejected** | declared 'subsumed', which predicts SUPPORTED; B-072 came back PARTIAL (`B-072`) |


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
| Duration | 376.6s |
| Generated | 2026-09-27T19:26:18+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup opus-5.5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
