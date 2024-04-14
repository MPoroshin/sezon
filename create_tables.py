from properties import Base, engine
from models import OrderStatus, Role, Employee
from sqlalchemy.orm import sessionmaker

Base.metadata.create_all(engine)

"""Session = sessionmaker(bind=engine)
session = Session()
session.add_all(
    [
        OrderStatus(status='Принят'),
        OrderStatus(status='Оплачен'),
        OrderStatus(status='Готовится'),
        OrderStatus(status='Готов'),
        Role(role='Администратор'),
        Role(role='Официант'),
        Role(role='Повар'),
        

    ]
)
roleAdminId = session.query(Role).filter(Role.role == 'Администратор').first().id,
session.add(
    Employee(
        name='Михаил',
        second_name='Порошин',
        role=roleAdminId,
        login='admin',
        password='admin',
        uvolen=False,
    ),
)

session.commit()"""