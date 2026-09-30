## Verdict

**13 finding(s).** In the claims: 3 dropped, 2 partially dropped, 1 contradicted. In the structure: 2 undeclared absence, 1 undeclared rewording, 1 false departure, 2 verbatim violation, 1 declared loss over budget. The merge declared **6** drop(s) of 104 source segment(s), **5.8%**, over the 3% budget: past that share the omissions are the finding, whatever each one says about itself. The 2 claim(s) they cost are listed in the review queue below.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 17 |
| Claims extracted from `source_a.md` | 16 |
| Claims extracted from `source_b.md` | 28 |
| Forward — source claims accounted for in the merge | **37/44** |
| Forward — carried only in part | 2 |
| Forward — `source_a.md` claims accounted for | **16/16** |
| Forward — `source_b.md` claims accounted for | **21/28** (2 in part) |
| Reverse — merge claims found in a source | **16/17** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **56/56** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Dropped — in a source, not in the merge

- **B-009** (`source_b.md:11`) — The Retry-After header is present on every refusal the gateway sends.
  - judged against: `merged.md`
  - rationale: The reference text states the refusal carries the Retry-After header but does not assert it is present on every refusal the gateway sends.
- **B-015** (`source_b.md:21`) — A 503 means the platform itself is overloaded.
  - judged against: `merged.md`
  - rationale: The reference text describes 503 as the overload path but does not state that 503 means the platform itself is overloaded.
- **B-026** (`source_b.md:29`) — A request body over the 5 megabyte limit is refused before it has been read at all.
  - judged against: `merged.md`
  - rationale: The reference text mentions a 5 megabyte limit but does not state that bodies exceeding it are refused before being read.

### Partly dropped — the merge carries some of this claim

- **B-003** (`source_b.md:5`) — Requests are counted against the credential rather than the connection, over a fixed window of 60 seconds whose start the gateway doesn't disclose.
  - evidence: 'Requests are counted against the credential that presented them, over a fixed window of 60 seconds, and never against a connection.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text states requests are counted over a fixed 60-second window against the credential, but does not state the gateway doesn't disclose the window start.
- **B-004** (`source_b.md:5`) — The count follows the credential wherever the caller happens to put it, including across hosts.
  - evidence: 'A client spread across multiple worker processes or hosts is throttled at the same point a single process would have been.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text states throttling applies across hosts, but uses different phrasing than 'the count follows the credential wherever the caller happens to put it'.

### Contradicted — the merge states something different

- **M-013** -- the two documents disagree
  - `merged.md:29` says: A body may exceed the 5 megabyte limit.
  - `source_a.md` says: 'a body may exceed the 5 megabyte limit' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source A states a body exceeding the 5MB limit is refused; the claim inverts this by stating it may exceed the limit.

## Length capped

