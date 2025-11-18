from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from ..config import settings

_engine: AsyncEngine | None = None
_session_factory: sessionmaker | None = None


async def init_db() -> None:
    """
    Initialize the global async SQLAlchemy engine and session factory.
    Safe to call multiple times.
    """
    global _engine, _session_factory
    if _engine is None:
        _engine = create_async_engine(settings.database_url, echo=False, future=True)
        _session_factory = sessionmaker(
            bind=_engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )


async def close_db() -> None:
    """Dispose the global engine (if initialized)."""
    global _engine
    if _engine is not None:
        await _engine.dispose()
        _engine = None


def get_session_factory() -> sessionmaker:
    if _session_factory is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return _session_factory


@asynccontextmanager
async def session_scope() -> AsyncGenerator[AsyncSession, None]:
    """
    Async context manager that yields a session and handles commit/rollback.
    """
    session_factory = get_session_factory()
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that yields a session per request.
    Usage: `Depends(get_session)`
    """
    session_factory = get_session_factory()
    async with session_factory() as session:
        yield session

