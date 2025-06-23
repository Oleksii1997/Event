import datetime
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from src.app.profile.models import AvatarModel
from src.app.profile.schemas import AvatarBase, CreateAvatar


class AvatarService:
    """Класс для роботи з аватарками"""

    @classmethod
    async def get_all_avatar(
        cls, profile_id: UUID, session: AsyncSession
    ) -> List[Optional[AvatarBase]]:
        """Отримуємо всі зображення аватарок користувача"""
        query = select(AvatarModel).where(AvatarModel.profile_id == profile_id)
        result = await session.execute(query)
        avatars = result.scalars().all()
        if avatars:
            return [
                AvatarBase.model_validate(avatar, from_attributes=True)
                for avatar in avatars
            ]
        else:
            return list()

    @classmethod
    async def create_avatar(
        cls, data: CreateAvatar, session: AsyncSession
    ) -> AvatarBase:
        """Записуємо посилання на збережений аватар в базу даних"""
        new_avatar = AvatarModel(**data.model_dump())
        session.add(new_avatar)
        await session.commit()
        print(f"New AVATAR{new_avatar}")
        return AvatarBase(**new_avatar.__dict__)
