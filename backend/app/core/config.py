from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    redis_url: str
    s3_endpoint: str
    s3_access_key: str
    s3_secret_key: str
    s3_bucket_name: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60
    gstn_api_key: str
    gstn_api_base_url: str
    gstn_cache_ttl: int = 86400
    llm_api_key: str = ""
    app_env: str = "local"
    log_level: str = "INFO"
    celery_result_db: int = 1
    progress_ttl_seconds: int = 3600
    gstn_max_concurrency: int = 200
    max_upload_size_bytes: int = 50 * 1024 * 1024
    batch_chunk_size: int = 1000
    gstn_timeout_seconds: int = 10
    refresh_hsn_stale_days: int = 45
    access_token_subject: str = "access"
    default_page_size: int = 100
    max_page_size: int = 1000
    allowed_file_extensions: tuple[str, ...] = Field(default=(".csv", ".xlsx", ".xls"))

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
