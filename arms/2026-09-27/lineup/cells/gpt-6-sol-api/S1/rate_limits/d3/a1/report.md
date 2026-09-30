## Verdict

**8 finding(s).** In the claims: 6 contradicted. In the structure: 1 undeclared absence, 1 verbatim violation.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 65 |
| Claims extracted from `source_a.md` | 54 |
| Claims extracted from `source_b.md` | 57 |
| Forward — source claims accounted for in the merge | **105/111** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **52/54** |
| Forward — `source_b.md` claims accounted for | **53/57** |
| Reverse — merge claims found in a source | **65/65** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **176/176** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **A-032** -- the two documents disagree
  - `source_a.md:23` says: A batch credential is allowed fifty times the default allowance.
  - `merged.md` says: 'The default allowance is 100 requests in a window, and a credential marked for batch work is allowed 1000 in the same window.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The batch allowance is ten times, not fifty times, the default.
- **A-037** -- the two documents disagree
  - `source_a.md:29` says: The gateway refuses a request for three reasons.
  - `merged.md` says: 'The gateway can refuse requests for reasons other than a spent cap. A credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text identifies a spent cap plus three other refusal reasons, not three reasons total.
- **B-028** -- the two documents disagree
  - `source_b.md:23` says: The batch allowance is 50 times the default.
  - `merged.md` says: 'The default allowance is 100 requests in a window, and a credential marked for batch work is allowed 1000 in the same window.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The stated allowances make batch 10 times the default, not 50 times.
- **B-038** -- the two documents disagree
  - `source_b.md:29` says: The gateway refuses a request for three separate reasons.
  - `merged.md` says: 'The gateway can refuse requests for reasons other than a spent cap. A credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text lists three reasons in addition to a spent cap, rather than three reasons total.
- **B-039** -- the two documents disagree
  - `source_b.md:29` says: Only one of the gateway’s three reasons for refusing a request is a cap.
  - `merged.md` says: 'The gateway can refuse requests for reasons other than a spent cap. A credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: A spent cap plus the three listed alternatives makes four reasons, not three.
- **B-040** -- the two documents disagree
  - `source_b.md:29` says: Two of the gateway’s three reasons for refusing a request have nothing to do with how much traffic a caller has sent in its current window.
  - `merged.md` says: 'The gateway can refuse requests for reasons other than a spent cap. A credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The claim's premise of three total reasons conflicts with the cap plus three listed alternatives.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 54 claim(s): 0 dropped, 2 contradicted, 0 carried in part, 52 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 32 | A batch credential is allowed fifty times the default allowance. | 23 | contradicted | 'The default allowance is 100 requests in a window, and a credential marked for batch work is allowed 1000 in the same window.' in `merged.md` -- The batch allowance is ten times, not fifty times, the default. |
