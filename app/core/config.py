from pydantic_settings import BaseSettings, SettingsConfigDict

class AppConfig(BaseSettings):
    CORS_ORIGIN: str
    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


get_settings = AppConfig()