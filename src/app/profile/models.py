import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from uuid import UUID, uuid4
from typing import List, Optional

# from src.app.location.models import CommunityModel
from src.config.models import (
    Base,
    str_256,
    str_1024,
    created_at,
    updated_at,
)

# from src.app.location.models import RegionModel, AreaModel, CityModel


class ProfileModel(Base):
    """Модель профелю користувача"""

    __tablename__ = "profile_table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user_table.id", ondelete="CASCADE")
    )
    user: Mapped["UserModel"] = relationship(back_populates="profile")
    avatar: Mapped[List["AvatarModel"]] = relationship(back_populates="profile_avatar")
    video_profile: Mapped["VideoProfileModel"] = relationship(
        back_populates="profile_video"
    )
    birthday: Mapped[datetime.datetime] = mapped_column(nullable=True)
    description: Mapped[Optional[str_1024]] = mapped_column(nullable=True)
    social_link: Mapped["SocialLinkModel"] = relationship(
        back_populates="profile_social"
    )

    area: Mapped[int] = mapped_column(ForeignKey("area_table.id", ondelete="CASCADE"))
    profile_area: Mapped["AreaModel"] = relationship(back_populates="area_profile")

    region: Mapped[int] = mapped_column(
        ForeignKey("region_table.id", ondelete="CASCADE")
    )
    profile_region: Mapped["RegionModel"] = relationship(
        back_populates="region_profile"
    )

    community: Mapped[int] = mapped_column(
        ForeignKey("community_table.id", ondelete="CASCADE")
    )
    profile_community: Mapped["CommunityModel"] = relationship(
        back_populates="community_profile"
    )

    city: Mapped[UUID] = mapped_column(ForeignKey("city_table.id", ondelete="CASCADE"))
    profile_city: Mapped["CityModel"] = relationship(back_populates="city_profile")

    created_at: Mapped[Optional[created_at]]
    updated_at: Mapped[Optional[updated_at]]


class AvatarModel(Base):
    """Модель зображення профелю"""

    __tablename__ = "avatar_table"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    avatar_url: Mapped[Optional[str_256]] = mapped_column(nullable=False)
    profile_id: Mapped[UUID] = mapped_column(
        ForeignKey("profile_table.id", ondelete="CASCADE")
    )
    created_at: Mapped[Optional[created_at]]
    updated_at: Mapped[Optional[updated_at]]

    profile_avatar: Mapped["ProfileModel"] = relationship(back_populates="avatar")


class VideoProfileModel(Base):
    """Модель відео для інформації про профіль"""

    __tablename__ = "video_profile_table"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    video_url: Mapped[Optional[str_256]] = mapped_column(nullable=False)
    profile_id: Mapped[UUID] = mapped_column(
        ForeignKey("profile_table.id", ondelete="CASCADE")
    )
    created_at: Mapped[Optional[created_at]]

    updated_at: Mapped[Optional[updated_at]]

    profile_video: Mapped["ProfileModel"] = relationship(back_populates="video_profile")


class SocialLinkModel(Base):
    """Модель посилань на соціальні мережі"""

    __tablename__ = "social_link_table"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    link: Mapped[Optional[str_256]] = mapped_column(nullable=False)
    profile_id: Mapped[UUID] = mapped_column(
        ForeignKey("profile_table.id", ondelete="CASCADE")
    )
    profile_social: Mapped[ProfileModel] = relationship(back_populates="social_link")
