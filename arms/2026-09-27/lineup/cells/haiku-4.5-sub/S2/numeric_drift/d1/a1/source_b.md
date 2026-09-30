# Vandrell Relay — Deployment Notes

Vandrell Relay is a fictional HTTP relay. This document is test data.

## Capacity

The connection limit is 512 concurrent connections.
Each request is retried at most 3 times.

## Networking

The relay listens on port 8443 by default.
The default connect timeout is 30 seconds.
