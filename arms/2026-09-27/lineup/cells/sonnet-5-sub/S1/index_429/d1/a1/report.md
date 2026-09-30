## Verdict

**7 finding(s).** In the claims: 3 contradicted, 1 partially invented. In the structure: 2 verbatim violation, 1 declared loss over budget.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 39 |
| Claims extracted from `source_a.md` | 54 |
| Claims extracted from `source_b.md` | 27 |
| Forward — source claims accounted for in the merge | **78/81** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **54/54** |
| Forward — `source_b.md` claims accounted for | **24/27** |
| Reverse — merge claims found in a source | **38/39** |
| Reverse — supported only in part | 1 |
| Evidence grounded | **115/120** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **B-001** -- the two documents disagree
  - `source_b.md:3` says: The document's author is Devin Okonkwo.
  - `merged.md` says: 'Author: Priya Raghunathan' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Document names a different author than claimed.
- **B-002** -- the two documents disagree
  - `source_b.md:4` says: The document was updated on 2026-04-11.
  - `merged.md` says: 'Updated: 2026-03-18' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Document gives a different update date than claimed.
- **B-003** -- the two documents disagree
  - `source_b.md:8` says: This note concerns a managed Nimbrel Ledger deployment (NMD).
  - `merged.md` says: 'the Managed Ledger Service (MLS)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Deployment is named MLS, not NMD as claimed.

### Partly invented — the sources carry some of this claim

- **M-026** (`merged.md:36`) — In one worker-pool exhaustion case, contributing factors included expensive queries and deep grouping.
  - evidence: 'Expensive queries: a handful of queries run for as long as 2 seconds each. A worker slot is unavailable for as long as one of them holds it, and the queue behind it grows.' in `source_b.md` (transcription_error)
  - judged against: `source_a.md` and `source_b.md`
  - rationale: Contributing factors are supported but neither source labels this scenario a 'worker-pool exhaustion case'.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 54 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 54 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The document is authored by Priya Raghunathan. | 3 | carried | 'Author: Priya Raghunathan' in `merged.md` -- Byline states the author directly. |
