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
        create table if not exists users (
        username text not null primary key,
        min_trying integer default 3,
        reg_date text not null);""")
    # сохраняем изменения в таблице
    db.commit()
    # закрываем соединение
    db.close()

# функция поиска пользователя в БД
def check(user, cur):
    """user - имя искомого пользователя, cur - курсор БД;
    возвращает True, если пользователь найден, иначе - False"""
    # переводим имена в тип строки
    user = (str(user),)
    # запрос на посик пользователя
    cur.execute('select * from users where username = ?', user)
    # сохраним вывод
    ans = cur.fetchall()
    # если в ответе нет строк
    if len(ans) == 0:
        # пользователь не найден
        return False
    # если же ответ содержит строку/строки
    else:
        # пользователь найден
        return True

# функция создания записи пользователя
def create_user(user, date, db_adres):
    """user - имя пользователя, date - дата регистрации, db_adres - путь к БД;
    создаёт запись в БД; если такой пользователь уже существет, то
    возвращает строку 'already exists'
    """
    # создадим курсор
    cur = connect_db(db_adres).cursor()
    # явно объявим типы данных
    user = str(user); date = str(date); data = (user, date,)
    # если пользователь уже существует
    if check(user, cur):
        # ничего не предпринимаем
        return('already exists')
    # если же пользователь отсутствует в БД
    else:
        # запишем данные в таблицу
        cur.execute('insert into users (username, reg_date) values (?,?)', data)
        cur.connection.commit()

# функция записи меньшего значения попыток
def wtry(user, new_try, db_adres):
    """user - имя пользователя, new_try - новое число попыток, db_adres - адрес
    БД; возвращает кортеж (имя пользователя, минимальное число попыток)
    """
    new_try = int(new_try)
    # подключаемся к БД
    con = connect_db(db_adres)
    cur = con.cursor()
    # если пользователь существует
    if check(user, cur):
        # получим текущее значение попыток
        t = (user,)
        cur.execute('select min_trying from users where username=?', t)
        cur_try = cur.fetchall()[0][0]
        # если новое число попыток меньше
        if new_try < cur_try:
            d = {'val': new_try, 'u': user}
            # записываем нвоое значение
            cur.execute('update users set min_trying=:val where username=:u',d)
            # сохраняем изменения
            con.commit()
        # вернём пару пользователь-попытки
        cur.execute('select username, min_trying from users where username=?', t)
        ans = cur.fetchall()[0]
        # закроем подключение
        con.close()
        return ans
    # если же пользователя не существует
    else:
        # закроем подключение
        con.close()
        # вернём сообщение о том, что пользователя нет в БД
        return f'{user} not exists'
