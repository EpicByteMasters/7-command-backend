from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = "Alpha hackathon backend"
    app_description: str = "MVP индивидуального плана развития"
    app_version: str = "1.0.0"
    database_url: str = "sqlite+aiosqlite:///./fastapi.db"
    secret: str = "SECRET"

    class Config:
        env_file = ".env"


settings = Settings()
