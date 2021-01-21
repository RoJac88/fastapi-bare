from typing import Optional
from pydantic import BaseModel
import datetime


class Account(BaseModel):
    name: str


class AccountOut(Account):
    uid: int


class BudgetLine(BaseModel):
    value: float
    credit: Optional[bool] = False
    transaction_date: datetime.date


class BudgetLineIn(BudgetLine):
    account_id: int


class BudgetLineOut(BudgetLine):
    txid: int
    account: AccountOut
