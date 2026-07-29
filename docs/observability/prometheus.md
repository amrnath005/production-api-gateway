# Prometheus Metrics Integration

Prometheus scrapes the API Gateway every 10 seconds.

---

## Configuration (`prometheus.yml`)

```yaml
global:
  scrape_interval: 10s

scrape_configs:
  - job_name: "api-gateway"
    metrics_path: "/api/v1/metrics"
    static_configs:
      - targets: ["gateway:8000"]
```

Target endpoint `GET /api/v1/metrics` exposes Prometheus exposition format text output.
