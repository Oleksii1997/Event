from fastapi import (
    HTTPException,
    status,
)
import bcrypt
from jwt.exceptions import InvalidTokenError


from src.app.auth.jwt import decode_jwt_token
from src.config.settings import settings_class


def get_password_hash(
    password: str,
) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def verify_password(
    plain_password: str,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=plain_password.encode(),
        hashed_password=hashed_password,
    )


async def get_payload_reset_password_token(
    reset_password_token: str,
) -> dict:
    """Розшифровуємо токен відновлення пароля та отримуємо payload (в payload повертаємо uuid користувача)"""

    try:
        payload = await decode_jwt_token(
            token=reset_password_token,
            public_key_path=settings_class.auth_jwt.public_key_recovery_password_path,
            algorithm=settings_class.auth_jwt.algorithm,
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid reset password token",
        )
    return payload
