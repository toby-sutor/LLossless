## Verdict

**5 finding(s), all in the merge's account of itself.** 5 false departure. The merged document itself carries no finding: 68 source claim(s) checked against the merge, 45 merge claim(s) checked against the sources, and none of the reconciler's checks found content missing, invented, altered or repeated. What is wrong is what the merge said it did. The 9 mechanical checks under Structure below cover what the claims do not: titles, invariant-core tokens, and all 63 source segment(s) — including the ones no claim was drawn from.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 45 |
| Claims extracted from `source_a.md` | 46 |
| Claims extracted from `source_b.md` | 22 |
| Forward — source claims accounted for in the merge | **68/68** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **46/46** |
| Forward — `source_b.md` claims accounted for | **22/22** |
| Reverse — merge claims found in a source | **45/45** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **111/113** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

None in the claims. The 5 finding(s) this run reports are structural and are listed under `## Structure` below.

## Length capped

- `$.decisions[0].reason` was 87 characters, over the 80-character cap; capped to fit

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 46 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 46 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The author of the document is Priya Raghunathan. | 3 | carried | 'Author: Priya Raghunathan' in `merged.md` -- The document header directly states the author name. |
| 2 | The document was updated on 2026-03-18. | 4 | carried | 'Updated: 2026-03-18' in `merged.md` -- The document header directly states the update date. |
| 3 | Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests`. | 8 | carried | 'Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests`.' in `merged.md` -- This is stated verbatim in the issue description. |
| 4 | Callers see a write that will not land. | 8 | carried | 'Callers see a write that will not land' in `merged.md` -- Directly stated in the issue description. |
| 5 | Nimbrel Relay stalls when an append is refused. | 8 | carried | 'Nimbrel Relay stalls' in `merged.md` -- Directly stated as one of the symptoms. |
| 6 | Batch loaders resend the same envelope when an append is refused. | 8 | carried | 'batch loaders resend the same envelope' in `merged.md` -- Directly stated as one of the symptoms. |
| 7 | Reads against the same shard begin to time out when an append is refused. | 8 | carried | 'reads against the same shard begin to time out' in `merged.md` -- Directly stated as one of the symptoms. |
| 8 | The refusal reaches the client. | 8 | carried | 'The refusal reaches the client' in `merged.md` -- Directly stated in the issue description. |
| 9 | The refusal is written to the Relay and Collector logs as well. | 8 | carried | 'is written to the Relay and Collector logs as well' in `merged.md` -- Directly stated in the issue description. |
| 10 | The example refusal envelope from a batched append includes the text "append batch refused after 0 of 64 envelopes: 429 Too Many Requests". | 13 | carried | 'append batch refused after 0 of 64 envelopes: 429 Too Many Requests' in `merged.md` -- This exact text appears in the example refusal envelope code block. |
| 11 | The ingest_and_leader_bytes value in the example refusal envelope is 88121344. | 13 | carried | 'ingest_and_leader_bytes=88121344' in `merged.md` -- This value appears verbatim in the code block. |
| 12 | The follower_bytes value in the example refusal envelope is 212992. | 13 | carried | 'follower_bytes=212992' in `merged.md` -- This value appears verbatim in the code block. |
| 13 | The all_bytes value in the example refusal envelope is 88334336. | 13 | carried | 'all_bytes=88334336' in `merged.md` -- This value appears verbatim in the code block. |
| 14 | The ingest_op_bytes value in the example refusal envelope is 155648. | 13 | carried | 'ingest_op_bytes=155648' in `merged.md` -- This value appears verbatim in the code block. |
| 15 | The max_ingest_bytes value in the example refusal envelope is 88080384. | 13 | carried | 'max_ingest_bytes=88080384' in `merged.md` -- This value appears verbatim in the code block. |
| 16 | The error type in the example refusal envelope is nbl_queue_refused_exception. | 13 | carried | '"type":"nbl_queue_refused_exception"' in `merged.md` -- The error type field in the JSON envelope matches this value. |
| 17 | The Ledger operations handbook covers Refused Appends with a walkthrough for each of the three refusal paths. | 16 | carried | 'The Ledger operations handbook now covers the same ground under Refused Appends, with a walkthrough for each of the three refusal paths set out below.' in `merged.md` -- This note states exactly the claimed fact. |
| 18 | Every Nimbrel Ledger release on every platform can refuse an append this way. | 20 | carried | 'Every Nimbrel Ledger release on every platform can refuse an append this way, including managed deployments such as:' in `merged.md` -- Directly stated in the Environment section. |
| 19 | A Ledger node sends a 429 - Too Many Requests reply once it has nowhere left to put the work. | 24 | carried | 'A [`429 - Too Many Requests` reply](https://docs.nimbrel.example/ledger/http-status-codes) is what a Ledger node sends once it has nowhere left to put the work' in `merged.md` -- Directly stated in the Cause section. |
| 20 | A Ledger node has nowhere left to put the work once an append queue or a read queue is full. | 24 | carried | 'which is to say once [an append queue or a read queue is full](https://docs.nimbrel.example/ledger/why-appends-are-refused)' in `merged.md` -- Directly stated in the Cause section. |
| 21 | There are 3 ways an append draws a 429. | 26 | carried | 'There are 3 ways an append draws a 429:' in `merged.md` -- Directly stated in the Cause section. |
| 22 | The `append` or `system_append` worker pools hold more batches than they have slots for. | 28 | carried | 'The `append` or `system_append` worker pools hold more batches than they have slots for (`nbctl pool status --all`)' in `merged.md` -- Directly stated as the first of the three refusal paths. |
| 23 | The command to check pool status is `nbctl pool status --all`. | 28 | carried | '(`nbctl pool status --all`)' in `merged.md` -- The command is stated alongside the worker pool cause. |
| 24 | The ingest memory guard has refused the batch. | 29 | carried | 'The ingest memory guard has refused the batch (`nbctl guard report ingest --counters`).' in `merged.md` -- Directly stated as the second of the three refusal paths. |
| 25 | The command to check the ingest memory guard is `nbctl guard report ingest --counters`. | 29 | carried | '(`nbctl guard report ingest --counters`)' in `merged.md` -- The command is stated alongside the ingest memory guard cause. |
| 26 | A circuit breaker has tripped. | 30 | carried | 'A circuit breaker has tripped (`nbctl breaker list --tripped`)' in `merged.md` -- Directly stated as one of the three ways an append draws a 429. |
| 27 | The command to list tripped breakers is `nbctl breaker list --tripped`. | 30 | carried | 'A circuit breaker has tripped (`nbctl breaker list --tripped`)' in `merged.md` -- The command is given in parentheses after the breaker trip statement. |
| 28 | A breaker trips on any operation and is not particular to appends. | 30 | carried | 'a breaker trips on any operation and is not particular to appends.' in `merged.md` -- Stated verbatim. |
| 29 | From release 4.6 and release 5.1 onward, appending to a `wide_text` column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory. | 32 | carried | '**From release 4.6 and release 5.1 onward**, appending to a `wide_text` column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory.' in `merged.md` -- Stated nearly verbatim. |
| 30 | The workaround recommends taking append and query load off the cluster for long enough that the queues drain and the nodes fall back under their limits. | 36 | carried | 'Take append and query load off the cluster for long enough that the queues drain and the nodes fall back under their limits.' in `merged.md` -- Matches the workaround statement. |
| 31 | The workaround recommends sending fewer envelopes per batch where batches carry `wide_text` columns and the cluster runs release 4.6 or release 5.1 or later. | 38 | carried | 'Where batches carry `wide_text` columns and the cluster runs release 4.6 or release 5.1 or later, send fewer envelopes per batch.' in `merged.md` -- Matches the workaround statement. |
| 32 | A cluster that refuses appends has been given more work than its hardware can carry. | 42 | carried | 'A cluster that refuses appends has been given more work than its hardware can carry, so the answer is hardware' in `merged.md` -- Directly stated. |
| 33 | The recommended resolution to a cluster refusing appends is hardware: larger nodes (scale up), or more of them (scale out). | 42 | carried | 'so the answer is hardware: larger nodes (scale up), or more of them (scale out).' in `merged.md` -- Directly stated. |
| 34 | Scale up is recommended first in most cases. | 42 | carried | 'Scale up first in most cases' in `merged.md` -- Directly stated. |
| 35 | Scale out is recommended when what is wanted is a further copy of the data for availability. | 42 | carried | 'scale out when what is wanted is a further copy of the data for availability' in `merged.md` -- Directly stated. |
| 36 | Splitting a hot stream over more leader shards spreads append load across more nodes. | 44 | carried | 'Splitting a hot stream over more leader shards spreads append load across more nodes, which helps in some layouts.' in `merged.md` -- Directly stated. |
| 37 | The first resolution step for wide_text columns on release 4.6 and release 5.1 and later is to cut the number of envelopes in each append batch. | 48 | carried | 'Begin by cutting the number of envelopes in each append batch.' in `merged.md` -- Directly stated as first step. |
| 38 | The second resolution step for wide_text columns on release 4.6 and release 5.1 and later is to add processor and memory capacity to the nodes where smaller batches do not clear it. | 49 | carried | 'Where smaller batches do not clear it, add processor and memory capacity to the nodes.' in `merged.md` -- Directly stated as second step. |
| 39 | The third resolution step is to raise the `ingest_guard.memory.leader.ceiling` cluster setting only after the previous steps. | 50 | carried | 'Only then raise the `ingest_guard.memory.leader.ceiling` cluster setting, which defaults to 10% of the heap.' in `merged.md` -- Directly stated as third step, only after previous steps. |
| 40 | The `ingest_guard.memory.leader.ceiling` cluster setting defaults to 10% of the heap. | 50 | carried | 'which defaults to 10% of the heap.' in `merged.md` -- Directly stated. |
| 41 | A higher ceiling lets a node hold more in-flight append memory before refusing. | 50 | carried | 'A higher ceiling lets a node hold more in-flight append memory before refusing' in `merged.md` -- Directly stated. |
| 42 | A node holding too much in-flight append memory runs out of memory instead of refusing. | 50 | carried | 'a node holding too much runs out of memory instead of refusing, which is the worse outcome.' in `merged.md` -- Directly stated. |
| 43 | The `ingest_guard.memory.leader.ceiling` setting is read at startup. | 50 | carried | 'The setting is read at startup, so the cluster must be restarted for a change to take.' in `merged.md` -- Directly stated. |
| 44 | The cluster must be restarted for a change to the `ingest_guard.memory.leader.ceiling` setting to take effect. | 50 | carried | 'The setting is read at startup, so the cluster must be restarted for a change to take.' in `merged.md` -- Directly stated. |
| 45 | Where scaling hardware is not open to you, the recommended change is fewer appends, cheaper queries, or both. | 52 | carried | 'Where none of that is open to you, the load itself is what changes: fewer appends, cheaper queries, or both.' in `merged.md` -- Directly stated. |
| 46 | Refusals that show up only during a spike usually clear on their own once the queues drain. | 52 | carried | 'Refusals that show up only during a spike usually clear on their own once the queues drain.' in `merged.md` -- Directly stated. |

