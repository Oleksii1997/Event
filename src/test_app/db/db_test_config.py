from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import create_async_engine


class SettingsTest(BaseSettings):
    """Дані тестової БД"""

    DB_TEST_HOST: str

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int | str

    @property
    def database_test_url_asyncpg(self):
        # return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.DB_TEST_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

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
