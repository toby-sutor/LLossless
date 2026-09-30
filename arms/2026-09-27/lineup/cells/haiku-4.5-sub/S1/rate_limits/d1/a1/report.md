## Verdict

**23 finding(s).** In the claims: 14 dropped, 1 partially dropped. In the structure: 2 undeclared absence, 3 undeclared rewording, 2 false departure, 1 verbatim violation.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 54 |
| Claims extracted from `source_a.md` | 50 |
| Claims extracted from `source_b.md` | 51 |
| Forward — source claims accounted for in the merge | **86/101** |
| Forward — carried only in part | 1 |
| Forward — `source_a.md` claims accounted for | **45/50** |
| Forward — `source_b.md` claims accounted for | **41/51** (1 in part) |
| Reverse — merge claims found in a source | **54/54** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **139/141** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Dropped — in a source, not in the merge

- **A-003** (`source_a.md:3`) — A refusal costs the platform almost nothing.
  - judged against: `merged.md`
  - rationale: The reference text does not state that a refusal costs the platform almost nothing.
- **A-009** (`source_a.md:5`) — A client spread across eight worker processes pays for the extra file descriptors.
  - judged against: `merged.md`
  - rationale: The reference text does not mention whether spreading across processes requires paying for extra file descriptors.
- **A-028** (`source_a.md:23`) — A batch credential is measured over exactly the same window.
  - judged against: `merged.md`
  - rationale: The reference text does not state when or how the tier is set on credentials.
- **A-029** (`source_a.md:23`) — The tier is set on the credential when it is issued.
  - judged against: `merged.md`
  - rationale: The reference text does not indicate whether tier can be requested per call.
- **A-043** (`source_a.md:35`) — The number of caps raised without a measurement behind them is 0.
  - judged against: `merged.md`
  - rationale: The reference text does not provide historical data on how many caps have been raised without measurement.
- **B-004** (`source_b.md:5`) — The start of the fixed window is not disclosed by the gateway.
  - judged against: `merged.md`
  - rationale: The reference text does not state whether the window start time is disclosed.
- **B-005** (`source_b.md:5`) — The count follows the credential wherever the caller happens to put it, including across hosts.
  - judged against: `merged.md`
  - rationale: The reference text does not specify that counts follow credentials across hosts.
- **B-008** (`source_b.md:7`) — A caller that needs more than that is almost always doing batch work under an interactive credential.
  - judged against: `merged.md`
  - rationale: The reference text does not characterize what work exceeds the default allowance.
- **B-012** (`source_b.md:11`) — The Retry-After header is present on every refusal the gateway sends.
  - judged against: `merged.md`
  - rationale: The reference text does not state that Retry-After is present on every refusal.
- **B-021** (`source_b.md:19`) — The cause of the refusal on the 503 path is an entirely different one.
  - judged against: `merged.md`
  - rationale: The reference text does not explicitly compare the causes of refusal on the 503 path versus other paths.
- **B-036** (`source_b.md:29`) — Two of the three have nothing to do with how much traffic a caller has sent in the window it is currently in.
  - judged against: `merged.md`
  - rationale: The reference text does not explicitly state which of the three reasons have no relation to traffic in the current window.
- **B-039** (`source_b.md:29`) — A request body over the 5 megabyte limit is refused before it has been read at all.
  - judged against: `merged.md`
  - rationale: The reference text does not state that oversized bodies are refused before being read.
- **B-043** (`source_b.md:31`) — The wasted budget is the caller's own.
  - judged against: `merged.md`
  - rationale: The reference text does not state whose budget is wasted in this scenario.
- **B-047** (`source_b.md:35`) — The team wants to know whether the load is smooth or bursty before it looks at the number at all.
  - judged against: `merged.md`
  - rationale: The reference text does not specify the order in which the team evaluates load characteristics versus numbers.

### Partly dropped — the merge carries some of this claim

- **B-022** (`source_b.md:19`) — Anything computed on the client side is a guess.
  - evidence: 'A wait derived client-side is a guess about a counter it cannot see' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text states client-side wait computation is a guess, but does not generalize to all client-side computation.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 50 claim(s): 5 dropped, 0 contradicted, 0 carried in part, 45 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 3 | A refusal costs the platform almost nothing. | 3 | dropped | The reference text does not state that a refusal costs the platform almost nothing. |
