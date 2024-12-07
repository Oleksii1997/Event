import logging
import emails
from emails.template import JinjaTemplate

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
from email.mime.text import MIMEText
def send_email(email_to: str, subject_template="", html_template="", environment={}):
    addr_from = "smtpeventtest@gmail.com"
    addr_to = "oleksiygr@i.ua"
    password = "111ttt999ooo"

    msg = MIMEMultipart()
    msg['From'] = addr_from
    msg['To'] = addr_to
    msg['subject'] = "Thema"
    text1 = ("Text")
    msg.attach(MIMEText(text1, 'plain'))

    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login(addr_from, password)
    smtpObj.send_message(msg)
    smtpObj.quit()



