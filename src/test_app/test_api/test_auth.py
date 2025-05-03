import pytest
import json

from main import app
from src.app.auth.jwt import create_jwt_token
from src.test_app.db.data_for_test import (
    TEST_USER_API,
    TEST_VERIFICATION_MODEL_DB,
    TEST_USER_MODEL_DB,
    TEST_USER_MODEL_DB_NO_CONFIRM_MAIL,
    JWT_TEST_DATA,
    TEST_USER_MODEL_DB_NO_ACTIVE_CONFIRM_MAIL,
)
from src.test_app.service.auth_service import (
    get_verification_email_link,
    check_verification_email_status,
)


@pytest.mark.asyncio
async def test_registration_user(client, override_session):
    """Тест реєстрації користувача. Перевіряємо запис даних, правильність їх збереження та
    випадок створення користувача який вже існує. Також перевіряємо запис даних в модель верифікації електронної пошти
    """

    response = await client.post(
        "/api/v1/auth/registration",
        json=TEST_USER_API,
    )
    resp = response.json()
    assert response.status_code == 200
    assert resp["msg"] == "User has been created"
    assert resp["firstname"] == TEST_USER_API["firstname"]
    assert resp["lastname"] == TEST_USER_API["lastname"]
    assert resp["phone_number"] == TEST_USER_API["phone_number"]
    assert resp["email"] == TEST_USER_API["email"]
    assert resp["is_active"] == TEST_USER_API["is_active"]
    assert resp["valid_email"] == TEST_USER_API["valid_email"]
    assert resp["is_staff"] == TEST_USER_API["is_staff"]
    assert resp["is_superuser"] == TEST_USER_API["is_superuser"]

    response_2 = await client.post(
        "/api/v1/auth/registration",
        json=TEST_USER_API,
    )
    assert response_2.__dict__["status_code"] == 400
    assert (
        json.loads(response_2.__dict__["_content"].decode("utf-8"))["detail"]
        == "User already exists"
    )

    verification_link_api = await get_verification_email_link(user_id=resp["id"])
    assert str(type(verification_link_api)) == "<class 'asyncpg.pgproto.pgproto.UUID'>"
    verification_link_db = await get_verification_email_link(
        user_id=TEST_VERIFICATION_MODEL_DB["user_id"]
    )
    assert str(verification_link_db) == TEST_VERIFICATION_MODEL_DB["link"]

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_confirm_email(client, override_session):
    """Тест api верифікації електронної пошти.
    При першій першому запиту відбувається зміна 'valid_email' на значення True в моделі 'user'
    та видалення запису з таблиці 'verification'.
    В другому запиті перевіряємо поведінку при спробі підтвердження лінку який не існує в таблиці 'verification'
    """

    response = await client.get(
        f"/api/v1/auth/confirm-email?link={TEST_VERIFICATION_MODEL_DB["link"]}",
    )
    resp = response.json()
    assert response.status_code == 200
    assert resp["msg"] == "Success verify email"

    response_2 = await client.get(
        f"/api/v1/auth/confirm-email?link={TEST_VERIFICATION_MODEL_DB["link"]}",
    )
    resp_2 = response_2.json()
    assert response_2.status_code == 404
    assert resp_2["detail"] == "E-mail verification link not found"

    assert (
        await check_verification_email_status(TEST_VERIFICATION_MODEL_DB["user_id"])
        == True
    )

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_login_access_refresh_jwt(client, override_session):
    """Тестуаємо api авторизації. Перевіряємо випадки коли користувач вводить правильні та не валідні дані"""

    response = await client.request(
        "POST",
        "/api/v1/auth/login/",
        data={
            "username": TEST_USER_MODEL_DB["phone_number"],
            "password": TEST_USER_MODEL_DB["password"],
        },
    )
    resp = response.json()
    assert response.status_code == 200
    assert str(type(resp["access_token"])) == "<class 'str'>"
    assert str(type(resp["refresh_token"])) == "<class 'str'>"
    assert resp["token_type"] == "Bearer"

    response_invalid = await client.request(
        "POST",
        "/api/v1/auth/login/",
        data={
            "username": "incorrect_username",
            "password": "incorrect_password",
        },
    )
    resp_incorrect = response_invalid.json()
    assert response_invalid.status_code == 400
    assert resp_incorrect["detail"] == "Incorrect phone number or password"

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_refresh_jwt(client, override_session):
    """Тестуємо отримання access токена по дійсному refresh токену"""
    payload = {"user_id": TEST_USER_MODEL_DB["user_id"]}
    refresh_jwt = await create_jwt_token(
        payload=payload,
        private_key_path=JWT_TEST_DATA["private_key_refresh_jwt_path"],
        expire_minutes=JWT_TEST_DATA["REFRESH_TOKEN_EXPIRE_MINUTES"],
        algorithm=JWT_TEST_DATA["algorithm"],
    )

    response = await client.request(
        "POST",
        f"/api/v1/auth/refresh_token/?refresh_token={refresh_jwt}",
    )
    resp = response.json()
    assert response.status_code == 200
    assert str(type(resp["access_token"])) == "<class 'str'>"
    assert str(type(resp["refresh_token"])) == "<class 'str'>"
    assert resp["token_type"] == "Bearer"

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_recovery_password(client, override_session):
    """Тестуємо функціонал відновлення пароля дійсними та невірними даними"""

    response_does_not_exist = await client.request(
        "POST",
        f"/api/v1/auth/recovery-password/not_exist{TEST_USER_MODEL_DB["email"]}",
    )
    resp = response_does_not_exist.json()
    assert response_does_not_exist.status_code == 404
    assert resp["detail"] == "User does not exist. Check your email."

    response_not_active = await client.request(
        "POST",
        f"/api/v1/auth/recovery-password/{TEST_USER_MODEL_DB_NO_ACTIVE_CONFIRM_MAIL["email"]}",
    )
    resp = response_not_active.json()
    assert response_not_active.status_code == 403
    assert resp["detail"] == "Your account inactive"

    response_not_confirm = await client.request(
        "POST",
        f"/api/v1/auth/recovery-password/{TEST_USER_MODEL_DB_NO_CONFIRM_MAIL["email"]}",
    )
    resp = response_not_confirm.json()
    assert response_not_confirm.status_code == 403
    assert (
        resp["detail"]
        == "Email not confirmed. Please confirm your email and try again."
    )

    response_valid = await client.request(
        "POST",
        f"/api/v1/auth/recovery-password/{TEST_USER_MODEL_DB["email"]}",
    )
    resp = response_valid.json()
    assert response_valid.status_code == 200
    assert resp["msg"] == "Recovery mail is send"

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_reset_password(client, override_session):
    """Перевіряємо функціонал відновлення пароля, також тестуємо випадки не валідного токена та некоректних даних
    в payload"""
    recovery_password_token = await create_jwt_token(
        payload={"user_id": TEST_USER_MODEL_DB["user_id"]},
        private_key_path=JWT_TEST_DATA["private_key_recovery_password_path"],
        expire_minutes=JWT_TEST_DATA["RECOVERY_PASSWORD_TOKEN_EXPIRE_MINUTES"],
        algorithm=JWT_TEST_DATA["algorithm"],
    )

    response = await client.request(
        "POST",
        f"/api/v1/auth/reset-password/?reset_password_token={recovery_password_token}",
        json={"new_password": "Oleksii@WM4635", "confirm_password": "Oleksii@WM4635"},
    )

    assert response.status_code == 200
    assert (response.json())["msg"] == "Password changed successfully"

    response_incorrect_token = await client.request(
        "POST",
        f"/api/v1/auth/reset-password/?reset_password_token=incorrect_token{recovery_password_token}",
        json={"new_password": "Oleksii@WM4635", "confirm_password": "Oleksii@WM4635"},
    )
    assert response_incorrect_token.status_code == 401
    assert (response_incorrect_token.json())["detail"] == "Invalid reset password token"

    recovery_password_token_not_exist_user = await create_jwt_token(
        payload={"user_id": "bb43ad9f-71f3-4ba2-a52f-ef1311f38b2f"},
        private_key_path=JWT_TEST_DATA["private_key_recovery_password_path"],
        expire_minutes=JWT_TEST_DATA["RECOVERY_PASSWORD_TOKEN_EXPIRE_MINUTES"],
        algorithm=JWT_TEST_DATA["algorithm"],
    )
    response_user_not_exist = await client.request(
        "POST",
        f"/api/v1/auth/reset-password/?reset_password_token={recovery_password_token_not_exist_user}",
        json={"new_password": "Oleksii@WM4635", "confirm_password": "Oleksii@WM4635"},
    )
    assert response_user_not_exist.status_code == 403
    assert (response_user_not_exist.json())["detail"] == "User does not exist"

    app.dependency_overrides.clear()
