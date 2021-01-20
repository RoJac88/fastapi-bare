from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = 'My App'
    secret_key: str
    database_uri: str
    test_db_uri: str

    class Config:
        env_file = '.env'


@lru_cache()
def get_settings():
    return Settings()
