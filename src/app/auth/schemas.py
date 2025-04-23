from pydantic import BaseModel, Field, EmailStr
from uuid import UUID, uuid4
from typing import Optional
from src.app.users.schemas import UserBase


class MsgBase(BaseModel):
    """Схема для відповіді при реєстрації користувача"""

    msg: str


class CreateUserResponseBase(UserBase):
    """Схема для відповіді під час реєстрації користувача"""

    msg: str


class MsgUserBase(BaseModel):
    """Схема для відповіді при реєстрації користувача"""

    msg: str
    user_id: UUID = Field(default_factory=uuid4)


class VerificationBase(BaseModel):
    """Схема для створення верифікаційного запису"""

    user_id: UUID = Field(default_factory=uuid4)


class VerificationEmailBase(BaseModel):
    """Схема для UUID при верифікації електронної пошти користувача"""

    link: UUID = Field(default_factory=uuid4)


class AuthToken(BaseModel):
    """Схема для токена"""

    access_token: str
    refresh_token: str | None
    token_type: str = "Bearer"
