# Vandrell Relay — Operator Guide

Vandrell Relay is a fictional HTTP relay. This document is test data.

## Listening and timeouts

Unless you override it, the relay binds to port 8443.
A connection that has not been established within 30 seconds is abandoned.
Once connected, the relay waits up to 120 seconds for a response.

## Capacity

No more than 512 connections may be open at the same time.
A failed request is attempted again up to 3 times.

## Transport security

Anything older than TLS 1.2 is rejected.

## Observability

Every access log line is a single JSON object.
Liveness is reported at /-/healthy.
