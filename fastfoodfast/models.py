import psycopg2, uuid
from .validation import validate_user, validate_order, validate_menu_item
from werkzeug.security import generate_password_hash, check_password_hash


expected_user_data_format = """
Ensure you follow these rules when providing user sign up data.

1. User data should have the format:
{
    'username': '<username>',
    'password': '<password>'
}
2. <username> and <password> cannot be empty strings
"""


class User:
    def __init__(self, db='fffdb'):
        self.database = db

    def connect_to_db(self):
        self.conn = psycopg2.connect(
            database=self.database,
            user='ongebo',
            password='nothing',
            host='127.0.0.1',
            port='5432'
        )
        self.cursor = self.conn.cursor()

    def register_user(self, user):
        if validate_user(user):
            self.connect_to_db()
            self.cursor.execute('SELECT username FROM users')
            for record in self.cursor.fetchall():
                if user['username'] in record:
                    raise Exception('Username: "{}" already exists!'.format(user['username']))
            new_user = dict()
            new_user['username'] = user['username']
            new_user['password'] = generate_password_hash(user['password'], method='sha256')
            new_user['admin'] = False
            self.cursor.execute(
                'INSERT INTO users (username, password, admin) VALUES (%s, %s, %s)',
                (new_user['username'], new_user['password'], new_user['admin'])
            )
            self.conn.commit()
            self.conn.close()
            return new_user
        else:
            raise Exception(expected_user_data_format)
    
    def get_user(self, username):
        if not isinstance(username, str):
            raise Exception('Username must be a string')
        self.connect_to_db()
        self.cursor.execute(
            "SELECT username, password FROM users WHERE username = '{}'".format(username)
        )
        result = self.cursor.fetchone()
        self.conn.close()
        if not result:
            raise Exception('No user with name "{}" exists'.format(username))
        user = dict()
        user['username'] = result[0]
        user['password'] = result[1]
        return user


class Order:
    def __init__(self, db='fffdb'):
        self.database = db
    
    def connect_to_db(self):
        self.conn = psycopg2.connect(
            database=self.database,
            user='ongebo',
            password='nothing',
            host='127.0.0.1',
            port='5432'
        )
        self.cursor = self.conn.cursor()

    def create_order(self, order, customer):
        """Adds a new order to the database"""
        if validate_order(order):
            new_order = dict()
            new_order['items'] = order['items']
            new_order['status'] = 'pending'
            total_cost = 0
            for item in order['items']:
                total_cost += float(item['cost'])
            new_order['total-cost'] = total_cost
            order_id = str(uuid.uuid4())[:8]
            new_order['order-id'] = order_id

            self.connect_to_db()
            self.cursor.execute(
                "INSERT INTO orders (public_id, customer, status, total_cost) VALUES (%s, %s, %s, %s)",
                (order_id, customer, 'pending', total_cost)
            )
            self.cursor.execute(
                "SELECT id FROM orders WHERE public_id = '{}'".format(order_id)
            )
            primary_key = self.cursor.fetchone()[0]
            for item in new_order['items']:
                self.cursor.execute(
                    'INSERT INTO order_items (order_id, item, quantity, cost) VALUES (%s, %s, %s, %s)',
                    (primary_key, item['item'], item['quantity'], item['cost'])
                )
            self.conn.commit()
            self.conn.close()
            return new_order
        else:
            raise Exception
    
    def get_order_history(self, customer):
        self.connect_to_db()
        self.cursor.execute(
            'SELECT id, public_id, status, total_cost FROM orders WHERE customer = %s',
            (customer, )
        )
        records = self.cursor.fetchall()
        if not records:
            raise Exception('No orders made by {}'.format(customer))
        orders = list()
        for record in records:
            order = dict()
            order['order-id'] = record[1]
            order['status'] = record[2]
            order['total-cost'] = record[3]
            self.cursor.execute(
                'SELECT item, quantity, cost FROM order_items WHERE order_id = %s',
                (record[0], )
            )
            items = list()
            for item in self.cursor.fetchall():
                item = {'item': item[0], 'quantity': item[1], 'cost': item[2]}
                items.append(item)
            order['items'] = items
            orders.append(order)
        return orders
    
    def get_all_orders(self):
        self.connect_to_db()
        self.cursor.execute(
            'SELECT id, public_id, customer, status, total_cost FROM orders'
        )
        records = self.cursor.fetchall()
        if not records:
            raise Exception('No orders available')
        orders = list()
        for record in records:
            order = dict()
            order['order-id'] = record[1]
            order['customer'] = record[2]
            order['status'] = record[3]
            order['total-cost'] = record[4]
            self.cursor.execute(
                'SELECT item, quantity, cost FROM order_items WHERE order_id = %s',
                (record[0], )
            )
            items = list()
            for item in self.cursor.fetchall():
                item = {'item': item[0], 'quantity': item[1], 'cost': item[2]}
                items.append(item)
            order['items'] = items
            orders.append(order)
        self.conn.close()
        return orders
    
    def get_specific_order(self, order_id):
        self.connect_to_db()
        self.cursor.execute('SELECT * FROM orders WHERE public_id = %s', (order_id, ))
        record = self.cursor.fetchone()
        if not record:
            raise Exception('No order with id {} exists!'.format(order_id))
        order = dict()
        items = list()
        self.cursor.execute(
            'SELECT item, quantity, cost FROM order_items WHERE order_id = %s',
            (record[0], )
        )
        for item in self.cursor.fetchall():
            item = {'item': item[0], 'quantity': item[1], 'cost': item[2]}
            items.append(item)
        order['items'] = items
        order['order-id'] = record[1]
        order['customer'] = record[2]
        order['status'] = record[3]
        order['total-cost'] = record[4]
        self.conn.close()
        return order
    
    def update_order_status(self, order_id, status):
        if not self.get_specific_order(order_id):
            raise Exception('The specified order does not exist!')
        if validate_order(status):
            if 'status' not in status:
                raise Exception('No status specified!')
            self.connect_to_db()
            self.cursor.execute(
                'UPDATE orders SET (status = %s) WHERE order_id = %s',
                (status['status'], order_id)
            )
            self.conn.commit()
            self.conn.close()
        else:
            raise Exception('Invalid data!')
    
    def is_admin(self, user):
        self.connect_to_db()
        self.cursor.execute('SELECT admin FROM users WHERE username = %s', (user, ))
        value = self.cursor.fetchone()[0]
        self.conn.close()
        return value


class Menu:
    def __init__(self, db='fffdb'):
        self.database = db

    def connect_to_db(self):
        self.conn = psycopg2.connect(
            database=self.database,
            user='ongebo',
            password='nothing',
            host='127.0.0.1',
            port='5432'
        )
        self.cursor = self.conn.cursor()

    def get_food_menu(self):
        self.connect_to_db()
        self.cursor.execute(
            'SELECT item, unit, rate FROM menu'
        )
        menu_items = self.cursor.fetchall()
        if not menu_items:
            raise Exception('The food menu is empty')
        menu = list()
        for item in menu_items:
            menu.append({'item': item[0], 'unit': item[1], 'rate': item[2]})
        return menu
    
    def add_menu_item(self, menu_item):
        validate_menu_item(menu_item)
        self.connect_to_db()
        self.cursor.execute(
            'INSERT INTO menu (item, unit, rate) VALUES (%s, %s, %s)',
            (menu_item['item'], menu_item['unit'], menu_item['rate'])
        )
        self.conn.commit()
        self.conn.close()
