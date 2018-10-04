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


def register_and_login_user(name, password, test_client):
    user_data = {'username': name, 'password': password}
    test_client.post('/api/v1/auth/signup', json=user_data)
    response = test_client.post('/api/v1/auth/login', json=user_data)
    token = response.get_json()['token']
    headers = {'Authorization': 'Bearer ' + token}
    return headers


def login_administrator(test_client):
    admin = {'username': 'admin', 'password': 'administrator'}
    response = test_client.post('/api/v1/auth/login', json=admin)
    token = response.get_json()['token']
    headers = {'Authorization': 'Bearer ' + token}
    return headers


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
    assert response_2.status_code == 200
    assert 'token' in response_2.get_json()
    connection.cursor().execute("DELETE FROM users WHERE username = 'Jon Snow'")
    connection.commit()
    connection.close()


def test_api_returns_error_message_given_wrong_login_data(test_client):
    invalid_data = {'username': 'something'}
    response = test_client.post('/api/v1/auth/login', json=invalid_data)
    assert response.status_code == 400
    assert 'error' in response.get_json()


def test_api_can_place_an_order_for_food(test_client, connection):
    user_data = {'username': 'Loki Odinson', 'password': 'mischief'}
    response_1 = test_client.post('/api/v1/auth/signup', json=user_data)
    assert response_1.status_code == 201
    response_2 = test_client.post('/api/v1/auth/login', json=user_data)
    data = response_2.get_json()
    assert response_2.status_code == 200 and 'token' in data
    order = {'items': [{'item': 'pizza', 'quantity': 1, 'cost': 20000}]}
    headers = {'Authorization': 'Bearer ' + data['token']}
    response_3 = test_client.post('/api/v1/users/orders', json=order, headers=headers)
    assert response_3.status_code == 201
    assert 'order-id' in response_3.get_json()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM order_items WHERE item = %s', ('pizza', ))
    cursor.execute('DELETE FROM orders WHERE customer = %s', ('Loki Odinson', ))
    cursor.execute('DELETE FROM users WHERE username = %s', ('Loki Odinson', ))
    connection.commit()
    connection.close()


def test_api_returns_error_message_given_incorrect_post_order_data(test_client, connection):
    user_data = {'username': 'Loki Odinson', 'password': 'mischief'}
    response_1 = test_client.post('/api/v1/auth/signup', json=user_data)
    response_2 = test_client.post('/api/v1/auth/login', json=user_data)
    data = response_2.get_json()
    headers = {'Authorization': 'Bearer ' + data['token']}
    response_3 = test_client.post('/api/v1/users/orders', json={}, headers=headers)
    assert response_1.status_code == 201
    assert response_2.status_code == 200
    assert response_3.status_code == 400
    assert b'invalid data' in response_3.data
    cursor = connection.cursor()
    cursor.execute('DELETE FROM users WHERE username = %s', ('Loki Odinson', ))
    connection.commit()
    connection.close()


def test_api_returns_user_order_history(test_client, connection):
    user_data = {'username': 'steve rodgers', 'password': 'capitan'}
    response_1 = test_client.post('/api/v1/auth/signup', json=user_data)
    response_2 = test_client.post('/api/v1/auth/login', json=user_data)
    data = response_2.get_json()
    headers = {'Authorization': 'Bearer ' + data['token']}
    order_1 = {'items': [{'item': 'hot dog', 'quantity': 2, 'cost': 15000}]}
    order_2 = {'items': [{'item': 'salad', 'quantity': 1, 'cost': 10000}]}
    response_3 = test_client.post('/api/v1/users/orders', json=order_1, headers=headers)
    response_4 = test_client.post('/api/v1/users/orders', json=order_2, headers=headers)
    response_5 = test_client.get('/api/v1/users/orders', headers=headers)
    assert response_1.status_code == 201 and response_2.status_code == 200
    assert response_3.status_code == 201 and response_4.status_code == 201
    assert response_5.status_code == 200
    assert response_3.get_json() in response_5.get_json()['orders']
    assert response_4.get_json() in response_5.get_json()['orders']
    cursor = connection.cursor()
    cursor.execute('DELETE FROM users WHERE username = %s', ('steve rodgers', ))
    cursor.execute('DELETE FROM order_items WHERE item = %s', ('hot dog', ))
    cursor.execute('DELETE FROM order_items WHERE item = %s', ('salad', ))
    cursor.execute('DELETE FROM orders WHERE customer = %s', ('steve rodgers', ))
    cursor.execute("DELETE FROM orders WHERE customer = '{}'".format('steve rodgers'))
    connection.commit()
    connection.close()


def test_api_returns_message_when_getting_non_existent_order_history(test_client, connection):
    user = {'username': 'winter soldier', 'password': 'soldier'}
    response = test_client.post('/api/v1/auth/signup', json=user)
    response = test_client.post('/api/v1/auth/login', json=user)
    token = response.get_json()['token']
    headers = {'Authorization': 'Bearer ' + token}
    response = test_client.get('/api/v1/users/orders', headers=headers)
    assert response.status_code == 404
    assert 'message' in response.get_json()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM users WHERE username = %s', ('winter soldier', ))
    connection.commit()
    connection.close()


def test_admin_can_get_a_specific_order_by_id(test_client, connection):
    headers = login_administrator(test_client)
    order = {'items': [{'item': 'rolex', 'quantity': 2, 'cost': 2000}]}
    response = test_client.post('/api/v1/users/orders', json=order, headers=headers)
    order_id = response.get_json()['order-id']
    response_2 = test_client.get('/api/v1/orders/{}'.format(order_id), headers=headers)
    assert response.status_code == 201
    assert response_2.status_code == 200
    assert response.get_json()['order-id'] == response_2.get_json()['order-id']
    assert response.get_json()['status'] == response_2.get_json()['status']
    assert response.get_json()['total-cost'] == response_2.get_json()['total-cost']
    connection.cursor().execute('DELETE FROM order_items WHERE item = %s', ('rolex', ))
    connection.cursor().execute('DELETE FROM orders WHERE customer = %s', ('admin', ))
    connection.commit()
    connection.close()


def test_admin_can_update_order_status(test_client, connection):
    headers_1 = register_and_login_user('quill', 'starlord', test_client)
    order = {'items': [{'item': 'milk', 'quantity': 1, 'cost': 5000}]}
    response_1 = test_client.post('/api/v1/users/orders', json=order, headers=headers_1)
    order_id = response_1.get_json()['order-id']
    headers_2 = login_administrator(test_client)
    response_3 = test_client.put(
        '/api/v1/orders/{}'.format(order_id), headers=headers_2, json={'status': 'processing'}
    )
    response_3 = test_client.get('/api/v1/orders/{}'.format(order_id), headers=headers_2)
    assert response_3.status_code == 200
    assert response_3.get_json()['status'] == 'processing'
    connection.cursor().execute('DELETE FROM order_items WHERE item = %s', ('milk', ))
    connection.cursor().execute('DELETE FROM orders WHERE customer = %s', ('quill', ))
    connection.commit()
    connection.close()

