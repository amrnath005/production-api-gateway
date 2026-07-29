# Architectural Decision Records (ADRs)

## ADR-001: Selection of FastAPI & Starlette for Gateway Core
- **Status**: Accepted
- **Context**: The Gateway requires low latency, non-blocking HTTP proxying, and built-in OpenAPI validation.
- **Decision**: Use FastAPI on Uvicorn (ASGI). FastAPI provides native async execution, Pydantic type safety, and fast routing.
- **Consequences**: Enables high concurrent throughput while keeping python syntax clean and maintainable.

## ADR-002: Dual-Layer Sliding Window Rate Limiting
- **Status**: Accepted
- **Context**: The Gateway must protect backend microservices from DoS attacks and rate bursts, with or without external cache instances.
- **Decision**: Implement Redis-backed atomic `INCR` sliding window rate limiting as primary, with an in-memory client IP dictionary fallback when Redis is unavailable.
- **Consequences**: Ensures high availability of rate limiting even during Redis failover.

## ADR-003: Low-Cardinality Metric Path Normalization
- **Status**: Accepted
- **Context**: Dynamic paths (e.g. `/api/v1/users/123` vs `/api/v1/users/456`) create high-cardinality label explosions in Prometheus TSDB.
- **Decision**: Normalize route paths centrally in `log_requests` middleware using route templates or replacing numeric IDs/UUIDs with `{id}`.
- **Consequences**: Keeps TSDB memory usage constant while accurately tracking all Gateway traffic.
