from sqladmin import ModelView
from src.app.users.models import UserModel


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
