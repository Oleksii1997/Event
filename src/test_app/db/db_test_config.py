from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import create_async_engine


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


def get_async_engine():
    settings_test = SettingsTest()
    async_engine_test = create_async_engine(
        url=settings_test.database_test_url_asyncpg,
        echo=True,
        pool_size=5,
        max_overflow=10,
    )
    return async_engine_test
