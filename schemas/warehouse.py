from pydantic import BaseModel
from typing import Optional

class WarehouseBase(BaseModel):
    name:str
    measure:str
    real_price:float
    trade_price:float
    number:int
    user_id:int


class WarehouseCreate(WarehouseBase):
    pass

class WarehouseUpdate(WarehouseBase):
    id:int
    status:bool