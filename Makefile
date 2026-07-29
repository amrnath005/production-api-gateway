.PHONY: up down logs test benchmark metrics dashboard traces clean

up:
	docker compose up -d --build

down:
	docker compose down -v

logs:
	docker compose logs -f gateway

test:
	python -m pytest

benchmark:
	k6 run load-testing/k6/k6-load-test.js

metrics:
	@echo "Prometheus: http://localhost:9090"
	@curl -s http://localhost:8000/api/v1/metrics | head -n 20

dashboard:
	@echo "Opening Grafana Dashboards: http://localhost:3000"

traces:
	@echo "Opening Jaeger UI: http://localhost:16686"

clean:
	docker compose down --remove-orphans -v
	find . -type d -name "__pycache__" -exec rm -rf {} +
