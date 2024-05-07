import asyncio

from db.engine import create_async_engine, proceed_schemas
from app.models.models import Base
from db.utils.url import get_url

from settings import ASYNC_DRIVER_NAME


async def create_tables():
    url = get_url(ASYNC_DRIVER_NAME)
    async_engine = create_async_engine(url)
    await proceed_schemas(async_engine, Base.metadata)


asyncio.run(create_tables())
