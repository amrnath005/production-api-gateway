# API Gateway Reference & Route Catalog

## Public Endpoints

### 1. Health Checks
- `GET /api/v1/health`: Basic liveness check. Returns `{"status": "healthy"}`.
- `GET /api/v1/health/db`: Database readiness check. Returns `{"status": "ready"}`.
- `GET /api/v1/ready`: Full system readiness check (Database & Redis).

### 2. Authentication
- `POST /login`: Request JWT access token.
  - **Body**: `{"username": "admin", "password": "yourpassword"}`
  - **Response**: `{"access_token": "<jwt>", "token_type": "bearer"}`

## Protected Endpoints

- `GET /profile`: Requires Bearer JWT header (`Authorization: Bearer <token>`). Returns active user profile claims.
- `GET /admin`: Requires Bearer JWT header with `role: admin`.

## User Management Endpoints (`/api/v1/users`)

- `POST /api/v1/users`: Create user (Requires `X-API-Key` header).
- `GET /api/v1/users`: List users (Requires `X-API-Key` header).
- `GET /api/v1/users/{id}`: Get user by ID.
- `PATCH /api/v1/users/{id}`: Update user fields.
- `DELETE /api/v1/users/{id}`: Delete user.

## Proxy Endpoints (`/api/v1/{service}/{path}`)

Dynamic proxy routing for registered microservices (`users`, `orders`):
- `GET /api/v1/users/info` -> Proxies to `USER_SERVICE_URL/users/info`
- `GET /api/v1/orders/123` -> Proxies to `ORDER_SERVICE_URL/orders/123`
