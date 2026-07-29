# Business Logic & Gateway Services

Summary of core services in `app/services/`:

1. **`GatewayService`**: Shared `httpx.AsyncClient` HTTP proxy execution engine.
2. **`CircuitBreaker`**: State machine (`CLOSED`, `OPEN`, `HALF_OPEN`) tracking failure thresholds per backend URL.
3. **`RetryService`**: Exponential backoff retry loop (0.1s, 0.2s, 0.4s) handling transient network timeouts.
4. **`RoundRobinLoadBalancer`**: Distributes traffic evenly across healthy microservice instances.
5. **`HealthMonitor`**: Background task checking downstream instance health every 10s and exporting availability gauges.
6. **`PerformanceService`**: Generates ETags (`304 Not Modified`) and handles Gzip compression.
