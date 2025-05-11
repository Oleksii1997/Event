from pydantic.v1 import UUID4
from sqlalchemy import text

from src.test_app.db.db_test_config import get_async_engine


async def get_verification_email_link(user_id: UUID4) -> UUID4:
    """Отримуємо link uuid верифікації електронної пошти користувача"""
    query = f'SELECT link FROM "verification_table" ' f"WHERE user_id='{user_id}'"
    async with get_async_engine().connect() as conn:
        result = await conn.execute(text(query))
    return (result.one())[0]


async def check_verification_email_status(user_id: UUID4) -> bool:
    """Перевіряємо статус верифікації електронної пошти користувача"""
    query = f'SELECT valid_email FROM "user_table" ' f"WHERE id='{user_id}'"
    async with get_async_engine().connect() as conn:
        result = await conn.execute(text(query))
    return (result.one())[0]
