from typing import Any

from pydantic import ConfigDict, field_validator, EmailStr
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_URL: str
    SECRET_KEY_JWT: str
    ALGORITHM: str
    PG_DB: str
    PG_USER: str
    PG_PASSWORD: str
    PG_PORT: int
    PG_DOMAIN: str
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    REDIS_HOST: str = 'redis-10936.c250.eu-central-1-1.ec2.cloud.redislabs.com'
    REDIS_PORT: int = 10936
    REDIS_PASSWORD: str = 'g0oqZcAN5vbLazSoBCuAStlLHMB0ZzjXs'
    CLD_NAME: str
    CLD_API_KEY: str
    CLD_API_SECRET: str


    @field_validator("ALGORITHM")
    @classmethod
    def validate_algorithm(cls, v: Any):
        if v not in ["HS256", "HS512"]:
            raise ValueError("algorithm must be HS256 or HS512")
        return v

    model_config = ConfigDict(extra='ignore', env_file=".env", env_file_encoding="utf-8")  # noqa


config = Settings()
