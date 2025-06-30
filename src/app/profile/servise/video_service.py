import datetime
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
import os
import aiofiles
import asyncio
from uuid import uuid4
from fastapi import UploadFile, HTTPException

from src.app.profile.models import VideoProfileModel
from src.app.profile.schemas import VideoBase, CreateVideoBase
from src.app.users.schemas import UserBase
from src.config.settings import MEDIA_PATH_VIDEO, MAX_VIDEO_SIZE_BITE


class VideoProfileService:
    """Клас для обробки відео профілю користувача"""

    @classmethod
    async def get_all_video(
        cls, profile_id: UUID, session: AsyncSession
    ) -> List[Optional[VideoBase]]:
        """Отримуємо всі відео профілю користувача.
        На даному етапі обмежуємо кількість відео які може завантажити користувач для опису профілю одним.
        Надалі, можливо розширимо це обмеження"""

        query = select(VideoProfileModel).where(
            VideoProfileModel.profile_id == profile_id
        )
        result = await session.execute(query)
        videos = result.scalars().all()
        if videos:
            return [
                VideoBase.model_validate(video, from_attributes=True)
                for video in videos
            ]
        else:
            return list()

    @classmethod
    async def create_video(
        cls, data: CreateVideoBase, session: AsyncSession
    ) -> VideoBase:
        """Записуємо посилання на збережене відео в базу даних"""
        new_video = VideoProfileModel(**data.model_dump())
        session.add(new_video)
        await session.commit()
        return VideoBase(**new_video.__dict__)

    @classmethod
    async def delete_video_profile(
        cls, video_id: UUID, session: AsyncSession
    ) -> VideoBase | None:
        """Видаляємо відповідний запис про відео профілю з бази даних"""
        query = select(VideoProfileModel).where(VideoProfileModel.id == video_id)
        result = await session.execute(query)
        video = result.scalars().one_or_none()
        if video is not None:
            return_video = VideoBase.model_validate(video, from_attributes=True)
            await session.delete(video)
            await session.commit()
            return return_video
        return None


async def seva_video_profile(file: UploadFile, user: UserBase) -> str:
    """Зберігаємо аватар користувача на сервер"""
    file_path = (
        f"{MEDIA_PATH_VIDEO}/{user.id}_{uuid4()}.{file.content_type.split('/')[1]}"
    )
    if file.size > MAX_VIDEO_SIZE_BITE:
        raise HTTPException(
            status_code=413, detail="Maximum allowed upload size is 15 MB"
        )
    elif file.content_type not in [
        "video/mp4",
    ]:
        raise HTTPException(
            status_code=403,
            detail=f"Unsupported file format {file.content_type}. Supported format: video/mp4",
        )
    else:
        await write_file(file_path=file_path, file=file)
    return file_path


async def write_file(file_path: str, file: UploadFile):
    """Читаємо та записуємо зображення на диск"""
    async with aiofiles.open(file_path, "wb") as buffer:
        data = await file.read()
        await buffer.write(data)


async def delete_video_from_directory(file_path: str):
    """Видаляємо відео з директорії де воно зберігається"""
    try:
        if os.path.exists(file_path):
            await asyncio.to_thread(os.remove, file_path)
    except OSError:
        print(f"ERROR deleted file {file_path}")
