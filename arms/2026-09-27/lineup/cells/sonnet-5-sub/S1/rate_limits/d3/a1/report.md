## Verdict

**2 finding(s).** In the structure: 1 undeclared rewording, 1 verbatim violation.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 45 |
| Claims extracted from `source_a.md` | 35 |
| Claims extracted from `source_b.md` | 39 |
| Forward — source claims accounted for in the merge | **74/74** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **35/35** |
| Forward — `source_b.md` claims accounted for | **39/39** |
| Reverse — merge claims found in a source | **45/45** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **119/119** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

None in the claims. The 2 finding(s) this run reports are structural and are listed under `## Structure` below.

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
| 1 | The gateway answers 429 at the edge when a credential's cap is spent. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge' in `merged.md` -- Directly stated. |
| 2 | The gateway answers 429 without waking the service behind it. | 3 | carried | 'without waking the service behind it' in `merged.md` -- Directly stated. |
| 3 | Requests are counted against the credential that presented them. | 5 | carried | 'Requests are counted against the credential that presented them' in `merged.md` -- Directly stated. |
| 4 | Requests are counted over a fixed window of 60 seconds. | 5 | carried | 'over a fixed window of 60 seconds' in `merged.md` -- Directly stated. |
| 5 | Requests are never counted against a connection. | 5 | carried | 'and never against a connection' in `merged.md` -- Directly stated. |
| 6 | A client spread across eight worker processes is throttled at exactly the point one process would have been. | 5 | carried | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `merged.md` -- Directly stated. |
| 7 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- Directly stated. |
| 8 | A credential marked for batch work is allowed 1000 requests in the same window. | 7 | carried | 'a credential marked for batch work is allowed 1000 requests in the same window' in `merged.md` -- Directly stated. |
| 9 | The refusal carries a Retry-After header. | 11 | carried | 'The refusal carries a Retry-After header' in `merged.md` -- Directly stated. |
| 10 | The Retry-After header's value is a whole number of seconds to wait. | 11 | carried | 'Its value is a whole number of seconds to wait' in `merged.md` -- Directly stated. |
| 11 | The gateway keeps no memory of who backed off politely. | 11 | carried | 'The gateway keeps no memory of who backed off politely' in `merged.md` -- Directly stated. |
| 12 | The body of the refusal is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- Directly stated. |
| 13 | The body of the refusal names what the gateway calls the "window" it counted in. | 13 | carried | 'it names what the gateway calls the "window" it counted in' in `merged.md` -- Directly stated. |
| 14 | The body of the refusal names the cap. | 13 | carried | 'It names the cap and the tier as well' in `merged.md` -- Directly stated. |
| 15 | The body of the refusal names the tier. | 13 | carried | 'It names the cap and the tier as well' in `merged.md` -- Directly stated. |
| 16 | The gateway does the same Retry-After arithmetic on the 503 path. | 19 | carried | 'it does the same on the 503 path' in `merged.md` -- Directly stated. |
| 17 | A 200 response wants nothing retried. | 21 | carried | 'A 200 wants nothing' in `merged.md` -- Directly stated. |
| 18 | A 429 response wants the stated wait. | 21 | carried | 'a 429 wants the stated wait' in `merged.md` -- Directly stated. |
| 19 | A 500 response may be retried once that wait has passed. | 21 | carried | 'a 500 may be retried once that wait has passed' in `merged.md` -- Directly stated. |
| 20 | A 503 response is the overload path. | 21 | carried | 'a 503 is the overload path' in `merged.md` -- Directly stated. |
| 21 | A batch credential is allowed fifty times the default allowance. | 23 | carried | 'fifty times the default allowance' in `merged.md` -- Directly stated. |
| 22 | A batch credential's allowance is measured over exactly the same window as the default allowance. | 23 | carried | 'measured over exactly the same window, not as a separate counting scheme' in `merged.md` -- Directly stated. |
| 23 | The tier is set on the credential when it is issued. | 23 | carried | 'The tier is set on the credential when it is issued' in `merged.md` -- Directly stated. |
| 24 | The tier cannot be asked for per call. | 23 | carried | 'and cannot be asked for per call' in `merged.md` -- Directly stated. |
| 25 | The gateway refuses a request for three reasons. | 29 | carried | 'The gateway refuses a request for three reasons' in `merged.md` -- Directly stated. |
| 26 | Only one of the three reasons the gateway refuses a request is the rate-limit cap reason. | 29 | carried | 'and only one of them is the one above' in `merged.md` -- Directly stated. |
| 27 | A credential may be suspended. | 29 | carried | 'A credential may be suspended' in `merged.md` -- Directly stated. |
| 28 | A route may be closed for maintenance. | 29 | carried | 'a route may be closed for maintenance' in `merged.md` -- Directly stated. |
| 29 | A body may exceed the 5 megabyte limit. | 29 | carried | 'a body may exceed the 5 megabyte limit and be refused before it has been read at all' in `merged.md` -- Directly stated. |
| 30 | None of the three non-cap refusal reasons clears itself by waiting for a stated number of seconds. | 29 | carried | 'None of those three clears itself by waiting for a stated number of seconds' in `merged.md` -- Directly stated. |
| 31 | The number of caps raised without a measurement behind them is 0. | 35 | carried | 'the number of caps raised without a measurement behind them is 0' in `merged.md` -- Directly stated. |
| 32 | Requests for a cap increase reach the platform team through the usual channel. | 37 | carried | 'Requests reach the platform team through the usual channel' in `merged.md` -- Directly stated. |
| 33 | Requests for a cap increase are answered within two working days. | 37 | carried | 'they are answered within two working days' in `merged.md` -- Directly stated. |
| 34 | There is no expedited path for requesting a cap increase. | 37 | carried | 'There is no expedited path' in `merged.md` -- Directly stated. |
| 35 | There is no exception list for requesting a cap increase. | 37 | carried | 'and no exception list' in `merged.md` -- Directly stated. |

