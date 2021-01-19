from fastapi import FastAPI, Depends
from .database import database, engine, metadata
from . import config


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
        'ps': 'don\'t tell anyone'
    }
