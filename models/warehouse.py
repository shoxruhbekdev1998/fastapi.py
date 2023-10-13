import datetime

from sqlalchemy import Column, Integer, String, Boolean,Float,Text,ForeignKey,Date,DateTime,func

from sqlalchemy.orm import relationship

from db import Base


class Warehouse(Base):
    __tablename__ = "Warehouse"
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(30), nullable=True)
    measure = Column(String(30), nullable=True)
    real_price = Column(Float, nullable = True)
    trade_price = Column(Float, nullable = True)
    number = Column(Integer, primary_key=False)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    status = Column(Boolean, nullable = True ,default=True)
    date = Column(Date(),nullable = True,default=func.now())


    users = relationship("Users", back_populates="warehouse")


