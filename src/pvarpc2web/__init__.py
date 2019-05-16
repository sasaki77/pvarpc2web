import os
from logging import Formatter
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask.logging import default_handler
from flask_cors import CORS

from .config import DefaultConfig
from .pvarpc2web import pvarpc2web
from .pvaapi import pvaapi
from .accessctrl import accessctrl


def create_app(config_obj='pvarpc2web.config.DefaultConfig'):
    """Create app for Flask application

    Parameters
    ----------
    object_name: str
        the python path to the config object
        (e.g. pvarpc2web.config.DefaultConfig)
    """

    app = Flask(__name__)

    app.config.from_object(config_obj)
    if 'PVARPC2WEB_CONFIG' in os.environ:
        app.config.from_envvar('PVARPC2WEB_CONFIG')

    app.logger.addHandler(default_handler)

    # settings for rotations handler
    log_path = app.config['LOG_PATH']
    log_byte = app.config['LOG_MAXBYTE']
    log_count = app.config['LOG_COUNT']
    if log_path:
        rhandler = RotatingFileHandler(log_path, maxBytes=log_byte,
                                       backupCount=log_count)
        fmt = Formatter('[%(asctime)s] %(levelname)s in '
                        '%(module)s: %(message)s')
        rhandler.setFormatter(fmt)
        app.logger.addHandler(rhandler)

    # settings for pvAccess
    pvaapi.timeout = app.config['PVA_RPC_TIMEOUT']

    # settings for access control
    if app.config['CHLIST_PATH']:
        accessctrl.read_config(app.config['CHLIST_PATH'])
    else:
        app.logger.info('Run without access control')

    app.register_blueprint(pvarpc2web)

    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    return app
