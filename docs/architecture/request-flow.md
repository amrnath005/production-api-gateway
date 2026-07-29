# End-to-End Request Flow & Trace Propagation

This document details the lifecycle of an HTTP request as it traverses the API Gateway processing pipeline.

---

## Request Execution Lifecycle

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
        RateLimiter-->>Gateway: Blocked (Count > Limit)
        Gateway-->>Client: 429 Too Many Requests
    else Rate Limit OK
        RateLimiter-->>Gateway: Allowed
        Gateway->>Auth: Validate Bearer Token / API Key
        alt Auth Failed
            Auth-->>Gateway: Invalid Credentials
            Gateway-->>Client: 401 Unauthorized / 403 Forbidden
        else Auth Passed
            Auth-->>Gateway: Claims / Authorized
            Gateway->>Cache: GET SHA-256(Method:Path:Query)
            alt Cache Hit (GET Requests)
                Cache-->>Gateway: Cached JSON Payload
                Gateway-->>Client: 200 OK (from Cache)
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
                        Gateway->>CB: Record Failure
                        Gateway-->>Client: 502 Bad Gateway / 504 Gateway Timeout
                    end
                end
            end
        end
    end
```

---

## Context & Trace Header Propagation

When an HTTP request enters the Gateway:
1. **Request ID Assignment**: `log_requests` middleware assigns a UUID `request_id` and reads or generates `X-Correlation-ID`.
2. **OpenTelemetry Context**: An active 128-bit `trace_id` is initialized in OpenTelemetry.
3. **Downstream Propagation**: The Gateway builds correlation headers for microservices via `build_correlation_headers()`:
   - `X-Request-ID`: Unique per-request identifier.
   - `X-Correlation-ID`: End-to-end multi-service transaction correlation ID.
   - `X-Trace-ID`: Hexadecimal trace string.
   - `traceparent`: W3C trace context format (`00-{trace_id}-{span_id}-01`).
