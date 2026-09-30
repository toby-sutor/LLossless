## Verdict

**2 finding(s).** In the claims: 1 partially dropped. In the structure: 1 verbatim violation.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 65 |
| Claims extracted from `source_a.md` | 40 |
| Claims extracted from `source_b.md` | 70 |
| Forward — source claims accounted for in the merge | **109/110** |
| Forward — carried only in part | 1 |
| Forward — `source_a.md` claims accounted for | **40/40** |
| Forward — `source_b.md` claims accounted for | **69/70** (1 in part) |
| Reverse — merge claims found in a source | **65/65** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **175/175** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Partly dropped — the merge carries some of this claim

- **B-016** (`source_b.md:7`) — Callers that retry immediately are most of the reason the cap is there.
  - evidence: 'Callers that retry at once are the largest single reason the cap is there at all.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text calls immediate retriers the largest single reason, which does not necessarily mean they account for most of the reason.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 40 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 40 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Every credential has a cap. | 3 | carried | 'Every credential has a cap.' in `merged.md` -- The text states this directly. |
| 2 | When a credential's cap is spent, the gateway answers 429 at the edge. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge' in `merged.md` -- The text states that the gateway answers 429 at the edge when the cap is spent. |
| 3 | When a credential's cap is spent, the gateway answers 429 without waking the service behind it. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge — without waking the service behind it' in `merged.md` -- The text states that the 429 is sent without waking the service behind the gateway. |
| 4 | Requests are counted against the credential that presented them. | 5 | carried | 'Requests are counted against the credential that presented them' in `merged.md` -- The text states this directly. |
| 5 | Requests are counted over a fixed window of 60 seconds. | 5 | carried | 'over a fixed window of 60 seconds' in `merged.md` -- The text states that the fixed window is 60 seconds. |
| 6 | Requests are never counted against a connection. | 5 | carried | 'and never against a connection' in `merged.md` -- The text states that requests are never counted against a connection. |
| 7 | Opening a second socket does not increase a caller's allowance. | 5 | carried | 'Opening a second socket therefore buys a caller nothing.' in `merged.md` -- Saying a second socket buys a caller nothing means it does not increase the allowance. |
| 8 | A client spread across eight worker processes is throttled at exactly the point one process would have been. | 5 | carried | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `merged.md` -- The text states this directly. |
| 9 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- The text states this directly. |
| 10 | A credential marked for batch work is allowed 1000 requests in the same window. | 7 | carried | 'a credential marked for batch work is allowed 1000 in the same window' in `merged.md` -- The text states the batch allowance as 1000 in the same window. |
| 11 | Callers that retry at once are the largest single reason the cap exists. | 7 | carried | 'Callers that retry at once are the largest single reason the cap is there at all.' in `merged.md` -- The text states this with the same meaning. |
| 12 | The refusal carries a Retry-After header. | 11 | carried | 'The refusal carries a Retry-After header' in `merged.md` -- The text states this directly. |
| 13 | The Retry-After header value is a whole number of seconds to wait. | 11 | carried | 'Its value is a whole number of seconds to wait.' in `merged.md` -- The text states that the header value is a whole number of seconds to wait. |
| 14 | The gateway keeps no memory of who backed off politely. | 11 | carried | 'The gateway keeps no memory of who backed off politely' in `merged.md` -- The text states this directly. |
| 15 | Waiting longer than the Retry-After header asks earns a caller no credit. | 11 | carried | 'waiting longer than the header asks earns a caller no credit at all' in `merged.md` -- The text states this directly. |
| 16 | The body of the refusal is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- The text states this directly. |
| 17 | The refusal body names the window the gateway counted in. | 13 | carried | 'what the gateway calls the “window” it counted in' in `merged.md` -- The text states that the body names the window the gateway counted in. |
| 18 | The refusal body names the cap. | 13 | carried | 'it names the cap' in `merged.md` -- The text states that the body names the cap. |
| 19 | The refusal body names the tier. | 13 | carried | 'the tier' in `merged.md` -- The text lists the tier among the fields the body names. |
| 20 | The gateway computes the wait on the 503 path as well as the 429 path. | 19 | carried | 'The gateway has already done that arithmetic, with information the caller does not have, and the same rule holds on the 503 path' in `merged.md` -- The text says the gateway computes the wait and that the same rule holds on the 503 path. |
| 21 | A 500 may be retried once the stated wait has passed. | 21 | carried | 'a 500 may be retried once that wait has passed' in `merged.md` -- The text states this directly. |
| 22 | A 503 is the overload path. | 21 | carried | 'a 503 is the overload path' in `merged.md` -- The text states this directly. |
| 23 | A batch credential is allowed fifty times the default allowance. | 23 | carried | 'A batch credential is allowed fifty times the default allowance' in `merged.md` -- The text states this value, even though it conflicts with the 1000 figure stated elsewhere. |
| 24 | A batch credential is measured over exactly the same window as the default. | 23 | carried | 'it is measured over exactly the same window' in `merged.md` -- The text states that a batch credential is measured over exactly the same window. |
| 25 | The tier is set on the credential when it is issued. | 23 | carried | 'The tier is set on the credential when it is issued' in `merged.md` -- The text states this directly. |
| 26 | The tier cannot be asked for per call. | 23 | carried | 'The tier is set on the credential when it is issued and cannot be asked for per call.' in `merged.md` -- The text states that the tier cannot be asked for per call. |
| 27 | Nothing else about the two tiers differs. | 23 | carried | 'Nothing else about the two tiers differs in any way.' in `merged.md` -- The text states the claim directly. |
| 28 | The gateway refuses a request for three reasons. | 29 | carried | 'The gateway refuses a request for three reasons' in `merged.md` -- The text states the claim directly. |
| 29 | A credential may be suspended. | 29 | carried | 'A credential may be suspended' in `merged.md` -- The text states the claim directly. |
| 30 | A route may be closed for maintenance. | 29 | carried | 'a route may be closed for maintenance' in `merged.md` -- The text states the claim directly. |
| 31 | The request body limit is 5 megabyte. | 29 | carried | 'a body may exceed the 5 megabyte limit' in `merged.md` -- The text gives a 5 megabyte body limit. |
| 32 | None of the other refusal causes clears itself by waiting for a stated number of seconds. | 29 | carried | 'None of those three clears itself by waiting for a stated number of seconds.' in `merged.md` -- The text states that the other refusal causes do not clear by waiting. |
| 33 | A cap can be raised. | 35 | carried | 'A cap can be raised' in `merged.md` -- The text states the claim directly. |
| 34 | The number of caps raised without a measurement behind them is 0. | 35 | carried | 'the number of caps raised without a measurement behind them is 0' in `merged.md` -- The text states the claim directly. |
| 35 | The platform team looks at whether the load is smooth or bursty. | 35 | carried | 'The platform team looks at whether the load is smooth or bursty' in `merged.md` -- The text states the claim directly. |
| 36 | A burst is cheaper to smooth than it is to serve at its peak. | 35 | carried | 'a burst is cheaper to smooth than it is to serve at its peak' in `merged.md` -- The text states the claim directly. |
| 37 | Requests for an increase reach the platform team through the usual channel. | 37 | carried | 'Requests reach the platform team through the usual channel' in `merged.md` -- In the increase section, the text says requests reach the team through the usual channel. |
| 38 | Requests for an increase are answered within two working days. | 37 | carried | 'they are answered within two working days' in `merged.md` -- The text states that increase requests are answered within two working days. |
| 39 | There is no expedited path for increase requests. | 37 | carried | 'There is no expedited path' in `merged.md` -- The text states the claim directly. |
| 40 | There is no exception list for increase requests. | 37 | carried | 'no exception list' in `merged.md` -- The text states the claim directly. |

