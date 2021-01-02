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

        layout = QtWidgets.QHBoxLayout()

        self.widget_1 = QtWidgets.QLabel(widget_1_content)
        self.widget_1.setAlignment(QtCore.Qt.AlignLeft)
        self.widget_1.setFixedWidth(250)
    
        self.label = QtWidgets.QLabel('Bitcoin page!')
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        layout.addWidget(self.widget_1)
        layout.addWidget(self.label)
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
