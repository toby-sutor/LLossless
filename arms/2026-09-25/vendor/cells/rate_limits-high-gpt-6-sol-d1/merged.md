# Rate limiting and the 429 contract for gateway clients

Every credential has a cap. When that cap is spent the gateway answers 429 at the edge — without waking the service behind it — so the refusal costs the platform almost nothing and costs a caller that files it under transport error a great deal. An earlier draft of this note argued for a client-side token bucket that mirrored the gateway’s own counters, and that section has been left out on purpose — two counters that disagree are worse than one counter that refuses, which is the whole reason the header exists.

Requests are counted against the credential that presented them, over a fixed window of 60 seconds, and never against a connection. The gateway does not disclose when the window starts. Opening a second socket therefore buys a caller nothing. A client spread across eight worker processes is throttled at exactly the point one process would have been — and pays for the extra file descriptors as well. The count follows the credential wherever the caller happens to put it, including across hosts.

The default allowance is 100 requests in a window, and a credential marked for batch work is allowed 1000 in the same window. The default allowance is enough for every interactive use of this API the platform team has seen; callers that need more are almost always doing batch work under an interactive credential. A refusal is not an outage or a gateway bug, whatever the error class in a client library happens to call it. It is the platform declining to spend capacity that has already been promised to somebody else, and waiting is the only correct answer. Callers that retry at once are the largest single reason the cap is there at all.

## How to read a refusal

The refusal carries a Retry-After header. Its value is a whole number of seconds to wait. The Retry-After header is present on every gateway refusal. Waiting that long and then continuing is the whole of the contract — a client that does it needs nothing else from this document. The gateway keeps no memory of who backed off politely, so waiting longer than the header asks earns a caller no credit at all.

The body of the refusal is JSON, and it names what the gateway calls the “window” it counted in. It names the cap and the tier as well. The cap, window and tier appear as plain JSON fields. None of those fields is a substitute for the header, and a caller that parses the body to compute its own wait is doing the same arithmetic twice. Computing a wait from those fields risks disagreeing with the gateway. The body is there so that a human reading a log afterwards can see why the request was refused — nothing in it is meant for the retry loop.

## How to retry well

Four rules, given in the order they should be applied.

1. Honour the header, every time. The gateway has already done that arithmetic, with information the caller does not have, and it does the same on the 503 path. A 503 has a different cause, but the same header rule applies. A wait derived on the client side is a guess about a counter it cannot see. There is no case at all where a guess is the better of the two.
2. Retry only what is safe to retry. A 200 wants nothing, a 429 wants the stated wait, a 500 may be retried once that wait has passed, and a 503 is the platform-overload path. The four cases are not interchangeable. A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive. Avoid writing that loop.
3. Batch is different. A batch credential is allowed 1000 requests in the same window. The tier is set on the credential when it is issued and cannot be asked for per call. Nothing else about the two tiers differs in any way. The window, header and body are identical across tiers, so a client written for one tier needs no change to run against the other.
4. Log every refusal seen. Keep the log for at least a week. A caller that cannot say how often it was refused last week cannot argue for a larger cap, and nobody at the far end will assemble that argument on its behalf. The log line should carry the credential, the window and the wait. Without refusal counts, a request for a larger cap is only a preference.

## Other refusals and their codes

Not all are caps. The gateway refuses requests for a cap and for three other reasons. A credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit. Suspension and route maintenance have nothing to do with traffic in the current window. A body over the 5 megabyte limit is refused before it has been read at all. None of those three clears itself by waiting for a stated number of seconds.

The distinction matters to a retry loop. A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service — and the log afterwards shows nothing at all except a long run of refusals. Such logs can look like an outage despite showing no successes; the wasted retry budget belongs to the caller. Reading the status code rather than the class it belongs to is what separates the two cases, and it costs one comparison.

## Asking for an increase

A cap can be raised, and the number of caps raised without a measurement behind them is 0. Bring a full week of refusal counts, the shape of the traffic across the day, and the deadline that traffic is serving. The platform team looks at whether the load is smooth or bursty — a burst is cheaper to smooth than it is to serve at its peak. The team considers the shape of the load before the number. A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all, which is the outcome everyone prefers. The fix is available to almost everybody and is the cheapest available.

Requests reach the platform team through the usual channel, and they are answered within two working days. There is no expedited path and no exception list. Chasing a request does not shorten the response time.