from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = "hackathon"
    app_description: str = "MVP платформа"
    app_version: str = "0.0.1"
    database_url: str = "sqlite+aiosqlite:///./fastapi.db"
    secret: str = "SECRET"

    class Config:
        env_file = ".env"


settings = Settings()
