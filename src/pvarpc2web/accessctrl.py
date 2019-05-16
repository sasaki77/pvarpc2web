import yaml


class AccessCtrl(object):

    def __init__(self):
        self._initialized = False

    def read_config(self, path):
        with open(path) as f:
            data = yaml.safe_load(f)
        self._allow = data.get('allow', [])
        self._deny = data.get('deny', [])
        self._initialized = True

    def check(self, ch_name):
        if not self._initialized:
            return True

        allow = False
        deny = False

        if ch_name in self._allow:
            allow = True

        if ch_name in self._deny:
            deny = True

        return (allow and not deny)


accessctrl = AccessCtrl()
