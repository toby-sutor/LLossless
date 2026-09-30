## Verdict

**31 finding(s).** In the claims: 6 dropped, 2 partially dropped, 2 contradicted. In the structure: 10 undeclared absence, 9 undeclared rewording, 2 verbatim violation.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 48 |
| Claims extracted from `source_a.md` | 57 |
| Claims extracted from `source_b.md` | 42 |
| Forward — source claims accounted for in the merge | **89/99** |
| Forward — carried only in part | 2 |
| Forward — `source_a.md` claims accounted for | **55/57** (1 in part) |
| Forward — `source_b.md` claims accounted for | **34/42** (1 in part) |
| Reverse — merge claims found in a source | **48/48** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **140/141** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Dropped — in a source, not in the merge

- **A-008** (`source_a.md:5`) — A client spread across eight worker processes pays for the extra file descriptors.
  - judged against: `merged.md`
  - rationale: The reference text does not mention any cost associated with extra file descriptors.
- **B-005** (`source_b.md:5`) — The gateway doesn't disclose the start of the window.
  - judged against: `merged.md`
  - rationale: The reference text does not discuss whether the gateway discloses the window start.
- **B-006** (`source_b.md:5`) — The count follows the credential wherever the caller happens to put it, including across hosts.
  - judged against: `merged.md`
  - rationale: The text mentions multiple processes but does not explicitly state the count follows across hosts.
- **B-017** (`source_b.md:21`) — The set of safe-to-retry responses is a smaller set than the set of responses that aren't a success.
  - judged against: `merged.md`
  - rationale: The text lists safe-to-retry cases but does not explicitly compare set sizes.
- **B-032** (`source_b.md:29`) — A request body over the 5 megabyte limit is refused before it has been read at all.
  - judged against: `merged.md`
  - rationale: The text lists body size as a refusal reason but does not specify timing of refusal or whether the body is read.
- **B-035** (`source_b.md:31`) — The wasted budget is the caller's own.
  - judged against: `merged.md`
  - rationale: The text states the budget is spent but does not specify it is the caller's own budget or that they bear the cost.

### Partly dropped — the merge carries some of this claim

- **A-007** (`source_a.md:5`) — A client spread across eight worker processes is throttled at exactly the point one process would have been.
  - evidence: 'a client spread across multiple worker processes is throttled at exactly the point a single process would have been.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text supports the principle but specifies 'multiple' processes, not the specific number 'eight.'
- **B-041** (`source_b.md:37`) — An answer takes two working days.
  - evidence: 'they are answered within two working days.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text states 'within' two days, not exactly two days; the claim is slightly more specific.

### Contradicted — the merge states something different

- **B-011** -- the two documents disagree
  - `source_b.md:11` says: The header is present on every refusal the gateway sends.
  - `merged.md` says: 'None of those three clears itself by waiting for a stated number of seconds.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text indicates suspended credentials, closed routes, and body size limits do not involve waiting stated seconds, implying they lack Retry-After headers.
- **B-023** -- the two documents disagree
  - `source_b.md:23` says: 1000 is 50 times the default.
  - `merged.md` says: 'The default allowance is 100 requests in a window.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: 1000 is 10 times the default (100), not 50 times.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 57 claim(s): 1 dropped, 0 contradicted, 1 carried in part, 55 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 8 | A client spread across eight worker processes pays for the extra file descriptors. | 5 | dropped | The reference text does not mention any cost associated with extra file descriptors. |
