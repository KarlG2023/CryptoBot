#!/usr/bin/env python3

import math
import os
import random
import string
import sys

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
        except Exception as e:
            print("Unexpected error:", e) #print as error message
            exit(84)

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("My Awesome App")

        label = QLabel("THIS IS AWESOME!!!")
        label.setAlignment(Qt.AlignCenter)

        self.setCentralWidget(label)

        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(16,16))
        self.addToolBar(toolbar)

        button_action = QAction(QIcon("bug.png"), "Your button", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.onMyToolBarButtonClick)
        button_action.setCheckable(True)
        toolbar.addAction(button_action)

        toolbar.addSeparator()

        button_action2 = QAction(QIcon("bug.png"), "Your button2", self)
        button_action2.setStatusTip("This is your button2")
        button_action2.triggered.connect(self.onMyToolBarButtonClick)
        button_action2.setCheckable(True)
        toolbar.addAction(button_action2)

        toolbar.addWidget(QLabel("Hello"))
        toolbar.addWidget(QCheckBox())

        self.setStatusBar(QStatusBar(self))


    def onMyToolBarButtonClick(self, s):
        print("click", s)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    api_credentials = getCredentials()
    log(api_credentials[0], api_credentials[1])

# API-KEY IK93HX6R-1RLQR66Q-ZA68OZD0-D1ADEV51
# SECRET 94a9667e060d10fc0cee29fe9b0e79ac7490acef8eb86a8105706beb6521757e40d57c033ca8d3f620010c5f539b442fb812fba2d24f4006454425c8132567a6