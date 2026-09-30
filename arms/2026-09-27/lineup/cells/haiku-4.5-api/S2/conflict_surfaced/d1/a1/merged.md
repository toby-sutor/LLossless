# Vandrell Relay — Configuration Reference

Vandrell Relay is a fictional HTTP relay. This document is test data.

## Networking

The relay listens on port 8443 by default.
The default read timeout is 120 seconds.

> **Unresolved: default connect timeout.**
> According to the Operator Guide, the default connect timeout is 30 seconds.
> According to the Deployment Notes, the default connect timeout is 60 seconds.
> The sources disagree and this merge does not choose between them. An operator must decide which value applies.

## Limits

The relay accepts at most 512 concurrent connections.
Each request is retried at most 3 times.

## Security

The minimum accepted TLS version is TLS 1.2.

## Operations

Access logs are written in JSON Lines format.
The health check endpoint is /-/healthy.
