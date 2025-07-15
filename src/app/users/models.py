from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID, uuid4
from typing import Optional, List

from src.config.models import (
    Base,
    str_16,
    str_64,
    str_48,
    str_128,
    bytes_256,
    created_at,
    updated_at,
)
from src.app.profile.models import ProfileModel
from src.app.friendship.models import FriendshipModel, FriendshipRequestModel


class UserModel(Base):
    """User model"""

    __tablename__: str = "user_table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, index=True)
    firstname: Mapped[Optional[str_48]] = mapped_column(nullable=False)
    lastname: Mapped[Optional[str_48]] = mapped_column(nullable=False)
    phone_number: Mapped[Optional[str_16]] = mapped_column(
        nullable=False, unique=True, index=True
    )
    password: Mapped[Optional[bytes_256]] = mapped_column(nullable=False)
    email: Mapped[Optional[str_64]] = mapped_column(nullable=False, unique=True)
    valid_email: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_staff: Mapped[bool] = mapped_column(default=False)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[Optional[created_at]]
    updated_at: Mapped[Optional[updated_at]]

    user_profile: Mapped["ProfileModel"] = relationship(back_populates="profile_user")
