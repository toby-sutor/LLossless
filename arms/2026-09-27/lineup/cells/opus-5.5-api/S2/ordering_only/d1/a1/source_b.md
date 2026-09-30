# Vandrell Relay — Configuration Reference

Vandrell Relay is a fictional HTTP relay. This document is test data.

## Logging

Access logs are written in JSON Lines format.
Log files are rotated when they reach 100 megabytes.

## Security

The minimum accepted TLS version is TLS 1.2.
Client certificate verification is disabled by default.

## Limits

The relay accepts at most 512 concurrent connections.
Each request is retried at most 3 times.
Retry backoff starts at 250 milliseconds and doubles on every attempt.

## Networking

The relay listens on port 8443 by default.
The default connect timeout is 30 seconds.
The default read timeout is 120 seconds.
The health check endpoint is /-/healthy.
