#!/usr/bin/env python3

import sys
import string
import math
from poloniex import Poloniex
import os

class main(object):
    def __init__(self):
        self.credentials = 0

    def log(self):
        try:
            if len(sys.argv) != 3:
                exit(84)
        except Exception as e:
            print("Unexpected error:", e)
            exit(84)

    def get_account_data(self):
        api_key = sys.argv[1]
        api_secret = sys.argv[2]
        polo = Poloniex(api_key, api_secret)
        
        # ticker = polo.returnTicker()['USDT_BTC']
        # print(ticker)
        
        balances = polo.returnBalances()
        print(balances)
        
        # help(polo)
        # print(polo.returnChartData(['USDT_BTC'], 86400, start=1605450419, end=1608042419 ))

obj_main = main()
obj_main.log()
obj_main.get_account_data()