| 7 | A client spread across eight worker processes is throttled at exactly the point one process would have been. | 5 | carried in part | 'a client spread across multiple worker processes is throttled at exactly the point a single process would have been.' in `merged.md` -- The text supports the principle but specifies 'multiple' processes, not the specific number 'eight.' |
| 1 | Every credential has a cap. | 3 | carried | 'Every credential has a cap.' in `merged.md` -- The reference text states this exactly. |
| 2 | When a cap is spent the gateway answers 429 at the edge without waking the service behind it. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge — without waking the service behind it —' in `merged.md` -- The text directly states the claim with equivalent wording. |
| 3 | Requests are counted against the credential that presented them. | 5 | carried | 'Requests are counted against the credential that presented them,' in `merged.md` -- The reference text states this explicitly. |
| 4 | Requests are counted over a fixed window of 60 seconds. | 5 | carried | 'over a fixed window of 60 seconds,' in `merged.md` -- The text explicitly states the window duration. |
| 5 | Requests are never counted against a connection. | 5 | carried | 'never against a connection.' in `merged.md` -- The reference text directly states requests are never counted against a connection. |
| 6 | Opening a second socket buys a caller nothing. | 5 | carried | 'Opening a second socket therefore buys a caller nothing,' in `merged.md` -- The text uses identical wording for this claim. |
| 9 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window.' in `merged.md` -- The text states this exactly. |
| 10 | A credential marked for batch work is allowed 1000 in the same window. | 7 | carried | 'A credential marked for batch work is allowed 1000 in the same window.' in `merged.md` -- The reference text explicitly states the batch allowance. |
| 11 | A refusal is not an outage. | 7 | carried | 'A refusal is not an outage,' in `merged.md` -- The text states this claim directly. |
| 12 | Callers that retry at once are the largest single reason the cap is there at all. | 7 | carried | 'Callers that retry immediately are the largest single reason the cap is there at all.' in `merged.md` -- 'Immediately' and 'at once' convey the same meaning in this context. |
| 13 | The refusal carries a Retry-After header. | 11 | carried | 'The refusal carries a Retry-After header.' in `merged.md` -- The text states this explicitly. |
| 14 | The Retry-After header value is a whole number of seconds to wait. | 11 | carried | 'Its value is a whole number of seconds to wait.' in `merged.md` -- The reference text directly describes the header value format. |
| 15 | Waiting that long and then continuing is the whole of the contract. | 11 | carried | 'Waiting that long and then continuing is the whole of the contract —' in `merged.md` -- The text states this exactly. |
| 16 | The gateway keeps no memory of who backed off politely. | 11 | carried | 'The gateway keeps no memory of who backed off politely,' in `merged.md` -- The reference text states this claim directly. |
| 17 | Waiting longer than the header asks earns a caller no credit at all. | 11 | carried | 'waiting longer than the header asks earns a caller no credit at all.' in `merged.md` -- The text uses equivalent wording for this claim. |
| 18 | The body of the refusal is JSON. | 13 | carried | 'The body of the refusal is JSON,' in `merged.md` -- The text explicitly states the body format. |
| 19 | The body names what the gateway calls the window it counted in. | 13 (unverified) | carried | 'It names what the gateway calls the "window" it counted in.' in `merged.md` -- The reference text directly states what the body contains. |
| 20 | The body names the cap and the tier. | 13 | carried | 'It names the cap and the tier as well.' in `merged.md` -- The text explicitly states the body names these fields. |
| 21 | None of the fields in the body is a substitute for the header. | 13 | carried | 'None of those fields is a substitute for the header,' in `merged.md` -- The text states this claim directly. |
| 22 | A caller that parses the body to compute its own wait is doing the same arithmetic twice. | 13 | carried | 'a caller that parses the body to compute its own wait is doing the same arithmetic twice.' in `merged.md` -- The reference text uses identical wording. |
| 23 | The gateway has already done the arithmetic, with information the caller does not have. | 19 | carried | 'The gateway has already done that arithmetic, with information the caller does not have,' in `merged.md` -- The text states this claim directly. |
| 24 | The gateway does the same on the 503 path. | 19 | carried | 'and it does the same on the 503 path.' in `merged.md` -- The text explicitly states this. |
| 25 | A wait derived on the client side is a guess about a counter it cannot see. | 19 | carried | 'A wait derived on the client side is a guess about a counter it cannot see.' in `merged.md` -- The reference text states this exactly. |
| 26 | A 200 wants nothing. | 21 | carried | 'A 200 wants nothing,' in `merged.md` -- The text uses identical wording. |
| 27 | A 429 wants the stated wait. | 21 | carried | 'a 429 wants the stated wait,' in `merged.md` -- The reference text states this directly. |
| 28 | A 500 may be retried once that wait has passed. | 21 | carried | 'a 500 may be retried once that wait has passed,' in `merged.md` -- 'May be retried' and 'can be retried' convey the same meaning. |
| 29 | A 503 is the overload path. | 21 | carried | 'and a 503 is the overload path.' in `merged.md` -- The text states this claim directly. |
| 30 | The four cases are not interchangeable. | 21 | carried | 'The four cases are not interchangeable.' in `merged.md` -- The reference text states this explicitly. |
| 31 | A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive. | 21 | carried | 'A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive.' in `merged.md` -- The text uses this claim word-for-word. |
| 32 | A batch credential is allowed fifty times the default allowance. | 23 | carried | 'A batch credential is allowed fifty times the default allowance,' in `merged.md` -- The reference text states this directly. |
| 33 | A batch credential is measured over exactly the same window. | 23 | carried | 'and it is measured over exactly the same window.' in `merged.md` -- The text explicitly states the batch window. |
| 34 | The tier is set on the credential when it is issued. | 23 | carried | 'The tier is set on the credential when it is issued' in `merged.md` -- The reference text states this claim. |
| 35 | The tier cannot be asked for per call. | 23 | carried | 'and cannot be asked for per call.' in `merged.md` -- The text directly states this. |
| 36 | Nothing else about the two tiers differs in any way. | 23 | carried | 'Nothing else about the two tiers differs in any way.' in `merged.md` -- The reference text states this exactly. |
| 37 | A caller that cannot say how often it was refused last week cannot argue for a larger cap. | 25 | carried | 'A caller that cannot say how often it was refused last week cannot argue for a larger cap,' in `merged.md` -- The text states this claim directly. |
| 38 | Nobody at the far end will assemble that argument on the caller's behalf. | 25 | carried | 'and nobody at the far end will assemble that argument on its behalf.' in `merged.md` -- The reference text uses equivalent wording for this claim. |
| 39 | The log line should carry the credential, the window and the wait. | 25 | carried | 'The log line should carry the credential, the window and the wait.' in `merged.md` -- The text states this exactly. |
| 40 | The gateway refuses requests for three reasons. | 29 | carried | 'The gateway refuses a request for three reasons' in `merged.md` -- The reference text explicitly states the number of refusal reasons. |
| 41 | One of those reasons is the rate cap mentioned above. | 29 | carried | 'and only one of them is the one above.' in `merged.md` -- The text states that the rate cap is one of the three reasons. |
| 42 | A credential may be suspended. | 29 | carried | 'A credential may be suspended,' in `merged.md` -- The reference text explicitly lists this as a refusal reason. |
| 43 | A route may be closed for maintenance. | 29 | carried | 'a route may be closed for maintenance,' in `merged.md` -- The text explicitly states this as a refusal reason. |
| 44 | A body may exceed the 5 megabyte limit. | 29 | carried | 'or a body may exceed the 5 megabyte limit.' in `merged.md` -- The reference text explicitly lists this as a refusal reason. |
| 45 | Suspended credentials, closed routes, and body size limits do not clear themselves by waiting for a stated number of seconds. | 29 | carried | 'None of those three clears itself by waiting for a stated number of seconds.' in `merged.md` -- The text directly supports this claim about non-rate-limiting refusals. |
| 46 | A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `merged.md` -- The text uses equivalent wording for this claim. |
| 47 | The log shows nothing except a long run of refusals when retrying against a suspended credential. | 31 | carried | 'and the log afterwards shows nothing at all except a long run of refusals.' in `merged.md` -- The reference text directly supports this claim. |
| 48 | Reading the status code rather than the class separates the two cases. | 31 | carried | 'Reading the status code rather than the class it belongs to is what separates the two cases,' in `merged.md` -- The text states this equivalently. |
| 49 | Distinguishing by status code costs one comparison. | 31 | carried | 'and it costs one comparison.' in `merged.md` -- The reference text states this explicitly. |
| 50 | A cap can be raised. | 35 | carried | 'A cap can be raised,' in `merged.md` -- The text states this claim directly. |
| 51 | The number of caps raised without a measurement behind them is 0. | 35 | carried | 'A cap can be raised, but only with measurement.' in `merged.md` -- 'Only with measurement' necessarily entails that zero are raised without measurement. |
| 52 | A burst is cheaper to smooth than to serve at its peak. | 35 | carried | 'a burst is cheaper to smooth than it is to serve at its peak.' in `merged.md` -- The reference text states this directly. |
| 53 | A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap. | 35 | carried | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all,' in `merged.md` -- The text uses equivalent wording. |
| 54 | Requests reach the platform team through the usual channel. | 37 | carried | 'Requests reach the platform team through the usual channel,' in `merged.md` -- The reference text states this explicitly. |
| 55 | Requests are answered within two working days. | 37 | carried | 'and they are answered within two working days.' in `merged.md` -- The text directly states the response time. |
| 56 | There is no expedited path. | 37 | carried | 'There is no expedited path' in `merged.md` -- The reference text states this exactly. |
| 57 | There is no exception list. | 37 | carried | 'and no exception list.' in `merged.md` -- The text explicitly states this. |

