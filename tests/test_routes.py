def test_index(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert "Главная страница AI Бизнес помощник" in response.data.decode('utf-8')


def test_login_page(test_client):
    response = test_client.get('/login')
    assert response.status_code == 200
    assert "Войти" in response.data.decode('utf-8')


def test_register_page(test_client):
    response = test_client.get('/register')
    assert response.status_code == 200
    assert "Регистрация" in response.data.decode('utf-8')