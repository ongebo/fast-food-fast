"""
Validation code for checking the correctness of data sent to the API.
"""
import re


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
    
    def validate_order(self, order):
        assert isinstance(order, dict), 'Order data must be represented in JSON!'
        assert 'items' in order, 'items to order not specified!'
        assert isinstance(order['items'], list), 'Specify order items as a list'
        assert len(order['items']) > 0, 'Items list empty!'
        for item in order['items']:
            self.validate_order_item(item)
    
    def validate_order_item(self, item):
        assert isinstance(item, dict), 'Specify order item as a dictionary!'
        assert 'item' in item, 'Specify item name!'
        assert 'quantity' in item, 'Item quantity not specified!'
        assert 'cost' in item, 'Item cost not specified!'
        assert isinstance(item['item'], str), 'Item name must be a string!'
        pattern = re.compile(r'[a-zA-Z]{2,30}( [a-zA-Z]{2,30})*$')
        assert pattern.match(item['item'].strip()), 'Invalid item specified!'
        assert float(item['quantity']), 'Specify quantity as a number!'
        assert float(item['quantity']) > 0, 'Item quantity cannot be negative!'
        assert float(item['cost']), 'Specify item cost as a number!'
        assert float(item['cost']) > 0, 'Item cost cannot be negative!'
        assert len(item) == 3, 'Redundant fields in request data!'
    
    def validate_user_data(self, user_data):
        assert isinstance(user_data, dict), 'Specify registration data in JSON format!'
        self.ensure_required_fields_present(user_data)
        self.validate_username(user_data['username'])
        self.validate_email_address(user_data['email'])
        self.validate_telephone_number(user_data['telephone'])
        self.validate_password(user_data['password'])
        return self.process_user_data(user_data)
    
    def ensure_required_fields_present(self, user_data):
        assert 'username' in user_data, 'Username not specified!'
        assert 'password' in user_data, 'Password not specified!'
        assert 'email' in user_data, 'Email address not specified!'
        assert 'telephone' in user_data, 'Phone number not specified!'
    
    def validate_username(self, username):
        assert isinstance(username, str), 'Username must be a string!'
        username_pattern = re.compile(r'[a-zA-Z]{3,30}( [a-zA-Z]{3,30})*$')
        error_message = (
            'Username can only contain letters. Names (firstname/lastname) are separated'
            ' by single spaces and each must contain atleast three letters!'
        )
        assert username_pattern.match(username.strip()), error_message
    
    def validate_email_address(self, email_address):
        assert isinstance(email_address, str), 'Email address must be a string!'
        pattern = re.compile(r'[a-zA-Z0-9]+@[a-zA-Z]+\.[a-zA-Z]{2,3}((\.[a-zA-Z]{2,3})+)?$')
        assert pattern.match(email_address.strip()), 'Email address is invalid!'
    
    def validate_telephone_number(self, telephone_number):
        assert isinstance(telephone_number, str), 'Telephone contact must be a string!'
        telephone_pattern = re.compile(r'\+[0-9]{1,3}-[0-9]{3}-[0-9]{6}$')
        assert telephone_pattern.match(telephone_number.strip()), 'Telephone contact is invalid!'
    
    def validate_password(self, password):
        assert isinstance(password, str), 'Password must be a string!'
        checks = {'a-z': str.islower, 'A-Z': str.isupper, '0-9': str.isdigit}
        for character in password:
            for key, check in checks.items():
                if check(character):
                    del checks[key]
                    break # move onto the next character
        password_is_valid = len(checks) == 0 and 6 <= len(password) <= 12
        error_message = (
            'Password must contain atleast one lowercase letter, one uppercase letter,'
            ' a digit and be 6 to 12 characters long!'
        )
        assert password_is_valid, error_message
    
    def process_user_data(self, user_data):
        user_data['username'] = user_data['username'].strip()
        user_data['email'] = user_data['email'].strip()
        user_data['telephone'] = user_data['telephone'].strip()
        return user_data
    
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
