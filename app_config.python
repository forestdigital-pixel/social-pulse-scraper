from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Supabase
    supabase_url: str
    supabase_key: str

    # Reddit
    reddit_client_id: str
    reddit_client_secret: str
    reddit_user_agent: str = "SocialPulse/1.0"

    # YouTube
    youtube_api_key: str

    # Auth
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS
    cors_origins: List[str] = ["*"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()