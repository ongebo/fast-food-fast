import pytest
from fastfoodfast import app
from fastfoodfast.models import Order


@pytest.fixture
def test_client():
    return app.test_client()


def reset_orders_list():
    Order.orders = list()


def test_index_page_contains_welcome_message(test_client):
    response = test_client.get('/')
    assert 'Welcome to Fast-Food-Fast!' in response.get_json()


def test_api_returns_empty_orders_list_when_no_order_has_been_created(test_client):
    response = test_client.get('/api/v1/orders')
    data = response.get_json()
    assert 'orders' in data and data['orders'] == []
    assert response.status_code == 200


def test_api_returns_created_order_in_orders_list(test_client):
    response_1 = test_client.post('/api/v1/orders', json={'items': []})
    response_2 = test_client.get('/api/v1/orders')
    assert response_1.get_json() in response_2.get_json()['orders']
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
    reset_orders_list()


def test_api_returns_404_for_a_wrong_order_id(test_client):
    response = test_client.get('/api/v1/orders/0')
    assert response.status_code == 404
    assert '404 - The requested resource does not exist' in response.get_json()