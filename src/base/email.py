import logging
import emails
from emails.template import JinjaTemplate
import  os
from src.config import settings
"""
def send_email(email_to: str, subject_template="", html_template="", environment={}):

    print("+"*100)
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )

    smtp_options = {"host": settings.SMTP_EMAIL_HOST, "port": settings.SMTP_EMAIL_PORT}
    if settings.SMTP_EMAIL_USE_TLS:
        smtp_options["tls"] = True
    if settings.SMTP_EMAIL_HOST_USER:
        smtp_options["user"] = settings.SMTP_EMAIL_HOST_USER
    if settings.SMTP_EMAIL_HOST_PASSWORD:
        smtp_options["password"] = settings.SMTP_EMAIL_HOST_PASSWORD
    #response = message.send(to=email_to, smtp=smtp_options)
    response = message.send(to='oleksiygr@i.ua', smtp={'host': 'aspmx.l.google.com', 'timeout': 5})
    logging.info(f"send email result: {response}")
    print(response)
"""
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


