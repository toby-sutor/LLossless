## Verdict

**12 finding(s).** In the claims: 7 partially dropped. In the structure: 2 undeclared absence, 1 undeclared rewording, 1 unresolved replacement, 1 verbatim violation.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 72 |
| Claims extracted from `source_a.md` | 60 |
| Claims extracted from `source_b.md` | 67 |
| Forward — source claims accounted for in the merge | **120/127** |
| Forward — carried only in part | 7 |
| Forward — `source_a.md` claims accounted for | **60/60** |
| Forward — `source_b.md` claims accounted for | **60/67** (7 in part) |
| Reverse — merge claims found in a source | **72/72** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **197/199** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Partly dropped — the merge carries some of this claim

- **B-021** (`source_b.md:13`) — The response body repeats the cap as a plain field.
  - evidence: 'It names the cap and the tier as well.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The body names the cap, but the text does not establish that it is a plain field.
- **B-022** (`source_b.md:13`) — The response body repeats the window as a plain field.
  - evidence: 'It names what the gateway calls the “window” it counted in.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The body names the window, but the text does not establish that it is a plain field.
- **B-023** (`source_b.md:13`) — The response body repeats the tier as a plain field.
  - evidence: 'It names the cap and the tier as well.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The body names the tier, but the text does not establish that it is a plain field.
- **B-031** (`source_b.md:19`) — Anything computed on the client side is a guess.
  - evidence: 'A wait derived on the client side is a guess about a counter it cannot see.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text calls a client-derived wait a guess, but does not say that anything computed client-side is a guess.
- **B-035** (`source_b.md:21`) — A 503 means the platform itself is overloaded.
  - evidence: 'and a 503 is the overload path.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text identifies 503 as the overload path, but does not explicitly say the platform itself is overloaded.
- **B-036** (`source_b.md:21`) — A caller that folds all four responses into one branch will retry hardest during the incident the cap was installed to survive.
  - evidence: 'A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text supports folding non-success responses into one branch, but does not say the client folds all four responses into that branch.
- **B-062** (`source_b.md:35`) — The team wants to know whether the load is smooth or bursty before it looks at the number.
  - evidence: 'The platform team looks at whether the load is smooth or bursty' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text says the team considers whether load is smooth or bursty, but does not state that this happens before it looks at the number.

## Length capped

