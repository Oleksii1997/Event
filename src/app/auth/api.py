from fastapi import HTTPException
from typing import Annotated
from fastapi import BackgroundTasks
from fastapi import APIRouter
from fastapi.params import Depends
from src.app.users.schemas import UserCreateBase
from src.app.auth.schemas import MsgBase

from src.app.auth.service import registration_user
auth_router = APIRouter()

@auth_router.post("/registration", response_model=MsgBase)
async def user_registration(user: Annotated[UserCreateBase, Depends()], task: BackgroundTasks):
    """Реєстрація нового користувача.

    P.S. Емейл та номер телефону є унікальними значеннями, тому користувачі з однаковими номерами телефону або адресами
    електронної пошти не можуть зареєструватися"""
    result = await registration_user(user, task)
    if result:
        raise HTTPException(status_code=400, detail="User already exists")
    else:
        return {"msg": "Email send"}