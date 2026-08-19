from typing import Annotated, TypeVar

from fastapi import Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlmodel import SQLModel

from sentinel.shared.config import settings

# --- Typevar placeholder for SqlModel objects ---
Model = TypeVar("Model", bound=SQLModel)


# --- Engine ----
# A note on config params used in this
# pool_size -> persistent connection kept open
# max_overflow -> extra connections when pool_size is exhausted, Total = max_overflow + pool_size
# pool connection -> time (seconds) to wait for free connection, if no connection raise error
# pool_recycle -> recycle connections
# pool_pre_ping -> select(1) before handing connections
# echo -> print sql on terminal
db_engine = create_async_engine(
    settings.database.async_url,
    echo=False,
    pool_size=10,
    max_overflow=10,
    pool_timeout=20,
    pool_recycle=1800,
    pool_pre_ping=True,
)


# --- session factory ----
# expire_on_commit: False — objects remain usable after commit.
# autoflush: False — flush only on explicit .commit() or .flush().
SessionFactory = async_sessionmaker(
    bind=db_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


# --- fastapi db dependancy ---
async def get_db_session():
    """Yield a request-scoped session; auto-rollback on unhandled exception."""
    async with SessionFactory() as db_session:
        try:
            yield db_session
        except Exception:
            await db_session.rollback()
            raise


# --- Annotated Dep ---
DbSessionDep = Annotated[AsyncSession, Depends(get_db_session)]


# --- CRUD Utils ---

async def create(
    instance: Model,
    db_session: AsyncSession | None = None,
) -> Model:
    """Insert a new row.  Auto-commits when no session is provided."""
    if db_session is None:
        async with SessionFactory() as db_session:
            async with db_session.begin():
                db_session.add(instance)
                await db_session.flush()
                await db_session.refresh(instance)
        return instance

    db_session.add(instance)
    await db_session.flush()
    await db_session.refresh(instance)
    return instance


async def get_one(
    model: type[Model],
    pk: object,
    db_session: AsyncSession | None = None,
) -> Model | None:
    """Fetch a single row by primary key."""
    if db_session is None:
        async with SessionFactory() as db_session:
            async with db_session.begin():
                return await db_session.get(model, pk)

    return await db_session.get(model, pk)


async def get_all(
    stmt,
    db_session: AsyncSession | None = None,
) -> list[Model]:
    """Fetch all rows. Pass pre-built query statement from upper layer."""
    if db_session is None:
        async with SessionFactory() as db_session:
            async with db_session.begin():
                result = await db_session.execute(stmt)
                return list(result.scalars().all())

    result = await db_session.execute(stmt)
    return list(result.scalars().all())


async def delete_by_id(
    model: type[Model],
    pk: object,
    db_session: AsyncSession | None = None,
) -> None:
    """Delete by primary key. No fetch, direct delete."""
    pk_col = list(model.__table__.primary_key.columns)[0]
    stmt = delete(model).where(pk_col == pk)

    if db_session is None:
        async with SessionFactory() as db_session:
            async with db_session.begin():
                await db_session.execute(stmt)
        return

    await db_session.execute(stmt)


async def check_exists(
    model: type[Model],
    db_session: AsyncSession | None = None,
    filters: dict | None = None,
) -> bool:
    """Check if any row exists.  Uses SELECT 1 (portable across all RDBMS)."""
    stmt = select(1).select_from(model).limit(1)
    if filters:
        for key, value in filters.items():
            stmt = stmt.where(getattr(model, key) == value)

    if db_session is None:
        async with SessionFactory() as db_session:
            async with db_session.begin():
                result = await db_session.execute(stmt)
                return result.scalar() is not None

    result = await db_session.execute(stmt)
    return result.scalar() is not None
