## Verdict

**7 finding(s).** In the claims: 3 partially dropped, 2 contradicted. In the structure: 1 false departure, 1 declared loss over budget.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 58 |
| Claims extracted from `source_a.md` | 39 |
| Claims extracted from `source_b.md` | 24 |
| Forward — source claims accounted for in the merge | **58/63** |
| Forward — carried only in part | 3 |
| Forward — `source_a.md` claims accounted for | **39/39** |
| Forward — `source_b.md` claims accounted for | **19/24** (3 in part) |
| Reverse — merge claims found in a source | **58/58** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **121/121** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Partly dropped — the merge carries some of this claim

- **B-012** (`source_b.md:20`) — Front proxy counters agree with the client reports of 429 refusals.
  - evidence: 'Where front proxy counters agree with the client reports, the refusals are real and not a client-side accounting error.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text treats agreement between front proxy counters and client reports only as a condition and never asserts that they actually agree.
- **B-013** (`source_b.md:20`) — The 429 refusals are real and not a client-side accounting error.
  - evidence: 'Where front proxy counters agree with the client reports, the refusals are real and not a client-side accounting error.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text says the refusals are real only when the counters agree, so it does not assert outright that these refusals are real.
- **B-019** (`source_b.md:26`) — Processor load on the deployment looks unremarkable while memory sits high.
  - evidence: 'where processor load looks unremarkable while memory sits high' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The condition appears only as a hypothetical and is not asserted to hold on this deployment.

### Contradicted — the merge states something different

- **B-001** -- the two documents disagree
  - `source_b.md:3` says: The author of the note on rising 429 refusals is Devin Okonkwo.
  - `merged.md` says: 'Author: Priya Raghunathan' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The document names a different author.
- **B-002** -- the two documents disagree
  - `source_b.md:4` says: The note on rising 429 refusals was updated 2026-04-11.
  - `merged.md` says: 'Updated: 2026-03-18' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The document gives a different update date.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 39 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 39 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The document author is Priya Raghunathan. | 3 | carried | 'Author: Priya Raghunathan' in `merged.md` -- The header names Priya Raghunathan as author. |
