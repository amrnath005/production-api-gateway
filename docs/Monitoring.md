# Observability & Monitoring Guide

## 1. Prometheus Metrics
The Gateway exposes Prometheus metrics at `/api/v1/metrics`:
- `gateway_requests_total`: Total request count labeled by method, endpoint, status.
- `gateway_request_duration_seconds`: Request latency histogram.
- `gateway_backend_requests_total`: Requests sent to backend microservices.
- `gateway_backend_failures_total`: Backend connection and failure counters.
- `gateway_circuit_open_total`: Circuit breaker trip event counters.
- `gateway_cache_hits_total` / `gateway_cache_misses_total`: Cache performance.

## 2. OpenTelemetry & Jaeger Tracing
Tracing is automatically configured via OpenTelemetry instrumenting FastAPI and HTTPX:
- Trace IDs (`X-Trace-ID`) and W3C trace contexts (`traceparent`) are propagated to downstream microservices.
- Visual traces are viewable in Jaeger UI at `http://localhost:16686`.

## 3. Grafana Dashboards
Provisioned Grafana dashboards are available at `http://localhost:3000` (Default login: `admin`/`admin`).
