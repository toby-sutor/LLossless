## Verdict

**No extracted claim was dropped, contradicted, invented, or carried only in part.** 54 source claim(s) checked against the merge, 43 merge claim(s) checked against the sources. The 9 mechanical checks under Structure below cover what the claims do not: titles, invariant-core tokens, and all 104 source segment(s) — including the ones no claim was drawn from.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 43 |
| Claims extracted from `source_a.md` | 31 |
| Claims extracted from `source_b.md` | 23 |
| Forward — source claims accounted for in the merge | **54/54** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **31/31** |
| Forward — `source_b.md` claims accounted for | **23/23** |
| Reverse — merge claims found in a source | **43/43** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **97/97** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

None.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 31 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 31 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The gateway answers 429 at the edge when a credential's cap is spent. | 3 | carried | 'the gateway answers 429 at the edge — without waking the service behind it' in `merged.md` -- Directly stated in the opening sentence. |
| 2 | The gateway answers 429 without waking the service behind it. | 3 | carried | 'the gateway answers 429 at the edge — without waking the service behind it' in `merged.md` -- Directly stated. |
| 3 | Requests are counted against the credential that presented them. | 5 | carried | 'Requests are counted against the credential that presented them' in `merged.md` -- Directly stated. |
| 4 | Requests are counted over a fixed window of 60 seconds. | 5 | carried | 'over a fixed window of 60 seconds' in `merged.md` -- Directly stated. |
| 5 | Requests are never counted against a connection. | 5 | carried | 'and never against a connection' in `merged.md` -- Directly stated. |
| 6 | A client spread across eight worker processes is throttled at exactly the point one process would have been. | 5 | carried | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `merged.md` -- Directly stated. |
| 7 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- Directly stated. |
| 8 | A credential marked for batch work is allowed 1000 requests in the same window. | 7 | carried | 'a credential marked for batch work is allowed 1000 in the same window' in `merged.md` -- Directly stated. |
| 9 | The refusal carries a Retry-After header. | 11 | carried | 'The refusal carries a Retry-After header, present on every refusal the gateway sends.' in `merged.md` -- Directly stated. |
| 10 | The Retry-After header's value is a whole number of seconds to wait. | 11 | carried | 'Its value is a whole number of seconds to wait.' in `merged.md` -- Directly stated. |
| 11 | The gateway keeps no memory of who backed off politely. | 11 | carried | 'The gateway keeps no memory of who backed off politely' in `merged.md` -- Directly stated. |
| 12 | The body of the refusal is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- Directly stated. |
| 13 | The body of the refusal names what the gateway calls the "window" it counted in. | 13 | carried | 'it names what the gateway calls the “window” it counted in' in `merged.md` -- Directly stated. |
| 14 | The body of the refusal names the cap. | 13 | carried | 'It names the cap and the tier as well.' in `merged.md` -- Directly stated that the body names the cap. |
| 15 | The body of the refusal names the tier. | 13 | carried | 'It names the cap and the tier as well.' in `merged.md` -- Directly stated that the body names the tier. |
| 16 | The gateway does the same arithmetic on the 503 path. | 19 | carried | 'it does the same on the 503 path, even though the cause of that refusal is an entirely different one' in `merged.md` -- Directly stated. |
| 17 | A batch credential is allowed fifty times the default allowance. | 23 | carried | 'A batch credential is allowed fifty times the default allowance' in `merged.md` -- Directly stated. |
| 18 | A batch credential's allowance is measured over exactly the same window as the default. | 23 | carried | 'and it is measured over exactly the same window' in `merged.md` -- Directly stated. |
| 19 | The tier is set on the credential when it is issued. | 23 | carried | 'The tier is set on the credential when it is issued' in `merged.md` -- Directly stated. |
| 20 | The tier cannot be asked for per call. | 23 | carried | 'and cannot be asked for per call' in `merged.md` -- Directly stated. |
| 21 | The gateway refuses a request for three reasons. | 29 | carried | 'The gateway refuses a request for three reasons and only one of them is the one above' in `merged.md` -- Directly stated. |
| 22 | Only one of the three reasons the gateway refuses a request is the rate-limit reason described above. | 29 | carried | 'The gateway refuses a request for three reasons and only one of them is the one above' in `merged.md` -- Directly stated. |
| 23 | A credential may be suspended. | 29 | carried | 'A credential may be suspended' in `merged.md` -- Directly stated. |
| 24 | A route may be closed for maintenance. | 29 | carried | 'a route may be closed for maintenance' in `merged.md` -- Directly stated. |
| 25 | A body may exceed the 5 megabyte limit. | 29 | carried | 'a body may exceed the 5 megabyte limit and be refused before it has even been read' in `merged.md` -- Directly stated. |
| 26 | None of the three non-cap refusal reasons clears itself by waiting for a stated number of seconds. | 29 | carried | 'None of those three clears itself by waiting for a stated number of seconds.' in `merged.md` -- Directly stated. |
| 27 | The number of caps raised without a measurement behind them is 0. | 35 | carried | 'the number of caps raised without a measurement behind them is 0' in `merged.md` -- Directly stated. |
| 28 | Requests for a cap increase reach the platform team through the usual channel. | 37 | carried | 'Requests reach the platform team through the usual channel' in `merged.md` -- Directly stated. |
| 29 | Requests for a cap increase are answered within two working days. | 37 | carried | 'they are answered within two working days' in `merged.md` -- Directly stated. |
| 30 | There is no expedited path for requesting a cap increase. | 37 | carried | 'There is no expedited path' in `merged.md` -- Directly stated. |
| 31 | There is no exception list for requesting a cap increase. | 37 | carried | 'and no exception list' in `merged.md` -- Directly stated. |

