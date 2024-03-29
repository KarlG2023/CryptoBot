#!/usr/bin/env python3

import os
import random
import string

from poloniex import Poloniex
from PySide2 import QtGui, QtCore, QtWidgets

import api_request.account #pylint: disable=import-error

def getCredentials():
    key, ok = QtWidgets.QInputDialog.getText(None, "Enter your credentials", "Api Key?", QtWidgets.QLineEdit.Password)
    api_secret, ok2 = QtWidgets.QInputDialog.getText(None, "Enter your credentials", "Api Secret?", QtWidgets.QLineEdit.Password)
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

def log_UI():
    # comment the next 2 lines to remove log functionnalities
    api_credentials = getCredentials()
    poloniex_obj = log(api_credentials[0], api_credentials[1])
    return poloniex_obj
