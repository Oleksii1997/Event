from fastapi import HTTPException
from typing import Annotated
from fastapi import BackgroundTasks
from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.app.users.schemas import UserCreateBase, NewUserBase
from src.app.users.service import UserService
from src.app.auth.schemas import MsgBase, AuthToken
from src.app.auth.service import registration_user
from src.app.auth.schemas import VerificationEmailBase
from src.app.auth.service import verify_user_email
from src.app.auth.jwt import create_jwt_token

auth_router = APIRouter()

@auth_router.post("/registration", response_model=MsgBase)
async def user_registration(user: UserCreateBase, task: BackgroundTasks):
    """Реєстрація нового користувача.

    P.S. e-mail та номер телефону є унікальними значеннями, тому користувачі з однаковими номерами телефону або адресами
    електронної пошти не можуть зареєструватися"""
    #user_dict: dict = user.model_dump()
    result = await registration_user(NewUserBase(**user.model_dump()), task)
    if result:
        raise HTTPException(status_code=400, detail="User already exists")
    else:
        return {"msg": "User has been created"}

@auth_router.get("/confirm-email", response_model=MsgBase)
async def confirm_email(data: Annotated[VerificationEmailBase, Depends()]):
    """Верифікація електронної пошти користувача. Для верифікації надішліть uuid запису про верифікацію"""
    if await verify_user_email(data):
        return {"msg": "Success verify email"}
    else:
        raise HTTPException(status_code=404, detail="E-mail verification link not found")


@auth_router.post("/login/access-token", response_model=AuthToken)
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Логінимося та отримуємо токен.
    В формі OAuth2PasswordRequestForm обов'язковими полями входу є username та password. В даному проекті замість
    username ми будемо використовувати номер телефону, поле phone_number!"""
    user = await UserService.authenticate(phone_number=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect phone number or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    token = await create_jwt_token(payload = {"user_id": f"{user.id}"})
    return AuthToken(access_token=token, token_type="Bearer")
