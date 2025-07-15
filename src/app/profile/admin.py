from markupsafe import Markup
from sqladmin import ModelView

from src.app.profile.models import SocialLinkModel, AvatarModel, VideoProfileModel
from src.app.users.models import ProfileModel
from src.config.settings import base_url


def format_image_url(model, attribute) -> Markup:
    """Для відображення зображення"""
    return Markup(
        f'<img src="{base_url}/{getattr(model, attribute)}" width="60" height="60"/>'
    )


def format_video_url(model, attribute) -> Markup:
    """Для відображення відео"""
    return Markup(
        f'<video width="320" height="240" controls>'
        f'<source src="{base_url}/{getattr(model, attribute)}" type="video/mp4">'
        f"Your browser does not support the video tag."
        f"</video>"
    )


class ProfileModelAdmin(ModelView, model=ProfileModel):
    """Опис моделі профілю користувача в адмінпанелі"""

    name = "Profile"
    name_plural = "Profiles"
    icon = "fas fa-user-circle"
    category = "Accounts"
    can_edit = False
    column_list = [ProfileModel.id, ProfileModel.profile_user]
    column_searchable_list = [ProfileModel.user_id, ProfileModel.id]
    column_labels = {
        ProfileModel.id: "Profile ID",
        ProfileModel.user_id: "User ID",
        ProfileModel.profile_user: "User",
        ProfileModel.profile_avatar: "Avatar",
        ProfileModel.profile_video: "Video",
        ProfileModel.birthday: "Birthday",
        ProfileModel.description: "Description profile",
        ProfileModel.profile_social_link: "Social link",
        ProfileModel.area: "Area ID",
        ProfileModel.profile_area: "Area",
        ProfileModel.region: "Region ID",
        ProfileModel.profile_region: "Region",
        ProfileModel.community: "Community ID",
        ProfileModel.profile_community: "Community",
        ProfileModel.city: "City ID",
        ProfileModel.profile_city: "City",
        ProfileModel.created_at: "Created",
        ProfileModel.updated_at: "Updated",
    }
    column_export_list = [
        "id",
        "profile_user",
        "birthday",
        "description",
        "profile_area",
        "profile_region",
        "profile_community",
        "profile_city",
    ]


class SocialLinkModelAdmin(ModelView, model=SocialLinkModel):
    """Опис моделі посилань на соціальні мережі в адмінпанелі"""

    name = "Social Link"
    name_plural = "Social Links"
    icon = "fa-brands fa-facebook"
    category = "Accounts"
    can_edit = False
    column_list = [SocialLinkModel.id, SocialLinkModel.link_type, SocialLinkModel.link]
    column_labels = {
        SocialLinkModel.id: "ID",
        SocialLinkModel.link_type: "Social network",
        SocialLinkModel.link: "Link",
        SocialLinkModel.profile_id: "Profile ID",
        SocialLinkModel.social_link_profile: "User profile",
    }
    column_searchable_list = [SocialLinkModel.id, SocialLinkModel.link]
    column_export_list = [
        SocialLinkModel.id,
        SocialLinkModel.link_type,
        SocialLinkModel.link,
        SocialLinkModel.profile_id,
    ]


class AvatarModelAdmin(ModelView, model=AvatarModel):
    """Опис моделі аватарок в адмінпанелі користувача"""

    name = "Avatar"
    name_plural = "Avatars"
    icon = "fas fa-images"
    category = "Accounts"
    column_formatters = {
        "avatar_url": format_image_url,
    }
    column_formatters_detail = {
        "avatar_url": format_image_url,
    }
    column_list = [AvatarModel.id, AvatarModel.avatar_url, AvatarModel.profile_id]
    column_labels = {
        AvatarModel.id: "ID",
        AvatarModel.avatar_url: "Avatar URL",
        AvatarModel.profile_id: "Profile ID",
        AvatarModel.avatar_profile: "User profile",
        AvatarModel.created_at: "Created",
    }
    column_searchable_list = [
        AvatarModel.id,
        AvatarModel.profile_id,
        AvatarModel.avatar_url,
    ]
    column_export_list = [
        AvatarModel.id,
        AvatarModel.avatar_url,
        AvatarModel.profile_id,
        AvatarModel.created_at,
    ]


class VideoProfileModelAdmin(ModelView, model=VideoProfileModel):
    """Опис моделі відео профілю в адмінпанелі користувача"""

    name = "Video"
    name_plural = "Videos"
    icon = "far fa-file-video"
    category = "Accounts"
    column_formatters = {
        "video_url": format_video_url,
    }
    column_formatters_detail = {
        "video_url": format_video_url,
    }
    column_list = [
        VideoProfileModel.id,
        VideoProfileModel.video_url,
        VideoProfileModel.profile_id,
    ]
    column_labels = {
        VideoProfileModel.id: "ID",
        VideoProfileModel.video_url: "Avatar URL",
        VideoProfileModel.profile_id: "Profile ID",
        VideoProfileModel.video_profile: "User profile",
        VideoProfileModel.created_at: "Created",
    }
    column_searchable_list = [
        VideoProfileModel.id,
        VideoProfileModel.profile_id,
        VideoProfileModel.video_url,
    ]
    column_export_list = [
        VideoProfileModel.id,
        VideoProfileModel.video_url,
        VideoProfileModel.profile_id,
        VideoProfileModel.created_at,
    ]
