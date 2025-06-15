from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from src.app.profile.schemas import (
    ProfileSocialLinkCreateBase,
    ProfileUUIDBase,
)
from src.app.auth.schemas import MsgBase
from src.app.users.schemas import UserBase
from src.app.profile.schemas import ProfileSocialLinkBase
from src.app.profile.models import SocialLinkModel
from src.app.profile.servise.profile_service import ProfileService
from uuid import UUID


class SocialLinkService:
    """Клас для роботи з посиланнями на соціальні мережі"""

    @classmethod
    async def get_all_social_link(
        cls,
        user: UserBase,
        session: AsyncSession,
    ) -> list[ProfileSocialLinkBase] | None:
        """Повертаємо всі соціальні мережі користувача"""
        profile_id = await ProfileService.get_profile_id_by_user(user, session)
        if profile_id is not None:
            query = select(SocialLinkModel).where(
                SocialLinkModel.profile_id == profile_id.id
            )
            result = await session.execute(query)
            links = result.scalars().all()
            return [
                ProfileSocialLinkBase.model_validate(item, from_attributes=True)
                for item in links
            ]
        else:
            return None

    @classmethod
    async def delete_social_link(
        cls,
        link_id: UUID,
        session: AsyncSession,
    ) -> ProfileSocialLinkBase | None:
        """Видаляємо посилання на соцмережу в профілі користувача"""
        query = (
            delete(SocialLinkModel)
            .where(SocialLinkModel.id == link_id)
            .returning(SocialLinkModel)
        )
        result = await session.execute(query)
        await session.commit()
        link = result.scalars().one_or_none()
        if link is None:
            return None
        return ProfileSocialLinkBase.model_validate(link, from_attributes=True)

    @classmethod
    async def create_social_link(
        cls,
        data: ProfileSocialLinkCreateBase,
        user: UserBase,
        session: AsyncSession,
    ) -> MsgBase | None:
        """
        Перевіряємо чи існує профіль користувача. Якщо профіль не існує - повертаємо None.
        Отримуємо соціальну мережу яку хоче додати користувач, перевіряємо чи такі посилання вже існують у користувача.
        Якщо такі посилання відсутні, то створюємо їх. Якщо посилання вже існують, виводимо повідомлення, що воно вже існує.
        Встановлюємо максимальну кількість можливих створених соцмереж - 20 соцмереж для одного користувача.
        Якщо кількість створених посилань перевищує максимально допустиму, то виводимо повідомлення яке про це повідомляє.
        У всіх випадках окрім відсутності профілю статус код відповіді - 200; У випадку якщо профіль не існує - 400
        Спочатку була думка зробити поле посилань на соціальні мережі унікальним, але від цього відмовились так, як
        у деяких людей соціальні мережі можуть бути спільними, також може бути соцмережі компаній.
        """
        profile_id = await ProfileService.get_profile_id_by_user(user, session)
        if profile_id is not None:
            exist_social_link = await cls.get_exist_link(
                profile=profile_id, session=session
            )
            new_link: dict = data.model_dump()
            if len(exist_social_link) >= 20:
                return MsgBase(
                    msg="You have reached the maximum number of added social media links, the maximum possible number of links is 20."
                )
            elif new_link["link"] not in exist_social_link:
                new_link["profile_id"] = profile_id.id
                session.add(SocialLinkModel(**new_link))
                await session.commit()
                return MsgBase(msg="Social media links added")
            else:
                return MsgBase(msg="Social media link already exist")
        else:
            return None

    @classmethod
    async def get_exist_link(
        cls,
        profile: ProfileUUIDBase,
        session: AsyncSession,
    ) -> list[str]:
        """Повертаємо список посилань які вже існують в базі даних"""
        query = select(SocialLinkModel).where(SocialLinkModel.profile_id == profile.id)
        result = await session.execute(query)
        links = result.scalars().all()
        return [item.link for item in links]
