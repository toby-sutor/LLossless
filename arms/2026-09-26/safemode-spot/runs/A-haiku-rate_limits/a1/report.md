## Verdict

**23 finding(s).** In the claims: 9 dropped, 8 partially dropped, 1 contradicted. In the structure: 1 undeclared absence, 1 undeclared rewording, 2 false departure, 1 declared loss over budget. The merge declared **4** drop(s) of 104 source segment(s), **3.8%**, over the 3% budget: past that share the omissions are the finding, whatever each one says about itself.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 53 |
| Claims extracted from `source_a.md` | 64 |
| Claims extracted from `source_b.md` | 61 |
| Forward — source claims accounted for in the merge | **107/125** |
| Forward — carried only in part | 8 |
| Forward — `source_a.md` claims accounted for | **61/64** (3 in part) |
| Forward — `source_b.md` claims accounted for | **46/61** (5 in part) |
| Reverse — merge claims found in a source | **53/53** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **166/169** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Dropped — in a source, not in the merge

- **B-005** (`source_b.md:5`) — The gateway doesn't disclose the start of the window.
  - judged against: `merged.md`
  - rationale: The reference text does not mention whether the gateway discloses the start of the window.
- **B-010** (`source_b.md:7`) — A caller that needs more than that is almost always doing batch work under an interactive credential.
  - judged against: `merged.md`
  - rationale: The reference text does not state that callers needing more than 100 are almost always doing batch work under an interactive credential.
- **B-025** (`source_b.md:19`) — The cause of the refusal is an entirely different one.
  - judged against: `merged.md`
  - rationale: The reference text does not state that the cause of refusal is an entirely different one.
- **B-045** (`source_b.md:29`) — Two of the three have nothing to do with how much traffic a caller has sent in the window it is currently in.
  - judged against: `merged.md`
  - rationale: The reference text lists three refusal reasons but does not specify how many relate to traffic volume in the current window.
- **B-048** (`source_b.md:29`) — A request body over the 5 megabyte limit is refused before it has been read at all.
  - judged against: `merged.md`
  - rationale: The reference text mentions the 5 megabyte body limit but does not specify when the refusal occurs relative to reading.
- **B-051** (`source_b.md:31`) — The wasted budget is the caller's own.
  - judged against: `merged.md`
  - rationale: While the text describes budget being spent, it does not explicitly state the budget is the caller's own.
- **B-053** (`source_b.md:33`) — It is available to almost everybody.
  - judged against: `merged.md`
  - rationale: The reference text does not state that moving work to quieter hours is available to almost everybody.
- **B-055** (`source_b.md:33`) — A cap cannot be raised but on the strength of an assertion that the current one is too small.
  - judged against: `merged.md`
  - rationale: The reference text states caps need measurements behind them but does not specify they must be assertions of the cap being too small.
- **B-061** (`source_b.md:37`) — Chasing it doesn't make it take fewer.
  - judged against: `merged.md`
  - rationale: The reference text notes no expedited path exists but does not explicitly state that attempting to expedite will not reduce the timeframe.

### Partly dropped — the merge carries some of this claim

- **A-009** (`source_a.md:5`) — A client spread across eight worker processes is throttled at exactly the point one process would have been.
  - evidence: 'A client spread across multiple worker processes is throttled at exactly the point one process would have been.' in `merged.md` (transcription_error)
  - judged against: `merged.md`
  - rationale: The text states the principle but says 'multiple' not 'eight' specifically.
- **A-010** (`source_a.md:5`) — A client spread across eight worker processes pays for the extra file descriptors.
  - evidence: 'pays for the extra file descriptors as well' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text states the principle but does not specify 'eight' processes.
- **A-044** (`source_a.md:25`) — A caller that cannot say how often it was refused last week cannot argue for a larger cap.
  - evidence: 'A caller that cannot say how often it was refused cannot argue for a larger cap' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text does not specify 'last week' but logs should be kept for at least a week.
- **B-018** (`source_b.md:13`) — It repeats the cap, the window and the tier as plain fields.
  - evidence: 'It names the cap and the tier as well' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: Text states these are named but does not specify they are 'plain fields' specifically.
- **B-026** (`source_b.md:19`) — Anything computed on the client side is a guess.
  - evidence: 'A wait derived on the client side is a guess' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: Text specifies 'wait' not 'anything computed', limiting the claim.
- **B-032** (`source_b.md:21`) — A caller that folds all four into one branch will retry hardest during exactly the incident the cap was installed to survive.
  - evidence: 'A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: Text says 'every non-success' not specifically 'all four' status codes mentioned.
- **B-035** (`source_b.md:23`) — The batch counting scheme is not a separate counting scheme.
  - evidence: 'and it is measured over exactly the same window.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: Text states the window is the same but does not explicitly say the counting scheme is not separate.
- **B-056** (`source_b.md:35`) — The team wants to know whether the load is smooth or bursty before it looks at the number at all.
  - evidence: 'The platform team looks at whether the load is smooth or bursty' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text states the team examines load characteristics but does not explicitly specify the temporal order of investigation.

### Contradicted — the merge states something different

- **B-042** -- the two documents disagree
  - `source_b.md:25` says: The counts are the whole of the argument.
  - `merged.md` says: 'Bring a week of refusal counts, the shape of the traffic across the day, and the deadline that traffic is serving' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text requires counts plus traffic shape plus deadline, contradicting that counts alone are sufficient.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 64 claim(s): 0 dropped, 0 contradicted, 3 carried in part, 61 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 9 | A client spread across eight worker processes is throttled at exactly the point one process would have been. | 5 | carried in part | 'A client spread across multiple worker processes is throttled at exactly the point one process would have been.' in `merged.md`, **transcription_error** -- The text states the principle but says 'multiple' not 'eight' specifically. |
