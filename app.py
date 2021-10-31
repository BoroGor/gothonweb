from flask import Flask, session, redirect, url_for, request, render_template, flash
from gothonweb import planisphere
from gothonweb.helpblock import help
from datetime import date
from pathlib import Path
import db_func as fn


# создаём объект класса Flask и присваиваем имя приложению - не переменной!
app = Flask(__name__)
# включаем режим отладки
app.debug = True

# задаём адрес для создания тестовой БД
DATABASE_abs = Path(app.root_path, 'static', 'main.db')
# добавим в конфигурацию приложения адрес БД
app.config.update(dict(DATABASE = DATABASE_abs))


# для начальной страницы
@app.route("/")
# создаём обрабатывающую функцию
def index():
    # создаём БД
    fn.create_db(app.config['DATABASE'])
    # создаём сессию с начальными данными - начальной комнатой
    # создаём пару КЛЮЧ - ЗНАЧЕНИЕ
    session["room_name"] = planisphere.START  # "central_corridor"
    # для оружейной
    session["try"] = 0
    # костыль, почему-то без него автоматически создаётся куки
    # сработает лишь при инициализации
    if 'cur_usr' in session:
        # удаляем куки пользователя
        session.pop('cur_usr', None)
    # перенаправляем на указанный адрес
    return redirect(url_for("login"))


# для страницы регистрации
@app.route("/login", methods=["GET", "POST"])
# создаём обрабатывающую функцию
def login():
    # если запрос на получение страницы, не отправку данных
    if request.method == "GET":
        # открываем форму входа в профиль
        return render_template("login.html")
    # если была отправлена форма
    if request.method == "POST":
        # запишем день, месяц и год дня регистрации
        d, m, y = date.today().day, date.today().month, date.today().year
        # запишем дату в формате "ГГГГ-ММ-ДД"
        today = '-'.join([str(y), str(m), str(d)])
        # считываем имя из формы
        user = request.form.get("username")
        # запишем пользователя в сессию
        session['cur_usr'] = str(user)
        # высвечиваем информацию об имени пользователя на следующей странице
        flash(f"^-^ Logged in as {session['cur_usr']} ^-^", 'info')
        # предотвращаем запись в основную БД во время тестов
        #
        # КОСТЫЛЬ КОСТЫЛЬ КОСТЫЛЬ КОСТЫЛЬ КОСТЫЛЬ КОСТЫЛЬ КОСТЫЛЬ КОСТЫЛЬ
        #
        if not app.testing:
            # сделаем запись об игроке в БД
            fn.create_user(session['cur_usr'], today, app.config['DATABASE'])
        # перенаправляем на страницу игры
        return redirect(url_for("game"))


# для страницы /game, задаём используемые методы
@app.route("/game", methods=["GET", "POST"])
# создаём обрабатывающую функцию
def game():
    # переменной присваиваем значение по ключу из сессии
    room_name = session.get("room_name")
    # если запрос на получение данных
    if request.method == "GET":
        # если есть имя комнаты, т.е. имя != None
        if room_name:
            # если было 3 неудачные попытки ввести код, то смерть в оружейной
            if room_name == "laser_weapon_armory" and session["try"] >= 3:
                # имя будущей комнаты - смерть в оруженой
                session["room_name"] = "armory_death"
                # перенаправляем для загрузки комнаты
                return redirect(url_for("game"))
            else:
                # за переменной закрепляем объект класса Room, найденный по имени
                room = planisphere.load_room(room_name)
                # возвращаем шаблон и передаём объект комнаты с помощью переменной
                return render_template("show_room.html", room=room, help=help)
        # если комнаты не существует, т.е. случился выход за карту
        else:
            # возвращаем шаблон
            return render_template("you_died.html")
    # если запрос на отправку данных
    elif request.method == "POST":
        # если запрос из оружейной
        if room_name == "laser_weapon_armory":
            # увеличиваем счётчик попыток ввести код
            session["try"] = session.get("try") + 1
        # присваиваем переменной данные, введённые в поле формы с
        # именем "action"; = None, если ключ не существует
        action = request.form.get("action")
        # если имя комнаты и данные существуют
        if room_name and action:
            # за переменной закрепляем объект класса Room, найденный по имени
            room = planisphere.load_room(room_name)
            # переменной присваиваем объект класса Room, найденный в "путях"
            # предыдущей комнаты
            next_room = room.go(action)
            # если следующей комнаты не существует: функция вернула "None"
            if not next_room:
                # изменяем данные сессии и закрепляем за "room_name"
                # имя переменной для объекта класса Room
                session["room_name"] = planisphere.name_room(room)
            # если следующая комната существует
            else:
                # изменяем данные сессии и закрепляем за "room_name"
                # имя переменной для объекта класса Room
                session["room_name"] = planisphere.name_room(next_room)
        # в любом случае при отправке данных перенаправляем на страницу /game
        return redirect(url_for("game"))
    # если метод запроса не "get" и форма не отправлялась
    else:
        # переход на страницу выхода за карту
        return render_template("you_died.html")


# YOU SHOULD CHANGE THIS IF YOU PUT ON THE INTERNET
app.secret_key = "A0Zr98j/3yX R~XHH!jmN]LWX/,?RT"

if __name__ == "__main__":
    app.run(host="localhost", port=5000)
