from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "DClaw Trademark"
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/dclaw_trademark"
    cors_origins: str = "*"

    class Config:
        env_prefix = "TRADEMARK_"

settings = Settings()