### `source_b.md` -- 39 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 39 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The gateway answers 429 at the edge when the cap is spent. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge' in `merged.md` -- Directly stated. |
| 2 | The gateway does not trouble the service behind it when answering 429. | 3 | carried | 'without waking the service behind it' in `merged.md` -- Directly stated. |
| 3 | An earlier draft of this note argued for a client-side token bucket that mirrored the gateway's own counters. | 3 | carried | "An earlier draft of this note argued for a client-side token bucket that mirrored the gateway's own counters" in `merged.md` -- Directly stated. |
| 4 | That section arguing for a client-side token bucket has been left out on purpose. | 3 | carried | 'that section was left out on purpose' in `merged.md` -- Directly stated. |
| 5 | Requests are counted against the credential rather than the connection. | 5 | carried | "Requests are counted against the credential that presented them, over a fixed window of 60 seconds whose start the gateway doesn't disclose, and never against a connection" in `merged.md` -- Directly stated. |
| 6 | Requests are counted over a fixed window of 60 seconds. | 5 | carried | 'over a fixed window of 60 seconds' in `merged.md` -- Directly stated. |
| 7 | The gateway does not disclose the start of the 60 second window. | 5 | carried | "whose start the gateway doesn't disclose" in `merged.md` -- Directly stated. |
| 8 | The count follows the credential wherever the caller happens to put it, including across hosts. | 5 | carried | 'since the count follows the credential wherever it goes, including across hosts' in `merged.md` -- Directly stated. |
| 9 | A caller spread over many worker processes is throttled at the same point a single process would have been. | 5 | carried | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `merged.md` -- Directly stated. |
| 10 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- Directly stated. |
| 11 | The header is called Retry-After. | 11 | carried | 'The refusal carries a Retry-After header' in `merged.md` -- Directly stated. |
| 12 | The Retry-After header's value is a whole number of seconds. | 11 | carried | 'Its value is a whole number of seconds to wait' in `merged.md` -- Directly stated. |
| 13 | The Retry-After header is present on every refusal the gateway sends. | 11 | carried | 'and it is present on every refusal the gateway sends' in `merged.md` -- Directly stated. |
| 14 | The response body is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- Directly stated. |
| 15 | The response body repeats the cap, the window and the tier as plain fields. | 13 | carried | 'it names what the gateway calls the "window" it counted in. It names the cap and the tier as well' in `merged.md` -- The body naming window, cap and tier supports the claim it repeats these as fields. |
| 16 | There are four rules for what the client does. | 17 | carried | 'Four rules, given in the order they should be applied' in `merged.md` -- Directly stated. |
| 17 | On the 503 path the same rule of honouring the header holds. | 19 | carried | 'and it does the same on the 503 path' in `merged.md` -- Directly stated. |
| 18 | The cause of a 503 refusal is an entirely different one from a 429. | 19 | carried | 'even though the cause of the refusal there is an entirely different one' in `merged.md` -- Directly stated. |
| 19 | A 200 needs nothing in terms of retry. | 21 | carried | 'A 200 wants nothing' in `merged.md` -- Directly stated. |
| 20 | A 429 needs the stated wait. | 21 | carried | 'a 429 wants the stated wait' in `merged.md` -- Directly stated. |
| 21 | A 500 can be retried once the stated wait has passed. | 21 | carried | 'a 500 may be retried once that wait has passed' in `merged.md` -- Directly stated. |
| 22 | A 503 means the platform itself is overloaded. | 21 | carried | 'a 503 is the overload path' in `merged.md` -- Overload path entails the platform being overloaded. |
| 23 | A batch credential is allowed 1000 requests in a window. | 23 | carried | 'A batch credential is allowed 1000 requests in a window' in `merged.md` -- Directly stated. |
| 24 | 1000 requests in a window is 50 times the default allowance. | 23 | carried | 'fifty times the default allowance' in `merged.md` -- Directly stated. |
| 25 | The window, the header and the body are identical between the batch tier and the interactive case. | 23 | carried | 'The window, the header and the body are identical to the interactive case' in `merged.md` -- Directly stated. |
| 26 | A client written for one tier needs no change at all to run against the other. | 23 | carried | 'so a client written for one tier needs no change at all to run against the other' in `merged.md` -- Directly stated. |
| 27 | Nothing else about the batch tier differs from the default. | 23 | carried | 'Nothing else about the two tiers differs in any way' in `merged.md` -- Directly stated. |
| 28 | The rule instructs to log every refusal seen. | 25 | carried | 'Log every refusal seen' in `merged.md` -- Directly stated. |
| 29 | The rule instructs to keep the log for at least a week. | 25 | carried | 'and keep the log for at least a week' in `merged.md` -- Directly stated. |
| 30 | The gateway refuses a request for three separate reasons. | 29 | carried | 'The gateway refuses a request for three reasons' in `merged.md` -- Directly stated. |
| 31 | Only one of the three refusal reasons is a cap. | 29 | carried | 'and only one of them is the one above' in `merged.md` -- Directly stated. |
| 32 | A credential can be suspended. | 29 | carried | 'A credential may be suspended' in `merged.md` -- Directly stated. |
| 33 | A route can be closed while it is being repaired. | 29 | carried | 'a route may be closed for maintenance' in `merged.md` -- Directly stated. |
| 34 | A request body over the 5 megabyte limit is refused before it has been read at all. | 29 | carried | 'a body may exceed the 5 megabyte limit and be refused before it has been read at all' in `merged.md` -- Directly stated. |
| 35 | A loop retrying against a suspended credential burns its whole budget and reaches nothing. | 31 | carried | 'A loop that waits and retries against a suspended credential spends its whole budget without ever reaching the service' in `merged.md` -- Directly stated. |
| 36 | The log afterwards shows a long run of refusals and no successes at all in the case of a suspended credential. | 31 | carried | 'the log afterwards shows nothing at all except a long run of refusals' in `merged.md` -- Directly stated. |
| 37 | An answer takes two working days. | 37 | carried | 'they are answered within two working days' in `merged.md` -- Directly stated. |
| 38 | There is no expedited path for requests to the platform team. | 37 | carried | 'There is no expedited path' in `merged.md` -- Directly stated. |
| 39 | Requests go to the platform team through the usual channel. | 35 | carried | 'Requests reach the platform team through the usual channel' in `merged.md` -- Directly stated. |

