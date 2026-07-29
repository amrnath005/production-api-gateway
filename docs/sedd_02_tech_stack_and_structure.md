# Enterprise Software Engineering Design Document (SEDD)
## Volume 2: Technology Stack Evaluation, Repository Structure & Code Walkthrough

---

## Section 8: Technology Stack Analysis & Trade-Off Evaluation

| Technology | Purpose | Selected Version | Trade-Off Rationale / Alternatives Considered | Enterprise Adoption |
| :--- | :--- | :--- | :--- | :--- |
| **FastAPI** | Async Web Framework | `0.139.2` | Chosen over Flask/Django for native ASGI `async/await` performance, automatic Pydantic schema validation, and OpenAPI doc generation. | Netflix, Uber, Microsoft |
| **Uvicorn** | ASGI Web Server | `0.51.0` | High-performanceuvloop/httptools implementation powering async request handling. | Cloudflare, Stripe |
| **PostgreSQL** | Relational Persistence | `16-alpine` | Chosen over MySQL/MongoDB for ACID compliance, JSONB support, and native async integration with SQLAlchemy 2.x. | Apple, Stripe, Instagram |
| **SQLAlchemy 2.x** | Async ORM Engine | `2.0.36` | Pure 2.x typed `async_sessionmaker` and `select()` API eliminates legacy 1.x blocking ORM patterns. | Dropbox, Red Hat |
| **Redis** | In-Memory Cache & Rate Limiting | `7-alpine` | Sub-millisecond latency for sliding-window rate limiting and response caching vs Memcached (which lacks data structures). | Twitter, GitHub, Airbnb |
| **Prometheus** | Metrics Collection | `v2.54.1` | Pull-based TSDB model for real-time alerting and SLA monitoring. | CNCF Graduated, Google |
| **Grafana** | Operational Dashboards | `11.2.0` | Provisioned multi-dashboard visualization engine with native Prometheus & Jaeger datasources. | Uber, Bloomberg |
| **Jaeger / OTel** | Distributed Tracing | `1.60` | W3C OTLP trace context propagation across microservices vs Zipkin. | Uber, CNCF |

---

## Section 9: Repository Structure & Architectural Blueprint

```text
api-gateway-project/
├── .github/
│   ├── dependabot.yml              # Automated dependency update schedule
│   └── workflows/
│       └── ci-cd.yml               # GitHub Actions CI/CD Pipeline (Test, Lint, Docker, K8s)
├── alembic/                        # Database Migration Scripts
│   ├── env.py                      # Async Alembic environment configuration
│   └── versions/                   # Migration revision history
├── app/                            # Core FastAPI Application Package
│   ├── core/                       # Framework Core & System Configuration
│   │   ├── dependencies.py         # FastAPI Route Security Dependencies (API Key, JWT Bearer)
│   │   ├── exceptions.py           # Domain Exception Hierarchy (GatewayException, CircuitOpenError)
│   │   ├── observability.py        # Structured JSON Logging & OTel Jaeger Tracing Initializer
│   │   ├── routes.py               # Downstream Microservice Registry
│   │   ├── security.py             # Salted PBKDF2 Password Hashing & JWT Verification
│   │   └── settings.py             # Pydantic-Settings Environment Configuration & Secret Validation
│   ├── db/                         # Persistence Layer Configuration
│   │   ├── base.py                 # SQLAlchemy Declarative Base
│   │   ├── config.py               # Async Engine Parameter Builder (SQLite / Postgres)
│   │   ├── health.py               # Database Health Check & Metric Gauge Exporter
│   │   ├── lifespan.py             # Lifespan Hook for Database Connection Pool Shutdown
│   │   ├── models/                 # SQLAlchemy ORM Models
│   │   │   └── user.py             # Database User Entity
│   │   └── session.py              # Async Engine & Session Maker Factory
│   ├── middleware/                 # ASGI Middleware Components
│   │   ├── logging.py              # Request Context, Trace Context & Low-Cardinality Metric Exporter
│   │   └── rate_limit.py           # Dual-layer Sliding Window Rate Limiter (Redis / Memory)
│   ├── models/                     # Pydantic Schemas & DTOs
│   │   └── user.py                 # User Request/Response Validation Schemas
│   ├── repositories/               # Data Access Object (DAO) Layer
│   │   └── users.py                # Async User Repository with Query Counting Metrics
│   ├── routers/                    # FastAPI APIRouter Endpoints
│   │   ├── admin.py                # Protected Admin Endpoint (`/admin`)
│   │   ├── cache.py                # Cache Invalidation API (`/api/v1/cache/invalidate`)
│   │   ├── health.py               # Health & Readiness Probes (`/api/v1/health`, `/ready`)
│   │   ├── login.py                # Authentication & JWT Token Issuance (`/login`)
│   │   ├── metrics.py              # Prometheus Metrics Exporter Endpoint (`/api/v1/metrics`)
│   │   ├── ping.py                 # Liveness Ping (`/ping`)
│   │   ├── profile.py              # Protected Profile Endpoint (`/profile`)
│   │   ├── proxy.py                # Dynamic Microservice Proxy Router (`/api/v1/{service}/{path}`)
│   │   ├── root.py                 # Root Welcome Endpoint (`/`)
│   │   ├── users.py                # User Management CRUD Endpoints (`/api/v1/users`)
│   │   └── version.py              # Version Info Endpoint (`/version`)
│   ├── services/                   # Business Logic & Infrastructure Services
│   │   ├── auth.py                 # JWT Token Signing Service
│   │   ├── cache.py                # Redis Async Cache Service & Decorator
│   │   ├── circuit_breaker.py      # State-machine Circuit Breaker Service
│   │   ├── gateway.py              # HTTPX Reverse Proxy Execution Engine
│   │   ├── health_checker.py       # Microservice Instance Ping Service
│   │   ├── health_monitor.py       # Background Service Health Monitoring Loop
│   │   ├── load_balancer.py        # Round-Robin Load Balancer Service
│   │   ├── metrics.py              # Central Prometheus Metric Registry
│   │   ├── performance.py          # Response Gzip Compression & ETag Feature Service
│   │   └── retry.py                # Exponential Backoff Retry Service
│   └── main.py                     # FastAPI Application Initialization & Lifespan Entrypoint
├── backend_service/                # Mock Downstream User Microservice (:8002)
├── order_service/                  # Mock Downstream Order Microservice (:8003)
├── docs/                           # Enterprise Documentation & User Guides
│   ├── DEFAULT_CREDENTIALS.md      # Zero-Config Credentials & Service Registry Table
│   ├── FIRST_RUN.md                # Beginner Walkthrough & Verification Steps
│   ├── Architecture.md             # Visual Mermaid Sequence Diagrams
│   ├── Deployment.md               # Docker & Kubernetes Deployment Manual
│   ├── LOCAL_DEVELOPMENT.md        # Makefile & Local Dev Workflow Guide
│   ├── MONITORING_GUIDE.md         # Prometheus Metrics Reference
│   ├── OBSERVABILITY_GUIDE.md      # OpenTelemetry & Jaeger Tracing Manual
│   └── sedd_*.md                   # Software Engineering Design Document Volumes
├── grafana/provisioning/           # Auto-Provisioned Grafana Datasources & 10 Dashboards
├── load-testing/                   # k6 & Locust Performance Load Test Scripts
├── pgadmin/                        # Auto-Connected pgAdmin Server Configs (`servers.json`, `pgpass`)
├── k8s/base/                       # Kubernetes Production Manifests (HPA, Ingress, Secrets, Probes)
├── docker-compose.yml              # Complete 10-Service Orchestration Manifest
├── Dockerfile                      # Multi-stage Optimized Gateway Image
├── Makefile                        # One-command Operational Commands (`make up`, `make test`)
├── requirements.txt                # Pinned Dependency Manifest
└── BENCHMARK_REPORT.md             # Load Test Benchmark Results Report
```

