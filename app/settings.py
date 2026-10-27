from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic.types import SecretStr


class Settings(BaseSettings):
    secret_key: SecretStr
    app_name: str = "Rooms"
    database_url: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()


def get_settings() -> Settings:
    return settings