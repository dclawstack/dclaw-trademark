from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    app_name: str = "DClaw Trademark"
    app_env: str = "dev"
    debug: bool = True

    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/dclaw_trademark"

    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 60

    openrouter_api_key: str = ""
    ollama_url: str = "http://localhost:11434"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
