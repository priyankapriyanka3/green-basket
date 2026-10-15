"""Application configuration using pydantic-settings."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    database_url: str = "sqlite:///./app.db"
    jwt_secret: str = "change-me-in-production"
    jwt_expiry_seconds: int = 3600
    debug: bool = False
    
    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
