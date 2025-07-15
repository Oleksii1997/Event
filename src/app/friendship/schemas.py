from typing import Optional
from uuid import UUID, uuid4
import datetime
from pydantic import BaseModel, Field, field_validator
from src.app.profile.schemas import AvatarBase, VideoBase


class CreateFriendshipRequestBase(BaseModel):
    """Модель запитів на дружбу"""

    sender_id: UUID = Field(default_factory=uuid4)
    receiver_id: UUID = Field(default_factory=uuid4)


class FriendshipRequestBase(CreateFriendshipRequestBase):
    """Повна модель заявок на дружбу"""

    id: UUID = Field(default_factory=uuid4)
    created_at: datetime.datetime


class CreateFriendshipBase(BaseModel):
    """Модель підписників"""

    user_id: UUID = Field(default_factory=uuid4)
    friend_id: UUID = Field(default_factory=uuid4)


class FriendshipBase(CreateFriendshipBase):
    """Повна модель підписників"""

    id: UUID = Field(default_factory=uuid4)
    created_at: datetime.datetime


class FriendshipAvatarBase(BaseModel):
    """Модель посилань на аватарки"""

    avatar_url: str


class FriendshipVideoBase(BaseModel):
    """Модель посилань на відео"""

    video_url: str


class MySubscribers(BaseModel):
    """Модель яка повертає інформацію про підписників (ті хто підписаний на нас)"""

    user_id: UUID = Field(default_factory=uuid4)
    first_name: str
    last_name: str
    avatar: list[Optional[FriendshipAvatarBase]]
    video: list[Optional[FriendshipVideoBase]]


class ISubscribe(BaseModel):
    """Модель яка повертає інформацію про друзів (на кого я підписаний)"""

    user_id: UUID = Field(default_factory=uuid4)
    first_name: str
    last_name: str
    avatar: list[Optional[FriendshipAvatarBase]]
    video: list[Optional[FriendshipVideoBase]]