| 37 | The gateway refuses a request for three reasons. | 29 | contradicted | 'The gateway can refuse requests for reasons other than a spent cap. A credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit.' in `merged.md` -- The text identifies a spent cap plus three other refusal reasons, not three reasons total. |
| 1 | Every credential has a cap. | 3 | carried | 'Every credential has a cap.' in `merged.md` -- The text states the claim directly. |
| 2 | When a credential’s cap is spent, the gateway answers 429 at the edge. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge' in `merged.md` -- The text specifies the response and where it is issued. |
| 3 | When a credential’s cap is spent, the gateway answers 429 without waking the service behind the gateway. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge — without waking the service behind it' in `merged.md` -- The text states both the 429 response and that the service is not woken. |
| 4 | Requests are counted against the credential that presented them. | 5 | carried | 'Requests are counted against the credential that presented them' in `merged.md` -- The text identifies the credential as the basis for counting. |
| 5 | Requests are counted over a fixed window of 60 seconds. | 5 | carried | 'over a fixed window of 60 seconds' in `merged.md` -- The text gives the fixed counting window. |
| 6 | Requests are never counted against a connection. | 5 | carried | 'and never against a connection' in `merged.md` -- The text explicitly rules out counting against a connection. |
| 7 | Opening a second socket does not increase a caller’s allowance. | 5 | carried | 'Opening a second socket therefore buys a caller nothing.' in `merged.md` -- A second socket provides no additional allowance. |
| 8 | A client spread across eight worker processes is throttled at exactly the point one process would have been. | 5 | carried | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `merged.md` -- The text states the same throttling point for eight processes and one. |
| 9 | A client spread across eight worker processes uses extra file descriptors. | 5 | carried | 'A client spread across eight worker processes is throttled at exactly the point one process would have been — and pays for the extra file descriptors as well.' in `merged.md` -- The text says the eight-process client incurs extra file descriptors. |
| 10 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- The text gives the default allowance as 100 requests per window. |
| 11 | A credential marked for batch work is allowed 1000 in the same window. | 7 | carried | 'a credential marked for batch work is allowed 1000 in the same window' in `merged.md` -- The text gives the batch allowance and says it uses the same window. |
| 12 | A refusal is not an outage. | 7 | carried | 'A refusal is not an outage' in `merged.md` -- The text states the claim directly. |
| 13 | The platform declines requests when the capacity for them has already been promised to somebody else. | 7 | carried | 'It is the platform declining to spend capacity that has already been promised to somebody else' in `merged.md` -- The text describes a refusal as declining to spend already-promised capacity. |
| 14 | Callers that retry at once are the largest single reason the cap exists. | 7 | carried | 'Callers that retry at once are the largest single reason the cap is there at all.' in `merged.md` -- The text states the claim directly. |
| 15 | The refusal carries a Retry-After header. | 11 | carried | 'The refusal carries a Retry-After header.' in `merged.md` -- The text states the claim directly. |
| 16 | The Retry-After header’s value is a whole number of seconds to wait. | 11 | carried | 'Its value is a whole number of seconds to wait.' in `merged.md` -- In context, “Its” refers to the Retry-After header. |
| 17 | The gateway keeps no memory of which callers backed off. | 11 | carried | 'The gateway keeps no memory of who backed off politely' in `merged.md` -- The text says the gateway does not remember callers who backed off. |
| 18 | Waiting longer than the Retry-After header asks earns a caller no credit. | 11 | carried | 'waiting longer than the header asks earns a caller no credit at all' in `merged.md` -- The text states that waiting beyond the header’s duration earns no credit. |
| 19 | The body of the refusal is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- The text states the body’s format. |
| 20 | The body of the refusal names what the gateway calls the “window” it counted in. | 13 | carried | 'it names what the gateway calls the “window” it counted in' in `merged.md` -- In context, “it” refers to the JSON body of the refusal. |
| 21 | The body of the refusal names the cap. | 13 | carried | 'It names the cap and the tier as well.' in `merged.md` -- In context, “It” refers to the body, which names the cap. |
| 22 | The body of the refusal names the tier. | 13 | carried | 'It names the cap and the tier as well.' in `merged.md` -- In context, “It” refers to the body, which names the tier. |
| 23 | The fields in the body of the refusal are not substitutes for the Retry-After header. | 13 | carried | 'These appear as plain fields. None of those fields is a substitute for the header' in `merged.md` -- The text says the body’s fields do not substitute for the header. |
| 24 | The gateway has already calculated the wait in the Retry-After header. | 19 | carried | 'Honour the header, every time. The gateway has already done that arithmetic' in `merged.md` -- The text says the gateway has already calculated the wait conveyed by the header. |
| 25 | The gateway calculates the wait using information the caller does not have. | 19 | carried | 'The gateway has already done that arithmetic, with information the caller does not have' in `merged.md` -- The text says the gateway performs the calculation using information unavailable to the caller. |
| 26 | The gateway performs the same wait calculation on the 503 path. | 19 | carried | 'The gateway has already done that arithmetic, with information the caller does not have, and it does the same on the 503 path.' in `merged.md` -- The text says the gateway performs the same arithmetic on the 503 path. |
| 27 | A caller cannot see the counter used to calculate the wait. | 19 | carried | 'A wait derived on the client side is a guess about a counter it cannot see.' in `merged.md` -- The caller cannot see the counter used to determine the wait. |
| 28 | A 200 requires no retry. | 21 | carried | 'A 200 wants nothing' in `merged.md` -- A 200 calls for no retry action. |
| 29 | A 429 calls for the stated wait. | 21 | carried | 'a 429 wants the stated wait' in `merged.md` -- The text explicitly assigns the stated wait to a 429. |
| 30 | A 500 may be retried once the stated wait has passed. | 21 | carried | 'a 500 may be retried once that wait has passed' in `merged.md` -- The text permits retrying a 500 after the wait. |
| 31 | A 503 is the overload path. | 21 | carried | 'a 503 is the overload path' in `merged.md` -- The text identifies 503 as the overload path. |
| 33 | A batch credential is measured over exactly the same window as the default allowance. | 23 | carried | 'A batch credential is allowed 1000 requests in the same window as the default credential.' in `merged.md` -- The text explicitly says both credentials use the same window. |
| 34 | The tier is set on the credential when the credential is issued. | 23 | carried | 'The tier is set on the credential when it is issued' in `merged.md` -- The tier is set at credential issuance. |
| 35 | The tier cannot be asked for per call. | 23 | carried | 'cannot be asked for per call' in `merged.md` -- The text rules out requesting the tier per call. |
| 36 | Nothing else about the two tiers differs. | 23 | carried | 'Nothing else about the two tiers differs in any way.' in `merged.md` -- The text explicitly states that nothing else differs. |
| 38 | A credential may be suspended. | 29 | carried | 'A credential may be suspended' in `merged.md` -- The text explicitly allows for a suspended credential. |
| 39 | A route may be closed for maintenance. | 29 | carried | 'a route may be closed for maintenance' in `merged.md` -- The text explicitly allows for a maintenance closure. |
| 40 | A body may exceed the 5 megabyte limit. | 29 | carried | 'a body may exceed the 5 megabyte limit' in `merged.md` -- The text states the body-size limit and that a body may exceed it. |
| 41 | A refusal caused by a suspended credential does not clear itself by waiting for a stated number of seconds. | 29 | carried | 'A credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit. A maintenance closure can occur while a route is being repaired, and an oversized body is refused before it has been read at all. Some of these refusals have nothing to do with traffic sent in the current window. None of those three clears itself by waiting for a stated number of seconds.' in `merged.md` -- A suspended credential is one of the three refusals that waiting does not clear. |
| 42 | A refusal caused by a route closed for maintenance does not clear itself by waiting for a stated number of seconds. | 29 | carried | 'A credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit. A maintenance closure can occur while a route is being repaired, and an oversized body is refused before it has been read at all. Some of these refusals have nothing to do with traffic sent in the current window. None of those three clears itself by waiting for a stated number of seconds.' in `merged.md` -- A maintenance closure is one of the three refusals that waiting does not clear. |
| 43 | A refusal caused by a body exceeding the 5 megabyte limit does not clear itself by waiting for a stated number of seconds. | 29 | carried | 'A credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit. A maintenance closure can occur while a route is being repaired, and an oversized body is refused before it has been read at all. Some of these refusals have nothing to do with traffic sent in the current window. None of those three clears itself by waiting for a stated number of seconds.' in `merged.md` -- An oversized body is one of the three refusals that waiting does not clear. |
| 44 | A loop that waits and retries against a suspended credential spends its whole budget without reaching the service. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `merged.md` -- The text states both the exhausted budget and failure to reach the service. |
| 45 | After a loop waits and retries against a suspended credential, the log shows only a long run of refusals. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service — and the log afterwards shows nothing at all except a long run of refusals.' in `merged.md` -- The text describes that loop and the resulting log of refusals. |
| 46 | A cap can be raised. | 35 | carried | 'A cap can be raised' in `merged.md` -- The text explicitly says a cap can be raised. |
| 47 | The number of caps raised without a measurement behind them is 0. | 35 | carried | 'the number of caps raised without a measurement behind them is 0' in `merged.md` -- The text gives zero as the number raised without measurement. |
| 48 | The platform team looks at whether the load is smooth or bursty. | 35 | carried | 'The platform team looks at whether the load is smooth or bursty' in `merged.md` -- The text explicitly states what the team assesses about the load. |
| 49 | A burst is cheaper to smooth than to serve at its peak. | 35 | carried | 'a burst is cheaper to smooth than it is to serve at its peak' in `merged.md` -- The text makes the same cost comparison. |
| 50 | A caller that can move half its work to a quieter hour usually gets what it needs without a change to the cap. | 35 | carried | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `merged.md` -- The text states that moving half the work usually avoids a cap change. |
| 51 | Requests for an increase reach the platform team through the usual channel. | 37 | carried | 'Requests reach the platform team through the usual channel' in `merged.md` -- The text identifies the usual channel as the route to the platform team. |
| 52 | Requests for an increase are answered within two working days. | 37 | carried | 'they are answered within two working days' in `merged.md` -- The text gives a response time of two working days. |
| 53 | There is no expedited path for requests for an increase. | 37 | carried | 'There is no expedited path and no exception list.' in `merged.md` -- The text explicitly rules out an expedited path. |
| 54 | There is no exception list for requests for an increase. | 37 | carried | 'There is no expedited path and no exception list.' in `merged.md` -- The text explicitly rules out an exception list. |