### `merged.md` -- 45 claim(s): 0 invented, 0 contradicted, 0 supported in part, 45 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | The gateway answers 429 at the edge when a credential's cap is spent. | supported | `source_a.md` | 'When that cap is spent the gateway answers 429 at the edge' in `source_a.md` -- Both sources state this directly. |
| 2 | The gateway does not wake the service behind it when answering 429 at the edge. | supported | `source_a.md` | 'without waking the service behind it' in `source_a.md` -- Directly stated in source_a. |
| 3 | Requests are counted against the credential that presented them. | supported | `source_a.md` | 'Requests are counted against the credential that presented them' in `source_a.md` -- Directly stated. |
| 4 | Requests are counted over a fixed window of 60 seconds. | supported | `source_a.md` | 'over a fixed window of 60 seconds' in `source_a.md` -- Directly stated. |
| 5 | The gateway does not disclose the start of the 60 second window. | supported | `source_b.md` | 'whose start the gateway doesn’t disclose' in `source_b.md` -- Directly stated in source_b. |
| 6 | Requests are never counted against a connection. | supported | `source_a.md` | 'and never against a connection' in `source_a.md` -- Directly stated. |
| 7 | The count follows the credential across hosts. | supported | `source_b.md` | 'The count follows the credential wherever the caller happens to put it, including across hosts.' in `source_b.md` -- Directly stated in source_b. |
| 8 | A client spread across eight worker processes is throttled at exactly the point one process would have been. | supported | `source_a.md` | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `source_a.md` -- Directly stated. |
| 9 | The default allowance is 100 requests in a window. | supported | `source_a.md` | 'The default allowance is 100 requests in a window' in `source_a.md` -- Directly stated. |
| 10 | A credential marked for batch work is allowed 1000 requests in the same window. | supported | `source_a.md` | 'a credential marked for batch work is allowed 1000 in the same window' in `source_a.md` -- Directly stated. |
| 11 | The refusal carries a Retry-After header. | supported | `source_a.md` | 'The refusal carries a Retry-After header' in `source_a.md` -- Directly stated. |
| 12 | The Retry-After header's value is a whole number of seconds to wait. | supported | `source_a.md` | 'Its value is a whole number of seconds to wait' in `source_a.md` -- Directly stated. |
| 13 | The Retry-After header is present on every refusal the gateway sends. | supported | `source_b.md` | 'it is present on every refusal the gateway sends' in `source_b.md` -- Directly stated in source_b. |
| 14 | The gateway keeps no memory of who backed off politely. | supported | `source_a.md` | 'The gateway keeps no memory of who backed off politely' in `source_a.md` -- Directly stated. |
| 15 | The body of the refusal is JSON. | supported | `source_a.md` | 'The body of the refusal is JSON' in `source_a.md` -- Directly stated. |
| 16 | The body of the refusal names what the gateway calls the "window" it counted in. | supported | `source_a.md` | 'it names what the gateway calls the “window” it counted in' in `source_a.md` -- Directly stated. |
| 17 | The body of the refusal names the cap. | supported | `source_a.md` | 'It names the cap and the tier as well' in `source_a.md` -- Directly stated. |
| 18 | The body of the refusal names the tier. | supported | `source_a.md` | 'It names the cap and the tier as well' in `source_a.md` -- Directly stated. |
| 19 | The gateway does the same Retry-After arithmetic on the 503 path. | supported | `source_a.md` | 'and it does the same on the 503 path' in `source_a.md` -- Directly stated referring to the header arithmetic. |
| 20 | The cause of a refusal on the 503 path is an entirely different one from the 429 path. | supported | `source_b.md` | 'even though the cause of the refusal is an entirely different one' in `source_b.md` -- Directly stated in source_b. |
| 21 | A 200 response wants nothing retried. | supported | `source_a.md` | 'A 200 wants nothing' in `source_a.md` -- Directly stated. |
| 22 | A 429 response wants the stated wait. | supported | `source_a.md` | 'a 429 wants the stated wait' in `source_a.md` -- Directly stated. |
| 23 | A 500 response may be retried once its wait has passed. | supported | `source_a.md` | 'a 500 may be retried once that wait has passed' in `source_a.md` -- Directly stated. |
| 24 | A 503 response is the overload path. | supported | `source_a.md` | 'a 503 is the overload path' in `source_a.md` -- Directly stated. |
| 25 | A batch credential is allowed 1000 requests in a window. | supported | `source_b.md` | 'A batch credential is allowed 1000 requests in a window' in `source_b.md` -- Directly stated in source_b. |
| 26 | 1000 requests is fifty times the default allowance. | supported | `source_b.md` | 'which is 50 times the default' in `source_b.md` -- Directly stated in source_b. |
| 27 | The batch credential's 1000 requests is measured over exactly the same window as the default allowance. | supported | `source_a.md` | 'and it is measured over exactly the same window' in `source_a.md` -- Directly stated. |
| 28 | The tier is set on the credential when it is issued. | supported | `source_a.md` | 'The tier is set on the credential when it is issued' in `source_a.md` -- Directly stated. |
| 29 | The tier cannot be asked for per call. | supported | `source_a.md` | 'and cannot be asked for per call' in `source_a.md` -- Directly stated. |
| 30 | The window, the header and the body are identical between the interactive case and the batch case. | supported | `source_b.md` | 'The window, the header and the body are identical to the interactive case' in `source_b.md` -- Directly stated in source_b. |
| 31 | The log line should carry the credential. | supported | `source_a.md` | 'The log line should carry the credential, the window and the wait' in `source_a.md` -- Directly stated. |
| 32 | The log line should carry the window. | supported | `source_a.md` | 'The log line should carry the credential, the window and the wait' in `source_a.md` -- Directly stated. |
| 33 | The log line should carry the wait. | supported | `source_a.md` | 'The log line should carry the credential, the window and the wait' in `source_a.md` -- Directly stated. |
| 34 | The gateway refuses a request for three reasons. | supported | `source_a.md` | 'The gateway refuses a request for three reasons and only one of them is the one above' in `source_a.md` -- Directly stated. |
| 35 | Only one of the gateway's three refusal reasons is the rate-cap reason described above. | supported | `source_a.md` | 'and only one of them is the one above' in `source_a.md` -- Directly stated. |
| 36 | A credential may be suspended. | supported | `source_a.md` | 'A credential may be suspended' in `source_a.md` -- Directly stated. |
| 37 | A route may be closed for maintenance. | supported | `source_a.md` | 'a route may be closed for maintenance' in `source_a.md` -- Directly stated. |
| 38 | A body may exceed the 5 megabyte limit and be refused before it has been read at all. | supported | `source_b.md` | 'a request body over the 5 megabyte limit is refused before it has been read at all' in `source_b.md` -- Directly stated in source_b. |
| 39 | None of the three non-cap refusal reasons clears itself by waiting for a stated number of seconds. | supported | `source_a.md` | 'None of those three clears itself by waiting for a stated number of seconds.' in `source_a.md` -- Directly stated. |
| 40 | A cap can be raised. | supported | `source_a.md` | 'A cap can be raised' in `source_a.md` -- Directly stated. |
| 41 | The number of caps raised without a measurement behind them is 0. | supported | `source_a.md` | 'the number of caps raised without a measurement behind them is 0' in `source_a.md` -- Directly stated. |
| 42 | Requests reach the platform team through the usual channel. | supported | `source_a.md` | 'Requests reach the platform team through the usual channel' in `source_a.md` -- Directly stated. |
| 43 | Requests to the platform team are answered within two working days. | supported | `source_a.md` | 'and they are answered within two working days' in `source_a.md` -- Directly stated. |
| 44 | There is no expedited path for requests to the platform team. | supported | `source_a.md` | 'There is no expedited path' in `source_a.md` -- Directly stated. |
| 45 | There is no exception list for requests to the platform team. | supported | `source_a.md` | 'and no exception list' in `source_a.md` -- Directly stated. |

