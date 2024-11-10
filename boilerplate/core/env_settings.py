from pydantic_settings import BaseSettings


class EnvSettings(BaseSettings):
    class Config:
        env_file_encoding = 'utf-8'

    SECRET_KEY: str
    DEBUG: bool


env_settings = EnvSettings()
