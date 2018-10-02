import pytest, psycopg2
from fastfoodfast import app
from werkzeug.security import check_password_hash


@pytest.fixture
def test_client():
    return app.test_client()


@pytest.fixture
def connection():
    conn = psycopg2.connect(
        database='fffdb',
        user='ongebo',
        password='nothing',
        host='127.0.0.1',
        port='5432'
    )
    return conn


def test_api_correctly_registers_a_user(test_client, connection):
    user_data = {'username': 'John Doe', 'password': 'JonathanDoe'}
    response = test_client.post('/api/v1/auth/signup', json=user_data)
    data = response.get_json()
    assert response.status_code == 201
    assert data['username'] == 'John Doe'
    assert check_password_hash(data['password'], 'JonathanDoe')
    assert data['admin'] == False
    connection.cursor().execute('DELETE FROM users WHERE username = \'John Doe\'')
    connection.commit()
    connection.close()


def test_api_returns_error_message_given_wrong_registration_data(test_client):
    invalid_user_data = {'username': '  ', 'password': 'something'}
    response = test_client.post('/api/v1/auth/signup', json=invalid_user_data)
    assert response.status_code == 400
    assert response.data # ensure that there is an error message


def test_api_correctly_logs_in_registered_user(test_client, connection):
    user_data = {'username': 'Jon Snow', 'password': 'winterfel'}
    response = test_client.post('/api/v1/auth/signup', json=user_data)
    assert response.status_code == 201
    response_2 = test_client.post('/api/v1/auth/login', json=user_data)
    assert response_2.status_code == 201
    assert 'token' in response_2.get_json()
    connection.cursor().execute("DELETE FROM users WHERE username = 'Jon Snow'")
    connection.commit()
    connection.close()


def test_api_returns_error_message_given_wrong_login_data(test_client):
    invalid_data = {'username': 'something'}
    response = test_client.post('/api/v1/auth/login', json=invalid_data)
    assert response.status_code == 400
    assert 'error' in response.get_json()
