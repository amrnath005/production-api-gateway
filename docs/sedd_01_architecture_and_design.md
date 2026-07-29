# Enterprise Software Engineering Design Document (SEDD)
## Volume 1: System Architecture, Design Patterns & Real-World Use Cases

---

## Section 4: Problem Statement & Architectural Justification

### 4.1 Why an API Gateway?
In modern microservices architectures, backend systems are decomposed into dozens or hundreds of decoupled services. Allowing client applications (mobile apps, single-page web applications, third-party API consumers) to communicate directly with individual microservices introduces severe architectural liabilities:

```
[ Un-Gatewayed Direct Microservices Communication (Anti-Pattern) ]

              +-------------------+
              | Client Application|
              +---------+---------+
                        |
        +---------------+---------------+
        |               |               |
        v               v               v
  +-----------+   +-----------+   +-----------+
  |  User     |   |  Order    |   | Inventory |
  | Service   |   | Service   |   | Service   |
  +-----------+   +-----------+   +-----------+
  (Exposes IP)    (Exposes IP)    (Exposes IP)
```

#### Key Vulnerabilities of Direct Communication:
1. **Network Overhead & Latency**: Clients must execute multiple HTTP round-trips to aggregate data across different microservices.
2. **Coupling & Leakage**: Internal microservice IP addresses, database schemas, and private endpoints are exposed to the public internet.
3. **Duplicated Cross-Cutting Concerns**: Authentication, authorization, rate limiting, CORS, SSL termination, and request logging must be reimplemented independently in every single microservice.
4. **Protocol Mismatch**: Downstream services may use high-performance internal protocols (gRPC, Protobuf, TCP sockets) that browsers cannot easily consume.

### 4.2 Architectural Solution: Centralized API Gateway
The **Production FastAPI API Gateway** resolves these challenges by introducing a unified, reverse-proxy entry point:

```mermaid
graph TD
    Client["Client Applications (Web / Mobile / API)"] --> |HTTPS / REST| Gateway["FastAPI API Gateway (Port 8000)"]
    
    subgraph Cross Cutting Concerns
        Gateway --> RateLimit["Sliding Window Rate Limiter (Redis)"]
        Gateway --> Auth["JWT & API Key Verification"]
        Gateway --> Cache["SHA-256 Response Cache (Redis)"]
        Gateway --> LB["Round-Robin Load Balancer & Circuit Breaker"]
    end

    LB --> UserSVC["User Microservice (Port 8002)"]
    LB --> OrderSVC["Order Microservice (Port 8003)"]

    Gateway --> DB["Async PostgreSQL 16 (SQLAlchemy 2.x)"]
    Gateway --> OTel["OpenTelemetry / Jaeger Tracing"]
    Gateway --> Prom["Prometheus Metrics Engine"]
```

---

## Section 5: Real-World Enterprise Use Cases

| Industry Sector | Enterprise Context | Gateway Feature Utilized | Value Delivered |
| :--- | :--- | :--- | :--- |
| **FinTech & Banking** | Payment Processing APIs | API Key Verification & Rate Limiting | Prevents brute-force attacks and enforces strict tier-based rate limits on account transactions. |
| **E-Commerce & Retail** | Flash Sales & Product Catalog | SHA-256 Redis Response Caching & ETag | Serves 10,000+ GET requests/sec directly from memory with `< 2ms` latency, offloading downstream microservices. |
| **Logistics & Fleet (Uber/FedEx)** | Driver Location Updates | Circuit Breaker & Exponential Retry | Automatically isolates unhealthy backend instances, retrying transient network timeouts without failing client requests. |
| **Healthcare & Telemedicine** | Patient Records Access | JWT Bearer Authentication & OpenTelemetry Tracing | Mandates token signature verification and generates W3C `traceparent` headers for HIPAA compliance auditing. |
| **Defense & Aerospace (ISRO/DRDO)** | Telemetry Data Distribution | Structured JSON Logging & Low-Cardinality Prometheus Metrics | Provides real-time operational visibility into subsystem metrics and error budgets without high-cardinality degradation. |