| 2 | The document was updated on 2026-03-18. | 4 | carried | 'Updated: 2026-03-18' in `merged.md` -- Update date stated directly. |
| 3 | Append requests to Nimbrel Ledger come back with HTTP 429 Too Many Requests. | 8 | carried | 'Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests`.' in `merged.md` -- Matches claim exactly. |
| 4 | Nimbrel Relay stalls when a write will not land. | 8 | carried | 'Nimbrel Relay stalls' in `merged.md` -- Stated directly as an effect of a stalled write. |
| 5 | Batch loaders resend the same envelope when a write will not land. | 8 | carried | 'batch loaders resend the same envelope' in `merged.md` -- Directly stated. |
| 6 | Reads against the same shard begin to time out when a write will not land. | 8 | carried | 'reads against the same shard begin to time out' in `merged.md` -- Directly stated. |
| 7 | The refusal reaches the client. | 8 | carried | 'The refusal reaches the client' in `merged.md` -- Directly stated. |
| 8 | The refusal is written to the Relay logs. | 8 | carried | 'is written to the Relay and Collector logs as well' in `merged.md` -- States refusal is written to Relay logs. |
| 9 | The refusal is written to the Collector logs. | 8 | carried | 'is written to the Relay and Collector logs as well' in `merged.md` -- States refusal is written to Collector logs. |
| 10 | A full refusal envelope from a batched append shows the append batch was refused after 0 of 64 envelopes. | 13 | carried | 'append batch refused after 0 of 64 envelopes' in `merged.md` -- Directly present in the example envelope. |
| 11 | The example refusal envelope shows the error type nbl_queue_refused_exception. | 13 | carried | '"type":"nbl_queue_refused_exception"' in `merged.md` -- Error type appears in example. |
| 12 | The example refusal envelope shows ingest_and_leader_bytes=88121344. | 13 | carried | 'ingest_and_leader_bytes=88121344' in `merged.md` -- Value present in example envelope. |
| 13 | The example refusal envelope shows follower_bytes=212992. | 13 | carried | 'follower_bytes=212992' in `merged.md` -- Value present in example envelope. |
| 14 | The example refusal envelope shows all_bytes=88334336. | 13 | carried | 'all_bytes=88334336' in `merged.md` -- Value present in example envelope. |
| 15 | The example refusal envelope shows ingest_op_bytes=155648. | 13 | carried | 'ingest_op_bytes=155648' in `merged.md` -- Value present in example envelope. |
| 16 | The example refusal envelope shows max_ingest_bytes=88080384. | 13 | carried | 'max_ingest_bytes=88080384' in `merged.md` -- Value present in example envelope. |
| 17 | The example refusal envelope shows a status of 429. | 13 | carried | '"status":429' in `merged.md` -- Status field present in example. |
| 18 | The Ledger operations handbook now covers the same ground under Refused Appends. | 16 | carried | 'The Ledger operations handbook now covers the same ground under Refused Appends' in `merged.md` -- Directly stated. |
| 19 | The Ledger operations handbook provides a walkthrough for each of the three refusal paths. | 16 | carried | 'with a walkthrough for each of the three refusal paths set out below' in `merged.md` -- Directly stated. |
| 20 | Every Nimbrel Ledger release on every platform can refuse an append this way. | 20 | carried | 'Every Nimbrel Ledger release on every platform can refuse an append this way.' in `merged.md` -- Matches claim exactly. |
| 21 | A 429 - Too Many Requests reply is what a Ledger node sends once it has nowhere left to put the work. | 24 | carried | 'A [`429 - Too Many Requests` reply](https://docs.nimbrel.example/ledger/http-status-codes) is what a Ledger node sends once it has nowhere left to put the work' in `merged.md` -- Directly stated. |
| 22 | A Ledger node has nowhere left to put the work once an append queue or a read queue is full. | 24 | carried | 'which is to say once [an append queue or a read queue is full]' in `merged.md` -- Directly stated. |
| 23 | There are 3 ways an append draws a 429. | 26 | carried | 'There are 3 ways an append draws a 429:' in `merged.md` -- Matches claim exactly. |
| 24 | The append or system_append worker pools hold more batches than they have slots for. | 28 | carried | 'The `append` or `system_append` worker pools hold more batches than they have slots for (`nbctl pool status --all`)' in `merged.md` -- Directly stated. |
| 25 | The command nbctl pool status --all is used in relation to worker pools. | 28 | carried | '(`nbctl pool status --all`)' in `merged.md` -- Command listed alongside worker pool description. |
| 26 | The ingest memory guard can refuse the batch. | 29 | carried | 'The ingest memory guard has refused the batch (`nbctl guard report ingest --counters`).' in `merged.md` -- Directly stated. |
| 27 | The command nbctl guard report ingest --counters is used in relation to the ingest memory guard. | 29 | carried | '(`nbctl guard report ingest --counters`)' in `merged.md` -- Command listed for ingest memory guard. |
| 28 | A circuit breaker can trip. | 30 | carried | 'A circuit breaker has tripped (`nbctl breaker list --tripped`)' in `merged.md` -- Directly stated. |
| 29 | The command nbctl breaker list --tripped is used in relation to circuit breakers. | 30 | carried | '(`nbctl breaker list --tripped`)' in `merged.md` -- Command listed for circuit breaker. |
| 30 | A breaker trips on any operation and is not particular to appends. | 30 | carried | 'a breaker trips on any operation and is not particular to appends' in `merged.md` -- Matches claim exactly. |
| 31 | From release 4.6 onward, appending to a wide_text column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory. | 32 | carried | 'From release 4.6 and release 5.1 onward, appending to a `wide_text` column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory.' in `merged.md`, **transcription_error** -- Covers release 4.6 onward for this behavior. |
| 32 | From release 5.1 onward, appending to a wide_text column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory. | 32 | carried | 'From release 4.6 and release 5.1 onward, appending to a `wide_text` column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory.' in `merged.md`, **transcription_error** -- Covers release 5.1 onward for this behavior. |
| 33 | The workaround for the issue is to take append and query load off the cluster for long enough that the queues drain and the nodes fall back under their limits. | 36 | carried | 'Take append and query load off the cluster for long enough that the queues drain and the nodes fall back under their limits.' in `merged.md` -- Matches claim exactly. |
| 34 | Where batches carry wide_text columns and the cluster runs release 4.6 or later, the workaround is to send fewer envelopes per batch. | 38 | carried | 'Where batches carry `wide_text` columns and the cluster runs release 4.6 or release 5.1 or later, send fewer envelopes per batch.' in `merged.md` -- Covers release 4.6 case for this workaround. |
| 35 | Where batches carry wide_text columns and the cluster runs release 5.1 or later, the workaround is to send fewer envelopes per batch. | 38 | carried | 'Where batches carry `wide_text` columns and the cluster runs release 4.6 or release 5.1 or later, send fewer envelopes per batch.' in `merged.md` -- Covers release 5.1 case for this workaround. |
| 36 | A cluster that refuses appends has been given more work than its hardware can carry. | 42 | carried | 'A cluster that refuses appends has been given more work than its hardware can carry, so the answer is hardware' in `merged.md` -- Matches claim exactly. |
| 37 | One resolution option is larger nodes, described as scaling up. | 42 | carried | 'larger nodes (scale up)' in `merged.md` -- Directly stated. |
| 38 | Another resolution option is more nodes, described as scaling out. | 42 | carried | 'or more of them (scale out)' in `merged.md` -- Directly stated. |
| 39 | Scaling out is recommended when what is wanted is a further copy of the data for availability, per the sizing notes. | 42 | carried | 'scale out when what is wanted is a further copy of the data for availability, per [the sizing notes]' in `merged.md` -- Matches claim exactly. |
| 40 | Splitting a hot stream over more leader shards spreads append load across more nodes. | 44 | carried | 'Splitting a hot stream over more leader shards spreads append load across more nodes' in `merged.md` -- Matches claim exactly. |
| 41 | Splitting a hot stream over more leader shards helps in some layouts. | 44 | carried | 'which helps in some layouts' in `merged.md` -- Directly stated. |
| 42 | For wide_text columns on release 4.6 and later, the first resolution step is to cut the number of envelopes in each append batch. | 48 | carried | 'Begin by cutting the number of envelopes in each append batch.' in `merged.md` -- Listed as step 1 for release 4.6 and later. |
| 43 | For wide_text columns on release 5.1 and later, the first resolution step is to cut the number of envelopes in each append batch. | 48 | carried | 'Begin by cutting the number of envelopes in each append batch.' in `merged.md` -- Listed as step 1 for release 5.1 and later. |
| 44 | Where smaller batches do not clear the issue, the second resolution step is to add processor and memory capacity to the nodes. | 49 | carried | 'Where smaller batches do not clear it, add processor and memory capacity to the nodes.' in `merged.md` -- Matches claim exactly. |
| 45 | The third resolution step is to raise the ingest_guard.memory.leader.ceiling cluster setting. | 50 | carried | 'Only then raise the `ingest_guard.memory.leader.ceiling` cluster setting' in `merged.md` -- Matches claim exactly. |
| 46 | The ingest_guard.memory.leader.ceiling cluster setting defaults to 10% of the heap. | 50 | carried | 'which defaults to 10% of the heap' in `merged.md` -- Directly stated. |
| 47 | A higher ceiling lets a node hold more in-flight append memory before refusing. | 50 | carried | 'A higher ceiling lets a node hold more in-flight append memory before refusing' in `merged.md` -- Matches claim exactly. |
| 48 | A node holding too much runs out of memory instead of refusing. | 50 | carried | 'a node holding too much runs out of memory instead of refusing' in `merged.md` -- Matches claim exactly. |
| 49 | A node running out of memory instead of refusing is the worse outcome. | 50 | carried | 'which is the worse outcome' in `merged.md` -- Directly stated. |
| 50 | The ingest_guard.memory.leader.ceiling setting is read at startup. | 50 | carried | 'The setting is read at startup' in `merged.md` -- Directly stated. |
| 51 | The cluster must be restarted for a change to the ingest_guard.memory.leader.ceiling setting to take effect. | 50 | carried | 'so the cluster must be restarted for a change to take' in `merged.md` -- Matches claim exactly. |
| 52 | Where scaling hardware or configuration changes are not open to you, the load itself is what changes. | 52 | carried | 'Where none of that is open to you, the load itself is what changes' in `merged.md` -- Matches claim exactly. |
| 53 | The load can be changed via fewer appends, cheaper queries, or both. | 52 | carried | 'fewer appends, cheaper queries, or both' in `merged.md` -- Directly stated. |
| 54 | Refusals that show up only during a spike usually clear on their own once the queues drain. | 52 | carried | 'Refusals that show up only during a spike usually clear on their own once the queues drain.' in `merged.md` -- Matches claim exactly. |

