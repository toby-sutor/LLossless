# Rate limiting and the 429 contract for gateway clients

Every credential has a cap. When that cap is spent the gateway answers 429 at the edge without waking the service behind it. Requests are counted against the credential rather than the connection over a fixed window of 60 seconds. Opening additional sockets provides no benefit, and a client spread across worker processes is throttled at exactly the point a single process would be. The default allowance is 100 requests in a window, and a credential marked for batch work is allowed 1000 in the same window. A 429 refusal is not an outage but the platform declining to spend capacity already promised to someone else; waiting is the correct answer. Attempting to implement a client-side counter that mirrors the gateway's own creates two disagreeing counters, which is worse than a single counter that refuses. Callers that retry immediately are the primary reason the cap exists.

## How to read a refusal

The refusal carries a Retry-After header. Its value is a whole number of seconds. Waiting that long and then continuing is the entire contract; a client that does it needs nothing else. The gateway keeps no memory of who backed off politely, so waiting longer than the header asks earns no credit.

The body of the refusal is JSON and names the window, cap, and tier. None of those fields is a substitute for the header, and a caller that parses the body to compute its own wait is doing the same arithmetic twice. The body exists so a human reading a log afterwards can see why the request was refused.

## How to retry well

Four rules, given in the order they should be applied.

1. Honour the header every time. The gateway has already done that arithmetic with information the caller does not have, and it does the same on the 503 path. A wait derived client-side is a guess about a counter it cannot see, and there is no case where a guess is better than the gateway's calculation.

2. Retry only what is safe to retry. A 200 needs nothing, a 429 needs the stated wait, a 500 can be retried once that wait has passed, and a 503 means the platform itself is overloaded. These cases are not interchangeable. A client that folds all non-success responses into one branch will retry hardest during exactly the incident the cap was installed to survive.

3. Batch is different. A batch credential is allowed 1000 requests in a window, which is 50 times the default and is measured over exactly the same window, not a separate counting scheme. A client written for one tier needs no change at all to run against the other. Nothing else about the two tiers differs.

4. Log every refusal seen. A caller that cannot say how often it was refused cannot argue for a larger cap, and nobody at the platform team will assemble that argument on its behalf. The log should carry the credential, the window, and the wait. Keep the log for at least a week.

## Other refusals and their codes

Not all refusals are caps. The gateway refuses a request for three separate reasons, and only one of them is a cap. A credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit. None of those three clears itself by waiting for a stated number of seconds. The distinction matters critically to a retry loop. A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service, and the log afterwards shows nothing but a long run of refusals. Reading the status code rather than the error class is what separates these cases, and it costs one comparison.

## Asking for an increase

A cap can be raised, but not without measurement behind the request. Bring a week of refusal counts, the shape of the traffic across the day, and the deadline that traffic is serving. The platform team looks at whether the load is smooth or bursty; a burst is cheaper to smooth than to serve at its peak. A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all, which is the outcome everyone prefers. Requests reach the platform team through the usual channel and are answered within two working days. There is no expedited path and no exception list.