| 10 | A client spread across eight worker processes pays for the extra file descriptors. | 5 | carried in part | 'pays for the extra file descriptors as well' in `merged.md` -- The text states the principle but does not specify 'eight' processes. |
| 44 | A caller that cannot say how often it was refused last week cannot argue for a larger cap. | 25 | carried in part | 'A caller that cannot say how often it was refused cannot argue for a larger cap' in `merged.md` -- The text does not specify 'last week' but logs should be kept for at least a week. |
| 1 | Every credential has a cap. | 3 | carried | 'Every credential has a cap.' in `merged.md` -- The reference text directly states this claim. |
| 2 | When a cap is spent, the gateway answers 429 at the edge without waking the service behind it. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge — without waking the service behind it' in `merged.md` -- The text states that 429 is answered at the edge without waking the service. |
| 3 | The refusal costs the platform almost nothing. | 3 | carried | 'so the refusal costs the platform almost nothing' in `merged.md` -- The reference text directly states this claim. |
| 4 | The refusal costs a caller that files it under transport error a great deal. | 3 | carried | 'and costs a caller that files it under transport error a great deal.' in `merged.md` -- The reference text directly states this claim. |
| 5 | Requests are counted against the credential that presented them. | 5 | carried | 'Requests are counted against the credential that presented them' in `merged.md` -- The reference text directly states this claim. |
| 6 | Requests are counted over a fixed window of 60 seconds. | 5 | carried | 'over a fixed window of 60 seconds' in `merged.md` -- The reference text directly states this claim. |
| 7 | Requests are never counted against a connection. | 5 | carried | 'and never against a connection.' in `merged.md` -- The reference text directly states this claim. |
| 8 | Opening a second socket buys a caller nothing. | 5 | carried | 'Opening a second socket therefore buys a caller nothing.' in `merged.md` -- The reference text directly states this claim. |
| 11 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- The reference text directly states this claim. |
| 12 | A credential marked for batch work is allowed 1000 in the same window. | 7 | carried | 'and a credential marked for batch work is allowed 1000 in the same window.' in `merged.md` -- The reference text directly states this claim. |
| 13 | A refusal is not an outage. | 7 | carried | 'A refusal is not an outage, whatever the error class in a client library happens to call it.' in `merged.md` -- The reference text directly states this claim. |
| 14 | Waiting is the only correct answer. | 7 | carried | 'and waiting is the only correct answer.' in `merged.md` -- The reference text directly states this claim. |
| 15 | Callers that retry at once are the largest single reason the cap is there at all. | 7 | carried | 'Callers that retry at once are the largest single reason the cap is there at all.' in `merged.md` -- The reference text directly states this claim. |
| 16 | The refusal carries a Retry-After header. | 11 | carried | 'The refusal carries a Retry-After header.' in `merged.md` -- The reference text directly states this claim. |
| 17 | The value of the Retry-After header is a whole number of seconds to wait. | 11 | carried | 'Its value is a whole number of seconds to wait.' in `merged.md` -- The reference text directly states this claim. |
| 18 | Waiting that long and then continuing is the whole of the contract. | 11 | carried | 'Waiting that long and then continuing is the whole of the contract' in `merged.md` -- The reference text directly states this claim. |
| 19 | A client that waits as specified and continues needs nothing else from this document. | 11 | carried | 'a client that does it needs nothing else from this document.' in `merged.md` -- The reference text directly states this claim. |
| 20 | The gateway keeps no memory of who backed off politely. | 11 | carried | 'The gateway keeps no memory of who backed off politely' in `merged.md` -- The reference text directly states this claim. |
| 21 | Waiting longer than the header asks earns a caller no credit at all. | 11 | carried | 'so waiting longer than the header asks earns a caller no credit at all.' in `merged.md` -- The reference text directly states this claim. |
| 22 | The body of the refusal is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- The reference text directly states this claim. |
| 23 | The refusal body names what the gateway calls the "window" it counted in. | 13 (unverified) | carried | 'and it names what the gateway calls the "window" it counted in.' in `merged.md` -- The reference text directly states this claim. |
| 24 | The refusal body names the cap and the tier. | 13 | carried | 'It names the cap and the tier as well.' in `merged.md` -- The reference text directly states this claim. |
| 25 | The fields in the refusal body are not a substitute for the header. | 13 | carried | 'None of those fields is a substitute for the header' in `merged.md` -- The reference text directly states this claim. |
| 26 | A caller that parses the body to compute its own wait is doing the same arithmetic twice. | 13 | carried | 'a caller that parses the body to compute its own wait is doing the same arithmetic twice' in `merged.md` -- The reference text directly states this claim. |
| 27 | The body is there so that a human reading a log afterwards can see why the request was refused. | 13 | carried | 'The body is there so that a human reading a log afterwards can see why the request was refused' in `merged.md` -- The reference text directly states this claim. |
| 28 | Nothing in the refusal body is meant for the retry loop. | 13 | carried | 'nothing in it is meant for the retry loop.' in `merged.md` -- The reference text directly states this claim. |
| 29 | The gateway has already done the arithmetic for the header with information the caller does not have. | 19 | carried | 'The gateway has already done that arithmetic, with information the caller does not have' in `merged.md` -- The reference text directly states this claim. |
| 30 | The gateway does the same arithmetic on the 503 path. | 19 | carried | 'and it does the same on the 503 path.' in `merged.md` -- The reference text directly states this claim. |
| 31 | A wait derived on the client side is a guess about a counter it cannot see. | 19 | carried | 'A wait derived on the client side is a guess about a counter it cannot see.' in `merged.md` -- The reference text directly states this claim. |
| 32 | There is no case at all where a guess is better than the header. | 19 | carried | 'There is no case at all where a guess is the better of the two.' in `merged.md` -- The reference text directly states this claim. |
| 33 | A 200 wants nothing. | 21 | carried | 'A 200 wants nothing' in `merged.md` -- The reference text directly states this claim. |
| 34 | A 429 wants the stated wait. | 21 | carried | 'a 429 wants the stated wait' in `merged.md` -- The reference text directly states this claim. |
| 35 | A 500 may be retried once that wait has passed. | 21 | carried | 'a 500 may be retried once that wait has passed' in `merged.md` -- The reference text directly states this claim. |
| 36 | A 503 is the overload path. | 21 | carried | 'and a 503 is the overload path.' in `merged.md` -- The reference text directly states this claim. |
| 37 | The four cases are not interchangeable. | 21 | carried | 'The four cases are not interchangeable.' in `merged.md` -- The reference text directly states this claim. |
| 38 | A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive. | 21 | carried | 'A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive.' in `merged.md` -- The reference text directly states this claim. |
| 39 | A batch credential is allowed fifty times the default allowance. | 23 | carried | 'A batch credential is allowed 1000 requests in a window, which is 50 times the default allowance' in `merged.md` -- The reference text states batch allows 1000 which is 50 times the default. |
| 40 | A batch credential is measured over exactly the same window. | 23 | carried | 'and it is measured over exactly the same window.' in `merged.md` -- The reference text directly states this claim. |
| 41 | The tier is set on the credential when it is issued. | 23 | carried | 'The tier is set on the credential when it is issued' in `merged.md` -- The reference text directly states this claim. |
| 42 | The tier cannot be asked for per call. | 23 | carried | 'and cannot be asked for per call.' in `merged.md` -- The reference text directly states this claim. |
| 43 | Nothing else about the two tiers differs in any way. | 23 | carried | 'Nothing else about the two tiers differs in any way.' in `merged.md` -- The reference text directly states this claim. |
| 45 | Nobody at the far end will assemble that argument on a caller's behalf. | 25 | carried | 'and nobody at the far end will assemble that argument on its behalf.' in `merged.md` -- The reference text directly states this claim. |
| 46 | The log line should carry the credential, the window and the wait. | 25 | carried | 'The log line should carry the credential, the window and the wait.' in `merged.md` -- The reference text directly states this claim. |
| 47 | The gateway refuses requests for three reasons. | 29 | carried | 'The gateway refuses a request for three reasons' in `merged.md` -- The reference text directly states this claim. |
| 48 | Only one of the three reasons is a cap. | 29 | carried | 'and only one of them is the one above.' in `merged.md` -- The reference text directly states this claim. |
| 49 | A credential may be suspended. | 29 | carried | 'A credential may be suspended' in `merged.md` -- The reference text directly states this claim. |
| 50 | A route may be closed for maintenance. | 29 | carried | 'a route may be closed for maintenance' in `merged.md` -- The reference text directly states this claim. |
| 51 | A body may exceed the 5 megabyte limit. | 29 | carried | 'or a body may exceed the 5 megabyte limit.' in `merged.md` -- The reference text directly states this claim. |
| 52 | None of those three reasons clears itself by waiting for a stated number of seconds. | 29 | carried | 'None of those three clears itself by waiting for a stated number of seconds.' in `merged.md` -- The reference text directly states this claim. |
| 53 | A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `merged.md` -- The reference text directly states this claim. |
| 54 | The log afterwards shows nothing at all except a long run of refusals when retrying against a suspended credential. | 31 | carried | 'and the log afterwards shows nothing at all except a long run of refusals.' in `merged.md` -- The reference text directly states this claim. |
| 55 | Reading the status code rather than the class it belongs to separates the two cases. | 31 | carried | 'Reading the status code rather than the class it belongs to is what separates the two cases' in `merged.md` -- The reference text directly states this claim. |
| 56 | Reading the status code rather than the class it belongs to costs one comparison. | 31 | carried | 'and it costs one comparison.' in `merged.md` -- The reference text directly states this claim. |
| 57 | A cap can be raised. | 35 | carried | 'A cap can be raised' in `merged.md` -- The reference text directly states this claim. |
| 58 | The number of caps raised without a measurement behind them is 0. | 35 | carried | 'and the number of caps raised without a measurement behind them is 0.' in `merged.md` -- The reference text directly states this claim. |
| 59 | A burst is cheaper to smooth than it is to serve at its peak. | 35 | carried | 'a burst is cheaper to smooth than it is to serve at its peak.' in `merged.md` -- The reference text directly states this claim. |
| 60 | A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all. | 35 | carried | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `merged.md` -- The reference text directly states this claim. |
| 61 | Requests reach the platform team through the usual channel. | 37 | carried | 'Requests reach the platform team through the usual channel' in `merged.md` -- The reference text directly states this claim. |
| 62 | Requests are answered within two working days. | 37 | carried | 'and they are answered within two working days.' in `merged.md` -- The reference text directly states this claim. |
| 63 | There is no expedited path. | 37 | carried | 'There is no expedited path' in `merged.md` -- The reference text directly states this claim. |
| 64 | There is no exception list. | 37 | carried | 'and no exception list.' in `merged.md` -- The reference text directly states this claim. |

