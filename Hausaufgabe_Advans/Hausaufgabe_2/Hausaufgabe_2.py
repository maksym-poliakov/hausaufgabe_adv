from typing import Annotated
from pydantic import BaseModel, Field, EmailStr,  StrictStr, model_validator
# Разработать систему регистрации пользователя, используя Pydantic для валидации входных данных,
# обработки вложенных структур и сериализации. Система должна обрабатывать данные в формате JSON.
# Задачи:
# Создать классы моделей данных с помощью Pydantic для пользователя и его адреса.
# Реализовать функцию, которая принимает JSON строку, десериализует её в объекты Pydantic, валидирует данные,
# и в случае успеха сериализует объект обратно в JSON и возвращает его.
# Добавить кастомный валидатор для проверки соответствия возраста и статуса занятости пользователя.
# Написать несколько примеров JSON строк для проверки различных сценариев валидации: успешные регистрации и случаи,
# когда валидация не проходит (например возраст не соответствует статусу занятости).
# Модели:
# Address: Должен содержать следующие поля:
# city: строка, минимум 2 символа.
# street: строка, минимум 3 символа.
# house_number: число, должно быть положительным.
# User: Должен содержать следующие поля:
# name: строка, должна быть только из букв, минимум 2 символа.
# age: число, должно быть между 0 и 120.
# email: строка, должна соответствовать формату email.
# is_employed: булево значение, статус занятости пользователя.
# address: вложенная модель адреса.
# Валидация:
# Проверка, что если пользователь указывает, что он занят (is_employed = true), его возраст должен быть от 18 до 65 лет.
# # Пример JSON данных для регистрации пользователя
json_input = """{
    "name": "John Doe",
    "age": 70,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }
}"""
# отрицательный номер дома
json_input1 = """{
    "name": "John Doee",
    "age": 70,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": -10
    }
}"""
# не верный email
json_input2 = """{
    "name": "John Doee",
    "age": 70,
    "email": "john.doeexample.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 10
    }
}"""
class Address(BaseModel) :
    city: str = Field(min_length=2)
    street: str = Field(min_length=3)
    house_number: int = Field(gt=0)

class User(BaseModel) :
    name: Annotated[StrictStr, Field(min_length=2)]
    age: int = Field(gt=0,lt=120)
    email: EmailStr
    is_employed: bool
    address: Address

    @model_validator(mode='after')
    def age_validator(self):
        if self.is_employed is not None:
            if self.is_employed and self.age < 18:
                raise ValueError ("Работающий пользователь должен быть не младше 18 лет")
        return self.age

try:
    user = User.model_validate_json(json_input1)
except ValueError as e :
    print(e)