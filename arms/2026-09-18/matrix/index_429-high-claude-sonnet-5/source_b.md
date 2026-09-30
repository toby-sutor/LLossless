# Rising 429 refusals on a managed Nimbrel Ledger deployment

Author: Devin Okonkwo
Updated: 2026-04-11

### Summary / Table of Contents

This note concerns a managed Nimbrel Ledger deployment (NMD) whose share of HTTP `429` replies climbed over a fortnight, as counted at the front proxy. It sets out what the evidence pointed at, which was expensive queries and deep grouping, and what was put forward in response.

### Environment

- Product: Nimbrel Ledger
- Version: 4.4, 5.x
- Platform: Nimbrel Cloud
- Deployment: Managed Ledger Service (MLS)
- Production Environment: Yes

### Issue Description

The managed deployment returns HTTP `429` on a growing share of requests, which is what the Ledger does when it refuses work rather than queueing it. Front proxy counters agree with the client reports, so the refusals are real and not a client-side accounting error.

### Contributing Factors

- **Expensive queries**: a handful of queries run for as long as 2 seconds each. A worker slot is unavailable for as long as one of them holds it, and the queue behind it grows.
- **Deep grouping**: grouping on `channel.id` yields a very large number of groups, and the memory that costs is charged to the same pool the append path draws on.
- **Resource accounting**: processor load looks unremarkable while memory sits high. The two do not agree, which points at query cost rather than at an undersized cluster.

### Proposed Actions

- **Lower the slow query threshold**: set it to 1 second, so that the queries actually responsible are recorded instead of averaged away.
- **Review what the queries are for**: go through the expensive ones with the team that wrote them, several of which look like they could ask for less.
- **Capture evidence during a refusal**: while the refusal rate is high, take a thread dump and a heap snapshot rather than reasoning from counters alone.

### References

{internal-notes}

- [Internal ticket NB-40917](https://tickets.nimbrel.example/issues/40917)

{/internal-notes}

- [Ledger slow query log](https://docs.nimbrel.example/ledger/slow-query-log)
- [HTTP 429 replies](https://support.nimbrel.example/knowledge/318kqp2)
