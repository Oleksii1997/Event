from typing import List

from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.params import Depends

from src.app.location.schemas import (
    AreaBase,
    RegionBase,
    CommunityBase,
    CityBase,
    CityCommunityRegionAreaBase,
)
from src.config.db_settings import get_session
from src.app.location.service import (
    AreaLocationService,
    RegionLocationService,
    CommunityLocationService,
    CityLocationService,
)

location_router = APIRouter(
    prefix="/location",
    tags=["location"],
)


@location_router.get("/areas", response_model=list[AreaBase])
async def all_area(
    session: AsyncSession = Depends(get_session),
) -> list[AreaBase]:
    """Повертаємо список всіх областей"""
    areas = await AreaLocationService(session=session).get_all_area()
    return areas


@location_router.get("/regions/{area_id}", response_model=list[RegionBase])
async def regions_in_area(
    area_id: int, session: AsyncSession = Depends(get_session)
) -> list[RegionBase]:
    """Повертаємо список районів певної області"""
    regions = await RegionLocationService(
        session=session, area_id=area_id
    ).get_region_in_area()
    return regions


@location_router.get("/community/{region_id}", response_model=list[CommunityBase])
async def community_in_region(
    region_id: int, session: AsyncSession = Depends(get_session)
) -> list[CommunityBase]:
    """Повертає список громад певного району"""
    community = await CommunityLocationService(
        session=session, region_id=region_id
    ).get_community_in_region()
    return community


@location_router.get("/city/{community_id}", response_model=list[CityBase])
async def city_in_community(
    community_id: int, session: AsyncSession = Depends(get_session)
) -> list[CityBase]:
    """Повертаємо список населених пунктів громади"""
    city = await CityLocationService(
        session=session, community_id=community_id
    ).get_city_in_community()
    return city


@location_router.get(
    "/city/search/{search_field}", response_model=list[CityCommunityRegionAreaBase]
)
async def city_search(
    search_field: str, session: AsyncSession = Depends(get_session)
) -> list[CityCommunityRegionAreaBase]:
    """Пошук населеного пункту по назві. Пошук ведеться по фразі, і використовує Fuzzy text search"""
    city = await CityLocationService(
        session=session, search_field=search_field
    ).get_city_by_search_name()
    return city
