from api.config import get_settings

settings = get_settings()
settings.database_uri = settings.test_database_uri
