## Verdict

**3 finding(s).** In the structure: 3 undeclared absence.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 36 |
| Claims extracted from `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 24 |
| Claims extracted from `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 25 |
| Forward — source claims accounted for in the merge | **49/49** |
| Forward — carried only in part | 0 |
| Forward — `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` claims accounted for | **24/24** |
| Forward — `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` claims accounted for | **25/25** |
| Reverse — merge claims found in a source | **36/36** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **78/85** |
| Units of work errored | 0 |

The model was shown `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` as `source_a.md`, `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` as `source_b.md`. Every filename in the findings below is the canonical one; the mapping above is how to read it. The names are fixed because the published figures were measured with them, and a prompt that varies with the caller's filenames is a prompt nothing was measured against.

## Findings

None in the claims. The 3 finding(s) this run reports are structural and are listed under `## Structure` below.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- 24 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 24 carried

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests`. | 8 | carried | 'Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests`.' in `merged.md` -- The reference text contains this exact sentence, matching the claim. |
| 2 | Nimbrel Relay stalls. | 8 | carried | 'Nimbrel Relay stalls' in `merged.md` -- The phrase appears verbatim in the description of the client‑side symptoms. |
| 3 | batch loaders resend the same envelope. | 8 | carried | 'batch loaders resend the same envelope' in `merged.md` -- The exact wording is present in the same sentence describing the failure. |
| 4 | reads against the same shard begin to time out. | 8 | carried | 'reads against the same shard begin to time out' in `merged.md` -- The reference text includes this phrase verbatim. |
| 5 | The refusal reaches the client. | 8 | carried | 'The refusal reaches the client' in `merged.md` -- The sentence states that the refusal reaches the client. |
| 6 | The refusal is written to the Relay and Collector logs as well. | 8 | carried | 'is written to the Relay and Collector logs as well' in `merged.md` -- The text explicitly says the refusal is written to those logs. |
| 7 | append batch refused after 0 of 64 envelopes: 429 Too Many Requests: {"error":{"root_cause":[{"type":"nbl_queue_refused_exception","reason":"refused append on ingest path [ingest_and_leader_bytes=88121344, follower_bytes=212992, all_bytes=88334336, ingest_op_bytes=155648, max_ingest_bytes=88080384]"}],"type":"nbl_queue_refused_exception","reason":"refused append on ingest path [ingest_and_leader_bytes=88121344, follower_bytes=212992, all_bytes=88334336, ingest_op_bytes=155648, max_ingest_bytes=88080384]"},"status":429} | 13 | carried | 'append batch refused after 0 of 64 envelopes: 429 Too Many Requests: {"error":{"root_cause":[{"type":"nbl_queue_refused_exception","reason":"refused append on ingest path [ingest_and_leader_bytes=88121344, follower_bytes=212992, all_bytes=88334336, ingest_op_bytes=155648, max_ingest_bytes=88080384]"}],"type":"nbl_queue_refused_exception","reason":"refused append on ingest path [ingest_and_leader_bytes=88121344, follower_bytes=212992, all_bytes=88334336, ingest_op_bytes=155648, max_ingest_bytes=88080384]"},"status":429}' in `merged.md` -- The code block contains the exact error line quoted in the claim. |
| 8 | Every Nimbrel Ledger release on every platform can refuse an append this way. | 20 | carried | 'Every Nimbrel Ledger release on every platform can refuse an append this way.' in `merged.md` -- The environment section states this sentence verbatim. |
| 9 | A `429 - Too Many Requests` reply is what a Ledger node sends once it has nowhere left to put the work, which is to say once an append queue or a read queue is full. | 24 (unverified) | carried | 'A [`429 - Too Many Requests` reply](https://docs.nimbrel.example/ledger/http-status-codes) is what a Ledger node sends once it has nowhere left to put the work, which is to say once [an append queue or a read queue is full](https://docs.nimbrel.example/ledger/why-appends-are-refused).' in `merged.md` -- The cause paragraph contains this exact description of the 429 reply. |
| 10 | There are 3 ways an append draws a 429: | 26 | carried | 'There are 3 ways an append draws a 429:' in `merged.md` -- The list introduction matches the claim word for word. |
| 11 | The `append` or `system_append` worker pools hold more batches than they have slots for (`nbctl pool status --all`) | 28 | carried | 'The `append` or `system_append` worker pools hold more batches than they have slots for (`nbctl pool status --all`)' in `merged.md` -- The bullet point lists this exact condition. |
| 12 | The ingest memory guard has refused the batch (`nbctl guard report ingest --counters`). | 29 | carried | 'The ingest memory guard has refused the batch (`nbctl guard report ingest --counters`).' in `merged.md` -- The text includes this sentence verbatim. |
| 13 | A circuit breaker has tripped (`nbctl breaker list --tripped`) | 30 | carried | 'A circuit breaker has tripped (`nbctl breaker list --tripped`)' in `merged.md` -- The bullet point contains this exact phrase. |
| 14 | A breaker trips on any operation and is not particular to appends. | 30 | carried | 'a breaker trips on any operation and is not particular to appends.' in `merged.md` -- The continuation of the bullet states this exactly. |
| 15 | **From release 4.6 and release 5.1 onward**, appending to a `wide_text` column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory. | 32 | carried | '**From release 4.6 and release 5.1 onward**, appending to a `wide_text` column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory.' in `merged.md` -- The footnote contains the claim verbatim. |
| 16 | Take append and query load off the cluster for long enough that the queues drain and the nodes fall back under their limits. | 36 | carried | 'Take append and query load off the cluster for long enough that the queues drain and the nodes fall back under their limits.' in `merged.md` -- The workaround paragraph includes this exact instruction. |
| 17 | A cluster that refuses appends has been given more work than its hardware can carry. | 42 | carried | 'A cluster that refuses appends has been given more work than its hardware can carry' in `merged.md` -- The resolution section states this sentence. |
| 18 | Splitting a hot stream over more leader shards spreads append load across more nodes. | 44 | carried | 'Splitting a hot stream over more leader shards spreads append load across more nodes' in `merged.md` -- The same paragraph contains this exact claim. |
| 19 | the `ingest_guard.memory.leader.ceiling` cluster setting defaults to 10% of the heap. | 50 | carried | 'the `ingest_guard.memory.leader.ceiling` cluster setting defaults to 10% of the heap.' in `merged.md`, **transcription_error** -- The resolution steps list this default verbatim. |
| 20 | A higher ceiling lets a node hold more in-flight append memory before refusing. | 50 | carried | 'A higher ceiling lets a node hold more in‑flight append memory before refusing' in `merged.md` -- The text includes this exact description of the higher ceiling effect. |
| 21 | a node holding too much runs out of memory instead of refusing. | 50 | carried | 'a node holding too much runs out of memory instead of refusing.' in `merged.md`, **transcription_error** -- The same sentence states this condition word for word. |
| 22 | The setting is read at startup. | 50 | carried | 'The setting is read at startup.' in `merged.md`, **transcription_error** -- The paragraph explicitly says the setting is read at startup. |
| 23 | the cluster must be restarted for a change to take. | 50 | carried | 'the cluster must be restarted for a change to take.' in `merged.md` -- The sentence contains this exact requirement. |
| 24 | Refusals that show up only during a spike usually clear on their own once the queues drain. | 52 | carried | 'Refusals that show up only during a spike usually clear on their own once the queues drain.' in `merged.md` -- The resolution includes this sentence verbatim. |

