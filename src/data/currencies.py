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

class currencies_json:
    def __init__(self, poloniex):
        self.poloniex_obj = poloniex
        self.currencies = ['BTC', 'ETH', 'LTC']

        #debug
        # os.remove("data/json/cryptocurrencies.json")

        # create file if it doesnt exist with basic currencies, load json object and write it for next session
        if not os.path.exists('data/json'):
            os.makedirs('data/json')
        if os.path.isfile("data/json/cryptocurrencies.json") == False:
            # self.currencies = ['BTC', 'ETH', 'LTC']
            self.data = {}
            self.data['crypto'] = []
            disabled = api_request.charts.getCurrenciesInfo(poloniex)['BTC']['disabled']
            price = api_request.charts.get_ticker(poloniex)['USDT_BTC']['highestBid']
            volume = api_request.charts.get24hVolume(poloniex)['USDT_BTC']
            print(self.data["crypto"])
            self.data['crypto'].append({
                'name': 'BTC',
                'disabled': disabled,
                'price': price,
                'volume': 0
            })
            disabled = api_request.charts.getCurrenciesInfo(poloniex)['ETH']['disabled']
            price = api_request.charts.get_ticker(poloniex)['BTC_ETH']['highestBid']
            volume = api_request.charts.get24hVolume(poloniex)['BTC_ETH']
            # print(volume)
            self.data['crypto'].append({
                'name': 'ETH',
                'disabled': disabled,
                'price': price,
                'volume': 0
            })
            disabled = api_request.charts.getCurrenciesInfo(poloniex)['LTC']['disabled']
            price = api_request.charts.get_ticker(poloniex)['BTC_LTC']['highestBid']
            self.data['crypto'].append({
                'name': 'LTC',
                'disabled': disabled,
                'price': price,
                'volume': 0
            })
            with open('data/json/cryptocurrencies.json', 'w') as outfile:
                json.dump(self.data, outfile)
        else:
            with open('data/json/cryptocurrencies.json') as json_file:
                self.data = json.load(json_file)
    
    # debug
    def print_data(self):
        for p in self.data['crypto']:
            print('Name: ' + p['name'])
    
    def add_currency(self, name):
        self.currencies.append(name)
        with open('data/json/cryptocurrencies.json', 'w') as outfile:
            json.dump(self.data, outfile)
    
    def remove_currency(self, name):
        self.currencies.remove(name)
        with open('data/json/cryptocurrencies.json', 'w') as outfile:
            json.dump(self.data, outfile)

# create and update crypto data from list and put in json.file / get info from json file
# can afford to write in json file because update is needed only each 1 to 5min
# work first here, add write to json if exist else create / add price info / disabled / 24h volume to json