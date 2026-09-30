## Verdict

**15 finding(s).** In the claims: 3 partially dropped. In the structure: 1 undeclared absence, 4 undeclared rewording, 6 false departure, 1 verbatim violation.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 73 |
| Claims extracted from `source_a.md` | 64 |
| Claims extracted from `source_b.md` | 60 |
| Forward — source claims accounted for in the merge | **121/124** |
| Forward — carried only in part | 3 |
| Forward — `source_a.md` claims accounted for | **64/64** |
| Forward — `source_b.md` claims accounted for | **57/60** (3 in part) |
| Reverse — merge claims found in a source | **73/73** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **195/197** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Partly dropped — the merge carries some of this claim

- **B-041** (`source_b.md:25`) — A caller that cannot say how often it was refused cannot make a case for a larger cap.
  - evidence: 'A caller that cannot say how often it was refused last week cannot argue for a larger cap' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text supports this for refusals during last week, but does not make the claim without that time limit.
- **B-047** (`source_b.md:29`) — A route can be closed while it is being repaired.
  - evidence: 'a route may be closed for maintenance' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text supports that a route may be closed, but does not say it is closed while being repaired.
- **B-059** (`source_b.md:37`) — An answer takes two working days.
  - evidence: 'they are answered within two working days.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text sets a limit of within two working days, but does not say every answer takes exactly two days.

## Length capped

