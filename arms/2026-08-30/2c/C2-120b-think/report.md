## Verdict

**5 finding(s).** In the claims: 1 hallucinated. In the structure: 3 undeclared absence, 1 verbatim violation.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 49 |
| Claims extracted from `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 25 |
| Claims extracted from `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 29 |
| Forward — source claims accounted for in the merge | **54/54** |
| Forward — carried only in part | 0 |
| Forward — `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` claims accounted for | **25/25** |
| Forward — `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` claims accounted for | **29/29** |
| Reverse — merge claims found in a source | **48/49** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **100/102** |
| Units of work errored | 0 |

The model was shown `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` as `source_a.md`, `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` as `source_b.md`. Every filename in the findings below is the canonical one; the mapping above is how to read it. The names are fixed because the published figures were measured with them, and a prompt that varies with the caller's filenames is a prompt nothing was measured against.

## Findings

### Invented — in the merge, in neither source

- **M-014** (`merged.md:14`) — which was expensive queries and deep grouping
  - rationale: No source contains the exact phrase "which was expensive queries and deep grouping".

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- 25 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 25 carried

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests`. | 8 | carried | 'Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests`.' in `merged.md` -- The reference text contains this exact sentence, confirming the claim. |
| 2 | Callers see a write that will not land: Nimbrel Relay stalls, batch loaders resend the same envelope, and reads against the same shard begin to time out. | 8 | carried | 'Callers see a write that will not land: Nimbrel Relay stalls, batch loaders resend the same envelope, and reads against the same shard begin to time out.' in `merged.md` -- The sentence appears verbatim in the Issue Description, supporting the claim. |
| 3 | The refusal reaches the client and is written to the Relay and Collector logs as well. | 8 | carried | 'The refusal reaches the client and is written to the Relay and Collector logs as well.' in `merged.md` -- The reference text states this exact sentence, so the claim is supported. |
| 4 | A full refusal envelope from a batched append reads like this: | 10 | carried | 'A full refusal envelope from a batched append reads like this:' in `merged.md` -- The same wording is present in the document, confirming the claim. |
| 5 | append batch refused after 0 of 64 envelopes: 429 Too Many Requests: {"error":{"root_cause":[{"type":"nbl_queue_refused_exception","reason":"refused append on ingest path [ingest_and_leader_bytes=88121344, follower_bytes=212992, all_bytes=88334336, ingest_op_bytes=155648, max_ingest_bytes=88080384]"}],"type":"nbl_queue_refused_exception","reason":"refused append on ingest path [ingest_and_leader_bytes=88121344, follower_bytes=212992, all_bytes=88334336, ingest_op_bytes=155648, max_ingest_bytes=88080384]"},"status":429} | 13 | carried | 'append batch refused after 0 of 64 envelopes: 429 Too Many Requests: {"error":{"root_cause":[{"type":"nbl_queue_refused_exception","reason":"refused append on ingest path [ingest_and_leader_bytes=88121344, follower_bytes=212992, all_bytes=88334336, ingest_op_bytes=155648, max_ingest_bytes=88080384]"}],"type":"nbl_queue_refused_exception","reason":"refused append on ingest path [ingest_and_leader_bytes=88121344, follower_bytes=212992, all_bytes=88334336, ingest_op_bytes=155648, max_ingest_bytes=88080384]"},"status":429}' in `merged.md` -- The code block contains this exact refusal envelope line, matching the claim. |
| 6 | The Ledger operations handbook now covers the same ground under Refused Appends, with a walkthrough for each of the three refusal paths set out below. | 16 | carried | 'The Ledger operations handbook now covers the same ground under Refused Appends, with a walkthrough for each of the three refusal paths set out below.' in `merged.md` -- The sentence appears in the note, matching the claim's wording. |
| 7 | Every Nimbrel Ledger release on every platform can refuse an append this way. | 20 | carried | 'Every Nimbrel Ledger release on every platform can refuse an append this way.' in `merged.md` -- The claim is verbatim in the Environment list, so it is supported. |
| 8 | A `429 - Too Many Requests` reply (https://docs.nimbrel.example/ledger/http-status-codes) is what a Ledger node sends once it has nowhere left to put the work, which is to say once [an append queue or a read queue is full](https://docs.nimbrel.example/ledger/why-appends-are-refused). | 24 (unverified) | carried | 'A [`429 - Too Many Requests` reply](https://docs.nimbrel.example/ledger/http-status-codes) is what a Ledger node sends once it has nowhere left to put the work, which is to say once [an append queue or a read queue is full](https://docs.nimbrel.example/ledger/why-appends-are-refused).' in `merged.md` -- The reference sentence conveys the same meaning as the claim, despite minor formatting differences. |
| 9 | There are 3 ways an append draws a 429: | 26 | carried | 'There are 3 ways an append draws a 429:' in `merged.md` -- The exact phrase is present in the Cause section, confirming the claim. |
| 10 | - The `append` or `system_append` worker pools hold more batches than they have slots for (`nbctl pool status --all`) | 28 | carried | '- The `append` or `system_append` worker pools hold more batches than they have slots for (`nbctl pool status --all`)' in `merged.md` -- The bullet point matches the claim word for word. |
| 11 | - The ingest memory guard has refused the batch (`nbctl guard report ingest --counters`). [1] | 29 | carried | '- The ingest memory guard has refused the batch (`nbctl guard report ingest --counters`). [1]' in `merged.md` -- The list entry is identical to the claim, so it is supported. |
| 12 | - A circuit breaker has tripped (`nbctl breaker list --tripped`) - a breaker trips on any operation and is not particular to appends. | 30 | carried | '- A circuit breaker has tripped (`nbctl breaker list --tripped`) - a breaker trips on any operation and is not particular to appends.' in `merged.md` -- The sentence appears exactly as claimed, providing support. |
| 13 | [1] **From release 4.6 and release 5.1 onward**, appending to a `wide_text` column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory. | 32 | carried | '[1] **From release 4.6 and release 5.1 onward**, appending to a `wide_text` column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory.' in `merged.md` -- The footnote contains the same wording, confirming the claim. |
| 14 | Take append and query load off the cluster for long enough that the queues drain and the nodes fall back under their limits. | 36 | carried | 'Take append and query load off the cluster for long enough that the queues drain and the nodes fall back under their limits.' in `merged.md` -- The Workaround section includes this exact recommendation. |
| 15 | Where batches carry `wide_text` columns and the cluster runs release 4.6 or release 5.1 or later, send fewer envelopes per batch. | 38 | carried | '- Where batches carry `wide_text` columns and the cluster runs release 4.6 or release 5.1 or later, send fewer envelopes per batch.' in `merged.md`, **transcription_error** -- The bullet matches the claim verbatim. |
| 16 | A cluster that refuses appends has been given more work than its hardware can carry, so the answer is hardware: larger nodes (scale up), or more of them (scale out). | 42 | carried | 'A cluster that refuses appends has been given more work than its hardware can carry, so the answer is hardware: larger nodes (scale up), or more of them (scale out).' in `merged.md` -- The Resolution paragraph states this sentence exactly. |
| 17 | Scale up first in most cases, and scale out when what is wanted is a further copy of the data for availability, per [the sizing notes](https://docs.nimbrel.example/ledger/sizing). | 42 | carried | 'Scale up first in most cases, and scale out when what is wanted is a further copy of the data for availability, per [the sizing notes](https://docs.nimbrel.example/ledger/sizing).' in `merged.md` -- The claim matches the sentence in the Resolution section. |
| 18 | Splitting a hot stream over more leader shards spreads append load across more nodes, which helps in some layouts. | 44 | carried | 'Splitting a hot stream over more leader shards spreads append load across more nodes, which helps in some layouts.' in `merged.md` -- The same wording appears in the Resolution, supporting the claim. |
| 19 | 1. Begin by cutting the number of envelopes in each append batch. | 48 | carried | '1. Begin by cutting the number of envelopes in each append batch.' in `merged.md` -- The numbered step is identical to the claim. |
| 20 | 2. Where smaller batches do not clear it, add processor and memory capacity to the nodes. | 49 | carried | '2. Where smaller batches do not clear it, add processor and memory capacity to the nodes.' in `merged.md` -- The second step matches the claim exactly. |
| 21 | 3. Only then raise the `ingest_guard.memory.leader.ceiling` cluster setting, which defaults to 10% of the heap. | 50 | carried | '3. Only then raise the `ingest_guard.memory.leader.ceiling` cluster setting, which defaults to 10% of the heap.' in `merged.md` -- The third step is verbatim in the document. |
| 22 | A higher ceiling lets a node hold more in-flight append memory before refusing, and a node holding too much runs out of memory instead of refusing, which is the worse outcome. | 50 | carried | 'A higher ceiling lets a node hold more in-flight append memory before refusing, and a node holding too much runs out of memory instead of refusing, which is the worse outcome.' in `merged.md` -- The sentence appears unchanged in the Resolution, confirming the claim. |
| 23 | The setting is read at startup, so the cluster must be restarted for a change to take. | 50 | carried | 'The setting is read at startup, so the cluster must be restarted for a change to take.' in `merged.md` -- The reference text contains this exact statement. |
| 24 | Where none of that is open to you, the load itself is what changes: fewer appends, cheaper queries, or both. | 52 | carried | 'Where none of that is open to you, the load itself is what changes: fewer appends, cheaper queries, or both.' in `merged.md` -- The claim matches the sentence in the Resolution. |
| 25 | Refusals that show up only during a spike usually clear on their own once the queues drain. | 52 | carried | 'Refusals that show up only during a spike usually clear on their own once the queues drain.' in `merged.md` -- The final sentence of the Resolution is identical to the claim. |

### `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` -- 29 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 29 carried

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | This note concerns a managed Nimbrel Ledger deployment (NMD) | 8 | carried | 'This note concerns a managed Nimbrel Ledger deployment (NMD)' in `merged.md` -- The reference text contains the exact phrase, so the claim is supported. |
| 2 | share of HTTP `429` replies climbed over a fortnight, as counted at the front proxy | 8 | carried | 'share of HTTP `429` replies climbed over a fortnight, as counted at the front proxy' in `merged.md` -- The reference text contains the exact phrase, so the claim is supported. |
| 3 | Product: Nimbrel Ledger | 12 | carried | 'Product: Nimbrel Ledger' in `merged.md` -- The reference text contains the exact phrase, so the claim is supported. |
| 4 | Version: 4.4, 5.x | 13 | carried | 'Version: 4.4, 5.x' in `merged.md` -- The reference text contains the exact phrase, so the claim is supported. |
| 5 | Platform: Nimbrel Cloud | 14 | carried | 'Platform: Nimbrel Cloud' in `merged.md` -- The reference text contains the exact phrase, so the claim is supported. |
| 6 | Deployment: Managed Ledger Service (MLS) | 15 | carried | 'Deployment: Managed Ledger Service (MLS)' in `merged.md` -- The reference text contains the exact phrase, so the claim is supported. |
| 7 | Production Environment: Yes | 16 | carried | 'Production Environment: Yes' in `merged.md` -- The reference text contains the exact phrase, so the claim is supported. |
| 8 | The managed deployment returns HTTP `429` on a growing share of requests | 20 | carried | 'The managed deployment returns HTTP `429` on a growing share of requests' in `merged.md` -- The reference text contains the exact phrase, so the claim is supported. |
| 9 | which is what the Ledger does when it refuses work rather than queueing it | 20 | carried | 'which is what the Ledger does when it refuses work rather than queueing it' in `merged.md` -- The reference text contains the exact phrase, so the claim is supported. |
| 10 | Front proxy counters agree with the client reports | 20 | carried | 'Front proxy counters agree with the client reports' in `merged.md` -- The reference text contains the exact phrase, so the claim is supported. |
| 11 | the refusals are real and not a client-side accounting error | 20 | carried | 'the refusals are real and not a client-side accounting error' in `merged.md` -- The reference text contains the exact phrase, so the claim is supported. |
| 12 | a handful of queries run for as long as 2 seconds each | 24 | carried | 'a handful of queries run for as long as 2 seconds each' in `merged.md` -- The reference text contains the exact phrase, so the claim is supported. |
| 13 | A worker slot is unavailable for as long as one of them holds it | 24 | carried | 'A worker slot is unavailable for as long as one of them holds it' in `merged.md` -- The reference text contains the exact phrase, so the claim is supported. |
| 14 | the queue behind it grows | 24 | carried | 'the queue behind it grows' in `merged.md` -- The reference text contains the exact phrase, so the claim is supported. |
| 15 | grouping on `channel.id` yields a very large number of groups | 25 | carried | 'grouping on `channel.id` yields a very large number of groups' in `merged.md` -- The reference text contains the exact phrase, so the claim is supported. |
| 16 | the memory that costs is charged to the same pool the append path draws on | 25 | carried | 'the memory that costs is charged to the same pool the append path draws on' in `merged.md` -- The reference text contains the exact phrase, so the claim is supported. |
| 17 | processor load looks unremarkable | 26 | carried | 'processor load looks unremarkable' in `merged.md` -- The reference text contains the exact phrase, so the claim is supported. |
| 18 | memory sits high | 26 | carried | 'memory sits high' in `merged.md` -- The reference text contains the exact phrase, so the claim is supported. |
| 19 | The two do not agree | 26 | carried | 'The two do not agree' in `merged.md` -- The reference text contains the exact phrase, so the claim is supported. |
| 20 | which points at query cost rather than at an undersized cluster | 26 | carried | 'which points at query cost rather than at an undersized cluster' in `merged.md` -- The reference text contains the exact phrase, so the claim is supported. |
| 21 | set it to 1 second | 30 | carried | 'set it to 1 second' in `merged.md` -- The reference text contains the exact phrase, so the claim is supported. |
| 22 | the queries actually responsible are recorded instead of averaged away | 30 | carried | 'the queries actually responsible are recorded instead of averaged away' in `merged.md` -- The reference text contains the exact phrase, so the claim is supported. |
| 23 | go through the expensive ones with the team that wrote them | 31 | carried | 'go through the expensive ones with the team that wrote them' in `merged.md` -- The reference text contains the exact phrase, so the claim is supported. |
| 24 | several of which look like they could ask for less | 31 | carried | 'several of which look like they could ask for less' in `merged.md` -- The reference text contains the exact phrase, so the claim is supported. |
| 25 | the refusal rate is high | 32 | carried | 'the refusal rate is high' in `merged.md` -- The reference text contains the exact phrase, so the claim is supported. |
| 26 | take a thread dump and a heap snapshot rather than reasoning from counters alone | 32 | carried | 'take a thread dump and a heap snapshot rather than reasoning from counters alone' in `merged.md` -- The reference text explicitly advises to take a thread dump and a heap snapshot rather than reasoning from counters alone. |
| 27 | Internal ticket NB-40917 | 38 | carried | '[Internal ticket NB-40917](https://tickets.nimbrel.example/issues/40917)' in `merged.md` -- The reference text lists an internal ticket NB-40917 in the References section. |
| 28 | Ledger slow query log | 42 | carried | '[Ledger slow query log](https://docs.nimbrel.example/ledger/slow-query-log)' in `merged.md` -- The reference text includes a reference entry titled Ledger slow query log. |
| 29 | HTTP 429 replies | 43 | carried | '[HTTP 429 replies](https://support.nimbrel.example/knowledge/318kqp2)' in `merged.md` -- The reference text contains a reference entry named HTTP 429 replies. |

### `merged.md` -- 49 claim(s): 1 invented, 0 contradicted, 0 supported in part, 48 supported

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 14 | which was expensive queries and deep grouping | invented | -- | No source contains the exact phrase "which was expensive queries and deep grouping". |
| 1 | Author: Priya Raghunathan | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'Author: Priya Raghunathan' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The author line appears exactly in source_a. |
| 2 | Updated: 2026-03-18 | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'Updated: 2026-03-18' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The updated date matches the line in source_a. |
| 3 | Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests` | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests`.' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The sentence is present verbatim in source_a. |
| 4 | Callers see a write that will not land | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'Callers see a write that will not land:' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The phrase appears exactly in source_a. |
| 5 | Nimbrel Relay stalls | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'Nimbrel Relay stalls' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The clause is stated verbatim in source_a. |
| 6 | batch loaders resend the same envelope | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'batch loaders resend the same envelope' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The exact wording is found in source_a. |
| 7 | reads against the same shard begin to time out | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'reads against the same shard begin to time out' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The sentence is present in source_a. |
| 8 | The refusal reaches the client | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'The refusal reaches the client' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The claim matches the line in source_a. |
| 9 | The refusal is written to the Relay and Collector logs as well | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'and is written to the Relay and Collector logs as well' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The phrase appears in source_a with the same meaning. |
| 10 | A full refusal envelope from a batched append reads like this | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'A full refusal envelope from a batched append reads like this:' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The sentence is exactly in source_a. |
| 11 | append batch refused after 0 of 64 envelopes: 429 Too Many Requests: {"error":{"root_cause":[{"type":"nbl_queue_refused_exception","reason":"refused append on ingest path [ingest_and_leader_bytes=88121344, follower_bytes=212992, all_bytes=88334336, ingest_op_bytes=155648, max_ingest_bytes=88080384]"}],"type":"nbl_queue_refused_exception","reason":"refused append on ingest path [ingest_and_leader_bytes=88121344, follower_bytes=212992, all_bytes=88334336, ingest_op_bytes=155648, max_ingest_bytes=88080384]"},"status":429} | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'append batch refused after 0 of 64 envelopes: 429 Too Many Requests: {"error":{"root_cause":[{"type":"nbl_queue_refused_exception","reason":"refused append on ingest path [ingest_and_leader_bytes=88121344, follower_bytes=212992, all_bytes=88334336, ingest_op_bytes=155648, max_ingest_bytes=88080384]"}],"type":"nbl_queue_refused_exception","reason":"refused append on ingest path [ingest_and_leader_bytes=88121344, follower_bytes=212992, all_bytes=88334336, ingest_op_bytes=155648, max_ingest_bytes=88080384]"},"status":429}' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The envelope line is reproduced verbatim in source_a. |
| 12 | The Ledger operations handbook now covers the same ground under Refused Appends, with a walkthrough for each of the three refusal paths set out below | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'The Ledger operations handbook now covers the same ground under Refused Appends, with a walkthrough for each of the three refusal paths set out below' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The statement is present in source_a. |
| 13 | This note concerns a managed Nimbrel Ledger deployment (NMD) whose share of HTTP `429` replies climbed over a fortnight, as counted at the front proxy | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 'This note concerns a managed Nimbrel Ledger deployment (NMD) whose share of HTTP `429` replies climbed over a fortnight, as counted at the front proxy' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` -- The sentence appears exactly in source_b. |
| 15 | The managed deployment returns HTTP `429` on a growing share of requests | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 'The managed deployment returns HTTP `429` on a growing share of requests' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` -- The claim matches a line in source_b. |
| 16 | which is what the Ledger does when it refuses work rather than queueing it | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 'which is what the Ledger does when it refuses work rather than queueing it' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` -- The exact wording is found in source_b. |
| 17 | Front proxy counters agree with the client reports | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 'Front proxy counters agree with the client reports' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` -- The sentence appears verbatim in source_b. |
| 18 | the refusals are real and not a client-side accounting error | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 'the refusals are real and not a client-side accounting error' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` -- The phrase is present in source_b. |
| 19 | Every Nimbrel Ledger release on every platform can refuse an append this way | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'Every Nimbrel Ledger release on every platform can refuse an append this way' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The claim is stated exactly in source_a. |
| 20 | Product: Nimbrel Ledger | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 'Product: Nimbrel Ledger' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` -- The line appears in source_b. |
| 21 | Version: 4.4, 5.x | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 'Version: 4.4, 5.x' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` -- The version line is present in source_b. |
| 22 | Platform: Nimbrel Cloud | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 'Platform: Nimbrel Cloud' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` -- The platform line matches source_b. |
| 23 | Deployment: Managed Ledger Service (MLS) | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 'Deployment: Managed Ledger Service (MLS)' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` -- The deployment line is verbatim in source_b. |
| 24 | Production Environment: Yes | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 'Production Environment: Yes' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` -- The production environment line appears in source_b. |
| 25 | A [`429 - Too Many Requests` reply](https://docs.nimbrel.example/ledger/http-status-codes) is what a Ledger node sends once it has nowhere left to put the work | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'A [`429 - Too Many Requests` reply](https://docs.nimbrel.example/ledger/http-status-codes) is what a Ledger node sends once it has nowhere left to put the work' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The statement is present in source_a. |
| 26 | an append queue or a read queue is full | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'an append queue or a read queue is full' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The phrase appears in source_a describing when a 429 is returned. |
| 27 | There are 3 ways an append draws a 429 | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'There are 3 ways an append draws a 429:' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- Source_a lists exactly three ways an append can draw a 429. |
| 28 | The `append` or `system_append` worker pools hold more batches than they have slots for (`nbctl pool status --all`) | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | '- The `append` or `system_append` worker pools hold more batches than they have slots for (`nbctl pool status --all`)' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The bullet in source_a states this condition for the worker pools. |
| 29 | The ingest memory guard has refused the batch (`nbctl guard report ingest --counters`) | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | '- The ingest memory guard has refused the batch (`nbctl guard report ingest --counters`). [1]' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- Source_a includes this exact statement about the ingest memory guard. |
| 30 | A circuit breaker has tripped (`nbctl breaker list --tripped`) | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | '- A circuit breaker has tripped (`nbctl breaker list --tripped`) - a breaker trips on any operation and is not particular to appends.' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The bullet in source_a mentions a circuit breaker tripping with the given command. |
| 31 | a breaker trips on any operation and is not particular to appends | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | '- A circuit breaker has tripped (`nbctl breaker list --tripped`) - a breaker trips on any operation and is not particular to appends.' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The same bullet explains that a breaker trips on any operation and is not specific to appends. |
| 32 | From release 4.6 and release 5.1 onward, appending to a `wide_text` column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | '**From release 4.6 and release 5.1 onward**, appending to a `wide_text` column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory.' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The footnote in source_a contains this exact description. |
| 33 | A handful of queries run for as long as 2 seconds each | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | '- **Expensive queries**: a handful of queries run for as long as 2 seconds each.' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` -- Source_b lists expensive queries lasting up to two seconds. |
| 34 | A worker slot is unavailable for as long as one of them holds it | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 'A worker slot is unavailable for as long as one of them holds it' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` -- The same bullet in source_b states this about worker slots. |
| 35 | the queue behind it grows | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 'and the queue behind it grows.' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` -- The bullet continues with this phrase describing the queue. |
| 36 | grouping on `channel.id` yields a very large number of groups | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 'grouping on `channel.id` yields a very large number of groups' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` -- Source_b's deep grouping bullet contains this exact wording. |
| 37 | the memory that costs is charged to the same pool the append path draws on | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 'and the memory that costs is charged to the same pool the append path draws on' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` -- The same bullet explains the memory cost attribution. |
| 38 | processor load looks unremarkable | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 'processor load looks unremarkable' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` -- Source_b's resource accounting bullet includes this phrase. |
| 39 | memory sits high | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 'memory sits high' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` -- The same bullet mentions memory sitting high. |
| 40 | The two do not agree, which points at query cost rather than at an undersized cluster | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 'The two do not agree, which points at query cost rather than at an undersized cluster.' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` -- Source_b directly states this conclusion about the two metrics. |
| 41 | A cluster that refuses appends has been given more work than its hardware can carry | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'A cluster that refuses appends has been given more work than its hardware can carry' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- The resolution section of source_a contains this statement. |
| 42 | Splitting a hot stream over more leader shards spreads append load across more nodes | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'Splitting a hot stream over more leader shards spreads append load across more nodes' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- Source_a mentions this as a mitigation technique. |
| 43 | The `ingest_guard.memory.leader.ceiling` cluster setting defaults to 10% of the heap | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'the `ingest_guard.memory.leader.ceiling` cluster setting, which defaults to 10% of the heap.' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- Source_a specifies the default of the ingest_guard setting. |
| 44 | A higher ceiling lets a node hold more in-flight append memory before refusing | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'A higher ceiling lets a node hold more in‑flight append memory before refusing' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md`, **transcription_error** -- Source_a explains the effect of raising the ceiling. |
| 45 | a node holding too much runs out of memory instead of refusing, which is the worse outcome | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'a node holding too much runs out of memory instead of refusing, which is the worse outcome' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- Source_a warns about nodes running out of memory. |
| 46 | The setting is read at startup | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'The setting is read at startup' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- Source_a notes that the setting is read at startup. |
| 47 | the cluster must be restarted for a change to take | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'the cluster must be restarted for a change to take' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- Source_a states that a restart is required for changes. |
| 48 | Refusals that show up only during a spike usually clear on their own once the queues drain | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` | 'Refusals that show up only during a spike usually clear on their own once the queues drain' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_a.md` -- Source_a describes this typical behavior of refusals. |
| 49 | Internal ticket NB-40917 | supported | `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` | 'Internal ticket NB-40917' in `<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md` -- Source_b references the internal ticket with that identifier. |

## Structure

**9** mechanical check(s) over **63** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.

Ordering: 10 run(s) over 53 attributed segment(s) — sources interleaved. 9 of 13 source heading(s) survive. This is a measurement, not a finding: a concatenation is the correct merge when the sources share no subject.

### Absent and undeclared — in a source, not in the merge, and no record explains it

- `b3` (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`) — 'Summary / Table of Contents' is not in the merge and no disposition record explains it (nearest merge segment m51 at 0.32)
- `b15` (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`) — 'Contributing Factors' is not in the merge and no disposition record explains it (nearest merge segment m39 at 0.33)
- `b21` (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`) — 'Proposed Actions' is not in the merge and no disposition record explains it (nearest merge segment m20 at 0.47)

### Verbatim violation — an invariant-core token did not survive unchanged

- `b2` (`<home>/Documents/Dev/vibe-coding/claimcheck/tests/pairs/index_429/source_b.md`) — numeric '2026-04-11' does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **2** departure(s) from its sources. Checking them confirms 1, rejects 0, and leaves 1 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | title superseded by base title | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Nimbrel Ledger append rejected with HTTP 429' and says so (no claim traced to it) |
| `b2` | superseded | author superseded by base author line | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |

## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | 5cefcb5c2a07 (hosted) |
| Fidelity | off |
| Title policy | keep-base |
| Base document | `source_a.md` (explicit) |
| Model (merge) | gpt-oss:120b |
| Model (decompose) | gpt-oss:120b |
| Model (verify) | gpt-oss:120b |
| Structured output | json_schema (pinned) |
| Decoding | temperature 0.0, seed 0, thinking decompose, merge, verify |
| claimcheck commit | 77358445a77c |
| Calls | 9 live, 0 cached, 0 replayed |
| Tokens | 51,120 in, 15,682 out |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 470.8s |
| Generated | 2026-08-30T16:53:37+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `21ce9934e2ce` |
| Prompt | `prompts/verify.md` `54c88ce35a87` |
| Prompt | `prompts/verify_reverse.md` `7f655f15e201` |

> **Document content left this machine.** It was sent to the endpoint in `CLAIMCHECK_BASE_URL` (id `5cefcb5c2a07`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.
