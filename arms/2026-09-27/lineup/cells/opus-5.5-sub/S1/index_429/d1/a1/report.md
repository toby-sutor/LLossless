## Verdict

**4 finding(s).** In the claims: 2 partially dropped, 2 contradicted.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 71 |
| Claims extracted from `source_a.md` | 37 |
| Claims extracted from `source_b.md` | 24 |
| Forward — source claims accounted for in the merge | **57/61** |
| Forward — carried only in part | 2 |
| Forward — `source_a.md` claims accounted for | **37/37** |
| Forward — `source_b.md` claims accounted for | **20/24** (2 in part) |
| Reverse — merge claims found in a source | **71/71** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **132/132** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Partly dropped — the merge carries some of this claim

- **B-012** (`source_b.md:20`) — Front proxy counters agree with the client reports of 429 refusals.
  - evidence: 'Where front proxy counters agree with the client reports' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text raises front proxy counters agreeing with client reports only as a condition and does not state that they did agree.
- **B-013** (`source_b.md:20`) — The 429 refusals are real and not a client-side accounting error.
  - evidence: 'the refusals are real and not a client-side accounting error' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text states the refusals are real only conditionally, when the counters agree, and does not assert it outright.

### Contradicted — the merge states something different

- **B-001** -- the two documents disagree
  - `source_b.md:3` says: The author of the note is Devin Okonkwo.
  - `merged.md` says: 'Author: Priya Raghunathan' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text names a different author.
- **B-002** -- the two documents disagree
  - `source_b.md:4` says: The note was updated on 2026-04-11.
  - `merged.md` says: 'Updated: 2026-03-18' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text gives a different update date.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 37 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 37 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests`. | 8 | carried | 'Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests`.' in `merged.md` -- The reference text states this verbatim. |
