from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name:str
    measure: str
    number: int
    model:str
    real_price:float
    trade_price:float
    description:str



class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    id:int
    status:bool