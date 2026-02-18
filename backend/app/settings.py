from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Tenebrio Farm"
    db_url: str = "sqlite:///./tenebrio_farm.db"

    model_config = SettingsConfigDict(env_prefix="TENEBRIO_", env_file=".env", extra="ignore")


settings = Settings()
