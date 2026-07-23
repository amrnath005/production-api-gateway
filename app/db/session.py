from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.settings import settings
from app.db.config import build_engine_kwargs, normalize_database_url


DATABASE_URL = normalize_database_url(settings.get_database_url())


def _create_engine_instance():
    try:
        return create_async_engine(DATABASE_URL, **build_engine_kwargs(DATABASE_URL))
    except Exception:
        fallback_url = "sqlite+aiosqlite://"
        return create_async_engine(fallback_url, **build_engine_kwargs(fallback_url))


engine = _create_engine_instance()
async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


@asynccontextmanager
async def session_scope() -> AsyncIterator[AsyncSession]:
    async with async_session_maker() as session:
        yield session


async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_session_maker() as session:
        yield session


async def close_database_connections() -> None:
    await engine.dispose()
