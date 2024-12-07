from select import select

from fastapi import BackgroundTasks
from sqlalchemy import select, or_, exists

from src.config.db_settings import new_session
from src.app.users.schemas import UserCreateBase
from src.app.users.models import UserModel
from src.app.users.service import UserCRUD
from src.app.auth.send_email import send_new_account_email

async def registration_user(new_user: UserCreateBase, task: BackgroundTasks) -> bool:
    """Реєстрація користувача"""
    async with new_session() as session:
        query = select(UserModel).where(or_(UserModel.phone_number == new_user.phone_number,
                                            UserModel.email == new_user.email))
        result = await session.execute(query)
        if result.scalar() is not None:
            return True
        else:
            await UserCRUD.created_user(new_user)
            task.add_task(send_new_account_email)
            return False