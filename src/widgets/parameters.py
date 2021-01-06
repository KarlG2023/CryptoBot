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

class Param(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Param, self).__init__(parent)

        layout = QtWidgets.QHBoxLayout()
        self.b1 = QtWidgets.QCheckBox("900")
        self.b1.setChecked(True)
        self.b1.stateChanged.connect(lambda:self.btnstate(self.b1))
        layout.addWidget(self.b1)
  		
        self.b2 = QtWidgets.QCheckBox("14400")
        self.b2.toggled.connect(lambda:self.btnstate(self.b2))
  
        layout.addWidget(self.b2)
        self.setLayout(layout)
        self.setWindowTitle("checkbox demo")
  
    def btnstate(self,b):
        if b.text() == "900":
            if b.isChecked() == True:
                print(b.text()+" is selected")
            else:
                print(b.text()+" is deselected")
  				
        if b.text() == "14400":
            if b.isChecked() == True:
                print(b.text()+" is selected")
            else:
                print(b.text()+" is deselected")


        # layout = QtWidgets.QHBoxLayout()
        # self.label = QtWidgets.QLabel('param page!')
        # layout.addWidget(self.label)
        # self.setLayout(layout)
