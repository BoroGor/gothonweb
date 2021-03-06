from flask import Flask, session, redirect, url_for, request, render_template
from gothonweb import planisphere
from gothonweb.helpblock import help
#import sqlite3 as sql3


# создаём объект класса Flask и присваиваем имя приложению - не переменной!
app = Flask(__name__)
# включаем режим отладки
app.debug = True


# для начальной страницы
@app.route("/")
# создаём обрабатывающую функцию
def index():
    # создаём сессию с начальными данными - начальной комнатой
    # создаём пару КЛЮЧ - ЗНАЧЕНИЕ
    session["room_name"] = planisphere.START  # "central_corridor"
    # для оружейной
    session["try"] = 0
    # перенаправляем на указанный адрес
    return redirect(url_for("login"))


# для страницы регистрации
@app.route("/login", methods=["GET", "POST"])
# создаём обрабатывающую функцию
def login():
    return render_template("login.html")


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
