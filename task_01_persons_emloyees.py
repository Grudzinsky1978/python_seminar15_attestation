import sys
import random
import argparse
import csv
import logging


FORMAT = '{levelname:<10} - {asctime:<20}. В модуле "{name}" ' \
        'в строке {lineno:03d} функция "{funcName}()" ' \
        'в {created} секунд записала сообщение: {msg}'
logging.basicConfig(filename='task_01_persons_emloyees.log.', filemode='a', encoding='utf-8', format=FORMAT, style='{', level=logging.INFO)
logger = logging.getLogger(__name__)


class InvalidNameError(ValueError):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        e_name = f'Неверное имя: {self.name}. Имя должно быть не пустой строкой.'
        logger.error(msg=e_name) # Добавлены логгеры
        return e_name
    

class InvalidPositionError(ValueError):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        e_position = f'Неверная должность: {self.name}. Должность должна быть не пустой строкой.'
        logger.error(msg=e_position) # Добавлены логгеры
        return e_position


class InvalidAgeError(ValueError):
    def __init__(self, age):
        self.age = age

    def __str__(self):
        e_age = f'Неверный возраст: {self.age}. Возраст должен быть неотрицательным целым числом не более 100.'
        logger.error(msg=e_age)
        return e_age


class InvalidIdError(ValueError):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        e_id = f'Неверный ID: {self.id}. ID должен быть 6-значным неотрицательным целым числом от 100000 до 999999.'
        logger.error(msg=e_id)
        return e_id


class Person:
    def __init__(self, last_name: str, first_name: str, patronymic: str = None, age: int = None):
        if not isinstance(last_name, str) or len(last_name.strip()) == 0:
            raise InvalidNameError(last_name)
        if not isinstance(first_name, str) or len(first_name.strip()) == 0:
            raise InvalidNameError(first_name)
        if patronymic != None:
            if not isinstance(patronymic, str) or len(patronymic.strip()) == 0:
                raise InvalidNameError(patronymic)
            self.patronymic = patronymic.title()
        else:
            self.patronymic = None
        if age != None:
            if not isinstance(age, int) or age <= 0 or age > 100: # Добавлено условие: возраст не больше 100 лет
                raise InvalidAgeError(age)

        self.last_name = last_name.title()
        self.first_name = first_name.title()
        self._age = age

    def full_name(self):
        if self.patronymic == None:
            return f'{self.last_name} {self.first_name}'
        else:
            return f'{self.last_name} {self.first_name} {self.patronymic}'

    def birthday(self):
        self._age += 1

    def get_age(self):
        return self._age


class Employee(Person):
    MAX_LEVEL = 7

    def __init__(self, last_name: str, first_name: str, patronymic: str = None, position: str = None, age: int = None, id: int = None):
        super().__init__(last_name, first_name, patronymic, age)
        if id != None:
            if not isinstance(id, int) or id < 100_000 or id > 999_999:
                raise InvalidIdError(id)
            else:
                self.id = id
        else:
            id = random.randint(100000, 999999) # Добавил генерацию id в случае, если id не указан
            self.id = id
        if position != None:
            if not isinstance(position, str) or len(position.strip()) == 0:
                raise InvalidPositionError(position)
            else:
                self.position = position
        else:
            self.position = None
            

    def get_level(self):
        s = sum(list(map(int, str(self.id)))) # Изменена строка в показе решения задачи https://autotest.gb.ru/problems/121?lesson_id=449110 (Погружение в Python (семинары), Задача 3). Было: s = sum(num for num in str(self.id))
        return s % self.MAX_LEVEL
    
    def __str__(self) -> str:
        return f'{self.full_name()}, {self.position}, {self._age}, {self.id}\n'
    

def createParser ():
    """
    Парсер для командной строки
    """
    parser = argparse.ArgumentParser(
        prog = 'coolprogram',
            description = '''Программа записывает данные о сотруднике в файл employees.txt.
            Если 6-значный ID не задан, то он будет сгенерирован автоматически.
            В командной строке после вызова файла, надо ввести -p, и записать параметры в следующем порядке:
            Фамилия, имя, отчество, должность, возраст, ID.
            Обязательными являются фамилия и имя, остальные параметры можно не указывать''',
            epilog = '''(c) Vlad'''
            )
    parser.add_argument ('-p', nargs='+')
    return parser


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args()
    if namespace.p:
        list_1 = []
        for i in namespace.p:
            if i.isnumeric():
                i = int(i)
            list_1.append(i)
        e1 = Employee(*list_1)
        with open('employees.txt', 'a', encoding="utf-8") as file_a:
            file_a.write(str(e1))
    else:
        sname = input('Введите фамилию: ')
        nm = input('Введите имя: ')
        patron = input('Введите отчество, если есть: ')
        if patron == '':
            patron = 'None'
        posit = input('Введите название должности, если знаете: ')
        if posit == '':
            posit = 'None'
        ag = input('Введите возраст, если знаете: ')
        if ag.isnumeric():
            ag = int(ag)
        else:
            ag = None
        iden = input('Введите ID, если знаете: ')
        if iden.isnumeric():
            iden = int(iden)
        else:
            iden = None

        e1 = Employee(last_name=sname, first_name=nm, patronymic=patron, position=posit, age=ag, id=iden)
        with open('employees.txt', 'a', encoding="utf-8") as file_a:
            file_a.write(str(e1))
    logger.info(msg=f'Создан сотрудник {str(e1)}. Данные записаны в файл employees.txt')
    print(f'Создан сотрудник {e1}. Данные записаны в файл employees.txt')