## Structure

**9** mechanical check(s) over **104** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **45** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **74**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 19 run(s) over 50 attributed segment(s) — sources interleaved. 6 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

`[-...-]` is what the source said and `{+...+}` is what the merge says.

### Reworded and undeclared — in the merge in altered wording, and no record explains it. At off this also covers layout: a segment whose source line breaks the merge ran together is altered and undeclared, and 380 reuses this kind rather than moving FINDING_KINDS off 12

- `a16` (`source_a.md`) — 'The body of the refusal is JSON, and it names what the gateway calls the “window” it counted in.' is reworded in the merge and no disposition record explains it (nearest merge segment m16 at 0.98)

  ```text
  In the source: The body of the refusal is JSON, and it names what the gateway calls the “window” it counted in.
  In the merge:  The body of the refusal is JSON, and it names what the gateway calls the "window" it counted in.
  What changed:  The body of the refusal is JSON, and it names what the gateway calls the [-“window”-] {+"window"+} it counted in.
  ```

### Verbatim violation — an invariant-core token did not survive unchanged

- `b31` (`source_b.md`) — numeric '50' (times) does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **67** departure(s) from its sources. Checking them confirms 32, rejects 1, and leaves 34 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 104 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | Title not chosen; base title used instead. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Rate limiting and the 429 contract for gateway clients' and says so (no claim traced to it) |
| `b2` | duplicate | Same fact as a2, kept once. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'duplicate' is what happened to it (no claim traced to it) |
| `b3` | duplicate | Same fact as a3, kept once. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-001`, `B-002`) |
| `b4` | reworded | Rationale for omitting client-side counters carried in. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-003`, `B-004`) |
| `a4` | reconciled | Window length and undisclosed start combined. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-003`, `A-004`, `A-005`) |
| `b5` | reconciled | Window length and undisclosed start combined. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-005`, `B-006`, `B-007`) |
| `a5` | reconciled | Socket futility combined with cross-host detail. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b6` | duplicate | Same fact as a5. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b7` | subsumed | Cross-host detail folded into a5's statement. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-008`) |
| `b8` | superseded | Duplicate of a6, which keeps the specific figure. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-009`) |
| `a7` | reconciled | Allowance figure and its rationale combined. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-007`, `A-008`) |
| `b9` | reconciled | Allowance figure and its rationale combined. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-010`) |
| `a8` | reconciled | Outage, bug and capacity claims combined. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b10` | reconciled | Outage, bug and capacity claims combined. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `a9` | reconciled | Outage, bug and capacity claims combined. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b11` | superseded | Duplicate of a10. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b12` | duplicate | Identical heading text to a11. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b13` | superseded | Duplicate of a12. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-011`) |
| `a13` | reconciled | Wait duration and universality combined. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-010`) |
| `b14` | reconciled | Wait duration and universality combined. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-012`, `B-013`) |
| `b15` | superseded | Same contract stated; a14's wording kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b16` | superseded | Same fact; a15's wording kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b17` | superseded | Duplicate description of body fields. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-014`, `B-015`) |
| `b18` | superseded | Same critique; a18's wording kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b19` | superseded | a19 states the same fact more completely. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b20` | superseded | Heading not chosen; base heading used. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b21` | superseded | Duplicate of a21. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-016`) |
| `b22` | superseded | Duplicate rule label of a22. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a23` | reconciled | 503-path detail combined with the arithmetic claim. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-016`) |
| `b23` | superseded | Duplicate of a23's core statement. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b24` | reconciled | 503-path detail combined with the arithmetic claim. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-017`, `B-018`) |
| `b25` | superseded | Duplicate of a24. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b26` | superseded | Duplicate of a25. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a26` | reconciled | Rule text combined with the scope clarification. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b27` | reconciled | Rule text combined with the scope clarification. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b28` | superseded | Duplicate of a27. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-019`, `B-020`, `B-021`, `B-022`) |
| `b29` | superseded | Duplicate of a29. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b30` | superseded | Same point as a30. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a32` | reconciled | Allowance figure and window-scope wording combined. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-021`, `A-022`) |
| `b31` | reconciled | Allowance figure and window-scope wording combined. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-023`, `B-024`) |
| `b33` | superseded | Duplicate of a34. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-027`) |
| `a35` | reconciled | Rule text combined with retention period. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b34` | reconciled | Rule text combined with retention period. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-028`, `B-029`) |
| `b35` | superseded | Duplicate of a36. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b37` | superseded | Heading not chosen; base heading used. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a40` | reconciled | Reason count combined with irrelevance detail. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-025`, `A-026`) |
| `b38` | superseded | Duplicate of a40's core statement. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-030`, `B-031`) |
| `b39` | reconciled | Reason count combined with irrelevance detail. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `a41` | reconciled | Refusal causes combined with read-before-refusal detail. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-027`, `A-028`, `A-029`) |
| `b40` | reconciled | Refusal causes combined with read-before-refusal detail. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-032`, `B-033`, `B-034`) |
| `a43` | reconciled | Comparison to a reader added to the base claim. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b41` | reconciled | Comparison to a reader added to the base claim. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `a44` | reconciled | Budget loss combined with outage-resemblance detail. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b42` | superseded | Duplicate of a44's core statement. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-035`) |
| `b43` | reconciled | Budget loss combined with outage-resemblance detail. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-036`) |
| `b46` | superseded | Same policy; a47's numeric wording kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b47` | superseded | Duplicate of a48. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a49` | reconciled | Evaluation-order detail combined with base claim. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b48` | reconciled | Evaluation-order detail combined with base claim. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b49` | superseded | Duplicate of a49's burst clause. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a50` | reconciled | Preference combined with cheapest-fix detail. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b44` | superseded | Duplicate of a50's core statement. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b45` | reconciled | Preference combined with cheapest-fix detail. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `a51` | reconciled | Turnaround time combined with chasing detail. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-032`, `A-033`) |
| `b50` | superseded | Duplicate of a51's core statement. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-039`) |
| `b52` | reconciled | Turnaround time combined with chasing detail. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-037`) |
| `b51` | superseded | Duplicate of a52. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-038`) |


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
| Duration | 385.7s |
| Generated | 2026-09-27T19:32:44+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup sonnet-5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
