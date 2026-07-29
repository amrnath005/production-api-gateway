# Production API Gateway & Observability Platform Documentation

Welcome to the official technical documentation for the **Production FastAPI API Gateway & Observability Platform**.

This documentation is organized into topic-based modules following CNCF and enterprise open-source standards.

---

## 📚 Documentation Index

### 🏛️ [Architecture](architecture/overview.md)
- [Architecture Overview](architecture/overview.md) — High-level system architecture, goals, and constraints.
- [Request Flow](architecture/request-flow.md) — End-to-end request lifecycle and trace propagation.
- [Architecture Diagrams](architecture/diagrams.md) — Complete set of Mermaid sequence and component diagrams.
- [Design Decisions](architecture/design-decisions.md) — Architectural Decision Records (ADRs) and design trade-offs.

### ⚙️ [Backend & Services](backend/api-reference.md)
- [API Reference](backend/api-reference.md) — Complete REST OpenAPI endpoint specification with sample JSON requests/responses.
- [Proxy Routing](backend/routing.md) — Dynamic microservice proxying, hop-by-hop header sanitization, and load balancing.
- [Authentication](backend/authentication.md) — JWT Bearer token issuance and PBKDF2-HMAC-SHA256 password hashing.
- [Database](backend/database.md) — Async PostgreSQL persistence with SQLAlchemy 2.x and Alembic migrations.
- [Redis Cache & Rate Limiting](backend/redis.md) — Redis response caching, ETags, and sliding-window rate limiting.
- [Services Catalog](backend/services.md) — Internal business logic services (Gateway, Circuit Breaker, Retry, Health Monitor).

### 📊 [Observability & Monitoring](observability/prometheus.md)
- [Prometheus Metrics](observability/prometheus.md) — Prometheus scraper setup, configuration, and `/api/v1/metrics` target.
- [Grafana Dashboards](observability/grafana.md) — 10 auto-provisioned operational dashboards and anonymous admin login.
- [Jaeger Distributed Tracing](observability/jaeger.md) — OpenTelemetry trace context propagation and Jaeger OTLP exporter.
- [Structured Logging](observability/logging.md) — Contextual JSON logging, request IDs, and correlation ID tracking.
- [Metrics Catalog](observability/metrics.md) — Comprehensive metric definitions, counters, gauges, and cardinality normalization.

### 🚀 [Deployment & Operations](deployment/local-setup.md)
- [Local Setup & Walkthrough](deployment/local-setup.md) — Zero-configuration local startup with Docker Compose and Makefile.
- [Docker Architecture](deployment/docker.md) — Multi-stage Dockerfile builds and Compose container topology.
- [Production Deployment](deployment/production.md) — NGINX reverse proxy, SSL/TLS, and production deployment guide.
- [Environment Configuration](deployment/environment.md) — Environment variable reference and Pydantic `SecretStr` validation.

### 🛡️ [Security](security/security.md)
- [Security Model & OWASP Hardening](security/security.md) — OWASP Top 10 mitigation strategies and security architecture.
- [API Key Authentication](security/api-keys.md) — `X-API-Key` verification and constant-time digest comparison.

### 🧪 [Testing & Performance](testing/testing.md)
- [Automated Testing Suite](testing/testing.md) — Pytest test runner, test structure, and unit/integration coverage.
- [Performance Benchmarks](testing/performance.md) — Multi-tier load test benchmarks (k6 & Locust for 100, 500, 1,000 VUs).

### 🛠️ [Development & Community](development/contributing.md)
- [Contributing Guide](development/contributing.md) — Developer setup, pull request workflows, and guidelines.
- [Coding Standards](development/coding-standards.md) — PEP 8 style rules, type hinting, and Clean Code practices.
- [Repository Structure](development/repository-structure.md) — Detailed folder tree and module responsibility blueprint.

### 🔮 [Roadmap & Interview Guide](roadmap/future-work.md)
- [Future Work & Roadmap](roadmap/future-work.md) — Planned enhancements (Kubernetes HPA, Kafka, Service Mesh).
- [Technical Interview Guide](interview/interview-guide.md) — 100+ deep-dive software engineering interview Q&As based on this repository.
