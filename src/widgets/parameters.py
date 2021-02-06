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

        # candle size settings
        self.candle_label = QtWidgets.QLabel("candle length")
        self.candle_label.setStyleSheet("background-color: #e6e6e6;border-style: outset;border-width: 2px;border-radius: 10px;border-color: grey;padding: 6px;")
        self.candle_label.setAlignment(QtCore.Qt.AlignCenter)
        self.candle_label.setMaximumHeight(50)
        layout.addWidget(self.candle_label, 0, 0, 1, 3)

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

        # window size settings
        self.resize_label = QtWidgets.QLabel("window size")
        self.resize_label.setStyleSheet("background-color: #e6e6e6;border-style: outset;border-width: 2px;border-radius: 10px;border-color: grey;padding: 6px;")
        self.resize_label.setAlignment(QtCore.Qt.AlignCenter)
        self.resize_label.setMaximumHeight(50)
        layout.addWidget(self.resize_label, 4, 0, 1, 3)

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

        # algo choice settings
        self.algo_label = QtWidgets.QLabel("algorythms")
        self.algo_label.setStyleSheet("background-color: #e6e6e6;border-style: outset;border-width: 2px;border-radius: 10px;border-color: grey;padding: 6px;")
        self.algo_label.setAlignment(QtCore.Qt.AlignCenter)
        self.algo_label.setMaximumHeight(50)
        layout.addWidget(self.algo_label, 8, 0, 1, 3)

        self.a1 = QtWidgets.QCheckBox("Relative Strength Index (14)")
        if param.rsi == 1:
            self.a1.setChecked(True)
        else:
            self.a1.setChecked(False)
  		
        self.a2 = QtWidgets.QCheckBox("Stochastic (14,3,3)")
        if param.stochastique == 1:
            self.a2.setChecked(True)
        else:
            self.a2.setChecked(False)

        self.a3 = QtWidgets.QCheckBox("Commodity Channel Index (20)")
        if param.cci == 1:
            self.a3.setChecked(True)
        else:
            self.a3.setChecked(False)
        
        self.a4 = QtWidgets.QCheckBox("Average Directional Index (14)")
        if param.adi == 1:
            self.a4.setChecked(True)
        else:
            self.a4.setChecked(False)
        
        self.a5 = QtWidgets.QCheckBox("Awesome Oscillator")
        if param.awesome == 1:
            self.a5.setChecked(True)
        else:
            self.a5.setChecked(False)
        
        self.a6 = QtWidgets.QCheckBox("Momentum (10)")
        if param.momentum == 1:
            self.a6.setChecked(True)
        else:
            self.a6.setChecked(False)
        
        self.a7 = QtWidgets.QCheckBox("MACD Level (12, 26)")
        if param.macd == 1:
            self.a7.setChecked(True)
        else:
            self.a7.setChecked(False)
        
        self.a8 = QtWidgets.QCheckBox("Stochastic RSI Fast (3, 3, 14, 14)")
        if param.stochrsi == 1:
            self.a8.setChecked(True)
        else:
            self.a8.setChecked(False)
        
        self.a9 = QtWidgets.QCheckBox("Bull Bear Power")
        if param.bullbear == 1:
            self.a9.setChecked(True)
        else:
            self.a9.setChecked(False)
        
        self.a10 = QtWidgets.QCheckBox("Exponential Moving Average (5)")
        if param.ema5 == 1:
            self.a10.setChecked(True)
        else:
            self.a10.setChecked(False)
        
        self.a11 = QtWidgets.QCheckBox("Exponential Moving Average (10)")
        if param.ema10 == 1:
            self.a11.setChecked(True)
        else:
            self.a11.setChecked(False)
        
        self.a12 = QtWidgets.QCheckBox("Exponential Moving Average (20)")
        if param.ema20 == 1:
            self.a12.setChecked(True)
        else:
            self.a12.setChecked(False)
        
        self.a13 = QtWidgets.QCheckBox("Simple Moving Average (5)")
        if param.sma5 == 1:
            self.a13.setChecked(True)
        else:
            self.a13.setChecked(False)
        
        self.a14 = QtWidgets.QCheckBox("Simple Moving Average (10)")
        if param.sma10 == 1:
            self.a14.setChecked(True)
        else:
            self.a14.setChecked(False)

        self.a15 = QtWidgets.QCheckBox("Simple Moving Average (20)")
        if param.sma20 == 1:
            self.a15.setChecked(True)
        else:
            self.a15.setChecked(False)
        
        self.a1.toggled.connect(lambda:self.btnstate(self.a1))
        self.a2.toggled.connect(lambda:self.btnstate(self.a2))
        self.a3.toggled.connect(lambda:self.btnstate(self.a3))
        self.a4.toggled.connect(lambda:self.btnstate(self.a4))
        self.a5.toggled.connect(lambda:self.btnstate(self.a5))
        self.a6.toggled.connect(lambda:self.btnstate(self.a6))
        self.a7.toggled.connect(lambda:self.btnstate(self.a7))
        self.a8.toggled.connect(lambda:self.btnstate(self.a8))
        self.a9.toggled.connect(lambda:self.btnstate(self.a9))
        self.a10.toggled.connect(lambda:self.btnstate(self.a10))
        self.a11.toggled.connect(lambda:self.btnstate(self.a11))
        self.a12.toggled.connect(lambda:self.btnstate(self.a12))
        self.a13.toggled.connect(lambda:self.btnstate(self.a13))
        self.a14.toggled.connect(lambda:self.btnstate(self.a14))
        self.a15.toggled.connect(lambda:self.btnstate(self.a15))
        layout.addWidget(self.a1, 9, 0)
        layout.addWidget(self.a2, 10, 0)
        layout.addWidget(self.a3, 11, 0)
        layout.addWidget(self.a4, 12, 0)
        layout.addWidget(self.a5, 13, 0)
        layout.addWidget(self.a6, 9, 1)
        layout.addWidget(self.a7, 10, 1)
        layout.addWidget(self.a8, 11, 1)
        layout.addWidget(self.a9, 12, 1)
        layout.addWidget(self.a10, 13, 1)
        layout.addWidget(self.a11, 9, 2)
        layout.addWidget(self.a12, 10, 2)
        layout.addWidget(self.a13, 11, 2)
        layout.addWidget(self.a14, 12, 2)
        layout.addWidget(self.a15, 13, 2)

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
        
        if b.text() == "Relative Strength Index (14)":
            if b.isChecked() == True:
                param.rsi = 1
            else:
                param.rsi = 0

        if b.text() == "Stochastic (14,3,3)":
            if b.isChecked() == True:
                param.stochastique = 1
            else:
                param.stochastique = 0
        
        if b.text() == "Commodity Channel Index (20)":
            if b.isChecked() == True:
                param.cci = 1
            else:
                param.cci = 0
        
        if b.text() == "Average Directional Index (14)":
            if b.isChecked() == True:
                param.adi = 1
            else:
                param.adi = 0
        
        if b.text() == "Awesome Oscillator":
            if b.isChecked() == True:
                param.awesome = 1
            else:
                param.awesome = 0
        
        if b.text() == "Momentum (10)":
            if b.isChecked() == True:
                param.momentum = 1
            else:
                param.momentum = 0

        if b.text() == "MACD Level (12, 26)":
            if b.isChecked() == True:
                param.macd = 1
            else:
                param.macd = 0
        
        if b.text() == "Stochastic RSI Fast (3, 3, 14, 14)":
            if b.isChecked() == True:
                param.stochrsi = 1
            else:
                param.stochrsi = 0
        
        if b.text() == "Bull Bear Power":
            if b.isChecked() == True:
                param.bullbear = 1
            else:
                param.bullbear = 0
        
        if b.text() == "Exponential Moving Average (5)":
            if b.isChecked() == True:
                param.ema5 = 1
            else:
                param.ema5 = 0
        
        if b.text() == "Exponential Moving Average (10)":
            if b.isChecked() == True:
                param.ema10 = 1
            else:
                param.ema10 = 0

        if b.text() == "Exponential Moving Average (20)":
            if b.isChecked() == True:
                param.ema20 = 1
            else:
                param.ema20 = 0
        
        if b.text() == "Simple Moving Average (5)":
            if b.isChecked() == True:
                param.sma5 = 1
            else:
                param.sma5 = 0
        
        if b.text() == "Simple Moving Average (10)":
            if b.isChecked() == True:
                param.sma10 = 1
            else:
                param.sma10 = 0
        
        if b.text() == "Simple Moving Average (20)":
            if b.isChecked() == True:
                param.sma20 = 1
            else:
                param.sma20 = 0
