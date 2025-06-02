import datetime
from uuid import UUID
from pydantic import BaseModel

from src.app.users.schemas import UserBase
from src.app.location.schemas import AreaBase, RegionBase, CommunityBase, CityBase


class ProfileBase(BaseModel):
    """Модель створення профілю користувача"""

    birthday: datetime.date
    description: str
    area: int
    region: int
    community: int
    city: int


class ProfileReplayBase(ProfileBase):
    """Відповідаємо при створенні нового профілю"""

    id: UUID
    profile_user: UserBase
    created_at: datetime.datetime
    updated_at: datetime.datetime


class ProfileReplayFullBase(BaseModel):
    """Модель профілю, повна, при відповіді даних профілю"""

    id: UUID
    profile_user: UserBase
    birthday: datetime.date
    description: str
    profile_area: AreaBase
    profile_region: RegionBase
    profile_community: CommunityBase
    profile_city: CityBase
    created_at: datetime.datetime
    updated_at: datetime.datetime
