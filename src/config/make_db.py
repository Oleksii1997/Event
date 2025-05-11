from src.config.models import Base
from src.config.db_settings import async_engine
from sqlalchemy import text


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def delete_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
