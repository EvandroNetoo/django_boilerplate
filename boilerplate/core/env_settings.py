from pathlib import Path

from pydantic_settings import BaseSettings


class EnvSettings(BaseSettings):
    class Config:
        env_file = str(Path(__file__).parent.parent.parent / '.env')
        env_file_encoding = 'utf-8'
        case_sensitive = True

    SECRET_KEY: str
    DEBUG: bool
    DATABASE_URL: str


env_settings = EnvSettings()
