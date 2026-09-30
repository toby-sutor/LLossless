## Verdict

**12 finding(s).** In the claims: 4 dropped, 2 contradicted. In the structure: 1 undeclared absence, 1 unresolved replacement, 2 verbatim violation, 2 declared loss over budget. The merge declared **10** drop(s) of 63 source segment(s), **15.9%**, over the 3% budget: past that share the omissions are the finding, whatever each one says about itself. The 5 claim(s) they cost are listed in the review queue below.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 18 |
| Claims extracted from `source_a.md` | 29 |
| Claims extracted from `source_b.md` | 15 |
| Forward — source claims accounted for in the merge | **33/44** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **29/29** |
| Forward — `source_b.md` claims accounted for | **4/15** |
| Reverse — merge claims found in a source | **18/18** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **51/53** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Dropped — in a source, not in the merge

- **B-003** (`source_b.md:8`) — The managed Nimbrel Ledger deployment's share of HTTP 429 replies climbed over a fortnight.
  - judged against: `merged.md`
  - rationale: The reference text does not specify a fortnight timeframe; it only mentions 'over time'.
- **B-011** (`source_b.md:24`) — A handful of queries run for as long as 2 seconds each.
  - judged against: `merged.md`
  - rationale: The reference text does not specify a query duration of 2 seconds.
- **B-012** (`source_b.md:24`) — A worker slot is unavailable for as long as one of the expensive queries holds it.
  - judged against: `merged.md`
  - rationale: The reference text does not state how long a worker slot is unavailable.
- **B-013** (`source_b.md:25`) — Grouping on channel.id yields a very large number of groups.
  - judged against: `merged.md`
  - rationale: The reference text mentions 'deep grouping operations' but does not specify grouping on channel.id.

### Contradicted — the merge states something different

- **B-001** -- the two documents disagree
  - `source_b.md:3` says: The document was authored by Devin Okonkwo.
  - `merged.md` says: 'Author: Priya Raghunathan' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The document's author is Priya Raghunathan, not Devin Okonkwo.
- **B-002** -- the two documents disagree
  - `source_b.md:4` says: The document was updated on 2026-04-11.
  - `merged.md` says: 'Updated: 2026-03-18' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The document was updated on 2026-03-18, not 2026-04-11.

## Length capped

