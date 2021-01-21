from typing import List
from fastapi import FastAPI, Depends
from . import config
from .database import database, engine, metadata
from .schemas import BudgetLine, BudgetLineOut
from .models import lines

metadata.create_all(engine)
app = FastAPI()


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


@app.get('/')
async def index(conf: config.Settings = Depends(config.get_settings)):
    return {
        'secret': conf.secret_key,
        'ps': 'don\'t tell anyone',
    }


@app.post('/budget/', response_model=BudgetLineOut)
async def create_spending(line: BudgetLine):
    query = lines.insert().values(**line.dict())
    last_record_id = await database.execute(query)
    return {'id': last_record_id, **line.dict()}


@app.get('/budget/', response_model=List[BudgetLineOut])
async def read_budget():
    query = lines.select()
    results = await database.execute(query)
    return results
