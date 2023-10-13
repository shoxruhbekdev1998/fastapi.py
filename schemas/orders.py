from datetime import date

from pydantic import BaseModel
from typing import Optional

class OrderBase(BaseModel):
    customers_id:int
    money:int
    type:str
    loan:float
    rest_money:float
    deadline:date



class OrderCreate(OrderBase):
    pass

class OrderUpdate(OrderBase):
    id:int
    status:bool