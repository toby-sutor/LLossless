## Verdict

**18 finding(s).** In the claims: 9 dropped, 1 contradicted. In the structure: 1 undeclared rewording, 1 unresolved replacement, 4 verbatim violation, 2 declared loss over budget. The merge declared **5** drop(s) of 63 source segment(s), **7.9%**, over the 3% budget: past that share the omissions are the finding, whatever each one says about itself. The 1 claim(s) they cost are listed in the review queue below.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 32 |
| Claims extracted from `source_a.md` | 20 |
| Claims extracted from `source_b.md` | 16 |
| Forward — source claims accounted for in the merge | **25/36** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **20/20** |
| Forward — `source_b.md` claims accounted for | **5/16** |
| Reverse — merge claims found in a source | **32/32** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **54/58** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Dropped — in a source, not in the merge

- **B-002** (`source_b.md:12`) — The product is Nimbrel Ledger.
  - judged against: `merged.md`
  - rationale: The reference text does not describe a specific case scenario.
- **B-003** (`source_b.md:13`) — The version is 4.4, 5.x.
  - judged against: `merged.md`
  - rationale: The reference text does not specify versions for any particular case.
- **B-004** (`source_b.md:14`) — The platform is Nimbrel Cloud.
  - judged against: `merged.md`
  - rationale: The reference text does not mention a specific platform for any case.
- **B-005** (`source_b.md:15`) — The deployment is Managed Ledger Service (MLS).
  - judged against: `merged.md`
  - rationale: The reference text does not mention Managed Ledger Service or any deployment type.
- **B-006** (`source_b.md:16`) — This is a production environment.
  - judged against: `merged.md`
  - rationale: The reference text does not specify whether scenarios are in a production environment.
- **B-007** (`source_b.md:20`) — The managed deployment returns HTTP 429 on a growing share of requests.
  - judged against: `merged.md`
  - rationale: The reference text does not describe a growing share of 429 responses for a specific deployment.
- **B-008** (`source_b.md:20`) — Front proxy counters agree with the client reports.
  - judged against: `merged.md`
  - rationale: The reference text does not mention front proxy counters or comparison with client reports.
- **B-009** (`source_b.md:20`) — The refusals are real and not a client-side accounting error.
  - judged against: `merged.md`
  - rationale: The reference text does not discuss whether refusals are real or accounting errors.
- **B-013** (`source_b.md:25`) — Grouping on channel.id yields a very large number of groups.
  - judged against: `merged.md`
  - rationale: The reference discusses high-cardinality fields generally but does not mention channel.id specifically.

### Contradicted — the merge states something different

- **B-010** -- the two documents disagree
  - `source_b.md:24` says: A handful of queries run for as long as 2 seconds each.
  - `merged.md` says: 'A query that runs for several seconds holds a worker slot unavailable for other work' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference states queries run for several seconds, contradicting the claim's specific value of 2 seconds.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 20 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 20 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Append requests to Nimbrel Ledger come back with HTTP 429 Too Many Requests. | 8 | carried | 'Append requests to Nimbrel Ledger return HTTP 429 `Too Many Requests`' in `merged.md` -- The reference text directly states this claim in the issue description. |
