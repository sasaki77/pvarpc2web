from .context import pvarpc2web
from .context import config
from .context import pvaapi


class PvaRpcTimeoutConfig(config.DefaultConfig):
    PVA_RPC_TIMEOUT = 3


def test_set_timeout():
    app = pvarpc2web.create_app(PvaRpcTimeoutConfig)
    assert pvaapi.timeout == 3
