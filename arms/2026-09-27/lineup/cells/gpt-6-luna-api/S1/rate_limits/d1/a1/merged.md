# Rate limiting and the 429 contract for gateway clients

Every credential has a cap. When that cap is spent the gateway answers 429 at the edge — without waking the service behind it — so the refusal costs the platform almost nothing and costs a caller that files it under transport error a great deal. An earlier draft of this note argued for a client-side token bucket that mirrored the gateway’s own counters, and that section has been left out on purpose — two counters that disagree are worse than one counter that refuses, which is the whole reason the header exists.

Requests are counted against the credential that presented them, over a fixed window of 60 seconds, and never against a connection. The window’s start is not disclosed by the gateway. Opening a second socket therefore buys a caller nothing. The count follows the credential wherever the caller happens to put it, including across hosts. A client spread across eight worker processes is throttled at exactly the point one process would have been — and pays for the extra file descriptors as well.

The default allowance is 100 requests in a window, and a credential marked for batch work is allowed 1000 in the same window. The default allowance is enough for every interactive use of this API the platform team has seen, and a caller that needs more than that is almost always doing batch work under an interactive credential. A refusal is not an outage, whatever the error class in a client library happens to call it. It is the platform declining to spend capacity that has already been promised to somebody else, and waiting is the only correct answer. The refusal isn’t a bug in the gateway either. Callers that retry at once are the largest single reason the cap is there at all.

## How to read a refusal

The refusal carries a Retry-After header. Its value is a whole number of seconds, and it is present on every refusal the gateway sends. Waiting that long and then continuing is the entire contract, and a caller that does exactly that will never need the rest of this note — which is the outcome it was written for, however unlikely that makes it to be read at all. The gateway keeps no memory of who backed off politely, so waiting longer than the header asks earns a caller no credit at all.

The body of the refusal is JSON, and it names what the gateway calls the “window” it counted in. It names the cap and the tier as well. None of those fields is a substitute for the header, and a caller that parses the body to compute its own wait is doing the same arithmetic twice. The body is there so that a human reading a log afterwards can see why the request was refused — nothing in it is meant for the retry loop.

## How to retry well

Four rules, given in the order they should be applied.

1. Honour the header, every time. The gateway has already done that arithmetic, with information the caller does not have, and it does the same on the 503 path. A wait derived on the client side is a guess about a counter it cannot see. There is no case at all where a guess is the better of the two. On the 503 path the same rule holds, even though the cause of the refusal is an entirely different one.

2. Retry only what is safe to retry. A 200 wants nothing, a 429 wants the stated wait, a 500 may be retried once that wait has passed, and a 503 is the overload path. The four cases are not interchangeable. A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive. Retry only what is safe to retry, which is a smaller set than the set of responses that aren’t a success. Avoid writing that loop.

3. Batch is different. A batch credential is allowed fifty times the default allowance, and it is measured over exactly the same window. The tier is set on the credential when it is issued and cannot be asked for per call. Nothing else about the two tiers differs in any way. The window, the header and the body are identical to the interactive case, so a client written for one tier needs no change at all to run against the other.

4. Log every refusal you see, and keep the log for at least a week. A caller that cannot say how often it was refused last week cannot argue for a larger cap, and nobody at the far end will assemble that argument on its behalf. The log line should carry the credential, the window and the wait. The counts are the whole of the argument, and without them a request is only a preference.

## Other refusals and their codes

Not all are caps. The gateway refuses a request for three reasons and only one of them is the one above. Two of the three have nothing to do with how much traffic a caller has sent in the window it is currently in. A credential can be suspended, a route can be closed while it is being repaired, and a request body over the 5 megabyte limit is refused before it has been read at all. None of those three clears itself by waiting for a stated number of seconds.

The distinction matters to a retry loop. A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service — and the log afterwards shows nothing at all except a long run of refusals. Reading the status code rather than the class it belongs to is what separates the two cases, and it costs one comparison. The log afterwards shows a long run of refusals and no successes at all, which reads like an outage and isn’t one — and the wasted budget is the caller’s own.

## Asking for an increase

A cap can be raised, and the number of caps raised without a measurement behind them is 0. A cap can be raised, but not on the strength of an assertion that the current one is too small. Bring a week of refusal counts, the shape of the traffic across the day, and the deadline that traffic is serving. The platform team looks at whether the load is smooth or bursty — a burst is cheaper to smooth than it is to serve at its peak. A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all, which is the outcome everyone prefers. That is the cheapest fix available to anybody, and it is available to almost everybody.

Requests reach the platform team through the usual channel. An answer takes two working days, and chasing it doesn’t make it take fewer. There is no expedited path and no exception list.