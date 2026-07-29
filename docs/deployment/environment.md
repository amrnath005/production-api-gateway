# Environment Configuration Reference

Configuration is managed by `app/core/settings.py` via `pydantic-settings`.

| Variable Name | Default Value | Description |
| :--- | :--- | :--- |
| `APP_NAME` | `api-gateway` | Service name |
| `APP_VERSION` | `1.0.0` | Service version |
| `ENVIRONMENT` | `development` | Deployment environment (`development` / `production`) |
| `JWT_SECRET` | *Local Dev Key* | Secret for signing JWTs (`SecretStr`) |
| `API_KEY` | *Local Dev Key* | Master API Key (`SecretStr`) |
| `REDIS_URL` | `redis://localhost:6379/0` | Async Redis connection string |
| `DATABASE_URL` | `postgresql+asyncpg://...` | PostgreSQL async connection string (`SecretStr`) |
| `DATABASE_POOL_SIZE` | `10` | SQLAlchemy idle pool size |
| `DATABASE_MAX_OVERFLOW` | `20` | Max overflow pool connections |
| `RATE_LIMIT` | `100` | Allowed requests per window |
| `RATE_LIMIT_WINDOW` | `60` | Sliding rate limit window (seconds) |
| `CACHE_TTL_SECONDS` | `60` | Default GET response cache TTL |
