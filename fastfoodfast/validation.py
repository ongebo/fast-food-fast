"""
Validation code for checking the correctness of data sent to the API.
"""


class Validation:
    def validate_status_data(self, status_data):
        """
        Checks if request data sent by admin to update the status of an order is valid i.e is
        of the form {'status': '<status>'}, where <status> can only be 'new', 'processing',
        'cancelled' or 'complete'. An exception is raised if the data is invalid.
        """
        assert isinstance(status_data, dict), 'Enter a dictionary to update status'
        assert 'status' in status_data, 'Specify status in your request data'
        status_data['status'] = status_data['status'].strip().lower()
        if status_data['status'] not in ['new', 'processing', 'cancelled', 'complete']:
            raise Exception('Specify status as new, processing, cancelled, or complete')
        assert len(status_data) == 1, 'Redundant data in status request'

    def validate_order_item(self, item):
        """Checks that an item (dictionary) in an order items list is valid"""
        try:
            assert isinstance(item, dict)
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
    
    def validate_order(self, order):
        """Returns True if the data for an order is valid, False otherwise"""
        try:
            assert isinstance(order, dict)
            assert 'items' in order
            assert isinstance(order['items'], list)
            for item in order['items']:
                assert self.validate_order_item(item)
            
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
    
    def validate_user_data(self, user_data):
        assert isinstance(user_data, dict), 'Registration data should be a valid JSON string'
        assert 'username' in user_data, 'Specify a username'
        user_data['username'] = self.process_username(user_data['username'])
        assert 'password' in user_data, 'Specify a password'
        error_message = (
            'password must contain atleast one lowercase letter, one uppercase letter, '
            'a digit and be 6 to 12 characters long'
        )
        assert self.is_valid_password(user_data['password']), error_message
        assert 'email' in user_data, 'Specify an email address'
        assert 'telephone' in user_data, 'Specify telephone contact'
    
    def process_username(self, username):
        assert isinstance(username, str), 'Username must be a string'
        names = username.strip().split()
        for name in names:
            assert len(name) >= 3, 'Each name (first/last name) must contain atleast 3 letters'
            for character in name:
                assert character.isalpha(), (
                    'Username can only contain valid name(s) separated by single spaces'
                )
        for i in range(len(names)):
            names[i] = names[i].capitalize() # capitalize all names
        return ' '.join(names)
    
    def is_valid_password(self, password):
        assert isinstance(password, str), 'Password should be a string'
        checks = {'a-z': str.islower, 'A-Z': str.isupper, '0-9': str.isdigit}
        for character in password:
            for key, check in checks.items():
                if check(character):
                    del checks[key]
                    break # move onto the next character
        return len(checks) == 0 and 6 <= len(password) <= 12
    
    def ensure_user_not_existent(self, username, cursor):
        cursor.execute('SELECT username FROM users')
        for record in cursor.fetchall():
            if username in record:
                raise Exception('{} already exists!'.format(username))
    
    def validate_menu_item(self, menu_item):
        """Ensures that menu item data sent by admin is valid, raises exception if invalid. """
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
