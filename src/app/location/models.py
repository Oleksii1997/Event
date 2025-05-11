from alembic.operations.toimpl import drop_table
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from typing import Optional

from src.config.models import Base, str_32


class AreaModel(Base):
    """Модель областей"""

    __tablename__ = "area_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    area_name: Mapped[Optional[str_32]] = mapped_column(nullable=True)
    area_region: Mapped[List["RegionModel"]] = relationship(
        back_populates="region_area"
    )
    area_profile: Mapped["ProfileModel"] = relationship(back_populates="profile_area")


class RegionModel(Base):
    """Модель районів"""

    __tablename__ = "region_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    region_name: Mapped[Optional[str_32]] = mapped_column(nullable=True)
    area_id: Mapped[int] = mapped_column(
        ForeignKey("area_table.id", ondelete="CASCADE")
    )
    region_area: Mapped["AreaModel"] = relationship(back_populates="area_region")
    region_community: Mapped[List["CommunityModel"]] = relationship(
        back_populates="community_region"
    )
    region_profile: Mapped["ProfileModel"] = relationship(
        back_populates="profile_region"
    )


class CommunityModel(Base):
    """Модель громад"""

    __tablename__ = "community_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    community_name: Mapped[Optional[str_32]] = mapped_column(nullable=True)
    region_id: Mapped[int] = mapped_column(
        ForeignKey("region_table.id", ondelete="CASCADE")
    )
    community_region: Mapped["RegionModel"] = relationship(
        back_populates="region_community"
    )
    community_city: Mapped[List["CityModel"]] = relationship(
        back_populates="city_community"
    )
    community_profile: Mapped["ProfileModel"] = relationship(
        back_populates="profile_community"
    )


class CityModel(Base):
    """Модель населених пунктів"""

    __tablename__ = "city_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Optional[str_32]] = mapped_column(nullable=True)
    community_id: Mapped[int] = mapped_column(
        ForeignKey("community_table.id", ondelete="CASCADE")
    )
    city_community: Mapped["CommunityModel"] = relationship(
        back_populates="community_city"
    )
    city_profile: Mapped["ProfileModel"] = relationship(back_populates="profile_city")
