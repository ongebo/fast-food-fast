"""
Unit Tests for the Application Models Defined in fastfoodfast/models.py
"""
import pytest
from fastfoodfast.models import Order, OrderNotFound, BadRequest, Menu
from fastfoodfast.validation import validate_order_item, validate_order


@pytest.fixture
def order_model():
    return Order()


@pytest.fixture
def menu_model():
    return Menu()


@pytest.fixture
def valid_order_items():
    order_item_1 = {'item': 'hamburger', 'quantity': 2, 'cost': 10000}
    order_item_2 = {'item': 'pizza', 'quantity': 0.5, 'cost': 10000.4}
    return [order_item_1, order_item_2]


@pytest.fixture
def invalid_order_items():
    order_item_1 = {'item': 45, 'quantity': 'alpha', 'cost': 'Ugx 2544'}
    order_item_2 = {}
    order_item_3 = ['pizza', 4, 67]
    return [order_item_1, order_item_2, order_item_3]


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
    for x in range(len(Order.orders)):
        if Order.orders[x]['order-id'] == id:
            del Order.orders[x]


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


def test_validation_returns_true_for_valid_order_items(order_model, valid_order_items):
    order_item_1 = valid_order_items[0]
    order_item_2 = valid_order_items[1]
    assert validate_order_item(order_item_1)
    assert validate_order_item(order_item_2)


def test_validation_returns_false_for_invalid_order_items(order_model, invalid_order_items):
    order_item_1 = invalid_order_items[0]
    order_item_2 = invalid_order_items[1]
    order_item_3 = invalid_order_items[2]
    assert validate_order_item(order_item_1) == False
    assert validate_order_item(order_item_2) == False
    assert validate_order_item(order_item_3) == False


def test_validation_returns_true_for_valid_orders(order_model, valid_order_items):
    order_1 = {'items': valid_order_items}
    order_2 = {'items': valid_order_items, 'status': 'pending', 'total-cost': 45000}
    order_3 = {'items': valid_order_items, 'order-id': 5}
    assert validate_order(order_1)
    assert validate_order(order_2)
    assert validate_order(order_3)


def test_validation_returns_false_for_invalid_orders(order_model, invalid_order_items):
    order_1 = {'items': invalid_order_items[0], 'status': 'accepted', 'total-cost': 45336, 'order-id': 45}
    order_2 = {'items': invalid_order_items[1], 'total-cost': 765}
    order_3 = {'items': invalid_order_items[2]}
    assert validate_order(order_1) == False
    assert validate_order(order_2) == False
    assert validate_order(order_3) == False


def test_that_order_model_correctly_creates_new_orders(order_model, valid_order_items):
    order_1 = {'items': valid_order_items}
    order_2 = {'items': valid_order_items, 'status': 'pending', 'total-cost': 45000}
    order_3 = {'items': valid_order_items, 'order-id': 5}
    result_1 = order_model.create_order(order_1)
    result_2 = order_model.create_order(order_2)
    result_3 = order_model.create_order(order_3)

    total_cost = 0
    for item in valid_order_items:
        total_cost += float(item['cost'])
    assert result_1['total-cost'] == total_cost
    assert result_2['total-cost'] == total_cost
    assert result_3['total-cost'] == total_cost
    assert 'status' in result_1 and result_1['status'] == 'pending'
    assert 'status' in result_2 and result_2['status'] == 'pending'
    assert 'status' in result_3 and result_3['status'] == 'pending'
    assert 'order-id' in result_1 and result_1['order-id'] == 0
    assert 'order-id' in result_2 and result_2['order-id'] == 1
    assert 'order-id' in result_3 and result_3['order-id'] == 2
    assert result_1 in Order.orders
    assert result_2 in Order.orders
    assert result_3 in Order.orders
    Order.orders = list()


def test_order_model_raises_bad_request_given_bad_orders_to_create(order_model, invalid_order_items):
    order_1 = {'items': invalid_order_items[0], 'status': 'accepted', 'total-cost': 45336, 'order-id': 45}
    order_2 = {'items': invalid_order_items[1], 'total-cost': 765}
    order_3 = {'items': invalid_order_items[2]}
    with pytest.raises(BadRequest):
        order_model.create_order(order_1)
        order_model.create_order(order_2)
        order_model.create_order(order_3)


def test_that_order_model_correctly_updates_an_order(order_model, valid_order_items):
    created_order = order_model.create_order({'items': valid_order_items})
    order_model.update_order_status(created_order['order-id'], {'status': 'accepted'})
    assert created_order['status'] == 'accepted'
    Order.orders = list()


def test_order_model_raises_exception_when_wrong_order_is_used_to_update(order_model, valid_order_items):
    order = order_model.create_order({'items': valid_order_items})
    with pytest.raises(BadRequest):
        order_model.update_order_status(order['order-id'], {1: 2, 2: 3})
    Order.orders = list()


def test_that_order_model_can_delete_an_order_with_specific_id(order_model):
    order_1 = add_order(34)
    order_2 = add_order(45)
    assert Order.orders == [order_1, order_2]
    order_model.delete_order(34)
    order_model.delete_order(45)
    assert Order.orders == []
    assert order_1 != None # the created orders
    assert order_2 != None # are still bound to order_1 and order_2


def test_order_model_raises_exception_when_trying_to_delete_non_existent_order(order_model):
    with pytest.raises(OrderNotFound):
        order_model.delete_order(567)


def test_menu_model_can_create_a_new_menu_item(menu_model):
    menu_item = {'item': 'Chicken', 'unit': 'piece', 'rate': 5000}
    created_item = menu_model.create_menu_item(menu_item)
    assert 'item-id' in created_item and created_item['item-id'] == 1
    assert len(Menu.menu_items) == 1
    assert created_item in Menu.menu_items
    Menu.menu_items = list()


def test_menu_model_raises_exception_when_creating_menu_item_with_bad_argument(menu_model):
    bad_item_1 = {}
    bad_item_2 = 567
    with pytest.raises(Exception):
        menu_model.create_menu_item(bad_item_1)
        menu_model.create_menu_item(bad_item_2)


def test_menu_model_correctly_validates_menu_items(menu_model):
    bad_item_1 = [1, 2, 3]
    bad_item_2 = {'rate': 5000, 'unit': 'pack'}
    valid_item = {'item': 'Pizza', 'rate': 20000}
    assert menu_model.is_valid_menu_item(bad_item_1) == False
    assert menu_model.is_valid_menu_item(bad_item_2) == False
    assert menu_model.is_valid_menu_item(valid_item) == True


def test_menu_model_can_return_all_food_menu_items(menu_model):
    assert menu_model.get_all() == []
    item = menu_model.create_menu_item({'item': 'pizza', 'rate': 20000})
    assert item in menu_model.get_all()
    Menu.menu_items = list()
