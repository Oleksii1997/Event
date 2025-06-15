from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import text

from src.test_app.db.data_for_test import (
    TEST_USER_MODEL_DB,
    TEST_VERIFICATION_MODEL_DB,
    TEST_USER_MODEL_DB_NO_CONFIRM_MAIL,
    TEST_USER_MODEL_DB_NO_ACTIVE_CONFIRM_MAIL,
)
from src.test_app.db.create_fake_data.create_fake_location import FakeLocationDB
from src.test_app.db.create_fake_data.create_fake_user import FakeUserDB
from src.test_app.db.create_fake_data.create_fake_profile import FakeProfileDB
from src.test_app.db.create_fake_data.create_fake_social_link import FakeSocialLinkDB


async def fake_data_db(conn: AsyncConnection):
    """Наповнюємо БД даними для тестування"""
    await FakeUserDB(conn=conn).create_fake_user()
    await FakeUserDB(conn=conn).create_fake_verification_email()
    await FakeLocationDB(conn=conn).fake_location_db()
    await FakeProfileDB(conn=conn).create_fake_profile()
    await FakeSocialLinkDB(conn=conn).create_fake_social_link()
