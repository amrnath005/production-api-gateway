# Kubernetes Deployment

This directory contains the production kustomize base for the API Gateway platform.

## Apply

```bash
kubectl apply -k k8s/base
```

## Production checklist

- Replace placeholder image names in `k8s/base/*.yaml`.
- Replace `api-gateway.example.com` with the production DNS name.
- Replace `api-gateway-secrets` values with externally managed secrets.
- Prefer a managed PostgreSQL service for production; the included StatefulSet is suitable for self-hosted clusters and non-managed environments.
- Run the migration job before rolling out a new gateway image that requires schema changes.

## Probes

- Liveness: `GET /api/v1/health`
- Readiness: `GET /api/v1/ready`
- Database health: `GET /api/v1/health/db`
