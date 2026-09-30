## Verdict

**8 finding(s).** In the claims: 1 contradicted. In the structure: 4 undeclared absence, 3 undeclared rewording.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 35 |
| Claims extracted from `source_a.md` | 35 |
| Claims extracted from `source_b.md` | 35 |
| Forward — source claims accounted for in the merge | **69/70** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **35/35** |
| Forward — `source_b.md` claims accounted for | **34/35** |
| Reverse — merge claims found in a source | **35/35** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **105/105** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **B-017** -- the two documents disagree
  - `source_b.md:19` says: Rule 2 applies on the 503 path, even though the cause of the refusal is an entirely different one.
  - `merged.md` says: "1. Honour the header, every time, and don't compute a wait of your own.\n   The gateway has already done that arithmetic, with information the caller cannot see, and it holds on the 503 path too, even though the cause of that refusal is an entirely different one." (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The 503 statement is attached to rule 1, not rule 2, contradicting the claim's attribution.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 35 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 35 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The gateway answers 429 at the edge when a credential's cap is spent. | 3 | carried | 'Every credential has a cap. When that cap is spent the gateway answers 429 at the edge' in `merged.md` -- Directly stated. |
| 2 | The gateway answers 429 without waking the service behind it. | 3 | carried | 'the gateway answers 429 at the edge — without waking the service behind it' in `merged.md` -- Directly stated. |
| 3 | Requests are counted against the credential that presented them. | 5 | carried | 'Requests are counted against the credential that presented them rather than the connection' in `merged.md` -- Directly stated. |
| 4 | Requests are counted over a fixed window of 60 seconds. | 5 | carried | "over a fixed window of 60 seconds whose start the gateway doesn't disclose" in `merged.md` -- Directly stated. |
| 5 | Requests are never counted against a connection. | 5 | carried | 'Requests are counted against the credential that presented them rather than the connection' in `merged.md` -- States counting is against credential rather than connection, implying never against connection. |
| 6 | A client spread across eight worker processes is throttled at exactly the point one process would have been. | 5 | carried | 'a client spread across eight worker processes is throttled at exactly the point one process would have been' in `merged.md` -- Directly stated. |
| 7 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- Directly stated. |
| 8 | A credential marked for batch work is allowed 1000 in the same window. | 7 | carried | 'a credential marked for batch work is allowed 1000 in the same window' in `merged.md` -- Directly stated. |
| 9 | The refusal carries a Retry-After header. | 11 | carried | 'The refusal carries a header called Retry-After.' in `merged.md` -- Directly stated. |
| 10 | The Retry-After header's value is a whole number of seconds to wait. | 11 | carried | 'Its value is a whole number of seconds to wait' in `merged.md` -- Directly stated. |
| 11 | The gateway keeps no memory of who backed off politely. | 11 | carried | 'The gateway keeps no memory of who backed off politely' in `merged.md` -- Directly stated. |
| 12 | The body of the refusal is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- Directly stated. |
| 13 | The body of the refusal names what the gateway calls the "window" it counted in. | 13 | carried | 'it names the window the gateway counted in' in `merged.md` -- Directly stated. |
| 14 | The body of the refusal names the cap. | 13 | carried | 'along with the cap and the tier' in `merged.md` -- Directly stated. |
| 15 | The body of the refusal names the tier. | 13 | carried | 'along with the cap and the tier' in `merged.md` -- Directly stated. |
| 16 | The gateway does the same Retry-After arithmetic on the 503 path. | 19 | carried | 'it holds on the 503 path too, even though the cause of that refusal is an entirely different one' in `merged.md` -- Directly stated. |
| 17 | A 200 response wants nothing retried. | 21 | carried | 'A 200 wants nothing' in `merged.md` -- Directly stated. |
| 18 | A 429 response wants the stated wait. | 21 | carried | 'a 429 wants the stated wait' in `merged.md` -- Directly stated. |
| 19 | A 500 response may be retried once that wait has passed. | 21 | carried | 'a 500 may be retried once that wait has passed' in `merged.md` -- Directly stated. |
| 20 | A 503 response is the overload path. | 21 | carried | 'a 503 is the overload path' in `merged.md` -- Directly stated. |
| 21 | A batch credential is allowed fifty times the default allowance. | 23 | carried | 'A batch credential is allowed fifty times the default allowance' in `merged.md` -- Directly stated. |
| 22 | The batch credential allowance is measured over exactly the same window as the default allowance. | 23 | carried | 'it is measured over exactly the same window' in `merged.md` -- Directly stated. |
| 23 | The tier is set on the credential when it is issued. | 23 | carried | 'The tier is set on the credential when it is issued' in `merged.md` -- Directly stated. |
| 24 | The tier cannot be asked for per call. | 23 | carried | 'and cannot be asked for per call' in `merged.md` -- Directly stated. |
| 25 | The gateway refuses a request for three reasons. | 29 | carried | 'The gateway refuses a request for three reasons' in `merged.md` -- Directly stated. |
| 26 | Only one of the gateway's three refusal reasons is the rate-limiting one. | 29 | carried | 'and only one of them is the one above' in `merged.md` -- Directly stated. |
| 27 | A credential may be suspended. | 29 | carried | 'A credential may be suspended' in `merged.md` -- Directly stated. |
| 28 | A route may be closed for maintenance. | 29 | carried | 'a route may be closed for maintenance' in `merged.md` -- Directly stated. |
| 29 | A body may exceed the 5 megabyte limit. | 29 | carried | 'a body may exceed the 5 megabyte limit and be refused before it has even been read' in `merged.md` -- Directly stated. |
| 30 | None of the three non-cap refusal reasons clears itself by waiting for a stated number of seconds. | 29 | carried | 'None of those three clears itself by waiting for a stated number of seconds.' in `merged.md` -- Directly stated. |
| 31 | The number of caps raised without a measurement behind them is 0. | 35 | carried | 'the number of caps raised without a measurement behind them is 0' in `merged.md` -- Directly stated. |
| 32 | Requests for a cap increase reach the platform team through the usual channel. | 37 | carried | 'Requests reach the platform team through the usual channel' in `merged.md` -- Directly stated. |
| 33 | Requests for a cap increase are answered within two working days. | 37 | carried | 'they are answered within two working days' in `merged.md` -- Directly stated. |
| 34 | There is no expedited path for requesting a cap increase. | 37 | carried | 'There is no expedited path' in `merged.md` -- Directly stated. |
| 35 | There is no exception list for requesting a cap increase. | 37 | carried | 'and no exception list' in `merged.md` -- Directly stated. |

### `source_b.md` -- 35 claim(s): 0 dropped, 1 contradicted, 0 carried in part, 34 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 17 | Rule 2 applies on the 503 path, even though the cause of the refusal is an entirely different one. | 19 | contradicted | "1. Honour the header, every time, and don't compute a wait of your own.\n   The gateway has already done that arithmetic, with information the caller cannot see, and it holds on the 503 path too, even though the cause of that refusal is an entirely different one." in `merged.md` -- The 503 statement is attached to rule 1, not rule 2, contradicting the claim's attribution. |
| 1 | The gateway answers 429 at the edge, without troubling the service behind it. | 3 | carried | 'the gateway answers 429 at the edge — without waking the service behind it' in `merged.md` -- Directly stated. |
| 2 | An earlier draft of this note argued for a client-side token bucket that mirrored the gateway's own counters. | 3 | carried | "An earlier draft of this note argued for a client-side token bucket that mirrored the gateway's own counters" in `merged.md` -- Directly stated. |
| 3 | That section arguing for a client-side token bucket has been left out on purpose. | 3 | carried | 'that section has been left out on purpose' in `merged.md` -- Directly stated. |
| 4 | Requests are counted against the credential rather than the connection. | 5 | carried | 'Requests are counted against the credential that presented them rather than the connection' in `merged.md` -- Directly stated. |
| 5 | Requests are counted over a fixed window of 60 seconds whose start the gateway doesn't disclose. | 5 | carried | "over a fixed window of 60 seconds whose start the gateway doesn't disclose" in `merged.md` -- Directly stated. |
| 6 | There is nothing to be gained by opening more sockets. | 5 | carried | 'Opening a second socket therefore buys a caller nothing.' in `merged.md` -- Directly stated. |
| 7 | The count follows the credential wherever the caller happens to put it, including across hosts. | 5 | carried | 'The count follows the credential wherever the caller puts it, including across hosts' in `merged.md` -- Directly stated. |
| 8 | A caller spread over many worker processes is throttled at the same point a single process would have been. | 5 | carried | 'a client spread across eight worker processes is throttled at exactly the point one process would have been' in `merged.md` -- Directly stated. |
| 9 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- Directly stated. |
| 10 | The default allowance of 100 requests in a window is enough for every interactive use of this API the platform team has seen. | 7 | carried | 'enough for every interactive use of this API the platform team has seen' in `merged.md` -- Directly stated. |
| 11 | The header is called Retry-After. | 11 | carried | 'The refusal carries a header called Retry-After.' in `merged.md` -- Directly stated. |
| 12 | The Retry-After header's value is a whole number of seconds. | 11 | carried | 'Its value is a whole number of seconds to wait' in `merged.md` -- Directly stated. |
| 13 | The Retry-After header is present on every refusal the gateway sends. | 11 | carried | 'it is present on every refusal the gateway sends' in `merged.md` -- Directly stated. |
| 14 | The response body is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- Directly stated. |
| 15 | The response body repeats the cap, the window and the tier as plain fields. | 13 | carried | 'it names the window the gateway counted in, along with the cap and the tier' in `merged.md` -- Directly stated. |
| 16 | There are four rules. | 17 | carried | 'Four rules, given in the order they should be applied.' in `merged.md` -- Directly stated. |
| 18 | A 200 needs nothing. | 21 | carried | 'A 200 wants nothing' in `merged.md` -- Directly stated. |
| 19 | A 429 needs the stated wait. | 21 | carried | 'a 429 wants the stated wait' in `merged.md` -- Directly stated. |
| 20 | A 500 can be retried once that wait has passed. | 21 | carried | 'a 500 may be retried once that wait has passed' in `merged.md` -- Directly stated. |
| 21 | A 503 means the platform itself is overloaded. | 21 | carried | 'a 503 is the overload path' in `merged.md` -- Overload path implies the platform is overloaded. |
| 22 | A batch credential is allowed 1000 requests in a window. | 23 | carried | 'a credential marked for batch work is allowed 1000 in the same window' in `merged.md` -- Directly stated. |
| 23 | 1000 requests in a window is 50 times the default. | 23 | carried | 'A batch credential is allowed fifty times the default allowance' in `merged.md` -- 1000 is fifty times the default of 100 as stated. |
| 24 | 1000 requests in a window is not a separate counting scheme. | 23 | carried | 'The window, the header and the body are identical to the interactive case, so a client written for one tier needs no change to run against the other.' in `merged.md` -- Implies the same counting scheme applies to batch. |
| 25 | The window, the header and the body are identical between the batch tier and the interactive case. | 23 | carried | 'The window, the header and the body are identical to the interactive case' in `merged.md` -- Directly stated. |
| 26 | Nothing else about the batch tier differs from the default. | 23 | carried | 'Nothing else about the two tiers differs in any way.' in `merged.md` -- Directly stated. |
| 27 | Rule 4 states to log every refusal you see. | 25 | carried | 'Log every refusal seen, and keep the log for at least a week.' in `merged.md` -- Directly stated. |
| 28 | Rule 4 states to keep the log for at least a week. | 25 | carried | 'keep the log for at least a week' in `merged.md` -- Directly stated. |
| 29 | The gateway refuses a request for three separate reasons. | 29 | carried | 'The gateway refuses a request for three reasons' in `merged.md` -- Directly stated. |
| 30 | Only one of the three reasons for refusal is a cap. | 29 | carried | 'and only one of them is the one above' in `merged.md` -- Directly stated. |
| 31 | A credential can be suspended. | 29 | carried | 'A credential may be suspended' in `merged.md` -- Directly stated. |
| 32 | A route can be closed while it is being repaired. | 29 | carried | 'a route may be closed for maintenance' in `merged.md` -- Directly stated. |
| 33 | A request body over the 5 megabyte limit is refused before it has been read at all. | 29 | carried | 'a body may exceed the 5 megabyte limit and be refused before it has even been read' in `merged.md` -- Directly stated. |
| 34 | A loop retrying against a suspended credential burns its whole budget and reaches nothing. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `merged.md` -- Directly stated. |
| 35 | An answer from the platform team takes two working days. | 37 | carried | 'they are answered within two working days' in `merged.md` -- Directly stated. |

### `merged.md` -- 35 claim(s): 0 invented, 0 contradicted, 0 supported in part, 35 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | The gateway answers 429 at the edge without waking the service behind it. | supported | `source_a.md` | 'the gateway answers 429 at the edge — without waking the service behind it' in `source_a.md` -- Directly stated in source_a. |
| 2 | Requests are counted against the credential that presented them rather than the connection. | supported | `source_b.md` | 'Requests are counted against the credential rather than the connection' in `source_b.md` -- Directly stated in source_b. |
| 3 | Requests are counted over a fixed window of 60 seconds. | supported | `source_a.md` | 'over a fixed window of 60 seconds' in `source_a.md` -- Directly stated in source_a. |
| 4 | The gateway does not disclose the start of the 60 second window. | supported | `source_b.md` | 'over a fixed window of 60 seconds whose start the gateway doesn’t disclose' in `source_b.md` -- Directly stated in source_b. |
| 5 | The count follows the credential wherever the caller puts it, including across hosts. | supported | `source_b.md` | 'The count follows the credential wherever the caller happens to put it, including across hosts.' in `source_b.md` -- Directly stated in source_b. |
| 6 | The default allowance is 100 requests in a window. | supported | `source_a.md` | 'The default allowance is 100 requests in a window' in `source_a.md` -- Directly stated in source_a. |
| 7 | A credential marked for batch work is allowed 1000 requests in the same window. | supported | `source_a.md` | 'a credential marked for batch work is allowed 1000 in the same window' in `source_a.md` -- Directly stated in source_a. |
| 8 | The refusal carries a header called Retry-After. | supported | `source_a.md` | 'The refusal carries a Retry-After header.' in `source_a.md` -- Directly stated in source_a. |
| 9 | The Retry-After header's value is a whole number of seconds to wait. | supported | `source_a.md` | 'Its value is a whole number of seconds to wait.' in `source_a.md` -- Directly stated in source_a. |
| 10 | The Retry-After header is present on every refusal the gateway sends. | supported | `source_b.md` | 'it is present on every refusal the gateway sends' in `source_b.md` -- Directly stated in source_b. |
| 11 | The gateway keeps no memory of who backed off politely. | supported | `source_a.md` | 'The gateway keeps no memory of who backed off politely' in `source_a.md` -- Directly stated in source_a. |
| 12 | The body of the refusal is JSON. | supported | `source_a.md` | 'The body of the refusal is JSON' in `source_a.md` -- Directly stated in source_a. |
| 13 | The body of the refusal names the window the gateway counted in, along with the cap and the tier. | supported | `source_a.md` | 'It names the cap and the tier as well.' in `source_a.md` -- Combined with the preceding sentence about the window, source_a names cap, tier, and window. |
| 14 | The gateway's own wait computation on the 429 path holds on the 503 path too. | supported | `source_a.md` | 'and it does the same on the 503 path' in `source_a.md` -- Directly stated in source_a that the gateway's arithmetic applies on the 503 path too. |
| 15 | The cause of a 503 refusal is an entirely different cause from a 429 refusal. | supported | `source_b.md` | 'On the 503 path the same rule holds, even though the cause of the refusal is an entirely different one.' in `source_b.md` -- Directly stated in source_b. |
| 16 | A 200 response wants nothing retried. | supported | `source_a.md` | 'A 200 wants nothing' in `source_a.md` -- Directly stated in source_a. |
| 17 | A 429 response wants the stated wait. | supported | `source_a.md` | 'a 429 wants the stated wait' in `source_a.md` -- Directly stated in source_a. |
| 18 | A 500 response may be retried once its wait has passed. | supported | `source_a.md` | 'a 500 may be retried once that wait has passed' in `source_a.md` -- Directly stated in source_a. |
| 19 | A 503 response is the overload path. | supported | `source_a.md` | 'a 503 is the overload path' in `source_a.md` -- Directly stated in source_a. |
| 20 | A batch credential is allowed fifty times the default allowance. | supported | `source_a.md` | 'A batch credential is allowed fifty times the default allowance' in `source_a.md` -- Directly stated in source_a. |
| 21 | A batch credential's allowance is measured over exactly the same window as the default allowance. | supported | `source_a.md` | 'it is measured over exactly the same window' in `source_a.md` -- Directly stated in source_a. |
| 22 | The tier is set on the credential when it is issued. | supported | `source_a.md` | 'The tier is set on the credential when it is issued' in `source_a.md` -- Directly stated in source_a. |
| 23 | The tier cannot be asked for per call. | supported | `source_a.md` | 'and cannot be asked for per call' in `source_a.md` -- Directly stated in source_a. |
| 24 | The log line should carry the credential, the window and the wait. | supported | `source_a.md` | 'The log line should carry the credential, the window and the wait.' in `source_a.md` -- Directly stated in source_a. |
| 25 | The gateway refuses a request for three reasons. | supported | `source_a.md` | 'The gateway refuses a request for three reasons' in `source_a.md` -- Directly stated in source_a. |
| 26 | Only one of the gateway's three refusal reasons is the rate-cap reason. | supported | `source_a.md` | 'and only one of them is the one above' in `source_a.md` -- Directly stated in source_a. |
| 27 | A credential may be suspended. | supported | `source_a.md` | 'A credential may be suspended' in `source_a.md` -- Directly stated in source_a. |
| 28 | A route may be closed for maintenance. | supported | `source_a.md` | 'a route may be closed for maintenance' in `source_a.md` -- Directly stated in source_a. |
| 29 | A body may exceed the 5 megabyte limit and be refused before it has even been read. | supported | `source_b.md` | 'a request body over the 5 megabyte limit is refused before it has been read at all' in `source_b.md` -- Directly stated in source_b. |
| 30 | None of the three non-cap refusal reasons clears itself by waiting for a stated number of seconds. | supported | `source_a.md` | 'None of those three clears itself by waiting for a stated number of seconds.' in `source_a.md` -- Directly stated in source_a referring to the three non-cap reasons listed just before. |
| 31 | The number of caps raised without a measurement behind them is 0. | supported | `source_a.md` | 'the number of caps raised without a measurement behind them is 0' in `source_a.md` -- Directly stated in source_a. |
| 32 | Requests for a cap increase reach the platform team through the usual channel. | supported | `source_a.md` | 'Requests reach the platform team through the usual channel' in `source_a.md` -- Directly stated in source_a. |
| 33 | Requests for a cap increase are answered within two working days. | supported | `source_a.md` | 'they are answered within two working days' in `source_a.md` -- Directly stated in source_a. |
| 34 | There is no expedited path for requesting a cap increase. | supported | `source_a.md` | 'There is no expedited path' in `source_a.md` -- Directly stated in source_a. |
| 35 | There is no exception list for requesting a cap increase. | supported | `source_a.md` | 'and no exception list' in `source_a.md` -- Directly stated in source_a. |

## Structure

**9** mechanical check(s) over **104** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **35** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **70**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 21 run(s) over 49 attributed segment(s) — sources interleaved. 6 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Absent and undeclared — in a source, not in the merge, and no record explains it

- `a8` (`source_a.md`) — 'A refusal is not an outage, whatever the error class in a client library happens to call it.' is not in the merge and no disposition record explains it (nearest merge segment m9 at 0.57)

  ```text
  In the source: A refusal is not an outage, whatever the error class in a client library happens to call it.
  ```
- `a16` (`source_a.md`) — 'The body of the refusal is JSON, and it names what the gateway calls the “window” it counted in.' is not in the merge and no disposition record explains it (nearest merge segment m16 at 0.68)

  ```text
  In the source: The body of the refusal is JSON, and it names what the gateway calls the “window” it counted in.
  ```
- `a17` (`source_a.md`) — 'It names the cap and the tier as well.' is not in the merge and no disposition record explains it (nearest merge segment m39 at 0.50)

  ```text
  In the source: It names the cap and the tier as well.
  ```
- `a40` (`source_a.md`) — 'The gateway refuses a request for three reasons and only one of them is the one above.' is not in the merge and no disposition record explains it (nearest merge segment m41 at 0.61)

  ```text
  In the source: The gateway refuses a request for three reasons and only one of them is the one above.
  ```

### Reworded and undeclared — in the merge in altered wording, and no record explains it. At off this also covers layout: a segment whose source line breaks the merge ran together is altered and undeclared, and 380 reuses this kind rather than moving FINDING_KINDS off 12

- `a12` (`source_a.md`) — 'The refusal carries a Retry-After header.' is reworded in the merge and no disposition record explains it (nearest merge segment m12 at 0.76)

  ```text
  In the source: The refusal carries a Retry-After header.
  In the merge:  The refusal carries a header called Retry-After.
  ```
- `a39` (`source_a.md`) — 'Not all are caps.' is reworded in the merge and no disposition record explains it (nearest merge segment m40 at 0.79)

  ```text
  In the source: Not all are caps.
  In the merge:  Not all refusals are caps.
  ```
- `b4` (`source_b.md`) — 'An earlier draft of this note argued for a client-side token bucket that mirrored the gateway’s own counters, and that section has been left out on purpose — two counters that disagree are worse than one counter that refuses, which is the whole reason the header exists.' is reworded in the merge and no disposition record explains it (nearest merge segment m4 at 0.77)

  ```text
  In the source: An earlier draft of this note argued for a client-side token bucket that mirrored the gateway’s own counters, and that section has been left out on purpose — two counters that disagree are worse than one counter that refuses, which is the whole reason the header exists.
  In the merge:  An earlier draft of this note argued for a client-side token bucket that mirrored the gateway's own counters; that section has been left out on purpose, because two counters that disagree are worse than one counter that refuses, which is the whole reason the header exists.
  ```

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **68** departure(s) from its sources. Checking them confirms 30, rejects 12, and leaves 26 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 104 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | Base title chosen instead. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Rate limiting and the 429 contract for gateway clients' and says so (no claim traced to it) |
| `b2` | duplicate | Same fact as a2, a's wording kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'duplicate' is what happened to it (no claim traced to it) |
| `b3` | duplicate | Same fact as a3, a's fuller wording kept. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-001`) |
| `a4` | reconciled | Combined with b5's undisclosed-start detail. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-003`, `A-004`, `A-005`) |
| `b5` | reconciled | Its extra detail joined with a4's counting rule. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-004`, `B-005`) |
| `b6` | duplicate | Same fact as a5, a's wording kept. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-006`) |
| `a6` | reconciled | Combined with b7's cross-host detail. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-006`) |
| `b7` | reconciled | Cross-host detail folded into a6's example. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-007`) |
| `b8` | duplicate | Same fact as a6, restated in combined sentence. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-008`) |
| `a7` | reconciled | Combined with b9's sufficiency and misuse detail. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-007`, `A-008`) |
| `b9` | reconciled | Its added detail joined with a7's allowance figures. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-009`, `B-010`) |
| `b10` | duplicate | Same fact as a8/a9, a's wording kept. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b11` | duplicate | Same fact as a10, a's wording kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'duplicate' is what happened to it (no claim traced to it) |
| `b12` | duplicate | Identical heading text to a11. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b13` | duplicate | Same fact as a12, wording combined into one sentence. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-011`) |
| `a13` | reconciled | Combined with b14's every-refusal detail. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-010`) |
| `b14` | reconciled | Its added detail joined with a13's header-value rule. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-012`, `B-013`) |
| `a14` | reconciled | Combined with b15's authorial-intent clause. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b15` | reconciled | Its added clause joined with a14's contract statement. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b16` | duplicate | Same fact as a15, a's wording kept. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b17` | duplicate | Same facts as a16/a17, combined into one sentence. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-014`, `B-015`) |
| `a18` | reconciled | Combined with b18's future-disagreement framing. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b18` | reconciled | Its framing joined with a18's redundancy point. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b19` | duplicate | Same fact as a19, a's wording kept. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b20` | superseded | Base heading chosen instead. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b21` | duplicate | Same fact as a21, a's wording kept. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-016`) |
| `a22` | reconciled | Combined with b22's compute-your-own-wait clause. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b22` | reconciled | Its clause joined into a22's rule heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `a23` | reconciled | Combined with b24's 503-cause clause. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-016`) |
| `b24` | reconciled | Its 503-cause clause joined with a23's rule. | **rejected** | declared 'reconciled', which predicts SUPPORTED; B-017 came back CONTRADICTED (`B-017`) |
| `b23` | duplicate | Same fact as a23, restated in combined sentence. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b25` | duplicate | Same fact as a24, a's wording kept. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b26` | duplicate | Same fact as a25, a's wording kept. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `a26` | reconciled | Combined with b27's smaller-set clarification. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b27` | reconciled | Its clarification joined into a26's rule heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b28` | duplicate | Same fact as a27, a's wording kept. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-018`, `B-019`, `B-020`, `B-021`) |
| `b29` | duplicate | Same fact as a29, a's wording kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'duplicate' is what happened to it (no claim traced to it) |
| `b30` | duplicate | Same fact as a30, a's wording kept. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `a32` | duplicate | Same fact as b31, a's wording kept. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`A-021`, `A-022`) |
| `b31` | superseded | Same fact as a32, a's wording kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-022`, `B-023`, `B-024`) |
| `b32` | reworded | Unique detail carried in condensed form. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-025`) |
| `b33` | duplicate | Same fact as a34, a's wording kept. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-026`) |
| `a35` | reconciled | Combined with b34's keep-for-a-week detail. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b34` | reconciled | Its retention detail joined with a35's rule heading. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-027`, `B-028`) |
| `b35` | duplicate | Same fact as a36, a's wording kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'duplicate' is what happened to it (no claim traced to it) |
| `b36` | reworded | Unique closing point on rule 4 carried as new sentence. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b37` | superseded | Base heading chosen instead. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b38` | duplicate | Same fact as a39/a40, a's wording kept. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-029`, `B-030`) |
| `b39` | reworded | Unique elaboration carried as added clause. | **rejected** | declared 'reworded', and its text is in the merge (no claim traced to it) |
| `a41` | reconciled | Combined with b40's before-it-is-read detail. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-027`, `A-028`, `A-029`) |
| `b40` | reconciled | Its extra detail joined with a41's list of reasons. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-031`, `B-032`, `B-033`) |
| `b41` | duplicate | Same fact as a43, a's wording kept. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b42` | duplicate | Same fact as a44, restated in combined sentence. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-034`) |
| `a44` | reconciled | Combined with b43's outage-framing and cost detail. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b43` | reconciled | Its framing joined with a44's description. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `a47` | reconciled | Combined with b46's assertion-not-enough clause. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-031`) |
| `b46` | reconciled | Its clause joined with a47's numeric fact. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b47` | duplicate | Same fact as a48, a's wording kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'duplicate' is what happened to it (no claim traced to it) |
| `a49` | reconciled | Combined with b48's before-the-number detail. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b48` | reconciled | Its ordering detail joined with a49's statement. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b49` | duplicate | Same fact as a49, restated in combined sentence. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b44` | duplicate | Same fact as a50, a's wording kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'duplicate' is what happened to it (no claim traced to it) |
| `a50` | reconciled | Combined with b45's cheapest-fix framing. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b45` | reconciled | Its framing joined with a50's outcome. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b50` | duplicate | Same fact as a51, a's wording kept. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `a51` | reconciled | Combined with b52's chasing-doesn't-help detail. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-032`, `A-033`) |
| `b52` | reconciled | Its added detail joined with a51's turnaround statement. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-035`) |
| `b51` | duplicate | Same fact as a52, a's wording kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'duplicate' is what happened to it (no claim traced to it) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | d320da0eb7ed (command) -- lineup sonnet-5-sub |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | claude-sonnet-5 -> claude-sonnet-5 |
| Model (decompose) | claude-sonnet-5 -> claude-sonnet-5 |
| Model (verify) | claude-sonnet-5 -> claude-sonnet-5 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile subscription, effort decompose=medium, merge=medium, verify=medium |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 6 live, 0 cached, 0 replayed |
| Tokens | unknown (6 call(s) reported no usage) |
| Cost | unmeasured (6 call(s) reported no tokens, so no figure can be derived) |
| Schema repairs | 0 |
| Isolation | decompose, merge, verify: safe mode, no tools |
| Errors | 0 |
| Duration | 266.5s |
| Generated | 2026-09-27T17:25:16+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup sonnet-5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
