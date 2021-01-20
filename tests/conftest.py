import sqlalchemy as sa
import pytest
from api.database import metadata
from api.config import get_settings

@pytest.fixture(scope='session', autouse=True)
def setup_database():
    engine = sa.create_engine(get_settings().test_db_uri)
    metadata.create_all(engine)
    yield
    metadata.drop_all(engine)
