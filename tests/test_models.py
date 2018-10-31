import pytest, psycopg2, os
from fastfoodfast.models import Users, Orders, Menu
from werkzeug.security import generate_password_hash, check_password_hash


@pytest.fixture
def database_connection():
    database_url = 'postgres://ongebo:nothing@127.0.0.1:5432/testdb'
    os.environ['DATABASE_URL'] = database_url
    conn = psycopg2.connect(database_url)
    return conn


def clean_users(conn, *usernames):
    """Used by tests to reset changes made to users table"""
    cursor = conn.cursor()
    for username in usernames:
        cursor.execute('DELETE FROM users WHERE username = %s', (username, ))


def clean_orders(conn, *customers):
    """Used by tests to revert changes made to database when testing orders management"""
    cursor = conn.cursor()
    for customer in customers:
        cursor.execute('SELECT id FROM orders WHERE customer = %s', (customer, ))
        for order_id in cursor.fetchall():
            cursor.execute('DELETE FROM order_items WHERE order_id = %s', (order_id, ))
        cursor.execute('DELETE FROM orders WHERE customer = %s', (customer, ))


def commit_and_close(conn):
    conn.commit()
    conn.close()


def test_model_correctly_registers_new_user_to_the_database(database_connection):
    user_model = Users()
    user_model.register_user(
        {
            'username': 'customer', 'password': 'P4$$word',
            'email': 'customer@mail.net', 'telephone': '+345-786-569134'
        }
    )
    cursor = database_connection.cursor()
    cursor.execute(
        'SELECT username, password, email, telephone, admin FROM '
        'users WHERE username = %s', ('customer', )
    )
    result = cursor.fetchone()
    assert 'customer' == result[0] and 'customer@mail.net' == result[2]
    assert result[3] == '+345-786-569134' and result[4] == False
    assert check_password_hash(result[1], 'P4$$word')
    clean_users(database_connection, 'customer')
    commit_and_close(database_connection)


def test_model_raises_exception_when_registering_with_existent_username(database_connection):
    user_model = Users()
    user = {
        'username': 'customer', 'password': 'P4$$word',
        'email': 'name@domain.com', 'telephone': '+2-465-231786'
    }
    user_model.register_user(user)
    with pytest.raises(Exception):
        user_model.register_user(user) # try to re-register user
    clean_users(database_connection, 'customer')
    commit_and_close(database_connection)


def test_model_raises_exception_given_incorrect_user_data_for_registration(database_connection):
    user_model = Users()
    incorrect_data = {'username': ' ', 'password': 786}
    with pytest.raises(Exception):
        user_model.register_user(incorrect_data)


def test_model_can_get_a_specific_user_by_username_from_db(database_connection):
    user_model = Users()
    user_model.register_user({
        'username': 'Thor', 'password': 'Asg4rd1an',
        'email': 'thor@asgard.avr', 'telephone': '+23-345-916919'
    })
    user = user_model.get_user('Thor')
    assert user['username'] == 'Thor'
    assert check_password_hash(user['password'], 'Asg4rd1an')
    clean_users(database_connection, 'Thor')
    commit_and_close(database_connection)


def test_model_raises_exception_when_retrieving_non_existent_user(database_connection):
    user_model = Users()
    with pytest.raises(Exception):
        user_model.get_user('Non-existent user!')
    with pytest.raises(Exception):
        user_model.get_user(34)


def test_model_can_add_a_new_order_to_the_database(database_connection):
    order_model = Orders()
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
    cursor.execute('SELECT * FROM order_items WHERE order_id = %s', (result[0], ))
    result = cursor.fetchone()
    assert 'pizza' in result and 1.0 in result and 18000 in result
    clean_orders(database_connection, 'skywalker')
    commit_and_close(database_connection)


def test_model_raises_exception_given_invalid_order_data(database_connection):
    order_model = Orders()
    with pytest.raises(Exception):
        order_model.create_order([], 'jon snow')


