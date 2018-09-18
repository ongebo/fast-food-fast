import pytest
from fastfoodfast import app


@pytest.fixture
def test_client():
    return app.test_client()


def test_index_page_contains_welcome_message(test_client):
    response = test_client.get('/')
    assert 'Welcome to Fast-Food-Fast!' in response.get_json()


def test_api_returns_empty_orders_list_when_no_order_has_been_created(test_client):
    response = test_client.get('/api/v1/orders')
    data = response.get_json()
    assert 'orders' in data and data['orders'] == []
    assert response.status_code == 200
