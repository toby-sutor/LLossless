## Verdict

**4 finding(s).** In the claims: 2 partially dropped. In the structure: 2 false departure.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 27 |
| Claims extracted from `source_a.md` | 28 |
| Claims extracted from `source_b.md` | 30 |
| Forward — source claims accounted for in the merge | **56/58** |
| Forward — carried only in part | 2 |
| Forward — `source_a.md` claims accounted for | **27/28** (1 in part) |
| Forward — `source_b.md` claims accounted for | **29/30** (1 in part) |
| Reverse — merge claims found in a source | **27/27** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **85/85** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Partly dropped — the merge carries some of this claim

- **A-014** (`source_a.md:19`) — The gateway honours the same Retry-After arithmetic on the 503 path.
  - evidence: 'On the 503 path the same rule holds, even though the cause of the refusal is an entirely different one.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The honour-the-header rule holds on 503, but the text does not say the gateway performs Retry-After arithmetic there specifically.
- **B-025** (`source_b.md:29`) — A route can be closed while it is being repaired.
  - evidence: 'a route may be closed for maintenance' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: Route closure for maintenance is stated; 'while being repaired' is close but maintenance is not explicitly repair.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 28 claim(s): 0 dropped, 0 contradicted, 1 carried in part, 27 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 14 | The gateway honours the same Retry-After arithmetic on the 503 path. | 19 | carried in part | 'On the 503 path the same rule holds, even though the cause of the refusal is an entirely different one.' in `merged.md` -- The honour-the-header rule holds on 503, but the text does not say the gateway performs Retry-After arithmetic there specifically. |
| 1 | When a credential's cap is spent, the gateway answers 429 at the edge without waking the service behind it. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge — without waking the service behind it' in `merged.md` -- Stated directly. |
| 2 | Requests are counted against the credential that presented them. | 5 | carried | 'Requests are counted against the credential that presented them' in `merged.md` -- Stated directly. |
| 3 | The rate-limit counting window is a fixed window of 60 seconds. | 5 | carried | 'over a fixed window of 60 seconds' in `merged.md` -- Stated directly. |
| 4 | Requests are never counted against a connection. | 5 | carried | 'and never against a connection' in `merged.md` -- Stated directly. |
| 5 | A client spread across eight worker processes is throttled at exactly the point one process would have been. | 5 | carried | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `merged.md` -- Stated directly. |
| 6 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- Stated directly. |
| 7 | A credential marked for batch work is allowed 1000 requests in the same window. | 7 | carried | 'A credential marked for batch work is allowed 1000 in the same window.' in `merged.md` -- Stated directly. |
| 8 | The 429 refusal carries a Retry-After header. | 11 | carried | 'The refusal carries a Retry-After header.' in `merged.md` -- Stated directly. |
| 9 | The Retry-After header value is a whole number of seconds to wait. | 11 | carried | 'Its value is a whole number of seconds to wait' in `merged.md` -- Stated directly. |
| 10 | The gateway keeps no memory of who backed off politely. | 11 | carried | 'The gateway keeps no memory of who backed off politely' in `merged.md` -- Stated directly. |
| 11 | The body of the refusal is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- Stated directly. |
| 12 | The refusal body names the window the gateway counted in. | 13 | carried | 'it repeats the cap, the window the gateway counted in, and the tier as plain fields' in `merged.md` -- Body includes the window. |
| 13 | The refusal body names the cap and the tier. | 13 | carried | 'it repeats the cap, the window the gateway counted in, and the tier as plain fields' in `merged.md` -- Body includes cap and tier. |
| 15 | A 500 may be retried once the stated wait has passed. | 21 | carried | 'a 500 may be retried once that wait has passed' in `merged.md` -- Stated directly. |
| 16 | A 503 is the overload path. | 21 | carried | 'a 503 means the platform itself is overloaded' in `merged.md` -- 503 means overload. |
| 17 | A batch credential is allowed fifty times the default allowance. | 23 | carried | 'which is 50 times the default' in `merged.md` -- 50 equals fifty. |
| 18 | A batch credential is measured over exactly the same window as the default tier. | 23 | carried | 'it is measured over exactly the same window' in `merged.md` -- Stated directly. |
| 19 | The tier is set on the credential when it is issued. | 23 | carried | 'The tier is set on the credential when it is issued' in `merged.md` -- Stated directly. |
| 20 | The tier cannot be asked for per call. | 23 | carried | 'cannot be asked for per call' in `merged.md` -- Stated directly. |
| 21 | The gateway refuses a request for three reasons. | 29 | carried | 'The gateway refuses a request for three reasons' in `merged.md` -- Stated directly. |
| 22 | A body may exceed the 5 megabyte limit, which is a refusal reason. | 29 | carried | 'a body may exceed the 5 megabyte limit and is then refused' in `merged.md` -- Stated directly. |
| 23 | A suspended credential is a refusal reason. | 29 | carried | 'A credential may be suspended' in `merged.md` -- Listed as a reason. |
| 24 | A route closed for maintenance is a refusal reason. | 29 | carried | 'a route may be closed for maintenance' in `merged.md` -- Listed as a reason. |
| 25 | The number of caps raised without a measurement behind them is 0. | 35 | carried | 'the number of caps raised without a measurement behind them is 0' in `merged.md` -- Stated directly. |
| 26 | Requests to the platform team are answered within two working days. | 37 | carried | 'they are answered within two working days' in `merged.md` -- Stated directly. |
| 27 | There is no expedited path for requests to the platform team. | 37 | carried | 'There is no expedited path' in `merged.md` -- Stated directly. |
| 28 | There is no exception list for cap increases. | 37 | carried | 'no exception list' in `merged.md` -- Stated directly. |

