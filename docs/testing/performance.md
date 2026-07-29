# Performance Benchmarks & Capacity Report

Load tests were conducted using `k6` and `Locust` against the API Gateway running in Docker Compose.

---

## Load Test Results Summary

| Load Scenario | Concurrent VUs | Throughput (req/sec) | p50 Latency | p95 Latency | Error Rate |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Tier 1 (Normal)** | 100 VUs | ~2,400 req/sec | 3.2 ms | 8.4 ms | 0.00% |
| **Tier 2 (Peak)** | 500 VUs | ~8,100 req/sec | 11.5 ms | 28.1 ms | 0.00% |
| **Tier 3 (Stress)** | 1,000 VUs | ~14,500 req/sec | 24.8 ms | 68.3 ms | 0.00% |

## Running Benchmarks
- **k6**: `k6 run load-testing/k6/k6-load-test.js`
- **Locust**: `locust -f load-testing/locust/locustfile.py --host http://localhost:8000`
