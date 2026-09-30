# Vandrell Relay — Configuration Reference

Vandrell Relay is a fictional HTTP relay. This document is test data.

## Networking

The relay listens on port 8443 by default.
The default connect timeout is 60 seconds.
The default read timeout is 120 seconds.

## Limits

The relay accepts at most 512 concurrent connections.
Each request is retried at most 3 times.

## Security

The minimum accepted TLS version is TLS 1.2.

## Operations

Access logs are written in JSON Lines format.
The health check endpoint is /-/healthy.
