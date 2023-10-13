from fastapi import APIRouter,Depends,HTTPException
from pydantic.datetime_parse import date

from db import Base,engine,get_db

from sqlalchemy.orm import Session

from routes.auth import get_current_active_user
from schemas.users import UserCurrent

Base.metadata.create_all(bind=engine)
from functions.income import add_incomes, all_incomes, update_incomes, delete_incomes
from schemas.income import *

router_income = APIRouter()

@router_income.post('/add')
def add_income(form:IncomeCreate,db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)):

    if add_incomes(form=form,db=db):
        raise HTTPException(status_code=200, detail="Amaliyot muvofaqqiyatli bajarildi")


@router_income.get('/',status_code=200)
def get_income(search:str=None,id:int=0,order_id:int=0,from_date:str=None,end_date:str=None,page:int=1,limit:int=5,status:bool=None,db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)):

        return all_incomes(db=db,status=status,search=search,id=id,order_id=order_id,from_date=from_date,end_date=end_date,page=page,limit=limit)



@router_income.put('/update',)
def update_income(form:IncomeUpdate,db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)):

    if update_incomes(id=form.id,form=form,db=db):
        raise HTTPException(status_code=200, detail="Amaliyot muvofaqqiyatli bajarildi")

@router_income.delete('/del',)
def delete_income(id:int,db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)):
    return delete_incomes(id=id,db=db)
