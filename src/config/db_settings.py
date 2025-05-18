from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


class Settings(BaseSettings):
    DB_HOST: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int | str

    @property
    def database_url_asyncpg(self):
        # return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.DB_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(env_file=".env_db")


settings = Settings()

async_engine = create_async_engine(
    url=settings.database_url_asyncpg, echo=True, pool_size=5, max_overflow=10
)

new_session = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_session():
    """Сесія для підключення до БД"""
    async with new_session() as session:
        yield session
