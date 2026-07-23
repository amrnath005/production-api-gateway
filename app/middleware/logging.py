import logging
import time
import uuid

from fastapi import Request
from opentelemetry import trace

from app.core.observability import clear_request_context, current_trace_id, set_request_context
from app.services.metrics import ACTIVE_REQUESTS

logger = logging.getLogger("gateway")
tracer = trace.get_tracer("gateway.middleware")


async def log_requests(request: Request, call_next):
    """Attach request IDs and emit structured JSON logs with trace context."""

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
        try:
            response = await call_next(request)
        except Exception as exc:
            latency_ms = round((time.perf_counter() - start_time) * 1000, 3)
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
        return response