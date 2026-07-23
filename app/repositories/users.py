from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.models.user import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, data: UserCreate) -> User:
        user = User(**data.model_dump())
        self._session.add(user)
        await self._commit()
        await self._session.refresh(user)
        return user

    async def get(self, user_id: int) -> User | None:
        return await self._session.get(User, user_id)

    async def get_by_email(self, email: str) -> User | None:
        result = await self._session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def list(self, limit: int = 50, offset: int = 0) -> list[User]:
        result = await self._session.execute(
            select(User).order_by(User.id).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def update(self, user_id: int, data: UserUpdate) -> User | None:
        user = await self.get(user_id)
        if user is None:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)

        await self._commit()
        await self._session.refresh(user)
        return user

    async def delete(self, user_id: int) -> bool:
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
