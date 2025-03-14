from src.base import email
from src.base.get_email_template import get_email_template
from src.config.settings import PROJECT_NAME


def send_new_account_email(context: dict):
    subject = f"Registration on the project website {PROJECT_NAME}"
    context["project_name"] = PROJECT_NAME
    template = get_email_template(context=context, template_name="verify_account.html")
    email.send_email(email_to=context["email"], subject=subject, html_template=template)


def send_recovery_password_email(context: dict):
    subject = f"Recovery password on the project website {PROJECT_NAME}"
    context["project_name"] = PROJECT_NAME
    template = get_email_template(
        context=context, template_name="recovery_password.html"
    )
    email.send_email(email_to=context["email"], subject=subject, html_template=template)