---

## Section 10: Source Code Architecture Walkthrough

### 10.1 Centralized Prometheus Metric Registry ([app/services/metrics.py](file:///c:/Users/salte/OneDrive/Desktop/api-gateway-project/app/services/metrics.py))
Defines all operational counters, gauges, and latency histograms exposed at `/api/v1/metrics`:

```python
from prometheus_client import Counter, Gauge, Histogram

REQUEST_COUNT = Counter(
    "gateway_requests_total",
    "Total number of requests",
    ["method", "endpoint", "status"],
)

REQUEST_LATENCY = Histogram(
    "gateway_request_duration_seconds",
    "Request latency",
    ["method", "endpoint"],
)

DB_STATUS = Gauge("gateway_db_status", "Database status (1 for ready, 0 for unavailable)")
DB_QUERIES = Counter("gateway_db_queries_total", "Total database queries executed")
REDIS_CONNECTIONS = Gauge("gateway_redis_connections", "Current Redis connections")
CIRCUIT_OPEN = Counter("gateway_circuit_open_total", "Circuit breaker opened")
```

### 10.2 Global Low-Cardinality Observability Middleware ([app/middleware/logging.py](file:///c:/Users/salte/OneDrive/Desktop/api-gateway-project/app/middleware/logging.py))
Intercepts every HTTP request, assigns trace context, normalizes path templates to prevent high cardinality, and updates global counters:

```python
def get_normalized_endpoint(request: Request) -> str:
    route = request.scope.get("route")
    if route and getattr(route, "path", None):
        return route.path

    path = request.url.path
    segments = path.strip("/").split("/")
    if not segments or segments == [""]:
        return "/"

    normalized = ["{id}" if s.isdigit() or UUID_RE.match(s) else s for s in segments]
    return "/" + "/".join(normalized)
```

### 10.3 Reverse Proxy Engine ([app/services/gateway.py](file:///c:/Users/salte/OneDrive/Desktop/api-gateway-project/app/services/gateway.py))
Manages long-lived HTTPX connection pools, strips hop-by-hop headers, executes load balancing, and delegates to the retry service:

```python
class GatewayService:
    def __init__(self) -> None:
        self._client = httpx.AsyncClient(
            timeout=settings.REQUEST_TIMEOUT,
            limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
        )

    async def forward_request(self, service: str, method: str, path: str, headers: dict, params: dict, body: bytes | None):
        backend_url = await load_balancer.get_next_instance(service_name=service, instances=SERVICE_REGISTRY[service])
        target_url = f"{backend_url}/{service}" + (f"/{path}" if path else "")
        forward_headers = sanitize_forward_headers(headers)

        circuit_breaker.before_request(backend_url)

        async def send():
            BACKEND_REQUESTS.labels(service=service, backend=backend_url).inc()
            return await self._client.request(method=method, url=target_url, headers=forward_headers, params=params, content=body)

        response = await retry_service.execute(send)
        circuit_breaker.record_success(backend_url)
        return response
```