| 2 | When Nimbrel Ledger appends are refused with HTTP 429, Nimbrel Relay stalls. | 8 | carried | 'Nimbrel Relay stalls' in `merged.md` -- The consequences of the refusal include Nimbrel Relay stalling. |
| 3 | When Nimbrel Ledger appends are refused with HTTP 429, batch loaders resend the same envelope. | 8 | carried | 'batch loaders resend the same envelope' in `merged.md` -- The consequences of the refusal include batch loaders resending the same envelope. |
| 4 | When Nimbrel Ledger appends are refused with HTTP 429, reads against the same shard begin to time out. | 8 | carried | 'reads against the same shard begin to time out' in `merged.md` -- The consequences of the refusal include reads against the same shard timing out. |
| 5 | The HTTP 429 append refusal reaches the client. | 8 | carried | 'The refusal reaches the client' in `merged.md` -- The reference text states the refusal reaches the client. |
| 6 | The HTTP 429 append refusal is written to the Relay and Collector logs. | 8 | carried | 'is written to the Relay and Collector logs as well' in `merged.md` -- The reference text states the refusal is written to the Relay and Collector logs. |
| 7 | The Ledger operations handbook covers refused appends under a section called Refused Appends. | 16 | carried | 'The Ledger operations handbook now covers the same ground under Refused Appends' in `merged.md` -- The note says the handbook covers the topic under Refused Appends. |
| 8 | The Refused Appends section of the Ledger operations handbook has a walkthrough for each of the three refusal paths. | 16 | carried | 'with a walkthrough for each of the three refusal paths set out below' in `merged.md` -- The note says the handbook section has a walkthrough for each of the three refusal paths. |
| 9 | Every Nimbrel Ledger release on every platform can refuse an append with HTTP 429. | 20 | carried | 'Every Nimbrel Ledger release on every platform can refuse an append this way.' in `merged.md` -- The reference text states every release on every platform can refuse an append this way, meaning with HTTP 429. |
| 10 | A Nimbrel Ledger node sends a 429 - Too Many Requests reply once it has nowhere left to put the work. | 24 | carried | 'A [`429 - Too Many Requests` reply](https://docs.nimbrel.example/ledger/http-status-codes) is what a Ledger node sends once it has nowhere left to put the work' in `merged.md` -- The reference text states a node sends a 429 once it has nowhere left to put the work. |
| 11 | A Nimbrel Ledger node sends a 429 reply once an append queue or a read queue is full. | 24 | carried | 'once [an append queue or a read queue is full](https://docs.nimbrel.example/ledger/why-appends-are-refused)' in `merged.md` -- The reference text states the 429 is sent once an append queue or a read queue is full. |
| 12 | There are 3 ways a Nimbrel Ledger append draws a 429. | 26 | carried | 'There are 3 ways an append draws a 429:' in `merged.md` -- The reference text states there are 3 ways an append draws a 429. |
| 13 | An append draws a 429 when the `append` or `system_append` worker pools hold more batches than they have slots for. | 28 | carried | 'The `append` or `system_append` worker pools hold more batches than they have slots for' in `merged.md` -- This is listed as the first of the three ways an append draws a 429. |
| 14 | Worker pool status can be checked with `nbctl pool status --all`. | 28 | carried | '(`nbctl pool status --all`)' in `merged.md` -- The command is given alongside the worker pool condition as the way to check it. |
| 15 | An append draws a 429 when the ingest memory guard has refused the batch. | 29 | carried | 'The ingest memory guard has refused the batch' in `merged.md` -- This is listed as one of the three ways an append draws a 429. |
| 16 | Ingest memory guard refusals can be checked with `nbctl guard report ingest --counters`. | 29 | carried | '(`nbctl guard report ingest --counters`)' in `merged.md` -- The command is given alongside the ingest memory guard condition as the way to check it. |
| 17 | An append draws a 429 when a circuit breaker has tripped. | 30 | carried | 'A circuit breaker has tripped' in `merged.md` -- This is listed as one of the three ways an append draws a 429. |
| 18 | Tripped circuit breakers can be listed with `nbctl breaker list --tripped`. | 30 | carried | '(`nbctl breaker list --tripped`)' in `merged.md` -- The command is given alongside the tripped circuit breaker condition. |
| 19 | A Nimbrel Ledger circuit breaker trips on any operation and is not particular to appends. | 30 | carried | 'a breaker trips on any operation and is not particular to appends' in `merged.md` -- The reference text states this directly. |
| 20 | From release 4.6 and release 5.1 onward, appending to a `wide_text` column draws a 429 whenever the batch would otherwise have run the node out of memory. | 32 | carried | '**From release 4.6 and release 5.1 onward**, appending to a `wide_text` column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory.' in `merged.md` -- The footnote states this with the same meaning. |
| 21 | A workaround for Nimbrel Ledger append 429s is to take append and query load off the cluster long enough that the queues drain and the nodes fall back under their limits. | 36 | carried | 'Take append and query load off the cluster for long enough that the queues drain and the nodes fall back under their limits.' in `merged.md` -- This is the stated workaround. |
| 22 | Where batches carry `wide_text` columns and the cluster runs release 4.6 or release 5.1 or later, sending fewer envelopes per batch is a workaround. | 38 | carried | 'Where batches carry `wide_text` columns and the cluster runs release 4.6 or release 5.1 or later, send fewer envelopes per batch.' in `merged.md` -- This is stated in the Workaround section. |
| 23 | A Nimbrel Ledger cluster that refuses appends has been given more work than its hardware can carry. | 42 | carried | 'A cluster that refuses appends has been given more work than its hardware can carry' in `merged.md` -- The reference text states this directly. |
| 24 | The resolution for a cluster refusing appends is hardware: larger nodes (scale up) or more nodes (scale out). | 42 | carried | 'so the answer is hardware: larger nodes (scale up), or more of them (scale out)' in `merged.md` -- The resolution is stated as hardware, either scaling up or scaling out. |
| 25 | According to the sizing notes, scaling up should come first in most cases. | 42 | carried | 'Scale up first in most cases' in `merged.md` -- This is stated with attribution to the sizing notes. |
| 26 | According to the sizing notes, scaling out is for when a further copy of the data is wanted for availability. | 42 | carried | 'scale out when what is wanted is a further copy of the data for availability, per [the sizing notes](https://docs.nimbrel.example/ledger/sizing)' in `merged.md` -- This is stated with attribution to the sizing notes. |
| 27 | Splitting a hot stream over more leader shards spreads append load across more nodes. | 44 | carried | 'Splitting a hot stream over more leader shards spreads append load across more nodes' in `merged.md` -- The reference text states this directly. |
| 28 | For `wide_text` columns on release 4.6 and release 5.1 and later, the first step is cutting the number of envelopes in each append batch. | 48 | carried | 'Begin by cutting the number of envelopes in each append batch.' in `merged.md` -- This is the first step listed for wide_text columns on those releases. |
| 29 | For `wide_text` columns on release 4.6 and release 5.1 and later, where smaller batches do not clear the refusals, add processor and memory capacity to the nodes. | 49 | carried | 'Where smaller batches do not clear it, add processor and memory capacity to the nodes.' in `merged.md` -- This is the second step listed for wide_text columns on those releases. |
| 30 | For `wide_text` columns on release 4.6 and release 5.1 and later, raising the `ingest_guard.memory.leader.ceiling` cluster setting should come only after cutting batch size and adding capacity. | 50 | carried | 'Only then raise the `ingest_guard.memory.leader.ceiling` cluster setting' in `merged.md` -- The third step says to raise the setting only after the first two steps. |
| 31 | The `ingest_guard.memory.leader.ceiling` cluster setting defaults to 10% of the heap. | 50 | carried | 'which defaults to 10% of the heap' in `merged.md` -- The reference text states the default is 10% of the heap. |
| 32 | A higher `ingest_guard.memory.leader.ceiling` lets a node hold more in-flight append memory before refusing. | 50 | carried | 'A higher ceiling lets a node hold more in-flight append memory before refusing' in `merged.md` -- The reference text states this directly. |
| 33 | A node holding too much in-flight append memory runs out of memory instead of refusing. | 50 | carried | 'a node holding too much runs out of memory instead of refusing' in `merged.md` -- The reference text states this in the context of in-flight append memory. |
| 34 | The `ingest_guard.memory.leader.ceiling` setting is read at startup. | 50 | carried | 'The setting is read at startup' in `merged.md` -- The reference text states the setting is read at startup. |
| 35 | The cluster must be restarted for a change to `ingest_guard.memory.leader.ceiling` to take effect. | 50 | carried | 'so the cluster must be restarted for a change to take' in `merged.md` -- The reference text states a restart is required for a change to take effect. |
| 36 | Where hardware and setting changes are not possible, the resolution is changing the load: fewer appends, cheaper queries, or both. | 52 | carried | 'Where none of that is open to you, the load itself is what changes: fewer appends, cheaper queries, or both.' in `merged.md` -- The reference text states this with the same meaning. |
| 37 | Append refusals that show up only during a spike usually clear on their own once the queues drain. | 52 | carried | 'Refusals that show up only during a spike usually clear on their own once the queues drain.' in `merged.md` -- The reference text states this directly. |

