import pytest
import json

from main import app
from src.test_app.data_for_test import TEST_USER_API


@pytest.mark.asyncio
async def test_registration_user(client):
    """Тест реєстрації користувача"""

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
    assert resp["is_active"] == True
    assert resp["valid_email"] == False
    assert resp["is_staff"] == False
    assert resp["is_superuser"] == False

    response_2 = await client.post(
        "/api/v1/auth/registration",
        json=TEST_USER_API,
    )
    assert response_2.__dict__["status_code"] == 400
    assert (
        json.loads(response_2.__dict__["_content"].decode("utf-8"))["detail"]
        == "User already exists"
    )
    app.dependency_overrides.clear()