### `source_b.md` -- 27 claim(s): 0 dropped, 3 contradicted, 0 carried in part, 24 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The document's author is Devin Okonkwo. | 3 | contradicted | 'Author: Priya Raghunathan' in `merged.md` -- Document names a different author than claimed. |
| 2 | The document was updated on 2026-04-11. | 4 | contradicted | 'Updated: 2026-03-18' in `merged.md` -- Document gives a different update date than claimed. |
| 3 | This note concerns a managed Nimbrel Ledger deployment (NMD). | 8 | contradicted | 'the Managed Ledger Service (MLS)' in `merged.md` -- Deployment is named MLS, not NMD as claimed. |
| 4 | The deployment's share of HTTP 429 replies climbed over a fortnight, as counted at the front proxy. | 8 | carried | 'the share of HTTP 429 replies climbed over a fortnight, as counted at the front proxy' in `merged.md` -- Matches claim exactly. |
| 5 | The evidence pointed at expensive queries and deep grouping. | 8 | carried | 'Investigation pointed to expensive queries and deep grouping as contributing factors' in `merged.md` -- Matches claim exactly. |
| 6 | The product is Nimbrel Ledger. | 12 | carried | 'Nimbrel Ledger version 4.4 and 5.x' in `merged.md` -- Product named as Nimbrel Ledger. |
| 7 | The version is 4.4, 5.x. | 13 | carried | 'Nimbrel Ledger version 4.4 and 5.x' in `merged.md` -- Version matches claim. |
| 8 | The platform is Nimbrel Cloud. | 14 | carried | 'running on Nimbrel Cloud under the Managed Ledger Service (MLS)' in `merged.md` -- Platform matches claim. |
| 9 | The deployment is Managed Ledger Service (MLS). | 15 | carried | 'under the Managed Ledger Service (MLS)' in `merged.md` -- Deployment matches claim. |
| 10 | The production environment status is Yes. | 16 | carried | 'in a production environment' in `merged.md` -- Matches claim exactly. |
| 11 | The managed deployment returns HTTP 429 on a growing share of requests. | 20 | carried | 'the share of HTTP 429 replies climbed over a fortnight' in `merged.md` -- Matches claim exactly. |
| 12 | HTTP 429 is what the Ledger returns when it refuses work rather than queueing it. | 20 | carried | 'A 429 is what the Ledger returns when it refuses work outright rather than queueing it.' in `merged.md` -- Matches claim exactly. |
| 13 | Front proxy counters agree with the client reports. | 20 | carried | 'front proxy counters agreed with client-side reports' in `merged.md` -- Matches claim exactly. |
| 14 | The refusals are real and not a client-side accounting error. | 20 | carried | 'confirming the refusals were real rather than a client-side accounting error' in `merged.md` -- Matches claim exactly. |
| 15 | A handful of queries run for as long as 2 seconds each. | 24 | carried | 'a handful of queries ran for as long as 2 seconds each' in `merged.md` -- Matches claim exactly. |
| 16 | A worker slot is unavailable for as long as one of the expensive queries holds it. | 24 | carried | 'a worker slot was unavailable for as long as one of them held it' in `merged.md` -- Matches claim exactly. |
| 17 | The queue behind the worker slot grows. | 24 | carried | 'so the queue behind it grew' in `merged.md` -- Matches claim exactly. |
| 18 | Grouping on channel.id yields a very large number of groups. | 25 | carried | 'Grouping on `channel.id` produced a very large number of groups' in `merged.md` -- Matches claim exactly. |
| 19 | The memory that grouping on channel.id costs is charged to the same pool the append path draws on. | 25 | carried | 'the memory that cost was charged to the same pool the append path draws on' in `merged.md` -- Matches claim exactly. |
| 20 | Processor load looks unremarkable while memory sits high. | 26 | carried | 'Processor load looked unremarkable while memory sat high' in `merged.md` -- Matches claim exactly. |
| 21 | Processor load and memory levels do not agree. | 26 | carried | 'Processor load looked unremarkable while memory sat high' in `merged.md` -- Contrast between unremarkable processor load and high memory necessarily entails disagreement between the two. |
| 22 | The disagreement between processor load and memory levels points at query cost rather than at an undersized cluster. | 26 | carried | 'Processor load looked unremarkable while memory sat high, which pointed at query cost rather than at an undersized cluster.' in `merged.md` -- Matches claim exactly. |
| 23 | The proposed action is to lower the slow query threshold to 1 second. | 30 | carried | 'lower the slow query threshold to 1 second' in `merged.md` -- Matches claim exactly. |
| 24 | Setting the slow query threshold to 1 second would result in the queries actually responsible being recorded instead of averaged away. | 30 | carried | 'so that the queries actually responsible are recorded instead of averaged away' in `merged.md` -- Matches claim exactly. |
| 25 | The proposed action is to review what the queries are for by going through the expensive ones with the team that wrote them. | 31 | carried | 'review the expensive queries with the team that wrote them' in `merged.md` -- Matches claim exactly. |
| 26 | Several of the expensive queries look like they could ask for less. | 31 | carried | 'since several may be able to ask for less' in `merged.md` -- Matches claim exactly. |
| 27 | The proposed action is to capture evidence during a refusal by taking a thread dump and a heap snapshot while the refusal rate is high. | 32 | carried | 'capture a thread dump and a heap snapshot while the refusal rate is high' in `merged.md` -- Matches claim exactly. |

