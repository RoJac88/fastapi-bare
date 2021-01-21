from .database import metadata
import sqlalchemy as sa
import datetime


accounts = sa.Table(
    'accounts', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String, unique=True, nullable=False),
)

lines = sa.Table(
    'lines', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('value', sa.Float, nullable=False),
    sa.Column('credit', sa.Boolean, default=False, nullable=False),
    sa.Column('transaction_date', sa.Date, default=datetime.date.today(), nullable=False),
    sa.Column('account_id', sa.Integer, sa.ForeignKey('accounts.id'), nullable=False),
)