### `source_b.md` -- 61 claim(s): 9 dropped, 1 contradicted, 5 carried in part, 46 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 5 | The gateway doesn't disclose the start of the window. | 5 (unverified) | dropped | The reference text does not mention whether the gateway discloses the start of the window. |
| 10 | A caller that needs more than that is almost always doing batch work under an interactive credential. | 7 | dropped | The reference text does not state that callers needing more than 100 are almost always doing batch work under an interactive credential. |
| 25 | The cause of the refusal is an entirely different one. | 19 | dropped | The reference text does not state that the cause of refusal is an entirely different one. |
| 45 | Two of the three have nothing to do with how much traffic a caller has sent in the window it is currently in. | 29 | dropped | The reference text lists three refusal reasons but does not specify how many relate to traffic volume in the current window. |
| 48 | A request body over the 5 megabyte limit is refused before it has been read at all. | 29 | dropped | The reference text mentions the 5 megabyte body limit but does not specify when the refusal occurs relative to reading. |
| 51 | The wasted budget is the caller's own. | 31 (unverified) | dropped | While the text describes budget being spent, it does not explicitly state the budget is the caller's own. |
| 53 | It is available to almost everybody. | 33 | dropped | The reference text does not state that moving work to quieter hours is available to almost everybody. |
| 55 | A cap cannot be raised but on the strength of an assertion that the current one is too small. | 33 | dropped | The reference text states caps need measurements behind them but does not specify they must be assertions of the cap being too small. |
| 61 | Chasing it doesn't make it take fewer. | 37 (unverified) | dropped | The reference text notes no expedited path exists but does not explicitly state that attempting to expedite will not reduce the timeframe. |
| 42 | The counts are the whole of the argument. | 25 | contradicted | 'Bring a week of refusal counts, the shape of the traffic across the day, and the deadline that traffic is serving' in `merged.md` -- The reference text requires counts plus traffic shape plus deadline, contradicting that counts alone are sufficient. |
| 18 | It repeats the cap, the window and the tier as plain fields. | 13 | carried in part | 'It names the cap and the tier as well' in `merged.md` -- Text states these are named but does not specify they are 'plain fields' specifically. |
| 26 | Anything computed on the client side is a guess. | 19 | carried in part | 'A wait derived on the client side is a guess' in `merged.md` -- Text specifies 'wait' not 'anything computed', limiting the claim. |
| 32 | A caller that folds all four into one branch will retry hardest during exactly the incident the cap was installed to survive. | 21 | carried in part | 'A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive.' in `merged.md` -- Text says 'every non-success' not specifically 'all four' status codes mentioned. |
| 35 | The batch counting scheme is not a separate counting scheme. | 23 | carried in part | 'and it is measured over exactly the same window.' in `merged.md` -- Text states the window is the same but does not explicitly say the counting scheme is not separate. |
| 56 | The team wants to know whether the load is smooth or bursty before it looks at the number at all. | 35 | carried in part | 'The platform team looks at whether the load is smooth or bursty' in `merged.md` -- The text states the team examines load characteristics but does not explicitly specify the temporal order of investigation. |
| 1 | Every credential has a cap of its own. | 3 | carried | 'Every credential has a cap.' in `merged.md` -- Same meaning as 'every credential has a cap of its own' in context. |
| 2 | When the cap is spent the gateway answers 429 at the edge, without troubling the service behind it. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge — without waking the service behind it' in `merged.md` -- 'without waking' conveys same meaning as 'without troubling'. |
| 3 | Requests are counted against the credential rather than the connection. | 5 | carried | 'Requests are counted against the credential that presented them...and never against a connection.' in `merged.md`, **transcription_error** -- The text states requests are counted against credential, not connection. |
| 4 | Requests are counted over a fixed window of 60 seconds. | 5 | carried | 'over a fixed window of 60 seconds' in `merged.md` -- The reference text directly states this claim. |
| 6 | The count follows the credential wherever the caller happens to put it. | 5 | carried | 'The count follows the credential wherever the caller happens to put it' in `merged.md` -- The reference text directly states this claim. |
| 7 | The count follows the credential including across hosts. | 5 | carried | 'including across hosts.' in `merged.md` -- The reference text directly states this claim. |
| 8 | A caller spread over many worker processes is throttled at the same point a single process would have been. | 5 | carried | 'A client spread across multiple worker processes is throttled at exactly the point one process would have been' in `merged.md` -- 'many' and 'multiple' convey the same meaning in this context. |
| 9 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- The reference text directly states this claim. |
| 11 | Callers that retry immediately are most of the reason the cap is there. | 7 | carried | 'Callers that retry at once are the largest single reason the cap is there at all.' in `merged.md` -- 'immediately' and 'at once' have identical meaning. |
| 12 | The header is called Retry-After. | 11 | carried | 'The refusal carries a Retry-After header.' in `merged.md` -- The reference text directly states this claim. |
| 13 | Its value is a whole number of seconds. | 11 | carried | 'Its value is a whole number of seconds to wait.' in `merged.md` -- The text includes the stated claim that it is a whole number of seconds. |
| 14 | It is present on every refusal the gateway sends. | 11 | carried | 'The refusal carries a Retry-After header.' in `merged.md` -- In a documentation section on how to read a refusal, stating the refusal carries this header means it is present on refusals. |
| 15 | Waiting that long and then continuing is the entire contract. | 11 | carried | 'Waiting that long and then continuing is the whole of the contract' in `merged.md` -- 'entire' and 'whole' convey the same meaning. |
| 16 | Nobody at this end is keeping score. | 11 | carried | 'The gateway keeps no memory of who backed off politely' in `merged.md` -- Gateway not keeping score is equivalent to not keeping memory of who backed off. |
| 17 | The response body is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- The reference text directly states this claim. |
| 19 | None of those fields is a substitute for the header. | 13 | carried | 'None of those fields is a substitute for the header' in `merged.md` -- The reference text directly states this claim. |
| 20 | There are four rules. | 17 | carried | 'Four rules' in `merged.md` -- The reference text directly states there are four rules. |
| 21 | The order they are given in is the order to apply them. | 17 | carried | 'given in the order they should be applied.' in `merged.md` -- The reference text directly states this claim. |
| 22 | The gateway has already done that arithmetic. | 19 | carried | 'The gateway has already done that arithmetic' in `merged.md` -- The reference text directly states this claim. |
| 23 | It did it with information the caller cannot see. | 19 | carried | 'with information the caller does not have' in `merged.md` -- 'cannot see' conveys same meaning as 'does not have'. |
| 24 | On the 503 path the same rule holds. | 19 | carried | 'and it does the same on the 503 path.' in `merged.md` -- The reference text directly states this claim. |
| 27 | The safe set to retry is a smaller set than the set of responses that aren't a success. | 21 (unverified) | carried | 'A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive.' in `merged.md` -- This necessarily entails that safe retry set is smaller than all non-success responses. |
| 28 | A 200 needs nothing. | 21 | carried | 'A 200 wants nothing' in `merged.md` -- 'needs' and 'wants' have identical meaning in this context. |
| 29 | A 429 needs the stated wait. | 21 | carried | 'a 429 wants the stated wait' in `merged.md` -- 'needs' and 'wants' have identical meaning in this context. |
| 30 | A 500 can be retried once that wait has passed. | 21 | carried | 'a 500 may be retried once that wait has passed' in `merged.md` -- 'can' and 'may' have identical meaning in this context. |
| 31 | A 503 means the platform itself is overloaded. | 21 | carried | 'a 503 is the overload path.' in `merged.md` -- 'overload path' means the platform itself is overloaded. |
| 33 | A batch credential is allowed 1000 requests in a window. | 23 | carried | 'and a credential marked for batch work is allowed 1000 in the same window.' in `merged.md` -- The reference text directly states this claim. |
| 34 | Which is 50 times the default. | 23 | carried | 'which is 50 times the default allowance' in `merged.md` -- The reference text directly states this claim. |
| 36 | The window, the header and the body are identical to the interactive case. | 23 | carried | 'The window, the header and the body are identical to the interactive case' in `merged.md` -- The reference text directly states this claim. |
| 37 | A client written for one tier needs no change at all to run against the other. | 23 | carried | 'a client written for one tier needs no change at all to run against the other' in `merged.md` -- The reference text directly states this claim in the section describing batch tier handling. |
| 38 | Nothing else about the batch tier differs from the default. | 23 | carried | 'Nothing else about the two tiers differs in any way' in `merged.md` -- The reference text explicitly states this in the batch tier section. |
| 39 | Keep the log for at least a week. | 25 | carried | 'Keep the log for at least a week' in `merged.md` -- The reference text states this requirement exactly in the section on how to retry well. |
| 40 | A caller that cannot say how often it was refused can't make a case for a larger cap. | 25 (unverified) | carried | 'A caller that cannot say how often it was refused cannot argue for a larger cap' in `merged.md` -- The reference text states this claim with the same meaning in the cap increase section. |
| 41 | The platform team won't assemble that case on its behalf. | 25 (unverified) | carried | 'nobody at the far end will assemble that argument on its behalf' in `merged.md` -- The reference text states this as part of describing the caller's responsibility to provide data. |
| 43 | The gateway refuses a request for three separate reasons. | 29 | carried | 'The gateway refuses a request for three reasons' in `merged.md` -- The reference text explicitly states this in the section on other refusals. |
| 44 | Only one of them is a cap. | 29 | carried | 'only one of them is the one above' in `merged.md` -- The reference text states that of the three reasons, only one is the cap-related refusal. |
| 46 | A credential can be suspended. | 29 | carried | 'A credential may be suspended' in `merged.md` -- The reference text lists suspension of a credential as one of three refusal reasons. |
| 47 | A route can be closed while it is being repaired. | 29 | carried | 'a route may be closed for maintenance' in `merged.md` -- The reference text states routes may be closed for maintenance; repair is a type of maintenance. |
| 49 | A loop retrying against a suspended credential burns its whole budget and reaches nothing. | 31 | carried | 'spends its whole budget without ever reaching the service' in `merged.md` -- The reference text describes this outcome for retry loops against suspended credentials. |
| 50 | The log afterwards shows a long run of refusals and no successes at all. | 31 | carried | 'the log afterwards shows nothing at all except a long run of refusals' in `merged.md` -- The reference text explicitly states what the log shows in this scenario. |
| 52 | A caller that can move half its work to a quieter hour usually finds it doesn't need a larger cap in the first place. | 33 (unverified) | carried | 'usually gets what it needs without any change to the cap at all' in `merged.md` -- The reference text states that shifting work to quieter hours usually achieves the caller's goals without a cap increase. |
| 54 | A cap can be raised. | 33 | carried | 'A cap can be raised' in `merged.md` -- The reference text explicitly opens the cap increase section with this statement. |
| 57 | A burst is cheaper to smooth out than it is to serve at its peak. | 35 | carried | 'a burst is cheaper to smooth than it is to serve at its peak' in `merged.md` -- The reference text states this directly in the discussion of load shape. |
| 58 | Requests go to the platform team through the usual channel. | 35 | carried | 'Requests reach the platform team through the usual channel' in `merged.md` -- The reference text states requests reach the team through the usual channel; reach and go convey the same meaning. |
| 59 | There is no expedited path. | 37 | carried | 'There is no expedited path' in `merged.md` -- The reference text explicitly states this as a constraint on the process. |
| 60 | An answer takes two working days. | 37 | carried | 'they are answered within two working days' in `merged.md` -- The reference text states the timeframe for responses. |

