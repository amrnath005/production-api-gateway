# Grafana Dashboard Provisioning Guide

## Dashboards Provisioned
Grafana automatically provisions 10 production-grade dashboards:
1. **Gateway Overview**: High-level throughput, latency, error rates.
2. **HTTP Requests**: Quantile latency (p50, p95, p99) and status code breakdown.
3. **Redis Cache**: Hit/miss rates and Redis operation latency.
4. **Database Performance**: Query rates and active DB connections.
5. **Authentication**: Login attempts and token issue rates.
6. **Rate Limiter**: HTTP 429 rate-limiting events.
7. **Circuit Breaker**: Tripped states and backend recovery timeout monitoring.
8. **Infrastructure**: Healthy vs unhealthy instance metrics.
9. **Application Health**: Core readiness status.
10. **Errors**: Detailed 4xx and 5xx failure breakdown.
