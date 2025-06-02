from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from src.app.users.service.jwt_user_service import (
    get_current_active_auth_user_from_access,
)

from src.app.users.schemas import UserBase
from src.app.auth.schemas import MsgBase
from src.config.db_settings import get_session
from src.app.profile.schemas import (
    ProfileBase,
    ProfileReplayBase,
    ProfileReplayFullBase,
)
from src.app.profile.servise.profile_service import ProfileService


http_bearer = HTTPBearer(auto_error=False)

profile_router = APIRouter(
    prefix="/profile",
    tags=["profile"],
    dependencies=[Depends(http_bearer)],
)


@profile_router.post("/create", response_model=ProfileReplayBase)
async def create_profile(
    data: ProfileBase,
    user: UserBase = Depends(get_current_active_auth_user_from_access),
    session: AsyncSession = Depends(get_session),
) -> ProfileReplayBase | HTTPException:
    """Створюємо профіль користувача"""
    profile = await ProfileService.get_profile_by_user(session=session, user=user)
    if profile is not None:
        raise HTTPException(status_code=400, detail="Profile already exist")
    else:
        return await ProfileService.create_profile(
            session=session, user=user, data=data
        )


@profile_router.delete("/delete")
async def delete_profile(
    user: UserBase = Depends(get_current_active_auth_user_from_access),
    session: AsyncSession = Depends(get_session),
) -> MsgBase:
    result = await ProfileService.delete_profile(session=session, user=user)
    if result is None:
        raise HTTPException(status_code=400, detail="Profile does not exist")
    else:
        return result


@profile_router.patch("/update", response_model=ProfileReplayBase)
async def update_profile(
    data: ProfileBase,
    user: UserBase = Depends(get_current_active_auth_user_from_access),
    session: AsyncSession = Depends(get_session),
) -> ProfileReplayBase | HTTPException:
    """Оновлюємо дані профілю користувача"""
    return await ProfileService.update_profile(data=data, session=session, user=user)


@profile_router.get("/get_detail/{user_id}", response_model=ProfileReplayFullBase)
async def get_detail_profile(
    user_id: UUID, session: AsyncSession = Depends(get_session)
) -> ProfileReplayFullBase | HTTPException:
    """Отримуємо профіль по ID користувача"""
    result = await ProfileService.get_profile_by_user_id(
        user_id=user_id, session=session
    )
    if result is None:
        raise HTTPException(status_code=400, detail="Profile does not exist")
    else:
        return result
