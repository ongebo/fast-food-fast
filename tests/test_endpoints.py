import pytest, psycopg2, os
from fastfoodfast import app
from werkzeug.security import check_password_hash


@pytest.fixture
def test_client():
    os.environ['DATABASE_URL'] = 'postgres://ongebo:nothing@127.0.0.1:5432/testdb'
    return app.test_client()


@pytest.fixture
def connection():
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    return conn


def register_and_login_user(name, password, test_client):
    """Signs up and logs in a new user, returns Authorization header for the user"""
    user_data = {
        'username': name, 'password': password,
        'email': 'name@domain.com', 'telephone': '+256-753-653973'
    }
    response_1 = test_client.post('/api/v1/auth/signup', json=user_data)
    assert response_1.status_code == 201
    response_2 = test_client.post('/api/v1/auth/login', json=user_data)
    token = response_2.get_json()['token']
    headers = {'Authorization': 'Bearer ' + token}
    return headers


def login_administrator(test_client):
    """Logs in the administrator and returns headers containing JWT token for the admin"""
    admin = {'username': 'admin', 'password': 'administrator'}
    response = test_client.post('/api/v1/auth/login', json=admin)
    token = response.get_json()['token']
    headers = {'Authorization': 'Bearer ' + token}
    return headers


def clean_users(conn, *usernames):
    """Used by tests to reset changes made to users table"""
    cursor = conn.cursor()
    for username in usernames:
        cursor.execute('DELETE FROM users WHERE username = %s', (username, ))


def clean_orders(conn, customer):
    """Used by tests to revert changes made to database when testing orders management"""
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM orders WHERE customer = %s', (customer, ))
    for order_id in cursor.fetchall():
        cursor.execute('DELETE FROM order_items WHERE order_id = %s', (order_id, ))
    cursor.execute('DELETE FROM orders WHERE customer = %s', (customer, ))


def commit_and_close(conn):
    conn.commit()
    conn.close()


def test_api_correctly_registers_a_user(test_client, connection):
    user_data = {
        'username': 'John Doe', 'password': 'J0nathanD0e',
        'email': 'jonathadoe@gmail.com', 'telephone': '+1-345-345981'
    }
    response = test_client.post('/api/v1/auth/signup', json=user_data)
    data = response.get_json()
    assert response.status_code == 201
    assert data['message'] == 'you were successfully registered!'
    clean_users(connection, 'John Doe')
    commit_and_close(connection)


def test_api_returns_error_message_given_wrong_registration_data(test_client):
    invalid_user_data = {'username': '  ', 'password': 'something'}
    response = test_client.post('/api/v1/auth/signup', json=invalid_user_data)
    assert response.status_code == 400
    assert response.get_json()['error'] # ensure that there is an error message


def test_api_correctly_logs_in_registered_user(test_client, connection):
    user_data = {
        'username': 'Jon Snow', 'password': 'W1nterfel',
        'email': 'jonsnow@winterfel.net', 'telephone': '+45-457-345911'
    }
    response_1 = test_client.post('/api/v1/auth/signup', json=user_data)
    assert response_1.status_code == 201
    response_2 = test_client.post('/api/v1/auth/login', json=user_data)
    assert response_2.status_code == 200
    assert 'token' in response_2.get_json()
    clean_users(connection, 'Jon Snow')
    commit_and_close(connection)


def test_api_returns_error_message_given_wrong_login_data(test_client):
    invalid_data = {'username': 'something'}
    response = test_client.post('/api/v1/auth/login', json=invalid_data)
    assert response.status_code == 400
    assert 'error' in response.get_json()


def test_api_can_place_an_order_for_food(test_client, connection):
    headers = register_and_login_user('Loki Odinson', 'M1sch1ef', test_client)
    order = {'items': [{'item': 'pizza', 'quantity': 1, 'cost': 20000}]}
    response = test_client.post('/api/v1/users/orders', json=order, headers=headers)
    assert response.status_code == 201
    assert 'order-id' in response.get_json()
    clean_orders(connection, 'Loki Odinson')
    clean_users(connection, 'Loki Odinson')
    commit_and_close(connection)


def test_api_returns_error_message_given_incorrect_post_order_data(test_client, connection):
    headers = register_and_login_user('okoye', 'Genera1', test_client)
    response = test_client.post('/api/v1/users/orders', json={}, headers=headers)
    assert response.status_code == 400
    assert 'error' in response.get_json()
    clean_users(connection, 'okoye')
    commit_and_close(connection)


