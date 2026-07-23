from typing import Generic, Protocol, TypeVar

ModelT = TypeVar("ModelT")


class Repository(Protocol, Generic[ModelT]):
    async def get(self, entity_id: int) -> ModelT | None:
        ...

    async def delete(self, entity_id: int) -> bool:
        ...
