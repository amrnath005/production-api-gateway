# Grafana Dashboard Provisioning

Grafana (`http://localhost:3000`) is pre-configured with anonymous admin auto-login (`GF_AUTH_ANONYMOUS_ENABLED: "true"`).

---

## 10 Provisioned Dashboards
1. **Gateway Overview**: Request volume, p95 latency, error rate, active connections.
2. **HTTP Requests**: Quantile latency breakdown (p50, p95, p99) & HTTP status code distribution.
3. **Redis Cache**: Hit/miss rates, cache latency, cached payload counts.
4. **Database Performance**: DB health state (`gateway_db_status`) & query execution rate (`gateway_db_queries_total`).
5. **Authentication**: Login attempt status codes.
6. **Rate Limiter**: HTTP 429 rate limit response rates.
7. **Circuit Breaker**: Tripped states & recovery.
8. **Infrastructure**: Healthy vs unhealthy instance metrics.
9. **Application Health**: Core readiness status.
10. **Errors**: 4xx and 5xx failure breakdown.