- `$.dispositions[5].reason` was 95 characters, over the 80-character cap; capped to fit

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 16 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 16 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Requests are counted against the credential that presented them, over a fixed window of 60 seconds, and never against a connection. | 5 | carried | 'Requests are counted against the credential that presented them, over a fixed window of 60 seconds, and never against a connection.' in `merged.md` -- The reference text states this claim verbatim in the second paragraph. |
| 2 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- The reference text states the default allowance is 100 requests in a window in the third paragraph. |
| 3 | A credential marked for batch work is allowed 1000 in the same window. | 7 | carried | 'a credential marked for batch work is allowed 1000 in the same window' in `merged.md` -- The reference text states batch credentials are allowed 1000 requests in the same window in the third paragraph. |
| 4 | The refusal carries a Retry-After header. | 11 | carried | 'The refusal carries a Retry-After header.' in `merged.md` -- The reference text states this claim in the first sentence of the 'How to read a refusal' section. |
| 5 | The Retry-After header value is a whole number of seconds to wait. | 11 | carried | 'Its value is a whole number of seconds to wait.' in `merged.md` -- The reference text describes the Retry-After header value as a whole number of seconds in the 'How to read a refusal' section. |
| 6 | The body of the refusal is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- The reference text states the refusal body is JSON in the second paragraph of 'How to read a refusal'. |
| 7 | The body of the refusal names what the gateway calls the "window" it counted in. | 13 (unverified) | carried | 'It names what the gateway calls the "window" it counted in.' in `merged.md` -- The reference text states the body names the window in the second paragraph of 'How to read a refusal'. |
| 8 | The body of the refusal names the cap and the tier. | 13 | carried | 'It names the cap and the tier as well.' in `merged.md` -- The reference text states the body names the cap and tier in the second paragraph of 'How to read a refusal'. |
| 9 | A batch credential is allowed fifty times the default allowance. | 23 | carried | 'A batch credential is allowed fifty times the default allowance' in `merged.md` -- The reference text states batch credentials are allowed fifty times the default allowance in the first rule under 'How to retry well'. |
| 10 | A batch credential is measured over exactly the same window as the default allowance. | 23 | carried | 'and it is measured over exactly the same window' in `merged.md` -- The reference text states batch credentials are measured over the same window in the third rule under 'How to retry well'. |
| 11 | The tier is set on the credential when it is issued and cannot be asked for per call. | 23 | carried | 'The tier is set on the credential when it is issued and cannot be asked for per call.' in `merged.md` -- The reference text states this claim in the third rule under 'How to retry well'. |
| 12 | The gateway refuses a request for three reasons. | 29 | carried | 'The gateway refuses a request for three reasons and only one of them is the one above.' in `merged.md` -- The reference text states the gateway refuses for three reasons in 'Other refusals and their codes'. |
| 13 | A credential may be suspended. | 29 | carried | 'A credential may be suspended' in `merged.md` -- The reference text lists credential suspension as one of three reasons for refusal in 'Other refusals and their codes'. |
| 14 | A route may be closed for maintenance. | 29 | carried | 'a route may be closed for maintenance' in `merged.md` -- The reference text lists route closure for maintenance as one of three reasons for refusal in 'Other refusals and their codes'. |
| 15 | A body may exceed the 5 megabyte limit. | 29 | carried | 'or a body may exceed the 5 megabyte limit' in `merged.md` -- The reference text lists body size exceeding 5 megabytes as one of three reasons for refusal in 'Other refusals and their codes'. |
| 16 | Requests are answered within two working days. | 37 | carried | 'they are answered within two working days' in `merged.md` -- The reference text states requests to the platform team are answered within two working days in 'Asking for an increase'. |