| 2 | When append requests return HTTP 429, Nimbrel Relay stalls. | 8 | carried | 'Nimbrel Relay stalls' in `merged.md` -- The reference text states this as one consequence when append requests return HTTP 429. |
| 3 | When append requests return HTTP 429, batch loaders resend the same envelope. | 8 | carried | 'batch loaders resend the same envelope' in `merged.md` -- The reference text states this consequence when append requests return HTTP 429. |
| 4 | When append requests return HTTP 429, reads against the same shard begin to time out. | 8 | carried | 'reads against the same shard begin to time out' in `merged.md` -- The reference text states this consequence when append requests return HTTP 429. |
| 5 | The refusal reaches the client and is written to the Relay and Collector logs as well. | 8 | carried | 'The refusal reaches the client and is written to the Relay and Collector logs as well.' in `merged.md` -- The reference text directly states this claim. |
| 6 | Every Nimbrel Ledger release on every platform can refuse an append this way. | 20 | carried | 'Every Nimbrel Ledger release on every platform can refuse an append this way.' in `merged.md` -- The reference text directly states this in the Environment section. |
| 7 | A Ledger node sends a 429 - Too Many Requests reply once an append queue or a read queue is full. | 24 | carried | 'A 429 - Too Many Requests reply is what a Ledger node sends once it has nowhere left to put the work, which is to say once an append queue or a read queue is full' in `merged.md`, **transcription_error** -- The reference text states that a Ledger node sends a 429 reply once a queue is full. |
| 8 | An append draws a 429 when the append or system_append worker pools hold more batches than they have slots for. | 28 | carried | 'The `append` or `system_append` worker pools hold more batches than they have slots for' in `merged.md` -- The reference text lists this as one of three ways an append draws a 429. |
| 9 | An append draws a 429 when the ingest memory guard has refused the batch. | 29 | carried | 'The ingest memory guard has refused the batch' in `merged.md` -- The reference text lists this as one of three ways an append draws a 429. |
| 10 | An append draws a 429 when a circuit breaker has tripped. | 30 | carried | 'A circuit breaker has tripped' in `merged.md` -- The reference text lists this as one of three ways an append draws a 429. |
| 11 | A circuit breaker trips on any operation and is not particular to appends. | 30 | carried | 'a breaker trips on any operation and is not particular to appends' in `merged.md` -- The reference text directly states that a circuit breaker is not particular to appends. |
| 12 | From release 4.6 and release 5.1 onward, appending to a wide_text column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory. | 32 (unverified) | carried | 'From release 4.6 and release 5.1 onward, appending to a `wide_text` column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory.' in `merged.md`, **transcription_error** -- The reference text directly states this claim in a footnote. |
| 13 | A cluster that refuses appends has been given more work than its hardware can carry. | 42 | carried | 'A cluster that refuses appends has been given more work than its hardware can carry' in `merged.md` -- The reference text directly states this in the Resolution section. |
| 14 | Splitting a hot stream over more leader shards spreads append load across more nodes, which helps in some layouts. | 44 | carried | 'Splitting a hot stream over more leader shards spreads append load across more nodes, which helps in some layouts.' in `merged.md` -- The reference text directly states this claim. |
| 15 | The ingest_guard.memory.leader.ceiling setting defaults to 10% of the heap. | 50 | carried | 'which defaults to 10% of the heap' in `merged.md` -- The reference text states the default value of the setting is 10% of the heap. |
| 16 | A higher ceiling in the ingest_guard.memory.leader.ceiling setting allows a node to hold more in-flight append memory before refusing. | 50 | carried | 'A higher ceiling lets a node hold more in-flight append memory before refusing' in `merged.md` -- The reference text states that a higher ceiling allows nodes to hold more in-flight append memory. |
| 17 | A node holding too much in-flight append memory runs out of memory instead of refusing. | 50 | carried | 'a node holding too much runs out of memory instead of refusing' in `merged.md` -- The reference text directly states this consequence of holding too much in-flight memory. |
| 18 | The ingest_guard.memory.leader.ceiling setting is read at startup. | 50 | carried | 'The setting is read at startup' in `merged.md` -- The reference text directly states this about the setting. |
| 19 | The cluster must be restarted for changes to the ingest_guard.memory.leader.ceiling setting to take effect. | 50 | carried | 'so the cluster must be restarted for a change to take' in `merged.md` -- The reference text states the cluster must be restarted for setting changes to take effect. |
| 20 | Refusals that show up only during a spike usually clear on their own once the queues drain. | 52 | carried | 'Refusals that show up only during a spike usually clear on their own once the queues drain.' in `merged.md` -- The reference text directly states this claim. |

