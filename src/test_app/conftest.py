from collections.abc import AsyncGenerator
import pytest
from fastapi import FastAPI
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from httpx import ASGITransport, AsyncClient

from src.config.models import Base
from main import app
from src.config.db_settings import get_session
from src.test_app.db.create_fake_data import fake_data_db
from src.test_app.db.db_test_config import SettingsTest


@pytest_asyncio.fixture(scope="function")
async def override_session():
    """Створюємо сесію для тестів, використовуємо тестову базу даних"""
    settings_test = SettingsTest()
    async_engine_test = create_async_engine(
        url=settings_test.database_test_url_asyncpg,
        echo=False,
        pool_size=5,
        max_overflow=10,
    )
    test_session = async_sessionmaker(async_engine_test, expire_on_commit=False)

    async with async_engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await fake_data_db(conn)

    async with test_session() as session_test:
        yield session_test


@pytest.fixture(scope="function")
def test_app(override_session: AsyncSession) -> FastAPI:
    """Перевизначаємо сесію в app"""
    session = lambda: override_session
    app.dependency_overrides[get_session] = session
    return app


@pytest_asyncio.fixture(scope="function")
async def client(test_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """Створюємо https клієнта"""
    async with AsyncClient(
        transport=ASGITransport(app=test_app), base_url="http://test"
    ) as client:
        yield client
