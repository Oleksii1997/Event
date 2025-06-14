from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import text

from src.test_app.db.data_for_test import (
    CREATE_PROFILE_DATA_DB,
    TEST_USER_FOR_PROFILE_DB,
)


class FakeProfileDB:
    """Створюємо тестового профілю користувача"""

    def __init__(self, conn: AsyncConnection):
        self.conn = conn

    async def create_fake_profile(self):
        """Створюємо профіль користувача для тестів"""
        query = (
            f'INSERT INTO "profile_table" '
            f"(id, user_id, birthday, description, area, region, community, city) "
            f"VALUES "
            f"('{CREATE_PROFILE_DATA_DB["id"]}', '{TEST_USER_FOR_PROFILE_DB["user_id"]}', '{CREATE_PROFILE_DATA_DB["birthday"]}', '{CREATE_PROFILE_DATA_DB["description"]}',"
            f"'{CREATE_PROFILE_DATA_DB["area"]}', '{CREATE_PROFILE_DATA_DB["region"]}', '{CREATE_PROFILE_DATA_DB["community"]}', '{CREATE_PROFILE_DATA_DB["city"]}')"
        )

        await self.conn.execute(text(query))
