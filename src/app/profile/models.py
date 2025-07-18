import datetime
from sqlalchemy import UniqueConstraint, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from uuid import UUID, uuid4
from typing import List, Optional, Literal, get_args
from sqlalchemy import Enum

# from src.app.location.models import CommunityModel
from src.config.models import (
    Base,
    str_128,
    str_256,
    str_1024,
    created_at,
    updated_at,
)

# from src.app.location.models import RegionModel, AreaModel, CityModel


class ProfileModel(Base):
    """Модель профелю користувача"""

    __tablename__ = "profile_table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, index=True)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user_table.id", ondelete="CASCADE")
    )
    profile_user: Mapped["UserModel"] = relationship(back_populates="user_profile")
    profile_avatar: Mapped[list["AvatarModel"]] = relationship(
        back_populates="avatar_profile",
        cascade="all, delete-orphan",
    )
    profile_video: Mapped[Optional["VideoProfileModel"]] = relationship(
        back_populates="video_profile", cascade="all, delete-orphan", uselist=False
    )
    birthday: Mapped[datetime.datetime] = mapped_column(nullable=True)
    description: Mapped[Optional[str_1024]] = mapped_column(nullable=True)
    profile_social_link: Mapped[list["SocialLinkModel"]] = relationship(
        back_populates="social_link_profile",
        cascade="all, delete",
        passive_deletes=True,
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

    __table_args__ = (UniqueConstraint("user_id"),)


class AvatarModel(Base):
    """Модель зображення профелю"""

    __tablename__ = "avatar_table"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    avatar_url: Mapped[Optional[str_256]] = mapped_column(nullable=False)
    profile_id: Mapped[UUID] = mapped_column(
        ForeignKey("profile_table.id", ondelete="CASCADE")
    )
    created_at: Mapped[Optional[created_at]]

    avatar_profile: Mapped["ProfileModel"] = relationship(
        back_populates="profile_avatar"
    )


class VideoProfileModel(Base):
    """Модель відео для інформації про профіль"""

    __tablename__ = "video_profile_table"
    __table_args__ = (UniqueConstraint("profile_id", name="uq_video_per_profile"),)

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    video_url: Mapped[Optional[str_256]] = mapped_column(nullable=False)
    profile_id: Mapped[UUID] = mapped_column(
        ForeignKey("profile_table.id", ondelete="CASCADE")
    )
    created_at: Mapped[Optional[created_at]]

    video_profile: Mapped["ProfileModel"] = relationship(back_populates="profile_video")


TypeSocialLinkEnum = Literal[
    "Facebook",
    "Instagram",
    "Linkedin",
    "Twitter",
    "YouTube",
    "TikTok",
    "WhatsApp",
    "Telegram",
    "Viber",
    "Signal",
    "Pinterest",
    "Reddit",
    "Website",
]


class SocialLinkModel(Base):
    """Модель посилань на соціальні мережі"""

    __tablename__ = "social_link_table"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    link_type: Mapped[TypeSocialLinkEnum] = mapped_column(
        Enum(
            *get_args(TypeSocialLinkEnum),
            name="link_type",
            create_constraint=True,
            validate_strings=True
        ),
    )
    link: Mapped[Optional[str_256]] = mapped_column(nullable=False)
    profile_id: Mapped[UUID] = mapped_column(
        ForeignKey("profile_table.id", ondelete="CASCADE")
    )
    social_link_profile: Mapped[ProfileModel] = relationship(
        back_populates="profile_social_link"
    )
