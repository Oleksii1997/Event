from fastapi import HTTPException
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from src.app.friendship.schemas import (
    CreateFriendshipRequestBase,
    FriendshipRequestBase,
    CreateFriendshipBase,
    FriendshipBase,
)
from src.app.friendship.models import FriendshipRequestModel, FriendshipModel


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