- `$.dispositions[8].reason` was 83 characters, over the 80-character cap; capped to fit
- `$.dispositions[10].reason` was 86 characters, over the 80-character cap; capped to fit
- `$.dispositions[43].reason` was 84 characters, over the 80-character cap; capped to fit
- `$.dispositions[47].reason` was 84 characters, over the 80-character cap; capped to fit
- `$.dispositions[49].reason` was 84 characters, over the 80-character cap; capped to fit
- `$.dispositions[51].reason` was 81 characters, over the 80-character cap; capped to fit
- `$.dispositions[52].reason` was 81 characters, over the 80-character cap; capped to fit
- `$.dispositions[53].reason` was 82 characters, over the 80-character cap; capped to fit

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 64 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 64 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Every credential has a cap. | 3 | carried | 'Every credential has a cap.' in `merged.md` -- The text explicitly says every credential has a cap. |
| 2 | When a credential's cap is spent, the gateway answers 429 at the edge. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge' in `merged.md` -- The text states that spending the cap causes the gateway to answer 429 at the edge. |
| 3 | The gateway answers 429 without waking the service behind it. | 3 | carried | 'the gateway answers 429 at the edge — without waking the service behind it' in `merged.md` -- The text says the 429 response does not wake the service behind the gateway. |
| 4 | A refusal costs the platform almost nothing. | 3 | carried | 'the refusal costs the platform almost nothing' in `merged.md` -- The text explicitly says the refusal costs the platform almost nothing. |
| 5 | A caller that files a refusal under transport error incurs a great deal of cost. | 3 | carried | 'costs a caller that files it under transport error a great deal' in `merged.md` -- The text says a caller filing the refusal under transport error incurs a great deal of cost. |
| 6 | Requests are counted against the credential that presented them. | 5 | carried | 'Requests are counted against the credential that presented them' in `merged.md` -- The text explicitly identifies the presenting credential as the basis for counting requests. |
| 7 | Requests are counted over a fixed window of 60 seconds. | 5 | carried | 'over a fixed window of 60 seconds' in `merged.md` -- The text states that requests are counted over a fixed 60-second window. |
| 8 | Requests are never counted against a connection. | 5 | carried | 'and never against a connection' in `merged.md` -- The text explicitly says requests are never counted against a connection. |
| 9 | Opening a second socket does not benefit a caller. | 5 | carried | 'Opening a second socket therefore buys a caller nothing.' in `merged.md` -- The text says opening a second socket provides no benefit to the caller. |
| 10 | A client spread across eight worker processes is throttled at exactly the point one process would have been. | 5 | carried | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `merged.md` -- The text explicitly compares throttling across eight processes with throttling one process. |
| 11 | A client spread across eight worker processes pays for the extra file descriptors. | 5 | carried | 'and pays for the extra file descriptors as well' in `merged.md` -- The text states that the client also pays for the extra file descriptors. |
| 12 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- The text gives the default allowance as 100 requests per window. |
| 13 | A credential marked for batch work is allowed 1000 requests in the same window. | 7 | carried | 'a credential marked for batch work is allowed 1000 in the same window' in `merged.md` -- The text gives batch credentials an allowance of 1000 in the same window. |
| 14 | A refusal is not an outage. | 7 | carried | 'A refusal is not an outage' in `merged.md` -- The text explicitly says a refusal is not an outage. |
| 15 | A refusal is the platform declining to spend capacity that has already been promised to somebody else. | 7 | carried | 'It is the platform declining to spend capacity that has already been promised to somebody else' in `merged.md` -- The text describes a refusal as the platform declining to spend already-promised capacity. |
| 16 | Callers that retry at once are the largest single reason the cap exists. | 7 | carried | 'Callers that retry at once are the largest single reason the cap is there at all.' in `merged.md` -- The text identifies callers retrying at once as the largest single reason for the cap. |
| 17 | A refusal carries a Retry-After header. | 11 | carried | 'The refusal carries a Retry-After header.' in `merged.md` -- The text explicitly says refusals carry a Retry-After header. |
| 18 | The Retry-After header value is a whole number of seconds to wait. | 11 | carried | 'Its value is a whole number of seconds to wait' in `merged.md` -- The text states the header value is a whole number of seconds to wait. |
| 19 | Waiting the amount of time stated in the header and then continuing is the whole of the contract. | 11 | carried | 'Waiting that long and then continuing is the whole of the contract' in `merged.md` -- “That long” refers to the wait specified by the header, and the text calls waiting and continuing the whole contract. |
| 20 | The gateway keeps no memory of who backed off politely. | 11 | carried | 'The gateway keeps no memory of who backed off politely' in `merged.md` -- The text explicitly says the gateway keeps no memory of callers who backed off politely. |
| 21 | Waiting longer than the header asks earns a caller no credit. | 11 | carried | 'so waiting longer than the header asks earns a caller no credit at all' in `merged.md` -- The text says waiting longer than the header requests earns the caller no credit. |
| 22 | The body of a refusal is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- The text explicitly says a refusal body is JSON. |
| 23 | The body names what the gateway calls the “window” it counted in. | 13 | carried | 'it names what the gateway calls the “window” it counted in' in `merged.md` -- The text says the body names the window in which the gateway counted the request. |
| 24 | The body names the cap. | 13 | carried | 'The response body repeats the cap' in `merged.md` -- The text explicitly says the response body repeats the cap. |
| 25 | The body names the tier. | 13 | carried | 'the tier as plain fields' in `merged.md` -- The text states that the response body includes the tier as a plain field. |
| 26 | The fields in the body are not substitutes for the header. | 13 | carried | 'none of those fields is a substitute for the header' in `merged.md` -- The text explicitly says none of the body fields substitutes for the header. |
| 27 | A caller that parses the body to compute its own wait is doing the same arithmetic twice. | 13 | carried | 'a caller that parses the body to compute its own wait is doing the same arithmetic twice' in `merged.md` -- The text states this directly. |
| 28 | The body is there so that a human reading a log afterwards can see why the request was refused. | 13 | carried | 'A caller reading the body can see why the request was refused; none of those fields is a substitute for the header, and a caller that parses the body to compute its own wait is doing the same arithmetic twice. The body is there for the human reading a log afterwards' in `merged.md` -- The text says the body shows why a request was refused and is there for a human reading a log afterwards. |
| 29 | Nothing in the body is meant for the retry loop. | 13 | carried | 'nothing in it is meant for the retry loop' in `merged.md` -- The text explicitly says the body is not meant for the retry loop. |
| 30 | The gateway has already done the arithmetic using information the caller does not have. | 19 | carried | 'The gateway has already done that arithmetic, with information the caller does not have' in `merged.md` -- The text states that the gateway has done the arithmetic using information unavailable to the caller. |
| 31 | The gateway does the same arithmetic on the 503 path. | 19 | carried | 'it does the same on the 503 path' in `merged.md` -- The text explicitly says the gateway does the same on the 503 path. |
| 32 | A wait derived on the client side is a guess about a counter the client cannot see. | 19 | carried | 'A wait derived on the client side is a guess about a counter it cannot see.' in `merged.md` -- The text states this directly. |
| 33 | A 200 wants nothing. | 21 | carried | 'A 200 wants nothing' in `merged.md` -- The text explicitly says a 200 wants nothing. |
| 34 | A 429 wants the stated wait. | 21 | carried | 'a 429 wants the stated wait' in `merged.md` -- The text explicitly says a 429 wants the stated wait. |
| 35 | A 500 may be retried once the stated wait has passed. | 21 | carried | 'a 500 may be retried once that wait has passed' in `merged.md` -- The text explicitly permits retrying a 500 after the stated wait has passed. |
| 36 | A 503 is the overload path. | 21 | carried | 'a 503 is the overload path' in `merged.md` -- The text explicitly describes a 503 as the overload path. |
| 37 | The four cases are not interchangeable. | 21 | carried | 'The four cases are not interchangeable.' in `merged.md` -- The text states that the four cases are not interchangeable. |
| 38 | A client that folds every non-success into one branch will retry hardest during the incident the cap was installed to survive. | 21 | carried | 'A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive.' in `merged.md` -- The text states that such a client retries hardest during the incident the cap was installed to survive. |
| 39 | A batch credential is allowed fifty times the default allowance. | 23 | carried | 'A batch credential is allowed fifty times the default allowance' in `merged.md` -- The text explicitly gives the batch credential fifty times the default allowance. |
| 40 | A batch credential is measured over exactly the same window as the default allowance. | 23 | carried | 'it is measured over exactly the same window' in `merged.md` -- The text says the batch allowance is measured over exactly the same window. |
| 41 | The tier is set on the credential when it is issued. | 23 | carried | 'The tier is set on the credential when it is issued' in `merged.md` -- The text states when and where the tier is set. |
| 42 | The tier cannot be requested per call. | 23 | carried | 'cannot be asked for per call' in `merged.md` -- The text says the tier cannot be requested per call. |
| 43 | Nothing else differs between the two tiers. | 23 | carried | 'Nothing else about the two tiers differs in any way.' in `merged.md` -- The text explicitly says nothing else differs between the tiers. |
| 44 | A caller that cannot say how often it was refused last week cannot argue for a larger cap. | 25 | carried | 'A caller that cannot say how often it was refused last week cannot argue for a larger cap' in `merged.md` -- The text states that a caller without last week's refusal count cannot argue for a larger cap. |
| 45 | Nobody at the far end will assemble that argument on the caller's behalf. | 25 | carried | 'nobody at the far end will assemble that argument on its behalf' in `merged.md` -- The text explicitly says nobody will assemble the argument on the caller's behalf. |
| 46 | The gateway refuses a request for three reasons. | 29 | carried | 'The gateway refuses a request for three reasons' in `merged.md` -- The text explicitly gives three reasons for gateway refusals. |
| 47 | Only one of the three refusal reasons is the rate-cap reason described above. | 29 | carried | 'only one of them is the cap described above' in `merged.md` -- The text says only one of the three refusal reasons is the cap described above. |
| 48 | A credential may be suspended. | 29 | carried | 'A credential may be suspended' in `merged.md` -- The text explicitly names credential suspension as a possible refusal reason. |
| 49 | A route may be closed for maintenance. | 29 | carried | 'a route may be closed for maintenance' in `merged.md` -- The text explicitly names a route closed for maintenance as a possible refusal reason. |
| 50 | A body may exceed the 5 megabyte limit. | 29 | carried | 'a body may exceed the 5 megabyte limit' in `merged.md` -- The text explicitly names a body exceeding the 5 megabyte limit as a possible refusal reason. |
| 51 | None of those three reasons clears itself by waiting for a stated number of seconds. | 29 | carried | 'None of those three clears itself by waiting for a stated number of seconds.' in `merged.md` -- The reference explicitly says none of the three refusals clears itself by waiting. |
| 52 | A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `merged.md` -- The reference states that a loop retrying against a suspended credential spends its whole budget without reaching the service. |
| 53 | The log afterwards shows nothing at all except a long run of refusals. | 31 | carried | 'the log afterwards shows nothing at all except a long run of refusals.' in `merged.md` -- The reference says the log shows nothing except a long run of refusals. |
| 54 | Reading the status code rather than the class it belongs to separates the two cases. | 31 | carried | 'Reading the status code rather than the class it belongs to is what separates the two cases' in `merged.md` -- The reference directly says reading the status code rather than its class separates the cases. |
| 55 | Separating the two cases by reading the status code rather than the class it belongs to costs one comparison. | 31 | carried | 'Reading the status code rather than the class it belongs to is what separates the two cases, and it costs one comparison.' in `merged.md` -- The reference states this method separates the cases and costs one comparison. |
| 56 | A cap can be raised. | 35 | carried | 'A cap can be raised' in `merged.md` -- The reference explicitly says a cap can be raised. |
| 57 | The number of caps raised without a measurement behind them is 0. | 35 | carried | 'the number of caps raised without a measurement behind them is 0.' in `merged.md` -- The reference gives the number of caps raised without measurement as 0. |
| 58 | The platform team looks at whether the load is smooth or bursty. | 35 | carried | 'The platform team looks at whether the load is smooth or bursty' in `merged.md` -- The reference says the platform team considers whether the load is smooth or bursty. |
| 59 | A burst is cheaper to smooth than it is to serve at its peak. | 35 | carried | 'a burst is cheaper to smooth than it is to serve at its peak.' in `merged.md` -- The reference explicitly compares smoothing a burst as cheaper than serving it at peak. |
| 60 | A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap. | 35 | carried | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `merged.md` -- The reference states that moving half the work to a quieter hour usually meets the caller’s need without changing the cap. |
| 61 | Requests reach the platform team through the usual channel. | 37 | carried | 'Requests reach the platform team through the usual channel' in `merged.md` -- The reference says requests reach the platform team through the usual channel. |
| 62 | Requests are answered within two working days. | 37 | carried | 'they are answered within two working days.' in `merged.md` -- The reference states requests are answered within two working days. |
| 63 | There is no expedited path. | 37 | carried | 'There is no expedited path' in `merged.md` -- The reference explicitly says there is no expedited path. |
| 64 | There is no exception list. | 37 | carried | 'There is no exception list.' in `merged.md`, **transcription_error** -- The reference explicitly says there is no exception list. |

