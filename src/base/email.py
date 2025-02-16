import logging
import emails
from emails.template import JinjaTemplate
import  os
from src.config import settings
import smtplib
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
from email.mime.text import MIMEText


from src.base.get_email_template import verify_auth_template
def send_email(email_to: str, subject="", html_template=""):
    """Відправка емейл"""

    assert settings.EMAILS_ENABLED, "No provided configuration for email variables (EMAIL_HOST, EMAIL_PORT and FROM_EMAIL)"

    msg = MIMEMultipart()
    msg['From'] = settings.EMAILS_FROM_EMAIL
    msg['To'] = email_to
    msg['subject'] = subject

    msg.attach(MIMEText(html_template, 'html'))

    smtpObj = smtplib.SMTP(settings.SMTP_EMAIL_HOST, settings.SMTP_EMAIL_PORT)
    smtpObj.starttls()
    smtpObj.login(settings.SMTP_EMAIL_HOST_USER, settings.SMTP_EMAIL_GOOGLE_APP_PASSWORD)
    smtpObj.send_message(msg)
    smtpObj.quit()