### `source_b.md` -- 22 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 22 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The Nimbrel Ledger deployment is version 4.4, 5.x. | 13 | carried | 'Version: 4.4, 5.x' in `merged.md` -- Directly stated in Environment section. |
| 2 | The platform used is Nimbrel Cloud. | 14 | carried | 'Platform: Nimbrel Cloud' in `merged.md` -- Directly stated in Environment section. |
| 3 | The deployment type is Managed Ledger Service (MLS). | 15 | carried | 'Deployment: Managed Ledger Service (MLS)' in `merged.md` -- Directly stated in Environment section. |
| 4 | The production environment is Yes. | 16 | carried | 'Production Environment: Yes' in `merged.md` -- Directly stated in Environment section. |
| 5 | The managed Nimbrel Ledger deployment's share of HTTP 429 replies climbed over a fortnight, as counted at the front proxy. | 8 | carried | 'the share of `429` replies can climb over a fortnight, as counted at the front proxy' in `merged.md` -- Directly stated in the reference text. |
| 6 | The managed deployment returns HTTP 429 on a growing share of requests. | 20 | carried | 'the share of `429` replies can climb over a fortnight, as counted at the front proxy' in `merged.md` -- The growing share of 429 replies on the managed deployment is stated directly. |
| 7 | The Ledger returns HTTP 429 when it refuses work rather than queueing it. | 20 | carried | 'the Ledger is refusing work rather than queueing it' in `merged.md` -- Directly states the Ledger refuses rather than queues work, which is what produces the 429. |
| 8 | Front proxy counters agree with the client reports. | 20 | carried | 'front proxy counters agree with client reports' in `merged.md` -- Directly stated. |
| 9 | The refusals are real and not a client-side accounting error. | 20 | carried | 'confirming the refusals are real rather than a client-side accounting error' in `merged.md` -- Directly stated. |
| 10 | A handful of queries run for as long as 2 seconds each. | 24 | carried | 'a handful of queries running for as long as 2 seconds each hold a worker slot for that long' in `merged.md` -- Directly stated. |
| 11 | A worker slot is unavailable for as long as one of the expensive queries holds it. | 24 | carried | 'a handful of queries running for as long as 2 seconds each hold a worker slot for that long' in `merged.md` -- States the worker slot is held for the duration of the query. |
| 12 | The queue behind the worker slot grows. | 24 | carried | 'so the queue behind it grows' in `merged.md` -- Directly stated. |
| 13 | Grouping on channel.id yields a very large number of groups. | 25 | carried | 'grouping on `channel.id` can yield a very large number of groups' in `merged.md` -- Directly stated. |
| 14 | The memory cost of grouping on channel.id is charged to the same pool the append path draws on. | 25 | carried | 'whose memory is charged to the same pool the append path draws on' in `merged.md` -- Directly stated. |
| 15 | Processor load looks unremarkable. | 26 | carried | 'Processor load can look unremarkable while memory sits high' in `merged.md` -- Directly stated. |
| 16 | Memory sits high. | 26 | carried | 'Processor load can look unremarkable while memory sits high' in `merged.md` -- Directly stated that memory sits high. |
| 17 | Processor load and memory do not agree. | 26 | carried | 'Processor load can look unremarkable while memory sits high, a mismatch that points at query cost rather than at an undersized cluster' in `merged.md` -- The text explicitly calls this a mismatch between processor load and memory. |
| 18 | The disagreement between processor load and memory points at query cost rather than at an undersized cluster. | 26 | carried | 'a mismatch that points at query cost rather than at an undersized cluster' in `merged.md` -- Directly stated. |
| 19 | The proposed action is to lower the slow query threshold to 1 second. | 30 | carried | 'Lower the slow query threshold to 1 second, so that the queries actually responsible are recorded instead of averaged away' in `merged.md` -- Directly stated as a resolution step. |
| 20 | Lowering the slow query threshold to 1 second would allow the queries actually responsible to be recorded instead of averaged away. | 30 | carried | 'so that the queries actually responsible are recorded instead of averaged away' in `merged.md` -- Directly stated. |
| 21 | The proposed action is to go through the expensive queries with the team that wrote them. | 31 | carried | 'Review the expensive queries with the team that wrote them; several may be able to ask for less.' in `merged.md` -- Directly stated as a resolution step. |
| 22 | The proposed action is to take a thread dump and a heap snapshot while the refusal rate is high. | 32 | carried | 'Capture evidence while the refusal rate is high - a thread dump and a heap snapshot - rather than reasoning from counters alone.' in `merged.md` -- Directly stated as a resolution step. |