### `source_b.md` -- 60 claim(s): 0 dropped, 0 contradicted, 3 carried in part, 57 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 41 | A caller that cannot say how often it was refused cannot make a case for a larger cap. | 25 | carried in part | 'A caller that cannot say how often it was refused last week cannot argue for a larger cap' in `merged.md` -- The text supports this for refusals during last week, but does not make the claim without that time limit. |
| 47 | A route can be closed while it is being repaired. | 29 | carried in part | 'a route may be closed for maintenance' in `merged.md` -- The text supports that a route may be closed, but does not say it is closed while being repaired. |
| 59 | An answer takes two working days. | 37 | carried in part | 'they are answered within two working days.' in `merged.md` -- The text sets a limit of within two working days, but does not say every answer takes exactly two days. |
| 1 | Every credential has its own cap. | 3 | carried | 'Every credential has a cap.' in `merged.md` -- The reference says every credential has a cap. |
| 2 | When a credential’s cap is spent, the gateway answers 429 at the edge. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge' in `merged.md` -- The reference states that spending the cap results in a 429 response at the edge. |
| 3 | The gateway answers 429 without troubling the service behind it. | 3 | carried | 'without waking the service behind it' in `merged.md` -- The reference says the gateway’s 429 response does not wake the service behind it. |
| 4 | Requests are counted against the credential rather than the connection. | 5 | carried | 'Requests are counted against the credential that presented them, over a fixed window of 60 seconds, and never against a connection.' in `merged.md` -- The reference says requests are counted against the presenting credential and never against a connection. |
| 5 | Requests are counted over a fixed window of 60 seconds. | 5 | carried | 'over a fixed window of 60 seconds' in `merged.md` -- The reference specifies a fixed 60-second counting window. |
| 6 | The gateway does not disclose the start of the fixed window. | 5 | carried | 'The gateway does not disclose where the window starts.' in `merged.md` -- The reference explicitly says the gateway does not disclose the window’s start. |
| 7 | The request count follows the credential across hosts. | 5 | carried | 'The count follows the credential wherever the caller puts it, including across hosts.' in `merged.md` -- The reference says the count follows the credential across hosts. |
| 8 | A caller spread over many worker processes is throttled at the same point as a single process. | 5 | carried | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `merged.md` -- The reference says a client using eight worker processes is throttled at the same point as one process. |
| 9 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- The reference gives the default allowance as 100 requests in a window. |
| 10 | A caller that needs more than the default allowance is almost always doing batch work under an interactive credential. | 7 | carried | 'a caller that needs more is almost always doing batch work under an interactive credential.' in `merged.md` -- The reference says callers needing more than the default are almost always doing batch work under an interactive credential. |
| 11 | A refusal is not an outage. | 7 | carried | 'A refusal is not an outage' in `merged.md` -- The reference explicitly says a refusal is not an outage. |
| 12 | A refusal is not a bug in the gateway. | 7 | carried | 'It is not a bug in the gateway.' in `merged.md` -- The text explicitly says a refusal is not a gateway bug. |
| 13 | A refusal is capacity being held for a request somebody else has already been promised. | 7 | carried | 'It is the platform declining to spend capacity that has already been promised to somebody else' in `merged.md` -- This directly describes the refusal as declining to spend capacity promised to someone else. |
| 14 | Callers that retry immediately are most of the reason the cap exists. | 7 | carried | 'Callers that retry at once are the largest single reason the cap is there at all.' in `merged.md` -- The text says callers retrying at once are the largest single reason for the cap. |
| 15 | The header is called Retry-After. | 11 | carried | 'The refusal carries a Retry-After header.' in `merged.md` -- The header is explicitly named Retry-After. |
| 16 | The Retry-After value is a whole number of seconds. | 11 | carried | 'Its value is a whole number of seconds to wait' in `merged.md` -- The text specifies that the header value is a whole number of seconds. |
| 17 | The Retry-After header is present on every refusal the gateway sends. | 11 | carried | 'it is present on every refusal the gateway sends.' in `merged.md` -- The text says the header is present on every gateway refusal. |
| 18 | Waiting the stated time and then continuing is the entire contract. | 11 | carried | 'Waiting that long and then continuing is the whole of the contract' in `merged.md` -- This states that waiting the specified time and continuing is the entire contract. |
| 19 | The response body is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- The refusal body is explicitly described as JSON. |
| 20 | The response body repeats the cap as a plain field. | 13 | carried | 'The response body repeats the cap, the window and the tier as plain fields.' in `merged.md` -- This states that the cap is repeated as a plain field. |
| 21 | The response body repeats the window as a plain field. | 13 | carried | 'The response body repeats the cap, the window and the tier as plain fields.' in `merged.md` -- This states that the window is repeated as a plain field. |
| 22 | The response body repeats the tier as a plain field. | 13 | carried | 'The response body repeats the cap, the window and the tier as plain fields.' in `merged.md` -- This states that the tier is repeated as a plain field. |
| 23 | None of the response body fields is a substitute for the header. | 13 | carried | 'none of those fields is a substitute for the header' in `merged.md` -- The text explicitly says none of the body fields substitutes for the header. |
| 24 | The response body is for the human reading the log afterwards. | 13 | carried | 'The body is there for the human reading a log afterwards' in `merged.md` -- The text says the body is intended for a human reading a log afterwards. |
| 25 | The gateway has already done the wait arithmetic. | 19 | carried | 'The gateway has already done that arithmetic' in `merged.md` -- The text explicitly says the gateway has already performed the arithmetic. |
| 26 | The gateway did the wait arithmetic with information the caller cannot see. | 19 | carried | 'with information the caller does not have' in `merged.md` -- The arithmetic is described as using information the caller does not have. |
| 27 | On the 503 path, the cause of the refusal is entirely different from the cause on the other path. | 19 | carried | 'A 200 wants nothing, a 429 wants the stated wait, a 500 may be retried once that wait has passed, and a 503 is the overload path. The four cases are not interchangeable.' in `merged.md` -- The text distinguishes the 503 overload path from the other response cases. |
| 28 | A 200 needs nothing. | 21 | carried | 'A 200 wants nothing' in `merged.md` -- The text explicitly says a 200 wants nothing. |
| 29 | A 429 needs the stated wait. | 21 | carried | 'a 429 wants the stated wait' in `merged.md` -- The text explicitly says a 429 wants the stated wait. |
| 30 | A 500 can be retried once that wait has passed. | 21 | carried | 'a 500 may be retried once that wait has passed' in `merged.md` -- The text states that a 500 may be retried after the wait has passed. |
| 31 | A 503 means the platform itself is overloaded. | 21 | carried | 'a 503 is the overload path' in `merged.md` -- The text identifies a 503 as the overload path. |
| 32 | The cap was installed to survive the incident when a caller retries hardest by folding all four responses into one branch. | 21 | carried | 'A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive.' in `merged.md` -- This directly links collapsing responses into one branch with retrying hardest during the incident the cap was installed to survive. |
| 33 | A batch credential is allowed 1000 requests in a window. | 23 | carried | 'a credential marked for batch work is allowed 1000 in the same window.' in `merged.md` -- The text states that a batch credential is allowed 1000 in the window. |
| 34 | The batch allowance is 50 times the default. | 23 | carried | 'A batch credential is allowed fifty times the default allowance' in `merged.md` -- The text explicitly gives the batch allowance as fifty times the default. |
| 35 | The batch tier does not use a separate counting scheme. | 23 | carried | 'Nothing else about the two tiers differs in any way.' in `merged.md` -- The text says the tiers differ in no way other than the stated difference, supporting that they do not use separate counting schemes. |
| 36 | The window is identical for the batch and interactive cases. | 23 | carried | 'The window, the header and the body are identical to the interactive case' in `merged.md` -- The text explicitly says the window is identical to the interactive case. |
| 37 | The header is identical for the batch and interactive cases. | 23 | carried | 'The window, the header and the body are identical to the interactive case' in `merged.md` -- The text explicitly says the header is identical for both tiers. |
| 38 | The body is identical for the batch and interactive cases. | 23 | carried | 'The window, the header and the body are identical to the interactive case' in `merged.md` -- The text explicitly says the body is identical for both tiers. |
| 39 | A client written for one tier needs no change to run against the other tier. | 23 | carried | 'a client written for one tier needs no change to run against the other.' in `merged.md` -- The text states that a client needs no change to run against the other tier. |
| 40 | Nothing else about the batch tier differs from the default. | 23 | carried | 'Nothing else about the two tiers differs in any way.' in `merged.md` -- This directly states that there are no other differences between the tiers. |
| 42 | The platform team will not assemble the case for a larger cap on the caller’s behalf. | 25 | carried | 'nobody at the far end will assemble that argument on its behalf.' in `merged.md` -- This directly says the team will not assemble the argument for the caller. |
| 43 | The gateway refuses requests for three separate reasons. | 29 | carried | 'The gateway refuses a request for three reasons' in `merged.md` -- The text explicitly gives three reasons for refusal. |
| 44 | Only one of the three refusal reasons is a cap. | 29 | carried | 'only one of them is the cap described above.' in `merged.md` -- This directly says only one of the three reasons is the cap. |
| 45 | Two of the three refusal reasons have nothing to do with how much traffic a caller has sent in its current window. | 29 | carried | 'Two of the three have nothing to do with how much traffic a caller has sent in its current window.' in `merged.md` -- The text states exactly this distinction for two of the three reasons. |
| 46 | A credential can be suspended. | 29 | carried | 'A credential may be suspended' in `merged.md` -- The text says a credential may be suspended. |
| 48 | A request body over the 5 megabyte limit is refused before it has been read at all. | 29 | carried | 'a body may exceed the 5 megabyte limit; an over-limit body is refused before it has been read at all.' in `merged.md` -- The text states both the size condition and that refusal occurs before the body is read. |
| 49 | A loop retrying against a suspended credential burns its whole budget and reaches nothing. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `merged.md` -- This directly states that such a loop uses its whole budget and never reaches the service. |
| 50 | The log afterwards shows a long run of refusals and no successes at all. | 31 | carried | 'and the log afterwards shows nothing at all except a long run of refusals. It shows no successes' in `merged.md` -- The text says the log contains a long run of refusals and no successes. |
| 51 | The log of refusals and no successes reads like an outage, although it is not one. | 31 | carried | 'and the log afterwards shows nothing at all except a long run of refusals. It shows no successes, reads like an outage, and is not one' in `merged.md` -- The text says the log has refusals and no successes, appears like an outage, and is not one. |
| 52 | The wasted budget is the caller’s own. | 31 | carried | 'the wasted budget is the caller’s own.' in `merged.md` -- The text directly attributes the wasted budget to the caller. |
| 53 | A caller that moves half its work to a quieter hour usually finds it does not need a larger cap. | 33 | carried | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `merged.md` -- Getting what it needs without changing the cap means it usually does not need a larger cap. |
| 54 | A cap can be raised. | 33 | carried | 'A cap can be raised' in `merged.md` -- The text explicitly says a cap can be raised. |
| 55 | The team wants to know whether the load is smooth or bursty before it looks at the number. | 35 | carried | 'The platform team looks at whether the load is smooth or bursty before it considers the cap amount' in `merged.md` -- The text says the team assesses whether load is smooth or bursty before considering the cap amount. |
| 56 | A burst is cheaper to smooth out than it is to serve at its peak. | 35 | carried | 'a burst is cheaper to smooth than it is to serve at its peak.' in `merged.md` -- The text directly compares smoothing a burst with serving it at peak. |
| 57 | Requests go to the platform team through the usual channel. | 35 | carried | 'Requests reach the platform team through the usual channel' in `merged.md` -- The text states that requests go through the usual channel. |
| 58 | There is no expedited path. | 37 | carried | 'There is no expedited path' in `merged.md` -- The text directly says there is no expedited path. |
| 60 | Chasing an answer does not make it take fewer days. | 37 | carried | 'Chasing an answer does not make it take fewer than two working days.' in `merged.md` -- This directly states that chasing cannot shorten the stated two-working-day period. |

