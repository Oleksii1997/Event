import pytest

from main import app
from src.test_app.db.data_for_test import (
    TEST_USER_MODEL_DB,
    JWT_TEST_DATA,
    TEST_CREATE_SOCIAL_LINK,
    INVALID_TEST_CREATE_SOCIAL_LINK,
    TEST_USER_FOR_PROFILE_DB,
    TEST_CREATE_SOCIAL_LINK_DB,
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
        == "Profile does not exist. Create your profile and edit"
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
    """Тестуємо створення посилань на соціальні мережі"""
    access_token = await create_jwt_token(
        payload={"user_id": TEST_USER_FOR_PROFILE_DB["user_id"]},
        private_key_path=JWT_TEST_DATA["private_key_access_jwt_path"],
        expire_minutes=JWT_TEST_DATA["ACCESS_TOKEN_EXPIRE_MINUTES"],
        algorithm=JWT_TEST_DATA["algorithm"],
    )
    response = await client.request(
        "POST",
        f"/api/v1/social_link/create",
        headers={"Authorization": f"Bearer {access_token}"},
        json=TEST_CREATE_SOCIAL_LINK,
    )
    assert response.status_code == 200
    assert response.json()["msg"] == "Social media links added"

    retry_response = await client.request(
        "POST",
        f"/api/v1/social_link/create",
        headers={"Authorization": f"Bearer {access_token}"},
        json=TEST_CREATE_SOCIAL_LINK,
    )
    assert retry_response.status_code == 200
    assert retry_response.json()["msg"] == "Social media link already exist"
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_max_limit_create_social_link(client, override_session):
    """Тестуємо перевищення допустимого ліміту створення посилань на соціальні мережі"""
    max_limit_social_link = 20
    access_token = await create_jwt_token(
        payload={"user_id": TEST_USER_FOR_PROFILE_DB["user_id"]},
        private_key_path=JWT_TEST_DATA["private_key_access_jwt_path"],
        expire_minutes=JWT_TEST_DATA["ACCESS_TOKEN_EXPIRE_MINUTES"],
        algorithm=JWT_TEST_DATA["algorithm"],
    )
    for i in range(0, max_limit_social_link + 2):
        TEST_CREATE_SOCIAL_LINK["link"] = f"{TEST_CREATE_SOCIAL_LINK["link"]} - {i}"
        response = await client.request(
            "POST",
            "/api/v1/social_link/create",
            headers={"Authorization": f"Bearer {access_token}"},
            json=TEST_CREATE_SOCIAL_LINK,
        )
        if i > max_limit_social_link:
            assert response.status_code == 200
            assert (
                response.json()["msg"]
                == "You have reached the maximum number of added social media links, the maximum possible number of links is 20."
            )
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_social_link(client, override_session):
    """Перевіряємо отримання даних посилання на соціальні мережі користувача"""
    access_token = await create_jwt_token(
        payload={"user_id": TEST_USER_FOR_PROFILE_DB["user_id"]},
        private_key_path=JWT_TEST_DATA["private_key_access_jwt_path"],
        expire_minutes=JWT_TEST_DATA["ACCESS_TOKEN_EXPIRE_MINUTES"],
        algorithm=JWT_TEST_DATA["algorithm"],
    )
    response = await client.request(
        "GET",
        "/api/v1/social_link/get",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    resp = response.json()
    assert response.status_code == 200
    assert resp[0]["id"] == TEST_CREATE_SOCIAL_LINK_DB["id"]
    assert resp[0]["link_type"] == TEST_CREATE_SOCIAL_LINK_DB["link_type"]
    assert resp[0]["link"] == TEST_CREATE_SOCIAL_LINK_DB["link"]

    access_token_without_profile = await create_jwt_token(
        payload={"user_id": TEST_USER_MODEL_DB["user_id"]},
        private_key_path=JWT_TEST_DATA["private_key_access_jwt_path"],
        expire_minutes=JWT_TEST_DATA["ACCESS_TOKEN_EXPIRE_MINUTES"],
        algorithm=JWT_TEST_DATA["algorithm"],
    )
    response_without_profile = await client.request(
        "GET",
        "/api/v1/social_link/get",
        headers={"Authorization": f"Bearer {access_token_without_profile}"},
    )
    assert response_without_profile.status_code == 400
    assert (
        response_without_profile.json()["detail"]
        == "Profile does not exist. Create your profile and edit"
    )


@pytest.mark.asyncio
async def test_delete_social_link(client, override_session):
    """Перевіряємо видалення посилання на соціальні мережі користувача"""
    access_token = await create_jwt_token(
        payload={"user_id": TEST_USER_FOR_PROFILE_DB["user_id"]},
        private_key_path=JWT_TEST_DATA["private_key_access_jwt_path"],
        expire_minutes=JWT_TEST_DATA["ACCESS_TOKEN_EXPIRE_MINUTES"],
        algorithm=JWT_TEST_DATA["algorithm"],
    )
    response = await client.request(
        "DELETE",
        f"/api/v1/social_link/delete?link_id={TEST_CREATE_SOCIAL_LINK_DB["id"]}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    resp = response.json()
    assert response.status_code == 200
    assert resp["id"] == TEST_CREATE_SOCIAL_LINK_DB["id"]
    assert resp["link_type"] == TEST_CREATE_SOCIAL_LINK_DB["link_type"]
    assert resp["link"] == TEST_CREATE_SOCIAL_LINK_DB["link"]

    response_retry = await client.request(
        "DELETE",
        f"/api/v1/social_link/delete?link_id={TEST_CREATE_SOCIAL_LINK_DB["id"]}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response_retry.status_code == 400
    assert response_retry.json()["detail"] == "Social link does not exist"
