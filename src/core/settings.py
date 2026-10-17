from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    log_lvl: str = "INFO" 
    postgres_host: str
    postgres_db: str
    postgres_user: str
    postgres_password: SecretStr
    postgres_port: int

    telegram_token: SecretStr = SecretStr("dummy_token")
    request_from_telegram_secret: SecretStr = SecretStr("dummy_secret")
    webhook_url: str = "https://dummy.url"
    telegram_user_id: int = 0

    @property
    def postgres_url(self) -> str:
        return URL.create(
            "postgresql+asyncpg",
            username=self.postgres_user,
            password=self.postgres_password.get_secret_value(),
            host=self.postgres_host,
            port=self.postgres_port,
            database=self.postgres_db,
        ).render_as_string(hide_password=False)


settings = Settings()
