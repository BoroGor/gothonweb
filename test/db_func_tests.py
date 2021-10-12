from nose.tools import *
import db_func as fn
from pathlib import Path
import sqlite3
from app import app


# задаём адрес для создания тестовой БД
DATABASE_abs = Path(app.root_path, 'static', 'test.db')
# добавим в конфигурацию приложения адрес БД
app.config.update(dict(DATABASE = DATABASE_abs))

# проверяем функцию подключения к БД
def test_connect_db():
    # функция возвращает объект класса "connect", адрес
    # берётся из конфигурации
    conn = fn.connect_db(app.config['DATABASE'])
    # проверим, создался ли файл
    eq_(Path(DATABASE_abs).exists(), True)
    # опишем функцию определения статуса соединения с БД
    def status(connection):
        # пробуем создать объект "курсора"
        try:
            # если объект создался, то
            connection.cursor()
            # присваиваем статус соединению "открыто"
            return 'open'
            # если же курсор не удалось создать, то
        except:
            # присваиваем статус "закрыто"
            return 'close'
    # проверяем, создано ли подключение и активно ли он
    eq_(status(conn), 'open')
    # закроем подключение
    conn.close()
    # проверим статус соединения
    eq_(status(conn), 'close')

# проверяем функцию создания и автоматической конфигурации БД
def test_create_db():
    # вызываем функцию, которая создаёт тестовую таблицу в тестовой БД
    fn.create_db(app.config['DATABASE'])
    # создаём блок вводных данных (имя, пароль, попытки, дата регистр)
    data =('First_User', 'firstpswrd', 0, '12-10-2021')
    # создаём активное подключение к БД
    cn = fn.connect_db(app.config['DATABASE'])
        