### `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` -- 25 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 25 carried

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | This note concerns a managed Nimbrel Ledger deployment (NMD) whose share of HTTP `429` replies climbed over a fortnight, as counted at the front proxy. | 8 | carried | 'This note concerns a managed Nimbrel Ledger deployment (NMD) whose share of HTTP `429` replies climbed over a fortnight, as counted at the front proxy.' in `merged.md` -- The issue description contains this exact statement. |
| 2 | It sets out what the evidence pointed at, which was expensive queries and deep grouping, and what was put forward in response. | 8 | carried | 'It sets out what the evidence pointed at, which was expensive queries and deep grouping, and what was put forward in response.' in `merged.md` -- The reference text contains the exact sentence stating the evidence pointed at expensive queries and deep grouping and the response. |
| 3 | Product: Nimbrel Ledger | 12 | carried | 'Product: Nimbrel Ledger' in `merged.md` -- The environment section lists the product as Nimbrel Ledger. |
| 4 | Version: 4.4, 5.x | 13 | carried | 'Version: 4.4, 5.x' in `merged.md` -- The version line in the environment section matches the claim. |
| 5 | Platform: Nimbrel Cloud | 14 | carried | 'Platform: Nimbrel Cloud' in `merged.md` -- The platform line in the environment section matches the claim. |
| 6 | Deployment: Managed Ledger Service (MLS) | 15 | carried | 'Deployment: Managed Ledger Service (MLS)' in `merged.md` -- The deployment line in the environment section matches the claim. |
| 7 | Production Environment: Yes | 16 | carried | 'Production Environment: Yes' in `merged.md` -- The production environment line in the environment section matches the claim. |
| 8 | The managed deployment returns HTTP `429` on a growing share of requests, which is what the Ledger does when it refuses work rather than queueing it. | 20 | carried | 'The managed deployment returns HTTP `429` on a growing share of requests, which is what the Ledger does when it refuses work rather than queueing it.' in `merged.md` -- The sentence directly states the managed deployment returns HTTP 429 and explains the Ledger’s behavior. |
| 9 | The Ledger returns HTTP `429` when it refuses work rather than queueing it. | 20 (unverified) | carried | 'which is what the Ledger does when it refuses work rather than queueing it' in `merged.md` -- The reference explains that the Ledger returns HTTP 429 when it refuses work rather than queueing it. |
| 10 | Front proxy counters agree with the client reports | 20 | carried | 'Front proxy counters agree with the client reports' in `merged.md` -- The issue description contains this exact statement. |
| 11 | the refusals are real | 20 | carried | 'the refusals are real' in `merged.md` -- The sentence states that the refusals are real. |
| 12 | the refusals are not a client-side accounting error | 20 (unverified) | carried | 'and not a client-side accounting error' in `merged.md` -- The same sentence clarifies the refusals are not a client‑side accounting error. |
| 13 | a handful of queries run for as long as 2 seconds each. | 24 | carried | 'a handful of queries run for as long as 2 seconds each.' in `merged.md` -- The cause section lists this exact description of expensive queries. |
| 14 | A worker slot is unavailable for as long as one of them holds it. | 24 (unverified) | carried | 'A worker slot is unavailable for as long as one of them holds it' in `merged.md` -- The cause section contains this statement about worker slot unavailability. |
| 15 | the queue behind it grows. | 24 | carried | 'and the queue behind it grows' in `merged.md` -- The same sentence continues with the queue growing. |
| 16 | grouping on `channel.id` yields a very large number of groups | 25 | carried | 'grouping on `channel.id` yields a very large number of groups' in `merged.md` -- The deep grouping bullet contains this exact phrase. |
| 17 | the memory that costs is charged to the same pool the append path draws on | 25 | carried | 'the memory that costs is charged to the same pool the append path draws on' in `merged.md` -- The same bullet explains the memory cost attribution. |
| 18 | processor load looks unremarkable while memory sits high. | 26 | carried | 'processor load looks unremarkable while memory sits high.' in `merged.md` -- The resource accounting bullet contains this exact observation. |
| 19 | The two do not agree, which points at query cost rather than at an undersized cluster. | 26 | carried | 'The two do not agree, which points at query cost rather than at an undersized cluster.' in `merged.md` -- The sentence directly matches the claim. |
| 20 | set it to 1 second | 30 | carried | 'set it to 1 second' in `merged.md` -- The proposed action to lower the slow query threshold includes this phrase. |
| 21 | the queries actually responsible are recorded instead of averaged away | 30 | carried | 'the queries actually responsible are recorded instead of averaged away' in `merged.md` -- The same action sentence contains this exact wording. |
| 22 | go through the expensive ones with the team that wrote them | 31 | carried | 'go through the expensive ones with the team that wrote them' in `merged.md` -- The review action bullet includes this exact instruction. |
| 23 | several of which look like they could ask for less. | 31 | carried | 'several of which look like they could ask for less.' in `merged.md` -- The same sentence continues with this observation. |
| 24 | the refusal rate is high | 32 | carried | 'the refusal rate is high' in `merged.md` -- The capture‑evidence action mentions the refusal rate being high. |
| 25 | take a thread dump and a heap snapshot rather than reasoning from counters alone. | 32 | carried | 'take a thread dump and a heap snapshot rather than reasoning from counters alone.' in `merged.md` -- The same action sentence contains this exact recommendation. |