- `$.dispositions[18].reason` was 90 characters, over the 80-character cap; capped to fit

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 29 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 29 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Author of the document is Priya Raghunathan. | 3 | carried | 'Author: Priya Raghunathan' in `merged.md` -- The document header explicitly states the author as Priya Raghunathan. |
| 2 | The document was updated on 2026-03-18. | 4 | carried | 'Updated: 2026-03-18' in `merged.md` -- The document header explicitly states the update date as 2026-03-18. |
| 3 | Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests`. | 8 | carried | 'Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests`.' in `merged.md` -- The first sentence of the Issue Description section directly states this claim. |
| 4 | Nimbrel Relay stalls when appends are refused. | 8 | carried | 'Nimbrel Relay stalls' in `merged.md` -- The Issue Description states that Nimbrel Relay stalls when appends are refused. |
| 5 | Batch loaders resend the same envelope when appends are refused. | 8 | carried | 'batch loaders resend the same envelope' in `merged.md` -- The Issue Description explicitly mentions batch loaders resending the same envelope when appends are refused. |
| 6 | Reads against the same shard begin to time out when appends are refused. | 8 | carried | 'reads against the same shard begin to time out' in `merged.md` -- The Issue Description states that reads against the same shard begin to time out when appends are refused. |
| 7 | The refusal is written to the Relay and Collector logs. | 8 | carried | 'The refusal reaches the client and is written to the Relay and Collector logs as well.' in `merged.md` -- The Issue Description explicitly states that the refusal is written to the Relay and Collector logs. |
| 8 | A full refusal envelope from a batched append shows 0 of 64 envelopes refused. | 13 | carried | 'append batch refused after 0 of 64 envelopes' in `merged.md` -- The refusal envelope example shows 0 of 64 envelopes refused, directly supporting the claim. |
| 9 | The ingest_and_leader_bytes value in the refusal envelope is 88121344. | 13 | carried | 'ingest_and_leader_bytes=88121344' in `merged.md` -- The refusal envelope example explicitly shows this byte value. |
| 10 | The follower_bytes value in the refusal envelope is 212992. | 13 | carried | 'follower_bytes=212992' in `merged.md` -- The refusal envelope example explicitly shows this byte value. |
| 11 | The all_bytes value in the refusal envelope is 88334336. | 13 | carried | 'all_bytes=88334336' in `merged.md` -- The refusal envelope example explicitly shows this byte value. |
| 12 | The ingest_op_bytes value in the refusal envelope is 155648. | 13 | carried | 'ingest_op_bytes=155648' in `merged.md` -- The refusal envelope example explicitly shows this byte value. |
| 13 | The max_ingest_bytes value in the refusal envelope is 88080384. | 13 | carried | 'max_ingest_bytes=88080384' in `merged.md` -- The refusal envelope example explicitly shows this byte value. |
| 14 | Every Nimbrel Ledger release on every platform can refuse an append with HTTP 429. | 20 | carried | 'Every Nimbrel Ledger release on every platform can refuse an append this way.' in `merged.md` -- The Environment section explicitly states this claim. |
| 15 | A Ledger node sends a 429 reply once an append queue or a read queue is full. | 24 | carried | 'once [an append queue or a read queue is full](https://docs.nimbrel.example/ledger/why-appends-are-refused)' in `merged.md` -- The Cause section states that a 429 is sent once an append queue or read queue is full. |
| 16 | The `append` or `system_append` worker pools can refuse appends if they hold more batches than they have slots for. | 28 | carried | 'The `append` or `system_append` worker pools hold more batches than they have slots for' in `merged.md` -- The Cause section lists this as one of the three ways an append draws a 429. |
| 17 | The ingest memory guard can refuse batches. | 29 | carried | 'The ingest memory guard has refused the batch' in `merged.md` -- The Cause section lists this as one of the three ways an append draws a 429. |
| 18 | A circuit breaker can trip and cause a 429 refusal. | 30 | carried | 'A circuit breaker has tripped (`nbctl breaker list --tripped`) - a breaker trips on any operation and is not particular to appends.' in `merged.md` -- The Cause section lists a circuit breaker tripping as one of the three ways to draw a 429. |
| 19 | From release 4.6 and release 5.1 onward, appending to a `wide_text` column draws a 429 whenever the batch would otherwise have run the node out of memory. | 32 (unverified) | carried | '**From release 4.6 and release 5.1 onward**, appending to a `wide_text` column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory.' in `merged.md` -- Footnote [1] in the Cause section explicitly states this claim with the specified version qualifications. |
| 20 | A workaround for refused appends is to take append and query load off the cluster for long enough that the queues drain. | 36 | carried | 'Take append and query load off the cluster for long enough that the queues drain and the nodes fall back under their limits.' in `merged.md` -- The Workaround section explicitly states this as a workaround for refused appends. |
| 21 | Where batches carry `wide_text` columns and the cluster runs release 4.6 or release 5.1 or later, sending fewer envelopes per batch is recommended. | 38 | carried | 'Where batches carry `wide_text` columns and the cluster runs release 4.6 or release 5.1 or later, send fewer envelopes per batch.' in `merged.md` -- The Workaround section explicitly recommends this action for the specified conditions. |
| 22 | A cluster that refuses appends has been given more work than its hardware can carry. | 42 | carried | 'A cluster that refuses appends has been given more work than its hardware can carry' in `merged.md` -- The Resolution section explicitly states this claim. |
| 23 | The resolution for refused appends is hardware: larger nodes (scale up), or more of them (scale out). | 42 | carried | 'the answer is hardware: larger nodes (scale up), or more of them (scale out)' in `merged.md` -- The Resolution section explicitly states these hardware solutions. |
| 24 | Splitting a hot stream over more leader shards spreads append load across more nodes. | 44 | carried | 'Splitting a hot stream over more leader shards spreads append load across more nodes' in `merged.md` -- The Resolution section explicitly states this claim. |
| 25 | The `ingest_guard.memory.leader.ceiling` cluster setting defaults to 10% of the heap. | 50 | carried | 'The setting is read at startup, so the cluster must be restarted for a change to take. Only then raise the `ingest_guard.memory.leader.ceiling` cluster setting, which defaults to 10% of the heap.' in `merged.md`, **transcription_error** -- The Resolution section explicitly states that this setting defaults to 10% of the heap. |
| 26 | A higher `ingest_guard.memory.leader.ceiling` lets a node hold more in-flight append memory before refusing. | 50 | carried | 'A higher ceiling lets a node hold more in-flight append memory before refusing' in `merged.md` -- The reference text directly states that a higher ceiling lets a node hold more in-flight append memory before refusing. |
| 27 | The `ingest_guard.memory.leader.ceiling` setting is read at startup. | 50 | carried | 'The setting is read at startup' in `merged.md` -- The reference text explicitly states that the setting is read at startup. |
| 28 | The cluster must be restarted for a change to the `ingest_guard.memory.leader.ceiling` setting to take effect. | 50 | carried | 'the cluster must be restarted for a change to take' in `merged.md` -- The reference text states that the cluster must be restarted for a change to take effect. |
| 29 | Refusals that show up only during a spike usually clear on their own once the queues drain. | 52 | carried | 'Refusals that show up only during a spike usually clear on their own once the queues drain.' in `merged.md` -- The reference text directly states this claim verbatim. |