### `source_b.md` -- 16 claim(s): 10 dropped, 1 contradicted, 0 carried in part, 5 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | A managed Nimbrel Ledger deployment's share of HTTP 429 replies climbed over a fortnight, as counted at the front proxy. | 8 | dropped | The reference is a general handbook article, not a case study describing a specific deployment's 429 metrics. |
| 2 | The product is Nimbrel Ledger. | 12 | dropped | The reference text does not describe a specific case scenario. |
| 3 | The version is 4.4, 5.x. | 13 | dropped | The reference text does not specify versions for any particular case. |
| 4 | The platform is Nimbrel Cloud. | 14 | dropped | The reference text does not mention a specific platform for any case. |
| 5 | The deployment is Managed Ledger Service (MLS). | 15 | dropped | The reference text does not mention Managed Ledger Service or any deployment type. |
| 6 | This is a production environment. | 16 | dropped | The reference text does not specify whether scenarios are in a production environment. |
| 7 | The managed deployment returns HTTP 429 on a growing share of requests. | 20 | dropped | The reference text does not describe a growing share of 429 responses for a specific deployment. |
| 8 | Front proxy counters agree with the client reports. | 20 | dropped | The reference text does not mention front proxy counters or comparison with client reports. |
| 9 | The refusals are real and not a client-side accounting error. | 20 | dropped | The reference text does not discuss whether refusals are real or accounting errors. |
| 13 | Grouping on channel.id yields a very large number of groups. | 25 | dropped | The reference discusses high-cardinality fields generally but does not mention channel.id specifically. |
| 10 | A handful of queries run for as long as 2 seconds each. | 24 | contradicted | 'A query that runs for several seconds holds a worker slot unavailable for other work' in `merged.md` -- The reference states queries run for several seconds, contradicting the claim's specific value of 2 seconds. |
| 11 | A worker slot is unavailable for as long as one of them holds it. | 24 | carried | 'A query that runs for several seconds holds a worker slot unavailable for other work' in `merged.md` -- The reference text states that a query holds a worker slot unavailable, supporting the claim. |
| 12 | The queue behind it grows. | 24 | carried | 'and the queue behind it grows' in `merged.md` -- The reference text directly states this claim about queue growth. |
| 14 | The memory that costs is charged to the same pool the append path draws on. | 25 | carried | 'the memory that costs is charged to the same pool the append path draws on' in `merged.md` -- The reference text directly states this claim about memory allocation. |
| 15 | Processor load looks unremarkable while memory sits high. | 26 | carried | 'When processor load looks unremarkable while memory sits high' in `merged.md` -- The reference states this condition when discussing what points toward query cost. |
| 16 | Processor load and memory do not agree. | 26 | carried | 'When processor load looks unremarkable while memory sits high' in `merged.md` -- The reference describes a situation where processor load and memory have conflicting values, supporting the claim. |