### `source_b.md` -- 70 claim(s): 0 dropped, 0 contradicted, 1 carried in part, 69 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 16 | Callers that retry immediately are most of the reason the cap is there. | 7 | carried in part | 'Callers that retry at once are the largest single reason the cap is there at all.' in `merged.md` -- The text calls immediate retriers the largest single reason, which does not necessarily mean they account for most of the reason. |
| 1 | Every credential has a cap of its own. | 3 | carried | 'Every credential has a cap.' in `merged.md` -- The text states that each credential has a cap. |
| 2 | When the cap is spent the gateway answers 429 at the edge. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge' in `merged.md` -- The text states the claim directly. |
| 3 | When the cap is spent the gateway answers without troubling the service behind it. | 3 | carried | 'without waking the service behind it' in `merged.md` -- Not waking the service has the same meaning as not troubling it. |
| 4 | Requests are counted against the credential rather than the connection. | 5 | carried | 'Requests are counted against the credential that presented them, over a fixed window of 60 seconds whose start the gateway does not disclose, and never against a connection.' in `merged.md` -- Requests are counted against the credential and never against a connection. |
| 5 | Requests are counted over a fixed window of 60 seconds. | 5 | carried | 'over a fixed window of 60 seconds' in `merged.md` -- The text states the claim directly. |
| 6 | The gateway doesn't disclose the start of the 60-second window. | 5 | carried | 'a fixed window of 60 seconds whose start the gateway does not disclose' in `merged.md` -- The text states the claim directly. |
| 7 | There is nothing to be gained by opening more sockets to avoid the gateway cap. | 5 | carried | 'Opening a second socket therefore buys a caller nothing.' in `merged.md` -- The text says additional sockets gain the caller nothing. |
| 8 | The request count follows the credential wherever the caller puts it, including across hosts. | 5 | carried | 'The count follows the credential wherever the caller happens to put it, including across hosts.' in `merged.md` -- The text states the claim directly. |
| 9 | A caller spread over many worker processes is throttled at the same point a single process would have been. | 5 | carried | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `merged.md` -- The text illustrates the point with eight worker processes, which carries the claim about many processes. |
| 10 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- The text states the claim directly. |
| 11 | The default allowance of 100 requests is enough for every interactive use of the API the platform team has seen. | 7 | carried | 'The default allowance is 100 requests in a window, which is enough for every interactive use of this API the platform team has seen' in `merged.md` -- The text states that the 100-request default covers every interactive use the platform team has seen. |
| 12 | A caller that needs more than 100 requests in a window is almost always doing batch work under an interactive credential. | 7 | carried | 'A caller that needs more than the default is almost always doing batch work under an interactive credential.' in `merged.md` -- The default is 100 requests, so needing more than the default is the same as needing more than 100. |
| 13 | A 429 refusal isn't an outage. | 7 | carried | 'A refusal is not an outage' in `merged.md` -- The text directly states that a refusal is not an outage. |
| 14 | A 429 refusal isn't a bug in the gateway. | 7 | carried | 'it is not a bug in the gateway' in `merged.md` -- The text directly states that a refusal is not a gateway bug. |
| 15 | A 429 refusal is capacity being held for a request somebody else has already been promised. | 7 | carried | 'It is the platform declining to spend capacity that has already been promised to somebody else' in `merged.md` -- The text describes a refusal as the platform holding capacity that was already promised to someone else. |
| 17 | The refusal header is called Retry-After. | 11 | carried | 'The refusal carries a Retry-After header' in `merged.md` -- The text names the header as Retry-After. |
| 18 | The Retry-After value is a whole number of seconds. | 11 | carried | 'Its value is a whole number of seconds to wait.' in `merged.md` -- The text states that the header value is a whole number of seconds. |
| 19 | The Retry-After header is present on every refusal the gateway sends. | 11 | carried | 'the header is present on every refusal the gateway sends' in `merged.md` -- The text states the header's presence on every refusal directly. |
| 20 | Waiting for the Retry-After duration and then continuing is the entire contract. | 11 | carried | 'Waiting that long and then continuing is the whole of the contract' in `merged.md` -- 'The whole of the contract' has the same meaning as 'the entire contract'. |
| 21 | Waiting longer than the Retry-After header asks earns nothing. | 11 | carried | 'waiting longer than the header asks earns a caller no credit at all' in `merged.md` -- The text states that waiting longer than asked earns no credit. |
| 22 | Nobody at the gateway end is keeping score of how long callers wait. | 11 | carried | 'The gateway keeps no memory of who backed off politely' in `merged.md` -- Keeping no memory of polite back-off means no score is kept of how long callers wait. |
| 23 | The refusal response body is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- The text states directly that the refusal body is JSON. |
| 24 | The refusal response body repeats the cap, the window and the tier as plain fields. | 13 | carried | 'it names the cap, the tier and what the gateway calls the “window” it counted in, as plain fields' in `merged.md` -- The body names the cap, the tier and the window as plain fields. |
| 25 | None of the response body fields is a substitute for the Retry-After header. | 13 | carried | 'None of those fields is a substitute for the header' in `merged.md` -- The text states directly that no body field substitutes for the header. |
| 26 | The refusal response body is for the human reading the log afterwards. | 13 | carried | 'The body is there so that a human reading a log afterwards can see why the request was refused' in `merged.md` -- The text states that the body exists for a human reading the log afterwards. |
| 27 | There are four rules for what the client does. | 17 | carried | 'Four rules, given in the order they should be applied.' in `merged.md` -- The retry section sets out four rules for the client. |
| 28 | The four client rules are to be applied in the order they are given. | 17 | carried | 'Four rules, given in the order they should be applied.' in `merged.md` -- The text says the rules are given in the order they should be applied. |
| 29 | Clients should honour the Retry-After header and not compute their own wait. | 19 | carried | 'Honour the header, every time, and do not compute your own wait.' in `merged.md` -- Rule one states this directly. |
| 30 | The gateway computes the wait with information the caller cannot see. | 19 | carried | 'The gateway has already done that arithmetic, with information the caller does not have' in `merged.md` -- The gateway computes the wait using information the caller lacks. |
| 31 | On the 503 path the rule to honour the header and not compute your own wait also holds. | 19 | carried | 'the same rule holds on the 503 path' in `merged.md` -- The text says the honour-the-header rule also holds on the 503 path. |
| 32 | The cause of a 503 refusal is entirely different from that of a 429 refusal. | 19 | carried | 'even though the cause of the refusal is an entirely different one' in `merged.md` -- The text states that the cause of a 503 refusal is entirely different. |
| 33 | The set of responses safe to retry is smaller than the set of responses that aren't a success. | 21 | carried | 'Retry only what is safe to retry, which is a smaller set than the set of responses that are not a success' in `merged.md` -- The text states directly that the safe-to-retry set is smaller than the non-success set. |
| 34 | A 200 response needs nothing. | 21 | carried | 'A 200 wants nothing' in `merged.md` -- 'Wants nothing' has the same meaning as 'needs nothing'. |
| 35 | A 429 response needs the stated wait. | 21 | carried | 'a 429 wants the stated wait' in `merged.md` -- 'Wants the stated wait' has the same meaning as 'needs the stated wait'. |
| 36 | A 500 response can be retried once the stated wait has passed. | 21 | carried | 'a 500 may be retried once that wait has passed' in `merged.md` -- The text states that a 500 may be retried once the wait has passed. |
| 37 | A 503 response means the platform itself is overloaded. | 21 | carried | 'a 503 is the overload path, meaning the platform itself is overloaded' in `merged.md` -- The text states directly that a 503 means the platform itself is overloaded. |
| 38 | A caller that folds 200, 429, 500 and 503 into one branch will retry hardest during exactly the incident the cap was installed to survive. | 21 | carried | 'A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive.' in `merged.md` -- Folding all four cases into one branch necessarily folds every non-success together, which the text says leads to the heaviest retrying during the incident. |
| 39 | A batch credential is allowed 1000 requests in a window. | 23 | carried | 'a credential marked for batch work is allowed 1000 in the same window' in `merged.md` -- The text states that a batch credential is allowed 1000 requests in the window. |
| 40 | The batch allowance of 1000 requests is 50 times the default. | 23 | carried | 'A batch credential is allowed fifty times the default allowance' in `merged.md` -- The text states the fifty-times ratio, though this sits inconsistently with the stated 100 default and 1000 batch figures, which should be recorded as a conflict. |
| 41 | The batch allowance is not a separate counting scheme. | 23 | carried | 'This is not a separate counting scheme.' in `merged.md` -- The text states directly that batch is not a separate counting scheme. |
| 42 | The window, the header and the body for the batch tier are identical to the interactive case. | 23 | carried | 'The window, the header and the body are identical to the interactive case' in `merged.md` -- The text states that the window, header and body are identical to the interactive case. |
| 43 | A client written for one tier needs no change to run against the other tier. | 23 | carried | 'a client written for one tier needs no change at all to run against the other' in `merged.md` -- The text states that a client written for one tier needs no change to run against the other. |
| 44 | Nothing else about the batch tier differs from the default. | 23 | carried | 'Nothing else about the two tiers differs in any way.' in `merged.md` -- The text states that nothing else differs between the two tiers. |
| 45 | Clients should log every refusal they see. | 25 | carried | 'Log every refusal seen' in `merged.md` -- The text instructs clients to log every refusal they see. |
| 46 | Clients should keep the refusal log for at least a week. | 25 | carried | 'keep the log for at least a week' in `merged.md` -- The text says to keep the log for at least a week. |
| 47 | A caller that cannot say how often it was refused can't make a case for a larger cap. | 25 | carried | 'A caller that cannot say how often it was refused last week cannot argue for a larger cap' in `merged.md` -- The text says that such a caller cannot argue for a larger cap. |
| 48 | The platform team won't assemble the case for a larger cap on a caller's behalf. | 25 | carried | 'nobody at the far end will assemble that argument on its behalf' in `merged.md` -- The text states that nobody at the far end, meaning the platform side, will assemble the argument for the caller. |
| 49 | The gateway refuses a request for three separate reasons. | 29 | carried | 'The gateway refuses a request for three reasons' in `merged.md` -- The text states that the gateway refuses requests for three reasons. |
| 50 | Only one of the three reasons the gateway refuses a request is a cap. | 29 | carried | 'only one of them is the one above' in `merged.md` -- The text states that only one of the three reasons is the cap described above. |
| 51 | Two of the three refusal reasons have nothing to do with how much traffic a caller has sent in the current window. | 29 | carried | 'the other two have nothing to do with how much traffic a caller has sent in the window it is currently in' in `merged.md` -- The text states that the other two reasons are unrelated to traffic sent in the current window. |
| 52 | A credential can be suspended. | 29 | carried | 'A credential may be suspended' in `merged.md` -- The text states that a credential may be suspended. |
| 53 | A route can be closed while it is being repaired. | 29 | carried | 'a route may be closed for maintenance' in `merged.md` -- The text says a route may be closed for maintenance, which matches being closed while it is repaired. |
| 54 | The request body limit is 5 megabyte. | 29 | carried | 'the 5 megabyte limit' in `merged.md` -- The text states that the body limit is 5 megabyte. |
| 55 | A request body over the 5 megabyte limit is refused before it has been read. | 29 | carried | 'in which case it is refused before it has been read at all' in `merged.md` -- The text says an oversize body is refused before it has been read. |
| 56 | A loop retrying against a suspended credential burns its whole budget and reaches nothing. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `merged.md` -- The text states that such a loop spends its whole budget without reaching the service. |
| 57 | The log after retrying against a suspended credential shows a long run of refusals and no successes. | 31 | carried | 'The log afterwards shows nothing but a long run of refusals and no successes' in `merged.md` -- The text states that the log shows a long run of refusals and no successes. |
| 58 | The run of refusals against a suspended credential is not an outage. | 31 | carried | 'which reads like an outage and is not one' in `merged.md` -- The text states that the run of refusals is not an outage. |
| 59 | The budget wasted retrying against a suspended credential is the caller's own. | 31 | carried | 'the budget it wastes is the caller’s own' in `merged.md` -- The text states that the wasted budget is the caller's own. |
| 60 | A caller that can move half its work to a quieter hour usually finds it doesn't need a larger cap. | 33 | carried | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `merged.md` -- The text states that moving half the work to a quieter hour usually meets the caller's needs without raising the cap. |
| 61 | Moving work to a quieter hour is available to almost everybody. | 33 | carried | 'it is the cheapest fix available to anybody, and it is available to almost everybody' in `merged.md` -- The text says moving half the work to a quieter hour is available to almost everybody. |
| 62 | A cap can be raised. | 33 | carried | 'A cap can be raised' in `merged.md` -- The text states this directly. |
| 63 | A cap is not raised on the strength of an assertion that the current one is too small. | 33 | carried | 'but not on the strength of an assertion that the current one is too small' in `merged.md` -- The text states this directly. |
| 64 | A request for a cap raise should bring the refusal counts for a full week, the shape of the traffic across the day, and the deadline the traffic exists to meet. | 33 | carried | 'Bring a week of refusal counts, the shape of the traffic across the day, and the deadline that traffic is serving.' in `merged.md` -- All three items are listed with the same meaning. |
| 65 | The platform team wants to know whether the load is smooth or bursty before it looks at the number. | 35 | carried | 'The platform team looks at whether the load is smooth or bursty before it looks at the number at all' in `merged.md` -- The text states this in equivalent words. |
| 66 | A burst is cheaper to smooth out than it is to serve at its peak. | 35 | carried | 'a burst is cheaper to smooth than it is to serve at its peak' in `merged.md` -- The text states this directly. |
| 67 | Cap raise requests go to the platform team through the usual channel. | 35 | carried | 'Requests reach the platform team through the usual channel' in `merged.md` -- In the section on asking for an increase, requests are said to reach the platform team through the usual channel. |
| 68 | There is no expedited path for cap raise requests. | 37 | carried | 'There is no expedited path' in `merged.md` -- The text states this directly. |
| 69 | An answer to a cap raise request takes two working days. | 37 | carried | 'they are answered within two working days' in `merged.md` -- The text gives a two-working-day turnaround for answers to requests, which carries the claim's two working days. |
| 70 | Chasing a cap raise request doesn't make the answer take fewer days. | 37 | carried | 'chasing an answer does not make it take fewer' in `merged.md` -- The text states that chasing does not shorten the time to an answer. |

