from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from src.app.auth.schemas import MsgBase
from src.app.users.schemas import UserBase
from src.app.users.service.user_service import UserService
from src.app.auth.schemas import MsgBase
from src.app.users.service.jwt_user_service import (
    get_current_active_auth_user_from_access,
)
from src.config.db_settings import get_session
from src.app.friendship.service import FriendRequestService
from src.app.friendship.schemas import (
    CreateFriendshipRequestBase,
    FriendshipRequestBase,
    FriendshipBase,
    CreateFriendshipBase,
)

http_bearer = HTTPBearer(auto_error=False)
friend_router = APIRouter(
    prefix="/friend", tags=["friend"], dependencies=[Depends(http_bearer)]
)


@friend_router.post("/subscribe", response_model=FriendshipRequestBase)
async def invite_friend(
    receiver_id: UUID,
    user: UserBase = Depends(get_current_active_auth_user_from_access),
    session: AsyncSession = Depends(get_session),
) -> FriendshipRequestBase | HTTPException:
    """Надсилаємо запит на дружбу"""
    exist_user = await UserService.check_exist_user(
        user_id=receiver_id, session=session
    )
    if not exist_user:
        raise HTTPException(
            status_code=400,
            detail="Користувач на якого ви хочете підписатися не існує. Невірний uuid користувача.",
        )
    if receiver_id == user.id:
        raise HTTPException(
            status_code=400,
            detail="Ви не можете підписатися самі на себе, sender_id повинно відрізнятися від reciever_id.",
        )
    data = CreateFriendshipRequestBase(sender_id=user.id, receiver_id=receiver_id)
    result = await FriendRequestService.create_friend_request(data, session)
    if result is None:
        raise HTTPException(
            status_code=400,
            detail=f"Ви вже відправляли заявку на дружбу. Заявка на дружбу користувача "
            f"uuid = {data.sender_id} до користувача uuid = {data.receiver_id} вже існує.",
        )
    return result


@friend_router.post("/accept", response_model=FriendshipBase)
async def accept_friend(
    sender_id: UUID,
    user: UserBase = Depends(get_current_active_auth_user_from_access),
    session: AsyncSession = Depends(get_session),
) -> FriendshipBase | HTTPException:
    """Приймаємо запит на дружбу"""
    exist_user = await UserService.check_exist_user(user_id=sender_id, session=session)
    if not exist_user:
        raise HTTPException(
            status_code=400,
            detail="Користувач заявку якого ви хочете прийняти не існує. Невірний uuid користувача.",
        )
    if sender_id == user.id:
        raise HTTPException(
            status_code=400,
            detail="Ви не можете підписатися самі на себе, sender_id повинно відрізнятися від reciever_id.",
        )
    data = CreateFriendshipRequestBase(sender_id=sender_id, receiver_id=user.id)
    check_data = await FriendRequestService.check_and_delete_subscribe_request(
        data, session
    )
    subscribe_data = CreateFriendshipBase(
        user_id=check_data.receiver_id, friend_id=check_data.sender_id
    )
    result = await FriendRequestService.subscribe_user(
        data=subscribe_data, session=session
    )
    if result is None:
        raise HTTPException(
            status_code=400,
            detail=f"Користувача "
            f"uuid = {data.user_id} вже підписаний на користувача uuid = {data.friend_id}.",
        )
    return result