### `merged.md` -- 73 claim(s): 0 invented, 0 contradicted, 0 supported in part, 73 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Every credential has a cap. | supported | `source_a.md` | 'Every credential has a cap.' in `source_a.md` -- Source_a.md states that every credential has a cap. |
| 2 | When a credential's cap is spent, the gateway answers 429 at the edge. | supported | `source_a.md` | 'When that cap is spent the gateway answers 429 at the edge' in `source_a.md` -- Source_a.md says a spent cap results in a 429 at the edge. |
| 3 | When a credential's cap is spent, the gateway does not wake the service behind it. | supported | `source_a.md` | 'without waking the service behind it' in `source_a.md` -- Source_a.md states that the edge refusal does not wake the service behind it. |
| 4 | Requests are counted against the credential that presented them. | supported | `source_a.md` | 'Requests are counted against the credential that presented them' in `source_a.md` -- Source_a.md explicitly says requests are counted against the presenting credential. |
| 5 | Requests are counted over a fixed window of 60 seconds. | supported | `source_a.md` | 'over a fixed window of 60 seconds' in `source_a.md` -- Source_a.md specifies a fixed 60-second window. |
| 6 | Requests are never counted against a connection. | supported | `source_a.md` | 'and never against a connection' in `source_a.md` -- Source_a.md says counts are never against a connection. |
| 7 | The gateway does not disclose where the window starts. | supported | `source_b.md` | 'whose start the gateway doesn’t disclose' in `source_b.md` -- Source_b.md explicitly says the gateway does not disclose the window’s start. |
| 8 | The request count follows the credential across hosts. | supported | `source_b.md` | 'The count follows the credential wherever the caller happens to put it, including across hosts.' in `source_b.md` -- Source_b.md states that the count follows the credential across hosts. |
| 9 | A client spread across eight worker processes is throttled at exactly the point one process would have been. | supported | `source_a.md` | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `source_a.md` -- Source_a.md states this for a client spread across eight worker processes. |
| 10 | A client spread across eight worker processes pays for the extra file descriptors. | supported | `source_a.md` | 'and pays for the extra file descriptors as well.' in `source_a.md` -- Source_a.md says the client pays for the extra file descriptors. |
| 11 | The default allowance is 100 requests in a window. | supported | `source_a.md` | 'The default allowance is 100 requests in a window' in `source_a.md` -- Source_a.md gives the default allowance as 100 requests per window. |
| 12 | A credential marked for batch work is allowed 1000 requests in the same window. | supported | `source_a.md` | 'a credential marked for batch work is allowed 1000 in the same window.' in `source_a.md` -- Source_a.md states that a batch credential is allowed 1000 requests in the same window. |
| 13 | The default allowance is enough for every interactive use of the API the platform team has seen. | supported | `source_b.md` | 'which is enough for every interactive use of this API the platform team has seen' in `source_b.md` -- Source_b.md describes the default allowance as enough for every interactive use the team has seen. |
| 14 | A caller that needs more is almost always doing batch work under an interactive credential. | supported | `source_b.md` | 'a caller that needs more than that is almost always doing batch work under an interactive credential.' in `source_b.md` -- Source_b.md directly states this about callers needing more than the default allowance. |
| 15 | A refusal is not an outage. | supported | `source_a.md` | 'A refusal is not an outage' in `source_a.md` -- Source_a.md explicitly says a refusal is not an outage. |
| 16 | A refusal is not a bug in the gateway. | supported | `source_b.md` | 'it isn’t a bug in the gateway' in `source_b.md` -- Source_b.md says a refusal is not a bug in the gateway. |
| 17 | Callers that retry at once are the largest single reason the cap exists. | supported | `source_a.md` | 'Callers that retry at once are the largest single reason the cap is there at all.' in `source_a.md` -- Source_a.md identifies callers retrying at once as the largest single reason for the cap. |
| 18 | A refusal carries a Retry-After header. | supported | `source_a.md` | 'The refusal carries a Retry-After header.' in `source_a.md` -- Source_a.md states that the refusal carries a Retry-After header. |
| 19 | The Retry-After header's value is a whole number of seconds to wait. | supported | `source_a.md` | 'Its value is a whole number of seconds to wait.' in `source_a.md` -- Source_a.md specifies the header value is a whole number of seconds to wait. |
| 20 | The Retry-After header is present on every refusal the gateway sends. | supported | `source_b.md` | 'it is present on every refusal the gateway sends.' in `source_b.md` -- Source_b.md says the header is present on every refusal the gateway sends. |
| 21 | The gateway keeps no memory of who backed off politely. | supported | `source_a.md` | 'The gateway keeps no memory of who backed off politely' in `source_a.md` -- Source_a.md explicitly says the gateway keeps no memory of callers who backed off politely. |
| 22 | Waiting longer than the header asks earns a caller no credit. | supported | `source_a.md` | 'so waiting longer than the header asks earns a caller no credit at all.' in `source_a.md` -- Source_a.md says waiting longer than requested earns no credit. |
| 23 | The refusal body is JSON. | supported | `source_a.md` | 'The body of the refusal is JSON' in `source_a.md` -- Source_a.md states that the refusal body is JSON. |
| 24 | The refusal body names what the gateway calls the “window” it counted in. | supported | `source_a.md` | 'it names what the gateway calls the “window” it counted in.' in `source_a.md` -- Source_a.md says the body names the window the gateway counted in. |
| 25 | The response body repeats the cap as a plain field. | supported | `source_b.md` | 'The response body is JSON and it repeats the cap, the window and the tier as plain fields.' in `source_b.md` -- Source_b.md says the response body repeats the cap as a plain field. |
| 26 | The response body repeats the window as a plain field. | supported | `source_b.md` | 'it repeats the cap, the window and the tier as plain fields.' in `source_b.md` -- The source explicitly says the response body repeats the window as a plain field. |
| 27 | The response body repeats the tier as a plain field. | supported | `source_b.md` | 'it repeats the cap, the window and the tier as plain fields.' in `source_b.md` -- The source explicitly says the response body repeats the tier as a plain field. |
| 28 | The body fields are not a substitute for the Retry-After header. | supported | `source_a.md` | 'None of those fields is a substitute for the header' in `source_a.md` -- The source says none of the body fields substitutes for the header. |
| 29 | A caller that parses the body to compute its own wait is doing the same arithmetic twice. | supported | `source_a.md` | 'a caller that parses the body to compute its own wait is doing the same arithmetic twice.' in `source_a.md` -- The source states this directly. |
| 30 | The body is intended for the human reading a log afterwards. | supported | `source_b.md` | 'The body is for the human reading the log afterwards.' in `source_b.md` -- The source says the body is for a human reading the log afterwards. |
| 31 | The gateway does the wait arithmetic with information the caller does not have. | supported | `source_a.md` | 'The gateway has already done that arithmetic, with information the caller does not have.' in `source_a.md`, **transcription_error** -- The source says the gateway did the arithmetic with information unavailable to the caller. |
| 32 | The gateway does the same wait arithmetic on the 503 path. | supported | `source_a.md` | 'and it does the same on the 503 path.' in `source_a.md` -- This follows the statement that the gateway has already done the wait arithmetic. |
| 33 | The safe-to-retry set is smaller than the set of responses that are not successes. | supported | `source_b.md` | 'Retry only what is safe to retry, which is a smaller set than the set of responses that aren’t a success.' in `source_b.md` -- The source directly compares the safe-to-retry set with non-success responses. |
| 34 | A 200 wants nothing. | supported | `source_a.md` | 'A 200 wants nothing' in `source_a.md` -- The source says a 200 wants nothing. |
| 35 | A 429 wants the stated wait. | supported | `source_a.md` | 'a 429 wants the stated wait' in `source_a.md` -- The source says a 429 wants the stated wait. |
| 36 | A 500 may be retried once the stated wait has passed. | supported | `source_a.md` | 'a 500 may be retried once that wait has passed' in `source_a.md` -- The source gives this retry rule for a 500. |
| 37 | A 503 is the overload path. | supported | `source_a.md` | 'a 503 is the overload path.' in `source_a.md` -- The source describes a 503 as the overload path. |
| 38 | The four response cases are not interchangeable. | supported | `source_a.md` | 'The four cases are not interchangeable.' in `source_a.md` -- The source explicitly says the four cases are not interchangeable. |
| 39 | A client that folds every non-success into one branch will retry hardest during the incident the cap was installed to survive. | supported | `source_a.md` | 'A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive.' in `source_a.md` -- The source states this consequence of folding every non-success into one branch. |
| 40 | A batch credential is allowed fifty times the default allowance. | supported | `source_a.md` | 'A batch credential is allowed fifty times the default allowance,' in `source_a.md` -- The source directly states the batch credential's allowance relative to the default. |
| 41 | A batch credential is measured over exactly the same window as the default allowance. | supported | `source_a.md` | 'and it is measured over exactly the same window.' in `source_a.md` -- The source says the batch allowance is measured over the same window. |
| 42 | The tier is set on the credential when it is issued. | supported | `source_a.md` | 'The tier is set on the credential when it is issued' in `source_a.md` -- The source explicitly states when the tier is set. |
| 43 | The tier cannot be requested per call. | supported | `source_a.md` | 'and cannot be asked for per call.' in `source_a.md` -- The source says the tier cannot be requested per call. |
| 44 | The window is identical to the interactive case. | supported | `source_b.md` | 'The window, the header and the body are identical to the interactive case,' in `source_b.md` -- The source explicitly says the window is identical to the interactive case. |
| 45 | The header is identical to the interactive case. | supported | `source_b.md` | 'The window, the header and the body are identical to the interactive case,' in `source_b.md` -- The source explicitly says the header is identical to the interactive case. |
| 46 | The body is identical to the interactive case. | supported | `source_b.md` | 'The window, the header and the body are identical to the interactive case,' in `source_b.md` -- The source explicitly says the body is identical to the interactive case. |
| 47 | A client written for one tier needs no change to run against the other tier. | supported | `source_b.md` | 'so a client written for one tier needs no change at all to run against the other.' in `source_b.md` -- The source directly states that no client changes are needed between tiers. |
| 48 | The two tiers differ in no other way. | supported | `source_a.md` | 'Nothing else about the two tiers differs in any way.' in `source_a.md` -- The source says there are no other differences between the tiers. |
| 49 | The gateway refuses a request for three reasons. | supported | `source_a.md` | 'The gateway refuses a request for three reasons' in `source_a.md` -- The source states there are three reasons the gateway refuses a request. |
| 50 | Only one of the three refusal reasons is the cap described above. | supported | `source_a.md` | 'The gateway refuses a request for three reasons and only one of them is the one above.' in `source_a.md` -- The source says only one of the three reasons is the rate-cap refusal described above. |
| 51 | Two of the three refusal reasons have nothing to do with how much traffic a caller has sent in its current window. | supported | `source_b.md` | 'Two of the three have nothing to do with how much traffic a caller has sent in the window it is currently in.' in `source_b.md` -- Source_b states that two of the three refusal reasons are unrelated to the caller’s traffic in its current window. |
| 52 | A credential may be suspended. | supported | `source_a.md` | 'A credential may be suspended' in `source_a.md` -- Source_a explicitly says a credential may be suspended. |
| 53 | A route may be closed for maintenance. | supported | `source_a.md` | 'a route may be closed for maintenance' in `source_a.md` -- Source_a explicitly gives a route closed for maintenance as a refusal reason. |
| 54 | A body may exceed the 5 megabyte limit. | supported | `source_a.md` | 'a body may exceed the 5 megabyte limit' in `source_a.md` -- Source_a explicitly names a body exceeding the 5 megabyte limit as a refusal reason. |
| 55 | An over-limit body is refused before it has been read at all. | supported | `source_b.md` | 'a request body over the 5 megabyte limit is refused before it has been read at all.' in `source_b.md` -- Source_b states that an over-limit request body is refused before being read. |
| 56 | None of the three refusal reasons clears itself by waiting for a stated number of seconds. | supported | `source_a.md` | 'None of those three clears itself by waiting for a stated number of seconds.' in `source_a.md` -- Source_a says none of the three refusal reasons clears itself by waiting. |
| 57 | A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service. | supported | `source_a.md` | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `source_a.md` -- Source_a directly describes the loop spending its budget without reaching the service. |
| 58 | After a loop retries against a suspended credential, the log shows nothing except a long run of refusals. | supported | `source_a.md` | 'the log afterwards shows nothing at all except a long run of refusals.' in `source_a.md` -- Source_a says the log after retries against a suspended credential shows only a long run of refusals. |
| 59 | The log shows no successes. | supported | `source_b.md` | 'The log afterwards shows a long run of refusals and no successes at all, which reads like an outage and isn’t one — and the wasted budget is the caller’s own.' in `source_b.md` -- Source_b explicitly says the log shows no successes. |
| 60 | The log reads like an outage, but it is not an outage. | supported | `source_b.md` | 'The log afterwards shows a long run of refusals and no successes at all, which reads like an outage and isn’t one — and the wasted budget is the caller’s own.' in `source_b.md` -- Source_b says the log reads like an outage but is not one. |
| 61 | The wasted budget belongs to the caller. | supported | `source_b.md` | 'the wasted budget is the caller’s own.' in `source_b.md` -- Source_b explicitly assigns the wasted budget to the caller. |
| 62 | Reading the status code rather than the class it belongs to separates the two cases. | supported | `source_a.md` | 'Reading the status code rather than the class it belongs to is what separates the two cases' in `source_a.md` -- Source_a says reading the status code rather than its class separates the cases. |
| 63 | Separating the two cases by reading the status code rather than its class costs one comparison. | supported | `source_a.md` | 'Reading the status code rather than the class it belongs to is what separates the two cases, and it costs one comparison.' in `source_a.md` -- Source_a explicitly says this distinction costs one comparison. |
| 64 | A cap can be raised. | supported | `source_a.md` | 'A cap can be raised' in `source_a.md` -- Source_a directly states that a cap can be raised. |
| 65 | The number of caps raised without a measurement behind them is 0. | supported | `source_a.md` | 'the number of caps raised without a measurement behind them is 0.' in `source_a.md` -- Source_a states that the number of unmeasured cap increases is 0. |
| 66 | The platform team looks at whether the load is smooth or bursty before it considers the cap amount. | supported | `source_b.md` | 'The team wants to know whether the load is smooth or bursty before it looks at the number at all.' in `source_b.md` -- Source_b says the team checks whether load is smooth or bursty before looking at the number. |
| 67 | A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap. | supported | `source_a.md` | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all, which is the outcome everyone prefers.' in `source_a.md` -- Source_a directly says shifting half the work to a quieter hour usually meets the caller’s need without changing the cap. |
| 68 | A cap cannot be raised on the strength of an assertion that the current one is too small. | supported | `source_b.md` | 'A cap can be raised, but not on the strength of an assertion that the current one is too small.' in `source_b.md` -- Source_b explicitly rules out raising a cap solely on an assertion that it is too small. |
| 69 | Requests reach the platform team through the usual channel. | supported | `source_a.md` | 'Requests reach the platform team through the usual channel' in `source_a.md` -- Source_a says requests reach the platform team through the usual channel. |
| 70 | Requests to the platform team are answered within two working days. | supported | `source_a.md` | 'Requests reach the platform team through the usual channel, and they are answered within two working days.' in `source_a.md` -- Source_a states that requests are answered within two working days. |
| 71 | There is no expedited path. | supported | `source_a.md` | 'There is no expedited path' in `source_a.md` -- Source_a explicitly says there is no expedited path. |
| 72 | There is no exception list. | supported | `source_a.md` | 'There is no expedited path and no exception list.' in `source_a.md` -- Source_a explicitly says there is no exception list. |
| 73 | Chasing an answer does not make the answer take fewer than two working days. | supported | `source_b.md` | 'An answer takes two working days, and chasing it doesn’t make it take fewer.' in `source_b.md` -- Source_b says an answer takes two working days and chasing it does not make it take fewer. |

