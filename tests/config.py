from pvarpc2web.config import DefaultConfig


class TestConfig(DefaultConfig):
    TESTING = True
    PVA_RPC_TIMEOUT = 1
    CHLIST_PATH = ''
