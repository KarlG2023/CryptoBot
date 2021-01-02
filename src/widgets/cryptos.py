#!/usr/bin/env python3

import json
import math
import os
import random
import string
import sys
import time

# sudo apt install libxcb-xinerama0/poloniex/PySide2
from enum import Enum
from poloniex import Poloniex
from PySide2 import QtGui, QtCore, QtWidgets

import api_request.account #pylint: disable=import-error
import api_request.charts #pylint: disable=import-error
import api_request.trades #pylint: disable=import-error

import data.charts #pylint: disable=import-error
import data.currencies #pylint: disable=import-error

import param_init #pylint: disable=import-error

def get_widget_1_content(currency):
    balance = "Balance:\n" + str(api_request.account.get_balance(param_init.poloniex_obj)[currency]) + currency + "\n\n"
    if currency == "BTC":
        last_trades= "Previous trades order:\n" + str(api_request.trades.getTradeHistory(param_init.poloniex_obj, "USDT_BTC", start=int(time.time())-(86400*30), end=int(time.time()), limit=10))
    else:
        last_trades= "Previous trades order:\n" + str(api_request.trades.getTradeHistory(param_init.poloniex_obj, "BTC_" + currency, start=int(time.time())-(86400*30), end=int(time.time()), limit=10))
    return balance + last_trades

class Bitcoin(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Bitcoin, self).__init__(parent)
  
        widget_1_content = get_widget_1_content("BTC")

        layout = QtWidgets.QGridLayout()

        self.widget_1 = QtWidgets.QLabel(widget_1_content)
        self.widget_1.setAlignment(QtCore.Qt.AlignLeft)
        self.widget_1.setFixedWidth(250)
    
        self.algo_1 = QtWidgets.QLabel('Fibonacci')
        self.algo_1.setAlignment(QtCore.Qt.AlignLeft)
        self.algo_1.setMinimumWidth(400)

        self.res_1 = QtWidgets.QLabel('Buy / Sell')
        self.res_1.setAlignment(QtCore.Qt.AlignCenter)
        self.res_1.setMaximumWidth(100)        
        
        self.algo_2 = QtWidgets.QLabel('X Buy Y Sell Z Neutral')
        self.algo_2.setAlignment(QtCore.Qt.AlignCenter)
        self.algo_2.setMaximumHeight(50)

        layout.addWidget(self.widget_1, 0, 0, 2, 1)
        layout.addWidget(self.algo_1, 0, 1)
        layout.addWidget(self.res_1, 0, 2)
        layout.addWidget(self.algo_2, 1, 1, 1, 2) # row x/col x / high x / width x
        self.setLayout(layout)

class Ethereum(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Ethereum, self).__init__(parent)
        
        widget_1_content = get_widget_1_content("ETH")

        layout = QtWidgets.QHBoxLayout()

        self.widget_1 = QtWidgets.QLabel(widget_1_content)
        self.widget_1.setAlignment(QtCore.Qt.AlignLeft)
        self.widget_1.setFixedWidth(250)
    
        self.label = QtWidgets.QLabel('Ethereum page!')
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        layout.addWidget(self.widget_1)
        layout.addWidget(self.label)
        self.setLayout(layout)

class Litecoin(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Litecoin, self).__init__(parent)
        
        widget_1_content = get_widget_1_content("LTC")

        layout = QtWidgets.QHBoxLayout()

        self.widget_1 = QtWidgets.QLabel(widget_1_content)
        self.widget_1.setAlignment(QtCore.Qt.AlignLeft)
        self.widget_1.setFixedWidth(250)
    
        self.label = QtWidgets.QLabel('Litecoin page!')
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        layout.addWidget(self.widget_1)
        layout.addWidget(self.label)
        self.setLayout(layout)
