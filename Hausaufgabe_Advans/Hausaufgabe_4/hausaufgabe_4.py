from sqlalchemy import Column, Integer, String, DECIMAL, BOOLEAN, ForeignKey, create_engine, func
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

#Шапка для отделения заданий
def print_task_number(task_numb:int) -> None:

    text = (f'\033[35m+++++++++++++++++++++++++++++++++++\n'
            f'+++++++++++ Задание № {task_numb} +++++++++++\n'
            f'+++++++++++++++++++++++++++++++++++\033[0m')
    print(text)
    return None

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

# Задача 1: Наполнение данными
# Добавьте в базу данных следующие категории и продукты
# Добавление категорий: Добавьте в таблицу categories следующие категории:
# Название: "Электроника", Описание: "Гаджеты и устройства."
# Название: "Книги", Описание: "Печатные книги и электронные книги."
# Название: "Одежда", Описание: "Одежда для мужчин и женщин."
# Добавление продуктов: Добавьте в таблицу products следующие продукты, убедившись,
# что каждый продукт связан с соответствующей категорией:
# Название: "Смартфон", Цена: 299.99, Наличие на складе: True, Категория: Электроника
# Название: "Ноутбук", Цена: 499.99, Наличие на складе: True, Категория: Электроника
# Название: "Научно-фантастический роман", Цена: 15.99, Наличие на складе: True, Категория: Книги
# Название: "Джинсы", Цена: 40.50, Наличие на складе: True, Категория: Одежда
# Название: "Футболка", Цена: 20.00, Наличие на складе: True, Категория: Одежда

electronics = Category(name="Электроника", description="Гаджеты и устройства.")
books = Category(name="Книги", description="Печатные книги и электронные книги.")
clothes = Category(name="Одежда", description="Одежда для мужчин и женщин.")

session.add_all([electronics,books,clothes])

session.commit()

session.add_all([Product(name="Смартфон",price=299.99,in_stock=True,category_id = electronics.id),
                 Product(name="Ноутбук",price=499.99,in_stock=True,category_id = electronics.id),
                 Product(name="Научно-фантастический роман",price=15.99,in_stock=True,category_id=books.id),
                 Product(name="Джинсы",price=40.50,in_stock=True,category_id=clothes.id),
                 Product(name="Футболка",price=20.00,in_stock=True,category_id=clothes.id)])


session.commit()

# Задача 2: Чтение данных
# Извлеките все записи из таблицы categories. Для каждой категории извлеките и выведите все связанные с ней продукты,
# включая их названия и цены.
categories = session.query(Category).group_by(Category.name).all()

print_task_number(2)
for category in categories:
    print(f"\nКатегория: {category.name} ({category.description})")
    print("Продукты:")
    for product in category.products:
        print(f"  - {product.name} Цена: ${product.price:.2f}")

# Задача 3: Обновление данных
# Найдите в таблице products первый продукт с названием "Смартфон". Замените цену этого продукта на 349.99.
smartphone = session.query(Product).filter(Product.name=="Смартфон").first()

if smartphone :
    smartphone.price = 349.99
    session.commit()

# Задача 4: Агрегация и группировка
# Используя агрегирующие функции и группировку, подсчитайте общее количество продуктов в каждой категории.
print_task_number(4)
group_product = (session.query(Category.name,func.count(Product.id).label("count_product"))
                 .join(Product).group_by(Category.name).all())

for gr_prod in group_product :
    print(gr_prod.name,":",gr_prod.count_product)

# Задача 5: Группировка с фильтрацией
# Отфильтруйте и выведите только те категории, в которых более одного продукта.
print_task_number(5)
group_product = (session.query(Category.name,func.count(Product.id).label("count_product"))
                 .join(Product).group_by(Category.name).having(func.count(Product.id) > 1))

for gr_prod in group_product :
    print(gr_prod.name,":",gr_prod.count_product)

