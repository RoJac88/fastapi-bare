import pytest
import os
from api.config import Settings
from api import models
from api.database import metadata, engine

settings = Settings(_env_file='test.env')

@pytest.fixture(autouse=True)
def db_setup():
    metadata.create_all(engine)
    yield
    metadata.drop_all(engine)
