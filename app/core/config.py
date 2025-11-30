from typing import List
import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="allow")  # <-- allow extra fields

    SECRET_KEY: str = os.getenv("SECRET_KEY", "LIN")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Log DATABASE_URL status (without exposing the full URL)
        db_url = self.DATABASE_URL
        if db_url:
            print(f"✅ DATABASE_URL is set (length: {len(db_url)}, starts with: {db_url[:20]}...)")
        else:
            print("⚠️ DATABASE_URL is not set - using default SQLite")


settings = Settings()