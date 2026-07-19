"""
Centralized application configuration.
All values are read from environment variables (or a local .env file).
"""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- App ---
    APP_NAME: str = "Kairaly Furniture Sofa Catalog"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = True

    # --- Database ---
    DATABASE_URL: str = "sqlite:///./kairaly.db"

    # --- Security ---
    SECRET_KEY: str = "insecure-dev-secret-change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

    # --- Default admin (used by seed script) ---
    DEFAULT_ADMIN_USERNAME: str = "admin"
    DEFAULT_ADMIN_PASSWORD: str = "admin123"
    DEFAULT_ADMIN_EMAIL: str = "admin@kairalyfurniture.com"

    # --- Uploads ---
    UPLOAD_DIR: str = "static/uploads"
    MAX_IMAGE_SIZE_MB: int = 5

    # --- CORS ---
    CORS_ORIGINS: str = "*"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def cors_origins_list(self) -> list[str]:
        if self.CORS_ORIGINS.strip() == "*":
            return ["*"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
