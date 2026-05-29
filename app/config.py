from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # load env variables here

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
