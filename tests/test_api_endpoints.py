import pytest
from fastfoodfast import app


@pytest.fixture
def test_client():
    return app.test_client()


def test_index_page_contains_welcome_message(test_client):
    response = test_client.get('/')
    assert b'Welcome to Fast-Food-Fast!' in response.data
