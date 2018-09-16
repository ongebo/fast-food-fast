class OrderNotFound(Exception):
    pass


class Order:
    orders = list()

    def get_all(self):
        return Order.orders
