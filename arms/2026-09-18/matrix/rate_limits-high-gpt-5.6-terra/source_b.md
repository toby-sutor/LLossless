# What a client should do when the gateway says 429

Every credential has a cap of its own. When the cap is spent the gateway answers 429 at the edge, without troubling the service behind it. An earlier draft of this note argued for a client-side token bucket that mirrored the gateway’s own counters, and that section has been left out on purpose — two counters that disagree are worse than one counter that refuses, which is the whole reason the header exists.

Requests are counted against the credential rather than the connection, over a fixed window of 60 seconds whose start the gateway doesn’t disclose. There is nothing to be gained by opening more sockets. The count follows the credential wherever the caller happens to put it, including across hosts. A caller spread over many worker processes is throttled at the same point a single process would have been.

The default allowance is 100 requests in a window, which is enough for every interactive use of this API the platform team has seen, and a caller that needs more than that is almost always doing batch work under an interactive credential. The refusal isn’t an outage and it isn’t a bug in the gateway — it is capacity being held for a request somebody else has already been promised. Callers that retry immediately are most of the reason the cap is there.

## How to read a refusal

The header is called Retry-After. Its value is a whole number of seconds, and it is present on every refusal the gateway sends. Waiting that long and then continuing is the entire contract, and a caller that does exactly that will never need the rest of this note — which is the outcome it was written for, however unlikely that makes it to be read at all. Waiting longer than the header asks earns nothing, because nobody at this end is keeping score.

The response body is JSON and it repeats the cap, the window and the tier as plain fields. None of those fields is a substitute for the header, and a caller that parses the body in order to compute its own wait has written code whose only possible future is to disagree with the gateway it is talking to. The body is for the human reading the log afterwards.

## What the client does

There are four rules, and the order they are given in is the order to apply them.

1. Honour the header and don’t compute your own wait. The gateway has already done that arithmetic and it did it with information the caller cannot see. On the 503 path the same rule holds, even though the cause of the refusal is an entirely different one. Anything computed on the client side is a guess. That guess is not worth having.

2. Retry only what is safe to retry, which is a smaller set than the set of responses that aren’t a success. A 200 needs nothing, a 429 needs the stated wait, a 500 can be retried once that wait has passed, and a 503 means the platform itself is overloaded. A caller that folds all four into one branch will retry hardest during exactly the incident the cap was installed to survive. That is the behaviour this rule exists to prevent.

3. A batch credential is allowed 1000 requests in a window, which is 50 times the default and not a separate counting scheme. The window, the header and the body are identical to the interactive case, so a client written for one tier needs no change at all to run against the other. Nothing else about the batch tier differs from the default.

4. Log every refusal you see, and keep the log for at least a week. A caller that cannot say how often it was refused can’t make a case for a larger cap, and the platform team won’t assemble that case on its behalf. The counts are the whole of the argument, and without them a request is only a preference.

## Other kinds of refusal

The gateway refuses a request for three separate reasons, and only one of them is a cap. Two of the three have nothing to do with how much traffic a caller has sent in the window it is currently in. A credential can be suspended, a route can be closed while it is being repaired, and a request body over the 5 megabyte limit is refused before it has been read at all.

The difference matters more to a retry loop than it does to a reader. A loop retrying against a suspended credential burns its whole budget and reaches nothing. The log afterwards shows a long run of refusals and no successes at all, which reads like an outage and isn’t one — and the wasted budget is the caller’s own.

A caller that can move half its work to a quieter hour usually finds it doesn’t need a larger cap in the first place. That is the cheapest fix available to anybody, and it is available to almost everybody. A cap can be raised, but not on the strength of an assertion that the current one is too small. Bring the refusal counts for a full week, the shape of the traffic across the day, and the deadline the traffic exists to meet.

The team wants to know whether the load is smooth or bursty before it looks at the number at all. A burst is cheaper to smooth out than it is to serve at its peak. Requests go to the platform team through the usual channel.

There is no expedited path. An answer takes two working days, and chasing it doesn’t make it take fewer.