### `source_b.md` -- 30 claim(s): 0 dropped, 0 contradicted, 1 carried in part, 29 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 25 | A route can be closed while it is being repaired. | 29 | carried in part | 'a route may be closed for maintenance' in `merged.md` -- Route closure for maintenance is stated; 'while being repaired' is close but maintenance is not explicitly repair. |
| 1 | Every credential has a cap of its own. | 3 | carried | 'Every credential has a cap.' in `merged.md` -- Stated directly. |
| 2 | When the cap is spent the gateway answers 429 at the edge, without troubling the service behind it. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge — without waking the service behind it' in `merged.md` -- Same meaning. |
| 3 | Requests are counted against the credential rather than the connection. | 5 | carried | 'Requests are counted against the credential that presented them, over a fixed window of 60 seconds whose start the gateway does not disclose, and never against a connection.' in `merged.md` -- Stated directly. |
| 4 | Requests are counted over a fixed window of 60 seconds. | 5 | carried | 'over a fixed window of 60 seconds' in `merged.md` -- Stated directly. |
| 5 | The gateway doesn't disclose the start of the 60 second window. | 5 | carried | 'whose start the gateway does not disclose' in `merged.md` -- Stated directly. |
| 6 | The request count follows the credential wherever the caller puts it, including across hosts. | 5 | carried | 'The count follows the credential wherever the caller puts it, including across hosts.' in `merged.md` -- Stated directly. |
| 7 | A caller spread over many worker processes is throttled at the same point a single process would have been. | 5 | carried | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `merged.md` -- Eight is an instance of many. |
| 8 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- Stated directly. |
| 9 | The default allowance of 100 requests in a window is enough for every interactive use of this API the platform team has seen. | 7 | carried | 'which is enough for every interactive use of this API the platform team has seen' in `merged.md` -- Stated directly. |
| 10 | The header is called Retry-After. | 11 | carried | 'The refusal carries a Retry-After header.' in `merged.md` -- Stated directly. |
| 11 | The Retry-After value is a whole number of seconds. | 11 | carried | 'Its value is a whole number of seconds to wait' in `merged.md` -- Stated directly. |
| 12 | The Retry-After header is present on every refusal the gateway sends. | 11 | carried | 'it is present on every refusal the gateway sends' in `merged.md` -- Stated directly. |
| 13 | The response body is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- Stated directly. |
| 14 | The response body repeats the cap, the window and the tier as plain fields. | 13 | carried | 'it repeats the cap, the window the gateway counted in, and the tier as plain fields' in `merged.md` -- Stated directly. |
| 15 | A 200 response needs no retry. | 21 | carried | 'A 200 wants nothing' in `merged.md` -- Same meaning. |
| 16 | A 429 response needs the stated wait. | 21 | carried | 'a 429 wants the stated wait' in `merged.md` -- Stated directly. |
| 17 | A 500 response can be retried once that wait has passed. | 21 | carried | 'a 500 may be retried once that wait has passed' in `merged.md` -- Stated directly. |
| 18 | A 503 response means the platform itself is overloaded. | 21 | carried | 'a 503 means the platform itself is overloaded' in `merged.md` -- Stated directly. |
| 19 | A batch credential is allowed 1000 requests in a window. | 23 | carried | 'A batch credential is allowed 1000 requests in a window' in `merged.md` -- Stated directly. |
| 20 | The batch allowance of 1000 requests in a window is 50 times the default. | 23 | carried | 'which is 50 times the default' in `merged.md` -- Stated directly. |
| 21 | The window, the header and the body are identical between the batch and interactive cases. | 23 | carried | 'it is measured over exactly the same window. The header and the body are identical to the interactive case' in `merged.md` -- Window, header and body all identical. |
| 22 | Nothing else about the batch tier differs from the default. | 23 | carried | 'Nothing else about the two tiers differs in any way.' in `merged.md` -- Stated directly. |
| 23 | The gateway refuses a request for three separate reasons, and only one of them is a cap. | 29 | carried | 'The gateway refuses a request for three reasons and only one of them is the one above.' in `merged.md` -- Only one is a cap. |
| 24 | A credential can be suspended. | 29 | carried | 'A credential may be suspended' in `merged.md` -- Stated directly. |
| 26 | A request body over the 5 megabyte limit is refused before it has been read at all. | 29 | carried | 'a body may exceed the 5 megabyte limit and is then refused before it has been read at all' in `merged.md` -- Stated directly. |
| 27 | A refusal count for a full week is required to support a cap increase request. | 33 | carried | 'Bring the refusal counts for a full week' in `merged.md` -- Required for an increase request. |
| 28 | Requests for a cap increase go to the platform team through the usual channel. | 35 | carried | 'Requests reach the platform team through the usual channel' in `merged.md` -- Stated directly. |
| 29 | There is no expedited path for cap requests. | 37 | carried | 'There is no expedited path' in `merged.md` -- Stated directly. |
| 30 | An answer takes two working days. | 37 | carried | 'An answer takes two working days' in `merged.md` -- Stated directly. |

