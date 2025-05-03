"""Дані які використовуються для тестування API"""

TEST_USER_API = {
    "firstname": "TestFirstname",
    "lastname": "TestLastname",
    "phone_number": "0952247846",
    "email": "biz.django@gmail.com",
    "password": "Oleksii@WM4635AA",
    "is_active": True,
    "valid_email": False,
    "is_staff": False,
    "is_superuser": False,
}

"""Дані для заповнення БД для тестування яки використовуються при запису використовуючи безпосередні SQL запити"""
TEST_USER_MODEL_DB = {
    "user_id": "5911770e-0996-40cf-8b4f-d3fa52b20ffb",
    "firstname": "TestFirstname_2",
    "lastname": "TestLastname_2",
    "phone_number": "0988888881",
    "email": "photoforkop@gmail.com",
    "password": "Oleksii@WM4635AA",
    "is_active": True,
    "valid_email": True,
    "is_staff": False,
    "is_superuser": False,
}

TEST_ME_UPDATE = {
    "firstname": "Firstname_update",
    "lastname": "Lastname_update",
    "phone_number": "0787777777",
    "email": "photoforkop@gmail.com",
}

TEST_USER_MODEL_DB_NO_CONFIRM_MAIL = {
    "user_id": "2dd210e8-bbe5-46e5-a2f1-5c96dbba1fe5",
    "firstname": "TestFirstname_confirm_mail",
    "lastname": "TestLastname_confirm_mail",
    "phone_number": "0658888882",
    "email": "pydjangobot@gmail.com",
    "password": "Oleksii@WM4635AA",
    "is_active": True,
    "valid_email": False,
    "is_staff": False,
    "is_superuser": False,
}

TEST_USER_MODEL_DB_NO_ACTIVE_CONFIRM_MAIL = {
    "user_id": "b9274d7b-13c2-4b10-ab99-b60a8430229b",
    "firstname": "TestFirstname_no_active",
    "lastname": "TestLastname_no_active",
    "phone_number": "0658888883",
    "email": "test_user_1@gmail.com",
    "password": "Oleksii@WM4635AA",
    "is_active": False,
    "valid_email": True,
    "is_staff": False,
    "is_superuser": False,
}

TEST_VERIFICATION_MODEL_DB = {
    "link": "3c115a40-526f-41a5-b791-440df67a8e7e",
    "user_id": "5911770e-0996-40cf-8b4f-d3fa52b20ffb",
}

JWT_TEST_DATA = {
    "algorithm": "RS256",
    "private_key_access_jwt_path": "src/app/certs/jwt-private.pem",
    "public_key_access_jwt_path": "src/app/certs/jwt-public.pem",
    "private_key_refresh_jwt_path": "src/app/certs/refresh-jwt-private.pem",
    "public_key_refresh_jwt_path": "src/app/certs/refresh-jwt-public.pem",
    "private_key_recovery_password_path": "src/app/certs/recovery-password-jwt-private.pem",
    "public_key_recovery_password_path": "src/app/certs/recovery-password-jwt-public.pem",
    "ACCESS_TOKEN_EXPIRE_MINUTES": 10,
    "REFRESH_TOKEN_EXPIRE_MINUTES": 20,
    "RECOVERY_PASSWORD_TOKEN_EXPIRE_MINUTES": 60,
}
