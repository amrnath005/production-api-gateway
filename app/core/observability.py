import json
import logging
import logging.config
import os
import threading
import traceback
import uuid
from contextvars import ContextVar
from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation import fastapi as fastapi_instrumentation
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.sdk.resources import Resource
from starlette.routing import Match
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

from app.core.settings import settings

_request_context: ContextVar[dict[str, Any]] = ContextVar(
    "request_context",
    default={},
)

_TRACING_CONFIGURED = False
_LOCK = threading.Lock()


class JSONFormatter(logging.Formatter):
    """Emit JSON logs with request correlation and tracing fields."""

    def format(self, record: logging.LogRecord) -> str:
        context = _request_context.get()
        payload: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "message": record.getMessage(),
            "request_id": context.get("request_id"),
            "trace_id": context.get("trace_id"),
            "correlation_id": context.get("correlation_id"),
            "service": context.get("service") or settings.APP_NAME,
            "backend": context.get("backend"),
            "method": context.get("method"),
            "path": context.get("path"),
            "status": context.get("status"),
            "latency": context.get("latency_ms"),
            "exception": None,
        }

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        elif getattr(record, "exception", None):
            payload["exception"] = str(record.exception)

        for key in ("request_id", "trace_id", "correlation_id", "service", "backend", "method", "path", "status", "latency"):
            if key in record.__dict__:
                payload[key] = record.__dict__[key]

        return json.dumps(payload, default=str)


def configure_logging() -> None:
    """Configure structured JSON logging for the gateway."""

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {"()": "app.core.observability.JSONFormatter"},
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "json",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "gateway": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
        },
    }

    logging.config.dictConfig(logging_config)


def configure_tracing(app: FastAPI) -> None:
    """Initialize OpenTelemetry tracing and instrument FastAPI and httpx."""

    global _TRACING_CONFIGURED
    if _TRACING_CONFIGURED:
        return

    with _LOCK:
        if _TRACING_CONFIGURED:
            return

        resource = Resource.create(
            {
                "service.name": settings.APP_NAME,
                "service.version": settings.APP_VERSION,
                "deployment.environment": settings.ENVIRONMENT,
            }
        )
        tracer_provider = TracerProvider(resource=resource)
        jaeger_endpoint = os.getenv("JAEGER_ENDPOINT", "http://localhost:14268/api/traces")

        try:
            jaeger_exporter = JaegerExporter(collector_endpoint=jaeger_endpoint)
            tracer_provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
        except Exception:
            tracer_provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

        trace.set_tracer_provider(tracer_provider)

        FastAPIInstrumentor.instrument_app(app)
        HTTPXClientInstrumentor().instrument()

        try:
            original_get_route_details = fastapi_instrumentation._get_route_details
        except AttributeError:
            original_get_route_details = None

        if original_get_route_details is not None:
            def _safe_get_route_details(scope):
                app_instance = scope.get("app")
                route = None

                if app_instance is None:
                    return None

                for starlette_route in getattr(app_instance, "routes", []):
                    try:
                        match, _ = starlette_route.matches(scope)
                    except Exception:
                        continue

                    if match == Match.FULL:
                        route = getattr(starlette_route, "path", None)
                        if route is not None:
                            return route

                try:
                    return original_get_route_details(scope)
                except AttributeError:
                    return None

            fastapi_instrumentation._get_route_details = _safe_get_route_details

        _TRACING_CONFIGURED = True


def set_request_context(**values: Any) -> Any:
    """Store request-scoped observability fields in a context variable."""

    context = dict(_request_context.get())
    context.update(values)
    _request_context.set(context)
    return context


def clear_request_context(token: Any | None = None) -> None:
    """Clear the request context after a request completes."""

    if token is None:
        _request_context.set({})
        return

    _request_context.set({})


def get_request_context() -> dict[str, Any]:
    """Return the current request-scoped observability context."""

    return dict(_request_context.get())


def build_correlation_headers(
    request_id: str | None = None,
    correlation_id: str | None = None,
    trace_id: str | None = None,
) -> dict[str, str]:
    """Build headers for downstream backend propagation."""

    context = get_request_context()
    request_id = request_id or context.get("request_id") or str(uuid.uuid4())
    correlation_id = correlation_id or context.get("correlation_id") or request_id
    trace_id = trace_id or context.get("trace_id")

    headers = {
        "X-Request-ID": request_id,
        "X-Correlation-ID": correlation_id,
    }

    if trace_id:
        headers["X-Trace-ID"] = trace_id

    span_context = trace.get_current_span().get_span_context()
    if span_context.is_valid:
        headers["traceparent"] = (
            f"00-{span_context.trace_id:032x}-{span_context.span_id:016x}-01"
        )

    return headers


def current_trace_id() -> str | None:
    """Return the active trace ID if one exists."""

    span_context = trace.get_current_span().get_span_context()
    if span_context.is_valid:
        return f"{span_context.trace_id:032x}"

    context = get_request_context()
    return context.get("trace_id")
