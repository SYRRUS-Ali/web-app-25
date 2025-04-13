import pytest
import os
import sys
sys.path.insert(0, os.path.abspath('.'))

from app import app, users
from flask import url_for, session, get_flashed_messages
from flask_login import FlaskLoginClient, current_user

@pytest.fixture
def client():
    app.test_client_class = FlaskLoginClient
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_visit_counter_increments(client):
    """Тест счетчика посещений"""
    response = client.get('/')
    assert 'Вы посетили эту страницу 1 раз' in response.get_data(as_text=True)
    
    response = client.get('/')
    assert 'Вы посетили эту страницу 2 раз' in response.get_data(as_text=True)

def test_visit_counter_per_user(client):
    """Тест уникального счетчика для каждого пользователя"""
    # Первый пользователь
    with client.session_transaction() as sess:
        sess['visits'] = 5
    response = client.get('/')
    assert 'Вы посетили эту страницу 6 раз' in response.get_data(as_text=True)
    
    # Новый пользователь (новая сессия)
    new_client = app.test_client()
    response = new_client.get('/')
    assert 'Вы посетили эту страницу 1 раз' in response.get_data(as_text=True)

def test_successful_login(client):
    """Тест успешной аутентификации"""
    response = client.post('/login', data={
        'username': 'ali',
        'password': 'ali2025'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Привет, ali! Вы вошли в систему.' in response.get_data(as_text=True)
    assert 'Секретная страница' in response.get_data(as_text=True)

def test_failed_login(client):
    """Тест неудачной аутентификации"""
    response = client.post('/login', data={
        'username': 'ali',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Неверное имя пользователя или пароль' in response.get_data(as_text=True)
    assert 'Форма входа' in response.get_data(as_text=True)

def test_authenticated_secret_access(client):
    """Тест доступа к секретной странице после входа"""
    client.post('/login', data={'username': 'ali', 'password': 'ali2025'})
    response = client.get('/secret')
    assert response.status_code == 200
    assert 'Секретная страница' in response.get_data(as_text=True)

def test_redirect_after_login(client):
    """Тест перенаправления после входа"""
    # Попытка доступа к секретной странице
    response = client.get('/secret')
    assert response.status_code == 302
    
    # Вход в систему
    response = client.post('/login', data={
        'username': 'ali',
        'password': 'ali2025',
        'next': '/secret'
    }, follow_redirects=True)
    
    # Должны быть перенаправлены на секретную страницу
    assert 'Секретная страница' in response.get_data(as_text=True)

def test_logout(client):
    """Тест выхода из системы"""
    client.post('/login', data={'username': 'ali', 'password': 'ali2025'})
    response = client.get('/logout', follow_redirects=True)
    assert 'Вы вышли из системы.' in response.get_data(as_text=True)
    assert 'Вы не авторизованы.' in response.get_data(as_text=True)

def test_navbar_for_authenticated_user(client):
    """Тест навигации для авторизованного пользователя"""
    client.post('/login', data={'username': 'ali', 'password': 'ali2025'})
    response = client.get('/')
    data = response.get_data(as_text=True)
    assert 'Секретная страница' in data
    assert 'Выход' in data
    assert 'Вход' not in data

def test_navbar_for_unauthenticated_user(client):
    """Тест навигации для неавторизованного пользователя"""
    response = client.get('/')
    data = response.get_data(as_text=True)
    assert 'Вход' in data
    assert 'Секретная страница' not in data
    assert 'Выход' not in data

def test_session_persistence(client):
    """Тест сохранения сессии"""
    response = client.get('/')
    assert 'Вы посетили эту страницу 1 раз' in response.get_data(as_text=True)
    
    with client.session_transaction() as sess:
        assert 'visits' in sess
        assert sess['visits'] == 1

def test_flash_messages(client):
    """Тест flash-сообщений"""
    client.post('/login', data={'username': 'ali', 'password': 'ali2025'})
    response = client.get('/')
    assert 'Вы успешно вошли в систему!' in response.get_data(as_text=True)
    
    client.get('/logout')
    response = client.get('/')
    assert 'Вы вышли из системы.' in response.get_data(as_text=True)


'''
python -m pytest tests/
'''