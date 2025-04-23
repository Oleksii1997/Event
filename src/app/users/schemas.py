from pydantic import BaseModel, EmailStr, field_validator, ValidationInfo
from uuid import UUID
from datetime import datetime


class NewUserBase(BaseModel):
    """Модель для створення користувача під час реєстрації"""

    firstname: str
    lastname: str
    phone_number: str
    email: EmailStr
    password: str


class ValidatePasswordBase:
    """Клас валідації пароля"""

    @field_validator("password")
    @classmethod
    def validate_password(cls, password):
        special_chars = (
            "$",
            "@",
            "#",
            "%",
            "!",
            "^",
            "&",
            "*",
            "(",
            ")",
            "-",
            "_",
            "+",
            "=",
            "{",
            "}",
            "[",
            "]",
        )
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
            error_str = (
                error_str
                + " Пароль повинен містити хоча б один спеціальний символ %, @, ^..."
            )
        if error_str:
            raise ValueError(error_str)
        return password


class UserCreateBase(NewUserBase, ValidatePasswordBase):
    """Модель для перевірки валідності пароля під час створення користувача"""

    pass


class RecoveryPasswordBase(BaseModel):
    """Валідація паролів при відновлнні паролю"""

    new_password: str
    confirm_password: str

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, new_password):
        ValidatePasswordBase.validate_password(new_password)
        return new_password

    @field_validator("confirm_password")
    @classmethod
    def check_equal_password(cls, confirm_password: str, info: ValidationInfo):
        if (
            "new_password" in info.data
            and confirm_password != info.data["new_password"]
        ):
            raise ValueError("Пароль і пароль підтвердження повинні бути однаковими")
        return confirm_password


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


class UpdateUserBase(BaseModel):
    """Модель оновлення даних користувача"""

    firstname: str
    lastname: str
    phone_number: str
    email: EmailStr
