from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqladmin import Admin

from src.app import routers
from src.config import settings
from src.config.make_db import create_tables, delete_tables
from src.config.db_settings import async_engine
from src.app.users.admin import UserModelAdmin, ProfileModelAdmin
from src.app.auth.admin import VerificationModelAdmin


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print("Clean DB")
    await create_tables()
    print("DB ready")
    yield
    print("OFF")


app = FastAPI(
    title="SocialEvent",
    description="Проект для об'єднання людей за спільними інтересами та цілями. Метою є створення платформи для "
    "організації заходів різних напрямків (починаючи від волонтерських ініціатив до розважальних заходів), "
    "та заходів різного масштабу і формату проведення (від концертів до пошуку напарника для гри в настольний теніс)",
    version="0.0.1",
    lifespan=lifespan,
)

admin = Admin(app, async_engine)
admin.add_view(UserModelAdmin)
admin.add_view(ProfileModelAdmin)
admin.add_view(VerificationModelAdmin)

app.include_router(routers.api_router, prefix=settings.settings_class.api_v1_prefix)
