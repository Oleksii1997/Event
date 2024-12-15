import os
from dotenv import dotenv_values, load_dotenv

"""Include /env file"""
load_dotenv()

PROJECT_NAME = "SocialEvent"

API_V1_STR = "/api/v1"

"""Database settings"""

"""Email"""
EMAIL_TEMPLATE_PATH = "src/email_template"

EMAILS_FROM_NAME = PROJECT_NAME


SMTP_EMAIL_HOST = os.getenv("SMTP_EMAIL_HOST")
SMTP_EMAIL_HOST_USER = os.getenv("SMTP_EMAIL_HOST_USER")
SMTP_EMAIL_PORT = os.getenv("SMTP_EMAIL_PORT")
SMTP_EMAIL_GOOGLE_APP_PASSWORD = os.getenv("SMTP_EMAIL_GOOGLE_APP_PASSWORD")
SMTP_EMAIL_USE_TLS = os.getenv("SMTP_EMAIL_USE_TLS")
EMAILS_FROM_EMAIL = os.getenv("EMAILS_FROM_EMAIL")

EMAILS_ENABLED = SMTP_EMAIL_HOST and SMTP_EMAIL_PORT and EMAILS_FROM_EMAIL