# Vandrell Relay — Deployment Notes

Vandrell Relay is a fictional HTTP relay. This document is test data.

## Defaults

- Listen port: 8443
- Connect timeout: 30 seconds
- Read timeout: 120 seconds
- Maximum concurrent connections: 512
- Retry attempts per request: 3

## Requirements

- TLS 1.2 is the oldest protocol version the relay will negotiate.
- The access log uses JSON Lines, one record per line.
- Health checks should target /-/healthy.
