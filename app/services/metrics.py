from prometheus_client import Counter, Gauge, Histogram

CACHE_HITS = Counter(
    "gateway_cache_hits_total",
    "Total cache hits",
)

CACHE_MISSES = Counter(
    "gateway_cache_misses_total",
    "Total cache misses",
)

CACHE_HIT_RATIO = Gauge(
    "gateway_cache_hit_ratio",
    "Current cache hit ratio",
)

CACHE_LATENCY = Histogram(
    "gateway_cache_latency_seconds",
    "Cache operation latency",
)

REDIS_CONNECTIONS = Gauge(
    "gateway_redis_connections",
    "Current Redis connections",
)

CACHED_RESPONSES = Counter(
    "gateway_cached_responses_total",
    "Number of responses cached",
)

COMPRESSION_USAGE = Counter(
    "gateway_compression_total",
    "Number of compressed responses",
)

REQUEST_COUNT = Counter(
    "gateway_requests_total",
    "Total number of requests",
    ["method", "endpoint", "status"],
)

REQUEST_LATENCY = Histogram(
    "gateway_request_duration_seconds",
    "Request latency",
    ["method", "endpoint"],
)

ACTIVE_REQUESTS = Gauge(
    "gateway_active_requests",
    "Number of active requests being processed",
)

BACKEND_REQUESTS = Counter(
    "backend_requests_total",
    "Requests sent to backend",
    ["service", "backend"],
)

BACKEND_FAILURES = Counter(
    "gateway_backend_failures_total",
    "Failed backend requests",
    ["service", "backend"],
)

RETRY_COUNT = Counter(
    "gateway_retry_total",
    "Retry attempts",
)

CIRCUIT_OPEN = Counter(
    "gateway_circuit_open_total",
    "Circuit breaker opened",
)

FAILED_REQUESTS = Counter(
    "gateway_failed_requests_total",
    "Failed gateway requests",
    ["method", "endpoint", "status"],
)

SUCCESSFUL_REQUESTS = Counter(
    "gateway_successful_requests_total",
    "Successful gateway requests",
    ["method", "endpoint", "status"],
)

HEALTHY_INSTANCES = Gauge(
    "gateway_healthy_instances",
    "Number of healthy backend instances",
)

UNHEALTHY_INSTANCES = Gauge(
    "gateway_unhealthy_instances",
    "Number of unhealthy backend instances",
)

LAST_HEALTH_CHECK = Gauge(
    "gateway_last_health_check_timestamp",
    "Last health check timestamp",
)

HEALTH_CHECK_DURATION = Histogram(
    "gateway_health_check_duration_seconds",
    "Health check latency",
    ["backend"],
)

BACKEND_AVAILABILITY = Gauge(
    "gateway_backend_availability",
    "Availability state of backend instances",
    ["backend"],
)