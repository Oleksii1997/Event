from fastapi import APIRouter
from src.app.users.endpoint import api

users_router = APIRouter()

#users_router.include_router(user.user_router, prefix="/user", tags=["user"])
