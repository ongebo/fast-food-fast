import psycopg2
from .validation import validate_user
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