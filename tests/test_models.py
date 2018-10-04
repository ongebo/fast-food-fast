import pytest, psycopg2, os
from fastfoodfast.models import User, Order, Menu
from werkzeug.security import generate_password_hash, check_password_hash


@pytest.fixture
def database_connection():
    database_url = 'postgres://ongebo:nothing@127.0.0.1:5432/testdb'
    os.environ['DATABASE_URL'] = database_url
    conn = psycopg2.connect(database_url)
    return conn


def test_model_correctly_registers_new_user_to_the_database(database_connection):
    user_model = User()
    new_user = user_model.register_user({'username': 'customer', 'password': 'p@$$word'})
    assert new_user['username'] == 'customer'
    assert check_password_hash(new_user['password'], 'p@$$word')
    assert new_user['admin'] == False
    cursor = database_connection.cursor()
    cursor.execute('SELECT username, password FROM users WHERE username = \'customer\'')
    result = cursor.fetchall()
    assert 'customer' in result[0]
    assert check_password_hash(result[0][1], 'p@$$word')
    cursor = database_connection.cursor()
    cursor.execute('DELETE FROM users WHERE username = \'customer\'')
    database_connection.commit()
    database_connection.close()


def test_model_raises_exception_when_registering_with_existent_username(database_connection):
    user_model = User()
    user = {'username': 'customer', 'password': 'p@$$word'}
    user_model.register_user(user)
    with pytest.raises(Exception):
        user_model.register_user(user) # try to re-register user
    cursor = database_connection.cursor()
    cursor.execute('DELETE FROM users WHERE username = \'customer\'')
    database_connection.commit()
    database_connection.close()


def test_model_raises_exception_given_incorrect_user_data_for_registration(database_connection):
    user_model = User()
    incorrect_data = {'username': ' ', 'password': 786}
    with pytest.raises(Exception):
        user_model.register_user(incorrect_data)


def test_model_can_get_a_specific_user_by_username_from_db(database_connection):
    user_model = User()
    database_connection.cursor().execute(
        "INSERT INTO users (username, password, admin) VALUES ('Thor', 'asgard', 'f')"
    )
    database_connection.commit()
    user = user_model.get_user('Thor')
    assert user['username'] == 'Thor'
    assert user['password'] == 'asgard'
    database_connection.cursor().execute(
        "DELETE FROM users WHERE username='Thor'"
    )
    database_connection.commit()
    database_connection.close()


def test_model_raises_exception_when_retrieving_non_existent_user(database_connection):
    user_model = User()
    with pytest.raises(Exception):
        user_model.get_user('Non-existent user!')
    with pytest.raises(Exception):
        user_model.get_user(34)


def test_model_can_add_a_new_order_to_the_database(database_connection):
    order_model = Order()
    order = {
        'items': [{'item': 'pizza', 'quantity': 1, 'cost': 18000}],
        'status': 'pending',
        'total-cost': 18000
    }
    created_order = order_model.create_order(order, 'skywalker')
    assert 'order-id' in created_order and 'status' in created_order
    cursor = database_connection.cursor()
    cursor.execute(
        'SELECT * FROM orders WHERE public_id = %s', (created_order['order-id'], )
    )
    result = cursor.fetchone()
    assert 'skywalker' in result and 'new' in result
    cursor.execute('SELECT * FROM order_items')
    result = cursor.fetchone()
    assert 'pizza' in result and 1.0 in result and 18000 in result
    cursor.execute('DELETE FROM order_items WHERE item = %s', ('pizza', ))
    cursor.execute('DELETE FROM orders WHERE public_id = %s', (created_order['order-id'], ))
    database_connection.commit()
    database_connection.close()


def test_model_raises_exception_given_invalid_order_data(database_connection):
    order_model = Order()
    with pytest.raises(Exception):
        order_model.create_order([], 'jon snow')


def test_model_can_get_order_history_for_a_given_customer(database_connection):
    order_model = Order()
    order_1 = {'items': [{'item': 'pizza', 'quantity': 2, 'cost': 40000}]}
    order_2 = {'items': [{'item': 'hamburger', 'quantity': 1, 'cost': 10000}]}
    created_order1 = order_model.create_order(order_1, 'luke skywalker')
    created_order2 = order_model.create_order(order_2, 'luke skywalker')
    orders = order_model.get_order_history('luke skywalker')
    assert created_order1 in orders and created_order2 in orders
    cursor = database_connection.cursor()
    cursor.execute('DELETE FROM order_items WHERE item = %s', ('pizza', ))
    cursor.execute('DELETE FROM order_items WHERE item = %s', ('hamburger', ))
    cursor.execute('DELETE FROM orders WHERE customer = %s', ('luke skywalker', ))
    database_connection.commit()
    database_connection.close()


def test_model_raises_exception_when_no_orders_have_been_made_by_a_user(database_connection):
    order_model = Order()
    with pytest.raises(Exception):
        order_model.get_order_history('museveni')


def test_model_can_return_all_orders_in_database(database_connection):
    order_model = Order()
    order_1 = {'items': [{'item': 'pillao', 'quantity': 1, 'cost': 15000}]}
    order_2 = {'items': [{'item': 'beef', 'quantity': 2, 'cost': 10000}]}
    created_order_1 = order_model.create_order(order_1, 'thanos')
    created_order_2 = order_model.create_order(order_2, 'nakia')
    orders = order_model.get_all_orders()
    created_order_1['customer'] = 'thanos'
    created_order_2['customer'] = 'nakia'
    assert created_order_1 in orders and created_order_2 in orders
    cursor = database_connection.cursor()
    cursor.execute('DELETE FROM order_items WHERE item = %s', ('pillao', ))
    cursor.execute('DELETE FROM order_items WHERE item = %s', ('beef', ))
    cursor.execute('DELETE FROM orders WHERE customer = %s', ('thanos', ))
    cursor.execute('DELETE FROM orders WHERE customer = %s', ('nakia', ))
    database_connection.commit()
    database_connection.close()


def test_model_can_add_new_menu_item_to_menu_table_in_database(database_connection):
    menu_model = Menu()
    item = {'item': 'chicken', 'unit': 'piece', 'rate': 10000}
    menu_model.add_menu_item(item)
    cursor = database_connection.cursor()
    cursor.execute('SELECT item, unit, rate FROM menu')
    added_item = cursor.fetchone()
    assert added_item[0] == item['item']
    assert added_item[1] == item['unit']
    assert added_item[2] == item['rate']
    cursor.execute('DELETE FROM menu WHERE item = %s', ('chicken', ))
    database_connection.commit()
    database_connection.close()


def test_model_can_return_list_of_food_items_in_the_menu(database_connection):
    menu_model = Menu()
    item_1 = {'item': 'chapati', 'unit': 'piece', 'rate': 1000}
    item_2 = {'item': 'samosa', 'unit': 'pack', 'rate': 5000}
    menu_model.add_menu_item(item_1)
    menu_model.add_menu_item(item_2)
    menu = menu_model.get_food_menu()
    assert item_1 in menu and item_2 in menu
    cursor = database_connection.cursor()
    cursor.execute('DELETE FROM menu WHERE item = %s', ('chapati', ))
    cursor.execute('DELETE FROM menu WHERE item = %s', ('samosa', ))
    database_connection.commit()
    database_connection.close()


def test_model_raises_exception_when_menu_table_is_empty(database_connection):
    menu_model = Menu()
    with pytest.raises(Exception):
        menu_model.get_food_menu()
