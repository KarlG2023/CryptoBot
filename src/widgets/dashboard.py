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

import chart_analysis.analysis #pylint: disable=import-error

import data.charts #pylint: disable=import-error
import data.currencies #pylint: disable=import-error

import param #pylint: disable=import-error

def get_account_data(currency):
    last_trades = ""
    balance = "Balance:\n" + str(param.balance[currency]) + " " + currency + "\n\n"

    if currency == "BTC":
        last_trades = "Previous trades order:\n" + param.trades_btc
    if currency == "ETH":
        last_trades = "Previous trades order:\n" + param.trades_eth
    if currency == "LTC":
        last_trades = "Previous trades order:\n" + param.trades_ltc
    return balance + last_trades

def print_action(status):
    if status == chart_analysis.analysis.ACTION.BUY:
        res = QtWidgets.QLabel('Buy')
        res.setAlignment(QtCore.Qt.AlignCenter)
        res.setStyleSheet("background-color: #99e699;border-radius: 10px")
        res.setMaximumWidth(100)
        res.setMinimumHeight(20)
        return res
    if status == chart_analysis.analysis.ACTION.SELL:
        res = QtWidgets.QLabel('Sell')
        res.setAlignment(QtCore.Qt.AlignCenter)
        res.setStyleSheet("background-color: #ff8080;border-radius: 10px")
        res.setMaximumWidth(60)
        res.setMinimumHeight(20)
        return res
    if status == chart_analysis.analysis.ACTION.NEUTRAL:
        res = QtWidgets.QLabel('Neutral')
        res.setAlignment(QtCore.Qt.AlignCenter)
        res.setStyleSheet("background-color: #cccccc;border-radius: 10px")
        res.setMaximumWidth(100)
        res.setMinimumHeight(20)
        return res
    if status == chart_analysis.analysis.ACTION.ERROR:
        res = QtWidgets.QLabel('Error')
        res.setAlignment(QtCore.Qt.AlignCenter)
        res.setStyleSheet("background-color: white;border-radius: 10px")
        res.setMaximumWidth(100)
        res.setMinimumHeight(20)
        return res
    
def set_data_style(label):
    label.setStyleSheet("background-color: #f2f2f2;border-style: outset;border-width: 2px;border-radius: 10px;border-color: grey;padding: 6px;")
    label.setAlignment(QtCore.Qt.AlignVCenter)
    label.setMinimumWidth(400)
    return label

def get_data(layout):

    widget_1_content = get_account_data("USDT")
    widget_2_content = get_account_data("BTC")
    widget_3_content = get_account_data("ETH")
    widget_4_content = get_account_data("LTC")

    layout = QtWidgets.QGridLayout()

    widget_1 = QtWidgets.QLabel(widget_1_content)
    widget_1.setStyleSheet("background-color: #e6e6e6;border-style: outset;border-width: 2px;border-radius: 10px;border-color: grey;padding: 6px;")
    widget_1.setAlignment(QtCore.Qt.AlignLeft)
    # widget_1.setFixedWidth(250)

    widget_2 = QtWidgets.QLabel(widget_2_content)
    widget_2.setStyleSheet("border-style: outset;border-width: 2px;border-radius: 10px;border-color: grey;padding: 6px;")
    widget_2.setAlignment(QtCore.Qt.AlignLeft)
    # widget_1.setFixedWidth(250)

    widget_3 = QtWidgets.QLabel(widget_3_content)
    widget_3.setStyleSheet("border-style: outset;border-width: 2px;border-radius: 10px;border-color: grey;padding: 6px;")
    widget_3.setAlignment(QtCore.Qt.AlignLeft)
    # widget_1.setFixedWidth(250)

    widget_4 = QtWidgets.QLabel(widget_4_content)
    widget_4.setStyleSheet("border-style: outset;border-width: 2px;border-radius: 10px;border-color: grey;padding: 6px;")
    widget_4.setAlignment(QtCore.Qt.AlignLeft)
    # widget_4.setFixedWidth(250)

    time_label = QtWidgets.QLabel(time.strftime("%H:%M:%S"))
    time_label.setStyleSheet("background-color: #e6e6e6;border-style: outset;border-width: 2px;border-radius: 10px;border-color: grey;padding: 6px;")
    
    algo_global = QtWidgets.QLabel("START")
    algo_global.setStyleSheet("background-color: #e6e6e6;border-style: outset;border-width: 2px;border-radius: 10px;border-color: grey;padding: 6px;")
    algo_global.setAlignment(QtCore.Qt.AlignCenter)
    algo_global.setMaximumHeight(50)

    layout.addWidget(widget_1, 0, 0, 15, 1)
    layout.addWidget(widget_2, 0, 1, 15, 1)
    layout.addWidget(widget_3, 0, 2, 15, 1)
    layout.addWidget(widget_4, 0, 3, 15, 1)

    layout.addWidget(time_label, 15, 0)
    layout.addWidget(algo_global, 15, 1, 1, 3) # row x/col x / high x / width x
    return layout

class Dashboard(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Dashboard, self).__init__(parent)

        layout = get_data(QtWidgets.QGridLayout())
        self.setLayout(layout)
