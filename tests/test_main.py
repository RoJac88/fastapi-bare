import pytest
from fastapi import Depends
from httpx import AsyncClient
from api.database import get_db
from api.main import app


@pytest.mark.asyncio
async def test_index():
    async with AsyncClient(app=app, base_url='http://127.0.0.1/') as client:
        response = await client.get('/')
    assert response.status_code == 200
    assert response.json() == {
        'secret': 'shhhhh',
        'ps': 'don\'t tell anyone',
    }


@pytest.mark.asyncio
async def test_create_account():
    async with AsyncClient(app=app, base_url='http://127.0.0.1/') as client:
        response = await client.post('/account/', json={'name': 'bobby'})
    assert response.status_code == 200
    assert response.json() == {
        'uid': 1,
        'name': 'bobby',
    }


@pytest.mark.asyncio
async def test_read_accont():
    async with AsyncClient(app=app, base_url='http://127.0.0.1/') as client:
        await client.post('/account/', json={'name': 'fischer'})
        response = await client.get('/account/1/')
    assert response.status_code == 200
    assert response.json() == {
        'uid': 1,
        'name': 'fischer',
    }


@pytest.mark.asyncio
async def test_read_spending(database=Depends(get_db)):
    async with AsyncClient(app=app, base_url='http://127.0.0.1/') as client:
        response = await client.get('/budget/')
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_spending(database=Depends(get_db)):
    newline = {
        'value': 500.50,
        'transaction_date': '2020-01-01',
        'account_id': 1,
    }
    async with AsyncClient(app=app, base_url='http://127.0.0.1/') as client:
        await client.post('/account/', json={'name': 'user'})
        response = await client.post('/budget/', json=newline)
    assert response.status_code == 200
    assert response.json() == {
        'value': 500.50,
        'transaction_date': '2020-01-01',
        'txid': 1,
        'credit': False, 
        'account': {
            'uid': 1,
            'name': 'user',
        }
    }
