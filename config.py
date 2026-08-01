from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    SECRET_KEY: SecretStr
    # SQLALCHEMY_DATABASE_URL: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int =30
    max_upload_size_bytes: int = 5* 1024 * 1024
    post_per_page: int = 5

settings= Settings() # loaded from .env file