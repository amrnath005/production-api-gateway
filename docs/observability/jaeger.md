# Jaeger Distributed Tracing

OpenTelemetry instruments FastAPI and HTTPX requests, exporting spans to Jaeger (`http://localhost:16686`).

---

## OTLP Trace Propagation
The Gateway injects W3C `traceparent` and `X-Trace-ID` headers into forwarded requests:

```text
traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
```

Traces visualize the complete lifecycle timing across middleware, cache lookups, database queries, and backend microservice requests.