- `$.dispositions[12].reason` was 81 characters, over the 80-character cap; capped to fit
- `$.dispositions[25].reason` was 81 characters, over the 80-character cap; capped to fit
- `$.dispositions[32].reason` was 86 characters, over the 80-character cap; capped to fit

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 60 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 60 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Every credential has a cap. | 3 | carried | 'Every credential has a cap.' in `merged.md` -- The text directly states that every credential has a cap. |
| 2 | When a credential's cap is spent, the gateway answers 429 at the edge. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge' in `merged.md` -- The text states that spending the cap results in a 429 response at the edge. |
| 3 | When a credential's cap is spent, the gateway answers without waking the service behind it. | 3 | carried | 'without waking the service behind it' in `merged.md` -- The text states that the edge refusal does not wake the service behind the gateway. |
| 4 | Requests are counted against the credential that presented them. | 5 | carried | 'Requests are counted against the credential that presented them' in `merged.md` -- The text directly identifies the presenting credential as the basis for counting requests. |
| 5 | Requests are counted over a fixed window of 60 seconds. | 5 | carried | 'over a fixed window of 60 seconds' in `merged.md` -- The text states that requests are counted over a fixed 60-second window. |
| 6 | Requests are never counted against a connection. | 5 | carried | 'and never against a connection' in `merged.md` -- The text explicitly says requests are never counted against a connection. |
| 7 | Opening a second socket does not increase a caller's allowance. | 5 | carried | 'Opening a second socket therefore buys a caller nothing.' in `merged.md` -- The text states that opening another socket provides no benefit, so it does not increase the allowance. |
| 8 | A client spread across eight worker processes is throttled at exactly the point one process would have been. | 5 | carried | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `merged.md` -- The text directly states that eight processes are throttled at the same point as one process. |
| 9 | A client spread across eight worker processes pays for the extra file descriptors. | 5 | carried | 'and pays for the extra file descriptors as well.' in `merged.md` -- The text states that the multi-process client pays for the extra file descriptors. |
| 10 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- The text directly gives the default allowance as 100 requests per window. |
| 11 | A credential marked for batch work is allowed 1000 requests in the same window. | 7 | carried | 'a credential marked for batch work is allowed 1000 in the same window.' in `merged.md` -- The text gives a batch credential an allowance of 1000 in the same window. |
| 12 | A refusal is not an outage. | 7 | carried | 'A refusal is not an outage' in `merged.md` -- The text explicitly says a refusal is not an outage. |
| 13 | The platform declines to spend capacity that has already been promised to somebody else. | 7 | carried | 'It is the platform declining to spend capacity that has already been promised to somebody else' in `merged.md` -- The text directly describes the refusal as declining to spend capacity promised to someone else. |
| 14 | Callers that retry at once are the largest single reason the cap is there. | 7 | carried | 'Callers that retry at once are the largest single reason the cap is there at all.' in `merged.md` -- The text identifies callers that retry immediately as the largest single reason for the cap. |
| 15 | The refusal carries a Retry-After header. | 11 | carried | 'The refusal carries a Retry-After header.' in `merged.md` -- The text directly states that the refusal carries a Retry-After header. |
| 16 | The Retry-After header's value is a whole number of seconds to wait. | 11 | carried | 'Its value is a whole number of seconds, and it is present on every refusal the gateway sends. Waiting that long and then continuing is the entire contract' in `merged.md` -- The text says the header value is a whole number of seconds and instructs the caller to wait that long. |
| 17 | The gateway keeps no memory of who backed off politely. | 11 | carried | 'The gateway keeps no memory of who backed off politely' in `merged.md` -- The text directly states that the gateway keeps no memory of callers who backed off politely. |
| 18 | Waiting longer than the Retry-After header asks earns a caller no credit. | 11 | carried | 'so waiting longer than the header asks earns a caller no credit at all.' in `merged.md` -- The text explicitly says waiting longer than the header requests earns no credit. |
| 19 | The body of the refusal is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- The text directly states that the refusal body is JSON. |
| 20 | The refusal body names the window the gateway counted in. | 13 (unverified) | carried | 'it names what the gateway calls the “window” it counted in.' in `merged.md` -- The text states that the body names the window in which the gateway counted requests. |
| 21 | The refusal body names the cap. | 13 | carried | 'It names the cap' in `merged.md` -- The text directly says that the body names the cap. |
| 22 | The refusal body names the tier. | 13 | carried | 'and the tier as well.' in `merged.md` -- The text says the body also names the tier. |
| 23 | None of the refusal body's fields is a substitute for the header. | 13 | carried | 'None of those fields is a substitute for the header' in `merged.md` -- The text explicitly says none of the body fields substitutes for the header. |
| 24 | A caller that parses the body to compute its own wait is doing the same arithmetic twice. | 13 | carried | 'a caller that parses the body to compute its own wait is doing the same arithmetic twice.' in `merged.md` -- The text directly states that parsing the body to compute a wait repeats the arithmetic. |
| 25 | The refusal body is there so a human reading a log afterwards can see why the request was refused. | 13 | carried | 'The body is there so that a human reading a log afterwards can see why the request was refused' in `merged.md` -- The text says the body lets a person reviewing a log see why the request was refused. |
| 26 | The gateway performs the Retry-After arithmetic using information the caller does not have. | 19 | carried | 'The gateway has already done that arithmetic, with information the caller does not have' in `merged.md` -- The text says the gateway has done the arithmetic using information unavailable to the caller. |
| 27 | The gateway performs the same arithmetic on the 503 path. | 19 | carried | 'and it does the same on the 503 path.' in `merged.md` -- The text explicitly says the gateway does the same arithmetic on the 503 path. |
| 28 | A wait derived on the client side is a guess about a counter the client cannot see. | 19 | carried | 'A wait derived on the client side is a guess about a counter it cannot see.' in `merged.md` -- This is stated directly. |
| 29 | A 200 wants nothing. | 21 | carried | 'A 200 wants nothing' in `merged.md` -- This is stated directly. |
| 30 | A 429 wants the stated wait. | 21 | carried | 'a 429 wants the stated wait' in `merged.md` -- This is stated directly. |
| 31 | A 500 may be retried once the stated wait has passed. | 21 | carried | 'a 500 may be retried once that wait has passed' in `merged.md` -- This is stated directly. |
| 32 | A 503 is the overload path. | 21 | carried | 'a 503 is the overload path' in `merged.md` -- This is stated directly. |
| 33 | The four cases are not interchangeable. | 21 | carried | 'The four cases are not interchangeable.' in `merged.md` -- This is stated directly. |
| 34 | A client that folds every non-success into one branch will retry hardest during the incident the cap was installed to survive. | 21 | carried | 'A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive.' in `merged.md` -- The text states this outcome directly. |
| 35 | A batch credential is allowed fifty times the default allowance. | 23 | carried | 'A batch credential is allowed fifty times the default allowance' in `merged.md` -- This is stated directly. |
| 36 | A batch credential is measured over exactly the same window as the default allowance. | 23 | carried | 'it is measured over exactly the same window' in `merged.md` -- The text says the batch credential is measured over the same window. |
| 37 | The tier is set on the credential when it is issued. | 23 | carried | 'The tier is set on the credential when it is issued' in `merged.md` -- This is stated directly. |
| 38 | The tier cannot be requested per call. | 23 | carried | 'cannot be asked for per call' in `merged.md` -- The text says the tier cannot be requested per call. |
| 39 | Nothing else about the two tiers differs. | 23 | carried | 'Nothing else about the two tiers differs in any way.' in `merged.md` -- This is stated directly. |
| 40 | A caller that cannot say how often it was refused last week cannot argue for a larger cap. | 25 | carried | 'A caller that cannot say how often it was refused last week cannot argue for a larger cap' in `merged.md` -- This is stated directly. |
| 41 | Nobody at the far end will assemble that argument on the caller's behalf. | 25 | carried | 'nobody at the far end will assemble that argument on its behalf' in `merged.md` -- This is stated directly. |
| 42 | The gateway refuses a request for three reasons. | 29 | carried | 'The gateway refuses a request for three reasons' in `merged.md` -- This is stated directly. |
| 43 | Only one of the gateway's three refusal reasons is the rate cap. | 29 | carried | 'only one of them is the one above' in `merged.md` -- The text says only one of the three reasons is the rate cap discussed above. |
| 44 | A credential may be suspended. | 29 | carried | 'A credential can be suspended' in `merged.md` -- This is stated directly. |
| 45 | A route may be closed for maintenance. | 29 | carried | 'a route can be closed while it is being repaired' in `merged.md` -- A route closed while being repaired is described as the maintenance case. |
| 46 | A body may exceed the 5 megabyte limit. | 29 | carried | 'a request body over the 5 megabyte limit is refused before it has been read at all' in `merged.md` -- The text states that a body over the limit is refused. |
| 47 | None of those three refusal reasons clears itself by waiting for a stated number of seconds. | 29 | carried | 'None of those three clears itself by waiting for a stated number of seconds.' in `merged.md` -- This is stated directly. |
| 48 | A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `merged.md` -- This is stated directly. |
| 49 | The log afterwards shows nothing except a long run of refusals. | 31 | carried | 'the log afterwards shows nothing at all except a long run of refusals' in `merged.md` -- The text says the log shows nothing except a long run of refusals. |
| 50 | Reading the status code rather than the class it belongs to separates the two cases. | 31 | carried | 'Reading the status code rather than the class it belongs to is what separates the two cases' in `merged.md` -- This is stated directly. |
| 51 | That status-code comparison costs one comparison. | 31 | carried | 'Reading the status code rather than the class it belongs to is what separates the two cases, and it costs one comparison.' in `merged.md` -- The text explicitly says the status-code comparison costs one comparison. |
| 52 | A cap can be raised. | 35 | carried | 'A cap can be raised' in `merged.md` -- The text explicitly states that a cap can be raised. |
| 53 | The number of caps raised without a measurement behind them is 0. | 35 | carried | 'the number of caps raised without a measurement behind them is 0.' in `merged.md` -- The text gives the number as 0. |
| 54 | The platform team looks at whether the load is smooth or bursty. | 35 | carried | 'The platform team looks at whether the load is smooth or bursty' in `merged.md` -- The text explicitly says the platform team considers whether load is smooth or bursty. |
| 55 | A burst is cheaper to smooth than it is to serve at its peak. | 35 | carried | 'a burst is cheaper to smooth than it is to serve at its peak.' in `merged.md` -- The text directly compares smoothing a burst as cheaper than serving it at peak. |
| 56 | A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap. | 35 | carried | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `merged.md` -- The text states that moving half the work to a quieter hour usually avoids any cap change. |
| 57 | Requests reach the platform team through the usual channel. | 37 | carried | 'Requests reach the platform team through the usual channel.' in `merged.md` -- The text states that requests reach the platform team through the usual channel. |
| 58 | Requests to the platform team are answered within two working days. | 37 | carried | 'An answer takes two working days' in `merged.md` -- The text says an answer takes two working days, which supports the stated timeframe. |
| 59 | There is no expedited path. | 37 | carried | 'There is no expedited path' in `merged.md` -- The text explicitly says there is no expedited path. |
| 60 | There is no exception list. | 37 | carried | 'There is no exception list.' in `merged.md`, **transcription_error** -- The text explicitly says there is no exception list. |

