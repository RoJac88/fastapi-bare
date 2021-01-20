import databases
import sqlalchemy as sa
from .config import get_settings

db = get_settings().database_uri
database = databases.Database(db)

metadata = sa.MetaData()

engine = sa.create_engine(get_settings().database_uri)