def test_api_returns_user_order_history(test_client, connection):
    headers = register_and_login_user('steve rodgers', 'C4pit4n', test_client)
    order_1 = {'items': [{'item': 'hot dog', 'quantity': 2, 'cost': 15000}]}
    order_2 = {'items': [{'item': 'salad', 'quantity': 1, 'cost': 10000}]}
    response_1 = test_client.post('/api/v1/users/orders', json=order_1, headers=headers)
    response_2 = test_client.post('/api/v1/users/orders', json=order_2, headers=headers)
    response_3 = test_client.get('/api/v1/users/orders', headers=headers)
    assert response_1.status_code == 201 and response_2.status_code == 201
    assert response_3.status_code == 200
    assert response_1.get_json() in response_3.get_json()['orders']
    assert response_2.get_json() in response_3.get_json()['orders']
    clean_users(connection, 'steve rodgers')
    clean_orders(connection, 'steve rodgers')
    commit_and_close(connection)


def test_api_returns_message_when_getting_non_existent_order_history(test_client, connection):
    headers = register_and_login_user('winter soldier', 'S0ldier', test_client)
    response = test_client.get('/api/v1/users/orders', headers=headers)
    assert response.status_code == 404
    assert 'error' in response.get_json()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM users WHERE username = %s', ('winter soldier', ))
    connection.commit()
    connection.close()

def test_admin_can_get_all_orders_from_database(test_client, connection):
    headers_1 = register_and_login_user('Prisca', 'Pr1sca$', test_client)
    headers_2 = register_and_login_user('Banner', 'St0ng3st', test_client)
    headers_3 = login_administrator(test_client)
    order_1 = {'items': [{'item': 'salad', 'quantity': 1, 'cost': 10000}]}
    order_2 = {'items': [{'item': 'salad', 'quantity': 1, 'cost': 10000}]}
    test_client.post('/api/v1/users/orders', json=order_1, headers=headers_1)
    test_client.post('/api/v1/users/orders', json=order_2, headers=headers_2)
    response = test_client.get('/api/v1/orders', headers=headers_3)
    assert response.status_code == 200
    order_items = list()
    for order in response.get_json()['orders']:
        order_items.append(order['items'])
    assert order_1['items'] in order_items and order_2['items'] in order_items
    clean_orders(connection, 'Prisca')
    clean_orders(connection, 'Banner')
    clean_users(connection, 'Prisca', 'Banner')
    commit_and_close(connection)


def test_admin_can_get_a_specific_order_by_id(test_client, connection):
    headers = login_administrator(test_client)
    order = {'items': [{'item': 'rolex', 'quantity': 2, 'cost': 2000}]}
    response_1 = test_client.post('/api/v1/users/orders', json=order, headers=headers)
    order_id = response_1.get_json()['order-id']
    response_2 = test_client.get('/api/v1/orders/{}'.format(order_id), headers=headers)
    assert response_1.status_code == 201
    assert response_2.status_code == 200
    assert response_1.get_json()['order-id'] == response_2.get_json()['order-id']
    assert response_1.get_json()['status'] == response_2.get_json()['status']
    assert response_1.get_json()['total-cost'] == response_2.get_json()['total-cost']
    clean_orders(connection, 'admin')
    commit_and_close(connection)


def test_admin_can_update_order_status(test_client, connection):
    headers_1 = register_and_login_user('quill', 'St4rl0rd', test_client)
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
    clean_orders(connection, 'quill')
    clean_users(connection, 'quill')
    commit_and_close(connection)


def test_api_can_return_created_menu_item_to_admin(test_client, connection):
    headers = login_administrator(test_client)
    menu_item = {'item': 'spaghetti', 'unit': 'pack', 'rate': 5000}
    response_1 = test_client.post('/api/v1/menu', json=menu_item, headers=headers)
    response_2 = test_client.get('/api/v1/menu', headers=headers)
    created_item = response_1.get_json()
    response_3 = test_client.get('/api/v1/menu/{}'.format(created_item['id']), headers=headers)
    assert response_1.status_code == 201 and response_3.status_code == 200
    assert created_item in response_2.get_json()['menu']
    assert menu_item == response_3.get_json()
    assert response_2.status_code == 200
    connection.cursor().execute('DELETE FROM menu WHERE item = %s', ('spaghetti', ))
    connection.commit()
    connection.close


