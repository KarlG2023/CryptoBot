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

import param #pylint: disable=import-error

class Param(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Param, self).__init__(parent)

        layout = QtWidgets.QGridLayout()

        # widget_1 = QtWidgets.QHBoxLayout()

        self.candle_label = QtWidgets.QLabel("Choose a candle length:")
        self.candle_label.setStyleSheet("background-color: #e6e6e6;border-style: outset;border-width: 2px;border-radius: 10px;border-color: grey;padding: 6px;")
        self.candle_label.setAlignment(QtCore.Qt.AlignCenter)
        self.candle_label.setMaximumHeight(50)
        layout.addWidget(self.candle_label, 0, 0, 1, 2)

        self.b1 = QtWidgets.QCheckBox("15 minutes")
        if param.candle_size == 900:
            self.b1.setChecked(True)
        else:
            self.b1.setChecked(False)
  		
        self.b2 = QtWidgets.QCheckBox("4 hours")
        if param.candle_size == 14400:
            self.b2.setChecked(True)
        else:
            self.b2.setChecked(False)

        self.b3 = QtWidgets.QCheckBox("1 day")
        if param.candle_size == 86400:
            self.b3.setChecked(True)
        else:
            self.b3.setChecked(False)
        
        self.b1.stateChanged.connect(lambda:self.btnstate(self.b1)) # why is it different ?
        self.b2.toggled.connect(lambda:self.btnstate(self.b2))
        self.b3.toggled.connect(lambda:self.btnstate(self.b3))
        layout.addWidget(self.b1, 1, 0)
        layout.addWidget(self.b2, 2, 0)
        layout.addWidget(self.b3, 3, 0)

        self.setLayout(layout)
  
    def btnstate(self,b):
        if b.text() == "15 minutes":
            if b.isChecked() == True:
                param.candle_size = 900
                print(b.text()+" is selected")

        if b.text() == "4 hours":
            if b.isChecked() == True:
                param.candle_size = 14400
                print(b.text()+" is selected")
        
        if b.text() == "1 day":
            if b.isChecked() == True:
                param.candle_size = 86400
                print(b.text()+" is selected")


        # layout = QtWidgets.QHBoxLayout()
        # self.label = QtWidgets.QLabel('param page!')
        # layout.addWidget(self.label)
        # self.setLayout(layout)
