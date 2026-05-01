import os

class Settings:
    app_name = "AI Content Production API"
    jwt_secret = os.getenv("JWT_SECRET", "change_me")
    jwt_algo = "HS256"
    access_token_minutes = int(os.getenv("ACCESS_TOKEN_MINUTES", "120"))

    postgres_url = os.getenv("DATABASE_URL", "postgresql+psycopg2://app:app@postgres:5432/content_db")
    redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")

    openai_api_key = os.getenv("OPENAI_API_KEY", "")
    openai_model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

settings = Settings()
