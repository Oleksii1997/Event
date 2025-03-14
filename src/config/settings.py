import os
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings


"""Include /env file"""
load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_NAME = "SocialEvent"


class AuthJWT(BaseModel):
    """Schema for path JWT key"""

    private_key_access_jwt_path: str = "src/app/certs/jwt-private.pem"
    public_key_access_jwt_path: str = "src/app/certs/jwt-public.pem"
    private_key_refresh_jwt_path: str = "src/app/certs/refresh-jwt-private.pem"
    public_key_refresh_jwt_path: str = "src/app/certs/refresh-jwt-public.pem"
    private_key_recovery_password_path: str = (
        "src/app/certs/recovery-password-jwt-private.pem"
    )
    public_key_recovery_password_path: str = (
        "src/app/certs/recovery-password-jwt-public.pem"
    )
    algorithm: str = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 20
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60
    RECOVERY_PASSWORD_TOKEN_EXPIRE_MINUTES: int = 60


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    auth_jwt: AuthJWT = AuthJWT()


settings_class = Settings()

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
SERVER_HOST = os.getenv("SERVER_HOST")

EMAILS_ENABLED = SMTP_EMAIL_HOST and SMTP_EMAIL_PORT and EMAILS_FROM_EMAIL
