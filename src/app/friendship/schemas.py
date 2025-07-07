from uuid import UUID, uuid4
import datetime
from pydantic import BaseModel, Field, field_validator


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