### `source_b.md` -- 67 claim(s): 0 dropped, 0 contradicted, 7 carried in part, 60 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 21 | The response body repeats the cap as a plain field. | 13 | carried in part | 'It names the cap and the tier as well.' in `merged.md` -- The body names the cap, but the text does not establish that it is a plain field. |
| 22 | The response body repeats the window as a plain field. | 13 | carried in part | 'It names what the gateway calls the “window” it counted in.' in `merged.md` -- The body names the window, but the text does not establish that it is a plain field. |
| 23 | The response body repeats the tier as a plain field. | 13 | carried in part | 'It names the cap and the tier as well.' in `merged.md` -- The body names the tier, but the text does not establish that it is a plain field. |
| 31 | Anything computed on the client side is a guess. | 19 | carried in part | 'A wait derived on the client side is a guess about a counter it cannot see.' in `merged.md` -- The text calls a client-derived wait a guess, but does not say that anything computed client-side is a guess. |
| 35 | A 503 means the platform itself is overloaded. | 21 | carried in part | 'and a 503 is the overload path.' in `merged.md` -- The text identifies 503 as the overload path, but does not explicitly say the platform itself is overloaded. |
| 36 | A caller that folds all four responses into one branch will retry hardest during the incident the cap was installed to survive. | 21 | carried in part | 'A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive.' in `merged.md` -- The text supports folding non-success responses into one branch, but does not say the client folds all four responses into that branch. |
| 62 | The team wants to know whether the load is smooth or bursty before it looks at the number. | 35 | carried in part | 'The platform team looks at whether the load is smooth or bursty' in `merged.md` -- The text says the team considers whether load is smooth or bursty, but does not state that this happens before it looks at the number. |
| 1 | Every credential has its own cap. | 3 | carried | 'Every credential has a cap.' in `merged.md` -- The text says every credential has a cap, supporting that each has its own cap. |
| 2 | When a credential's cap is spent, the gateway answers 429 at the edge. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge' in `merged.md` -- The text states that spending the cap results in a 429 at the edge. |
| 3 | When a credential's cap is spent, the gateway does not trouble the service behind it. | 3 | carried | 'without waking the service behind it' in `merged.md` -- The text says the gateway refuses at the edge without waking the service. |
| 4 | Requests are counted against the credential rather than the connection. | 5 | carried | 'Requests are counted against the credential that presented them, over a fixed window of 60 seconds, and never against a connection.' in `merged.md` -- The text explicitly contrasts counting against the credential with counting against a connection. |
| 5 | Requests are counted over a fixed window of 60 seconds. | 5 | carried | 'over a fixed window of 60 seconds' in `merged.md` -- The text specifies a fixed 60-second window. |
| 6 | The gateway doesn’t disclose the start of the fixed window. | 5 | carried | 'The window’s start is not disclosed by the gateway.' in `merged.md` -- The text explicitly says the gateway does not disclose the window’s start. |
| 7 | The count follows the credential across hosts. | 5 | carried | 'The count follows the credential wherever the caller happens to put it, including across hosts.' in `merged.md` -- The text says the count follows the credential across hosts. |
| 8 | A caller spread over many worker processes is throttled at the same point as a single process. | 5 | carried | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `merged.md` -- The text says a caller using multiple worker processes is throttled at the same point as one process. |
| 9 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- The text gives the default allowance as 100 requests per window. |
| 10 | A caller that needs more than the default allowance is almost always doing batch work under an interactive credential. | 7 | carried | 'a caller that needs more than that is almost always doing batch work under an interactive credential.' in `merged.md` -- The text states that callers needing more than the default are almost always doing batch work under an interactive credential. |
| 11 | The refusal isn’t an outage. | 7 | carried | 'A refusal is not an outage' in `merged.md` -- The text explicitly says a refusal is not an outage. |
| 12 | The refusal isn’t a bug in the gateway. | 7 | carried | 'The refusal isn’t a bug in the gateway either.' in `merged.md` -- The text explicitly says the refusal is not a gateway bug. |
| 13 | The refusal is capacity being held for a request somebody else has already been promised. | 7 | carried | 'It is the platform declining to spend capacity that has already been promised to somebody else' in `merged.md` -- The text describes the refusal as declining to spend capacity already promised to someone else. |
| 14 | Callers that retry immediately are most of the reason the cap is there. | 7 | carried | 'Callers that retry at once are the largest single reason the cap is there at all.' in `merged.md` -- The text identifies callers retrying immediately as the largest single reason for the cap. |
| 15 | The header is called Retry-After. | 11 | carried | 'The refusal carries a Retry-After header.' in `merged.md` -- The text names the refusal’s header as Retry-After. |
| 16 | The value of the Retry-After header is a whole number of seconds. | 11 | carried | 'Its value is a whole number of seconds' in `merged.md` -- The text directly states the Retry-After value is a whole number of seconds. |
| 17 | The Retry-After header is present on every refusal the gateway sends. | 11 | carried | 'it is present on every refusal the gateway sends' in `merged.md` -- The text says the header is present on every refusal the gateway sends. |
| 18 | Waiting the time specified by the header and then continuing is the entire contract. | 11 | carried | 'Waiting that long and then continuing is the entire contract' in `merged.md` -- This directly states that waiting the header-specified time and continuing is the entire contract. |
| 19 | Nobody at the gateway's end is keeping score when a caller waits longer than the header asks. | 11 | carried | 'The gateway keeps no memory of who backed off politely, so waiting longer than the header asks earns a caller no credit at all.' in `merged.md` -- The gateway keeps no memory of callers who wait longer, so it is not keeping score of that behavior. |
| 20 | The response body is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- The text directly identifies the refusal body as JSON. |
| 24 | None of the response body fields is a substitute for the header. | 13 | carried | 'None of those fields is a substitute for the header' in `merged.md` -- The text directly says none of the body fields substitutes for the header. |
| 25 | The response body is for the human reading the log afterwards. | 13 | carried | 'The body is there so that a human reading a log afterwards can see why the request was refused' in `merged.md` -- The text says the body is intended to help a human reading the log afterwards understand the refusal. |
| 26 | The four rules are to be applied in the order they are given. | 17 | carried | 'Four rules, given in the order they should be applied.' in `merged.md` -- The text explicitly says the four rules are presented in application order. |
| 27 | The gateway has already done the arithmetic for the wait. | 19 | carried | 'The gateway has already done that arithmetic' in `merged.md` -- The text states that the gateway has already done the arithmetic for the wait. |
| 28 | The gateway did the arithmetic with information the caller cannot see. | 19 | carried | 'with information the caller does not have' in `merged.md` -- The text says the gateway's arithmetic uses information unavailable to the caller. |
| 29 | The same rule applies on the 503 path. | 19 | carried | 'On the 503 path the same rule holds' in `merged.md` -- The text directly says the same rule applies on the 503 path. |
| 30 | The cause of a refusal on the 503 path is entirely different. | 19 | carried | 'even though the cause of the refusal is an entirely different one.' in `merged.md` -- The text says the cause of a refusal on the 503 path is entirely different. |
| 32 | A 200 needs nothing. | 21 | carried | 'A 200 wants nothing' in `merged.md` -- The text directly says a 200 wants nothing. |
| 33 | A 429 needs the stated wait. | 21 | carried | 'a 429 wants the stated wait' in `merged.md` -- The text directly says a 429 wants the stated wait. |
| 34 | A 500 can be retried once the stated wait has passed. | 21 | carried | 'a 500 may be retried once that wait has passed' in `merged.md` -- The text directly permits retrying a 500 after the stated wait has passed. |
| 37 | The cap was installed to survive that incident. | 21 | carried | 'the incident the cap was installed to survive' in `merged.md` -- The text directly states that the cap was installed to survive the incident. |
| 38 | A batch credential is allowed 1000 requests in a window. | 23 | carried | 'a credential marked for batch work is allowed 1000 in the same window.' in `merged.md` -- The text directly gives batch credentials an allowance of 1000 in the same window. |
| 39 | The batch allowance is 50 times the default. | 23 | carried | 'A batch credential is allowed fifty times the default allowance' in `merged.md` -- The text directly states that the batch allowance is fifty times the default. |
| 40 | The batch tier does not use a separate counting scheme. | 23 | carried | 'Nothing else about the two tiers differs in any way.' in `merged.md` -- The text says nothing about the tiers differs, which rules out a separate counting scheme. |
| 41 | The window is identical for the batch and interactive cases. | 23 | carried | 'The window, the header and the body are identical to the interactive case' in `merged.md` -- The text explicitly says the batch and interactive cases use the identical window. |
| 42 | The header is identical for the batch and interactive cases. | 23 | carried | 'The window, the header and the body are identical to the interactive case' in `merged.md` -- The text explicitly says the batch and interactive cases use the identical header. |
| 43 | The body is identical for the batch and interactive cases. | 23 | carried | 'The window, the header and the body are identical to the interactive case' in `merged.md` -- The text explicitly says the batch and interactive cases use the identical body. |
| 44 | A client written for one tier needs no change to run against the other tier. | 23 | carried | 'a client written for one tier needs no change at all to run against the other' in `merged.md` -- The text directly states that a client needs no change to run against the other tier. |
| 45 | Nothing else about the batch tier differs from the default. | 23 | carried | 'Nothing else about the two tiers differs in any way.' in `merged.md` -- The text explicitly states that nothing else differs between the tiers. |
| 46 | A caller that cannot say how often it was refused can’t make a case for a larger cap. | 25 | carried | 'A caller that cannot say how often it was refused last week cannot argue for a larger cap' in `merged.md` -- The text says a caller unable to report how often it was refused cannot argue for a larger cap. |
| 47 | The platform team won’t assemble a case for a larger cap on a caller's behalf. | 25 | carried | 'nobody at the far end will assemble that argument on its behalf' in `merged.md` -- The text says the caller’s argument will not be assembled on its behalf. |
| 48 | The gateway refuses requests for three separate reasons. | 29 | carried | 'The gateway refuses a request for three reasons' in `merged.md` -- The text directly states that the gateway refuses requests for three reasons. |
| 49 | Only one of the gateway's three refusal reasons is a cap. | 29 | carried | 'only one of them is the one above' in `merged.md` -- The text identifies only one of the three refusal reasons as the cap described above. |
| 50 | Two of the gateway's three refusal reasons have nothing to do with how much traffic a caller has sent in its current window. | 29 | carried | 'Two of the three have nothing to do with how much traffic a caller has sent in the window it is currently in.' in `merged.md` -- The text directly states that two reasons are unrelated to traffic sent in the current window. |
| 51 | A credential can be suspended. | 29 | carried | 'A credential can be suspended' in `merged.md` -- The text explicitly lists suspension of a credential as a refusal reason. |
| 52 | A route can be closed while it is being repaired. | 29 | carried | 'a route can be closed while it is being repaired' in `merged.md` -- The text explicitly states that a route can be closed during repairs. |
| 53 | A request body over the 5 megabyte limit is refused before it has been read. | 29 | carried | 'a request body over the 5 megabyte limit is refused before it has been read at all' in `merged.md` -- The text directly states that an over-limit body is refused before being read. |
| 54 | A loop retrying against a suspended credential burns its whole budget. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget' in `merged.md` -- The text says a loop retrying against a suspended credential spends its whole budget. |
| 55 | A loop retrying against a suspended credential reaches nothing. | 31 | carried | 'without ever reaching the service' in `merged.md` -- The text says retries against a suspended credential never reach the service. |
| 56 | The log afterwards shows a long run of refusals. | 31 | carried | 'The log afterwards shows a long run of refusals' in `merged.md` -- The text directly states that the log shows a long run of refusals. |
| 57 | The log afterwards shows no successes at all. | 31 | carried | 'no successes at all' in `merged.md` -- The text explicitly says the log shows no successes. |
| 58 | The log reads like an outage, but it isn’t one. | 31 | carried | 'which reads like an outage and isn’t one' in `merged.md` -- The text says the log reads like an outage even though it is not one. |
| 59 | The wasted budget belongs to the caller. | 31 | carried | 'the wasted budget is the caller’s own' in `merged.md` -- The text directly assigns the wasted budget to the caller. |
| 60 | A caller that can move half its work to a quieter hour usually finds that it doesn’t need a larger cap. | 33 | carried | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `merged.md` -- The text says callers moving half their work to a quieter hour usually need no cap change. |
| 61 | A cap can be raised. | 33 | carried | 'A cap can be raised' in `merged.md` -- The text explicitly states that a cap can be raised. |
| 63 | A burst is cheaper to smooth out than it is to serve at its peak. | 35 | carried | 'a burst is cheaper to smooth than it is to serve at its peak' in `merged.md` -- The text directly compares smoothing a burst as cheaper than serving it at peak. |
| 64 | Requests go to the platform team through the usual channel. | 35 | carried | 'Requests reach the platform team through the usual channel.' in `merged.md` -- The text directly states that requests reach the team through the usual channel. |
| 65 | There is no expedited path. | 37 | carried | 'There is no expedited path' in `merged.md` -- The text explicitly states there is no expedited path. |
| 66 | An answer takes two working days. | 37 | carried | 'An answer takes two working days' in `merged.md` -- The reference states that an answer takes two working days. |
| 67 | Chasing an answer doesn’t make it take fewer than two working days. | 37 | carried | 'An answer takes two working days, and chasing it doesn’t make it take fewer.' in `merged.md` -- The reference says chasing an answer does not make the two-working-day wait shorter. |

