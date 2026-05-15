from pathlib import Path
from typing import List
from urllib.parse import urlsplit, urlunsplit

from pydantic import model_validator
from pydantic_settings import BaseSettings

ENV_FILE = Path(__file__).resolve().parents[2] / ".env"

CANONICAL_DATABASE_HOST = "khafeefa_database"
CANONICAL_DATABASE_USER = "getkhafeefa"
CANONICAL_DATABASE_PASSWORD = "getkhafeefa"


def normalize_database_url(url: str, host: str, user: str, password: str) -> str:
    parts = urlsplit(url)
    hostname = parts.hostname or host or CANONICAL_DATABASE_HOST

    if hostname in {"localhost", "127.0.0.1", "::1", "getkhafeefa_database", "khafeefa_database"}:
        hostname = CANONICAL_DATABASE_HOST

    # EasyPanel may keep stale DATABASE_URL/DATABASE_USER values after a redeploy.
    # Force the credentials that match the initialized PostgreSQL role.
    username = CANONICAL_DATABASE_USER
    current_password = CANONICAL_DATABASE_PASSWORD

    auth = username
    if current_password:
        auth = f"{auth}:{current_password}"
    if auth:
        auth = f"{auth}@"

    port = f":{parts.port}" if parts.port else ""
    return urlunsplit(parts._replace(netloc=f"{auth}{hostname}{port}"))


class Settings(BaseSettings):
    ENVIRONMENT: str = "production"
    APP_NAME: str = "khafeefa-api"
    API_BASE_URL: str = "https://api.getkhafeefa.shop"
    FRONTEND_ORIGIN: str = "https://getkhafeefa.shop"
    CORS_ORIGINS: str = "https://getkhafeefa.shop"
    
    DATABASE_URL: str = "postgres://getkhafeefa:getkhafeefa@khafeefa_database:5432/getkhafeefa?sslmode=disable"
    DATABASE_HOST: str = CANONICAL_DATABASE_HOST
    DATABASE_USER: str = CANONICAL_DATABASE_USER
    DATABASE_PASSWORD: str = CANONICAL_DATABASE_PASSWORD
    RUN_MIGRATIONS_ON_START: bool = True
    
    ORDER_WEBHOOK_URL: str = ""
    ORDER_WEBHOOK_SECRET: str = ""
    
    MAXMIND_ACCOUNT_ID: str = ""
    MAXMIND_LICENSE_KEY: str = ""
    MAXMIND_MINFRAUD_ENDPOINT: str = "https://minfraud.maxmind.com/minfraud/v2.0/insights"
    MAXMIND_MAX_RISK_SCORE: int = 15
    MAXMIND_ALLOW_TEST_PHONES: str = "055000000"
    ALLOW_NON_KUWAIT_IPS: bool = False
    FRAUD_API_FAILURE_MODE: str = "allow"
    
    META_PIXEL_ID: str = ""
    META_ACCESS_TOKEN: str = ""
    META_TEST_EVENT_CODE: str = ""
    
    TIKTOK_PIXEL_CODE: str = ""
    TIKTOK_ACCESS_TOKEN: str = ""
    TIKTOK_TEST_EVENT_CODE: str = ""
    
    SNAP_PIXEL_ID: str = ""
    SNAP_ACCESS_TOKEN: str = ""
    SNAP_TEST_EVENT_CODE: str = ""
    
    WHATSAPP_SUPPORT_NUMBER: str = ""
    LOG_LEVEL: str = "INFO"

    @property
    def test_phones_list(self) -> List[str]:
        return [p.strip() for p in self.MAXMIND_ALLOW_TEST_PHONES.split(",") if p.strip()]

    @model_validator(mode="after")
    def normalize_database_settings(self) -> "Settings":
        self.DATABASE_HOST = CANONICAL_DATABASE_HOST
        self.DATABASE_USER = CANONICAL_DATABASE_USER
        self.DATABASE_PASSWORD = CANONICAL_DATABASE_PASSWORD
        self.DATABASE_URL = normalize_database_url(
            self.DATABASE_URL,
            self.DATABASE_HOST,
            self.DATABASE_USER,
            self.DATABASE_PASSWORD,
        )
        return self

    class Config:
        env_file = ENV_FILE

settings = Settings()
