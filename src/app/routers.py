from fastapi import APIRouter

from src.app.users.api import user_router
from src.app.auth.api import auth_router

api_router = APIRouter()

api_router.include_router(user_router, tags=["user"])
api_router.include_router(auth_router, tags=["auth"])