### `merged.md` -- 53 claim(s): 0 invented, 0 contradicted, 0 supported in part, 53 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Every credential has a cap | supported | `source_a.md` | 'Every credential has a cap.' in `source_a.md` -- Source A states this claim directly. |
| 2 | When a credential's cap is spent, the gateway answers 429 at the edge | supported | `source_a.md` | 'When that cap is spent the gateway answers 429 at the edge' in `source_a.md` -- Source A states this claim directly. |
| 3 | Requests are counted against the credential that presented them over a fixed window of 60 seconds | supported | `source_a.md` | 'Requests are counted against the credential that presented them, over a fixed window of 60 seconds' in `source_a.md` -- Source A states this claim directly. |
| 4 | Requests are never counted against a connection | supported | `source_a.md` | 'and never against a connection.' in `source_a.md` -- Source A states this claim directly. |
| 5 | Opening a second socket therefore buys a caller nothing | supported | `source_a.md` | 'Opening a second socket therefore buys a caller nothing.' in `source_a.md` -- Source A states this claim directly. |
| 6 | The count follows the credential wherever the caller happens to put it, including across hosts | supported | `source_b.md` | 'The count follows the credential wherever the caller happens to put it, including across hosts.' in `source_b.md` -- Source B states this claim directly. |
| 7 | A client spread across multiple worker processes is throttled at exactly the point one process would have been | supported | `source_a.md` | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `source_a.md` -- Source A states this claim directly. |
| 8 | A client spread across multiple worker processes pays for the extra file descriptors as well | supported | `source_a.md` | 'and pays for the extra file descriptors as well.' in `source_a.md` -- Source A states this claim directly. |
| 9 | The default allowance is 100 requests in a window | supported | `source_a.md` | 'The default allowance is 100 requests in a window' in `source_a.md` -- Source A states this claim directly. |
| 10 | A credential marked for batch work is allowed 1000 requests in the same window | supported | `source_a.md` | 'and a credential marked for batch work is allowed 1000 in the same window.' in `source_a.md` -- Source A states this claim directly. |
| 11 | Callers that retry at once are the largest single reason the cap is there at all | supported | `source_a.md` | 'Callers that retry at once are the largest single reason the cap is there at all.' in `source_a.md` -- Source A states this claim directly. |
| 12 | The refusal carries a Retry-After header | supported | `source_a.md` | 'The refusal carries a Retry-After header.' in `source_a.md` -- Source A states this claim directly. |
| 13 | The value of the Retry-After header is a whole number of seconds to wait | supported | `source_a.md` | 'Its value is a whole number of seconds to wait.' in `source_a.md` -- Source A states this claim directly. |
| 14 | The gateway keeps no memory of who backed off politely | supported | `source_a.md` | 'The gateway keeps no memory of who backed off politely' in `source_a.md` -- Source A states this claim directly. |
| 15 | Waiting longer than the Retry-After header asks earns a caller no credit at all | supported | `source_a.md` | 'Waiting longer than the header asks earns a caller no credit at all.' in `source_a.md` -- Source A states this claim directly. |
| 16 | The body of the refusal is JSON | supported | `source_a.md` | 'The body of the refusal is JSON' in `source_a.md` -- Source A states this claim directly. |
| 17 | The body of the refusal names what the gateway calls the "window" it counted in | supported | `source_a.md` | 'and it names what the gateway calls the "window" it counted in.' in `source_a.md`, **transcription_error** -- Source A states this claim directly. |
| 18 | The body of the refusal names the cap and the tier | supported | `source_a.md` | 'It names the cap and the tier as well.' in `source_a.md` -- Source A states this claim directly. |
| 19 | The gateway has already done that arithmetic with information the caller does not have | supported | `source_a.md` | 'The gateway has already done that arithmetic, with information the caller does not have' in `source_a.md` -- Source A states this claim directly. |
| 20 | The gateway does the same arithmetic on the 503 path | supported | `source_a.md` | 'and it does the same on the 503 path.' in `source_a.md` -- Source A states this claim directly. |
| 21 | A 200 wants nothing | supported | `source_a.md` | 'A 200 wants nothing' in `source_a.md` -- Source A states this claim directly. |
| 22 | A 429 wants the stated wait | supported | `source_a.md` | 'a 429 wants the stated wait' in `source_a.md` -- Source A states this claim directly. |
| 23 | A 500 may be retried once that wait has passed | supported | `source_a.md` | 'a 500 may be retried once that wait has passed' in `source_a.md` -- Source A states this claim directly. |
| 24 | A 503 is the overload path | supported | `source_a.md` | 'and a 503 is the overload path.' in `source_a.md` -- Source A states this claim directly. |
| 25 | The four cases are not interchangeable | supported | `source_a.md` | 'The four cases are not interchangeable.' in `source_a.md` -- Source A states this claim directly. |
| 26 | A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive | supported | `source_a.md` | 'A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive.' in `source_a.md` -- Source A states this claim directly. |
| 27 | A batch credential is allowed 1000 requests in a window | supported | `source_b.md` | 'A batch credential is allowed 1000 requests in a window' in `source_b.md` -- Source B states this claim directly. |
| 28 | 1000 is 50 times the default allowance | supported | `source_b.md` | 'which is 50 times the default' in `source_b.md` -- Source B states this claim directly. |
| 29 | A batch credential is measured over exactly the same window as the interactive case | supported | `source_b.md` | 'The window, the header and the body are identical to the interactive case' in `source_b.md` -- Source B states this claim directly. |
| 30 | The tier is set on the credential when it is issued | supported | `source_a.md` | 'The tier is set on the credential when it is issued' in `source_a.md` -- Source A states this claim directly. |
| 31 | The tier cannot be asked for per call | supported | `source_a.md` | 'and cannot be asked for per call.' in `source_a.md` -- Source A states this claim directly. |
| 32 | The window, the header and the body are identical to the interactive case | supported | `source_b.md` | 'The window, the header and the body are identical to the interactive case' in `source_b.md` -- Source B states this claim directly. |
| 33 | A client written for one tier needs no change at all to run against the other tier | supported | `source_b.md` | 'so a client written for one tier needs no change at all to run against the other.' in `source_b.md` -- Source B states this claim directly. |
| 34 | Nothing else about the two tiers differs in any way | supported | `source_a.md` | 'Nothing else about the two tiers differs in any way.' in `source_a.md` -- Source A states this claim directly. |
| 35 | Nobody at the far end will assemble an argument for a larger cap on a caller's behalf | supported | `source_a.md` | 'nobody at the far end will assemble that argument on its behalf.' in `source_a.md` -- Source A states this claim directly. |
| 36 | Not all refusals are due to caps | supported | `source_a.md` | 'Not all are caps.' in `source_a.md` -- Source A states this claim directly. |
| 37 | The gateway refuses a request for three reasons | supported | `source_a.md` | 'The gateway refuses a request for three reasons and only one of them is the one above.' in `source_a.md` -- Source A states this claim directly. |
| 38 | Only one of the three reasons the gateway refuses a request is the cap | supported | `source_a.md` | 'The gateway refuses a request for three reasons and only one of them is the one above.' in `source_a.md` -- Source A states this claim directly. |
| 39 | A credential may be suspended | supported | `source_a.md` | 'A credential may be suspended' in `source_a.md` -- Source A states this claim directly. |
| 40 | A route may be closed for maintenance | supported | `source_a.md` | 'a route may be closed for maintenance' in `source_a.md` -- Source A states this claim directly. |
| 41 | A body may exceed the 5 megabyte limit | supported | `source_a.md` | 'or a body may exceed the 5 megabyte limit.' in `source_a.md` -- Source A states this claim directly. |
| 42 | None of those three reasons clears itself by waiting for a stated number of seconds | supported | `source_a.md` | 'None of those three clears itself by waiting for a stated number of seconds.' in `source_a.md` -- Source A states this claim directly. |
| 43 | A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service | supported | `source_a.md` | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `source_a.md` -- Source A states this claim directly. |
| 44 | The log afterwards shows nothing except a long run of refusals | supported | `source_a.md` | 'and the log afterwards shows nothing at all except a long run of refusals.' in `source_a.md` -- Source A states this claim directly. |
| 45 | A cap can be raised | supported | `source_a.md` | 'A cap can be raised' in `source_a.md` -- Source A states this claim directly. |
| 46 | The number of caps raised without a measurement behind them is 0 | supported | `source_a.md` | 'the number of caps raised without a measurement behind them is 0.' in `source_a.md` -- Source A states this claim directly. |
| 47 | A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all | supported | `source_a.md` | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `source_a.md` -- Source A states this claim directly. |
| 48 | The platform team looks at whether the load is smooth or bursty | supported | `source_a.md` | 'The platform team looks at whether the load is smooth or bursty' in `source_a.md` -- Source A states this claim directly. |
| 49 | A burst is cheaper to smooth than it is to serve at its peak | supported | `source_a.md` | 'a burst is cheaper to smooth than it is to serve at its peak.' in `source_a.md` -- Source A states this claim directly. |
| 50 | Requests reach the platform team through the usual channel | supported | `source_a.md` | 'Requests reach the platform team through the usual channel' in `source_a.md` -- Source A states this claim directly. |
| 51 | Requests are answered within two working days | supported | `source_a.md` | 'they are answered within two working days.' in `source_a.md` -- Source A states this claim directly. |
| 52 | There is no expedited path | supported | `source_a.md` | 'There is no expedited path and no exception list.' in `source_a.md` -- Source A states this claim directly. |
| 53 | There is no exception list | supported | `source_a.md` | 'There is no expedited path and no exception list.' in `source_a.md` -- Source A states this claim directly. |