### `source_b.md` -- 28 claim(s): 5 dropped, 0 contradicted, 2 carried in part, 21 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 9 | The Retry-After header is present on every refusal the gateway sends. | 11 | dropped | The reference text states the refusal carries the Retry-After header but does not assert it is present on every refusal the gateway sends. |
| 15 | A 503 means the platform itself is overloaded. | 21 | dropped | The reference text describes 503 as the overload path but does not state that 503 means the platform itself is overloaded. |
| 19 | The window, the header and the body are identical in the interactive case and the batch case. | 23 | dropped | The reference text does not compare the window, header and body between interactive and batch cases. |
| 20 | A client written for one tier needs no change at all to run against the other tier. | 23 | dropped | The reference text does not state whether a client written for one tier needs no changes to run against the other. |
| 26 | A request body over the 5 megabyte limit is refused before it has been read at all. | 29 | dropped | The reference text mentions a 5 megabyte limit but does not state that bodies exceeding it are refused before being read. |
| 3 | Requests are counted against the credential rather than the connection, over a fixed window of 60 seconds whose start the gateway doesn't disclose. | 5 (unverified) | carried in part | 'Requests are counted against the credential that presented them, over a fixed window of 60 seconds, and never against a connection.' in `merged.md` -- The text states requests are counted over a fixed 60-second window against the credential, but does not state the gateway doesn't disclose the window start. |
| 4 | The count follows the credential wherever the caller happens to put it, including across hosts. | 5 | carried in part | 'A client spread across multiple worker processes or hosts is throttled at the same point a single process would have been.' in `merged.md` -- The text states throttling applies across hosts, but uses different phrasing than 'the count follows the credential wherever the caller happens to put it'. |
| 1 | Every credential has a cap of its own. | 3 | carried | 'Every credential has a cap.' in `merged.md` -- The reference text states this claim in the opening sentence. |
| 2 | When the cap is spent the gateway answers 429 at the edge, without troubling the service behind it. | 3 | carried | 'When that cap is spent the gateway answers 429 at the edge — without waking the service behind it' in `merged.md` -- The reference text states the gateway answers 429 without troubling the service when the cap is spent. |
| 5 | A caller spread over many worker processes is throttled at the same point a single process would have been. | 5 | carried | 'A client spread across multiple worker processes or hosts is throttled at the same point a single process would have been.' in `merged.md` -- The reference text states this claim about throttling across worker processes in the second paragraph. |
| 6 | The default allowance is 100 requests in a window. | 7 | carried | 'The default allowance is 100 requests in a window' in `merged.md` -- The reference text states the default allowance is 100 requests in the third paragraph. |
| 7 | The header is called Retry-After. | 11 | carried | 'The refusal carries a Retry-After header.' in `merged.md` -- The reference text identifies the header as Retry-After in the 'How to read a refusal' section. |
| 8 | The value of Retry-After is a whole number of seconds. | 11 | carried | 'Its value is a whole number of seconds to wait.' in `merged.md` -- The reference text describes the Retry-After value as a whole number of seconds in 'How to read a refusal'. |
| 10 | The response body is JSON. | 13 | carried | 'The body of the refusal is JSON' in `merged.md` -- The reference text explicitly states that the refusal body is JSON. |
| 11 | The response body repeats the cap, the window and the tier as plain fields. | 13 | carried | 'It names what the gateway calls the "window" it counted in. It names the cap and the tier as well.' in `merged.md` -- The reference text states the body names the window, cap, and tier as fields. |
| 12 | A 200 needs nothing. | 21 | carried | 'A 200 wants nothing' in `merged.md` -- The reference text directly states that a 200 response wants nothing. |
| 13 | A 429 needs the stated wait. | 21 | carried | 'a 429 wants the stated wait' in `merged.md` -- The reference text directly states that a 429 response wants the stated wait. |
| 14 | A 500 can be retried once that wait has passed. | 21 | carried | 'a 500 may be retried once that wait has passed' in `merged.md` -- The reference text directly states that a 500 may be retried once that wait has passed. |
| 16 | A batch credential is allowed 1000 requests in a window. | 23 | carried | 'a credential marked for batch work is allowed 1000 in the same window' in `merged.md` -- The reference text explicitly states a batch credential is allowed 1000 requests in a window. |
| 17 | A batch credential's allowance is 50 times the default. | 23 | carried | 'A batch credential is allowed fifty times the default allowance' in `merged.md` -- The reference text states a batch credential's allowance is fifty times the default. |
| 18 | The batch tier is not a separate counting scheme. | 23 | carried | 'it is measured over exactly the same window' in `merged.md` -- The reference text states batch is measured over exactly the same window as default, entailing they use the same counting scheme. |
| 21 | Nothing else about the batch tier differs from the default. | 23 | carried | 'Nothing else about the two tiers differs in any way.' in `merged.md` -- The reference text explicitly states nothing else about the two tiers differs in any way. |
| 22 | The gateway refuses a request for three separate reasons. | 29 | carried | 'The gateway refuses a request for three reasons and only one of them is the one above.' in `merged.md` -- The reference text states the gateway refuses for three reasons, entailing three separate reasons. |
| 23 | Only one of the three reasons the gateway refuses a request is a cap. | 29 | carried | 'The gateway refuses a request for three reasons and only one of them is the one above.' in `merged.md` -- The reference text explicitly states only one of the three reasons is a cap (the topic of the section above). |
| 24 | A credential can be suspended. | 29 | carried | 'A credential may be suspended' in `merged.md` -- The reference text directly states a credential may be suspended. |
| 25 | A route can be closed while it is being repaired. | 29 | carried | 'a route may be closed for maintenance' in `merged.md` -- The reference text states a route may be closed for maintenance, which is consistent with the claim. |
| 27 | An answer from the platform team takes two working days. | 37 | carried | 'they are answered within two working days' in `merged.md` -- The reference text states platform team answers requests within two working days. |
| 28 | Chasing an answer from the platform team doesn't make it take fewer days. | 37 (unverified) | carried | 'There is no expedited path and no exception list.' in `merged.md` -- The reference text states there is no expedited path, entailing chasing an answer does not make it take fewer days. |

