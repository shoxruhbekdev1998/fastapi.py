import datetime

from sqlalchemy import Column, Integer, String, Boolean,Float,Text,ForeignKey,Date,DateTime,func

from sqlalchemy.orm import relationship

from db import Base


class Trades(Base):
    __tablename__ = "Trades"
    id = Column(Integer, primary_key=True,autoincrement=True)
    product_id = Column(Integer, ForeignKey("Products.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("Orders.id"), nullable=False)
    name = Column(String(30), nullable=True)
    last_name = Column(String(30), nullable=True)
    address = Column(String(100),nullable =True)
    number = Column(Integer, nullable=False)
    measure = Column(String(30), nullable=True)
    status = Column(Boolean, nullable=True,default=True)
    date = Column(Date(),nullable = True,default=func.now())

    product = relationship("Products", back_populates="trade")
    order = relationship("Orders", back_populates="trade")



