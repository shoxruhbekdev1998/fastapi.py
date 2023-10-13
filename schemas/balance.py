from pydantic import BaseModel
from typing import Optional

class BalanceBase(BaseModel):
    money:int
    type:str




class BalanceCreate(BalanceBase):
    pass

class BalanceUpdate(BalanceBase):
    id:int
    status:bool