### `merged.md` -- 45 claim(s): 0 invented, 0 contradicted, 0 supported in part, 45 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests`. | supported | `source_a.md` | 'Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests`.' in `source_a.md` -- Directly stated in the issue description. |
| 2 | Callers see a write that will not land. | supported | `source_a.md` | 'Callers see a write that will not land' in `source_a.md` -- Directly stated in the issue description. |
| 3 | Nimbrel Relay stalls. | supported | `source_a.md` | 'Nimbrel Relay stalls' in `source_a.md` -- Directly stated in the issue description. |
| 4 | Batch loaders resend the same envelope. | supported | `source_a.md` | 'batch loaders resend the same envelope' in `source_a.md` -- Directly stated in the issue description. |
| 5 | Reads against the same shard begin to time out. | supported | `source_a.md` | 'reads against the same shard begin to time out' in `source_a.md` -- Directly stated in the issue description. |
| 6 | The refusal reaches the client. | supported | `source_a.md` | 'The refusal reaches the client' in `source_a.md` -- Directly stated in the issue description. |
| 7 | The refusal is written to the Relay and Collector logs as well. | supported | `source_a.md` | 'and is written to the Relay and Collector logs as well.' in `source_a.md` -- Directly stated in the issue description. |
| 8 | On a managed Nimbrel Ledger deployment, the share of 429 replies can climb over a fortnight, as counted at the front proxy. | supported | `source_b.md` | 'whose share of HTTP `429` replies climbed over a fortnight, as counted at the front proxy' in `source_b.md` -- Directly stated in the summary. |
| 9 | The Ledger is refusing work rather than queueing it. | supported | `source_b.md` | 'which is what the Ledger does when it refuses work rather than queueing it' in `source_b.md` -- Directly stated in the issue description. |
| 10 | Front proxy counters agree with client reports. | supported | `source_b.md` | 'Front proxy counters agree with the client reports' in `source_b.md` -- Directly stated in the issue description. |
| 11 | The refusals are real rather than a client-side accounting error. | supported | `source_b.md` | 'so the refusals are real and not a client-side accounting error' in `source_b.md` -- Directly stated in the issue description. |
| 12 | A batch append was refused after 0 of 64 envelopes, returning 429 Too Many Requests. | supported | `source_a.md` | 'append batch refused after 0 of 64 envelopes: 429 Too Many Requests' in `source_a.md` -- Directly quoted from the sample refusal envelope. |
| 13 | The Ledger operations handbook now covers the same ground under Refused Appends. | supported | `source_a.md` | 'The Ledger operations handbook now covers the same ground under Refused Appends' in `source_a.md` -- Directly stated in the note. |
| 14 | The Ledger operations handbook provides a walkthrough for each of the three refusal paths. | supported | `source_a.md` | 'with a walkthrough for each of the three refusal paths set out below.' in `source_a.md` -- Directly stated in the note. |
| 15 | Every Nimbrel Ledger release on every platform can refuse an append this way. | supported | `source_a.md` | 'Every Nimbrel Ledger release on every platform can refuse an append this way.' in `source_a.md` -- Directly stated in the environment section. |
| 16 | The product is Nimbrel Ledger. | supported | `source_b.md` | 'Product: Nimbrel Ledger' in `source_b.md` -- Directly listed in the environment section. |
| 17 | The affected versions are 4.4, 5.x. | supported | `source_b.md` | 'Version: 4.4, 5.x' in `source_b.md` -- Directly listed in the environment section. |
| 18 | The platform is Nimbrel Cloud. | supported | `source_b.md` | 'Platform: Nimbrel Cloud' in `source_b.md` -- Directly listed in the environment section. |
| 19 | The deployment is Managed Ledger Service (MLS). | supported | `source_b.md` | 'Deployment: Managed Ledger Service (MLS)' in `source_b.md` -- Directly listed in the environment section. |
| 20 | The production environment value is Yes. | supported | `source_b.md` | 'Production Environment: Yes' in `source_b.md` -- Directly listed in the environment section. |
| 21 | A 429 - Too Many Requests reply is what a Ledger node sends once it has nowhere left to put the work. | supported | `source_a.md` | 'is what a Ledger node sends once it has nowhere left to put the work' in `source_a.md` -- Directly stated in the cause section. |
| 22 | A Ledger node has nowhere left to put the work once an append queue or a read queue is full. | supported | `source_a.md` | 'which is to say once an append queue or a read queue is full' in `source_a.md`, **transcription_error** -- Directly stated in the cause section. |
| 23 | There are 3 ways an append draws a 429. | supported | `source_a.md` | 'There are 3 ways an append draws a 429:' in `source_a.md` -- Directly stated in the cause section. |
| 24 | The `append` or `system_append` worker pools can hold more batches than they have slots for, as shown by `nbctl pool status --all`. | supported | `source_a.md` | 'The `append` or `system_append` worker pools hold more batches than they have slots for (`nbctl pool status --all`)' in `source_a.md` -- Directly stated in the cause section list. |
| 25 | The ingest memory guard can refuse the batch, as reported by `nbctl guard report ingest --counters`. | supported | `source_a.md` | 'The ingest memory guard has refused the batch (`nbctl guard report ingest --counters`).' in `source_a.md` -- Directly stated in the cause section list. |
| 26 | A circuit breaker can trip, as shown by `nbctl breaker list --tripped`. | supported | `source_a.md` | 'A circuit breaker has tripped (`nbctl breaker list --tripped`)' in `source_a.md` -- Source_a lists this exact mechanism as one of the three ways an append draws a 429. |
| 27 | A breaker trips on any operation and is not particular to appends. | supported | `source_a.md` | 'a breaker trips on any operation and is not particular to appends' in `source_a.md` -- Source_a states this directly about circuit breakers. |
| 28 | From release 4.6 and release 5.1 onward, appending to a `wide_text` column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory. | supported | `source_a.md` | '**From release 4.6 and release 5.1 onward**, appending to a `wide_text` column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory.' in `source_a.md` -- This is verbatim from source_a's footnote. |
| 29 | The ingest memory guard's pool can also be filled by query cost rather than by appends themselves. | supported | `source_b.md` | 'the memory that costs is charged to the same pool the append path draws on' in `source_b.md` -- Source_b states query grouping memory is charged to the append path's pool, and source_a identifies that pool as governed by the ingest memory guard, jointly entailing the claim. |
| 30 | A handful of queries running for as long as 2 seconds each hold a worker slot for that long. | supported | `source_b.md` | 'a handful of queries run for as long as 2 seconds each. A worker slot is unavailable for as long as one of them holds it' in `source_b.md` -- Directly stated in source_b's contributing factors. |
| 31 | The queue behind the worker slot grows as a result of queries holding it for that long. | supported | `source_b.md` | 'and the queue behind it grows' in `source_b.md` -- Directly stated in the same passage of source_b. |
| 32 | Grouping on `channel.id` can yield a very large number of groups. | supported | `source_b.md` | 'grouping on `channel.id` yields a very large number of groups' in `source_b.md` -- Directly stated in source_b. |
| 33 | The memory of those groups is charged to the same pool the append path draws on. | supported | `source_b.md` | 'the memory that costs is charged to the same pool the append path draws on' in `source_b.md` -- Directly stated in source_b. |
| 34 | Processor load can look unremarkable while memory sits high. | supported | `source_b.md` | 'processor load looks unremarkable while memory sits high' in `source_b.md` -- Directly stated in source_b. |
| 35 | A cluster that refuses appends has been given more work than its hardware can carry. | supported | `source_a.md` | 'A cluster that refuses appends has been given more work than its hardware can carry, so the answer is hardware' in `source_a.md` -- Directly stated in source_a's Resolution section. |
| 36 | Scale up means using larger nodes. | supported | `source_a.md` | 'larger nodes (scale up)' in `source_a.md` -- Directly stated in source_a. |
| 37 | Scale out means using more nodes. | supported | `source_a.md` | 'or more of them (scale out)' in `source_a.md` -- Directly stated in source_a. |
| 38 | Scaling out provides a further copy of the data for availability. | supported | `source_a.md` | 'scale out when what is wanted is a further copy of the data for availability' in `source_a.md` -- Directly stated in source_a. |
| 39 | Splitting a hot stream over more leader shards spreads append load across more nodes. | supported | `source_a.md` | 'Splitting a hot stream over more leader shards spreads append load across more nodes, which helps in some layouts.' in `source_a.md` -- Directly stated in source_a. |
| 40 | The `ingest_guard.memory.leader.ceiling` cluster setting defaults to 10% of the heap. | supported | `source_a.md` | 'which defaults to 10% of the heap' in `source_a.md` -- Directly stated in source_a's Resolution section. |
| 41 | A higher `ingest_guard.memory.leader.ceiling` setting lets a node hold more in-flight append memory before refusing. | supported | `source_a.md` | 'A higher ceiling lets a node hold more in-flight append memory before refusing.' in `source_a.md`, **transcription_error** -- Directly stated in source_a. |
| 42 | A node holding too much memory runs out of memory instead of refusing. | supported | `source_a.md` | 'a node holding too much runs out of memory instead of refusing, which is the worse outcome.' in `source_a.md` -- Directly stated in source_a. |
| 43 | The `ingest_guard.memory.leader.ceiling` setting is read at startup. | supported | `source_a.md` | 'The setting is read at startup' in `source_a.md` -- Directly stated in source_a. |
| 44 | The cluster must be restarted for a change to the `ingest_guard.memory.leader.ceiling` setting to take effect. | supported | `source_a.md` | 'so the cluster must be restarted for a change to take' in `source_a.md` -- Directly stated in source_a. |
| 45 | Refusals that show up only during a spike usually clear on their own once the queues drain. | supported | `source_a.md` | 'Refusals that show up only during a spike usually clear on their own once the queues drain.' in `source_a.md` -- Directly stated in source_a's closing paragraph. |