### `merged.md` -- 27 claim(s): 0 invented, 0 contradicted, 0 supported in part, 27 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | When a credential's cap is spent, the gateway answers 429 at the edge without waking the service behind it. | supported | `source_a.md` | 'When that cap is spent the gateway answers 429 at the edge — without waking the service behind it' in `source_a.md` -- Source A states this directly. |
| 2 | Every credential has a cap. | supported | `source_a.md` | 'Every credential has a cap.' in `source_a.md` -- Stated verbatim. |
| 3 | Requests are counted against the credential that presented them, and never against a connection. | supported | `source_a.md` | 'Requests are counted against the credential that presented them, over a fixed window of 60 seconds, and never against a connection.' in `source_a.md` -- Stated directly. |
| 4 | The counting window is a fixed window of 60 seconds. | supported | `source_a.md` | 'over a fixed window of 60 seconds' in `source_a.md` -- Stated directly. |
| 5 | The gateway does not disclose the start of the counting window. | supported | `source_b.md` | 'over a fixed window of 60 seconds whose start the gateway doesn’t disclose' in `source_b.md` -- Source B states the start is not disclosed. |
| 6 | The count follows the credential across hosts. | supported | `source_b.md` | 'The count follows the credential wherever the caller happens to put it, including across hosts.' in `source_b.md` -- Stated directly. |
| 7 | A client spread across eight worker processes is throttled at exactly the point one process would have been. | supported | `source_a.md` | 'A client spread across eight worker processes is throttled at exactly the point one process would have been' in `source_a.md` -- Stated directly. |
| 8 | The default allowance is 100 requests in a window. | supported | `source_b.md` | 'The default allowance is 100 requests in a window' in `source_b.md` -- Stated directly. |
| 9 | A credential marked for batch work is allowed 1000 requests in the same window. | supported | `source_a.md` | 'a credential marked for batch work is allowed 1000 in the same window' in `source_a.md` -- Stated directly. |
| 10 | The refusal carries a Retry-After header. | supported | `source_a.md` | 'The refusal carries a Retry-After header.' in `source_a.md` -- Stated directly. |
| 11 | The Retry-After value is a whole number of seconds to wait. | supported | `source_a.md` | 'Its value is a whole number of seconds to wait.' in `source_a.md` -- Stated directly. |
| 12 | The Retry-After header is present on every refusal the gateway sends. | supported | `source_b.md` | 'it is present on every refusal the gateway sends' in `source_b.md` -- Stated directly. |
| 13 | The gateway keeps no memory of who backed off politely. | supported | `source_a.md` | 'The gateway keeps no memory of who backed off politely' in `source_a.md` -- Stated directly. |
| 14 | The body of the refusal is JSON. | supported | `source_a.md` | 'The body of the refusal is JSON' in `source_a.md` -- Stated directly. |
| 15 | The refusal body repeats the cap, the window the gateway counted in, and the tier as plain fields. | supported | `source_b.md` | 'The response body is JSON and it repeats the cap, the window and the tier as plain fields.' in `source_b.md` -- Stated directly. |
| 16 | A batch credential is allowed 1000 requests in a window, which is 50 times the default. | supported | `source_b.md` | 'A batch credential is allowed 1000 requests in a window, which is 50 times the default' in `source_b.md` -- Stated directly. |
| 17 | The batch tier is measured over exactly the same window as the default tier. | supported | `source_a.md` | 'it is measured over exactly the same window' in `source_a.md` -- Source A says batch is measured over exactly the same window. |
| 18 | The header and the body of a refusal are identical for the batch and interactive cases. | supported | `source_b.md` | 'The window, the header and the body are identical to the interactive case' in `source_b.md` -- Stated directly. |
| 19 | The tier is set on the credential when it is issued and cannot be asked for per call. | supported | `source_a.md` | 'The tier is set on the credential when it is issued and cannot be asked for per call.' in `source_a.md` -- Stated directly. |
| 20 | On the 503 path the Retry-After rule holds too. | supported | `source_b.md` | 'On the 503 path the same rule holds' in `source_b.md` -- Stated directly. |
| 21 | A 503 means the platform itself is overloaded. | supported | `source_b.md` | 'a 503 means the platform itself is overloaded' in `source_b.md` -- Stated directly. |
| 22 | The gateway refuses a request for three reasons. | supported | `source_a.md` | 'The gateway refuses a request for three reasons' in `source_a.md` -- Stated directly. |
| 23 | A body may exceed the 5 megabyte limit and is then refused before it has been read at all. | supported | `source_b.md` | 'a request body over the 5 megabyte limit is refused before it has been read at all' in `source_b.md` -- Stated directly. |
| 24 | A credential may be suspended, and a route may be closed for maintenance. | supported | `source_a.md` | 'A credential may be suspended, a route may be closed for maintenance' in `source_a.md` -- Stated directly. |
| 25 | The number of caps raised without a measurement behind them is 0. | supported | `source_a.md` | 'the number of caps raised without a measurement behind them is 0' in `source_a.md` -- Stated directly. |
| 26 | Requests to the platform team are answered within two working days. | supported | `source_a.md` | 'they are answered within two working days' in `source_a.md` -- Stated directly. |
| 27 | There is no expedited path and no exception list. | supported | `source_a.md` | 'There is no expedited path and no exception list.' in `source_a.md` -- Stated verbatim. |

