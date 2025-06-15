from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import text

from src.test_app.db.data_for_test import (
    CREATE_PROFILE_DATA_DB,
    TEST_CREATE_SOCIAL_LINK_DB,
)


class FakeSocialLinkDB:
    """Створюємо тестовий запис посилання на соціальні мережі"""

    def __init__(self, conn: AsyncConnection):
        self.conn = conn

    async def create_fake_social_link(self):
        """Створюємо запис посилання на соцмережі"""
        query = (
            f'INSERT INTO "social_link_table" '
            f"(id, link_type, link, profile_id) "
            f"VALUES "
            f"('{TEST_CREATE_SOCIAL_LINK_DB["id"]}', '{TEST_CREATE_SOCIAL_LINK_DB["link_type"]}', '{TEST_CREATE_SOCIAL_LINK_DB["link"]}', '{CREATE_PROFILE_DATA_DB["id"]}')"
        )

        await self.conn.execute(text(query))
