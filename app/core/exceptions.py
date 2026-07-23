class GatewayException(Exception):
    """Base exception for all API Gateway domain errors."""

    def __init__(self, message: str, status_code: int = 500) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class CircuitOpenError(GatewayException):
    """Raised when a circuit breaker for a backend service is OPEN."""

    def __init__(self, backend: str) -> None:
        super().__init__(
            message=f"Circuit breaker is OPEN for backend service '{backend}'.",
            status_code=503,
        )
        self.backend = backend


class ServiceUnavailableError(GatewayException):
    """Raised when no healthy backend instances are available."""

    def __init__(self, service_name: str) -> None:
        super().__init__(
            message=f"All backend instances for service '{service_name}' are unavailable.",
            status_code=503,
        )
        self.service_name = service_name


class BackendTimeoutError(GatewayException):
    """Raised when a request to a downstream backend service times out."""

    def __init__(self, service_name: str) -> None:
        super().__init__(
            message=f"Timeout waiting for response from backend service '{service_name}'.",
            status_code=504,
        )
        self.service_name = service_name
