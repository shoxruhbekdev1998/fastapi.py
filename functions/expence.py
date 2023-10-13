from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from functions.balance import balance_sub
from models.expence import Expence
from routes.auth import get_password_hash
from utils.pagination import pagination


def all_expences(search, id, from_date, end_date, page, limit, db, status):
    expences = db.query(Expence).filter(Expence.id >= 0)
    if search:
        expences = expences.filter(Expence.money.like(search) |
                                   Expence.type.like(search) |
                                   Expence.comment.like(search))
    if id:
        expences = expences.filter(Expence.id == id)

    if from_date and end_date:
        expences = expences.filter(Expence.date >= from_date, Expence.date <= end_date)

    if status == True:
        expences = expences.filter(Expence.status == status)

    elif status == False:
        expences = expences.filter(Expence.status == status)

    else:
        expences = expences.filter(Expence.id >= 0)

    return pagination(form=expences, page=page, limit=limit)


def add_expences(form, db):
    new_expences = Expence(
        money=form.money,
        type=form.type,
        comment=form.comment,
    )
    db.add(new_expences)
    db.commit()
    db.refresh(new_expences)
    balance_sub(type=form.type,money=form.money,db=db)

    return {"data": "User add base"}


def update_expences(id, form, db):
    if one_expence(id=form.id, db=db) is None:
        raise HTTPException(status_code=400, detail="Bunday raqamli expence yo'q")
    db.query(Expence).filter(Expence.id == id).update({
        Expence.money: form.money,
        Expence.type: form.type,
        Expence.comment: form.comment,
        Expence.status: form.status,

    })
    db.commit()


def one_expence(id, db):
    return db.query(Expence).filter(Expence.id == id).first()


def delete_expences(id, db):
    db.query(Expence).filter(Expence.id == id).update({
        Expence.status: False
    })

    db.commit()
    return {"data": "Malumot o'chirildi"}