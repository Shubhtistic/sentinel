from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class CommonSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class DatabaseSettings(CommonSettings):
    postgres_server: str
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_port: int

    @property
    def async_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_server}:{self.postgres_port}/{self.postgres_db}"


class RedisSettings(CommonSettings):
    redis_host: str
    redis_port: int
    redis_db: int

    @property
    def redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"


class Settings(CommonSettings):
    database: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