### `merged.md` -- 32 claim(s): 0 invented, 0 contradicted, 0 supported in part, 32 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Append requests to Nimbrel Ledger return HTTP 429 Too Many Requests. | supported | `source_a.md` | 'Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests`.' in `source_a.md` -- Source A directly states this in the issue description. |
| 2 | Callers experience writes that will not land. | supported | `source_a.md` | 'Callers see a write that will not land' in `source_a.md` -- Source A directly states this outcome for callers. |
| 3 | Nimbrel Relay stalls. | supported | `source_a.md` | 'Nimbrel Relay stalls' in `source_a.md` -- Source A lists this as one consequence when appends are refused. |
| 4 | Batch loaders resend the same envelope. | supported | `source_a.md` | 'batch loaders resend the same envelope' in `source_a.md` -- Source A lists this as a consequence of refused appends. |
| 5 | Reads against the same shard begin to time out. | supported | `source_a.md` | 'reads against the same shard begin to time out' in `source_a.md` -- Source A lists this as a consequence of refused appends. |
| 6 | The refusal reaches the client. | supported | `source_a.md` | 'The refusal reaches the client' in `source_a.md` -- Source A states the refusal reaches the client and is logged. |
| 7 | The refusal is written to the Relay and Collector logs. | supported | `source_a.md` | 'is written to the Relay and Collector logs as well' in `source_a.md` -- Source A states the refusal is written to both logs. |
| 8 | Every Nimbrel Ledger release on every platform can refuse an append this way. | supported | `source_a.md` | 'Every Nimbrel Ledger release on every platform can refuse an append this way.' in `source_a.md` -- Source A states this in the Environment section. |
| 9 | A Ledger node sends a 429 reply when an append queue or a read queue is full. | supported | `source_a.md` | 'A Ledger node sends once it has nowhere left to put the work, which is to say once an append queue or a read queue is full' in `source_a.md`, **transcription_error** -- Source A explains when a 429 reply is sent by a Ledger node. |
| 10 | There are 3 ways an append draws a 429. | supported | `source_a.md` | 'There are 3 ways an append draws a 429:' in `source_a.md` -- Source A explicitly states there are 3 ways. |
| 11 | The append or system_append worker pools can hold more batches than they have slots for. | supported | `source_a.md` | 'The `append` or `system_append` worker pools hold more batches than they have slots for' in `source_a.md` -- Source A lists this as the first way an append draws a 429. |
| 12 | The ingest memory guard can refuse a batch. | supported | `source_a.md` | 'The ingest memory guard has refused the batch' in `source_a.md` -- Source A lists ingest memory guard refusal as the second way. |
| 13 | A circuit breaker can trip. | supported | `source_a.md` | 'A circuit breaker has tripped' in `source_a.md` -- Source A lists circuit breaker trip as the third way. |
| 14 | A breaker trips on any operation and is not particular to appends. | supported | `source_a.md` | 'a breaker trips on any operation and is not particular to appends' in `source_a.md` -- Source A clarifies breaker behavior is not append-specific. |
| 15 | A query that runs for several seconds holds a worker slot unavailable for other work. | supported | `source_b.md` | 'A worker slot is unavailable for as long as one of them holds it' in `source_b.md` -- Source B states that long-running queries hold worker slots unavailable. |
| 16 | The queue behind a long-running query grows. | supported | `source_b.md` | 'the queue behind it grows' in `source_b.md` -- Source B states the queue grows when a slot is held by a long query. |
| 17 | Grouping on high-cardinality fields yields a very large number of groups. | supported | `source_b.md` | 'grouping on `channel.id` yields a very large number of groups' in `source_b.md` -- Source B provides this example of high-cardinality grouping. |
| 18 | The memory cost of grouping on high-cardinality fields is charged to the same pool the append path draws on. | supported | `source_b.md` | 'the memory that costs is charged to the same pool the append path draws on' in `source_b.md` -- Source B states grouping memory cost is charged to the append pool. |
| 19 | When processor load looks unremarkable while memory sits high, this points toward query cost rather than an undersized cluster. | supported | `source_b.md` | 'processor load looks unremarkable while memory sits high. The two do not agree, which points at query cost rather than at an undersized cluster' in `source_b.md` -- Source B explains what high memory with unremarkable processor load indicates. |
| 20 | From release 4.6 and release 5.1 onward, appending to a wide_text column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory. | supported | `source_a.md` | 'From release 4.6 and release 5.1 onward, appending to a `wide_text` column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory.' in `source_a.md`, **transcription_error** -- Source A footnote [1] states this behavior from those releases forward. |
| 21 | Setting the slow query threshold to 1 second causes expensive queries to be recorded individually instead of being averaged into statistics. | supported | `source_b.md` | 'set it to 1 second, so that the queries actually responsible are recorded instead of averaged away' in `source_b.md` -- Source B proposes this threshold change to record queries individually. |
| 22 | A cluster that refuses appends has been given more work than its hardware can carry. | supported | `source_a.md` | 'A cluster that refuses appends has been given more work than its hardware can carry' in `source_a.md` -- Source A states this directly in the Resolution section. |
| 23 | The answer to refusing appends is hardware: larger nodes (scale up) or more nodes (scale out). | supported | `source_a.md` | 'the answer is hardware: larger nodes (scale up), or more of them (scale out)' in `source_a.md` -- Source A identifies hardware as the answer and lists both scaling approaches. |
| 24 | Splitting a hot stream over more leader shards spreads append load across more nodes. | supported | `source_a.md` | 'Splitting a hot stream over more leader shards spreads append load across more nodes' in `source_a.md` -- Source A states this strategy for spreading append load. |
| 25 | Spreading append load across more nodes helps in some layouts. | supported | `source_a.md` | 'which helps in some layouts' in `source_a.md` -- Source A notes that load spreading helps in some layouts. |
| 26 | The ingest_guard.memory.leader.ceiling setting defaults to 10% of the heap. | supported | `source_a.md` | 'which defaults to 10% of the heap' in `source_a.md` -- Source A specifies the default value of this setting. |
| 27 | A higher ceiling on ingest_guard.memory.leader.ceiling lets a node hold more in-flight append memory before refusing. | supported | `source_a.md` | 'A higher ceiling lets a node hold more in-flight append memory before refusing' in `source_a.md` -- Source A explains the effect of raising the ceiling. |
| 28 | A node holding too much memory runs out of memory instead of refusing. | supported | `source_a.md` | 'and a node holding too much runs out of memory instead of refusing' in `source_a.md` -- Source A states this consequence of an excessively high ceiling. |
| 29 | Running out of memory is worse than refusing. | supported | `source_a.md` | 'which is the worse outcome' in `source_a.md` -- Source A characterizes running out of memory as worse than refusing. |
| 30 | The ingest_guard.memory.leader.ceiling setting is read at startup. | supported | `source_a.md` | 'The setting is read at startup' in `source_a.md` -- Source A states when the setting is read. |
| 31 | The cluster must be restarted for a change to the ingest_guard.memory.leader.ceiling setting to take effect. | supported | `source_a.md` | 'so the cluster must be restarted for a change to take' in `source_a.md` -- Source A states the cluster must be restarted for the change to take effect. |
| 32 | Refusals that show up only during a spike usually clear on their own once the queues drain. | supported | `source_a.md` | 'Refusals that show up only during a spike usually clear on their own once the queues drain.' in `source_a.md` -- Source A states this in the Workaround section. |

