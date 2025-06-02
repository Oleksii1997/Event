import datetime
from pytz import timezone
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, field_validator

from src.app.users.schemas import UserBase
from src.app.location.schemas import AreaBase, RegionBase, CommunityBase, CityBase


class ValidateBirthday:
    """Перевіряємо на валідність дату народження, вона не може бути менш як 0 та більше ніж 120 років"""

    @field_validator("birthday")
    @classmethod
    def validate_birthday(cls, birthday: datetime.date):
        error_str = ""
        if datetime.datetime.now(tz=timezone("Europe/Kyiv")).date() <= birthday:
            error_str = "Birthday date validation error. The date of birth must be earlier than the current date. \n"
        elif datetime.datetime.now(
            tz=timezone("Europe/Kyiv")
        ).date() >= birthday + datetime.timedelta(days=40 * 366 + 80 * 365):
            error_str = (
                error_str
                + "Error validating date of birth. Date of birth must be no older than 120 years."
            )
        else:
            pass
        if error_str:
            raise ValueError(error_str)
        return birthday


class ProfileBase(BaseModel, ValidateBirthday):
    """Модель створення профілю користувача"""

    birthday: datetime.date
    description: str
    area: int
    region: int
    community: int
    city: int


class ProfileReplayBase(ProfileBase):
    """Відповідаємо при створенні нового профілю"""

    id: UUID = Field(default_factory=uuid4)
    profile_user: UserBase
    created_at: datetime.datetime
    updated_at: datetime.datetime


class ProfileReplayFullBase(BaseModel, ValidateBirthday):
    """Модель профілю, повна, при відповіді даних профілю"""

    id: UUID = Field(default_factory=uuid4)
    profile_user: UserBase
    birthday: datetime.date
    description: str
    profile_area: AreaBase
    profile_region: RegionBase
    profile_community: CommunityBase
    profile_city: CityBase
    created_at: datetime.datetime
    updated_at: datetime.datetime
