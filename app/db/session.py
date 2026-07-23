from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.settings import settings
from app.db.config import build_engine_kwargs, normalize_database_url


DATABASE_URL = normalize_database_url(settings.DATABASE_URL)
engine = create_async_engine(DATABASE_URL, **build_engine_kwargs(DATABASE_URL))
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