| 9 | A client spread across eight worker processes pays for the extra file descriptors. | 5 | dropped | The reference text does not mention whether spreading across processes requires paying for extra file descriptors. |
| 28 | A batch credential is measured over exactly the same window. | 23 | dropped | The reference text does not state when or how the tier is set on credentials. |
| 29 | The tier is set on the credential when it is issued. | 23 | dropped | The reference text does not indicate whether tier can be requested per call. |
| 43 | The number of caps raised without a measurement behind them is 0. | 35 | dropped | The reference text does not provide historical data on how many caps have been raised without measurement. |
| 1 | Every credential has a cap. | 3 | carried | 'Every credential has a cap.' in `merged.md` -- The reference text directly states this claim in the opening sentence. |
| 2 | When a credential's cap is spent, the gateway answers 429 at the edge without waking the service behind it. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge without waking the service behind it.' in `merged.md` -- The reference text states this explicitly in the first paragraph. |
| 4 | Requests are counted against the credential that presented them. | 5 | carried | 'Requests are counted against the credential rather than the connection' in `merged.md` -- The reference text directly states requests are counted against the credential, not the connection. |
| 5 | Requests are counted over a fixed window of 60 seconds. | 5 | carried | 'over a fixed window of 60 seconds' in `merged.md` -- The reference text explicitly specifies a fixed window of 60 seconds. |
| 6 | Requests are never counted against a connection. | 5 | carried | 'Requests are counted against the credential rather than the connection' in `merged.md` -- The statement that requests are counted against the credential, not the connection, entails they are never counted against a connection. |
| 7 | Opening a second socket buys a caller nothing. | 5 | carried | 'Opening additional sockets provides no benefit' in `merged.md` -- The reference text states this principle, making opening a second socket equivalent to opening any additional socket. |
| 8 | A client spread across eight worker processes is throttled at exactly the point one process would have been. | 5 | carried | 'a client spread across worker processes is throttled at exactly the point a single process would be.' in `merged.md` -- The reference text states the general principle that applies to any number of worker processes, including eight. |
| 10 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- The reference text explicitly states the default allowance. |
| 11 | A credential marked for batch work is allowed 1000 in the same window. | 7 | carried | 'a credential marked for batch work is allowed 1000 in the same window' in `merged.md` -- The reference text directly states this allowance for batch credentials. |
| 12 | A refusal is not an outage. | 7 | carried | 'A 429 refusal is not an outage' in `merged.md` -- The reference text explicitly states a 429 refusal is not an outage. |
| 13 | Callers that retry at once are the largest single reason the cap is there at all. | 7 | carried | 'Callers that retry immediately are the primary reason the cap exists.' in `merged.md` -- The reference text states this as fact in the first paragraph. |
| 14 | The refusal carries a Retry-After header. | 11 | carried | 'The refusal carries a Retry-After header.' in `merged.md` -- The reference text directly states the refusal carries a Retry-After header. |
| 15 | The Retry-After header's value is a whole number of seconds to wait. | 11 | carried | 'Its value is a whole number of seconds.' in `merged.md` -- The reference text explicitly describes the header value as a whole number of seconds. |
| 16 | The gateway keeps no memory of who backed off politely. | 11 | carried | 'The gateway keeps no memory of who backed off politely' in `merged.md` -- The reference text directly states this fact. |
| 17 | Waiting longer than the Retry-After header asks earns a caller no credit at all. | 11 | carried | 'waiting longer than the header asks earns no credit.' in `merged.md` -- The reference text states this in the section on reading refusals. |
| 18 | The body of the refusal is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- The reference text explicitly states the refusal body is JSON. |
| 19 | The body of the refusal names what the gateway calls the window it counted in. | 13 (unverified) | carried | 'names the window, cap, and tier' in `merged.md` -- The reference text states the body names the window among other fields. |
| 20 | The body of the refusal names the cap and the tier. | 13 | carried | 'names the window, cap, and tier' in `merged.md` -- The reference text states the body names both the cap and the tier. |
| 21 | A caller that parses the body to compute its own wait is doing the same arithmetic twice. | 13 | carried | 'a caller that parses the body to compute its own wait is doing the same arithmetic twice.' in `merged.md` -- The reference text explicitly makes this statement. |
| 22 | A 200 response wants nothing. | 21 | carried | 'A 200 needs nothing' in `merged.md` -- The reference text uses identical language in the retry rules section. |
| 23 | A 429 response wants the stated wait. | 21 | carried | 'a 429 needs the stated wait' in `merged.md` -- The reference text explicitly states this in the retry rules. |
| 24 | A 500 response may be retried once that wait has passed. | 21 | carried | 'a 500 can be retried once that wait has passed' in `merged.md` -- The reference text includes this in the retry rules section. |
| 25 | A 503 response is the overload path. | 21 | carried | 'a 503 means the platform itself is overloaded.' in `merged.md` -- The reference text describes 503 as the overload path in the retry rules. |
| 26 | A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive. | 21 | carried | 'A client that folds all non-success responses into one branch will retry hardest during exactly the incident the cap was installed to survive.' in `merged.md` -- The reference text states this exact principle in the second retry rule. |
| 27 | A batch credential is allowed fifty times the default allowance. | 23 | carried | 'A batch credential is allowed 1000 requests in a window, which is 50 times the default' in `merged.md` -- The reference text explicitly states the 50x relationship. |
| 30 | The tier cannot be asked for per call. | 23 | carried | 'Nothing else about the two tiers differs.' in `merged.md` -- The reference text uses identical language when discussing batch tier differences. |
| 31 | Nothing else about the two credential tiers differs. | 23 | carried | 'Nothing else about the two tiers differs.' in `merged.md` -- The reference text explicitly states this conclusion about the two tiers. |
| 32 | Not all gateway refusals are due to caps. | 29 | carried | 'Not all refusals are caps.' in `merged.md` -- The reference text opens the section on other refusals with this statement. |
| 33 | The gateway refuses a request for three reasons and only one of them is the cap. | 29 | carried | 'The gateway refuses a request for three separate reasons, and only one of them is a cap.' in `merged.md` -- The reference text explicitly states this in the other refusals section. |
| 34 | A credential may be suspended. | 29 | carried | 'A credential may be suspended' in `merged.md` -- The reference text lists credential suspension as one refusal reason. |
| 35 | A route may be closed for maintenance. | 29 | carried | 'a route may be closed for maintenance' in `merged.md` -- The reference text lists route closure for maintenance as a reason. |
| 36 | A request body may exceed the 5 megabyte limit. | 29 | carried | 'a body may exceed the 5 megabyte limit' in `merged.md` -- The reference text mentions body size exceeding 5 megabytes as a refusal reason. |
| 37 | Credential suspension, route closure, and request body size violations do not clear themselves by waiting for a stated number of seconds. | 29 | carried | 'None of those three clears itself by waiting for a stated number of seconds.' in `merged.md` -- The reference text directly states these non-cap refusals do not clear by waiting. |
| 38 | A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `merged.md` -- The reference text provides this exact consequence of retrying against suspension. |
| 39 | After a retry loop against a suspended credential, the log shows nothing except a long run of refusals. | 31 | carried | 'the log afterwards shows nothing but a long run of refusals.' in `merged.md` -- The reference text describes the log as showing nothing but refusals in this scenario. |
| 40 | Reading the status code rather than the error class it belongs to separates the two cases. | 31 | carried | 'Reading the status code rather than the error class is what separates these cases' in `merged.md` -- The reference text identifies status code reading as the distinguishing factor. |
| 41 | Reading the status code rather than error class costs one comparison. | 31 | carried | 'and it costs one comparison.' in `merged.md` -- The reference text explicitly states the cost of this distinction. |
| 42 | A cap can be raised. | 35 | carried | 'A cap can be raised' in `merged.md` -- The reference text begins the cap increase section with this statement. |
| 44 | The platform team looks at whether the load is smooth or bursty. | 35 | carried | 'The platform team looks at whether the load is smooth or bursty' in `merged.md` -- The reference text states this as part of the platform team's evaluation process. |
| 45 | A burst is cheaper to smooth than it is to serve at its peak. | 35 | carried | 'a burst is cheaper to smooth than to serve at its peak.' in `merged.md` -- The reference text uses nearly identical language describing burst cost comparison. |
| 46 | A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap. | 35 | carried | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `merged.md` -- The reference text provides this exact principle for managing capacity. |
| 47 | Requests reach the platform team through the usual channel. | 37 | carried | 'Requests reach the platform team through the usual channel' in `merged.md` -- The reference text explicitly states this in the cap increase section. |
| 48 | Requests are answered within two working days. | 37 | carried | 'are answered within two working days.' in `merged.md` -- The reference text specifies the response time for cap increase requests. |
| 49 | There is no expedited path. | 37 | carried | 'There is no expedited path' in `merged.md` -- The reference text explicitly states the absence of expedited processing. |
| 50 | There is no exception list. | 37 | carried | 'and no exception list.' in `merged.md` -- The reference text explicitly states there is no exception list for cap increases. |

