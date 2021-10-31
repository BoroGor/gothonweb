from nose.tools import *
from app import app
from flask import session


# настройка конфигурации приложения для тестирования, чтобы ошибки
# обрабатывались клиентом тестирования, а не самим приложением
app.testing = True
client = app.test_client()



# функция определения заголовка страницы
def name_head(response_object):
    # тип получаемых данных "str"
    data = response_object.data.decode()
    # индекс вхождения заголовка страницы
    beg = int(data.index('h1') + 4)
    # индекс закрывающего тега заголовка страницы
    end = int(data.index('/h1') - 2)
    # вывод среза текста (заголовка страницы)
    return data[beg:end]

# проверяем соответствие секретного ключа
def test_secret_key():
    rv = app.secret_key
    eq_(rv, 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT')

# проверяем существование страницы [/]
def test_index():
    response = client.get('/', follow_redirects = False)
    eq_(response.status_code, 302)
    #  и автоматический переход на следующую страницу
    response = client.get('/', follow_redirects = True)
    print(response.headers)
    eq_(response.status_code, 200)
    # проверяем то, что перешли на нужную страницу
    eq_(name_head(response), 'Create Your Unique Nickname')

# проверка страницы [/game]
def test_game():
    # проверка существования страницы
    response = client.get('/game', follow_redirects = True)
    eq_(response.status_code, 200)
    # проверка соответствия стартовой странице
    eq_(name_head(response), 'Central Corridor')

# проверка отправки формы и переходов на соответствующие страницы
def test_action_form():
    # проверка отправки пустой формы
    data = {'action':''}
    response = client.post('/game', follow_redirects = False, data=data)
    eq_(response.status_code, 302)
    # переход на новую страницу и проверка ожидания
    response = client.post('/game', follow_redirects = True, data=data)
    eq_(response.status_code, 200)
    # перехода на новую страницу быть не должно
    eq_(name_head(response), 'Central Corridor')

    # проверка проигрыша в центральном коридоре
    data = {'action': 'shoot'}
    response = client.post('/game', follow_redirects = True, data=data)
    eq_(response.status_code, 200)
    # перехода на новую страницу быть не должно
    eq_(name_head(response), 'death')

    # переход в оружейную и проверка смерти после трёх
    with app.test_request_context('/game'):
        # было сделано до запроса 3 попытки
        session['try']=3
        # комната - оружейная
        session['romm_name']="laser_weapon_armory"
        # данные, приводящие к проигрышу
        data = {'action': '0000'}
        response = client.post('/game', follow_redirects = True, data = data)
        # проверка существования страницы
        eq_(response.status_code, 200)
        # проверка перехода на нужную страницу
        eq_(name_head(response), 'death')

# проверка регистрации/входа, [/login]
def test_login():
    # проверка получения нужной страницы
    res = client.get('/login', follow_redirects = True)
    eq_(name_head(res), 'Create Your Unique Nickname')
    # проверка работы формы логина
    with app.test_request_context('/login'):
        # дата для ввода в форму
        data = {'username': 'login user'}
        res = client.post('/login', follow_redirects = True, data = data)
        # проверка флеш-уведомления при логине
        assert_in('login user', res.data.decode())

# проверка обновления числа попыток
