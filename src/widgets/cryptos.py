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

import data.charts
import data.currencies

class Bitcoin(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Bitcoin, self).__init__(parent)
        layout = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel('Bitcoin page!')
        layout.addWidget(self.label)
        self.setLayout(layout)

class Ethereum(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Ethereum, self).__init__(parent)
        layout = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel('Ethereum page!')
        layout.addWidget(self.label)
        self.setLayout(layout)

class Litecoin(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Litecoin, self).__init__(parent)
        layout = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel('Litecoin page!')
        layout.addWidget(self.label)
        self.setLayout(layout)