## Structure

**9** mechanical check(s) over **63** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **32** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **36**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 6 run(s) over 38 attributed segment(s) — sources interleaved. 8 of 13 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

`[-...-]` is what the source said and `{+...+}` is what the merge says.

### Reworded and undeclared — in the merge in altered wording, and no record explains it. At off this also covers layout: a segment whose source line breaks the merge ran together is altered and undeclared, and 380 reuses this kind rather than moving FINDING_KINDS off 12

- `a5` (`source_a.md`) — 'Callers see a write that will not land: Nimbrel Relay stalls, batch loaders resend the same envelope, and reads against the same shard begin to time out.' is reworded in the merge and no disposition record explains it (nearest merge segment m5 at 0.96)

  ```text
  In the source: Callers see a write that will not land: Nimbrel Relay stalls, batch loaders resend the same envelope, and reads against the same shard begin to time out.
  In the merge:  Callers experience writes that will not land: Nimbrel Relay stalls, batch loaders resend the same envelope, and reads against the same shard begin to time out.
  What changed:  Callers [-see a write-] {+experience writes+} that will not land: Nimbrel Relay stalls, batch loaders resend the same envelope, and reads against the same shard begin to time out.
  ```

### Unresolved replacement — a record points at text the merge does not contain

- `b22` — segment b22 is declared 'subsumed' with replacement '...set the slow query threshold to 1 second so that expensive queries are recorded individually instead of being averaged into statistics.', which is not in the merged document

  ```text
  In the merge: ...set the slow query threshold to 1 second so that expensive queries are recorded individually instead of being averaged into statistics.
  ```

### Verbatim violation — an invariant-core token did not survive unchanged

- `b8` (`source_b.md`) — numeric '4.4' does not survive into the merge unchanged
- `b13` (`source_b.md`) — code '`429`' does not survive into the merge unchanged
- `b16` (`source_b.md`) — numeric '2' (seconds) does not survive into the merge unchanged
- `b18` (`source_b.md`) — code '`channel.id`' does not survive into the merge unchanged

### Over budget — declared loss past the ceiling

- 5 absent segments are declared replaced by the same replacement (b10, b11, b7, b8, b9), over the ceiling of 3. One replacement standing in for that many segments has not replaced them, it has dropped them: the detail it names is gone from the document
- 5 of 63 segments are declared dropped (7.9%), over the 3% budget

## Review queue

**1** claim(s) the merge declared dropped and the forward pass confirms are gone. Each is a decision to review — put the fact back, or agree it stays out — and none of them is counted as a finding above.

- **B-001** (`source_b.md:8`) — A managed Nimbrel Ledger deployment's share of HTTP 429 replies climbed over a fortnight, as counted at the front proxy.
  - left out of: `b4`
  - the merge's reason: Incident-specific context; general facts covered elsewhere.
  - confirmed absent: the forward pass looked for this claim in `merged.md` and did not find it -- The reference is a general handbook article, not a case study describing a specific deployment's 429 metrics.

