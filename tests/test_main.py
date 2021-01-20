import pytest
from httpx import AsyncClient
from api.config import get_settings
import databases
from api.main import app


@pytest.fixture
async def database():
    uri = get_settings().test_db_uri
    db = databases.Database(uri)
    await db.connect()
    yield db
    await db.disconnect()


@pytest.mark.asyncio
async def test_index(database):
    async with AsyncClient(app=app, base_url='http://127.0.0.1/') as client:
        response = await client.get('/')
    assert response.status_code == 200
    assert response.json() == {
        'secret': 'shhhhh',
        'ps': 'don\'t tell anyone'
    }
