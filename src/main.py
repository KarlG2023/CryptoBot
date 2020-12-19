#!/usr/bin/env python3

import math
import os
import random
import string
import sys

# sudo apt install libxcb-xinerama0/poloniex/PySide2
from poloniex import Poloniex
from PySide2.QtWidgets import (QApplication, QInputDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget)
from PySide2.QtCore import Slot, Qt

import api_request.account
import api_request.charts
import api_request.trades

class MyWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.api_key = QLabel("api_key:")
        self.api_key.setAlignment(Qt.AlignCenter)
        self.text_key = QLineEdit(self)
        self.text_key.move(200, 500)
        self.api_secret = QLabel("api_secret:")
        self.api_secret.setAlignment(Qt.AlignCenter)
        self.text_secret = QLineEdit(self)
        self.text_secret.move(400, 500)
        self.button = QPushButton("Login")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.api_key)
        self.layout.addWidget(self.text_key)
        self.layout.addWidget(self.api_secret)
        self.layout.addWidget(self.text_secret)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        # Connecting the signal
        self.button.clicked.connect(self.log)

    @Slot()
    def log(self):
        # obj_poloniex = api_request.account.log(api_key, api_secret)
        # api_request.account.get_help(obj_poloniex)
        print("logged")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec_())

# API-KEY IK93HX6R-1RLQR66Q-ZA68OZD0-D1ADEV51
# SECRET 94a9667e060d10fc0cee29fe9b0e79ac7490acef8eb86a8105706beb6521757e40d57c033ca8d3f620010c5f539b442fb812fba2d24f4006454425c8132567a6