from fastapi import HTTPException
from typing import Optional
from uuid import UUID
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr
from fastapi import BackgroundTasks

from src.config.settings import SERVER_HOST
from src.config.db_settings import new_session
from src.app.auth.security import get_password_hash, verify_password
from src.app.auth.schemas import VerificationBase
from src.app.users.schemas import NewUserBase, UserBase, UpdateUserBase
from src.app.users.models import UserModel
from src.app.auth.send_email import send_update_account_email


class UserService:
    """Клас для роботи з профілем користувача під час реєстрації, аутентифікації та відновлення пароля"""

    @classmethod
    async def created_user(
        cls,
        data: NewUserBase,
        session: AsyncSession,
    ) -> UserBase:

        user_dict: dict = data.model_dump()
        user_dict["password"] = get_password_hash(user_dict["password"])
        user = UserModel(**user_dict)
        session.add(user)
        await session.flush()
        await session.commit()
        return UserBase(**user.__dict__)

    @classmethod
    async def update_user(
        cls,
        user: UserBase,
        data: UpdateUserBase,
        session: AsyncSession,
        task: BackgroundTasks,
    ) -> UserBase:
        """Оновлюємо деякі поля моделі користувача
        Якщо користувач змінює електронну пошту, то ми повинні змінити статус верифікації електронної адреси та змісити
        користувача пройти підтвердження електронної пошти ще раз"""
        from src.app.auth.service import create_verification

        if user.email == data.email:
            stmt = (
                update(UserModel)
                .values(
                    firstname=data.firstname,
                    lastname=data.lastname,
                    phone_number=data.phone_number,
                    email=data.email,
                )
                .where(UserModel.id == user.id)
                .returning(UserModel)
            )
            result = await session.execute(stmt)
            await session.commit()
            user = result.scalars().one()
        else:
            stmt = (
                update(UserModel)
                .values(
                    firstname=data.firstname,
                    lastname=data.lastname,
                    phone_number=data.phone_number,
                    email=data.email,
                    valid_email=False,
                )
                .where(UserModel.id == user.id)
                .returning(UserModel)
            )
            result = await session.execute(stmt)
            await session.commit()
            user = result.scalars().one()
            verify_id = await create_verification(
                data=VerificationBase(user_id=user.id), session=session
            )
            context: dict[str, str | EmailStr] = {
                "phone_number": user.phone_number,
                "email": user.email,
                "firstname": user.firstname,
                "lastname": user.lastname,
                "link": f"{SERVER_HOST}/api/v1/confirm-email?link={verify_id}",
            }
            task.add_task(send_update_account_email, context)
        return UserBase.model_validate(user.__dict__)

    @classmethod
    async def delete_user(cls, user: UserBase, session: AsyncSession) -> UserBase:
        """Видаляємо користувача, повертаємо значення видаленого профілю"""

        stmt = delete(UserModel).where(UserModel.id == user.id).returning(UserModel)
        result = await session.execute(stmt)
        await session.commit()
        user = result.scalars().one()
        return UserBase.model_validate(user.__dict__)

    @classmethod
    async def authenticate(
        cls, phone_number: str, password: str, session: AsyncSession
    ) -> Optional[UserModel]:
        """Аутенифікація та перевірка пароля користувача"""
        query = select(UserModel).where(UserModel.phone_number == phone_number)
        result = await session.execute(query)
        user = result.scalars().one_or_none()
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    @classmethod
    async def check_valid_email(cls, user_id: UUID, session: AsyncSession):
        """Змінюємо статус валідності електронної адреси моделі користувача"""
        query = select(UserModel).where(UserModel.id == user_id)
        result = await session.execute(query)
        user = result.scalars().one_or_none()
        if user:
            user.valid_email = True
            await session.commit()
        else:
            raise HTTPException(status_code=400, detail="User not exists")

    @classmethod
    async def get_user(cls, user_id: UUID, session: AsyncSession) -> UserBase | None:
        """Отримуємо користувача"""
        query = select(UserModel).where(UserModel.id == user_id)
        result = await session.execute(query)
        user = result.scalars().one_or_none()
        if user is not None:
            user = UserBase.model_validate(user.__dict__)
        return user

    @classmethod
    async def check_exist_user(cls, user_id: UUID, session: AsyncSession) -> bool:
        """Перевіряє чи користувач із даним id існує"""
        query = select(UserModel).where(UserModel.id == user_id)
        result = await session.execute(query)
        user = result.scalars().one_or_none()
        if user is not None:
            return True
        else:
            return False

    @classmethod
    async def get_user_by_email(
        cls, email: str, session: AsyncSession
    ) -> UserBase | None:
        """Отримуємо користувача"""
        query = select(UserModel).where(UserModel.email == email)
        result = await session.execute(query)
        user = result.scalars().one_or_none()
        if user is not None:
            user = UserBase.model_validate(user.__dict__)
        return user

    @classmethod
    async def recovery_password(
        cls, user_id: UUID, password: str, session: AsyncSession
    ) -> bool:
        """Отримуємо користувача та змінюємо пароль. Повертаємо True якщо пароль змінено і False якщо
        користувача не існує"""
        query = select(UserModel).where(UserModel.id == user_id)
        result = await session.execute(query)
        user = result.scalars().one_or_none()
        if user is not None:
            user.password = get_password_hash(password)
            await session.commit()
            return True
        return False
