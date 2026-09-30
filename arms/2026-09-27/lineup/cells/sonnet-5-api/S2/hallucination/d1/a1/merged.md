# Vandrell Relay — Configuration Reference

Vandrell Relay is a fictional HTTP relay. This document is test data.

## Networking

The relay listens on port 8443 by default.
The default connect timeout is 30 seconds.
The relay accepts at most 512 concurrent connections.
Upstream traffic can be forwarded through a SOCKS5 proxy.

## Security

The minimum accepted TLS version is TLS 1.2.
Client certificate verification is disabled by default.

## Operations

Access logs are written in JSON Lines format.
The health check endpoint is /-/healthy.
