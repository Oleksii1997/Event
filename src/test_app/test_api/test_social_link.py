import pytest

from main import app
from src.test_app.db.data_for_test import (
    TEST_USER_MODEL_DB,
    JWT_TEST_DATA,
    TEST_CREATE_SOCIAL_LINK,
    INVALID_TEST_CREATE_SOCIAL_LINK,
)
from src.app.auth.jwt import create_jwt_token


@pytest.mark.asyncio
async def test_create_social_link_without_profile(client, override_session):
    """Тестуємо API створення посилань на соціальні мережі, перевіряємо випадки авторизованого та неавторизованого користувача, валідних та невалідних даних"""
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
        "POST",
        f"/api/v1/social_link/create",
        json=TEST_CREATE_SOCIAL_LINK,
    )
    assert response_no_authorized.status_code == 401
    assert (response_no_authorized.json())["detail"] == "Not authenticated"

    response_invalid_token = await client.request(
        "POST",
        f"/api/v1/social_link/create",
        headers={"Authorization": f"Bearer {access_user_not_exist_token}"},
        json=TEST_CREATE_SOCIAL_LINK,
    )
    assert response_invalid_token.status_code == 401
    assert (response_invalid_token.json())["detail"] == "Token invalid (user not found)"

    response_without_profile = await client.request(
        "POST",
        f"/api/v1/social_link/create",
        headers={"Authorization": f"Bearer {access_token}"},
        json=TEST_CREATE_SOCIAL_LINK,
    )
    assert response_without_profile.status_code == 400
    assert (
        response_without_profile.json()["detail"]
        == "Profile does not exist. Creat your profile and edit"
    )

    response_invalid_data = await client.request(
        "POST",
        f"/api/v1/social_link/create",
        headers={"Authorization": f"Bearer {access_token}"},
        json=INVALID_TEST_CREATE_SOCIAL_LINK,
    )
    assert response_invalid_data.status_code == 422

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_create_social_link(client, override_session):
    """Створюємо користувача, профіль користувача та тестуємо випадок створення посилань на соціальні мережі та
    випадок перевищення кількості створених посилань на соціальні мережі"""
    app.dependency_overrides.clear()
