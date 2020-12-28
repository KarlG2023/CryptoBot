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

import data.charts
import data.currencies

def getCredentials():
    key, ok = QInputDialog.getText(None, "Enter your credentials", "Api Key?", QLineEdit.Password)
    api_secret, ok2 = QInputDialog.getText(None, "Enter your credentials", "Api Secret?", QLineEdit.Password)
    if ok and ok2 and key and api_secret:
        return key, api_secret

def log(api_key, api_secret):
        obj_poloniex = api_request.account.log(api_key, api_secret)
        try:
            api_request.account.get_balance(obj_poloniex) # simple call to the api to see if credetials are ok
            return obj_poloniex
        except Exception as e:
            print("Unexpected error:", e)
            exit(84)

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.poloniex_obj = self.log_UI()

        # self.currencies_json = data.currencies.currencies_json(self.poloniex_obj)
        self.charts_json = data.charts.charts_json(self.poloniex_obj)

        self.setWindowTitle("CyptoBot")

        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(32,32))
        self.addToolBar(toolbar)

        button_action = QAction(QIcon("../assets/parameters.png"), "Bot Configuration", self)
        button_action.setStatusTip("Bot Configuration")
        button_action.triggered.connect(self.paramClick)
        button_action.setCheckable(True)
        toolbar.addAction(button_action)

        toolbar.addSeparator()

        button_action2 = QAction(QIcon("../assets/cryptobot.png"), "Assets Dashboard", self)
        button_action2.setStatusTip("Assets Dashboard")
        button_action2.triggered.connect(self.dashboardClick)
        button_action2.setCheckable(True)
        toolbar.addAction(button_action2)

        self.setStatusBar(QStatusBar(self))
        self.initUI()

    def log_UI(self):
        # comment the next 2 lines to remove log functionnalities
        # api_credentials = getCredentials()
        # poloniex_obj = log(api_credentials[0], api_credentials[1])
    
        # comment the next line for password feature
        poloniex_obj = log("4Z69MO3Y-JT0EDZS8-RG86RCYZ-FOFNHGTH", "a34c54261425e235a1ea3b4d87de52cabedbd115169ac146cc17a00d0765847b0f005ac02cb877f822f9c82a10680ac882f57eab87132a10c2f16e8fa8d4c63e")

        return poloniex_obj

    # called when dashboard button clicked
    def dashboardClick(self, s):
        print("want to see the dashboard", s)

    # called when param button clicked
    def paramClick(self, s):
        print("Want to see the param", s)

    # create and start time to perform actions on a cycle of 1000ms (rename?)
    def initUI(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.Time)
        self.timer.start(1000)

    # update charts data here
    def Time(self):
        label = QLabel(time.strftime("%H:%M:%S "))
        label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(label)
        if int(time.strftime("%S")) % 10 == 0:
            self.charts_json.print_data()
            # self.currencies_json.print_data()
            # do some shit each %S/%M/%H seconds/minutes/hours (do it on a thread pls)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dashboard = MainWindow()
    dashboard.resize(1920, 1080)
    dashboard.show()
    app.exec_()

# API-KEY 4Z69MO3Y-JT0EDZS8-RG86RCYZ-FOFNHGTH
# SECRET a34c54261425e235a1ea3b4d87de52cabedbd115169ac146cc17a00d0765847b0f005ac02cb877f822f9c82a10680ac882f57eab87132a10c2f16e8fa8d4c63e