### `source_b.md` -- 42 claim(s): 5 dropped, 2 contradicted, 1 carried in part, 34 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 5 | The gateway doesn't disclose the start of the window. | 5 (unverified) | dropped | The reference text does not discuss whether the gateway discloses the window start. |
| 6 | The count follows the credential wherever the caller happens to put it, including across hosts. | 5 | dropped | The text mentions multiple processes but does not explicitly state the count follows across hosts. |
| 17 | The set of safe-to-retry responses is a smaller set than the set of responses that aren't a success. | 21 (unverified) | dropped | The text lists safe-to-retry cases but does not explicitly compare set sizes. |
| 32 | A request body over the 5 megabyte limit is refused before it has been read at all. | 29 | dropped | The text lists body size as a refusal reason but does not specify timing of refusal or whether the body is read. |
| 35 | The wasted budget is the caller's own. | 31 (unverified) | dropped | The text states the budget is spent but does not specify it is the caller's own budget or that they bear the cost. |
| 11 | The header is present on every refusal the gateway sends. | 11 | contradicted | 'None of those three clears itself by waiting for a stated number of seconds.' in `merged.md` -- The text indicates suspended credentials, closed routes, and body size limits do not involve waiting stated seconds, implying they lack Retry-After headers. |
| 23 | 1000 is 50 times the default. | 23 | contradicted | 'The default allowance is 100 requests in a window.' in `merged.md` -- 1000 is 10 times the default (100), not 50 times. |
| 41 | An answer takes two working days. | 37 | carried in part | 'they are answered within two working days.' in `merged.md` -- The text states 'within' two days, not exactly two days; the claim is slightly more specific. |
| 1 | Every credential has a cap of its own. | 3 | carried | 'Every credential has a cap.' in `merged.md` -- The singular 'a cap' per credential necessarily implies 'of its own.' |
| 2 | When a credential's cap is spent, the gateway answers 429 at the edge, without troubling the service behind it. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge — without waking the service behind it —' in `merged.md` -- 'Without troubling' and 'without waking' convey the same meaning. |
| 3 | Requests are counted against the credential rather than the connection. | 5 | carried | 'Requests are counted against the credential that presented them, over a fixed window of 60 seconds, never against a connection.' in `merged.md` -- The text explicitly contrasts credential with connection counting. |
| 4 | Requests are counted over a fixed window of 60 seconds. | 5 | carried | 'over a fixed window of 60 seconds,' in `merged.md` -- The reference text directly states the window duration. |
| 7 | A caller spread over many worker processes is throttled at the same point a single process would have been. | 5 | carried | 'a client spread across multiple worker processes is throttled at exactly the point a single process would have been.' in `merged.md` -- 'Many processes' and 'multiple processes' convey the same meaning. |
| 8 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window.' in `merged.md` -- The reference text states this explicitly. |
| 9 | The header is called Retry-After. | 11 | carried | 'The refusal carries a Retry-After header.' in `merged.md` -- The text explicitly names the header. |
| 10 | The header's value is a whole number of seconds. | 11 | carried | 'Its value is a whole number of seconds to wait.' in `merged.md` -- The text directly describes the header value format. |
| 12 | The response body is JSON. | 13 | carried | 'The body of the refusal is JSON,' in `merged.md` -- The reference text explicitly states the body format. |
| 13 | The response body repeats the cap, the window and the tier as plain fields. | 13 | carried | 'It names what the gateway calls the "window" it counted in. It names the cap and the tier as well.' in `merged.md` -- The text states the body contains these fields in JSON format. |
| 14 | The body is for the human reading the log afterwards. | 13 | carried | 'The body is there so that a human reading a log afterwards can see why the request was refused' in `merged.md` -- The reference text states this purpose directly. |
| 15 | There are four rules. | 17 | carried | 'Four rules, given in the order they should be applied.' in `merged.md` -- The text explicitly states there are four rules. |
| 16 | On the 503 path the same rule holds. | 19 | carried | 'and it does the same on the 503 path.' in `merged.md` -- The text directly states the gateway applies the same arithmetic principle to 503. |
| 18 | A 200 response needs nothing. | 21 | carried | 'A 200 wants nothing,' in `merged.md` -- 'Needs' and 'wants' are equivalent in this context. |
| 19 | A 429 response needs the stated wait. | 21 | carried | 'a 429 wants the stated wait,' in `merged.md` -- The text uses equivalent wording. |
| 20 | A 500 response can be retried once that wait has passed. | 21 | carried | 'a 500 may be retried once that wait has passed,' in `merged.md` -- 'Can be retried' and 'may be retried' convey the same meaning. |
| 21 | A 503 response means the platform itself is overloaded. | 21 | carried | 'a 503 is the overload path.' in `merged.md` -- 'Overload path' necessarily means the platform is overloaded when 503 is returned. |
| 22 | A batch credential is allowed 1000 requests in a window. | 23 | carried | 'A credential marked for batch work is allowed 1000 in the same window.' in `merged.md` -- The reference text explicitly states the batch allowance. |
| 24 | The batch tier is not a separate counting scheme. | 23 | carried | 'and it is measured over exactly the same window.' in `merged.md` -- Identical window and measurement method mean the same counting scheme is used. |
| 25 | The window, the header and the body are identical to the interactive case. | 23 | carried | 'Nothing else about the two tiers differs in any way.' in `merged.md` -- 'Nothing else differs' necessarily entails window, header, and body are identical. |
| 26 | Nothing else about the batch tier differs from the default. | 23 | carried | 'Nothing else about the two tiers differs in any way.' in `merged.md` -- The text directly states no other differences between batch and default tiers. |
| 27 | The gateway refuses a request for three separate reasons. | 29 | carried | 'The gateway refuses a request for three reasons' in `merged.md` -- The reference text explicitly states three separate refusal reasons. |
| 28 | Only one of them is a cap. | 29 | carried | 'and only one of them is the one above.' in `merged.md` -- The text states the rate cap is the only cap-related reason. |
| 29 | Two of the three refusal reasons have nothing to do with how much traffic a caller has sent in the window it is currently in. | 29 | carried | 'A credential may be suspended, a route may be closed for maintenance' in `merged.md` -- These two reasons don't involve current-window traffic counts. |
| 30 | A credential can be suspended. | 29 | carried | 'A credential may be suspended,' in `merged.md` -- The reference text explicitly lists this refusal reason. |
| 31 | A route can be closed while it is being repaired. | 29 | carried | 'a route may be closed for maintenance,' in `merged.md` -- Maintenance includes repair. |
| 33 | A loop retrying against a suspended credential burns its whole budget and reaches nothing. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `merged.md` -- 'Burns its whole budget' and 'spends its whole budget' convey the same meaning; 'reaches nothing' means never reaching the service. |
| 34 | The log afterwards shows a long run of refusals and no successes at all. | 31 | carried | 'and the log afterwards shows nothing at all except a long run of refusals.' in `merged.md` -- 'Nothing except refusals' entails no successes and only refusals. |
| 36 | A cap can be raised. | 33 | carried | 'A cap can be raised,' in `merged.md` -- The reference text states this explicitly. |
| 37 | A cap cannot be raised on the strength of an assertion that the current one is too small. | 33 | carried | 'A cap can be raised, but only with measurement.' in `merged.md` -- 'Only with measurement' necessarily entails no raises without measurement. |
| 38 | The team wants to know whether the load is smooth or bursty before it looks at the number at all. | 35 | carried | 'The platform team looks at whether the load is smooth or bursty — a burst is cheaper to smooth than it is to serve at its peak. A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all,' in `merged.md` -- The text indicates smoothness is evaluated before changing the cap. |
| 39 | Requests go to the platform team through the usual channel. | 35 | carried | 'Requests reach the platform team through the usual channel,' in `merged.md` -- The reference text states this directly. |
| 40 | There is no expedited path. | 37 | carried | 'There is no expedited path' in `merged.md` -- The text explicitly states this. |
| 42 | Chasing the request doesn't make it take fewer days. | 37 (unverified) | carried | 'There is no expedited path' in `merged.md` -- No expedited path necessarily means chasing the request cannot make it faster. |

