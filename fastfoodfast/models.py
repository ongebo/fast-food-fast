import psycopg2, uuid, os
from .validation import Validation
from werkzeug.security import generate_password_hash, check_password_hash


validator = Validation()


class Model:
    """Base class for the model classes"""
    def connect_to_db(self):
        self.conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        self.cursor = self.conn.cursor()


class User(Model):
    def register_user(self, user_data):
        """Adds a new user to the database"""
        user_data = validator.validate_user_data(user_data)
        self.connect_to_db()
        validator.ensure_user_not_existent(user_data['username'], self.cursor)
        password_hash = generate_password_hash(user_data['password'], method='sha256')
        self.cursor.execute(
            'INSERT INTO users (username, password, email, tel, admin) VALUES (%s, %s, %s, %s, %s)',
            (
                user_data['username'], password_hash, user_data['email'],
                user_data['telephone'], False
            )
        )
        self.conn.commit()
        self.conn.close()
    
    def get_user(self, username):
        """Retrieves a user from the database"""
        if not isinstance(username, str):
            raise Exception('Username must be a string')
        self.connect_to_db()
        self.cursor.execute(
            'SELECT username, password FROM users WHERE username = %s',
            (username, )
        )
        result = self.cursor.fetchone()
        self.conn.close()
        if not result:
            raise Exception('No user with name {} exists!'.format(username))
        user = dict()
        user['username'] = result[0]
        user['password'] = result[1]
        return user


class Order(Model):
    def create_order(self, order, customer):
        """Adds a new order to the database"""
        validator.validate_order(order)
        total_cost = 0
        for item in order['items']:
            item['item'] = item['item'].strip() # remove leading and lagging spaces
            total_cost += float(item['cost'])
        order_id = str(uuid.uuid4())[:8] # random public ID for security
        new_order = {
            'items': order['items'], 'status': 'new',
            'total-cost': total_cost, 'order-id': order_id
        }
        # add order to the database
        self.connect_to_db()
        self.cursor.execute(
            'INSERT INTO orders (public_id, customer, status, total_cost) VALUES (%s, %s, %s, %s)',
            (order_id, customer, 'new', total_cost)
        )
        self.cursor.execute(
            'SELECT id FROM orders WHERE public_id = %s', (order_id, )
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
    
    def get_order_history(self, customer):
        """Returns a list of all orders made by a user"""
        self.connect_to_db()
        self.cursor.execute(
            'SELECT id, public_id, status, total_cost FROM orders WHERE customer = %s',
            (customer, )
        )
        records = self.cursor.fetchall()
        if not records:
            raise Exception('No orders made by {}!'.format(customer))
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
        """Fetches all orders from the database"""
        self.connect_to_db()
        self.cursor.execute(
            'SELECT id, public_id, customer, status, total_cost FROM orders'
        )
        records = self.cursor.fetchall()
        if not records:
            raise Exception('No orders available!')
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
        """"Fetches a specific order from the database with public_id = <order_id>"""
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
        """Updates the status of an order with <order_id>"""
        if not self.get_specific_order(order_id):
            raise Exception('The specified order does not exist!')
        validator.validate_status_data(status)
        self.connect_to_db()
        self.cursor.execute(
            'UPDATE orders SET status = %s WHERE public_id = %s',
            (status['status'], order_id)
        )
        self.conn.commit()
        self.conn.close()
    
    def is_admin(self, user):
        """Returns True if user is admin, False otherwise"""
        self.connect_to_db()
        self.cursor.execute('SELECT admin FROM users WHERE username = %s', (user, ))
        value = self.cursor.fetchone()[0]
        self.conn.close()
        return value


class Menu(Model):
    def get_food_menu(self):
        """Returns all food items in the menu"""
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
        """Adds a new item to the food menu"""
        validator.validate_menu_item(menu_item)
        self.connect_to_db()
        self.cursor.execute(
            'INSERT INTO menu (item, unit, rate) VALUES (%s, %s, %s)',
            (menu_item['item'], menu_item['unit'], menu_item['rate'])
        )
        self.conn.commit()
        self.conn.close()