### `merged.md` -- 39 claim(s): 0 invented, 0 contradicted, 1 supported in part, 38 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 26 | In one worker-pool exhaustion case, contributing factors included expensive queries and deep grouping. | supported in part | `source_b.md` | 'Expensive queries: a handful of queries run for as long as 2 seconds each. A worker slot is unavailable for as long as one of them holds it, and the queue behind it grows.' in `source_b.md`, **transcription_error** -- Contributing factors are supported but neither source labels this scenario a 'worker-pool exhaustion case'. |
| 1 | Append requests to Nimbrel Ledger come back with HTTP 429 Too Many Requests. | supported | `source_a.md` | 'Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests`.' in `source_a.md` -- Matches source_a's opening statement almost verbatim. |
| 2 | Nimbrel Relay stalls when an append write will not land. | supported | `source_a.md` | 'Nimbrel Relay stalls, batch loaders resend the same envelope, and reads against the same shard begin to time out.' in `source_a.md` -- Directly states Relay stalls when writes fail to land. |
| 3 | Batch loaders resend the same envelope when an append write will not land. | supported | `source_a.md` | 'Nimbrel Relay stalls, batch loaders resend the same envelope, and reads against the same shard begin to time out.' in `source_a.md` -- Directly states batch loaders resend the envelope. |
| 4 | Reads against the same shard begin to time out when an append write will not land. | supported | `source_a.md` | 'Nimbrel Relay stalls, batch loaders resend the same envelope, and reads against the same shard begin to time out.' in `source_a.md` -- Directly states reads against the same shard time out. |
| 5 | The refusal reaches the client. | supported | `source_a.md` | 'The refusal reaches the client and is written to the Relay and Collector logs as well.' in `source_a.md` -- States the refusal reaches the client. |
| 6 | The refusal is written to the Relay and Collector logs as well. | supported | `source_a.md` | 'The refusal reaches the client and is written to the Relay and Collector logs as well.' in `source_a.md` -- States the refusal is written to Relay and Collector logs. |
| 7 | On one managed Nimbrel Ledger deployment (MLS), the share of HTTP 429 replies climbed over a fortnight, as counted at the front proxy. | supported | `source_b.md` | 'This note concerns a managed Nimbrel Ledger deployment (NMD) whose share of HTTP `429` replies climbed over a fortnight, as counted at the front proxy.' in `source_b.md` -- Fortnight climb at front proxy comes from the summary span; the MLS label is completed by the Environment section's 'Deployment: Managed Ledger Service (MLS)' line for the same deployment. |
| 8 | Front proxy counters agreed with client-side reports, confirming the refusals were real rather than a client-side accounting error. | supported | `source_b.md` | 'Front proxy counters agree with the client reports, so the refusals are real and not a client-side accounting error.' in `source_b.md` -- States exactly this confirmation. |
| 9 | A 429 is what the Ledger returns when it refuses work outright rather than queueing it. | supported | `source_b.md` | 'which is what the Ledger does when it refuses work rather than queueing it' in `source_b.md` -- Directly matches the claim's phrasing about refusing rather than queueing. |
| 10 | Investigation pointed to expensive queries and deep grouping as contributing factors. | supported | `source_b.md` | 'It sets out what the evidence pointed at, which was expensive queries and deep grouping, and what was put forward in response.' in `source_b.md` -- States investigation pointed to expensive queries and deep grouping. |
| 11 | A full refusal envelope from a batched append shows the batch refused after 0 of 64 envelopes with a 429 Too Many Requests error, including ingest_and_leader_bytes=88121344, follower_bytes=212992, all_bytes=88334336, ingest_op_bytes=155648, and max_ingest_bytes=88080384. | supported | `source_a.md` | 'append batch refused after 0 of 64 envelopes: 429 Too Many Requests: {"error":{"root_cause":[{"type":"nbl_queue_refused_exception","reason":"refused append on ingest path [ingest_and_leader_bytes=88121344, follower_bytes=212992, all_bytes=88334336, ingest_op_bytes=155648, max_ingest_bytes=88080384]"}]' in `source_a.md` -- The claim's numeric values and description match the sample envelope exactly. |
| 12 | The Ledger operations handbook now covers the same ground under Refused Appends. | supported | `source_a.md` | 'The Ledger operations handbook now covers the same ground under Refused Appends, with a walkthrough for each of the three refusal paths set out below.' in `source_a.md` -- States exactly this. |
| 13 | There are three refusal paths set out in the document. | supported | `source_a.md` | 'with a walkthrough for each of the three refusal paths set out below' in `source_a.md` -- States three refusal paths are set out. |
| 14 | Every Nimbrel Ledger release on every platform can refuse an append this way. | supported | `source_a.md` | 'Every Nimbrel Ledger release on every platform can refuse an append this way.' in `source_a.md` -- Exact match. |
| 15 | One recorded instance of the issue occurred on Nimbrel Ledger version 4.4 and 5.x. | supported | `source_b.md` | 'Version: 4.4, 5.x' in `source_b.md` -- States the recorded instance's version. |
| 16 | The recorded instance ran on Nimbrel Cloud under the Managed Ledger Service (MLS). | supported | `source_b.md` | 'Deployment: Managed Ledger Service (MLS)' in `source_b.md` -- States the deployment ran on Nimbrel Cloud under MLS, matching the Environment section. |
| 17 | The recorded instance occurred in a production environment. | supported | `source_b.md` | 'Production Environment: Yes' in `source_b.md` -- Confirms production environment. |
| 18 | A 429 Too Many Requests reply is what a Ledger node sends once it has nowhere left to put the work. | supported | `source_a.md` | 'is what a Ledger node sends once it has nowhere left to put the work' in `source_a.md` -- Direct match. |
| 19 | A Ledger node has nowhere left to put the work once an append queue or a read queue is full. | supported | `source_a.md` | 'which is to say once an append queue or a read queue is full' in `source_a.md`, **transcription_error** -- Direct match. |
| 20 | There are 3 ways an append draws a 429. | supported | `source_a.md` | 'There are 3 ways an append draws a 429:' in `source_a.md` -- Exact match. |
| 21 | The append or system_append worker pools hold more batches than they have slots for. | supported | `source_a.md` | 'The `append` or `system_append` worker pools hold more batches than they have slots for' in `source_a.md` -- Direct match. |
| 22 | The ingest memory guard has refused the batch. | supported | `source_a.md` | 'The ingest memory guard has refused the batch' in `source_a.md` -- Direct match. |
| 23 | A circuit breaker has tripped. | supported | `source_a.md` | 'A circuit breaker has tripped' in `source_a.md` -- Direct match. |
| 24 | A breaker trips on any operation and is not particular to appends. | supported | `source_a.md` | 'a breaker trips on any operation and is not particular to appends.' in `source_a.md` -- Direct match. |
| 25 | From release 4.6 and release 5.1 onward, appending to a wide_text column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory. | supported | `source_a.md` | 'From release 4.6 and release 5.1 onward, appending to a `wide_text` column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory.' in `source_a.md`, **transcription_error** -- Exact match. |
| 27 | A handful of queries ran for as long as 2 seconds each. | supported | `source_b.md` | 'a handful of queries run for as long as 2 seconds each.' in `source_b.md` -- Direct match. |
| 28 | A worker slot was unavailable for as long as one of the expensive queries held it. | supported | `source_b.md` | 'A worker slot is unavailable for as long as one of them holds it' in `source_b.md` -- Direct match. |
| 29 | The queue behind the unavailable worker slot grew. | supported | `source_b.md` | 'and the queue behind it grows.' in `source_b.md` -- Direct match. |
| 30 | Grouping on channel.id produced a very large number of groups. | supported | `source_b.md` | 'grouping on `channel.id` yields a very large number of groups' in `source_b.md` -- Direct match. |
| 31 | The memory cost of grouping on channel.id was charged to the same pool the append path draws on. | supported | `source_b.md` | 'and the memory that costs is charged to the same pool the append path draws on.' in `source_b.md` -- Direct match. |
| 32 | Processor load looked unremarkable while memory sat high. | supported | `source_b.md` | 'processor load looks unremarkable while memory sits high.' in `source_b.md` -- Direct match. |
| 33 | Splitting a hot stream over more leader shards spreads append load across more nodes. | supported | `source_a.md` | 'Splitting a hot stream over more leader shards spreads append load across more nodes, which helps in some layouts.' in `source_a.md` -- Exact match. |
| 34 | The ingest_guard.memory.leader.ceiling cluster setting defaults to 10% of the heap. | supported | `source_a.md` | 'which defaults to 10% of the heap.' in `source_a.md` -- Direct match. |
| 35 | A higher ceiling lets a node hold more in-flight append memory before refusing. | supported | `source_a.md` | 'A higher ceiling lets a node hold more in-flight append memory before refusing' in `source_a.md` -- Direct match. |
| 36 | A node holding too much memory runs out of memory instead of refusing. | supported | `source_a.md` | 'a node holding too much runs out of memory instead of refusing, which is the worse outcome.' in `source_a.md` -- Direct match. |
| 37 | The ingest_guard.memory.leader.ceiling setting is read at startup. | supported | `source_a.md` | 'The setting is read at startup, so the cluster must be restarted for a change to take.' in `source_a.md` -- States setting is read at startup. |
| 38 | The cluster must be restarted for a change to the ingest_guard.memory.leader.ceiling setting to take effect. | supported | `source_a.md` | 'The setting is read at startup, so the cluster must be restarted for a change to take.' in `source_a.md` -- States the cluster must be restarted for a change to take effect. |
| 39 | Refusals that show up only during a spike usually clear on their own once the queues drain. | supported | `source_a.md` | 'Refusals that show up only during a spike usually clear on their own once the queues drain.' in `source_a.md` -- Exact match. |

