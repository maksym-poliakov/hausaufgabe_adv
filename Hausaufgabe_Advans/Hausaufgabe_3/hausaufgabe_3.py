# Задача 1: Создайте экземпляр движка для подключения к SQLite базе данных в памяти.
# Задача 2: Создайте сессию для взаимодействия с базой данных, используя созданный движок.
# Задача 3: Определите модель продукта Product со следующими типами колонок:
# id: числовой идентификатор
# name: строка (макс. 100 символов)
# price: числовое значение с фиксированной точностью
# in_stock: логическое значение
# Задача 4: Определите связанную модель категории Category со следующими типами колонок:
# id: числовой идентификатор
# name: строка (макс. 100 символов)
# description: строка (макс. 255 символов)
# Задача 5: Установите связь между таблицами Product и Category с помощью колонки category_id.

from sqlalchemy import Column, Integer, String, DECIMAL,BOOLEAN,ForeignKey, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

engine = create_engine('sqlite:///:memory:')

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Product(Base) :
    __tablename__ = 'product'
    id = Column(Integer,primary_key=True)
    name = Column(String(100))
    price = Column(DECIMAL(10,2))
    in_stock = Column(BOOLEAN)
    category_id = Column(Integer, ForeignKey('category.id'))

    category = relationship("Category", back_populates="products")


class Category(Base) :
    __tablename__ = 'category'
    id = Column(Integer,primary_key=True)
    name = Column(String(100))
    description = Column(String(255))

    products = relationship("Product", back_populates="category")



Base.metadata.create_all(bind=engine)

category = Category(name='Auto',description='BMW')
product1 = Product(name='Car',price=120000.50,in_stock=True,category=category)

session.add(category)
session.add(product1)

session.commit()

print(session.query(Product).first().name)
print(session.query(Product).first().category.name)