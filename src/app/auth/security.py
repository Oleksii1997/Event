import bcrypt


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