> **Over budget.** The merge declared **5** drop(s) of 63 source segment(s), **7.9%**, over the 3% budget: past that share the omissions are the finding, whatever each one says about itself.

## Declarations

The merge declared **26** departure(s) from its sources. Checking them confirms 10, rejects 9, and leaves 7 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 5 of 63 source segment(s) declared gone, **7.9%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a4` | reworded | Changed 'come back' to 'return' for clarity. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-001`) |
| `b1` | superseded | Base title kept; B's title describes one case. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Nimbrel Ledger append rejected with HTTP 429' and says so (no claim traced to it) |
| `b2` | superseded | Base author maintained; B's case had different author. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b3` | dropped | Summary/TOC not part of base structure. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b4` | dropped | Incident-specific context; general facts covered elsewhere. | **confirmed** | declared 'dropped' and every claim from it came back MISSING (`B-001`) |
| `b5` | subsumed | Case-specific findings generalized into principles. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b6` | superseded | Duplicate section header; a10 kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b7` | subsumed | Product info is instance of general fact. | **rejected** | declared 'subsumed', which predicts SUPPORTED; B-002 came back MISSING (`B-002`) |
| `b8` | subsumed | Version info is instance of general fact. | **rejected** | declared 'subsumed', which predicts SUPPORTED; B-003 came back MISSING (`B-003`) |
| `b9` | subsumed | Platform info is instance of general fact. | **rejected** | declared 'subsumed', which predicts SUPPORTED; B-004 came back MISSING (`B-004`) |
| `b10` | subsumed | Deployment type is instance of general fact. | **rejected** | declared 'subsumed', which predicts SUPPORTED; B-005 came back MISSING (`B-005`) |
| `b11` | subsumed | Production environment is instance of general fact. | **rejected** | declared 'subsumed', which predicts SUPPORTED; B-006 came back MISSING (`B-006`) |
| `b12` | superseded | Duplicate section header; a3 kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b13` | subsumed | Managed deployment case is instance of general phenomenon. | **rejected** | declared 'subsumed', which predicts SUPPORTED; B-007 came back MISSING (`B-007`) |
| `b14` | subsumed | Real refusals confirmed in issue description. | **rejected** | declared 'subsumed', which predicts SUPPORTED; B-008 came back MISSING, B-009 came back MISSING (`B-008`, `B-009`) |
| `b15` | dropped | Section header reorganized into Cause. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b16` | subsumed | Expensive query observation generalized to principle. | **rejected** | declared 'subsumed', which predicts SUPPORTED; B-010 came back CONTRADICTED (`B-010`) |
| `b17` | subsumed | Worker slot effect subsumed into cause explanation. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-011`, `B-012`) |
| `b18` | subsumed | Deep grouping example becomes general principle. | **rejected** | declared 'subsumed', which predicts SUPPORTED; B-013 came back MISSING (`B-013`) |
| `b19` | subsumed | Resource accounting observation integrated into cause. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-015`) |
| `b20` | subsumed | Diagnostic principle about query cost integrated. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-016`) |
| `b21` | dropped | Section header reorganized into Workaround. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b22` | subsumed | Recommendation becomes investigation step. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b23` | subsumed | Recommendation becomes investigation step. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b24` | subsumed | Recommendation becomes investigation step. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b25` | dropped | Section header not in base structure; links preserved. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | 45fff742d0ed (command) -- lineup haiku-4.5-sub |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | claude-haiku-4-5-20251001 -> claude-haiku-4-5-20251001 |
| Model (decompose) | claude-haiku-4-5-20251001 -> claude-haiku-4-5-20251001 |
| Model (verify) | claude-haiku-4-5-20251001 -> claude-haiku-4-5-20251001 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile subscription, effort decompose one level (extended thinking on/off; default kept), merge one level (extended thinking on/off; default kept), verify one level (extended thinking on/off; default kept) |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 7 live, 0 cached, 0 replayed |
| Tokens | unknown (7 call(s) reported no usage) |
| Cost | unmeasured (7 call(s) reported no tokens, so no figure can be derived) |
| Schema repairs | 1 |
| Isolation | decompose, merge, verify: safe mode, no tools |
| Errors | 0 |
| Duration | 998.1s |
| Generated | 2026-09-27T16:39:11+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup haiku-4.5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
