import os
import aiofiles
import asyncio
from uuid import uuid4
from fastapi import UploadFile, HTTPException

from src.app.profile.models import AvatarModel
from src.config.settings import MEDIA_PATH_AVATAR, MAX_AVATAR_SIZE_BITE
from src.app.users.schemas import UserBase


async def seva_image_avatar(file: UploadFile, user: UserBase) -> str:
    """Зберігаємо аватар користувача на сервер"""
    file_path = (
        f"{MEDIA_PATH_AVATAR}/{user.id}_{uuid4()}.{file.content_type.split('/')[1]}"
    )
    if file.size > MAX_AVATAR_SIZE_BITE:
        raise HTTPException(
            status_code=413, detail="Maximum allowed upload size is 200 kB"
        )
    elif file.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
        raise HTTPException(
            status_code=403,
            detail=f"Unsupported file format {file.content_type}. Supported format: image/jpeg, image/jpg, image/png",
        )
    else:
        await write_image(file_path=file_path, file=file)
    return file_path


async def write_image(file_path: str, file: UploadFile):
    """Читаємо та записуємо зображення на диск"""
    async with aiofiles.open(file_path, "wb") as buffer:
        data = await file.read()
        await buffer.write(data)


async def delete_avatar_from_directory(file_path: str):
    """Видаляємо зображення з директорії де воно зберігається"""
    try:
        if os.path.exists(file_path):
            await asyncio.to_thread(os.remove, file_path)
    except OSError:
        print(f"ERROR deleted file {file_path}")
