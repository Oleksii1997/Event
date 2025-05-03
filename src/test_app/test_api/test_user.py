import pytest
import json

from main import app
from src.app.auth.jwt import create_jwt_token
from src.test_app.db.data_for_test import (
    TEST_USER_MODEL_DB,
    JWT_TEST_DATA,
    TEST_ME_UPDATE,
)


@pytest.mark.asyncio
async def test_user_me(client, override_session):
    """Тестуємо функціонал отримання інформації про власний профіль, перевіряємо випадки коли користувач не
    авторизований та коли користувач не існує (дані в payload не дійсні) або jwt токен не дійсний
    """

    response_no_authorized = await client.request(
        "GET",
        f"/api/v1/user/me",
    )
    assert response_no_authorized.status_code == 401
    assert (response_no_authorized.json())["detail"] == "Not authenticated"

    access_token = await create_jwt_token(
        payload={"user_id": TEST_USER_MODEL_DB["user_id"]},
        private_key_path=JWT_TEST_DATA["private_key_access_jwt_path"],
        expire_minutes=JWT_TEST_DATA["ACCESS_TOKEN_EXPIRE_MINUTES"],
        algorithm=JWT_TEST_DATA["algorithm"],
    )
    response_authorized = await client.request(
        "GET", f"/api/v1/user/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    resp = response_authorized.json()
    assert response_authorized.status_code == 200
    assert resp["id"] == TEST_USER_MODEL_DB["user_id"]
    assert resp["firstname"] == TEST_USER_MODEL_DB["firstname"]
    assert resp["lastname"] == TEST_USER_MODEL_DB["lastname"]
    assert resp["email"] == TEST_USER_MODEL_DB["email"]
    assert resp["phone_number"] == TEST_USER_MODEL_DB["phone_number"]

    response_invalid_token = await client.request(
        "GET",
        f"/api/v1/user/me",
        headers={"Authorization": f"Bearer invalid_token{access_token}"},
    )
    assert response_invalid_token.status_code == 401
    assert (response_invalid_token.json())["detail"] == "Invalid access token error"

    access_user_not_exist_token = await create_jwt_token(
        payload={"user_id": "b4085628-0776-4203-a822-718f9d6db521"},
        private_key_path=JWT_TEST_DATA["private_key_access_jwt_path"],
        expire_minutes=JWT_TEST_DATA["ACCESS_TOKEN_EXPIRE_MINUTES"],
        algorithm=JWT_TEST_DATA["algorithm"],
    )
    response_user_not_exist_token = await client.request(
        "GET",
        f"/api/v1/user/me",
        headers={"Authorization": f"Bearer {access_user_not_exist_token}"},
    )
    assert response_user_not_exist_token.status_code == 401
    assert (response_user_not_exist_token.json())[
        "detail"
    ] == "Token invalid (user not found)"

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_user_update(client, override_session):
    """Тестуємо функціонал оновлення даних користувача, перевіряємо випадок неавторизованого користувача, не валідного"""
    access_token = await create_jwt_token(
        payload={"user_id": TEST_USER_MODEL_DB["user_id"]},
        private_key_path=JWT_TEST_DATA["private_key_access_jwt_path"],
        expire_minutes=JWT_TEST_DATA["ACCESS_TOKEN_EXPIRE_MINUTES"],
        algorithm=JWT_TEST_DATA["algorithm"],
    )
    access_user_not_exist_token = await create_jwt_token(
        payload={"user_id": "b4085628-0776-4203-a822-718f9d6db521"},
        private_key_path=JWT_TEST_DATA["private_key_access_jwt_path"],
        expire_minutes=JWT_TEST_DATA["ACCESS_TOKEN_EXPIRE_MINUTES"],
        algorithm=JWT_TEST_DATA["algorithm"],
    )

    response_no_authorized = await client.request(
        "PATCH",
        f"/api/v1/user/me/update",
        json=TEST_ME_UPDATE,
    )
    assert response_no_authorized.status_code == 401
    assert (response_no_authorized.json())["detail"] == "Not authenticated"

    response_authorized = await client.request(
        "PATCH",
        f"/api/v1/user/me/update",
        headers={"Authorization": f"Bearer {access_token}"},
        json=TEST_ME_UPDATE,
    )
    resp = response_authorized.json()
    assert response_authorized.status_code == 200
    assert resp["id"] == TEST_USER_MODEL_DB["user_id"]
    assert resp["firstname"] == TEST_ME_UPDATE["firstname"]
    assert resp["lastname"] == TEST_ME_UPDATE["lastname"]
    assert resp["email"] == TEST_ME_UPDATE["email"]
    assert resp["phone_number"] == TEST_ME_UPDATE["phone_number"]

    response_invalid_token = await client.request(
        "PATCH",
        f"/api/v1/user/me/update",
        headers={"Authorization": f"Bearer invalid_token{access_token}"},
        json=TEST_ME_UPDATE,
    )
    assert response_invalid_token.status_code == 401
    assert (response_invalid_token.json())["detail"] == "Invalid access token error"

    response_user_not_exist_token = await client.request(
        "PATCH",
        f"/api/v1/user/me/update",
        headers={"Authorization": f"Bearer {access_user_not_exist_token}"},
        json=TEST_ME_UPDATE,
    )
    assert response_user_not_exist_token.status_code == 401
    assert (response_user_not_exist_token.json())[
        "detail"
    ] == "Token invalid (user not found)"

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_user_delete(client, override_session):
    """Тестуємо видалення акаунту користувача, перевіряємо випадки неавторизованого користувача, валідних та невалідних
    даних в payload токена"""
    access_token = await create_jwt_token(
        payload={"user_id": TEST_USER_MODEL_DB["user_id"]},
        private_key_path=JWT_TEST_DATA["private_key_access_jwt_path"],
        expire_minutes=JWT_TEST_DATA["ACCESS_TOKEN_EXPIRE_MINUTES"],
        algorithm=JWT_TEST_DATA["algorithm"],
    )
    access_user_not_exist_token = await create_jwt_token(
        payload={"user_id": "b4085628-0776-4203-a822-718f9d6db521"},
        private_key_path=JWT_TEST_DATA["private_key_access_jwt_path"],
        expire_minutes=JWT_TEST_DATA["ACCESS_TOKEN_EXPIRE_MINUTES"],
        algorithm=JWT_TEST_DATA["algorithm"],
    )

    response_no_authorized = await client.request(
        "DELETE",
        f"/api/v1/user/me/delete",
    )
    assert response_no_authorized.status_code == 401
    assert (response_no_authorized.json())["detail"] == "Not authenticated"

    response_authorized = await client.request(
        "DELETE",
        f"/api/v1/user/me/delete",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    resp = response_authorized.json()
    assert response_authorized.status_code == 200
    assert resp["id"] == TEST_USER_MODEL_DB["user_id"]
    assert resp["firstname"] == TEST_USER_MODEL_DB["firstname"]
    assert resp["lastname"] == TEST_USER_MODEL_DB["lastname"]
    assert resp["email"] == TEST_USER_MODEL_DB["email"]
    assert resp["phone_number"] == TEST_USER_MODEL_DB["phone_number"]

    response_invalid_token = await client.request(
        "DELETE",
        f"/api/v1/user/me/delete",
        headers={"Authorization": f"Bearer invalid_token{access_token}"},
        json=TEST_ME_UPDATE,
    )
    assert response_invalid_token.status_code == 401
    assert (response_invalid_token.json())["detail"] == "Invalid access token error"

    response_user_not_exist_token = await client.request(
        "DELETE",
        f"/api/v1/user/me/delete",
        headers={"Authorization": f"Bearer {access_user_not_exist_token}"},
        json=TEST_ME_UPDATE,
    )
    assert response_user_not_exist_token.status_code == 401
    assert (response_user_not_exist_token.json())[
        "detail"
    ] == "Token invalid (user not found)"

    app.dependency_overrides.clear()
