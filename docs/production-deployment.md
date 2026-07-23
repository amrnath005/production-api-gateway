# Production Deployment

## CI/CD

GitHub Actions runs dependency installation, compilation, Alembic migrations, tests, Python dependency auditing, Docker image builds, container image scanning, and optional Kubernetes rollout.

Required repository settings for deployment:

- `ENABLE_K8S_DEPLOY=true` repository variable
- `KUBE_CONFIG` repository secret

Production secret requirements:

- `JWT_SECRET` and `API_KEY` must be at least 16 characters.
- Placeholder values such as `change-me-in-production` are rejected when `ENVIRONMENT=production`.
- `DATABASE_URL` must be explicitly configured and must not use the localhost development default.

Images are pushed to GitHub Container Registry:

- `ghcr.io/<owner>/api-gateway`
- `ghcr.io/<owner>/api-gateway-user-service`
- `ghcr.io/<owner>/api-gateway-order-service`

## Kubernetes

Apply the production base:

```bash
kubectl apply -k k8s/base
```

Before applying in production, replace placeholder hostnames, image names, and secrets. The manifests include namespace, ConfigMap, Secret, Deployments, Services, Ingress, HPA, probes, resources, Redis, PostgreSQL, and an Alembic migration job.

## NGINX and HTTPS

The NGINX production overlay expects certificate files at:

- `nginx/certs/fullchain.pem`
- `nginx/certs/privkey.pem`

Run with:

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build
```

For Kubernetes, TLS is configured through Ingress and the `api-gateway-tls` secret.

## Load testing

Run the k6 scenario:

```bash
k6 run -e BASE_URL=https://api-gateway.example.com -e API_KEY=<api-key> load-testing/k6-gateway.js
```

The load profile validates health and user creation while enforcing p95 and p99 latency thresholds.

## Rollback

Use Kubernetes rollout history:

```bash
kubectl -n production-api-gateway rollout undo deployment/api-gateway
```
