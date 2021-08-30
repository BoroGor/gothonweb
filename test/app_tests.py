from nose.tools import *
from app import app
from flask import session, request


# настройка конфигурации приложения для тестирования, чтобы ошибки
# обрабатывались клиентом тестирования, а не самим приложением
app.testing = True
client = app.test_client()


# проверяем соответствие секретного ключа
def test_secret_key():
    rv = app.secret_key
    eq_(rv, 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT')

# проверяем существование страницы [/] и автоматический переход
def test_index():
    response = client.get('/', follow_redirects = False)
    eq_(response.status_code, 302)

    response = client.get('/', follow_redirects = True)
    eq_(response.status_code, 200)

    #with app.test_request_context('/', method='GET'):
        #request('/', method = 'GET')
        #s = session.open_session(app, r)
