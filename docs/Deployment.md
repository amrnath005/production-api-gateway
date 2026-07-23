# Production Deployment Guide

## 1. Prerequisites
- Docker Engine 24.0+
- Docker Compose v2+
- Kubernetes 1.28+ cluster with `kubectl` and `kustomize`
- PostgreSQL 16+ database
- Redis 7+ instance

## 2. Docker Compose Deployment
To run the full stack (API Gateway, User Service, Order Service, PostgreSQL, Redis, Prometheus, Grafana, Jaeger) locally:

```bash
docker-compose up --build -d
```

Check health status:
```bash
docker-compose ps
```

## 3. Kubernetes Deployment (Kustomize)
Deploy the production manifests:

```bash
kubectl apply -k k8s/base
```

Check deployment rollout:
```bash
kubectl -n production-api-gateway rollout status deployment/api-gateway
```

## 4. Environment Configuration
Ensure production secret values are set in `k8s/base/secret.yaml` or Kubernetes Secrets vault:
- `JWT_SECRET`: High-entropy 32+ character key.
- `API_KEY`: High-entropy 32+ character API Key.
- `DATABASE_URL`: Production PostgreSQL async connection string (`postgresql+asyncpg://...`).
