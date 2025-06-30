import datetime
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from src.app.auth.schemas import MsgBase
from src.app.profile.models import AvatarModel
from src.app.profile.schemas import AvatarBase, CreateAvatarBase


class AvatarService:
    """Класс для роботи з аватарками"""

    @classmethod
    async def get_all_avatar(
        cls, profile_id: UUID, session: AsyncSession
    ) -> List[Optional[AvatarBase]]:
        """Отримуємо всі зображення аватарок користувача"""
        query = (
            select(AvatarModel)
            .where(AvatarModel.profile_id == profile_id)
            .order_by(AvatarModel.created_at)
        )
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
        cls, data: CreateAvatarBase, session: AsyncSession
    ) -> AvatarBase:
        """Записуємо посилання на збережений аватар в базу даних"""
        new_avatar = AvatarModel(**data.model_dump())
        session.add(new_avatar)
        await session.commit()
        print(f"New AVATAR{new_avatar}")
        return AvatarBase(**new_avatar.__dict__)

    @classmethod
    async def delete_avatar(
        cls, avatar_id: UUID, session: AsyncSession
    ) -> AvatarBase | None:
        """Видаляємо відповідний запис про аватар з бази даних"""
        query = select(AvatarModel).where(AvatarModel.id == avatar_id)
        result = await session.execute(query)
        image = result.scalars().one_or_none()
        if image is not None:
            avatar = AvatarBase.model_validate(image, from_attributes=True)
            await session.delete(image)
            await session.commit()
            return avatar
        return None
