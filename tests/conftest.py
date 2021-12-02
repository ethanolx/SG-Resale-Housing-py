import pytest
from app import create_app

test_app = create_app(env='testing')


@pytest.fixture
def app():
    with test_app.app_context():
        yield test_app


@pytest.fixture
def client(app):
    return app.test_client()