### `source_b.md` -- 23 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 23 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The gateway answers 429 at the edge when the cap is spent, without troubling the service behind it. | 3 | carried | 'the gateway answers 429 at the edge — without waking the service behind it' in `merged.md` -- Directly stated. |
| 2 | Requests are counted against the credential rather than the connection. | 5 | carried | "Requests are counted against the credential that presented them, over a fixed window of 60 seconds whose start the gateway doesn't disclose, and never against a connection." in `merged.md` -- States requests are counted against the credential and never against a connection. |
| 3 | Requests are counted over a fixed window of 60 seconds. | 5 | carried | 'over a fixed window of 60 seconds' in `merged.md` -- Directly stated. |
| 4 | The gateway doesn't disclose the start of the fixed window. | 5 | carried | "whose start the gateway doesn't disclose" in `merged.md` -- Directly stated. |
| 5 | The count follows the credential wherever the caller puts it, including across hosts. | 5 | carried | 'The count follows the credential wherever the caller puts it, including across hosts.' in `merged.md` -- Directly stated. |
| 6 | A caller spread over many worker processes is throttled at the same point a single process would have been. | 5 | carried | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `merged.md` -- Directly stated. |
| 7 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- Directly stated. |
| 8 | The header is called Retry-After. | 11 | carried | 'The refusal carries a Retry-After header' in `merged.md` -- Directly names the header. |
| 9 | The Retry-After header's value is a whole number of seconds. | 11 | carried | 'Its value is a whole number of seconds to wait.' in `merged.md` -- Directly stated. |
| 10 | The Retry-After header is present on every refusal the gateway sends. | 11 | carried | 'present on every refusal the gateway sends' in `merged.md` -- Directly stated. |
| 11 | The response body is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- Directly stated. |
| 12 | The response body repeats the cap, the window and the tier as plain fields. | 13 | carried | 'it names what the gateway calls the “window” it counted in. It names the cap and the tier as well.' in `merged.md` -- States the body names the window, cap and tier. |
| 13 | There are four rules. | 17 | carried | 'Four rules, given in the order they should be applied.' in `merged.md` -- Directly stated. |
| 14 | The same rule of honouring the header and not computing your own wait holds on the 503 path. | 19 | carried | 'and it does the same on the 503 path, even though the cause of that refusal is an entirely different one' in `merged.md` -- States the same honour-the-header logic applies on the 503 path. |
| 15 | A batch credential is allowed 1000 requests in a window. | 23 | carried | 'a credential marked for batch work is allowed 1000 in the same window' in `merged.md` -- Directly stated. |
| 16 | A batch credential's 1000 requests in a window is 50 times the default. | 23 | carried | 'A batch credential is allowed fifty times the default allowance' in `merged.md` -- States the batch allowance is fifty times the default, matching 1000 vs 100. |
| 17 | The window, the header and the body are identical between the batch and interactive tiers. | 23 | carried | 'The window, the header and the body are identical to the interactive case' in `merged.md` -- Directly stated. |
| 18 | The gateway refuses a request for three separate reasons. | 29 | carried | 'The gateway refuses a request for three reasons and only one of them is the one above' in `merged.md` -- Directly stated. |
| 19 | Only one of the gateway's three refusal reasons is a cap. | 29 | carried | 'and only one of them is the one above' in `merged.md` -- Directly stated. |
| 20 | A credential can be suspended. | 29 | carried | 'A credential may be suspended' in `merged.md` -- Directly stated. |
| 21 | A route can be closed while it is being repaired. | 29 | carried | 'a route may be closed for maintenance' in `merged.md` -- Maintenance implies repair; directly stated. |
| 22 | A request body over the 5 megabyte limit is refused before it has been read at all. | 29 | carried | 'a body may exceed the 5 megabyte limit and be refused before it has even been read' in `merged.md` -- Directly stated. |
| 23 | An answer from the platform team takes two working days. | 37 | carried | 'they are answered within two working days' in `merged.md` -- Directly stated. |