## Structure

**9** mechanical check(s) over **104** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **73** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **124**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 27 run(s) over 62 attributed segment(s) — sources interleaved. 6 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

`[-...-]` is what the source said and `{+...+}` is what the merge says.

### Absent and undeclared — in a source, not in the merge, and no record explains it

- `a13` (`source_a.md`) — 'Its value is a whole number of seconds to wait.' is not in the merge and no disposition record explains it (nearest merge segment m18 at 0.64)

  ```text
  In the source: Its value is a whole number of seconds to wait.
  ```

### Reworded and undeclared — in the merge in altered wording, and no record explains it. At off this also covers layout: a segment whose source line breaks the merge ran together is altered and undeclared, and 380 reuses this kind rather than moving FINDING_KINDS off 12

- `a39` (`source_a.md`) — 'Not all are caps.' is reworded in the merge and no disposition record explains it (nearest merge segment m49 at 0.79)

  ```text
  In the source: Not all are caps.
  In the merge:  Not all refusals are caps.
  ```
- `a40` (`source_a.md`) — 'The gateway refuses a request for three reasons and only one of them is the one above.' is reworded in the merge and no disposition record explains it (nearest merge segment m50 at 0.92)

  ```text
  In the source: The gateway refuses a request for three reasons and only one of them is the one above.
  In the merge:  The gateway refuses a request for three reasons and only one of them is the cap described above.
  What changed:  The gateway refuses a request for three reasons and only one of them is the [-one-] {+cap described+} above.
  ```
