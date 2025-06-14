from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import text

from src.app.auth.security import get_password_hash
from src.test_app.db.data_for_test import (
    TEST_USER_MODEL_DB,
    TEST_VERIFICATION_MODEL_DB,
    TEST_USER_MODEL_DB_NO_CONFIRM_MAIL,
    TEST_USER_MODEL_DB_NO_ACTIVE_CONFIRM_MAIL,
    TEST_USER_FOR_PROFILE_DB,
)


class FakeUserDB:
    """Створюємо тестового користувача та запис в модель верифікації електронної пошти"""

    def __init__(self, conn: AsyncConnection):
        self.conn = conn

    async def create_fake_user(self):
        """Записуємо в базу даних фейкового користувача"""
        hash_password = str(get_password_hash(password=TEST_USER_MODEL_DB["password"]))[
            1:
        ]
        hash_password_no_confirm = str(
            get_password_hash(password=TEST_USER_MODEL_DB_NO_CONFIRM_MAIL["password"])
        )[1:]
        hash_password_user_with_profile = str(
            get_password_hash(password=TEST_USER_FOR_PROFILE_DB["password"])
        )[1:]
        query = (
            f'INSERT INTO "user_table" '
            f"(id, firstname, lastname, phone_number, password, email, valid_email, is_active, is_staff, is_superuser) "
            f"VALUES "
            f"('{TEST_USER_MODEL_DB["user_id"]}', '{TEST_USER_MODEL_DB["firstname"]}', '{TEST_USER_MODEL_DB["lastname"]}', '{TEST_USER_MODEL_DB["phone_number"]}', "
            f"{hash_password}::bytea, "
            f"'{TEST_USER_MODEL_DB["email"]}', '{TEST_USER_MODEL_DB["valid_email"]}', '{TEST_USER_MODEL_DB["is_active"]}', "
            f"'{TEST_USER_MODEL_DB["is_staff"]}', '{TEST_USER_MODEL_DB["is_superuser"]}'), "
            f"('{TEST_USER_MODEL_DB_NO_CONFIRM_MAIL["user_id"]}', '{TEST_USER_MODEL_DB_NO_CONFIRM_MAIL["firstname"]}', '{TEST_USER_MODEL_DB_NO_CONFIRM_MAIL["lastname"]}', '{TEST_USER_MODEL_DB_NO_CONFIRM_MAIL["phone_number"]}', "
            f"{hash_password_no_confirm}::bytea, "
            f"'{TEST_USER_MODEL_DB_NO_CONFIRM_MAIL["email"]}', '{TEST_USER_MODEL_DB_NO_CONFIRM_MAIL["valid_email"]}', '{TEST_USER_MODEL_DB_NO_CONFIRM_MAIL["is_active"]}', "
            f"'{TEST_USER_MODEL_DB_NO_CONFIRM_MAIL["is_staff"]}', '{TEST_USER_MODEL_DB_NO_CONFIRM_MAIL["is_superuser"]}'), "
            f"('{TEST_USER_MODEL_DB_NO_ACTIVE_CONFIRM_MAIL["user_id"]}', '{TEST_USER_MODEL_DB_NO_ACTIVE_CONFIRM_MAIL["firstname"]}', '{TEST_USER_MODEL_DB_NO_ACTIVE_CONFIRM_MAIL["lastname"]}', '{TEST_USER_MODEL_DB_NO_ACTIVE_CONFIRM_MAIL["phone_number"]}', "
            f"{hash_password_no_confirm}::bytea, "
            f"'{TEST_USER_MODEL_DB_NO_ACTIVE_CONFIRM_MAIL["email"]}', '{TEST_USER_MODEL_DB_NO_ACTIVE_CONFIRM_MAIL["valid_email"]}', '{TEST_USER_MODEL_DB_NO_ACTIVE_CONFIRM_MAIL["is_active"]}', "
            f"'{TEST_USER_MODEL_DB_NO_ACTIVE_CONFIRM_MAIL["is_staff"]}', '{TEST_USER_MODEL_DB_NO_ACTIVE_CONFIRM_MAIL["is_superuser"]}'), "
            f"('{TEST_USER_FOR_PROFILE_DB["user_id"]}', '{TEST_USER_FOR_PROFILE_DB["firstname"]}', '{TEST_USER_FOR_PROFILE_DB["lastname"]}', '{TEST_USER_FOR_PROFILE_DB["phone_number"]}', "
            f"{hash_password_user_with_profile}::bytea, "
            f"'{TEST_USER_FOR_PROFILE_DB["email"]}', '{TEST_USER_FOR_PROFILE_DB["valid_email"]}', '{TEST_USER_FOR_PROFILE_DB["is_active"]}', "
            f"'{TEST_USER_FOR_PROFILE_DB["is_staff"]}', '{TEST_USER_FOR_PROFILE_DB["is_superuser"]}')"
        )

        await self.conn.execute(text(query))

    async def create_fake_verification_email(self):
        """Запис в таблицю верифікації електронної пошти (verification) даних для тестування"""
        query = (
            f'INSERT INTO "verification_table" '
            f"(link, user_id) "
            f"VALUES "
            f"('{TEST_VERIFICATION_MODEL_DB["link"]}', '{TEST_VERIFICATION_MODEL_DB["user_id"]}')"
        )
        await self.conn.execute(text(query))
