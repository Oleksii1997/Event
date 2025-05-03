from src.app.auth.security import get_password_hash, verify_password


def test_get_password_hash():
    """Тест хешування пароля"""
    password = "Test18password!"
    hash_password = get_password_hash(password=password)
    assert str(type(hash_password)) == "<class 'bytes'>"


def test_verify_password():
    """Тест верифікації хешованого пароля"""
    password = "Test18password!"
    hash_password = get_password_hash(password=password)
    assert (
        verify_password(plain_password=password, hashed_password=hash_password) == True
    )
