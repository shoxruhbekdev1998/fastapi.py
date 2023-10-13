from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.warehouse import Warehouse
from routes.auth import get_password_hash
from utils.pagination import pagination


def all_warehouses(search,id,from_date,end_date,page,limit,db,status):
    # if status==True:
    #     status_filter = Products.status==status
    # elif status==False:
    #     status_filter =Products.status==status
    # else:
    #     status_filter = Products.id>=0
    #
    # products= db.query(Products).options(joinedload(Products.trade)).filter(status_filter).all()
    # return products

    warehouse = db.query(Warehouse).filter(Warehouse.id >= 0)
    if search:
        warehouse = warehouse.filter(Warehouse.name.like(search) |
                                     Warehouse.measure.like(search)|
                                     Warehouse.real_price.like(search) |
                                     Warehouse.trade_price.like(search)|
                                     Warehouse.number.like(search)|
                                     Warehouse.user_id.like(search))
    if id:

        warehouse =warehouse.filter(Warehouse.id == id)

    if from_date and end_date:
        warehouse=warehouse.filter(Warehouse.date>=from_date, Warehouse.date<=end_date)


    if status == True:
     warehouse = warehouse.filter(Warehouse.status==status)

    elif status == False:
     warehouse = warehouse.filter(Warehouse.status==status)

    else:
        warehouse = warehouse.filter(Warehouse.id>=0)

    return pagination(form=warehouse,page=page, limit=limit)


def add_warehouses(form,db):
    new_warehouse=Warehouse(
                   name=form.name,
                   measure=form.measure,
                   real_price=form.real_price,
                   trade_price=form.trade_price,
                   number=form.number,
                   user_id=form.user_id
                   )
    db.add(new_warehouse)
    db.commit()
    db.refresh(new_warehouse)

    return{"data" : "User add base"}

def update_warehouses(id,form,db):
    if one_warehouses(id=form.id,db=db) is None:
        raise HTTPException(status_code=400,detail="Bunday raqamli product yo'q")
    db.query(Warehouse).filter(Warehouse.id==id).update({
        Warehouse.name:form.name,
        Warehouse.measure:form.measure,
        Warehouse.real_price:form.real_price,
        Warehouse.trade_price:form.trade_price,
        Warehouse.number:form.number,
        Warehouse.user_id: form.user_id,
        Warehouse.status: form.status,

    })
    db.commit()


def one_warehouses(id,db):
    return db.query(Warehouse).filter(Warehouse.id==id).first()

def delete_warehouses(id,db):
    db.query(Warehouse).filter(Warehouse.id==id).update({
        Warehouse.status:False
    })

    db.commit()
    return {"data":"Malumot o'chirildi"}



def warehousen_adding(name,measure,real_price,trade_price,number,user_id,db):
    product = db.query(Warehouse).filter(Warehouse.name == name).first()
    if not product:
        new_warehouse = Warehouse(
            name=name,
            measure=measure,
            real_price=real_price,
            trade_price=trade_price,
            number=number,
            user_id=user_id
        )
        db.add(new_warehouse)
        db.commit()
        db.refresh(new_warehouse)
    else:
        new_number = product.number + number
        db.query(Warehouse).filter(Warehouse.name == name).update({
        Warehouse.number:new_number
        })
        db.commit()

def warehousen_sub(name,number,db):
    product = db.query(Warehouse).filter(Warehouse.name == name).first()
    new_number = product.number - number
    db.query(Warehouse).filter(Warehouse.name == name).update({
        Warehouse.number:new_number
    })
    db.commit()