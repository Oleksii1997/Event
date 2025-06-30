from fastapi import APIRouter

from src.app.users.api import user_router
from src.app.auth.api import auth_router
from src.app.location.api import location_router

from src.app.profile.api import (
    profile_router,
    social_link_router,
    avatar_router,
    video_router,
)

api_router = APIRouter()

api_router.include_router(user_router, tags=["user"])
api_router.include_router(auth_router, tags=["auth"])
api_router.include_router(location_router, tags=["location"])
api_router.include_router(profile_router, tags=["profile"])
api_router.include_router(social_link_router, tags=["social_link"])
api_router.include_router(avatar_router, tags=["user_avatar"])
api_router.include_router(video_router, tags=["video_profile"])
