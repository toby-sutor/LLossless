## Verdict

**3 finding(s).** In the claims: 1 partially dropped, 2 partially invented.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 55 |
| Claims extracted from `source_a.md` | 38 |
| Claims extracted from `source_b.md` | 27 |
| Forward — source claims accounted for in the merge | **64/65** |
| Forward — carried only in part | 1 |
| Forward — `source_a.md` claims accounted for | **37/38** (1 in part) |
| Forward — `source_b.md` claims accounted for | **27/27** |
| Reverse — merge claims found in a source | **53/55** |
| Reverse — supported only in part | 2 |
| Evidence grounded | **120/120** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Partly dropped — the merge carries some of this claim

- **A-028** (`source_a.md:42`) — A cluster that refuses appends has been given more work than its hardware can carry.
  - evidence: 'When refusals stem from more work than the hardware can carry' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text identifies excess work as a cause of some refusals, not as the cause of every cluster's refusals.

### Partly invented — the sources carry some of this claim

- **M-037** (`merged.md:45`) — Evidence points to expensive queries as a cause of the append refusals.
  - evidence: 'It sets out what the evidence pointed at, which was expensive queries and deep grouping, and what was put forward in response.' in `source_b.md` (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - rationale: The evidence points to expensive queries for rising 429 refusals, but does not identify those refusals as append refusals.
- **M-038** (`merged.md:45`) — Evidence points to deep grouping as a cause of the append refusals.
  - evidence: 'It sets out what the evidence pointed at, which was expensive queries and deep grouping, and what was put forward in response.' in `source_b.md` (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - rationale: The evidence points to deep grouping for rising 429 refusals, but does not identify those refusals as append refusals.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 38 claim(s): 0 dropped, 0 contradicted, 1 carried in part, 37 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 28 | A cluster that refuses appends has been given more work than its hardware can carry. | 42 | carried in part | 'When refusals stem from more work than the hardware can carry' in `merged.md` -- The text identifies excess work as a cause of some refusals, not as the cause of every cluster's refusals. |
| 1 | Append requests to Nimbrel Ledger can return HTTP 429 `Too Many Requests`. | 8 | carried | 'Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests`.' in `merged.md` -- The text states that append requests return HTTP 429. |
| 2 | When Nimbrel Ledger refuses an append, the write does not land. | 8 | carried | 'Callers see a write that will not land' in `merged.md` -- The text says the refused write will not land. |
| 3 | When Nimbrel Ledger refuses an append, Nimbrel Relay stalls. | 8 | carried | 'Nimbrel Relay stalls' in `merged.md` -- The text lists a Relay stall among the effects of append refusal. |
| 4 | When Nimbrel Ledger refuses an append, batch loaders resend the same envelope. | 8 | carried | 'batch loaders resend the same envelope' in `merged.md` -- The text states that batch loaders resend the same envelope. |
| 5 | When Nimbrel Ledger refuses an append, reads against the same shard begin to time out. | 8 | carried | 'reads against the same shard begin to time out' in `merged.md` -- The text states that reads against the same shard begin to time out. |
| 6 | The Nimbrel Ledger append refusal reaches the client. | 8 | carried | 'The refusal reaches the client' in `merged.md` -- The text explicitly says the refusal reaches the client. |
| 7 | The Nimbrel Ledger append refusal is written to the Relay logs. | 8 | carried | 'is written to the Relay and Collector logs as well' in `merged.md` -- The text explicitly includes the Relay logs. |
| 8 | The Nimbrel Ledger append refusal is written to the Collector logs. | 8 | carried | 'is written to the Relay and Collector logs as well' in `merged.md` -- The text explicitly includes the Collector logs. |
| 9 | The example batched append was refused after 0 of 64 envelopes. | 13 | carried | 'append batch refused after 0 of 64 envelopes' in `merged.md` -- The example gives exactly that refused-envelope count. |
| 10 | The example batched append refusal returned 429 Too Many Requests. | 13 | carried | 'append batch refused after 0 of 64 envelopes: 429 Too Many Requests' in `merged.md` -- The example identifies the refusal as 429 Too Many Requests. |
| 11 | The example batched append refusal has error type `nbl_queue_refused_exception`. | 13 | carried | '"type":"nbl_queue_refused_exception"' in `merged.md` -- The example gives that error type. |
| 12 | The example batched append refusal reports `ingest_and_leader_bytes=88121344`. | 13 | carried | 'ingest_and_leader_bytes=88121344' in `merged.md` -- The example reports the stated ingest-and-leader byte value. |
| 13 | The example batched append refusal reports `follower_bytes=212992`. | 13 | carried | 'follower_bytes=212992' in `merged.md` -- The example reports the stated follower byte value. |
| 14 | The example batched append refusal reports `all_bytes=88334336`. | 13 | carried | 'all_bytes=88334336' in `merged.md` -- The example reports the stated total byte value. |
| 15 | The example batched append refusal reports `ingest_op_bytes=155648`. | 13 | carried | 'ingest_op_bytes=155648' in `merged.md` -- The example reports the stated ingest-operation byte value. |
| 16 | The example batched append refusal reports `max_ingest_bytes=88080384`. | 13 | carried | 'max_ingest_bytes=88080384' in `merged.md` -- The example reports the stated maximum ingest byte value. |
| 17 | Every Nimbrel Ledger release on every platform can refuse an append this way. | 20 | carried | 'Every Nimbrel Ledger release on every platform can refuse an append this way.' in `merged.md` -- The text states the same release and platform scope. |
| 18 | A Ledger node sends a `429 - Too Many Requests` reply once an append queue or a read queue is full. | 24 | carried | 'A [`429 - Too Many Requests` reply](https://docs.nimbrel.example/ledger/http-status-codes) is what a Ledger node sends once it has nowhere left to put the work, which is to say once [an append queue or a read queue is full](https://docs.nimbrel.example/ledger/why-appends-are-refused).' in `merged.md` -- The text connects the reply to a full append or read queue. |
| 19 | There are 3 ways an append draws a 429. | 26 | carried | 'There are 3 ways an append draws a 429:' in `merged.md` -- The text explicitly gives the number of ways. |
| 20 | An append draws a 429 when the `append` or `system_append` worker pools hold more batches than they have slots for. | 28 | carried | 'The `append` or `system_append` worker pools hold more batches than they have slots for (`nbctl pool status --all`)' in `merged.md` -- The text lists this worker-pool condition as a way an append draws a 429. |
| 21 | An append draws a 429 when the ingest memory guard has refused the batch. | 29 | carried | 'The ingest memory guard has refused the batch (`nbctl guard report ingest --counters`). [1]' in `merged.md` -- The text lists refusal by the ingest memory guard as a way an append draws a 429. |
| 22 | An append draws a 429 when a circuit breaker has tripped. | 30 | carried | 'A circuit breaker has tripped (`nbctl breaker list --tripped`)' in `merged.md` -- The text lists a tripped circuit breaker as a way an append draws a 429. |
| 23 | A circuit breaker can trip on any operation. | 30 | carried | 'a breaker trips on any operation' in `merged.md` -- The text says a breaker trips on any operation. |
| 24 | A circuit breaker is not particular to appends. | 30 | carried | 'is not particular to appends' in `merged.md` -- The text says a breaker is not particular to appends. |
| 25 | From release 4.6 and release 5.1 onward, appending to a `wide_text` column draws a 429 whenever the batch would otherwise have run the node out of memory. | 32 | carried | '**From release 4.6 and release 5.1 onward**, appending to a `wide_text` column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory.' in `merged.md` -- The text states the release scope, column type, and out-of-memory condition. |
| 26 | Taking append and query load off the cluster for long enough allows the queues to drain. | 36 | carried | 'Take append and query load off the cluster for long enough that the queues drain and the nodes fall back under their limits.' in `merged.md` -- The text says reducing both loads for long enough lets the queues drain. |
| 27 | Taking append and query load off the cluster for long enough allows the nodes to fall back under their limits. | 36 | carried | 'Take append and query load off the cluster for long enough that the queues drain and the nodes fall back under their limits.' in `merged.md` -- The text says reducing both loads for long enough lets the nodes fall back under their limits. |
| 29 | Larger nodes constitute scale up. | 42 | carried | 'use larger nodes (scale up)' in `merged.md` -- The text equates using larger nodes with scaling up. |
| 30 | More nodes constitute scale out. | 42 | carried | 'or more of them (scale out)' in `merged.md` -- The text equates using more nodes with scaling out. |
| 31 | Splitting a hot stream over more leader shards spreads append load across more nodes. | 44 | carried | 'Splitting a hot stream over more leader shards spreads append load across more nodes' in `merged.md` -- The text states the claimed effect of splitting a hot stream. |
| 32 | Splitting a hot stream over more leader shards helps in some layouts. | 44 | carried | 'Splitting a hot stream over more leader shards spreads append load across more nodes, which helps in some layouts.' in `merged.md` -- The text says this approach helps in some layouts. |
| 33 | The `ingest_guard.memory.leader.ceiling` cluster setting defaults to 10% of the heap. | 50 | carried | 'the `ingest_guard.memory.leader.ceiling` cluster setting, which defaults to 10% of the heap.' in `merged.md` -- The text gives the stated default for the setting. |
| 34 | A higher `ingest_guard.memory.leader.ceiling` lets a node hold more in-flight append memory before refusing. | 50 | carried | 'A higher ceiling lets a node hold more in-flight append memory before refusing' in `merged.md` -- The text states the effect of raising the ceiling. |
| 35 | A node holding too much in-flight append memory runs out of memory instead of refusing. | 50 | carried | 'A higher ceiling lets a node hold more in-flight append memory before refusing, and a node holding too much runs out of memory instead of refusing' in `merged.md` -- The sentence links excess in-flight append memory to running out of memory instead of refusing. |
| 36 | The `ingest_guard.memory.leader.ceiling` setting is read at startup. | 50 | carried | 'The setting is read at startup' in `merged.md` -- The setting referred to is `ingest_guard.memory.leader.ceiling`. |
| 37 | The cluster must be restarted for a change to the `ingest_guard.memory.leader.ceiling` setting to take. | 50 | carried | 'The setting is read at startup, so the cluster must be restarted for a change to take.' in `merged.md` -- The text says a restart is required for a change to that setting to take. |
| 38 | Append refusals that show up only during a spike usually clear on their own once the queues drain. | 52 | carried | 'Refusals that show up only during a spike usually clear on their own once the queues drain.' in `merged.md` -- The text states the claimed behavior of spike-only refusals. |

### `source_b.md` -- 27 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 27 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Devin Okonkwo is the author. | 3 | carried | 'Author: Devin Okonkwo' in `merged.md` -- Devin Okonkwo is listed as an author. |
| 2 | The document was updated on 2026-04-11. | 4 | carried | 'Updated: 2026-04-11' in `merged.md` -- The text lists that update date. |
| 3 | The share of HTTP `429` replies from a managed Nimbrel Ledger deployment (NMD) climbed over a fortnight. | 8 | carried | 'In a managed Nimbrel Ledger deployment (NMD), the share of HTTP `429` replies counted at the front proxy rises over a fortnight' in `merged.md` -- The text describes a rising share of HTTP 429 replies over a fortnight in an NMD deployment. |
| 4 | The front proxy counted the HTTP `429` replies from the managed Nimbrel Ledger deployment (NMD). | 8 | carried | 'In a managed Nimbrel Ledger deployment (NMD), the share of HTTP `429` replies counted at the front proxy rises over a fortnight' in `merged.md` -- The text says the front proxy counted those replies. |
| 5 | The evidence pointed at expensive queries as a cause of the HTTP `429` replies. | 8 | carried | 'Evidence points to expensive queries and deep grouping; the proposed actions address both.' in `merged.md` -- The text identifies expensive queries as a factor in the refusals. |
| 6 | The evidence pointed at deep grouping as a cause of the HTTP `429` replies. | 8 | carried | 'Evidence points to expensive queries and deep grouping; the proposed actions address both.' in `merged.md` -- The text identifies deep grouping as a factor in the refusals. |
| 7 | The product is Nimbrel Ledger. | 12 | carried | '- Product: Nimbrel Ledger' in `merged.md` -- The product field names Nimbrel Ledger. |
| 8 | The versions are 4.4, 5.x. | 13 | carried | '- Version: 4.4, 5.x' in `merged.md` -- The version field lists 4.4 and 5.x. |
| 9 | The platform is Nimbrel Cloud. | 14 | carried | '- Platform: Nimbrel Cloud' in `merged.md` -- The platform field names Nimbrel Cloud. |
| 10 | The deployment is Managed Ledger Service (MLS). | 15 | carried | '- Deployment: Managed Ledger Service (MLS)' in `merged.md` -- The deployment field names Managed Ledger Service (MLS). |
| 11 | The deployment is a production environment. | 16 | carried | '- Production Environment: Yes' in `merged.md` -- The environment field confirms a production environment. |
| 12 | The managed deployment returns HTTP `429` on a growing share of requests. | 20 | carried | 'In a managed Nimbrel Ledger deployment (NMD), the share of HTTP `429` replies counted at the front proxy rises over a fortnight as Ledger refuses work rather than queueing it.' in `merged.md` -- The text says the share of HTTP 429 replies rises in the managed deployment. |
| 13 | The Ledger returns HTTP `429` when it refuses work rather than queueing it. | 20 | carried | 'the share of HTTP `429` replies counted at the front proxy rises over a fortnight as Ledger refuses work rather than queueing it' in `merged.md` -- The text links HTTP 429 replies to Ledger refusing work rather than queueing it. |
| 14 | Front proxy counters agree with the client reports. | 20 | carried | 'Front proxy counters agree with the client reports' in `merged.md` -- The text states that the counters agree with client reports. |
| 15 | The HTTP `429` refusals are not a client-side accounting error. | 20 | carried | 'Front proxy counters agree with the client reports, so the refusals are real and not a client-side accounting error.' in `merged.md` -- The text explicitly rules out a client-side accounting error. |
| 16 | A handful of queries run for as long as 2 seconds each. | 24 | carried | 'a handful of queries run for as long as 2 seconds each' in `merged.md` -- The text gives the same query duration. |
| 17 | A worker slot is unavailable for as long as one of the expensive queries holds it. | 24 | carried | 'A worker slot is unavailable for as long as one of them holds it' in `merged.md` -- In context, “one of them” refers to the expensive queries. |
| 18 | The queue behind a worker slot held by an expensive query grows. | 24 | carried | 'A worker slot is unavailable for as long as one of them holds it, and the queue behind it grows.' in `merged.md` -- The text says the queue grows while a query holds the worker slot. |
| 19 | Grouping on `channel.id` yields a very large number of groups. | 25 | carried | 'grouping on `channel.id` yields a very large number of groups' in `merged.md` -- The text states the same result of grouping on that field. |
| 20 | The memory cost of grouping on `channel.id` is charged to the same pool the append path draws on. | 25 | carried | 'grouping on `channel.id` yields a very large number of groups, and the memory that costs is charged to the same pool the append path draws on' in `merged.md` -- The text assigns the grouping memory cost to the append path’s pool. |
| 21 | Processor load looks unremarkable. | 26 | carried | 'processor load looks unremarkable' in `merged.md` -- The text describes processor load in the same terms. |
| 22 | Memory sits high. | 26 | carried | 'memory sits high' in `merged.md` -- The text states that memory use is high. |
| 23 | The difference between processor load and memory use points at query cost rather than an undersized cluster. | 26 | carried | 'processor load looks unremarkable while memory sits high. The two do not agree, which points at query cost rather than at an undersized cluster.' in `merged.md` -- The text draws the claimed conclusion from the mismatch. |
| 24 | A proposed action is to set the slow query threshold to 1 second. | 30 | carried | '**Lower the slow query threshold**: set it to 1 second' in `merged.md` -- The text proposes setting the threshold to 1 second. |
| 25 | A proposed action is to review the expensive queries with the team that wrote them. | 31 | carried | '**Review what the queries are for**: go through the expensive ones with the team that wrote them' in `merged.md` -- The text proposes reviewing the expensive queries with their authors. |
| 26 | A proposed action is to take a thread dump while the refusal rate is high. | 32 | carried | 'while the refusal rate is high, take a thread dump and a heap snapshot rather than reasoning from counters alone' in `merged.md` -- The text proposes taking a thread dump while refusals are high. |
| 27 | A proposed action is to take a heap snapshot while the refusal rate is high. | 32 | carried | 'while the refusal rate is high, take a thread dump and a heap snapshot rather than reasoning from counters alone' in `merged.md` -- The text proposes taking a heap snapshot while refusals are high. |

### `merged.md` -- 55 claim(s): 0 invented, 0 contradicted, 2 supported in part, 53 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 37 | Evidence points to expensive queries as a cause of the append refusals. | supported in part | `source_b.md` | 'It sets out what the evidence pointed at, which was expensive queries and deep grouping, and what was put forward in response.' in `source_b.md` -- The evidence points to expensive queries for rising 429 refusals, but does not identify those refusals as append refusals. |
| 38 | Evidence points to deep grouping as a cause of the append refusals. | supported in part | `source_b.md` | 'It sets out what the evidence pointed at, which was expensive queries and deep grouping, and what was put forward in response.' in `source_b.md` -- The evidence points to deep grouping for rising 429 refusals, but does not identify those refusals as append refusals. |
| 1 | Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests`. | supported | `source_a.md` | 'Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests`.' in `source_a.md` -- The source states the claim directly. |
| 2 | An append write that receives HTTP 429 `Too Many Requests` will not land. | supported | `source_a.md` | 'Callers see a write that will not land' in `source_a.md` -- The source describes this as the result of an append request receiving HTTP 429. |
| 3 | Nimbrel Relay stalls when append requests are refused. | supported | `source_a.md` | 'Nimbrel Relay stalls' in `source_a.md` -- The source lists this as an effect of refused append requests. |
| 4 | Batch loaders resend the same envelope when append requests are refused. | supported | `source_a.md` | 'batch loaders resend the same envelope' in `source_a.md` -- The source lists this as an effect of refused append requests. |
| 5 | Reads against the same shard begin to time out when append requests are refused. | supported | `source_a.md` | 'reads against the same shard begin to time out' in `source_a.md` -- The source lists this as an effect of refused append requests. |
| 6 | The append refusal reaches the client. | supported | `source_a.md` | 'The refusal reaches the client' in `source_a.md` -- The source states the claim directly. |
| 7 | The append refusal is written to the Relay and Collector logs. | supported | `source_a.md` | 'is written to the Relay and Collector logs as well.' in `source_a.md` -- The source says the refusal is written to both logs. |
| 8 | In a managed Nimbrel Ledger deployment (NMD), the share of HTTP `429` replies counted at the front proxy rises over a fortnight. | supported | `source_b.md` | 'a managed Nimbrel Ledger deployment (NMD) whose share of HTTP `429` replies climbed over a fortnight, as counted at the front proxy.' in `source_b.md` -- The source states the deployment, trend, period, and measurement point. |
| 9 | Ledger refuses work rather than queueing it. | supported | `source_b.md` | 'the Ledger does when it refuses work rather than queueing it.' in `source_b.md` -- The source explicitly describes refusal instead of queueing. |
| 10 | Front proxy counters agree with client reports of HTTP `429` replies. | supported | `source_b.md` | 'Front proxy counters agree with the client reports' in `source_b.md` -- The client reports concern HTTP `429` replies. |
| 11 | The reported refusals are not a client-side accounting error. | supported | `source_b.md` | 'the refusals are real and not a client-side accounting error.' in `source_b.md` -- The source explicitly rules out a client-side accounting error. |
| 12 | A batched append was refused after 0 of 64 envelopes. | supported | `source_a.md` | 'append batch refused after 0 of 64 envelopes' in `source_a.md` -- The refusal envelope states this count. |
| 13 | The batched append refusal returned 429 Too Many Requests. | supported | `source_a.md` | 'append batch refused after 0 of 64 envelopes: 429 Too Many Requests' in `source_a.md` -- The refusal envelope identifies the response as 429 Too Many Requests. |
| 14 | The batched append refusal has type `nbl_queue_refused_exception`. | supported | `source_a.md` | '"type":"nbl_queue_refused_exception"' in `source_a.md` -- The refusal envelope gives this type. |
| 15 | The batched append was refused on the ingest path. | supported | `source_a.md` | 'refused append on ingest path' in `source_a.md` -- The refusal envelope identifies the ingest path. |
| 16 | The batched append refusal reported ingest_and_leader_bytes=88121344. | supported | `source_a.md` | 'ingest_and_leader_bytes=88121344' in `source_a.md` -- The refusal envelope reports this value. |
| 17 | The batched append refusal reported follower_bytes=212992. | supported | `source_a.md` | 'follower_bytes=212992' in `source_a.md` -- The refusal envelope reports this value. |
| 18 | The batched append refusal reported all_bytes=88334336. | supported | `source_a.md` | 'all_bytes=88334336' in `source_a.md` -- The refusal envelope reports this value. |
| 19 | The batched append refusal reported ingest_op_bytes=155648. | supported | `source_a.md` | 'ingest_op_bytes=155648' in `source_a.md` -- The refusal envelope reports this value. |
| 20 | The batched append refusal reported max_ingest_bytes=88080384. | supported | `source_a.md` | 'max_ingest_bytes=88080384' in `source_a.md` -- The refusal envelope reports this value. |
| 21 | The batched append refusal reported status 429. | supported | `source_a.md` | '"status":429' in `source_a.md` -- The refusal envelope reports status 429. |
| 22 | Every Nimbrel Ledger release on every platform can refuse an append this way. | supported | `source_a.md` | 'Every Nimbrel Ledger release on every platform can refuse an append this way.' in `source_a.md` -- The source states the claim directly. |
| 23 | The listed Nimbrel Ledger versions are 4.4, 5.x. | supported | `source_b.md` | '- Version: 4.4, 5.x' in `source_b.md` -- The source lists these versions. |
| 24 | The listed platform for Nimbrel Ledger is Nimbrel Cloud. | supported | `source_b.md` | '- Platform: Nimbrel Cloud' in `source_b.md` -- The source lists this platform. |
| 25 | The listed Nimbrel Ledger deployment is Managed Ledger Service (MLS). | supported | `source_b.md` | '- Deployment: Managed Ledger Service (MLS)' in `source_b.md` -- The source lists this deployment. |
| 26 | The listed Nimbrel Ledger production environment is Yes. | supported | `source_b.md` | '- Production Environment: Yes' in `source_b.md` -- The listed production environment is Yes. |
| 27 | A Ledger node sends a `429 - Too Many Requests` reply once it has nowhere left to put the work. | supported | `source_a.md` | 'is what a Ledger node sends once it has nowhere left to put the work' in `source_a.md` -- The source describes when a Ledger node sends a 429 reply. |
| 28 | A Ledger node can send a `429 - Too Many Requests` reply when an append queue is full. | supported | `source_a.md` | 'A [`429 - Too Many Requests` reply](https://docs.nimbrel.example/ledger/http-status-codes) is what a Ledger node sends once it has nowhere left to put the work, which is to say once [an append queue or a read queue is full](https://docs.nimbrel.example/ledger/why-appends-are-refused).' in `source_a.md` -- The source includes a full append queue as a condition for a 429 reply. |
| 29 | A Ledger node can send a `429 - Too Many Requests` reply when a read queue is full. | supported | `source_a.md` | 'A [`429 - Too Many Requests` reply](https://docs.nimbrel.example/ledger/http-status-codes) is what a Ledger node sends once it has nowhere left to put the work, which is to say once [an append queue or a read queue is full](https://docs.nimbrel.example/ledger/why-appends-are-refused).' in `source_a.md` -- The source includes a full read queue as a condition for a 429 reply. |
| 30 | There are 3 ways an append draws a 429. | supported | `source_a.md` | 'There are 3 ways an append draws a 429:' in `source_a.md` -- The source states the number directly. |
| 31 | An append can draw a 429 when the `append` worker pool holds more batches than it has slots for. | supported | `source_a.md` | '- The `append` or `system_append` worker pools hold more batches than they have slots for (`nbctl pool status --all`)' in `source_a.md` -- The source identifies an overfull `append` worker pool as a way an append draws a 429. |
| 32 | An append can draw a 429 when the `system_append` worker pool holds more batches than it has slots for. | supported | `source_a.md` | '- The `append` or `system_append` worker pools hold more batches than they have slots for (`nbctl pool status --all`)' in `source_a.md` -- The source identifies an overfull `system_append` worker pool as a way an append draws a 429. |
| 33 | An append can draw a 429 when the ingest memory guard has refused the batch. | supported | `source_a.md` | '- The ingest memory guard has refused the batch (`nbctl guard report ingest --counters`). [1]' in `source_a.md` -- The source lists ingest memory guard refusal as a way an append draws a 429. |
| 34 | An append can draw a 429 when a circuit breaker has tripped. | supported | `source_a.md` | '- A circuit breaker has tripped (`nbctl breaker list --tripped`) - a breaker trips on any operation and is not particular to appends.' in `source_a.md` -- The source lists a tripped circuit breaker as a way an append draws a 429. |
| 35 | A circuit breaker trips on any operation and is not particular to appends. | supported | `source_a.md` | 'a breaker trips on any operation and is not particular to appends.' in `source_a.md` -- The source states this directly. |
| 36 | From release 4.6 and release 5.1 onward, appending to a `wide_text` column draws a 429 whenever the batch would otherwise have run the node out of memory. | supported | `source_a.md` | '[1] **From release 4.6 and release 5.1 onward**, appending to a `wide_text` column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory.' in `source_a.md` -- The source states the release condition and out-of-memory condition. |
| 39 | A handful of queries run for as long as 2 seconds each. | supported | `source_b.md` | 'a handful of queries run for as long as 2 seconds each.' in `source_b.md` -- The source states the query duration directly. |
| 40 | A worker slot is unavailable for as long as a query holds it. | supported | `source_b.md` | 'A worker slot is unavailable for as long as one of them holds it' in `source_b.md` -- In context, “one of them” refers to the expensive queries. |
| 41 | The queue behind a worker slot grows while a query holds the slot. | supported | `source_b.md` | 'A worker slot is unavailable for as long as one of them holds it, and the queue behind it grows.' in `source_b.md` -- The source says the queue grows while a query occupies the worker slot. |
| 42 | Grouping on `channel.id` yields a very large number of groups. | supported | `source_b.md` | 'grouping on `channel.id` yields a very large number of groups' in `source_b.md` -- The source states this directly. |
| 43 | Memory used by grouping on `channel.id` is charged to the same pool the append path draws on. | supported | `source_b.md` | 'grouping on `channel.id` yields a very large number of groups, and the memory that costs is charged to the same pool the append path draws on.' in `source_b.md` -- The source identifies the shared memory pool. |
| 44 | Processor load looks unremarkable while memory sits high. | supported | `source_b.md` | 'processor load looks unremarkable while memory sits high.' in `source_b.md` -- The source states this directly. |
| 45 | Taking append and query load off the cluster lets queues drain. | supported | `source_a.md` | 'Take append and query load off the cluster for long enough that the queues drain and the nodes fall back under their limits.' in `source_a.md` -- The source says reducing both loads allows the queues to drain. |
| 46 | Taking append and query load off the cluster lets nodes fall back under their limits. | supported | `source_a.md` | 'Take append and query load off the cluster for long enough that the queues drain and the nodes fall back under their limits.' in `source_a.md` -- The source says reducing both loads allows nodes to fall back under their limits. |
| 47 | Splitting a hot stream over more leader shards spreads append load across more nodes. | supported | `source_a.md` | 'Splitting a hot stream over more leader shards spreads append load across more nodes' in `source_a.md` -- The source states this directly. |
| 48 | Splitting a hot stream over more leader shards helps in some layouts. | supported | `source_a.md` | 'Splitting a hot stream over more leader shards spreads append load across more nodes, which helps in some layouts.' in `source_a.md` -- The source expressly says this helps in some layouts. |
| 49 | The `ingest_guard.memory.leader.ceiling` cluster setting defaults to 10% of the heap. | supported | `source_a.md` | 'the `ingest_guard.memory.leader.ceiling` cluster setting, which defaults to 10% of the heap.' in `source_a.md` -- The source gives that setting and its default. |
| 50 | A higher `ingest_guard.memory.leader.ceiling` lets a node hold more in-flight append memory before refusing. | supported | `source_a.md` | 'A higher ceiling lets a node hold more in-flight append memory before refusing' in `source_a.md` -- The sentence refers to the `ingest_guard.memory.leader.ceiling` setting named immediately before it. |
| 51 | A node holding too much in-flight append memory runs out of memory instead of refusing. | supported | `source_a.md` | 'a node holding too much runs out of memory instead of refusing' in `source_a.md` -- The source says this in the context of holding more in-flight append memory. |
| 52 | The `ingest_guard.memory.leader.ceiling` setting is read at startup. | supported | `source_a.md` | 'The setting is read at startup' in `source_a.md` -- The preceding sentence identifies the setting as `ingest_guard.memory.leader.ceiling`. |
| 53 | The cluster must be restarted for a change to `ingest_guard.memory.leader.ceiling` to take. | supported | `source_a.md` | 'the cluster must be restarted for a change to take' in `source_a.md` -- The passage identifies the change as one to `ingest_guard.memory.leader.ceiling`. |
| 54 | Refusals that show up only during a spike usually clear on their own once the queues drain. | supported | `source_a.md` | 'Refusals that show up only during a spike usually clear on their own once the queues drain.' in `source_a.md` -- The source states the claim verbatim. |
| 55 | Setting the slow query threshold to 1 second records the queries actually responsible instead of averaging them away. | supported | `source_b.md` | 'set it to 1 second, so that the queries actually responsible are recorded instead of averaged away' in `source_b.md` -- The source identifies the threshold being set as the slow query threshold. |

## Structure

**9** mechanical check(s) over **63** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **55** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **65**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 10 run(s) over 51 attributed segment(s) — sources interleaved. 8 of 13 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

No structural finding.

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **13** departure(s) from its sources. Checking them confirms 8, rejects 1, and leaves 4 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 63 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | The title slot keeps the base title. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Nimbrel Ledger append rejected with HTTP 429' and says so (no claim traced to it) |
| `b3` | superseded | The issue slot keeps the base heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b4` | reconciled | The issue sentence combines the measured rise with the refusal behavior. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-003`, `B-004`) |
| `b5` | reworded | The summary's findings move to the cause section. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-005`, `B-006`) |
| `b6` | duplicate | The environment heading already appears in the base. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b12` | duplicate | The issue heading already appears in the base. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b13` | reconciled | The issue sentence combines the measured rise with the refusal behavior. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-012`, `B-013`) |
| `b15` | superseded | The contributing factors move under the base cause heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b17` | reworded | The query explanation joins its list item without indentation. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-017`, `B-018`) |
| `b20` | reworded | The resource-accounting explanation joins its list item. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-023`) |
| `b21` | superseded | The proposed actions move under the base resolution heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b25` | reworded | The reference label becomes prose within the resolution section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a23` | reworded | The hardware remedy is framed for capacity-driven refusals. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-028 came back PARTIAL (`A-028`) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | bf7d5842201d (hosted) |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | gpt-6-sol |
| Model (decompose) | gpt-6-sol |
| Model (verify) | gpt-6-sol |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed 0, thinking decompose, merge, verify, profile openai-reasoning |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 10 live, 0 cached, 0 replayed |
| Tokens | 32,343 in, 22,644 out, 0 cached, 5,014 reasoning |
| Cost | ~$0.29 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 235.5s |
| Generated | 2026-09-27T15:29:44+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `bf7d5842201d`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
