from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from fastapi import (
    HTTPException,
    status,
)
from fastapi.params import Depends


from src.app.auth.jwt import decode_jwt_token
from src.config.settings import settings_class

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/login/access-token",
)


async def get_payload_access_token(access_token: str = Depends(oauth2_scheme)) -> dict:
    """Розшифровуємо access токен та отримуємо payload"""

    try:
        payload = await decode_jwt_token(
            token=access_token,
            public_key_path=settings_class.auth_jwt.public_key_access_jwt_path,
            algorithm=settings_class.auth_jwt.algorithm,
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token error",
        )
    return payload


async def get_payload_refresh_token(
    refresh_token: str = Depends(oauth2_scheme),
) -> dict:
    """Розшифровуємо refresh токен та отримуємо payload"""

    try:
        payload = await decode_jwt_token(
            token=refresh_token,
            public_key_path=settings_class.auth_jwt.public_key_refresh_jwt_path,
            algorithm=settings_class.auth_jwt.algorithm,
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token error",
        )
    return payload