## Structure

**9** mechanical check(s) over **104** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **53** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **125**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 9 run(s) over 54 attributed segment(s) — sources interleaved. 6 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

`[-...-]` is what the source said and `{+...+}` is what the merge says.

### Absent and undeclared — in a source, not in the merge, and no record explains it

- `b52` (`source_b.md`) — 'An answer takes two working days, and chasing it doesn’t make it take fewer.' is not in the merge and no disposition record explains it (nearest merge segment m53 at 0.38)

  ```text
  In the source: An answer takes two working days, and chasing it doesn’t make it take fewer.
  ```

### Reworded and undeclared — in the merge in altered wording, and no record explains it. At off this also covers layout: a segment whose source line breaks the merge ran together is altered and undeclared, and 380 reuses this kind rather than moving FINDING_KINDS off 12

- `a16` (`source_a.md`) — 'The body of the refusal is JSON, and it names what the gateway calls the “window” it counted in.' is reworded in the merge and no disposition record explains it (nearest merge segment m17 at 0.98)

  ```text
  In the source: The body of the refusal is JSON, and it names what the gateway calls the “window” it counted in.
  In the merge:  The body of the refusal is JSON, and it names what the gateway calls the "window" it counted in.
  What changed:  The body of the refusal is JSON, and it names what the gateway calls the [-“window”-] {+"window"+} it counted in.
  ```

