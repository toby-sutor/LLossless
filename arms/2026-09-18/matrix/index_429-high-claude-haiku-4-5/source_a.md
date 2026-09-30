# Nimbrel Ledger append rejected with HTTP 429

Author: Priya Raghunathan
Updated: 2026-03-18

### Issue Description

Append requests to Nimbrel Ledger come back with HTTP 429 `Too Many Requests`. Callers see a write that will not land: Nimbrel Relay stalls, batch loaders resend the same envelope, and reads against the same shard begin to time out. The refusal reaches the client and is written to the Relay and Collector logs as well.

A full refusal envelope from a batched append reads like this:

```
append batch refused after 0 of 64 envelopes: 429 Too Many Requests: {"error":{"root_cause":[{"type":"nbl_queue_refused_exception","reason":"refused append on ingest path [ingest_and_leader_bytes=88121344, follower_bytes=212992, all_bytes=88334336, ingest_op_bytes=155648, max_ingest_bytes=88080384]"}],"type":"nbl_queue_refused_exception","reason":"refused append on ingest path [ingest_and_leader_bytes=88121344, follower_bytes=212992, all_bytes=88334336, ingest_op_bytes=155648, max_ingest_bytes=88080384]"},"status":429}
```

> **NOTE:** The Ledger operations handbook now covers the same ground under Refused Appends, with a walkthrough for each of the three refusal paths set out below.

### Environment

Every Nimbrel Ledger release on every platform can refuse an append this way.

### Cause

A [`429 - Too Many Requests` reply](https://docs.nimbrel.example/ledger/http-status-codes) is what a Ledger node sends once it has nowhere left to put the work, which is to say once [an append queue or a read queue is full](https://docs.nimbrel.example/ledger/why-appends-are-refused).

There are 3 ways an append draws a 429:

- The `append` or `system_append` worker pools hold more batches than they have slots for (`nbctl pool status --all`)
- The ingest memory guard has refused the batch (`nbctl guard report ingest --counters`). [1]
- A circuit breaker has tripped (`nbctl breaker list --tripped`) - a breaker trips on any operation and is not particular to appends.

[1] **From release 4.6 and release 5.1 onward**, appending to a `wide_text` column draws a 429 on its own account whenever the batch would otherwise have run the node out of memory.

### Workaround

Take append and query load off the cluster for long enough that the queues drain and the nodes fall back under their limits.

Where batches carry `wide_text` columns and the cluster runs release 4.6 or release 5.1 or later, send fewer envelopes per batch.

### Resolution

A cluster that refuses appends has been given more work than its hardware can carry, so the answer is hardware: larger nodes (scale up), or more of them (scale out). Scale up first in most cases, and scale out when what is wanted is a further copy of the data for availability, per [the sizing notes](https://docs.nimbrel.example/ledger/sizing).

Splitting a hot stream over more leader shards spreads append load across more nodes, which helps in some layouts.

For `wide_text` columns on release 4.6 and release 5.1 and later:

1. Begin by cutting the number of envelopes in each append batch.
2. Where smaller batches do not clear it, add processor and memory capacity to the nodes.
3. Only then raise the `ingest_guard.memory.leader.ceiling` cluster setting, which defaults to 10% of the heap. A higher ceiling lets a node hold more in-flight append memory before refusing, and a node holding too much runs out of memory instead of refusing, which is the worse outcome. The setting is read at startup, so the cluster must be restarted for a change to take.

Where none of that is open to you, the load itself is what changes: fewer appends, cheaper queries, or both. Refusals that show up only during a spike usually clear on their own once the queues drain.