## Structure

**9** mechanical check(s) over **63** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **45** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **68**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 6 run(s) over 44 attributed segment(s) — sources interleaved. 9 of 13 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

`[-...-]` is what the source said and `{+...+}` is what the merge says.

### Declared gone, still here — a record says the content departed and the merge carries the segment unchanged

- `b7` (`source_b.md`) — 'Product: Nimbrel Ledger' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Product: Nimbrel Ledger
  In the merge:  - Product: Nimbrel Ledger
  What changed:  {+-+} Product: Nimbrel Ledger
  ```
- `b8` (`source_b.md`) — 'Version: 4.4, 5.x' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Version: 4.4, 5.x
  In the merge:  - Version: 4.4, 5.x
  What changed:  {+-+} Version: 4.4, 5.x
  ```
- `b9` (`source_b.md`) — 'Platform: Nimbrel Cloud' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Platform: Nimbrel Cloud
  In the merge:  - Platform: Nimbrel Cloud
  What changed:  {+-+} Platform: Nimbrel Cloud
  ```
- `b10` (`source_b.md`) — 'Deployment: Managed Ledger Service (MLS)' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Deployment: Managed Ledger Service (MLS)
  In the merge:  - Deployment: Managed Ledger Service (MLS)
  What changed:  {+-+} Deployment: Managed Ledger Service (MLS)
  ```
