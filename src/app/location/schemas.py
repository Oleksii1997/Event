from pydantic import BaseModel


class AreaBase(BaseModel):
    """схема відобреження області"""

    id: int
    area_name: str


class RegionBase(BaseModel):
    """схема відображення районів"""

    id: int
    region_name: str
    area_id: int


class CommunityBase(BaseModel):
    """Схема відображення громад"""

    id: int
    community_name: str
    region_id: int


class CityBase(BaseModel):
    """Схема відображення населених пунктів"""

    id: int
    city_name: str
    community_id: int


class RegionAreaBase(RegionBase):
    """Схема для районів з вкладеною областю"""

    region_area: AreaBase


class CommunityRegionAreaBase(CommunityBase):
    """Схема для громад з вкладеним районом та областю"""

    community_region: RegionAreaBase


class CityCommunityRegionAreaBase(CityBase):
    """Схема населених пунктів з вкладеними громадою, районом та областю"""

    city_community: CommunityRegionAreaBase