### `source_b.md` -- 51 claim(s): 9 dropped, 0 contradicted, 1 carried in part, 41 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 4 | The start of the fixed window is not disclosed by the gateway. | 5 (unverified) | dropped | The reference text does not state whether the window start time is disclosed. |
| 5 | The count follows the credential wherever the caller happens to put it, including across hosts. | 5 | dropped | The reference text does not specify that counts follow credentials across hosts. |
| 8 | A caller that needs more than that is almost always doing batch work under an interactive credential. | 7 | dropped | The reference text does not characterize what work exceeds the default allowance. |
| 12 | The Retry-After header is present on every refusal the gateway sends. | 11 | dropped | The reference text does not state that Retry-After is present on every refusal. |
| 21 | The cause of the refusal on the 503 path is an entirely different one. | 19 | dropped | The reference text does not explicitly compare the causes of refusal on the 503 path versus other paths. |
| 36 | Two of the three have nothing to do with how much traffic a caller has sent in the window it is currently in. | 29 | dropped | The reference text does not explicitly state which of the three reasons have no relation to traffic in the current window. |
| 39 | A request body over the 5 megabyte limit is refused before it has been read at all. | 29 | dropped | The reference text does not state that oversized bodies are refused before being read. |
| 43 | The wasted budget is the caller's own. | 31 (unverified) | dropped | The reference text does not state whose budget is wasted in this scenario. |
| 47 | The team wants to know whether the load is smooth or bursty before it looks at the number at all. | 35 | dropped | The reference text does not specify the order in which the team evaluates load characteristics versus numbers. |
| 22 | Anything computed on the client side is a guess. | 19 | carried in part | 'A wait derived client-side is a guess about a counter it cannot see' in `merged.md` -- The text states client-side wait computation is a guess, but does not generalize to all client-side computation. |
| 1 | Every credential has a cap of its own. | 3 | carried | 'Every credential has a cap.' in `merged.md` -- The statement that every credential has a cap necessarily entails each has its own cap. |
| 2 | When the cap is spent the gateway answers 429 at the edge, without troubling the service behind it. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge without waking the service behind it.' in `merged.md` -- The reference text uses equivalent language describing this response behavior. |
| 3 | Requests are counted against the credential rather than the connection, over a fixed window of 60 seconds. | 5 | carried | 'Requests are counted against the credential rather than the connection over a fixed window of 60 seconds.' in `merged.md` -- The reference text combines these statements in describing the counting mechanism. |
| 6 | A caller spread over many worker processes is throttled at the same point a single process would have been. | 5 | carried | 'a client spread across worker processes is throttled at exactly the point a single process would be.' in `merged.md` -- The reference text states this principle for multiple worker processes. |
| 7 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- The reference text explicitly states this default allowance. |
| 9 | Callers that retry immediately are most of the reason the cap is there. | 7 | carried | 'Callers that retry immediately are the primary reason the cap exists.' in `merged.md` -- The reference text states immediate retries are the primary reason. |
| 10 | The header is called Retry-After. | 11 | carried | 'The refusal carries a Retry-After header.' in `merged.md` -- The reference text identifies this header by its exact name. |
| 11 | Its value is a whole number of seconds. | 11 | carried | 'Its value is a whole number of seconds.' in `merged.md` -- The reference text specifies the header value format. |
| 13 | The response body is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- The reference text states the refusal body is JSON format. |
| 14 | The response body repeats the cap, the window and the tier as plain fields. | 13 | carried | 'names the window, cap, and tier' in `merged.md` -- The reference text lists these fields as plain data in the JSON body. |
| 15 | The body is for the human reading the log afterwards. | 13 | carried | 'The body exists so a human reading a log afterwards can see why the request was refused.' in `merged.md` -- The reference text explicitly states this purpose of the body. |
| 16 | There are four rules. | 17 | carried | 'Four rules' in `merged.md` -- The reference text introduces the retry guidance with this count. |
| 17 | The order they are given in is the order to apply them. | 17 | carried | 'given in the order they should be applied.' in `merged.md` -- The reference text specifies the order of application for the rules. |
| 18 | The gateway has already done that arithmetic. | 19 | carried | 'The gateway has already done that arithmetic' in `merged.md` -- The reference text uses identical language in the first rule. |
| 19 | The gateway did the arithmetic with information the caller cannot see. | 19 | carried | 'with information the caller does not have' in `merged.md` -- The reference text states the gateway has information unavailable to the caller. |
| 20 | On the 503 path the same rule holds. | 19 | carried | 'it does the same on the 503 path.' in `merged.md` -- The reference text states the header rule applies identically on the 503 path. |
| 23 | A 200 needs nothing. | 21 | carried | 'A 200 needs nothing' in `merged.md` -- The reference text uses identical language in the retry rules. |
| 24 | A 429 needs the stated wait. | 21 | carried | 'a 429 needs the stated wait' in `merged.md` -- The reference text includes this requirement in the retry rules. |
| 25 | A 500 can be retried once that wait has passed. | 21 | carried | 'a 500 can be retried once that wait has passed' in `merged.md` -- The reference text states this rule for 500 responses. |
| 26 | A 503 means the platform itself is overloaded. | 21 | carried | 'a 503 means the platform itself is overloaded.' in `merged.md` -- The reference text provides this definition in the retry rules. |
| 27 | A caller that folds all four into one branch will retry hardest during exactly the incident the cap was installed to survive. | 21 | carried | 'A client that folds all non-success responses into one branch will retry hardest during exactly the incident the cap was installed to survive.' in `merged.md` -- The reference text states this principle about folding non-success responses. |
| 28 | A batch credential is allowed 1000 requests in a window. | 23 | carried | 'A batch credential is allowed 1000 requests in a window' in `merged.md` -- The reference text explicitly states this allowance. |
| 29 | 1000 is 50 times the default. | 23 | carried | 'which is 50 times the default' in `merged.md` -- The reference text explicitly provides this mathematical relationship. |
| 30 | The window, the header and the body are identical to the interactive case. | 23 | carried | 'A client written for one tier needs no change at all to run against the other. Nothing else about the two tiers differs.' in `merged.md` -- The necessity that no client changes are needed entails the window, header and body are identical. |
| 31 | Nothing else about the batch tier differs from the default. | 23 | carried | 'Nothing else about the two tiers differs.' in `merged.md` -- The reference text explicitly states this about the batch tier. |
| 32 | A caller that cannot say how often it was refused can't make a case for a larger cap. | 25 (unverified) | carried | 'A caller that cannot say how often it was refused cannot argue for a larger cap' in `merged.md` -- The reference text states inability to document refusals prevents cap increase arguments. |
| 33 | The platform team won't assemble that case on its behalf. | 25 (unverified) | carried | 'and nobody at the platform team will assemble that argument on its behalf.' in `merged.md` -- The reference text explicitly states the team will not make the case for the caller. |
| 34 | The gateway refuses a request for three separate reasons. | 29 | carried | 'The gateway refuses a request for three separate reasons' in `merged.md` -- The reference text explicitly states this count of separate reasons. |
| 35 | Only one of them is a cap. | 29 | carried | 'and only one of them is a cap.' in `merged.md` -- The reference text directly states that one of three reasons is the cap. |
| 37 | A credential can be suspended. | 29 | carried | 'A credential may be suspended' in `merged.md` -- The reference text lists credential suspension as a refusal reason. |
| 38 | A route can be closed while it is being repaired. | 29 | carried | 'a route may be closed for maintenance' in `merged.md` -- The reference text mentions route closure during maintenance as a refusal reason. |
| 40 | A loop retrying against a suspended credential burns its whole budget. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget' in `merged.md` -- The reference text states this consequence of retrying against suspension. |
| 41 | A loop retrying against a suspended credential reaches nothing. | 31 | carried | 'without ever reaching the service' in `merged.md` -- The reference text states this outcome of the retry loop. |
| 42 | The log afterwards shows a long run of refusals and no successes at all. | 31 | carried | 'the log afterwards shows nothing but a long run of refusals.' in `merged.md` -- The reference text describes the log as containing nothing but refusals. |
| 44 | A caller that can move half its work to a quieter hour usually finds it doesn't need a larger cap in the first place. | 33 (unverified) | carried | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `merged.md` -- The reference text uses equivalent language about not needing cap changes. |
| 45 | A cap can be raised. | 33 | carried | 'A cap can be raised' in `merged.md` -- The reference text explicitly states that caps can be raised. |
| 46 | A cap cannot be raised but not on the strength of an assertion that the current one is too small. | 33 | carried | 'A cap can be raised, but not without measurement behind the request.' in `merged.md` -- The reference text establishes that measurement is required for cap increases. |
| 48 | Requests go to the platform team through the usual channel. | 35 | carried | 'Requests reach the platform team through the usual channel' in `merged.md` -- The reference text states this routing for cap increase requests. |
| 49 | There is no expedited path. | 37 | carried | 'There is no expedited path' in `merged.md` -- The reference text explicitly states the absence of expedited processing. |
| 50 | An answer takes two working days. | 37 | carried | 'are answered within two working days.' in `merged.md` -- The reference text specifies this response time for all cap increase requests. |
| 51 | Chasing an answer doesn't make it take fewer working days. | 37 (unverified) | carried | 'There is no expedited path and no exception list.' in `merged.md` -- The text states there is no expedited path, which directly entails that attempting to chase or push for a faster answer will not reduce the working days required. |

