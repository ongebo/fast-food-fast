import psycopg2


def get_database_credentials():
    while True:
        try:
            db = input('Database name: ')
            username = input('User: ')
            password = input('Password: ')
            conn = psycopg2.connect(
                database=db,
                user=username,
                password=password,
                host='127.0.0.1',
                port='5432'
            )
            print('Successfully connected to database...\n')
            return conn
        except:
            print('\nWrong Credentials, try again.\n')


def main():
    conn = get_database_credentials()
    cursor = conn.cursor()
    cursor.execute(
        """
        DROP TABLE IF EXISTS users;
        CREATE TABLE users (
            Id SERIAL PRIMARY KEY,
            Username VARCHAR(80) NOT NULL,
            Password VARCHAR(80) NOT NULL
        );
        """
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
    print('Database tables successfully setup...')


if __name__ == '__main__':
    main()
