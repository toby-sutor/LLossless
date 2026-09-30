## Verdict

**2 finding(s).** In the claims: 1 contradicted, 1 partially invented.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 76 |
| Claims extracted from `source_a.md` | 47 |
| Claims extracted from `source_b.md` | 27 |
| Forward — source claims accounted for in the merge | **74/74** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **47/47** |
| Forward — `source_b.md` claims accounted for | **27/27** |
| Reverse — merge claims found in a source | **74/76** |
| Reverse — supported only in part | 1 |
| Evidence grounded | **150/150** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **M-004** -- the two documents disagree
  - `merged.md:7` says: The document "Nimbrel Ledger append rejected with HTTP 429" was updated on 2026-04-11.
  - `source_a.md` says: 'Updated: 2026-03-18' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The document with this title was updated 2026-03-18; the date 2026-04-11 belongs to the differently titled source B document.

### Partly invented — the sources carry some of this claim

- **M-003** (`merged.md:6`) — Devin Okonkwo is an author of the document "Nimbrel Ledger append rejected with HTTP 429".
  - evidence: 'Author: Devin Okonkwo' in `source_b.md` (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - rationale: Devin Okonkwo is named as an author, but of the differently titled source B document, not of the document with this title.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 47 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 47 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The document "Nimbrel Ledger append rejected with HTTP 429" was authored by Priya Raghunathan. | 3 | carried | 'Author: Priya Raghunathan' in `merged.md` -- The document lists Priya Raghunathan as an author. |
| 2 | The document "Nimbrel Ledger append rejected with HTTP 429" was updated on 2026-03-18. | 4 | carried | 'Updated: 2026-03-18' in `merged.md` -- The document lists this update date. |
| 3 | Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests`. | 8 | carried | 'Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests`.' in `merged.md` -- Stated verbatim in the issue description. |
| 4 | When Nimbrel Ledger append requests are refused with HTTP 429, Nimbrel Relay stalls. | 8 | carried | 'Nimbrel Relay stalls' in `merged.md` -- The issue description lists the Relay stalling as a symptom. |
| 5 | When Nimbrel Ledger append requests are refused with HTTP 429, batch loaders resend the same envelope. | 8 | carried | 'batch loaders resend the same envelope' in `merged.md` -- The issue description lists this symptom. |
| 6 | When Nimbrel Ledger append requests are refused with HTTP 429, reads against the same shard begin to time out. | 8 | carried | 'reads against the same shard begin to time out' in `merged.md` -- The issue description lists this symptom. |
| 7 | The HTTP 429 append refusal from Nimbrel Ledger reaches the client. | 8 | carried | 'The refusal reaches the client' in `merged.md` -- Stated directly. |
| 8 | The HTTP 429 append refusal from Nimbrel Ledger is written to the Relay and Collector logs. | 8 | carried | 'is written to the Relay and Collector logs as well' in `merged.md` -- Stated directly. |
| 9 | In the example refusal envelope, the append batch was refused after 0 of 64 envelopes. | 13 | carried | 'append batch refused after 0 of 64 envelopes' in `merged.md` -- The example envelope begins with this text. |
| 10 | In the example refusal envelope, the error type is nbl_queue_refused_exception. | 13 | carried | '"type":"nbl_queue_refused_exception"' in `merged.md` -- The example envelope gives this error type. |
| 11 | In the example refusal envelope, the reason given is "refused append on ingest path". | 13 | carried | '"reason":"refused append on ingest path [' in `merged.md` -- The example envelope gives this reason. |
| 12 | In the example refusal envelope, ingest_and_leader_bytes is 88121344. | 13 | carried | 'ingest_and_leader_bytes=88121344' in `merged.md` -- The value appears in the example envelope. |
| 13 | In the example refusal envelope, follower_bytes is 212992. | 13 | carried | 'follower_bytes=212992' in `merged.md` -- The value appears in the example envelope. |
| 14 | In the example refusal envelope, all_bytes is 88334336. | 13 | carried | 'all_bytes=88334336' in `merged.md` -- The value appears in the example envelope. |
| 15 | In the example refusal envelope, ingest_op_bytes is 155648. | 13 | carried | 'ingest_op_bytes=155648' in `merged.md` -- The value appears in the example envelope. |
| 16 | In the example refusal envelope, max_ingest_bytes is 88080384. | 13 | carried | 'max_ingest_bytes=88080384' in `merged.md` -- The value appears in the example envelope. |
| 17 | In the example refusal envelope, the status is 429. | 13 | carried | '"status":429' in `merged.md` -- The example envelope ends with status 429. |
| 18 | The Ledger operations handbook covers refused appends under Refused Appends. | 16 | carried | 'The Ledger operations handbook now covers the same ground under Refused Appends' in `merged.md` -- The note states this. |
| 19 | The Ledger operations handbook has a walkthrough for each of the three refusal paths. | 16 | carried | 'with a walkthrough for each of the three refusal paths set out below' in `merged.md` -- The note states the handbook has a walkthrough per refusal path. |
| 20 | Every Nimbrel Ledger release on every platform can refuse an append with HTTP 429. | 20 | carried | 'Every Nimbrel Ledger release on every platform can refuse an append this way.' in `merged.md` -- The environment section states this, with 'this way' referring to the HTTP 429 refusal. |
| 21 | A `429 - Too Many Requests` reply is what a Ledger node sends once an append queue or a read queue is full. | 24 | carried | 'is what a Ledger node sends once it has nowhere left to put the work, which is to say once [an append queue or a read queue is full]' in `merged.md` -- The cause section states this. |
| 22 | There are 3 ways a Nimbrel Ledger append draws a 429. | 26 | carried | 'There are 3 ways an append draws a 429:' in `merged.md` -- Stated directly. |
| 23 | A Nimbrel Ledger append draws a 429 when the `append` or `system_append` worker pools hold more batches than they have slots for. | 28 | carried | 'The `append` or `system_append` worker pools hold more batches than they have slots for' in `merged.md` -- Listed as one of the three ways. |
| 24 | The command `nbctl pool status --all` shows the state of the `append` and `system_append` worker pools. | 28 | carried | 'The `append` or `system_append` worker pools hold more batches than they have slots for (`nbctl pool status --all`)' in `merged.md` -- The command is given alongside the worker pool condition as the way to check it. |
| 25 | A Nimbrel Ledger append draws a 429 when the ingest memory guard has refused the batch. | 29 | carried | 'The ingest memory guard has refused the batch' in `merged.md` -- Listed as one of the three ways. |
| 26 | The command `nbctl guard report ingest --counters` reports ingest memory guard refusals. | 29 | carried | 'The ingest memory guard has refused the batch (`nbctl guard report ingest --counters`)' in `merged.md` -- The command is given alongside the ingest memory guard condition. |
| 27 | A Nimbrel Ledger append draws a 429 when a circuit breaker has tripped. | 30 | carried | 'A circuit breaker has tripped' in `merged.md` -- Listed as one of the three ways. |
| 28 | The command `nbctl breaker list --tripped` lists tripped circuit breakers. | 30 | carried | 'A circuit breaker has tripped (`nbctl breaker list --tripped`)' in `merged.md` -- The command is given alongside the circuit breaker condition. |
| 29 | A Nimbrel Ledger circuit breaker trips on any operation and is not particular to appends. | 30 | carried | 'a breaker trips on any operation and is not particular to appends' in `merged.md` -- Stated directly. |
| 30 | From release 4.6 and release 5.1 onward, appending to a `wide_text` column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory. | 32 | carried | '**From release 4.6 and release 5.1 onward**, appending to a `wide_text` column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory.' in `merged.md` -- Stated in footnote 1. |
| 31 | The workaround for Nimbrel Ledger 429 append refusals is to take append and query load off the cluster for long enough that the queues drain and the nodes fall back under their limits. | 36 | carried | 'Take append and query load off the cluster for long enough that the queues drain and the nodes fall back under their limits.' in `merged.md` -- Stated in the workaround section. |
| 32 | Where batches carry `wide_text` columns and the cluster runs release 4.6 or release 5.1 or later, the workaround is to send fewer envelopes per batch. | 38 | carried | 'Where batches carry `wide_text` columns and the cluster runs release 4.6 or release 5.1 or later, send fewer envelopes per batch.' in `merged.md` -- Stated in the workaround section. |
| 33 | A Nimbrel Ledger cluster that refuses appends has been given more work than its hardware can carry. | 42 | carried | 'A cluster that refuses appends has been given more work than its hardware can carry' in `merged.md` -- Stated in the resolution section. |
| 34 | The resolution for a Nimbrel Ledger cluster that refuses appends is larger nodes (scale up) or more nodes (scale out). | 42 | carried | 'so the answer is hardware: larger nodes (scale up), or more of them (scale out)' in `merged.md` -- Stated in the resolution section. |
| 35 | Per the sizing notes, scale up first in most cases. | 42 | carried | 'Scale up first in most cases' in `merged.md` -- Stated and attributed to the sizing notes. |
| 36 | Per the sizing notes, scale out when what is wanted is a further copy of the data for availability. | 42 | carried | 'scale out when what is wanted is a further copy of the data for availability, per [the sizing notes]' in `merged.md` -- Stated and attributed to the sizing notes. |
| 37 | Splitting a hot stream over more leader shards spreads append load across more nodes. | 44 | carried | 'Splitting a hot stream over more leader shards spreads append load across more nodes' in `merged.md` -- Stated directly. |
| 38 | For `wide_text` columns on release 4.6 and release 5.1 and later, the first step is cutting the number of envelopes in each append batch. | 48 | carried | '1. Begin by cutting the number of envelopes in each append batch.' in `merged.md` -- This is step 1 of the wide_text list. |
| 39 | For `wide_text` columns on release 4.6 and release 5.1 and later, where smaller batches do not clear the refusals, the second step is to add processor and memory capacity to the nodes. | 49 | carried | '2. Where smaller batches do not clear it, add processor and memory capacity to the nodes.' in `merged.md` -- This is step 2 of the wide_text list. |
| 40 | For `wide_text` columns on release 4.6 and release 5.1 and later, raising the `ingest_guard.memory.leader.ceiling` cluster setting is the third step, taken only after cutting batch size and adding capacity. | 50 | carried | '3. Only then raise the `ingest_guard.memory.leader.ceiling` cluster setting' in `merged.md` -- Step 3 says to raise the setting only after the preceding two steps. |
| 41 | The `ingest_guard.memory.leader.ceiling` cluster setting defaults to 10% of the heap. | 50 | carried | 'which defaults to 10% of the heap' in `merged.md` -- The default is stated in step 3. |
| 42 | A higher `ingest_guard.memory.leader.ceiling` lets a node hold more in-flight append memory before refusing. | 50 | carried | 'A higher ceiling lets a node hold more in-flight append memory before refusing' in `merged.md` -- Stated in step 3. |
| 43 | A node holding too much in-flight append memory runs out of memory instead of refusing. | 50 | carried | 'a node holding too much runs out of memory instead of refusing' in `merged.md` -- Stated in step 3. |
| 44 | The `ingest_guard.memory.leader.ceiling` setting is read at startup. | 50 | carried | 'The setting is read at startup' in `merged.md` -- Stated in step 3. |
| 45 | The cluster must be restarted for a change to the `ingest_guard.memory.leader.ceiling` setting to take. | 50 | carried | 'so the cluster must be restarted for a change to take' in `merged.md` -- Stated in step 3. |
| 46 | Where hardware and setting changes are not available, the load itself must change: fewer appends, cheaper queries, or both. | 52 | carried | 'Where none of that is open to you, the load itself is what changes: fewer appends, cheaper queries, or both.' in `merged.md` -- Stated in the resolution section in equivalent words. |
| 47 | Refusals that show up only during a spike usually clear on their own once the queues drain. | 52 | carried | 'Refusals that show up only during a spike usually clear on their own once the queues drain.' in `merged.md` -- Stated verbatim. |

### `source_b.md` -- 27 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 27 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The note on rising 429 refusals on a managed Nimbrel Ledger deployment was authored by Devin Okonkwo. | 3 | carried | 'Author: Devin Okonkwo' in `merged.md` -- The document lists Devin Okonkwo as an author. |
| 2 | The note on rising 429 refusals on a managed Nimbrel Ledger deployment was updated on 2026-04-11. | 4 | carried | 'Updated: 2026-04-11' in `merged.md` -- The document lists this update date. |
| 3 | The managed Nimbrel Ledger deployment's share of HTTP 429 replies climbed over a fortnight, as counted at the front proxy. | 8 | carried | 'the refusals can show up as a share of HTTP `429` replies that climbs over a fortnight, as counted at the front proxy' in `merged.md` -- The merged text states the fortnight climb counted at the front proxy in generalised form. |
| 4 | The evidence on the rising HTTP 429 replies on the managed Nimbrel Ledger deployment pointed at expensive queries and deep grouping. | 8 | carried | 'On a managed deployment with a rising refusal rate, the evidence points at expensive queries and deep grouping' in `merged.md` -- Stated in the cause section. |
| 5 | The affected product is Nimbrel Ledger. | 12 | carried | '- Product: Nimbrel Ledger' in `merged.md` -- Listed in the environment section. |
| 6 | The affected Nimbrel Ledger versions are 4.4, 5.x. | 13 | carried | '- Version: 4.4, 5.x' in `merged.md` -- Listed in the environment section. |
| 7 | The platform of the affected Nimbrel Ledger deployment is Nimbrel Cloud. | 14 | carried | '- Platform: Nimbrel Cloud' in `merged.md` -- Listed in the environment section. |
| 8 | The affected deployment is Managed Ledger Service (MLS). | 15 | carried | '- Deployment: Managed Ledger Service (MLS)' in `merged.md` -- Listed in the environment section. |
| 9 | The affected Nimbrel Ledger deployment is a production environment. | 16 | carried | '- Production Environment: Yes' in `merged.md` -- Listed in the environment section. |
| 10 | The managed Nimbrel Ledger deployment returns HTTP 429 on a growing share of requests. | 20 | carried | 'The Ledger returns HTTP `429` on a growing share of requests' in `merged.md` -- Stated in the paragraph about the managed deployment. |
| 11 | Nimbrel Ledger returns HTTP 429 when it refuses work rather than queueing it. | 20 | carried | 'The Ledger returns HTTP `429` on a growing share of requests when it refuses work rather than queueing it' in `merged.md` -- The sentence ties the 429 to refusing work rather than queueing it. |
| 12 | Front proxy counters agree with the client reports of HTTP 429 refusals on the managed Nimbrel Ledger deployment. | 20 | carried | 'Front proxy counters agree with the client reports' in `merged.md` -- Stated in the managed deployment paragraph. |
| 13 | The HTTP 429 refusals on the managed Nimbrel Ledger deployment are real and not a client-side accounting error. | 20 | carried | 'so the refusals are real and not a client-side accounting error' in `merged.md` -- Stated in the managed deployment paragraph. |
| 14 | A handful of queries on the managed Nimbrel Ledger deployment run for as long as 2 seconds each. | 24 | carried | 'a handful of queries run for as long as 2 seconds each' in `merged.md` -- Stated under expensive queries. |
| 15 | A worker slot in Nimbrel Ledger is unavailable for as long as an expensive query holds it. | 24 | carried | 'A worker slot is unavailable for as long as one of them holds it' in `merged.md` -- Stated under expensive queries, where 'one of them' is an expensive query. |
| 16 | The queue behind a worker slot held by an expensive query grows. | 24 | carried | 'and the queue behind it grows' in `merged.md` -- Stated under expensive queries. |
| 17 | Grouping on `channel.id` yields a very large number of groups. | 25 | carried | 'grouping on `channel.id` yields a very large number of groups' in `merged.md` -- Stated under deep grouping. |
| 18 | The memory cost of grouping on `channel.id` is charged to the same pool the append path draws on. | 25 | carried | 'the memory that costs is charged to the same pool the append path draws on' in `merged.md` -- Stated under deep grouping. |
| 19 | On the managed Nimbrel Ledger deployment, processor load looks unremarkable while memory sits high. | 26 | carried | 'processor load looks unremarkable while memory sits high' in `merged.md` -- Stated under resource accounting. |
| 20 | The disagreement between processor load and memory on the managed Nimbrel Ledger deployment points at query cost rather than at an undersized cluster. | 26 | carried | 'The two do not agree, which points at query cost rather than at an undersized cluster' in `merged.md` -- Stated under resource accounting. |
| 21 | A proposed action is to set the slow query threshold to 1 second, so that the queries actually responsible are recorded. | 30 | carried | 'set it to 1 second, so that the queries actually responsible are recorded instead of averaged away' in `merged.md` -- Listed as a proposed action on the slow query threshold. |
| 22 | A proposed action is to go through the expensive queries with the team that wrote them. | 31 | carried | 'go through the expensive ones with the team that wrote them' in `merged.md` -- Listed as a proposed action. |
| 23 | Several of the expensive queries look like they could ask for less. | 31 | carried | 'several of which look like they could ask for less' in `merged.md` -- Stated in the query review action. |
| 24 | A proposed action is to take a thread dump and a heap snapshot while the refusal rate is high. | 32 | carried | 'while the refusal rate is high, take a thread dump and a heap snapshot rather than reasoning from counters alone' in `merged.md` -- Listed as a proposed action. |
| 25 | Internal ticket NB-40917 is located at https://tickets.nimbrel.example/issues/40917. | 38 | carried | '[Internal ticket NB-40917](https://tickets.nimbrel.example/issues/40917)' in `merged.md` -- The reference link gives this URL. |
| 26 | The Ledger slow query log documentation is located at https://docs.nimbrel.example/ledger/slow-query-log. | 42 | carried | '[Ledger slow query log](https://docs.nimbrel.example/ledger/slow-query-log)' in `merged.md` -- The reference link gives this URL. |
| 27 | The HTTP 429 replies knowledge article is located at https://support.nimbrel.example/knowledge/318kqp2. | 43 | carried | '[HTTP 429 replies](https://support.nimbrel.example/knowledge/318kqp2)' in `merged.md` -- The reference link gives this URL. |

### `merged.md` -- 76 claim(s): 0 invented, 1 contradicted, 1 supported in part, 74 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 4 | The document "Nimbrel Ledger append rejected with HTTP 429" was updated on 2026-04-11. | contradicted | `source_a.md` | 'Updated: 2026-03-18' in `source_a.md` -- The document with this title was updated 2026-03-18; the date 2026-04-11 belongs to the differently titled source B document. |
| 3 | Devin Okonkwo is an author of the document "Nimbrel Ledger append rejected with HTTP 429". | supported in part | `source_b.md` | 'Author: Devin Okonkwo' in `source_b.md` -- Devin Okonkwo is named as an author, but of the differently titled source B document, not of the document with this title. |
| 1 | Priya Raghunathan is an author of the document "Nimbrel Ledger append rejected with HTTP 429". | supported | `source_a.md` | 'Author: Priya Raghunathan' in `source_a.md` -- Source A carries this title and names Priya Raghunathan as its author. |
| 2 | The document "Nimbrel Ledger append rejected with HTTP 429" was updated on 2026-03-18. | supported | `source_a.md` | 'Updated: 2026-03-18' in `source_a.md` -- Source A, which carries this title, gives this update date. |
| 5 | Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests`. | supported | `source_a.md` | 'Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests`' in `source_a.md` -- Source A states this directly. |
| 6 | When Nimbrel Ledger append requests are refused with HTTP 429, Nimbrel Relay stalls. | supported | `source_a.md` | 'Nimbrel Relay stalls' in `source_a.md` -- Source A lists the Relay stalling as a symptom of the refusal. |
| 7 | When Nimbrel Ledger append requests are refused with HTTP 429, batch loaders resend the same envelope. | supported | `source_a.md` | 'batch loaders resend the same envelope' in `source_a.md` -- Source A lists this as a symptom of the refusal. |
| 8 | When Nimbrel Ledger append requests are refused with HTTP 429, reads against the same shard begin to time out. | supported | `source_a.md` | 'reads against the same shard begin to time out' in `source_a.md` -- Source A lists this as a symptom of the refusal. |
| 9 | The Nimbrel Ledger HTTP 429 append refusal reaches the client. | supported | `source_a.md` | 'The refusal reaches the client' in `source_a.md` -- Source A states this directly. |
| 10 | The Nimbrel Ledger HTTP 429 append refusal is written to the Relay and Collector logs. | supported | `source_a.md` | 'is written to the Relay and Collector logs as well' in `source_a.md` -- Source A states the refusal is written to these logs. |
| 11 | On a managed Nimbrel Ledger deployment (NMD), the refusals can show up as a share of HTTP `429` replies that climbs over a fortnight, as counted at the front proxy. | supported | `source_b.md` | 'whose share of HTTP `429` replies climbed over a fortnight, as counted at the front proxy' in `source_b.md` -- The claim generalises source B's account of the managed deployment's climbing 429 share. |
| 12 | The Nimbrel Ledger returns HTTP `429` on a growing share of requests when it refuses work rather than queueing it. | supported | `source_b.md` | 'The managed deployment returns HTTP `429` on a growing share of requests, which is what the Ledger does when it refuses work rather than queueing it' in `source_b.md` -- Source B states this in near-identical words. |
| 13 | On a managed Nimbrel Ledger deployment, front proxy counters agree with the client reports of HTTP 429 refusals. | supported | `source_b.md` | 'Front proxy counters agree with the client reports' in `source_b.md` -- Source B states this directly. |
| 14 | The HTTP 429 refusals on a managed Nimbrel Ledger deployment are real and not a client-side accounting error. | supported | `source_b.md` | 'so the refusals are real and not a client-side accounting error' in `source_b.md` -- Source B states this directly. |
| 15 | In the example refusal envelope from a Nimbrel Ledger batched append, the append batch was refused after 0 of 64 envelopes. | supported | `source_a.md` | 'append batch refused after 0 of 64 envelopes' in `source_a.md` -- The example envelope in source A begins with this text. |
| 16 | In the example Nimbrel Ledger refusal envelope, the error type is nbl_queue_refused_exception. | supported | `source_a.md` | '"type":"nbl_queue_refused_exception"' in `source_a.md` -- The example envelope gives this error type. |
| 17 | In the example Nimbrel Ledger refusal envelope, the reason is a refused append on ingest path. | supported | `source_a.md` | 'refused append on ingest path' in `source_a.md` -- The example envelope gives this reason. |
| 18 | In the example Nimbrel Ledger refusal envelope, ingest_and_leader_bytes=88121344. | supported | `source_a.md` | 'ingest_and_leader_bytes=88121344' in `source_a.md` -- The value appears in the example envelope. |
| 19 | In the example Nimbrel Ledger refusal envelope, follower_bytes=212992. | supported | `source_a.md` | 'follower_bytes=212992' in `source_a.md` -- The value appears in the example envelope. |
| 20 | In the example Nimbrel Ledger refusal envelope, all_bytes=88334336. | supported | `source_a.md` | 'all_bytes=88334336' in `source_a.md` -- The value appears in the example envelope. |
| 21 | In the example Nimbrel Ledger refusal envelope, ingest_op_bytes=155648. | supported | `source_a.md` | 'ingest_op_bytes=155648' in `source_a.md` -- The value appears in the example envelope. |
| 22 | In the example Nimbrel Ledger refusal envelope, max_ingest_bytes=88080384. | supported | `source_a.md` | 'max_ingest_bytes=88080384' in `source_a.md` -- The value appears in the example envelope. |
| 23 | In the example Nimbrel Ledger refusal envelope, the status is 429. | supported | `source_a.md` | '"status":429' in `source_a.md` -- The example envelope ends with status 429. |
| 24 | The Ledger operations handbook covers refused appends under Refused Appends. | supported | `source_a.md` | 'The Ledger operations handbook now covers the same ground under Refused Appends' in `source_a.md` -- The note in source A states this. |
| 25 | The Ledger operations handbook has a walkthrough for each of the three refusal paths. | supported | `source_a.md` | 'with a walkthrough for each of the three refusal paths set out below' in `source_a.md` -- The note in source A states this. |
| 26 | Every Nimbrel Ledger release on every platform can refuse an append with HTTP 429. | supported | `source_a.md` | 'Every Nimbrel Ledger release on every platform can refuse an append this way.' in `source_a.md` -- Source A's Environment section states this, where 'this way' refers to the HTTP 429 refusal. |
| 27 | The rising refusal rate on a managed deployment is observed with the product Nimbrel Ledger. | supported | `source_b.md` | 'Product: Nimbrel Ledger' in `source_b.md` -- Source B's environment lists this product. |
| 28 | The rising refusal rate on a managed Nimbrel Ledger deployment is observed on Version: 4.4, 5.x. | supported | `source_b.md` | 'Version: 4.4, 5.x' in `source_b.md` -- Source B's environment lists these versions. |
| 29 | The rising refusal rate on a managed Nimbrel Ledger deployment is observed on the platform Nimbrel Cloud. | supported | `source_b.md` | 'Platform: Nimbrel Cloud' in `source_b.md` -- Source B's environment lists this platform. |
| 30 | The rising refusal rate on a managed Nimbrel Ledger deployment is observed on the deployment type Managed Ledger Service (MLS). | supported | `source_b.md` | 'Deployment: Managed Ledger Service (MLS)' in `source_b.md` -- Source B's environment lists this deployment type. |
| 31 | The rising refusal rate on a managed Nimbrel Ledger deployment is observed in a production environment. | supported | `source_b.md` | 'Production Environment: Yes' in `source_b.md` -- Source B's environment marks it as production. |
| 32 | A `429 - Too Many Requests` reply is what a Nimbrel Ledger node sends once it has nowhere left to put the work. | supported | `source_a.md` | 'is what a Ledger node sends once it has nowhere left to put the work' in `source_a.md` -- Source A's Cause section states this. |
| 33 | A Nimbrel Ledger node sends a `429 - Too Many Requests` reply once an append queue or a read queue is full. | supported | `source_a.md` | 'an append queue or a read queue is full' in `source_a.md` -- Source A equates the 429 reply with a full append or read queue. |
| 34 | There are 3 ways a Nimbrel Ledger append draws a 429. | supported | `source_a.md` | 'There are 3 ways an append draws a 429' in `source_a.md` -- Source A states this directly. |
| 35 | A Nimbrel Ledger append draws a 429 when the `append` or `system_append` worker pools hold more batches than they have slots for. | supported | `source_a.md` | 'The `append` or `system_append` worker pools hold more batches than they have slots for' in `source_a.md` -- This is the first of the three listed ways. |
| 36 | The command `nbctl pool status --all` shows the state of the Nimbrel Ledger `append` and `system_append` worker pools. | supported | `source_a.md` | '(`nbctl pool status --all`)' in `source_a.md` -- Source A attaches this command to the worker pool cause as the way to check it. |
| 37 | A Nimbrel Ledger append draws a 429 when the ingest memory guard has refused the batch. | supported | `source_a.md` | 'The ingest memory guard has refused the batch' in `source_a.md` -- This is the second of the three listed ways. |
| 38 | The command `nbctl guard report ingest --counters` reports on the Nimbrel Ledger ingest memory guard. | supported | `source_a.md` | '(`nbctl guard report ingest --counters`)' in `source_a.md` -- Source A attaches this command to the ingest memory guard cause. |
| 39 | A Nimbrel Ledger append draws a 429 when a circuit breaker has tripped. | supported | `source_a.md` | 'A circuit breaker has tripped' in `source_a.md` -- This is the third of the three listed ways. |
| 40 | The command `nbctl breaker list --tripped` lists tripped Nimbrel Ledger circuit breakers. | supported | `source_a.md` | '(`nbctl breaker list --tripped`)' in `source_a.md` -- Source A attaches this command to the tripped circuit breaker cause. |
| 41 | A Nimbrel Ledger circuit breaker trips on any operation and is not particular to appends. | supported | `source_a.md` | 'a breaker trips on any operation and is not particular to appends' in `source_a.md` -- Source A states this directly. |
| 42 | From release 4.6 and release 5.1 onward, appending to a `wide_text` column in Nimbrel Ledger draws a 429 on its own account whenever the batch would otherwise have run the node out of memory. | supported | `source_a.md` | 'appending to a `wide_text` column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory' in `source_a.md` -- Footnote 1 in source A states this for release 4.6 and release 5.1 onward. |
| 43 | On a managed Nimbrel Ledger deployment with a rising refusal rate, the evidence points at expensive queries and deep grouping. | supported | `source_b.md` | 'what the evidence pointed at, which was expensive queries and deep grouping' in `source_b.md` -- Source B's summary states this. |
| 44 | On a managed Nimbrel Ledger deployment with a rising refusal rate, a handful of queries run for as long as 2 seconds each. | supported | `source_b.md` | 'a handful of queries run for as long as 2 seconds each' in `source_b.md` -- Source B states this directly. |
| 45 | A Nimbrel Ledger worker slot is unavailable for as long as an expensive query holds it. | supported | `source_b.md` | 'A worker slot is unavailable for as long as one of them holds it' in `source_b.md` -- Source B states this of the expensive queries. |
| 46 | The queue behind a Nimbrel Ledger worker slot held by an expensive query grows. | supported | `source_b.md` | 'and the queue behind it grows' in `source_b.md` -- Source B states the queue behind the held slot grows. |
| 47 | On a managed Nimbrel Ledger deployment with a rising refusal rate, grouping on `channel.id` yields a very large number of groups. | supported | `source_b.md` | 'grouping on `channel.id` yields a very large number of groups' in `source_b.md` -- Source B states this directly. |
| 48 | The memory cost of grouping on `channel.id` in Nimbrel Ledger is charged to the same pool the append path draws on. | supported | `source_b.md` | 'the memory that costs is charged to the same pool the append path draws on' in `source_b.md` -- Source B states this directly. |
| 49 | On a managed Nimbrel Ledger deployment with a rising refusal rate, processor load looks unremarkable while memory sits high. | supported | `source_b.md` | 'processor load looks unremarkable while memory sits high' in `source_b.md` -- Source B states this directly. |
| 50 | On a managed Nimbrel Ledger deployment with a rising refusal rate, the disagreement between processor load and memory points at query cost rather than at an undersized cluster. | supported | `source_b.md` | 'which points at query cost rather than at an undersized cluster' in `source_b.md` -- Source B draws this conclusion from the disagreement between processor load and memory. |
| 51 | The workaround for Nimbrel Ledger append refusals is to take append and query load off the cluster for long enough that the queues drain and the nodes fall back under their limits. | supported | `source_a.md` | 'Take append and query load off the cluster for long enough that the queues drain and the nodes fall back under their limits.' in `source_a.md` -- Source A's Workaround section states this. |
| 52 | Where batches carry `wide_text` columns and the Nimbrel Ledger cluster runs release 4.6 or release 5.1 or later, the workaround is to send fewer envelopes per batch. | supported | `source_a.md` | 'Where batches carry `wide_text` columns and the cluster runs release 4.6 or release 5.1 or later, send fewer envelopes per batch.' in `source_a.md` -- Source A's Workaround section states this. |
| 53 | A Nimbrel Ledger cluster that refuses appends has been given more work than its hardware can carry. | supported | `source_a.md` | 'A cluster that refuses appends has been given more work than its hardware can carry' in `source_a.md` -- Source A's Resolution section states this. |
| 54 | The resolution for a Nimbrel Ledger cluster that refuses appends is hardware: larger nodes (scale up), or more of them (scale out). | supported | `source_a.md` | 'so the answer is hardware: larger nodes (scale up), or more of them (scale out)' in `source_a.md` -- Source A's Resolution section states this. |
| 55 | Per the Nimbrel Ledger sizing notes, scale up first in most cases. | supported | `source_a.md` | 'Scale up first in most cases' in `source_a.md` -- Source A states this and attributes it to the sizing notes. |
| 56 | Per the Nimbrel Ledger sizing notes, scale out when what is wanted is a further copy of the data for availability. | supported | `source_a.md` | 'scale out when what is wanted is a further copy of the data for availability' in `source_a.md` -- Source A states this and attributes it to the sizing notes. |
| 57 | Splitting a hot stream over more leader shards in Nimbrel Ledger spreads append load across more nodes. | supported | `source_a.md` | 'Splitting a hot stream over more leader shards spreads append load across more nodes' in `source_a.md` -- Source A states this directly. |
| 58 | Splitting a hot stream over more leader shards in Nimbrel Ledger helps in some layouts. | supported | `source_a.md` | 'which helps in some layouts' in `source_a.md` -- Source A states this of splitting a hot stream over more leader shards. |
| 59 | For `wide_text` columns on Nimbrel Ledger release 4.6 and release 5.1 and later, the first step is cutting the number of envelopes in each append batch. | supported | `source_a.md` | 'Begin by cutting the number of envelopes in each append batch.' in `source_a.md` -- This is step 1 of source A's wide_text list. |
| 60 | For `wide_text` columns on Nimbrel Ledger release 4.6 and release 5.1 and later, where smaller batches do not clear the refusals, the second step is to add processor and memory capacity to the nodes. | supported | `source_a.md` | 'Where smaller batches do not clear it, add processor and memory capacity to the nodes.' in `source_a.md` -- This is step 2 of source A's wide_text list. |
| 61 | For `wide_text` columns on Nimbrel Ledger release 4.6 and release 5.1 and later, raising the `ingest_guard.memory.leader.ceiling` cluster setting is the last step, after cutting batch size and adding capacity. | supported | `source_a.md` | 'Only then raise the `ingest_guard.memory.leader.ceiling` cluster setting' in `source_a.md` -- This is step 3 of the list, to be taken only after the first two steps. |
| 62 | The Nimbrel Ledger `ingest_guard.memory.leader.ceiling` cluster setting defaults to 10% of the heap. | supported | `source_a.md` | 'which defaults to 10% of the heap' in `source_a.md` -- Source A gives this default for the setting. |
| 63 | A higher `ingest_guard.memory.leader.ceiling` lets a Nimbrel Ledger node hold more in-flight append memory before refusing. | supported | `source_a.md` | 'A higher ceiling lets a node hold more in-flight append memory before refusing' in `source_a.md` -- Source A states this directly. |
| 64 | A Nimbrel Ledger node holding too much in-flight append memory runs out of memory instead of refusing. | supported | `source_a.md` | 'a node holding too much runs out of memory instead of refusing' in `source_a.md` -- Source A states this directly. |
| 65 | The Nimbrel Ledger `ingest_guard.memory.leader.ceiling` setting is read at startup. | supported | `source_a.md` | 'The setting is read at startup' in `source_a.md` -- Source A states this directly. |
| 66 | The Nimbrel Ledger cluster must be restarted for a change to the `ingest_guard.memory.leader.ceiling` setting to take. | supported | `source_a.md` | 'so the cluster must be restarted for a change to take' in `source_a.md` -- Source A states this directly. |
| 67 | Where scaling and setting changes are not available for a Nimbrel Ledger cluster that refuses appends, the load itself is what changes: fewer appends, cheaper queries, or both. | supported | `source_a.md` | 'Where none of that is open to you, the load itself is what changes: fewer appends, cheaper queries, or both.' in `source_a.md` -- 'None of that' refers to the scaling and setting changes described just before it. |
| 68 | Nimbrel Ledger refusals that show up only during a spike usually clear on their own once the queues drain. | supported | `source_a.md` | 'Refusals that show up only during a spike usually clear on their own once the queues drain.' in `source_a.md` -- Source A states this directly. |
| 69 | For a managed Nimbrel Ledger deployment whose refusals trace to query cost, a proposed action is to lower the slow query threshold to 1 second. | supported | `source_b.md` | '**Lower the slow query threshold**: set it to 1 second' in `source_b.md` -- Source B lists this as a proposed action. |
| 70 | Setting the Nimbrel Ledger slow query threshold to 1 second causes the queries actually responsible to be recorded instead of averaged away. | supported | `source_b.md` | 'so that the queries actually responsible are recorded instead of averaged away' in `source_b.md` -- Source B gives this as the purpose of the 1 second threshold. |
| 71 | For a managed Nimbrel Ledger deployment whose refusals trace to query cost, a proposed action is to go through the expensive queries with the team that wrote them. | supported | `source_b.md` | 'go through the expensive ones with the team that wrote them' in `source_b.md` -- Source B lists this as a proposed action. |
| 72 | Several of the expensive queries on the managed Nimbrel Ledger deployment look like they could ask for less. | supported | `source_b.md` | 'several of which look like they could ask for less' in `source_b.md` -- Source B states this of the expensive queries. |
| 73 | For a managed Nimbrel Ledger deployment whose refusals trace to query cost, a proposed action is to take a thread dump and a heap snapshot while the refusal rate is high. | supported | `source_b.md` | 'while the refusal rate is high, take a thread dump and a heap snapshot' in `source_b.md` -- Source B lists this as a proposed action. |
| 74 | Internal ticket NB-40917 is located at https://tickets.nimbrel.example/issues/40917. | supported | `source_b.md` | '[Internal ticket NB-40917](https://tickets.nimbrel.example/issues/40917)' in `source_b.md` -- Source B's references give this link for the ticket. |
| 75 | The Ledger slow query log documentation is located at https://docs.nimbrel.example/ledger/slow-query-log. | supported | `source_b.md` | '[Ledger slow query log](https://docs.nimbrel.example/ledger/slow-query-log)' in `source_b.md` -- Source B's references give this link. |
| 76 | The HTTP 429 replies knowledge article is located at https://support.nimbrel.example/knowledge/318kqp2. | supported | `source_b.md` | '[HTTP 429 replies](https://support.nimbrel.example/knowledge/318kqp2)' in `source_b.md` -- Source B's references give this link. |

## Structure

**9** mechanical check(s) over **63** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **76** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **74**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 10 run(s) over 54 attributed segment(s) — sources interleaved. 9 of 13 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

No structural finding.

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **7** departure(s) from its sources. Checking them confirms 4, rejects 0, and leaves 3 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 63 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | Title: base title kept. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Nimbrel Ledger append rejected with HTTP 429' and says so (no claim traced to it) |
| `b3` | superseded | Summary heading has no base slot; its content moved to Issue Description. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b4` | reworded | Issue description: generalised from the single-occasion framing. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-003`) |
| `b5` | subsumed | Summary overview folded into lead-ins for Cause and Resolution lists. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-004`) |
| `b13` | reworded | Issue description: tightened to avoid repeating the deployment framing. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-010`, `B-011`) |
| `b15` | superseded | Heading consolidated under the base's Cause heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b21` | superseded | Heading consolidated under the base's Resolution heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | 640c0f94c750 (command) -- lineup fable-sub |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | fable -> claude-fable-5-1 |
| Model (decompose) | fable -> claude-fable-5-1 |
| Model (verify) | fable -> claude-fable-5-1 |
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
| Duration | 315.4s |
| Generated | 2026-09-28T01:14:19+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup fable-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
