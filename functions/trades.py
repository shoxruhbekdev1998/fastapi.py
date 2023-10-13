from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from functions.warehouse import  warehousen_sub
from functions.orders import one_order
from functions.products import one_product
from models.orders import Orders

from models.products import Products
from models.trades import Trades
from routes.auth import get_password_hash
from utils.pagination import pagination


def all_trades(search,product_id,order_id,from_date,end_date,page,limit,status,db):
    # if status == True:
    #     status_filter = Trades.status == status
    # elif status == False:
    #     status_filter = Trades.status == status
    # else:
    #     status_filter = Trades.id >= 0
    #
    # trades = db.query(Trades).options(joinedload(Trades.product), joinedload(Trades.order)).filter(status_filter).all()
    # return trades

    trades = db.query(Trades).filter(Trades.id>=0)



    if search:
        trades= trades.filter(Trades.name.like(search) |
                              Trades.last_name.like(search) |
                              Trades.address.like(search) |
                              Trades.number.like(search))

    if product_id:
        trades = trades.filter(Trades.product_id==product_id)
    if order_id:
        trades = trades.filter(Trades.order_id == order_id)
    if from_date and end_date:
        trades=trades.filter(Trades.date>=from_date, Trades.date<=end_date)



    if status == True:
     trades = trades.filter(Trades.status==status)

    elif status == False:
     trades = trades.filter(Trades.status==status)

    else:
        trades = trades.filter(Trades.id>=0)

    return pagination(form=trades,page=page,limit=limit)






def add_trades(form,db):
    # order = db.query(Orders).filter(Orders.id==form.order_id).all()
    # if not order:
    #     raise HTTPException(status_code=400,detail="Bunday raqamli order mavjud emas !")
    #
    # product = db.query(Products).filter(Products.id == form.product_id).all()
    # if not product:
    #     raise HTTPException(status_code=400, detail="Bunday raqamli product mavjud emas !")

    if one_order(id=form.order_id,db=db) is None:
        raise HTTPException(status_code=400, detail="Bunday raqamli order mavjud emas !")
    if one_product(id=form.order_id, db=db) is None:
        raise HTTPException(status_code=400, detail="Bunday raqamli product mavjud emas !")

    new_trades=Trades(
                   product_id=form.product_id,
                   order_id=form.order_id,
                   name=form.name,
                   last_name=form.last_name,
                   address=form.address,
                   number=form.number,
                   measure=form.measure,
                   )
    db.add(new_trades)
    db.commit()
    db.refresh(new_trades)
    warehousen_sub(name=form.name, number=form.number, db=db)

    return{"data" : "User add base"}

def update_trades(id,form,db):
    if one_trade(id=form.id,db=db) is None:
        raise HTTPException(status_code=400,detail="Bunday id ga ega trade mavjud emas")
    if one_order(id=form.order_id,db=db) is None:
        raise HTTPException(status_code=400, detail="Bunday raqamli order mavjud emas !")
    if one_product(id=form.order_id, db=db) is None:
        raise HTTPException(status_code=400, detail="Bunday raqamli product mavjud emas !")
    db.query(Trades).filter(Trades.id==id).update({
        Trades.product_id:form.product_id,
        Trades.order_id:form.order_id,
        Trades.name: form.name,
        Trades.last_name: form.last_name,
        Trades.address: form.address,
        Trades.number: form.number,
        Trades.measure:form.measure,
        Trades.status: form.status,

    })
    db.commit()


def one_trade(id,db):
    return db.query(Trades).filter(Trades.id==id).first()

def delete_trades(id,db):
    db.query(Trades).filter(Trades.id==id).update({
        Products.status:False
    })

    db.commit()
    return {"data":"Malumot o'chirildi"}