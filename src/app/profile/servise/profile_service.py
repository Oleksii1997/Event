from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from uuid import UUID

from sqlalchemy.orm import joinedload

from src.app.profile.schemas import (
    ProfileBase,
    ProfileReplayBase,
    ProfileReplayFullBase,
)
from src.app.profile.models import ProfileModel
from src.app.users.schemas import UserBase
from src.app.auth.schemas import MsgBase


class ProfileService:
    """Класс для роботи з профелем користувача"""

    @classmethod
    async def create_profile(
        cls, data: ProfileBase, user: UserBase, session: AsyncSession
    ) -> ProfileReplayBase:
        """Створюємо новий профіль користувача"""
        profile_dict: dict = data.model_dump()
        profile_dict["user_id"] = user.id
        new_profile = ProfileModel(**profile_dict)
        session.add(new_profile)
        await session.commit()
        return ProfileReplayBase(**new_profile.__dict__, profile_user=user)

    @classmethod
    async def get_profile_by_user(
        cls, user: UserBase, session: AsyncSession
    ) -> ProfileReplayBase | None:
        """Перевіряємо чи профіль користувача існує, та повертаємо значення профілю"""
        query = select(ProfileModel).where(ProfileModel.user_id == user.id)
        result = await session.execute(query)
        new_profile = result.scalars().one_or_none()
        if new_profile is not None:
            new_profile = ProfileReplayBase(**new_profile.__dict__, profile_user=user)
        return new_profile

    @classmethod
    async def get_profile_by_user_id(
        cls, user_id: UUID, session: AsyncSession
    ) -> ProfileReplayFullBase | None:
        """Отримуємо профіль по id користувача"""
        query = (
            select(ProfileModel)
            .where(ProfileModel.user_id == user_id)
            .options(joinedload(ProfileModel.profile_user))
            .options(joinedload(ProfileModel.profile_area))
            .options(joinedload(ProfileModel.profile_region))
            .options(joinedload(ProfileModel.profile_community))
            .options(joinedload(ProfileModel.profile_city))
        )
        result = await session.execute(query)
        profile = result.scalars().one_or_none()
        if profile is not None:
            return ProfileReplayFullBase.model_validate(profile, from_attributes=True)
        else:
            return None

    @classmethod
    async def delete_profile(
        cls, user: UserBase, session: AsyncSession
    ) -> MsgBase | None:
        """Видаляємо профіль користувача і повертаємо повідомлення про видалення профілю. Якщо профіль не існує, то
        повертаємо None"""
        query = select(ProfileModel).where(ProfileModel.user_id == user.id)
        result = await session.execute(query)
        new_profile = result.scalars().one_or_none()
        if new_profile is not None:
            await session.delete(new_profile)
            await session.commit()
            return MsgBase(msg="User profile success deleted")
        else:
            return None

    @classmethod
    async def update_profile(
        cls, data: ProfileBase, user: UserBase, session: AsyncSession
    ) -> ProfileReplayBase:
        """Оновлюємо інформацію профілю користувача"""
        query = (
            update(ProfileModel)
            .values(
                birthday=data.birthday,
                description=data.description,
                area=data.area,
                region=data.region,
                community=data.community,
                city=data.city,
            )
            .where(ProfileModel.user_id == user.id)
            .returning(ProfileModel)
        )
        result = await session.execute(query)
        await session.commit()
        profile = result.scalars().one()
        return ProfileReplayBase(**profile.__dict__, profile_user=user)
