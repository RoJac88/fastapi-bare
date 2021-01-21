from pydantic import BaseModel
import datetime

class BudgetLine(BaseModel):
    value: float
    credit: bool
    transaction_date: datetime.date
    account_id: int


class BudgetLineOut(BudgetLine):
    id: int