### `merged.md` -- 54 claim(s): 0 invented, 0 contradicted, 0 supported in part, 54 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Every credential has a cap. | supported | `source_a.md` | 'Every credential has a cap.' in `source_a.md` -- Source states this claim directly and identically. |
| 2 | When a credential's cap is reached, the gateway answers 429 at the edge without waking the service behind it. | supported | `source_a.md` | 'When that cap is spent the gateway answers 429 at the edge — without waking the service behind it' in `source_a.md` -- Source describes the exact behavior claimed: gateway responds 429 at edge without waking the backend service. |
| 3 | Requests are counted against the credential rather than the connection over a fixed window of 60 seconds. | supported | `source_a.md` | 'Requests are counted against the credential that presented them, over a fixed window of 60 seconds, and never against a connection.' in `source_a.md` -- Source states requests are counted by credential over a 60-second window, not by connection. |
| 4 | Opening additional sockets provides no benefit. | supported | `source_a.md` | 'Opening a second socket therefore buys a caller nothing.' in `source_a.md` -- Source directly states that additional sockets provide no benefit. |
| 5 | A client spread across worker processes is throttled at exactly the point a single process would be. | supported | `source_a.md` | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `source_a.md` -- Source describes that distributed clients are throttled at the same point as a single process would be. |
| 6 | The default allowance is 100 requests in a window. | supported | `source_a.md` | 'The default allowance is 100 requests in a window' in `source_a.md` -- Both sources state the default allowance is exactly 100 requests per window. |
| 7 | A credential marked for batch work is allowed 1000 in the same window. | supported | `source_a.md` | 'a credential marked for batch work is allowed 1000 in the same window' in `source_a.md` -- Source states batch credentials receive 1000 requests in the same window. |
| 8 | A 429 refusal is not an outage but the platform declining to spend capacity already promised to someone else. | supported | `source_a.md` | 'A refusal is not an outage, whatever the error class in a client library happens to call it. It is the platform declining to spend capacity that has already been promised to somebody else' in `source_a.md` -- Source explains that 429 is not an outage but the platform protecting already-promised capacity. |
| 9 | Attempting to implement a client-side counter that mirrors the gateway's own creates two disagreeing counters. | supported | `source_b.md` | "An earlier draft of this note argued for a client-side token bucket that mirrored the gateway's own counters, and that section has been left out on purpose — two counters that disagree are worse than one counter that refuses" in `source_b.md`, **transcription_error** -- Source explicitly discusses mirroring the gateway with a client-side bucket and identifies disagreeing counters as problematic. |
| 10 | Callers that retry immediately are the primary reason the cap exists. | supported | `source_a.md` | 'Callers that retry at once are the largest single reason the cap is there at all.' in `source_a.md` -- Source identifies immediate retries as the primary reason for the cap's existence. |
| 11 | The refusal carries a Retry-After header. | supported | `source_a.md` | 'The refusal carries a Retry-After header.' in `source_a.md` -- Source directly states that 429 refusals carry a Retry-After header. |
| 12 | The Retry-After header value is a whole number of seconds. | supported | `source_a.md` | 'Its value is a whole number of seconds to wait.' in `source_a.md` -- Source states the Retry-After header value is a whole number of seconds. |
| 13 | Waiting the time specified in the Retry-After header and then continuing is the entire contract. | supported | `source_a.md` | 'Waiting that long and then continuing is the whole of the contract' in `source_a.md` -- Source describes waiting the header time and continuing as the complete contract. |
| 14 | A client that waits the time specified in the Retry-After header and then continues needs nothing else. | supported | `source_a.md` | 'a client that does it needs nothing else from this document' in `source_a.md` -- Source states a client following the header needs no other guidance from the documentation. |
| 15 | The gateway keeps no memory of who backed off politely. | supported | `source_a.md` | 'The gateway keeps no memory of who backed off politely' in `source_a.md` -- Source explicitly states the gateway has no memory of clients that wait politely. |
| 16 | Waiting longer than the time specified in the Retry-After header earns no credit. | supported | `source_a.md` | 'waiting longer than the header asks earns a caller no credit at all.' in `source_a.md` -- Source states waiting beyond the header time provides no benefit. |
| 17 | The body of the refusal is JSON and names the window, cap, and tier. | supported | `source_a.md` | 'The body of the refusal is JSON, and it names what the gateway calls the "window" it counted in. It names the cap and the tier as well.' in `source_a.md`, **transcription_error** -- Source describes the JSON body as containing window, cap, and tier information. |
| 18 | A caller that parses the body to compute its own wait is doing the same arithmetic twice. | supported | `source_a.md` | 'a caller that parses the body to compute its own wait is doing the same arithmetic twice' in `source_a.md` -- Source warns that parsing the body to compute wait duplicates the gateway's already-completed arithmetic. |
| 19 | The body exists so a human reading a log afterwards can see why the request was refused. | supported | `source_a.md` | 'The body is there so that a human reading a log afterwards can see why the request was refused' in `source_a.md` -- Source explains the body's purpose is for human interpretation during log review. |
| 20 | The gateway has already done that arithmetic with information the caller does not have. | supported | `source_a.md` | 'The gateway has already done that arithmetic, with information the caller does not have' in `source_a.md` -- Source states the gateway has completed arithmetic using information unavailable to the caller. |
| 21 | The gateway does the same arithmetic on the 503 path. | supported | `source_a.md` | 'and it does the same on the 503 path' in `source_a.md` -- Source indicates the gateway applies identical arithmetic logic to the 503 response path. |
| 22 | A wait derived client-side is a guess about a counter the caller cannot see. | supported | `source_a.md` | 'A wait derived on the client side is a guess about a counter it cannot see.' in `source_a.md` -- Source describes client-side wait calculations as guesses about inaccessible counters. |
| 23 | A 200 response needs nothing. | supported | `source_a.md` | 'A 200 wants nothing' in `source_a.md` -- Source lists 200 as requiring no action in the retry logic. |
| 24 | A 429 response needs the stated wait. | supported | `source_a.md` | 'a 429 wants the stated wait' in `source_a.md` -- Source specifies that 429 responses require the wait specified in the header. |
| 25 | A 500 response can be retried once that wait has passed. | supported | `source_a.md` | 'a 500 may be retried once that wait has passed' in `source_a.md` -- Source allows 500 responses to be retried after the Retry-After wait period. |
| 26 | A 503 response means the platform itself is overloaded. | supported | `source_a.md` | 'a 503 is the overload path' in `source_a.md` -- Source identifies 503 as the platform overload response. |
| 27 | These response codes are not interchangeable. | supported | `source_a.md` | 'The four cases are not interchangeable.' in `source_a.md` -- Source explicitly states these four response codes require different handling and are not interchangeable. |
| 28 | A client that folds all non-success responses into one branch will retry hardest during exactly the incident the cap was installed to survive. | supported | `source_a.md` | 'A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive.' in `source_a.md` -- Source warns that treating all failures uniformly causes worst retries during the very incident the cap prevents. |
| 29 | A batch credential is allowed 1000 requests in a window. | supported | `source_a.md` | 'a credential marked for batch work is allowed 1000 in the same window' in `source_a.md` -- Source states batch credentials receive 1000 requests within the window. |
| 30 | 1000 is 50 times the default. | supported | `source_a.md` | 'A batch credential is allowed fifty times the default allowance' in `source_a.md` -- Source states 1000 is fifty times the default of 100. |
| 31 | The batch allowance is measured over exactly the same window, not a separate counting scheme. | supported | `source_a.md` | 'it is measured over exactly the same window' in `source_a.md` -- Source confirms batch allowance uses the identical 60-second window, not a separate counting mechanism. |
| 32 | A client written for one tier needs no change at all to run against the other. | supported | `source_b.md` | 'so a client written for one tier needs no change at all to run against the other' in `source_b.md` -- Source states clients can work against both tiers without modification. |
| 33 | Nothing else about the two tiers differs. | supported | `source_a.md` | 'Nothing else about the two tiers differs in any way.' in `source_a.md` -- Source states tiers are identical in all aspects except the allowance size. |
| 34 | A caller that cannot say how often it was refused cannot argue for a larger cap. | supported | `source_a.md` | 'A caller that cannot say how often it was refused last week cannot argue for a larger cap' in `source_a.md` -- Source requires refusal data as evidence for cap increase requests. |
| 35 | Nobody at the platform team will assemble that argument on behalf of a caller. | supported | `source_a.md` | 'and nobody at the far end will assemble that argument on its behalf' in `source_a.md` -- Source states the platform team will not build a cap-increase case without the caller providing data. |
| 36 | Not all refusals are caps. | supported | `source_a.md` | 'Not all are caps.' in `source_a.md` -- Source identifies that multiple refusal reasons exist beyond rate limiting caps. |
| 37 | The gateway refuses a request for three separate reasons. | supported | `source_a.md` | 'The gateway refuses a request for three reasons' in `source_a.md` -- Source identifies exactly three distinct reasons the gateway refuses requests. |
| 38 | Only one of those three reasons is a cap. | supported | `source_b.md` | 'and only one of them is a cap' in `source_b.md` -- Source states only one of the three refusal reasons relates to rate-limit caps. |
| 39 | A credential may be suspended. | supported | `source_a.md` | 'A credential may be suspended' in `source_a.md` -- Source lists credential suspension as one of the three non-cap refusal reasons. |
| 40 | A route may be closed for maintenance. | supported | `source_a.md` | 'a route may be closed for maintenance' in `source_a.md` -- Source identifies route maintenance closure as a non-cap refusal reason. |
| 41 | A request body may exceed the 5 megabyte limit. | supported | `source_a.md` | 'a body may exceed the 5 megabyte limit' in `source_a.md` -- Source identifies oversized request bodies as a non-cap refusal reason. |
| 42 | None of those three clears itself by waiting for a stated number of seconds. | supported | `source_a.md` | 'None of those three clears itself by waiting for a stated number of seconds.' in `source_a.md` -- Source clarifies that non-cap refusals are permanent and will not resolve through waiting. |
| 43 | A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service. | supported | `source_a.md` | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `source_a.md` -- Source describes the consequence of retry loops against permanent refusals. |
| 44 | The log afterwards shows nothing but a long run of refusals. | supported | `source_a.md` | 'and the log afterwards shows nothing at all except a long run of refusals' in `source_a.md` -- Source describes logs from retry loops against permanent errors. |
| 45 | Reading the status code rather than the error class is what separates these cases. | supported | `source_a.md` | 'Reading the status code rather than the class it belongs to is what separates the two cases' in `source_a.md` -- Source identifies status code inspection as the key distinction between cap and non-cap refusals. |
| 46 | Reading the status code costs one comparison. | supported | `source_a.md` | 'and it costs one comparison' in `source_a.md` -- Source notes the minimal overhead of reading the status code. |
| 47 | A cap can be raised, but not without measurement behind the request. | supported | `source_a.md` | 'A cap can be raised, and the number of caps raised without a measurement behind them is 0.' in `source_a.md` -- Source indicates caps are only raised with supporting measurement data. |
| 48 | The platform team looks at whether the load is smooth or bursty. | supported | `source_a.md` | 'The platform team looks at whether the load is smooth or bursty' in `source_a.md` -- Source describes the team's analysis of traffic patterns for cap requests. |
| 49 | A burst is cheaper to smooth than to serve at its peak. | supported | `source_a.md` | 'a burst is cheaper to smooth than it is to serve at its peak' in `source_a.md` -- Source explains the team's preference for load smoothing over cap increases. |
| 50 | A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all. | supported | `source_a.md` | 'A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all' in `source_a.md` -- Source indicates load shifting often resolves capacity issues without requiring higher caps. |
| 51 | Requests reach the platform team through the usual channel. | supported | `source_a.md` | 'Requests reach the platform team through the usual channel' in `source_a.md` -- Source specifies the standard process for submitting cap increase requests. |
| 52 | Requests are answered within two working days. | supported | `source_a.md` | 'and they are answered within two working days' in `source_a.md` -- Source provides the service level for responding to cap requests. |
| 53 | There is no expedited path. | supported | `source_a.md` | 'There is no expedited path' in `source_a.md` -- Source explicitly states no expedited option exists for cap requests. |
| 54 | There is no exception list. | supported | `source_a.md` | 'and no exception list.' in `source_a.md` -- Source explicitly states no exceptions exist to the standard cap request process. |

