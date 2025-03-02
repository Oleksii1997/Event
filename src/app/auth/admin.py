from sqladmin import ModelView
from src.app.auth.models import VerificationModel


class VerificationModelAdmin(ModelView, model = VerificationModel):

    name = "Verification e-mail"
    name_plural = "Verifications e-mail"
    icon = "fas fa-mail-bulk"
    category = "Verification"
    column_list = [VerificationModel.link, VerificationModel.user_id, VerificationModel.created_at]
    column_labels = {VerificationModel.link: "UUID", VerificationModel.user_id: "User UUID",
                     VerificationModel.created_at: "Created at"}