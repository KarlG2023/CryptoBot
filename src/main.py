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

def getCredentials():
    key, ok = QInputDialog.getText(None, "Enter your credentials", "Api Key?", QLineEdit.Password)
    api_secret, ok2 = QInputDialog.getText(None, "Enter your credentials", "Api Secret?", QLineEdit.Password)
    if ok and ok2 and key and api_secret:
        return key, api_secret

def log(api_key, api_secret):
        obj_poloniex = api_request.account.log(api_key, api_secret)
        try:
            api_request.account.get_balance(obj_poloniex) #print in dashboard
            return obj_poloniex
        except Exception as e:
            print("Unexpected error:", e) #print as error message
            exit(84)

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.log_UI()
        self.setWindowTitle("CyptoBot")

        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(32,32))
        self.addToolBar(toolbar)

        button_action = QAction(QIcon("../assets/parameters.png"), "Bot Configuration", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.paramClick)
        button_action.setCheckable(True)
        toolbar.addAction(button_action)

        toolbar.addSeparator()

        button_action2 = QAction(QIcon("../assets/cryptobot.png"), "Assets Dashboard", self)
        button_action2.setStatusTip("This is your button2")
        button_action2.triggered.connect(self.dashboardClick)
        button_action2.setCheckable(True)
        toolbar.addAction(button_action2)

        self.setStatusBar(QStatusBar(self))
        self.initUI()

    def log_UI(self):
        # comment the next 2 lines to remove log functionnalities
        # api_credentials = getCredentials()
        # self.poloniex_obj = log(api_credentials[0], api_credentials[1])
    
        # comment the next line for password feature
        self.poloniex_obj = log("IK93HX6R-1RLQR66Q-ZA68OZD0-D1ADEV51", "94a9667e060d10fc0cee29fe9b0e79ac7490acef8eb86a8105706beb6521757e40d57c033ca8d3f620010c5f539b442fb812fba2d24f4006454425c8132567a6")

    # called when dashboard button clicked
    def dashboardClick(self, s):
        print("want to see the dashboard", s)

    # called when param button clicked
    def paramClick(self, s):
        print("Want to see the param", s)

    # change timer to update data
    def initUI(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.Time)
        self.timer.start(1000)
        label = QLabel(time.strftime("%H:%M:%S ") + str(api_request.charts.get_ticker(self.poloniex_obj)['USDT_BTC']['last'])+" USDT_BTC")
        label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(label)

    def Time(self):
        if int(time.strftime("%S")) % 10 == 0:
            label = QLabel(time.strftime("%H:%M:%S ") + str(api_request.charts.get_ticker(self.poloniex_obj)['USDT_BTC']['last'])+" USDT_BTC")
            label.setAlignment(Qt.AlignCenter)
            self.setCentralWidget(label)
            # create database (json) in log and update database in another file and called here (see what data i need and create json table accordingly) 
            # start with one crypto

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dashboard = MainWindow()
    dashboard.resize(1920, 1080)
    dashboard.show()
    app.exec_()

# API-KEY IK93HX6R-1RLQR66Q-ZA68OZD0-D1ADEV51
# SECRET 94a9667e060d10fc0cee29fe9b0e79ac7490acef8eb86a8105706beb6521757e40d57c033ca8d3f620010c5f539b442fb812fba2d24f4006454425c8132567a6