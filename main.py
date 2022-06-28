import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import Publisher, Shop, Book, Stock, Sale, create_table

user_name = input('Enter login : ')
password = input('Enter password: ')
database_name = input('Name database: ')


def create_dsn(name, user_password, db_name, driver='postgresql'):
    DSN = f'{driver}://{name}:{user_password}@localhost:5432/{db_name}'
    return DSN


engine = sqlalchemy.create_engine(create_dsn(user_name, password, database_name))
create_table(engine)

# Сессия
Session = sessionmaker(bind=engine)
session = Session()


# Загрузка тестовых данных
def init_test_data(session):
    with open('fixtures/tests_data.json', 'r') as fd:
        data = json.load(fd)

    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()


init_test_data(session)


# Поиск издателя
def search_publisher(value):
    if value.isdigit():
        query = session.query(Publisher).filter(Publisher.id == value)
    else:
        query = session.query(Publisher).filter(Publisher.name == value)

    for s in query.all():
        print(f'{s.id}: {s.name}')


search_publisher(value=input('Имя автора или его идентификатор: '))

# Закрытие сессии
session.close()
