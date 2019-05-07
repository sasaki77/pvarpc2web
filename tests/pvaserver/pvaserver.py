import math
import time
import argparse
from datetime import datetime

from collections import OrderedDict

import pytz

import pvaccess as pva


ENTITIES = ["long", "float", "string", "str"]
TYPES = {"long": pva.LONG, "float": pva.FLOAT, "string": pva.STRING}


class PvaServer():

    def __init__(self, prefix=""):
        self.srv = pva.RpcServer()
        self.srv.registerService(prefix + "add", self.add)
        self.srv.registerService(prefix + "add_nturi", self.add_nturi)

    def run(self):
        self.srv.startListener()

    def stop(self):
        self.srv.stopListener()

    def add(self, x):
        try:
            lhs = x.getString("lhs")
            rhs = x.getString("rhs")
        except (pva.FieldNotFound, pva.InvalidRequest):
            return pva.PvString("error")

        result = float(lhs) + float(rhs)

        return pva.PvFloat(result)

    def add_nturi(self, x):
        try:
            query = x.getStructure("query")
        except (pva.FieldNotFound, pva.InvalidRequest):
            return pva.PvString("error")

        q_po = pva.PvObject({"lhs": pva.STRING,
                             "rhs": pva.STRING,
                             })
        q_po.setString("lhs", query["lhs"])
        q_po.setString("rhs", query["rhs"])

        return self.add(q_po)
