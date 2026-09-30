## Verdict

**3 finding(s).** In the claims: 2 partially dropped. In the structure: 1 undeclared rewording.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 72 |
| Claims extracted from `source_a.md` | 39 |
| Claims extracted from `source_b.md` | 20 |
| Forward — source claims accounted for in the merge | **57/59** |
| Forward — carried only in part | 2 |
| Forward — `source_a.md` claims accounted for | **39/39** |
| Forward — `source_b.md` claims accounted for | **18/20** (2 in part) |
| Reverse — merge claims found in a source | **72/72** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **128/131** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Partly dropped — the merge carries some of this claim

- **B-013** (`source_b.md:24`) — A handful of queries run for as long as 2 seconds each.
  - evidence: 'Some queries run for as long as 2 seconds each' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The reference gives the duration but says only “Some queries,” not that a handful do.
- **B-018** (`source_b.md:26`) — Processor load looks unremarkable.
  - evidence: 'Processor load can look unremarkable' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The reference says processor load can look unremarkable, but does not assert unconditionally that it does.

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
| 1 | Nimbrel Ledger append requests can return HTTP 429 `Too Many Requests`. | 8 | carried | 'Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests`.' in `merged.md` -- The text explicitly says append requests can come back with HTTP 429 `Too Many Requests`. |
| 2 | A write refused by Nimbrel Ledger will not land. | 8 | carried | 'Callers see a write that will not land' in `merged.md` -- The text describes the refused write as one that will not land. |
| 3 | Nimbrel Relay stalls when callers see a write that will not land. | 8 | carried | 'Nimbrel Relay stalls' in `merged.md` -- The text states that Nimbrel Relay stalls in this situation. |
| 4 | Batch loaders resend the same envelope when callers see a write that will not land. | 8 | carried | 'batch loaders resend the same envelope' in `merged.md` -- The text states that batch loaders resend the same envelope. |
| 5 | Reads against the same shard begin to time out when callers see a write that will not land. | 8 | carried | 'reads against the same shard begin to time out' in `merged.md` -- The text states that reads against the same shard begin to time out. |
| 6 | A refusal reaches the client. | 8 | carried | 'The refusal reaches the client' in `merged.md` -- The text explicitly says the refusal reaches the client. |
| 7 | A refusal is written to the Relay logs. | 8 | carried | 'is written to the Relay' in `merged.md` -- The text says the refusal is written to the Relay logs. |
| 8 | A refusal is written to the Collector logs. | 8 | carried | 'is written to the ... Collector logs' in `merged.md`, **transcription_error** -- The text says the refusal is written to the Collector logs. |
| 9 | The sample append batch was refused after 0 of 64 envelopes. | 13 | carried | 'append batch refused after 0 of 64 envelopes' in `merged.md` -- The sample refusal states that zero of 64 envelopes were accepted. |
| 10 | The sample append refusal response was 429 Too Many Requests. | 13 | carried | '429 Too Many Requests' in `merged.md` -- The sample refusal response gives HTTP 429 Too Many Requests. |
| 11 | The sample refusal error type is `nbl_queue_refused_exception`. | 13 | carried | '"type":"nbl_queue_refused_exception"' in `merged.md` -- The sample error identifies its type as `nbl_queue_refused_exception`. |
| 12 | The sample refusal reason is refused append on ingest path. | 13 | carried | 'refused append on ingest path' in `merged.md` -- The sample refusal reason is “refused append on ingest path.” |
| 13 | The sample refusal reports ingest_and_leader_bytes=88121344. | 13 | carried | 'ingest_and_leader_bytes=88121344' in `merged.md` -- The sample refusal reports the stated ingest_and_leader_bytes value. |
| 14 | The sample refusal reports follower_bytes=212992. | 13 | carried | 'follower_bytes=212992' in `merged.md` -- The sample refusal reports the stated follower_bytes value. |
| 15 | The sample refusal reports all_bytes=88334336. | 13 | carried | 'all_bytes=88334336' in `merged.md` -- The sample refusal reports the stated all_bytes value. |
| 16 | The sample refusal reports ingest_op_bytes=155648. | 13 | carried | 'ingest_op_bytes=155648' in `merged.md` -- The sample refusal reports the stated ingest_op_bytes value. |
| 17 | The sample refusal reports max_ingest_bytes=88080384. | 13 | carried | 'max_ingest_bytes=88080384' in `merged.md` -- The sample refusal reports the stated max_ingest_bytes value. |
| 18 | Every Nimbrel Ledger release on every platform can refuse an append this way. | 20 | carried | 'Every Nimbrel Ledger release on every platform can refuse an append this way.' in `merged.md` -- The text states this applies to every release on every platform. |
| 19 | A Ledger node sends a `429 - Too Many Requests` reply once it has nowhere left to put the work. | 24 | carried | 'A [`429 - Too Many Requests` reply](https://docs.nimbrel.example/ledger/http-status-codes) is what a Ledger node sends once it has nowhere left to put the work' in `merged.md` -- The text directly links the 429 reply to the node having nowhere left to put the work. |
| 20 | A Ledger node has nowhere left to put the work once an append queue or a read queue is full. | 24 | carried | 'which is to say once [an append queue or a read queue is full](https://docs.nimbrel.example/ledger/why-appends-are-refused).' in `merged.md` -- The text explains that having nowhere left to put work means an append queue or read queue is full. |
| 21 | There are 3 ways an append draws a 429. | 26 | carried | 'There are 3 ways an append draws a 429:' in `merged.md` -- The text explicitly says there are three ways an append draws a 429. |
| 22 | The `append` or `system_append` worker pools can hold more batches than they have slots for. | 28 | carried | 'The `append` or `system_append` worker pools hold more batches than they have slots for' in `merged.md` -- The text lists worker pools exceeding their available slots as a cause. |
| 23 | The ingest memory guard can refuse a batch. | 29 | carried | 'The ingest memory guard has refused the batch' in `merged.md` -- The text lists the ingest memory guard refusing the batch as a cause. |
| 24 | A circuit breaker can trip. | 30 | carried | 'A circuit breaker has tripped' in `merged.md` -- The text lists a tripped circuit breaker as a way an append draws a 429. |
| 25 | A breaker trips on any operation. | 30 | carried | 'a breaker trips on any operation and is not particular to appends.' in `merged.md` -- The text explicitly states that a breaker trips on any operation. |
| 26 | A breaker is not particular to appends. | 30 | carried | 'a breaker trips on any operation and is not particular to appends.' in `merged.md` -- The reference explicitly says a breaker is not particular to appends. |
| 27 | From release 4.6 and release 5.1 onward, appending to a `wide_text` column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory. | 32 | carried | 'From release 4.6 and release 5.1 onward, appending to a `wide_text` column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory.' in `merged.md`, **transcription_error** -- The reference states this condition and its release range verbatim. |
| 28 | A cluster that refuses appends has been given more work than its hardware can carry. | 42 | carried | 'A cluster that refuses appends has been given more work than its hardware can carry' in `merged.md` -- The reference directly states this about a cluster that refuses appends. |
| 29 | Scaling up means using larger nodes. | 42 | carried | 'larger nodes (scale up)' in `merged.md` -- The reference equates scale up with using larger nodes. |
| 30 | Scaling out means using more nodes. | 42 | carried | 'more of them (scale out)' in `merged.md` -- The reference equates scale out with having more nodes. |
| 31 | Scale out can provide a further copy of the data for availability. | 42 | carried | 'scale out when what is wanted is a further copy of the data for availability' in `merged.md` -- The reference states that scale out is used when a further data copy is wanted for availability. |
| 32 | Splitting a hot stream over more leader shards spreads append load across more nodes. | 44 | carried | 'Splitting a hot stream over more leader shards spreads append load across more nodes' in `merged.md` -- The reference directly states that splitting a hot stream over more leader shards spreads append load across more nodes. |
| 33 | Splitting a hot stream over more leader shards helps in some layouts. | 44 | carried | 'which helps in some layouts.' in `merged.md` -- The reference says this arrangement helps in some layouts. |
| 34 | The `ingest_guard.memory.leader.ceiling` cluster setting defaults to 10% of the heap. | 50 | carried | 'the `ingest_guard.memory.leader.ceiling` cluster setting, which defaults to 10% of the heap.' in `merged.md` -- The reference gives the setting's default as 10% of the heap. |
| 35 | A higher `ingest_guard.memory.leader.ceiling` lets a node hold more in-flight append memory before refusing. | 50 | carried | 'A higher ceiling lets a node hold more in-flight append memory before refusing' in `merged.md` -- The reference directly states what a higher ceiling permits. |
| 36 | A node holding too much in-flight append memory runs out of memory instead of refusing. | 50 | carried | 'a node holding too much runs out of memory instead of refusing' in `merged.md` -- The reference explicitly contrasts running out of memory with refusing when a node holds too much. |
| 37 | The `ingest_guard.memory.leader.ceiling` setting is read at startup. | 50 | carried | 'The setting is read at startup' in `merged.md` -- The reference directly states when the setting is read. |
| 38 | The cluster must be restarted for a change to the `ingest_guard.memory.leader.ceiling` setting to take. | 50 | carried | 'the cluster must be restarted for a change to take' in `merged.md` -- The reference states that a restart is required for the change to take. |
| 39 | Refusals that show up only during a spike usually clear on their own once the queues drain. | 52 | carried | 'Refusals that show up only during a spike usually clear on their own once the queues drain.' in `merged.md` -- The reference states that spike-only refusals usually clear once the queues drain. |

