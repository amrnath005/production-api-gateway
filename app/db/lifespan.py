async def close_database_pool() -> None:
    try:
        from app.db.session import close_database_connections
    except ImportError:
        return

    await close_database_connections()
