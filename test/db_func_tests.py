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
def test_create_user():
    # создаём блок вводных данных (имя, дата регистр)
    user = 'FU'; d = '2021-10-25'
    # создаём активное подключение к БД
    con = fn.connect_db(app.config['DATABASE'])
    # создаём объект курсора для SQL-вызовов
    cur = con.cursor()
    # создаём запись пользователя
    fn.create_user(user, d, app.config['DATABASE'])
    # проверим, создался ли пользователь
    eq_(fn.check(user, cur), True)
    # попытаемся создать ещё одного такого же пользователя
    ans = fn.create_user(user, d, app.config['DATABASE'])
    # проверим, что попытка не удалась
    eq_(ans, 'already exists')
    # проверим дату регистрации пользователя
    cur.execute('select reg_date from users where username=?', (user,))
    # запомним ответ на запрос
    f = cur.fetchall()
    # проверим, что выведена одна запись
    eq_(len(f), 1)
    # прочитаем дату
    ch_d = f[0][0]
    # проверим, что дата определена верно
    eq_(ch_d, d)
    # чистим таблицу
    cur.execute('delete from users')
    con.commit()
    # закрываем подключение
    con.close()

# проверка функции записи минимального числа попыток
def test_wtry():
    # входные данные
    ntry = 3; user = 'user'; rd = 'rd'
    # создадим запись об игроке
    fn.create_user(user, rd, app.config['DATABASE'])
    # на вход - игрок, попытки, адрес БД
    # записывает новое значение попыток в профиль, если их число меньше
    ans = fn.wtry(user, ntry, app.config['DATABASE'])
    # ожидаемый ответ ('user', 3)
    eq_(ans, (user, 3))
    # изменим входные данные
    ntry2 = 2
    ans2 = fn.wtry(user, ntry2, app.config['DATABASE'])
    # ожидаемый ответ ('user', 2)
    eq_(ans2, (user, 2))
    # попытаемся обновить попытки несуществующего игрока
    ans3 = fn.wtry('kjdf', ntry2, app.config['DATABASE'])
    eq_(ans3, 'kjdf not exists')
    # почистим БД
    con = fn.connect_db(app.config['DATABASE'])
    con.cursor().execute('delete from users')
    con.commit()
    con.close()
