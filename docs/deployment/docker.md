# Docker Multi-Stage Builds & Container Architecture

The gateway [Dockerfile](file:///c:/Users/salte/OneDrive/Desktop/api-gateway-project/Dockerfile) uses a 2-stage multi-stage build:

1. **`builder` stage**: Installs dependencies into `--prefix=/install` with `--ignore-installed`.
2. **`runtime` stage**: Copies `/install` into standard `/usr/local` on a clean `python:3.12-slim` base, dropping build dependencies and running as non-root `appuser`.

## Container Network Architecture
All containers communicate over the isolated `app-network` bridge. Service discovery uses container names (`postgres`, `redis`, `user-service`, `order-service`).
