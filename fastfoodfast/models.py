class OrderNotFound(Exception):
    pass


class BadRequest(Exception):
    pass


class Order:
    orders = list()

    def get_all(self):
        return Order.orders
    
    def get_order(self, id):
        if not isinstance(id, int):
            raise TypeError('The id should be an integer')
        for order in Order.orders:
            if order['order-id'] == id:
                return order
        raise OrderNotFound('No order with id {} exists'.format(id))
    
    def create_order(self, order):
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
    
    def update_order_status(self, id, new_order):
        order_to_update = self.get_order(id)
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
    
    def validate_order_item(self, item):
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
