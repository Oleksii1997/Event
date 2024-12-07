import datetime
from cgi import maxlen
from email.policy import default

from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID, uuid4
from typing import Annotated, Optional

from src.config.models import Base

"""creating a new object type for some database fields"""
str_64 = Annotated[str,64]
str_48 = Annotated[str, 48]
str_16 = Annotated[str, 16]
str_128 = Annotated[str, 128]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('UTC', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('UTC', now())"),
                                                        onupdate=datetime.datetime.now(datetime.UTC))]

class UserModel(Base):
    """User model"""
    __tablename__: str = "user"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    firstname: Mapped[str_48]
    lastname: Mapped[str_48]
    phone_number: Mapped[str_16] = mapped_column(unique=True)
    password: Mapped[str_128]
    email: Mapped[str_64] = mapped_column(unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_staff: Mapped[bool] = mapped_column(default=False)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

class ProfileModel(Base):
    """Profile user model"""
    __tablename__ = "profile"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    birthday: Mapped[datetime.datetime] = mapped_column(default=None)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
