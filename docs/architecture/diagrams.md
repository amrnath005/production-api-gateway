# System Architecture Diagrams

This document collects all architectural Mermaid diagrams illustrating components, state machines, deployment topologies, and caching flows.

---

## 1. Circuit Breaker State Machine

```mermaid
stateDiagram-v2
    [*] --> CLOSED: Normal Operation
    CLOSED --> OPEN: Failure Threshold Reached (5 failures)
    OPEN --> HALF_OPEN: Recovery Timeout Expired (30s)
    HALF_OPEN --> CLOSED: Probe Request Succeeds
    HALF_OPEN --> OPEN: Probe Request Fails
```

---

## 2. Dynamic Retry Flow

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

---

## 3. Redis Cache Lookup Flow

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
        Gateway->>Redis: SET cache:sha256(request_key) with TTL=60s
        Gateway-->>Client: 200 OK Response
    end
```

---

## 4. Kubernetes Deployment Topology

```mermaid
graph LR
    subgraph Kubernetes Cluster
        Ingress["Nginx Ingress Controller"] --> GatewayPods["API Gateway Pods (HPA 2-10 Replicas)"]
        GatewayPods --> RedisService["Redis Service"]
        GatewayPods --> PostgresService["PostgreSQL StatefulSet"]
        GatewayPods --> UserPods["User Microservice Pods"]
        GatewayPods --> OrderPods["Order Microservice Pods"]
    end
```
