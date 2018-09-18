import pytest
from fastfoodfast.models import Order, OrderNotFound


@pytest.fixture
def order_model():
    return Order()


def add_order(id):
    order = {'order-id': id, 'status': 'pending'}
    order_items = [
        {'item': 'Pizza', 'quantity': 1, 'cost': 15000},
        {'item': 'Salad', 'quantity': 2, 'cost': 10000}
    ]
    total_cost = 0
    for item in order_items:
        total_cost += item['cost']
    order['items'] = order_items
    order['total-cost'] = total_cost
    Order.orders.append(order)
    return order


def delete_order(id):
    for order in Order.orders:
        if order['order-id'] == id:
            del order


def test_returns_correct_list_of_orders(order_model):
    assert order_model.get_all() == Order.orders


def test_order_model_can_return_order_with_correct_id(order_model):
    order = add_order(3)
    retrieved_order = order_model.get_order(3)
    assert order == retrieved_order
    delete_order(3)


def test_order_model_raises_type_error_given_an_id_which_is_not_an_integer(order_model):
    with pytest.raises(TypeError):
        order_model.get_order('3')
    with pytest.raises(TypeError):
        order_model.get_order(23.45)


def test_order_model_raises_order_not_found_if_requested_order_does_not_exist(order_model):
    with pytest.raises(OrderNotFound):
        order_model.get_order(34)


def test_order_model_returns_true_for_valid_order_items(order_model):
    order_item_1 = {'item': 'hamburger', 'quantity': 2, 'cost': 10000}
    order_item_2 = {'item': 'pizza', 'quantity': 0.5, 'cost': 10000.4}
    assert order_model.validate_order_item(order_item_1)
    assert order_model.validate_order_item(order_item_2)


def test_order_model_returns_false_for_invalid_order_items(order_model):
    order_item_1 = {'item': 45, 'quantity': 'alpha', 'cost': 'Ugx 2544'}
    order_item_2 = {}
    order_item_3 = ['pizza', 4, 67]
    assert order_model.validate_order_item(order_item_1) == False
    assert order_model.validate_order_item(order_item_2) == False
    assert order_model.validate_order_item(order_item_3) == False
