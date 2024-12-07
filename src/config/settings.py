import os

PROJECT_NAME = "SocialEvent"

API_V1_STR = "/api/v1"

"""Database settings"""

"""Email"""
EMAIL_TEMPLATE_PATH = "src/email_template"

EMAILS_FROM_NAME = PROJECT_NAME

"""
SMTP_EMAIL_HOST = os.environ.get("EMAIL_HOST")
SMTP_EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
SMTP_EMAIL_PORT = os.environ.get("EMAIL_PORT")
SMTP_EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
SMTP_EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS")
EMAILS_FROM_EMAIL = os.environ.get("EMAILS_FROM_EMAIL")
"""

SMTP_EMAIL_HOST = "aspmx.l.google.com"
SMTP_EMAIL_HOST_USER = "smtpeventtest@gmail.com"
SMTP_EMAIL_PORT = 587
SMTP_EMAIL_HOST_PASSWORD = "111ttt999ooo"
SMTP_EMAIL_USE_TLS = True
EMAILS_FROM_EMAIL = "smtpeventtest@gmail.com"

EMAILS_ENABLED = SMTP_EMAIL_HOST and SMTP_EMAIL_PORT and EMAILS_FROM_EMAIL