---

## Section 7: System Architecture & Request Lifecycles

### 7.1 High-Level Request Lifecycle Diagram

```mermaid
sequenceDiagram
    autonumber
    actor Client
    participant Gateway as FastAPI Gateway
    participant RateLimiter as Rate Limiter (Redis)
    participant Auth as Security / Auth
    participant Cache as Redis Cache
    participant CB as Circuit Breaker & Load Balancer
    participant Backend as Microservice Instance

    Client->>Gateway: HTTP Request (Headers + Payload)
    Gateway->>RateLimiter: Check Client IP Rate Limit
    alt Rate Limit Exceeded
        RateLimiter-->>Gateway: Blocked (Current Count > Limit)
        Gateway-->>Client: 429 Too Many Requests
    else Rate Limit OK
        RateLimiter-->>Gateway: Allowed
        Gateway->>Auth: Validate Bearer Token / API Key
        alt Auth Failed
            Auth-->>Gateway: Invalid / Missing Credentials
            Gateway-->>Client: 401 Unauthorized / 403 Forbidden
        else Auth Passed
            Auth-->>Gateway: Claims / Authorized
            Gateway->>Cache: GET SHA-256(Method:Path:Query)
            alt Cache Hit (GET Requests)
                Cache-->>Gateway: Cached JSON Payload
                Gateway-->>Client: 200 OK (from Redis Cache)
            else Cache Miss
                Cache-->>Gateway: null
                Gateway->>CB: Check Circuit State (CLOSED / HALF_OPEN)
                alt Circuit OPEN
                    CB-->>Gateway: CircuitOpenError
                    Gateway-->>Client: 503 Service Unavailable
                else Circuit CLOSED
                    Gateway->>CB: Select Healthy Backend (Round-Robin)
                    Gateway->>Backend: Forward Sanitized HTTP Request
                    alt Backend Success
                        Backend-->>Gateway: 200 OK Response
                        Gateway->>CB: Record Success
                        Gateway->>Cache: SET Response JSON (TTL: 60s)
                        Gateway-->>Client: 200 OK Response
                    else Backend Error / Timeout
                        Backend-->>Gateway: 5xx / Connection Timeout
                        Gateway->>CB: Record Failure (Inc Failure Count)
                        Gateway-->>Client: 502 Bad Gateway / 504 Gateway Timeout
                    end
                end
            end
        end
    end
```

---

## Section 20: End-to-End Request Lifecycle & Trace Propagation

### 20.1 Distributed Trace Propagation Protocol

```mermaid
graph LR
    subgraph Client Header Injection
        Req["HTTP GET /api/v1/orders/12345"]
    end

    subgraph API Gateway Processing
        Context["Generate Trace ID: 4bf92f3577b34da6a3ce929d0e0e4736"]
        Span["Start Span: gateway.forward_request"]
        HeaderBuild["Inject Headers:<br/>X-Request-ID: uuid-v4<br/>X-Correlation-ID: uuid-v4<br/>traceparent: 00-4bf92f35...-016x-01"]
    end

    subgraph Downstream Microservice
        ServiceReceive["Extract W3C traceparent"]
        ServiceSpan["Start Child Span: order-service.query_db"]
    end

    Req --> Context --> Span --> HeaderBuild --> ServiceReceive --> ServiceSpan
```

1. **Client Request Arrival**: The incoming HTTP request is intercepted by `log_requests` middleware in `app/middleware/logging.py`.
2. **Context Creation**: A unique 128-bit OpenTelemetry `trace_id` and 64-bit `span_id` are initialized alongside `request_id` and `correlation_id`.
3. **Header Sanitization & Injection**: Hop-by-hop headers (`Host`, `Connection`, `Transfer-Encoding`) are stripped, while `X-Request-ID`, `X-Correlation-ID`, `X-Trace-ID`, and standard W3C `traceparent` headers are injected into the forwarded HTTP request.
4. **Jaeger OTLP Export**: The span tree is asynchronously batched and transmitted to Jaeger at `http://jaeger:14268/api/traces`.