| 2 | The document was updated 2026-03-18. | 4 | carried | 'Updated: 2026-03-18' in `merged.md` -- The header gives the update date as 2026-03-18. |
| 3 | Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests`. | 8 | carried | 'Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests`.' in `merged.md` -- The text states this verbatim. |
| 4 | When Nimbrel Ledger appends are refused with HTTP 429, Nimbrel Relay stalls. | 8 | carried | 'Nimbrel Relay stalls' in `merged.md` -- The text lists Relay stalling as a symptom of the refused write. |
| 5 | When Nimbrel Ledger appends are refused with HTTP 429, batch loaders resend the same envelope. | 8 | carried | 'batch loaders resend the same envelope' in `merged.md` -- The text lists batch loaders resending the same envelope as a symptom. |
| 6 | When Nimbrel Ledger appends are refused with HTTP 429, reads against the same shard begin to time out. | 8 | carried | 'reads against the same shard begin to time out' in `merged.md` -- The text lists reads on the same shard timing out as a symptom. |
| 7 | The append refusal reaches the client. | 8 | carried | 'The refusal reaches the client' in `merged.md` -- The text states the refusal reaches the client. |
| 8 | The append refusal is written to the Relay and Collector logs. | 8 | carried | 'is written to the Relay and Collector logs as well' in `merged.md` -- The text states the refusal is also written to the Relay and Collector logs. |
| 9 | The Ledger operations handbook covers refused appends under Refused Appends. | 16 | carried | 'The Ledger operations handbook now covers the same ground under Refused Appends' in `merged.md` -- The note says the handbook covers this topic under Refused Appends. |
| 10 | The Ledger operations handbook has a walkthrough for each of the three refusal paths. | 16 | carried | 'with a walkthrough for each of the three refusal paths set out below' in `merged.md` -- The note says the handbook has a walkthrough for each of the three refusal paths. |
| 11 | Every Nimbrel Ledger release on every platform can refuse an append with HTTP 429. | 20 | carried | 'Every Nimbrel Ledger release on every platform can refuse an append this way.' in `merged.md` -- The Environment section states that every release on every platform can refuse an append this way. |
| 12 | A Ledger node sends a 429 - Too Many Requests reply once an append queue or a read queue is full. | 24 | carried | 'is what a Ledger node sends once it has nowhere left to put the work, which is to say once [an append queue or a read queue is full]' in `merged.md` -- The Cause section says a node sends the 429 reply once an append queue or a read queue is full. |
| 13 | There are 3 ways an append draws a 429. | 26 | carried | 'There are 3 ways an append draws a 429:' in `merged.md` -- The text states this directly. |
| 14 | An append draws a 429 when the `append` or `system_append` worker pools hold more batches than they have slots for. | 28 | carried | 'The `append` or `system_append` worker pools hold more batches than they have slots for' in `merged.md` -- This is listed as one of the ways an append draws a 429. |
| 15 | Worker pool status can be checked with `nbctl pool status --all`. | 28 | carried | '(`nbctl pool status --all`)' in `merged.md` -- The command is given alongside the worker pool cause. |
| 16 | An append draws a 429 when the ingest memory guard has refused the batch. | 29 | carried | 'The ingest memory guard has refused the batch' in `merged.md` -- This is listed as one of the ways an append draws a 429. |
| 17 | Ingest memory guard refusals can be checked with `nbctl guard report ingest --counters`. | 29 | carried | '(`nbctl guard report ingest --counters`)' in `merged.md` -- The command is given alongside the ingest memory guard cause. |
| 18 | An append draws a 429 when a circuit breaker has tripped. | 30 | carried | 'A circuit breaker has tripped' in `merged.md` -- This is listed as one of the ways an append draws a 429. |
| 19 | Tripped circuit breakers can be listed with `nbctl breaker list --tripped`. | 30 | carried | '(`nbctl breaker list --tripped`)' in `merged.md` -- The command is given alongside the tripped circuit breaker cause. |
| 20 | A circuit breaker trips on any operation and is not particular to appends. | 30 | carried | 'a breaker trips on any operation and is not particular to appends' in `merged.md` -- The text states this directly. |
| 21 | From release 4.6 and release 5.1 onward, appending to a `wide_text` column draws a 429 whenever the batch would otherwise have run the node out of memory. | 32 | carried | '**From release 4.6 and release 5.1 onward**, appending to a `wide_text` column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory.' in `merged.md` -- The footnote states this. |
| 22 | Taking append and query load off the cluster long enough lets the queues drain and the nodes fall back under their limits. | 36 | carried | 'Take append and query load off the cluster for long enough that the queues drain and the nodes fall back under their limits.' in `merged.md` -- The Workaround section states this. |
| 23 | Where batches carry `wide_text` columns and the cluster runs release 4.6 or release 5.1 or later, the workaround is to send fewer envelopes per batch. | 38 | carried | 'Where batches carry `wide_text` columns and the cluster runs release 4.6 or release 5.1 or later, send fewer envelopes per batch.' in `merged.md` -- The Workaround section states this. |
| 24 | A cluster that refuses appends has been given more work than its hardware can carry. | 42 | carried | 'A cluster that refuses appends has been given more work than its hardware can carry' in `merged.md` -- The Resolution section states this. |
| 25 | The resolution for a cluster that refuses appends is larger nodes (scale up) or more nodes (scale out). | 42 | carried | 'so the answer is hardware: larger nodes (scale up), or more of them (scale out)' in `merged.md` -- The Resolution section gives scaling up or scaling out as the answer. |
| 26 | The sizing notes recommend scaling up first in most cases. | 42 | carried | 'Scale up first in most cases, and scale out when what is wanted is a further copy of the data for availability, per [the sizing notes](https://docs.nimbrel.example/ledger/sizing).' in `merged.md` -- The text attributes the scale-up-first recommendation to the sizing notes. |
| 27 | The sizing notes recommend scaling out when a further copy of the data for availability is wanted. | 42 | carried | 'Scale up first in most cases, and scale out when what is wanted is a further copy of the data for availability, per [the sizing notes](https://docs.nimbrel.example/ledger/sizing).' in `merged.md` -- The text attributes scaling out for a further availability copy to the sizing notes. |
| 28 | Splitting a hot stream over more leader shards spreads append load across more nodes. | 44 | carried | 'Splitting a hot stream over more leader shards spreads append load across more nodes' in `merged.md` -- The text states this directly. |
| 29 | Splitting a hot stream over more leader shards helps in some layouts. | 44 | carried | 'Splitting a hot stream over more leader shards spreads append load across more nodes, which helps in some layouts.' in `merged.md` -- The text says the split helps in some layouts. |
| 30 | For `wide_text` columns on release 4.6 and release 5.1 and later, the first step is cutting the number of envelopes in each append batch. | 48 | carried | 'Begin by cutting the number of envelopes in each append batch.' in `merged.md` -- This is step 1 of the list for wide_text columns on 4.6 and 5.1 and later. |
| 31 | For `wide_text` columns on release 4.6 and release 5.1 and later, where smaller batches do not clear the refusals, add processor and memory capacity to the nodes. | 49 | carried | 'Where smaller batches do not clear it, add processor and memory capacity to the nodes.' in `merged.md` -- This is step 2 of the wide_text list. |
| 32 | Raising the `ingest_guard.memory.leader.ceiling` cluster setting should only be done after reducing batch size and adding processor and memory capacity. | 50 | carried | 'Only then raise the `ingest_guard.memory.leader.ceiling` cluster setting' in `merged.md` -- Step 3 comes only after steps 1 and 2, which are reducing batch size and adding capacity. |
| 33 | The `ingest_guard.memory.leader.ceiling` cluster setting defaults to 10% of the heap. | 50 | carried | 'which defaults to 10% of the heap' in `merged.md` -- The default is stated as 10% of the heap. |
| 34 | A higher `ingest_guard.memory.leader.ceiling` lets a node hold more in-flight append memory before refusing. | 50 | carried | 'A higher ceiling lets a node hold more in-flight append memory before refusing' in `merged.md` -- The text states this directly. |
| 35 | A node holding too much in-flight append memory runs out of memory instead of refusing. | 50 | carried | 'a node holding too much runs out of memory instead of refusing' in `merged.md` -- The text states this directly. |
| 36 | The `ingest_guard.memory.leader.ceiling` setting is read at startup. | 50 | carried | 'The setting is read at startup' in `merged.md` -- The text states this directly. |
| 37 | The cluster must be restarted for a change to `ingest_guard.memory.leader.ceiling` to take effect. | 50 | carried | 'so the cluster must be restarted for a change to take' in `merged.md` -- The text states that a restart is required for a change to take effect. |
| 38 | Where hardware and setting changes are not possible, the remedy is fewer appends, cheaper queries, or both. | 52 | carried | 'Where none of that is open to you, the load itself is what changes: fewer appends, cheaper queries, or both.' in `merged.md` -- The text states this with the same meaning. |
| 39 | Refusals that show up only during a spike usually clear on their own once the queues drain. | 52 | carried | 'Refusals that show up only during a spike usually clear on their own once the queues drain.' in `merged.md` -- This is stated verbatim. |

