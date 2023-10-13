from fastapi import APIRouter,Depends,HTTPException
from pydantic.datetime_parse import date

from db import Base,engine,get_db

from sqlalchemy.orm import Session

from routes.auth import get_current_active_user
from schemas.users import UserCurrent

Base.metadata.create_all(bind=engine)
from functions.trades import add_trades,all_trades,update_trades,delete_trades
from schemas.trades import *

router_trade = APIRouter()

@router_trade.post('/add')
def add_trade(form:TradeCreate,db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)):

    if add_trades(form=form,db=db):
        raise HTTPException(status_code=200, detail="Amaliyot muvofaqqiyatli bajarildi")


@router_trade.get('/',status_code=200)
def get_trade(search:str=None,product_id:int=0,order_id:int=0,from_date:str=None,end_date:str=None,page:int=1,limit:int=5,status:bool=None,db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)):

        return all_trades(db=db,status=status,search=search,product_id=product_id,order_id=order_id,from_date=from_date,end_date=end_date,page=page,limit=limit)



@router_trade.put('/update',)
def update_trade(form:TradeUpdate,db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)):

    if update_trades(id=form.id,form=form,db=db):
        raise HTTPException(status_code=200, detail="Amaliyot muvofaqqiyatli bajarildi")

@router_trade.delete('/del',)
def delete_trade(id:int,db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)):
    return delete_trades(id=id,db=db)