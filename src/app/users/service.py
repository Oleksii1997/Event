from typing import Optional
from uuid import UUID
from fastapi import HTTPException, status
from fastapi.params import Depends

from sqlalchemy import select

from src.app.users.schemas import NewUserBase, UserBase
from src.config.db_settings import new_session
from src.app.users.models import UserModel
from src.app.auth.security import get_password_hash, verify_password

from src.app.auth.jwt_auth_service import get_payload_access_token


class UserService:
    """Сlass for working with the user profile and hash password"""

    @classmethod
    async def created_user(cls, data: NewUserBase):
        async with new_session() as session:
            user_dict: dict = data.model_dump()
            user_dict["password"] = get_password_hash(user_dict["password"])
            user = UserModel(**user_dict)
            session.add(user)
            await session.flush()
            await session.commit()
            return user

    @classmethod
    async def authenticate(
        cls, phone_number: str, password: str
    ) -> Optional[UserModel]:
        """Аутенифікація та перевірка пароля користувача"""
        async with new_session() as session:
            query = select(UserModel).where(UserModel.phone_number == phone_number)
            result = await session.execute(query)
            user = result.scalars().one_or_none()
            if not user:
                return None
            if not verify_password(password, user.password):
                return None
            return user

    @classmethod
    async def check_valid_email(cls, user_id: UUID):
        """Змінюємо статус валідності електронної адреси моделі користувача"""
        async with new_session() as session:
            query = select(UserModel).where(UserModel.id == user_id)
            result = await session.execute(query)
            user = result.scalars().one_or_none()
            if user:
                user.valid_email = True
                # session.add(user)
                await session.commit()
            else:
                raise HTTPException(status_code=400, detail="User not exists")

    @classmethod
    async def get_user(cls, user_id: UUID) -> UserBase | None:
        """Отримуємо користувача"""
        async with new_session() as session:
            query = select(UserModel).where(UserModel.id == user_id)
            result = await session.execute(query)
            user = result.scalars().one_or_none()
            if user is not None:
                user = UserBase.model_validate(user.__dict__)
            return user


async def get_current_auth_user(
    payload: dict = Depends(get_payload_access_token),
) -> UserBase:
    """Отримуємо користувача з токена (в токені передається user_id)"""

    user_id: UUID | None = payload.get("user_id")

    if user_id is not None:
        user = await UserService.get_user(user_id=user_id)
        if user is not None:
            return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalid (user not found)",
    )


async def get_current_active_auth_user(user: UserBase = Depends(get_current_auth_user)):
    """Перевіряємо чи користувач активний"""
    if user.is_active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User inactive",
    )
