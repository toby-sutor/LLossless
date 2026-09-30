## Verdict

**37 finding(s).** In the claims: 7 dropped, 1 contradicted. In the structure: 24 undeclared absence, 5 verbatim violation.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 29 |
| Claims extracted from `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 24 |
| Claims extracted from `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 19 |
| Forward — source claims accounted for in the merge | **35/43** |
| Forward — carried only in part | 0 |
| Forward — `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` claims accounted for | **24/24** |
| Forward — `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` claims accounted for | **11/19** |
| Reverse — merge claims found in a source | **29/29** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **58/65** |
| Units of work errored | 0 |

The model was shown `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` as `source_a.md`, `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` as `source_b.md`. Every filename in the findings below is the canonical one; the mapping above is how to read it. The names are fixed because the published figures were measured with them, and a prompt that varies with the caller's filenames is a prompt nothing was measured against.

## Findings

### Dropped — in a source, not in the merge

- **B-001** (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md:3`) — Author: Devin Okonkwo
  - rationale: The reference text does not mention Devin Okonkwo as an author.
- **B-003** (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md:8`) — This note concerns a managed Nimbrel Ledger deployment (NMD) whose share of HTTP `429` replies climbed over a fortnight, as counted at the front proxy.
  - rationale: The reference text does not mention a managed deployment's share of HTTP 429 replies increasing over a fortnight.
- **B-005** (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md:13`) — Version: 4.4, 5.x
  - rationale: The reference text does not mention versions 4.4 or 5.x.
- **B-006** (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md:14`) — Platform: Nimbrel Cloud
  - rationale: The reference text does not specify the platform as Nimbrel Cloud.
- **B-007** (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md:15`) — Deployment: Managed Ledger Service (MLS)
  - rationale: The reference text does not mention Managed Ledger Service (MLS).
- **B-008** (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md:16`) — Production Environment: Yes
  - rationale: The reference text does not specify the environment as production.
