from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def database_url_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

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
