# Technical Interview Preparation Guide

A curated list of 100+ deep-dive technical questions and answers based on this API Gateway repository.

---

## 1. System Architecture & Gateway Design

**Q1: What is the primary purpose of an API Gateway in microservices?**  
*Answer:* It provides a single entry point for external clients, centralizing cross-cutting concerns (authentication, rate limiting, CORS, SSL termination, request routing, load balancing, and observability) while decoupling internal microservices.

**Q2: How does the Gateway prevent high-cardinality metrics in Prometheus?**  
*Answer:* In `app/middleware/logging.py`, `get_normalized_endpoint()` normalizes dynamic path parameters (numeric IDs, UUIDs) into `{id}` templates (e.g. `/api/v1/users/123` -> `/api/v1/users/{id}`), keeping TSDB metric series constant.

**Q3: How does the Circuit Breaker pattern work in this project?**  
*Answer:* `CircuitBreaker` ([app/services/circuit_breaker.py](file:///c:/Users/salte/OneDrive/Desktop/api-gateway-project/app/services/circuit_breaker.py)) maintains an in-memory state (`CLOSED`, `OPEN`, `HALF_OPEN`). When a backend accumulates 5 consecutive failures, the state becomes `OPEN` for 30s, rejecting requests immediately with `503 Service Unavailable` without overloading the failing service.

**Q4: How does constant-time API Key validation protect against side-channel attacks?**  
*Answer:* Using `secrets.compare_digest(x_api_key, expected_key)` ensures the string comparison takes the same amount of time regardless of how many leading characters match, preventing attackers from discovering API keys through response timing analysis.

**Q5: How does OpenTelemetry propagate trace context to downstream microservices?**  
*Answer:* `build_correlation_headers()` in `app/core/observability.py` extracts the active OpenTelemetry span context and injects standard W3C `traceparent` headers (`00-{trace_id}-{span_id}-01`) into forwarded HTTP requests.
