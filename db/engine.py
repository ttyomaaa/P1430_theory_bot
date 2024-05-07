from typing import Union

from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine, AsyncEngine
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from db.utils.url import get_url


def create_async_engine(url: Union[URL, str]):
    return _create_async_engine(url=url, echo=True, pool_pre_ping=True)


async def proceed_schemas(engine: AsyncEngine, metadata) -> None:
    async with engine.begin() as con:
        await con.run_sync(metadata.create_all)


def get_session_maker(engine):
    return sessionmaker(engine, class_=AsyncSession)


def session_maker():
    postgres_url = get_url("postgresql+asyncpg")
    async_engine = create_async_engine(postgres_url)
    return get_session_maker(async_engine)