- `a48` (`source_a.md`) — 'Bring a week of refusal counts, the shape of the traffic across the day, and the deadline that traffic is serving.' is reworded in the merge and no disposition record explains it (nearest merge segment m60 at 0.82)

  ```text
  In the source: Bring a week of refusal counts, the shape of the traffic across the day, and the deadline that traffic is serving.
  In the merge:  Bring refusal counts for a full week, the shape of the traffic across the day, and the deadline that traffic exists to meet.
  What changed:  Bring {+refusal counts for+} a [-week of refusal counts,-] {+full week,+} the shape of the traffic across the day, and the deadline that traffic [-is serving.-] {+exists to meet.+}
  ```
- `b7` (`source_b.md`) — 'The count follows the credential wherever the caller happens to put it, including across hosts.' is reworded in the merge and no disposition record explains it (nearest merge segment m7 at 0.93)

  ```text
  In the source: The count follows the credential wherever the caller happens to put it, including across hosts.
  In the merge:  The count follows the credential wherever the caller puts it, including across hosts.
  What changed:  The count follows the credential wherever the caller [-happens to put-] {+puts+} it, including across hosts.
  ```

### Declared gone, still here — a record says the content departed and the merge carries the segment unchanged

- `a7` (`source_a.md`) — 'The default allowance is 100 requests in a window, and a credential marked for batch work is allowed 1000 in the same window.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: The default allowance is 100 requests in a window, and a credential marked for batch work is allowed 1000 in the same window.
  In the merge:  The default allowance is 100 requests in a window, and a credential marked for batch work is allowed 1000 in the same window. That default is enough for every interactive use of the API the platform team has seen; a caller that needs more is almost always doing batch work under an interactive credential.
  ```
- `a8` (`source_a.md`) — 'A refusal is not an outage, whatever the error class in a client library happens to call it.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: A refusal is not an outage, whatever the error class in a client library happens to call it.
  In the merge:  A refusal is not an outage, whatever the error class in a client library happens to call it. It is not a bug in the gateway. It is the platform declining to spend capacity that has already been promised to somebody else, and waiting is the only correct answer.
  ```
