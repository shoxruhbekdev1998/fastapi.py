from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from functions.customers import one_customer
from models.customers import Customers
from models.orders import Orders
from routes.auth import get_password_hash
from utils.pagination import pagination


def all_orders(search,id,customers_id,from_date,end_date,page,limit,db,status):
    # if status==True:
    #     status_filter = Orders.status==status
    # elif status==False:
    #     status_filter =Orders.status==status
    # else:
    #     status_filter = Orders.id>=0
    # orders= db.query(Orders).options(joinedload(Orders.trade),joinedload(Orders.customer)).filter(status_filter).all()
    # return orders
    orders = db.query(Orders).filter(Orders.id >= 0)
    if search:
        orders = orders.filter(Orders.money.like(search) |
                                     Orders.type.like(search) |
                                     Orders.rest_money.like(search) |
                                     Orders.loan.like(search))
    if id:
       orders = orders.filter(Orders.id == id)
    if customers_id:
        orders = orders.filter(Orders.customers_id == customers_id)
    if from_date and end_date:
        orders=orders.filter(Orders.date>=from_date, Orders.date<=end_date)

    if status == True:
     orders =orders.filter(Orders.status==status)

    elif status == False:
     orders = orders.filter(Orders.status==status)

    else:
        orders = orders.filter(Orders.id>=0)

    return pagination(form=orders, page=page, limit=limit)

def one_order(id,db):
    return db.query(Orders).filter(Orders.id==id).first()


def add_orders(form,db):
    # customer = db.query(Customers).filter(Customers.id == form.customers_id).all()
    # if not customer:
    # raise HTTPException(status_code=400, detail="Bunday raqamli customer mavjud emas !")
    if one_customer(id=form.customers_id,db=db) is None:
        raise HTTPException(status_code=400, detail="Bunday raqamli customer mavjud emas !")

    new_orders=Orders(
                   customers_id=form.customers_id,
                   money=form.money,
                   type=form.type,
                   loan=form.loan,
                   rest_money=form.rest_money,
                   deadline=form.deadline,
                   )
    db.add(new_orders)
    db.commit()
    db.refresh(new_orders)

    return{"data" : "User add base"}

def update_orders(id,form,db):
    if one_order(id=form.id,db=db) is None:
        raise HTTPException(status_code=400,detail="Bunday id raqamli order mavjud emas")

    if one_customer(id=form.customers_id,db=db) is None:
        raise HTTPException(status_code=400, detail="Bunday raqamli customer mavjud emas !")

    db.query(Orders).filter(Orders.id==id).update({
        Orders.customers_id:form.customers_id,
        Orders.money:form.money,
        Orders.type:form.type,
        Orders.loan:form.loan,
        Orders.rest_money:form.rest_money,
        Orders.deadline:form.deadline,
        Orders.status: form.status,

    })
    db.commit()

def delete_orders(id,db):
    db.query(Orders).filter(Orders.id==id).update({
        Orders.status:False
    })

    db.commit()
    return {"data":"Malumot o'chirildi"}

