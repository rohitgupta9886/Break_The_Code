import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    ENVIRONMENT: str = Field(default="development")
    PROJECT_NAME: str = Field(default="Break The Code")
    API_V1_STR: str = Field(default="/api/v1")
    
    SECRET_KEY: str = Field(default="dev_secret_key_change_in_production_jwt_signature_breakthecode_2026")
    JWT_SECRET: str = Field(default="dev_jwt_secret_change_in_production_breakthecode_2026")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=120)
    ALGORITHM: str = Field(default="HS256")
    
    # Database
    DATABASE_URL: str = Field(default="sqlite+aiosqlite:///./breakthecode.db")
    SYNC_DATABASE_URL: str = Field(default="sqlite:///./breakthecode.db")
    
    # Redis
    REDIS_URL: Optional[str] = Field(default="redis://localhost:6379/0")
    
    # AI Provider
    LLM_PROVIDER: str = Field(default="gemini")
    LLM_API_KEY: Optional[str] = Field(default=None)
    GEMINI_API_KEY: Optional[str] = Field(default=None)
    GOOGLE_API_KEY: Optional[str] = Field(default=None)
    GEMINI_MODEL: str = Field(default="gemini-3-flash-preview")
    LANGSMITH_API_KEY: Optional[str] = Field(default=None)
    LANGSMITH_PROJECT: str = Field(default="break-the-code")
    LANGSMITH_TRACING: bool = Field(default=False)
    
    # CORS
    FRONTEND_URL: str = Field(default="http://localhost:3000")
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]

    def get_gemini_api_key(self) -> Optional[str]:
        """Resolves the Google Gemini API key from various supported environment variables."""
        return self.GEMINI_API_KEY or self.GOOGLE_API_KEY or self.LLM_API_KEY

    class Config:
        env_file = (".env", "../.env")
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"

settings = Settings()
