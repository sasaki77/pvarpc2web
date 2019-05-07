import os

from .context import pvarpc2web


def test_config():
    """Test create_app without passing test config."""
    assert not pvarpc2web.create_app().testing
    assert pvarpc2web.create_app('pvarpc2web.config.TestingConfig').testing


def test_config_from_file():
    base_path = os.path.abspath((os.path.dirname(__file__)))
    config_path = os.path.join(base_path, 'config.cfg')
    os.environ['PVARPC2WEB_CONFIG'] = config_path
    app = pvarpc2web.create_app()
    assert app.config['LOG_MAXBYTE'] == 1
    assert app.config['LOG_COUNT'] == 2
