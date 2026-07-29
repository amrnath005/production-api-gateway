# Local Development Platform Guide

## 1. Quick Start
To spin up the entire production-grade local development platform:

```bash
docker compose up -d
```

Or using `make`:
```bash
make up
```

## 2. Platform Endpoints

| Service | Port | Endpoint URL | Default Credentials |
| :--- | :---: | :--- | :--- |
| **FastAPI Gateway** | 8000 | `http://localhost:8000` | N/A |
| **Swagger UI** | 8000 | `http://localhost:8000/docs` | N/A |
| **Grafana Dashboards** | 3000 | `http://localhost:3000` | `admin` / `admin` |
| **Prometheus Metrics** | 9090 | `http://localhost:9090` | N/A |
| **Jaeger Tracing** | 16686 | `http://localhost:16686` | N/A |
| **pgAdmin (Postgres)** | 5050 | `http://localhost:5050` | `admin@admin.com` / `admin` |
| **RedisInsight** | 5540 | `http://localhost:5540` | N/A |

## 3. Workflow Commands
- Start platform: `make up`
- View gateway logs: `make logs`
- Run unit tests: `make test`
- Run load benchmarks: `make benchmark`
- Stop & clean volumes: `make clean`
