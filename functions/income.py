from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from functions.balance import balance_adding
from models.income import Income
from functions.orders import one_order

from routes.auth import get_password_hash
from utils.pagination import pagination


def all_incomes(search, id,order_id, from_date, end_date, page, limit, db, status):
    incomes = db.query(Income).filter(Income.id >= 0)
    if search:
        incomes = incomes.filter(Income.money.like(search) |
                                   Income.type.like(search) )
    if id:
        incomes = incomes.filter(Income.id == id)

    if order_id:
        incomes = incomes.filter(Income.order_id == order_id)

    if from_date and end_date:
        incomes = incomes.filter(Income.date >= from_date, Income.date <= end_date)

    if status == True:
        incomes = incomes.filter(Income.status == status)

    elif status == False:
        incomes = incomes.filter(Income.status == status)

    else:
        incomes = incomes.filter(Income.id >= 0)

    return pagination(form=incomes, page=page, limit=limit)


def add_incomes(form, db):

    if one_order(id=form.order_id,db=db) is None:
        raise HTTPException(status_code=400, detail="Bunday raqamli order mavjud emas !")

    new_incomes = Income(
        money=form.money,
        type=form.type,
        order_id=form.order_id,
    )
    db.add(new_incomes)
    db.commit()
    db.refresh(new_incomes)
    balance_adding(type=form.type,money=form.money,db=db)

    return {"data": "User add base"}


def update_incomes(id, form, db):
    if one_income(id=form.id, db=db) is None:
        raise HTTPException(status_code=400, detail="Bunday raqamli income yo'q")
    if one_order(id=form.order_id,db=db) is None:
        raise HTTPException(status_code=400, detail="Bunday raqamli order mavjud emas !")
    db.query(Income).filter(Income.id == id).update({
        Income.money: form.money,
        Income.type: form.type,
        Income.order_id: form.order_id,
        Income.status: form.status,

    })
    db.commit()


def one_income(id, db):
    return db.query(Income).filter(Income.id == id).first()


def delete_incomes(id, db):
    db.query(Income).filter(Income.id == id).update({
        Income.status: False
    })

    db.commit()
    return {"data": "Malumot o'chirildi"}