### `source_b.md` -- 15 claim(s): 9 dropped, 2 contradicted, 0 carried in part, 4 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 3 | The managed Nimbrel Ledger deployment's share of HTTP 429 replies climbed over a fortnight. | 8 | dropped | The reference text does not specify a fortnight timeframe; it only mentions 'over time'. |
| 5 | The version is 4.4, 5.x. | 13 | dropped | The reference text mentions releases 4.6, 5.1, and later but does not specify versions 4.4 or 5.x. |
| 6 | The platform is Nimbrel Cloud. | 14 | dropped | The reference text does not mention Nimbrel Cloud as the platform. |
| 7 | The deployment is Managed Ledger Service (MLS). | 15 | dropped | The reference text does not mention Managed Ledger Service (MLS) by that acronym or name. |
| 8 | The environment is production. | 16 | dropped | The reference text does not explicitly state that the environment is production. |
| 10 | Front proxy counters agree with client reports. | 20 | dropped | The reference text does not state that front proxy counters agree with client reports. |
| 11 | A handful of queries run for as long as 2 seconds each. | 24 | dropped | The reference text does not specify a query duration of 2 seconds. |
| 12 | A worker slot is unavailable for as long as one of the expensive queries holds it. | 24 | dropped | The reference text does not state how long a worker slot is unavailable. |
| 13 | Grouping on channel.id yields a very large number of groups. | 25 | dropped | The reference text mentions 'deep grouping operations' but does not specify grouping on channel.id. |
| 1 | The document was authored by Devin Okonkwo. | 3 | contradicted | 'Author: Priya Raghunathan' in `merged.md` -- The document's author is Priya Raghunathan, not Devin Okonkwo. |
| 2 | The document was updated on 2026-04-11. | 4 | contradicted | 'Updated: 2026-03-18' in `merged.md` -- The document was updated on 2026-03-18, not 2026-04-11. |
| 4 | The product is Nimbrel Ledger. | 12 | carried | 'Nimbrel Ledger' in `merged.md` -- The document title and content confirm the product is Nimbrel Ledger. |
| 9 | The managed deployment returns HTTP 429 on a growing share of requests. | 20 | carried | 'HTTP `429` replies may grow over time as counted at the front proxy' in `merged.md` -- The reference text states that HTTP 429 replies may grow over time in a managed deployment. |
| 14 | The memory cost of deep grouping is charged to the same pool the append path draws on. | 25 | carried | 'deep grouping operations that consume memory from the same pool the append path draws on' in `merged.md` -- The reference text states that the memory cost of grouping is charged to the same pool the append path uses. |
| 15 | Processor load looks unremarkable while memory sits high. | 26 | carried | 'resource accounting patterns where processor load appears normal while memory sits high' in `merged.md` -- The reference text states that processor load appears normal while memory sits high. |

