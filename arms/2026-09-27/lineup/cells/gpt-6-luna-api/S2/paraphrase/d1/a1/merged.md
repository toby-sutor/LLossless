# Vandrell Relay — Configuration Reference

Vandrell Relay is a fictional HTTP relay. This document is test data.

## Network defaults

The relay's default listen port is 8443.
Connections that do not complete a handshake inside 30 seconds are dropped.
The relay allows a response 120 seconds to arrive before it times out.

## Capacity and retries

At most 512 connections may be held open concurrently.
The relay makes up to 3 further attempts after a request fails.

## Security and observability

The relay will not negotiate any protocol version below TLS 1.2.
Access log records are emitted one JSON object per line.
The endpoint /-/healthy answers health checks.