### Declared gone, still here — a record says the content departed and the merge carries the segment unchanged

- `b7` (`source_b.md`) — 'The count follows the credential wherever the caller happens to put it, including across hosts.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: The count follows the credential wherever the caller happens to put it, including across hosts.
  In the merge:  The count follows the credential wherever the caller happens to put it, including across hosts.
  ```
- `b32` (`source_b.md`) — 'The window, the header and the body are identical to the interactive case, so a client written for one tier needs no change at all to run against the other.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: The window, the header and the body are identical to the interactive case, so a client written for one tier needs no change at all to run against the other.
  In the merge:  Nothing else about the two tiers differs in any way.
  ```

### Over budget — declared loss past the ceiling

- 4 of 104 segments are declared dropped (3.8%), over the 3% budget

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

> **Over budget.** The merge declared **4** drop(s) of 104 source segment(s), **3.8%**, over the 3% budget: past that share the omissions are the finding, whatever each one says about itself.

## Declarations

The merge declared **55** departure(s) from its sources. Checking them confirms 27, rejects 14, and leaves 14 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 4 of 104 source segment(s) declared gone, **3.8%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a6` | reworded | Changed specific count to general term for clarity. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-009 came back PARTIAL, A-010 came back PARTIAL (`A-009`, `A-010`) |
| `a18` | reworded | Incorporated detail from source_b about client-side disagreement. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-025`, `A-026`) |
| `a32` | reworded | Specified numeric allowance and ratio for precision. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-039`, `A-040`) |
| `a36` | reworded | Removed time reference for general applicability. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-044 came back PARTIAL (`A-044`) |
| `b1` | superseded | Base document title chosen for better coverage. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Rate limiting and the 429 contract for gateway clients' and says so (no claim traced to it) |
| `b2` | duplicate | Same fact stated in a2. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-001`) |
| `b3` | subsumed | Content absorbed in opening explanation. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-002`) |
| `b4` | dropped | Meta-commentary on document drafting, not core guidance. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b5` | subsumed | Factual content covered by a4. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-003`, `B-004`) |
| `b6` | subsumed | Same guidance in first paragraph. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b7` | subsumed | Additional detail incorporated into first paragraph. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-006`, `B-007`) |
| `b8` | subsumed | Same guidance as a6 in first paragraph. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-008`) |
| `b9` | subsumed | Allowance information covered by a7. | **rejected** | declared 'subsumed', which predicts SUPPORTED; B-010 came back MISSING (`B-010`) |
| `b10` | subsumed | Same explanation of refusals in first section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b11` | subsumed | Retry behavior explained in a10. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-011`) |
| `b12` | subsumed | Header identification covered by a12. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b13` | subsumed | Header format explained in a13. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-012`) |
| `b14` | subsumed | Contract defined in a14. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-013`, `B-014`) |
| `b15` | subsumed | No reward for excess waiting explained in a15. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-015`) |
| `b16` | subsumed | Response body described in a16-a17. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-016`) |
| `b17` | reconciled | Phrase combined with a18 to convey both sources' cautions. | **rejected** | declared 'reconciled', which predicts SUPPORTED; B-018 came back PARTIAL (`B-018`) |
| `b18` | superseded | a19 provides more detail about body purpose. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-019`) |
| `b19` | superseded | Base section heading used instead. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b20` | superseded | a21 states the same introduction. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b21` | superseded | a22 chosen for its emphatic phrasing. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-020`, `B-021`) |
| `b22` | subsumed | Same reasoning in a23. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b23` | subsumed | 503 path rule covered in a23. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-022`, `B-023`) |
| `b24` | subsumed | Same concept in a24. | **rejected** | declared 'subsumed', which predicts SUPPORTED; B-025 came back MISSING (`B-025`) |
| `b25` | subsumed | Same conclusion in a25. | **rejected** | declared 'subsumed', which predicts SUPPORTED; B-026 came back PARTIAL (`B-026`) |
| `b26` | superseded | a26 chosen for conciseness. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b27` | subsumed | Same status code guidance in a27. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b28` | subsumed | Same danger identified in a29. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-028`, `B-029`, `B-030`, `B-031`) |
| `b29` | subsumed | Same avoidance recommendation in a30. | **rejected** | declared 'subsumed', which predicts SUPPORTED; B-032 came back PARTIAL (`B-032`) |
| `b30` | reconciled | Numeric detail from b30 combined with a32. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b31` | reconciled | Compatibility assurance from b31 added to rule 3. | **rejected** | declared 'reconciled', which predicts SUPPORTED; B-035 came back PARTIAL (`B-035`) |
| `b32` | subsumed | Same statement in a34. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-036`, `B-037`) |
| `b33` | reconciled | Retention requirement from b33 combined with a35-a37. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-038`) |
| `b34` | subsumed | Same guidance in a36. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-039`) |
| `b35` | dropped | Philosophical point about argument strength not needed. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'dropped' is what happened to it (no claim traced to it) |
| `b36` | superseded | Base section heading used. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-042`) |
| `b37` | subsumed | Same enumeration in a39. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b38` | dropped | Distinction between traffic and non-traffic reasons implicit. | **rejected** | declared 'dropped', which predicts MISSING; B-043 came back SUPPORTED, B-044 came back SUPPORTED (`B-043`, `B-044`) |
| `b39` | superseded | a40 lists the same three reasons. | **rejected** | declared 'superseded', which predicts SUPPORTED or CONTRADICTED or PARTIAL; B-045 came back MISSING (`B-045`) |
| `b40` | subsumed | Same point in a42. | **rejected** | declared 'subsumed', which predicts SUPPORTED; B-048 came back MISSING (`B-048`) |
| `b41` | subsumed | Same warning in a43. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b42` | subsumed | Same consequence in a43. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-049`) |
| `b43` | superseded | a49 provides same advice with clearer framing. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-050`) |
| `b44` | dropped | Availability claim not essential to core guidance. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'dropped' is what happened to it (no claim traced to it) |
| `b45` | subsumed | Conditional cap increase in a46. | **rejected** | declared 'subsumed', which predicts SUPPORTED; B-053 came back MISSING (`B-053`) |
| `b46` | superseded | a47 states the same data requirements. | **rejected** | declared 'superseded', which predicts SUPPORTED or CONTRADICTED or PARTIAL; B-055 came back MISSING (`B-055`) |
| `b47` | subsumed | Load analysis in a48. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b48` | subsumed | Burst vs smooth analysis in a48. | **rejected** | declared 'subsumed', which predicts SUPPORTED; B-056 came back PARTIAL (`B-056`) |
| `b49` | subsumed | Channel and timing in a50. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-057`) |
| `b50` | subsumed | No expedited path stated in a51. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-058`) |
| `b51` | superseded | a50 specifies timing explicitly. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-059`) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | bbb0be176544 (command) -- Claude Code - Haiku |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | haiku -> claude-haiku-4-5-20251001 |
| Model (decompose) | haiku -> claude-haiku-4-5-20251001 |
| Model (verify) | haiku -> claude-haiku-4-5-20251001 |
| Structured output | prompt (probed) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile subscription, effort decompose=low, merge=medium, verify=low |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 6cc1b1703658 |
| Calls | 9 live, 0 cached, 0 replayed |
| Tokens | unknown (9 call(s) reported no usage) |
| Cost | unmeasured (9 call(s) reported no tokens, so no figure can be derived) |
| Schema repairs | 2 |
| Isolation | decompose, merge, verify: safe mode, no tools |
| Errors | 0 |
| Duration | 1200.7s |
| Generated | 2026-09-26T15:54:22+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `5afca8163bfa` |
| Prompt | `prompts/verify_reverse.md` `cb2face6b7f4` |

> **Document content was handed to a program on this machine (`Claude Code - Haiku`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