### `merged.md` -- 72 claim(s): 0 invented, 0 contradicted, 0 supported in part, 72 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Every credential has a cap. | supported | `source_a.md` | 'Every credential has a cap.' in `source_a.md` -- Source_a.md states directly that every credential has a cap. |
| 2 | When a credential’s cap is spent, the gateway answers 429 at the edge. | supported | `source_a.md` | 'When that cap is spent the gateway answers 429 at the edge' in `source_a.md` -- Source_a.md states that spending the cap triggers a 429 at the edge. |
| 3 | The gateway answers 429 without waking the service behind it. | supported | `source_a.md` | 'without waking the service behind it' in `source_a.md` -- Source_a.md says the edge refusal does not wake the service behind it. |
| 4 | Requests are counted against the credential that presented them. | supported | `source_a.md` | 'Requests are counted against the credential that presented them' in `source_a.md` -- Source_a.md identifies the presenting credential as the basis for counting requests. |
| 5 | Requests are counted over a fixed window of 60 seconds. | supported | `source_a.md` | 'over a fixed window of 60 seconds' in `source_a.md` -- Source_a.md specifies a fixed 60-second counting window. |
| 6 | Requests are never counted against a connection. | supported | `source_a.md` | 'and never against a connection' in `source_a.md` -- Source_a.md explicitly says requests are never counted against a connection. |
| 7 | The gateway does not disclose the window’s start. | supported | `source_b.md` | 'whose start the gateway doesn’t disclose' in `source_b.md` -- Source_b.md states that the gateway does not disclose the window’s start. |
| 8 | Opening a second socket does not increase a caller’s allowance. | supported | `source_a.md` | 'Opening a second socket therefore buys a caller nothing.' in `source_a.md` -- Source_a.md says that opening a second socket provides no benefit, supporting that it does not increase the allowance. |
| 9 | The request count follows the credential across hosts. | supported | `source_b.md` | 'The count follows the credential wherever the caller happens to put it, including across hosts.' in `source_b.md` -- Source_b.md states that the count follows the credential across hosts. |
| 10 | A client spread across eight worker processes is throttled at exactly the same point as one process. | supported | `source_a.md` | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `source_a.md` -- Source_a.md directly states that an eight-process client is throttled at the same point as one process. |
| 11 | A client spread across eight worker processes pays for the extra file descriptors. | supported | `source_a.md` | 'and pays for the extra file descriptors as well.' in `source_a.md` -- Source_a.md says the multi-process caller pays for the extra file descriptors. |
| 12 | The default allowance is 100 requests in a window. | supported | `source_a.md` | 'The default allowance is 100 requests in a window' in `source_a.md` -- Source_a.md states the default allowance is 100 requests per window. |
| 13 | A credential marked for batch work is allowed 1000 requests in the same window. | supported | `source_a.md` | 'a credential marked for batch work is allowed 1000 in the same window.' in `source_a.md` -- Source_a.md gives batch credentials an allowance of 1000 in the same window. |
| 14 | The platform team has seen every interactive use of the API fit within the default allowance. | supported | `source_b.md` | 'which is enough for every interactive use of this API the platform team has seen' in `source_b.md` -- Source_b.md says the default allowance is enough for every interactive use the platform team has seen. |
| 15 | A caller that needs more than the default allowance is almost always doing batch work under an interactive credential. | supported | `source_b.md` | 'a caller that needs more than that is almost always doing batch work under an interactive credential.' in `source_b.md` -- Source_b.md directly states this about callers needing more than the default allowance. |
| 16 | A refusal is not an outage. | supported | `source_a.md` | 'A refusal is not an outage,' in `source_a.md` -- Source_a.md explicitly distinguishes a refusal from an outage. |
| 17 | A refusal is the platform declining to spend capacity that has already been promised to somebody else. | supported | `source_a.md` | 'It is the platform declining to spend capacity that has already been promised to somebody else,' in `source_a.md` -- Source_a.md describes a refusal as the platform declining to spend already-promised capacity. |
| 18 | Callers that retry at once are the largest single reason the cap exists. | supported | `source_a.md` | 'Callers that retry at once are the largest single reason the cap is there at all.' in `source_a.md` -- Source_a.md identifies callers retrying at once as the largest single reason for the cap. |
| 19 | A refusal carries a Retry-After header. | supported | `source_a.md` | 'The refusal carries a Retry-After header.' in `source_a.md` -- Source_a.md states that a refusal carries a Retry-After header. |
| 20 | The Retry-After header’s value is a whole number of seconds. | supported | `source_a.md` | 'Its value is a whole number of seconds to wait.' in `source_a.md` -- Source_a.md specifies that the header value is a whole number of seconds. |
| 21 | The Retry-After header is present on every refusal the gateway sends. | supported | `source_b.md` | 'it is present on every refusal the gateway sends.' in `source_b.md` -- Source_b.md states that the Retry-After header is present on every gateway refusal. |
| 22 | The gateway keeps no memory of who backed off politely. | supported | `source_a.md` | 'The gateway keeps no memory of who backed off politely,' in `source_a.md` -- Source_a.md directly states that the gateway keeps no memory of callers who backed off politely. |
| 23 | Waiting longer than the Retry-After header asks earns a caller no credit. | supported | `source_a.md` | 'waiting longer than the header asks earns a caller no credit at all.' in `source_a.md` -- Source_a.md says waiting beyond the header’s requested time earns no credit. |
| 24 | The body of a refusal is JSON. | supported | `source_a.md` | 'The body of the refusal is JSON,' in `source_a.md` -- Source_a.md explicitly says the refusal body is JSON. |
| 25 | The refusal body names the window the gateway counted in. | supported | `source_a.md` | 'it names what the gateway calls the “window” it counted in.' in `source_a.md` -- Source_a.md says the refusal body names the window used for counting. |
| 26 | The refusal body names the cap. | supported | `source_a.md` | 'The body of the refusal is JSON, and it names what the gateway calls the “window” it counted in. It names the cap and the tier as well.' in `source_a.md` -- The source explicitly says the refusal body names the cap. |
| 27 | The refusal body names the tier. | supported | `source_a.md` | 'The body of the refusal is JSON, and it names what the gateway calls the “window” it counted in. It names the cap and the tier as well.' in `source_a.md` -- The source explicitly says the refusal body names the tier. |
| 28 | The fields in the refusal body are not a substitute for the Retry-After header. | supported | `source_a.md` | 'None of those fields is a substitute for the header' in `source_a.md` -- The source states that the refusal-body fields cannot substitute for the header. |
| 29 | Parsing the refusal body to compute a wait repeats the same arithmetic twice. | supported | `source_a.md` | 'a caller that parses the body to compute its own wait is doing the same arithmetic twice.' in `source_a.md` -- The source directly says computing a wait from the body repeats the arithmetic. |
| 30 | The refusal body is there so a human reading a log afterwards can see why the request was refused. | supported | `source_a.md` | 'The body is there so that a human reading a log afterwards can see why the request was refused' in `source_a.md` -- The source explicitly gives this purpose for the body. |
| 31 | The gateway has already done the wait arithmetic using information the caller does not have. | supported | `source_a.md` | 'The gateway has already done that arithmetic, with information the caller does not have' in `source_a.md` -- The source says the gateway has calculated the wait using information unavailable to the caller. |
| 32 | The gateway does the same wait arithmetic on the 503 path. | supported | `source_a.md` | 'and it does the same on the 503 path.' in `source_a.md` -- The source explicitly says the gateway follows the same arithmetic on the 503 path. |
| 33 | The cause of a 503 refusal is different from the cause of the refusal discussed in the note. | supported | `source_b.md` | 'On the 503 path the same rule holds, even though the cause of the refusal is an entirely different one.' in `source_b.md` -- The source says the 503 path has a different cause from the refusal discussed in the note. |
| 34 | A 200 wants nothing. | supported | `source_a.md` | 'A 200 wants nothing' in `source_a.md` -- The source states that a 200 needs no action. |
| 35 | A 429 wants the stated wait. | supported | `source_a.md` | 'a 429 wants the stated wait' in `source_a.md` -- The source states that a 429 requires the stated wait. |
| 36 | A 500 may be retried once the stated wait has passed. | supported | `source_a.md` | 'a 500 may be retried once that wait has passed' in `source_a.md` -- The source explicitly permits retrying a 500 after the stated wait. |
| 37 | A 503 is the overload path. | supported | `source_a.md` | 'and a 503 is the overload path.' in `source_a.md` -- The source identifies a 503 as the overload path. |
| 38 | The four response cases are not interchangeable. | supported | `source_a.md` | 'The four cases are not interchangeable.' in `source_a.md` -- The source explicitly says the response cases are not interchangeable. |
| 39 | A client that folds every non-success response into one branch will retry hardest during the incident the cap was installed to survive. | supported | `source_a.md` | 'A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive.' in `source_a.md` -- The source states this consequence for a client that combines non-success responses into one branch. |
| 40 | A batch credential is allowed fifty times the default allowance. | supported | `source_a.md` | 'A batch credential is allowed fifty times the default allowance' in `source_a.md` -- The source directly states the batch allowance is fifty times the default. |
| 41 | A batch credential is measured over exactly the same window as the default allowance. | supported | `source_a.md` | 'A batch credential is allowed fifty times the default allowance, and it is measured over exactly the same window.' in `source_a.md` -- The source says the batch allowance uses exactly the same window. |
| 42 | The tier is set on the credential when it is issued. | supported | `source_a.md` | 'The tier is set on the credential when it is issued' in `source_a.md` -- The source explicitly states when and where the tier is set. |
| 43 | The tier cannot be requested per call. | supported | `source_a.md` | 'and cannot be asked for per call.' in `source_a.md` -- The source states that the tier cannot be requested per call. |
| 44 | Nothing else about the two tiers differs. | supported | `source_a.md` | 'Nothing else about the two tiers differs in any way.' in `source_a.md` -- The source says there are no other differences between the tiers. |
| 45 | The window is identical for the batch and interactive cases. | supported | `source_b.md` | 'The window, the header and the body are identical to the interactive case' in `source_b.md` -- The source explicitly says the batch and interactive windows are identical. |
| 46 | The header is identical for the batch and interactive cases. | supported | `source_b.md` | 'The window, the header and the body are identical to the interactive case' in `source_b.md` -- The source explicitly says the batch and interactive headers are identical. |
| 47 | The body is identical for the batch and interactive cases. | supported | `source_b.md` | 'The window, the header and the body are identical to the interactive case' in `source_b.md` -- The source explicitly says the batch and interactive bodies are identical. |
| 48 | A caller that cannot say how often it was refused last week cannot argue for a larger cap. | supported | `source_a.md` | 'A caller that cannot say how often it was refused last week cannot argue for a larger cap' in `source_a.md` -- The source directly connects lacking last week's refusal count with being unable to argue for a larger cap. |
| 49 | Nobody at the far end will assemble the argument for a larger cap on the caller’s behalf. | supported | `source_a.md` | 'nobody at the far end will assemble that argument on its behalf.' in `source_a.md` -- The source says no one at the far end will assemble the argument for the caller. |
| 50 | The gateway refuses a request for three reasons. | supported | `source_a.md` | 'The gateway refuses a request for three reasons and only one of them is the one above.' in `source_a.md` -- The source explicitly says the gateway refuses requests for three reasons. |
| 51 | Only one of the three refusal reasons is the cap-related reason discussed above. | supported | `source_b.md` | 'The gateway refuses a request for three separate reasons, and only one of them is a cap.' in `source_b.md` -- The source states that only one of the three refusal reasons is a cap. |
| 52 | Two of the three refusal reasons have nothing to do with how much traffic a caller has sent in its current window. | supported | `source_b.md` | 'Two of the three have nothing to do with how much traffic a caller has sent in the window it is currently in.' in `source_b.md` -- The source states this directly. |
| 53 | A credential can be suspended. | supported | `source_b.md` | 'A credential can be suspended' in `source_b.md` -- The source explicitly says a credential can be suspended. |
| 54 | A route can be closed while it is being repaired. | supported | `source_b.md` | 'a route can be closed while it is being repaired' in `source_b.md` -- The source explicitly describes a route being closed while repaired. |
| 55 | A request body over the 5 megabyte limit is refused before it has been read. | supported | `source_b.md` | 'a request body over the 5 megabyte limit is refused before it has been read at all.' in `source_b.md` -- The source states both the size threshold and that refusal occurs before the body is read. |
| 56 | None of the three refusal reasons clears itself by waiting for a stated number of seconds. | supported | `source_a.md` | 'None of those three clears itself by waiting for a stated number of seconds.' in `source_a.md` -- The source says none of the three refusal reasons clears through waiting. |
| 57 | A loop that waits and retries against a suspended credential spends its whole budget without reaching the service. | supported | `source_a.md` | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `source_a.md` -- The source directly states that this loop spends its budget without reaching the service. |
| 58 | The log afterwards shows a long run of refusals for a loop retrying against a suspended credential. | supported | `source_a.md` | 'and the log afterwards shows nothing at all except a long run of refusals.' in `source_a.md` -- This passage describes the log after the loop retrying against a suspended credential. |
| 59 | Reading the status code rather than the class it belongs to separates the two cases. | supported | `source_a.md` | 'Reading the status code rather than the class it belongs to is what separates the two cases' in `source_a.md` -- The source states that reading the status code separates the two cases. |
| 60 | Reading the status code rather than the class it belongs to costs one comparison. | supported | `source_a.md` | 'Reading the status code rather than the class it belongs to is what separates the two cases, and it costs one comparison.' in `source_a.md` -- The source explicitly says this distinction costs one comparison. |
| 61 | The log afterwards shows a long run of refusals and no successes at all. | supported | `source_b.md` | 'The log afterwards shows a long run of refusals and no successes at all' in `source_b.md` -- The source directly describes the log as showing refusals and no successes. |
| 62 | A cap can be raised. | supported | `source_a.md` | 'A cap can be raised' in `source_a.md` -- The source explicitly says a cap can be raised. |
| 63 | The number of caps raised without a measurement behind them is 0. | supported | `source_a.md` | 'the number of caps raised without a measurement behind them is 0.' in `source_a.md` -- The source gives the number of caps raised without measurement as zero. |
| 64 | A cap cannot be raised on the strength of an assertion that the current cap is too small. | supported | `source_b.md` | 'A cap can be raised, but not on the strength of an assertion that the current one is too small.' in `source_b.md` -- The source directly rejects raising a cap based only on that assertion. |
| 65 | The platform team looks at whether the load is smooth or bursty. | supported | `source_a.md` | 'The platform team looks at whether the load is smooth or bursty' in `source_a.md` -- The source says the platform team looks at whether load is smooth or bursty. |
| 66 | A burst is cheaper to smooth than it is to serve at its peak. | supported | `source_a.md` | 'a burst is cheaper to smooth than it is to serve at its peak.' in `source_a.md` -- The source states that smoothing a burst is cheaper than serving it at peak. |
| 67 | A caller that can move half its work to a quieter hour usually gets what it needs without a cap change. | supported | `source_a.md` | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `source_a.md` -- The source states that moving half the work usually meets the need without a cap change. |
| 68 | Requests reach the platform team through the usual channel. | supported | `source_a.md` | 'Requests reach the platform team through the usual channel' in `source_a.md` -- The source says requests reach the platform team through the usual channel. |
| 69 | An answer takes two working days. | supported | `source_b.md` | 'An answer takes two working days' in `source_b.md` -- The source states that an answer takes two working days. |
| 70 | Chasing an answer does not make it take fewer days. | supported | `source_b.md` | 'chasing it doesn’t make it take fewer.' in `source_b.md` -- The source says chasing the answer does not make it take fewer days. |
| 71 | There is no expedited path. | supported | `source_a.md` | 'There is no expedited path.' in `source_a.md`, **attribution_error** -- The source explicitly says there is no expedited path. |
| 72 | There is no exception list. | supported | `source_a.md` | 'There is no expedited path and no exception list.' in `source_a.md` -- The source explicitly says there is no exception list. |

