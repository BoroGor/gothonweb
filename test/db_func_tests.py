from nose.tools import *
import db_func as fn
from pathlib import Path
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
    # проверим, создался ли файл
    eq_(Path(DATABASE_abs).exists(), True)
    # проверим содержимое файла
    # создадим объект курсора, для вызова SQL-запросов
    cur = fn.connect_db(app.config['DATABASE']).cursor()
    # вернём тип объекта запроса, преобразуем в строку
    a = str(type(cur.execute('select * from users')))
    # если нет ошибки, то тип объекта совпадёт с ожидаемым
    eq_("<class 'sqlite3.Cursor'>", a)
    # закроем соединение
    cur.connection.close()

# проверка функции нахождения пользователя
def test_check_db():
    # создаём активное подключение к БД
    con = fn.connect_db(app.config['DATABASE'])
    # создаём курсор
    cur = con.cursor()
    # задаём имя искомого пользователя, дату рег-ии
    user = 'u'; rd = ''
    # пытаемся найти пользователя в пустой таблице
    eq_(fn.check(user, cur), False)
    # создаём пользователя
    cur.execute('insert into users (username, reg_date) values (?,?)', [user, rd])
    cur.execute('select * from users where username = ?', user)
    print(cur.fetchall())
    # сохраняем изменения
    con.commit()
    # пытаемся найти пользователя
    eq_(fn.check(user, cur), True)
    # чистим таблицу
    cur.execute('delete from users')
    # сохраняем изменения
    con.commit()
    # закрываем подключение
    con.close()

# проверка функции регистрации/входа пользователя
def test_login():
    # создаём блок вводных данных (имя, пароль, дата регистр)
    username = 'FU'; date = '2021-10-25'
    # создаём активное подключение к БД
    cn = fn.connect_db(app.config['DATABASE'])
    # создаём объект курсора для SQL-вызовов
    cur = cn.cursor()
    #cur.execute("insert into test_users ('username, pswrd, reg_date')")
    # закрываем подключение
    cn.close()
