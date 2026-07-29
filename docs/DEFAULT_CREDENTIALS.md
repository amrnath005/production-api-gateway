# Default Credentials & Service Registry

This document lists every service running in the API Gateway local development stack, including URLs, default credentials, pre-configured connections, and operational notes.

| Service | URL | Username | Password | Database | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **FastAPI API Gateway** | `http://localhost:8000` | N/A | N/A | N/A | Core Gateway Service |
| **Swagger OpenAPI Docs** | `http://localhost:8000/docs` | `admin` | `admin123` | N/A | Interactive API documentation and endpoint testing |
| **PostgreSQL Database** | `localhost:5432` | `gateway` | `gateway_password` | `api_gateway` | Primary relational database |
| **pgAdmin 4** | `http://localhost:5050` | `admin@admin.com` | `admin` | `api_gateway` | **Auto-connects to PostgreSQL** on startup (Server: `API Gateway Postgres`) |
| **Redis In-Memory Store** | `localhost:6379` | *None* | *None* | `0` | Caching layer and sliding window rate limiter |
| **RedisInsight** | `http://localhost:5540` | *None* | *None* | `0` | **Auto-connects to Redis** on startup (Host: `redis:6379`) |
| **Grafana Dashboards** | `http://localhost:3000` | `admin` | `admin` | N/A | **Auto-login enabled** as Admin (Anonymous access enabled for dev) |
| **Prometheus Metrics** | `http://localhost:9090` | *None* | *None* | N/A | Scrapes Gateway metrics at `/api/v1/metrics` every 10s |
| **Jaeger Tracing UI** | `http://localhost:16686` | *None* | *None* | N/A | Visualizes OpenTelemetry distributed traces |
| **Kafka / Kafka UI** | N/A | N/A | N/A | N/A | Not deployed (Gateway relies on direct HTTP/REST & gRPC proxying) |

---

## Zero-Configuration Summary

> [!NOTE]
> Every UI component in the stack is pre-configured:
> - **pgAdmin (`:5050`)**: Auto-loads `API Gateway Postgres` server using `/pgadmin4/pgpass`.
> - **RedisInsight (`:5540`)**: Auto-connects to `redis:6379`.
> - **Grafana (`:3000`)**: Pre-loads Prometheus datasource and 10 dashboards with anonymous admin auto-login.
