from sqladmin import ModelView

from src.app.profile.models import SocialLinkModel
from src.app.users.models import ProfileModel


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