### `source_b.md` -- 24 claim(s): 0 dropped, 2 contradicted, 2 carried in part, 20 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The author of the note is Devin Okonkwo. | 3 | contradicted | 'Author: Priya Raghunathan' in `merged.md` -- The reference text names a different author. |
| 2 | The note was updated on 2026-04-11. | 4 | contradicted | 'Updated: 2026-03-18' in `merged.md` -- The reference text gives a different update date. |
| 12 | Front proxy counters agree with the client reports of 429 refusals. | 20 | carried in part | 'Where front proxy counters agree with the client reports' in `merged.md` -- The text raises front proxy counters agreeing with client reports only as a condition and does not state that they did agree. |
| 13 | The 429 refusals are real and not a client-side accounting error. | 20 | carried in part | 'the refusals are real and not a client-side accounting error' in `merged.md` -- The text states the refusals are real only conditionally, when the counters agree, and does not assert it outright. |
| 3 | The managed Nimbrel Ledger deployment's share of HTTP `429` replies climbed over a fortnight, as counted at the front proxy. | 8 | carried | 'can take a growing share of requests as counted at the front proxy; on one deployment that share climbed over a fortnight' in `merged.md` -- The reference text states the 429 share, counted at the front proxy, climbed over a fortnight on one managed deployment. |
| 4 | The evidence pointed at expensive queries and deep grouping as causes of the rising 429 replies. | 8 | carried | 'A refusal rate that climbs steadily can point at expensive queries and deep grouping' in `merged.md` -- The generalized statement carries the claim that a rising refusal rate points at expensive queries and deep grouping. |
| 5 | The product is Nimbrel Ledger. | 12 | carried | '- Product: Nimbrel Ledger' in `merged.md` -- The Environment section lists the product as Nimbrel Ledger. |
| 6 | The Nimbrel Ledger version is 4.4, 5.x. | 13 | carried | '- Version: 4.4, 5.x' in `merged.md` -- The Environment section lists the version as 4.4, 5.x. |
| 7 | The platform is Nimbrel Cloud. | 14 | carried | '- Platform: Nimbrel Cloud' in `merged.md` -- The Environment section lists the platform as Nimbrel Cloud. |
| 8 | The deployment is Managed Ledger Service (MLS). | 15 | carried | '- Deployment: Managed Ledger Service (MLS)' in `merged.md` -- The Environment section lists the deployment as Managed Ledger Service (MLS). |
| 9 | The deployment is a production environment. | 16 | carried | '- Production Environment: Yes' in `merged.md` -- The Environment section states it is a production environment. |
| 10 | The managed deployment returns HTTP `429` on a growing share of requests. | 20 | carried | 'On a managed Nimbrel Ledger deployment (NMD), HTTP `429` replies, which the Ledger sends when it refuses work rather than queueing it, can take a growing share of requests' in `merged.md` -- The generalized statement, with the fortnight example, carries the growing share of 429 replies on the managed deployment. |
| 11 | The Ledger returns HTTP `429` when it refuses work rather than queueing it. | 20 | carried | 'which the Ledger sends when it refuses work rather than queueing it' in `merged.md` -- The reference text states this directly. |
| 14 | A handful of queries run for as long as 2 seconds each. | 24 | carried | 'a handful of queries run for as long as 2 seconds each' in `merged.md` -- The reference text states this directly. |
| 15 | A worker slot is unavailable for as long as an expensive query holds it. | 24 | carried | 'A worker slot is unavailable for as long as one of them holds it' in `merged.md` -- The reference text states this about the expensive queries. |
| 16 | The queue behind a worker slot held by an expensive query grows. | 24 | carried | 'and the queue behind it grows' in `merged.md` -- The reference text states the queue behind the held slot grows. |
| 17 | Grouping on `channel.id` yields a very large number of groups. | 25 | carried | 'grouping on `channel.id` yields a very large number of groups' in `merged.md` -- The reference text states this directly. |
| 18 | The memory cost of grouping on `channel.id` is charged to the same pool the append path draws on. | 25 | carried | 'the memory that costs is charged to the same pool the append path draws on' in `merged.md` -- The reference text states this directly. |
| 19 | Processor load looks unremarkable while memory sits high. | 26 | carried | 'processor load looks unremarkable while memory sits high' in `merged.md` -- The reference text states this directly. |
| 20 | The disagreement between processor load and memory points at query cost rather than at an undersized cluster. | 26 | carried | 'The two do not agree, which points at query cost rather than at an undersized cluster.' in `merged.md` -- The reference text states this directly. |
| 21 | The proposed action is to lower the slow query threshold to 1 second. | 30 | carried | '**Lower the slow query threshold**: set it to 1 second' in `merged.md` -- This is listed as a recommended action. |
| 22 | Several of the expensive queries look like they could ask for less. | 31 | carried | 'several of which look like they could ask for less' in `merged.md` -- The reference text states this about the expensive queries. |
| 23 | The proposed action is to take a thread dump and a heap snapshot while the refusal rate is high. | 32 | carried | 'while the refusal rate is high, take a thread dump and a heap snapshot' in `merged.md` -- This is listed as a recommended action. |
| 24 | The internal ticket for this issue is NB-40917. | 38 | carried | '[Internal ticket NB-40917](https://tickets.nimbrel.example/issues/40917)' in `merged.md` -- The References section lists internal ticket NB-40917. |

