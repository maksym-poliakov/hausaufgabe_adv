from app.models import db
# Создание модели Category:
# Создайте новую модель Category с использованием SQLAlchemy в модуле models.
# Модель должна содержать следующие поля:
# id: первичный ключ, целое число, авто-инкремент.
# name: строка, название категории, не должно быть пустым.
# Модель Question должна быть обновлена, чтобы включить ссылку на Category через внешний ключ.

class Category(db.Model):

    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=True)  # Поле не должно быть пустым
    questions = db.relationship("Question", back_populates="category", lazy=True)  # Обратная связь с Question

    def __repr__(self):
        return f'Category: {self.name}'