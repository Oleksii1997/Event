from typing import Optional
from uuid import UUID
from fastapi import HTTPException, status
from fastapi.params import Depends

from sqlalchemy import select

from src.app.users.schemas import NewUserBase, UserBase
from src.config.db_settings import new_session
from src.app.users.models import UserModel
from src.app.auth.security import get_password_hash, verify_password


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