### `merged.md` -- 71 claim(s): 0 invented, 0 contradicted, 0 supported in part, 71 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | The Nimbrel Ledger append rejected with HTTP 429 document was authored by Priya Raghunathan. | supported | `source_a.md` | 'Author: Priya Raghunathan' in `source_a.md` -- Source A names Priya Raghunathan as author of the append-rejected-with-429 document. |
| 2 | The Nimbrel Ledger append rejected with HTTP 429 document was updated 2026-03-18. | supported | `source_a.md` | 'Updated: 2026-03-18' in `source_a.md` -- Source A gives the update date as 2026-03-18. |
| 3 | Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests`. | supported | `source_a.md` | 'Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests`.' in `source_a.md` -- Stated verbatim in source A. |
| 4 | When Nimbrel Ledger appends are refused with HTTP 429, Nimbrel Relay stalls. | supported | `source_a.md` | 'Nimbrel Relay stalls' in `source_a.md` -- Source A lists Relay stalling as a consequence of the refused append. |
| 5 | When Nimbrel Ledger appends are refused with HTTP 429, batch loaders resend the same envelope. | supported | `source_a.md` | 'batch loaders resend the same envelope' in `source_a.md` -- Source A lists batch loaders resending the same envelope. |
| 6 | When Nimbrel Ledger appends are refused with HTTP 429, reads against the same shard begin to time out. | supported | `source_a.md` | 'reads against the same shard begin to time out' in `source_a.md` -- Source A states reads against the same shard begin to time out. |
| 7 | The HTTP 429 append refusal reaches the client. | supported | `source_a.md` | 'The refusal reaches the client and is written to the Relay and Collector logs as well.' in `source_a.md` -- Source A states the refusal reaches the client. |
| 8 | The HTTP 429 append refusal is written to the Relay and Collector logs. | supported | `source_a.md` | 'The refusal reaches the client and is written to the Relay and Collector logs as well.' in `source_a.md` -- Source A states the refusal is written to the Relay and Collector logs. |
| 9 | The Nimbrel Ledger sends HTTP 429 replies when it refuses work rather than queueing it. | supported | `source_b.md` | 'which is what the Ledger does when it refuses work rather than queueing it' in `source_b.md` -- Source B states that returning 429 is what the Ledger does when it refuses work rather than queueing it. |
| 10 | On a managed Nimbrel Ledger deployment (NMD), HTTP 429 replies can take a growing share of requests as counted at the front proxy. | supported | `source_b.md` | 'This note concerns a managed Nimbrel Ledger deployment (NMD) whose share of HTTP `429` replies climbed over a fortnight, as counted at the front proxy.' in `source_b.md` -- Source B describes an NMD whose share of 429 replies grew as counted at the front proxy; the claim generalises this occasion. |
| 11 | On one managed Nimbrel Ledger deployment, the share of HTTP 429 replies climbed over a fortnight. | supported | `source_b.md` | 'This note concerns a managed Nimbrel Ledger deployment (NMD) whose share of HTTP `429` replies climbed over a fortnight, as counted at the front proxy.' in `source_b.md` -- Source B states the share of 429 replies climbed over a fortnight on one managed deployment. |
| 12 | Where front proxy counters agree with the client reports, the HTTP 429 refusals are real and not a client-side accounting error. | supported | `source_b.md` | 'Front proxy counters agree with the client reports, so the refusals are real and not a client-side accounting error.' in `source_b.md` -- Source B draws this conclusion from the agreement of proxy counters and client reports; the claim generalises it. |
| 13 | In the example refusal envelope, the append batch was refused after 0 of 64 envelopes. | supported | `source_a.md` | 'append batch refused after 0 of 64 envelopes' in `source_a.md` -- The example envelope in source A shows refusal after 0 of 64 envelopes. |
| 14 | In the example refusal envelope, the error type is nbl_queue_refused_exception. | supported | `source_a.md` | '"type":"nbl_queue_refused_exception"' in `source_a.md` -- The example envelope gives the error type as nbl_queue_refused_exception. |
| 15 | In the example refusal envelope, ingest_and_leader_bytes=88121344. | supported | `source_a.md` | 'ingest_and_leader_bytes=88121344' in `source_a.md` -- Value appears in the example envelope in source A. |
| 16 | In the example refusal envelope, follower_bytes=212992. | supported | `source_a.md` | 'follower_bytes=212992' in `source_a.md` -- Value appears in the example envelope in source A. |
| 17 | In the example refusal envelope, all_bytes=88334336. | supported | `source_a.md` | 'all_bytes=88334336' in `source_a.md` -- Value appears in the example envelope in source A. |
| 18 | In the example refusal envelope, ingest_op_bytes=155648. | supported | `source_a.md` | 'ingest_op_bytes=155648' in `source_a.md` -- Value appears in the example envelope in source A. |
| 19 | In the example refusal envelope, max_ingest_bytes=88080384. | supported | `source_a.md` | 'max_ingest_bytes=88080384' in `source_a.md` -- Value appears in the example envelope in source A. |
| 20 | The Ledger operations handbook covers refused appends under Refused Appends. | supported | `source_a.md` | 'The Ledger operations handbook now covers the same ground under Refused Appends' in `source_a.md` -- Source A states the handbook covers this under Refused Appends. |
| 21 | The Ledger operations handbook has a walkthrough for each of the three refusal paths. | supported | `source_a.md` | 'with a walkthrough for each of the three refusal paths set out below' in `source_a.md` -- Source A states the handbook has a walkthrough for each of the three refusal paths. |
| 22 | Every Nimbrel Ledger release on every platform can refuse an append with HTTP 429. | supported | `source_a.md` | 'Every Nimbrel Ledger release on every platform can refuse an append this way.' in `source_a.md` -- Source A states every release on every platform can refuse an append this way, meaning with a 429. |
| 23 | Managed Nimbrel Ledger deployments are affected by HTTP 429 append refusals. | supported | `source_a.md` | 'Every Nimbrel Ledger release on every platform can refuse an append this way.' in `source_a.md` -- Source A says every release on every platform can refuse appends with 429, and source B shows a managed deployment on Nimbrel Cloud returning 429s; together they entail that managed deployments are affected. |
| 24 | The example affected environment runs Nimbrel Ledger versions 4.4, 5.x. | supported | `source_b.md` | '- Version: 4.4, 5.x' in `source_b.md` -- Source B's environment lists versions 4.4, 5.x. |
| 25 | The example affected environment's platform is Nimbrel Cloud. | supported | `source_b.md` | '- Platform: Nimbrel Cloud' in `source_b.md` -- Source B's environment lists the platform as Nimbrel Cloud. |
| 26 | The example affected environment's deployment is Managed Ledger Service (MLS). | supported | `source_b.md` | '- Deployment: Managed Ledger Service (MLS)' in `source_b.md` -- Source B's environment lists the deployment as Managed Ledger Service (MLS). |
| 27 | The example affected environment is a production environment. | supported | `source_b.md` | '- Production Environment: Yes' in `source_b.md` -- Source B marks the environment as production. |
| 28 | A Ledger node sends a 429 - Too Many Requests reply once it has nowhere left to put the work. | supported | `source_a.md` | 'is what a Ledger node sends once it has nowhere left to put the work' in `source_a.md` -- Source A states a node sends a 429 once it has nowhere left to put the work. |
| 29 | A Ledger node sends a 429 reply once an append queue or a read queue is full. | supported | `source_a.md` | 'an append queue or a read queue is full' in `source_a.md` -- Source A equates having nowhere to put the work with an append or read queue being full. |
| 30 | There are 3 ways a Nimbrel Ledger append draws a 429. | supported | `source_a.md` | 'There are 3 ways an append draws a 429:' in `source_a.md` -- Stated directly in source A. |
| 31 | A Nimbrel Ledger append draws a 429 when the append or system_append worker pools hold more batches than they have slots for. | supported | `source_a.md` | 'The `append` or `system_append` worker pools hold more batches than they have slots for' in `source_a.md` -- Source A lists this as one of the three ways an append draws a 429. |
| 32 | The command `nbctl pool status --all` checks the append and system_append worker pools. | supported | `source_a.md` | 'The `append` or `system_append` worker pools hold more batches than they have slots for (`nbctl pool status --all`)' in `source_a.md` -- Source A gives this command alongside the worker pool condition as the way to check it. |
| 33 | A Nimbrel Ledger append draws a 429 when the ingest memory guard has refused the batch. | supported | `source_a.md` | 'The ingest memory guard has refused the batch' in `source_a.md` -- Source A lists the ingest memory guard refusal as a 429 path. |
| 34 | The command `nbctl guard report ingest --counters` checks the ingest memory guard. | supported | `source_a.md` | 'The ingest memory guard has refused the batch (`nbctl guard report ingest --counters`)' in `source_a.md` -- Source A pairs this command with the ingest memory guard condition. |
| 35 | A Nimbrel Ledger append draws a 429 when a circuit breaker has tripped. | supported | `source_a.md` | 'A circuit breaker has tripped' in `source_a.md` -- Source A lists a tripped circuit breaker as a 429 path. |
| 36 | The command `nbctl breaker list --tripped` lists tripped circuit breakers. | supported | `source_a.md` | 'A circuit breaker has tripped (`nbctl breaker list --tripped`)' in `source_a.md` -- Source A pairs this command with the tripped circuit breaker condition. |
| 37 | A Nimbrel Ledger circuit breaker trips on any operation and is not particular to appends. | supported | `source_a.md` | 'a breaker trips on any operation and is not particular to appends' in `source_a.md` -- Stated directly in source A. |
| 38 | From release 4.6 and release 5.1 onward, appending to a wide_text column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory. | supported | `source_a.md` | 'appending to a `wide_text` column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory' in `source_a.md` -- Source A states this for release 4.6 and release 5.1 onward. |
| 39 | A refusal rate that climbs steadily can point at expensive queries and deep grouping. | supported | `source_b.md` | 'It sets out what the evidence pointed at, which was expensive queries and deep grouping' in `source_b.md` -- Source B found that a climbing refusal rate pointed at expensive queries and deep grouping; the claim generalises that occasion. |
| 40 | A handful of queries run for as long as 2 seconds each. | supported | `source_b.md` | 'a handful of queries run for as long as 2 seconds each' in `source_b.md` -- Stated directly in source B. |
| 41 | A worker slot is unavailable for as long as an expensive query holds it. | supported | `source_b.md` | 'A worker slot is unavailable for as long as one of them holds it' in `source_b.md` -- Source B states a worker slot is unavailable while an expensive query holds it. |
| 42 | The queue behind a worker slot held by an expensive query grows. | supported | `source_b.md` | 'and the queue behind it grows' in `source_b.md` -- Source B states the queue behind the held slot grows. |
| 43 | Grouping on channel.id yields a very large number of groups. | supported | `source_b.md` | 'grouping on `channel.id` yields a very large number of groups' in `source_b.md` -- Stated directly in source B. |
| 44 | The memory cost of grouping on channel.id is charged to the same pool the append path draws on. | supported | `source_b.md` | 'the memory that costs is charged to the same pool the append path draws on' in `source_b.md` -- Source B states the grouping memory is charged to the pool the append path uses. |
| 45 | Processor load looks unremarkable while memory sits high. | supported | `source_b.md` | 'processor load looks unremarkable while memory sits high' in `source_b.md` -- Stated directly in source B. |
| 46 | Processor load and memory usage not agreeing points at query cost rather than at an undersized cluster. | supported | `source_b.md` | 'The two do not agree, which points at query cost rather than at an undersized cluster.' in `source_b.md` -- Stated directly in source B. |
| 47 | Taking append and query load off the cluster for long enough lets the queues drain and the nodes fall back under their limits. | supported | `source_a.md` | 'Take append and query load off the cluster for long enough that the queues drain and the nodes fall back under their limits.' in `source_a.md` -- Source A's workaround states this in different words. |
| 48 | Where batches carry wide_text columns and the cluster runs release 4.6 or release 5.1 or later, the workaround is to send fewer envelopes per batch. | supported | `source_a.md` | 'Where batches carry `wide_text` columns and the cluster runs release 4.6 or release 5.1 or later, send fewer envelopes per batch.' in `source_a.md` -- Stated in source A's workaround section. |
| 49 | A cluster that refuses appends has been given more work than its hardware can carry. | supported | `source_a.md` | 'A cluster that refuses appends has been given more work than its hardware can carry' in `source_a.md` -- Stated directly in source A. |
| 50 | The resolution for a cluster that refuses appends is larger nodes (scale up) or more nodes (scale out). | supported | `source_a.md` | 'so the answer is hardware: larger nodes (scale up), or more of them (scale out)' in `source_a.md` -- Source A gives scaling up or out as the resolution. |
| 51 | Per the sizing notes, scale up first in most cases. | supported | `source_a.md` | 'Scale up first in most cases' in `source_a.md` -- Source A attributes this guidance to the sizing notes. |
| 52 | Per the sizing notes, scale out when what is wanted is a further copy of the data for availability. | supported | `source_a.md` | 'scale out when what is wanted is a further copy of the data for availability, per [the sizing notes]' in `source_a.md` -- Source A states this per the sizing notes. |
| 53 | Splitting a hot stream over more leader shards spreads append load across more nodes. | supported | `source_a.md` | 'Splitting a hot stream over more leader shards spreads append load across more nodes' in `source_a.md` -- Stated directly in source A. |
| 54 | Splitting a hot stream over more leader shards helps in some layouts. | supported | `source_a.md` | 'which helps in some layouts' in `source_a.md` -- Source A states splitting helps in some layouts. |
| 55 | For wide_text columns on release 4.6 and release 5.1 and later, the first step is cutting the number of envelopes in each append batch. | supported | `source_a.md` | 'Begin by cutting the number of envelopes in each append batch.' in `source_a.md` -- Source A's first step for wide_text columns on those releases. |
| 56 | For wide_text columns on release 4.6 and release 5.1 and later, where smaller batches do not clear the refusals, add processor and memory capacity to the nodes. | supported | `source_a.md` | 'Where smaller batches do not clear it, add processor and memory capacity to the nodes.' in `source_a.md` -- Source A's second step for wide_text columns. |
| 57 | For wide_text columns, raising the ingest_guard.memory.leader.ceiling cluster setting should come only after cutting batch size and adding capacity. | supported | `source_a.md` | 'Only then raise the `ingest_guard.memory.leader.ceiling` cluster setting' in `source_a.md` -- Source A orders raising the ceiling after cutting batch size and adding capacity. |
| 58 | The ingest_guard.memory.leader.ceiling cluster setting defaults to 10% of the heap. | supported | `source_a.md` | 'which defaults to 10% of the heap' in `source_a.md` -- Source A gives the default as 10% of the heap. |
| 59 | A higher ingest_guard.memory.leader.ceiling lets a node hold more in-flight append memory before refusing. | supported | `source_a.md` | 'A higher ceiling lets a node hold more in-flight append memory before refusing' in `source_a.md` -- Stated directly in source A. |
| 60 | A node holding too much in-flight append memory runs out of memory instead of refusing. | supported | `source_a.md` | 'a node holding too much runs out of memory instead of refusing' in `source_a.md` -- Stated directly in source A. |
| 61 | A node running out of memory is a worse outcome than a node refusing appends. | supported | `source_a.md` | 'a node holding too much runs out of memory instead of refusing, which is the worse outcome' in `source_a.md` -- Source A calls running out of memory the worse outcome compared with refusing. |
| 62 | The ingest_guard.memory.leader.ceiling setting is read at startup. | supported | `source_a.md` | 'The setting is read at startup' in `source_a.md` -- Stated directly in source A. |
| 63 | The cluster must be restarted for a change to ingest_guard.memory.leader.ceiling to take effect. | supported | `source_a.md` | 'so the cluster must be restarted for a change to take' in `source_a.md` -- Stated directly in source A. |
| 64 | Where scaling and setting changes are not possible, the load must change: fewer appends, cheaper queries, or both. | supported | `source_a.md` | 'Where none of that is open to you, the load itself is what changes: fewer appends, cheaper queries, or both.' in `source_a.md` -- Source A says that when the scaling and setting options are unavailable, the load must change. |
| 65 | Refusals that show up only during a spike usually clear on their own once the queues drain. | supported | `source_a.md` | 'Refusals that show up only during a spike usually clear on their own once the queues drain.' in `source_a.md` -- Stated verbatim in source A. |
| 66 | Where query cost rather than an undersized cluster is behind the refusals, the recommended action is to act on the queries. | supported | `source_b.md` | 'go through the expensive ones with the team that wrote them, several of which look like they could ask for less' in `source_b.md` -- Source B found that query cost rather than cluster size was behind the refusals and proposed acting on the queries; the claim generalises that response. |
| 67 | The recommended slow query threshold is 1 second. | supported | `source_b.md` | 'set it to 1 second' in `source_b.md` -- Source B proposes lowering the slow query threshold to 1 second. |
| 68 | Lowering the slow query threshold to 1 second lets the queries actually responsible be recorded instead of averaged away. | supported | `source_b.md` | 'so that the queries actually responsible are recorded instead of averaged away' in `source_b.md` -- Source B gives this as the reason for the 1 second threshold. |
| 69 | The recommendation is to go through the expensive queries with the team that wrote them. | supported | `source_b.md` | 'go through the expensive ones with the team that wrote them' in `source_b.md` -- Stated among source B's proposed actions. |
| 70 | While the refusal rate is high, the recommendation is to take a thread dump and a heap snapshot rather than reasoning from counters alone. | supported | `source_b.md` | 'while the refusal rate is high, take a thread dump and a heap snapshot rather than reasoning from counters alone' in `source_b.md` -- Stated among source B's proposed actions. |
| 71 | The internal ticket for this issue is NB-40917. | supported | `source_b.md` | '[Internal ticket NB-40917](https://tickets.nimbrel.example/issues/40917)' in `source_b.md` -- Source B references internal ticket NB-40917 for this issue. |

