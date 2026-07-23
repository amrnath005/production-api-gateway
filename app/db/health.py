from typing import Any

from sqlalchemy import text


async def check_database_health(session_factory: Any | None = None) -> dict[str, Any]:
    if session_factory is None:
        from app.db.session import async_session_maker

        session_factory = async_session_maker

    try:
        async with session_factory() as session:
            await session.execute(text("SELECT 1"))
        return {"status": "ready"}
    except Exception as exc:
        return {
            "status": "unavailable",
            "error": exc.__class__.__name__,
        }
