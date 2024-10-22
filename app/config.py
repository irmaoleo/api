# app/config.py
from pydantic_settings import BaseSettings

class MongoSettings(BaseSettings):
    mongodb_uri: str
    mongodb_name: str

    class Config:
        env_file = ".env"

mongoSettings = MongoSettings()
