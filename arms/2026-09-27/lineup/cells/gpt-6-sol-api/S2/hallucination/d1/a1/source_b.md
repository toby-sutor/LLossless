# Vandrell Relay — Deployment Notes

Vandrell Relay is a fictional HTTP relay. This document is test data.

## Networking

The relay listens on port 8443 by default.
The relay accepts at most 512 concurrent connections.

## Operations

Access logs are written in JSON Lines format.
The health check endpoint is /-/healthy.
