# API Reference Specification

The Gateway exposes standard REST endpoints alongside dynamic microservice proxy routes.

---

## 1. System & Health Endpoints

### `GET /api/v1/health`
Basic liveness probe.
- **Authentication**: Public
- **Response `200 OK`**:
  ```json
  {
    "status": "healthy"
  }
  ```

### `GET /ready`
System readiness check verifying PostgreSQL and Redis status.
- **Authentication**: Public
- **Response `200 OK`**:
  ```json
  {
    "status": "ready",
    "checks": {
      "database": { "status": "ready" },
      "cache": { "status": "ready", "url": "redis://redis:6379/0" }
    }
  }
  ```

---

## 2. Authentication & User Management

### `POST /login`
Exchanges user credentials for a JWT Bearer token.
- **Request Body**:
  ```json
  {
    "username": "admin",
    "password": "admin123"
  }
  ```
- **Response `200 OK`**:
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
  ```

### `GET /profile`
Returns claims for authenticated user.
- **Headers**: `Authorization: Bearer <token>`
- **Response `200 OK`**:
  ```json
  {
    "message": "Authenticated Successfully",
    "username": "admin",
    "role": "admin"
  }
  ```

---

## 3. User Management CRUD (`/api/v1/users`)

### `POST /api/v1/users`
- **Headers**: `X-API-Key: <configured_key>`
- **Request Body**:
  ```json
  {
    "username": "alice",
    "email": "alice@example.com",
    "password": "SecretPassword123!",
    "role": "user"
  }
  ```
- **Response `201 Created`**:
  ```json
  {
    "id": 1,
    "username": "alice",
    "email": "alice@example.com",
    "is_active": true,
    "role": "user",
    "created_at": "2026-07-29T10:00:00Z"
  }
  ```

---

## 4. Cache Management (`/api/v1/cache`)

### `DELETE /api/v1/cache/invalidate`
Invalidates cached GET responses by key or pattern.
- **Query Params**: `key=cache:...` or `pattern=cache:*`
- **Response `200 OK`**:
  ```json
  {
    "status": "ok",
    "deleted": 1
  }
  ```
