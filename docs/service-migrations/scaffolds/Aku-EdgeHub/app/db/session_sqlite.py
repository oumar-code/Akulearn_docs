"""SQLite async session — replaces the default asyncpg session for offline mode."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# check_same_thread is a SQLite-only connect arg; asyncpg rejects it.
_connect_args: dict = (
    {"check_same_thread": False}
    if settings.database_url.startswith("sqlite")
    else {}
)

engine: AsyncEngine = create_async_engine(
    settings.database_url,
    connect_args=_connect_args,
    echo=settings.db_echo,
)

AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    pass


async def init_db() -> None:
    """Create all tables on startup (SQLite schema bootstrap)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency — yields an async SQLite session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