## Structure

**9** mechanical check(s) over **104** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **54** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **101**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 13 run(s) over 44 attributed segment(s) — sources interleaved. 6 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

`[-...-]` is what the source said and `{+...+}` is what the merge says.

### Absent and undeclared — in a source, not in the merge, and no record explains it

- `a6` (`source_a.md`) — 'A client spread across eight worker processes is throttled at exactly the point one process would have been — and pays for the extra file descriptors as well.' is not in the merge and no disposition record explains it (nearest merge segment m5 at 0.61)

  ```text
  In the source: A client spread across eight worker processes is throttled at exactly the point one process would have been — and pays for the extra file descriptors as well.
  ```
- `a8` (`source_a.md`) — 'A refusal is not an outage, whatever the error class in a client library happens to call it.' is not in the merge and no disposition record explains it (nearest merge segment m7 at 0.47)

  ```text
  In the source: A refusal is not an outage, whatever the error class in a client library happens to call it.
  ```

### Reworded and undeclared — in the merge in altered wording, and no record explains it. At off this also covers layout: a segment whose source line breaks the merge ran together is altered and undeclared, and 380 reuses this kind rather than moving FINDING_KINDS off 12

- `a9` (`source_a.md`) — 'It is the platform declining to spend capacity that has already been promised to somebody else, and waiting is the only correct answer.' is reworded in the merge and no disposition record explains it (nearest merge segment m7 at 0.77)

  ```text
  In the source: It is the platform declining to spend capacity that has already been promised to somebody else, and waiting is the only correct answer.
  In the merge:  A 429 refusal is not an outage but the platform declining to spend capacity already promised to someone else; waiting is the correct answer.
  ```