### `merged.md` -- 17 claim(s): 0 invented, 1 contradicted, 0 supported in part, 16 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 13 | A body may exceed the 5 megabyte limit. | contradicted | `source_a.md` | 'a body may exceed the 5 megabyte limit' in `source_a.md` -- Source A states a body exceeding the 5MB limit is refused; the claim inverts this by stating it may exceed the limit. |
| 1 | Requests are counted against the credential that presented them, over a fixed window of 60 seconds. | supported | `source_a.md` | 'Requests are counted against the credential that presented them, over a fixed window of 60 seconds' in `source_a.md` -- Source A states this claim verbatim. |
| 2 | Requests are never counted against a connection. | supported | `source_a.md` | 'and never against a connection' in `source_a.md` -- Source A explicitly states requests are never counted against a connection. |
| 3 | The default allowance is 100 requests in a window. | supported | `source_a.md` | 'The default allowance is 100 requests in a window' in `source_a.md` -- Source A states this claim verbatim. |
| 4 | A credential marked for batch work is allowed 1000 in the same window. | supported | `source_a.md` | 'a credential marked for batch work is allowed 1000 in the same window' in `source_a.md` -- Source A states this claim verbatim. |
| 5 | The refusal carries a Retry-After header. | supported | `source_a.md` | 'The refusal carries a Retry-After header' in `source_a.md` -- Source A states this claim verbatim. |
| 6 | The value of the Retry-After header is a whole number of seconds to wait. | supported | `source_a.md` | 'Its value is a whole number of seconds to wait' in `source_a.md` -- Source A states the Retry-After header value is a whole number of seconds to wait. |
| 7 | The body of the refusal is JSON. | supported | `source_a.md` | 'The body of the refusal is JSON' in `source_a.md` -- Source A states this claim verbatim. |
| 8 | A batch credential is allowed fifty times the default allowance. | supported | `source_a.md` | 'A batch credential is allowed fifty times the default allowance' in `source_a.md` -- Source A states this claim verbatim in the batch rules section. |
| 9 | A batch credential is measured over exactly the same window as the default allowance. | supported | `source_a.md` | 'and it is measured over exactly the same window' in `source_a.md` -- Source A states batch credentials are measured over exactly the same window as default. |
| 10 | The tier for a batch credential is set on the credential when it is issued. | supported | `source_a.md` | 'The tier is set on the credential when it is issued' in `source_a.md` -- Source A states this claim verbatim. |
| 11 | The tier for a batch credential cannot be asked for per call. | supported | `source_a.md` | 'and cannot be asked for per call' in `source_a.md` -- Source A states the tier cannot be asked for per call. |
| 12 | The gateway refuses a request for three reasons. | supported | `source_a.md` | 'The gateway refuses a request for three reasons and only one of them is the one above' in `source_a.md` -- Source A states the gateway refuses a request for three reasons. |
| 14 | Requests reach the platform team through the usual channel. | supported | `source_a.md` | 'Requests reach the platform team through the usual channel' in `source_a.md` -- Source A states this claim verbatim. |
| 15 | Requests to the platform team are answered within two working days. | supported | `source_a.md` | 'they are answered within two working days' in `source_a.md` -- Source A states requests are answered within two working days. |
| 16 | There is no expedited path for requesting a cap increase. | supported | `source_a.md` | 'There is no expedited path' in `source_a.md` -- Source A states there is no expedited path for requesting cap increases. |
| 17 | There is no exception list for requesting a cap increase. | supported | `source_a.md` | 'and no exception list' in `source_a.md` -- Source A states there is no exception list for cap increase requests. |

## Structure

**9** mechanical check(s) over **104** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **17** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **44**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 5 run(s) over 51 attributed segment(s) — sources interleaved. 6 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

`[-...-]` is what the source said and `{+...+}` is what the merge says.

### Absent and undeclared — in a source, not in the merge, and no record explains it

