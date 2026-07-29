# Structured JSON Logging

Logs are formatted as structured JSON payloads in `app/core/observability.py`.

---

## Log Output Schema

```json
{
  "timestamp": "2026-07-29T10:00:00.123456Z",
  "message": "request_completed",
  "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "correlation_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "service": "api-gateway",
  "backend": "http://user-service:8002",
  "method": "GET",
  "path": "/api/v1/users/1",
  "status": 200,
  "latency": 3.24,
  "exception": null
}
```
