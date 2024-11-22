# app/core/config.py

from pydantic_settings import BaseSettings
from pydantic import Field, HttpUrl

class Settings(BaseSettings):
    APP_NAME: str = Field(default="ToDo List Application")
    DEBUG: bool = Field(default=False)
    VERSION: str = Field(default="1.0.0")

    # Database Settings
    MONGODB_URI: str = Field(..., env="MONGODB_URI")
    DATABASE_NAME: str = Field(default="projectDB")

    # Security Settings
    JWT_SECRET_KEY: str = Field(..., env="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)

    # Email Settings (if you plan to send emails)
    EMAIL_HOST: str = Field(..., env="EMAIL_HOST")
    EMAIL_PORT: int = Field(default=587)
    EMAIL_USERNAME: str = Field(..., env="EMAIL_USERNAME")
    EMAIL_PASSWORD: str = Field(..., env="EMAIL_PASSWORD")
    EMAIL_FROM: str = Field(..., env="EMAIL_FROM")
    EMAIL_FROM_NAME: str = Field(default="ToDo App Support")
    EMAIL_TLS: bool = Field(default=True)
    EMAIL_SSL: bool = Field(default=False)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Initialize the settings
settings = Settings()