### `merged.md` -- 43 claim(s): 0 invented, 0 contradicted, 0 supported in part, 43 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | When a credential's cap is spent the gateway answers 429 at the edge. | supported | `source_a.md` | 'When that cap is spent the gateway answers 429 at the edge' in `source_a.md` -- Source_a states this directly. |
| 2 | The gateway answers 429 without waking the service behind it. | supported | `source_a.md` | 'the gateway answers 429 at the edge — without waking the service behind it' in `source_a.md` -- Directly stated in source_a. |
| 3 | An earlier draft of this note argued for a client-side token bucket that mirrored the gateway's own counters. | supported | `source_b.md` | 'An earlier draft of this note argued for a client-side token bucket that mirrored the gateway’s own counters' in `source_b.md` -- Directly stated in source_b. |
| 4 | That section arguing for a client-side token bucket has been left out on purpose. | supported | `source_b.md` | 'and that section has been left out on purpose' in `source_b.md` -- Directly stated in source_b. |
| 5 | Requests are counted against the credential that presented them. | supported | `source_a.md` | 'Requests are counted against the credential that presented them' in `source_a.md` -- Directly stated in source_a. |
| 6 | Requests are counted over a fixed window of 60 seconds. | supported | `source_a.md` | 'over a fixed window of 60 seconds' in `source_a.md` -- Directly stated in source_a. |
| 7 | The gateway does not disclose the start of the 60 second window. | supported | `source_b.md` | 'over a fixed window of 60 seconds whose start the gateway doesn’t disclose' in `source_b.md` -- Directly stated in source_b. |
| 8 | Requests are never counted against a connection. | supported | `source_a.md` | 'and never against a connection' in `source_a.md` -- Directly stated in source_a. |
| 9 | The count follows the credential wherever the caller puts it, including across hosts. | supported | `source_b.md` | 'The count follows the credential wherever the caller happens to put it, including across hosts.' in `source_b.md` -- Directly stated in source_b. |
| 10 | Opening a second socket buys a caller nothing. | supported | `source_a.md` | 'Opening a second socket therefore buys a caller nothing.' in `source_a.md` -- Directly stated in source_a. |
| 11 | A client spread across eight worker processes is throttled at exactly the point one process would have been. | supported | `source_a.md` | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `source_a.md` -- Directly stated in source_a. |
| 12 | A client spread across eight worker processes pays for the extra file descriptors as well. | supported | `source_a.md` | 'and pays for the extra file descriptors as well' in `source_a.md` -- Directly stated in source_a. |
| 13 | The default allowance is 100 requests in a window. | supported | `source_a.md` | 'The default allowance is 100 requests in a window' in `source_a.md` -- Directly stated in source_a. |
| 14 | A credential marked for batch work is allowed 1000 requests in the same window. | supported | `source_a.md` | 'a credential marked for batch work is allowed 1000 in the same window' in `source_a.md` -- Directly stated in source_a. |
| 15 | The refusal carries a Retry-After header. | supported | `source_a.md` | 'The refusal carries a Retry-After header.' in `source_a.md` -- Directly stated in source_a. |
| 16 | The Retry-After header is present on every refusal the gateway sends. | supported | `source_b.md` | 'it is present on every refusal the gateway sends' in `source_b.md` -- Directly stated in source_b. |
| 17 | The Retry-After header's value is a whole number of seconds to wait. | supported | `source_a.md` | 'Its value is a whole number of seconds to wait.' in `source_a.md` -- Directly stated in source_a. |
| 18 | The gateway keeps no memory of who backed off politely. | supported | `source_a.md` | 'The gateway keeps no memory of who backed off politely' in `source_a.md` -- Directly stated in source_a. |
| 19 | The body of the refusal is JSON. | supported | `source_a.md` | 'The body of the refusal is JSON' in `source_a.md` -- Directly stated in source_a. |
| 20 | The body of the refusal names what the gateway calls the "window" it counted in. | supported | `source_a.md` | 'it names what the gateway calls the “window” it counted in' in `source_a.md` -- Directly stated in source_a. |
| 21 | The body of the refusal names the cap and the tier. | supported | `source_a.md` | 'It names the cap and the tier as well.' in `source_a.md` -- Directly stated in source_a. |
| 22 | The gateway does the same Retry-After arithmetic on the 503 path. | supported | `source_a.md` | 'and it does the same on the 503 path' in `source_a.md` -- Directly stated in source_a regarding the header arithmetic. |
| 23 | The cause of a 503 refusal is an entirely different one from the cause of a 429 refusal. | supported | `source_b.md` | 'even though the cause of the refusal is an entirely different one' in `source_b.md` -- Directly stated in source_b. |
| 24 | A 200 response wants nothing retried. | supported | `source_a.md` | 'A 200 wants nothing' in `source_a.md` -- Directly stated in source_a. |
| 25 | A 429 response wants the stated wait. | supported | `source_a.md` | 'a 429 wants the stated wait' in `source_a.md` -- Directly stated in source_a. |
| 26 | A 500 response may be retried once its wait has passed. | supported | `source_a.md` | 'a 500 may be retried once that wait has passed' in `source_a.md` -- Directly stated in source_a. |
| 27 | A 503 response is the overload path. | supported | `source_a.md` | 'a 503 is the overload path' in `source_a.md` -- Directly stated in source_a. |
| 28 | A batch credential is allowed fifty times the default allowance. | supported | `source_a.md` | 'A batch credential is allowed fifty times the default allowance' in `source_a.md` -- Directly stated in source_a. |
| 29 | The batch credential's allowance is measured over exactly the same window as the interactive credential. | supported | `source_a.md` | 'it is measured over exactly the same window' in `source_a.md` -- Directly stated in source_a. |
| 30 | The tier is set on the credential when it is issued. | supported | `source_a.md` | 'The tier is set on the credential when it is issued' in `source_a.md` -- Directly stated in source_a. |
| 31 | The tier cannot be asked for per call. | supported | `source_a.md` | 'cannot be asked for per call' in `source_a.md` -- Directly stated in source_a. |
| 32 | The window, the header and the body are identical between the interactive and batch tiers. | supported | `source_b.md` | 'The window, the header and the body are identical to the interactive case' in `source_b.md` -- Directly stated in source_b. |
| 33 | The gateway refuses a request for three reasons. | supported | `source_a.md` | 'The gateway refuses a request for three reasons' in `source_a.md` -- Directly stated in source_a. |
| 34 | Only one of the gateway's three refusal reasons is the rate-limiting one described above. | supported | `source_a.md` | 'and only one of them is the one above' in `source_a.md` -- Directly stated in source_a. |
| 35 | A credential may be suspended. | supported | `source_a.md` | 'A credential may be suspended' in `source_a.md` -- Directly stated in source_a. |
| 36 | A route may be closed for maintenance. | supported | `source_a.md` | 'a route may be closed for maintenance' in `source_a.md` -- Directly stated in source_a. |
| 37 | A body may exceed the 5 megabyte limit and be refused before it has even been read. | supported | `source_b.md` | 'a request body over the 5 megabyte limit is refused before it has been read at all' in `source_b.md` -- Directly stated in source_b. |
| 38 | None of the three non-cap refusal reasons clears itself by waiting for a stated number of seconds. | supported | `source_a.md` | 'None of those three clears itself by waiting for a stated number of seconds.' in `source_a.md` -- Directly stated in source_a. |
| 39 | The number of caps raised without a measurement behind them is 0. | supported | `source_a.md` | 'the number of caps raised without a measurement behind them is 0' in `source_a.md` -- Directly stated in source_a. |
| 40 | Requests for a cap increase reach the platform team through the usual channel. | supported | `source_a.md` | 'Requests reach the platform team through the usual channel' in `source_a.md` -- Directly stated in source_a. |
| 41 | Requests for a cap increase are answered within two working days. | supported | `source_a.md` | 'and they are answered within two working days' in `source_a.md` -- Directly stated in source_a. |
| 42 | There is no expedited path for a cap increase request. | supported | `source_a.md` | 'There is no expedited path' in `source_a.md` -- Directly stated in source_a. |
| 43 | There is no exception list for a cap increase request. | supported | `source_a.md` | 'and no exception list' in `source_a.md` -- Directly stated in source_a. |