- `a9` (`source_a.md`) — 'It is the platform declining to spend capacity that has already been promised to somebody else, and waiting is the only correct answer.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: It is the platform declining to spend capacity that has already been promised to somebody else, and waiting is the only correct answer.
  In the merge:  A refusal is not an outage, whatever the error class in a client library happens to call it. It is not a bug in the gateway. It is the platform declining to spend capacity that has already been promised to somebody else, and waiting is the only correct answer.
  ```
- `a18` (`source_a.md`) — 'None of those fields is a substitute for the header, and a caller that parses the body to compute its own wait is doing the same arithmetic twice.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: None of those fields is a substitute for the header, and a caller that parses the body to compute its own wait is doing the same arithmetic twice.
  In the merge:  A caller reading the body can see why the request was refused; none of those fields is a substitute for the header, and a caller that parses the body to compute its own wait is doing the same arithmetic twice.
  What changed:  [-None-] {+A caller reading the body can see why the request was refused; none+} of those fields is a substitute for the header, and a caller that parses the body to compute its own wait is doing the same arithmetic twice.
  ```
- `b36` (`source_b.md`) — 'The counts are the whole of the argument, and without them a request is only a preference.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: The counts are the whole of the argument, and without them a request is only a preference.
  In the merge:  The counts are the whole of the argument, and without them a request is only a preference.
  ```
- `b46` (`source_b.md`) — 'A cap can be raised, but not on the strength of an assertion that the current one is too small.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: A cap can be raised, but not on the strength of an assertion that the current one is too small.
  In the merge:  A cap can be raised, but not on the strength of an assertion that the current one is too small.
  ```