### `source_b.md` -- 24 claim(s): 0 dropped, 2 contradicted, 3 carried in part, 19 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The author of the note on rising 429 refusals is Devin Okonkwo. | 3 | contradicted | 'Author: Priya Raghunathan' in `merged.md` -- The document names a different author. |
| 2 | The note on rising 429 refusals was updated 2026-04-11. | 4 | contradicted | 'Updated: 2026-03-18' in `merged.md` -- The document gives a different update date. |
| 12 | Front proxy counters agree with the client reports of 429 refusals. | 20 | carried in part | 'Where front proxy counters agree with the client reports, the refusals are real and not a client-side accounting error.' in `merged.md` -- The text treats agreement between front proxy counters and client reports only as a condition and never asserts that they actually agree. |
| 13 | The 429 refusals are real and not a client-side accounting error. | 20 | carried in part | 'Where front proxy counters agree with the client reports, the refusals are real and not a client-side accounting error.' in `merged.md` -- The text says the refusals are real only when the counters agree, so it does not assert outright that these refusals are real. |
| 19 | Processor load on the deployment looks unremarkable while memory sits high. | 26 | carried in part | 'where processor load looks unremarkable while memory sits high' in `merged.md` -- The condition appears only as a hypothetical and is not asserted to hold on this deployment. |
| 3 | The managed Nimbrel Ledger deployment's share of HTTP 429 replies climbed over a fortnight, as counted at the front proxy. | 8 | carried | 'the problem can show as a share of HTTP `429` replies, counted at the front proxy, that climbs over a fortnight' in `merged.md` -- This generalised statement carries the claim about the managed deployment. |
| 4 | The evidence pointed at expensive queries and deep grouping as causes of the rising 429 refusals. | 8 | carried | 'Expensive queries and deep grouping can also push the refusal rate up' in `merged.md` -- The text names expensive queries and deep grouping as contributors to rising refusals. |
| 5 | The affected product is Nimbrel Ledger. | 12 | carried | 'This includes production deployments of Nimbrel Ledger 4.4 and 5.x on the Managed Ledger Service (MLS) on Nimbrel Cloud.' in `merged.md` -- The product named is Nimbrel Ledger. |
| 6 | The affected Nimbrel Ledger versions are 4.4 and 5.x. | 13 | carried | 'This includes production deployments of Nimbrel Ledger 4.4 and 5.x on the Managed Ledger Service (MLS) on Nimbrel Cloud.' in `merged.md` -- Versions 4.4 and 5.x are stated. |
| 7 | The affected platform is Nimbrel Cloud. | 14 | carried | 'This includes production deployments of Nimbrel Ledger 4.4 and 5.x on the Managed Ledger Service (MLS) on Nimbrel Cloud.' in `merged.md` -- The platform is Nimbrel Cloud. |
| 8 | The deployment type is Managed Ledger Service (MLS). | 15 | carried | 'This includes production deployments of Nimbrel Ledger 4.4 and 5.x on the Managed Ledger Service (MLS) on Nimbrel Cloud.' in `merged.md` -- The deployment type is the Managed Ledger Service (MLS). |
| 9 | The affected deployment is a production environment. | 16 | carried | 'This includes production deployments of Nimbrel Ledger 4.4 and 5.x on the Managed Ledger Service (MLS) on Nimbrel Cloud.' in `merged.md` -- Production deployments are stated. |
| 10 | The managed deployment returns HTTP 429 on a growing share of requests. | 20 | carried | 'the problem can show as a share of HTTP `429` replies, counted at the front proxy, that climbs over a fortnight' in `merged.md` -- A climbing share of 429 replies matches a growing share of requests refused. |
| 11 | The Ledger returns HTTP 429 when it refuses work rather than queueing it. | 20 | carried | 'A `429` is what the Ledger returns when it refuses work rather than queueing it.' in `merged.md` -- This is stated directly. |
| 14 | A handful of queries run for as long as 2 seconds each. | 24 | carried | 'a handful of queries run for as long as 2 seconds each' in `merged.md` -- The text states this directly. |
| 15 | A worker slot is unavailable for as long as an expensive query holds it. | 24 | carried | 'A worker slot is unavailable for as long as one of them holds it' in `merged.md` -- Here 'one of them' refers to the expensive queries, which matches the claim. |
| 16 | The queue behind a worker slot held by an expensive query grows. | 24 | carried | 'and the queue behind it grows' in `merged.md` -- The text states that the queue behind the held worker slot grows. |
| 17 | Grouping on channel.id yields a very large number of groups. | 25 | carried | 'grouping on `channel.id` yields a very large number of groups' in `merged.md` -- The text states this directly. |
| 18 | The memory cost of grouping on channel.id is charged to the same pool the append path draws on. | 25 | carried | 'the memory that costs is charged to the same pool the append path draws on' in `merged.md` -- The text states that the memory cost of this grouping is charged to the append path's pool. |
| 20 | The disagreement between processor load and memory points at query cost rather than at an undersized cluster. | 26 | carried | 'the two do not agree, which points at query cost rather than at an undersized cluster' in `merged.md` -- The text states that the disagreement points at query cost rather than an undersized cluster. |
| 21 | The proposed action is to set the slow query threshold to 1 second. | 30 | carried | 'set it to 1 second' in `merged.md` -- The text recommends lowering the slow query threshold to 1 second. |
| 22 | The proposed action is to go through the expensive queries with the team that wrote them. | 31 | carried | 'go through the expensive ones with the team that wrote them' in `merged.md` -- The text recommends reviewing the expensive queries with the team that wrote them. |
| 23 | The proposed action is to take a thread dump and a heap snapshot while the refusal rate is high. | 32 | carried | 'while the refusal rate is high, take a thread dump and a heap snapshot' in `merged.md` -- The text recommends capturing a thread dump and a heap snapshot during high refusal rates. |
| 24 | The internal ticket for the issue is NB-40917. | 38 | carried | '[Internal ticket NB-40917]' in `merged.md` -- The references list internal ticket NB-40917. |

