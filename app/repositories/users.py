from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.db.models.user import User
from app.models.user import UserCreate, UserUpdate
from app.services.metrics import DB_QUERIES


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, data: UserCreate) -> User:
        DB_QUERIES.inc()
        user_dict = data.model_dump()
        raw_password = user_dict.pop("password", None)
        if raw_password:
            user_dict["hashed_password"] = hash_password(raw_password)

        user = User(**user_dict)
        self._session.add(user)
        await self._commit()
        await self._session.refresh(user)
        return user

    async def get(self, user_id: int) -> User | None:
        DB_QUERIES.inc()
        return await self._session.get(User, user_id)

    async def get_by_username(self, username: str) -> User | None:
        DB_QUERIES.inc()
        result = await self._session.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        DB_QUERIES.inc()
        result = await self._session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def list(self, limit: int = 50, offset: int = 0) -> list[User]:
        DB_QUERIES.inc()
        result = await self._session.execute(
            select(User).order_by(User.id).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def update(self, user_id: int, data: UserUpdate) -> User | None:
        DB_QUERIES.inc()
        user = await self.get(user_id)
        if user is None:
            return None

        update_dict = data.model_dump(exclude_unset=True)
        raw_password = update_dict.pop("password", None)
        if raw_password:
            update_dict["hashed_password"] = hash_password(raw_password)

        for field, value in update_dict.items():
            setattr(user, field, value)

        await self._commit()
        await self._session.refresh(user)
        return user

    async def delete(self, user_id: int) -> bool:
        DB_QUERIES.inc()
        user = await self.get(user_id)
        if user is None:
            return False

        await self._session.delete(user)
        await self._commit()
        return True

    async def _commit(self) -> None:
        try:
            await self._session.commit()
        except Exception:
            await self._session.rollback()
            raise
