from collections.abc import AsyncGenerator
import pytest
from fastapi import FastAPI
import pytest_asyncio
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from src.config.models import Base
from main import app
from src.app.users.models import UserModel, ProfileModel
from src.app.auth.models import (
    VerificationModel,
)  # Цей імпорт повинен бути, бо інакше не підтягує моделі
from src.config.db_settings import get_session
from src.config.settings import base_url

from httpx import ASGITransport, AsyncClient


class SettingsTest(BaseSettings):
    """Дані тестової БД"""

    DB_TEST_HOST: str
    DB_TEST_PORT: int
    DB_TEST_USER: str
    DB_TEST_PASS: str
    DB_TEST_NAME: str

    @property
    def database_test_url_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_TEST_USER}:{self.DB_TEST_PASS}@{self.DB_TEST_HOST}:{self.DB_TEST_PORT}/{self.DB_TEST_NAME}"

    model_config = SettingsConfigDict(env_file=".env_test_db")


@pytest_asyncio.fixture()
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

    async with test_session() as session_test:
        yield session_test


@pytest.fixture()
def test_app(override_session: AsyncSession) -> FastAPI:
    """Перевизначаємо сесію в app"""
    session = lambda: override_session
    app.dependency_overrides[get_session] = session
    return app


@pytest_asyncio.fixture()
async def client(test_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """Створюємо https клієнта"""
    async with AsyncClient(
        transport=ASGITransport(app=test_app), base_url="http://test"
    ) as client:
        yield client