### `merged.md` -- 58 claim(s): 0 invented, 0 contradicted, 0 supported in part, 58 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | The document author is Priya Raghunathan. | supported | `source_a.md` | 'Author: Priya Raghunathan' in `source_a.md` -- Source A names Priya Raghunathan as its author. |
| 2 | The document was updated 2026-03-18. | supported | `source_a.md` | 'Updated: 2026-03-18' in `source_a.md` -- Source A gives this update date. |
| 3 | Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests`. | supported | `source_a.md` | 'Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests`.' in `source_a.md` -- Source A states this verbatim. |
| 4 | When Nimbrel Ledger appends are refused, Nimbrel Relay stalls. | supported | `source_a.md` | 'Nimbrel Relay stalls' in `source_a.md` -- Source A lists Relay stalling as a symptom of refused appends. |
| 5 | When Nimbrel Ledger appends are refused, batch loaders resend the same envelope. | supported | `source_a.md` | 'batch loaders resend the same envelope' in `source_a.md` -- Source A lists batch loaders resending the same envelope as a symptom. |
| 6 | When Nimbrel Ledger appends are refused, reads against the same shard begin to time out. | supported | `source_a.md` | 'reads against the same shard begin to time out' in `source_a.md` -- Source A lists read timeouts on the same shard as a symptom. |
| 7 | The append refusal reaches the client. | supported | `source_a.md` | 'The refusal reaches the client' in `source_a.md` -- Source A states that the refusal reaches the client. |
| 8 | The append refusal is written to the Relay and Collector logs. | supported | `source_a.md` | 'is written to the Relay and Collector logs as well' in `source_a.md` -- Source A states that the refusal is also written to the Relay and Collector logs. |
| 9 | On a managed Nimbrel Ledger deployment (NMD), the problem can show as a share of HTTP 429 replies, counted at the front proxy, that climbs over a fortnight. | supported | `source_b.md` | 'managed Nimbrel Ledger deployment (NMD) whose share of HTTP `429` replies climbed over a fortnight, as counted at the front proxy' in `source_b.md` -- Source B describes this occurrence, and the claim generalises it, which is allowed at high fidelity. |
| 10 | The Ledger returns a 429 when it refuses work rather than queueing it. | supported | `source_b.md` | 'which is what the Ledger does when it refuses work rather than queueing it' in `source_b.md` -- Source B states that a 429 is what the Ledger returns when it refuses work rather than queueing it. |
| 11 | Where front proxy counters agree with the client reports, the refusals are real and not a client-side accounting error. | supported | `source_b.md` | 'Front proxy counters agree with the client reports, so the refusals are real and not a client-side accounting error.' in `source_b.md` -- The claim generalises Source B's statement about this particular deployment. |
| 12 | The example batched append was refused after 0 of 64 envelopes. | supported | `source_a.md` | 'append batch refused after 0 of 64 envelopes' in `source_a.md` -- Source A's example envelope shows the batch refused after 0 of 64 envelopes. |
| 13 | The example refusal envelope has error type nbl_queue_refused_exception. | supported | `source_a.md` | '"type":"nbl_queue_refused_exception"' in `source_a.md` -- Source A's example envelope carries this error type. |
| 14 | The example refusal reports ingest_and_leader_bytes=88121344 and max_ingest_bytes=88080384. | supported | `source_a.md` | 'ingest_and_leader_bytes=88121344' in `source_a.md` -- Source A's example envelope reports both values, including max_ingest_bytes=88080384. |
| 15 | The example refusal reports follower_bytes=212992, all_bytes=88334336 and ingest_op_bytes=155648. | supported | `source_a.md` | 'follower_bytes=212992, all_bytes=88334336, ingest_op_bytes=155648' in `source_a.md` -- Source A's example envelope reports these three values. |
| 16 | The Ledger operations handbook covers refused appends under Refused Appends. | supported | `source_a.md` | 'The Ledger operations handbook now covers the same ground under Refused Appends' in `source_a.md` -- Source A's note states that the handbook covers this topic under Refused Appends. |
| 17 | The Ledger operations handbook has a walkthrough for each of the three refusal paths. | supported | `source_a.md` | 'with a walkthrough for each of the three refusal paths set out below' in `source_a.md` -- Source A's note states that the handbook has a walkthrough for each of the three paths. |
| 18 | Every Nimbrel Ledger release on every platform can refuse an append with HTTP 429. | supported | `source_a.md` | 'Every Nimbrel Ledger release on every platform can refuse an append this way.' in `source_a.md` -- Source A states this in its Environment section. |
| 19 | Production deployments of Nimbrel Ledger 4.4 and 5.x on the Managed Ledger Service (MLS) on Nimbrel Cloud can refuse appends with HTTP 429. | supported | `source_a.md` | 'Every Nimbrel Ledger release on every platform can refuse an append this way.' in `source_a.md` -- Source A's universal statement, combined with Source B's environment list (4.4 and 5.x, Nimbrel Cloud, MLS, production), jointly entails the claim. |
| 20 | A Ledger node sends a 429 Too Many Requests reply once an append queue or a read queue is full. | supported | `source_a.md` | 'is what a Ledger node sends once it has nowhere left to put the work, which is to say once [an append queue or a read queue is full]' in `source_a.md` -- Source A states that a node sends a 429 once an append or read queue is full. |
| 21 | There are 3 ways an append draws a 429. | supported | `source_a.md` | 'There are 3 ways an append draws a 429:' in `source_a.md` -- Source A states this directly. |
| 22 | An append draws a 429 when the append or system_append worker pools hold more batches than they have slots for. | supported | `source_a.md` | 'The `append` or `system_append` worker pools hold more batches than they have slots for' in `source_a.md` -- Source A lists this as one of the three ways an append draws a 429. |
| 23 | Worker pool status can be checked with `nbctl pool status --all`. | supported | `source_a.md` | '`nbctl pool status --all`' in `source_a.md` -- Source A gives this command against the worker pool cause. |
| 24 | An append draws a 429 when the ingest memory guard has refused the batch. | supported | `source_a.md` | 'The ingest memory guard has refused the batch' in `source_a.md` -- Source A lists this as one of the three ways an append draws a 429. |
| 25 | Ingest memory guard refusals can be checked with `nbctl guard report ingest --counters`. | supported | `source_a.md` | '`nbctl guard report ingest --counters`' in `source_a.md` -- Source A gives this command against the ingest memory guard cause. |
| 26 | An append draws a 429 when a circuit breaker has tripped. | supported | `source_a.md` | 'A circuit breaker has tripped (`nbctl breaker list --tripped`)' in `source_a.md` -- Source A lists a tripped circuit breaker as one of the three ways an append draws a 429. |
| 27 | Tripped circuit breakers can be listed with `nbctl breaker list --tripped`. | supported | `source_a.md` | 'A circuit breaker has tripped (`nbctl breaker list --tripped`)' in `source_a.md` -- Source A gives `nbctl breaker list --tripped` as the command for this case. |
| 28 | A circuit breaker trips on any operation and is not particular to appends. | supported | `source_a.md` | 'a breaker trips on any operation and is not particular to appends' in `source_a.md` -- Source A states this directly. |
| 29 | From release 4.6 and release 5.1 onward, appending to a wide_text column draws a 429 whenever the batch would otherwise have run the node out of memory. | supported | `source_a.md` | '**From release 4.6 and release 5.1 onward**, appending to a `wide_text` column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory.' in `source_a.md` -- Source A's footnote states this directly. |
| 30 | Expensive queries and deep grouping can push the refusal rate up. | supported | `source_b.md` | 'It sets out what the evidence pointed at, which was expensive queries and deep grouping' in `source_b.md` -- Source B attributes the rising 429 share to expensive queries and deep grouping, which the claim generalises. |
| 31 | A handful of queries run for as long as 2 seconds each. | supported | `source_b.md` | 'a handful of queries run for as long as 2 seconds each' in `source_b.md` -- Source B states this directly. |
| 32 | A worker slot is unavailable for as long as an expensive query holds it. | supported | `source_b.md` | 'A worker slot is unavailable for as long as one of them holds it' in `source_b.md` -- Source B states this about the expensive queries. |
| 33 | The queue behind a worker slot held by an expensive query grows. | supported | `source_b.md` | 'and the queue behind it grows' in `source_b.md` -- Source B states that the queue behind the held slot grows. |
| 34 | Grouping on channel.id yields a very large number of groups. | supported | `source_b.md` | 'grouping on `channel.id` yields a very large number of groups' in `source_b.md` -- Source B states this directly. |
| 35 | The memory cost of grouping on channel.id is charged to the same pool the append path draws on. | supported | `source_b.md` | 'the memory that costs is charged to the same pool the append path draws on' in `source_b.md` -- Source B states this directly. |
| 36 | Unremarkable processor load with high memory points at query cost rather than at an undersized cluster. | supported | `source_b.md` | 'The two do not agree, which points at query cost rather than at an undersized cluster.' in `source_b.md` -- Source B states that the processor and memory mismatch points at query cost. |
| 37 | A workaround is to take append and query load off the cluster until the queues drain and the nodes fall back under their limits. | supported | `source_a.md` | 'Take append and query load off the cluster for long enough that the queues drain and the nodes fall back under their limits.' in `source_a.md` -- Source A gives this as the workaround. |
| 38 | Where batches carry wide_text columns and the cluster runs release 4.6 or release 5.1 or later, a workaround is to send fewer envelopes per batch. | supported | `source_a.md` | 'Where batches carry `wide_text` columns and the cluster runs release 4.6 or release 5.1 or later, send fewer envelopes per batch.' in `source_a.md` -- Source A states this workaround directly. |
| 39 | A cluster that refuses appends has been given more work than its hardware can carry. | supported | `source_a.md` | 'A cluster that refuses appends has been given more work than its hardware can carry' in `source_a.md` -- Source A states this directly. |
| 40 | The resolution for a cluster refusing appends is larger nodes (scale up) or more nodes (scale out). | supported | `source_a.md` | 'so the answer is hardware: larger nodes (scale up), or more of them (scale out)' in `source_a.md` -- Source A gives scaling up or scaling out as the resolution. |
| 41 | Per the sizing notes, scaling up should be done first in most cases. | supported | `source_a.md` | 'Scale up first in most cases, and scale out when what is wanted is a further copy of the data for availability, per [the sizing notes]' in `source_a.md` -- Source A attributes scale-up-first to the sizing notes. |
| 42 | Per the sizing notes, scaling out should be done when a further copy of the data for availability is wanted. | supported | `source_a.md` | 'Scale up first in most cases, and scale out when what is wanted is a further copy of the data for availability, per [the sizing notes]' in `source_a.md` -- Source A attributes scale-out-for-availability to the sizing notes. |
| 43 | Splitting a hot stream over more leader shards spreads append load across more nodes. | supported | `source_a.md` | 'Splitting a hot stream over more leader shards spreads append load across more nodes' in `source_a.md` -- Source A states this directly. |
| 44 | Splitting a hot stream over more leader shards helps in some layouts. | supported | `source_a.md` | 'which helps in some layouts' in `source_a.md` -- Source A states that splitting helps in some layouts. |
| 45 | For wide_text columns on release 4.6 and release 5.1 and later, the first step is to cut the number of envelopes in each append batch. | supported | `source_a.md` | 'Begin by cutting the number of envelopes in each append batch.' in `source_a.md` -- Source A gives this as step 1 for wide_text columns on those releases. |
| 46 | For wide_text columns, where smaller batches do not clear the refusals, processor and memory capacity should be added to the nodes. | supported | `source_a.md` | 'Where smaller batches do not clear it, add processor and memory capacity to the nodes.' in `source_a.md` -- Source A gives this as step 2. |
| 47 | For wide_text columns, the ingest_guard.memory.leader.ceiling cluster setting should be raised only after reducing batch size and adding capacity. | supported | `source_a.md` | 'Only then raise the `ingest_guard.memory.leader.ceiling` cluster setting' in `source_a.md` -- Source A orders raising the ceiling after steps 1 and 2. |
| 48 | The ingest_guard.memory.leader.ceiling cluster setting defaults to 10% of the heap. | supported | `source_a.md` | 'which defaults to 10% of the heap' in `source_a.md` -- Source A states the default directly. |
| 49 | A higher ingest_guard.memory.leader.ceiling lets a node hold more in-flight append memory before refusing. | supported | `source_a.md` | 'A higher ceiling lets a node hold more in-flight append memory before refusing' in `source_a.md` -- Source A states this directly. |
| 50 | A node holding too much in-flight append memory runs out of memory instead of refusing. | supported | `source_a.md` | 'a node holding too much runs out of memory instead of refusing' in `source_a.md` -- Source A states this directly. |
| 51 | The ingest_guard.memory.leader.ceiling setting is read at startup. | supported | `source_a.md` | 'The setting is read at startup' in `source_a.md` -- Source A states directly that the ceiling setting is read at startup. |
| 52 | The cluster must be restarted for a change to ingest_guard.memory.leader.ceiling to take effect. | supported | `source_a.md` | 'so the cluster must be restarted for a change to take' in `source_a.md` -- Source A states that the cluster must be restarted for a change to the setting to take effect. |
| 53 | Where hardware and setting changes are not possible, the load must change through fewer appends, cheaper queries, or both. | supported | `source_a.md` | 'Where none of that is open to you, the load itself is what changes: fewer appends, cheaper queries, or both.' in `source_a.md` -- Source A says that when the hardware and setting options are unavailable, the load changes through fewer appends, cheaper queries, or both. |
| 54 | Where query cost is suspected, the slow query threshold should be set to 1 second. | supported | `source_b.md` | '**Lower the slow query threshold**: set it to 1 second' in `source_b.md` -- Source B proposes a 1-second slow query threshold in a case attributed to query cost, and the claim generalises that particular recommendation. |
| 55 | Where query cost is suspected, the expensive queries should be reviewed with the team that wrote them. | supported | `source_b.md` | 'go through the expensive ones with the team that wrote them' in `source_b.md` -- Source B proposes reviewing the expensive queries with the team that wrote them, which the claim generalises to cases where query cost is suspected. |
| 56 | While the refusal rate is high, a thread dump and a heap snapshot should be taken. | supported | `source_b.md` | 'while the refusal rate is high, take a thread dump and a heap snapshot' in `source_b.md` -- Source B states that a thread dump and a heap snapshot should be taken while the refusal rate is high. |
| 57 | Refusals that show up only during a spike usually clear on their own once the queues drain. | supported | `source_a.md` | 'Refusals that show up only during a spike usually clear on their own once the queues drain.' in `source_a.md` -- Source A states this almost verbatim. |
| 58 | The issue is tracked in internal ticket NB-40917. | supported | `source_b.md` | '[Internal ticket NB-40917](https://tickets.nimbrel.example/issues/40917)' in `source_b.md` -- Source B lists internal ticket NB-40917 as the reference for this issue. |

