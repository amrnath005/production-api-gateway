# Load Testing & Benchmark Instructions

## k6 Load Testing
Run the multi-tier k6 load test:
```bash
k6 run load-testing/k6/k6-load-test.js
```

## Locust Load Testing
Run Locust interactive load test:
```bash
locust -f load-testing/locust/locustfile.py --host http://localhost:8000
```
Access Locust UI at `http://localhost:8089`.
