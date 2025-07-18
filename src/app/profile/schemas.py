import datetime
from pytz import timezone
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, field_validator
from enum import Enum

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


class ProfileUUIDBase(BaseModel):
    """Модель UUID"""

    id: UUID = Field(default_factory=uuid4)


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


class SocialLinkTypeEnum(str, Enum):
    facebook = "Facebook"
    instagram = "Instagram"
    linkedin = "Linkedin"
    twitter = "Twitter"
    youtube = "YouTube"
    tiktok = "TikTok"
    whatsapp = "WhatsApp"
    telegram = "Telegram"
    viber = "Viber"
    signal = "Signal"
    pinterest = "Pinterest"
    reddit = "Reddit"
    website = "Website"


class ProfileSocialLinkCreateBase(BaseModel):
    """Модель посилань на соцмережі, при створенні"""

    link_type: SocialLinkTypeEnum
    link: str


class ProfileSocialLincCreateReturnBase(BaseModel):
    profile_id: UUID = Field(default_factory=uuid4)
    social_link: list[ProfileSocialLinkCreateBase]


class ProfileSocialLinkBase(BaseModel):
    """Модель соціальних мереж"""

    id: UUID = Field(default_factory=uuid4)
    link_type: SocialLinkTypeEnum
    link: str
    profile_id: UUID = Field(default_factory=uuid4)


class ProfileWithSocialLinkBase(ProfileReplayBase):
    """Профіль з посиланнями на соціальні мережі"""

    profile_social_link: list[ProfileSocialLinkBase]


class AvatarBase(BaseModel):
    """Модель аватарок"""

    id: UUID = Field(default_factory=uuid4)
    avatar_url: str
    profile_id: UUID = Field(default_factory=uuid4)
    created_at: datetime.datetime


class CreateAvatarBase(BaseModel):
    """Модель створення нового аватару"""

    avatar_url: str
    profile_id: UUID = Field(default_factory=uuid4)


class VideoBase(BaseModel):
    """Модель відео профілю"""

    id: UUID = Field(default_factory=uuid4)
    video_url: str
    profile_id: UUID = Field(default_factory=uuid4)
    # created_at: datetime.datetime


class CreateVideoBase(BaseModel):
    """Модель створення нового відео"""

    video_url: str
    profile_id: UUID = Field(default_factory=uuid4)
