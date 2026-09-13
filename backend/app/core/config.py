from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "OpsFlow API"
    app_env: str = "development"
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/opsflow"
    jwt_secret: str = "development-only-secret"
    cors_origins: str = "http://localhost:4200"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def allowed_origins(self) -> list[str]:
        return [value.strip() for value in self.cors_origins.split(",") if value.strip()]

@lru_cache
def get_settings() -> Settings:
    return Settings()
