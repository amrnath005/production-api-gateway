# Persistence

The gateway uses PostgreSQL with SQLAlchemy 2.x async sessions and Alembic migrations.

## Runtime configuration

- `DATABASE_URL`
- `DATABASE_POOL_SIZE`
- `DATABASE_MAX_OVERFLOW`
- `DATABASE_POOL_TIMEOUT`
- `DATABASE_POOL_RECYCLE_SECONDS`
- `DATABASE_ECHO`

`postgresql://` URLs are normalized to `postgresql+asyncpg://` at runtime for async operation.

## Migrations

```bash
alembic upgrade head
```

The first migration creates the `users` table used by the CRUD example.

## Health checks

- `GET /api/v1/health` keeps the existing lightweight liveness response.
- `GET /api/v1/health/db` verifies database connectivity with `SELECT 1`.
- `GET /api/v1/ready` checks database and Redis readiness.

## CRUD example

The `/api/v1/users` resource is backed by `UserRepository` and async SQLAlchemy sessions. All user CRUD endpoints retain API-key protection.
