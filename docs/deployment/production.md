# Production Deployment Manual

## 1. Environment Secrets Setup
In production, set high-entropy secrets in your environment or Kubernetes Secret vault:
- `ENVIRONMENT=production`
- `JWT_SECRET=<32+_character_random_string>`
- `API_KEY=<32+_character_random_string>`
- `DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/dbname`

## 2. Kubernetes Deployment
Deploy using Kustomize manifests under `k8s/base/`:

```bash
kubectl apply -k k8s/base
```
Includes Deployment, Service, ConfigMap, Secret, Ingress, HPA, and Liveness/Readiness probes.
