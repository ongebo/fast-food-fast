import pytest
from fastfoodfast.models import Order


@pytest.fixture
def order_model():
    return Order()


def test_returns_correct_list_of_orders(order_model):
    assert order_model.get_all() == Order.orders
