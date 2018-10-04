"""
Validation functions for checking the correctness of data sent to the API.
"""


def validate_status_data(status_data):
    assert isinstance(status_data, dict), 'Enter a dictionary to update status'
    assert 'status' in status_data, 'Specify status in your request data'
    status_data['status'] = status_data['status'].strip().lower()
    if status_data['status'] not in ['new', 'processing', 'cancelled', 'complete']:
        raise Exception('Specify status as new, processing, cancelled, or complete')
    assert len(status_data) == 1, 'Redundant data in status request'


def validate_order_item(item):
        """Checks that an item (dictionary) in an order items list is valid"""
        try:
            dict(item)
            assert 'item' in item and isinstance(item['item'], str)
            item['item'] = item['item'].strip() # remove leading and trailing spaces
            assert len(item['item']) != 0
            for c in item['item']:
                assert c.isalnum() or c.isspace()
            assert 'quantity' in item and float(item['quantity'])
            assert float(item['quantity']) > 0 # quantity cannot be zero or negative
            assert 'cost' in item and float(item['cost'])
            assert float(item['cost']) > 0 # cost cannot be negative
            assert len(item) == 3
            return True
        except (AssertionError, TypeError, ValueError):
            return False
    

def validate_order(order):
        """Returns True if the data for an order is valid, False otherwise"""
        try:
            assert isinstance(order, dict)
            assert 'items' in order
            assert isinstance(order['items'], list)
            for item in order['items']:
                assert validate_order_item(item)
            
            if len(order) == 2:
                assert 'status' in order or 'total-cost' in order or 'order-id' in order
            elif len(order) == 3:
                condition_1 = 'status' in order and 'total-cost' in order
                condition_2 = 'status' in order and 'order-id' in order
                condition_3 = 'total-cost' in order and 'order-id' in order
                assert condition_1 or condition_2 or condition_3
            elif len(order) == 4:
                assert 'status' in order and 'total-cost' in order and 'order-id' in order
            elif len(order) > 4:
                return False
            
            if 'status' in order:
                order['status'] = order['status'].strip().lower()
                assert order['status'] in ['pending', 'accepted', 'complete']
            if 'total-cost' in order:
                assert float(order['total-cost'])
            if 'order-id' in order:
                assert float(order['order-id'])
            return True
        except:
            return False


def validate_user(user):
    try:
        assert isinstance(user, dict)
        assert 'username' in user
        user['username'] = user['username'].strip()
        assert len(user['username']) != 0
        assert 'password' in user and isinstance(user['password'], str)
        user['password'] = user['password'].strip()
        assert len(user['password']) != 0
        return True
    except:
        return False


def validate_menu_item(menu_item):
    assert isinstance(menu_item, dict), 'Invalid format for menu item, it should be a dictionary'
    assert 'item' in menu_item and isinstance(menu_item['item'], str), 'Define item as a string'
    menu_item['item'] = menu_item['item'].strip()
    if len(menu_item['item']) == 0:
        raise Exception('Item name cannot be empty!')
    for c in menu_item['item']:
        if not c.isalnum() and not c.isspace():
            raise Exception('Item name can only contain letters, numbers and spaces')
    assert 'unit' in menu_item and isinstance(menu_item['unit'], str), 'Specify correct item unit'
    assert 'rate' in menu_item and float(menu_item['rate']), 'Specify correc item rate'
    assert len(menu_item) == 3, 'Redundant data specified for menu item'
