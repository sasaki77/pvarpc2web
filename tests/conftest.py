import os

import pytest

from pvarpc2web.config import DefaultConfig

from .context import pvarpc2web


class TestConfig(DefaultConfig):
    TESTING = True
    PVA_RPC_TIMEOUT = 1
    CHLIST_PATH = ''


@pytest.fixture
def app():
    base_path = os.path.abspath((os.path.dirname(__file__)))
    config_path = os.path.join(base_path, 'chlist.yml')

    TestConfig.CHLIST_PATH = config_path

    app = pvarpc2web.create_app(TestConfig)
    return app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()
