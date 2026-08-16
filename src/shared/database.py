from typing import Annotated, AsyncIterator, TypeVar

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlmodel import SQLModel, select

from src.shared.config import settings

ModelT = TypeVar("ModelT", bound=SQLModel)

engine = create_async_engine(
    settings.DB_URL,
    echo=False,
    pool_pre_ping=True,
)

SessionFactory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_session() -> AsyncIterator[AsyncSession]:
    """FastAPI dependency yielding a scoped session."""
    async with SessionFactory() as session:
        yield session


DbSession = Annotated[AsyncSession, Depends(get_session)]


async def init_db() -> None:
    """Create tables for all registered models. Generic, no domain imports.

    Callers must import every model module before this runs so the
    SQLModel metadata registry is fully populated.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def commit_or_rollback(session: AsyncSession) -> None:
    """Commit; roll back and re-raise if anything goes wrong."""
    try:
        await session.commit()
    except Exception:
        await session.rollback()
        raise


async def get_by_id(session: AsyncSession, model: type[ModelT], pk) -> ModelT | None:
    return await session.get(model, pk)


async def get_all(
    session: AsyncSession,
    model: type[ModelT],
    *,
    order_by=None,
) -> list[ModelT]:
    stmt = select(model)
    if order_by is not None:
        stmt = stmt.order_by(order_by)
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def add(session: AsyncSession, obj: ModelT) -> ModelT:
    session.add(obj)
    await session.flush()
    await session.refresh(obj)
    return obj
