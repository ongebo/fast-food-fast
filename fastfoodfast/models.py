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
                Order.orders.append(new_order)
                return new_order
            else:
                raise BadRequest
        except:
            raise
