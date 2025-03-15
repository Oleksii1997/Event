from sqladmin import ModelView
from src.app.users.models import UserModel, ProfileModel
from src.app.auth.models import VerificationModel


class UserModelAdmin(ModelView, model=UserModel):

    name = "User"
    name_plural = "Users"
    icon = "fas fa-user-alt"
    category = "Accounts"
    column_list = [
        UserModel.id,
        UserModel.firstname,
        UserModel.lastname,
        UserModel.phone_number,
        UserModel.email,
    ]
    column_searchable_list = [UserModel.id, UserModel.phone_number, UserModel.email]
    column_sortable_list = [
        UserModel.created_at,
    ]
    column_labels = {
        UserModel.id: "UUID",
        UserModel.firstname: "Firstname",
        UserModel.lastname: "Lastname",
        UserModel.phone_number: "Phone number",
        UserModel.password: "Password",
        UserModel.email: "E-mail",
        UserModel.valid_email: "Email confirmed",
        UserModel.is_active: "Is active",
        UserModel.is_staff: "Is staff",
        UserModel.is_superuser: "Is superuser",
        UserModel.created_at: "Created",
        UserModel.updated_at: "Updated",
    }
    column_export_exclude_list = [
        UserModel.password,
    ]
    column_details_exclude_list = [
        UserModel.password,
    ]
    form_edit_rules = ["valid_email", "is_active", "is_staff", "is_superuser"]


class ProfileModelAdmin(ModelView, model=ProfileModel):

    name = "Profile"
    name_plural = "Profiles"
    icon = "fas fa-user-circle"
    category = "Accounts"
    column_list = [ProfileModel.id, ProfileModel.birthday]
    column_searchable_list = [
        ProfileModel.user_id,
    ]
    column_labels = {
        ProfileModel.id: "UUID",
        ProfileModel.birthday: "Birthday",
        ProfileModel.user_id: "User",
        ProfileModel.created_at: "Created",
        ProfileModel.updated_at: "Updated",
    }
    column_export_list = "__all__"
