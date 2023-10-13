from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from functions.warehouse import  warehousen_adding
from models.products import Products
from routes.auth import get_password_hash
from utils.pagination import pagination


def all_products(search,id,from_date,end_date,page,limit,db,status):
    # if status==True:
    #     status_filter = Products.status==status
    # elif status==False:
    #     status_filter =Products.status==status
    # else:
    #     status_filter = Products.id>=0
    #
    # products= db.query(Products).options(joinedload(Products.trade)).filter(status_filter).all()
    # return products

    products = db.query(Products).filter(Products.id >= 0)
    if search:
        products = products.filter(Products.name.like(search) |
                                     Products.measure.like(search) |
                                     Products.model.like(search)|
                                     Products.real_price.like(search) |
                                     Products.trade_price.like(search))
    if id:

        products =products.filter(Products.id == id)

    if from_date and end_date:
        products=products.filter(Products.date>=from_date, Products.date<=end_date)


    if status == True:
     products = products.filter(Products.status==status)

    elif status == False:
     products = products.filter(Products.status==status)

    else:
        products = products.filter(Products.id>=0)

    return pagination(form=products,page=page, limit=limit)


def add_products(form,user_id,db):
    new_products=Products(
                   name=form.name,
                   measure=form.measure,
                   number= form.number,
                   model=form.model,
                   real_price=form.real_price,
                   trade_price=form.trade_price,
                   description=form.description,
                   )
    db.add(new_products)
    db.commit()
    db.refresh(new_products)
    warehousen_adding(name=form.name,measure=form.measure, number=form.number,real_price=form.real_price,trade_price=form.trade_price,user_id=user_id, db=db)

    return{"data" : "User add base"}

def update_products(id,form,db):
    if one_product(id=form.id,db=db) is None:
        raise HTTPException(status_code=400,detail="Bunday raqamli product yo'q")
    db.query(Products).filter(Products.id==id).update({
        Products.name:form.name,
        Products.measure: form.measure,
        Products.number:form.number,
        Products.model:form.model,
        Products.real_price:form.real_price,
        Products.trade_price:form.trade_price,
        Products.description:form.description,
        Products.status: form.status,

    })
    db.commit()


def one_product(id,db):
    return db.query(Products).filter(Products.id==id).first()

def delete_products(id,db):
    db.query(Products).filter(Products.id==id).update({
        Products.status:False
    })

    db.commit()
    return {"data":"Malumot o'chirildi"}