### `source_b.md` -- 20 claim(s): 0 dropped, 0 contradicted, 2 carried in part, 18 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 13 | A handful of queries run for as long as 2 seconds each. | 24 | carried in part | 'Some queries run for as long as 2 seconds each' in `merged.md` -- The reference gives the duration but says only “Some queries,” not that a handful do. |
| 18 | Processor load looks unremarkable. | 26 | carried in part | 'Processor load can look unremarkable' in `merged.md` -- The reference says processor load can look unremarkable, but does not assert unconditionally that it does. |
| 1 | The share of HTTP `429` replies on a managed Nimbrel Ledger deployment (NMD) climbed over a fortnight. | 8 | carried | 'On a managed Nimbrel Ledger deployment (NMD), the front proxy can count a rising share of HTTP `429` replies over a fortnight.' in `merged.md` -- The reference describes a rising share of HTTP 429 replies over a fortnight on a managed deployment. |
| 2 | The share of HTTP `429` replies was counted at the front proxy. | 8 | carried | 'the front proxy can count a rising share of HTTP `429` replies over a fortnight.' in `merged.md` -- The reference locates the counting of the reply share at the front proxy. |
| 3 | The product is Nimbrel Ledger. | 12 | carried | 'Product: Nimbrel Ledger' in `merged.md` -- The environment section names Nimbrel Ledger as the product. |
| 4 | The product version is 4.4. | 13 | carried | 'Version: 4.4, 5.x' in `merged.md` -- The version list includes 4.4. |
| 5 | The product version is 5.x. | 13 | carried | 'Version: 4.4, 5.x' in `merged.md` -- The version list includes 5.x. |
| 6 | The platform is Nimbrel Cloud. | 14 | carried | 'Platform: Nimbrel Cloud' in `merged.md` -- The environment section names Nimbrel Cloud as the platform. |
| 7 | The deployment is Managed Ledger Service (MLS). | 15 | carried | 'Deployment: Managed Ledger Service (MLS)' in `merged.md` -- The environment section names Managed Ledger Service (MLS) as the deployment. |
| 8 | The production environment is Yes. | 16 | carried | 'Production Environment: Yes' in `merged.md` -- The environment section states that the production environment is Yes. |
| 9 | The managed deployment returns HTTP `429` on a growing share of requests. | 20 | carried | 'On a managed Nimbrel Ledger deployment (NMD), the front proxy can count a rising share of HTTP `429` replies over a fortnight.' in `merged.md` -- The reference describes a rising share of HTTP 429 replies on the managed deployment. |
| 10 | The Ledger returns HTTP `429` when it refuses work rather than queueing it. | 20 | carried | 'The Ledger returns HTTP `429` when it refuses work rather than queueing it.' in `merged.md` -- The reference directly states when the Ledger returns HTTP 429. |
| 11 | Front proxy counters agree with the client reports. | 20 | carried | 'Front proxy counters agree with client reports' in `merged.md` -- The reference explicitly says front proxy counters agree with client reports. |
| 12 | The refusals are real and not a client-side accounting error. | 20 | carried | 'Front proxy counters agree with client reports, so the refusals are real and not a client-side accounting error.' in `merged.md` -- The reference explicitly says the refusals are real and not a client-side accounting error. |
| 14 | A worker slot is unavailable for as long as one of the queries holds it. | 24 | carried | 'Some queries run for as long as 2 seconds each, occupying worker slots' in `merged.md` -- The reference says the queries occupy worker slots, which means those slots are unavailable while occupied. |
| 15 | The queue behind a worker slot grows while one of the queries holds it. | 24 | carried | 'allowing the queue behind them to grow.' in `merged.md` -- The reference explicitly says the queue behind the queries grows. |
| 16 | Grouping on `channel.id` yields a very large number of groups. | 25 | carried | 'Deep grouping on `channel.id` yields a very large number of groups' in `merged.md` -- The reference explicitly states that deep grouping on `channel.id` yields a very large number of groups. |
| 17 | The memory cost of grouping on `channel.id` is charged to the same pool the append path draws on. | 25 | carried | 'the memory that costs is charged to the same pool the append path draws on.' in `merged.md` -- The reference explicitly assigns the memory cost to the same pool used by the append path. |
| 19 | Memory sits high. | 26 | carried | 'memory sits high' in `merged.md` -- The reference explicitly states that memory sits high. |
| 20 | Processor load and memory do not agree. | 26 | carried | 'Processor load can look unremarkable while memory sits high; this mismatch points at query cost rather than at an undersized cluster.' in `merged.md` -- The reference describes unremarkable processor load alongside high memory as a mismatch. |

