from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import sessionmaker

from properties import Base


class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)
    role = Column(String)

class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    second_name = Column(String)
    role = Column(Integer, ForeignKey(Role.id))
    login = Column(String)
    password = Column(String)
    uvolen = Column(Boolean)

class Smena(Base):
    __tablename__ = 'smena'
    id = Column(Integer, primary_key=True)
    time =  Column(DateTime)

class OrderStatus(Base):
    __tablename__ = 'order_status'
    id = Column(Integer, primary_key=True)
    status = Column(String)
    
class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    smena = Column(Integer, ForeignKey(Smena.id))
    table = Column(Integer)
    countClient = Column(Integer)
    time =  Column(DateTime)
    status = Column(Integer, ForeignKey(OrderStatus.id))
    drinks  = Column(String)
    dishes = Column(String)


class EmployeeAndSmena(Base):
    __tablename__ = 'employee_and_smena'
    id = Column(Integer, primary_key=True)
    employee = Column(Integer, ForeignKey(Employee.id))
    smena = Column(Integer, ForeignKey(Smena.id))