### `merged.md` -- 18 claim(s): 0 invented, 0 contradicted, 0 supported in part, 18 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests`. | supported | `source_a.md` | 'Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests`.' in `source_a.md` -- Source A states this directly in the issue description opening sentence. |
| 2 | Nimbrel Relay stalls when append requests are refused. | supported | `source_a.md` | 'Nimbrel Relay stalls' in `source_a.md` -- Source A explicitly states that callers see 'Nimbrel Relay stalls' when appends are refused. |
| 3 | Batch loaders resend the same envelope when append requests are refused. | supported | `source_a.md` | 'batch loaders resend the same envelope' in `source_a.md` -- Source A explicitly states that when append requests are refused, 'batch loaders resend the same envelope'. |
| 4 | Reads against the same shard begin to time out when append requests are refused. | supported | `source_a.md` | 'reads against the same shard begin to time out' in `source_a.md` -- Source A explicitly states that when append requests are refused, 'reads against the same shard begin to time out'. |
| 5 | The refusal is written to the Relay and Collector logs. | supported | `source_a.md` | 'The refusal reaches the client and is written to the Relay and Collector logs as well.' in `source_a.md` -- Source A states that the refusal is 'written to the Relay and Collector logs as well'. |
| 6 | A full refusal envelope from a batched append shows 0 of 64 envelopes refused. | supported | `source_a.md` | 'append batch refused after 0 of 64 envelopes: 429 Too Many Requests' in `source_a.md` -- The refusal envelope shown in source A explicitly displays '0 of 64 envelopes' refused. |
| 7 | Every Nimbrel Ledger release on every platform can refuse an append this way. | supported | `source_a.md` | 'Every Nimbrel Ledger release on every platform can refuse an append this way.' in `source_a.md` -- Source A states this directly in the Environment section. |
| 8 | In a managed Nimbrel Ledger deployment, HTTP `429` replies may grow over time as counted at the front proxy. | supported | `source_b.md` | 'a managed Nimbrel Ledger deployment (NMD) whose share of HTTP `429` replies climbed over a fortnight, as counted at the front proxy.' in `source_b.md` -- Source B describes a managed deployment whose 429 replies grew over time as counted at the front proxy. |
| 9 | A 429 - Too Many Requests reply is what a Ledger node sends once an append queue or a read queue is full. | supported | `source_a.md` | 'A [`429 - Too Many Requests` reply](https://docs.nimbrel.example/ledger/http-status-codes) is what a Ledger node sends once it has nowhere left to put the work, which is to say once [an append queue or a read queue is full](https://docs.nimbrel.example/ledger/why-appends-are-refused).' in `source_a.md` -- Source A explicitly states that a 429 is sent once an append queue or read queue is full. |
| 10 | The `append` or `system_append` worker pools can refuse an append when they hold more batches than they have slots for. | supported | `source_a.md` | 'The `append` or `system_append` worker pools hold more batches than they have slots for' in `source_a.md` -- Source A lists this as the first of three ways an append draws a 429. |
| 11 | The ingest memory guard can refuse a batch. | supported | `source_a.md` | 'The ingest memory guard has refused the batch' in `source_a.md` -- Source A lists this as the second of three ways an append draws a 429. |
| 12 | A circuit breaker can trip and cause a 429. | supported | `source_a.md` | 'A circuit breaker has tripped (`nbctl breaker list --tripped`) - a breaker trips on any operation and is not particular to appends.' in `source_a.md` -- Source A lists circuit breaker trips as the third way an append draws a 429. |
| 13 | Expensive queries can hold worker slots for extended periods in a managed deployment. | supported | `source_b.md` | '**Expensive queries**: a handful of queries run for as long as 2 seconds each. A worker slot is unavailable for as long as one of them holds it, and the queue behind it grows.' in `source_b.md` -- Source B explicitly states that expensive queries hold worker slots for extended periods in the managed deployment context. |
| 14 | Deep grouping operations consume memory from the same pool the append path draws on in a managed deployment. | supported | `source_b.md` | '**Deep grouping**: grouping on `channel.id` yields a very large number of groups, and the memory that costs is charged to the same pool the append path draws on.' in `source_b.md` -- Source B explicitly states that deep grouping memory is charged to the same pool as the append path. |
| 15 | From release 4.6 and release 5.1 onward, appending to a `wide_text` column draws a 429 whenever the batch would otherwise have run the node out of memory. | supported | `source_a.md` | 'From release 4.6 and release 5.1 onward, appending to a `wide_text` column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory.' in `source_a.md`, **transcription_error** -- Source A states this directly in a footnote discussing wide_text columns on releases 4.6 and 5.1 onward. |
| 16 | The `ingest_guard.memory.leader.ceiling` cluster setting defaults to 10% of the heap. | supported | `source_a.md` | 'which defaults to 10% of the heap' in `source_a.md` -- Source A states that the ingest_guard.memory.leader.ceiling 'defaults to 10% of the heap'. |
| 17 | The `ingest_guard.memory.leader.ceiling` cluster setting is read at startup. | supported | `source_a.md` | 'The setting is read at startup' in `source_a.md` -- Source A explicitly states that the ingest_guard.memory.leader.ceiling setting 'is read at startup'. |
| 18 | The cluster must be restarted for a change to the `ingest_guard.memory.leader.ceiling` setting to take effect. | supported | `source_a.md` | 'so the cluster must be restarted for a change to take.' in `source_a.md` -- Source A states that because the setting is read at startup, 'the cluster must be restarted for a change to take'. |

