# Prometheus Metrics Configuration Guide

## Configuration
Prometheus scrapes the API Gateway every 10 seconds via `prometheus.yml`:

```yaml
global:
  scrape_interval: 10s

scrape_configs:
  - job_name: "api-gateway"
    metrics_path: "/api/v1/metrics"
    static_configs:
      - targets: ["gateway:8000"]
```