### `merged.md` -- 65 claim(s): 0 invented, 0 contradicted, 0 supported in part, 65 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Every credential has a cap. | supported | `source_a.md` | 'Every credential has a cap.' in `source_a.md` -- Source A states this verbatim. |
| 2 | When a credential's cap is spent the gateway answers 429 at the edge. | supported | `source_a.md` | 'When that cap is spent the gateway answers 429 at the edge' in `source_a.md` -- Source A states the gateway answers 429 at the edge when the cap is spent. |
| 3 | The gateway's 429 refusal does not wake the service behind the gateway. | supported | `source_a.md` | 'without waking the service behind it' in `source_a.md` -- Source A says the 429 is given without waking the service behind the gateway. |
| 4 | Requests are counted against the credential that presented them. | supported | `source_a.md` | 'Requests are counted against the credential that presented them' in `source_a.md` -- Source A states this directly. |
| 5 | Requests are counted over a fixed window of 60 seconds. | supported | `source_a.md` | 'over a fixed window of 60 seconds' in `source_a.md` -- Source A states requests are counted over a fixed 60-second window. |
| 6 | The gateway does not disclose the start of the 60-second counting window. | supported | `source_b.md` | 'over a fixed window of 60 seconds whose start the gateway doesn’t disclose' in `source_b.md` -- Source B says the gateway does not disclose the window's start. |
| 7 | Requests are never counted against a connection. | supported | `source_a.md` | 'and never against a connection' in `source_a.md` -- Source A says requests are never counted against a connection. |
| 8 | The request count follows the credential across hosts. | supported | `source_b.md` | 'The count follows the credential wherever the caller happens to put it, including across hosts.' in `source_b.md` -- Source B states the count follows the credential across hosts. |
| 9 | Opening a second socket does not increase a caller's allowance. | supported | `source_a.md` | 'Opening a second socket therefore buys a caller nothing.' in `source_a.md` -- Source A says a second socket buys a caller nothing, which is the same meaning. |
| 10 | A client spread across eight worker processes is throttled at exactly the point one process would have been. | supported | `source_a.md` | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `source_a.md` -- Source A states this verbatim. |
| 11 | The default allowance is 100 requests in a window. | supported | `source_a.md` | 'The default allowance is 100 requests in a window' in `source_a.md` -- Source A states the default allowance is 100 requests per window. |
| 12 | The default allowance of 100 requests is enough for every interactive use of the API the platform team has seen. | supported | `source_b.md` | 'which is enough for every interactive use of this API the platform team has seen' in `source_b.md` -- Source B says the default is enough for every interactive use the team has seen. |
| 13 | A credential marked for batch work is allowed 1000 requests in the same window. | supported | `source_a.md` | 'a credential marked for batch work is allowed 1000 in the same window' in `source_a.md` -- Source A states the batch allowance of 1000 in the same window. |
| 14 | A caller that needs more than the default allowance is almost always doing batch work under an interactive credential. | supported | `source_b.md` | 'a caller that needs more than that is almost always doing batch work under an interactive credential' in `source_b.md` -- Source B states this directly. |
| 15 | A rate-limit refusal is not an outage. | supported | `source_a.md` | 'A refusal is not an outage' in `source_a.md` -- Source A states a refusal is not an outage. |
| 16 | A rate-limit refusal is not a bug in the gateway. | supported | `source_b.md` | 'The refusal isn’t an outage and it isn’t a bug in the gateway' in `source_b.md` -- Source B says the refusal is not a bug in the gateway. |
| 17 | A rate-limit refusal is the platform declining to spend capacity that has already been promised to somebody else. | supported | `source_a.md` | 'It is the platform declining to spend capacity that has already been promised to somebody else' in `source_a.md` -- Source A states this directly. |
| 18 | Callers that retry at once are the largest single reason the cap exists. | supported | `source_a.md` | 'Callers that retry at once are the largest single reason the cap is there at all.' in `source_a.md` -- Source A states this with the same meaning. |
| 19 | The refusal carries a Retry-After header. | supported | `source_a.md` | 'The refusal carries a Retry-After header.' in `source_a.md` -- Source A states this verbatim. |
| 20 | The Retry-After header is present on every refusal the gateway sends. | supported | `source_b.md` | 'it is present on every refusal the gateway sends' in `source_b.md` -- Source B says the header is present on every refusal. |
| 21 | The Retry-After header value is a whole number of seconds to wait. | supported | `source_a.md` | 'Its value is a whole number of seconds to wait.' in `source_a.md` -- Source A states this directly. |
| 22 | Waiting as long as the Retry-After header specifies and then continuing is the whole of the contract. | supported | `source_a.md` | 'Waiting that long and then continuing is the whole of the contract' in `source_a.md` -- Source A states this directly. |
| 23 | The gateway keeps no memory of who backed off politely. | supported | `source_a.md` | 'The gateway keeps no memory of who backed off politely' in `source_a.md` -- Source A states this verbatim. |
| 24 | Waiting longer than the Retry-After header asks earns a caller no credit. | supported | `source_a.md` | 'waiting longer than the header asks earns a caller no credit at all' in `source_a.md` -- Source A states this directly. |
| 25 | The body of the refusal is JSON. | supported | `source_a.md` | 'The body of the refusal is JSON' in `source_a.md` -- Source A states this verbatim. |
| 26 | The refusal body names the cap, the tier and the window as plain fields. | supported | `source_b.md` | 'The response body is JSON and it repeats the cap, the window and the tier as plain fields.' in `source_b.md` -- Source B says the body repeats the cap, window and tier as plain fields. |
| 27 | None of the refusal body fields is a substitute for the Retry-After header. | supported | `source_a.md` | 'None of those fields is a substitute for the header' in `source_a.md` -- Source A says none of the body fields substitutes for the header. |
| 28 | The refusal body is there so that a human reading a log can see why the request was refused. | supported | `source_a.md` | 'The body is there so that a human reading a log afterwards can see why the request was refused' in `source_a.md` -- Source A states this purpose of the body directly. |
| 29 | Nothing in the refusal body is meant for the retry loop. | supported | `source_a.md` | 'nothing in it is meant for the retry loop' in `source_a.md` -- Source A states nothing in the body is meant for the retry loop. |
| 30 | The gateway computes the wait with information the caller does not have. | supported | `source_a.md` | 'The gateway has already done that arithmetic, with information the caller does not have' in `source_a.md` -- Source A says the gateway computes the wait with information the caller lacks. |
| 31 | The rule to honour the header also holds on the 503 path. | supported | `source_b.md` | 'On the 503 path the same rule holds' in `source_b.md` -- Source B says the honour-the-header rule holds on the 503 path. |
| 32 | The cause of a 503 refusal is different from the cause of a 429 refusal. | supported | `source_b.md` | 'even though the cause of the refusal is an entirely different one' in `source_b.md` -- Source B says the 503 refusal has an entirely different cause. |
| 33 | A client-side token bucket that mirrors the gateway's own counters does not help. | supported | `source_b.md` | 'two counters that disagree are worse than one counter that refuses' in `source_b.md` -- Source B deliberately rejected a mirroring client-side token bucket as worse than relying on the gateway's counter. |
| 34 | A 200 response requires no retry. | supported | `source_b.md` | 'A 200 needs nothing' in `source_b.md` -- Source B states a 200 needs nothing. |
| 35 | A 429 response requires waiting the stated wait. | supported | `source_b.md` | 'a 429 needs the stated wait' in `source_b.md` -- Source B states a 429 needs the stated wait. |
| 36 | A 500 response may be retried once the stated wait has passed. | supported | `source_b.md` | 'a 500 can be retried once that wait has passed' in `source_b.md` -- Source B states a 500 can be retried once the wait has passed. |
| 37 | A 503 response indicates the platform itself is overloaded. | supported | `source_b.md` | 'a 503 means the platform itself is overloaded' in `source_b.md` -- Source B states a 503 means the platform itself is overloaded. |
| 38 | A client that folds every non-success into one branch will retry hardest during the incident the cap was installed to survive. | supported | `source_a.md` | 'A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive.' in `source_a.md` -- Source A states this directly. |
| 39 | A batch credential is allowed fifty times the default allowance. | supported | `source_a.md` | 'A batch credential is allowed fifty times the default allowance' in `source_a.md` -- Source A states the batch allowance is fifty times the default. |
| 40 | A batch credential is measured over exactly the same window as the default allowance. | supported | `source_a.md` | 'it is measured over exactly the same window' in `source_a.md` -- Source A says the batch credential uses exactly the same window. |
| 41 | Batch credentials do not use a separate counting scheme. | supported | `source_b.md` | 'not a separate counting scheme' in `source_b.md` -- Source B says the batch tier is not a separate counting scheme. |
| 42 | The tier is set on the credential when it is issued. | supported | `source_a.md` | 'The tier is set on the credential when it is issued' in `source_a.md` -- Source A states the tier is set on the credential at issue. |
| 43 | The tier cannot be requested per call. | supported | `source_a.md` | 'cannot be asked for per call' in `source_a.md` -- Source A says the tier cannot be asked for per call. |
| 44 | The window, the header and the body are identical for batch and interactive tiers. | supported | `source_b.md` | 'The window, the header and the body are identical to the interactive case' in `source_b.md` -- Source B states the window, header and body are identical across tiers. |
| 45 | A client written for one tier needs no change to run against the other tier. | supported | `source_b.md` | 'a client written for one tier needs no change at all to run against the other' in `source_b.md` -- Source B states this directly. |
| 46 | Nothing else about the batch and interactive tiers differs. | supported | `source_a.md` | 'Nothing else about the two tiers differs in any way.' in `source_a.md` -- Source A states nothing else differs between the tiers. |
| 47 | Callers should keep the log of refusals for at least a week. | supported | `source_b.md` | 'keep the log for at least a week' in `source_b.md` -- Source B says to keep the refusal log for at least a week. |
| 48 | The refusal log line should carry the credential, the window and the wait. | supported | `source_a.md` | 'The log line should carry the credential, the window and the wait.' in `source_a.md` -- Source A states this directly. |
| 49 | The gateway refuses a request for three reasons. | supported | `source_a.md` | 'The gateway refuses a request for three reasons' in `source_a.md` -- Source A states the gateway refuses for three reasons. |
| 50 | A credential may be suspended. | supported | `source_a.md` | 'A credential may be suspended' in `source_a.md` -- Source A states a credential may be suspended. |
| 51 | A route may be closed for maintenance. | supported | `source_a.md` | 'a route may be closed for maintenance' in `source_a.md` -- Source A states a route may be closed for maintenance. |
| 52 | The request body limit is 5 megabytes. | supported | `source_a.md` | 'a body may exceed the 5 megabyte limit' in `source_a.md` -- Source A names a 5 megabyte body limit. |
| 53 | A body exceeding the 5 megabyte limit is refused before it has been read. | supported | `source_b.md` | 'a request body over the 5 megabyte limit is refused before it has been read at all' in `source_b.md` -- Source B states oversized bodies are refused before being read. |
| 54 | A suspended credential, a closed route, and an oversized body do not clear by waiting for a stated number of seconds. | supported | `source_a.md` | 'None of those three clears itself by waiting for a stated number of seconds.' in `source_a.md` -- Source A states none of the three other refusals clears by waiting. |
| 55 | A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service. | supported | `source_a.md` | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `source_a.md` -- Source A states this verbatim. |
| 56 | Distinguishing the cases by reading the status code costs one comparison. | supported | `source_a.md` | 'Reading the status code rather than the class it belongs to is what separates the two cases, and it costs one comparison.' in `source_a.md` -- Source A states reading the status code costs one comparison. |
| 57 | A cap can be raised. | supported | `source_a.md` | 'A cap can be raised' in `source_a.md` -- Both sources state a cap can be raised. |
| 58 | The number of caps raised without a measurement behind them is 0. | supported | `source_a.md` | 'the number of caps raised without a measurement behind them is 0' in `source_a.md` -- Source A states this directly. |
| 59 | The platform team looks at whether the load is smooth or bursty before it looks at the number. | supported | `source_b.md` | 'The team wants to know whether the load is smooth or bursty before it looks at the number at all.' in `source_b.md` -- Source B states the team checks smooth versus bursty before looking at the number. |
| 60 | A burst is cheaper to smooth than to serve at its peak. | supported | `source_a.md` | 'a burst is cheaper to smooth than it is to serve at its peak' in `source_a.md` -- Source A states this directly. |
| 61 | A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap. | supported | `source_a.md` | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `source_a.md` -- Source A states this directly. |
| 62 | Requests for a cap increase reach the platform team through the usual channel. | supported | `source_a.md` | 'Requests reach the platform team through the usual channel' in `source_a.md` -- Source A states requests reach the platform team through the usual channel. |
| 63 | Requests for a cap increase are answered within two working days. | supported | `source_a.md` | 'they are answered within two working days' in `source_a.md` -- Source A states requests are answered within two working days. |
| 64 | There is no expedited path for cap increase requests. | supported | `source_a.md` | 'There is no expedited path and no exception list.' in `source_a.md` -- Source A states there is no expedited path. |
| 65 | There is no exception list for cap increase requests. | supported | `source_a.md` | 'There is no expedited path and no exception list.' in `source_a.md` -- Source A states there is no exception list. |

