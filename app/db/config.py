from app.core.settings import settings


def normalize_database_url(url: str) -> str:
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return url


def build_engine_kwargs(url: str) -> dict[str, object]:
    if url.startswith("sqlite"):
        return {"echo": settings.DATABASE_ECHO}

    return {
        "echo": settings.DATABASE_ECHO,
        "pool_pre_ping": True,
        "pool_size": settings.DATABASE_POOL_SIZE,
        "max_overflow": settings.DATABASE_MAX_OVERFLOW,
        "pool_timeout": settings.DATABASE_POOL_TIMEOUT,
        "pool_recycle": settings.DATABASE_POOL_RECYCLE_SECONDS,
    }
