import os
import sys

import pvarpc2web
from pvarpc2web import create_app
from pvarpc2web import config
from pvarpc2web.pvaapi import pvaapi

sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
                )
