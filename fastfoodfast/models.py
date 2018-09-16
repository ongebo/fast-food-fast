class OrderNotFound(Exception):
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
