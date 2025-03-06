import uuid
from typing import Annotated
from fastapi import APIRouter
from fastapi.params import Depends

from src.app.users.schemas import UserBase

from src.app.users.service import get_current_active_auth_user
from src.app.users.service import UserService

from src.app.auth.jwt_auth_service import get_payload_access_token

user_router = APIRouter()


@user_router.get("/me", response_model=UserBase)
async def auth_user(
    payload: dict = Depends(get_payload_access_token),
    user: UserBase = Depends(get_current_active_auth_user),
) -> UserBase:
    """Віддаємо інформацію про авторизованого користувача"""
    return user
