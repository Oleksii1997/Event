import asyncio
from sqlalchemy import event
from src.app.profile.models import AvatarModel, ProfileModel, VideoProfileModel
from src.app.users.models import UserModel
from src.app.profile.servise.image_service import delete_avatar_from_directory
from src.app.profile.servise.video_service import delete_video_from_directory


@event.listens_for(AvatarModel, "after_delete")
def avatar_post_delete_event(mapper, connection, target):
    """Обробник подій який спрацьовує при видаленні запису з моделі аватарок який запускає видалення фото з директорії,
    шлях до якої збережено в avatar_url"""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.create_task(
                delete_avatar_from_directory(file_path=target.avatar_url)
            )
        else:
            loop.run_until_complete(
                delete_avatar_from_directory(file_path=target.avatar_url)
            )
    except RuntimeError:
        asyncio.run(delete_avatar_from_directory(file_path=target.avatar_url))


@event.listens_for(VideoProfileModel, "after_delete")
def video_profile_post_delete_event(mapper, connection, target):
    """Обробник подій який спрацьовує при видаленні запису з моделі відео профілю який запускає видалення відео з директорії,
    шлях до якої збережено в video_url"""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.create_task(delete_video_from_directory(file_path=target.video_url))
        else:
            loop.run_until_complete(
                delete_video_from_directory(file_path=target.video_url)
            )
    except RuntimeError:
        asyncio.run(delete_video_from_directory(file_path=target.video_url))