### `source_b.md` -- 57 claim(s): 0 dropped, 4 contradicted, 0 carried in part, 53 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 28 | The batch allowance is 50 times the default. | 23 | contradicted | 'The default allowance is 100 requests in a window, and a credential marked for batch work is allowed 1000 in the same window.' in `merged.md` -- The stated allowances make batch 10 times the default, not 50 times. |
| 38 | The gateway refuses a request for three separate reasons. | 29 | contradicted | 'The gateway can refuse requests for reasons other than a spent cap. A credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit.' in `merged.md` -- The text lists three reasons in addition to a spent cap, rather than three reasons total. |
| 39 | Only one of the gateway’s three reasons for refusing a request is a cap. | 29 | contradicted | 'The gateway can refuse requests for reasons other than a spent cap. A credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit.' in `merged.md` -- A spent cap plus the three listed alternatives makes four reasons, not three. |
| 40 | Two of the gateway’s three reasons for refusing a request have nothing to do with how much traffic a caller has sent in its current window. | 29 | contradicted | 'The gateway can refuse requests for reasons other than a spent cap. A credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit.' in `merged.md` -- The claim's premise of three total reasons conflicts with the cap plus three listed alternatives. |
| 1 | Every credential has a cap of its own. | 3 | carried | 'Every credential has a cap.' in `merged.md` -- The text assigns a cap to every credential. |
| 2 | When a credential’s cap is spent, the gateway answers 429 at the edge. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge' in `merged.md` -- The gateway returns 429 at the edge when the cap is spent. |
| 3 | When a credential’s cap is spent, the gateway does not send the request to the service behind it. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge — without waking the service behind it' in `merged.md` -- The refusal occurs at the edge without reaching the service behind it. |
| 4 | Requests are counted against the credential rather than the connection. | 5 | carried | 'Requests are counted against the credential that presented them, over a fixed window of 60 seconds, and never against a connection.' in `merged.md` -- The text contrasts counting by credential with counting by connection. |
| 5 | Requests are counted over a fixed window of 60 seconds. | 5 | carried | 'over a fixed window of 60 seconds' in `merged.md` -- The counting window is explicitly fixed at 60 seconds. |
| 6 | The gateway does not disclose the start of the fixed window. | 5 | carried | 'The gateway does not disclose when the window starts.' in `merged.md` -- The start of the window is explicitly undisclosed. |
| 7 | The request count follows the credential across hosts. | 5 | carried | 'The count follows the credential across hosts.' in `merged.md` -- The text states that the count follows the credential across hosts. |
| 8 | A caller spread over many worker processes is throttled at the same point as a single process. | 5 | carried | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `merged.md` -- Eight worker processes are throttled at the same point as one. |
| 9 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- The stated default allowance is 100 requests per window. |
| 10 | A caller that needs more than the default allowance is almost always doing batch work under an interactive credential. | 7 | carried | 'callers needing more are almost always doing batch work under an interactive credential.' in `merged.md` -- The text describes callers needing more than the default allowance in those terms. |
| 11 | The header is called Retry-After. | 11 | carried | 'The refusal carries a Retry-After header.' in `merged.md` -- The text names the header Retry-After. |
| 12 | The Retry-After header’s value is a whole number of seconds. | 11 | carried | 'Its value is a whole number of seconds to wait.' in `merged.md` -- The stated header value is a whole number of seconds. |
| 13 | The Retry-After header is present on every refusal the gateway sends. | 11 | carried | 'The refusal carries a Retry-After header. It is present on every refusal the gateway sends.' in `merged.md` -- The text says the header appears on every gateway refusal. |
| 14 | The response body is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- The refusal body is explicitly described as JSON. |
| 15 | The response body repeats the cap as a plain field. | 13 | carried | 'It names the cap and the tier as well. These appear as plain fields.' in `merged.md` -- The body names the cap as a plain field. |
| 16 | The response body repeats the window as a plain field. | 13 | carried | 'The body of the refusal is JSON, and it names what the gateway calls the “window” it counted in. It names the cap and the tier as well. These appear as plain fields.' in `merged.md` -- The body names the window among its plain fields. |
| 17 | The response body repeats the tier as a plain field. | 13 | carried | 'It names the cap and the tier as well. These appear as plain fields.' in `merged.md` -- The body names the tier as a plain field. |
| 18 | The cap, window and tier fields are not substitutes for the Retry-After header. | 13 | carried | 'It names the cap and the tier as well. These appear as plain fields. None of those fields is a substitute for the header' in `merged.md` -- The text says the body fields do not replace the header. |
| 19 | The gateway computes the wait stated in the Retry-After header. | 19 | carried | 'Honour the header, every time. The gateway has already done that arithmetic' in `merged.md` -- The text attributes the header's wait calculation to the gateway. |
| 20 | The gateway computes the wait using information the caller cannot see. | 19 | carried | 'The gateway has already done that arithmetic, with information the caller does not have' in `merged.md` -- The gateway's calculation uses information unavailable to the caller. |
| 21 | The rule to honour the Retry-After header also applies on the 503 path. | 19 | carried | 'Honour the header, every time. The gateway has already done that arithmetic, with information the caller does not have, and it does the same on the 503 path.' in `merged.md` -- The instruction to honour the header explicitly includes the 503 path. |
| 22 | The cause of a 503 refusal differs from the cause of a cap refusal. | 19 | carried | 'a 429 wants the stated wait, a 500 may be retried once that wait has passed, and a 503 is the overload path' in `merged.md` -- The text identifies 503 as the overload path, distinct from a cap-related 429. |
| 23 | A 200 response needs no retry. | 21 | carried | 'A 200 wants nothing' in `merged.md` -- A 200 calls for no retry action. |
| 24 | A 429 response requires the stated wait. | 21 | carried | 'a 429 wants the stated wait' in `merged.md` -- The text instructs callers to wait as stated for a 429. |
| 25 | A 500 response can be retried once the stated wait has passed. | 21 | carried | 'a 500 may be retried once that wait has passed' in `merged.md` -- The text permits retrying a 500 after the stated wait. |
| 26 | A 503 response means the platform itself is overloaded. | 21 | carried | 'a 503 is the overload path' in `merged.md` -- The text identifies a 503 as the overload response. |
| 27 | A batch credential is allowed 1000 requests in a window. | 23 | carried | 'A batch credential is allowed 1000 requests in the same window as the default credential.' in `merged.md` -- The batch allowance is explicitly 1000 requests per window. |
| 29 | The batch tier does not use a separate counting scheme. | 23 | carried | 'A batch credential is allowed 1000 requests in the same window as the default credential. The tier is set on the credential when it is issued and cannot be asked for per call. The window, the header and the body are identical to the interactive case, so a client written for one tier needs no change at all to run against the other. Nothing else about the two tiers differs in any way.' in `merged.md` -- The tiers share the window and otherwise differ only in the stated allowance. |
| 30 | The batch tier’s window is identical to the interactive tier’s window. | 23 | carried | 'The window, the header and the body are identical to the interactive case' in `merged.md` -- The batch window is explicitly identical to the interactive window. |
| 31 | The batch tier’s header is identical to the interactive tier’s header. | 23 | carried | 'The window, the header and the body are identical to the interactive case' in `merged.md` -- The batch header is explicitly identical to the interactive header. |
| 32 | The batch tier’s body is identical to the interactive tier’s body. | 23 | carried | 'The window, the header and the body are identical to the interactive case' in `merged.md` -- The batch body is explicitly identical to the interactive body. |
| 33 | A client written for one tier needs no change to run against the other tier. | 23 | carried | 'a client written for one tier needs no change at all to run against the other' in `merged.md` -- The text states that clients need no changes between tiers. |
| 34 | Nothing else about the batch tier differs from the default. | 23 | carried | 'Nothing else about the two tiers differs in any way.' in `merged.md` -- The text explicitly rules out other differences between the tiers. |
| 35 | The client is instructed to log every refusal. | 25 | carried | 'Log every refusal seen.' in `merged.md` -- The instruction covers every refusal. |
| 36 | The client is instructed to keep refusal logs for at least a week. | 25 | carried | 'Keep the log for at least a week.' in `merged.md` -- The specified minimum retention is one week. |
| 37 | The platform team will not assemble a caller’s case for a larger cap on the caller’s behalf. | 25 | carried | 'nobody at the far end will assemble that argument on its behalf' in `merged.md` -- The caller must assemble its own argument for a larger cap. |
| 41 | A credential can be suspended. | 29 | carried | 'A credential may be suspended' in `merged.md` -- The text explicitly allows for suspension of a credential. |
| 42 | A route can be closed while it is being repaired. | 29 | carried | 'A maintenance closure can occur while a route is being repaired' in `merged.md` -- The text says a route can be closed during repair. |
| 43 | A request body over the 5 megabyte limit is refused before it has been read at all. | 29 | carried | 'a body may exceed the 5 megabyte limit. A maintenance closure can occur while a route is being repaired, and an oversized body is refused before it has been read at all.' in `merged.md` -- The text gives the size limit and says an oversized body is refused before being read. |
| 44 | A loop retrying against a suspended credential burns its whole budget. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `merged.md` -- The text explicitly says such a loop spends its whole budget. |
| 45 | A loop retrying against a suspended credential reaches nothing. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `merged.md` -- The retries never reach the service. |
| 46 | The log after retries against a suspended credential shows a long run of refusals. | 31 | carried | 'the log afterwards shows nothing at all except a long run of refusals' in `merged.md` -- The text describes the resulting log as a long run of refusals. |
| 47 | The log after retries against a suspended credential shows no successes at all. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service — and the log afterwards shows nothing at all except a long run of refusals. The log shows no successes' in `merged.md` -- The text explicitly says that the log after those retries shows no successes. |
| 48 | A cap can be raised. | 33 | carried | 'A cap can be raised' in `merged.md` -- The text states that a cap can be raised. |
| 49 | A cap cannot be raised solely on an assertion that the current cap is too small. | 33 | carried | 'A cap can be raised, and the number of caps raised without a measurement behind them is 0.' in `merged.md` -- An assertion alone provides no measurement, and the text says no caps are raised without one. |
| 50 | A request for a larger cap requires refusal counts for a full week. | 33 | carried | 'Bring a week of refusal counts' in `merged.md` -- The text asks applicants to bring refusal counts covering a week. |
| 51 | A request for a larger cap requires the shape of the traffic across the day. | 33 | carried | 'Bring a week of refusal counts, the shape of the traffic across the day, and the deadline that traffic is serving.' in `merged.md` -- The requested information includes the shape of traffic across the day. |
| 52 | A request for a larger cap requires the deadline the traffic exists to meet. | 33 | carried | 'Bring a week of refusal counts, the shape of the traffic across the day, and the deadline that traffic is serving.' in `merged.md` -- The requested information includes the deadline the traffic serves. |
| 53 | The platform team wants to know whether the load is smooth or bursty before it looks at the number. | 35 | carried | 'The platform team looks at whether the load is smooth or bursty — a burst is cheaper to smooth than it is to serve at its peak. The team assesses the traffic pattern before considering a higher cap.' in `merged.md` -- The team checks whether load is smooth or bursty before considering a higher cap. |
| 54 | Requests go to the platform team through the usual channel. | 35 | carried | 'Requests reach the platform team through the usual channel' in `merged.md` -- The text names the usual channel as the route for requests. |
| 55 | There is no expedited path. | 37 | carried | 'There is no expedited path' in `merged.md` -- The text explicitly rules out an expedited path. |
| 56 | An answer takes two working days. | 37 | carried | 'they are answered within two working days' in `merged.md` -- The text gives two working days as the response-time limit. |
| 57 | Chasing an answer does not reduce the time it takes. | 37 | carried | 'Chasing a request does not shorten that response time.' in `merged.md` -- The text says chasing a request does not shorten the response time. |