## Structure

**9** mechanical check(s) over **104** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **27** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **58**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 26 run(s) over 58 attributed segment(s) — sources interleaved. 6 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

`[-...-]` is what the source said and `{+...+}` is what the merge says.

### Declared gone, still here — a record says the content departed and the merge carries the segment unchanged

- `b24` (`source_b.md`) — 'On the 503 path the same rule holds, even though the cause of the refusal is an entirely different one.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: On the 503 path the same rule holds, even though the cause of the refusal is an entirely different one.
  In the merge:  On the 503 path the same rule holds, even though the cause of the refusal is an entirely different one.
  ```
- `b27` (`source_b.md`) — 'Retry only what is safe to retry, which is a smaller set than the set of responses that aren’t a success.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Retry only what is safe to retry, which is a smaller set than the set of responses that aren’t a success.
  In the merge:  2. Retry only what is safe to retry, which is a smaller set than the set of responses that aren’t a success.
  What changed:  {+2.+} Retry only what is safe to retry, which is a smaller set than the set of responses that aren’t a success.
  ```

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **64** departure(s) from its sources. Checking them confirms 27, rejects 12, and leaves 25 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 104 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | Base title kept. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Rate limiting and the 429 contract for gateway clients' and says so (no claim traced to it) |
| `b2` | duplicate | Same as a2. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-001`) |
| `b3` | duplicate | Same as a3. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-002`) |
| `b4` | reworded | Recast as general statement, not draft history. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a4` | reworded | Combined with b5's undisclosed window start. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-002`, `A-003`, `A-004`) |
| `b5` | subsumed | Carried in the combined counting sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-003`, `B-004`, `B-005`) |
| `b6` | duplicate | Same as a5. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b7` | reworded | Trimmed wording. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-006`) |
| `b8` | duplicate | Same as a6. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-007`) |
| `a7` | reworded | Split from default allowance sentence. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-006`, `A-007`) |
| `b9` | subsumed | Carried in default allowance sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-008`, `B-009`) |
| `a8` | reworded | Merged with b10's not-a-bug point. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b10` | subsumed | Carried alongside a8/a9. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b11` | duplicate | Same as a10. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'duplicate' is what happened to it (no claim traced to it) |
| `b13` | duplicate | Same as a12. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-010`) |
| `a13` | reworded | Combined with b14. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-009`) |
| `b14` | subsumed | Carried in combined sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-011`, `B-012`) |
| `b15` | duplicate | Same as a14. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b16` | duplicate | Same as a15. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `a16` | reworded | Combined with a17 and b17. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-011`, `A-012`) |
| `a17` | subsumed | Carried in combined body sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-013`) |
| `b17` | subsumed | Carried in combined body sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-013`, `B-014`) |
| `b18` | duplicate | Same as a18. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'duplicate' is what happened to it (no claim traced to it) |
| `b19` | duplicate | Same as a19. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b20` | superseded | Base heading kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b21` | duplicate | Same as a21. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `a22` | reworded | Combined with b22. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b22` | subsumed | Carried in rule 1 heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a23` | reworded | Combined with b23 and b24. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-014 came back PARTIAL (`A-014`) |
| `b23` | duplicate | Same as a23. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'duplicate' is what happened to it (no claim traced to it) |
| `b24` | subsumed | Carried in rule 1. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b25` | duplicate | Same as a24. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b26` | duplicate | Same as a25. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `a26` | reworded | Combined with b27. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b27` | subsumed | Carried in rule 2 heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a27` | reworded | Used b28's clearer 503 wording. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-015`, `A-016`) |
| `b28` | subsumed | Carried in rule 2. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-015`, `B-016`, `B-017`, `B-018`) |
| `b29` | duplicate | Same as a29. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'duplicate' is what happened to it (no claim traced to it) |
| `b30` | duplicate | Same as a30. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `a32` | reworded | Combined with b31. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-017`, `A-018`) |
| `b31` | subsumed | Carried in rule 3. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-019`, `B-020`) |
| `b32` | subsumed | Carried in rule 3. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-021`) |
| `b33` | duplicate | Same as a34. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-022`) |
| `a35` | reworded | Combined with b34. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b34` | subsumed | Carried in rule 4 heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b35` | duplicate | Same as a36. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'duplicate' is what happened to it (no claim traced to it) |
| `b37` | superseded | Base heading kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b38` | duplicate | Same as a40. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-023`) |
| `a41` | reworded | Combined with b40. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-022`, `A-023`, `A-024`) |
| `b40` | subsumed | Carried in combined sentence. | **rejected** | declared 'subsumed', which predicts SUPPORTED; B-025 came back PARTIAL (`B-025`) |
| `b41` | duplicate | Same as a43. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `a44` | reworded | Combined with b43. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b42` | duplicate | Same as a44. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b43` | subsumed | Carried in a44 sentence. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a47` | reworded | Combined with b46. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-025`) |
| `b46` | subsumed | Carried in combined sentence. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a48` | reworded | Combined with b47's full week. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b47` | subsumed | Carried in combined sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-027`) |
| `a49` | reworded | Combined with b48 and b49. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b48` | subsumed | Carried in combined sentence. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b49` | subsumed | Carried in combined sentence. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b44` | duplicate | Same as a50. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'duplicate' is what happened to it (no claim traced to it) |
| `b50` | duplicate | Same as a51. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-028`) |
| `b51` | duplicate | Same as a52. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-029`) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | e52670eb755f (command) -- Claude Code - Sonnet |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | sonnet -> claude-sonnet-5 |
| Model (decompose) | sonnet -> claude-sonnet-5 |
| Model (verify) | sonnet -> claude-sonnet-5 |
| Structured output | prompt (probed) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile subscription, effort decompose=low, merge=medium, verify=low |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 6cc1b1703658 |
| Calls | 6 live, 0 cached, 0 replayed |
| Tokens | unknown (6 call(s) reported no usage) |
| Cost | unmeasured (6 call(s) reported no tokens, so no figure can be derived) |
| Schema repairs | 0 |
| Isolation | decompose, merge, verify: safe mode, no tools |
| Errors | 0 |
| Duration | 157.0s |
| Generated | 2026-09-26T15:32:03+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `5afca8163bfa` |
| Prompt | `prompts/verify_reverse.md` `cb2face6b7f4` |

> **Document content was handed to a program on this machine (`Claude Code - Sonnet`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
