import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.config import settings


def send_email(email_to: str, subject="", html_template=""):
    """Відправка емейл"""

    assert (
        settings.EMAILS_ENABLED
    ), "No provided configuration for email variables (EMAIL_HOST, EMAIL_PORT and FROM_EMAIL)"

    msg = MIMEMultipart()
    msg["From"] = settings.EMAILS_FROM_EMAIL
    msg["To"] = email_to
    msg["subject"] = subject

    msg.attach(MIMEText(html_template, "html"))

    smtpObj = smtplib.SMTP(settings.SMTP_EMAIL_HOST, settings.SMTP_EMAIL_PORT)
    smtpObj.starttls()
    smtpObj.login(
        settings.SMTP_EMAIL_HOST_USER, settings.SMTP_EMAIL_GOOGLE_APP_PASSWORD
    )
    smtpObj.send_message(msg)
    smtpObj.quit()