### `merged.md` -- 65 claim(s): 0 invented, 0 contradicted, 0 supported in part, 65 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Every credential has a cap. | supported | `source_a.md` | 'Every credential has a cap.' in `source_a.md` -- The source states the claim directly. |
| 2 | When a credential’s cap is spent, the gateway answers 429 at the edge. | supported | `source_a.md` | 'When that cap is spent the gateway answers 429 at the edge' in `source_a.md` -- The source identifies the response and where it occurs. |
| 3 | When a credential’s cap is spent, the gateway answers 429 without waking the service behind it. | supported | `source_a.md` | 'When that cap is spent the gateway answers 429 at the edge — without waking the service behind it' in `source_a.md` -- The source states that a spent cap produces a 429 without waking the service. |
| 4 | An earlier draft proposed a client-side token bucket that mirrored the gateway’s counters. | supported | `source_b.md` | 'An earlier draft of this note argued for a client-side token bucket that mirrored the gateway’s own counters' in `source_b.md` -- The source describes the earlier draft’s proposal. |
| 5 | The proposed client-side token bucket was left out. | supported | `source_b.md` | 'An earlier draft of this note argued for a client-side token bucket that mirrored the gateway’s own counters, and that section has been left out on purpose' in `source_b.md` -- The source says the section proposing the token bucket was left out. |
| 6 | Requests are counted against the credential that presented them. | supported | `source_a.md` | 'Requests are counted against the credential that presented them' in `source_a.md` -- The source states how requests are attributed. |
| 7 | Requests are counted over a fixed window of 60 seconds. | supported | `source_a.md` | 'over a fixed window of 60 seconds' in `source_a.md` -- The source gives the counting window and its length. |
| 8 | Requests are never counted against a connection. | supported | `source_a.md` | 'and never against a connection' in `source_a.md` -- The source explicitly rules out counting against a connection. |
| 9 | The gateway does not disclose when the window starts. | supported | `source_b.md` | 'over a fixed window of 60 seconds whose start the gateway doesn’t disclose' in `source_b.md` -- The source says the gateway does not disclose the window’s start. |
| 10 | Opening a second socket does not increase a caller’s allowance. | supported | `source_a.md` | 'Opening a second socket therefore buys a caller nothing.' in `source_a.md` -- The source says another socket provides no allowance benefit. |
| 11 | The request count follows the credential across hosts. | supported | `source_b.md` | 'The count follows the credential wherever the caller happens to put it, including across hosts.' in `source_b.md` -- The source explicitly includes counting across hosts. |
| 12 | A client spread across eight worker processes is throttled at exactly the point one process would have been. | supported | `source_a.md` | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `source_a.md` -- The source states the same comparison for eight worker processes. |
| 13 | A client spread across eight worker processes uses extra file descriptors. | supported | `source_a.md` | 'A client spread across eight worker processes is throttled at exactly the point one process would have been — and pays for the extra file descriptors as well.' in `source_a.md` -- The source says the eight-process client pays for extra file descriptors. |
| 14 | The default allowance is 100 requests in a window. | supported | `source_a.md` | 'The default allowance is 100 requests in a window' in `source_a.md` -- The source states the default allowance. |
| 15 | A credential marked for batch work is allowed 1000 requests in the same window. | supported | `source_a.md` | 'a credential marked for batch work is allowed 1000 in the same window' in `source_a.md` -- The source gives the batch allowance in the same request-counting window. |
| 16 | Callers needing more than the default allowance are almost always doing batch work under an interactive credential. | supported | `source_b.md` | 'a caller that needs more than that is almost always doing batch work under an interactive credential' in `source_b.md` -- The source states this characterization of callers needing more than the default. |
| 17 | A refusal is not an outage. | supported | `source_a.md` | 'A refusal is not an outage' in `source_a.md` -- The source states the claim directly. |
| 18 | Callers that retry at once are the largest single reason the cap exists. | supported | `source_a.md` | 'Callers that retry at once are the largest single reason the cap is there at all.' in `source_a.md` -- The source gives immediate retries as the largest single reason for the cap. |
| 19 | A refusal carries a Retry-After header. | supported | `source_a.md` | 'The refusal carries a Retry-After header.' in `source_a.md` -- The source states the header’s presence. |
| 20 | The Retry-After header is present on every refusal the gateway sends. | supported | `source_b.md` | 'it is present on every refusal the gateway sends' in `source_b.md` -- The source says the Retry-After header is present on every gateway refusal. |
| 21 | The Retry-After header’s value is a whole number of seconds to wait. | supported | `source_a.md` | 'Its value is a whole number of seconds to wait.' in `source_a.md` -- The source specifies the header value and its unit. |
| 22 | The gateway keeps no memory of who backed off politely. | supported | `source_a.md` | 'The gateway keeps no memory of who backed off politely' in `source_a.md` -- The source states the claim directly. |
| 23 | Waiting longer than the Retry-After header asks earns a caller no credit at all. | supported | `source_a.md` | 'waiting longer than the header asks earns a caller no credit at all' in `source_a.md` -- The source states that waiting longer earns no credit. |
| 24 | The body of the refusal is JSON. | supported | `source_a.md` | 'The body of the refusal is JSON' in `source_a.md` -- The source states the refusal body’s format. |
| 25 | The body of the refusal names what the gateway calls the “window” it counted in. | supported | `source_a.md` | 'The body of the refusal is JSON, and it names what the gateway calls the “window” it counted in.' in `source_a.md` -- The source says the refusal body names the counted window. |
| 26 | The body of the refusal names the cap. | supported | `source_a.md` | 'It names the cap and the tier as well.' in `source_a.md` -- The refusal body names the cap. |
| 27 | The body of the refusal names the tier. | supported | `source_a.md` | 'It names the cap and the tier as well.' in `source_a.md` -- The refusal body names the tier. |
| 28 | The window, cap and tier appear as plain fields in the refusal body. | supported | `source_b.md` | 'The response body is JSON and it repeats the cap, the window and the tier as plain fields.' in `source_b.md` -- The source explicitly identifies all three as plain fields. |
| 29 | A client-computed wait can disagree with the gateway. | supported | `source_b.md` | 'a caller that parses the body in order to compute its own wait has written code whose only possible future is to disagree with the gateway it is talking to.' in `source_b.md` -- The source says a client-computed wait can disagree with the gateway. |
| 30 | The gateway computes the wait using information the caller does not have. | supported | `source_b.md` | 'The gateway has already done that arithmetic and it did it with information the caller cannot see.' in `source_b.md` -- The source states both who does the arithmetic and why the caller cannot reproduce it. |
| 31 | The gateway performs the same wait arithmetic on the 503 path. | supported | `source_a.md` | 'The gateway has already done that arithmetic, with information the caller does not have, and it does the same on the 503 path.' in `source_a.md` -- The same gateway arithmetic applies on the 503 path. |
| 32 | A 200 requires no retry. | supported | `source_a.md` | 'A 200 wants nothing' in `source_a.md` -- A 200 calls for no retry action. |
| 33 | A 429 requires the stated wait. | supported | `source_a.md` | 'a 429 wants the stated wait' in `source_a.md` -- The source gives the stated wait as the response to a 429. |
| 34 | A 500 may be retried once the stated wait has passed. | supported | `source_a.md` | 'a 500 may be retried once that wait has passed' in `source_a.md` -- The claim matches the source's condition for retrying a 500. |
| 35 | A 503 is the overload path. | supported | `source_a.md` | 'a 503 is the overload path.' in `source_a.md` -- The source directly identifies the 503 path as overload. |
| 36 | A batch credential is allowed 1000 requests in the same window as the default credential. | supported | `source_a.md` | 'The default allowance is 100 requests in a window, and a credential marked for batch work is allowed 1000 in the same window.' in `source_a.md` -- The source gives the batch allowance and says it uses the same window. |
| 37 | The tier is set on the credential when it is issued. | supported | `source_a.md` | 'The tier is set on the credential when it is issued' in `source_a.md` -- The source states when the credential's tier is set. |
| 38 | The tier cannot be asked for per call. | supported | `source_a.md` | 'cannot be asked for per call.' in `source_a.md` -- The source says the tier cannot be requested per call. |
| 39 | The window is identical for batch and interactive credentials. | supported | `source_b.md` | 'The window, the header and the body are identical to the interactive case' in `source_b.md` -- The batch-tier passage says its window is identical to the interactive case. |
| 40 | The header is identical for batch and interactive credentials. | supported | `source_b.md` | 'The window, the header and the body are identical to the interactive case' in `source_b.md` -- The batch-tier passage says its header is identical to the interactive case. |
| 41 | The body is identical for batch and interactive credentials. | supported | `source_b.md` | 'The window, the header and the body are identical to the interactive case' in `source_b.md` -- The batch-tier passage says its body is identical to the interactive case. |
| 42 | A client written for one tier needs no change to run against the other. | supported | `source_b.md` | 'a client written for one tier needs no change at all to run against the other.' in `source_b.md` -- The source states the claim directly. |
| 43 | Nothing else about the batch and interactive tiers differs. | supported | `source_a.md` | 'Nothing else about the two tiers differs in any way.' in `source_a.md` -- The source says there are no other differences between the tiers. |
| 44 | The gateway can refuse requests for reasons other than a spent cap. | supported | `source_a.md` | 'Not all are caps.' in `source_a.md` -- The source says some gateway refusals are not cap refusals. |
| 45 | A credential may be suspended. | supported | `source_a.md` | 'A credential may be suspended' in `source_a.md` -- The source directly identifies suspension as a possibility. |
| 46 | A route may be closed for maintenance. | supported | `source_a.md` | 'a route may be closed for maintenance' in `source_a.md` -- The source directly identifies maintenance closure as a possibility. |
| 47 | A body may exceed the 5 megabyte limit. | supported | `source_a.md` | 'a body may exceed the 5 megabyte limit.' in `source_a.md` -- The source states the body-size limit and the possibility of exceeding it. |
| 48 | A maintenance closure can occur while a route is being repaired. | supported | `source_a.md` | 'a route may be closed for maintenance' in `source_a.md` -- Source_b.md adds that a route can be closed while it is being repaired; together, the passages support a maintenance closure during repair. |
| 49 | An oversized body is refused before it has been read at all. | supported | `source_b.md` | 'a request body over the 5 megabyte limit is refused before it has been read at all.' in `source_b.md` -- The source directly states when an oversized body is refused. |
| 50 | Some refusals for suspended credentials, maintenance closures or oversized bodies have nothing to do with traffic sent in the current window. | supported | `source_b.md` | 'Two of the three have nothing to do with how much traffic a caller has sent in the window it is currently in. A credential can be suspended, a route can be closed while it is being repaired, and a request body over the 5 megabyte limit is refused before it has been read at all.' in `source_b.md` -- The passage says some non-cap refusals are unrelated to traffic in the current window and lists the relevant kinds. |
| 51 | Refusals for suspended credentials, maintenance closures and oversized bodies do not clear themselves by waiting for a stated number of seconds. | supported | `source_a.md` | 'A credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit. None of those three clears itself by waiting for a stated number of seconds.' in `source_a.md` -- The source names all three refusals and says waiting does not clear them. |
| 52 | A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service. | supported | `source_a.md` | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `source_a.md` -- The source states the claim directly. |
| 53 | The log from a loop that waits and retries against a suspended credential shows a long run of refusals. | supported | `source_a.md` | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service — and the log afterwards shows nothing at all except a long run of refusals.' in `source_a.md` -- The source describes the resulting log as a long run of refusals. |
| 54 | The log from a loop that waits and retries against a suspended credential shows no successes. | supported | `source_b.md` | 'A loop retrying against a suspended credential burns its whole budget and reaches nothing. The log afterwards shows a long run of refusals and no successes at all' in `source_b.md` -- The source says the log from that loop shows no successes. |
| 55 | A cap can be raised. | supported | `source_a.md` | 'A cap can be raised' in `source_a.md` -- The source states the claim directly. |
| 56 | The number of caps raised without a measurement behind them is 0. | supported | `source_a.md` | 'the number of caps raised without a measurement behind them is 0' in `source_a.md` -- The source states the number directly. |
| 57 | The platform team looks at whether the load is smooth or bursty. | supported | `source_a.md` | 'The platform team looks at whether the load is smooth or bursty' in `source_a.md` -- The source states the claim directly. |
| 58 | The platform team assesses the traffic pattern before considering a higher cap. | supported | `source_b.md` | 'The team wants to know whether the load is smooth or bursty before it looks at the number at all.' in `source_b.md` -- In the discussion of raising caps, the source says the team considers the traffic pattern before the cap number. |
| 59 | A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap. | supported | `source_a.md` | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `source_a.md` -- The source states the claim directly. |
| 60 | Moving work to a quieter hour is available to almost everybody. | supported | `source_b.md` | 'That is the cheapest fix available to anybody, and it is available to almost everybody.' in `source_b.md` -- “That” refers to moving work to a quieter hour in the preceding sentence. |
| 61 | Requests reach the platform team through the usual channel. | supported | `source_a.md` | 'Requests reach the platform team through the usual channel' in `source_a.md` -- The source states the claim directly. |
| 62 | Requests to the platform team are answered within two working days. | supported | `source_a.md` | 'Requests reach the platform team through the usual channel, and they are answered within two working days.' in `source_a.md` -- The source gives the response time for those requests. |
| 63 | Chasing a request does not shorten the response time. | supported | `source_b.md` | 'An answer takes two working days, and chasing it doesn’t make it take fewer.' in `source_b.md` -- The source says chasing does not reduce the time to an answer. |
| 64 | There is no expedited path. | supported | `source_b.md` | 'There is no expedited path.' in `source_b.md` -- The source states the claim directly. |
| 65 | There is no exception list. | supported | `source_a.md` | 'There is no expedited path and no exception list.' in `source_a.md` -- The source explicitly says there is no exception list. |

