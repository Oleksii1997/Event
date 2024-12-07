from pydantic import BaseModel


class MsgBase(BaseModel):
    """Схема для відповіді при реєстрації користувача"""
    msg: str