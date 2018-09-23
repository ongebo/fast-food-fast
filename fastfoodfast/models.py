"""
Model Classes Responsible for Handling Non-Persistent Data for the Application
"""
class OrderNotFound(Exception):
    pass


class BadRequest(Exception):
    pass


class Order:
    orders = list()

    def get_all(self):
        return Order.orders
    
    def get_order(self, order_id):
        """Returns order with specific order_id if it exists"""
        if not isinstance(order_id, int):
            raise TypeError('The id should be an integer')
        for order in Order.orders:
            if order['order-id'] == order_id:
                return order
        raise OrderNotFound('No order with id {} exists'.format(order_id))
    
    def create_order(self, order):
        """Creates and returns a reference to a new order in the orders list"""
        if self.validate_order(order):
            new_order = dict()
            new_order['items'] = order['items']
            new_order['status'] = 'pending'
            total_cost = 0
            for item in order['items']:
                total_cost += float(item['cost'])
            new_order['total-cost'] = total_cost
            order_id = 0 if len(Order.orders) == 0 else Order.orders[-1]['order-id'] + 1
            new_order['order-id'] = order_id
            Order.orders.append(new_order)
            return new_order
        else:
            raise BadRequest
    
    def update_order_status(self, order_id, new_order):
        """Updates order having id <order_id> with new_order"""
        order_to_update = self.get_order(order_id)
        if 'items' not in new_order:
            new_order['items'] = order_to_update['items'][:] # slice to create a new copy
        if self.validate_order(new_order):
            order_to_update.update(new_order)
            total_cost = 0
            for item in order_to_update['items']:
                total_cost += item['cost']
            order_to_update['total-cost'] = total_cost
        else:
            raise BadRequest
    
    def delete_order(self, order_id):
        """Deletes order with specified order_id, raises exception if it's non-existent"""
        if not isinstance(order_id, int):
            raise TypeError('The id should be an integer')
        order_present = False
        order_index = None
        for order in Order.orders:
            if order['order-id'] == order_id:
                order_present = True
                order_index = Order.orders.index(order)
                break # assuming there's no other order in the list with 'order-id' == order_id
        if order_present:
            del Order.orders[order_index]
        else:
            raise OrderNotFound('No order with id {} exists'.format(order_id))
    
    def validate_order_item(self, item):
        """Checks that an item (dictionary) in an order items list is valid"""
        try:
            dict(item)
            assert 'item' in item and isinstance(item['item'], str)
            assert 'quantity' in item and float(item['quantity'])
            assert 'cost' in item and float(item['cost'])
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
                assert order['status'] in ['pending', 'accepted', 'complete']
            if 'total-cost' in order:
                assert float(order['total-cost'])
            if 'order-id' in order:
                assert float(order['order-id'])
            return True
        except:
            return False


class Menu:
    menu_items = list()

    def create_menu_item(self, menu_item):
        """Adds new food item to the menu, returns reference to it"""
        if self.is_valid_menu_item(menu_item):
            new_item = dict()
            new_item['item'] = menu_item['item']
            new_item['rate'] = menu_item['rate']
            new_item['unit'] = menu_item.get('unit')
            item_id = 1 if len(Menu.menu_items) == 0 else Menu.menu_items[-1]['item-id'] + 1
            new_item['item-id'] = item_id
            Menu.menu_items.append(new_item)
            return new_item
        else:
            raise Exception('Invalid menu item data.')

    def is_valid_menu_item(self, menu_item):
        """Returns True if menu_item argument is valid, False otherwise"""
        try:
            assert isinstance(menu_item, dict)
            assert 'item' in menu_item and isinstance(menu_item['item'], str)
            assert 'rate' in menu_item and float(menu_item['rate'])

            if len(menu_item) == 3:
                assert 'unit' in menu_item or 'item-id' in menu_item
            elif len(menu_item) == 4:
                assert 'unit' in menu_item and 'item-id' in menu_item
            elif len(menu_item) > 4:
                return False
            
            if 'unit' in menu_item:
                assert isinstance(menu_item['unit'], str)
            if 'item-id' in menu_item:
                assert float(menu_item['item-id'])
            return True
        except AssertionError:
            return False
    
    def get_all(self):
        return Menu.menu_items