- `b11` (`source_b.md`) — 'Production Environment: Yes' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Production Environment: Yes
  In the merge:  - Production Environment: Yes
  What changed:  {+-+} Production Environment: Yes
  ```

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **25** departure(s) from its sources. Checking them confirms 18, rejects 0, and leaves 7 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 63 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a11` | reworded | Extended to introduce the specific managed-deployment details that follow. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-018`) |
| `b1` | superseded | Base title chosen instead. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Nimbrel Ledger append rejected with HTTP 429' and says so (no claim traced to it) |
| `b2` | superseded | Base byline chosen instead. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b3` | superseded | Folded under base's Issue Description heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b4` | subsumed | Merged with b12-b14 into one Issue Description sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-005`) |
| `b5` | subsumed | Its preview of the evidence is carried by the detailed Cause paragraph. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b6` | duplicate | Same heading as base's Environment section. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b7` | subsumed | Folded into combined Environment section list. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b8` | subsumed | Folded into combined Environment section list. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-001`) |
| `b9` | subsumed | Folded into combined Environment section list. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-002`) |
| `b10` | subsumed | Folded into combined Environment section list. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-003`) |
| `b11` | subsumed | Folded into combined Environment section list. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-004`) |
| `b12` | subsumed | Merged with b4, b13, b14 into one Issue Description sentence. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b13` | subsumed | Merged with b4, b12, b14 into one Issue Description sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-006`, `B-007`) |
| `b14` | subsumed | Merged with b4, b12, b13 into one Issue Description sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-008`, `B-009`) |
| `b15` | superseded | Folded under base's Cause heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b16` | subsumed | Folded into the combined Cause paragraph on query-driven memory pressure. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-010`) |
| `b17` | subsumed | Folded into the combined Cause paragraph on query-driven memory pressure. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-011`, `B-012`) |
| `b18` | subsumed | Folded into the combined Cause paragraph on query-driven memory pressure. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-013`, `B-014`) |
| `b19` | subsumed | Folded into the combined Cause paragraph on query-driven memory pressure. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-015`, `B-016`) |
| `b20` | subsumed | Folded into the combined Cause paragraph on query-driven memory pressure. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-017`, `B-018`) |
| `b21` | superseded | Folded under base's Resolution heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b22` | reworded | Bold markdown label dropped, listed as a numbered resolution step. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-019`, `B-020`) |
| `b23` | reworded | Bold markdown label dropped, listed as a numbered resolution step. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-021`) |
| `b24` | reworded | Bold markdown label dropped, listed as a numbered resolution step. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-022`) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | ec0c9ecb43e3 (hosted) |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | claude-sonnet-5 |
| Model (decompose) | claude-sonnet-5 |
| Model (verify) | claude-sonnet-5 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile anthropic |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 9 live, 0 cached, 0 replayed |
| Tokens | 43,263 in, 80,705 out |
| Cost | ~$0.89 estimated (rates read 2026-08-31) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 670.0s |
| Generated | 2026-09-27T16:07:43+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
