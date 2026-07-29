# Central Prometheus Metrics Catalog

All metrics exported by `app/services/metrics.py`:

| Metric Name | Type | Description | Labels |
| :--- | :--- | :--- | :--- |
| `gateway_requests_total` | Counter | Total requests processed | `method`, `endpoint`, `status` |
| `gateway_request_duration_seconds` | Histogram | Request latency distribution | `method`, `endpoint` |
| `gateway_active_requests` | Gauge | Currently active requests | None |
| `gateway_db_status` | Gauge | Database health status (1/0) | None |
| `gateway_db_queries_total` | Counter | Total DB queries executed | None |
| `gateway_redis_connections` | Gauge | Live Redis connection status | None |
| `gateway_cache_hits_total` | Counter | Total cache hits | None |
| `gateway_cache_misses_total` | Counter | Total cache misses | None |
| `gateway_cache_latency_seconds` | Histogram | Redis cache access latency | None |
| `gateway_circuit_open_total` | Counter | Total circuit breaker trips | None |
| `gateway_retry_total` | Counter | Total exponential retries | None |
| `gateway_healthy_instances` | Gauge | Count of healthy backends | None |
| `gateway_unhealthy_instances` | Gauge | Count of unhealthy backends | None |
| `backend_requests_total` | Counter | Downstream backend requests | `service`, `backend` |
| `gateway_backend_failures_total` | Counter | Downstream backend errors | `service`, `backend` |

---

## Low-Cardinality Path Normalization
To prevent Prometheus TSDB memory degradation, `log_requests` middleware normalizes dynamic URL parameters (numbers, UUIDs) into `{id}` templates (e.g. `/api/v1/users/123` -> `/api/v1/users/{id}`).
