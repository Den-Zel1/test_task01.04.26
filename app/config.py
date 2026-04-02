from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FastAPI Project"
    admin_email: str
    items_per_user: int = 50

    # Автоматически читает из .env
    model_config = SettingsConfigDict(env_file="../.env")


settings = Settings()