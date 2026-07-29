# Repository Structure & Blueprint

```text
api-gateway-project/
├── .github/                     # GitHub Actions CI/CD workflows & Dependabot
├── alembic/                      # Database migration scripts
├── app/                          # Core Gateway Application
│   ├── core/                     # Configuration, security, routes, exceptions, observability
│   ├── db/                       # Session, async engine, health, models
│   ├── middleware/               # Logging and sliding window rate limiter middleware
│   ├── models/                   # Pydantic validation DTOs
│   ├── repositories/             # User repository DAO layer
│   ├── routers/                  # FastAPI APIRouter endpoints
│   ├── services/                 # Gateway reverse proxy, circuit breaker, retry, cache logic
│   └── main.py                   # FastAPI lifespan application entrypoint
├── backend_service/              # Mock User microservice container (:8002)
├── order_service/                # Mock Order microservice container (:8003)
├── docs/                         # Topic-based enterprise documentation
├── grafana/provisioning/         # Provisioned datasources and 10 dashboards
├── k8s/base/                     # Production Kubernetes Kustomize manifests
├── load-testing/                 # k6 and Locust benchmark scripts
├── pgadmin/                      # Auto-connected pgAdmin configuration
├── docker-compose.yml            # 10-service orchestration manifest
├── Dockerfile                    # Multi-stage optimized Docker build
├── Makefile                      # Operational developer commands
└── requirements.txt              # Pinned Python requirements
```
