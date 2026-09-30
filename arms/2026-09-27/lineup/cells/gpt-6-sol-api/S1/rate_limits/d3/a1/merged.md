# Rate limiting and the 429 contract for gateway clients

Every credential has a cap. When that cap is spent the gateway answers 429 at the edge — without waking the service behind it — so the refusal costs the platform almost nothing and costs a caller that files it under transport error a great deal. An earlier draft proposed a client-side token bucket that mirrored the gateway’s counters; it was left out because two counters that disagree are worse than one counter that refuses.

Requests are counted against the credential that presented them, over a fixed window of 60 seconds, and never against a connection. The gateway does not disclose when the window starts. Opening a second socket therefore buys a caller nothing. The count follows the credential across hosts. A client spread across eight worker processes is throttled at exactly the point one process would have been — and pays for the extra file descriptors as well.

The default allowance is 100 requests in a window, and a credential marked for batch work is allowed 1000 in the same window. The default allowance is enough for every interactive use of this API the platform team has seen; callers needing more are almost always doing batch work under an interactive credential. A refusal is not an outage, whatever the error class in a client library happens to call it, and it is not a gateway bug. It is the platform declining to spend capacity that has already been promised to somebody else, and waiting is the only correct answer. Callers that retry at once are the largest single reason the cap is there at all.

## How to read a refusal

The refusal carries a Retry-After header. It is present on every refusal the gateway sends. Its value is a whole number of seconds to wait. Waiting that long and then continuing is the whole of the contract — a client that does it needs nothing else from this document. That is the intended outcome, even if it leaves the rest of this guidance unread. The gateway keeps no memory of who backed off politely, so waiting longer than the header asks earns a caller no credit at all.

The body of the refusal is JSON, and it names what the gateway calls the “window” it counted in. It names the cap and the tier as well. These appear as plain fields. None of those fields is a substitute for the header, and a caller that parses the body to compute its own wait is doing the same arithmetic twice. A client-computed wait can disagree with the gateway. The body is there so that a human reading a log afterwards can see why the request was refused — nothing in it is meant for the retry loop.

## How to retry well

Four rules, given in the order they should be applied.

1. Honour the header, every time. The gateway has already done that arithmetic, with information the caller does not have, and it does the same on the 503 path. A wait derived on the client side is a guess about a counter it cannot see. There is no case at all where a guess is the better of the two.

2. Retry only what is safe to retry. Retryable responses are a smaller set than all unsuccessful responses. A 200 wants nothing, a 429 wants the stated wait, a 500 may be retried once that wait has passed, and a 503 is the overload path. The four cases are not interchangeable. A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive. Avoid writing that loop.

3. Batch is different. A batch credential is allowed 1000 requests in the same window as the default credential. The tier is set on the credential when it is issued and cannot be asked for per call. The window, the header and the body are identical to the interactive case, so a client written for one tier needs no change at all to run against the other. Nothing else about the two tiers differs in any way.

4. Log every refusal seen. Keep the log for at least a week. A caller that cannot say how often it was refused last week cannot argue for a larger cap, and nobody at the far end will assemble that argument on its behalf. Without refusal counts, a request for a larger cap is only a preference. The log line should carry the credential, the window and the wait.

## Other refusals and their codes

Not all are caps. The gateway can refuse requests for reasons other than a spent cap. A credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit. A maintenance closure can occur while a route is being repaired, and an oversized body is refused before it has been read at all. Some of these refusals have nothing to do with traffic sent in the current window. None of those three clears itself by waiting for a stated number of seconds.

The distinction matters to a retry loop. A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service — and the log afterwards shows nothing at all except a long run of refusals. The log shows no successes; that pattern can be mistaken for an outage, but the wasted retry budget belongs to the caller. Reading the status code rather than the class it belongs to is what separates the two cases, and it costs one comparison.

## Asking for an increase

A cap can be raised, and the number of caps raised without a measurement behind them is 0. Bring a week of refusal counts, the shape of the traffic across the day, and the deadline that traffic is serving. The platform team looks at whether the load is smooth or bursty — a burst is cheaper to smooth than it is to serve at its peak. The team assesses the traffic pattern before considering a higher cap. A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all, which is the outcome everyone prefers. Moving work to a quieter hour is the cheapest fix available and is available to almost everybody.

Requests reach the platform team through the usual channel, and they are answered within two working days. Chasing a request does not shorten that response time. There is no expedited path and no exception list.