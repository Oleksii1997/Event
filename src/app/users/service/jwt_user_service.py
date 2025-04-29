from fastapi import HTTPException, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID


from src.app.auth.jwt_auth_service import (
    get_payload_access_token,
    get_payload_refresh_token,
)
from src.app.users.service.user_service import UserService
from src.app.users.schemas import UserBase
from src.config.db_settings import new_session, get_session


async def _get_current_auth_user(payload: dict, session: AsyncSession) -> UserBase:
    """Отримуємо користувача з токена (в токені передається user_id)"""

    user_id: UUID | None = payload.get("user_id")

    if user_id is not None:
        user = await UserService.get_user(user_id=user_id, session=session)
        if user is not None:
            return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalid (user not found)",
    )


async def _get_current_active_auth_user(user: UserBase) -> UserBase:
    """Перевіряємо чи користувач активний"""
    if user.is_active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User inactive",
    )


async def get_current_auth_user_from_access(
    payload: dict = Depends(get_payload_access_token),
    session: AsyncSession = Depends(get_session),
) -> UserBase:
    """Перевіряємо чи користувач з access токена існує"""
    return await _get_current_auth_user(payload=payload, session=session)


async def get_current_active_auth_user_from_access(
    user: UserBase = Depends(get_current_auth_user_from_access),
) -> UserBase:
    """Перевіряємо чи користувач активний"""
    return await _get_current_active_auth_user(user)


async def get_current_auth_user_from_refresh(
    payload: dict = Depends(get_payload_refresh_token),
    session: AsyncSession = Depends(get_session),
) -> UserBase:
    """Перевіряємо чи користувач з refresh токена існує"""
    return await _get_current_auth_user(payload=payload, session=session)


async def get_current_active_auth_user_from_refresh(
    user: UserBase = Depends(get_current_auth_user_from_refresh),
) -> UserBase:
    """Перевіряємо чи користувач активний"""
    return await _get_current_active_auth_user(user)
