# API Gateway

## Local production environment with Docker

### Run the stack
```bash
docker compose up --build
```

### Service URLs
- Gateway: http://localhost:8000
- User Service: http://localhost:8002
- Order Service: http://localhost:8003
- Redis: redis://localhost:6379/0
- PostgreSQL: postgresql://gateway:gateway_password@localhost:5432/api_gateway
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)
- Jaeger UI: http://localhost:16686

### Key endpoints
```bash
curl http://localhost:8000/api/v1/health
curl http://localhost:8000/api/v1/ready
curl http://localhost:8000/api/v1/health/db
curl http://localhost:8000/api/v1/metrics
curl http://localhost:8002/health
curl http://localhost:8003/health
```

### Environment variables
- `USER_SERVICE_URL` and `ORDER_SERVICE_URL` are set to the Docker service names by default in Compose.
- `REDIS_URL` points to the Redis container.
- `DATABASE_URL` points to the PostgreSQL database.
- `DATABASE_POOL_SIZE`, `DATABASE_MAX_OVERFLOW`, `DATABASE_POOL_TIMEOUT`, and `DATABASE_POOL_RECYCLE_SECONDS` tune SQLAlchemy async connection pooling.
- `JAEGER_ENDPOINT` targets the Jaeger container for tracing export.
- `PROMETHEUS_URL` and `GRAFANA_URL` are used by the monitoring configuration.

### Secret management
- Configuration is loaded through `pydantic-settings` in [app/core/settings.py](app/core/settings.py).
- Sensitive values use `SecretStr` for `JWT_SECRET`, `API_KEY`, and `DATABASE_URL`.
- Development mode allows placeholder values from [.env.example](.env.example).
- Production mode rejects placeholder secrets, enforces minimum secret length, and requires an explicitly configured `DATABASE_URL`.
- Access secret values in application code through `settings.get_jwt_secret()`, `settings.get_api_key()`, and `settings.get_database_url()` rather than reading fields directly.

### Persistence
- PostgreSQL persistence is implemented with SQLAlchemy 2.x async sessions.
- Alembic migrations are stored under [alembic](alembic).
- User CRUD examples are available at `/api/v1/users` and remain protected by the configured API key.
- More details are available in [docs/persistence.md](docs/persistence.md).

### Observability
- Prometheus metrics are exposed at `/api/v1/metrics`.
- The gateway emits counters and histograms for request volume, latency, backend traffic, retries, circuit breaker opens, success/failure counts, backend failures, cache hits/misses, Redis connections, and compression usage.
- OpenTelemetry is enabled for FastAPI, middleware spans, and `httpx` requests.
- Trace IDs are propagated downstream with `traceparent` and `X-Trace-ID` headers.
- Traces are exported to Jaeger when `JAEGER_ENDPOINT` is reachable; otherwise the exporter falls back to console output.

### Redis and Caching
- Redis is configured via `REDIS_URL`, `REDIS_POOL_SIZE`, `CACHE_TTL_SECONDS`, and `CACHE_BYPASS`.
- GET responses can be cached using the cache service and invalidated with `DELETE /api/v1/cache/invalidate?key=...` or `?pattern=...`.
- The cache layer supports TTL expiration, manual invalidation, and pattern-based invalidation.

### Kubernetes
- Production Kubernetes manifests are available under [k8s/base](k8s/base).
- The base includes namespace, ConfigMap, Secret, Deployments, Services, Ingress, resource limits, readiness/liveness probes, HPA, Redis, PostgreSQL, and migrations.
- Deployment notes are available in [k8s/README.md](k8s/README.md).

### Production Deployment
- GitHub Actions CI/CD is defined in [.github/workflows/ci-cd.yml](.github/workflows/ci-cd.yml).
- NGINX reverse proxy and HTTPS configuration are available under [nginx](nginx).
- Load testing is available in [load-testing/k6-gateway.js](load-testing/k6-gateway.js).
- Production deployment and architecture docs are available in [docs/production-deployment.md](docs/production-deployment.md) and [docs/final-architecture.md](docs/final-architecture.md).

### Performance
- Gzip compression is applied for eligible GET responses when the client advertises `Accept-Encoding: gzip`.
- ETags are generated for GET responses and honored via `If-None-Match` with `304 Not Modified` responses.

### Prometheus and Grafana
- A sample Prometheus config is available in [prometheus.yml](prometheus.yml).
- Grafana datasource and dashboard provisioning files are available under [grafana/provisioning](grafana/provisioning).

### Troubleshooting
- If a service fails to start, inspect the container logs with `docker compose logs <service>`.
- If the gateway cannot reach the user or order services, confirm the Docker network and service names in Compose.
- If Grafana does not show Prometheus, wait for the provisioning step to finish and refresh the UI.

### Example Usage
```bash
pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
curl http://127.0.0.1:8000/api/v1/health
curl http://127.0.0.1:8000/api/v1/metrics
curl -X DELETE "http://127.0.0.1:8000/api/v1/cache/invalidate?pattern=cache:*"
```
