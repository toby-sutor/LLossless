# Rate limiting and the 429 contract for gateway clients

Every credential has a cap of its own. When that cap is spent the gateway answers 429 at the edge — without waking the service behind it — so the refusal costs the platform almost nothing and costs a caller that files it under transport error a great deal. An earlier draft of this guidance argued for a client-side token bucket that mirrored the gateway's own counters; that approach is deliberately left out, because two counters that disagree are worse than one counter that refuses, which is the whole reason the header exists.

Requests are counted against the credential that presented them, never against a connection, over a fixed window of 60 seconds whose start the gateway does not disclose. The count follows the credential wherever the caller puts it, including across hosts. Opening a second socket therefore buys a caller nothing. A client spread across eight worker processes is throttled at exactly the point one process would have been — and pays for the extra file descriptors as well.

The default allowance is 100 requests in a window, which is enough for every interactive use of this API the platform team has seen; a caller that needs more is almost always doing batch work under an interactive credential. A credential marked for batch work is allowed 1000 in the same window. A refusal is not an outage and not a bug in the gateway, whatever the error class in a client library happens to call it. It is the platform declining to spend capacity that has already been promised to somebody else, and waiting is the only correct answer. Callers that retry at once are the largest single reason the cap is there at all.

## How to read a refusal

Every refusal carries a Retry-After header. Its value is a whole number of seconds to wait. Waiting that long and then continuing is the whole of the contract — a client that does it needs nothing else from this document, which is the outcome it was written for. The gateway keeps no memory of who backed off politely, so waiting longer than the header asks earns a caller no credit at all.

The body of the refusal is JSON, and it names, as plain fields, the cap, the tier and what the gateway calls the “window” it counted in. None of those fields is a substitute for the header. A caller that parses the body to compute its own wait is doing the same arithmetic twice, in code whose only possible future is to disagree with the gateway it is talking to. The body is there so that a human reading a log afterwards can see why the request was refused — nothing in it is meant for the retry loop.

## How to retry well

Four rules, given in the order they should be applied.

1. Honour the header, every time, and do not compute your own wait. The gateway has already done that arithmetic, with information the caller does not have, and it does the same on the 503 path, even though the cause of that refusal is entirely different. A wait derived on the client side is a guess about a counter it cannot see. There is no case at all where a guess is the better of the two.

2. Retry only what is safe to retry, which is a smaller set than the set of responses that are not a success. A 200 wants nothing, a 429 wants the stated wait, a 500 may be retried once that wait has passed, and a 503 is the overload path, meaning the platform itself is overloaded. The four cases are not interchangeable. A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive. Avoid writing that loop.

3. Batch is different. A batch credential is allowed 1000 requests in a window — fifty times the default allowance — and it is measured over exactly the same window; it is not a separate counting scheme. The tier is set on the credential when it is issued and cannot be asked for per call. The window, the header and the body are identical to the interactive case, so a client written for one tier needs no change to run against the other. Nothing else about the two tiers differs in any way.

4. Log every refusal seen, and keep the log for at least a week. A caller that cannot say how often it was refused last week cannot argue for a larger cap, and nobody at the far end, the platform team included, will assemble that argument on its behalf. The counts are the whole of the argument; without them a request is only a preference. The log line should carry the credential, the window and the wait.

## Other refusals and their codes

Not all refusals are caps. The gateway refuses a request for three reasons, and only one of them is the cap described above; two of the three have nothing to do with how much traffic a caller has sent in the window it is currently in. A credential may be suspended, a route may be closed for maintenance, or a body may exceed the 5 megabyte limit, in which case it is refused before it has been read at all. None of those three clears itself by waiting for a stated number of seconds.

The distinction matters more to a retry loop than to a reader. A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service, and the wasted budget is the caller's own. The log afterwards shows nothing but a long run of refusals and no successes, which reads like an outage and is not one. Reading the status code rather than the class it belongs to is what separates the two cases, and it costs one comparison.

## Asking for an increase

A cap can be raised, but not on the strength of an assertion that the current one is too small: the number of caps raised without a measurement behind them is 0. Bring a full week of refusal counts, the shape of the traffic across the day, and the deadline that traffic is serving. Before it looks at the number at all, the platform team looks at whether the load is smooth or bursty — a burst is cheaper to smooth than it is to serve at its peak. A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all, which is the outcome everyone prefers. It is the cheapest fix available to anybody, and it is available to almost everybody.

Requests reach the platform team through the usual channel, and they are answered within two working days; chasing an answer does not make it come sooner. There is no expedited path and no exception list.