### `merged.md` -- 48 claim(s): 0 invented, 0 contradicted, 0 supported in part, 48 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Every credential has a cap. | supported | `source_a.md` | 'Every credential has a cap.' in `source_a.md` -- source_a.md opens with this exact statement. |
| 2 | The gateway answers 429 at the edge when that cap is spent. | supported | `source_a.md` | 'When that cap is spent the gateway answers 429 at the edge' in `source_a.md` -- source_a.md states this in the opening paragraph. |
| 3 | Requests are counted against the credential that presented them, over a fixed window of 60 seconds. | supported | `source_a.md` | 'Requests are counted against the credential that presented them, over a fixed window of 60 seconds' in `source_a.md` -- source_a.md states this directly in the second paragraph. |
| 4 | Requests are never counted against a connection. | supported | `source_a.md` | 'and never against a connection' in `source_a.md` -- source_a.md explicitly states requests are never counted against a connection. |
| 5 | Opening a second socket buys a caller nothing. | supported | `source_a.md` | 'Opening a second socket therefore buys a caller nothing.' in `source_a.md` -- source_a.md states this directly. |
| 6 | A client spread across multiple worker processes is throttled at exactly the point a single process would have been. | supported | `source_a.md` | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `source_a.md` -- source_a.md states this in the second paragraph. |
| 7 | The default allowance is 100 requests in a window. | supported | `source_a.md` | 'The default allowance is 100 requests in a window' in `source_a.md` -- source_a.md states this directly. |
| 8 | A credential marked for batch work is allowed 1000 in the same window. | supported | `source_a.md` | 'a credential marked for batch work is allowed 1000 in the same window' in `source_a.md` -- source_a.md states this in the opening section. |
| 9 | A refusal is the platform declining to spend capacity that has already been promised to somebody else. | supported | `source_a.md` | 'It is the platform declining to spend capacity that has already been promised to somebody else' in `source_a.md` -- source_a.md defines a refusal this way in the opening section. |
| 10 | Callers that retry immediately are the largest single reason the cap is there at all. | supported | `source_a.md` | 'Callers that retry at once are the largest single reason the cap is there at all.' in `source_a.md` -- source_a.md states this explicitly in the opening section. |
| 11 | The refusal carries a Retry-After header. | supported | `source_a.md` | 'The refusal carries a Retry-After header.' in `source_a.md` -- source_a.md states this in the 'How to read a refusal' section. |
| 12 | The value of the Retry-After header is a whole number of seconds to wait. | supported | `source_a.md` | 'Its value is a whole number of seconds to wait.' in `source_a.md` -- source_a.md states this in the 'How to read a refusal' section. |
| 13 | The gateway keeps no memory of who backed off politely. | supported | `source_a.md` | 'The gateway keeps no memory of who backed off politely' in `source_a.md` -- source_a.md states this in the 'How to read a refusal' section. |
| 14 | Waiting longer than the header asks earns a caller no credit at all. | supported | `source_a.md` | 'waiting longer than the header asks earns a caller no credit at all' in `source_a.md` -- source_a.md states this in the 'How to read a refusal' section. |
| 15 | The body of the refusal is JSON. | supported | `source_a.md` | 'The body of the refusal is JSON' in `source_a.md` -- source_a.md states this in the 'How to read a refusal' section. |
| 16 | The body names what the gateway calls the window it counted in. | supported | `source_a.md` | 'It names what the gateway calls the "window" it counted in.' in `source_a.md`, **transcription_error** -- source_a.md states this in the 'How to read a refusal' section. |
| 17 | The body names the cap and the tier. | supported | `source_a.md` | 'It names the cap and the tier as well.' in `source_a.md` -- source_a.md states this in the 'How to read a refusal' section. |
| 18 | A caller that parses the body to compute its own wait is doing the same arithmetic twice. | supported | `source_a.md` | 'a caller that parses the body to compute its own wait is doing the same arithmetic twice' in `source_a.md` -- source_a.md states this in the 'How to read a refusal' section. |
| 19 | The gateway has already done the arithmetic with information the caller does not have. | supported | `source_a.md` | 'The gateway has already done that arithmetic, with information the caller does not have' in `source_a.md` -- source_a.md states this in the 'How to retry well' section. |
| 20 | The gateway does the same on the 503 path. | supported | `source_a.md` | 'and it does the same on the 503 path' in `source_a.md` -- source_a.md states this in the 'How to retry well' section. |
| 21 | A wait derived on the client side is a guess about a counter the client cannot see. | supported | `source_a.md` | 'A wait derived on the client side is a guess about a counter it cannot see.' in `source_a.md` -- source_a.md states this in the 'How to retry well' section. |
| 22 | A 200 response wants nothing. | supported | `source_a.md` | 'A 200 wants nothing' in `source_a.md` -- source_a.md states this in the 'How to retry well' section rule 2. |
| 23 | A 429 response wants the stated wait. | supported | `source_a.md` | 'a 429 wants the stated wait' in `source_a.md` -- source_a.md states this in the 'How to retry well' section rule 2. |
| 24 | A 500 may be retried once that wait has passed. | supported | `source_a.md` | 'a 500 may be retried once that wait has passed' in `source_a.md` -- source_a.md states this in the 'How to retry well' section rule 2. |
| 25 | A 503 is the overload path. | supported | `source_a.md` | 'and a 503 is the overload path' in `source_a.md` -- source_a.md states this in the 'How to retry well' section rule 2. |
| 26 | A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive. | supported | `source_a.md` | 'A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive.' in `source_a.md` -- source_a.md states this in the 'How to retry well' section rule 2. |
| 27 | A batch credential is allowed fifty times the default allowance. | supported | `source_a.md` | 'A batch credential is allowed fifty times the default allowance' in `source_a.md` -- source_a.md states this in the 'How to retry well' section rule 3. |
| 28 | A batch credential allowance is measured over exactly the same window. | supported | `source_a.md` | 'and it is measured over exactly the same window' in `source_a.md` -- source_a.md states this in the 'How to retry well' section rule 3. |
| 29 | The tier is set on the credential when it is issued. | supported | `source_a.md` | 'The tier is set on the credential when it is issued' in `source_a.md` -- source_a.md states this in the 'How to retry well' section rule 3. |
| 30 | The tier cannot be asked for per call. | supported | `source_a.md` | 'and cannot be asked for per call' in `source_a.md` -- source_a.md states this in the 'How to retry well' section rule 3. |
| 31 | Nothing else about the two tiers differs in any way. | supported | `source_a.md` | 'Nothing else about the two tiers differs in any way.' in `source_a.md` -- source_a.md states this in the 'How to retry well' section rule 3. |
| 32 | Nobody at the far end will assemble the argument on the caller's behalf. | supported | `source_a.md` | 'and nobody at the far end will assemble that argument on its behalf' in `source_a.md` -- source_a.md states this in the 'How to retry well' section rule 4. |
| 33 | A credential may be suspended. | supported | `source_a.md` | 'A credential may be suspended' in `source_a.md` -- source_a.md states this in the 'Other refusals and their codes' section. |
| 34 | A route may be closed for maintenance. | supported | `source_a.md` | 'a route may be closed for maintenance' in `source_a.md` -- source_a.md states this in the 'Other refusals and their codes' section. |
| 35 | A body may exceed the 5 megabyte limit. | supported | `source_a.md` | 'or a body may exceed the 5 megabyte limit' in `source_a.md` -- source_a.md states this in the 'Other refusals and their codes' section. |
| 36 | None of those three clears itself by waiting for a stated number of seconds. | supported | `source_a.md` | 'None of those three clears itself by waiting for a stated number of seconds.' in `source_a.md` -- source_a.md states this in the 'Other refusals and their codes' section. |
| 37 | A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service. | supported | `source_a.md` | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `source_a.md` -- source_a.md states this in the 'Other refusals and their codes' section. |
| 38 | The log afterwards shows nothing at all except a long run of refusals. | supported | `source_a.md` | 'and the log afterwards shows nothing at all except a long run of refusals' in `source_a.md` -- source_a.md states this in the 'Other refusals and their codes' section. |
| 39 | Reading the status code rather than the class it belongs to is what separates the two cases. | supported | `source_a.md` | 'Reading the status code rather than the class it belongs to is what separates the two cases' in `source_a.md` -- source_a.md states this in the 'Other refusals and their codes' section. |
| 40 | Reading the status code rather than the class it belongs to costs one comparison. | supported | `source_a.md` | 'and it costs one comparison' in `source_a.md` -- source_a.md states this in the 'Other refusals and their codes' section. |
| 41 | The platform team looks at whether the load is smooth or bursty. | supported | `source_a.md` | 'The platform team looks at whether the load is smooth or bursty' in `source_a.md` -- source_a.md states this in the 'Asking for an increase' section. |
| 42 | A burst is cheaper to smooth than it is to serve at its peak. | supported | `source_a.md` | 'a burst is cheaper to smooth than it is to serve at its peak' in `source_a.md` -- source_a.md states this in the 'Asking for an increase' section. |
| 43 | A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all. | supported | `source_a.md` | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `source_a.md` -- source_a.md states this in the 'Asking for an increase' section. |
| 44 | Everyone prefers the outcome where callers get what they need without the cap being changed. | supported | `source_a.md` | 'which is the outcome everyone prefers' in `source_a.md` -- source_a.md states this in the 'Asking for an increase' section. |
| 45 | Requests reach the platform team through the usual channel. | supported | `source_a.md` | 'Requests reach the platform team through the usual channel' in `source_a.md` -- source_a.md states this in the 'Asking for an increase' section. |
| 46 | Requests are answered within two working days. | supported | `source_a.md` | 'and they are answered within two working days' in `source_a.md` -- source_a.md states this in the 'Asking for an increase' section. |
| 47 | There is no expedited path. | supported | `source_a.md` | 'There is no expedited path' in `source_a.md` -- source_a.md states this in the 'Asking for an increase' section. |
| 48 | There is no exception list. | supported | `source_a.md` | 'and no exception list' in `source_a.md` -- source_a.md states this in the 'Asking for an increase' section. |

