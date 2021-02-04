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

import api_request.account
import api_request.charts
import api_request.trades

import chart_analysis.analysis

import data.charts
import data.currencies

import param

import widgets.cryptos
import widgets.dashboard
import widgets.login
import widgets.parameters

from enum import Enum

class Tab(Enum):
    PARAM = 0
    DASHBOARD = 1
    BITCOIN = 2
    ETHEREUM = 3
    LITECOIN = 4

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        param.init()
        param.init_algo()
        param.init_account()
        param.init_json()

        param.cryptobot.btc_update()
        param.cryptobot.eth_update()
        param.cryptobot.ltc_update()
        
        self.tab = Tab.DASHBOARD

        self.setWindowTitle("CyptoBot")
        self.toolbar()

        self.central_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.widget = widgets.dashboard.Dashboard(self)
        self.central_widget.addWidget(self.widget)
        self.time()

    # creation of a timer for the program
    def time(self):
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(500)

    # using the timer for repetitiv actions
    def update(self):
        self.setFixedSize(param.window_x, param.window_y)
        self.widgets_update()

        # update balance (comment for test phase)
        if int(time.strftime("%M")) == 0:
            param.balance = api_request.account.get_balance(param.poloniex_obj)

        period = ""
        duration = 0
        update_latency = 0
        if param.candle_size == 900:
            period = "%M"
            duration = 15
            update_latency = 3
        if param.candle_size == 14400:
            period = "%H"
            duration = 4
            update_latency = 1
        if param.candle_size == 86400:
            period = "%D"
            duration = 1

        if int(time.strftime("%S")) == 1 and param.bot_status == 2:
            param.bot_status = 1
        
        # condition d'achat
        if int(time.strftime(period))%duration == update_latency and int(time.strftime("%S")) == 0 and param.bot_status == 1:
            param.bot_status = 2
            if param.cryptobot.get_status("BTC") == chart_analysis.analysis.ACTION.BUY and param.balance['USDT'] != 0:
                param.balance = api_request.account.get_balance(param.poloniex_obj)
                price = api_request.charts.get_ticker(param.poloniex_obj)['USDT_BTC']['last']
                quantity = (param.balance['USDT'] / price)*(pow(param.bull_strength['BTC'], 2))
                if param.balance['USDT'] - (quantity * price) > 1:
                    param.bear_strength['BTC'] = 0.9
                    param.bull_strength['BTC'] += 0.1
                    # param.balance['BTC'] = param.balance['BTC'] + quantity
                    # param.balance['USDT'] = param.balance['USDT'] - (quantity * price)

                    api_request.trades.cancelOrder(param.poloniex_obj, param.btc_order)
                    param.btc_order = api_request.trades.buy(param.poloniex_obj, "USDT_BTC", price, quantity, 0, 0, 0)

                    print("[" + str(time.strftime("%H")) + ":" + str(time.strftime("%M")) + ":" + str(time.strftime("%S")) + "]")
                    print("BOUGHT " + str(quantity) + " BTC at " + str(price))
                    print("Balance: " + str(param.balance) + "\n")
                if param.balance['USDT'] - (quantity * price) < 1:
                    # param.balance['BTC'] = param.balance['BTC'] + (param.balance['USDT'] / price)
                    # param.balance['USDT'] = 0

                    api_request.trades.cancelOrder(param.poloniex_obj, param.btc_order)
                    param.btc_order = api_request.trades.buy(param.poloniex_obj, "USDT_BTC", price, param.balance['USDT'], 0, 0, 0)

                    print("[" + str(time.strftime("%H")) + ":" + str(time.strftime("%M")) + ":" + str(time.strftime("%S")) + "]")
                    print("BOUGHT " + str(param.balance['USDT'] / price) + " BTC at " + str(price))
                    print("Balance: " + str(param.balance) + "\n")

            if param.cryptobot.get_status("BTC") == chart_analysis.analysis.ACTION.SELL and param.balance['BTC'] != 0:
                param.balance = api_request.account.get_balance(param.poloniex_obj)
                price = api_request.charts.get_ticker(param.poloniex_obj)['USDT_BTC']['last']
                quantity = (param.balance['BTC'])*(pow(param.bear_strength['BTC'], 2))
                if (param.balance['BTC'] * price) - quantity * price > 1:
                    param.bull_strength['BTC'] = 0.1
                    param.bear_strength['BTC'] -= 0.1
                    # param.balance['USDT'] += price * quantity
                    # param.balance['BTC'] = param.balance['BTC'] - quantity

                    api_request.trades.cancelOrder(param.poloniex_obj, param.btc_order)
                    param.btc_order = api_request.trades.sell(param.poloniex_obj, "USDT_BTC", price, quantity, 0, 0, 0)

                    print("[" + str(time.strftime("%H")) + ":" + str(time.strftime("%M")) + ":" + str(time.strftime("%S")) + "]")
                    print("SOLD " + str(quantity) + " BTC at " + str(price))
                    print("Balance: " + str(param.balance) + "\n")
                if (param.balance['BTC'] * price) - quantity * price < 1:
                    # param.balance['USDT'] += price * param.balance['BTC']
                    # param.balance['BTC'] = 0

                    api_request.trades.cancelOrder(param.poloniex_obj, param.btc_order)
                    param.btc_order = api_request.trades.sell(param.poloniex_obj, "USDT_BTC", price, param.balance['BTC'], 0, 0, 0)

                    print("[" + str(time.strftime("%H")) + ":" + str(time.strftime("%M")) + ":" + str(time.strftime("%S")) + "]")
                    print("SOLD " + str(quantity) + " BTC at " + str(price))
                    print("Balance: " + str(param.balance) + "\n")

            if param.cryptobot.get_status("ETH") == chart_analysis.analysis.ACTION.BUY and param.balance['USDT'] != 0:
                param.balance = api_request.account.get_balance(param.poloniex_obj)
                price = api_request.charts.get_ticker(param.poloniex_obj)['USDT_ETH']['last']
                quantity = (param.balance['USDT'] / price)*(pow(param.bull_strength['ETH'], 2))
                if param.balance['USDT'] - (quantity * price) > 1:
                    param.bear_strength['ETH'] = 0.9
                    param.bull_strength['ETH'] += 0.1
                    # param.balance['ETH'] = param.balance['ETH'] + quantity
                    # param.balance['USDT'] = param.balance['USDT'] - (quantity * price)

                    api_request.trades.cancelOrder(param.poloniex_obj, param.eth_order)
                    param.eth_order = api_request.trades.buy(param.poloniex_obj, "USDT_ETH", price, quantity, 0, 0, 0)

                    print("[" + str(time.strftime("%H")) + ":" + str(time.strftime("%M")) + ":" + str(time.strftime("%S")) + "]")
                    print("BOUGHT " + str(quantity) + " ETH at " + str(price))
                    print("Balance: " + str(param.balance) + "\n")
                if param.balance['USDT'] - (quantity * price) < 1:
                    # param.balance['ETH'] = param.balance['ETH'] + (param.balance['USDT'] / price)
                    # param.balance['USDT'] = 0

                    api_request.trades.cancelOrder(param.poloniex_obj, param.eth_order)
                    param.eth_order = api_request.trades.buy(param.poloniex_obj, "USDT_ETH", price, param.balance['USDT'], 0, 0, 0)

                    print("[" + str(time.strftime("%H")) + ":" + str(time.strftime("%M")) + ":" + str(time.strftime("%S")) + "]")
                    print("BOUGHT " + str(param.balance['USDT'] / price) + " ETH at " + str(price))
                    print("Balance: " + str(param.balance) + "\n")

            if param.cryptobot.get_status("ETH") == chart_analysis.analysis.ACTION.SELL and param.balance['ETH'] != 0:
                param.balance = api_request.account.get_balance(param.poloniex_obj)
                price = api_request.charts.get_ticker(param.poloniex_obj)['USDT_ETH']['last']
                quantity = (param.balance['ETH'])*(pow(param.bear_strength['ETH'], 2))
                if (param.balance['ETH'] * price) - quantity * price > 1:
                    param.bull_strength['ETH'] = 0.1
                    param.bear_strength['ETH'] -= 0.1
                    # param.balance['USDT'] += price * quantity
                    # param.balance['ETH'] = param.balance['ETH'] - quantity

                    api_request.trades.cancelOrder(param.poloniex_obj, param.eth_order)
                    param.eth_order = api_request.trades.sell(param.poloniex_obj, "USDT_ETH", price, quantity, 0, 0, 0)

                    print("[" + str(time.strftime("%H")) + ":" + str(time.strftime("%M")) + ":" + str(time.strftime("%S")) + "]")
                    print("SOLD " + str(quantity) + " ETH at " + str(price))
                    print("Balance: " + str(param.balance) + "\n")
                if (param.balance['ETH'] * price) - quantity * price < 1:
                    # param.balance['USDT'] += price * param.balance['ETH']
                    # param.balance['ETH'] = 0

                    api_request.trades.cancelOrder(param.poloniex_obj, param.eth_order)
                    param.eth_order = api_request.trades.sell(param.poloniex_obj, "USDT_ETH", price, param.balance['ETH'], 0, 0, 0)

                    print("[" + str(time.strftime("%H")) + ":" + str(time.strftime("%M")) + ":" + str(time.strftime("%S")) + "]")
                    print("SOLD ETH at " + str(price))
                    print("Balance: " + str(param.balance) + "\n")

            if param.cryptobot.get_status("LTC") == chart_analysis.analysis.ACTION.BUY and param.balance['USDT'] != 0:
                param.balance = api_request.account.get_balance(param.poloniex_obj)
                price = api_request.charts.get_ticker(param.poloniex_obj)['USDT_LTC']['last']
                quantity = (param.balance['USDT'] / price)*(pow(param.bull_strength['LTC'], 2))
                if param.balance['USDT'] - (quantity * price) > 1:
                    param.bear_strength['LTC'] = 0.9
                    param.bull_strength['LTC'] += 0.1
                    # param.balance['LTC'] = param.balance['LTC'] + quantity
                    # param.balance['USDT'] = param.balance['USDT'] - (quantity * price)

                    api_request.trades.cancelOrder(param.poloniex_obj, param.ltc_order)
                    param.ltc_order = api_request.trades.buy(param.poloniex_obj, "USDT_LTC", price, quantity, 0, 0, 0)
                    
                    print("[" + str(time.strftime("%H")) + ":" + str(time.strftime("%M")) + ":" + str(time.strftime("%S")) + "]")
                    print("BOUGHT " + str(quantity) + " LTC at " + str(price))
                    print("Balance: " + str(param.balance) + "\n")
                if param.balance['USDT'] - (quantity * price) < 1:
                    # param.balance['LTC'] = param.balance['LTC'] + (param.balance['USDT'] / price)
                    # param.balance['USDT'] = 0

                    api_request.trades.cancelOrder(param.poloniex_obj, param.ltc_order)
                    param.ltc_order = api_request.trades.buy(param.poloniex_obj, "USDT_LTC", price, param.balance['USDT'], 0, 0, 0)

                    print("[" + str(time.strftime("%H")) + ":" + str(time.strftime("%M")) + ":" + str(time.strftime("%S")) + "]")
                    print("BOUGHT " + str(param.balance['USDT'] / price) + " LTC at " + str(price))
                    print("Balance: " + str(param.balance) + "\n")

            if param.cryptobot.get_status("LTC") == chart_analysis.analysis.ACTION.SELL and param.balance['LTC'] != 0:
                param.balance = api_request.account.get_balance(param.poloniex_obj)
                price = api_request.charts.get_ticker(param.poloniex_obj)['USDT_LTC']['last']
                quantity = (param.balance['LTC'])*(pow(param.bear_strength['LTC'], 2))
                if (param.balance['LTC'] * price) - quantity * price > 1:
                    param.bull_strength['LTC'] = 0.1
                    param.bear_strength['LTC'] -= 0.1
                    # param.balance['USDT'] += price * quantity
                    # param.balance['LTC'] = param.balance['LTC'] - quantity

                    api_request.trades.cancelOrder(param.poloniex_obj, param.ltc_order)
                    param.ltc_order = api_request.trades.sell(param.poloniex_obj, "USDT_LTC", price, quantity, 0, 0, 0)

                    print("[" + str(time.strftime("%H")) + ":" + str(time.strftime("%M")) + ":" + str(time.strftime("%S")) + "]")
                    print("SOLD " + str(quantity) + " LTC at " + str(price))
                    print("Balance: " + str(param.balance) + "\n")
                if (param.balance['LTC'] * price) - quantity * price < 1:
                    # param.balance['USDT'] += price * param.balance['LTC']
                    # param.balance['LTC'] = 0

                    api_request.trades.cancelOrder(param.poloniex_obj, param.ltc_order)
                    param.ltc_order = api_request.trades.sell(param.poloniex_obj, "USDT_LTC", price, param.balance['LTC'], 0, 0, 0)

                    print("[" + str(time.strftime("%H")) + ":" + str(time.strftime("%M")) + ":" + str(time.strftime("%S")) + "]")
                    print("SOLD LTC at " + str(price))
                    print("Balance: " + str(param.balance) + "\n")
            
        if int(time.strftime("%S")) == 30:
            param.charts_json = data.charts.charts_json(param.poloniex_obj, param.candle_size)
            param.estimate_balance = param.balance['USDT'] + (api_request.charts.get_ticker(param.poloniex_obj)['USDT_BTC']['last'] * param.balance['BTC']) + (api_request.charts.get_ticker(param.poloniex_obj)['USDT_ETH']['last'] * param.balance['ETH']) + (api_request.charts.get_ticker(param.poloniex_obj)['USDT_LTC']['last'] * param.balance['LTC'])
        if int(time.strftime("%S")) == 40:
            param.cryptobot.btc_update()
            param.trades_btc = str(api_request.trades.getTradeHistory(param.poloniex_obj, "USDT_BTC", start=int(time.time())-(86400), end=int(time.time()), limit=10))
        if int(time.strftime("%S")) == 45:
            param.cryptobot.eth_update()
            param.trades_eth = str(api_request.trades.getTradeHistory(param.poloniex_obj, "USDT_ETH", start=int(time.time())-(86400), end=int(time.time()), limit=10))
        if int(time.strftime("%S")) == 50:
            param.cryptobot.ltc_update()
            param.trades_ltc = str(api_request.trades.getTradeHistory(param.poloniex_obj, "USDT_LTC", start=int(time.time())-(86400), end=int(time.time()), limit=10))

    # update widgets data
    def widgets_update(self):
        self.central_widget.removeWidget(self.widget)
        if self.tab == Tab.PARAM:
            self.widget = widgets.parameters.Param(self)
        if self.tab == Tab.DASHBOARD:
            self.widget = widgets.dashboard.Dashboard(self)
        if self.tab == Tab.BITCOIN:
            self.widget = widgets.cryptos.Bitcoin(self)
        if self.tab == Tab.ETHEREUM:
            self.widget = widgets.cryptos.Ethereum(self)
        if self.tab == Tab.LITECOIN:
            self.widget = widgets.cryptos.Litecoin(self)
        self.central_widget.addWidget(self.widget)
        self.central_widget.setCurrentWidget(self.widget)

    # change widget from x to param
    def to_param(self):
        self.tab = Tab.PARAM
        self.widget = widgets.parameters.Param(self)
        self.central_widget.addWidget(self.widget)
        self.central_widget.setCurrentWidget(self.widget)

    # change widget from x to dashboard
    def to_dashboard(self):
        self.tab = Tab.DASHBOARD
        self.widget = widgets.dashboard.Dashboard(self)
        self.central_widget.addWidget(self.widget)
        self.central_widget.setCurrentWidget(self.widget)
    
    # change widget from x to bitcoin
    def to_btc(self):
        self.tab = Tab.BITCOIN
        self.widget = widgets.cryptos.Bitcoin(self)
        self.central_widget.addWidget(self.widget)
        self.central_widget.setCurrentWidget(self.widget)

    # change widget from x to ethereum
    def to_eth(self):
        self.tab = Tab.ETHEREUM
        self.widget = widgets.cryptos.Ethereum(self)
        self.central_widget.addWidget(self.widget)
        self.central_widget.setCurrentWidget(self.widget)

    # change widget from x to litecoin
    def to_ltc(self):
        self.tab = Tab.LITECOIN
        self.widget = widgets.cryptos.Litecoin(self)
        self.central_widget.addWidget(self.widget)
        self.central_widget.setCurrentWidget(self.widget)

    # toolbar
    def toolbar(self):
        toolbar = QtWidgets.QToolBar()
        toolbar.setIconSize(QtCore.QSize(32,32))
        self.addToolBar(toolbar)

        button_action = QtWidgets.QAction(QtGui.QIcon("../assets/parameters.png"), "Parameters", self)
        button_action.triggered.connect(self.to_param)
        toolbar.addAction(button_action)

        toolbar.addSeparator()

        button_action2 = QtWidgets.QAction(QtGui.QIcon("../assets/cryptobot.png"), "Assets Dashboard", self)
        button_action2.triggered.connect(self.to_dashboard)
        toolbar.addAction(button_action2)

        button_action3 = QtWidgets.QAction(QtGui.QIcon("../assets/btc.png"), "Bitcoin", self)
        button_action3.triggered.connect(self.to_btc)
        toolbar.addAction(button_action3)

        button_action4 = QtWidgets.QAction(QtGui.QIcon("../assets/eth.png"), "Ethereum", self)
        button_action4.triggered.connect(self.to_eth)
        toolbar.addAction(button_action4)

        button_action5 = QtWidgets.QAction(QtGui.QIcon("../assets/ltc.png"), "Litecoin", self)
        button_action5.triggered.connect(self.to_ltc)
        toolbar.addAction(button_action5)

        self.setStatusBar(QtWidgets.QStatusBar(self))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    with open("style/style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
    dashboard = MainWindow()
    dashboard.resize(param.window_x, param.window_y)
    dashboard.show()
    app.exec_()
