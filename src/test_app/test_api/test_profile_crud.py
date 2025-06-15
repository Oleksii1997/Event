from uuid import UUID
import pytest

from main import app
from src.test_app.db.data_for_test import (
    TEST_USER_MODEL_DB,
    JWT_TEST_DATA,
    TEST_CREATE_SOCIAL_LINK,
    INVALID_TEST_CREATE_SOCIAL_LINK,
    CREATE_PROFILE_DATA_API,
    PROFILE_FUTURE_BIRTHDAY,
    PROFILE_OLD_BIRTHDAY,
    FAKE_PROFILE_UUID,
    CREATE_PROFILE_DATA_DB,
    TEST_USER_FOR_PROFILE_DB,
    PROFILE_UPDATE_DB,
    PROFILE_CITY_DOSE_NOT_EXIST,
    PROFILE_FAKE_LOCATION,
)
from src.app.auth.jwt import create_jwt_token


@pytest.mark.asyncio
async def test_create_profile(client, override_session):
    """Перевіряємо створення профілю"""

    access_token = await create_jwt_token(
        payload={"user_id": TEST_USER_MODEL_DB["user_id"]},
        private_key_path=JWT_TEST_DATA["private_key_access_jwt_path"],
        expire_minutes=JWT_TEST_DATA["ACCESS_TOKEN_EXPIRE_MINUTES"],
        algorithm=JWT_TEST_DATA["algorithm"],
    )

    response = await client.request(
        "POST",
        f"/api/v1/profile/create",
        headers={"Authorization": f"Bearer {access_token}"},
        json=PROFILE_FUTURE_BIRTHDAY,
    )
    assert response.status_code == 422

    response = await client.request(
        "POST",
        f"/api/v1/profile/create",
        headers={"Authorization": f"Bearer {access_token}"},
        json=PROFILE_OLD_BIRTHDAY,
    )
    assert response.status_code == 422

    response_correct = await client.request(
        "POST",
        f"/api/v1/profile/create",
        headers={"Authorization": f"Bearer {access_token}"},
        json=CREATE_PROFILE_DATA_API,
    )
    resp = response_correct.json()
    assert response_correct.status_code == 200
    assert resp["profile_user"]["phone_number"] == TEST_USER_MODEL_DB["phone_number"]
    assert resp["profile_user"]["email"] == TEST_USER_MODEL_DB["email"]
    assert resp["birthday"] == CREATE_PROFILE_DATA_API["birthday"]
    assert resp["description"] == CREATE_PROFILE_DATA_API["description"]
    assert resp["profile_area"]["id"] == CREATE_PROFILE_DATA_API["area"]
    assert resp["profile_region"]["id"] == CREATE_PROFILE_DATA_API["region"]
    assert resp["profile_community"]["id"] == CREATE_PROFILE_DATA_API["community"]
    assert resp["profile_city"]["id"] == CREATE_PROFILE_DATA_API["city"]

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_profile_detail(client, override_session):
    """Тестуємо отримання інформації про профіль користувача"""
    access_token = await create_jwt_token(
        payload={"user_id": TEST_USER_FOR_PROFILE_DB["user_id"]},
        private_key_path=JWT_TEST_DATA["private_key_access_jwt_path"],
        expire_minutes=JWT_TEST_DATA["ACCESS_TOKEN_EXPIRE_MINUTES"],
        algorithm=JWT_TEST_DATA["algorithm"],
    )
    response = await client.request(
        "GET",
        f"/api/v1/profile/get_detail?id={FAKE_PROFILE_UUID}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Profile does not exist"

    response = await client.request(
        "GET",
        f"/api/v1/profile/get_detail?id={TEST_USER_FOR_PROFILE_DB["user_id"]}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    resp = response.json()
    assert response.status_code == 200
    assert (
        resp["profile_user"]["phone_number"] == TEST_USER_FOR_PROFILE_DB["phone_number"]
    )
    assert resp["profile_user"]["email"] == TEST_USER_FOR_PROFILE_DB["email"]
    assert resp["birthday"] == CREATE_PROFILE_DATA_DB["birthday"]
    assert resp["description"] == CREATE_PROFILE_DATA_DB["description"]
    assert resp["profile_area"]["id"] == CREATE_PROFILE_DATA_DB["area"]
    assert resp["profile_region"]["id"] == CREATE_PROFILE_DATA_DB["region"]
    assert resp["profile_community"]["id"] == CREATE_PROFILE_DATA_DB["community"]
    assert resp["profile_city"]["id"] == CREATE_PROFILE_DATA_DB["city"]

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_update_profile(client, override_session):
    """Тестуємо API оновлення даних профілю користувача"""
    access_token = await create_jwt_token(
        payload={"user_id": TEST_USER_FOR_PROFILE_DB["user_id"]},
        private_key_path=JWT_TEST_DATA["private_key_access_jwt_path"],
        expire_minutes=JWT_TEST_DATA["ACCESS_TOKEN_EXPIRE_MINUTES"],
        algorithm=JWT_TEST_DATA["algorithm"],
    )
    response = await client.request(
        "PATCH",
        "/api/v1/profile/update",
        headers={"Authorization": f"Bearer {access_token}"},
        json=PROFILE_UPDATE_DB,
    )
    resp = response.json()
    assert response.status_code == 200
    assert resp["id"] == CREATE_PROFILE_DATA_DB["id"]
    assert resp["birthday"] == PROFILE_UPDATE_DB["birthday"]
    assert resp["description"] == PROFILE_UPDATE_DB["description"]
    assert resp["profile_area"]["id"] == PROFILE_UPDATE_DB["area"]
    assert resp["profile_region"]["id"] == PROFILE_UPDATE_DB["region"]
    assert resp["profile_community"]["id"] == PROFILE_UPDATE_DB["community"]
    assert resp["profile_city"]["id"] == PROFILE_UPDATE_DB["city"]


@pytest.mark.asyncio
async def test_update_profile_fake_location(client, override_session):
    """Тестуємо API оновлення даних профілю користувача"""
    access_token = await create_jwt_token(
        payload={"user_id": TEST_USER_FOR_PROFILE_DB["user_id"]},
        private_key_path=JWT_TEST_DATA["private_key_access_jwt_path"],
        expire_minutes=JWT_TEST_DATA["ACCESS_TOKEN_EXPIRE_MINUTES"],
        algorithm=JWT_TEST_DATA["algorithm"],
    )
    response = await client.request(
        "PATCH",
        "/api/v1/profile/update",
        headers={"Authorization": f"Bearer {access_token}"},
        json=PROFILE_CITY_DOSE_NOT_EXIST,
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"] == "City object dose not exist in location datatable"
    )

    response = await client.request(
        "PATCH",
        "/api/v1/profile/update",
        headers={"Authorization": f"Bearer {access_token}"},
        json=PROFILE_FAKE_LOCATION,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Location data is invalid"

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_delete_profile(client, override_session):
    """Тестуємо видалення профілю"""
    access_token = await create_jwt_token(
        payload={"user_id": TEST_USER_FOR_PROFILE_DB["user_id"]},
        private_key_path=JWT_TEST_DATA["private_key_access_jwt_path"],
        expire_minutes=JWT_TEST_DATA["ACCESS_TOKEN_EXPIRE_MINUTES"],
        algorithm=JWT_TEST_DATA["algorithm"],
    )
    response = await client.request(
        "DELETE",
        "/api/v1/profile/delete",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert response.json()["msg"] == "User profile success deleted"

    response_profile_not_exist = await client.request(
        "DELETE",
        "/api/v1/profile/delete",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response_profile_not_exist.status_code == 400
    assert response_profile_not_exist.json()["detail"] == "Profile does not exist"

    app.dependency_overrides.clear()
