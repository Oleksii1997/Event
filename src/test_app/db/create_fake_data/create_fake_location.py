from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import text
from src.test_app.db.data_for_test import (
    AREA_TEST_DATA,
    REGION_TEST_DATA,
    COMMUNITY_TEST_DATA,
    CITY_TEST_DATA,
)


class FakeLocationDB:
    """Клас запису тестових даних в таблицю областей, районів, громад та населених пунктів"""

    def __init__(self, conn: AsyncConnection):
        self.conn = conn

    async def create_fake_area(self):
        """Запис тестових даних в таблицю областей"""
        query = 'INSERT INTO "area_table" (id, area_name) VALUES '
        for item in AREA_TEST_DATA:
            query = query + f"('{item['id']}', '{item['area_name']}'), "
        await self.conn.execute(text(query[:-2]))

    async def create_fake_region(self):
        """Запис тестових даних в таблицю районів"""
        query = 'INSERT INTO "region_table" (id, region_name, area_id) VALUES'
        for item in REGION_TEST_DATA:
            query = (
                query
                + f"('{item['id']}', '{item['region_name']}', '{item['area_id']}'), "
            )
        await self.conn.execute(text(query[:-2]))

    async def create_fake_community(self):
        """Запис тестових даних в таблицю громад"""
        query = 'INSERT INTO "community_table" (id, community_name, region_id) VALUES'
        for item in COMMUNITY_TEST_DATA:
            query = (
                query
                + f"('{item['id']}', '{item['community_name']}', '{item['region_id']}'), "
            )
        await self.conn.execute(text(query[:-2]))

    async def create_fake_city(self):
        """Запис тестових даних в таблицю населених пунктів"""
        query = 'INSERT INTO "city_table" (id, city_name, community_id) VALUES'
        for item in CITY_TEST_DATA:
            query = (
                query
                + f"('{item['id']}', '{item['city_name']}', '{item['community_id']}'), "
            )
        await self.conn.execute(text(query[:-2]))

    async def fake_location_db(self):
        """Наповнюємо таблицю локацій тестовими даними
        Послідовність наповнення важлива, тому що таблиці містять зв'язки ForeignKey"""
        await self.create_fake_area()
        await self.create_fake_region()
        await self.create_fake_community()
        await self.create_fake_city()
