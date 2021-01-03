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

import api_request.account #pylint: disable=import-error
import api_request.charts #pylint: disable=import-error
import api_request.trades #pylint: disable=import-error

class charts_json:
    def __init__(self, poloniex):
        self.poloniex_obj = poloniex

        self.data_btc = self.init_data('USDT_BTC')
        self.data_ltc = self.init_data('USDT_LTC')
        self.data_eth = self.init_data('USDT_ETH')

    # putting a full month in json
    def init_data(self, crypto):
        data = []
        polo_data = str(api_request.charts.get_chart_data(self.poloniex_obj, [crypto], 900, start=int(time.time())-(86400*30), end=int(time.time()))).replace("'", '"').replace("None", "null")
        tmp = str()
        data_json = {}
        data_json['candle'] = []

        for i in range(1, len(polo_data) - 1):
            if i > 2:
                if polo_data[i] == ',' and polo_data[i - 1] == '}':
                    data.append(tmp)
                    tmp = str()
                    i += 1
            tmp += str(polo_data[i])
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
        return data_json
        # with open("data/json/charts.json", "w") as outfile:
        #     json.dump(data_json, outfile)


    def get_data(self, data_json, element): # add x param to get last x element ?
        res = []
        for i in data_json["candle"]:
            res.append(i[element])
        return res
    
    def get_data_btc(self):
        return self.data_btc
    
    def get_data_eth(self):
        return self.data_eth
    
    def get_data_ltc(self):
        return self.data_ltc

    # extract the json values from a given json
    # put path of the json to extract and select a element to extract
    # you will receive a list with every values for an element ask
    def print_data_in_file(self, path, element):
        res = []
        with open(path) as json_file:
            data_json = json.load(json_file)
            for i in data_json["candle"]:
                res.append(i[element])
        return res