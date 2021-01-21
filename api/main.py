from typing import List
from fastapi import FastAPI, Depends
from . import config
from .database import metadata, get_db
from .schemas import BudgetLineIn, BudgetLineOut, AccountOut, Account
from .models import accounts, lines

app = FastAPI()


@app.get('/')
async def index(conf: config.Settings = Depends(config.get_settings)):
    return {
        'secret': conf.secret_key,
        'ps': 'don\'t tell anyone',
    }


@app.post('/account/', response_model=AccountOut)
async def create_account(account: Account, database=Depends(get_db)):
    query = accounts.insert().values(**account.dict())
    new_id = await database.execute(query)
    return {'uid': new_id, **account.dict()}


@app.get('/account/{uid}/', response_model=AccountOut)
async def read_account(uid: int, database=Depends(get_db)):
    query = accounts.select().where(accounts.c.uid==uid)
    result = await database.fetch_one(query)
    return result


@app.post('/budget/', response_model=BudgetLineOut)
async def create_spending(line: BudgetLineIn, database=Depends(get_db)):
    query = lines.insert().values(**line.dict())
    last_record_id = await database.execute(query)
    account_query = accounts.select().where(accounts.c.uid==line.dict().get('account_id'))
    account = await database.fetch_one(account_query)
    return {'txid': last_record_id, **line.dict(), 'account': account}


@app.get('/budget/', response_model=List[BudgetLineOut])
async def read_budget(database=Depends(get_db)):
    query = lines.join(accounts).select()
    records = await database.fetch_all(query)
    res = []
    for r in records:
        data = dict(r)
        account = {'uid': r.get('account_id'), 'name': r.get('name')}
        data['account'] = account
        res.append(data)
    return res
