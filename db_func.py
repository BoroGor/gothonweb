import sqlite3
from pathlib import Path


# функция подключения к БД
def connect_db(db_adres):
    """db_adres - путь к БД типа "str". Функция возвращает объект класса
    "sqlite3.connect()".
    """
    # создаём объект класса "connect"
    conn = sqlite3.connect(db_adres)
    # возвращаем объект
    return conn

# функция создания БД и автоматическая конфигуреция,
# если раньше БД не существовало
def create_db(db_adres):
    """Функция конфигурации тестовой таблицы БД"""
    # создаём подключение и БД, если её не существовало
    db = connect_db(db_adres)
    # вызовем команду создания таблицы и необходимых столбцов
    db.cursor().executescript("""
        create table if not exists test_users (
        id integer not null primary key autoincrement,
        username text not null,
        pswrd text not null,
        min_trying integer,
        reg_date text not null);""")
    # сохраняем изменения в таблице
    db.commit()
    # закрываем соединение
    db.close()
