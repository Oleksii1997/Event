from pydantic import BaseModel, EmailStr, field_validator
from uuid import UUID
from datetime import datetime


class NewUserBase(BaseModel):
    """Модель для створення користувача під час реєстрації"""
    firstname: str
    lastname: str
    phone_number: str
    email: EmailStr
    password: str


class UserCreateBase(NewUserBase):
    """Модель для перевірки валідності пароля під час створення користувача"""

    @field_validator("password")
    @classmethod
    def validate_password(cls, password):
        special_chars = ('$', '@', '#', '%', '!', '^', '&', '*', '(', ')', '-', '_', '+', '=', '{', '}', '[', ']')
        error_str = ""
        if len(password) < 8:
            error_str = " Довжина паролю повинна бути більша 8 символів. "
        if not any(c.isdigit() for c in password):
            error_str = error_str + " Пароль повинен містити числа. "
        if not any(c.isupper() for c in password):
            error_str = error_str + " Пароль повинен містити літери великого регістру."
        if not any(c.islower() for c in password):
            error_str = error_str + " Пароль повинен містити літери малого регістру. "
        if not any(v in special_chars for v in password):
            error_str = error_str + " Пароль повинен містити хоча б один спеціальний символ %, @, ^..."
        if error_str:
            raise ValueError(error_str)
        return password

class UserAuthBase(BaseModel):
    """Модель для аутентифікації користувача"""
    phone_number: str
    password: str

class UserBase(BaseModel):
    """Модель інформації про користувача"""
    id: UUID
    firstname: str
    lastname: str
    phone_number: str
    email: EmailStr
    valid_email: bool
    is_active: bool
    is_staff: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime


