from fastapi import HTTPException
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc
from src.app.friendship.schemas import (
    CreateFriendshipRequestBase,
    FriendshipRequestBase,
    CreateFriendshipBase,
    FriendshipBase,
)
from src.app.friendship.models import FriendshipRequestModel, FriendshipModel
from src.app.friendship.schemas import (
    MySubscribers,
    ISubscribe,
    FriendshipAvatarBase,
    FriendshipVideoBase,
)
from src.app.profile.models import AvatarModel, VideoProfileModel
from src.app.users.models import UserModel, ProfileModel


class FriendRequestService:
    """Класс роботи з моделлю заявок моделі запиту підписки на дружбу"""

    @classmethod
    async def create_friend_request(
        cls, data: CreateFriendshipRequestBase, session: AsyncSession
    ) -> FriendshipRequestBase | None:
        """Робимо запис в базу даних про створення заявки на дружбу"""
        new_request = FriendshipRequestModel(**data.model_dump())
        session.add(new_request)
        try:
            await session.commit()
            return FriendshipRequestBase(**new_request.__dict__)
        except IntegrityError:
            await session.rollback()
            return None

    @classmethod
    async def check_exist_subscribe_request(
        cls, data: CreateFriendshipRequestBase, session: AsyncSession
    ) -> bool:
        """Перевіряємо чи існує заявка на дружбу. Якщо запис вже існує, повертаємо True, якщо не існує - повертаємо False"""
        query = select(FriendshipRequestModel).where(
            and_(
                FriendshipRequestModel.sender_id == data.sender_id,
                FriendshipRequestModel.receiver_id == data.receiver_id,
            )
        )
        result = await session.execute(query)
        item = result.scalars().one_or_none()
        if item is not None:
            return True
        else:
            return False

    @classmethod
    async def check_and_delete_subscribe_request(
        cls, data: CreateFriendshipRequestBase, session: AsyncSession
    ) -> CreateFriendshipRequestBase | HTTPException:
        """Перевіряємо чи існує заявка на дружбу. Видаляємо заявку на дружбу"""
        query = select(FriendshipRequestModel).where(
            and_(
                FriendshipRequestModel.sender_id == data.sender_id,
                FriendshipRequestModel.receiver_id == data.receiver_id,
            )
        )
        result = await session.execute(query)
        item = result.scalars().one_or_none()
        if item is not None:
            await session.delete(item)
            await session.commit()
            return data
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Заявка на дружбу користувача uuid = {data.sender_id} до користувача uuid = {data.receiver_id} не існує.",
            )

    @classmethod
    async def subscribe_user(
        cls, data: CreateFriendshipBase, session: AsyncSession
    ) -> FriendshipBase | None:
        """Створюємо підписку на користувача, запис в таблицю дружби"""
        new_friend = FriendshipModel(**data.model_dump())
        session.add(new_friend)
        try:
            await session.commit()
            return FriendshipBase(**new_friend.__dict__)
        except IntegrityError:
            await session.rollback()
            return None


class FriendInfoService:
    """Клас для отримання інформації про підписки та підписників"""

    @classmethod
    async def get_my_subscribers(
        cls, user_id: UUID, session: AsyncSession
    ) -> list[MySubscribers]:
        """Отримуємо своїх підписників (ті хто підписний на мене)"""
        query = (
            select(
                UserModel.id,
                UserModel.firstname,
                UserModel.lastname,
                AvatarModel,
                VideoProfileModel,
            )
            .join(FriendshipModel, FriendshipModel.friend_id == UserModel.id)
            .outerjoin(ProfileModel, ProfileModel.user_id == UserModel.id)
            .outerjoin(AvatarModel, AvatarModel.profile_id == ProfileModel.id)
            .outerjoin(
                VideoProfileModel, VideoProfileModel.profile_id == ProfileModel.id
            )
            .where(FriendshipModel.user_id == user_id)
            .order_by(desc(AvatarModel.created_at))
        )
        result = await session.execute(query)
        data = result.all()

        subscribers_dict = {}
        for user_id, first_name, last_name, avatar, video in data:
            if user_id not in subscribers_dict:
                subscribers_dict[user_id] = MySubscribers(
                    user_id=user_id,
                    first_name=first_name,
                    last_name=last_name,
                    avatar=[],
                    video=[],
                )
            if avatar:
                new_avatar = FriendshipAvatarBase(avatar_url=avatar.avatar_url)
                if new_avatar not in subscribers_dict[user_id].avatar:
                    subscribers_dict[user_id].avatar.append(new_avatar)
            if video:
                new_video = FriendshipVideoBase(video_url=video.video_url)
                if new_video not in subscribers_dict[user_id].video:
                    subscribers_dict[user_id].video.append(new_video)

        subscribers = list(subscribers_dict.values())
        return subscribers
