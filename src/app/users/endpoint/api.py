import uuid
from typing import Annotated
from fastapi import APIRouter
from fastapi.params import Depends

from src.app.users.schemas import UserCreateBase, UserAuthBase
from src.app.users.service import UserCRUD
user_router = APIRouter()

"""
@user_router.get("/auth_user")
async def auth_user(user: Annotated[UserAuthBase, Depends()]):
    result = await UserCRUD.authenticate(user)
"""