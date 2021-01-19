import databases
import sqlalchemy as sa
from .config import get_settings

database = databases.Database(get_settings().database_uri)

metadata = sa.MetaData()

engine = sa.create_engine(get_settings().database_uri)