## Structure

**9** mechanical check(s) over **104** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **72** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **127**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 23 run(s) over 62 attributed segment(s) — sources interleaved. 6 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Absent and undeclared — in a source, not in the merge, and no record explains it

- `b9` (`source_b.md`) — 'The default allowance is 100 requests in a window, which is enough for every interactive use of this API the platform team has seen, and a caller that needs more than that is almost always doing batch work under an interactive credential.' is not in the merge and no disposition record explains it (nearest merge segment m10 at 0.49)

  ```text
  In the source: The default allowance is 100 requests in a window, which is enough for every interactive use of this API the platform team has seen, and a caller that needs more than that is almost always doing batch work under an interactive credential.
  ```
- `b10` (`source_b.md`) — 'The refusal isn’t an outage and it isn’t a bug in the gateway — it is capacity being held for a request somebody else has already been promised.' is not in the merge and no disposition record explains it (nearest merge segment m14 at 0.47)

  ```text
  In the source: The refusal isn’t an outage and it isn’t a bug in the gateway — it is capacity being held for a request somebody else has already been promised.
  ```

### Reworded and undeclared — in the merge in altered wording, and no record explains it. At off this also covers layout: a segment whose source line breaks the merge ran together is altered and undeclared, and 380 reuses this kind rather than moving FINDING_KINDS off 12