## Structure

**9** mechanical check(s) over **63** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **18** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **44**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 4 run(s) over 39 attributed segment(s) — sources interleaved. 9 of 13 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Absent and undeclared — in a source, not in the merge, and no record explains it

- `b5` (`source_b.md`) — 'It sets out what the evidence pointed at, which was expensive queries and deep grouping, and what was put forward in response.' is not in the merge and no disposition record explains it (nearest merge segment m35 at 0.34)

  ```text
  In the source: It sets out what the evidence pointed at, which was expensive queries and deep grouping, and what was put forward in response.
  ```

### Unresolved replacement — a record points at text the merge does not contain

- `b13` — segment b13 is declared 'subsumed' with replacement 'In a managed deployment, HTTP `429` replies may grow over time as counted at the front proxy.', which is not in the merged document

  ```text
  In the merge: In a managed deployment, HTTP `429` replies may grow over time as counted at the front proxy.
  ```

### Verbatim violation — an invariant-core token did not survive unchanged

- `b16` (`source_b.md`) — numeric '2' (seconds) does not survive into the merge unchanged
- `b18` (`source_b.md`) — code '`channel.id`' does not survive into the merge unchanged

### Over budget — declared loss past the ceiling

- 6 absent segments are declared replaced by the same replacement (b15, b16, b17, b18, b19, b20), over the ceiling of 3. One replacement standing in for that many segments has not replaced them, it has dropped them: the detail it names is gone from the document
- 10 of 63 segments are declared dropped (15.9%), over the 3% budget

## Review queue

**5** claim(s) the merge declared dropped and the forward pass confirms are gone. Each is a decision to review — put the fact back, or agree it stays out — and none of them is counted as a finding above.

- **B-005** (`source_b.md:13`) — The version is 4.4, 5.x.
  - left out of: `b8`
  - the merge's reason: Specific version numbers from managed case omitted; general applicability kept.
  - confirmed absent: the forward pass looked for this claim in `merged.md` and did not find it -- The reference text mentions releases 4.6, 5.1, and later but does not specify versions 4.4 or 5.x.
- **B-006** (`source_b.md:14`) — The platform is Nimbrel Cloud.
  - left out of: `b9`
  - the merge's reason: Platform specification from managed deployment example omitted.
  - confirmed absent: the forward pass looked for this claim in `merged.md` and did not find it -- The reference text does not mention Nimbrel Cloud as the platform.
- **B-007** (`source_b.md:15`) — The deployment is Managed Ledger Service (MLS).
  - left out of: `b10`
  - the merge's reason: Deployment type specification from managed example omitted.
  - confirmed absent: the forward pass looked for this claim in `merged.md` and did not find it -- The reference text does not mention Managed Ledger Service (MLS) by that acronym or name.
