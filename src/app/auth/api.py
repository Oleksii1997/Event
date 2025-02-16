from fastapi import HTTPException
from typing import Annotated
from fastapi import BackgroundTasks
from fastapi import APIRouter
from fastapi.params import Depends
from src.app.users.schemas import UserCreateBase
from src.app.auth.schemas import MsgBase
from src.app.auth.service import registration_user
from src.app.auth.schemas import VerificationEmailBase
from src.app.auth.service import verify_user_email
auth_router = APIRouter()

@auth_router.post("/registration", response_model=MsgBase)
async def user_registration(user: Annotated[UserCreateBase, Depends()], task: BackgroundTasks):
    """Реєстрація нового користувача.

    P.S. e-mail та номер телефону є унікальними значеннями, тому користувачі з однаковими номерами телефону або адресами
    електронної пошти не можуть зареєструватися"""
    result = await registration_user(user, task)
    if result:
        raise HTTPException(status_code=400, detail="User already exists")
    else:
        return {"msg": "Email send"}

@auth_router.get("/confirm-email", response_model=MsgBase)
async def confirm_email(data: Annotated[VerificationEmailBase, Depends()]):
    """Верифікація електронної пошти користувача. Для верифікації надішліть uuid запису про верифікацію"""
    if await verify_user_email(data):
        return {"msg": "Success verify email"}
    else:
        raise HTTPException(status_code=404, detail="E-mail verification link not found")
