from select import select

from fastapi import BackgroundTasks
from pydantic import EmailStr
from sqlalchemy import select, or_, exists

from src.config.db_settings import new_session
from src.app.users.schemas import NewUserBase
from src.app.users.models import UserModel
from src.app.users.service import UserService
from src.app.auth.send_email import send_new_account_email
from src.app.auth.schemas import VerificationBase, VerificationEmailBase
from src.app.auth.models import VerificationModel
from src.config.settings import SERVER_HOST
from src.app.users.service import UserService
from src.app.auth.jwt import decode_jwt_token

async def registration_user(new_user: NewUserBase, task: BackgroundTasks) -> bool:
    """Реєстрація користувача

        Перевіряємо чи існує користувач, якщо існує то повертаємо True
        Якщо користувача не існує, то створюємо його та створюємо запис для верифікації користувача,
        відправляємо електронного листа для верифікації реєстрації
    """
    async with new_session() as session:
        query = select(UserModel).where(or_(UserModel.phone_number == new_user.phone_number,
                                            UserModel.email == new_user.email))
        result = await session.execute(query)
        if result.scalar() is not None:
            return True
        else:

            user = await UserService.created_user(new_user)
            verify_id = await create_verification(VerificationBase(user_id = user.id))
            context: dict[str, str | EmailStr] = {
                "phone_number": new_user.phone_number,
                "email": new_user.email,
                "firstname": new_user.firstname,
                "lastname": new_user.lastname,
                "link": f"{SERVER_HOST}/api/v1/confirm-email?link={verify_id}"
            }
            task.add_task(send_new_account_email, context)
            return False

async def create_verification(data: VerificationBase):
    """Створення запису в моделі верифікації"""
    async with new_session() as session:
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

