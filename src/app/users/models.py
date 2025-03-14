import datetime
from sqlalchemy import text, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID, uuid4
from typing import Annotated

from src.config.models import Base


"""creating a new object type for some database fields"""
str_64 = Annotated[str, 64]
str_48 = Annotated[str, 48]
str_16 = Annotated[str, 16]
str_128 = Annotated[str, 128]
bytes_256 = Annotated[bytes, 256]
created_at = Annotated[
    datetime.datetime, mapped_column(DateTime(timezone=True), server_default=func.now())
]
updated_at = Annotated[
    datetime.datetime,
    mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    ),
]


class UserModel(Base):
    """User model"""

    __tablename__: str = "user"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    firstname: Mapped[str_48]
    lastname: Mapped[str_48]
    phone_number: Mapped[str_16] = mapped_column(unique=True)
    password: Mapped[bytes_256]
    email: Mapped[str_64] = mapped_column(unique=True)
    valid_email: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_staff: Mapped[bool] = mapped_column(default=False)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    # verification: Mapped["VerificationModel"] = relationship(back_populates="user", uselist=False, cascade="all, delete")


class ProfileModel(Base):
    """Profile user model"""

    __tablename__ = "profile"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    birthday: Mapped[datetime.datetime] = mapped_column(default=None)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
