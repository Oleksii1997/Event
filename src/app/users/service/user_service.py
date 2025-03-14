from fastapi import HTTPException
from typing import Optional
from uuid import UUID
from sqlalchemy import select

from src.config.db_settings import new_session
from src.app.auth.security import get_password_hash, verify_password
from src.app.users.schemas import NewUserBase, UserBase
from src.app.users.models import UserModel


class UserService:
    """Клас для роботи з профілем користувача під час реєстрації, аутентифікації та відновлення пароля"""

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

    @classmethod
    async def get_user_by_email(cls, email: str) -> UserBase | None:
        """Отримуємо користувача"""
        async with new_session() as session:
            query = select(UserModel).where(UserModel.email == email)
            result = await session.execute(query)
            user = result.scalars().one_or_none()
            if user is not None:
                user = UserBase.model_validate(user.__dict__)
            return user

    @classmethod
    async def recovery_password(cls, user_id: UUID, password: str) -> bool:
        """Отримуємо користувача та змінюємо пароль. Повертаємо True якщо пароль змінено і False якщо
        користувача не існує"""
        async with new_session() as session:
            query = select(UserModel).where(UserModel.id == user_id)
            result = await session.execute(query)
            user = result.scalars().one_or_none()
            if user is not None:
                user.password = get_password_hash(password)
                await session.commit()
                return True
            return False
