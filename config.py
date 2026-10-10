from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_url: str     
    SECRET_KEY: SecretStr
    # SQLALCHEMY_DATABASE_URL: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int =30

    #S3
    S3_BUCKET_NAME:str
    S3_REGION:str = "us-east-1"
    S3_ACCESS_KEY_ID:str | None = None
    S3_SECRET_KEY_ID:str | None = None
    S3_ENDPOINT_URL:str |None = None

    max_upload_size_bytes: int = 5* 1024 * 1024
    post_per_page: int = 5

    PASSWORD_RESET_TOKEN_EXPIRE_HOURS: int = 60
    reset_token_expire_minutes: int = 60
    mail_server: str = "localhost"
    mail_port: int = 587
    mail_username: str = ""
    mail_password: SecretStr = SecretStr("")
    mail_from: str = "noreply@example.com"
    mail_use_tls: bool = True

    frontend_url:str = "http://localhost:8000"
    
    

settings= Settings() # loaded from .env file