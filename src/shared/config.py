from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # load env variables here

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        # postgresql+asyncpg://user:password@host:port/dbname

    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        # redis://localhost:6379/0

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
