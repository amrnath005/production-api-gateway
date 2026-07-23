import pytest
from app.core.exceptions import (
    BackendTimeoutError,
    CircuitOpenError,
    GatewayException,
    ServiceUnavailableError,
)


def test_gateway_exception_status_codes():
    exc = GatewayException("Error message", status_code=500)
    assert exc.status_code == 500
    assert str(exc) == "Error message"

    circuit_exc = CircuitOpenError("http://localhost:8002")
    assert circuit_exc.status_code == 503
    assert "Circuit breaker is OPEN" in circuit_exc.message

    svc_exc = ServiceUnavailableError("users")
    assert svc_exc.status_code == 503
    assert "users" in svc_exc.message

    timeout_exc = BackendTimeoutError("orders")
    assert timeout_exc.status_code == 504
    assert "orders" in timeout_exc.message
