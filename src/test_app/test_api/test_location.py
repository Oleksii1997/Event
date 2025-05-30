import pytest
import json

from src.test_app.db.data_for_test import (
    AREA_TEST_DATA,
    REGION_TEST_DATA,
    COMMUNITY_TEST_DATA,
    CITY_TEST_DATA,
    TEST_AREA_ID,
    TEST_REGION_ID,
    TEST_COMMUNITY_ID,
    TEST_FAKE_ID,
    TEST_SEARCH_STRING_1,
    TEST_SEARCH_STRING_2,
    LEN_TEST_SEARCH_1,
    LEN_TEST_SEARCH_2,
    RESULT_SEARCH_2,
    FAKE_SEARCH_STRING,
)


@pytest.mark.asyncio
async def test_all_area(client, override_session):
    """Перевіряємо api отримання областей"""
    response = await client.get(
        "/api/v1/location/areas",
    )
    resp: list[dict] = response.json()
    assert response.status_code == 200
    assert len(AREA_TEST_DATA) == len(resp)
    for item in resp:
        assert True if item in AREA_TEST_DATA else False


@pytest.mark.asyncio
async def test_regions_in_area(client, override_session):
    """Перевіряємо api отримання областей"""

    response = await client.get(
        f"/api/v1/location/regions/{TEST_AREA_ID}",
    )
    resp: list[dict] = response.json()
    assert response.status_code == 200
    assert len(REGION_TEST_DATA) == len(resp)
    for resp_item in resp:
        assert True if resp_item in REGION_TEST_DATA else False

    response = await client.get(
        f"/api/v1/location/regions/{TEST_FAKE_ID}",
    )
    assert response.status_code == 200
    assert 0 == len(response.json())


@pytest.mark.asyncio
async def test_community_in_region(client, override_session):
    """Перевіряємо api отримання громад"""
    response = await client.get(f"/api/v1/location/community/{TEST_REGION_ID}")
    resp: list[dict] = response.json()
    assert response.status_code == 200
    assert len(COMMUNITY_TEST_DATA) == len(resp)
    for resp_item in resp:
        assert True if resp_item in COMMUNITY_TEST_DATA else False

    response = await client.get(
        f"/api/v1/location/community/{TEST_FAKE_ID}",
    )
    assert response.status_code == 200
    assert 0 == len(response.json())


@pytest.mark.asyncio
async def test_city_in_community(client, override_session):
    """Перевіряємо api населених пунктів в громаді"""
    response = await client.get(f"/api/v1/location/city/{TEST_COMMUNITY_ID}")
    resp: list[dict] = response.json()
    assert response.status_code == 200
    assert len(CITY_TEST_DATA) == len(resp)
    for resp_item in resp:
        assert True if resp_item in CITY_TEST_DATA else False

    response = await client.get(
        f"/api/v1/location/city/{TEST_FAKE_ID}",
    )
    assert response.status_code == 200
    assert 0 == len(response.json())


@pytest.mark.asyncio
async def test_city_search(client, override_session):
    """Перевіряємо пошук населених пунктів по назві"""
    response = await client.get(f"/api/v1/location/city/search/{TEST_SEARCH_STRING_1}")
    resp: list[dict] = response.json()
    assert response.status_code == 200
    assert LEN_TEST_SEARCH_1 == len(resp)
    for resp_item in resp:
        city = {
            "id": resp_item["id"],
            "city_name": resp_item["city_name"],
            "community_id": resp_item["community_id"],
        }
        assert True if city in CITY_TEST_DATA else False

    response = await client.get(f"/api/v1/location/city/search/{TEST_SEARCH_STRING_2}")
    resp: list[dict] = response.json()
    assert response.status_code == 200
    assert LEN_TEST_SEARCH_2 == len(resp)
    for resp_item in resp:
        assert True if resp_item in RESULT_SEARCH_2 else False

    response = await client.get(f"/api/v1/location/city/search/{FAKE_SEARCH_STRING}")
    assert response.status_code == 200
    assert 0 == len(response.json())
