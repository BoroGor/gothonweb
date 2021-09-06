from nose.tools import *
from app import app


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
    eq_(name_head(response), 'Central Corridor')

# проверка страницы [/game]
def test_game():
    # проверка существования страницы
    response = client.get('/game', follow_redirects = True)
    eq_(response.status_code, 200)
    # проверка соответствия стартовой странице
    eq_(name_head(response), 'Central Corridor')

# проверка отправки формы и переходов на соответствующие страницы
def test_form():
    pass