def test_api_raises_404_when_fetching_non_existent_menu_item(test_client):
    headers = login_administrator(test_client)
    response = test_client.get('/api/v1/menu/0', headers=headers)
    assert response.status_code == 404


def test_api_enables_admin_to_edit_a_menu_item(test_client, connection):
    headers = login_administrator(test_client)
    item = {'item': 'Muchomo', 'unit': 'Stick', 'rate': 4000}
    response_1 = test_client.post('/api/v1/menu', json=item, headers=headers)
    item_id = response_1.get_json()['id']
    item['rate'] = 3000 # update item's rate
    response_2 = test_client.put('/api/v1/menu/{}'.format(item_id), headers=headers, json=item)
    response_3 = test_client.get('/api/v1/menu/{}'.format(item_id), headers=headers)
    assert response_1.status_code == 201 and response_2.status_code == 200
    assert response_3.status_code == 200
    assert item == response_3.get_json()
    connection.cursor().execute('DELETE FROM menu WHERE item = %s', ('Muchomo', ))
    commit_and_close(connection)


def test_api_returns_error_for_bad_request_or_unauthorized_access_to_edit_menu_item(test_client, connection):
    headers_1 = login_administrator(test_client)
    headers_2 = register_and_login_user('Mike', 'M1chael', test_client)
    item = {'item': 'Hamburger', 'unit': 'Pack'} # invalid menu item
    response_1 = test_client.put('/api/v1/menu/1', headers=headers_1, json=item)
    response_2 = test_client.put('/api/v1/menu/-2', headers=headers_1, json=item)
    response_3 = test_client.put('/api/v1/menu/1', headers=headers_2, json=item)
    assert response_1.status_code == 400
    assert response_2.status_code == 404
    assert response_3.status_code == 401
    clean_users(connection, 'Mike')
    commit_and_close(connection)


def test_api_enables_admin_to_delete_a_specific_menu_item(test_client):
    headers = login_administrator(test_client)
    menu_item = {'item': 'Juice', 'unit': 'Glass', 'rate': 2500}
    item_id = test_client.post('/api/v1/menu', headers=headers, json=menu_item).get_json()['id']
    response_1 = test_client.delete('/api/v1/menu/{}'.format(item_id), headers=headers)
    response_2 = test_client.get('/api/v1/menu', headers=headers)
    assert response_1.status_code == 200
    assert response_2.status_code == 404


def test_api_returns_404_when_admin_tries_to_delete_non_existent_menu_item(test_client):
    headers = login_administrator(test_client)
    response = test_client.delete('/api/v1/menu/0', headers=headers)
    assert response.status_code == 404
    assert 'error' in response.get_json()


def test_api_returns_401_when_non_admin_user_tries_to_delete_menu_item(test_client, connection):
    headers = register_and_login_user('Jack Sparrow', 'P1rateCap', test_client)
    response = test_client.delete('/api/v1/menu/1', headers=headers)
    assert response.status_code == 401
    assert 'error' in response.get_json()
    clean_users(connection, 'Jack Sparrow')
    commit_and_close(connection)


def test_api_returns_error_for_unauthorized_access_to_admin_routes(test_client, connection):
    headers = register_and_login_user('Tony Stark', '1ronM4n', test_client)
    response_1 = test_client.get('/api/v1/orders', headers=headers)
    response_2 = test_client.get('/api/v1/orders/67DAEDe', headers=headers)
    status = {'status': 'processing'}
    response_3 = test_client.put('/api/v1/orders/afdfik76', json=status, headers=headers)
    menu_item = {'item': 'hot dog', 'unit': 'pack', 'rate': 10000}
    response_4 = test_client.post('/api/v1/menu', json=menu_item, headers=headers)
    assert response_1.status_code == 401 and 'error' in response_1.get_json()
    assert response_2.status_code == 401 and 'error' in response_2.get_json()
    assert response_3.status_code == 401 and 'error' in response_3.get_json()
    assert response_4.status_code == 401 and 'error' in response_4.get_json()
    clean_users(connection, 'Tony Stark')
    commit_and_close(connection)


def test_api_returns_404_error_when_requesting_non_existent_url(test_client):
    response = test_client.get('/api/v2')
    assert response.status_code == 404
    assert 'error' in response.get_json()