## Structure

**9** mechanical check(s) over **104** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **43** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **54**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 21 run(s) over 54 attributed segment(s) — sources interleaved. 6 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

No structural finding.

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **66** departure(s) from its sources. Checking them confirms 24, rejects 2, and leaves 40 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 104 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | Title decision kept base title. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Rate limiting and the 429 contract for gateway clients' and says so (no claim traced to it) |
| `b2` | superseded | Same fact, base wording kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b3` | superseded | Same fact, base wording kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-001`) |
| `b4` | reworded | Unique fact from b, kept near-verbatim. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a4` | reconciled | Combined with b5's undisclosed-start detail. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-003`, `A-004`, `A-005`) |
| `b5` | reconciled | Combined with a4's counting rule. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-002`, `B-003`, `B-004`) |
| `b7` | reworded | Unique cross-host detail kept, lightly reworded. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-005`) |
| `b6` | superseded | Same fact, base wording kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b8` | superseded | Same fact, base wording kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-006`) |
| `a7` | reconciled | Combined with b9's interactive-use and misuse detail. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-007`, `A-008`) |
| `b9` | reconciled | Combined with a7's allowance numbers. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-007`) |
| `a8` | reconciled | Combined with b10's not-a-bug clause. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b10` | reconciled | Combined with a8's error-class clause. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b11` | superseded | Same fact, base wording kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b12` | duplicate | Identical heading already carried from base. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `a12` | reconciled | Combined with b14's present-on-every-refusal detail. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-009`) |
| `b13` | superseded | Same fact as a12, folded into combined sentence. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-008`) |
| `b14` | reconciled | Combined with a12's header-name statement. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-009`, `B-010`) |
| `b15` | superseded | Same fact, base wording kept; editorial aside dropped. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b16` | superseded | Same fact, base wording kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b17` | superseded | Same fact, base wording kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-011`, `B-012`) |
| `b18` | superseded | Same fact, base wording kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b19` | superseded | Same fact, base wording kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b20` | superseded | Heading decision kept base heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b21` | superseded | Same fact, base wording kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-013`) |
| `b22` | superseded | Extra clause duplicates content carried under rule 1's detail. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a23` | reconciled | Combined with b24's differing-cause detail. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-016`) |
| `b23` | duplicate | Restates a23's arithmetic claim. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b24` | reconciled | Combined with a23's arithmetic claim. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-014`) |
| `b25` | superseded | Same fact, base wording kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b26` | superseded | Same fact, base wording kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a26` | reconciled | Combined with b27's clarifying clause. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b27` | reconciled | Combined with a26's rule statement. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b28` | superseded | Same fact, base wording kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b29` | superseded | Same fact, base wording kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b30` | superseded | Same fact, base wording kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b31` | superseded | Same fact, base wording kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-015`, `B-016`) |
| `b32` | reworded | Unique cross-tier detail kept, lightly reworded. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-017`) |
| `b33` | superseded | Same fact, base wording kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a35` | reconciled | Combined with b34's retention period detail. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b34` | reconciled | Combined with a35's logging rule. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b35` | superseded | Same fact, base wording kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a37` | reconciled | Combined with b36's argument-value detail. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b36` | reconciled | Combined with a37's log-content detail. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b37` | superseded | Heading decision kept base heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b38` | superseded | Same fact, base wording kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-018`, `B-019`) |
| `a41` | reconciled | Combined with b40's refused-before-read detail. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-023`, `A-024`, `A-025`) |
| `b40` | reconciled | Combined with a41's list of three reasons. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-020`, `B-021`, `B-022`) |
| `a43` | reconciled | Combined with b41's reader-comparison detail. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b41` | reconciled | Combined with a43's retry-loop claim. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `a44` | reconciled | Combined with b42/b43's outage-resemblance detail. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b42` | reconciled | Combined with a44's suspended-credential detail. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b43` | reconciled | Combined with a44's suspended-credential detail. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `a47` | reconciled | Combined with b46's no-assertion-alone detail. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-027`) |
| `b46` | reconciled | Combined with a47's zero-measurement statistic. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b47` | superseded | Same fact, base wording kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a49` | reconciled | Combined with b48's before-the-number detail. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b48` | reconciled | Combined with a49's smooth-vs-bursty claim. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b49` | duplicate | Restates the burst-cheaper-to-smooth fact. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `a50` | reconciled | Combined with b44/b45's cheapest-fix detail. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b44` | reconciled | Combined with a50's quieter-hour claim. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b45` | reconciled | Combined with a50's quieter-hour claim. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `a51` | reconciled | Combined with b50/b52's chasing-doesn't-help detail. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-028`, `A-029`) |
| `b50` | reconciled | Combined with a51's channel/timing claim. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b52` | reconciled | Combined with a51's channel/timing claim. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-023`) |
| `b51` | superseded | Same fact, base wording kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |


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
| Duration | 292.6s |
| Generated | 2026-09-27T18:47:20+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup sonnet-5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
