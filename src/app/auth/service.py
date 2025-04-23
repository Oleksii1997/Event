from select import select

from fastapi import BackgroundTasks, Depends
from pydantic import EmailStr
from sqlalchemy import select, or_
from typing import Annotated

from src.config.db_settings import new_session

from src.config.settings import SERVER_HOST
from src.app.users.service.user_service import UserService
from src.app.auth.send_email import send_new_account_email, send_recovery_password_email

from src.app.users.schemas import NewUserBase, UserBase
from src.app.auth.schemas import VerificationBase, VerificationEmailBase

from src.app.users.models import UserModel
from src.app.auth.models import VerificationModel

from sqlalchemy.ext.asyncio import AsyncSession


async def registration_user(
    new_user: NewUserBase,
    session: AsyncSession,
    task: BackgroundTasks,
) -> UserBase | None:
    """Реєстрація користувача

    Перевіряємо чи існує користувач, якщо існує, то повертаємо True
    Якщо користувача не існує, то створюємо його та створюємо запис для верифікації користувача,
    відправляємо електронного листа для верифікації реєстрації
    """
    query = select(UserModel).where(
        or_(
            UserModel.phone_number == new_user.phone_number,
            UserModel.email == new_user.email,
        )
    )
    result = await session.execute(query)
    if result.scalar() is not None:
        return None
    else:
        user: UserBase = await UserService.created_user(data=new_user, session=session)
        verify_id = await create_verification(
            data=VerificationBase(user_id=user.id), session=session
        )
        context: dict[str, str | EmailStr] = {
            "phone_number": new_user.phone_number,
            "email": new_user.email,
            "firstname": new_user.firstname,
            "lastname": new_user.lastname,
            "link": f"{SERVER_HOST}/api/v1/confirm-email?link={verify_id}",
        }
        task.add_task(send_new_account_email, context)
        return user


async def recovery_password_mail(
    user: UserBase, recovery_password_token: str, task: BackgroundTasks
):
    """Генеруємо контекст повідомлення, по відновленню пароля та надсилаємо листа"""
    context: dict[str, str | EmailStr] = {
        "email": user.email,
        "firstname": user.firstname,
        "lastname": user.lastname,
        "link": f"{SERVER_HOST}/api/v1/reset-password?token={recovery_password_token}",
    }
    task.add_task(send_recovery_password_email, context)
    return


async def create_verification(
    data: VerificationBase,
    session: AsyncSession,
):
    """Створення запису в моделі верифікації"""
    verification_dict: dict = data.model_dump()
    verify = VerificationModel(**verification_dict)
    session.add(verify)
    await session.flush()
    await session.commit()
    return verify.link


async def verify_user_email(data: VerificationEmailBase) -> bool:
    """Підтвердження верифікації електронної пошти користувача"""
    async with new_session() as session:
        query = select(VerificationModel).where(VerificationModel.link == data.link)
        result = await session.execute(query)
        res = result.scalars().one_or_none()
        if res is not None:
            await UserService.check_valid_email(res.user_id)
            await session.delete(res)
            await session.commit()
            return True
        else:
            return False
