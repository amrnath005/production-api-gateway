# Distributed Tracing & OpenTelemetry Guide

## Architecture
Every incoming HTTP request generates a unique 128-bit OpenTelemetry trace ID and span ID.

## Propagation
Trace context is propagated down to microservices (`user-service`, `order-service`) via standard W3C `traceparent` and `X-Trace-ID` headers built in `build_correlation_headers()`.

## Visualizing Traces
Open Jaeger UI at `http://localhost:16686` and filter by service `api-gateway`. Spans illustrate:
1. `HTTP GET /api/v1/users` (Root Span)
2. `auth.verify_token` (Child Span)
3. `rate_limit.check` (Child Span)
4. `cache.get` (Child Span)
5. `gateway.forward_request` (Child Span)
6. `httpx.request` (Child Span)
