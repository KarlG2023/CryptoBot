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
        self.widgets_update()
        if int(time.strftime("%S")) == 0:
            param.cryptobot.btc_update()
        if int(time.strftime("%S")) == 20:
            param.cryptobot.eth_update()
        if int(time.strftime("%S")) == 40:
            param.cryptobot.ltc_update()
        if int(time.strftime("%M")) % 1 == 0 and int(time.strftime("%S")) == 30:
            param.charts_json = data.charts.charts_json(param.poloniex_obj, param.candle_size)

    # update widgets data
    def widgets_update(self):
        self.central_widget.removeWidget(self.widget) # pas opti / créer tout les widgets et les updates en dehors du init
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
    dashboard.resize(1280, 720)
    dashboard.show()
    app.exec_()
