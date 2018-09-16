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
            if order['id'] == id:
                return order
        raise OrderNotFound('No order with id {} exists'.format(id))
    
    def create_order(self, order):
        try:
            if 'items' in order:
                for item in order['items']:
                    assert 'item' in item and 'quantity' in item and 'cost' in item
                new_order = dict()
                total_cost = 0
                for item in order['items']:
                    total_cost += int(item['cost'])
                order_id = None
                if len(Order.orders) == 0:
                    order_id = 0
                else:
                    order_id = Order.orders[-1]['order-id'] + 1
                new_order['order-id'] = order_id
                new_order['items'] = order['items']
                new_order['total-cost'] = total_cost
                new_order['status'] = 'pending'
                Order.orders.append(new_order)
                return new_order
            else:
                raise BadRequest
        except:
            raise
    
    def update_order_status(self, id, new_order):
        order_to_update = self.get_order(id)
        if self.validate_order(new_order):
            order_to_update.update(new_order)
        else:
            raise BadRequest
    
    def validate_order_item(self, item):
        try:
            dict(item)
        except:
            return False
        if 'item' not in item and type(item['item']) != str:
            return False
        elif 'quantity' not in item and not str(item['quantity']).isdigit():
            return False
        elif 'cost' not in item and not str(item['cost']).isdigit():
            return False
        elif len(item) > 3:
            return False
        else:
            return True
    
    def validate_order(self, order):
        try:
            dict(order)
            list(order['items'])
        except:
            return False
        items_list_correct = True
        for item in order['items']:
            if not self.validate_order_item(item): items_list_correct = False
        if not items_list_correct:
            return False
        elif 2 <= len(order) <= 3 and 'status' not in order and 'total-amount' not in order:
            return False
        elif len(order) > 3:
            return False
        else:
            return True
