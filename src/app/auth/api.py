from fastapi import BackgroundTasks, HTTPException, APIRouter, status
from fastapi.params import Depends
from fastapi.security import HTTPBearer, OAuth2PasswordRequestForm
from typing import Annotated


from src.config.settings import settings_class
from src.app.auth.jwt import create_jwt_token
from src.app.auth.security import get_payload_reset_password_token
from src.app.auth.jwt_auth_service import (
    get_payload_refresh_token,
    get_payload_access_token,
)
from src.app.auth.service import (
    registration_user,
    recovery_password_mail,
    verify_user_email,
)
from src.app.users.service.jwt_user_service import (
    get_current_active_auth_user_from_refresh,
)
from src.app.users.service.user_service import UserService

from src.app.users.schemas import (
    UserCreateBase,
    NewUserBase,
    UserBase,
    RecoveryPasswordBase,
)
from src.app.auth.schemas import MsgBase, AuthToken, VerificationEmailBase


http_bearer = HTTPBearer(auto_error=False)
auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    dependencies=[Depends(http_bearer)],
)


@auth_router.post("/registration", response_model=MsgBase)
async def user_registration(user: UserCreateBase, task: BackgroundTasks):
    """Реєстрація нового користувача.

    P.S. e-mail та номер телефону є унікальними значеннями, тому користувачі з однаковими номерами телефону або адресами
    електронної пошти не можуть зареєструватися"""
    # user_dict: dict = user.model_dump()
    result = await registration_user(NewUserBase(**user.model_dump()), task)
    if result:
        raise HTTPException(status_code=400, detail="User already exists")
    else:
        return MsgBase(msg="User has been created")


@auth_router.get("/confirm-email", response_model=MsgBase)
async def confirm_email(data: Annotated[VerificationEmailBase, Depends()]):
    """Верифікація електронної пошти користувача. Для верифікації надішліть uuid запису про верифікацію"""
    if await verify_user_email(data):
        return MsgBase(msg="Success verify email")
    else:
        raise HTTPException(
            status_code=404, detail="E-mail verification link not found"
        )


@auth_router.post("/login/", response_model=AuthToken)
async def login_access_refresh_jwt(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> AuthToken:
    """Логінимося та отримуємо токен.
    В формі OAuth2PasswordRequestForm обов'язковими полями входу є username та password. В даному проекті замість
    username ми будемо використовувати номер телефону, поле phone_number!"""
    user = await UserService.authenticate(
        phone_number=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect phone number or password"
        )
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token = await create_jwt_token(
        payload={"user_id": f"{user.id}"},
        private_key_path=settings_class.auth_jwt.private_key_access_jwt_path,
        expire_minutes=settings_class.auth_jwt.ACCESS_TOKEN_EXPIRE_MINUTES,
        algorithm=settings_class.auth_jwt.algorithm,
    )
    refresh_token = await create_jwt_token(
        payload={"user_id": f"{user.id}"},
        private_key_path=settings_class.auth_jwt.private_key_refresh_jwt_path,
        expire_minutes=settings_class.auth_jwt.REFRESH_TOKEN_EXPIRE_MINUTES,
        algorithm=settings_class.auth_jwt.algorithm,
    )
    return AuthToken(access_token=access_token, refresh_token=refresh_token)


@auth_router.post(
    "/refresh_token/", response_model=AuthToken, response_model_exclude_none=True
)
async def refresh_jwt(
    payload: dict = Depends(get_payload_refresh_token),
    user: UserBase = Depends(get_current_active_auth_user_from_refresh),
) -> AuthToken:
    """Отримуємо refresh токен, валідуємо його і повертаємо access токен"""
    access_token = await create_jwt_token(
        payload={"user_id": f"{user.id}"},
        private_key_path=settings_class.auth_jwt.private_key_access_jwt_path,
        expire_minutes=settings_class.auth_jwt.ACCESS_TOKEN_EXPIRE_MINUTES,
        algorithm=settings_class.auth_jwt.algorithm,
    )
    return AuthToken(access_token=access_token, refresh_token=payload["refresh_token"])


@auth_router.post("/recovery-password/{email}", response_model=MsgBase)
async def recovery_password(email: str, task: BackgroundTasks):
    """Відновлення пароля.
    Перевіряємо чи користувач з введеною адресою існує зареєстрований. Якщо існує, і електронна пошта підтверджена,
    генеруємо токен для відновлення пароля та надсилаємо лінк на вказану в профілі електронну пошту. Якщо електронна
    пошта не підтверджена, то просимо підтвердити
    """
    user: UserBase | None = await UserService.get_user_by_email(email=email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist. Check your email.",
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account inactive",
        )
    elif not user.valid_email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not confirmed. Please confirm your email and try again.",
        )
    else:
        recovery_password_token = await create_jwt_token(
            payload={"user_id": f"{user.id}"},
            private_key_path=settings_class.auth_jwt.private_key_recovery_password_path,
            expire_minutes=settings_class.auth_jwt.RECOVERY_PASSWORD_TOKEN_EXPIRE_MINUTES,
            algorithm=settings_class.auth_jwt.algorithm,
        )
        await recovery_password_mail(
            user=user, recovery_password_token=recovery_password_token, task=task
        )
        return MsgBase(msg="Recovery mail is send")


@auth_router.post("/reset-password/", response_model=MsgBase)
async def reset_password(
    password: RecoveryPasswordBase,
    payload_reset_password_token: dict = Depends(get_payload_reset_password_token),
):
    """Відновлення пароля"""
    result = await UserService.recovery_password(
        user_id=payload_reset_password_token["user_id"], password=password.new_password
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not exist",
        )
    return MsgBase(msg="Password changed successfully")
