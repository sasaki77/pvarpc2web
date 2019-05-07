import pytest

from .context import pvarpc2web


@pytest.fixture
def app():
    app = pvarpc2web.create_app('pvarpc2web.config.TestingConfig')
    return app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()
