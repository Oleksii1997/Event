from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import HTTPBearer

from src.app.users.service.jwt_user_service import (
    get_current_active_auth_user_from_access,
)
from src.app.auth.jwt_auth_service import get_payload_access_token

from src.app.users.schemas import UserBase


http_bearer = HTTPBearer(auto_error=False)

user_router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[Depends(http_bearer)],
)


@user_router.get("/me", response_model=UserBase)
async def auth_user(
    payload: dict = Depends(get_payload_access_token),
    user: UserBase = Depends(get_current_active_auth_user_from_access),
) -> UserBase:
    """Віддаємо інформацію про авторизованого користувача"""
    return user
