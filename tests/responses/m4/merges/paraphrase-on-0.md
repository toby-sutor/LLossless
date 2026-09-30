Vandrell Relay — Operator Guide and Deployment Notes

Vandrell Relay is a fictional HTTP relay. This document is test data.

## Listening and timeouts

Unless you override it, the relay binds to port 8443. A connection that has not been established within 30 seconds is abandoned. Once connected, the relay waits up to 120 seconds for a response.

## Capacity

No more than 512 connections may be open at the same time. A failed request is attempted again up to 3 times.

## Transport security

Anything older than TLS 1.2 is rejected. TLS 1.2 is the oldest protocol version the relay will negotiate.

## Observability

Every access log line is a single JSON object. The access log uses JSON Lines, one record per line. Liveness is reported at /-/healthy. Health checks should target /-/healthy.