### `merged.md` -- 72 claim(s): 0 invented, 0 contradicted, 0 supported in part, 72 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Priya Raghunathan is listed as an author. | supported | `source_a.md` | 'Author: Priya Raghunathan' in `source_a.md` -- The author line lists Priya Raghunathan. |
| 2 | The document lists an update date of 2026-03-18 for Priya Raghunathan's entry. | supported | `source_a.md` | 'Updated: 2026-03-18' in `source_a.md` -- The document gives this update date. |
| 3 | Devin Okonkwo is listed as an author. | supported | `source_b.md` | 'Author: Devin Okonkwo' in `source_b.md` -- The author line lists Devin Okonkwo. |
| 4 | The document lists an update date of 2026-04-11 for Devin Okonkwo's entry. | supported | `source_b.md` | 'Updated: 2026-04-11' in `source_b.md` -- The document gives this update date. |
| 5 | Append requests to Nimbrel Ledger can come back with HTTP 429 `Too Many Requests`. | supported | `source_a.md` | 'Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests`.' in `source_a.md` -- The issue description states that append requests can return this response. |
| 6 | Callers see a write that will not land. | supported | `source_a.md` | 'Callers see a write that will not land' in `source_a.md` -- The source directly describes callers seeing a write that will not land. |
| 7 | Nimbrel Relay stalls. | supported | `source_a.md` | 'Nimbrel Relay stalls' in `source_a.md` -- The source states that Nimbrel Relay stalls. |
| 8 | Batch loaders resend the same envelope. | supported | `source_a.md` | 'batch loaders resend the same envelope' in `source_a.md` -- The source states that batch loaders resend the same envelope. |
| 9 | Reads against the same shard begin to time out. | supported | `source_a.md` | 'reads against the same shard begin to time out' in `source_a.md` -- The source states that reads against the same shard begin to time out. |
| 10 | The refusal reaches the client. | supported | `source_a.md` | 'The refusal reaches the client' in `source_a.md` -- The source directly says the refusal reaches the client. |
| 11 | The refusal is written to the Relay logs. | supported | `source_a.md` | 'written to the Relay' in `source_a.md` -- The source says the refusal is written to the Relay logs. |
| 12 | The refusal is written to the Collector logs. | supported | `source_a.md` | 'written to the Collector logs' in `source_a.md`, **transcription_error** -- The source says the refusal is written to the Collector logs. |
| 13 | On a managed Nimbrel Ledger deployment (NMD), the front proxy can count a rising share of HTTP `429` replies over a fortnight. | supported | `source_b.md` | 'This note concerns a managed Nimbrel Ledger deployment (NMD) whose share of HTTP `429` replies climbed over a fortnight, as counted at the front proxy.' in `source_b.md` -- This states the share climbed over a fortnight and was counted at the front proxy. |
| 14 | The Ledger returns HTTP `429` when it refuses work rather than queueing it. | supported | `source_b.md` | 'The managed deployment returns HTTP `429` on a growing share of requests, which is what the Ledger does when it refuses work rather than queueing it.' in `source_b.md` -- The source directly links HTTP 429 with the Ledger refusing work rather than queueing it. |
| 15 | Front proxy counters agree with client reports. | supported | `source_b.md` | 'Front proxy counters agree with the client reports' in `source_b.md` -- The source states that the front proxy counters agree with client reports. |
| 16 | The refusals are real and not a client-side accounting error. | supported | `source_b.md` | 'the refusals are real and not a client-side accounting error' in `source_b.md` -- The source explicitly says the refusals are real, not a client-side accounting error. |
| 17 | The sample append batch was refused after 0 of 64 envelopes. | supported | `source_a.md` | 'append batch refused after 0 of 64 envelopes' in `source_a.md` -- The sample response gives this refusal count. |
| 18 | The sample refusal was an append refusal on the ingest path. | supported | `source_a.md` | 'refused append on ingest path' in `source_a.md` -- The sample response identifies the refusal as an append refusal on the ingest path. |
| 19 | The sample refusal response has status 429. | supported | `source_a.md` | 'status":429' in `source_a.md` -- The sample refusal response specifies status 429. |
| 20 | The sample refusal type is nbl_queue_refused_exception. | supported | `source_a.md` | 'type":"nbl_queue_refused_exception"' in `source_a.md` -- The sample refusal response gives this exception type. |
| 21 | The sample refusal has ingest_and_leader_bytes=88121344. | supported | `source_a.md` | 'ingest_and_leader_bytes=88121344' in `source_a.md` -- The sample refusal response gives this ingest and leader byte count. |
| 22 | The sample refusal has follower_bytes=212992. | supported | `source_a.md` | 'follower_bytes=212992' in `source_a.md` -- The sample refusal response gives this follower byte count. |
| 23 | The sample refusal has all_bytes=88334336. | supported | `source_a.md` | 'all_bytes=88334336' in `source_a.md` -- The sample refusal response gives this total byte count. |
| 24 | The sample refusal has ingest_op_bytes=155648. | supported | `source_a.md` | 'ingest_op_bytes=155648' in `source_a.md` -- The sample refusal response gives this ingest operation byte count. |
| 25 | The sample refusal has max_ingest_bytes=88080384. | supported | `source_a.md` | 'max_ingest_bytes=88080384' in `source_a.md` -- The sample refusal response gives this maximum ingest byte count. |
| 26 | Every Nimbrel Ledger release on every platform can refuse an append this way. | supported | `source_a.md` | 'Every Nimbrel Ledger release on every platform can refuse an append this way.' in `source_a.md` -- The source states this directly in its Environment section. |
| 27 | The listed product is Nimbrel Ledger. | supported | `source_b.md` | '- Product: Nimbrel Ledger' in `source_b.md` -- The listed product is Nimbrel Ledger. |
| 28 | The listed versions are 4.4, 5.x. | supported | `source_b.md` | '- Version: 4.4, 5.x' in `source_b.md` -- The listed versions are 4.4 and 5.x. |
| 29 | The listed platform is Nimbrel Cloud. | supported | `source_b.md` | '- Platform: Nimbrel Cloud' in `source_b.md` -- The listed platform is Nimbrel Cloud. |
| 30 | The listed deployment is Managed Ledger Service (MLS). | supported | `source_b.md` | '- Deployment: Managed Ledger Service (MLS)' in `source_b.md` -- The deployment is listed as Managed Ledger Service (MLS). |
| 31 | The listed production environment value is Yes. | supported | `source_b.md` | '- Production Environment: Yes' in `source_b.md` -- The listed production environment value is Yes. |
| 32 | A Ledger node sends a [`429 - Too Many Requests` reply](https://docs.nimbrel.example/ledger/http-status-codes) once it has nowhere left to put the work. | supported | `source_a.md` | 'A [`429 - Too Many Requests` reply](https://docs.nimbrel.example/ledger/http-status-codes) is what a Ledger node sends once it has nowhere left to put the work' in `source_a.md` -- The source states that a Ledger node sends this reply once it has nowhere left to put the work. |
| 33 | An append queue or a read queue being full is described as the Ledger having nowhere left to put the work. | supported | `source_a.md` | 'once [an append queue or a read queue is full](https://docs.nimbrel.example/ledger/why-appends-are-refused).' in `source_a.md` -- The source identifies a full append or read queue as what it means to have nowhere left to put the work. |
| 34 | There are 3 ways an append draws a 429. | supported | `source_a.md` | 'There are 3 ways an append draws a 429:' in `source_a.md` -- The source explicitly says there are three ways an append draws a 429. |
| 35 | The `append` or `system_append` worker pools can hold more batches than they have slots for. | supported | `source_a.md` | 'The `append` or `system_append` worker pools hold more batches than they have slots for (`nbctl pool status --all`)' in `source_a.md` -- The source lists worker pools holding more batches than available slots as one way an append draws a 429. |
| 36 | The ingest memory guard can refuse a batch. | supported | `source_a.md` | 'The ingest memory guard has refused the batch (`nbctl guard report ingest --counters`). [1]' in `source_a.md` -- The source lists refusal by the ingest memory guard as one way an append draws a 429. |
| 37 | A circuit breaker can trip and cause an append to draw a 429. | supported | `source_a.md` | 'A circuit breaker has tripped (`nbctl breaker list --tripped`) - a breaker trips on any operation and is not particular to appends.' in `source_a.md` -- The source lists a tripped circuit breaker as a way an append draws a 429. |
| 38 | A breaker trips on any operation. | supported | `source_a.md` | 'a breaker trips on any operation' in `source_a.md` -- The source directly states that a breaker trips on any operation. |
| 39 | A breaker is not particular to appends. | supported | `source_a.md` | 'and is not particular to appends.' in `source_a.md` -- The source directly states that a breaker is not particular to appends. |
| 40 | From release 4.6 and release 5.1 onward, appending to a `wide_text` column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory. | supported | `source_a.md` | '[1] **From release 4.6 and release 5.1 onward**, appending to a `wide_text` column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory.' in `source_a.md` -- The source states this release-specific condition and outcome directly. |
| 41 | Expensive queries can contribute to refusals. | supported | `source_b.md` | '- **Expensive queries**: a handful of queries run for as long as 2 seconds each. A worker slot is unavailable for as long as one of them holds it, and the queue behind it grows.' in `source_b.md` -- Expensive queries are listed as a contributing factor to the refusals. |
| 42 | Deep grouping can contribute to refusals. | supported | `source_b.md` | '- **Deep grouping**: grouping on `channel.id` yields a very large number of groups, and the memory that costs is charged to the same pool the append path draws on.' in `source_b.md` -- Deep grouping is listed as a contributing factor to the refusals. |
| 43 | Some queries run for as long as 2 seconds each. | supported | `source_b.md` | 'a handful of queries run for as long as 2 seconds each.' in `source_b.md` -- The source says a handful of queries run for as long as two seconds each. |
| 44 | Some queries occupy worker slots. | supported | `source_b.md` | 'A worker slot is unavailable for as long as one of them holds it' in `source_b.md` -- The source says a query holding a worker slot makes it unavailable. |
| 45 | Some queries allow the queue behind them to grow. | supported | `source_b.md` | 'and the queue behind it grows.' in `source_b.md` -- The source states that the queue behind a query holding a slot grows. |
| 46 | Deep grouping on `channel.id` yields a very large number of groups. | supported | `source_b.md` | 'grouping on `channel.id` yields a very large number of groups' in `source_b.md` -- The source states that grouping on `channel.id` yields a very large number of groups. |
| 47 | The memory cost of deep grouping on `channel.id` is charged to the same pool the append path draws on. | supported | `source_b.md` | 'the memory that costs is charged to the same pool the append path draws on.' in `source_b.md` -- The source directly connects the grouping memory cost to the pool used by the append path. |
| 48 | Processor load can look unremarkable while memory sits high. | supported | `source_b.md` | 'processor load looks unremarkable while memory sits high.' in `source_b.md` -- The source directly describes unremarkable processor load alongside high memory. |
| 49 | A mismatch between unremarkable processor load and high memory points at query cost rather than at an undersized cluster. | supported | `source_b.md` | 'The two do not agree, which points at query cost rather than at an undersized cluster.' in `source_b.md` -- The source says the discrepancy points to query cost rather than an undersized cluster. |
| 50 | Taking append and query load off the cluster long enough allows the queues to drain. | supported | `source_a.md` | 'Take append and query load off the cluster for long enough that the queues drain and the nodes fall back under their limits.' in `source_a.md` -- The source says taking append and query load off long enough allows the queues to drain. |
| 51 | Taking append and query load off the cluster long enough allows the nodes to fall back under their limits. | supported | `source_a.md` | 'Take append and query load off the cluster for long enough that the queues drain and the nodes fall back under their limits.' in `source_a.md` -- The workaround explicitly says this allows the queues to drain and nodes to fall back under their limits. |
| 52 | Where batches carry `wide_text` columns and the cluster runs release 4.6 or release 5.1 or later, fewer envelopes per batch can be sent. | supported | `source_a.md` | 'Where batches carry `wide_text` columns and the cluster runs release 4.6 or release 5.1 or later, send fewer envelopes per batch.' in `source_a.md` -- The source gives fewer envelopes per batch as the guidance for that condition. |
| 53 | The slow query threshold can be set to 1 second. | supported | `source_b.md` | 'set it to 1 second' in `source_b.md` -- The proposed action explicitly sets the slow query threshold to 1 second. |
| 54 | Setting the slow query threshold to 1 second records the queries actually responsible instead of averaging them away. | supported | `source_b.md` | 'so that the queries actually responsible are recorded instead of averaged away.' in `source_b.md` -- The source states that setting the threshold to 1 second will record the responsible queries instead of averaging them away. |
| 55 | Several of the expensive queries look like they could ask for less. | supported | `source_b.md` | 'several of which look like they could ask for less.' in `source_b.md` -- The source says several of the expensive queries look like they could ask for less. |
| 56 | During a refusal, a thread dump and a heap snapshot can be taken while the refusal rate is high. | supported | `source_b.md` | 'while the refusal rate is high, take a thread dump and a heap snapshot rather than reasoning from counters alone.' in `source_b.md` -- The proposed action recommends taking both snapshots while the refusal rate is high. |
| 57 | The document describes a cluster that refuses appends as having been given more work than its hardware can carry. | supported | `source_a.md` | 'A cluster that refuses appends has been given more work than its hardware can carry' in `source_a.md` -- The source describes a refusing cluster as having more work than its hardware can carry. |
| 58 | Larger nodes are described as scaling up. | supported | `source_a.md` | 'larger nodes (scale up)' in `source_a.md` -- The source explicitly labels larger nodes as scaling up. |
| 59 | Having more nodes is described as scaling out. | supported | `source_a.md` | 'more of them (scale out)' in `source_a.md` -- The source explicitly labels having more nodes as scaling out. |
| 60 | Scale up is preferred first in most cases. | supported | `source_a.md` | 'Scale up first in most cases' in `source_a.md` -- The source says to scale up first in most cases. |
| 61 | Scale out is used when what is wanted is a further copy of the data for availability. | supported | `source_a.md` | 'scale out when what is wanted is a further copy of the data for availability' in `source_a.md` -- The source gives a further copy of the data for availability as the reason to scale out. |
| 62 | Splitting a hot stream over more leader shards spreads append load across more nodes. | supported | `source_a.md` | 'Splitting a hot stream over more leader shards spreads append load across more nodes' in `source_a.md` -- The source states that splitting a hot stream over more leader shards spreads append load across more nodes. |
| 63 | Splitting a hot stream over more leader shards helps in some layouts. | supported | `source_a.md` | 'which helps in some layouts.' in `source_a.md` -- The source says that this approach helps in some layouts. |
| 64 | For `wide_text` columns on release 4.6 and release 5.1 and later, the guidance begins by cutting the number of envelopes in each append batch. | supported | `source_a.md` | 'For `wide_text` columns on release 4.6 and release 5.1 and later:\n\n1. Begin by cutting the number of envelopes in each append batch.' in `source_a.md` -- The source gives cutting batch envelope counts as the first step for the stated `wide_text` releases. |
| 65 | Where smaller batches do not clear the issue, the guidance is to add processor and memory capacity to the nodes. | supported | `source_a.md` | '2. Where smaller batches do not clear it, add processor and memory capacity to the nodes.' in `source_a.md` -- The source recommends adding processor and memory capacity if smaller batches do not resolve the issue. |
| 66 | The guidance is to raise the `ingest_guard.memory.leader.ceiling` cluster setting only after the earlier steps. | supported | `source_a.md` | '3. Only then raise the `ingest_guard.memory.leader.ceiling` cluster setting, which defaults to 10% of the heap.' in `source_a.md` -- The source says to raise the setting only after the preceding steps. |
| 67 | The `ingest_guard.memory.leader.ceiling` cluster setting defaults to 10% of the heap. | supported | `source_a.md` | 'the `ingest_guard.memory.leader.ceiling` cluster setting, which defaults to 10% of the heap.' in `source_a.md` -- The source gives the setting's default as 10% of the heap. |
| 68 | A higher `ingest_guard.memory.leader.ceiling` lets a node hold more in-flight append memory before refusing. | supported | `source_a.md` | 'A higher ceiling lets a node hold more in-flight append memory before refusing' in `source_a.md` -- The source states that a higher ceiling allows more in-flight append memory before refusal. |
| 69 | A node holding too much in-flight append memory runs out of memory instead of refusing. | supported | `source_a.md` | 'a node holding too much runs out of memory instead of refusing' in `source_a.md` -- The source states that holding too much results in running out of memory rather than refusal. |
| 70 | The setting is read at startup. | supported | `source_a.md` | 'The setting is read at startup' in `source_a.md` -- The source explicitly says the setting is read at startup. |
| 71 | The cluster must be restarted for a change to the setting to take effect. | supported | `source_a.md` | 'the cluster must be restarted for a change to take.' in `source_a.md` -- The source states that a restart is required for a setting change to take effect. |
| 72 | Refusals that show up only during a spike usually clear on their own once the queues drain. | supported | `source_a.md` | 'Refusals that show up only during a spike usually clear on their own once the queues drain.' in `source_a.md` -- The source states that spike-only refusals usually clear once the queues drain. |

## Structure

**9** mechanical check(s) over **63** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **72** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **59**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 12 run(s) over 47 attributed segment(s) — sources interleaved. 8 of 13 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

`[-...-]` is what the source said and `{+...+}` is what the merge says.

### Reworded and undeclared — in the merge in altered wording, and no record explains it. At off this also covers layout: a segment whose source line breaks the merge ran together is altered and undeclared, and 380 reuses this kind rather than moving FINDING_KINDS off 12

- `b14` (`source_b.md`) — 'Front proxy counters agree with the client reports, so the refusals are real and not a client-side accounting error.' is reworded in the merge and no disposition record explains it (nearest merge segment m10 at 0.98)

  ```text
  In the source: Front proxy counters agree with the client reports, so the refusals are real and not a client-side accounting error.
  In the merge:  Front proxy counters agree with client reports, so the refusals are real and not a client-side accounting error.
  What changed:  Front proxy counters agree with [-the-] client reports, so the refusals are real and not a client-side accounting error.
  ```

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **14** departure(s) from its sources. Checking them confirms 7, rejects 2, and leaves 5 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 63 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | The base title is retained. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Nimbrel Ledger append rejected with HTTP 429' and says so (no claim traced to it) |
| `b3` | subsumed | The overview content is consolidated under the base issue heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b4` | reconciled | The deployment, rising share, interval, and counter are combined. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-001`, `B-002`) |
| `b5` | subsumed | The evidence and proposed response are detailed in Cause and Workaround. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b12` | duplicate | The issue heading is already present in the base structure. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b13` | reconciled | Combined with b4 to retain the deployment trend and front-proxy context. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-009`, `B-010`) |
| `b15` | subsumed | Contributing factors are consolidated under the base Cause heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b16` | reconciled | Query duration and its effect on worker slots are combined. | **rejected** | declared 'reconciled', which predicts SUPPORTED; B-013 came back PARTIAL (`B-013`) |
| `b17` | reconciled | The queue effect is combined with the query-duration statement. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-014`, `B-015`) |
| `b18` | reworded | The grouping and shared memory-pool cause is clarified. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-016`, `B-017`) |
| `b19` | reconciled | The resource readings and their stated implication are combined. | **rejected** | declared 'reconciled', which predicts SUPPORTED; B-018 came back PARTIAL (`B-018`) |
| `b20` | reconciled | The mismatch and its interpretation are combined with b19. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-020`) |
| `b21` | subsumed | The proposed actions are placed under the base Workaround heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b25` | subsumed | The reference heading is represented by the retained reference links. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | bf7d5842201d (hosted) |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | gpt-6-luna |
| Model (decompose) | gpt-6-luna |
| Model (verify) | gpt-6-luna |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed 0, thinking decompose, merge, verify, profile openai-reasoning |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 10 live, 0 cached, 0 replayed |
| Tokens | 32,287 in, 30,448 out, 0 cached, 13,656 reasoning |
| Cost | ~$0.02 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 207.3s |
| Generated | 2026-09-27T15:25:48+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `bf7d5842201d`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
