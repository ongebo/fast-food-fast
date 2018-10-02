import pytest, psycopg2
from fastfoodfast.models import User
from werkzeug.security import generate_password_hash, check_password_hash


@pytest.fixture
def database_connection():
    conn = psycopg2.connect(
        database='fffdb',
        user='ongebo',
        password='nothing',
        host='127.0.0.1',
        port='5432'
    )
    return conn


def test_model_correctly_registers_new_user_to_the_database(database_connection):
    user_model = User()
    new_user = user_model.register_user({'username': 'customer', 'password': 'p@$$word'})
    assert new_user['username'] == 'customer'
    assert check_password_hash(new_user['password'], 'p@$$word')
    assert new_user['admin'] == False
    cursor = database_connection.cursor()
    cursor.execute('SELECT username, password FROM users WHERE username = \'customer\'')
    result = cursor.fetchall()
    assert 'customer' in result[0]
    assert check_password_hash(result[0][1], 'p@$$word')
    cursor = database_connection.cursor()
    cursor.execute('DELETE FROM users WHERE username = \'customer\'')
    database_connection.commit()
    database_connection.close()


def test_model_raises_exception_when_registering_with_existent_username(database_connection):
    user_model = User()
    user = {'username': 'customer', 'password': 'p@$$word'}
    user_model.register_user(user)
    with pytest.raises(Exception):
        user_model.register_user(user) # try to re-register user
    cursor = database_connection.cursor()
    cursor.execute('DELETE FROM users WHERE username = \'customer\'')
    database_connection.commit()
    database_connection.close()


def test_model_raises_exception_given_incorrect_user_data_for_registration(database_connection):
    user_model = User()
    incorrect_data = {'username': ' ', 'password': 786}
    with pytest.raises(Exception):
        user_model.register_user(incorrect_data)


def test_model_can_get_a_specific_user_by_username_from_db(database_connection):
    user_model = User()
    database_connection.cursor().execute(
        "INSERT INTO users (username, password, admin) VALUES ('Thor', 'asgard', 'f')"
    )
    database_connection.commit()
    user = user_model.get_user('Thor')
    assert user['username'] == 'Thor'
    assert user['password'] == 'asgard'
    database_connection.cursor().execute(
        "DELETE FROM users WHERE username='Thor'"
    )
    database_connection.commit()
    database_connection.close()


def test_model_raises_exception_when_retrieving_non_existent_user():
    user_model = User()
    with pytest.raises(Exception):
        user_model.get_user('Non-existent user!')
    with pytest.raises(Exception):
        user_model.get_user(34)
