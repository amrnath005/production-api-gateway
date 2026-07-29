import logging
import re
import time
import uuid

from fastapi import Request
from opentelemetry import trace

from app.core.observability import clear_request_context, current_trace_id, set_request_context
from app.services.metrics import (
    ACTIVE_REQUESTS,
    FAILED_REQUESTS,
    REQUEST_COUNT,
    REQUEST_LATENCY,
    SUCCESSFUL_REQUESTS,
)

logger = logging.getLogger("gateway")
tracer = trace.get_tracer("gateway.middleware")

UUID_RE = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")


def get_normalized_endpoint(request: Request) -> str:
    """Extract a low-cardinality endpoint string for Prometheus metrics."""

    route = request.scope.get("route")
    if route and getattr(route, "path", None):
        return route.path

    path = request.url.path
    segments = path.strip("/").split("/")
    if not segments or segments == [""]:
        return "/"

    normalized = []
    for segment in segments:
        if segment.isdigit() or UUID_RE.match(segment):
            normalized.append("{id}")
        else:
            normalized.append(segment)

    return "/" + "/".join(normalized)


async def log_requests(request: Request, call_next):
    """Attach request IDs, emit structured JSON logs, and record global Prometheus metrics."""

    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    correlation_id = request.headers.get("X-Correlation-ID") or request_id

    with tracer.start_as_current_span(f"{request.method} {request.url.path}") as span:
        trace_id = current_trace_id() or f"{span.get_span_context().trace_id:032x}" or request_id

        set_request_context(
            request_id=request_id,
            correlation_id=correlation_id,
            trace_id=trace_id,
            service="api-gateway",
            method=request.method,
            path=request.url.path,
        )

        ACTIVE_REQUESTS.inc()
        start_time = time.perf_counter()
        response = None
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            process_time = time.perf_counter() - start_time
            latency_ms = round(process_time * 1000, 3)
            endpoint = get_normalized_endpoint(request)

            REQUEST_COUNT.labels(method=request.method, endpoint=endpoint, status="500").inc()
            REQUEST_LATENCY.labels(method=request.method, endpoint=endpoint).observe(process_time)
            FAILED_REQUESTS.labels(method=request.method, endpoint=endpoint, status="500").inc()

            logger.exception(
                "request_failed",
                extra={
                    "request_id": request_id,
                    "correlation_id": correlation_id,
                    "trace_id": trace_id,
                    "service": "api-gateway",
                    "method": request.method,
                    "path": request.url.path,
                    "status": 500,
                    "latency_ms": latency_ms,
                    "exception": exc,
                },
            )
            raise
        finally:
            ACTIVE_REQUESTS.dec()
            process_time = time.perf_counter() - start_time
            latency_ms = round(process_time * 1000, 3)

            if response is not None:
                endpoint = get_normalized_endpoint(request)
                status_str = str(response.status_code)

                REQUEST_COUNT.labels(method=request.method, endpoint=endpoint, status=status_str).inc()
                REQUEST_LATENCY.labels(method=request.method, endpoint=endpoint).observe(process_time)

                if response.status_code >= 400:
                    FAILED_REQUESTS.labels(method=request.method, endpoint=endpoint, status=status_str).inc()
                else:
                    SUCCESSFUL_REQUESTS.labels(method=request.method, endpoint=endpoint, status=status_str).inc()

                response.headers["X-Request-ID"] = request_id
                response.headers["X-Correlation-ID"] = correlation_id

                logger.info(
                    "request_completed",
                    extra={
                        "request_id": request_id,
                        "correlation_id": correlation_id,
                        "trace_id": trace_id,
                        "service": "api-gateway",
                        "method": request.method,
                        "path": request.url.path,
                        "status": response.status_code,
                        "latency_ms": latency_ms,
                    },
                )

            clear_request_context()