from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.balance import Balance
from routes.auth import get_password_hash
from utils.pagination import pagination


def all_balances(search,id,from_date,end_date,page,limit,db,status):

    balances = db.query(Balance).filter(Balance.id >= 0)
    if search:
        balances = balances.filter(Balance.money.like(search) |
                                     Balance.type.like(search))
    if id:

        balances =balances.filter(Balance.id == id)

    if from_date and end_date:
        balances=balances.filter(Balance.date>=from_date, Balance.date<=end_date)


    if status == True:
     balances = balances.filter(Balance.status==status)

    elif status == False:
     balances = balances.filter(Balance.status==status)

    else:
        balances = balances.filter(Balance.id>=0)

    return pagination(form=balances,page=page, limit=limit)


def add_balances(form,db):
    new_balances=Balance(
                   money=form.money,
                   type=form.type,
                   )
    db.add(new_balances)
    db.commit()
    db.refresh(new_balances)

    return{"data" : "User add base"}

def update_balances(id,form,db):
    if one_balance(id=form.id,db=db) is None:
        raise HTTPException(status_code=400,detail="Bunday raqamli balance yo'q")
    db.query(Balance).filter(Balance.id==id).update({
        Balance.money:form.money,
        Balance.type:form.type,
        Balance.status: form.status,

    })
    db.commit()


def one_balance(id,db):
    return db.query(Balance).filter(Balance.id==id).first()

def delete_balances(id,db):
    db.query(Balance).filter(Balance.id==id).update({
        Balance.status:False
    })

    db.commit()
    return {"data":"Malumot o'chirildi"}


def balance_adding(type,money,db):
    balance = db.query(Balance).filter(Balance.type==type).first()
    new_money = balance.money + money
    db.query(Balance).filter(Balance.type==type).update({
        Balance.money:new_money
    })
    db.commit()


def balance_sub(type,money,db):
    balance = db.query(Balance).filter(Balance.type==type).first()
    new_money = balance.money - money
    db.query(Balance).filter(Balance.type==type).update({
        Balance.money:new_money
    })
    db.commit()
