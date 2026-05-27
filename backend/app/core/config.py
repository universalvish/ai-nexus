# AI Nexus Backend

from pydantic_settings import BaseSettings
from typing import List, Optional
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    # App Info
    app_name: str = "AI Nexus"
    app_version: str = "1.0.0"
    debug: bool = False
    secret_key: str = "change-me-in-production"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # CORS
    allowed_origins: List[str] = ["http://localhost:3000", "https://*.vercel.app"]

    # Database
    database_url: str = "postgresql+asyncpg://user:password@localhost:5432/ainexus"
    sync_database_url: str = "postgresql://user:password@localhost:5432/ainexus"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # JWT
    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7

    # Security
    bcrypt_rounds: int = 12
    rate_limit_per_minute: int = 60
    rate_limit_burst: int = 10

    # AI APIs
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    hugging_face_api_key: Optional[str] = None

    # Vector DB
    chroma_persist_directory: str = "./data/chroma"

    # Email
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    email_from: str = "noreply@ainexus.ai"

    # Stripe
    stripe_secret_key: Optional[str] = None
    stripe_webhook_secret: Optional[str] = None
    stripe_price_free: Optional[str] = None
    stripe_price_pro: Optional[str] = None
    stripe_price_business: Optional[str] = None

    # Cloudflare
    cloudflare_api_key: Optional[str] = None
    cloudflare_zone_id: Optional[str] = None

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()