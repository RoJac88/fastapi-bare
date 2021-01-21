import pytest
from api import models
from api.database import metadata, engine


@pytest.fixture(autouse=True)
def db_setup():
    metadata.create_all(engine)
    yield
    metadata.drop_all(engine)
