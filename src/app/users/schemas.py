from pydantic import BaseModel, EmailStr

class UserCreateBase(BaseModel):
    """Модель для створення користувача під час реєстрації"""
    firstname: str
    lastname: str
    phone_number: str
    email: EmailStr
    password: str

class UserAuthBase(BaseModel):
    """Модель для аутентифікації користувача"""
    phone_number: str
    password: str
