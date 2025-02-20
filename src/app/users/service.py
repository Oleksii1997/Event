from typing import Optional

from sqlalchemy import select

from src.app.users.schemas import NewUserBase, UserAuthBase, UserCreateBase
from src.config.db_settings import new_session
from src.app.users.models import UserModel
from src.app.auth.security import get_password_hash, verify_password


class UserCRUD:
    """Сlass for working with the user profile and hash password"""
    @classmethod
    async def created_user(cls, data: NewUserBase):
        async with new_session() as session:
            user_dict: dict = data.model_dump()
            user_dict["password"] = get_password_hash(user_dict["password"])
            user = UserModel(**user_dict)
            session.add(user)
            await session.flush()
            await session.commit()
            return user

    @classmethod
    async def authenticate(cls, data:UserAuthBase) -> Optional[UserModel]:
        async with new_session() as session:
            auth_dict: dict = data.model_dump()
            query = select(UserModel).where(UserModel.phone_number == auth_dict["phone_number"])
            result = await session.execute(query)
            task_models = result.scalars().one_or_none()
            return task_models