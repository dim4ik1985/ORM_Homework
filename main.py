import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import Publisher, Shop, Book, Stock, Sale, create_table
from config import USER_NAME, PASSWORD, DATABASE


def create_dsn(name, user_password, db_name, driver='postgresql'):
    DSN = f'{driver}://{name}:{user_password}@localhost:5432/{db_name}'
    return DSN


engine = sqlalchemy.create_engine(create_dsn(USER_NAME, PASSWORD, DATABASE))
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
        for p in session.query(Publisher).filter(Publisher.id == value).all():
            print(p)
    else:
        for p in session.query(Publisher).filter(Publisher.name == value).all():
            print(p)


search_publisher(value=input('Имя автора или его идентификатор: '))

# Закрытие сессии
session.close()
