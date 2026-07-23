import pytest

pytest.importorskip("sqlalchemy")
pytest.importorskip("aiosqlite")

import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.health import check_database_health
from app.models.user import UserCreate, UserUpdate
from app.repositories.users import UserRepository


@pytest_asyncio.fixture
async def session_factory():
    engine = create_async_engine(
        "sqlite+aiosqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    factory = async_sessionmaker(engine, expire_on_commit=False)

    yield factory

    await engine.dispose()


@pytest.mark.asyncio
async def test_user_repository_crud(session_factory):
    async with session_factory() as session:
        repository = UserRepository(session)

        created = await repository.create(
            UserCreate(username="alice", email="alice@example.com", age=31)
        )
        fetched = await repository.get(created.id)
        listed = await repository.list()
        updated = await repository.update(created.id, UserUpdate(age=32))
        deleted = await repository.delete(created.id)

        assert fetched is not None
        assert fetched.email == "alice@example.com"
        assert listed == [created]
        assert updated is not None
        assert updated.age == 32
        assert deleted is True
        assert await repository.get(created.id) is None


@pytest.mark.asyncio
async def test_database_health_check_reports_ready(session_factory):
    health = await check_database_health(session_factory)

    assert health == {"status": "ready"}
