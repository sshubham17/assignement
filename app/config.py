import os
from pydantic import BaseModel
from pydantic_settings import BaseSettings

class Info(BaseModel):
    app_name: str = "E-Commerce APIs"
    app_description: str = "E-commerce api that interacts with users."
info = Info()

class Settings(BaseSettings,):
    APP_NAME: str = "FastAPI App"
    api_version: str = "v1"
    DEBUG: bool = True
    LOG_LEVEL: str = "info"
settings = Settings()

class Database(BaseSettings):
    # Database connection settings
    DB_USER: str = os.environ.get('DB_USER') or "postgres"
    DB_PASSWORD: str = os.environ.get('DB_PASSWORD') or "postgres"
    DB_HOST: str = os.environ.get('DB_HOST') or "localhost"  # Use the service name as the hostname
    DB_PORT: int = int(os.environ.get('DB_PORT')) if os.environ.get('DB_PORT') else 5432
    DB_DEFAULT_DATABASE: str = "postgres"

db = Database()