## Structure

**9** mechanical check(s) over **104** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **48** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **99**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 1 run(s) over 47 attributed segment(s) — not conclusive on this evidence base. 6 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

`[-...-]` is what the source said and `{+...+}` is what the merge says.

### Absent and undeclared — in a source, not in the merge, and no record explains it

- `a5` (`source_a.md`) — 'Opening a second socket therefore buys a caller nothing.' is not in the merge and no disposition record explains it (nearest merge segment m5 at 0.48)

  ```text
  In the source: Opening a second socket therefore buys a caller nothing.
  ```
- `b24` (`source_b.md`) — 'On the 503 path the same rule holds, even though the cause of the refusal is an entirely different one.' is not in the merge and no disposition record explains it (nearest merge segment m50 at 0.44)

  ```text
  In the source: On the 503 path the same rule holds, even though the cause of the refusal is an entirely different one.
  ```
- `b25` (`source_b.md`) — 'Anything computed on the client side is a guess.' is not in the merge and no disposition record explains it (nearest merge segment m24 at 0.59)

  ```text
  In the source: Anything computed on the client side is a guess.
  ```
- `b26` (`source_b.md`) — 'That guess is not worth having.' is not in the merge and no disposition record explains it (nearest merge segment m28 at 0.49)

  ```text
  In the source: That guess is not worth having.
  ```
