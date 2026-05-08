from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "Chat2Anything Migration API"
    app_env: str = "dev"
    app_host: str = "0.0.0.0"
    app_port: int = 8100

    database_url: str = "sqlite:///./migration.db"
    jwt_secret: str = "change_me"
    jwt_algorithm: str = "HS256"
    jwt_expire_seconds: int = 7200

    bootstrap_admin_username: str = "admin"
    bootstrap_admin_password: str = "123456"
    bootstrap_admin_department: str = "platform"

    storage_dir: str = "./storage/uploads"
    context_window_default: int = 5
    rag_top_k: int = 5

    audit_retention_days: int = 180

    @property
    def storage_path(self) -> Path:
        path = Path(self.storage_dir).resolve()
        path.mkdir(parents=True, exist_ok=True)
        return path


settings = Settings()

