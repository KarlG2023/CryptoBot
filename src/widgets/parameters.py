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

        # candle size

        self.candle_label = QtWidgets.QLabel("candle length")
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
        
        self.b1.toggled.connect(lambda:self.btnstate(self.b1))
        self.b2.toggled.connect(lambda:self.btnstate(self.b2))
        self.b3.toggled.connect(lambda:self.btnstate(self.b3))
        layout.addWidget(self.b1, 1, 0)
        layout.addWidget(self.b2, 2, 0)
        layout.addWidget(self.b3, 3, 0)

        # window size

        self.resize_label = QtWidgets.QLabel("window size")
        self.resize_label.setStyleSheet("background-color: #e6e6e6;border-style: outset;border-width: 2px;border-radius: 10px;border-color: grey;padding: 6px;")
        self.resize_label.setAlignment(QtCore.Qt.AlignCenter)
        self.resize_label.setMaximumHeight(50)
        layout.addWidget(self.resize_label, 4, 0, 1, 2)

        self.b4 = QtWidgets.QCheckBox("780*700")
        if param.window_x == 780 and param.window_y == 700:
            self.b4.setChecked(True)
        else:
            self.b4.setChecked(False)
  		
        self.b5 = QtWidgets.QCheckBox("1280*720")
        if param.window_x == 1280 and param.window_y == 720:
            self.b5.setChecked(True)
        else:
            self.b5.setChecked(False)

        self.b6 = QtWidgets.QCheckBox("1610*990")
        if param.window_x == 1610 and param.window_y == 990:
            self.b6.setChecked(True)
        else:
            self.b6.setChecked(False)
        
        self.b4.toggled.connect(lambda:self.btnstate(self.b4))
        self.b5.toggled.connect(lambda:self.btnstate(self.b5))
        self.b6.toggled.connect(lambda:self.btnstate(self.b6))
        layout.addWidget(self.b4, 5, 0)
        layout.addWidget(self.b5, 6, 0)
        layout.addWidget(self.b6, 7, 0)

        self.setLayout(layout)
  
    def btnstate(self,b):
        if b.text() == "15 minutes":
            if b.isChecked() == True:
                param.candle_size = 900

        if b.text() == "4 hours":
            if b.isChecked() == True:
                param.candle_size = 14400
        
        if b.text() == "1 day":
            if b.isChecked() == True:
                param.candle_size = 86400
        
        if b.text() == "780*700":
            if b.isChecked() == True:
                param.window_x = 780
                param.window_y = 700

        if b.text() == "1280*720":
            if b.isChecked() == True:
                param.window_x = 1280
                param.window_y = 720
        
        if b.text() == "1610*990":
            if b.isChecked() == True:
                param.window_x = 1610
                param.window_y = 990
