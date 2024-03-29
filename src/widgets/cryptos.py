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
import chart_analysis.oscillators #pylint: disable=import-error

import data.charts #pylint: disable=import-error
import data.currencies #pylint: disable=import-error

import param #pylint: disable=import-error

def get_account_data(currency):
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
        res.setMaximumWidth(100)
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

def get_data(layout, crypto):
    widget_1_content = get_account_data(crypto)

    layout = QtWidgets.QGridLayout()

    widget_1 = QtWidgets.QLabel(widget_1_content)
    widget_1.setStyleSheet("background-color: #e6e6e6;border-style: outset;border-width: 2px;border-radius: 10px;border-color: grey;padding: 6px;")
    widget_1.setAlignment(QtCore.Qt.AlignLeft)
    widget_1.setFixedWidth(250)

    algo_1 = QtWidgets.QLabel('Relative Strength Index (14)')
    algo_1 = set_data_style(algo_1)

    res_1 = print_action(param.cryptobot.get_rsi(crypto))

    algo_2 = QtWidgets.QLabel('Stochastic (14,3,3)')
    algo_2 = set_data_style(algo_2)

    res_2 = print_action(param.cryptobot.get_stochastique(crypto))

    algo_3 = QtWidgets.QLabel('Commodity Channel Index (20)')
    algo_3 = set_data_style(algo_3)

    res_3 = print_action(param.cryptobot.get_cci(crypto))

    algo_4 = QtWidgets.QLabel('Average Directional Index (14)')
    algo_4 = set_data_style(algo_4)

    res_4 = print_action(param.cryptobot.get_adi(crypto))

    algo_5 = QtWidgets.QLabel('Awesome Oscillator')
    algo_5 = set_data_style(algo_5)

    res_5 = print_action(param.cryptobot.get_awesome(crypto))

    algo_6 = QtWidgets.QLabel('Momentum (10)')
    algo_6 = set_data_style(algo_6)

    res_6 = print_action(param.cryptobot.get_momentum(crypto))

    algo_7 = QtWidgets.QLabel('MACD Level (12, 26)')
    algo_7 = set_data_style(algo_7)

    res_7 = print_action(param.cryptobot.get_macd(crypto))

    algo_8 = QtWidgets.QLabel('Stochastic RSI Fast (3, 3, 14, 14)')
    algo_8 = set_data_style(algo_8)

    res_8 = print_action(param.cryptobot.get_stochrsi(crypto))

    algo_9 = QtWidgets.QLabel('Bull Bear Power')
    algo_9 = set_data_style(algo_9)

    res_9 = print_action(param.cryptobot.get_bullbear(crypto))

    algo_10 = QtWidgets.QLabel('Exponential Moving Average (5)')
    algo_10 = set_data_style(algo_10)

    res_10 = print_action(param.cryptobot.get_ema5(crypto))

    algo_11 = QtWidgets.QLabel('Simple Moving Average (5)')
    algo_11 = set_data_style(algo_11)

    res_11 = print_action(param.cryptobot.get_sma5(crypto))

    algo_12 = QtWidgets.QLabel('Exponential Moving Average (10)')
    algo_12 = set_data_style(algo_12)

    res_12 = print_action(param.cryptobot.get_ema10(crypto))

    algo_13 = QtWidgets.QLabel('Simple Moving Average (10)')
    algo_13 = set_data_style(algo_13)

    res_13 = print_action(param.cryptobot.get_sma10(crypto))

    algo_14 = QtWidgets.QLabel('Exponential Moving Average (20)')
    algo_14 = set_data_style(algo_14)

    res_14 = print_action(param.cryptobot.get_ema20(crypto))

    algo_15 = QtWidgets.QLabel('Simple Moving Average (20)')
    algo_15 = set_data_style(algo_15)

    res_15 = print_action(param.cryptobot.get_sma20(crypto))

    time_label = QtWidgets.QLabel(time.strftime("%H:%M:%S"))
    time_label.setStyleSheet("background-color: #e6e6e6;border-style: outset;border-width: 2px;border-radius: 10px;border-color: grey;padding: 6px;")
    
    algo_global = QtWidgets.QLabel(param.cryptobot.get_status_string(crypto))
    algo_global.setStyleSheet("background-color: #e6e6e6;border-style: outset;border-width: 2px;border-radius: 10px;border-color: grey;padding: 6px;")
    algo_global.setAlignment(QtCore.Qt.AlignCenter)
    algo_global.setMaximumHeight(50)

    res_global = print_action(param.cryptobot.get_status(crypto))

    # print_action(chart_analysis.analysis.ACTION.BUY)

    nbr_widget = 0

    if param.rsi != 0:
        layout.addWidget(algo_1, nbr_widget, 1)
        layout.addWidget(res_1, nbr_widget, 2)
        nbr_widget += 1
    if param.stochastique != 0:
        layout.addWidget(algo_2, nbr_widget, 1)
        layout.addWidget(res_2, nbr_widget, 2)
        nbr_widget += 1
    if param.cci != 0:
        layout.addWidget(algo_3, nbr_widget, 1)
        layout.addWidget(res_3, nbr_widget, 2)
        nbr_widget += 1
    if param.adi != 0:
        layout.addWidget(algo_4, nbr_widget, 1)
        layout.addWidget(res_4, nbr_widget, 2)
        nbr_widget += 1
    if param.awesome != 0:
        layout.addWidget(algo_5, nbr_widget, 1)
        layout.addWidget(res_5, nbr_widget, 2)
        nbr_widget += 1
    if param.momentum != 0:
        layout.addWidget(algo_6, nbr_widget, 1)
        layout.addWidget(res_6, nbr_widget, 2)
        nbr_widget += 1
    if param.macd != 0:
        layout.addWidget(algo_7, nbr_widget, 1)
        layout.addWidget(res_7, nbr_widget, 2)
        nbr_widget += 1
    if param.stochrsi != 0:
        layout.addWidget(algo_8, nbr_widget, 1)
        layout.addWidget(res_8, nbr_widget, 2)
        nbr_widget += 1
    if param.bullbear != 0:
        layout.addWidget(algo_9, nbr_widget, 1)
        layout.addWidget(res_9, nbr_widget, 2)
        nbr_widget += 1
    if param.ema5 != 0:
        layout.addWidget(algo_10, nbr_widget, 1)
        layout.addWidget(res_10, nbr_widget, 2)
        nbr_widget += 1
    if param.sma5 != 0:
        layout.addWidget(algo_11, nbr_widget, 1)
        layout.addWidget(res_11, nbr_widget, 2)
        nbr_widget += 1
    if param.ema10 != 0:
        layout.addWidget(algo_12, nbr_widget, 1)
        layout.addWidget(res_12, nbr_widget, 2)
        nbr_widget += 1
    if param.sma10 != 0:
        layout.addWidget(algo_13, nbr_widget, 1)
        layout.addWidget(res_13, nbr_widget, 2)
        nbr_widget += 1
    if param.ema20 != 0:
        layout.addWidget(algo_14, nbr_widget, 1)
        layout.addWidget(res_14, nbr_widget, 2)
        nbr_widget += 1
    if param.sma20 != 0:
        layout.addWidget(algo_15, nbr_widget, 1)
        layout.addWidget(res_15, nbr_widget, 2)
        nbr_widget += 1
    
    layout.addWidget(widget_1, 0, 0, nbr_widget, 1)

    layout.addWidget(time_label, nbr_widget + 1, 0)
    layout.addWidget(algo_global, nbr_widget + 1, 1, 1, 1) # row x/col x / high x / width x
    layout.addWidget(res_global, nbr_widget + 1, 2)
    return layout

class Bitcoin(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Bitcoin, self).__init__(parent)
  
        layout = get_data(QtWidgets.QGridLayout(), "BTC")
        self.setLayout(layout)

class Ethereum(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Ethereum, self).__init__(parent)
        
        layout = get_data(QtWidgets.QGridLayout(), "ETH")
        self.setLayout(layout)

class Litecoin(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Litecoin, self).__init__(parent)
        
        layout = get_data(QtWidgets.QGridLayout(), "LTC")
        self.setLayout(layout)
