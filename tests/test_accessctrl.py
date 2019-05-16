import os

from pvarpc2web.accessctrl import AccessCtrl


def test_check():
    accessctrl = AccessCtrl()
    base_path = os.path.abspath((os.path.dirname(__file__)))
    chlist_path = os.path.join(base_path, 'chlist.yml')
    accessctrl.read_config(chlist_path)

    assert accessctrl.check('allowed_ch') is True
    assert accessctrl.check('denied_ch') is False
    assert accessctrl.check('both_ch') is False
    assert accessctrl.check('not_exist') is False
