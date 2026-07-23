# System Architecture & Design Diagrams

## 1. Component Diagram
```mermaid
graph TD
    Client["Client / User"] --> |HTTPS| Gateway["API Gateway (FastAPI)"]
    Gateway --> Auth["Auth & Security Middleware"]
    Gateway --> RateLimit["Rate Limiter (Redis / In-Memory)"]
    Gateway --> Cache["Response Cache (Redis)"]
    Gateway --> CircuitBreaker["Circuit Breaker & Load Balancer"]
    CircuitBreaker --> UserService["User Microservice (Port 8002)"]
    CircuitBreaker --> OrderService["Order Microservice (Port 8003)"]
    Gateway --> DB["PostgreSQL Database"]
    Gateway --> Telemetry["OpenTelemetry / Jaeger"]
    Gateway --> Prometheus["Prometheus Metrics (/api/v1/metrics)"]
```

## 2. Deployment Diagram
```mermaid
graph LR
    subgraph Kubernetes Cluster
        Ingress["Nginx Ingress Controller"] --> GatewayPods["API Gateway Pods (HPA: 2-10 replicas)"]
        GatewayPods --> RedisCluster["Redis Service"]
        GatewayPods --> PostgresStateful["PostgreSQL Service"]
        GatewayPods --> UserPods["User Service Pods"]
        GatewayPods --> OrderPods["Order Service Pods"]
    end
```

## 3. Authentication Flow
```mermaid
sequenceDiagram
    autonumber
    Client->>Gateway: POST /login {username, password}
    Gateway->>Database: Query user by username
    Database-->>Gateway: Return user & hashed_password
    Gateway->>Gateway: Verify PBKDF2 password hash
    Gateway->>Client: Return JWT Access Token (Bearer)
```

## 4. Gateway Request Proxy Flow
```mermaid
sequenceDiagram
    autonumber
    Client->>Gateway: Request /api/v1/{service}/{path} (Bearer Token)
    Gateway->>Gateway: Auth Middleware & Rate Limiter check
    Gateway->>Gateway: Sanitize hop-by-hop headers (strip Host)
    Gateway->>LoadBalancer: Get healthy backend URL
    Gateway->>CircuitBreaker: Check before_request(backend)
    Gateway->>Backend: Forward HTTP request (with X-Correlation-ID)
    Backend-->>Gateway: HTTP Response
    Gateway->>CircuitBreaker: Record Success
    Gateway-->>Client: Forward Response with X-Request-ID
```

## 5. Circuit Breaker Flow
```mermaid
stateDiagram-v2
    [*] --> CLOSED
    CLOSED --> OPEN: Failures >= Threshold (5)
    OPEN --> HALF_OPEN: Recovery Timeout (30s)
    HALF_OPEN --> CLOSED: Request Succeeds
    HALF_OPEN --> OPEN: Request Fails
```

## 6. Retry Flow
```mermaid
sequenceDiagram
    autonumber
    Gateway->>Backend: Attempt 1
    Backend-->>Gateway: Connection Error / Timeout
    Gateway->>Gateway: Sleep(initial_delay = 0.1s)
    Gateway->>Backend: Attempt 2
    Backend-->>Gateway: Connection Error / Timeout
    Gateway->>Gateway: Sleep(delay * 2 = 0.2s)
    Gateway->>Backend: Attempt 3 (Success)
    Backend-->>Gateway: 200 OK
```

## 7. Redis Cache Flow
```mermaid
sequenceDiagram
    autonumber
    Client->>Gateway: GET /api/v1/resource
    Gateway->>Redis: GET cache:sha256(request_key)
    alt Cache Hit
        Redis-->>Gateway: Cached Response JSON
        Gateway-->>Client: 200 OK (from Cache)
    else Cache Miss
        Redis-->>Gateway: null
        Gateway->>Backend: Forward Request
        Backend-->>Gateway: 200 OK Response
        Gateway->>Redis: SET cache:sha256(request_key) with TTL
        Gateway-->>Client: 200 OK
    end
```

## 8. Database Flow
```mermaid
sequenceDiagram
    autonumber
    Gateway->>Session: Depends(get_session)
    Session->>Engine: Acquire AsyncConnection from Pool
    Gateway->>UserRepository: Execute SQLAlchemy 2.x Select/Insert
    UserRepository->>Database: PostgreSQL Async Connection
    Database-->>UserRepository: Result Rows
    Session->>Engine: Release Connection to Pool
```