- `a10` (`source_a.md`) — 'Callers that retry at once are the largest single reason the cap is there at all.' is reworded in the merge and no disposition record explains it (nearest merge segment m9 at 0.71)

  ```text
  In the source: Callers that retry at once are the largest single reason the cap is there at all.
  In the merge:  Callers that retry immediately are the primary reason the cap exists.
  ```
- `a23` (`source_a.md`) — 'The gateway has already done that arithmetic, with information the caller does not have, and it does the same on the 503 path.' is reworded in the merge and no disposition record explains it (nearest merge segment m21 at 1.00)

  ```text
  In the source: The gateway has already done that arithmetic, with information the caller does not have, and it does the same on the 503 path.
  In the merge:  The gateway has already done that arithmetic with information the caller does not have, and it does the same on the 503 path.
  What changed:  The gateway has already done that arithmetic[-,-] with information the caller does not have, and it does the same on the 503 path.
  ```

### Declared gone, still here — a record says the content departed and the merge carries the segment unchanged

- `b28` (`source_b.md`) — 'A 200 needs nothing, a 429 needs the stated wait, a 500 can be retried once that wait has passed, and a 503 means the platform itself is overloaded.' is declared 'superseded' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: A 200 needs nothing, a 429 needs the stated wait, a 500 can be retried once that wait has passed, and a 503 means the platform itself is overloaded.
  In the merge:  A 200 needs nothing, a 429 needs the stated wait, a 500 can be retried once that wait has passed, and a 503 means the platform itself is overloaded.
  ```
- `b38` (`source_b.md`) — 'The gateway refuses a request for three separate reasons, and only one of them is a cap.' is declared 'superseded' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: The gateway refuses a request for three separate reasons, and only one of them is a cap.
  In the merge:  The gateway refuses a request for three separate reasons, and only one of them is a cap.
  ```

