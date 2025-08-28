from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Db(BaseModel):
    url: PostgresDsn
    echo: bool = True
    echo_pool: bool = True
    pool_size: int = 30
    max_overflow: int = 10

    naming_convection: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class RunApp(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8082
    reload: bool = True
    app: str = "main:app"


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    question: str = "/questions"
    answer: str = "/answers"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        case_sensitive=False,
    )

    db: Db
    app: RunApp = RunApp()
    api: ApiPrefix = ApiPrefix()


settings: Settings = Settings()
