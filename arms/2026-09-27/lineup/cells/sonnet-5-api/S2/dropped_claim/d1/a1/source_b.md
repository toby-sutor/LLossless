# Vandrell Relay — Deployment Notes

Vandrell Relay is a fictional HTTP relay. This document is test data.

## Runtime

The relay listens on port 8443 by default.
The relay accepts at most 512 concurrent connections.
One worker process is started per CPU core.

## Logging

Access logs are written in JSON Lines format.
Log files are rotated when they reach 100 megabytes.

## Health

The health check endpoint is /-/healthy.
A relay that fails 3 consecutive health checks is removed from rotation.
