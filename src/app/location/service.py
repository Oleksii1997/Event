from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload, contains_eager
from sqlalchemy import select, text, func

from src.app.location.models import AreaModel, RegionModel, CommunityModel, CityModel
from src.app.location.schemas import (
    AreaBase,
    RegionBase,
    CommunityBase,
    CityBase,
    CityCommunityRegionAreaBase,
)


class AreaLocationService:
    """Клас роботи з об'єктами локації (області)"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_area(self) -> list[AreaBase]:
        """Отримуємо список областей"""
        query = select(AreaModel).order_by("area_name")
        result = await self.session.execute(query)
        areas = result.scalars().all()
        all_area = []
        if areas is not None:
            for item in areas:
                all_area.append(AreaBase.model_validate(item.__dict__))
        return all_area


class RegionLocationService:
    """Клас для роботи з об'єктами локації (районні центри)"""

    def __init__(self, session: AsyncSession, area_id: int):
        self.session = session
        self.area_id = area_id

    async def get_region_in_area(self) -> list[RegionBase]:
        """Отримуємо список районів обраної області"""
        query = select(RegionModel).where(RegionModel.area_id == self.area_id)
        result = await self.session.execute(query)
        regions = result.scalars().all()
        all_regions = []
        if regions is not None:
            for item in regions:
                all_regions.append(RegionBase.model_validate(item.__dict__))
        return all_regions


class CommunityLocationService:
    """Клас для роботи з об'єктами локації (територіальні громади)"""

    def __init__(self, session: AsyncSession, region_id: int):
        self.session = session
        self.region_id = region_id

    async def get_community_in_region(self) -> list[CommunityBase]:
        """Отримуємо громади певного району"""
        query = select(CommunityModel).where(CommunityModel.region_id == self.region_id)
        result = await self.session.execute(query)
        community = result.scalars().all()
        all_community = []
        if community is not None:
            for item in community:
                all_community.append(CommunityBase.model_validate(item.__dict__))
        return all_community


class CityLocationService:
    """Клас для роботи з об'єктами локації (населені пункти)"""

    def __init__(
        self,
        session: AsyncSession,
        community_id: int = None,
        search_field: str = None,
        city_id: int = None,
    ) -> None:
        self.session = session
        self.community_id = community_id
        self.search_field = search_field
        self.city_id = city_id

    async def get_city_in_community(self) -> list[CityBase]:
        """Отримуємо список населених пунктів певної громади"""
        query = select(CityModel).where(CityModel.community_id == self.community_id)
        result = await self.session.execute(query)
        city = result.scalars().all()
        all_city = []
        if city is not None:
            for item in city:
                all_city.append(CityBase.model_validate(item.__dict__))
        return all_city

    async def get_city_by_search_name(self) -> list[CityCommunityRegionAreaBase]:
        """Отримуємо список населених пунктів по пошуковій фразі"""

        query = (
            select(CityModel)
            .join(CommunityModel)
            .join(RegionModel)
            .join(AreaModel)
            .options(
                contains_eager(CityModel.city_community)
                .contains_eager(CommunityModel.community_region)
                .contains_eager(RegionModel.region_area)
            )
            .where(CityModel.city_name.icontains(self.search_field))
            .limit(50)
        )

        result = await self.session.execute(query)
        city = result.unique().scalars().all()
        all_city_full = [
            CityCommunityRegionAreaBase.model_validate(item, from_attributes=True)
            for item in city
        ]
        return all_city_full

    async def get_info_by_city_id(self) -> CityCommunityRegionAreaBase | None:
        """Отримуємо вкладену модель, інформації про населений пункт. З ID населеного пункту отримуємо
        область, район та громаду до яких відноситься даний населений пункт"""
        query = (
            select(CityModel)
            .join(CommunityModel)
            .join(RegionModel)
            .join(AreaModel)
            .options(
                contains_eager(CityModel.city_community)
                .contains_eager(CommunityModel.community_region)
                .contains_eager(RegionModel.region_area)
            )
            .where(CityModel.id == self.city_id)
        )
        result = await self.session.execute(query)
        city = result.unique().scalars().one_or_none()
        if city is None:
            return None
        return CityCommunityRegionAreaBase.model_validate(city, from_attributes=True)
