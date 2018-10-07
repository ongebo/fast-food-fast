import psycopg2, os, sys
from werkzeug.security import generate_password_hash


def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute(
        """
        DROP TABLE IF EXISTS users;
        CREATE TABLE users (
            Id SERIAL PRIMARY KEY,
            Username VARCHAR(80) NOT NULL,
            Password VARCHAR(80) NOT NULL,
            Admin BOOLEAN NOT NULL
        );
        """
    )
    cursor.execute(
        """
        INSERT INTO users (username, password, admin) VALUES (%s, %s, %s)
        """,
        ('admin', generate_password_hash('administrator', method='sha256'), True)
    )
    cursor.execute(
        """
        DROP TABLE IF EXISTS menu;
        CREATE TABLE menu (
            Id SERIAL PRIMARY KEY,
            Item VARCHAR(80),
            Unit VARCHAR(80),
            Rate real
        );
        """
    )
    cursor.execute(
        """
        DROP TABLE IF EXISTS orders CASCADE;
        CREATE TABLE orders (
            Id SERIAL PRIMARY KEY,
            Public_Id VARCHAR(80),
            Customer VARCHAR(80),
            Status VARCHAR(80),
            Total_Cost REAL
        );
        """
    )
    cursor.execute(
        """
        DROP TABLE IF EXISTS order_items;
        CREATE TABLE order_items (
            Id SERIAL PRIMARY KEY,
            Order_Id SERIAL REFERENCES orders(Id),
            Item VARCHAR(80),
            Quantity REAL,
            Cost REAL
        );
        """
    )
    conn.commit()
    conn.close()


def setup_testdb():
    conn = psycopg2.connect(
        database='testdb',
        user='ongebo',
        password='nothing',
        host='127.0.0.1',
        port='5432'
    )
    create_tables(conn)


def main():
    if len(sys.argv) == 2 and sys.argv[1] == 'testdb':
        setup_testdb()
        print('Test database tables successfully setup...')
        return
    conn = None
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    except:
        print('Could not establish connection to database...')
        return
    create_tables(conn)
    print('Database tables successfully setup...')


if __name__ == '__main__':
    main()