from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from models.customers import Customers
from routes.auth import get_password_hash
from utils.pagination import pagination


def all_customers(search,id,from_date,end_date,db,page,limit,status):
    # if status==True:
    #     status_filter = Customers.status==status
    # elif status==False:
    #     status_filter =Customers.status==status
    # else:
    #     status_filter = Customers.id>=0
    # customers= db.query(Customers).options(joinedload(Customers.order)).filter(status_filter).all()
    # return customers

    customers = db.query(Customers).filter(Customers.id>=0)
    if search:
        customers = customers.filter(Customers.name.like(search) |
                               Customers.last_name.like(search) |
                               Customers.address.like(search) |
                               Customers.number.like(search))
    if id:
        customers = customers.filter(Customers.id==id)

    if status == True:
     customers = customers.filter(Customers.status==status)

    if from_date and end_date:
        customers=customers.filter(Customers.date>=from_date, Customers.date<=end_date)


    elif status == False:
     customers = customers.filter(Customers.status==status)

    else:
        customers = customers.filter(Customers.id>=0)

    return pagination(form=customers, page=page, limit=limit)

def add_customers(form,db):
    number = db.query(Customers).filter(Customers.number == form.number).all()
    if number:
        raise HTTPException(status_code=400, detail="Bunday numberga ega customer mavjud qayta kiriting !")
    new_customer=Customers(name=form.name,
                   last_name=form.last_name,
                   number=form.number,
                   address=form.address,
                   )
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return{"data" : "User add base"}

def update_customers(id,form,db):
    if one_customer(id=form.id,db=db) is None:
        raise HTTPException(status_code=400, detail="Bunday raqamli customer mavjud emas !")
    db.query(Customers).filter(Customers.id==id).update({
        Customers.name:form.name,
        Customers.last_name:form.last_name,
        Customers.address:form.address,
        Customers.number:form.number,
        Customers.status:form.status,

    })
    db.commit()


def one_customer(id,db):
    return db.query(Customers).filter(Customers.id==id).first()

def delete_customers(id,db):
    db.query(Customers).filter(Customers.id==id).update({
        Customers.status:False
    })

    db.commit()
    return {"data":"Malumot o'chirildi"}

