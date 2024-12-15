from src.base import email
from src.base.get_email_template import verify_auth_template
from src.config.settings import PROJECT_NAME

def send_new_account_email(context):
    subject = f"Registration on the project website {PROJECT_NAME}"
    context["project_name"] = PROJECT_NAME
    template = verify_auth_template(context)
    print(template)
    email.send_email(email_to=context["email"], subject=subject, html_template=template)