#!/usr/bin/env python3

import json
import math
import os
import random
import string
import sys
import time

# sudo apt install libxcb-xinerama0/poloniex/PySide2
from poloniex import Poloniex
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import api_request.account
import api_request.charts
import api_request.trades

class charts_json:
    def __init__(self, poloniex):
        self.poloniex_obj = poloniex
        self.data = str(api_request.charts.get_chart_data(self.poloniex_obj, ['USDT_BTC'], 900, start=int(time.time())-(86400*30), end=int(time.time()))).replace("'", '"')
        self.data2 = self.data.replace("None", "null")

    def print_data(self):
        print(self.data2)
