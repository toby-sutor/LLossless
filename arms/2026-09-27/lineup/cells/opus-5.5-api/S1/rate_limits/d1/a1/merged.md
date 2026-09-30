# Rate limiting and the 429 contract for gateway clients

Every credential has a cap of its own. When that cap is spent the gateway answers 429 at the edge — without waking the service behind it — so the refusal costs the platform almost nothing and costs a caller that files it under transport error a great deal.

Requests are counted against the credential that presented them, never against a connection, over a fixed window of 60 seconds whose start the gateway doesn’t disclose. The count follows the credential wherever the caller puts it, including across hosts, so opening a second socket buys a caller nothing. A client spread across eight worker processes is throttled at exactly the point one process would have been — and pays for the extra file descriptors as well.

The default allowance is 100 requests in a window, which is enough for every interactive use of this API the platform team has seen, and a credential marked for batch work is allowed 1000 in the same window. A caller that needs more than the default is almost always doing batch work under an interactive credential.

A refusal is not an outage and not a bug in the gateway, whatever the error class in a client library happens to call it. It is the platform declining to spend capacity that has already been promised to somebody else, and waiting is the only correct answer. Callers that retry at once are most of the reason the cap is there at all — the largest single reason for it.

## How to read a refusal

Every refusal the gateway sends carries a Retry-After header. Its value is a whole number of seconds to wait. Waiting that long and then continuing is the whole of the contract — a client that does it needs nothing else from this document, which is the outcome the document is written for, even though it makes the rest unlikely ever to be read. The gateway keeps no memory of who backed off politely, so waiting longer than the header asks earns a caller no credit at all.

The body of the refusal is JSON, and it repeats the cap, the tier and what the gateway calls the “window” it counted in as plain fields. None of those fields is a substitute for the header, and a caller that parses the body to compute its own wait is doing the same arithmetic twice, in code whose only possible future is to disagree with the gateway it is talking to. The body is there so that a human reading a log afterwards can see why the request was refused — nothing in it is meant for the retry loop.

## How to retry well

Four rules, given in the order they should be applied.

1. Honour the header, every time, and don’t compute your own wait. The gateway has already done that arithmetic, with information the caller does not have, and the same rule holds on the 503 path, even though the cause of that refusal is an entirely different one. A wait derived on the client side is a guess about a counter it cannot see, and there is no case at all where a guess is the better of the two. Nor is a client-side token bucket that mirrors the gateway’s own counters any help: two counters that disagree are worse than one counter that refuses, which is the whole reason the header exists.

2. Retry only what is safe to retry, which is a smaller set than the set of responses that aren’t a success. A 200 needs nothing, a 429 needs the stated wait, a 500 can be retried once that wait has passed, and a 503 means the platform itself is overloaded. The four cases are not interchangeable. A client that folds every non-success into one branch will retry hardest during exactly the incident the cap was installed to survive. Avoid writing that loop; it is the behaviour this rule exists to prevent.

3. Batch is different. A batch credential is allowed fifty times the default allowance, measured over exactly the same window rather than under a separate counting scheme. The tier is set on the credential when it is issued and cannot be asked for per call. The window, the header and the body are identical to the interactive case, so a client written for one tier needs no change at all to run against the other; nothing else about the two tiers differs in any way.

4. Log every refusal seen, and keep the log for at least a week. The log line should carry the credential, the window and the wait. A caller that cannot say how often it was refused last week cannot argue for a larger cap, and nobody at the far end will assemble that argument on its behalf. The counts are the whole of the argument, and without them a request is only a preference.

## Other refusals and their codes

Not all are caps. The gateway refuses a request for three reasons and only one of them is the one above. Two of the three have nothing to do with how much traffic a caller has sent in the window it is currently in. A credential may be suspended, a route may be closed for maintenance while it is being repaired, or a body may exceed the 5 megabyte limit, in which case it is refused before it has been read at all. None of those three clears itself by waiting for a stated number of seconds.

The distinction matters more to a retry loop than to a reader. A loop that waits and retries against a suspended credential spends its whole budget — the caller’s own — without ever reaching the service, and the log afterwards shows nothing but a long run of refusals and no successes, which reads like an outage and isn’t one. Reading the status code rather than the class it belongs to is what separates the two cases, and it costs one comparison.

## Asking for an increase

A cap can be raised, but not on the strength of an assertion that the current one is too small: the number of caps raised without a measurement behind them is 0. Bring a week of refusal counts, the shape of the traffic across the day, and the deadline that traffic is serving. Before it looks at the number at all, the platform team looks at whether the load is smooth or bursty — a burst is cheaper to smooth than it is to serve at its peak. A caller that can move half its work to a quieter hour usually gets what it needs without any change to the cap at all, which is the outcome everyone prefers and the cheapest fix available, open to almost everybody.

Requests reach the platform team through the usual channel, and they are answered within two working days; chasing an answer doesn’t make it come sooner. There is no expedited path and no exception list.