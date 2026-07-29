# Async PostgreSQL & SQLAlchemy 2.x Integration

Database operations use async SQLAlchemy 2.x sessions managed by `async_sessionmaker` in [app/db/session.py](file:///c:/Users/salte/OneDrive/Desktop/api-gateway-project/app/db/session.py).

---

## Connection Pool Tuning
- **Engine**: `postgresql+asyncpg`
- **Pool Size**: `10`
- **Max Overflow**: `20`
- **Pool Timeout**: `30s`
- **Pool Recycle**: `1800s`
- **Pre-Ping**: `True` (Health check ping prior to query checkout)

## Schema & Repository Pattern
User data access is encapsulated within `UserRepository` ([app/repositories/users.py](file:///c:/Users/salte/OneDrive/Desktop/api-gateway-project/app/repositories/users.py)) enforcing transaction isolation and incrementing the `gateway_db_queries_total` Prometheus counter.
