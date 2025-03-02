import datetime

import aiofiles

from src.app import certs
import jwt


from src.config.settings import settings_class

async def create_jwt_token(payload: dict,
                           private_key_path: str = settings_class.auth_jwt.private_key_jwt_path,
                           algorithm: str = settings_class.auth_jwt.algorithm,
                           expire_minutes: int = settings_class.auth_jwt.ACCESS_TOKEN_EXPIRE_MINUTES,
                           expire_timedelta: datetime.timedelta | None = None
                           ):
    """Create JWT token"""
    private_key = await read_jwt_key(private_key_path)
    to_encode = payload.copy()
    now = datetime.datetime.now(datetime.timezone.utc)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + datetime.timedelta(minutes=expire_minutes)
        to_encode.update(
            exp = expire,
            iat = now
        )
    token = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return token


async def decode_jwt_token(
    token: str | bytes,
    public_key_path: str = settings_class.auth_jwt.public_key_jwt_path,
    algorithm: str = settings_class.auth_jwt.algorithm
    ) -> dict:
    """Decode access token"""
    public_key = read_jwt_key(public_key_path)
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded

async def read_jwt_key(link: str) -> str:
    """Read jwt-private and jwt-public key"""
    async with aiofiles.open(link, mode="r") as f:
        key = ""
        async for line in f:
            key = key + line
    return key

