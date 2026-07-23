import json
import logging

from fastapi.testclient import TestClient
from prometheus_client import generate_latest

from app.core.observability import JSONFormatter, build_correlation_headers, clear_request_context, set_request_context
from app.main import app
from app.services import metrics


def test_json_formatter_includes_observability_fields():
    clear_request_context()
    set_request_context(
        request_id="req-123",
        correlation_id="corr-456",
        trace_id="trace-789",
        service="api-gateway",
        backend="backend-a",
        method="GET",
        path="/api/v1/users",
        status=200,
        latency_ms=12.3,
    )

    record = logging.LogRecord(
        name="gateway",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="request completed",
        args=(),
        exc_info=None,
    )

    payload = json.loads(JSONFormatter().format(record))

    assert payload["request_id"] == "req-123"
    assert payload["correlation_id"] == "corr-456"
    assert payload["trace_id"] == "trace-789"
    assert payload["service"] == "api-gateway"
    assert payload["backend"] == "backend-a"
    assert payload["method"] == "GET"
    assert payload["path"] == "/api/v1/users"
    assert payload["status"] == 200
    assert payload["latency"] == 12.3
    assert payload["exception"] is None


def test_build_correlation_headers_includes_request_ids_and_trace_context():
    headers = build_correlation_headers(request_id="req-1", correlation_id="corr-2")

    assert headers["X-Request-ID"] == "req-1"
    assert headers["X-Correlation-ID"] == "corr-2"
    assert "traceparent" in headers or "X-Trace-ID" in headers


def test_metrics_endpoint_returns_prometheus_output():
    with TestClient(app) as client:
        response = client.get("/api/v1/metrics")

    assert response.status_code == 200
    assert "gateway_requests_total" in response.text


def test_backend_failure_metric_is_exposed():
    metrics.BACKEND_FAILURES.labels(service="users", backend="http://localhost:8002").inc()
    output = generate_latest().decode()

    assert "gateway_backend_failures_total" in output
