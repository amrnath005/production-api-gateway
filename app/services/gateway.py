import httpx
from opentelemetry import trace

from app.core.observability import set_request_context
from app.core.routes import SERVICE_REGISTRY
from app.core.settings import settings

from app.services.circuit_breaker import circuit_breaker
from app.services.load_balancer import load_balancer
from app.services.retry import retry_service
from app.services.metrics import BACKEND_FAILURES, BACKEND_REQUESTS, FAILED_REQUESTS, REQUEST_COUNT, REQUEST_LATENCY, SUCCESSFUL_REQUESTS

tracer = trace.get_tracer("gateway.gateway_service")


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
                        headers=headers,
                        params=params,
                        content=body,
                    )

                response = await retry_service.execute(send)

                circuit_breaker.record_success(backend_url)
                REQUEST_COUNT.labels(method=method, endpoint=path or "/", status=response.status_code).inc()
                REQUEST_LATENCY.labels(method=method, endpoint=path or "/").observe(response.elapsed.total_seconds())
                SUCCESSFUL_REQUESTS.labels(method=method, endpoint=path or "/", status=response.status_code).inc()

                return response

            except (
                httpx.ConnectError,
                httpx.TimeoutException,
                httpx.NetworkError,
            ) as exc:

                circuit_breaker.record_failure(backend_url)
                BACKEND_FAILURES.labels(service=service, backend=backend_url).inc()
                REQUEST_COUNT.labels(method=method, endpoint=path or "/", status="5xx").inc()
                FAILED_REQUESTS.labels(method=method, endpoint=path or "/", status="5xx").inc()
                raise exc


gateway_service = GatewayService()