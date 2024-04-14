from typing import List
from sqlalchemy.orm import sessionmaker
from properties import engine
from models import Employee, Order, Role, Smena, EmployeeAndSmena
from sqlalchemy import func, and_, desc, any_
from sqlalchemy.sql import text
from datetime import datetime


Session = sessionmaker(bind=engine)
session = Session()

def changeStatusByOrderIdAndStatusId(orderId, statusId):
    order = session.query(Order).filter(Order.id == orderId).first()
    order.status = statusId
    session.commit()

def makeAuth(login, password):
    return session.query(Employee).filter(
        and_(Employee.login == login, Employee.password == password)).first()

def getRoleById(id):
    return session.query(Role).filter(Role.id == id).first()

def getLastSmena(employee: Employee):
    return session.execute(
        text(f"""
            select
            smena.id
            from
            smena
            join employee_and_smena on smena.id = employee_and_smena.smena
            group by smena.id
            having
            {employee.id} = ANY(array_agg(employee_and_smena.employee))
            order by smena.time DESC limit 1;
        """)
    ).first()
    
def getOrderById(id):
    return session.query(Order).filter(Order.id == id).first()

def getSmenaDataAll():
    return session.execute(
        text("""
            select
            smena.id,
            smena.time,
            array_agg(employee.id) as employees_ids,
            array_agg(employee.name) as employees_names,
            array_agg(employee.second_name) as employees_second_names,
            array_agg(role.role) as employees_roles
            from
            employee 
            join employee_and_smena on employee.id = employee_and_smena.employee
            join smena on employee_and_smena.smena = smena.id
            join role on role.id = employee.role
            group by smena.id
        """)
    ).all()

def getOrdersDataAll(limit, employee: Employee):
    if (employee.role == 1):
        query = text(f"""
            select
            smena.id,
            smena.time,
            array_agg(public.order.id) as orders_ids,
            array_agg(public.order.table) as orders_tables,
            array_agg(public.order."countClient") as orders_countsClients,
            array_agg(public.order.time) as orders_times,
            array_agg(public.order.drinks) as orders_drinks,
            array_agg(public.order.dishes) as orders_dishes,
            array_agg(order_status.status) as orders_statuses
            from
            public.order
            join smena on public.order.smena = smena.id
            join order_status on public.order.status = order_status.id
            group by smena.id, smena.time
            order by smena.time DESC limit {limit};
        """)
    else:
        query = text(f"""
            select
            smena.id,
            smena.time,
            array_agg(public.order.id) as orders_ids,
            array_agg(public.order.table) as orders_tables,
            array_agg(public.order."countClient") as orders_countsClients,
            array_agg(public.order.time) as orders_times,
            array_agg(public.order.drinks) as orders_drinks,
            array_agg(public.order.dishes) as orders_dishes,
            array_agg(order_status.status) as orders_statuses
            from
            public.order
            join smena on public.order.smena = smena.id
            join order_status on public.order.status = order_status.id
            join employee_and_smena on smena.id = employee_and_smena.smena
            
            group by smena.id, smena.time, employee_and_smena.employee
            having
            {employee.id} = ANY(array_agg(employee_and_smena.employee))
            order by smena.time DESC limit {limit};
        """)

    return session.execute(
        query
    ).all()

def getEmployees():
    return session.execute(
        text("""
            select
            employee.id,
            employee.name,
            employee.second_name,
            role.role
            from employee join role on employee.role = role.id
            where employee.uvolen = false
        """)
    ).all()

def deleteEmployeeById(id):
    employee = session.query(Employee).filter(Employee.id == id).first()
    employee.uvolen = True
    session.commit()
def createSmena(employeesIds: List[int]):
    smena = Smena(time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    
    session.add(smena[0])
    session.commit()
    for employeeId in employeesIds:
        session.add(
            EmployeeAndSmena(
                smena=smena[0].id,
                employee=employeeId,
            ),
        )
    session.commit()

def createEmployee(name, secondName, role, login, password):
    employee = Employee(
        name=name,
        second_name=secondName,
        role=role,
        login=login,
        password=password,
        uvolen=False,
    )
    session.add(employee)
    session.commit()

def createOrder(table, countClients, drinks, dishes, smena_id):
    order = Order(
        smena = smena_id,
        table = table,
        countClient = countClients,
        time =  datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        status = 1,
        drinks  = drinks,
        dishes = dishes,
    )
    session.add(order)
    session.commit()
    