import pytest
from app import create_app

@pytest.fixture
def app():
    yield create_app(env='testing')

@pytest.fixture
def client(app):
    return app.test_client()