from pydantic_settings import BaseSettings
from pathlib import Path
from typing import List

ENV_FILE = Path(__file__).resolve().parents[2] / ".env"

class Settings(BaseSettings):
    ENVIRONMENT: str = "production"
    APP_NAME: str = "khafeefa-api"
    API_BASE_URL: str = "https://api.getkhafeefa.shop"
    FRONTEND_ORIGIN: str = "https://getkhafeefa.shop"
    CORS_ORIGINS: str = "https://getkhafeefa.shop"
    
    DATABASE_URL: str = "postgres://khafeefa:khafeefa@localhost:5432/getkhafeefa?sslmode=disable"
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

    class Config:
        env_file = ENV_FILE

settings = Settings()