### Verbatim violation — an invariant-core token did not survive unchanged

- `a47` (`source_a.md`) — numeric '0' does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **81** departure(s) from its sources. Checking them confirms 39, rejects 14, and leaves 28 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 1 of 104 source segment(s) declared gone, **1.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | Base document's title was chosen. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Rate limiting and the 429 contract for gateway clients' and says so (no claim traced to it) |
| `a3` | reworded | Cost impact detail omitted; core contract stated. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-003 came back MISSING (`A-003`) |
| `a4` | reworded | Minor wording adjustment for clarity. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-004`, `A-005`, `A-006`) |
| `a5` | reworded | Modernised phrasing. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-007`) |
| `a13` | reworded | Dropped 'to wait' as it is implied. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-015`) |
| `a14` | reworded | Removed meta-commentary about the document itself. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a15` | reworded | Minor wording simplification. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-016`, `A-017`) |
| `a16` | reworded | Simplified; merged with a17. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-018`) |
| `a17` | subsumed | Content combined into reworded a16. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-020`) |
| `a19` | reworded | Removed clause about retry loop; kept purpose. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a22` | reworded | Minor punctuation change. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a24` | reworded | Hyphenated 'client-side' for consistency. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a25` | reworded | Reframed comparison for clarity. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a27` | superseded | b28 wording is clearer; used instead. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`A-022`, `A-023`, `A-024`, `A-025`) |
| `a28` | reworded | Changed 'four' to 'These' for flow. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a29` | reworded | Changed 'every non-success' to 'all non-success responses'. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-026`) |
| `a30` | subsumed | Advice to avoid loop is implicit in rule. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a32` | reconciled | Combined with b31 for complete statement. | **rejected** | declared 'reconciled', which predicts SUPPORTED; A-028 came back MISSING (`A-028`) |
| `a33` | dropped | Implementation detail not critical to contract. | **rejected** | declared 'dropped', which predicts MISSING; A-030 came back SUPPORTED (`A-030`) |
| `a34` | reworded | Removed 'in any way' as unnecessary. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-031`) |
| `a36` | reworded | Changed 'far end' to 'platform team'; removed 'last week'. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a37` | reworded | Added Oxford comma. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a39` | reworded | Added 'refusals' for clarity. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-032`) |
| `a40` | superseded | b38 wording is clearer; used instead. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`A-033`) |
| `a43` | reworded | Added 'critically' for emphasis. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a44` | reworded | Changed em-dash to comma; simplified 'nothing but'. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-038`, `A-039`) |
| `a45` | reworded | Changed 'the class it belongs to' to 'error class'; 'two cases' to 'these'. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-040`, `A-041`) |
| `a47` | reworded | Restructured from assertion about zero to negation. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-043 came back MISSING (`A-043`) |
| `a49` | reworded | Changed em-dash to semicolon; minor rewording. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-044`, `A-045`) |
| `a51` | reworded | Parallel construction. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-047`, `A-048`) |
| `b2` | duplicate | Same fact as a2; a2 wording used. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-001`) |
| `b3` | subsumed | Core fact carried in merged opening. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-002`) |
| `b4` | reworded | Reframed as explanation of principle rather than document history. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b5` | superseded | a4 version used; detail about undisclosed start omitted. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-003`) |
| `b6` | subsumed | Core concept carried in a5 rewording. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b7` | subsumed | Across-hosts principle subsumed in broader statement. | **rejected** | declared 'subsumed', which predicts SUPPORTED; B-005 came back MISSING (`B-005`) |
| `b8` | duplicate | Duplicate of a6 concept. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-006`) |
| `b9` | superseded | a7 more definitive; editorial context omitted. | **rejected** | declared 'superseded', which predicts SUPPORTED or CONTRADICTED or PARTIAL; B-008 came back MISSING (`B-008`) |
| `b10` | subsumed | Core concept in opening explanation. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b11` | superseded | a10 version reworded and used. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-009`) |
| `b12` | duplicate | Same heading as a11. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b13` | subsumed | Covered by merged text. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-010`) |
| `b14` | superseded | a13 version used; 'always present' detail omitted. | **rejected** | declared 'superseded', which predicts SUPPORTED or CONTRADICTED or PARTIAL; B-012 came back MISSING (`B-012`) |
| `b15` | subsumed | Meta-commentary removed; core contract carried. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b16` | duplicate | Same fact as a15. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b17` | subsumed | Content merged into a16. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-013`, `B-014`) |
| `b18` | superseded | a18 version used. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b19` | superseded | a19 version used. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-015`) |
| `b20` | superseded | Base document's heading chosen. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b21` | superseded | a21 version used. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-016`, `B-017`) |
| `b22` | subsumed | Carried in merged rule 1. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b23` | subsumed | Content in merged rule 1. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-018`, `B-019`) |
| `b24` | subsumed | 503 path covered in rule 1. | **rejected** | declared 'subsumed', which predicts SUPPORTED; B-021 came back MISSING (`B-021`) |
| `b25` | subsumed | Covered in rule 1. | **rejected** | declared 'subsumed', which predicts SUPPORTED; B-022 came back PARTIAL (`B-022`) |
| `b26` | subsumed | Covered in rule 1. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b27` | subsumed | Core rule carried in rule 2. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b28` | superseded | b28 wording clearer than a27; used in rule 2. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-023`, `B-024`, `B-025`, `B-026`) |
| `b29` | superseded | a29 version used with minor rewording. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-027`) |
| `b30` | subsumed | Behaviour explanation carries the prevention goal. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b31` | reconciled | Combined with a32 to include both 1000 spec and window detail. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-028`, `B-029`) |
| `b32` | subsumed | Carried in rule 3. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-030`) |
| `b33` | duplicate | Same as a34. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-031`) |
| `b34` | reconciled | Weekly retention requirement from b34 added to a35. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b35` | superseded | a36 wording used; 'can't' changed to 'cannot'. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b36` | subsumed | Importance of counts implied in rule 4. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b37` | superseded | Base document's heading chosen. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b38` | superseded | b38 wording clearer; used over a40. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-034`, `B-035`) |
| `b39` | subsumed | Implication carried in discussion of three reasons. | **rejected** | declared 'subsumed', which predicts SUPPORTED; B-036 came back MISSING (`B-036`) |
| `b40` | superseded | a41 version used. | **rejected** | declared 'superseded', which predicts SUPPORTED or CONTRADICTED or PARTIAL; B-039 came back MISSING (`B-039`) |
| `b41` | superseded | a43 version reworded and used. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b42` | subsumed | Carried in a44 rewording. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-040`, `B-041`) |
| `b43` | subsumed | Outage misattribution idea carried in a44. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-042`) |
| `b44` | superseded | a50 version used. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b45` | subsumed | Cheapest fix idea carried in a50. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b46` | superseded | a47 version used. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-045`, `B-046`) |
| `b47` | superseded | a48 version used. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b48` | subsumed | Smooth vs bursty evaluation carried in a49. | **rejected** | declared 'subsumed', which predicts SUPPORTED; B-047 came back MISSING (`B-047`) |
| `b49` | duplicate | Same fact as a49. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b50` | subsumed | Channel detail carried in a51. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-048`) |
| `b51` | superseded | a52 version used with both expedited and exception elements. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-049`) |
| `b52` | subsumed | Two working days timeline carried in a51. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-050`) |


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
| Calls | 8 live, 0 cached, 0 replayed |
| Tokens | unknown (8 call(s) reported no usage) |
| Cost | unmeasured (8 call(s) reported no tokens, so no figure can be derived) |
| Schema repairs | 1 |
| Isolation | decompose, merge, verify: safe mode, no tools |
| Errors | 0 |
| Duration | 1125.1s |
| Generated | 2026-09-27T17:44:02+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup haiku-4.5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
