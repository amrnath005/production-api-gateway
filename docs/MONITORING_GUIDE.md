# Monitoring & Alerting Guide

## Overview
Monitoring combines Prometheus metric scrapers, Grafana dashboards, and automated alert conditions.

## Key Metrics Tracked
- **Requests/sec**: `rate(gateway_requests_total[1m])`
- **p95 Latency**: `histogram_quantile(0.95, sum by (le) (rate(gateway_request_duration_seconds_bucket[5m])))`
- **Error Rate**: `rate(gateway_failed_requests_total[1m])`
- **Circuit Breaker Status**: `gateway_circuit_open_total`
- **Cache Hit Ratio**: `rate(gateway_cache_hits_total[1m]) / (rate(gateway_cache_hits_total[1m]) + rate(gateway_cache_misses_total[1m]))`

## Prometheus Rules & Alerts
Prometheus automatically scrapes the `/api/v1/metrics` target every 10 seconds.
