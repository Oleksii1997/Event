import pytest

from src.app.auth.jwt import create_jwt_token, decode_jwt_token, read_jwt_key
from src.app.auth.jwt_auth_service import (
    get_payload_access_token,
    get_payload_refresh_token,
)
from src.test_app.db.data_for_test import TEST_USER_MODEL_DB, JWT_TEST_DATA


@pytest.mark.asyncio
async def test_read_jwt_key():
    """Тестуємо функцію яка читає private і public ключі з файлу"""
    key = await read_jwt_key(link=JWT_TEST_DATA["private_key_access_jwt_path"])
    assert str(type(key)) == "<class 'str'>"


@pytest.mark.asyncio
async def test_create_jwt_token():
    """Тестуємо створення access токена"""
    payload = {"user_id": TEST_USER_MODEL_DB["user_id"]}
    jwt = await create_jwt_token(
        payload=payload,
        private_key_path=JWT_TEST_DATA["private_key_access_jwt_path"],
        expire_minutes=JWT_TEST_DATA["ACCESS_TOKEN_EXPIRE_MINUTES"],
        algorithm=JWT_TEST_DATA["algorithm"],
    )
    assert str(type(jwt)) == "<class 'str'>"


@pytest.mark.asyncio
async def test_decode_jwt_token():
    """Тестуємо декодування JWT токена"""
    payload = {"user_id": TEST_USER_MODEL_DB["user_id"]}
    jwt = await create_jwt_token(
        payload=payload,
        private_key_path=JWT_TEST_DATA["private_key_access_jwt_path"],
        expire_minutes=JWT_TEST_DATA["ACCESS_TOKEN_EXPIRE_MINUTES"],
        algorithm=JWT_TEST_DATA["algorithm"],
    )
    decode_payload = await decode_jwt_token(
        token=jwt,
        public_key_path=JWT_TEST_DATA["public_key_access_jwt_path"],
        algorithm=JWT_TEST_DATA["algorithm"],
    )
    assert str(type(decode_payload)) == "<class 'dict'>"
    assert decode_payload["user_id"] == TEST_USER_MODEL_DB["user_id"]


@pytest.mark.asyncio
async def test_get_payload_access_token():
    """Перевіряємо функцію розшифровки access токена. Також перевіряємо випадок некоректного токена"""

    payload = {"user_id": TEST_USER_MODEL_DB["user_id"]}
    access_jwt = await create_jwt_token(
        payload=payload,
        private_key_path=JWT_TEST_DATA["private_key_access_jwt_path"],
        expire_minutes=JWT_TEST_DATA["ACCESS_TOKEN_EXPIRE_MINUTES"],
        algorithm=JWT_TEST_DATA["algorithm"],
    )
    decode_payload = await get_payload_access_token(access_token=access_jwt)

    assert str(type(decode_payload)) == "<class 'dict'>"
    assert decode_payload["user_id"] == TEST_USER_MODEL_DB["user_id"]


@pytest.mark.asyncio
async def test_get_payload_refresh_token():
    """Перевіряємо функцію розшифровки access токена. Також перевіряємо випадок некоректного токена"""

    payload = {"user_id": TEST_USER_MODEL_DB["user_id"]}
    refresh_jwt = await create_jwt_token(
        payload=payload,
        private_key_path=JWT_TEST_DATA["private_key_refresh_jwt_path"],
        expire_minutes=JWT_TEST_DATA["REFRESH_TOKEN_EXPIRE_MINUTES"],
        algorithm=JWT_TEST_DATA["algorithm"],
    )
    decode_payload = await get_payload_refresh_token(refresh_token=refresh_jwt)

    assert str(type(decode_payload)) == "<class 'dict'>"
    assert decode_payload["user_id"] == TEST_USER_MODEL_DB["user_id"]
