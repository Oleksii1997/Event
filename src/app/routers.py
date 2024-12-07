from fastapi import APIRouter
from src.app.users.routers import users_router
from src.app.auth.api import auth_router

api_router = APIRouter()

#api_router.include_router(users_router, tags=["user"])
api_router.include_router(auth_router, tags=["auth"])