### Verbatim violation — an invariant-core token did not survive unchanged

- `b31` (`source_b.md`) — numeric '50' (times) does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **58** departure(s) from its sources. Checking them confirms 40, rejects 12, and leaves 6 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 104 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | The title slot keeps the base document’s broader title. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Rate limiting and the 429 contract for gateway clients' and says so (no claim traced to it) |
| `b2` | duplicate | The opening states that each credential has a cap. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-001`) |
| `b3` | superseded | The opening keeps the fuller base wording for the 429 response. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-002`, `B-003`) |
| `b5` | subsumed | The counting paragraph includes the credential, window, and undisclosed start. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-004`, `B-005`, `B-006`) |
| `b6` | duplicate | The base sentence already states that more sockets do not help. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b8` | duplicate | The base sentence states the same worker-process throttling point. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-008`) |
| `a7` | subsumed | The allowance paragraph retains the limits and adds the interactive-use context. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-012`, `A-013`) |
| `b9` | subsumed | The allowance paragraph carries the default’s observed interactive-use context. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-009`, `B-010`) |
| `a8` | subsumed | The refusal paragraph retains the outage distinction and adds that it is not a b | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-014`) |
| `a9` | subsumed | The refusal paragraph retains the capacity explanation and waiting guidance. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-015`) |
| `b10` | subsumed | The refusal paragraph preserves its capacity explanation and adds the bug distin | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-011`, `B-012`, `B-013`) |
| `b11` | duplicate | The base sentence already gives the reason for the cap. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-014`) |
| `b12` | duplicate | This heading is identical to the base heading. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b13` | duplicate | The base sentence already identifies the Retry-After header. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-015`) |
| `b14` | subsumed | The header paragraph retains whole seconds and adds universal presence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-016`, `B-017`) |
| `b15` | subsumed | The section retains the contract and the note’s intended outcome. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-018`) |
| `b16` | duplicate | The base sentence already states that waiting longer earns no credit. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `a17` | duplicate | The body paragraph states the cap, window, and tier together. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`A-024`, `A-025`) |
| `b17` | subsumed | The body paragraph retains all three fields and their plain-field format. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-019`, `B-020`, `B-021`, `B-022`) |
| `a18` | subsumed | The body paragraph preserves the header rule and duplicate-arithmetic warning. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-026`, `A-027`) |
| `a19` | subsumed | The body paragraph retains the human-log purpose and retry-loop distinction. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-028`, `A-029`) |
| `b18` | duplicate | The body paragraph already warns against computing a wait from the body. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-023`) |
| `b19` | duplicate | The base wording already states the body’s human-reading purpose. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-024`) |
| `b20` | superseded | The base heading is retained for the retry guidance section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b21` | duplicate | The base introduction already states the number and order of the rules. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b22` | duplicate | The base rule states that clients must honour the header. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b23` | duplicate | The base rule already explains the gateway’s arithmetic and 503 path. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-025`, `B-026`) |
| `b24` | duplicate | The base rule already applies header arithmetic on the 503 path. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-027`) |
| `b25` | duplicate | The base rule already describes client-side calculation as a guess. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b26` | duplicate | The base rule already says a client-side guess is never better. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b27` | subsumed | The retry rule includes the narrower safe set and the response-specific actions. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b28` | duplicate | The base rule already lists the actions for all four response codes. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-028`, `B-029`, `B-030`, `B-031`) |
| `b29` | duplicate | The base rule already states the consequence of combining response branches. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-032`) |
| `b30` | duplicate | The base rule already tells clients to avoid that loop. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b31` | duplicate | The batch rule states the 50-times allowance and shared window. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-033`, `B-034`, `B-035`) |
| `b32` | subsumed | The batch rule retains the identical interface and no-change client detail. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-036`, `B-037`, `B-038`, `B-039`) |
| `b33` | duplicate | The base rule already says nothing else differs between the tiers. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-040`) |
| `b34` | subsumed | The logging rule keeps the instruction and adds the minimum retention period. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b35` | duplicate | The base rule already states why refusal counts are needed. | **rejected** | declared 'duplicate', which predicts SUPPORTED; B-041 came back PARTIAL (`B-041`) |
| `b36` | subsumed | The logging paragraph retains the counts-as-evidence point. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b37` | superseded | The base heading is retained for the non-cap refusal section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b38` | duplicate | The base section already states there are three reasons and one is a cap. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-043`, `B-044`) |
| `b39` | reworded | The non-cap section retains the distinction from current-window traffic. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-045`) |
| `a41` | subsumed | The refusal list keeps all three causes and adds when an over-limit body is refu | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-048`, `A-049`, `A-050`) |
| `b40` | subsumed | The refusal list retains the three causes and the body-reading detail. | **rejected** | declared 'subsumed', which predicts SUPPORTED; B-047 came back PARTIAL (`B-047`) |
| `b41` | duplicate | The base section already explains why the distinction matters to retries. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b42` | duplicate | The base sentence already gives the suspended-credential retry consequence. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-049`) |
| `b43` | subsumed | The retry section preserves the no-success, false-outage, and wasted-budget deta | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-050`, `B-051`, `B-052`) |
| `b44` | duplicate | The increase section already states the quieter-hour solution. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-053`) |
| `b45` | reworded | The increase section retains the stated cost and broad availability of reschedul | **rejected** | declared 'reworded', and its text is in the merge (no claim traced to it) |
| `b46` | subsumed | The increase section retains the condition against assertion-only requests. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-054`) |
| `b47` | superseded | The base request keeps the measurement, traffic-shape, and deadline requirements | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a49` | subsumed | The increase section keeps the load-pattern assessment and burst-cost comparison | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-058`, `A-059`) |
| `b48` | subsumed | The increase section preserves the load-pattern review before considering the ca | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-055`) |
| `b49` | duplicate | The increase section already states the burst-smoothing cost comparison. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-056`) |
| `b50` | duplicate | The base sentence already gives the usual channel. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-057`) |
| `b51` | duplicate | The base sentence already states there is no expedited path. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-058`) |
| `b52` | reworded | The increase section retains that chasing does not speed up an answer. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-059 came back PARTIAL (`B-059`) |


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
| Calls | 12 live, 0 cached, 0 replayed |
| Tokens | 42,657 in, 37,548 out, 10,748 cached, 14,002 reasoning |
| Cost | ~$0.02 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 258.6s |
| Generated | 2026-09-27T16:22:08+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `bf7d5842201d`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
