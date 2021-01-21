import databases
import sqlalchemy as sa
from .config import get_settings

uri = get_settings().database_uri

metadata = sa.MetaData()
engine = sa.create_engine(uri)

async def get_db():
    db = databases.Database(uri)
    await db.connect()
    try:
        yield db
    finally:
        await db.disconnect()
