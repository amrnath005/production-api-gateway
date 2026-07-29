# Changelog

All notable changes to the **Production FastAPI API Gateway** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-07-29

### Added
- **Observability Platform**: Integrated OpenTelemetry W3C trace propagation, Jaeger OTLP exporter, Prometheus `/api/v1/metrics` exporter, and 10 auto-provisioned Grafana dashboards.
- **Zero-Configuration Developer Experience**: Auto-connected pgAdmin (`:5050`), auto-connected RedisInsight (`:5540`), and Grafana anonymous admin auto-login (`:3000`).
- **Resilience Engine**: Circuit Breaker state machine, exponential backoff retries with jitter, and background health-monitored round-robin load balancer.
- **Security Hardening**: Salted `PBKDF2-HMAC-SHA256` password hashing, constant-time `secrets.compare_digest` API key verification, and JWT Bearer token authentication.
- **Database & Cache**: Async PostgreSQL persistence with SQLAlchemy 2.x, Alembic migrations, SHA-256 Redis GET response caching, ETags (`304 Not Modified`), and Gzip compression.
- **Load Benchmark Suite**: Multi-tier load tests for 100, 500, and 1,000 concurrent virtual users using `k6` and `Locust`.
- **Enterprise Documentation**: Restructured CNCF/enterprise-grade topic-based documentation under `docs/`.