## Structure

**9** mechanical check(s) over **63** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **71** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **61**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 8 run(s) over 51 attributed segment(s) — sources interleaved. 9 of 13 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

No structural finding.

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **11** departure(s) from its sources. Checking them confirms 7, rejects 1, and leaves 3 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 63 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | Base title kept. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Nimbrel Ledger append rejected with HTTP 429' and says so (no claim traced to it) |
| `b2` | superseded | Base byline kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-001`, `B-002`) |
| `b3` | superseded | Summary content moved under the base's Issue Description heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b4` | reconciled | Summary and symptom describe one climbing refusal rate. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-003`) |
| `b5` | subsumed | Evidence pointer introduces the causes; responses sit in Resolution. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-004`) |
| `b6` | duplicate | Same heading as base. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b12` | duplicate | Same heading as base. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b13` | reconciled | Symptom and summary describe one climbing refusal rate. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-010`, `B-011`) |
| `b14` | reworded | Stated generally rather than for one deployment. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-012 came back PARTIAL, B-013 came back PARTIAL (`B-012`, `B-013`) |
| `b15` | superseded | Contributing factors consolidated under the base's Cause heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b21` | superseded | Proposed actions consolidated under the base's Resolution heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | 31c2462e2828 (command) -- lineup opus-5.5-sub |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | claude-opus-5-5 -> claude-opus-5-5 |
| Model (decompose) | claude-opus-5-5 -> claude-opus-5-5 |
| Model (verify) | claude-opus-5-5 -> claude-opus-5-5 |
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
| Duration | 278.7s |
| Generated | 2026-09-27T16:16:18+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup opus-5.5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
