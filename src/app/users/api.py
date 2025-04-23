from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import HTTPBearer

from src.app.auth.schemas import MsgBase
from src.app.users.service.jwt_user_service import (
    get_current_active_auth_user_from_access,
)
from src.app.auth.jwt_auth_service import get_payload_access_token
from src.app.users.service.user_service import UserService

from src.app.users.schemas import UserBase, UpdateUserBase

http_bearer = HTTPBearer(auto_error=False)

user_router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[Depends(http_bearer)],
)


@user_router.get("/me", response_model=UserBase)
async def auth_user(
    user: UserBase = Depends(get_current_active_auth_user_from_access),
) -> UserBase:
    """Віддаємо інформацію про авторизованого користувача"""
    return user


@user_router.patch("/me/update", response_model=UserBase)
async def user_update(
    new_user_data: UpdateUserBase,
    user: UserBase = Depends(get_current_active_auth_user_from_access),
) -> UserBase:
    """Оновлення даних про користувача"""
    new_user = await UserService.update_user(user=user, data=new_user_data)
    return new_user


@user_router.delete("/me/delete", response_model=UserBase)
async def user_delete(
    user: UserBase = Depends(get_current_active_auth_user_from_access),
) -> UserBase:
    """Видаляємо користувача та повертаємо значення видаленої моделі"""
    user = await UserService.delete_user(user=user)
    return user
