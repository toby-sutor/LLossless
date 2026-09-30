# Vandrell Relay — Configuration Reference

Vandrell Relay is a fictional HTTP relay. This document is test data.

## Networking

The relay listens on port 8443 by default.
The default connect timeout is 30 seconds.
The default read timeout is 120 seconds.

## Limits

The relay accepts at most 512 concurrent connections.
Each request is retried at most 3 times.
One worker process is started per CPU core.

## Security

The minimum accepted TLS version is TLS 1.2.

## Logging and health

Log files are rotated when they reach 100 megabytes.
The health check endpoint is /-/healthy.
A relay that fails 3 consecutive health checks is removed from rotation.