## Structure

**9** mechanical check(s) over **63** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **39** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **81**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 4 run(s) over 39 attributed segment(s) — sources interleaved. 9 of 13 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Verbatim violation — an invariant-core token did not survive unchanged

- `b4` (`source_b.md`) — code '`429`' does not survive into the merge unchanged
- `b13` (`source_b.md`) — code '`429`' does not survive into the merge unchanged

### Over budget — declared loss past the ceiling

- 5 absent segments are declared replaced by the same replacement (b10, b11, b7, b8, b9), over the ceiling of 3. One replacement standing in for that many segments has not replaced them, it has dropped them: the detail it names is gone from the document

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **24** departure(s) from its sources. Checking them confirms 20, rejects 1, and leaves 3 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 63 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | Base title chosen over this one. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Nimbrel Ledger append rejected with HTTP 429' and says so (no claim traced to it) |
| `b2` | superseded | Base author/date kept instead. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-001`, `B-002`) |
| `b3` | superseded | Summary heading consolidated into base's Issue Description. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b4` | reworded | Restated as part of Issue Description, MLS name aligned with Environment. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-003 came back CONTRADICTED (`B-003`) |
| `b5` | reworded | Restated to point readers to the merged Cause section. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-005`) |
| `b6` | duplicate | Same heading as base's Environment section. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b7` | reworded | Environment attributes folded into one sentence. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-006`) |
| `b8` | reworded | Environment attributes folded into one sentence. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-007`) |
| `b9` | reworded | Environment attributes folded into one sentence. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-008`) |
| `b10` | reworded | Environment attributes folded into one sentence. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-009`) |
| `b11` | reworded | Environment attributes folded into one sentence. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-010`) |
| `b12` | duplicate | Same heading as base's Issue Description section. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b13` | reworded | Restated within the merged Issue Description paragraph. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-011`, `B-012`) |
| `b14` | reworded | Folded into the same Issue Description sentence as b4. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-013`, `B-014`) |
| `b15` | superseded | Contributing Factors heading consolidated into base's Cause heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b16` | reworded | Bullet list turned into a prose addition under Cause. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-015`) |
| `b17` | reworded | Bullet list turned into a prose addition under Cause. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-016`, `B-017`) |
| `b18` | reworded | Bullet list turned into a prose addition under Cause. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-018`, `B-019`) |
| `b19` | reworded | Bullet list turned into a prose addition under Cause. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-020`) |
| `b20` | reworded | Bullet list turned into a prose addition under Cause. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-021`, `B-022`) |
| `b21` | superseded | Proposed Actions heading consolidated into base's Workaround heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b22` | reworded | Proposed Actions bullets folded into a Workaround paragraph. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-023`, `B-024`) |
| `b23` | reworded | Proposed Actions bullets folded into a Workaround paragraph. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-025`, `B-026`) |
| `b24` | reworded | Proposed Actions bullets folded into a Workaround paragraph. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-027`) |


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
| Duration | 372.9s |
| Generated | 2026-09-27T16:22:32+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup sonnet-5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
