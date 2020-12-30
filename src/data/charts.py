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


    # putting a full month in json
    def get_data(self):
        data = []
        new_data = []
        tmp = str()
        data_json = {}
        data_json['candle'] = []

        for i in range(1, len(self.data2) - 1):
            if i > 2:
                if self.data2[i] == ',' and self.data2[i - 1] == '}':
                    data.append(tmp)
                    tmp = str()
                    i += 1
            tmp += str(self.data2[i])
        for i in range(1, len(data)):
            new_tmp = {}
            data_row = []
            tmp_data = str()
            tmp_data = data[i].replace(" ", "").replace('"', "'").replace("{", "").replace("}", "")
            tmp_data_data = str()
            for i in tmp_data:
                if i == ':':
                    tmp_data_data += i + "'"
                elif i == ',':
                    tmp_data_data += "'" + i
                else:
                    tmp_data_data += i
            tmp_data_data += "'"
            data_row = tmp_data_data.split(',')
            for i in data_row:
                a = i.replace("'", "").split(':')
                new_tmp[a[0]] = a[1]
            data_json['candle'].append(new_tmp)
        
        with open("data/json/charts.json", "w") as outfile:
            json.dump(data_json, outfile)

    # extract the json values from a given json
    # put path of the json to extract and select a element to extract
    # you will receive a list with every values for an element ask
    def print_data(self, path, element):
        res = []
        with open(path) as json_file:
            data_json = json.load(json_file)
            for i in data_json["candle"]:
                res.append(i[element])
        return res