### `merged.md` -- 36 claim(s): 0 invented, 0 contradicted, 0 supported in part, 36 supported

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests` | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests`' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The exact sentence appears in source_a.md, matching the claim. |
| 2 | The managed deployment returns HTTP `429` on a growing share of requests, which is what the Ledger does when it refuses work rather than queueing it | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 'The managed deployment returns HTTP `429` on a growing share of requests, which is what the Ledger does when it refuses work rather than queueing it' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` -- The claim is verbatim in source_b.md. |
| 3 | Front proxy counters agree with the client reports | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 'Front proxy counters agree with the client reports' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` -- Source_b.md contains this exact phrase. |
| 4 | The refusals are real and not a client-side accounting error | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 'the refusals are real and not a client-side accounting error' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` -- The sentence appears in source_b.md confirming the claim. |
| 5 | Callers see a write that will not land | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'Callers see a write that will not land' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The phrase is present in source_a.md. |
| 6 | Nimbrel Relay stalls | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'Nimbrel Relay stalls' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- Source_a.md includes this exact wording. |
| 7 | Batch loaders resend the same envelope | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'batch loaders resend the same envelope' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The claim matches a sentence in source_a.md. |
| 8 | Reads against the same shard begin to time out | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'reads against the same shard begin to time out' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The exact wording is found in source_a.md. |
| 9 | The refusal reaches the client | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'The refusal reaches the client' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- Source_a.md contains this exact statement. |
| 10 | The refusal is written to the Relay and Collector logs as well | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'and is written to the Relay and Collector logs as well' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The phrase appears in source_a.md confirming the claim. |
| 11 | This note concerns a managed Nimbrel Ledger deployment (NMD) whose share of HTTP `429` replies climbed over a fortnight, as counted at the front proxy | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 'This note concerns a managed Nimbrel Ledger deployment (NMD) whose share of HTTP `429` replies climbed over a fortnight, as counted at the front proxy' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` -- The sentence is verbatim in source_b.md. |
| 12 | The evidence pointed at expensive queries and deep grouping | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 'The evidence pointed at expensive queries and deep grouping' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`, **transcription_error** -- Source_b.md includes this exact phrase. |
| 13 | Every Nimbrel Ledger release on every platform can refuse an append this way | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'Every Nimbrel Ledger release on every platform can refuse an append this way' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The claim matches a line in source_a.md. |
| 14 | A `429 - Too Many Requests` reply is what a Ledger node sends once it has nowhere left to put the work | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'A `429 - Too Many Requests` reply is what a Ledger node sends once it has nowhere left to put the work' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md`, **transcription_error** -- The exact sentence is present in source_a.md. |
| 15 | An append queue or a read queue is full | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'an append queue or a read queue is full' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The phrase appears in source_a.md within a link. |
| 16 | There are 3 ways an append draws a 429 | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'There are 3 ways an append draws a 429' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- Source_a.md contains this exact wording. |
| 17 | A circuit breaker has tripped | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'A circuit breaker has tripped' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The claim is directly stated in source_a.md. |
| 18 | A breaker trips on any operation and is not particular to appends | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'A breaker trips on any operation and is not particular to appends' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The sentence appears verbatim in source_a.md. |
| 19 | From release 4.6 and release 5.1 onward, appending to a `wide_text` column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | '**From release 4.6 and release 5.1 onward**, appending to a `wide_text` column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The claim matches the bolded statement in source_a.md. |
| 20 | Expensive queries: a handful of queries run for as long as 2 seconds each | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | '**Expensive queries**: a handful of queries run for as long as 2 seconds each' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` -- Source_b.md includes this exact bullet point. |
| 21 | A worker slot is unavailable for as long as one of them holds it | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 'A worker slot is unavailable for as long as one of them holds it' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` -- The phrase is present verbatim in source_b.md. |
| 22 | The queue behind it grows | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 'and the queue behind it grows' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` -- The clause appears in source_b.md. |
| 23 | Grouping on `channel.id` yields a very large number of groups | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 'grouping on `channel.id` yields a very large number of groups' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` -- The exact wording is found in source_b.md. |
| 24 | The memory that costs is charged to the same pool the append path draws on | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 'and the memory that costs is charged to the same pool the append path draws on' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` -- Source_b.md contains this sentence verbatim. |
| 25 | Processor load looks unremarkable | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 'processor load looks unremarkable' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` -- The phrase appears in source_b.md. |
| 26 | Memory sits high | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 'memory sits high' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` -- The source document states that memory sits high, directly matching the claim. |
| 27 | The two do not agree | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 'The two do not agree' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` -- The source explicitly says "The two do not agree", which is the claim. |
| 28 | A cluster that refuses appends has been given more work than its hardware can carry | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'A cluster that refuses appends has been given more work than its hardware can carry' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The source contains this exact sentence, confirming the claim. |
| 29 | Splitting a hot stream over more leader shards spreads append load across more nodes | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'Splitting a hot stream over more leader shards spreads append load across more nodes' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The source states this sentence verbatim, supporting the claim. |
| 30 | `ingest_guard.memory.leader.ceiling` cluster setting defaults to 10% of the heap | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'Only then raise the `ingest_guard.memory.leader.ceiling` cluster setting, which defaults to 10% of the heap' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The source indicates the setting defaults to 10% of the heap, matching the claim. |
| 31 | A higher ceiling lets a node hold more in‑flight append memory before refusing | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'A higher ceiling lets a node hold more in‑flight append memory before refusing' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md`, **transcription_error** -- The source contains this exact wording, confirming the claim. |
| 32 | A node holding too much runs out of memory instead of refusing | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'a node holding too much runs out of memory instead of refusing' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The source states this sentence (case difference only), which matches the claim. |
| 33 | The setting is read at startup | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'The setting is read at startup' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The source explicitly says the setting is read at startup. |
| 34 | The cluster must be restarted for a change to take | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'so the cluster must be restarted for a change to take' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The source includes this clause, confirming the claim. |
| 35 | Refusals that show up only during a spike usually clear on their own once the queues drain | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'Refusals that show up only during a spike usually clear on their own once the queues drain' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The source contains this exact sentence, supporting the claim. |
| 36 | The slow query threshold is set to 1 second | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 'Lower the slow query threshold: set it to 1 second' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`, **transcription_error** -- The source states that the slow query threshold is set to 1 second. |

