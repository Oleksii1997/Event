from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.app.profile.schemas import (
    ProfileSocialLinkCreateBase,
    ProfileSocialLincCreateReturnBase,
)
from src.app.users.schemas import UserBase
from src.app.profile.models import ProfileModel, SocialLinkModel
from src.app.profile.servise.profile_service import ProfileService
from uuid import UUID


class SocialLinkService:
    """Клас для роботи з посиланнями на соціальні мережі"""

    @classmethod
    async def create_social_link(
        cls,
        data: list[ProfileSocialLinkCreateBase],
        user: UserBase,
        session: AsyncSession,
    ) -> ProfileSocialLincCreateReturnBase | None:
        """Записуємо нові посилання на соціальні мережі"""
        profile = await ProfileService.get_profile_by_user(user, session)
        if profile is not None:
            for item in data:
                new_link: dict = item.model_dump()
                new_link["profile_id"] = profile.id
                session.add(SocialLinkModel(**new_link))
                await session.commit()
            return ProfileSocialLincCreateReturnBase(
                profile_id=profile.id, social_link=data
            )
        else:
            return None