- `b5` (`source_b.md`) — 'Requests are counted against the credential rather than the connection, over a fixed window of 60 seconds whose start the gateway doesn’t disclose.' is reworded in the merge and no disposition record explains it (nearest merge segment m5 at 0.70)

  ```text
  In the source: Requests are counted against the credential rather than the connection, over a fixed window of 60 seconds whose start the gateway doesn’t disclose.
  In the merge:  Requests are counted against the credential that presented them, over a fixed window of 60 seconds, and never against a connection.
  ```

### Unresolved replacement — a record points at text the merge does not contain

- `b31` — segment b31 is declared 'duplicate' with replacement 'The default allowance is 100 requests in a window, and a credential marked for batch work is allowed 1000 in the same window. A batch credential is allowed fifty times the default allowance, and it is measured over exactly the same window.', which is not in the merged document

  ```text
  In the merge: The default allowance is 100 requests in a window, and a credential marked for batch work is allowed 1000 in the same window. A batch credential is allowed fifty times the default allowance, and it is measured over exactly the same window.
  ```

### Verbatim violation — an invariant-core token did not survive unchanged

- `b31` (`source_b.md`) — numeric '50' (times) does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **38** departure(s) from its sources. Checking them confirms 23, rejects 10, and leaves 5 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 104 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | Title slot: retain the base document’s subject-specific title. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Rate limiting and the 429 contract for gateway clients' and says so (no claim traced to it) |
| `a13` | duplicate | Header slot: the retained sentence also states the wait is in seconds. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`A-016`) |
| `a14` | subsumed | Retry contract: the retained sentence carries the complete wait instruction. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b2` | duplicate | Credential cap: the base sentence states the same fact. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-001`) |
| `b3` | duplicate | 429 response: the base sentence already states the edge response. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-002`, `B-003`) |
| `b6` | duplicate | Socket use: the base sentence states the same consequence. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b8` | duplicate | Worker throttling: the base sentence states the same throttling point. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-008`) |
| `b11` | duplicate | Immediate retries: the base sentence states the same cause. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-014`) |
| `b13` | duplicate | Header name: the retained sentence identifies Retry-After. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-015`) |
| `b16` | duplicate | Waiting longer: the retained sentence states that it earns no credit. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-019`) |
| `b17` | duplicate | Response body: the retained sentences name the same JSON fields. | **rejected** | declared 'duplicate', which predicts SUPPORTED; B-021 came back PARTIAL, B-022 came back PARTIAL, B-023 came back PARTIAL (`B-021`, `B-022`, `B-023`) |
| `b18` | duplicate | Wait calculation: the retained sentence gives the same warning. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-024`) |
| `b19` | duplicate | Body purpose: the retained sentence includes both the human and retry-loop roles | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-025`) |
| `b20` | superseded | Heading slot: keep the base heading for retry guidance. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b21` | duplicate | Rule order: the retained sentence states the same ordering. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-026`) |
| `b22` | duplicate | Header rule: the retained rule includes honoring the header and the 503 path. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b23` | duplicate | Gateway calculation: the retained sentence states the same point. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-027`, `B-028`) |
| `b25` | duplicate | Client-side wait: the retained sentence describes it as a guess. | **rejected** | declared 'duplicate', which predicts SUPPORTED; B-031 came back PARTIAL (`B-031`) |
| `b26` | duplicate | Guess quality: the retained sentence states that a guess is not preferable. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b28` | duplicate | Response handling: the retained sentence gives the same four cases. | **rejected** | declared 'duplicate', which predicts SUPPORTED; B-035 came back PARTIAL (`B-035`) |
| `b29` | duplicate | Retry behavior: the retained sentence states the same risk. | **rejected** | declared 'duplicate', which predicts SUPPORTED; B-036 came back PARTIAL (`B-036`) |
| `b30` | duplicate | Loop guidance: the retained instruction gives the same warning. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b31` | duplicate | Batch allowance: the retained sentences state the same allowance and window. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-038`, `B-039`, `B-040`) |
| `b33` | duplicate | Tier differences: the retained sentence states that there are none. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-045`) |
| `a35` | superseded | Logging rule: the selected wording adds the required retention period. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b35` | duplicate | Increase evidence: the retained sentence states the same need for refusal counts | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-046`, `B-047`) |
| `b37` | superseded | Heading slot: keep the base heading, which also covers refusal codes. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b38` | duplicate | Refusal causes: the retained sentence states the same three-reason distinction. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-048`, `B-049`) |
| `a41` | superseded | Refusal causes: the selected wording adds repair and unread-body details. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`A-044`, `A-045`, `A-046`) |
| `b41` | duplicate | Retry distinction: the retained sentence states the same relevance. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b42` | duplicate | Suspended credentials: the retained sentence states the same retry outcome. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-054`, `B-055`) |
| `b44` | duplicate | Quieter-hour fix: the retained sentence states the same benefit. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-060`) |
| `b47` | duplicate | Increase request: the retained sentence includes the week, traffic shape and dea | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'duplicate' is what happened to it (no claim traced to it) |
| `b48` | duplicate | Load assessment: the retained sentence states the same smooth-or-bursty review. | **rejected** | declared 'duplicate', which predicts SUPPORTED; B-062 came back PARTIAL (`B-062`) |
| `b49` | duplicate | Burst handling: the retained sentence gives the same cost comparison. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-063`) |
| `b50` | duplicate | Request channel: the retained sentence states the same route. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-064`) |
| `b51` | duplicate | Expedited path: the retained sentence also states there is no exception list. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-065`) |
| `a51` | subsumed | Request handling: the combined sentences retain the channel and response time. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-057`, `A-058`) |


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
| Calls | 13 live, 0 cached, 0 replayed |
| Tokens | 45,908 in, 39,919 out, 0 cached, 15,959 reasoning |
| Cost | ~$0.02 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 271.7s |
| Generated | 2026-09-27T15:46:12+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `bf7d5842201d`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