## Structure

**9** mechanical check(s) over **63** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **58** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **63**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 8 run(s) over 44 attributed segment(s) — sources interleaved. 9 of 13 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Declared gone, still here — a record says the content departed and the merge carries the segment unchanged

- `b20` (`source_b.md`) — 'The two do not agree, which points at query cost rather than at an undersized cluster.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: The two do not agree, which points at query cost rather than at an undersized cluster.
  In the merge:  - **Resource accounting**: where processor load looks unremarkable while memory sits high, the two do not agree, which points at query cost rather than at an undersized cluster.
  ```

### Over budget — declared loss past the ceiling

- 5 absent segments are declared replaced by the same replacement (b10, b11, b7, b8, b9), over the ceiling of 3. One replacement standing in for that many segments has not replaced them, it has dropped them: the detail it names is gone from the document

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **18** departure(s) from its sources. Checking them confirms 13, rejects 2, and leaves 3 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 63 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | Base title kept. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Nimbrel Ledger append rejected with HTTP 429' and says so (no claim traced to it) |
| `b2` | superseded | Metadata block: base block kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-001`, `B-002`) |
| `b3` | superseded | Summary content folded into the base Issue Description section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b4` | reworded | Issue description: generalised from one deployment. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-003`) |
| `b5` | subsumed | Cause: evidence summary becomes lead-in to factors list. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-004`) |
| `b6` | duplicate | Same heading as base. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b7` | subsumed | Environment list folded into one sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-005`) |
| `b8` | subsumed | Environment list folded into one sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-006`) |
| `b9` | subsumed | Environment list folded into one sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-007`) |
| `b10` | subsumed | Environment list folded into one sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-008`) |
| `b11` | subsumed | Environment list folded into one sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-009`) |
| `b12` | duplicate | Same heading as base. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b13` | reworded | Issue description: generalised wording. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-010`, `B-011`) |
| `b14` | reworded | Issue description: stated generally as a check. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-012 came back PARTIAL, B-013 came back PARTIAL (`B-012`, `B-013`) |
| `b15` | superseded | Contributing factors consolidated under base Cause heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b19` | reworded | Cause: merged with b20 and stated generally. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-019 came back PARTIAL (`B-019`) |
| `b20` | subsumed | Cause: joined into the resource accounting bullet. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-020`) |
| `b21` | superseded | Proposed actions consolidated under base Resolution heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | ec0c9ecb43e3 (hosted) |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | claude-opus-5-5 |
| Model (decompose) | claude-opus-5-5 |
| Model (verify) | claude-opus-5-5 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile anthropic |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 10 live, 0 cached, 0 replayed |
| Tokens | 48,753 in, 31,885 out |
| Cost | ~$0.83 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 242.7s |
| Generated | 2026-09-27T15:56:33+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
