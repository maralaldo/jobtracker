from pydantic_settings import BaseSettings
import secrets


class Settings(BaseSettings):
    PROJECT_NAME: str = "JobTracker"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost/jobtracker"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
