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
    ProfileSocialLinkCreateBase,
    ProfileSocialLincCreateReturnBase,
)
from src.app.profile.servise.profile_service import ProfileService
from src.app.profile.servise.social_link_service import SocialLinkService


http_bearer = HTTPBearer(auto_error=False)

profile_router = APIRouter(
    prefix="/profile",
    tags=["profile"],
    dependencies=[Depends(http_bearer)],
)


@profile_router.post("/create", response_model=ProfileReplayFullBase)
async def create_profile(
    data: ProfileBase,
    user: UserBase = Depends(get_current_active_auth_user_from_access),
    session: AsyncSession = Depends(get_session),
) -> ProfileReplayFullBase | HTTPException:
    """Створюємо профіль користувача"""
    profile = await ProfileService.get_profile_by_user(session=session, user=user)
    if profile is not None:
        raise HTTPException(status_code=400, detail="Profile already exist")
    else:
        new_short_profile = await ProfileService.create_profile(
            session=session, user=user, data=data
        )
        return await ProfileService.get_profile_by_user_id(
            user_id=new_short_profile.profile_user.id, session=session
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


@profile_router.patch("/update", response_model=ProfileReplayFullBase)
async def update_profile(
    data: ProfileBase,
    user: UserBase = Depends(get_current_active_auth_user_from_access),
    session: AsyncSession = Depends(get_session),
) -> ProfileReplayFullBase | HTTPException:
    """Оновлюємо дані профілю користувача"""
    profile = await ProfileService.update_profile(data=data, session=session, user=user)
    return await ProfileService.get_profile_by_user_id(
        user_id=profile.profile_user.id, session=session
    )


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


@profile_router.post(
    "/social_link/add", response_model=ProfileSocialLincCreateReturnBase
)
async def create_social_link(
    data: list[ProfileSocialLinkCreateBase],
    user: UserBase = Depends(get_current_active_auth_user_from_access),
    session: AsyncSession = Depends(get_session),
) -> ProfileSocialLincCreateReturnBase:
    new_link = await SocialLinkService.create_social_link(data, user, session)
    if new_link is None:
        raise HTTPException(
            status_code=400,
            detail="Profile does not exist. Creat your profile and edit",
        )
    else:
        return new_link
