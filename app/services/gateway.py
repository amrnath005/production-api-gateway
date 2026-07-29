import httpx
from opentelemetry import trace

from app.core.exceptions import BackendTimeoutError
from app.core.observability import set_request_context
from app.core.routes import SERVICE_REGISTRY
from app.core.settings import settings

from app.services.circuit_breaker import circuit_breaker
from app.services.load_balancer import load_balancer
from app.services.retry import retry_service
from app.services.metrics import BACKEND_FAILURES, BACKEND_REQUESTS

tracer = trace.get_tracer("gateway.gateway_service")

HOP_BY_HOP_HEADERS = {
    "host",
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailers",
    "transfer-encoding",
    "upgrade",
    "content-length",
}


def sanitize_forward_headers(headers: dict) -> dict:
    """Filter out hop-by-hop headers before forwarding requests to backend services."""

    return {
        k: v for k, v in headers.items()
        if k.lower() not in HOP_BY_HOP_HEADERS
    }


class GatewayService:

    def __init__(self) -> None:
        self._client = httpx.AsyncClient(
            timeout=settings.REQUEST_TIMEOUT,
            limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
        )

    async def close(self) -> None:
        await self._client.aclose()

    async def forward_request(
        self,
        service: str,
        method: str,
        path: str,
        headers: dict,
        params: dict,
        body: bytes | None,
    ):

        backend_url = await load_balancer.get_next_instance(
            service_name=service,
            instances=SERVICE_REGISTRY[service],
        )

        target_url = f"{backend_url}/{service}"
        set_request_context(backend=backend_url)

        if path:
            target_url += f"/{path}"

        forward_headers = sanitize_forward_headers(headers)

        circuit_breaker.before_request(backend_url)

        with tracer.start_as_current_span("gateway.forward_request") as span:
            span.set_attribute("gateway.service", service)
            span.set_attribute("gateway.backend", backend_url)
            span.set_attribute("gateway.path", path or "/")

            try:

                async def send():

                    BACKEND_REQUESTS.labels(
                        service=service,
                        backend=backend_url,
                    ).inc()

                    return await self._client.request(
                        method=method,
                        url=target_url,
                        headers=forward_headers,
                        params=params,
                        content=body,
                    )

                response = await retry_service.execute(send)

                circuit_breaker.record_success(backend_url)

                return response

            except httpx.TimeoutException as exc:
                circuit_breaker.record_failure(backend_url)
                BACKEND_FAILURES.labels(service=service, backend=backend_url).inc()
                raise BackendTimeoutError(service) from exc

            except (
                httpx.ConnectError,
                httpx.NetworkError,
            ) as exc:

                circuit_breaker.record_failure(backend_url)
                BACKEND_FAILURES.labels(service=service, backend=backend_url).inc()
                raise exc


gateway_service = GatewayService()