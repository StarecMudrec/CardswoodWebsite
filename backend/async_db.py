"""Async DB: PostgreSQL (AsyncSession) and SQLite (aiosqlite) for read-only cards."""
import os
from contextlib import asynccontextmanager
import aiosqlite
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from config import Config

# PostgreSQL async
async_engine = create_async_engine(
    Config.ASYNC_DATABASE_URI,
    echo=os.environ.get("SQL_ECHO", "").lower() in ("1", "true"),
)
async_session_factory = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
)


@asynccontextmanager
async def get_async_session():
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# SQLite path (read-only cards DB)
SQLITE_DB_PATH = getattr(Config, "SQLITE_DB_PATH", "/app/db/offcardswood.db")


@asynccontextmanager
async def get_sqlite_conn():
    """Async context manager for read-only SQLite (cards)."""
    conn = await aiosqlite.connect(f"file:{SQLITE_DB_PATH}?mode=ro", uri=True)
    try:
        conn.row_factory = aiosqlite.Row
        yield conn
    finally:
        await conn.close()
