from pydantic import BaseModel
from typing import Optional


class IncomeBase(BaseModel):
    money:int
    type: str
    order_id:int



class IncomeCreate(IncomeBase):
    pass


class IncomeUpdate(IncomeBase):
    id: int
    status: bool