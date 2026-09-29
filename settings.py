from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str
    DEBUG: bool
    DATABASE_URL: str
    SECRET_KEY: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()