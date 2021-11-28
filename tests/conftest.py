import pytest
from app import create_app

test_app = create_app(env='testing')

@pytest.fixture
def app():
    yield test_app

@pytest.fixture
def client(app):
    return app.test_client()