## Structure

**9** mechanical check(s) over **104** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **65** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **110**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 25 run(s) over 54 attributed segment(s) — sources interleaved. 6 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Verbatim violation — an invariant-core token did not survive unchanged

- `b31` (`source_b.md`) — numeric '50' (times) does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **70** departure(s) from its sources. Checking them confirms 53, rejects 4, and leaves 13 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 104 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a4` | reconciled | Counting basis combined with undisclosed window start. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-004`, `A-005`, `A-006`) |
| `a7` | reconciled | Allowances combined with sufficiency note from b. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-009`, `A-010`) |
| `a8` | reworded | Not-an-outage statement extended with b's not-a-bug point. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a12` | reworded | Header sentence extended with presence on every refusal. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-012`) |
| `a14` | reworded | Contract sentence extended with b's closing remark. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a16` | reworded | Body field list merged into one sentence. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-016`, `A-017`) |
| `a17` | subsumed | Cap and tier folded into body field sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-018`, `A-019`) |
| `a18` | reworded | Body-parsing warning combined with b's wording. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a22` | reworded | Rule 1 extended with b's instruction. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a23` | reworded | 503 path note merged with b's detail. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-020`) |
| `a26` | reworded | Rule 2 extended with b's clarification. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a27` | reworded | 503 meaning added from b. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-021`, `A-022`) |
| `a35` | reworded | Rule 4 extended with retention period. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a40` | reworded | Three reasons sentence merged with b's detail. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-028`) |
| `a41` | reworded | Oversize body detail added from b. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-029`, `A-030`, `A-031`) |
| `a43` | reworded | b's comparative wording adopted. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a44` | reworded | Suspended-credential loop split and merged with b. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a47` | reworded | Raising condition merged with b's wording. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-033`, `A-034`) |
| `a49` | reworded | Ordering detail added from b. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-035`, `A-036`) |
| `a50` | reworded | Quieter-hour advice merged with b's remark. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a51` | reworded | Response time merged with b's chasing note. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-037`, `A-038`) |
| `b1` | superseded | Base title kept. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Rate limiting and the 429 contract for gateway clients' and says so (no claim traced to it) |
| `b2` | duplicate | Same fact as a2. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-001`) |
| `b3` | duplicate | Same fact as a3. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-002`, `B-003`) |
| `b4` | reworded | Draft history restated generally under rule 1. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b5` | reconciled | Counting basis combined with undisclosed window start. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-004`, `B-005`, `B-006`) |
| `b6` | duplicate | Same fact as a5. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-007`) |
| `b8` | duplicate | Same fact as a6. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-009`) |
| `b9` | reconciled | Default allowance combined with a7's tiers. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-010`, `B-011`, `B-012`) |
| `b10` | subsumed | Folded into a8 and a9. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-013`, `B-014`, `B-015`) |
| `b11` | duplicate | Same point as a10. | **rejected** | declared 'duplicate', which predicts SUPPORTED; B-016 came back PARTIAL (`B-016`) |
| `b12` | duplicate | Same heading as a11. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b13` | duplicate | Header name already stated. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-017`) |
| `b14` | subsumed | Presence and value folded into header sentences. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-018`, `B-019`) |
| `b15` | subsumed | Folded into a14. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-020`) |
| `b16` | duplicate | Same point as a15. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-021`, `B-022`) |
| `b17` | subsumed | Folded into body field sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-023`, `B-024`) |
| `b18` | subsumed | Folded into a18. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-025`) |
| `b19` | duplicate | Same point as a19. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-026`) |
| `b20` | superseded | Base heading kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b21` | duplicate | Same point as a21. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-027`, `B-028`) |
| `b22` | subsumed | Folded into rule 1 heading. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-029`) |
| `b23` | duplicate | Same point as a23. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-030`) |
| `b24` | subsumed | Folded into a23. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-031`, `B-032`) |
| `b25` | duplicate | Same point as a24. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b26` | duplicate | Same point as a25. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b27` | subsumed | Folded into rule 2 heading. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-033`) |
| `b28` | subsumed | Folded into a27. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-034`, `B-035`, `B-036`, `B-037`) |
| `b29` | duplicate | Same point as a29. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-038`) |
| `b30` | duplicate | Same point as a30. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b31` | subsumed | Batch figure stated earlier; counting-scheme point kept. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-039`, `B-040`, `B-041`) |
| `b33` | duplicate | Same point as a34. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-044`) |
| `b34` | subsumed | Folded into rule 4 heading. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-045`, `B-046`) |
| `b35` | duplicate | Same point as a36. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-047`, `B-048`) |
| `b37` | superseded | Base heading kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b38` | subsumed | Folded into a40. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-049`, `B-050`) |
| `b39` | subsumed | Folded into a40. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-051`) |
| `b40` | subsumed | Folded into a41. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-052`, `B-053`, `B-054`, `B-055`) |
| `b41` | subsumed | Folded into a43. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b42` | subsumed | Folded into a44. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-056`) |
| `b43` | subsumed | Folded into a44. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-057`, `B-058`, `B-059`) |
| `b44` | duplicate | Same point as a50. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-060`) |
| `b45` | subsumed | Folded into a50. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-061`) |
| `b46` | subsumed | Folded into a47. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-062`, `B-063`) |
| `b47` | duplicate | Same point as a48. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-064`) |
| `b48` | subsumed | Folded into a49. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-065`) |
| `b49` | duplicate | Same point as a49. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-066`) |
| `b50` | duplicate | Same point as a51. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-067`) |
| `b51` | duplicate | Same point as a52. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-068`) |
| `b52` | subsumed | Folded into a51. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-069`, `B-070`) |


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
| Calls | 13 live, 0 cached, 0 replayed |
| Tokens | 71,683 in, 58,899 out |
| Cost | ~$1.46 estimated (rates read 2026-09-25) |
| Schema repairs | 1 |
| Errors | 0 |
| Duration | 438.0s |
| Generated | 2026-09-27T17:11:59+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
