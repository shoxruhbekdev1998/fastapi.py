from fastapi import APIRouter,Depends,HTTPException
from pydantic.datetime_parse import date

from db import Base,engine,get_db

from sqlalchemy.orm import Session

from routes.auth import get_current_active_user
from schemas.users import UserCurrent

Base.metadata.create_all(bind=engine)
from functions.expence import add_expences, all_expences, update_expences, delete_expences
from schemas.expence import *

router_expence = APIRouter()

@router_expence.post('/add')
def add_expence(form:ExpenceCreate,db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)):

    if add_expences(form=form,db=db):
        raise HTTPException(status_code=200, detail="Amaliyot muvofaqqiyatli bajarildi")


@router_expence.get('/',status_code=200)
def get_expence(search:str=None,id:int=0,from_date:str=None,end_date:str=None,page:int=1,limit:int=5,status:bool=None,db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)):

        return all_expences(db=db,status=status,search=search,id=id,from_date=from_date,end_date=end_date,page=page,limit=limit)



@router_expence.put('/update',)
def update_expence(form:ExpenceUpdate,db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)):

    if update_expences(id=form.id,form=form,db=db):
        raise HTTPException(status_code=200, detail="Amaliyot muvofaqqiyatli bajarildi")

@router_expence.delete('/del',)
def delete_expence(id:int,db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)):
    return delete_expences(id=id,db=db)