- `a47` (`source_a.md`) — 'A cap can be raised, and the number of caps raised without a measurement behind them is 0.' is not in the merge and no disposition record explains it (nearest merge segment m47 at 0.58)

  ```text
  In the source: A cap can be raised, and the number of caps raised without a measurement behind them is 0.
  ```
- `b20` (`source_b.md`) — 'What the client does' is not in the merge and no disposition record explains it (nearest merge segment m38 at 0.44)

  ```text
  In the source: What the client does
  ```

### Reworded and undeclared — in the merge in altered wording, and no record explains it. At off this also covers layout: a segment whose source line breaks the merge ran together is altered and undeclared, and 380 reuses this kind rather than moving FINDING_KINDS off 12

- `a16` (`source_a.md`) — 'The body of the refusal is JSON, and it names what the gateway calls the “window” it counted in.' is reworded in the merge and no disposition record explains it (nearest merge segment m16 at 0.98)

  ```text
  In the source: The body of the refusal is JSON, and it names what the gateway calls the “window” it counted in.
  In the merge:  The body of the refusal is JSON, and it names what the gateway calls the "window" it counted in.
  What changed:  The body of the refusal is JSON, and it names what the gateway calls the [-“window”-] {+"window"+} it counted in.
  ```

### Declared gone, still here — a record says the content departed and the merge carries the segment unchanged