- **B-008** (`source_b.md:16`) — The environment is production.
  - left out of: `b11`
  - the merge's reason: Production environment flag from managed example omitted.
  - confirmed absent: the forward pass looked for this claim in `merged.md` and did not find it -- The reference text does not explicitly state that the environment is production.
- **B-010** (`source_b.md:20`) — Front proxy counters agree with client reports.
  - left out of: `b14`
  - the merge's reason: Client-side accounting validation specific to one managed case omitted.
  - confirmed absent: the forward pass looked for this claim in `merged.md` and did not find it -- The reference text does not state that front proxy counters agree with client reports.

> **Over budget.** The merge declared **10** drop(s) of 63 source segment(s), **15.9%**, over the 3% budget: past that share the omissions are the finding, whatever each one says about itself.

## Declarations

The merge declared **22** departure(s) from its sources. Checking them confirms 10, rejects 7, and leaves 5 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 10 of 63 source segment(s) declared gone, **15.9%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | Base document title chosen; source_b title describes a specific case. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Nimbrel Ledger append rejected with HTTP 429' and says so (no claim traced to it) |
| `b2` | dropped | Author and date from document b are not carried; source_a metadata retained. | **rejected** | declared 'dropped', which predicts MISSING; B-001 came back CONTRADICTED, B-002 came back CONTRADICTED (`B-001`, `B-002`) |
| `b3` | dropped | Summary/Table of Contents heading serves no purpose in merged structure. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b4` | subsumed | Evidence of rising refusals integrated into Environment section. | **rejected** | declared 'subsumed', which predicts SUPPORTED; B-003 came back MISSING (`B-003`) |
| `b6` | dropped | Structured metadata from managed deployment not carried; general case retained. | **rejected** | declared 'dropped', and its text is in the merge (no claim traced to it) |
| `b7` | dropped | Product version and platform details from managed deployment example omitted. | **rejected** | declared 'dropped', which predicts MISSING; B-004 came back SUPPORTED (`B-004`) |
| `b8` | dropped | Specific version numbers from managed case omitted; general applicability kept. | **confirmed** | declared 'dropped' and every claim from it came back MISSING (`B-005`) |
| `b9` | dropped | Platform specification from managed deployment example omitted. | **confirmed** | declared 'dropped' and every claim from it came back MISSING (`B-006`) |
| `b10` | dropped | Deployment type specification from managed example omitted. | **confirmed** | declared 'dropped' and every claim from it came back MISSING (`B-007`) |
| `b11` | dropped | Production environment flag from managed example omitted. | **confirmed** | declared 'dropped' and every claim from it came back MISSING (`B-008`) |
| `b13` | subsumed | Observation of rising refusals integrated into Environment section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-009`) |
| `b14` | dropped | Client-side accounting validation specific to one managed case omitted. | **confirmed** | declared 'dropped' and every claim from it came back MISSING (`B-010`) |
| `b15` | subsumed | Contributing factors from managed case merged into Cause section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b16` | subsumed | Expensive queries detail merged into Cause section. | **rejected** | declared 'subsumed', which predicts SUPPORTED; B-011 came back MISSING (`B-011`) |
| `b17` | subsumed | Worker slot impact merged into Cause section. | **rejected** | declared 'subsumed', which predicts SUPPORTED; B-012 came back MISSING (`B-012`) |
| `b18` | subsumed | Deep grouping detail merged into Cause section. | **rejected** | declared 'subsumed', which predicts SUPPORTED; B-013 came back MISSING (`B-013`) |
| `b19` | subsumed | Resource accounting observation merged into Cause section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-015`) |
| `b20` | subsumed | CPU/memory disagreement detail merged into Cause section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b21` | dropped | Heading 'Proposed Actions' replaced by content integration into Workaround and R | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b22` | subsumed | Slow query threshold action moved to Workaround section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b23` | subsumed | Query review action merged into Workaround section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b24` | subsumed | Evidence capture action moved to Resolution section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |


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
| Calls | 8 live, 0 cached, 0 replayed |
| Tokens | 28,242 in, 14,140 out |
| Cost | ~$0.10 estimated (rates read 2026-08-31) |
| Schema repairs | 1 |
| Errors | 0 |
| Duration | 106.3s |
| Generated | 2026-09-27T16:09:30+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