- **B-010** (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md:20`) — Front proxy counters agree with the client reports, so the refusals are real and not a client-side accounting error.
  - rationale: The reference text does not mention front proxy counters agreeing with client reports.

### Contradicted — the merge states something different

- **B-002** -- the two documents disagree
  - `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md:4` says: Updated: 2026-04-11
  - `merged.md` says: 'Author: Priya Raghunathan Updated: 2026-03-18' (grounded)
  - why this was read as a contradiction: The reference text states the update date as 2026-03-18, which contradicts the claim's date of 2026-04-11.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- 24 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 24 carried

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Author: Priya Raghunathan | 3 | carried | 'Author: Priya Raghunathan' in `merged.md` -- The reference text states the author is Priya Raghunathan. |
| 2 | Updated: 2026-03-18 | 4 | carried | 'Updated: 2026-03-18' in `merged.md` -- The reference text states the updated date is 2026-03-18. |
| 3 | Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests`. | 8 | carried | 'Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests`.' in `merged.md` -- The reference text states append requests result in HTTP 429. |
| 4 | Callers see a write that will not land: Nimbrel Relay stalls, batch loaders resend the same envelope, and reads against the same shard begin to time out. | 8 | carried | 'Callers see a write that will not land: Nimbrel Relay stalls, batch loaders resend the same envelope, and reads against the same shard begin to time out.' in `merged.md` -- The reference text describes the effects of the refusal. |
| 5 | The refusal reaches the client and is written to the Relay and Collector logs as well. | 8 | carried | 'The refusal reaches the client and is written to the Relay and Collector logs as well.' in `merged.md` -- The reference text states the refusal is logged in Relay and Collector logs. |
| 6 | The Ledger operations handbook now covers the same ground under Refused Appends, with a walkthrough for each of the three refusal paths set out below. | 16 | carried | 'The Ledger operations handbook now covers the same ground under Refused Appends, with a walkthrough for each of the three refusal paths set out below.' in `merged.md` -- The reference text mentions the handbook covers refused appends. |
| 7 | Every Nimbrel Ledger release on every platform can refuse an append this way. | 20 | carried | 'Every Nimbrel Ledger release on every platform can refuse an append this way.' in `merged.md` -- The reference text states all releases can refuse appends. |
| 8 | A [`429 - Too Many Requests` reply](https://docs.nimbrel.example/ledger/http-status-codes) is what a Ledger node sends once it has nowhere left to put the work, which is to say once [an append queue or a read queue is full](https://docs.nimbrel.example/ledger/why-appends-are-refused). | 24 | carried | 'A [`429 - Too Many Requests` reply](https://docs.nimbrel.example/ledger/http-status-codes) is what a Ledger node sends once it has nowhere left to put the work, which is to say once [an append queue or a read queue is full](https://docs.nimbrel.example/ledger/why-appends-are-refused).' in `merged.md` -- The reference text explains the 429 response and queue full condition. |
| 9 | There are 3 ways an append draws a 429: | 26 | carried | 'There are 3 ways an append draws a 429:' in `merged.md` -- The reference text lists three causes for a 429 response. |
| 10 | The `append` or `system_append` worker pools hold more batches than they have slots for (`nbctl pool status --all`) | 28 | carried | 'The `append` or `system_append` worker pools hold more batches than they have slots for (`nbctl pool status --all`)' in `merged.md` -- The reference text states worker pools cause 429 when overloaded. |
| 11 | The ingest memory guard has refused the batch (`nbctl guard report ingest --counters`). [1] | 29 | carried | 'The ingest memory guard has refused the batch (`nbctl guard report ingest --counters`). [1]' in `merged.md` -- The reference text mentions the ingest memory guard refusing batches. |
| 12 | A circuit breaker has tripped (`nbctl breaker list --tripped`) - a breaker trips on any operation and is not particular to appends. | 30 | carried | 'A circuit breaker has tripped (`nbctl breaker list --tripped`) - a breaker trips on any operation and is not particular to appends.' in `merged.md` -- The reference text states circuit breakers cause 429 responses. |
| 13 | From release 4.6 and release 5.1 onward, appending to a `wide_text` column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory. | 32 (unverified) | carried | 'From release 4.6 and release 5.1 onward, appending to a `wide_text` column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory.' in `merged.md`, **transcription_error** -- The reference text explains the wide_text column issue in specific releases. |
| 14 | Take append and query load off the cluster for long enough that the queues drain and the nodes fall back under their limits. | 36 | carried | 'Take append and query load off the cluster for long enough that the queues drain and the nodes fall back under their limits.' in `merged.md` -- The reference text suggests reducing load to clear queues. |
| 15 | Where batches carry `wide_text` columns and the cluster runs release 4.6 or release 5.1 or later, send fewer envelopes per batch. | 38 | carried | 'Where batches carry `wide_text` columns and the cluster runs release 4.6 or release 5.1 or later, send fewer envelopes per batch.' in `merged.md` -- The reference text advises fewer envelopes for wide_text columns. |
| 16 | A cluster that refuses appends has been given more work than its hardware can carry, so the answer is hardware: larger nodes (scale up), or more of them (scale out). | 42 | carried | 'A cluster that refuses appends has been given more work than its hardware can carry, so the answer is hardware: larger nodes (scale up), or more of them (scale out).' in `merged.md` -- The reference text recommends scaling hardware to resolve refusals. |
| 17 | Splitting a hot stream over more leader shards spreads append load across more nodes, which helps in some layouts. | 44 | carried | 'Splitting a hot stream over more leader shards spreads append load across more nodes, which helps in some layouts.' in `merged.md` -- The reference text suggests splitting streams to distribute load. |
| 18 | Begin by cutting the number of envelopes in each append batch. | 48 | carried | 'Begin by cutting the number of envelopes in each append batch.' in `merged.md` -- The reference text recommends reducing batch size first. |
| 19 | Where smaller batches do not clear it, add processor and memory capacity to the nodes. | 49 | carried | 'Where smaller batches do not clear it, add processor and memory capacity to the nodes.' in `merged.md` -- The reference text suggests adding capacity if needed. |
| 20 | Only then raise the `ingest_guard.memory.leader.ceiling` cluster setting, which defaults to 10% of the heap. | 50 | carried | 'Only then raise the `ingest_guard.memory.leader.ceiling` cluster setting, which defaults to 10% of the heap.' in `merged.md` -- The reference text states the default setting and its adjustment. |
| 21 | A higher ceiling lets a node hold more in-flight append memory before refusing, and a node holding too much runs out of memory instead of refusing, which is the worse outcome. | 50 | carried | 'A higher ceiling lets a node hold more in-flight append memory before refusing, and a node holding too much runs out of memory instead of refusing, which is the worse outcome.' in `merged.md` -- The reference text explains the risk of increasing the ceiling. |
| 22 | The setting is read at startup, so the cluster must be restarted for a change to take. | 50 | carried | 'The setting is read at startup, so the cluster must be restarted for a change to take.' in `merged.md` -- The reference text states the setting is read at startup. |
| 23 | Where none of that is open to you, the load itself is what changes: fewer appends, cheaper queries, or both. | 52 | carried | 'Where none of that is open to you, the load itself is what changes: fewer appends, cheaper queries, or both.' in `merged.md` -- The reference text suggests changing load as a last option. |
| 24 | Refusals that show up only during a spike usually clear on their own once the queues drain. | 52 | carried | 'Refusals that show up only during a spike usually clear on their own once the queues drain.' in `merged.md` -- The reference text states temporary refusals clear after queues drain. |

### `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` -- 19 claim(s): 7 dropped, 1 contradicted, 0 carried in part, 11 carried

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Author: Devin Okonkwo | 3 | dropped | The reference text does not mention Devin Okonkwo as an author. |
| 3 | This note concerns a managed Nimbrel Ledger deployment (NMD) whose share of HTTP `429` replies climbed over a fortnight, as counted at the front proxy. | 8 | dropped | The reference text does not mention a managed deployment's share of HTTP 429 replies increasing over a fortnight. |
| 5 | Version: 4.4, 5.x | 13 | dropped | The reference text does not mention versions 4.4 or 5.x. |
| 6 | Platform: Nimbrel Cloud | 14 | dropped | The reference text does not specify the platform as Nimbrel Cloud. |
| 7 | Deployment: Managed Ledger Service (MLS) | 15 | dropped | The reference text does not mention Managed Ledger Service (MLS). |
| 8 | Production Environment: Yes | 16 | dropped | The reference text does not specify the environment as production. |
| 10 | Front proxy counters agree with the client reports, so the refusals are real and not a client-side accounting error. | 20 | dropped | The reference text does not mention front proxy counters agreeing with client reports. |
| 2 | Updated: 2026-04-11 | 4 | contradicted | 'Author: Priya Raghunathan Updated: 2026-03-18' in `merged.md` -- The reference text states the update date as 2026-03-18, which contradicts the claim's date of 2026-04-11. |
| 4 | Product: Nimbrel Ledger | 12 | carried | '# Nimbrel Ledger append rejected with HTTP 429' in `merged.md` -- The reference text explicitly states the product as Nimbrel Ledger. |
| 9 | The managed deployment returns HTTP `429` on a growing share of requests, which is what the Ledger does when it refuses work rather than queueing it. | 20 | carried | 'A [`429 - Too Many Requests` reply](https://docs.nimbrel.example/ledger/http-status-codes) is what a Ledger node sends once it has nowhere left to put the work, which is to say once [an append queue or a read queue is full](https://docs.nimbrel.example/ledger/why-appends-are-refused).' in `merged.md` -- The reference text explains that HTTP 429 occurs when the Ledger refuses work instead of queueing it. |
| 11 | Expensive queries: a handful of queries run for as long as 2 seconds each. | 24 | carried | 'Expensive queries: a handful of queries run for as long as 2 seconds each.' in `merged.md` -- The reference text states that expensive queries run for up to 2 seconds. |
| 12 | Deep grouping: grouping on `channel.id` yields a very large number of groups, and the memory that costs is charged to the same pool the append path draws on. | 25 | carried | 'Deep grouping: grouping on `channel.id` yields a very large number of groups, and the memory that costs is charged to the same pool the append path draws on.' in `merged.md` -- The reference text describes deep grouping on `channel.id` affecting memory. |
| 13 | Resource accounting: processor load looks unremarkable while memory sits high. | 26 | carried | 'Resource accounting: processor load looks unremarkable while memory sits high.' in `merged.md` -- The reference text mentions high memory with normal processor load. |
| 14 | Lower the slow query threshold: set it to 1 second, so that the queries actually responsible are recorded instead of averaged away. | 30 | carried | 'Lower the slow query threshold: set it to 1 second, so that the queries actually responsible are recorded instead of averaged away.' in `merged.md` -- The reference text suggests lowering the slow query threshold to 1 second. |
| 15 | Review what the queries are for: go through the expensive ones with the team that wrote them, several of which look like they could ask for less. | 31 | carried | 'Review what the queries are for: go through the expensive ones with the team that wrote them, several of which look like they could ask for less.' in `merged.md` -- The reference text recommends reviewing expensive queries with the team. |
| 16 | Capture evidence during a refusal: while the refusal rate is high, take a thread dump and a heap snapshot rather than reasoning from counters alone. | 32 | carried | 'Capture evidence during a refusal: while the refusal rate is high, take a thread dump and a heap snapshot rather than reasoning from counters alone.' in `merged.md` -- The reference text suggests capturing evidence during a refusal. |
| 17 | Internal ticket NB-40917 | 38 | carried | '- [Internal ticket NB-40917](https://tickets.nimbrel.example/issues/40917)' in `merged.md` -- The reference text references Internal ticket NB-40917. |
| 18 | Ledger slow query log | 42 | carried | '- [Ledger slow query log](https://docs.nimbrel.example/ledger/slow-query-log)' in `merged.md` -- The reference text includes a link to the Ledger slow query log. |
| 19 | HTTP 429 replies | 43 | carried | '- [HTTP 429 replies](https://support.nimbrel.example/knowledge/318kqp2)' in `merged.md` -- The reference text includes a link about HTTP 429 replies. |

### `merged.md` -- 29 claim(s): 0 invented, 0 contradicted, 0 supported in part, 29 supported

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Author: Priya Raghunathan Updated: 2026-03-18 | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'Author: Priya Raghunathan Updated: 2026-03-18' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The claim matches the author and date in source_a.md. |
| 2 | Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests`. | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests`.' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The claim is directly stated in source_a.md. |
| 3 | Callers see a write that will not land: Nimbrel Relay stalls, batch loaders resend the same envelope, and reads against the same shard begin to time out. | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'Callers see a write that will not land: Nimbrel Relay stalls, batch loaders resend the same envelope, and reads against the same shard begin to time out.' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The claim is explicitly described in source_a.md. |
| 4 | The refusal reaches the client and is written to the Relay and Collector logs as well. | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'The refusal reaches the client and is written to the Relay and Collector logs as well.' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The claim is directly stated in source_a.md. |
| 5 | Every Nimbrel Ledger release on every platform can refuse an append this way. | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'Every Nimbrel Ledger release on every platform can refuse an append this way.' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The claim is explicitly mentioned in source_a.md. |
| 6 | A [`429 - Too Many Requests` reply](https://docs.nimbrel.example/ledger/http-status-codes) is what a Ledger node sends once it has nowhere left to put the work, which is to say once [an append queue or a read queue is full](https://docs.nimbrel.example/ledger/why-appends-are-refused). | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'A [`429 - Too Many Requests` reply](https://docs.nimbrel.example/ledger/http-status-codes) is what a Ledger node sends once it has nowhere left to put the work, which is to say once [an append queue or a read queue is full](https://docs.nimbrel.example/ledger/why-appends-are-refused).' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The claim is directly stated in source_a.md. |
| 7 | The `append` or `system_append` worker pools hold more batches than they have slots for (`nbctl pool status --all`) | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'The `append` or `system_append` worker pools hold more batches than they have slots for (`nbctl pool status --all`)' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The claim is explicitly listed in source_a.md. |
| 8 | The ingest memory guard has refused the batch (`nbctl guard report ingest --counters`). [1] | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'The ingest memory guard has refused the batch (`nbctl guard report ingest --counters`). [1]' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The claim is directly stated in source_a.md. |
| 9 | A circuit breaker has tripped (`nbctl breaker list --tripped`) - a breaker trips on any operation and is not particular to appends. | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'A circuit breaker has tripped (`nbctl breaker list --tripped`) - a breaker trips on any operation and is not particular to appends.' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The claim is explicitly mentioned in source_a.md. |
| 10 | Expensive queries: a handful of queries run for as long as 2 seconds each. | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 'Expensive queries: a handful of queries run for as long as 2 seconds each.' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`, **transcription_error** -- The claim is directly stated in source_b.md. |
| 11 | Deep grouping: grouping on `channel.id` yields a very large number of groups, and the memory that costs is charged to the same pool the append path draws on. | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 'Deep grouping: grouping on `channel.id` yields a very large number of groups, and the memory that costs is charged to the same pool the append path draws on.' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`, **transcription_error** -- The claim is explicitly described in source_b.md. |
| 12 | Resource accounting: processor load looks unremarkable while memory sits high. | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 'Resource accounting: processor load looks unremarkable while memory sits high.' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`, **transcription_error** -- The claim is directly stated in source_b.md. |
| 13 | [1] **From release 4.6 and release 5.1 onward**, appending to a `wide_text` column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory. | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | '[1] **From release 4.6 and release 5.1 onward**, appending to a `wide_text` column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory.' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The claim is explicitly mentioned in source_a.md. |
| 14 | Take append and query load off the cluster for long enough that the queues drain and the nodes fall back under their limits. | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'Take append and query load off the cluster for long enough that the queues drain and the nodes fall back under their limits.' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The claim is directly stated in source_a.md. |
| 15 | Where batches carry `wide_text` columns and the cluster runs release 4.6 or release 5.1 or later, send fewer envelopes per batch. | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'Where batches carry `wide_text` columns and the cluster runs release 4.6 or release 5.1 or later, send fewer envelopes per batch.' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The claim is explicitly mentioned in source_a.md. |
| 16 | Lower the slow query threshold: set it to 1 second, so that the queries actually responsible are recorded instead of averaged away. | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 'Lower the slow query threshold: set it to 1 second, so that the queries actually responsible are recorded instead of averaged away.' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`, **transcription_error** -- The claim is directly stated in source_b.md. |
| 17 | Review what the queries are for: go through the expensive ones with the team that wrote them, several of which look like they could ask for less. | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 'Review what the queries are for: go through the expensive ones with the team that wrote them, several of which look like they could ask for less.' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`, **transcription_error** -- The claim is explicitly described in source_b.md. |
| 18 | Capture evidence during a refusal: while the refusal rate is high, take a thread dump and a heap snapshot rather than reasoning from counters alone. | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 'Capture evidence during a refusal: while the refusal rate is high, take a thread dump and a heap snapshot rather than reasoning from counters alone.' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`, **transcription_error** -- The claim is directly stated in source_b.md. |
| 19 | A cluster that refuses appends has been given more work than its hardware can carry, so the answer is hardware: larger nodes (scale up), or more of them (scale out). | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'A cluster that refuses appends has been given more work than its hardware can carry, so the answer is hardware: larger nodes (scale up), or more of them (scale out).' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The claim is explicitly mentioned in source_a.md. |
| 20 | Scale up first in most cases, and scale out when what is wanted is a further copy of the data for availability, per [the sizing notes](https://docs.nimbrel.example/ledger/sizing). | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'Scale up first in most cases, and scale out when what is wanted is a further copy of the data for availability, per [the sizing notes](https://docs.nimbrel.example/ledger/sizing).' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The claim is directly stated in source_a.md. |
| 21 | Splitting a hot stream over more leader shards spreads append load across more nodes, which helps in some layouts. | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'Splitting a hot stream over more leader shards spreads append load across more nodes, which helps in some layouts.' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The claim is explicitly described in source_a.md. |
| 22 | Begin by cutting the number of envelopes in each append batch. | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'Begin by cutting the number of envelopes in each append batch.' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The claim is directly stated in source_a.md. |
| 23 | Where smaller batches do not clear it, add processor and memory capacity to the nodes. | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'Where smaller batches do not clear it, add processor and memory capacity to the nodes.' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The claim is explicitly mentioned in source_a.md. |
| 24 | A higher ceiling lets a node hold more in-flight append memory before refusing, and a node holding too much runs out of memory instead of refusing, which is the worse outcome. | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'A higher ceiling lets a node hold more in-flight append memory before refusing, and a node holding too much runs out of memory instead of refusing, which is the worse outcome.' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The claim is directly stated in source_a.md. |
| 25 | Where none of that is open to you, the load itself is what changes: fewer appends, cheaper queries, or both. | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'Where none of that is open to you, the load itself is what changes: fewer appends, cheaper queries, or both.' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The claim is explicitly mentioned in source_a.md. |
| 26 | Refusals that show up only during a spike usually clear on their own once the queues drain. | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'Refusals that show up only during a spike usually clear on their own once the queues drain.' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The claim is directly stated in source_a.md under the Resolution section, exactly as written in the claim. The wording matches precisely, so the claim is supported by the source document provided. The evidence is taken verbatim from the source, ensuring accuracy and direct support for the claim made. The rationale confirms that the source explicitly states the claim, leaving no room for ambiguity. |
| 27 | [Internal ticket NB-40917](https://tickets.nimbrel.example/issues/40917) | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | '[Internal ticket NB-40917](https://tickets.nimbrel.example/issues/40917)' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` -- The claim is present in source_b.md under the References section, exactly as written in the claim. The link is included verbatim, ensuring that the evidence directly supports the claim without any alterations. The rationale confirms that the source explicitly states the claim, providing clear support. The evidence is taken directly from the source, maintaining the integrity and accuracy required. |
| 28 | [Ledger slow query log](https://docs.nimbrel.example/ledger/slow-query-log) | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | '[Ledger slow query log](https://docs.nimbrel.example/ledger/slow-query-log)' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` -- The claim is present in source_b.md under the References section, exactly as written in the claim. The link is included verbatim, ensuring that the evidence directly supports the claim without any alterations. The rationale confirms that the source explicitly states the claim, providing clear support. The evidence is taken directly from the source, maintaining the integrity and accuracy required. |
| 29 | [HTTP 429 replies](https://support.nimbrel.example/knowledge/318kqp2) | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | '[HTTP 429 replies](https://support.nimbrel.example/knowledge/318kqp2)' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` -- The claim is present in source_b.md under the References section, exactly as written in the claim. The link is included verbatim, ensuring that the evidence directly supports the claim without any alterations. The rationale confirms that the source explicitly states the claim, providing clear support. The evidence is taken directly from the source, maintaining the integrity and accuracy required. |

## Structure

**9** mechanical check(s) over **63** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.

Ordering: 6 run(s) over 39 attributed segment(s) — sources interleaved. 9 of 13 source heading(s) survive. This is a measurement, not a finding: a concatenation is the correct merge when the sources share no subject.

### Absent and undeclared — in a source, not in the merge, and no record explains it

- `a7` (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md`) — 'A full refusal envelope from a batched append reads like this:' is not in the merge and no disposition record explains it (nearest merge segment m33 at 0.44)
- `a8` (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md`) — '```\nappend batch refused after 0 of 64 envelopes: 429 Too Many Requests: {"error":{"root_cause":[{"type":"nbl_queue_refused_exception","reason":"refused append on ingest path [ingest_and_leader_bytes=88121344, follower_bytes=212992, all_bytes=88334336, ingest_op_bytes=155648, max_ingest_bytes=88080384]"}],"type":"nbl_queue_refused_exception","reason":"refused append on ingest path [ingest_and_leader_bytes=88121344, follower_bytes=212992, all_bytes=88334336, ingest_op_bytes=155648, max_ingest_bytes=88080384]"},"status":429}\n```' is not in the merge and no disposition record explains it (nearest merge segment m22 at 0.17)
- `b2` (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`) — 'Author: Devin Okonkwo Updated: 2026-04-11' is not in the merge and no disposition record explains it (nearest merge segment m2 at 0.67)
- `b3` (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`) — 'Summary / Table of Contents' is not in the merge and no disposition record explains it (nearest merge segment m40 at 0.32)
- `b4` (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`) — 'This note concerns a managed Nimbrel Ledger deployment (NMD) whose share of HTTP `429` replies climbed over a fortnight, as counted at the front proxy.' is not in the merge and no disposition record explains it (nearest merge segment m9 at 0.39)
- `b5` (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`) — 'It sets out what the evidence pointed at, which was expensive queries and deep grouping, and what was put forward in response.' is not in the merge and no disposition record explains it (nearest merge segment m26 at 0.40)
- `b7` (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`) — 'Product: Nimbrel Ledger' is not in the merge and no disposition record explains it (nearest merge segment m1 at 0.42)
- `b8` (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`) — 'Version: 4.4, 5.x' is not in the merge and no disposition record explains it (nearest merge segment m28 at 0.37)
- `b9` (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`) — 'Platform: Nimbrel Cloud' is not in the merge and no disposition record explains it (nearest merge segment m24 at 0.39)
- `b10` (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`) — 'Deployment: Managed Ledger Service (MLS)' is not in the merge and no disposition record explains it (nearest merge segment m4 at 0.34)
- `b11` (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`) — 'Production Environment: Yes' is not in the merge and no disposition record explains it (nearest merge segment m8 at 0.58)
- `b14` (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`) — 'Front proxy counters agree with the client reports, so the refusals are real and not a client-side accounting error.' is not in the merge and no disposition record explains it (nearest merge segment m27 at 0.42)
- `b15` (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`) — 'Contributing Factors' is not in the merge and no disposition record explains it (nearest merge segment m16 at 0.43)
- `b16` (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`) — '**Expensive queries**: a handful of queries run for as long as 2 seconds each.' is not in the merge and no disposition record explains it (nearest merge segment m17 at 0.97)
- `b17` (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`) — 'A worker slot is unavailable for as long as one of them holds it, and the queue behind it grows.' is not in the merge and no disposition record explains it (nearest merge segment m39 at 0.42)
- `b18` (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`) — '**Deep grouping**: grouping on `channel.id` yields a very large number of groups, and the memory that costs is charged to the same pool the append path draws on.' is not in the merge and no disposition record explains it (nearest merge segment m18 at 0.99)
- `b19` (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`) — '**Resource accounting**: processor load looks unremarkable while memory sits high.' is not in the merge and no disposition record explains it (nearest merge segment m19 at 0.97)
- `b20` (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`) — 'The two do not agree, which points at query cost rather than at an undersized cluster.' is not in the merge and no disposition record explains it (nearest merge segment m34 at 0.45)
- `b21` (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`) — 'Proposed Actions' is not in the merge and no disposition record explains it (nearest merge segment m24 at 0.49)
- `b22` (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`) — '**Lower the slow query threshold**: set it to 1 second, so that the queries actually responsible are recorded instead of averaged away.' is not in the merge and no disposition record explains it (nearest merge segment m25 at 0.98)
- `b23` (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`) — '**Review what the queries are for**: go through the expensive ones with the team that wrote them, several of which look like they could ask for less.' is not in the merge and no disposition record explains it (nearest merge segment m26 at 0.99)
- `b24` (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`) — '**Capture evidence during a refusal**: while the refusal rate is high, take a thread dump and a heap snapshot rather than reasoning from counters alone.' is not in the merge and no disposition record explains it (nearest merge segment m27 at 0.99)
- `b26` (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`) — '{internal-notes}' is not in the merge and no disposition record explains it (nearest merge segment m40 at 0.38)
- `b28` (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`) — '{/internal-notes}' is not in the merge and no disposition record explains it (nearest merge segment m40 at 0.37)

### Verbatim violation — an invariant-core token did not survive unchanged

- `a8` (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md`) — code_block '```\nappend batch refused after 0 of 64 envelopes: 429 Too Many Requests: {"error":{"root_cause":[{"type":"nbl_queue_refused_exception","reason":"refused append on ingest path [ingest_and_leader_bytes=88121344, follower_bytes=212992, all_bytes=88334336, ingest_op_bytes=155648, max_ingest_bytes=88080384]"}],"type":"nbl_queue_refused_exception","reason":"refused append on ingest path [ingest_and_leader_bytes=88121344, follower_bytes=212992, all_bytes=88334336, ingest_op_bytes=155648, max_ingest_bytes=88080384]"},"status":429}\n```' does not survive into the merge unchanged
- `b2` (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`) — numeric '2026-04-11' does not survive into the merge unchanged
- `b4` (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`) — code '`429`' does not survive into the merge unchanged
- `b8` (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`) — numeric '4.4' does not survive into the merge unchanged
- `b13` (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`) — code '`429`' does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **2** departure(s) from its sources. Checking them confirms 2, rejects 0, and leaves 0 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | Base document's title was kept | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Nimbrel Ledger append rejected with HTTP 429' and says so (no claim traced to it) |
| `b13` | duplicate | a4 already states it | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-009`) |

## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | 1c859caa0f73 (hosted) |
| Fidelity | off |
| Title policy | keep-base |
| Base document | `source_a.md` (explicit) |
| Model (merge) | deepseek-r1:70b |
| Model (decompose) | deepseek-r1:70b |
| Model (verify) | deepseek-r1:70b |
| Structured output | json_schema (pinned), field order any |
| Decoding | temperature 0.0, seed 0, thinking decompose, merge, verify |
| claimcheck commit | 15dd9b3c3747 |
| Calls | 11 live, 0 cached, 0 replayed |
| Tokens | 29,716 in, 25,558 out |
| Schema repairs | 3 |
| Errors | 0 |
| Duration | 1417.5s |
| Generated | 2026-08-30T22:36:43+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `21ce9934e2ce` |
| Prompt | `prompts/verify.md` `54c88ce35a87` |
| Prompt | `prompts/verify_reverse.md` `7f655f15e201` |

> **Document content left this machine.** It was sent to the endpoint in `CLAIMCHECK_BASE_URL` (id `1c859caa0f73`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.