- `b30` (`source_b.md`) — 'That is the behaviour this rule exists to prevent.' is not in the merge and no disposition record explains it (nearest merge segment m13 at 0.41)

  ```text
  In the source: That is the behaviour this rule exists to prevent.
  ```
- `b32` (`source_b.md`) — 'The window, the header and the body are identical to the interactive case, so a client written for one tier needs no change at all to run against the other.' is not in the merge and no disposition record explains it (nearest merge segment m14 at 0.46)

  ```text
  In the source: The window, the header and the body are identical to the interactive case, so a client written for one tier needs no change at all to run against the other.
  ```
- `b36` (`source_b.md`) — 'The counts are the whole of the argument, and without them a request is only a preference.' is not in the merge and no disposition record explains it (nearest merge segment m47 at 0.45)

  ```text
  In the source: The counts are the whole of the argument, and without them a request is only a preference.
  ```
- `b43` (`source_b.md`) — 'The log afterwards shows a long run of refusals and no successes at all, which reads like an outage and isn’t one — and the wasted budget is the caller’s own.' is not in the merge and no disposition record explains it (nearest merge segment m19 at 0.42)

  ```text
  In the source: The log afterwards shows a long run of refusals and no successes at all, which reads like an outage and isn’t one — and the wasted budget is the caller’s own.
  ```
