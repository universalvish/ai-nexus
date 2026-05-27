# Secure Production Configuration
# DO NOT commit actual values - use secrets only

import os
from typing import List
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Production settings with security defaults."""
    
    # Application
    APP_NAME: str = "AI Nexus"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "production"  # Never set to development in production
    DEBUG: bool = False  # CRITICAL: Must be False in production
    
    # Security
    SECRET_KEY: str = ""  # MUST be set via environment variable
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    PASSWORD_RESET_TOKEN_EXPIRE_HOURS: int = 1
    
    # Database
    DATABASE_URL: str = ""  # MUST be set via environment variable
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_PASSWORD: str = ""
    
    # CORS - CRITICAL: Restrict to specific origins only
    CORS_ORIGINS: str = ""  # Comma-separated list of allowed origins
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from string."""
        if not self.CORS_ORIGINS:
            return []
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # AI Services - API keys should be in secrets
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    HUGGINGFACE_API_KEY: str = ""
    
    # Stripe
    STRIPE_SECRET_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    
    # Supabase
    SUPABASE_URL: str = ""
    SUPABASE_ANON_KEY: str = ""
    SUPABASE_SERVICE_KEY: str = ""
    
    # Admin Configuration
    ADMIN_EMAIL: str = "admin@localhost"
    EMERGENCY_STOP_ENABLED: bool = True
    
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "production"
    
    @property
    def is_secure(self) -> bool:
        """Verify all security requirements are met."""
        return (
            not self.DEBUG and
            bool(self.SECRET_KEY) and
            len(self.SECRET_KEY) >= 32 and
            bool(self.DATABASE_URL) and
            self.is_production
        )
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        # Don't load from .env in production
        if os.getenv("ENVIRONMENT", "").lower() == "production":
            env_file = ""


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Create settings instance
settings = get_settings()