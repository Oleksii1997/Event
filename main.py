from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.app import routers
from src.config import settings
from src.config.make_db import create_tables, delete_tables
from src.app.users.models import UserModel, ProfileModel
from src.app.auth.models import VerificationModel

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
    lifespan=lifespan
)

app.include_router(routers.api_router, prefix=settings.API_V1_STR)