- `b45` (`source_b.md`) — 'That is the cheapest fix available to anybody, and it is available to almost everybody.' is not in the merge and no disposition record explains it (nearest merge segment m32 at 0.42)

  ```text
  In the source: That is the cheapest fix available to anybody, and it is available to almost everybody.
  ```
- `b49` (`source_b.md`) — 'A burst is cheaper to smooth out than it is to serve at its peak.' is not in the merge and no disposition record explains it (nearest merge segment m48 at 0.64)

  ```text
  In the source: A burst is cheaper to smooth out than it is to serve at its peak.
  ```

### Reworded and undeclared — in the merge in altered wording, and no record explains it. At off this also covers layout: a segment whose source line breaks the merge ran together is altered and undeclared, and 380 reuses this kind rather than moving FINDING_KINDS off 12

- `a4` (`source_a.md`) — 'Requests are counted against the credential that presented them, over a fixed window of 60 seconds, and never against a connection.' is reworded in the merge and no disposition record explains it (nearest merge segment m4 at 0.98)

  ```text
  In the source: Requests are counted against the credential that presented them, over a fixed window of 60 seconds, and never against a connection.
  In the merge:  Requests are counted against the credential that presented them, over a fixed window of 60 seconds, never against a connection.
  What changed:  Requests are counted against the credential that presented them, over a fixed window of 60 seconds, [-and-] never against a connection.
  ```
- `a7` (`source_a.md`) — 'The default allowance is 100 requests in a window, and a credential marked for batch work is allowed 1000 in the same window.' is reworded in the merge and no disposition record explains it (nearest merge segment m7 at 0.72)

  ```text
  In the source: The default allowance is 100 requests in a window, and a credential marked for batch work is allowed 1000 in the same window.
  In the merge:  A credential marked for batch work is allowed 1000 in the same window.
  ```
- `a10` (`source_a.md`) — 'Callers that retry at once are the largest single reason the cap is there at all.' is reworded in the merge and no disposition record explains it (nearest merge segment m10 at 0.93)

  ```text
  In the source: Callers that retry at once are the largest single reason the cap is there at all.
  In the merge:  Callers that retry immediately are the largest single reason the cap is there at all.
  What changed:  Callers that retry [-at once-] {+immediately+} are the largest single reason the cap is there at all.
  ```
- `a16` (`source_a.md`) — 'The body of the refusal is JSON, and it names what the gateway calls the “window” it counted in.' is reworded in the merge and no disposition record explains it (nearest merge segment m16 at 0.98)

  ```text
  In the source: The body of the refusal is JSON, and it names what the gateway calls the “window” it counted in.
  In the merge:  The body of the refusal is JSON, and it names what the gateway calls the "window" it counted in.
  What changed:  The body of the refusal is JSON, and it names what the gateway calls the [-“window”-] {+"window"+} it counted in.
  ```
- `b23` (`source_b.md`) — 'The gateway has already done that arithmetic and it did it with information the caller cannot see.' is reworded in the merge and no disposition record explains it (nearest merge segment m23 at 0.72)

  ```text
  In the source: The gateway has already done that arithmetic and it did it with information the caller cannot see.
  In the merge:  The gateway has already done that arithmetic, with information the caller does not have, and it does the same on the 503 path.
  ```
- `b28` (`source_b.md`) — 'A 200 needs nothing, a 429 needs the stated wait, a 500 can be retried once that wait has passed, and a 503 means the platform itself is overloaded.' is reworded in the merge and no disposition record explains it (nearest merge segment m27 at 0.83)

  ```text
  In the source: A 200 needs nothing, a 429 needs the stated wait, a 500 can be retried once that wait has passed, and a 503 means the platform itself is overloaded.
  In the merge:  A 200 wants nothing, a 429 wants the stated wait, a 500 may be retried once that wait has passed, and a 503 is the overload path.
  What changed:  A 200 [-needs-] {+wants+} nothing, a 429 [-needs-] {+wants+} the stated wait, a 500 [-can-] {+may+} be retried once that wait has passed, and a 503 [-means-] {+is+} the [-platform itself is overloaded.-] {+overload path.+}
  ```