def test_model_can_get_order_history_for_a_given_customer(database_connection):
    order_model = Orders()
    order_1 = {'items': [{'item': 'pizza', 'quantity': 2, 'cost': 40000}]}
    order_2 = {'items': [{'item': 'hamburger', 'quantity': 1, 'cost': 10000}]}
    created_order1 = order_model.create_order(order_1, 'luke skywalker')
    created_order2 = order_model.create_order(order_2, 'luke skywalker')
    orders = order_model.get_order_history('luke skywalker')
    assert created_order1 in orders and created_order2 in orders
    clean_orders(database_connection, 'luke skywalker')
    commit_and_close(database_connection)


def test_model_raises_exception_when_no_orders_have_been_made_by_a_user(database_connection):
    order_model = Orders()
    with pytest.raises(Exception):
        order_model.get_order_history('museveni')


def test_model_can_return_all_orders_in_database(database_connection):
    order_model = Orders()
    order_1 = {'items': [{'item': 'pillao', 'quantity': 1, 'cost': 15000}]}
    order_2 = {'items': [{'item': 'beef', 'quantity': 2, 'cost': 10000}]}
    created_order_1 = order_model.create_order(order_1, 'thanos')
    created_order_2 = order_model.create_order(order_2, 'nakia')
    orders = order_model.get_all_orders()
    created_order_1['customer'] = 'thanos'
    created_order_2['customer'] = 'nakia'
    assert created_order_1 in orders and created_order_2 in orders
    clean_orders(database_connection, 'thanos', 'nakia')
    commit_and_close(database_connection)


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
    commit_and_close(database_connection)


def test_model_can_return_list_of_food_items_in_the_menu(database_connection):
    menu_model = Menu()
    item_1 = {'item': 'chapati', 'unit': 'piece', 'rate': 1000}
    item_2 = {'item': 'samosa', 'unit': 'pack', 'rate': 5000}
    menu_model.add_menu_item(item_1)
    menu_model.add_menu_item(item_2)
    menu = menu_model.get_food_menu(return_id=False)
    assert item_1 in menu and item_2 in menu
    cursor = database_connection.cursor()
    cursor.execute('DELETE FROM menu WHERE item = %s', ('chapati', ))
    cursor.execute('DELETE FROM menu WHERE item = %s', ('samosa', ))
    commit_and_close(database_connection)


def test_model_raises_exception_when_menu_table_is_empty(database_connection):
    menu_model = Menu()
    with pytest.raises(Exception):
        menu_model.get_food_menu()


def test_model_can_return_specific_item_from_food_menu(database_connection):
    menu_model = Menu()
    item = {'item': 'Roast Chicken', 'unit': 'Set', 'rate': 15000}
    created_item = menu_model.add_menu_item(item)
    created_item = menu_model.get_specific_menu_item(created_item['id'])
    assert item == created_item
    cursor = database_connection.cursor()
    cursor.execute('DELETE FROM menu WHERE item = %s', ('Roast Chicken', ))
    commit_and_close(database_connection)


def test_model_raises_exception_when_getting_non_existent_item_from_menu(database_connection):
    menu_model = Menu()
    with pytest.raises(Exception):
        menu_model.get_specific_menu_item(-3)


def test_model_updates_a_menu_item(database_connection):
    menu_model = Menu()
    item = {'item': 'Pork', 'unit': 'kilogram', 'rate': 14000}
    created_item = menu_model.add_menu_item(item)
    item['rate'] = 18000 # change rate from 14000 to 18000
    menu_model.update_menu_item(created_item['id'], item)
    updated_item = menu_model.get_specific_menu_item(created_item['id'])
    assert updated_item['rate'] == 18000
    cursor = database_connection.cursor()
    cursor.execute('DELETE FROM menu WHERE item = %s', ('Pork', ))
    commit_and_close(database_connection)


def test_model_can_delete_a_specific_menu_item(database_connection):
    menu_model = Menu()
    item_id = menu_model.add_menu_item({'item': 'Salad', 'unit': 'Plate', 'rate': 7000})['id']
    menu_model.delete_menu_item(item_id)
    with pytest.raises(Exception):
        menu_model.get_specific_menu_item(item_id)