## Structure

**9** mechanical check(s) over **63** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.

Ordering: 10 run(s) over 54 attributed segment(s) — sources interleaved. 10 of 13 source heading(s) survive. This is a measurement, not a finding: a concatenation is the correct merge when the sources share no subject.

### Absent and undeclared — in a source, not in the merge, and no record explains it

- `a30` (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md`) — 'A higher ceiling lets a node hold more in-flight append memory before refusing, and a node holding too much runs out of memory instead of refusing, which is the worse outcome.' is not in the merge and no disposition record explains it (nearest merge segment m44 at 0.99)
- `b3` (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`) — 'Summary / Table of Contents' is not in the merge and no disposition record explains it (nearest merge segment m52 at 0.32)
- `b15` (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`) — 'Contributing Factors' is not in the merge and no disposition record explains it (nearest merge segment m48 at 0.39)

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **3** departure(s) from its sources. Checking them confirms 3, rejects 0, and leaves 0 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | title slot kept base title | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Nimbrel Ledger append rejected with HTTP 429' and says so (no claim traced to it) |
| `b12` | duplicate | duplicate Issue Description heading | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b6` | duplicate | duplicate Environment heading | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |

## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | 29d412c5e668 (hosted) |
| Fidelity | off |
| Title policy | keep-base |
| Base document | `source_a.md` (explicit) |
| Model (merge) | gpt-oss:120b |
| Model (decompose) | gpt-oss:120b |
| Model (verify) | gpt-oss:120b |
| Structured output | json_schema (pinned) |
| Decoding | temperature 0.0, seed 0, thinking decompose, merge, verify |
| claimcheck commit | ee9e03043716 |
| Calls | 8 live, 0 cached, 0 replayed |
| Tokens | 50,008 in, 13,140 out |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 451.8s |
| Generated | 2026-08-31T07:19:57+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `21ce9934e2ce` |
| Prompt | `prompts/verify.md` `54c88ce35a87` |
| Prompt | `prompts/verify_reverse.md` `7f655f15e201` |

> **Document content left this machine.** It was sent to the endpoint in `CLAIMCHECK_BASE_URL` (id `29d412c5e668`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.