## Structure

**9** mechanical check(s) over **104** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **65** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **111**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 17 run(s) over 57 attributed segment(s) — sources interleaved. 6 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Absent and undeclared — in a source, not in the merge, and no record explains it

- `b7` (`source_b.md`) — 'The count follows the credential wherever the caller happens to put it, including across hosts.' is not in the merge and no disposition record explains it (nearest merge segment m8 at 0.65)

  ```text
  In the source: The count follows the credential wherever the caller happens to put it, including across hosts.
  ```

### Verbatim violation — an invariant-core token did not survive unchanged

- `b31` (`source_b.md`) — numeric '50' (times) does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **54** departure(s) from its sources. Checking them confirms 32, rejects 10, and leaves 12 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 104 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | Title: the base title was chosen. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Rate limiting and the 429 contract for gateway clients' and says so (no claim traced to it) |
| `b2` | duplicate | Credential cap: the base states the same fact. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-001`) |
| `b3` | duplicate | Edge refusal: the base carries the same fact. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-002`, `B-003`) |
| `b4` | reworded | Client-side counters: retain the draft history and its rationale. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b5` | subsumed | Counting window: add the undisclosed start to the base rule. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-004`, `B-005`, `B-006`) |
| `b6` | duplicate | Sockets: the base states the same consequence. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b8` | duplicate | Workers: the base gives the same rule with a concrete count. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-008`) |
| `b9` | subsumed | Default tier: retain the allowance and observed usage. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-009`, `B-010`) |
| `b10` | subsumed | Refusal meaning: retain the gateway-bug distinction. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a8` | reworded | Refusal meaning: add the compatible gateway-bug detail. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-012`) |
| `b11` | duplicate | Immediate retries: the base states the same cause. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'duplicate' is what happened to it (no claim traced to it) |
| `b12` | duplicate | Reading section: the heading is identical. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b13` | duplicate | Header name: the base already names it. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-011`) |
| `b14` | subsumed | Header contract: retain its presence and whole-number value. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-012`, `B-013`) |
| `b15` | subsumed | Waiting contract: retain the note's intended outcome. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b16` | duplicate | Extra waiting: the base states the same consequence. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b17` | subsumed | Response body: retain the plain-field detail. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-014`, `B-015`, `B-016`, `B-017`) |
| `b18` | subsumed | Retry timing: retain the risk of disagreeing with the gateway. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-018`) |
| `b19` | duplicate | Body purpose: the base states the same use. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b20` | superseded | Retry heading: preserve the base section structure. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b21` | duplicate | Rule order: the base states the same instruction. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b22` | subsumed | First rule: the base also prohibits a client-computed wait. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b23` | duplicate | Header arithmetic: the base states the same rationale. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-019`, `B-020`) |
| `b24` | duplicate | 503 timing: the base applies the same rule. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-021`, `B-022`) |
| `b25` | duplicate | Client wait: the base calls it a guess. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b26` | duplicate | Client guess: the base rejects it. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b27` | subsumed | Second rule: retain the narrower retryable set. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b28` | duplicate | Status handling: the base carries all four cases. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-023`, `B-024`, `B-025`, `B-026`) |
| `b29` | duplicate | Shared retry branch: the base states the same risk. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'duplicate' is what happened to it (no claim traced to it) |
| `b30` | duplicate | Retry-loop warning: the base gives the same instruction. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `a32` | superseded | Batch allowance: choose stated counts over the conflicting ratio. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`A-032`, `A-033`) |
| `b31` | superseded | Batch allowance: keep 1000 and reject the conflicting 50 times. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-027`, `B-028`, `B-029`) |
| `b32` | duplicate | Tier compatibility: the sentence is carried unchanged. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-030`, `B-031`, `B-032`, `B-033`) |
| `b33` | duplicate | Tier differences: the base states the same limit. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-034`) |
| `b34` | subsumed | Refusal logs: retain the minimum retention period. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-035`, `B-036`) |
| `b35` | duplicate | Increase evidence: the base states the same requirement. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-037`) |
| `b36` | reworded | Increase evidence: retain the need for counts without excluding other evidence. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b37` | superseded | Other-refusals heading: preserve the base section structure. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a40` | superseded | Refusal reasons: retain the distinction, not the inconsistent count. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`A-037`) |
| `b38` | superseded | Refusal reasons: retain the distinction, not the inconsistent count. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-038`, `B-039`) |
| `b39` | reworded | Other refusals: preserve independence from window traffic. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-040 came back CONTRADICTED (`B-040`) |
| `b40` | subsumed | Other refusals: retain repair and pre-read details alongside the list. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-041`, `B-042`, `B-043`) |
| `b41` | duplicate | Retry distinction: the base states its importance. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b42` | duplicate | Suspended credential: the base carries the wasted-budget outcome. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-044`, `B-045`) |
| `b43` | subsumed | Suspended credential: retain the misleading log and caller cost. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-046`, `B-047`) |
| `b44` | duplicate | Quieter hour: the base states the same alternative. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'duplicate' is what happened to it (no claim traced to it) |
| `b45` | reworded | Traffic smoothing: retain its cost and availability. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b46` | duplicate | Cap increase: the base requires measured evidence. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-048`, `B-049`) |
| `b47` | duplicate | Increase request: the base lists the same evidence. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-050`, `B-051`, `B-052`) |
| `b48` | subsumed | Increase review: retain the order of assessment. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-053`) |
| `b49` | duplicate | Bursts: the base states the same cost comparison. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b50` | duplicate | Request channel: the base names the same destination. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-054`) |
| `b51` | duplicate | Expedited path: the base states the same restriction. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-055`) |
| `b52` | subsumed | Response time: retain that chasing does not accelerate it. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-056`, `B-057`) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | bf7d5842201d (hosted) |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | gpt-6-sol |
| Model (decompose) | gpt-6-sol |
| Model (verify) | gpt-6-sol |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed 0, thinking decompose, merge, verify, profile openai-reasoning |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 12 live, 0 cached, 0 replayed |
| Tokens | 41,998 in, 31,046 out, 10,748 cached, 4,310 reasoning |
| Cost | ~$0.38 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 301.0s |
| Generated | 2026-09-27T16:27:09+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `bf7d5842201d`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
