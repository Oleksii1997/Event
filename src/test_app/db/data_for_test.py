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

"""Користувач для тестування профілю користувача"""
TEST_USER_FOR_PROFILE_DB = {
    "user_id": "a192bcfe-0b91-437c-a365-6b3134f65387",
    "firstname": "TestFirstname_profile",
    "lastname": "TestLastname_profile",
    "phone_number": "0998567683",
    "email": "rvk10discord@gmail.com",
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

AREA_TEST_DATA = [
    {"id": 18, "area_name": "Сумська область"},
    {"id": 11, "area_name": "Київська область"},
]

TEST_AREA_ID = 18  # id області районів які є тестовими даними
TEST_REGION_ID = 1392  # id району громади якої представлені у тестових даних
TEST_COMMUNITY_ID = (
    4579  # id громади населені пункти якої представлені у тестових даних
)
TEST_FAKE_ID = 181  # хибне значення id для перевірки випадків коли передаються дані за якими немає зв'язаних об'єктів
REGION_TEST_DATA = [
    {"id": 1390, "region_name": "Роменський район", "area_id": 18},
    {"id": 1389, "region_name": "Охтирський район", "area_id": 18},
    {"id": 1391, "region_name": "Сумський район", "area_id": 18},
    {"id": 1392, "region_name": "Шосткинський район", "area_id": 18},
    {"id": 1388, "region_name": "Конотопський район", "area_id": 18},
]

COMMUNITY_TEST_DATA = [
    {"id": 4569, "community_name": "Свеська територіальна громада", "region_id": 1392},
    {
        "id": 4543,
        "community_name": "Глухівська територіальна громада",
        "region_id": 1392,
    },
    {
        "id": 4545,
        "community_name": "Дружбівська територіальна громада",
        "region_id": 1392,
    },
    {
        "id": 4547,
        "community_name": "Есманьська територіальна громада",
        "region_id": 1392,
    },
    {
        "id": 4579,
        "community_name": "Шалигинська територіальна громада",
        "region_id": 1392,
    },
    {
        "id": 4580,
        "community_name": "Шосткинська територіальна громада",
        "region_id": 1392,
    },
    {
        "id": 4534,
        "community_name": "Березівська територіальна громада",
        "region_id": 1392,
    },
    {
        "id": 4570,
        "community_name": "Середино-Будська територіальна громада",
        "region_id": 1392,
    },
    {
        "id": 4582,
        "community_name": "Ямпільська територіальна громада",
        "region_id": 1392,
    },
    {
        "id": 4548,
        "community_name": "Зноб-Новгородська територіальна громада",
        "region_id": 1392,
    },
]

TEST_SEARCH_STRING_1 = "сел"  # приклад пошукового запиту №1
LEN_TEST_SEARCH_1 = 10  # довжина списку результату запиту який повинен бути при виконанні пошукового запиту №1
TEST_SEARCH_STRING_2 = "черне"  # приклад пошукового запиту №2
RESULT_SEARCH_2 = [
    {
        "id": 6638,
        "city_name": "село Черневе",
        "community_id": 4579,
        "city_community": {
            "id": 4579,
            "community_name": "Шалигинська територіальна громада",
            "region_id": 1392,
            "community_region": {
                "id": 1392,
                "region_name": "Шосткинський район",
                "area_id": 18,
                "region_area": {"id": 18, "area_name": "Сумська область"},
            },
        },
    }
]
LEN_TEST_SEARCH_2 = 1  # довжина списку результату запиту який повинен бути при виконанні пошукового запиту №2
FAKE_SEARCH_STRING = "фейкова назва"  # хибна назва населеного пункту для перевірки випадку коли пошуковий запит не дасть результату
CITY_TEST_DATA = [
    {"id": 6633, "city_name": "село Гудове", "community_id": 4579},
    {"id": 6634, "city_name": "село Ємадикине", "community_id": 4579},
    {"id": 6635, "city_name": "село Сваркове", "community_id": 4579},
    {"id": 6636, "city_name": "село Соснівка", "community_id": 4579},
    {"id": 6637, "city_name": "село Старикове", "community_id": 4579},
    {"id": 6638, "city_name": "село Черневе", "community_id": 4579},
    {"id": 6639, "city_name": "село Вовківка", "community_id": 4579},
    {"id": 6640, "city_name": "село Катеринівка", "community_id": 4579},
    {"id": 6641, "city_name": "село Ходине", "community_id": 4579},
    {"id": 6642, "city_name": "селище Шалигине", "community_id": 4579},
]

TEST_CREATE_SOCIAL_LINK = {"link_type": "Facebook", "link": "facebook test link"}
TEST_CREATE_SOCIAL_LINK_DB = {
    "id": "cba0bfd5-9caf-4356-a5e8-99848e821c3e",
    "link_type": "Telegram",
    "link": "Link by telegram",
}
INVALID_TEST_CREATE_SOCIAL_LINK = {
    "link_type": "Fake type",
    "link": "facebook test link fake",
}

CREATE_PROFILE_DATA_API = {
    "birthday": "2025-05-31",
    "description": "Опис про себе, тестовий запис",
    "area": 18,
    "region": 1392,
    "community": 4579,
    "city": 6638,
}
CREATE_PROFILE_DATA_DB = {
    "id": "bcf08e76-4dbe-4dcb-9351-4192b02ee2af",
    "birthday": "2019-05-31",
    "description": "Опис про себе, тестовий запис, База Даних",
    "area": 18,
    "region": 1392,
    "community": 4579,
    "city": 6639,
}
PROFILE_UPDATE_DB = {
    "birthday": "1987-04-17",
    "description": "Оновлені дані профілю",
    "area": 18,
    "region": 1392,
    "community": 4579,
    "city": 6639,
}
PROFILE_FUTURE_BIRTHDAY = {
    "birthday": "2126-05-31",
    "description": "Опис про себе, тестовий запис",
    "area": 18,
    "region": 1392,
    "community": 4579,
    "city": 6638,
}
PROFILE_OLD_BIRTHDAY = {
    "birthday": "2126-05-31",
    "description": "Опис про себе, тестовий запис",
    "area": 18,
    "region": 1392,
    "community": 4579,
    "city": 6638,
}
PROFILE_CITY_DOSE_NOT_EXIST = {
    "birthday": "2019-05-31",
    "description": "Опис про себе, тестовий запис",
    "area": 18,
    "region": 1392,
    "community": 4579,
    "city": 6638000,
}
PROFILE_FAKE_LOCATION = {
    "birthday": "2019-05-31",
    "description": "Опис про себе, тестовий запис",
    "area": 18,
    "region": 13920000,
    "community": 4579,
    "city": 6638,
}
FAKE_PROFILE_UUID = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