- `b29` (`source_b.md`) — 'A caller that folds all four into one branch will retry hardest during exactly the incident the cap was installed to survive.' is reworded in the merge and no disposition record explains it (nearest merge segment m29 at 0.90)

  ```text
  In the source: A caller that folds all four into one branch will retry hardest during exactly the incident the cap was installed to survive.
  In the merge:  A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive.
  What changed:  A [-caller-] {+client+} that folds [-all four-] {+every non-success+} into one branch will retry hardest during exactly the incident the cap was installed to survive.
  ```
- `b33` (`source_b.md`) — 'Nothing else about the batch tier differs from the default.' is reworded in the merge and no disposition record explains it (nearest merge segment m34 at 0.76)

  ```text
  In the source: Nothing else about the batch tier differs from the default.
  In the merge:  Nothing else about the two tiers differs in any way.
  ```
- `b35` (`source_b.md`) — 'A caller that cannot say how often it was refused can’t make a case for a larger cap, and the platform team won’t assemble that case on its behalf.' is reworded in the merge and no disposition record explains it (nearest merge segment m36 at 0.80)

  ```text
  In the source: A caller that cannot say how often it was refused can’t make a case for a larger cap, and the platform team won’t assemble that case on its behalf.
  In the merge:  A caller that cannot say how often it was refused last week cannot argue for a larger cap, and nobody at the far end will assemble that argument on its behalf.
  ```

### Verbatim violation — an invariant-core token did not survive unchanged

- `a47` (`source_a.md`) — numeric '0' does not survive into the merge unchanged
- `b31` (`source_b.md`) — numeric '50' (times) does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **41** departure(s) from its sources. Checking them confirms 23, rejects 3, and leaves 15 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 1 of 104 source segment(s) declared gone, **1.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a3` | reworded | Condensed to remove elaboration; core facts preserved. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-002`) |
| `a6` | reworded | Changed 'eight' to 'multiple'; dropped detail about file descriptors. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-007 came back PARTIAL, A-008 came back MISSING (`A-007`, `A-008`) |
| `a39` | superseded | a40 states the same point more specifically; a39 not carried. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a47` | reworded | Condensed equivalent claim; maintains the substance. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-050`, `A-051`) |
| `b1` | superseded | Base document title chosen; title decision made above. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Rate limiting and the 429 contract for gateway clients' and says so (no claim traced to it) |
| `b2` | superseded | a2 wording carried instead; same fact. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-001`) |
| `b3` | superseded | a3 wording carried, incorporating both source details. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-002`) |
| `b4` | dropped | Editorial comment about document history, not client guidance. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b5` | superseded | a4 version carried; expresses the same constraint. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-003`, `B-004`) |
| `b6` | superseded | a5 version carried; conveys the same principle. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b7` | subsumed | Credential counting follows it everywhere; covered by a4. | **rejected** | declared 'subsumed', which predicts SUPPORTED; B-006 came back MISSING (`B-006`) |
| `b8` | superseded | a6 version carried; makes the same point. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-007`) |
| `b9` | subsumed | Default values carried; editorial about adequacy not included. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-008`) |
| `b10` | superseded | a8 and a9 wording carried; expresses the principle directly. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b11` | superseded | a10 version carried; essentially equivalent. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b13` | superseded | a12 version carried; clearer phrasing. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-009`) |
| `b14` | superseded | a13 version carried; both versions equivalent. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-010`, `B-011`) |
| `b15` | superseded | a14 version carried; more concise. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b16` | superseded | a15 version carried; equivalent meaning. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b17` | superseded | a16 and a17 versions carried. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-012`, `B-013`) |
| `b18` | superseded | a18 version carried; clearer phrasing. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b19` | superseded | a19 version carried; equivalent. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-014`) |
| `b20` | superseded | Base heading chosen; decision made above. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b21` | superseded | a21 version carried; equivalent. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-015`) |
| `b22` | superseded | a22-a25 rule 1 carried; clearer framing. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b27` | superseded | a26-a30 rule 2 carried; more direct wording. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b31` | superseded | a31-a34 rule 3 carried; base document structure kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-022`, `B-023`, `B-024`) |
| `b34` | superseded | a35-a37 rule 4 carried; equivalent guidance. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b37` | superseded | a38 heading carried; base structure maintained. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b38` | superseded | a40 version carried; more specific phrasing. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-027`, `B-028`) |
| `b39` | subsumed | Distinction between traffic and non-traffic refusals covered. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-029`) |
| `b40` | superseded | a41 version carried; equivalent statement. | **rejected** | declared 'superseded', which predicts SUPPORTED or CONTRADICTED or PARTIAL; B-032 came back MISSING (`B-032`) |
| `b41` | subsumed | Why distinction matters covered in a43-a45. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b42` | superseded | a44 version carried; same content. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-033`) |
| `b44` | superseded | a50 version carried; directly addresses the point. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b46` | subsumed | Measurement requirement covered in a46-a48. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-036`, `B-037`) |
| `b47` | superseded | a48 version carried; equivalent statement. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b48` | superseded | a49 version carried; both state the same evaluation. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-038`) |
| `b50` | superseded | a51 version carried; includes both the channel and timeline. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-039`) |
| `b51` | superseded | a52 version carried; same statement. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-040`) |
| `b52` | superseded | a51 and a52 together cover timeline and process. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-041`) |


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
| Duration | 1066.2s |
| Generated | 2026-09-27T19:50:31+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup haiku-4.5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
