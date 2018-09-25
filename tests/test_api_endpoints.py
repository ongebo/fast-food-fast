"""
This module contains functional tests for the flask application (fastfoodfast).
Run the tests using the pytest testing framework, by navigating to the project's
root folder, and entering the command 'pytest' in the terminal.
"""
import pytest
from fastfoodfast import app
from fastfoodfast.models import Order, Menu


@pytest.fixture
def test_client():
    return app.test_client()


def reset_orders_list():
    Order.orders = list()


def reset_menu():
    Menu.menu_items = list()


def test_index_page_contains_welcome_message(test_client):
    response = test_client.get('/')
    assert 'Welcome to Fast-Food-Fast!' in response.get_json()
    assert response.status_code == 200


def test_api_returns_empty_orders_list_when_no_order_has_been_created(test_client):
    response = test_client.get('/api/v1/orders')
    data = response.get_json()
    assert 'orders' in data and data['orders'] == []
    assert response.status_code == 200


def test_api_returns_created_order_in_orders_list(test_client):
    response_1 = test_client.post('/api/v1/orders', json={'items': []})
    response_2 = test_client.get('/api/v1/orders')
    assert response_1.get_json() in response_2.get_json()['orders']
    assert response_1.status_code == 201
    assert response_2.status_code == 200
    reset_orders_list()


def test_api_correctly_creates_a_new_order(test_client):
    order_items = [
        {'item': 'hamburger', 'quantity': 2, 'cost': 12000},
        {'item': 'pizza', 'quantity': 1, 'cost': 12000}
    ]
    response = test_client.post('/api/v1/orders', json={'items': order_items})
    data = response.get_json()
    reset_orders_list()
    assert 'items' in data and data['items'] == order_items
    assert 'status' in data and data['status'] == 'pending'
    assert 'total-cost' in data and data['total-cost'] == 24000
    assert 'order-id' in data
    assert response.status_code == 201


def test_api_returns_help_text_incase_of_bad_order_format_in_request(test_client):
    response = test_client.post('/api/v1/orders', json={'items': [1, 2]})
    data = response.get_json()
    reset_orders_list()
    assert 'help' in data and 'order should have the format:' in data['help']
    assert response.status_code == 400


def test_api_can_return_a_specific_order_that_exists(test_client):
    response_1 = test_client.post('/api/v1/orders', json={'items': []})
    response_2 = test_client.get('/api/v1/orders/{}'.format(response_1.get_json()['order-id']))
    assert response_1.get_json() == response_2.get_json()
    assert response_2.status_code == 200
    assert response_1.status_code == 201
    reset_orders_list()


def test_api_returns_404_for_a_wrong_order_id(test_client):
    response_1 = test_client.get('/api/v1/orders/0')
    response_2 = test_client.put('/api/v1/orders/45', json={'status': 'accepted'})
    assert response_1.status_code == 404
    assert response_2.status_code == 404
    assert '404 - The requested resource does not exist' in response_1.get_json()


def test_api_can_update_status_of_a_created_order(test_client):
    response_1 = test_client.post('/api/v1/orders', json={'items': []})
    order_id = response_1.get_json()['order-id']
    response_2 = test_client.put('/api/v1/orders/{}'.format(order_id), json={'status': 'accepted'})
    response_3 = test_client.get('/api/v1/orders/{}'.format(order_id))
    assert response_3.get_json()['status'] == 'accepted'
    assert response_1.status_code == 201
    assert response_2.status_code == 200
    assert response_3.status_code == 200
    reset_orders_list()


def test_api_returns_error_message_for_wrong_order_update_data(test_client):
    response_1 = test_client.post('/api/v1/orders', json={'items': []})
    order_id = response_1.get_json()['order-id']
    response_2 = test_client.put('/api/v1/orders/{}'.format(order_id), json={'status': 'invalid'})
    assert response_1.status_code == 201
    assert response_2.status_code == 400
    assert 'Bad Request!' in response_2.get_json()
    reset_orders_list()


def test_api_deletes_an_order_with_specific_id(test_client):
    response_1 = test_client.post('/api/v1/orders', json={'items': []})
    order_id = response_1.get_json()['order-id']
    response_2 = test_client.delete('/api/v1/orders/{}'.format(order_id))
    assert response_1.status_code == 201
    assert response_2.status_code == 204


def test_api_returns_error_message_when_deleting_a_non_existent_order(test_client):
    response = test_client.delete('/api/v1/orders/34')
    assert response.status_code == 404
    assert '404 - The requested resource does not exist' in response.get_json()


def test_api_correctly_creates_new_menu_items(test_client):
    valid_item_1 = {'item': 'Chicken', 'unit': 'piece', 'rate': 5000}
    valid_item_2 = {'rate': 7000, 'item': 'hamburger'}
    response_1 = test_client.post('/api/v1/menu-items', json=valid_item_1)
    response_2 = test_client.post('/api/v1/menu-items', json=valid_item_2)
    assert response_1.status_code == 201
    assert response_2.status_code == 201
    assert response_1.get_json()['item-id'] == 1
    assert response_2.get_json()['item-id'] == 2
    reset_menu()


def test_api_returns_400_given_wrong_request_data_to_create_menuitem(test_client):
    response = test_client.post('/api/v1/menu-items', json={})
    assert response.status_code == 400
    assert 'Invalid menu item data' in response.get_json()['help']


def test_api_can_return_all_food_menu_items(test_client):
    response_1 = test_client.post('/api/v1/menu-items', json={'item': 'chicken', 'rate': 5000})
    assert response_1.status_code == 201
    response_2 = test_client.get('/api/v1/menu-items')
    assert response_2.status_code == 200
    assert response_1.get_json() in response_2.get_json()['menu-items']
    reset_menu()