- `b46` (`source_b.md`) — 'A cap can be raised, but not on the strength of an assertion that the current one is too small.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: A cap can be raised, but not on the strength of an assertion that the current one is too small.
  In the merge:  A cap can be raised, but not on the strength of an assertion that the current one is too small.
  ```

### Verbatim violation — an invariant-core token did not survive unchanged

- `a47` (`source_a.md`) — numeric '0' does not survive into the merge unchanged
- `b31` (`source_b.md`) — numeric '50' (times) does not survive into the merge unchanged

### Over budget — declared loss past the ceiling

- 6 of 104 segments are declared dropped (5.8%), over the 3% budget

## Review queue

**2** claim(s) the merge declared dropped and the forward pass confirms are gone. Each is a decision to review — put the fact back, or agree it stays out — and none of them is counted as a finding above.

- **B-019** (`source_b.md:23`) — The window, the header and the body are identical in the interactive case and the batch case.
  - left out of: `b32`
  - the merge's reason: Assertion about identical headers not supported by base doc.
  - confirmed absent: the forward pass looked for this claim in `merged.md` and did not find it -- The reference text does not compare the window, header and body between interactive and batch cases.
- **B-020** (`source_b.md:23`) — A client written for one tier needs no change at all to run against the other tier.
  - left out of: `b32`
  - the merge's reason: Assertion about identical headers not supported by base doc.
  - confirmed absent: the forward pass looked for this claim in `merged.md` and did not find it -- The reference text does not state whether a client written for one tier needs no changes to run against the other.

> **Over budget.** The merge declared **6** drop(s) of 104 source segment(s), **5.8%**, over the 3% budget: past that share the omissions are the finding, whatever each one says about itself.

## Declarations

The merge declared **51** departure(s) from its sources. Checking them confirms 17, rejects 4, and leaves 30 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 6 of 104 source segment(s) declared gone, **5.8%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a6` | reworded | Combined with b7 fact about hosts; clearer and more general. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b1` | superseded | Base document title was chosen over source_b.md title. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Rate limiting and the 429 contract for gateway clients' and says so (no claim traced to it) |
| `b2` | subsumed | Same fact carried in opening sentence; redundant version dropped. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-001`) |
| `b3` | subsumed | Same fact in a1 and a3 combined; b3 version superseded. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-002`) |
| `b4` | dropped | Editorial note about omission; not part of documentation. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b5` | subsumed | Same essential fact in a4; b5's detail about gateway not disclosing start is not | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b6` | subsumed | Same meaning as a5; a5 version carried. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b7` | reconciled | Combined with a6 to cover both processes and hosts. | **rejected** | declared 'reconciled', which predicts SUPPORTED; B-004 came back PARTIAL (`B-004`) |
| `b8` | subsumed | Same fact as a6 combined with b7; b8 version subsumed. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-005`) |
| `b9` | subsumed | Same facts in a7; b9's explanatory context not essential. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-006`) |
| `b10` | subsumed | Same facts in a8 and a9; b10 version superseded. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b11` | subsumed | Same fact as a10; b11 version superseded. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b13` | subsumed | Same fact in a12; b13 just names it differently. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-007`) |
| `b14` | subsumed | Same fact as a13; redundant version dropped. | **rejected** | declared 'subsumed', which predicts SUPPORTED; B-009 came back MISSING (`B-009`) |
| `b15` | subsumed | Same fact as a14; b15's framing about outcome subsumed. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b16` | subsumed | Same fact as a15; b16 phrasing subsumed. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b17` | subsumed | Same facts as a16 and a17; b17 combined version superseded. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-010`, `B-011`) |
| `b18` | subsumed | Same fact as a18; b18 phrasing subsumed. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b19` | subsumed | Same fact as a19; b19 phrasing subsumed. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b21` | subsumed | Same opening as a21; redundant version dropped. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b22` | superseded | a22 version chosen; more emphatic and complete. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b23` | subsumed | Comparable to a23; a23 version carried. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b24` | subsumed | Same point as a23; b24's detail subsumed. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b25` | subsumed | Same fact as a24; b25 phrasing subsumed. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b26` | subsumed | Same fact as a25; b26 phrasing subsumed. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b27` | superseded | a26 heading chosen; simpler and clearer. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b28` | subsumed | Same codes in a27; a27 version carried. | **rejected** | declared 'subsumed', which predicts SUPPORTED; B-015 came back MISSING (`B-015`) |
| `b29` | subsumed | Same fact as a29; a29 version carried. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b30` | subsumed | Same point as a30; redundant version dropped. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b31` | reworded | a32 wording chosen; clearer than b31's specific number mention. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-016`, `B-017`, `B-018`) |
| `b32` | dropped | Assertion about identical headers not supported by base doc. | **confirmed** | declared 'dropped' and every claim from it came back MISSING (`B-019`, `B-020`) |
| `b33` | subsumed | Same fact as a34; redundant version dropped. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-021`) |
| `b34` | superseded | a35 imperative chosen; more direct. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b35` | subsumed | Same fact as a36; a36 version carried. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b36` | dropped | Meta-observation about argument strength; not essential. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b37` | superseded | a39 and a40 version chosen; clearer structure. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b38` | subsumed | Same fact as a40; a40 version carried. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-022`, `B-023`) |
| `b39` | dropped | Analytical detail about reasons; not essential to documentation. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b40` | subsumed | Same three reasons as a41; a41 version carried. | **rejected** | declared 'subsumed', which predicts SUPPORTED; B-026 came back MISSING (`B-026`) |
| `b41` | subsumed | Same fact as a43; a43 version carried. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b42` | subsumed | Same fact as a44; a44 version carried. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b43` | dropped | Explains impact of wasted budget; not essential to the rule. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b44` | subsumed | Same fact as a50; a50 version carried with stronger result. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b45` | dropped | Meta-assessment of fix availability; not essential. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b46` | subsumed | Same fact as a47; reworded for clarity at high fidelity. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b47` | subsumed | Same fact as a48; a48 version carried. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b48` | reworded | b48 and a49 combined; a49 phrasing chosen for clarity. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b49` | subsumed | Same fact as a49; a49 version carried. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b50` | subsumed | Same fact as a51; a51 version carried. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b51` | subsumed | Same fact as a52; a52 version carried. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b52` | subsumed | Same fact as a51; a51 version carried. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-027`) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | ec0c9ecb43e3 (hosted) |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | claude-haiku-4-5-20251001 |
| Model (decompose) | claude-haiku-4-5-20251001 |
| Model (verify) | claude-haiku-4-5-20251001 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile anthropic, effort decompose one level (extended thinking on/off; default kept), merge one level (extended thinking on/off; default kept), verify one level (extended thinking on/off; default kept) |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 9 live, 0 cached, 0 replayed |
| Tokens | 32,051 in, 16,812 out |
| Cost | ~$0.12 estimated (rates read 2026-08-31) |
| Schema repairs | 2 |
| Errors | 0 |
| Duration | 129.7s |
| Generated | 2026-09-27T16:41:11+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
